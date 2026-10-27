#!/usr/bin/env python3
"""Fail-closed physical-row boundaries in the IVTFF structural auditor.

These are synthetic regression fixtures, not evidence of corruption in any
historical transcription. No random draws or corpus mutation are involved.
"""
import unittest

from scripts.audit_ivtff_page_locus_ids import (
    NON_PHYSICAL_SEPARATORS, audit_text, structural_errors,
)


class PhysicalRowBoundaryTests(unittest.TestCase):
    def test_unicode_separator_cannot_forge_a_page_header(self):
        # Under str.splitlines(), each separator manufactures a second
        # apparent page header from text physically inside a comment.
        for separator in NON_PHYSICAL_SEPARATORS:
            with self.subTest(codepoint=f"U+{ord(separator):04X}"):
                text = (
                    "<f1r> <! $L=A>\n"
                    "<f1r.1,@P0> daiin\n"
                    "# comment" + separator + "<f2r> <! $L=B>\n"
                    "<f2r.1,@P0> chedy\n"
                )
                report = audit_text(text)
                self.assertEqual(report["page_header_count"], 1)
                self.assertEqual(report["record_count"], 2)
                self.assertEqual(report["invalid_physical_separator_count"], 1)
                self.assertEqual(report["invalid_physical_separators"], [{
                    "line": 3,
                    "codepoints": [f"U+{ord(separator):04X}"],
                }])
                self.assertEqual(report["page_mismatch_count"], 1)
                self.assertIn(
                    "invalid_physical_separator_count=1",
                    structural_errors(report),
                )

    def test_bad_separator_inside_header_never_activates_page(self):
        text = (
            "<f1r> <! $L=A>\n"
            "<f1r.1,@P0> daiin\n"
            "<f2r> <! $L=B\u2028>\n"
            "<f2r.1,@P0> chedy\n"
        )
        report = audit_text(text)
        self.assertEqual(report["page_header_count"], 1)
        self.assertEqual(report["invalid_physical_separator_count"], 1)
        self.assertEqual(report["page_mismatch_count"], 1)
        self.assertTrue(structural_errors(report))

    def test_cr_lf_crlf_remain_valid_physical_line_endings(self):
        for ending in ("\n", "\r", "\r\n"):
            with self.subTest(ending=repr(ending)):
                text = ending.join([
                    "<f1r> <! $L=A>",
                    "<f1r.1,@P0> daiin",
                    "<f2r> <! $L=B>",
                    "<f2r.1,@P0> chedy",
                ])
                report = audit_text(text)
                self.assertEqual(report["page_header_count"], 2)
                self.assertEqual(report["record_count"], 2)
                self.assertEqual(report["invalid_physical_separator_count"], 0)
                self.assertEqual(structural_errors(report), [])

    def test_diagnostic_preview_is_bounded_but_total_is_exact(self):
        text = "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n" + (
            "# invalid\u2028hidden\n" * 51
        )
        report = audit_text(text)
        self.assertEqual(report["invalid_physical_separator_count"], 51)
        self.assertEqual(len(report["invalid_physical_separators"]), 50)
        self.assertIn("invalid_physical_separator_count=51", structural_errors(report))

    def test_unicode_comment_without_separator_is_not_rejected(self):
        text = "<f1r> <! caf\u00e9 $L=A>\n<f1r.1,@P0> daiin"
        report = audit_text(text)
        self.assertEqual(structural_errors(report), [])


if __name__ == "__main__":
    unittest.main()
