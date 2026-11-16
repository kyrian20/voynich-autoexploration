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
            corrupt_manifest=False, extra_member=False, raw_payload=None,
            manifest_target="ivtff-minimum-format.json"):
    if records is None:
        records = [
            {"source": source, "sha256": digest, "status": "PASS", "errors": []}
            for source, digest in verifier.SOURCES.items()
        ]
    payload = json.dumps({"audit": audit, "status": status, "files": records},
                         sort_keys=True).encode("utf-8")
    if raw_payload is not None:
        payload = raw_payload
    digest = hashlib.sha256(payload).hexdigest()
    if corrupt_manifest:
        digest = "0" * 64
    manifest = (digest + "  " + manifest_target + "\n").encode("ascii")
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

    def test_rejects_top_level_json_list(self):
        with self.assertRaisesRegex(ValueError, "invalid report object"):
            self.check(fixture(raw_payload=b"[]"))

    def test_rejects_non_object_file_record(self):
        records = [
            {"source": source, "sha256": digest, "status": "PASS", "errors": []}
            for source, digest in verifier.SOURCES.items()
        ]
        records[1] = "malformed-record"
        with self.assertRaisesRegex(ValueError, "invalid file record"):
            self.check(fixture(records))

    def test_rejects_duplicate_json_key(self):
        # The former json.loads last-value-wins parser incorrectly accepted
        # this conflicting FAIL then PASS report with otherwise valid records.
        valid_report = json.dumps({
            "audit": "IVTFF file-level minimums", "status": "PASS",
            "files": [
                {"source": source, "sha256": digest,
                 "status": "PASS", "errors": []}
                for source, digest in verifier.SOURCES.items()
            ],
        }).encode("utf-8")
        payload = b'{"status":"FAIL",' + valid_report[1:]
        with self.assertRaisesRegex(ValueError, "duplicate JSON field"):
            self.check(fixture(raw_payload=payload))

    def test_rejects_nonfinite_json_constant(self):
        # Python json.loads normally accepts NaN/Infinity despite JSON RFC 8259.
        # An unrelated metadata field must not make a receipt non-portable.
        valid = json.loads(json.dumps({
            "audit": "IVTFF file-level minimums", "status": "PASS",
            "files": [{"source": source, "sha256": digest,
                       "status": "PASS", "errors": []}
                      for source, digest in verifier.SOURCES.items()],
        }))
        for constant in (b"NaN", b"Infinity", b"-Infinity"):
            with self.subTest(constant=constant):
                payload = json.dumps(valid).encode("utf-8")
                payload = payload[:-1] + b',"untrusted_metric":' + constant + b'}'
                with self.assertRaisesRegex(ValueError, "non-finite JSON constant"):
                    self.check(fixture(raw_payload=payload))

    def test_rejects_manifest_path_alias(self):
        with self.assertRaisesRegex(ValueError, "invalid inner manifest"):
            self.check(fixture(manifest_target="../ivtff-minimum-format.json"))

    def test_accepts_historical_runner_manifest_target(self):
        result = self.check(fixture(
            manifest_target="/home/runner/work/_temp/ivtff-minimum-format.json"))
        self.assertEqual(result["status"], "VERIFIED_RECEIPT_ONLY")

    def test_deeply_nested_json_cli_rejects_cleanly(self):
        # A checksum-consistent JSON payload can exceed Python's parser depth.
        # Verify the actual CLI error boundary, not merely json.loads itself.
        from contextlib import redirect_stderr
        from unittest.mock import patch
        # Parser nesting limits vary by Python build/version. Inject the exact
        # parser exception to test the CLI boundary deterministically.
        archive = fixture()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "deep.zip"
            path.write_bytes(archive)
            error = io.StringIO()
            with patch.object(verifier, "ZIP_SHA", hashlib.sha256(archive).hexdigest()), \
                 patch.object(verifier.json, "loads", side_effect=RecursionError("maximum recursion depth exceeded")), \
                 patch("sys.argv", ["verify_pr287_ivtff_artifact.py", str(path)]), \
                 redirect_stderr(error):
                self.assertEqual(verifier.main(), 1)
            self.assertIn("REJECTED:", error.getvalue())
            self.assertIn("maximum recursion depth", error.getvalue())

    def test_rejects_oversized_receipt_before_decompression(self):
        # Synthetic valid-looking JSON with an oversized irrelevant field.
        payload = json.dumps({
            "audit": "IVTFF file-level minimums", "status": "PASS",
            "files": [{"source": source, "sha256": digest,
                       "status": "PASS", "errors": []}
                      for source, digest in verifier.SOURCES.items()],
            "padding": "x" * verifier.MAX_MEMBER_BYTES,
        }).encode("utf-8")
        with self.assertRaisesRegex(ValueError, "oversized ZIP member"):
            self.check(fixture(raw_payload=payload))

    def test_rejects_oversized_manifest(self):
        # Correct ZIP checksum must not permit unbounded manifest reads.
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("ivtff-minimum-format.json", b"{}")
            z.writestr("ivtff-minimum-format.sha256", b"x" * 4097)
        with self.assertRaisesRegex(ValueError, "oversized ZIP member"):
            self.check(stream.getvalue())

    def test_report_failure(self):
        with self.assertRaisesRegex(ValueError, "unexpected audit/status"):
            self.check(fixture(status="FAIL"))


if __name__ == "__main__":
    unittest.main()
