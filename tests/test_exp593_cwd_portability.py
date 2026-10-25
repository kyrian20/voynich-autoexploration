#!/usr/bin/env python3
"""Regression: EXP-593 must resolve its frozen input outside repository cwd.

This is a read-only parser/provenance check. It does not rerun the historical
5,000-permutation experiment or replace any archived JSON/Markdown outputs.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/exp593_daiin_variants.py"
EXPECTED_SHA256 = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"


class Exp593CwdPortabilityTest(unittest.TestCase):
    def test_parse_from_unrelated_working_directory(self):
        # runpy imports the actual script without calling main() (which would
        # write dated artifacts and run 5,000 Monte Carlo permutations).
        program = """
import hashlib
import pathlib
import runpy
import sys
script = pathlib.Path(sys.argv[1]).resolve()
root = pathlib.Path(sys.argv[2]).resolve()
m = runpy.run_path(str(script), run_name='exp593_portability_test')
assert m['ROOT'] == root
assert m['SOURCE'] == root / 'data/transcriptions/eva_zl3b.txt'
assert m['OUT'] == root / 'research/experiments'
assert str(m['SOURCE'].relative_to(root)) == 'data/transcriptions/eva_zl3b.txt'
raw, lines = m['parse']()
assert hashlib.sha256(raw).hexdigest() == sys.argv[3]
assert len(lines) == 4188, len(lines)
assert sum(len(row['tokens']) for row in lines) == 32732
print('EXP-593: foreign-cwd parse, corpus SHA-256 and historical coverage OK')
"""
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse((Path(tmp) / "data/transcriptions/eva_zl3b.txt").exists())
            completed = subprocess.run(
                [sys.executable, "-c", program, str(SCRIPT), str(ROOT), EXPECTED_SHA256],
                cwd=tmp,
                capture_output=True,
                text=True,
                check=False,
                timeout=45,
            )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("historical coverage OK", completed.stdout)


if __name__ == "__main__":
    unittest.main()
