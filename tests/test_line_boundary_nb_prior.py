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
        # Every training candidate has the same categorical features; their
        # likelihood factors need not cancel once an OOV bucket is reserved.
        features = module.feats("abcd", "efgh")
        return ([{"y": 0, "f": features} for _ in range(negatives)] +
                [{"y": 1, "f": features} for _ in range(positives)])

    def check_posterior(self, negatives: int, positives: int, alpha: float):
        # Isolate the class prior with zero categorical features. Once an
        # explicit OOV bucket is modeled, even an observed constant feature
        # has class-dependent smoothing and no longer cancels.
        train = [{"y": row["y"], "f": {"prior_only": ()}}
                 for row in self.rows(negatives, positives)]
        p, counts = module.pred(train, [{"y": 0, "f": {"prior_only": ()}}],
                                "prior_only", alpha=alpha)
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


class NaiveBayesOOVNormalizationContract(unittest.TestCase):
    def test_unseen_category_has_one_reserved_bucket(self):
        # Three negatives and one positive, with the same two tuple features.
        # Both features are unseen at evaluation. For each class and feature,
        # the observed category and the OOV bucket must sum to probability 1.
        train = NaiveBayesClassPriorContract.rows(3, 1)
        test = [{"y": 0, "f": module.feats("zzzz", "yyyy")}]
        p, _ = module.pred(train, test, "full_tuple", alpha=0.5)
        prior0, prior1 = 3.5 / 5.0, 1.5 / 5.0
        oov0, oov1 = 0.5 / 4.0, 0.5 / 2.0
        self.assertAlmostEqual((3.0 + 0.5) / 4.0 + oov0, 1.0)
        self.assertAlmostEqual((1.0 + 0.5) / 2.0 + oov1, 1.0)
        expected = prior1 * oov1**2 / (prior0 * oov0**2 + prior1 * oov1**2)
        self.assertAlmostEqual(expected, 12.0 / 19.0)
        self.assertAlmostEqual(p[0], expected)

    def test_observed_category_uses_same_normalized_support(self):
        train = NaiveBayesClassPriorContract.rows(3, 1)
        test = NaiveBayesClassPriorContract.rows(1, 0)
        p, _ = module.pred(train, test, "full_tuple", alpha=0.5)
        prior0, prior1 = 3.5 / 5.0, 1.5 / 5.0
        seen0, seen1 = 3.5 / 4.0, 1.5 / 2.0
        expected = prior1 * seen1**2 / (prior0 * seen0**2 + prior1 * seen1**2)
        self.assertAlmostEqual(p[0], expected)


if __name__ == "__main__":
    unittest.main()
