import itertools
from fractions import Fraction
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_exp173_line_null import expectation


class ExactControl(unittest.TestCase):
    def test_exhaustive_joint_orders(self):
        lines = [['yam', 'x'], ['a', 'b', 'c', 'd', 'e', 'xxam']]
        for feature, end, expected in [(lambda w: w.endswith('am'), -1, Fraction(2, 3)),
                                        (lambda w: w.startswith('y'), 0, Fraction(1, 2))]:
            total = count = 0
            for a, b in itertools.product(*(itertools.permutations(x) for x in lines)):
                total += feature(a[end]) + feature(b[end])
                count += 1
            self.assertEqual(Fraction(total, count), expected)
            self.assertEqual(Fraction(expectation(lines, feature, end)['expected_within_line_fraction']), expected)

    def test_singleton_is_fixed(self):
        r = expectation([['am']], lambda w: w.endswith('am'), -1)
        self.assertEqual((r['observed'], r['expected_within_line'], r['ratio_within_line']), (1, 1, 1))

    def test_zero_feature(self):
        self.assertIsNone(expectation([['x', 'z']], lambda w: w.endswith('am'), -1)['ratio_within_line'])

    def test_reject_empty(self):
        for lines in ([], [[]]):
            with self.assertRaises(ValueError):
                expectation(lines, lambda w: True, 0)


if __name__ == '__main__':
    unittest.main()
