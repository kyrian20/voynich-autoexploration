"""Compare category counting to independent enumeration of whole-token permutations."""
import collections
from fractions import Fraction
import itertools
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.audit_constrained_pair import CONTROLS,row_distribution,stratum,moments
class ConditionalNull(unittest.TestCase):
    def test_whole_token_permutations(self):
        examples=[('daiin','dam'),('daiin','dain','dam','x'),
                  ('dam','daiin','dam','daiin','dain'),('x','dam','daiin','dan','dam','y')]
        for words in examples:
            for control in CONTROLS:
                with self.subTest(words=words,control=control):
                    keys=[stratum(w,i,len(words),control) for i,w in enumerate(words)]
                    counts=collections.Counter()
                    for order in itertools.permutations(range(len(words))):
                        if any(keys[source]!=keys[destination] for destination,source in enumerate(order)):continue
                        permutation=tuple(words[source] for source in order)
                        # Deliberately use direct consecutive tuple counting, not production pair_count.
                        count=list(zip(permutation,permutation[1:])).count(('daiin','dam'))
                        counts[count]+=1
                    total=sum(counts.values())
                    expected={k:Fraction(v,total) for k,v in counts.items()}
                    self.assertEqual(row_distribution(words,control)[0],expected)
    def test_degenerate_control_not_treated_as_discriminating(self):
        dist,_=row_distribution(['daiin','dam'],'fixed_endpoints')
        self.assertEqual(dist,{1:Fraction(1)})
        self.assertEqual(moments(dist)[1],0)
    def test_neutral_and_planted_enrichment_cases(self):
        dist,_=row_distribution(['daiin','dam','x','daiin','dam'],'same_initial')
        self.assertEqual(sum(dist.values()),1)
        self.assertGreater(moments(dist)[1],0)
        with self.assertRaises(ValueError):row_distribution(['daiin','dam'],'unregistered')
if __name__=='__main__':unittest.main()
