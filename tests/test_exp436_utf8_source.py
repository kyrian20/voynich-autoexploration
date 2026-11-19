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


    def test_unicode_whitespace_only_rejected_with_matching_digest(self):
        with tempfile.TemporaryDirectory() as d:
            latin, italian = Path(d) / "latin.txt", Path(d) / "italian.txt"
            latin.write_text("\u00a0\u2003\u3000", encoding="utf-8")
            italian.write_text("testo italiano", encoding="utf-8")
            approved = {
                "latin": hashlib.sha256(latin.read_bytes()).hexdigest(),
                "italian": hashlib.sha256(italian.read_bytes()).hexdigest(),
            }
            result = evaluate(latin, italian, approved)
            self.assertFalse(result["ok"])
            self.assertEqual(result["sources"]["latin"]["status"], "BLANK_SOURCE")
            self.assertEqual(result["sources"]["italian"]["status"], "HASH_MATCH")

    def test_unicode_whitespace_split_across_chunks(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "boundary_blank.txt"
            path.write_bytes(b" " * (1024 * 1024 - 1) + "\u3000".encode("utf-8"))
            self.assertEqual(inspect(path)["status"], "BLANK_SOURCE")

    def test_unicode_whitespace_then_real_text_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "nonblank.txt"
            path.write_text("\u00a0\u2003parola", encoding="utf-8")
            self.assertEqual(inspect(path)["status"], "UNVERIFIED")


    def test_format_only_corpus_rejected_despite_approved_digest(self):
        with tempfile.TemporaryDirectory() as d:
            latin, italian = Path(d) / "latin.txt", Path(d) / "italian.txt"
            latin.write_text("\ufeff\u200b\u200d\u2060", encoding="utf-8")
            italian.write_text("testo italiano", encoding="utf-8")
            approved = {
                "latin": hashlib.sha256(latin.read_bytes()).hexdigest(),
                "italian": hashlib.sha256(italian.read_bytes()).hexdigest(),
            }
            result = evaluate(latin, italian, approved)
            self.assertFalse(result["ok"])
            self.assertEqual(result["sources"]["latin"]["status"], "BLANK_SOURCE")
            self.assertEqual(result["sources"]["italian"]["status"], "HASH_MATCH")

    def test_format_only_crosses_read_boundary(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "boundary_format.txt"
            path.write_bytes(b" " * (1024 * 1024 - 1) + "\u200b".encode("utf-8"))
            self.assertEqual(inspect(path)["status"], "BLANK_SOURCE")

    def test_real_text_with_bom_and_joiners_remains_eligible(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "real_text.txt"
            path.write_text("\ufeff\u200bparola\u200d", encoding="utf-8")
            self.assertEqual(inspect(path)["status"], "UNVERIFIED")

if __name__ == "__main__":
    unittest.main()
