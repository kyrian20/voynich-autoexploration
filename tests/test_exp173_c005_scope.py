"""Pure regression tests for the EXP-173/C005 scope audit."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.audit_exp173_c005_scope import (
    binomial_upper_tail, cluster_counterexample, git_blob_sha1, result_snapshot,
)


class ScopeAuditTests(unittest.TestCase):
    def test_binomial_tail_known_cases(self):
        self.assertAlmostEqual(binomial_upper_tail(2, 1, .5), .75)
        self.assertEqual(binomial_upper_tail(2, 0, .5), 1.0)
        self.assertEqual(binomial_upper_tail(2, 2, .5), .25)

    def test_cluster_counterexample_is_not_a_vms_p_value(self):
        example = cluster_counterexample()
        self.assertEqual(example['line_level_k'], 20)
        self.assertEqual(example['line_level_n'], 200)
        self.assertAlmostEqual(example['line_binomial_p'], 0.00266457955, places=10)
        self.assertAlmostEqual(example['folio_binomial_p'], 0.264160475056, places=10)
        self.assertGreater(example['folio_binomial_p'], .05)
        self.assertLess(example['line_binomial_p'], .05)

    def test_invalid_design_rejected(self):
        with self.assertRaises(ValueError):
            cluster_counterexample(positive_folios=21)
        with self.assertRaises(ValueError):
            binomial_upper_tail(5, 6, .5)

    def test_snapshot_keeps_archived_claim_separate_from_toy(self):
        snapshot = result_snapshot()
        self.assertEqual(snapshot['historical_claim']['status'], 'REPORTED_NOT_REPRODUCED_HERE')
        self.assertFalse(snapshot['method_flags']['folio_cluster_robust_p_calculated'])
        self.assertNotEqual(snapshot['historical_claim']['reported_p'],
                            str(snapshot['synthetic_control']['line_binomial_p']))

    def test_git_blob_hash_is_content_sensitive(self):
        self.assertEqual(git_blob_sha1(b''), 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391')
        self.assertNotEqual(git_blob_sha1(b'abc'), git_blob_sha1(b'abd'))


if __name__ == '__main__':
    unittest.main()
