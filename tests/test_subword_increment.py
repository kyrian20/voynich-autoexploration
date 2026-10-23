import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from analyze_subword_increment import checks, constrained, CharacterContext, BPE, pairs

class IncrementTests(unittest.TestCase):
    def test_synthetic_gates(self):
        result = checks()['increment']
        self.assertGreater(result['positive'], .5)
        self.assertLess(abs(result['negative']), 1e-10)

    def test_targets_and_unknown_context(self):
        train = [{'group':'a','tokens':['edge','aba','xx','edge']}]*50
        bpe = BPE(train)
        rows = train + [{'group':'new','tokens':['edge','ab!','xyz','edge']}]
        coarse = CharacterContext(bpe)
        self.assertEqual([(g,b) for g,_,b in pairs(rows,bpe)],[(g,b) for g,_,b in pairs(rows,coarse)])
        self.assertEqual(coarse.encode('ab!')[-1], '<UNKNOWN_CHAR>')

    def test_support_counts_word_changes_not_duplicate_slots(self):
        rows = [{'group':'x','tokens':['edge','aba','aca','aba','zz','edge']}]
        output,support = constrained(rows,11)
        self.assertEqual(support['interior_positions'],4)
        self.assertEqual(support['eligible_positions'],3)
        self.assertLessEqual(support['changed_positions'],3)
        self.assertEqual(output,constrained(rows,11)[0])
        _,none = constrained([{'group':'x','tokens':['edge','aba','aba','edge']}],11)
        self.assertEqual(none['eligible_positions'],0)

if __name__ == '__main__':
    unittest.main()
