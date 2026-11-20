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

    def test_joint_occurrences_exceed_tokens_is_rejected(self):
        saved, report = fixture()
        # Each spelling individually fits two tokens; their total of three does not.
        saved["tokens"] = 2
        report = report.replace("- Tokens: 3", "- Tokens: 2")
        self.assertFalse(archive_result_complete(saved, report))

    def test_joint_initials_exceed_lines_is_rejected(self):
        saved, report = fixture()
        # All three spellings claim the first position of only two lines.
        saved["lines"] = 2
        report = report.replace("- Líneas: 3", "- Líneas: 2")
        self.assertFalse(archive_result_complete(saved, report))

    def test_joint_finals_exceed_lines_is_rejected(self):
        saved, report = fixture()
        saved["lines"] = 2
        report = report.replace("- Líneas: 3", "- Líneas: 2")
        for word in VARIANTS:
            saved["observed"][word]["line_final"] = 1
            saved["observed"][word]["by_currier"]["A"]["line_final"] = 1
            report = report.replace(
                f"| {word} | 1 | 1 | 0 |", f"| {word} | 1 | 1 | 1 |"
            )
        report = report.replace("| A | 1 | 1 | 0 |", "| A | 1 | 1 | 1 |")
        self.assertFalse(archive_result_complete(saved, report))

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

    def test_null_mean_exceeding_variant_occurrences_is_rejected(self):
        saved, report = fixture()
        # One occurrence cannot start more than one line in any shuffle.
        # The total line count is three, so the old lines-only bound missed this.
        saved["tests"]["daiin"]["null_mean_initial"] = 2.0
        saved["tests"]["daiin"]["observed_standardized_statistic"] = -1.0
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
        saved["tokens"] = 4
        row = saved["observed"]["daiin"]
        row.update({"occurrences": 2, "line_initial": 2, "initial_fraction": 1.0})
        row["by_currier"]["A"].update({"occurrences": 2, "line_initial": 2})
        saved["tests"]["daiin"]["observed_standardized_statistic"] = 2.0
        report = report.replace("- Líneas: 3", "- Líneas: 1").replace("- Tokens: 3", "- Tokens: 4")
        report = report.replace("| daiin | 1 | 1 | 0 |", "| daiin | 2 | 2 | 0 |")
        report = report.replace("| A | 1 | 1 | 0 |", "| A | 2 | 2 | 0 |", 1)
        self.assertFalse(archive_result_complete(saved, report))

    def test_line_final_exceeds_total_lines_is_rejected(self):
        saved, report = fixture()
        saved["lines"] = 1
        saved["tokens"] = 4
        row = saved["observed"]["daiin"]
        row.update({"occurrences": 2, "line_final": 2, "initial_fraction": 0.5})
        row["by_currier"]["A"].update({"occurrences": 2, "line_final": 2})
        report = report.replace("- Líneas: 3", "- Líneas: 1").replace("- Tokens: 3", "- Tokens: 4")
        report = report.replace("| daiin | 1 | 1 | 0 |", "| daiin | 2 | 1 | 2 |")
        report = report.replace("| A | 1 | 1 | 0 |", "| A | 2 | 1 | 2 |", 1)
        self.assertFalse(archive_result_complete(saved, report))

    def test_boolean_test_statistic_is_rejected(self):
        saved, report = fixture()
        saved["tests"]["dain"]["empirical_p"] = True
        self.assertFalse(archive_result_complete(saved, report))



class GeneratorZeroVarianceTests(unittest.TestCase):
    def test_generator_rejects_undefined_z_before_archive_write(self):
        """One deterministic null draw contradicts observed initials: no archive."""
        from unittest.mock import patch
        from scripts import exp593_daiin_variants as exp

        class ReverseShuffle:
            def shuffle(self, tokens):
                tokens.reverse()

        lines = [
            {"folio": "1r", "line": i + 1, "currier": "A",
             "tokens": ["daiin", "other"]}
            for i in range(1000)
        ]
        with (patch.object(exp.SOURCE.__class__, "exists", return_value=True),
              patch.object(exp, "parse", return_value=(b"synthetic", lines)),
              patch.object(exp, "archive_status", return_value="new"),
              patch.object(exp, "archive_paths", return_value=("unused.json", "unused.md")),
              patch.object(exp, "N_PERM", 1),
              patch.object(exp.random, "Random", return_value=ReverseShuffle()),
              patch.object(exp, "write_archive_pair") as writer):
            with self.assertRaisesRegex(RuntimeError, "undefined z-score for daiin"):
                exp.main()
            writer.assert_not_called()

if __name__ == "__main__":
    unittest.main()
