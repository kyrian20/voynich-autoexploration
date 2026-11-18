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
