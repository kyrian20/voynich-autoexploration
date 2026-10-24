#!/usr/bin/env python3
"""Deterministic counterexamples for EXP-260's legacy MI calculation."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "exp260_scope", ROOT / "scripts/audit_exp260_mi_scope.py")
scope = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scope)


class PairMutualInformation(unittest.TestCase):
    def test_independent_balanced_pairs_have_zero_mi(self):
        self.assertAlmostEqual(scope.true_adjacent_pair_mi(
            ["aa", "ab", "ba", "bb"])["mi_bits"], 0.0)

    def test_deterministic_two_way_pairs_have_one_bit(self):
        self.assertAlmostEqual(scope.true_adjacent_pair_mi(
            ["aa", "bb"])["mi_bits"], 1.0)

    def test_legacy_unigram_marginals_can_create_spurious_two_bits(self):
        words = ["ab", "ac"]  # first character constant: true MI = zero
        functions, _ = scope.load_legacy_functions()
        legacy = functions["compute_pmi"](words, None, min_count=1)[4]
        correct = scope.true_adjacent_pair_mi(words)["mi_bits"]
        self.assertAlmostEqual(correct, 0.0)
        self.assertAlmostEqual(legacy, 2.0)

    def test_min_count_censoring_excludes_observed_pairs_from_legacy_sum(self):
        words = ["ab", "ab", "ab", "ac"]
        functions, _ = scope.load_legacy_functions()
        legacy = functions["compute_pmi"](words, None, min_count=2)[4]
        correct = scope.true_adjacent_pair_mi(words)["mi_bits"]
        self.assertAlmostEqual(legacy, 1.5)
        self.assertAlmostEqual(correct, 0.0)

    def test_empty_pairs_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "No adjacent pairs"):
            scope.true_adjacent_pair_mi(["a", "b"])


if __name__ == "__main__":
    unittest.main()
