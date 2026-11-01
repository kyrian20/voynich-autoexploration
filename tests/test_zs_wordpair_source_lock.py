"""Regression tests for the frozen input of the Zhang–Sheng partial audit.

No NumPy or full word-pair simulation is needed: this tests source provenance
and the snapshot passed to the reader, not the scientific score.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research/maintenance/2026-11-01-zs-wordpair-audit/wordpair_audit.py"
spec = importlib.util.spec_from_file_location("zs_wordpair_source_lock", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class WordPairFrozenInputTests(unittest.TestCase):
    def test_both_reviewed_sources_match_sha256_and_git_blob(self):
        for name in ("eva_zl3b.txt", "eva_it2a.txt"):
            with self.subTest(source=name):
                path = ROOT / "data/transcriptions" / name
                snapshot, receipt = audit.load_verified_source(path)
                raw = path.read_bytes()
                self.assertEqual(snapshot.encode("utf-8"), raw)
                self.assertEqual(receipt["sha256"], hashlib.sha256(raw).hexdigest())
                self.assertEqual(
                    receipt["git_blob_sha"],
                    hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest(),
                )
                self.assertEqual(
                    (receipt["sha256"], receipt["git_blob_sha"]),
                    audit.SOURCE_LOCK[name],
                )

    def test_mutated_source_fails_before_metrics(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "eva_zl3b.txt"
            path.write_bytes(b"altered source")
            with self.assertRaisesRegex(ValueError, "Frozen word-pair source mismatch"):
                audit.load_verified_source(path)

    def test_unregistered_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "unknown.txt"
            path.write_bytes(b"")
            with self.assertRaisesRegex(ValueError, "Unregistered word-pair source"):
                audit.load_verified_source(path)

    def test_symlinked_file_rejected_even_if_bytes_are_correct(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "eva_zl3b.txt"
            path.symlink_to(ROOT / "data/transcriptions/eva_zl3b.txt")
            with self.assertRaisesRegex(ValueError, "Symlinked word-pair source"):
                audit.load_verified_source(path)

    def test_symlinked_parent_rejected_even_if_bytes_are_correct(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp) / "redirect"
            parent.symlink_to(ROOT / "data/transcriptions", target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "Symlinked word-pair source"):
                audit.load_verified_source(parent / "eva_it2a.txt")

    def test_invalid_page_header_rejected_by_both_readers(self):
        for reader in (audit.read_pages, audit.read_pages_legacy):
            with self.subTest(reader=reader.__name__):
                for header in ("f1rEXTRA", "f0r", "f1r7"):
                    with self.subTest(header=header):
                        source_text = f"<{header}> $L=A\\n"
                        with self.assertRaisesRegex(ValueError, "Invalid IVTFF page header"):
                            reader(Path("/not/used"), source_text=source_text, keep_empty=True)

    def test_duplicate_physical_page_alias_rejected_by_both_readers(self):
        source_text = (
            "<f1r> $L=A\\n"
            "<f1r.1,@P0> daiin.daiin\\n"
            "<f01r> $L=A\\n"
            "<f01r.1,@P0> daiin.daiin\\n"
        )
        for reader in (audit.read_pages, audit.read_pages_legacy):
            with self.subTest(reader=reader.__name__):
                with self.assertRaisesRegex(ValueError, "Duplicate physical IVTFF page header"):
                    reader(Path("/not/used"), source_text=source_text, keep_empty=True)

    def test_frozen_sources_still_have_unique_page_headers(self):
        expected = {"eva_zl3b.txt": 227, "eva_it2a.txt": 225}
        for name, count in expected.items():
            with self.subTest(source=name):
                source = ROOT / "data/transcriptions" / name
                snapshot, _ = audit.load_verified_source(source)
                for reader in (audit.read_pages, audit.read_pages_legacy):
                    with self.subTest(reader=reader.__name__):
                        pages = reader(
                            source, source_text=snapshot, keep_empty=True,
                            categories={"P", "C", "R"},
                        )
                        self.assertEqual(len(pages), count)


    def test_reader_can_use_snapshot_without_reopening_path(self):
        source_text = "<f1r> $L=A\n<f1r.1,@P0> daiin.daiin\n"
        nonexistent = Path("/definitely/not/a/wordpair/corpus.txt")
        pages = audit.read_pages_legacy(
            nonexistent, categories={"P"}, keep_empty=True, source_text=source_text
        )
        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0]["lines"], [["daiin", "daiin"]])


if __name__ == "__main__":
    unittest.main()
