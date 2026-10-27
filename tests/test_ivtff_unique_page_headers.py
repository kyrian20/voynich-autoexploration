"""Synthetic duplicate-header regressions for the additive Currier preflight.

Do not modify or rebaseline EXP-173 historical dependency snapshots.
"""
import unittest
from pathlib import Path

from scripts.audit_ivtff_unique_page_headers import audit_unique_page_headers
from scripts.audit_ivtff_metadata import SOURCE


class UniqueFolioHeaderTests(unittest.TestCase):
    def test_valid_independent_pages(self):
        text = "<f1r> <! $L=A>\n<f67r1> <! $L=B>\n<fRos> <! $Q=A>\n"
        result = audit_unique_page_headers(text)
        self.assertEqual(result["folio_headers"], 3)
        self.assertEqual(result["distinct_folio_ids"], 3)

    def test_repeated_pages_fail_even_with_identical_or_missing_language(self):
        for page in ("f1r", "f67r1", "fRos"):
            for first in ("<! $L=A>", "<! $Q=A>"):
                for second in ("<! $L=A>", "<! $L=B>"):
                    with self.subTest(page=page, first=first, second=second):
                        text = f"<{page}> {first}\n<{page}> {second}\n"
                        with self.assertRaisesRegex(
                            ValueError, f"Duplicate IVTFF folio header {page} at line 2"
                        ):
                            audit_unique_page_headers(text)

    def test_archived_source_census_unchanged(self):
        source = SOURCE.read_bytes().decode("utf-8-sig")
        result = audit_unique_page_headers(source)
        self.assertEqual(result["folio_headers"], 227)
        self.assertEqual(result["distinct_folio_ids"], 227)


    def test_fake_line_boundaries_inside_comment_are_rejected(self):
        # Never promote a Unicode/control separator to a physical header.
        for separator in ("\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"):
            with self.subTest(separator=repr(separator)):
                text = "<f1r> <! $L=A>\n<!editor" + separator + "<f2r> <! $L=B>\n"
                with self.assertRaisesRegex(ValueError, r"Non-physical IVTFF line separator at line 2"):
                    audit_unique_page_headers(text)

    def test_cr_lf_and_crlf_are_valid_physical_boundaries(self):
        text = "<f1r> <! $L=A>\r\n<f2r> <! $L=B>\r<f3r> <! $L=A>\n"
        result = audit_unique_page_headers(text)
        self.assertEqual(result["folio_headers"], 3)


if __name__ == "__main__":
    unittest.main()
