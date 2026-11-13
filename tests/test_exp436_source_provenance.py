"""Regression tests for the separate EXP-436 source gate (no historical replay)."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts.check_exp436_source_provenance import evaluate

class ProvenanceGateTests(unittest.TestCase):
    def test_missing_input_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "missing"
            self.assertFalse(evaluate(p, p, {})["ok"])

    def test_matching_both_hashes_is_required(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "latin", Path(d) / "italian"
            a.write_bytes(b"synthetic latin fixture")
            b.write_bytes(b"synthetic italian fixture")
            hashes = {"latin": hashlib.sha256(a.read_bytes()).hexdigest(),
                      "italian": hashlib.sha256(b.read_bytes()).hexdigest()}
            self.assertFalse(evaluate(a, b, {"latin": hashes["latin"]})["ok"])
            result = evaluate(a, b, hashes)
            self.assertTrue(result["ok"])
            self.assertEqual(result["sources"]["latin"]["status"], "HASH_MATCH")
            b.write_bytes(b"changed")
            self.assertFalse(evaluate(a, b, hashes)["ok"])

    def test_same_bytes_cannot_fill_both_language_roles(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "latin", Path(d) / "italian"
            a.write_bytes(b"same synthetic source")
            b.write_bytes(a.read_bytes())
            digest = hashlib.sha256(a.read_bytes()).hexdigest()
            report = evaluate(a, b, {"latin": digest, "italian": digest})
            self.assertFalse(report["ok"])
            self.assertEqual(report["sources"]["latin"]["status"], "DUPLICATE_SOURCE")
            self.assertEqual(report["sources"]["italian"]["status"], "DUPLICATE_SOURCE")
            self.assertEqual(a.read_bytes(), b.read_bytes())

    def test_streaming_hash_matches_across_multiple_chunks(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "latin", Path(d) / "italian"
            a.write_bytes(b"A" * (1024 * 1024 + 7))
            b.write_bytes(b"B" * (2 * 1024 * 1024 + 3))
            approved = {"latin": hashlib.sha256(a.read_bytes()).hexdigest(),
                        "italian": hashlib.sha256(b.read_bytes()).hexdigest()}
            report = evaluate(a, b, approved)
            self.assertTrue(report["ok"])
            self.assertEqual(report["sources"]["latin"]["sha256"], approved["latin"])
            self.assertEqual(report["sources"]["italian"]["sha256"], approved["italian"])

    def test_whitespace_only_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "latin", Path(d) / "italian"
            a.write_bytes(b" \\t\\r\\n" * 500000)
            b.write_bytes(b"synthetic italian fixture")
            approved = {"latin": hashlib.sha256(a.read_bytes()).hexdigest(),
                        "italian": hashlib.sha256(b.read_bytes()).hexdigest()}
            report = evaluate(a, b, approved)
            self.assertFalse(report["ok"])
            self.assertEqual(report["sources"]["latin"]["status"], "BLANK_SOURCE")
            self.assertEqual(report["sources"]["italian"]["status"], "HASH_MATCH")
            self.assertEqual(hashlib.sha256(a.read_bytes()).hexdigest(), approved["latin"])

    def test_unreadable_existing_input_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "latin", Path(d) / "italian"
            a.write_bytes(b"synthetic latin fixture")
            b.write_bytes(b"synthetic italian fixture")
            approved = {"latin": hashlib.sha256(a.read_bytes()).hexdigest(),
                        "italian": hashlib.sha256(b.read_bytes()).hexdigest()}
            original_open = Path.open

            def guarded_open(path, *args, **kwargs):
                if path == a:
                    raise PermissionError("synthetic denied read")
                return original_open(path, *args, **kwargs)

            with patch.object(Path, "open", guarded_open):
                report = evaluate(a, b, approved)
            self.assertFalse(report["ok"])
            self.assertEqual(report["sources"]["latin"]["status"], "UNREADABLE")
            self.assertEqual(report["sources"]["latin"]["reason"], "PermissionError")
            self.assertEqual(report["sources"]["italian"]["status"], "HASH_MATCH")

    def test_runtime_error_during_streaming_read_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "latin", Path(d) / "italian"
            a.write_bytes(b"synthetic latin fixture")
            b.write_bytes(b"synthetic italian fixture")
            approved = {"latin": hashlib.sha256(a.read_bytes()).hexdigest(),
                        "italian": hashlib.sha256(b.read_bytes()).hexdigest()}
            original_open = Path.open

            def guarded_open(path, *args, **kwargs):
                if path == a:
                    raise RuntimeError("synthetic runtime failure")
                return original_open(path, *args, **kwargs)

            with patch.object(Path, "open", guarded_open):
                report = evaluate(a, b, approved)
            self.assertFalse(report["ok"])
            self.assertEqual(report["sources"]["latin"]["status"], "UNREADABLE")
            self.assertEqual(report["sources"]["latin"]["reason"], "RuntimeError")
            self.assertEqual(report["sources"]["italian"]["status"], "HASH_MATCH")
            self.assertEqual(a.read_bytes(), b"synthetic latin fixture")

    def test_metadata_inspection_error_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "latin", Path(d) / "italian"
            a.write_bytes(b"synthetic latin fixture")
            b.write_bytes(b"synthetic italian fixture")
            approved = {"latin": hashlib.sha256(a.read_bytes()).hexdigest(),
                        "italian": hashlib.sha256(b.read_bytes()).hexdigest()}
            original_is_file = Path.is_file

            def guarded_is_file(path):
                if path == a:
                    raise PermissionError("synthetic metadata denied")
                return original_is_file(path)

            with patch.object(Path, "is_file", guarded_is_file):
                report = evaluate(a, b, approved)
            self.assertFalse(report["ok"])
            self.assertEqual(report["sources"]["latin"]["status"], "UNREADABLE")
            self.assertEqual(report["sources"]["latin"]["reason"], "PermissionError")
            self.assertEqual(report["sources"]["italian"]["status"], "HASH_MATCH")

    def test_known_english_caesar_hash_never_approved(self):
        from scripts.check_exp436_source_provenance import KNOWN_INVALID
        self.assertIn("eaa456256c46507f872efd965335b370605e6d323ca89ef2012cb71b516183d7", KNOWN_INVALID)

if __name__ == "__main__":
    unittest.main()
