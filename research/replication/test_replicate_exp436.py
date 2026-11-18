"""Tests for replicate_exp436.py; run: python -m unittest discover -s research/replication -p 'test_*.py'."""
import tempfile
import unittest
from pathlib import Path
import replicate_exp436 as m

class TestReplication(unittest.TestCase):
    def test_classes(self):
        r = m.analyze(["aa"] * 5 + ["bbbb", "cccc", "cccc"])
        self.assertEqual(r["class_tokens"], {"hapax": 1, "mid": 2, "frequent": 5})
        self.assertAlmostEqual(r["hapax_frequent_ratio"], 2)
    def test_empty(self):
        self.assertIsNone(m.analyze([])["hapax_frequent_ratio"])
    def test_markers(self):
        text = "header\n*** START OF THE PROJECT GUTENBERG EBOOK X ***\nAA BBBB\n*** END OF THE PROJECT GUTENBERG EBOOK X ***\nfooter"
        self.assertEqual(m.body(text).strip(), "AA BBBB")
        with self.assertRaises(ValueError):
            m.body("missing boundaries")
    def test_unicode_letters(self):
        self.assertEqual(m.TOKEN.findall("für Größe città 123 abc_123"), ["für", "Größe", "città", "abc"])
    def test_missing_french_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            for lang, rel in m.SOURCES.items():
                if lang == "french":
                    continue
                p = Path(tmp) / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("*** START OF THE PROJECT GUTENBERG EBOOK X ***\\naa aa aa aa aa bbbb\\n*** END OF THE PROJECT GUTENBERG EBOOK X ***", encoding="utf-8")
            r = m.run(Path(tmp))
            self.assertEqual(r["corpora"]["french"]["status"], "unavailable")
            self.assertEqual(r["corpora"]["german"]["tokens"], 6)
    def test_legacy_cp1252_decoding(self):
        with tempfile.TemporaryDirectory() as tmp:
            for lang, rel in m.SOURCES.items():
                if lang == "french":
                    continue
                p = Path(tmp) / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                sample = "*** START OF THE PROJECT GUTENBERG EBOOK X ***\\nélève élève élève élève élève naïve\\n*** END OF THE PROJECT GUTENBERG EBOOK X ***"
                p.write_bytes(sample.encode("cp1252" if lang == "latin" else "utf-8"))
            r = m.run(Path(tmp))
            self.assertEqual(r["corpora"]["latin"]["decoded_as"], "cp1252")
            self.assertEqual(r["corpora"]["latin"]["tokens"], 6)
            self.assertEqual(r["corpora"]["latin"]["hapax_frequent_ratio"], 1.0)
    def test_integration(self):
        with tempfile.TemporaryDirectory() as tmp:
            for rel in m.SOURCES.values():
                p = Path(tmp) / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("*** START OF THE PROJECT GUTENBERG EBOOK X ***\naa aa aa aa aa bbbb\n*** END OF THE PROJECT GUTENBERG EBOOK X ***")
            r = m.run(Path(tmp))
            self.assertEqual(r["corpora"]["latin"]["tokens"], 6)
            self.assertEqual(r["corpora"]["italian"]["hapax_frequent_ratio"], 2)

if __name__ == "__main__":
    unittest.main()
