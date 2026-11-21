"""Regression: EXP-173 frozen receipt permits only the pinned IVTFF reader repair.

No historical output or source corpus is rewritten. Synthetic snapshot inputs only.
"""
import contextlib
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_exp173_reader_bridge.py"
spec = importlib.util.spec_from_file_location("exp173_reader_bridge_provenance", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
KEY = "scripts/audit_ivtff_metadata.py"
OLD = "c01c335b1727f53369caba468e366d4d539b63e96c2db84c75a071b2e54c0116"
NEW = "1a7c42fddd37e466c8b0891137d4a8db80d7ad68d5fcac745b108a8fc417b7e5"


class TestReaderBridgeReceipt(unittest.TestCase):
    def test_pinned_repair_sha_matches_actual_source(self):
        self.assertEqual(hashlib.sha256((ROOT / KEY).read_bytes()).hexdigest(), NEW)

    def check_snapshot(self, new_digest=NEW, altered=False, old_digest=OLD):
        archived = {"dependencies_sha256": {KEY: old_digest}, "files": [{"tokens": 5}]}
        actual = {"dependencies_sha256": {KEY: new_digest},
                  "files": [{"tokens": 6 if altered else 5}]}
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "results.json").write_text(json.dumps(archived), encoding="utf-8")
            (folder / "changed-rows.json.gz").write_bytes(
                gzip.compress(b"{}"))
            with (patch.object(module, "run", return_value=(actual, {})),
                  patch.object(sys, "argv", ["audit_exp173_reader_bridge.py", "--check", str(folder)]),
                  contextlib.redirect_stdout(io.StringIO())):
                module.main()

    def test_only_pinned_reader_digest_drift_is_accepted(self):
        self.check_snapshot()

    def test_scientific_value_drift_is_rejected(self):
        with self.assertRaisesRegex(SystemExit, "Snapshot mismatch: results.json"):
            self.check_snapshot(altered=True)

    def test_unapproved_new_digest_is_rejected(self):
        with self.assertRaisesRegex(SystemExit, "Snapshot mismatch: results.json"):
            self.check_snapshot(new_digest="0" * 64)

    def test_unapproved_historical_digest_is_rejected(self):
        with self.assertRaisesRegex(SystemExit, "Snapshot mismatch: results.json"):
            self.check_snapshot(old_digest="f" * 64)


if __name__ == "__main__":
    unittest.main()
