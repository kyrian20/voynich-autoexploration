#!/usr/bin/env python3
"""Regression: --out must never replace an unselected canonical IVTFF corpus."""
import contextlib
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import audit_ivtff_minimum_format as auditor


class UnselectedCanonicalProtectionTests(unittest.TestCase):
    def test_output_aliases_unselected_canonical_corpus_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            canonical = folder / auditor.CORPORA[0]
            canonical.parent.mkdir(parents=True)
            original = b"#=IVTFF Eva- 2.0 M optional header extension\n<f1r>\n"
            canonical.write_bytes(original)
            other = folder / "other.ivtff"
            other.write_bytes(original)
            symlink = folder / "alias-symlink.json"
            symlink.symlink_to(canonical)
            hardlink = folder / "alias-hardlink.json"
            os.link(canonical, hardlink)

            for destination in (canonical, symlink, hardlink):
                with self.subTest(destination=destination):
                    argv = ["audit_ivtff_minimum_format.py", "--out",
                            str(destination), str(other)]
                    stderr, stdout = io.StringIO(), io.StringIO()
                    with patch.object(auditor, "ROOT", folder), \
                         patch.object(sys, "argv", argv), \
                         contextlib.redirect_stderr(stderr), \
                         contextlib.redirect_stdout(stdout):
                        status = auditor.main()
                    self.assertEqual(status, 2)
                    self.assertIn("Refusing --out", stderr.getvalue())
                    self.assertEqual(stdout.getvalue(), "")
                    self.assertEqual(canonical.read_bytes(), original)
                    self.assertEqual(other.read_bytes(), original)
                    self.assertEqual(destination.read_bytes(), original)
                    self.assertEqual(list(folder.glob(".ivtff-receipt-*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
