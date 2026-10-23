"""Regression for contradictory $L values across separate IVTFF headers."""
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_ivtff_metadata_strict import validate


class DuplicateLanguageHeaders(unittest.TestCase):
    def test_identical_repeated_assignment_is_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "fixture.ivtff"
            path.write_text(
                "<f1r> <! $L=A>\n"
                "<f1r> <! $L=A>\n"
                "<f2r> <! $L=B>\n",
                encoding="utf-8",
            )
            report = validate(path)
            self.assertEqual(report["folio_headers"], 3)
            self.assertEqual(report["folios_with_language"], 2)
            self.assertEqual(report["consistent_repeated_language_headers"], 1)
            self.assertEqual(report["contradictory_repeated_language_headers"], 0)

    def test_conflicting_repeated_assignment_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "fixture.ivtff"
            path.write_text(
                "<f1r> <! $Q=A $L=B>\n"
                "<f1r> <! $Q=B $L=A>\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, r"f1r at line 2: B versus A"):
                validate(path)

    def test_quire_without_language_does_not_conflict(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "fixture.ivtff"
            path.write_text(
                "<f1r> <! $Q=B>\n"
                "<f1r> <! $L=A>\n",
                encoding="utf-8",
            )
            report = validate(path)
            self.assertEqual(report["folios_with_language"], 1)
            self.assertEqual(report["consistent_repeated_language_headers"], 0)


if __name__ == "__main__":
    unittest.main()
