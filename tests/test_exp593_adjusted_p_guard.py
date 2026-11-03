"""Regression: a synchronized max-T correction cannot lower an empirical p-value.

This checks archive adjudication only; it does not rerun permutations or
make a scientific claim about the frozen EXP-593 result.
"""
import copy
import json
import unittest
from pathlib import Path

from scripts.exp593_daiin_variants import archive_result_complete

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "research/experiments/2026-11-03-exp593-corrected-L-metadata.json"
REPORT = ARCHIVE.with_suffix(".md")


class Exp593MaxTArchiveGuard(unittest.TestCase):
    def test_frozen_archive_still_accepted(self):
        saved = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        report = REPORT.read_text(encoding="utf-8")
        self.assertTrue(archive_result_complete(saved, report))

    def test_reject_adjusted_p_below_empirical_even_when_report_agrees(self):
        saved = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        report = REPORT.read_text(encoding="utf-8")
        bad = copy.deepcopy(saved)
        word = "daiiin"
        old = bad["tests"][word]["max_stat_adjusted_p"]
        bad["tests"][word]["max_stat_adjusted_p"] = 0.5
        observed = bad["observed"][word]
        test = bad["tests"][word]
        original_row = (
            f"| {word} | {observed['occurrences']} | {observed['line_initial']} | "
            f"{observed['line_final']} | {test['empirical_p']:.6f} | {old:.6f} |"
        )
        tampered_row = original_row.replace(f"| {old:.6f} |", "| 0.500000 |")
        self.assertIn(original_row, report)
        report = report.replace(original_row, tampered_row)
        self.assertFalse(archive_result_complete(bad, report))


if __name__ == "__main__":
    unittest.main()
