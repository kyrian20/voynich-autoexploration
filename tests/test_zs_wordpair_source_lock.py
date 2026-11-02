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



    def test_filtered_category_cannot_bridge_slash_continuation(self):
        # Before the guard, filtering @L0 out of the P-only view joined
        # two nonadjacent physical rows into the artificial token 'daiin'.
        cases = (
            "<f1r> $L=A\n<f1r.1,@P0> dai/\n"
            "<f1r.2,@L0> ignored\n<f1r.3,@P0> /in\n",
            "<f1r> $L=A\n<f1r.1,@P0> dai/\n"
            "# intervening physical comment\n<f1r.2,@P0> /in\n",
            "<f1r> $L=A\n<f1r.1,@P0> dai/\n"
            "\n<f1r.2,@P0> /in\n",
        )
        for source_text in cases:
            with self.subTest(source_text=source_text):
                with self.assertRaisesRegex(ValueError, "Interrupted IVTFF continuation"):
                    audit.read_pages(
                        Path("/not/used"), source_text=source_text,
                        categories={"P"}, keep_empty=True,
                    )

    def test_adjacent_continuation_and_filtered_independent_rows_survive(self):
        adjacent = (
            "<f1r> $L=A\n<f1r.1,@P0> dai/\n"
            "<f1r.2,@P0> /in\n"
        )
        pages = audit.read_pages(
            Path("/not/used"), source_text=adjacent,
            categories={"P"}, keep_empty=True,
        )
        self.assertEqual(pages[0]["lines"], [["daiin"]])
        self.assertEqual(pages[0]["line_loci"], [["f1r.1,@P0", "f1r.2,@P0"]])

        independent = (
            "<f1r> $L=A\n<f1r.1,@P0> daiin\n"
            "<f1r.2,@L0> ignored\n<f1r.3,@P0> chedy\n"
        )
        pages = audit.read_pages(
            Path("/not/used"), source_text=independent,
            categories={"P"}, keep_empty=True,
        )
        self.assertEqual(pages[0]["lines"], [["daiin"], ["chedy"]])

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

    def test_glued_or_indented_structural_tags_rejected_by_both_readers(self):
        # Both readers previously accepted a glued payload and silently
        # ignored an indented page boundary or text locus.
        cases = (
            ("<f1r>$L=A\n", "Missing separator after IVTFF structural tag"),
            ("<f1r> $L=A\n<f1r.1,@P0>daiin\n",
             "Missing separator after IVTFF structural tag"),
            (" <f1r> $L=A\n", "Indented IVTFF structural tag"),
            ("<f1r> $L=A\n\t<f1r.1,@P0> daiin\n",
             "Indented IVTFF structural tag"),
        )
        for source_text, error in cases:
            for reader in (audit.read_pages, audit.read_pages_legacy):
                with self.subTest(reader=reader.__name__, source=source_text):
                    with self.assertRaisesRegex(ValueError, error):
                        reader(Path("/not/used"), source_text=source_text,
                               categories={"P"}, keep_empty=True)

    def test_missing_opening_tag_rejected_by_both_readers(self):
        # A damaged page boundary cannot be treated as an ignorable comment.
        cases = (
            "<f1r> $L=A\nf2r> $L=B\n",
            "<f1r> $L=A\nf1r.1,@P0> daiin\n",
        )
        for source_text in cases:
            for reader in (audit.read_pages, audit.read_pages_legacy):
                with self.subTest(reader=reader.__name__, source=source_text):
                    with self.assertRaisesRegex(ValueError, "Missing opening <"):
                        reader(Path("/not/used"), source_text=source_text,
                               categories={"P"}, keep_empty=True)

    def test_malformed_locator_codes_rejected_even_when_filtered(self):
        # A malformed @L row must not disappear before structural validation.
        bad_tags = ("@L0 extra", "@L0;AB", "@L0\u00a0", "@L0\t", "@L0;é")
        for tag in bad_tags:
            source_text = f"<f1r> $L=A\n<f1r.1,{tag}> daiin\n"
            for reader in (audit.read_pages, audit.read_pages_legacy):
                with self.subTest(reader=reader.__name__, tag=tag):
                    with self.assertRaisesRegex(ValueError, "Invalid IVTFF text locus"):
                        reader(Path("/not/used"), source_text=source_text,
                               categories={"P"}, keep_empty=True)

    def test_valid_tag_separators_and_transcriber_suffix_survive(self):
        source_text = (
            "<f1r>\t$L=A\n"
            "<f1r.1,@P0;A>\t daiin.daiin\n"
            "<f1r.2,+P0> chedy\n"
        )
        for reader in (audit.read_pages, audit.read_pages_legacy):
            with self.subTest(reader=reader.__name__):
                pages = reader(Path("/not/used"), source_text=source_text,
                               categories={"P"}, keep_empty=True)
                self.assertEqual(pages[0]["lines"], [["daiin", "daiin"], ["chedy"]])

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


    def test_archived_page_halves_share_four_physical_leaves(self):
        # The 225 source-order pages were used in the archived metric. Foldout
        # panels from four physical sheets straddle alternating block borders.
        expected = {"f67", "f72", "f90", "f102"}
        for name in ("eva_zl3b.txt", "eva_it2a.txt"):
            with self.subTest(source=name):
                path = ROOT / "data/transcriptions" / name
                snapshot, _ = audit.load_verified_source(path)
                pages = audit.read_pages(path, source_text=snapshot,
                                         uncertain_space="split",
                                         categories={"P", "C", "R"},
                                         keep_empty=True)
                pages = [p for p in pages if p["id"] not in {"f116v", "fRos"}]
                self.assertEqual(len(pages), 225)
                diagnostic = audit.audit_page_half_leakage(pages)
                self.assertEqual(diagnostic["cross_half_physical_leaf_count"], 4)
                self.assertEqual({row["leaf"] for row in diagnostic["overlaps"]}, expected)
                with self.assertRaisesRegex(ValueError, "Physical leaf overlap"):
                    audit.require_disjoint_physical_leaves(pages)

    def test_overlap_gate_rejects_cross_block_foldout_but_not_same_block(self):
        pages = [{"id": "f67r1", "lines": []}]
        pages.extend({"id": f"f{i}r", "lines": []} for i in range(1, 10))
        pages.append({"id": "f67v2", "lines": []})
        diagnostic = audit.audit_page_half_leakage(pages)
        self.assertEqual(diagnostic["cross_half_physical_leaf_count"], 1)
        self.assertEqual(diagnostic["overlaps"][0]["leaf"], "f67")
        # The gate must fail before attempting a statistical calculation.
        with self.assertRaisesRegex(ValueError, "Physical leaf overlap"):
            audit.metric(pages, require_leaf_independence=True, shuffles=1, top_k=2)
        self.assertEqual(
            audit.require_disjoint_physical_leaves([pages[0], pages[-1]]),
            audit.audit_page_half_leakage([pages[0], pages[-1]]),
        )

    def test_metric_rejects_empty_pairs_and_missing_half_before_simulation(self):
        # A small synthetic view must not produce a numeric-looking receipt
        # with no eligible pairs or no text in the second page-block half.
        single_half = [{"id": "f1r", "lines": [["daiin", "qokedy", "chedy", "otol"]]}]
        with self.assertRaisesRegex(ValueError, "Both page halves must contain text lines"):
            audit.metric(single_half, shuffles=1, top_k=4)

        def both_halves(tokens):
            return ([{"id": "f1r", "lines": [tokens]}]
                    + [{"id": f"f{i}r", "lines": []} for i in range(2, 11)]
                    + [{"id": "f11r", "lines": [tokens]}])

        with self.assertRaisesRegex(ValueError, "No eligible word pairs"):
            audit.metric(both_halves(["daiin"]), shuffles=1, top_k=1)

    def test_metric_rejects_singular_and_undefined_correlations(self):
        # Two eligible types produce a rank-deficient additive-effect design;
        # three fully connected types have zero residual degrees of freedom.
        def both_halves(tokens):
            return ([{"id": "f1r", "lines": [tokens]}]
                    + [{"id": f"f{i}r", "lines": []} for i in range(2, 11)]
                    + [{"id": "f11r", "lines": [tokens]}])

        with self.assertRaisesRegex(ValueError, "rank deficient"):
            audit.metric(both_halves(["daiin", "qokedy"]), shuffles=1, top_k=2)
        with self.assertRaisesRegex(ValueError, "Undefined/nonfinite word-pair correlation"):
            audit.metric(both_halves(["daiin", "qokedy", "chedy"]), shuffles=1, top_k=3)

    def test_metric_rejects_empty_or_malformed_shuffle_counts(self):
        # A zero or negative shuffle count previously left expected pair
        # counts at zero, yet still entered the statistical calculation.
        pages = [{"id": "f1r", "lines": [["daiin", "qokedy", "chedy"]]}]
        for invalid in (0, -1, True, 1.5, "20", None):
            with self.subTest(shuffles=invalid):
                with self.assertRaisesRegex(ValueError, "shuffles must be a positive integer"):
                    audit.metric(pages, shuffles=invalid)

    def test_metric_rejects_invalid_vocabulary_size_and_seed(self):
        pages = [{"id": "f1r", "lines": [["daiin", "qokedy", "chedy"]]}]
        for invalid in (0, -1, True, 1.5, "300", None):
            with self.subTest(top_k=invalid):
                with self.assertRaisesRegex(ValueError, "top_k must be a positive integer"):
                    audit.metric(pages, top_k=invalid)
        for invalid in (True, 1.5, "20261101", None):
            with self.subTest(seed=invalid):
                with self.assertRaisesRegex(ValueError, "seed must be an integer"):
                    audit.metric(pages, seed=invalid)

    def test_physical_leaf_aliases_and_invalid_block_sizes(self):
        self.assertEqual(audit.physical_leaf_id("f067r1"), "f67")
        self.assertEqual(audit.physical_leaf_id("f67v6"), "f67")
        self.assertEqual(audit.physical_leaf_id("fRos"), "fRos")
        with self.assertRaisesRegex(ValueError, "Invalid IVTFF physical leaf"):
            audit.physical_leaf_id("f0r")
        for size in (0, -1, True, 1.5):
            with self.subTest(size=size):
                with self.assertRaisesRegex(ValueError, "positive integer"):
                    audit.audit_page_half_leakage([], block_pages=size)


if __name__ == "__main__":
    unittest.main()
