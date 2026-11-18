"""Synthetic regression: reject unsupported compression in either receipt member.

The #307 fixture mutates only the JSON member. This independently exercises
the manifest member and confirms the verifier fails closed before interpreting
its contents. No historical receipt or corpus is changed.
"""
from contextlib import redirect_stderr
import hashlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research/maintenance/verify_pr287_ivtff_artifact.py"
spec = importlib.util.spec_from_file_location("ivtff_both_member_methods", SCRIPT)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class UnsupportedMethodByMember(unittest.TestCase):
    def test_each_member_consistent_unsupported_method_is_rejected(self):
        payload = b'{"audit":"IVTFF file-level minimums","status":"PASS","files":[]}'
        manifest = hashlib.sha256(payload).hexdigest().encode("ascii") + b"  ivtff-minimum-format.json\n"
        names = ("ivtff-minimum-format.json", "ivtff-minimum-format.sha256")
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(names[0], payload)
            archive.writestr(names[1], manifest)
        original = stream.getvalue()
        with zipfile.ZipFile(io.BytesIO(original)) as archive:
            local_offsets = [archive.getinfo(name).header_offset for name in names]
        # Two central directory records; do not confuse local-header offsets.
        central_offsets = []
        cursor = 0
        for _ in names:
            position = original.find(b"PK\x01\x02", cursor)
            self.assertGreaterEqual(position, 0)
            central_offsets.append(position)
            cursor = position + 4
        self.assertEqual(len(set(local_offsets)), 2)
        self.assertEqual(len(set(central_offsets)), 2)
        with tempfile.TemporaryDirectory() as directory:
            for index, name in enumerate(names):
                with self.subTest(member=name):
                    data = bytearray(original)
                    local = local_offsets[index]
                    central = central_offsets[index]
                    self.assertEqual(data[local:local + 4], b"PK\x03\x04")
                    self.assertEqual(data[central:central + 4], b"PK\x01\x02")
                    data[local + 8:local + 10] = (99).to_bytes(2, "little")
                    data[central + 10:central + 12] = (99).to_bytes(2, "little")
                    mutated = bytes(data)
                    path = Path(directory) / f"unsupported-{index}.zip"
                    path.write_bytes(mutated)
                    stderr = io.StringIO()
                    with patch.object(verifier, "ZIP_SHA", hashlib.sha256(mutated).hexdigest()), \
                         patch.object(sys, "argv", [str(SCRIPT), str(path)]), \
                         redirect_stderr(stderr):
                        self.assertEqual(verifier.main(), 1)
                    diagnostic = stderr.getvalue()
                    self.assertIn("REJECTED:", diagnostic)
                    self.assertIn("compression method is not supported", diagnostic)
                    self.assertNotIn("header mismatch", diagnostic)
                    self.assertNotIn("Traceback", diagnostic)


if __name__ == "__main__":
    unittest.main()
