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



class OpportunitySnapshotTransitionTests(unittest.TestCase):
    SELF = 'scripts/audit_predecessor_opportunities.py'
    BRIDGE = 'scripts/audit_exp173_reader_bridge.py'
    PARAGRAPH = 'scripts/audit_exp173_paragraph_strata.py'
    OLD_SELF = 'd4c6a7fc43adce9c485eb6089e9dc8692a34ba3d9bc667b47706459fdeaefbc0'
    OLD_BRIDGE = 'cab48f865203d049f7c5a579146ca340c0cf61100d058792d11dcb29490363f8'
    NEW_BRIDGE = '5609e672a461f03c25e1462e5b3615e785741e9c5a15b366da880f71029bc223'
    OLD_PARAGRAPH = 'ce646d9bfb33fa3519e8d1d55aa3e093364910c292da9e8bb8016cd745df581c'
    NEW_PARAGRAPH = '19c7754050439705310c43f52ef21c0dab11bcf1928e9a6c52ff285a7e168594'

    def snapshots(self):
        archived = {'dependencies_sha256': {
            self.SELF: self.OLD_SELF, self.BRIDGE: self.OLD_BRIDGE,
            self.PARAGRAPH: self.OLD_PARAGRAPH, 'scripts/unchanged.py': 'a' * 64},
            'files': [{'lines': 12, 'expected_changed_predecessors_exact': '7/3'}]}
        actual = {'dependencies_sha256': {
            self.SELF: 'b' * 64, self.BRIDGE: self.NEW_BRIDGE,
            self.PARAGRAPH: self.NEW_PARAGRAPH, 'scripts/unchanged.py': 'a' * 64},
            'files': [{'lines': 12, 'expected_changed_predecessors_exact': '7/3'}]}
        return actual, archived

    def test_pinned_source_changes_and_self_digest_preserve_snapshot(self):
        actual, archived = self.snapshots()
        self.assertEqual(set(verify_snapshot(actual, archived)),
                         {self.SELF, self.BRIDGE, self.PARAGRAPH})

    def test_metric_drift_is_rejected(self):
        actual, archived = self.snapshots()
        actual['files'][0]['lines'] = 13
        with self.assertRaisesRegex(SystemExit, 'Opportunity snapshot mismatch'):
            verify_snapshot(actual, archived)

    def test_unapproved_source_hash_is_rejected(self):
        actual, archived = self.snapshots()
        actual['dependencies_sha256'][self.BRIDGE] = '0' * 64
        with self.assertRaisesRegex(SystemExit, 'Opportunity snapshot mismatch'):
            verify_snapshot(actual, archived)

    def test_unapproved_historical_hash_is_rejected(self):
        actual, archived = self.snapshots()
        archived['dependencies_sha256'][self.PARAGRAPH] = 'f' * 64
        with self.assertRaisesRegex(SystemExit, 'Opportunity snapshot mismatch'):
            verify_snapshot(actual, archived)

if __name__ == '__main__':
    unittest.main()
