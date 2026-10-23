#!/usr/bin/env python3
"""Controls for train-only segmentation and boundary prediction."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from analyze_subword_boundary import BPE, Predictor, pairs, score, shuffled, synthetic_checks, GRID, UNK

class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.train=[{'group':'train','tokens':['edge',a,b,'edge']} for a in ('aba','aca') for b in ('xx','yy') for _ in range(10)]
        self.dev=[{**r,'group':'development'} for r in self.train]

    def test_known_positive_and_negative(self):
        result=synthetic_checks()
        self.assertGreater(result['positive']['gain_bits'],.5)
        self.assertEqual(result['negative']['gain_bits'],0)

    def test_no_smoothing_gain_with_unequal_context_sizes(self):
        train=self.train+[r for r in self.train if r['tokens'][1]=='aca']*3
        model=Predictor(train,self.dev,BPE(train))
        self.assertLess(abs(score(model,self.dev)['gain_bits']),1e-10)

    def test_segmentation_reconstructs_and_freezes_on_unseen_letters(self):
        bpe=BPE(self.train)
        original=(list(bpe.merges),set(bpe.units),set(bpe.alphabet))
        for word in ('abaca','edge','xyx'):
            self.assertEqual(''.join(bpe.encode(word)),word)
        self.assertIn(UNK,bpe.encode('Ω'))
        self.assertEqual(original,(bpe.merges,bpe.units,bpe.alphabet))

    def test_training_order_does_not_change_merges(self):
        self.assertEqual(BPE(self.train).merges,BPE(list(reversed(self.train))).merges)

    def test_normalized_at_every_weight_seen_and_unseen(self):
        bpe=BPE(self.train);m=Predictor(self.train,self.dev,bpe)
        for context in list(m.totals)+['absent']:
            for weight in GRID:
                self.assertAlmostEqual(sum(m.probability(context,b,weight) for b in bpe.units),1,places=12)

    def test_excludes_extremes_short_lines_and_cross_line_pairs(self):
        bpe=BPE(self.train)
        rows=[{'group':'a','tokens':['aba','xx']},{'group':'b','tokens':['aca','yy','xx']},
              {'group':'c','tokens':['edge','aba','yy','edge']}]
        self.assertEqual(list(pairs(rows,bpe)),[('c',bpe.encode('aba')[-1],bpe.encode('yy')[0])])

    def test_shuffle_keeps_originals_endpoints_and_inventory(self):
        rows=[{'group':'a','tokens':['left','a','b','c','right']}, {'group':'b','tokens':['one']}]
        control=shuffled(rows,3)
        self.assertEqual(rows[0]['tokens'],['left','a','b','c','right'])
        for row,changed in zip(rows,control):
            self.assertEqual(row['tokens'][0],changed['tokens'][0])
            self.assertEqual(row['tokens'][-1],changed['tokens'][-1])
            self.assertCountEqual(row['tokens'],changed['tokens'])

if __name__=='__main__':
    unittest.main()
