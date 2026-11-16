"""Offline regressions for the exact-head IVTFF receipt verifier.

Fixtures are synthetic; the historical artifact and source corpora are never
rewritten. SHA-256 of the fixture ZIP is passed explicitly to verify().
"""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research/maintenance/verify_pr287_ivtff_artifact.py"
spec = importlib.util.spec_from_file_location("ivtff_receipt_verifier", SCRIPT)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


def fixture(records=None, *, audit="IVTFF file-level minimums", status="PASS",
            corrupt_manifest=False, extra_member=False):
    if records is None:
        records = [
            {"source": source, "sha256": digest, "status": "PASS", "errors": []}
            for source, digest in verifier.SOURCES.items()
        ]
    payload = json.dumps({"audit": audit, "status": status, "files": records},
                         sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    if corrupt_manifest:
        digest = "0" * 64
    manifest = (digest + "  ivtff-minimum-format.json\n").encode("ascii")
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("ivtff-minimum-format.json", payload)
        z.writestr("ivtff-minimum-format.sha256", manifest)
        if extra_member:
            z.writestr("unexpected.txt", b"extra")
    return stream.getvalue()


class ReceiptRegression(unittest.TestCase):
    def check(self, archive, *, expected_sha=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipt.zip"
            path.write_bytes(archive)
            sha = expected_sha or hashlib.sha256(archive).hexdigest()
            return verifier.verify(path, expected_zip_sha=sha)

    def test_valid_synthetic_receipt(self):
        result = self.check(fixture())
        self.assertEqual(result["status"], "VERIFIED_RECEIPT_ONLY")
        self.assertEqual(result["corpus_sha256"], verifier.SOURCES)

    def test_outer_zip_digest_mismatch(self):
        with self.assertRaisesRegex(ValueError, "ZIP SHA-256 mismatch"):
            self.check(fixture(), expected_sha="0" * 64)

    def test_inner_digest_mismatch(self):
        with self.assertRaisesRegex(ValueError, "inner JSON SHA-256 mismatch"):
            self.check(fixture(corrupt_manifest=True))

    def test_extra_zip_member(self):
        with self.assertRaisesRegex(ValueError, "unexpected ZIP members"):
            self.check(fixture(extra_member=True))

    def test_duplicate_source(self):
        source, digest = next(iter(verifier.SOURCES.items()))
        records = [{"source": source, "sha256": digest, "status": "PASS", "errors": []}] * 3
        with self.assertRaisesRegex(ValueError, "unknown or duplicate source"):
            self.check(fixture(records))

    def test_bad_corpus_digest(self):
        records = [
            {"source": source, "sha256": "0" * 64 if i == 0 else digest,
             "status": "PASS", "errors": []}
            for i, (source, digest) in enumerate(verifier.SOURCES.items())
        ]
        with self.assertRaisesRegex(ValueError, "corpus digest/status mismatch"):
            self.check(fixture(records))

    def test_report_failure(self):
        with self.assertRaisesRegex(ValueError, "unexpected audit/status"):
            self.check(fixture(status="FAIL"))


if __name__ == "__main__":
    unittest.main()
