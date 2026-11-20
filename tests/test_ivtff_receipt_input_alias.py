#!/usr/bin/env python3
"""Regression: an IVTFF receipt must never destroy its own audited evidence."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_ivtff_minimum_format.py"
VALID = b"#=IVTFF Eva- 2.0 M optional header extension\n<f1r>\n"


class ReceiptInputAliasTests(unittest.TestCase):
    def run_audit(self, source: Path, output: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--out", str(output), str(source)],
            capture_output=True, text=True, check=False,
        )

    def test_direct_input_alias_rejected_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "corpus.txt"
            source.write_bytes(VALID)
            before = hashlib.sha256(source.read_bytes()).hexdigest()
            result = self.run_audit(source, source)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("Refusing to overwrite", result.stderr)
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)

    def test_symlink_input_alias_rejected_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "corpus.txt"
            source.write_bytes(VALID)
            output = Path(directory) / "receipt.json"
            try:
                output.symlink_to(source)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink unavailable: {exc}")
            result = self.run_audit(source, output)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(source.read_bytes(), VALID)

    def test_hardlink_input_alias_rejected_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "corpus.txt"
            source.write_bytes(VALID)
            output = Path(directory) / "receipt.json"
            try:
                os.link(source, output)
            except OSError as exc:
                self.skipTest(f"hardlink unavailable: {exc}")
            result = self.run_audit(source, output)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(source.read_bytes(), VALID)

    def test_independent_receipt_allowed_and_source_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "corpus.txt"
            source.write_bytes(VALID)
            output = Path(directory) / "receipt.json"
            result = self.run_audit(source, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"status": "PASS"', output.read_text(encoding="utf-8"))
            self.assertEqual(source.read_bytes(), VALID)


if __name__ == "__main__":
    unittest.main()
