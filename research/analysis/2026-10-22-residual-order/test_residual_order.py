from collections import Counter
import unittest
from residual_order import Model,UNK,shuffled,is_test
from prepare_inputs import pg_body
class ProbabilityContracts(unittest.TestCase):
 def setUp(self):
  self.rows=[{'group':'f1','id':'a','tokens':['daiin','dam','dain','dam']},
             {'group':'f2','id':'b','tokens':['dain','dam','daiin','x']}]
 def test_normalization_seen_and_unseen_contexts(self):
  for cap in (None,2):
   model=Model(self.rows,cap)
   for previous in ('daiin','dain','unknown','aa','x'):
    all_probs=[model.probabilities(previous,w) for w in model.events]
    for i in range(4):self.assertAlmostEqual(sum(p[i] for p in all_probs),1.0,places=12)
 def test_unknown_targets_collapse_to_single_event(self):
  m=Model(self.rows,2)
  self.assertEqual(m.probabilities('daiin','absent'),m.probabilities('daiin',UNK))
 def test_unseen_identity_backs_off_to_edge_length(self):
  m=Model(self.rows)
  p=m.probabilities('zzzz','dam');self.assertEqual(p[3],p[2])
 def test_shuffle_preserves_records_and_multisets(self):
  out=shuffled(self.rows,17)
  self.assertEqual([r['id'] for r in out],['a','b'])
  for a,b in zip(self.rows,out):self.assertEqual(Counter(a['tokens']),Counter(b['tokens']))
 def test_stable_vocabulary_under_shuffle_ties(self):
  self.assertEqual(Model(self.rows,2).vocab,Model(shuffled(self.rows,17),2).vocab)
 def test_physical_leaf_grouping_does_not_depend_on_side(self):
  import re
  groups=[re.match(r'f\d+',p)[0] for p in ('f89r1','f89v2','f89r2')]
  self.assertEqual(len(set(groups)),1);self.assertEqual(len({is_test(g) for g in groups}),1)
 def test_gutenberg_offsets_apply_after_start_anchor(self):
  self.assertEqual(pg_body(b'header\nANCHOR abc\n*** END OF X\nfooter','ANCHOR'),'ANCHOR abc\n')
  with self.assertRaises(ValueError):pg_body(b'no markers','ANCHOR')
if __name__=='__main__':unittest.main()
