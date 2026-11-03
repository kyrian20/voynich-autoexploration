"""EXP-593 archive guard: standardized statistics must match archived null moments.

No permutations are rerun and the frozen historical outputs remain unchanged.
"""
import copy
import json
import unittest
from pathlib import Path

from scripts.exp593_daiin_variants import archive_result_complete

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "research/experiments/2026-11-03-exp593-corrected-L-metadata.json"
REPORT = ARCHIVE.with_suffix(".md")


class Exp593ZscoreArchiveGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        cls.report = REPORT.read_text(encoding="utf-8")

    def test_original_archive_passes(self):
        self.assertTrue(archive_result_complete(self.saved, self.report))

    def test_reject_forged_zscore_without_changing_report(self):
        bad = copy.deepcopy(self.saved)
        bad["tests"]["daiin"]["observed_standardized_statistic"] += 1.0
        self.assertFalse(archive_result_complete(bad, self.report))

    def test_reject_zero_sd_with_nonzero_zscore(self):
        bad = copy.deepcopy(self.saved)
        bad["tests"]["daiiin"]["null_sd_initial"] = 0.0
        bad["tests"]["daiiin"]["observed_standardized_statistic"] = 1.0
        self.assertFalse(archive_result_complete(bad, self.report))


if __name__ == "__main__":
    unittest.main()
