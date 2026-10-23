from collections import Counter
from fractions import Fraction
import itertools
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_predecessor_opportunities import CONTROLS, key, opportunity, summarize


class OpportunityTests(unittest.TestCase):
    def test_enumerated_controls(self):
        alphabet = ('aba', 'aca', 'aa', 'bb')
        for n in range(1, 5):
            for interior in itertools.product(alphabet, repeat=n):
                words = ('first',) + interior + ('xam',)
                for control in CONTROLS:
                    valid = [words[:1]+p+words[-1:] for p in itertools.permutations(interior)
                             if all(key(a, control) == key(b, control) for a, b in zip(interior, p))]
                    for row in valid:
                        self.assertEqual(Counter(row), Counter(words))
                        self.assertEqual((row[0], row[-1]), (words[0], words[-1]))
                    expected = Fraction(sum(row[-2] != words[-2] for row in valid), len(valid))
                    actual = opportunity(words, control)
                    self.assertEqual(Fraction(actual['change_probability_exact']), expected)
                    self.assertEqual(actual['variable'], expected > 0)

    def test_repeated_candidates(self):
        result = opportunity(['first', 'aba', 'aca', 'aba', 'xam'], 'edges_length')
        self.assertEqual(result['candidates'], {'aba': 2, 'aca': 1})
        self.assertEqual(result['change_probability_exact'], '1/3')

    def test_short_lines_fixed(self):
        for words in (['a'], ['a', 'xam'], ['a', 'b', 'xam']):
            self.assertFalse(opportunity(words, 'interior')['variable'])

    def test_partition_and_no_mutation(self):
        rows = [('a', ['first', 'aba', 'aca', 'xam']), ('b', ['first', 'y'])]
        before = repr(rows)
        result = summarize(rows, 'edges_length')
        self.assertEqual(result['am_final']['variable_lines'], 1)
        self.assertEqual(result['other_final']['lines'], 1)
        self.assertEqual(repr(rows), before)

    def test_invalid(self):
        for words in ([], ['']):
            with self.assertRaises(ValueError):
                opportunity(words, 'interior')
        with self.assertRaises(ValueError):
            opportunity(['x'], 'unknown')


if __name__ == '__main__':
    unittest.main()
