#!/usr/bin/env python3
"""Regression tests for IVTFF brace inventory scope (no corpus mutation)."""
import unittest

from scripts.audit_ivtff_brace_spans import audit_text, mask_non_record_text


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


if __name__ == "__main__":
    unittest.main()
