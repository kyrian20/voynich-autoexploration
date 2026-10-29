"""Regression: binary Naive Bayes class priors use one alpha per class.

This tests the intended categorical NB prior independently of IVTFF data.
With identical feature values in every training row, likelihood factors
cancel exactly, leaving only the class prior. Historical code added 2*alpha
to *each* numerator while dividing by n+2*alpha.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_replication_prior", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class NaiveBayesClassPriorContract(unittest.TestCase):
    @staticmethod
    def rows(negatives: int, positives: int):
        # Every candidate has identical categorical features; there is no
        # predictive likelihood evidence to shift the class prior.
        features = module.feats("abcd", "efgh")
        return ([{"y": 0, "f": features} for _ in range(negatives)] +
                [{"y": 1, "f": features} for _ in range(positives)])

    def check_posterior(self, negatives: int, positives: int, alpha: float):
        train = self.rows(negatives, positives)
        p, counts = module.pred(train, self.rows(1, 0), "full_tuple", alpha=alpha)
        self.assertEqual(counts[0], negatives)
        self.assertEqual(counts[1], positives)
        self.assertEqual(len(p), 1)
        self.assertAlmostEqual(
            p[0], (positives + alpha) / (negatives + positives + 2 * alpha)
        )

    def test_imbalanced_classes_alpha_half(self):
        # Old implementation: 1/3; correct Dirichlet(0.5,0.5): 0.3.
        self.check_posterior(3, 1, 0.5)

    def test_imbalanced_classes_alpha_one(self):
        # Old implementation: 3/8; correct Laplace prior: 1/3.
        self.check_posterior(3, 1, 1.0)

    def test_zero_positive_class_still_has_finite_smoothed_prior(self):
        self.check_posterior(4, 0, 0.5)

    def test_reversed_class_balance(self):
        self.check_posterior(1, 3, 0.5)


if __name__ == "__main__":
    unittest.main()
