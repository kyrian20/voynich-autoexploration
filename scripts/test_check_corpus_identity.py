import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from check_corpus_identity import audit


class CorpusIdentityTests(unittest.TestCase):
    def test_detects_mutation_and_missing(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            f = root / "data/reference_corpora/arabic/quran_arabic.txt"
            f.parent.mkdir(parents=True)
            raw = b"Title: Drum-Taps\nLanguage: English\n"
            f.write_bytes(raw)
            m = root / "inventory.json"
            entry = {"path": str(f.relative_to(root)), "sha256": hashlib.sha256(raw).hexdigest(),
                     "bytes": len(raw), "header_title": ["Title: Drum-Taps"],
                     "header_language": ["Language: English"]}
            m.write_text(json.dumps({"excluded_from_new_language_baselines": [entry]}))
            self.assertEqual(audit(root, m), [])
            f.write_bytes(raw + b"changed")
            self.assertTrue(any("mismatch" in x for x in audit(root, m)))
            f.unlink()
            self.assertTrue(any("missing" in x for x in audit(root, m)))

    def test_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            m = root / "inventory.json"
            m.write_text(json.dumps({"excluded_from_new_language_baselines": [
                {"path": "../secret", "sha256": "x", "bytes": 1}]}))
            self.assertTrue(any("unsafe" in x for x in audit(root, m)))


    def test_rejects_symlink_escape_even_when_bytes_match(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "repo"
            root.mkdir()
            outside = base / "external.txt"
            raw = b"Title: Drum-Taps\\nLanguage: English\\n"
            outside.write_bytes(raw)
            link = root / "data" / "external.txt"
            link.parent.mkdir()
            link.symlink_to(outside)
            manifest = root / "inventory.json"
            manifest.write_text(json.dumps({"excluded_from_new_language_baselines": [{
                "path": "data/external.txt", "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw), "header_title": ["Title: Drum-Taps"],
                "header_language": ["Language: English"]}]}))
            self.assertTrue(any("unsafe" in x for x in audit(root, manifest)))

if __name__ == "__main__":
    unittest.main()
