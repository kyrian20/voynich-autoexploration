import itertools
from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_am_lexical_contributions import decompose


class LexicalTests(unittest.TestCase):
    def test_enumerated_expectation(self):
        for size in range(1, 6):
            for line in itertools.product(('a', 'xam', 'yam'), repeat=size):
                result = decompose([line])
                permutations = list(itertools.permutations(line))
                expected = Fraction(sum(p[-1].endswith('am') for p in permutations), len(permutations))
                self.assertEqual(Fraction(result['expected_exact']), expected)
                for row in result['types']:
                    e = Fraction(sum(p[-1] == row['word'] for p in permutations), len(permutations))
                    self.assertEqual(Fraction(row['expected_exact']), e)
                    remaining = Fraction(sum(p[-1].endswith('am') and p[-1] != row['word']
                                             for p in permutations), len(permutations))
                    self.assertEqual(Fraction(row['remaining_expected_exact']), remaining)

    def test_additive_and_feature_exclusion(self):
        lines = [['a', 'xam', 'yam'], ['b', 'xam'], ['yam']]
        before = [line[:] for line in lines]
        result = decompose(lines)
        self.assertEqual(lines, before)
        self.assertEqual(result['observed'], 3)
        self.assertEqual(result['expected_exact'], '13/6')
        for row in result['types']:
            feature = lambda w: w.endswith('am') and w != row['word']
            e = sum((Fraction(sum(map(feature, line)), len(line)) for line in lines), Fraction())
            o = sum(feature(line[-1]) for line in lines)
            self.assertEqual(row['remaining_expected_exact'], str(e))
            self.assertEqual(row['remaining_observed'], o)

    def test_single_type_and_zero_observed(self):
        result = decompose([['xam', 'a']])
        self.assertEqual(result['types'][0]['observed'], 0)
        self.assertIsNone(result['types'][0]['remaining_ratio'])
        self.assertFalse(result['all_single_type_feature_exclusions_above_one'])

    def test_no_feature(self):
        self.assertEqual(decompose([['a']])['types'], [])

    def test_empty_rejected(self):
        for lines in ([], [[]]):
            with self.assertRaises(ValueError):
                decompose(lines)


if __name__ == '__main__':
    unittest.main()
