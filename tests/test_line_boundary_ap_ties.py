"""Tie-aware average precision regression for the line-boundary replica."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_replication_ap", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AveragePrecisionTieContract(unittest.TestCase):
    def test_all_equal_scores_equal_prevalence_independent_of_row_order(self):
        # Historical implementation returned 1.0 for [1,0] and 0.5 for [0,1].
        for labels in ([1, 0], [0, 1], [1, 0, 1, 0], [0, 1, 0, 1]):
            with self.subTest(labels=labels):
                self.assertAlmostEqual(module.ap(labels, [0.5] * len(labels)),
                                       sum(labels) / len(labels))

    def test_tied_top_group_is_a_single_threshold(self):
        self.assertAlmostEqual(module.ap([1, 0, 1, 0], [.9, .9, .2, .2]),
                               .5 * .5 + .5 * .5)
        self.assertAlmostEqual(module.ap([0, 1, 0, 1], [.9, .9, .2, .2]),
                               .5)

    def test_unique_scores_retain_standard_average_precision(self):
        self.assertAlmostEqual(module.ap([1, 0, 1], [.9, .5, .4]),
                               (1 + 2 / 3) / 2)
        self.assertAlmostEqual(module.ap([0, 1, 1], [.9, .8, .7]),
                               (1 / 2 + 2 / 3) / 2)

    def test_no_positive_label_retains_undefined_result(self):
        self.assertTrue(math.isnan(module.ap([0, 0], [.4, .4])))


if __name__ == "__main__":
    unittest.main()
