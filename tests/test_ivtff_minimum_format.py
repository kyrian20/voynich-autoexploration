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
        delete = audit_bytes(VALID_HEADER + b"\n" + b"a\x7fb")
        self.assertIn("non_ascii_byte", {e["code"] for e in non_ascii["errors"]})
        self.assertIn("control_byte_in_line", {e["code"] for e in vertical_tab["errors"]})
        self.assertIn("control_byte_in_line", {e["code"] for e in tab["errors"]})
        self.assertIn("control_byte_in_line", {e["code"] for e in delete["errors"]})

    def test_reports_both_independent_byte_error_classes_on_same_line(self):
        # Previous scanner stopped at the first bad byte and hid the TAB.
        report = audit_bytes(VALID_HEADER + b"\n" + b"a\xc3\xa9b\tc")
        self.assertEqual(report["status"], "FAIL")
        errors = [e for e in report["errors"] if e.get("line") == 2]
        self.assertEqual([(e["code"], e["column"]) for e in errors],
                         [("non_ascii_byte", 2), ("control_byte_in_line", 5)])

    def test_reports_one_error_per_class_per_line_not_per_byte(self):
        report = audit_bytes(VALID_HEADER + b"\n" + b"\xc3\xa9\xff\t\x7f")
        self.assertEqual([e["code"] for e in report["errors"]],
                         ["non_ascii_byte", "control_byte_in_line"])

    def test_reports_control_before_non_ascii_and_resets_per_line(self):
        # Reverse ordering is a separate scanner path: a control byte must
        # not hide a later non-ASCII byte, and state must reset at CRLF.
        report = audit_bytes(VALID_HEADER + b"\r\n" + b"a\tb\xff" + b"\r\n" + b"\x7fc\xc3")
        self.assertEqual(report["status"], "FAIL")
        errors = [(e["line"], e["code"], e["column"]) for e in report["errors"]]
        self.assertEqual(errors, [
            (2, "control_byte_in_line", 2),
            (2, "non_ascii_byte", 4),
            (3, "control_byte_in_line", 1),
            (3, "non_ascii_byte", 3),
        ])

    def test_rejects_short_or_malformed_header(self):
        for raw in (b"#=IVTFF Eva- 2.0", b"#=IVTFF Eva- 2.X M", b" #=IVTFF Eva- 2.0 M"):
            with self.subTest(raw=raw):
                report = audit_bytes(raw + b"\n")
                self.assertNotEqual(report["status"], "PASS", report)


if __name__ == "__main__":
    unittest.main()
