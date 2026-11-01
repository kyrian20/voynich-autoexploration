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
                        source_text = f"<{header}> $L=A\n"
                        with self.assertRaisesRegex(ValueError, "Invalid IVTFF page header"):
                            reader(Path("/not/used"), source_text=source_text, keep_empty=True)

    def test_duplicate_physical_page_alias_rejected_by_both_readers(self):
        source_text = (
            "<f1r> $L=A\n"
            "<f1r.1,@P0> daiin.daiin\n"
            "<f01r> $L=A\n"
            "<f01r.1,@P0> daiin.daiin\n"
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


    def test_nonphysical_separators_cannot_forge_page_headers(self):
        # Before this repair splitlines() turned the hidden f2r tag into a
        # genuine second page, even though it belonged to a comment row.
        for separator in audit.NON_PHYSICAL_SEPARATORS:
            source_text = (
                "<f1r> $L=A\n"
                + "# comment" + separator + "<f2r> $L=B\n"
                + "<f2r.1,@P0> daiin.daiin\n"
            )
            for reader in (audit.read_pages, audit.read_pages_legacy):
                with self.subTest(reader=reader.__name__, codepoint=ord(separator)):
                    with self.assertRaisesRegex(ValueError, "Non-physical IVTFF separator"):
                        reader(Path("/not/used"), source_text=source_text, keep_empty=True)

    def test_physical_crlf_cr_and_lf_still_parse(self):
        for newline in ("\n", "\r", "\r\n"):
            source_text = newline.join((
                "<f1r> $L=A",
                "<f1r.1,@P0> daiin.daiin",
                "",
            ))
            for reader in (audit.read_pages, audit.read_pages_legacy):
                with self.subTest(reader=reader.__name__, newline=repr(newline)):
                    pages = reader(Path("/not/used"), source_text=source_text,
                                   categories={"P"}, keep_empty=True)
                    self.assertEqual(len(pages), 1)
                    self.assertEqual(len(pages[0]["lines"]), 1)



    def test_numeric_locus_alias_rejected_even_when_category_excluded(self):
        # Prior readers silently double-counted identical physical loci;
        # the legacy reader also silently ignored malformed text rows.
        source_text = (
            "<f1r> $L=A\n"
            "<f1r.1,@L0> daiin.daiin\n"
            "<f1r.01,@L0> qokedy.daiin\n"
        )
        for reader in (audit.read_pages, audit.read_pages_legacy):
            with self.subTest(reader=reader.__name__):
                with self.assertRaisesRegex(ValueError, "Duplicate physical IVTFF text locus"):
                    reader(Path("/not/used"), source_text=source_text,
                           categories={"P"}, keep_empty=True)

    def test_orphan_invalid_and_truncated_loci_fail_closed(self):
        cases = (
            ("<f1r.1,@P0> daiin.daiin\n", "Text line before page header"),
            ("<f1r> $L=A\n<f1r.x,@P0> daiin.daiin\n", "Invalid IVTFF text locus"),
            ("<f1r> $L=A\n<f1r.0,@P0> daiin.daiin\n", "Invalid IVTFF text locus"),
            ("<f1r> $L=A\n<f1r.1,@P0 daiin.daiin\n", "Malformed IVTFF record"),
            ("<f1r> $L=A\n<f2r.1,@P0> daiin.daiin\n", "Page/locus mismatch"),
        )
        for source_text, error in cases:
            for reader in (audit.read_pages, audit.read_pages_legacy):
                with self.subTest(reader=reader.__name__, error=error):
                    with self.assertRaisesRegex(ValueError, error):
                        reader(Path("/not/used"), source_text=source_text, keep_empty=True)

    def test_distinct_locus_tags_are_not_false_duplicates(self):
        source_text = (
            "<f1r> $L=A\n"
            "<f1r.1,@P0> daiin.daiin\n"
            "<f1r.1,+P0> qokedy.daiin\n"
        )
        for reader in (audit.read_pages, audit.read_pages_legacy):
            with self.subTest(reader=reader.__name__):
                pages = reader(Path("/not/used"), source_text=source_text,
                               categories={"P"}, keep_empty=True)
                self.assertEqual(len(pages), 1)
                self.assertEqual(len(pages[0]["lines"]), 2)


if __name__ == "__main__":
    unittest.main()
