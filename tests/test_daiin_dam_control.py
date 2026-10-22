import itertools
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.audit_daiin_dam_control import expected,pair_count,holm
class PairControl(unittest.TestCase):
    def test_exact_expectation_against_exhaustive_multiset_permutations(self):
        for words in [('daiin','dam'),('daiin','daiin','dam','x'),('dam','dam','daiin','x')]:
            permutations=list(itertools.permutations(words))
            self.assertAlmostEqual(expected(words),sum(map(pair_count,permutations))/len(permutations))
    def test_direction_and_boundaries(self):
        self.assertEqual(pair_count(['dam','daiin']),0)
        self.assertEqual(pair_count(['daiin','dam','daiin','dam']),2)
        self.assertEqual(expected([]),0)
    def test_holm_monotone_original_order(self):
        self.assertEqual(holm([.02,.001,.8,.01]),[.04,.004,.8,.03])
if __name__=='__main__':unittest.main()
