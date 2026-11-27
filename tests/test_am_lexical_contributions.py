import hashlib
import itertools
from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_am_lexical_contributions import decompose, verify_snapshot


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



class LexicalSnapshotTransitionTests(unittest.TestCase):
    ROOT = Path(__file__).resolve().parents[1]
    SELF = 'scripts/audit_am_lexical_contributions.py'
    PARAGRAPH = 'scripts/audit_exp173_paragraph_strata.py'
    BRIDGE = 'scripts/audit_exp173_reader_bridge.py'
    OLD_PARAGRAPH = 'ce646d9bfb33fa3519e8d1d55aa3e093364910c292da9e8bb8016cd745df581c'
    NEW_PARAGRAPH = '19c7754050439705310c43f52ef21c0dab11bcf1928e9a6c52ff285a7e168594'
    OLD_BRIDGE = 'cab48f865203d049f7c5a579146ca340c0cf61100d058792d11dcb29490363f8'
    NEW_BRIDGE = '5609e672a461f03c25e1462e5b3615e785741e9c5a15b366da880f71029bc223'

    def snapshots(self):
        archived = {'dependencies_sha256': {
            self.PARAGRAPH: self.OLD_PARAGRAPH,
            self.BRIDGE: self.OLD_BRIDGE,
            self.SELF: 'e270a0da9d99b82147a837458559cbfae8c9227dcb302d6d3a639f28fd3f57a9',
            'scripts/unchanged.py': 'a' * 64},
            'files': [{'observed': 7, 'expected_exact': '11/3'}]}
        actual = {'dependencies_sha256': {
            self.PARAGRAPH: self.NEW_PARAGRAPH,
            self.BRIDGE: self.NEW_BRIDGE,
            self.SELF: 'b' * 64,
            'scripts/unchanged.py': 'a' * 64},
            'files': [{'observed': 7, 'expected_exact': '11/3'}]}
        return actual, archived

    def test_exact_reader_source_transitions_are_accepted(self):
        actual, archived = self.snapshots()
        self.assertEqual(set(verify_snapshot(actual, archived)), {self.SELF, self.PARAGRAPH, self.BRIDGE})

    def test_scientific_snapshot_value_drift_is_rejected(self):
        actual, archived = self.snapshots()
        actual['files'][0]['observed'] = 8
        with self.assertRaisesRegex(SystemExit, 'Lexical snapshot mismatch'):
            verify_snapshot(actual, archived)

    def test_unapproved_current_dependency_digest_is_rejected(self):
        actual, archived = self.snapshots()
        actual['dependencies_sha256'][self.BRIDGE] = '0' * 64
        with self.assertRaisesRegex(SystemExit, 'Lexical snapshot mismatch'):
            verify_snapshot(actual, archived)

    def test_unapproved_historical_dependency_digest_is_rejected(self):
        actual, archived = self.snapshots()
        archived['dependencies_sha256'][self.PARAGRAPH] = 'f' * 64
        with self.assertRaisesRegex(SystemExit, 'Lexical snapshot mismatch'):
            verify_snapshot(actual, archived)

    def test_transition_pins_match_checked_in_sources(self):
        for path, digest in ((self.PARAGRAPH, self.NEW_PARAGRAPH),
                             (self.BRIDGE, self.NEW_BRIDGE)):
            self.assertEqual(hashlib.sha256((self.ROOT / path).read_bytes()).hexdigest(), digest)

if __name__ == '__main__':
    unittest.main()
