"""EXP-601 historical physical-leaf clustering scope: synthetic and frozen regressions."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import audit_exp601_physical_leaf_cluster_scope as mod


class Exp601PhysicalLeafScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.archive = json.loads((ROOT / mod.RESULT).read_text(encoding="utf-8"))

    def test_real_archive_81_units_are_only_40_numbered_leaves(self):
        audited = mod.audit()
        self.assertEqual(audited["status"], "INVALID_FOR_CLAIM")
        self.assertEqual(audited["historical_page_ids_sha256"], mod.FROZEN_PAGE_IDS_SHA256)
        crosswalk = audited["crosswalk"]
        self.assertEqual(crosswalk["historical_resampling_units"], 81)
        self.assertEqual(crosswalk["distinct_numbered_physical_leaves"], 40)
        self.assertEqual(crosswalk["leaves_with_both_sides"], 36)
        self.assertEqual(crosswalk["page_panel_units_per_leaf_histogram"],
                         {"1": 3, "2": 35, "4": 2})
        self.assertEqual(crosswalk["page_panel_ids_by_numbered_leaf"]["86"],
                         ["f86v3", "f86v4", "f86v5", "f86v6"])
        self.assertEqual(crosswalk["page_panel_ids_by_numbered_leaf"]["95"],
                         ["f95r1", "f95r2", "f95v1", "f95v2"])

    def test_synthetic_both_sides_and_panels_are_one_leaf(self):
        result = mod.classify_units(["f86v3", "f86v4", "f95r1", "f95v2", "f2r"])
        self.assertEqual(result["distinct_numbered_physical_leaves"], 3)
        self.assertEqual(result["leaves_with_both_sides"], 1)
        self.assertEqual(result["page_panel_units_per_leaf_histogram"], {"1": 1, "2": 2})

    def test_reject_duplicate_page_identifier(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            mod.classify_units(["f2r", "f2r"])

    def test_reject_unicode_or_unrecognized_identifiers(self):
        for page in ("f１２r", "f2x", "f2r_extra", "f0v", "f2r\n", ""):
            with self.subTest(page=page):
                with self.assertRaisesRegex(ValueError, "Unrecognized"):
                    mod.classify_units([page])

    def test_reject_historical_sample_or_seed_drift(self):
        altered = copy.deepcopy(self.archive)
        altered["sample"]["represented_folios"] = 40
        with self.assertRaisesRegex(ValueError, "resampling-unit count drift"):
            mod.adjudicate(altered)
        altered = copy.deepcopy(self.archive)
        altered["primary_effect"]["bootstrap_seed"] = 123
        with self.assertRaisesRegex(ValueError, "bootstrap seed drift"):
            mod.adjudicate(altered)

    def test_reject_same_count_wrong_page_identity(self):
        altered = copy.deepcopy(self.archive)
        altered["leave_one_folio_out"]["all_folios"][0]["folio"] = "f999r"
        with self.assertRaisesRegex(ValueError, "identity or order drift"):
            mod.adjudicate(altered)

    def test_reject_same_summary_different_historical_panel_id(self):
        altered = copy.deepcopy(self.archive)
        original_ids = [row["folio"] for row in self.archive["leave_one_folio_out"]["all_folios"]]
        altered["leave_one_folio_out"]["all_folios"][0]["folio"] = "f103r1"
        changed_ids = [row["folio"] for row in altered["leave_one_folio_out"]["all_folios"]]
        original = mod.classify_units(original_ids)
        changed = mod.classify_units(changed_ids)
        # Regression demonstrates why the old aggregate-only guard was insufficient.
        for key in ("historical_resampling_units", "distinct_numbered_physical_leaves",
                    "leaves_with_both_sides", "page_panel_units_per_leaf_histogram"):
            self.assertEqual(original[key], changed[key])
        with self.assertRaisesRegex(ValueError, "identity or order drift"):
            mod.adjudicate(altered)

    def test_reject_same_id_set_different_archive_order(self):
        altered = copy.deepcopy(self.archive)
        rows = altered["leave_one_folio_out"]["all_folios"]
        rows[0], rows[1] = rows[1], rows[0]
        with self.assertRaisesRegex(ValueError, "identity or order drift"):
            mod.adjudicate(altered)

    def test_reject_frozen_source_mutation_and_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = root / "original.txt"
            original.write_bytes(b"frozen")
            expected = mod.git_blob_sha1(b"frozen")
            self.assertEqual(mod.frozen_bytes(original, blob_sha1=expected), b"frozen")
            original.write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError, "mismatch"):
                mod.frozen_bytes(original, blob_sha1=expected)
            link = root / "link.txt"
            try:
                link.symlink_to(original)
            except (NotImplementedError, OSError):
                self.skipTest("Symlinks unavailable")
            with self.assertRaisesRegex(ValueError, "symlinked"):
                mod.frozen_bytes(link, blob_sha1=mod.git_blob_sha1(b"tampered"))


if __name__ == "__main__":
    unittest.main()
