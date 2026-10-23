from collections import Counter
from fractions import Fraction
import itertools
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_folio_context_control import analyze, group, signature


class FolioTests(unittest.TestCase):
    def test_enumerated_multiline_control(self):
        original = [('f1r.1', ['first', 'aba', 'aca', 'xam']),
                    ('f1v.1', ['open', 'ada', 'aca', 'last'])]
        slots = [(i, j) for i, (_, words) in enumerate(original) for j in range(1, len(words)-1)]
        inventory = [original[i][1][j] for i, j in slots]
        signatures = [signature(w) for w in inventory]
        changes = Counter()
        valid = 0
        for perm in itertools.permutations(inventory):
            if [signature(w) for w in perm] != signatures:
                continue
            rows = [(identifier, words[:]) for identifier, words in original]
            for (i, j), word in zip(slots, perm):
                rows[i][1][j] = word
            self.assertEqual(Counter(w for _, words in rows for w in words),
                             Counter(w for _, words in original for w in words))
            for (identifier, words), (_, old) in zip(rows, original):
                self.assertEqual((words[0], words[-1], len(words)), (old[0], old[-1], len(old)))
                self.assertEqual([signature(w) for w in words], [signature(w) for w in old])
                changes[identifier] += words[-2] != old[-2]
            valid += 1
        result = analyze(original)
        for category in result.values():
            expected = sum((Fraction(changes[d['id']], valid) for d in category['variable_rows']), Fraction())
            self.assertEqual(Fraction(category['expected_changed_predecessors_exact']), expected)

    def test_no_cross_folio_exchange(self):
        rows = [('f1r.1', ['first', 'aba', 'xam']), ('f2r.1', ['first', 'aca', 'xam'])]
        self.assertEqual(analyze(rows)['am_final']['variable_lines'], 0)

    def test_no_cross_signature_exchange(self):
        for alternate in ('abc', 'abba'):
            rows = [('f1r.1', ['first', 'aba', 'xam']), ('f1v.1', ['first', alternate, 'xam'])]
            self.assertEqual(analyze(rows)['am_final']['variable_lines'], 0)

    def test_panels_grouped_and_line_inventory_relaxed(self):
        rows = [('f1r2.1', ['first', 'aba', 'xam']), ('f1v3.1', ['first', 'aca', 'xam'])]
        before = repr(rows)
        result = analyze(rows)['am_final']
        self.assertEqual(result['variable_lines'], 2)
        self.assertEqual(result['expected_changed_predecessors_exact'], '1')
        self.assertEqual(repr(rows), before)

    def test_degenerate(self):
        self.assertEqual(analyze([('f1r.1', ['xam'])])['am_final']['variable_lines'], 0)

    def test_reject_invalid(self):
        for rows in ([], [('f1r.1', [])], [('f1r.1', [''])], [('f1r.1', ['a']), ('f1r.1', ['a'])]):
            with self.assertRaises(ValueError):
                analyze(rows)
        with self.assertRaises(ValueError):
            group('unresolved')


if __name__ == '__main__':
    unittest.main()
