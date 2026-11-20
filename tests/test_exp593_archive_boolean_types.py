"""Regression: boolean archive statistics must never masquerade as numbers.

This exercises the pure completeness guard, not a historical reproduction.
"""
import copy
import unittest

from scripts.exp593_daiin_variants import VARIANTS, archive_result_complete


def fixture():
    observed = {}
    tests = {}
    report = ["- Líneas: 3", "- Tokens: 3"]
    for word in VARIANTS:
        observed[word] = {
            "occurrences": 1, "line_initial": 1, "line_final": 0,
            "initial_fraction": 1.0,
            "by_currier": {"A": {"occurrences": 1, "line_initial": 1, "line_final": 0}},
        }
        tests[word] = {
            "null_mean_initial": 0.0, "null_sd_initial": 1.0,
            "observed_standardized_statistic": 1.0,
            "empirical_p": 0.5, "max_stat_adjusted_p": 0.5,
        }
        report.append(f"| {word} | 1 | 1 | 0 | 0.500000 | 0.500000 |")
    for word in VARIANTS:
        report.extend([
            f"### {word}", "| Clase | Ocurrencias | Inicio | Final |",
            "| A | 1 | 1 | 0 |",
        ])
    return {
        "lines": 3, "tokens": 3, "null_model": "synthetic",
        "limitations": ["synthetic fixture"], "observed": observed, "tests": tests,
    }, "\n".join(report)


class ArchiveNumericTypeTests(unittest.TestCase):
    def test_valid_synthetic_archive(self):
        saved, report = fixture()
        self.assertTrue(archive_result_complete(saved, report))

    def test_boolean_initial_fraction_is_rejected(self):
        saved, report = fixture()
        saved["observed"]["daiin"]["initial_fraction"] = True
        self.assertFalse(archive_result_complete(saved, report))

    def test_boolean_test_statistic_is_rejected(self):
        saved, report = fixture()
        saved["tests"]["dain"]["empirical_p"] = True
        self.assertFalse(archive_result_complete(saved, report))


if __name__ == "__main__":
    unittest.main()
