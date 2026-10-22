#!/usr/bin/env python3
import copy
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_decipherment_anchor_concordances import find_targets
from scripts.fetch_decipherment_anchor_images import select_images
from scripts.ivtff_lossless import lex


def row(identifier, body, locus='P0'):
    return {'id':identifier,'folio':identifier.split('.')[0], 'locus':locus,
            'source_line':1,'body':body,'payload':lex(body)}


def canvas(label, number):
    return {'id':f'canvas-{number}','label':{'none':[label]},
            'items':[{'items':[{'body':{
                'id':f'https://collections.library.yale.edu/iiif/2/{number}/full/full/0/default.jpg',
                'width':100,'height':200}}]}]}


class AnchorEvidenceTests(unittest.TestCase):
    def test_exact_tokens_and_occurrences_not_substrings_or_lines(self):
        d=find_targets([row('f1r.1','adam.dam.dame.dam')],'split')
        self.assertEqual(d['dam']['occurrences'],2)
        self.assertEqual([m['token_index_zero_based'] for m in d['dam']['matches']],[1,3])

    def test_uncertain_space_changes_view_without_changing_source(self):
        r=row('f65r.1','otaim,dam.alam','Lp')
        a=find_targets([r],'split');b=find_targets([r],'join')
        self.assertEqual((a['otaim']['occurrences'],a['dam']['occurrences'],a['alam']['occurrences']),(1,1,1))
        self.assertEqual((b['otaim']['occurrences'],b['dam']['occurrences'],b['otaimdam']['occurrences']),(0,0,1))
        self.assertEqual(r['body'],'otaim,dam.alam')

    def test_primary_alternative_remains_explicitly_conditional(self):
        d=find_targets([row('f41v.1','keer[e:o]dal','Lp')],'split')
        self.assertEqual(d['keeredal']['occurrences'],1)
        self.assertEqual(d['keerodal']['occurrences'],0)

    def test_subdivided_page_and_locus_retained(self):
        d=find_targets([row('f67r1.1','dam','Ri')],'split')['dam']
        self.assertEqual(d['folios'],['f67r1'])
        self.assertEqual(d['locus_counts'],{'Ri':1})

    def test_unresolved_markup_rejected(self):
        with self.assertRaises(ValueError):
            find_targets([row('f1r.1','[dam')],'split')

    def test_canvas_selection_uses_exact_labels_not_order_or_substrings(self):
        fixture={'items':[canvas('12r',9),canvas('65r',3),
                          canvas('2v',8),canvas('2r',1),canvas('41v',2)]}
        self.assertEqual([x['canvas'] for x in select_images(fixture)],
                         ['canvas-1','canvas-2','canvas-3'])
        duplicate=copy.deepcopy(fixture)
        duplicate['items'].append(canvas('2r',4))
        with self.assertRaises(ValueError):
            select_images(duplicate)
        missing={'items':[canvas('2r',1),canvas('41v',2)]}
        with self.assertRaises(ValueError):
            select_images(missing)


if __name__ == '__main__':
    unittest.main()

