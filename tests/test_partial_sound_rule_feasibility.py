#!/usr/bin/env python3
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_partial_sound_rule_feasibility import inspect_word
from scripts.fetch_egerton_comparator import select_comparator


class RuleFeasibilityGuards(unittest.TestCase):
    def test_no_unknown_deletion_or_overlapping_offsets(self):
        word='ytoail'
        result=inspect_word(word)
        units=result['units']
        self.assertEqual(''.join(u['raw'] for u in units),word)
        self.assertEqual(units[0]['start'],0)
        self.assertEqual(units[-1]['end'],len(word))
        for left,right in zip(units,units[1:]):
            self.assertEqual(left['end'],right['start'])
        self.assertEqual(result['unmapped_characters'],['i','l','t'])
        self.assertIsNone(result['plaintext'])

    def test_published_clusters_not_split_into_overlapping_characters(self):
        units=inspect_word('shiin')['units']
        self.assertEqual([u['raw'] for u in units],['sh','iin'])
        self.assertEqual(units[0]['proposed_sounds'],['kʰ','x','tʃ'])
        self.assertEqual(units[1]['proposed_sounds'],['ur'])

    def test_f41v_variants_not_normalized_to_fit_a_name(self):
        a=inspect_word('keeredal');b=inspect_word('keerodal')
        self.assertNotEqual(a['units'][4]['proposed_sounds'],
                            b['units'][4]['proposed_sounds'])
        for r in (a,b):
            self.assertEqual(r['unmapped_characters'],['l'])
            self.assertTrue(r['positions_with_multiple_proposals'])
            self.assertTrue(r['repeated_e_duration_not_decided'])
            self.assertIsNone(r['plaintext'])

    def test_complete_symbol_coverage_never_means_semantic_validation(self):
        r=inspect_word('dam')
        self.assertEqual(r['unmapped_characters'],[])
        self.assertTrue(r['unresolved_context_positions'])
        self.assertTrue(r['positions_with_multiple_proposals'])
        self.assertEqual(r['status'],'UNVALIDATED_PARTIAL_SOUND_PROJECTION')
        self.assertIsNone(r['plaintext'])

    def test_historical_folio_exact_match_and_ambiguity_rejected(self):
        def canvas(label,num):
            return {'id':str(num),'label':{'en':[label]},'width':100,'height':200,
                    'items':[{'items':[{'body':{'service':[{
                        '@id':f'https://bl.digirati.io/images/ark:/81055/{num}'}]}}]}]}
        m={'items':[canvas('f.127v',1),canvas('f.27v',2)]}
        self.assertEqual(select_comparator(m)['canvas'],'2')
        m['items'].append(canvas('f.27v',3))
        with self.assertRaises(ValueError):
            select_comparator(m)


if __name__=='__main__':
    unittest.main()

