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


if __name__ == "__main__":
    unittest.main()
