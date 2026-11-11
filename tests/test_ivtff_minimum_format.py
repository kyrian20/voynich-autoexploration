#!/usr/bin/env python3
"""Synthetic guards for the narrow IVTFF file-level minimum audit."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_ivtff_minimum_format import audit_bytes


VALID_HEADER = b"#=IVTFF Eva- 2.0 M optional header extension"


class IvtffMinimumFormatTests(unittest.TestCase):
    def test_accepts_minimum_header_trailer_and_ascii_data(self):
        report = audit_bytes(VALID_HEADER + b"\n<f1r>\n<f1r.1,@P0> daiin\n")
        self.assertEqual(report["status"], "PASS", report)
        self.assertEqual(report["maximum_line_chars"], len(VALID_HEADER))

    def test_accepts_each_physical_newline_form(self):
        for ending in (b"\n", b"\r", b"\r\n"):
            with self.subTest(ending=ending):
                report = audit_bytes(VALID_HEADER + ending + b"<f1r>" + ending)
                self.assertEqual(report["status"], "PASS", report)

    def test_accepts_exactly_2048_characters_and_rejects_2049(self):
        accepted = audit_bytes(VALID_HEADER + b"\n" + b"x" * 2048)
        rejected = audit_bytes(VALID_HEADER + b"\n" + b"x" * 2049)
        self.assertEqual(accepted["status"], "PASS", accepted)
        self.assertIn("line_too_long", {e["code"] for e in rejected["errors"]})

    def test_rejects_non_ascii_and_control_bytes_inside_lines(self):
        non_ascii = audit_bytes(VALID_HEADER + b"\n" + "é".encode("utf-8"))
        vertical_tab = audit_bytes(VALID_HEADER + b"\n" + b"a\vb")
        tab = audit_bytes(VALID_HEADER + b"\n" + b"a\tb")
        self.assertIn("non_ascii_byte", {e["code"] for e in non_ascii["errors"]})
        self.assertIn("control_byte_in_line", {e["code"] for e in vertical_tab["errors"]})
        self.assertIn("control_byte_in_line", {e["code"] for e in tab["errors"]})

    def test_rejects_short_or_malformed_header(self):
        for raw in (b"#=IVTFF Eva- 2.0", b"#=IVTFF Eva- 2.X M", b" #=IVTFF Eva- 2.0 M"):
            with self.subTest(raw=raw):
                report = audit_bytes(raw + b"\n")
                self.assertNotEqual(report["status"], "PASS", report)


if __name__ == "__main__":
    unittest.main()
