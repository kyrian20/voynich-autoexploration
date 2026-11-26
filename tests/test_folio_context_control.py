from collections import Counter
from fractions import Fraction
import itertools
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_folio_context_control import analyze, group, signature, verify_snapshot


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



class FolioSnapshotTransitionTests(unittest.TestCase):
    SELF = 'scripts/audit_folio_context_control.py'
    BRIDGE = 'scripts/audit_exp173_reader_bridge.py'
    PARAGRAPH = 'scripts/audit_exp173_paragraph_strata.py'
    OLD_SELF = '77ec301c4ac0cda185f7eb31315c39cab649633a34a679f58a86f1925b7eca35'
    OLD_BRIDGE = 'cab48f865203d049f7c5a579146ca340c0cf61100d058792d11dcb29490363f8'
    NEW_BRIDGE = '5609e672a461f03c25e1462e5b3615e785741e9c5a15b366da880f71029bc223'
    OLD_PARAGRAPH = 'ce646d9bfb33fa3519e8d1d55aa3e093364910c292da9e8bb8016cd745df581c'
    NEW_PARAGRAPH = '19c7754050439705310c43f52ef21c0dab11bcf1928e9a6c52ff285a7e168594'

    def snapshots(self):
        archived = {'dependencies_sha256': {
            self.SELF: self.OLD_SELF, self.BRIDGE: self.OLD_BRIDGE,
            self.PARAGRAPH: self.OLD_PARAGRAPH, 'scripts/unchanged.py': 'a' * 64},
            'files': [{'variable_lines': 4, 'expected_changed_predecessors_exact': '1/2'}]}
        actual = {'dependencies_sha256': {
            self.SELF: 'b' * 64, self.BRIDGE: self.NEW_BRIDGE,
            self.PARAGRAPH: self.NEW_PARAGRAPH, 'scripts/unchanged.py': 'a' * 64},
            'files': [{'variable_lines': 4, 'expected_changed_predecessors_exact': '1/2'}]}
        return actual, archived

    def test_pinned_source_changes_and_self_digest_preserve_snapshot(self):
        actual, archived = self.snapshots()
        self.assertEqual(set(verify_snapshot(actual, archived)),
                         {self.SELF, self.BRIDGE, self.PARAGRAPH})

    def test_output_value_drift_is_rejected(self):
        actual, archived = self.snapshots()
        actual['files'][0]['variable_lines'] = 5
        with self.assertRaisesRegex(SystemExit, 'Folio-control snapshot mismatch'):
            verify_snapshot(actual, archived)

    def test_unapproved_source_hash_is_rejected(self):
        actual, archived = self.snapshots()
        actual['dependencies_sha256'][self.BRIDGE] = '0' * 64
        with self.assertRaisesRegex(SystemExit, 'Folio-control snapshot mismatch'):
            verify_snapshot(actual, archived)

    def test_unapproved_historical_hash_is_rejected(self):
        actual, archived = self.snapshots()
        archived['dependencies_sha256'][self.PARAGRAPH] = 'f' * 64
        with self.assertRaisesRegex(SystemExit, 'Folio-control snapshot mismatch'):
            verify_snapshot(actual, archived)

if __name__ == '__main__':
    unittest.main()
