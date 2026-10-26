"""Synthetic ASCII-identifier regressions for two derived IVTFF readers.

These tests do not edit or reinterpret frozen manuscript transcriptions.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

from scripts import audit_research_readiness as readiness
from scripts.ivtff_lossless import lex, tokens

ROOT = Path(__file__).resolve().parents[1]
ANCHOR = runpy.run_path(str(ROOT / "research/decipherment/2026-10-26-astronomical-anchor/run.py"))
ANCHOR_INVENTORY = ANCHOR["inventory"]
ANCHOR_EXPECTED = ANCHOR_INVENTORY.__globals__["EXPECTED"]

VALID = "<f68r3.11,@Ls> doaro\n<fRos.1,@L0> dary\n"
BAD = (
    "<f٦٨r3.12,@Ls> doary\n",   # Unicode page number
    "<f68r3.١٢,@Ls> doary\n",   # Unicode record number
    "<fRos.١,@L0> doary\n",     # Unicode number on a named page
)


class DerivedReaderAsciiTests(unittest.TestCase):
    def scan_anchor(self, content: str):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fixture.txt"
            path.write_text(content, encoding="utf-8")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            with patch.dict(ANCHOR_EXPECTED, {"fixture.txt": digest}):
                return ANCHOR_INVENTORY(path, lex, tokens)

    def scan_readiness(self, content: str):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            directory = root / "data" / "transcriptions"
            directory.mkdir(parents=True)
            (directory / "fixture.txt").write_text(content, encoding="utf-8")
            with patch.object(readiness, "ROOT", root):
                return readiness.audit_source("fixture", "fixture.txt")

    def test_valid_ascii_identifiers_remain_accepted(self):
        anchor = self.scan_anchor(VALID)
        self.assertEqual((anchor["numeric_records"], anchor["named_records"]), (1, 1))
        readiness_result = self.scan_readiness(VALID)
        self.assertEqual(readiness_result["records"], 2)

    def test_unicode_decimal_identifier_fails_closed_in_both_readers(self):
        for bad in BAD:
            with self.subTest(bad=bad):
                text = VALID + bad
                with self.assertRaisesRegex(ValueError, "Non-ASCII decimal digit"):
                    self.scan_anchor(text)
                with self.assertRaisesRegex(ValueError, "Non-ASCII decimal digit"):
                    self.scan_readiness(text)

    def test_regex_does_not_accept_unicode_decimal_ids(self):
        for bad in BAD:
            with self.subTest(bad=bad):
                self.assertIsNone(ANCHOR_INVENTORY.__globals__["ROW"].match(bad))
                self.assertIsNone(readiness.ROW.match(bad))


if __name__ == "__main__":
    unittest.main()
