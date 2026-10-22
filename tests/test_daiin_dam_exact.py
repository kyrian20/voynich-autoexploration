import collections
from fractions import Fraction
import itertools
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.audit_daiin_dam_exact import distribution,pair_count,convolve
class ExactNull(unittest.TestCase):
    def test_all_category_multisets_through_length_six(self):
        for n in range(7):
            groups=collections.defaultdict(collections.Counter)
            for words in itertools.product(('daiin','dam','x'),repeat=n):
                key=(words.count('daiin'),words.count('dam'),words.count('x'))
                groups[key][pair_count(words)]+=1
            for (a,b,o),counts in groups.items():
                words=['daiin']*a+['dam']*b+['x']*o
                total=sum(counts.values())
                self.assertEqual(distribution(words),{k:Fraction(v,total) for k,v in counts.items()})
    def test_convolution_of_two_independent_short_lines(self):
        d=distribution(['daiin','dam'])
        self.assertEqual(convolve(d,d),{0:Fraction(1,4),1:Fraction(1,2),2:Fraction(1,4)})
if __name__=='__main__':unittest.main()
