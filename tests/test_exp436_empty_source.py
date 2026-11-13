"""Fail-closed regression: an empty comparison corpus cannot be approved by hash alone."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts.check_exp436_source_provenance import evaluate


class EmptyCorpusRegression(unittest.TestCase):
    def test_empty_latin_is_rejected_even_with_matching_approved_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            latin = Path(directory) / "latin.txt"
            italian = Path(directory) / "italian.txt"
            latin.write_bytes(b"")
            italian.write_bytes(b"synthetic Italian control")
            before = (latin.read_bytes(), italian.read_bytes())
            approved = {
                "latin": hashlib.sha256(before[0]).hexdigest(),
                "italian": hashlib.sha256(before[1]).hexdigest(),
            }
            result = evaluate(latin, italian, approved)
            self.assertFalse(result["ok"])
            self.assertEqual(result["sources"]["latin"]["status"], "EMPTY_SOURCE")
            self.assertEqual(result["sources"]["italian"]["status"], "HASH_MATCH")
            self.assertEqual((latin.read_bytes(), italian.read_bytes()), before)


if __name__ == "__main__":
    unittest.main()
