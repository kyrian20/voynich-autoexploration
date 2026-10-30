#!/usr/bin/env python3
"""Regression tests for IVTFF brace inventory scope (no corpus mutation)."""
import hashlib
import unittest

from scripts.audit_ivtff_brace_spans import (
    FILES, audit_text, mask_non_record_text, require_valid_structure,
)
from scripts.ivtff_physical_rows import NON_PHYSICAL_SEPARATORS


class BraceInventoryScopeTests(unittest.TestCase):
    def test_record_payload_only_and_original_offsets(self):
        source = (
            "# {hash-comment}\n"
            "<f1r> <! $L=A> {header-note}\n"
            "<f1r.1,@P0> a{ch}b<!editor {comment}> c{sh}d\n"
            "free {untagged}\n"
            "<f86v4> <! $L=B>\n"
            "<f86v4.2,@P0> [{y'}:x] <!editor {tag}>\n"
        )
        legacy = audit_text(source)
        masked = mask_non_record_text(source)
        scoped = audit_text(masked)
        self.assertEqual(len(masked), len(source))
        self.assertEqual(masked.count("\n"), source.count("\n"))
        self.assertEqual(legacy["brace_span_count"], 7)
        self.assertEqual(scoped["brace_span_count"], 3)
        self.assertEqual(
            [row["content"] for row in scoped["examples"]],
            ["ch", "sh", "y'"],
        )
        self.assertEqual(
            [row["offset"] for row in scoped["examples"]],
            [source.index("{ch}"), source.index("{sh}"), source.index("{y'}")],
        )
        self.assertEqual(scoped["unmatched_open_brace_count"], 0)
        self.assertEqual(scoped["unmatched_close_brace_count"], 0)

    def test_metadata_only_is_not_lexical(self):
        source = (
            "# {hash}\n"
            "<f1r> <! editorial {header}>\n"
            "plain {prose}\n"
            "<f1r.1,@P0> <! editorial {tag}>\n"
        )
        self.assertEqual(audit_text(source)["brace_span_count"], 3)
        self.assertEqual(
            audit_text(mask_non_record_text(source))["brace_span_count"], 0
        )

    def test_unclosed_spans_do_not_pair_across_loci(self):
        source = (
            "<fRos> <! $L=B>\n"
            "<fRos.1,@P0> {open\n"
            "<fRos.2,@P0> close}\n"
        )
        scoped = audit_text(mask_non_record_text(source))
        self.assertEqual(scoped["brace_span_count"], 0)
        self.assertEqual(scoped["unmatched_open_brace_count"], 1)
        self.assertEqual(scoped["unmatched_close_brace_count"], 1)

    def test_nonrecord_and_inline_tags_do_not_break_line_endings(self):
        source = "<f1r.1,@P0> a{ch}b<! {note}>\r\nplain {prose}\r\n"
        masked = mask_non_record_text(source)
        self.assertEqual(len(masked), len(source))
        self.assertEqual(masked.count("\r\n"), 2)
        self.assertEqual(audit_text(masked)["brace_span_count"], 1)

    def test_fake_unicode_row_separators_fail_closed(self):
        for separator in NON_PHYSICAL_SEPARATORS:
            with self.subTest(codepoint=f"U+{ord(separator):04X}"):
                source = (
                    "<f1r> <! $L=A>\n"
                    "<f1r.1,@P0> a{ch}b\n"
                    "# comment" + separator + "<f1r.2,@P0> {forged}\n"
                )
                with self.assertRaisesRegex(ValueError, "Non-physical"):
                    audit_text(source)
                with self.assertRaisesRegex(ValueError, "Non-physical"):
                    mask_non_record_text(source)
                with self.assertRaisesRegex(ValueError, "Invalid IVTFF"):
                    require_valid_structure(source)

    def test_glued_locus_rejected_before_inventory(self):
        source = (
            "<f1r> <! $L=A>\n"
            "<f1r.1,@P0> a{ch}b\n"
            "<f1r.2,@P0>junk{forged}\n"
        )
        with self.assertRaisesRegex(ValueError, "Invalid IVTFF"):
            require_valid_structure(source)
        # The direct masking helper also refuses to promote malformed tags.
        self.assertEqual(
            audit_text(mask_non_record_text(source))["brace_span_count"], 1
        )

    def test_unicode_locus_digit_rejected(self):
        source = (
            "<f1r> <! $L=A>\n"
            "<f1r.1,@P0> a{ch}b\n"
            "<f1r.\u0661,@P0> {forged}\n"
        )
        with self.assertRaisesRegex(ValueError, "Invalid IVTFF"):
            require_valid_structure(source)
        self.assertEqual(
            audit_text(mask_non_record_text(source))["brace_span_count"], 1
        )

    def test_frozen_corpus_brace_counts_unchanged(self):
        expected = {
            "ZL3b": ("bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc", 446),
            "ZL3a": ("56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2", 444),
            "IT2a": ("7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5", 0),
        }
        for label, path in FILES:
            with self.subTest(label=label):
                raw = path.read_bytes()
                digest, count = expected[label]
                self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
                text = raw.decode("utf-8-sig")
                require_valid_structure(text)
                self.assertEqual(
                    audit_text(mask_non_record_text(text))["brace_span_count"], count
                )


if __name__ == "__main__":
    unittest.main()
