"""Regression: EXP-593 must not silently overwrite contradictory folio metadata."""
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / "scripts/exp593_daiin_variants.py"), run_name="exp593_header_test")


class Exp593HeaderConflictTest(unittest.TestCase):
    def parse_fixture(self, headers):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "fixture.txt"
            source.write_text(headers + "<f1r.1,P0> daiin dain\n", encoding="utf-8")
            with patch.dict(MODULE["parse"].__globals__, {"SOURCE": source}):
                return MODULE["parse"]()[1]

    def test_conflicting_folio_language_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "conflicting Currier headers"):
            self.parse_fixture("<f1r> $L=A\n<f1r> $L=B\n")

    def test_repeated_consistent_folio_language_is_allowed(self):
        rows = self.parse_fixture("<f1r> $L=A\n<f1r> $L=A\n")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["currier"], "A")


if __name__ == "__main__":
    unittest.main()
