"""EXP-436: approved digests cannot bypass strict UTF-8 decoding."""
import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.check_exp436_source_provenance import evaluate, inspect


class UTF8SourceGateTests(unittest.TestCase):
    def test_invalid_utf8_rejected_even_with_matching_digest(self):
        with tempfile.TemporaryDirectory() as d:
            latin, italian = Path(d) / "latin.txt", Path(d) / "italian.txt"
            latin.write_bytes(b"latin\xfftext")
            italian.write_bytes("città".encode("utf-8"))
            approved = {
                "latin": hashlib.sha256(latin.read_bytes()).hexdigest(),
                "italian": hashlib.sha256(italian.read_bytes()).hexdigest(),
            }
            result = evaluate(latin, italian, approved)
            self.assertFalse(result["ok"])
            self.assertEqual(result["sources"]["latin"]["status"], "INVALID_ENCODING")
            self.assertEqual(result["sources"]["italian"]["status"], "HASH_MATCH")

    def test_truncated_multibyte_sequence_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "truncated.txt"
            path.write_bytes(b"latin " + b"\xe2\x82")
            self.assertEqual(inspect(path)["status"], "INVALID_ENCODING")

    def test_valid_utf8_split_across_read_chunks(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "boundary.txt"
            path.write_bytes(b"a" * (1024 * 1024 - 1) + "é".encode("utf-8") + b"z")
            self.assertEqual(inspect(path)["status"], "UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
