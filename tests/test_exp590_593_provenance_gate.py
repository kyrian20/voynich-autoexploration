"""Synthetic regression tests; never substitute these for historical reproduction."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from research.maintenance.check_exp590_593_reproduction import FILES, inspect

class ProvenanceGateTests(unittest.TestCase):
    def test_missing_attestations_and_mutated_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            source.write_bytes(b"original")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            for name in FILES:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({"source": "source.txt", "source_sha256": digest}), encoding="utf-8")
            issues = inspect(root)
            self.assertEqual(len(issues), 12)
            self.assertEqual(sum("no attested" in issue for issue in issues), 12)
            source.write_bytes(b"altered")
            issues = inspect(root)
            self.assertEqual(sum("source SHA-256 mismatch" in issue for issue in issues), 2)

    def test_malformed_record_and_digest_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            source.write_bytes(b"original")
            for name, payload in zip(FILES, ([], {"source": "source.txt", "source_sha256": []})):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload), encoding="utf-8")
            issues = inspect(root)
            self.assertTrue(any("must be an object" in issue for issue in issues))
            self.assertTrue(any("source path or SHA-256 absent" in issue for issue in issues))

    def test_two_unhashable_digests_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.txt").write_bytes(b"original")
            for name in FILES:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({"source": "source.txt", "source_sha256": []}), encoding="utf-8")
            issues = inspect(root)
            self.assertEqual(sum("source path or SHA-256 absent" in issue for issue in issues), 2)

    def test_missing_json_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(len(inspect(Path(directory))), 2)

if __name__ == "__main__":
    unittest.main()
