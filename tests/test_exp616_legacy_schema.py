"""EXP-616 legacy field-name regression; no new target scoring."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import audit_exp616_legacy_schema as mod


class Exp616LegacySchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import json
        cls.original = json.loads((ROOT / mod.ARCHIVE).read_text(encoding="utf-8"))

    def test_legacy_removed_is_remaining(self):
        corrected = mod.adjudicate(self.original)
        self.assertEqual(corrected["status"], "SCHEMA_CORRECTION_ONLY_NOT_REPRODUCED")
        self.assertEqual(corrected["results"]["ZL3b"]["leave_out"][0]["remaining"]["cells"], 171)
        self.assertEqual(corrected["results"]["ZL3b"]["leave_out"][0]["excluded"]["cells"], 109)
        self.assertEqual(corrected["results"]["IT2a"]["leave_out"][0]["remaining"]["cells"], 173)

    def test_nominal_numeric_leaves_are_not_legacy_folio_units(self):
        corrected = mod.adjudicate(self.original)
        self.assertEqual(corrected["nominal_numeric_leaf_count"], 12)
        self.assertEqual(corrected["results"]["ZL3b"]["all"]["folios"], 23)
        first = corrected["results"]["ZL3b"]["leave_out"][0]
        self.assertEqual(first["excluded"]["folios"], 8)
        self.assertEqual(first["nominal_numeric_leaf_count"], 4)

    def test_frozen_corpora_and_archive(self):
        result = mod.audit()
        self.assertEqual(set(result["sources"]), {"ZL3b", "IT2a"})
        self.assertEqual(len(result["archive_sha256"]), 64)

    def test_detect_same_total_but_wrong_remaining_count(self):
        altered = copy.deepcopy(self.original)
        altered["results"]["ZL3b"]["leave_out"][0]["removed"]["cells"] += 1
        with self.assertRaisesRegex(ValueError, "not additive"):
            mod.adjudicate(altered)

    def test_detect_rate_drift(self):
        altered = copy.deepcopy(self.original)
        altered["results"]["IT2a"]["leave_out"][1]["removed"]["sh_rate"] += 0.01
        altered["results"]["IT2a"]["leave_out"][1]["removed"]["difference_sh_minus_ch"] += 0.01
        with self.assertRaisesRegex(ValueError, "weighted rate drift"):
            mod.adjudicate(altered)

    def test_detect_block_reordering(self):
        altered = copy.deepcopy(self.original)
        altered["results"]["ZL3b"]["leave_out"].reverse()
        with self.assertRaisesRegex(ValueError, "alignment drift"):
            mod.adjudicate(altered)

    def test_detect_source_identity_drift(self):
        altered = copy.deepcopy(self.original)
        altered["sources"]["IT2a"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "source Git blob SHA-1 drift"):
            mod.adjudicate(altered)

    def test_reject_boolean_rate_in_synthetic_summary(self):
        # Python bool is an int subclass; JSON true/false must not be rates.
        summary = {
            "cells": 2, "folios": 1, "ch_n": 1, "sh_n": 1,
            "ch_rate": 0.25, "sh_rate": 0.75,
            "difference_sh_minus_ch": 0.5,
        }
        mod.check_summary(summary)  # Valid numeric control.
        for field in ("ch_rate", "sh_rate", "difference_sh_minus_ch"):
            with self.subTest(field=field):
                altered = summary.copy()
                altered[field] = False
                with self.assertRaisesRegex(ValueError, "Invalid rate"):
                    mod.check_summary(altered)

    def test_reject_boolean_rate_with_true(self):
        summary = {
            "cells": 2, "folios": 1, "ch_n": 1, "sh_n": 1,
            "ch_rate": True, "sh_rate": 1.0,
            "difference_sh_minus_ch": 0.0,
        }
        # This previously passed because True == 1 and 1.0 - True == 0.
        with self.assertRaisesRegex(ValueError, "Invalid rate"):
            mod.check_summary(summary)

    def test_reject_invalid_counts(self):
        altered = copy.deepcopy(self.original)
        altered["results"]["ZL3b"]["all"]["ch_n"] = -1
        with self.assertRaisesRegex(ValueError, "Invalid nonnegative count"):
            mod.adjudicate(altered)


if __name__ == "__main__":
    unittest.main()
