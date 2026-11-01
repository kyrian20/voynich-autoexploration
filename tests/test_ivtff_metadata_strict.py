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

    def test_zero_padded_alias_cannot_hide_conflicting_currier_label(self):
        # Previously both spellings occupied separate string keys.
        for first, alias in (("f1r", "f01r"), ("f86v4", "f086v4")):
            with self.subTest(alias=alias), tempfile.TemporaryDirectory() as d:
                path = Path(d) / "fixture.ivtff"
                path.write_text(
                    f"<{first}> <! $L=A>\\n<{alias}> <! $L=B>\\n".replace("\\\\n", "\\n"),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValueError, rf"{alias} at line 2: A versus B"):
                    validate(path)

    def test_same_physical_page_alias_counts_once_but_panels_stay_distinct(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "fixture.ivtff"
            path.write_text(
                "<f86v4> <! $L=A>\\n"
                "<f086v4> <! $L=A>\\n"
                "<f86v5> <! $L=B>\\n"
                "<fRos> <! $L=A>\\n".replace("\\\\n", "\\n"),
                encoding="utf-8",
            )
            report = validate(path)
            self.assertEqual(report["folio_headers"], 4)
            self.assertEqual(report["folios_with_language"], 3)
            self.assertEqual(report["consistent_repeated_language_headers"], 1)

    def test_non_ascii_folio_digits_rejected_in_strict_audit(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "fixture.ivtff"
            path.write_text("<f١r> <! $L=A>\\n".replace("\\\\n", "\\n"), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid physical IVTFF folio header"):
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


    def test_invalid_or_malformed_currier_assignment_is_rejected(self):
        # Previously the legacy reader returned None for unsupported values,
        # and the strict audit silently skipped those page headers.
        for field in ("$L=C", "$L=", "$L=A $L=A", "$L=A$L=B"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as d:
                path = Path(d) / "fixture.ivtff"
                path.write_text(f"<f1r> <! {field}>\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, r"Invalid Currier \$L on f1r at line 1"):
                    validate(path)

    def test_invalid_assignment_cannot_erase_existing_valid_language(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "fixture.ivtff"
            path.write_text("<f1r> <! $L=A>\n<f1r> <! $L=C>\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, r"Invalid Currier \$L on f1r at line 2"):
                validate(path)

    def test_no_currier_field_remains_unclassified(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "fixture.ivtff"
            path.write_text("<f1r> <! $Q=A $I=B>\n", encoding="utf-8")
            report = validate(path)
            self.assertEqual(report["folios_with_language"], 0)


    def test_fake_line_boundaries_inside_comment_are_rejected(self):
        # str.splitlines() previously invented a second folio header here.
        for separator in ("\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"):
            with self.subTest(separator=repr(separator)), tempfile.TemporaryDirectory() as d:
                path = Path(d) / "fixture.ivtff"
                path.write_text(
                    "<f1r> <! $L=A>\n"
                    "<!editor" + separator + "<f1r> <! $L=B>\n",
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValueError, r"Non-physical IVTFF line separator at line 2"):
                    validate(path)

    def test_cr_lf_and_crlf_are_valid_physical_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "fixture.ivtff"
            path.write_bytes(
                b"<f1r> <! $L=A>\r\n<f2r> <! $L=B>\r<f3r> <! $L=A>\n"
            )
            report = validate(path)
            self.assertEqual(report["folio_headers"], 3)
            self.assertEqual(report["folios_with_language"], 3)


if __name__ == "__main__":
    unittest.main()
