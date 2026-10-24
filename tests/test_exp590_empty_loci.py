#!/usr/bin/env python3
"""Synthetic regressions for raw-nonempty/ASCII-empty locus reconciliation."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_exp590_empty_loci import inspect_text


class TestExp590EmptyLoci(unittest.TestCase):
    def test_explains_dropped_but_nonempty_loci(self):
        text = ("<f1r> <! $L=A>\n"
                "<f1r.1,@P0> daiin.ol\n"
                "<f1r.2,@P0> <%><$>\n"
                "<f1r.3,@P0> {ch}\n"
                "<f1r.4,@P0> [x:y]\n"
                "<f1r.5,@P0> @140\n"
                "<fRos> <! $L=B>\n"
                "<fRos.23,@L0> daiin\n")
        report, selected = inspect_text(text)
        self.assertEqual(selected, [("f1r", 1), ("fRos", 23)])
        self.assertEqual((report["records_with_nonempty_raw_body"],
                          report["records_with_ascii_tokens"],
                          report["records_with_no_ascii_tokens"],
                          report["tokens"], report["exact_daiin_occurrences"]),
                         (6, 2, 4, 3, 2))
        self.assertEqual([x["tag"] for x in report["empty_loci"]],
                         ["f1r.2,@P0", "f1r.3,@P0", "f1r.4,@P0", "f1r.5,@P0"])
        self.assertTrue(all(len(x["body_sha256"]) == 64 for x in report["empty_loci"]))

    def test_empty_raw_body_not_confused_with_filtered_body(self):
        report, selected = inspect_text("<f1r.1,@P0>   \n<f1r.2,@P0> {ch}\n")
        self.assertEqual(selected, [])
        self.assertEqual(report["records_with_nonempty_raw_body"], 1)
        self.assertEqual(report["records_with_no_ascii_tokens"], 1)


if __name__ == "__main__":
    unittest.main()
