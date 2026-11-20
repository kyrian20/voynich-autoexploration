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

    def test_negative_null_mean_is_rejected(self):
        saved, report = fixture()
        saved["tests"]["daiin"]["null_mean_initial"] = -1.0
        saved["tests"]["daiin"]["observed_standardized_statistic"] = 2.0
        self.assertFalse(archive_result_complete(saved, report))

    def test_null_mean_above_line_count_is_rejected(self):
        saved, report = fixture()
        saved["tests"]["daiin"]["null_mean_initial"] = 4.0
        saved["tests"]["daiin"]["observed_standardized_statistic"] = -3.0
        self.assertFalse(archive_result_complete(saved, report))

    def test_zero_variance_inconsistent_observation_is_rejected(self):
        saved, report = fixture()
        saved["tests"]["daiin"]["null_mean_initial"] = 0.0
        saved["tests"]["daiin"]["null_sd_initial"] = 0.0
        saved["tests"]["daiin"]["observed_standardized_statistic"] = 0.0
        self.assertFalse(archive_result_complete(saved, report))

    def test_occurrences_exceed_total_tokens_is_rejected(self):
        saved, report = fixture()
        saved["tokens"] = 2
        report = report.replace("- Tokens: 3", "- Tokens: 2")
        self.assertFalse(archive_result_complete(saved, report))

    def test_line_initial_exceeds_total_lines_is_rejected(self):
        saved, report = fixture()
        saved["lines"] = 1
        report = report.replace("- Líneas: 3", "- Líneas: 1")
        self.assertFalse(archive_result_complete(saved, report))

    def test_line_final_exceeds_total_lines_is_rejected(self):
        saved, report = fixture()
        saved["lines"] = 1
        report = report.replace("- Líneas: 3", "- Líneas: 1")
        saved["observed"]["daiin"]["line_final"] = 2
        saved["observed"]["daiin"]["occurrences"] = 2
        saved["observed"]["daiin"]["initial_fraction"] = 0.5
        saved["observed"]["daiin"]["by_currier"]["A"].update({"line_final": 2, "occurrences": 2})
        report = report.replace("| daiin | 1 | 1 | 0 |", "| daiin | 2 | 1 | 2 |").replace("| A | 1 | 1 | 0 |", "| A | 2 | 1 | 2 |", 1)
        self.assertFalse(archive_result_complete(saved, report))

    def test_boolean_test_statistic_is_rejected(self):
        saved, report = fixture()
        saved["tests"]["dain"]["empirical_p"] = True
        self.assertFalse(archive_result_complete(saved, report))


if __name__ == "__main__":
    unittest.main()
