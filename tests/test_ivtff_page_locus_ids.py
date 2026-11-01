#!/usr/bin/env python3
"""Regression fixtures for IVTFF page and locus-ID structural coverage."""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_ivtff_page_locus_ids import SOURCES, audit_text, structural_errors
from experiments.exp_602_independent_ivtff_parser_audit.script import compare


def main() -> None:
    valid = "\n".join([
        "# fixture",
        "<f1r> <! $L=A>",
        "<f1r.1,@P0> daiin",
        "<f67r1> <! $L=B>",
        "<f67r1.5,@Cc> daiin",
        "<f86v4> <! $L=B>",
        "<f86v4.160,+P0> daiin",
        "<fRos> <! $L=B>",
        "<fRos.23,@L0> daiin",
    ])
    report = audit_text(valid)
    assert report["page_header_count"] == 4, report
    assert report["record_count"] == 4, report
    assert report["malformed_header_count"] == 0, report
    assert report["malformed_record_count"] == 0, report
    assert report["page_mismatch_count"] == 0, report
    assert report["locus_number_out_of_range_count"] == 0, report
    assert structural_errors(report) == [], report

    # The structural auditor must not accept a valid-looking <f...> prefix
    # followed immediately by text or another tag. Unlike the older reader,
    # this guard fails closed and invalidates an apparent page transition.
    for damaged_page in (
        "<f2r>garbage", "<fRos><! $L=B>",
        "<f86v4>garbage", "<f٢r>garbage",
    ):
        glued = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + damaged_page + "\n<f1r.2,@P0> chedy\n"
        )
        assert glued["page_header_count"] == 1, glued
        assert glued["malformed_header_count"] == 1, glued
        assert glued["page_mismatch_count"] == 1, glued
        assert glued["malformed_headers"][0]["reason"] == "missing separator after page tag", glued
        assert set(structural_errors(glued)) == {
            "malformed_header_count=1", "page_mismatch_count=1"
        }, glued

    for damaged_record in (
        "<f1r.2,@P0>garbage", "<f1r.2,@P0><!comment>",
    ):
        glued = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n" + damaged_record + "\n"
        )
        assert glued["record_count"] == 1, glued
        assert glued["malformed_record_count"] == 1, glued
        assert structural_errors(glued) == ["malformed_record_count=1"], glued

    # Properly separated tags (space, tab or end of row) remain accepted.
    separated = audit_text(
        "<f1r>\t<! $L=A>\n<f1r.1,@P0> daiin\n"
        "<f2r> <! $L=B>\n<f2r.1,@P0> chedy\n"
    )
    assert structural_errors(separated) == [], separated

    # A repeated physical page header is an integrity defect even when its
    # later loci have new record tags: otherwise duplicate-record checks pass
    # and one folio may be split into disjoint blocks without warning.
    repeated_page = audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
        "<f2r> <! $L=B>\n<f2r.1,@P0> chedy\n"
        "<f1r> <! $L=A>\n<f1r.2,@P0> or\n"
    )
    assert repeated_page["page_header_count"] == 3, repeated_page
    assert repeated_page["distinct_page_headers"] == 2, repeated_page
    assert repeated_page["record_count"] == 3, repeated_page
    assert repeated_page["duplicate_record_tag_count"] == 0, repeated_page
    assert repeated_page["page_mismatch_count"] == 0, repeated_page
    assert repeated_page["duplicate_page_header_count"] == 1, repeated_page
    assert repeated_page["duplicate_page_headers"] == [
        {"page": "f1r", "first_line": 1, "repeated_line": 5}
    ], repeated_page
    assert structural_errors(repeated_page) == [
        "duplicate_page_header_count=1"
    ], repeated_page

    # Zero padding in a folio number cannot create a second physical page.
    # Raw spellings remain visible in diagnostics; identity is numeric.
    for first, alias in (
        ("f1r", "f01r"),
        ("f86v4", "f086v4"),
        ("f86v5", "f0086v5"),
    ):
        aliased_page = audit_text(
            f"<{first}> first\n<{first}.1,@P0> word\n"
            f"<{alias}> alias\n<{alias}.2,@P0> second\n"
        )
        assert aliased_page["page_header_count"] == 2, aliased_page
        assert aliased_page["distinct_page_headers"] == 1, aliased_page
        assert aliased_page["duplicate_page_header_count"] == 1, aliased_page
        assert aliased_page["duplicate_page_headers"] == [
            {"page": alias, "first_line": 1, "repeated_line": 3}
        ], aliased_page
        assert structural_errors(aliased_page) == [
            "duplicate_page_header_count=1"
        ], aliased_page
    distinct_panels = audit_text(
        "<f86v4> first\n<f86v4.1,@P0> a\n"
        "<f86v5> second\n<f86v5.1,@P0> b\n"
    )
    assert structural_errors(distinct_panels) == [], distinct_panels

    # A second fRos header must also be visible, but must not be rewritten
    # or silently merged with the first block.
    repeated_ros = audit_text(
        "<fRos> <! $L=B>\n<fRos.1,@P0> daiin\n"
        "<fRos> <! $L=B>\n<fRos.2,@P0> chedy\n"
    )
    assert repeated_ros["duplicate_page_header_count"] == 1, repeated_ros
    assert repeated_ros["duplicate_record_tag_count"] == 0, repeated_ros
    assert structural_errors(repeated_ros) == [
        "duplicate_page_header_count=1"
    ], repeated_ros

    # IVTFF numeric identifiers use ASCII digits. Python's regex \d
    # also accepts Unicode decimal numerals; accepting those could create
    # a phantom folio or a malformed record with apparently valid counts.
    unicode_page = audit_text("<f١r> <! $L=A>\n<f١r.1,@P0> daiin\n")
    assert unicode_page["malformed_header_count"] == 1, unicode_page
    assert unicode_page["malformed_record_count"] == 1, unicode_page
    assert structural_errors(unicode_page), unicode_page

    unicode_record = audit_text("<f1r> <! $L=A>\n<f1r.٢,@P0> daiin\n")
    assert unicode_record["malformed_record_count"] == 1, unicode_record
    assert structural_errors(unicode_record), unicode_record

    # A damaged page boundary must invalidate the previously active page,
    # not silently attach a later record to the wrong folio.
    unicode_boundary = audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
        "<f٢r> <! $L=B>\n<f1r.2,@P0> chedy\n"
    )
    assert unicode_boundary["malformed_header_count"] == 1, unicode_boundary
    assert unicode_boundary["page_mismatch_count"] == 1, unicode_boundary

    # The broad missing-opening-bracket diagnostic must still catch a
    # Unicode lookalike rather than silently discard the malformed line.
    unicode_missing_opener = audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
        "f٢r> <! $L=B>\n"
    )
    assert unicode_missing_opener["malformed_header_count"] == 1, unicode_missing_opener

    # A stray comma after a physical page ID used to be classified as a
    # malformed locus. The old page then remained active and a subsequent
    # old-page record passed the scope check. Diagnose the broken boundary
    # as a header, without promoting it to a valid page.
    for broken_header in (
        "<f2r,> <! $L=B>",
        "<fRos,> <! $L=B>",
        "<f86v4 ,> <! $L=B>",
        "<f٢r,> <! $L=B>",
    ):
        comma_boundary = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_header + "\n<f1r.2,@P0> chedy\n"
        )
        assert comma_boundary["record_count"] == 2, comma_boundary
        assert comma_boundary["malformed_header_count"] == 1, comma_boundary
        assert comma_boundary["malformed_record_count"] == 0, comma_boundary
        assert comma_boundary["page_mismatch_count"] == 1, comma_boundary
        assert comma_boundary["malformed_headers"][0]["reason"] == "comma in page header"
        assert structural_errors(comma_boundary) == [
            "malformed_header_count=1", "page_mismatch_count=1",
        ], comma_boundary

    # A malformed page tag with BOTH a comma and glued payload must
    # invalidate the active folio. The former suffix-first dispatch recorded
    # a malformed locus and silently accepted the subsequent old-page locus.
    for glued_header in (
        "<f2r,>garbage",
        "<fRos,><! $L=B>",
        "<f86v4 ,>garbage",
        "<f٢r,>garbage",
    ):
        report = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + glued_header + "\n<f1r.2,@P0> chedy\n"
        )
        assert report["page_header_count"] == 1, report
        assert report["record_count"] == 2, report
        assert report["malformed_header_count"] == 1, report
        assert report["malformed_record_count"] == 0, report
        assert report["page_mismatch_count"] == 1, report
        assert report["malformed_headers"][0]["reason"] == "comma in page header", report
        assert structural_errors(report) == [
            "malformed_header_count=1", "page_mismatch_count=1",
        ], report

    # An indented comma-damaged page boundary previously vanished entirely:
    # the old f1r scope stayed active and its next locus was accepted.
    # This is diagnostic only; none of these headers becomes a valid page.
    for broken_header in (
        " <f2r,> <! $L=B>",
        "\t<fRos,> <! $L=B>",
        " <f86v4,> <! $L=B>",
        " <f٢r,> <! $L=B>",
    ):
        report = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_header + "\n<f1r.2,@P0> chedy\n"
        )
        assert report["record_count"] == 2, report
        assert report["malformed_header_count"] == 1, report
        assert report["malformed_record_count"] == 0, report
        assert report["page_mismatch_count"] == 1, report
        assert structural_errors(report) == [
            "malformed_header_count=1", "page_mismatch_count=1",
        ], report
    # A non-page indented tag containing a comma is not a page boundary.
    unrelated_comma = audit_text(
        "<f1r> <! $L=A>\n <unrelated,>\n<f1r.1,@P0> daiin\n"
    )
    assert structural_errors(unrelated_comma) == [], unrelated_comma

    # A lost opening bracket plus stray comma must not preserve the old folio.
    for broken in ("f2r,> <! $L=B>", "fRos,> <! $L=B>"):
        report = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken + "\n<f1r.2,@P0> chedy\n"
        )
        assert report["malformed_header_count"] == 1, report
        assert report["page_mismatch_count"] == 1, report
        assert report["malformed_record_count"] == 0, report
    # Do not classify untagged prose as a damaged page boundary.
    prose = audit_text("<f1r>\n<f1r.1,@P0> daiin\nf2r,>commentary\n")
    assert structural_errors(prose) == [], prose

    # A malformed locus containing a comma remains a record error and must
    # not invalidate the active page or be mistaken for a page boundary.
    comma_locus = audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0,> daiin\n<f1r.2,@P0> chedy\n"
    )
    assert comma_locus["malformed_record_count"] == 1, comma_locus
    assert comma_locus["malformed_header_count"] == 0, comma_locus
    assert comma_locus["page_mismatch_count"] == 0, comma_locus
    assert structural_errors(comma_locus) == [
        "malformed_record_count=1"
    ], comma_locus

    bad = "\n".join([
        "<f1r> <! $L=A>",
        "<f67r1.5,@Cc> daiin",  # locus page must match active header
        "<f1r.1000,@P0> daiin", # numeric ID has too many digits
        "<fnotapage> <! $L=A>",
    ])
    report = audit_text(bad)
    assert report["page_mismatch_count"] == 1, report
    assert report["malformed_record_count"] == 1, report
    assert report["malformed_header_count"] == 1, report
    assert set(structural_errors(report)) == {
        "malformed_header_count=1",
        "malformed_record_count=1",
        "page_mismatch_count=1",
    }, report

    # Previously these non-duplicate errors were printed but returned exit 0.
    outside = audit_text("<f1r> <! $L=A>\n<f1r.161,@P0> daiin\n")
    assert structural_errors(outside) == ["locus_number_out_of_range_count=1"], outside
    assert set(structural_errors(audit_text(""))) == {
        "page_header_count=0", "record_count=0"
    }

    # Repeated exact tags must remain visible in the structural audit.
    duplicate = "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n<f1r.1,@P0> chedy\n"
    repeated = audit_text(duplicate)
    assert repeated["record_count"] == 2, repeated
    assert repeated["duplicate_record_tag_count"] == 1, repeated
    assert structural_errors(repeated) == ["duplicate_record_tag_count=1"], repeated
    assert repeated["duplicate_record_tags"] == [
        {"tag": "f1r.1,@P0", "first_line": 2, "repeated_line": 3}
    ], repeated

    # An alias of the folio number AND of the line number must not hide
    # a repeated physical locus. The pre-existing page-spelling mismatch
    # remains independently visible; this is a second diagnostic.
    for page, alias in (("f1r", "f01r"), ("f86v4", "f086v4")):
        report = audit_text(
            f"<{page}> first\n"
            f"<{page}.1,@P0> first\n"
            f"<{alias}.01,@P0> repeated\n"
        )
        assert report["duplicate_record_tag_count"] == 1, report
        assert report["duplicate_record_tags"] == [
            {"tag": f"{alias}.01,@P0", "first_line": 2, "repeated_line": 3}
        ], report
        assert report["page_mismatch_count"] == 1, report
        assert structural_errors(report) == [
            "page_mismatch_count=1", "duplicate_record_tag_count=1"
        ], report

        # Different locator codes remain distinct records even if the
        # folio spelling differs; the page-spelling warning is retained.
        distinct_locator = audit_text(
            f"<{page}> first\n"
            f"<{page}.1,@P0> first\n"
            f"<{alias}.01,+P0> other reading\n"
        )
        assert distinct_locator["duplicate_record_tag_count"] == 0, distinct_locator
        assert distinct_locator["page_mismatch_count"] == 1, distinct_locator

    # Same physical line with decimal padding must not evade duplicate
    # detection; page panels and Rosettes obey the same rule. This is
    # identifier integrity, not a claim about token interpretation.
    for page in ("f1r", "f86v4", "fRos"):
        aliased = audit_text(
            f"<{page}> page\n<{page}.1,@P0> first\n<{page}.01,@P0> second\n"
        )
        assert aliased["record_count"] == 2, aliased
        assert aliased["duplicate_record_tag_count"] == 1, aliased
        assert aliased["duplicate_record_tags"] == [
            {"tag": f"{page}.01,@P0", "first_line": 2, "repeated_line": 3}
        ], aliased
        assert structural_errors(aliased) == [
            "duplicate_record_tag_count=1"
        ], aliased
    # Same physical line with a different locator/transcriber is not
    # an alias of the complete IVTFF identifier.
    distinct = audit_text(
        "<f1r> page\n<f1r.1,@P0> first\n<f1r.01,+P0> second\n"
    )
    assert structural_errors(distinct) == [], distinct

    # A damaged record with no opening "<" was previously ignored entirely:
    # a clean-looking report could lose a locus while keeping valid rows.
    damaged = (
        "<f1r> <! $L=A>\n"
        "<f1r.1,@P0> daiin\n"
        "f1r.2,@P0> chedy\n"
        "<fRos> <! $L=B>\n"
        "fRos.23,@L0> daiin\n"
    )
    missing = audit_text(damaged)
    assert missing["record_count"] == 1, missing
    assert missing["malformed_record_count"] == 2, missing
    assert [row["reason"] for row in missing["malformed_records"]] == [
        "missing opening <", "missing opening <"
    ], missing
    assert structural_errors(missing) == ["malformed_record_count=2"], missing

    # A row with a valid locus ID but an indented opening tag used to
    # disappear from the audit without contributing to any error counter.
    indented = audit_text(
        "<f1r> <! $L=A>\n"
        "<f1r.1,@P0> daiin\n"
        " <f1r.2,@P0> chedy\n"
        "\t<f1r.3,@P0> or\n"
        "  f1r.4,@P0> y\n"
    )
    assert indented["record_count"] == 1, indented
    assert indented["malformed_record_count"] == 3, indented
    assert [row["reason"] for row in indented["malformed_records"]] == [
        "leading whitespace before locus <",
        "leading whitespace before locus <",
        "missing opening <",
    ], indented
    assert structural_errors(indented) == ["malformed_record_count=3"], indented

    # An indented page header cannot silently leave the previous active
    # page in force: the subsequent locus must be rejected as unmatched.
    indented_header = audit_text(
        "<f1r> <! $L=A>\n"
        " <f2r> <! $L=B>\n"
        "<f2r.1,@P0> chedy\n"
    )
    assert indented_header["malformed_header_count"] == 1, indented_header
    assert indented_header["page_mismatch_count"] == 1, indented_header
    assert set(structural_errors(indented_header)) == {
        "malformed_header_count=1", "page_mismatch_count=1",
    }, indented_header

    # A malformed indented page header previously vanished without an error,
    # leaving the previous active page in force for subsequent records.
    # The broad candidate detector must not promote either spelling to valid.
    for broken_header in (" <f٢r> <! $L=B>", " <f2r7> <! $L=B>"):
        indented_invalid_boundary = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_header + "\n<f1r.2,@P0> chedy\n"
        )
        assert indented_invalid_boundary["record_count"] == 2, indented_invalid_boundary
        assert indented_invalid_boundary["malformed_header_count"] == 1, indented_invalid_boundary
        assert indented_invalid_boundary["page_mismatch_count"] == 1, indented_invalid_boundary
        assert set(structural_errors(indented_invalid_boundary)) == {
            "malformed_header_count=1", "page_mismatch_count=1",
        }, indented_invalid_boundary
    # A malformed indented page boundary with padding INSIDE the angle
    # brackets was silently discarded: the previous page stayed active.
    # This is diagnostic only; no damaged page becomes a valid header.
    for broken_header in (
        " <f2r > <! $L=B>",
        " < f2r> <! $L=B>",
        "\t<f2r7 > <! $L=B>",
    ):
        broken = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_header + "\n<f1r.2,@P0> chedy\n"
        )
        assert broken["malformed_header_count"] == 1, broken
        assert broken["page_mismatch_count"] == 1, broken
        assert broken["record_count"] == 2, broken
        assert set(structural_errors(broken)) == {
            "malformed_header_count=1", "page_mismatch_count=1",
        }, broken
    # A truncated, indented page boundary with trailing metadata was ignored
    # because the detector compared the entire tag to a page ID. This left
    # f1r active and silently accepted its next locus as belonging to f1r.
    for broken_header in (
        " <f2r <! $L=B",
        " \t<f2r $L=B",
        " <f٢r <! $L=B",
        " <f2r $L=B>",
    ):
        truncated_indented = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_header + "\n<f1r.2,@P0> chedy\n"
        )
        assert truncated_indented["malformed_header_count"] == 1, truncated_indented
        assert truncated_indented["page_mismatch_count"] == 1, truncated_indented
        assert truncated_indented["malformed_record_count"] == 0, truncated_indented
        assert structural_errors(truncated_indented) == [
            "malformed_header_count=1", "page_mismatch_count=1"
        ], truncated_indented

    # A truncated but unrelated indented metadata tag is not a page boundary.
    unrelated_truncated = audit_text(
        "<f1r> <! $L=A>\n <unrelated $L=B\n<f1r.1,@P0> daiin\n"
    )
    assert structural_errors(unrelated_truncated) == [], unrelated_truncated

    # Unrelated metadata, including padding, must remain unclassified.
    unrelated_padded = audit_text(
        "<f1r> <! $L=A>\n <unrelated >\n<f1r.1,@P0> daiin\n"
    )
    assert structural_errors(unrelated_padded) == [], unrelated_padded

    unrelated_indented_tag = audit_text(
        "<f1r> <! $L=A>\n <unrelated>\n<f1r.1,@P0> daiin\n"
    )
    assert structural_errors(unrelated_indented_tag) == [], unrelated_indented_tag

    # Missing "<" in a page header previously vanished as ordinary text,
    # even when an otherwise clean file contained valid records.
    missing_header = audit_text(
        "<f1r> <! $L=A>\n"
        "<f1r.1,@P0> daiin\n"
        "f2r> <! $L=B>\n"
        "<f2r.1,@P0> chedy\n"
        " fRos> <! $L=A>\n"
        "<fRos.23,@L0> or\n"
    )
    assert missing_header["page_header_count"] == 1, missing_header
    assert missing_header["malformed_header_count"] == 2, missing_header
    assert missing_header["page_mismatch_count"] == 2, missing_header
    assert [row["reason"] for row in missing_header["malformed_headers"]] == [
        "missing opening <", "missing opening <"
    ], missing_header
    assert set(structural_errors(missing_header)) == {
        "malformed_header_count=2", "page_mismatch_count=2"
    }, missing_header

    # A page boundary can lose both its opening "<" and closing ">".
    # The adjacent IVTFF metadata comment is an unambiguous structural cue;
    # previously the line vanished and the old page remained active.
    for broken_header in (
        "f2r <! $L=B>",
        "f2r <! $L=B",
        "  fRos <! $L=B>",
    ):
        damaged_metadata_boundary = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_header + "\n<f1r.2,@P0> chedy\n"
        )
        assert damaged_metadata_boundary["malformed_header_count"] == 1, damaged_metadata_boundary
        assert damaged_metadata_boundary["page_mismatch_count"] == 1, damaged_metadata_boundary
        assert damaged_metadata_boundary["record_count"] == 2, damaged_metadata_boundary
        assert structural_errors(damaged_metadata_boundary) == [
            "malformed_header_count=1", "page_mismatch_count=1"
        ], damaged_metadata_boundary

    # A lost opening '<' AND a lost separator before the IVTFF metadata
    # comment used to vanish as free text. The next old-page locus was then
    # silently accepted. Treat this as a broken page boundary, not a page.
    for broken_header in (
        "f2r<! $L=B>", "fRos<! $L=B>",
        "f86v4<! $L=B", "  f٢r<! $L=B>",
    ):
        glued_metadata_boundary = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_header + "\n<f1r.2,@P0> chedy\n"
        )
        assert glued_metadata_boundary["page_header_count"] == 1, glued_metadata_boundary
        assert glued_metadata_boundary["record_count"] == 2, glued_metadata_boundary
        assert glued_metadata_boundary["malformed_header_count"] == 1, glued_metadata_boundary
        assert glued_metadata_boundary["malformed_record_count"] == 0, glued_metadata_boundary
        assert glued_metadata_boundary["page_mismatch_count"] == 1, glued_metadata_boundary
        assert structural_errors(glued_metadata_boundary) == [
            "malformed_header_count=1", "page_mismatch_count=1",
        ], glued_metadata_boundary

    # A folio-like prefix with extra letters, or prose before a comment,
    # is not a plausible page boundary. Avoid false-positive invalidation.
    for prose in ("f2rnotes<! $L=B>", "f2r commentary <! $L=B>"):
        unrelated = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + prose + "\n<f1r.2,@P0> chedy\n"
        )
        assert structural_errors(unrelated) == [], unrelated

    # Free text mentioning a folio, without a metadata comment, is not a header.
    prose_folio = audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\nf2r commentary\n"
    )
    assert structural_errors(prose_folio) == [], prose_folio

    # Also fail closed if the damaged header is the last line: no following
    # locus is required for the error to be observable.
    trailing_header = audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\nf86v4> <! $L=B>\n"
    )
    assert structural_errors(trailing_header) == [
        "malformed_header_count=1"
    ], trailing_header

    # An unterminated page tag was counted as a malformed RECORD, leaving
    # f1r active. The next f1r locus then appeared valid despite the broken
    # boundary. Fail closed for both bare and metadata-bearing headers.
    for broken_header in ("<f2r", "<f2r <! $L=B", "<f2r7"):
        truncated = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_header + "\n<f1r.2,@P0> chedy\n"
        )
        assert truncated["record_count"] == 2, truncated
        assert truncated["malformed_header_count"] == 1, truncated
        assert truncated["malformed_record_count"] == 0, truncated
        assert truncated["page_mismatch_count"] == 1, truncated
        assert set(structural_errors(truncated)) == {
            "malformed_header_count=1", "page_mismatch_count=1",
        }, truncated

    # An incomplete locus or unrelated metadata is not a page boundary.
    incomplete_locus = audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
        "<f1r.2,@P0\n<f1r.3,@P0> chedy\n"
    )
    assert incomplete_locus["malformed_record_count"] == 1, incomplete_locus
    assert incomplete_locus["malformed_header_count"] == 0, incomplete_locus
    assert incomplete_locus["page_mismatch_count"] == 0, incomplete_locus
    incomplete_metadata = audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
        "<unrelated\n<f1r.2,@P0> chedy\n"
    )
    assert incomplete_metadata["malformed_record_count"] == 1, incomplete_metadata
    assert incomplete_metadata["malformed_header_count"] == 0, incomplete_metadata
    assert incomplete_metadata["page_mismatch_count"] == 0, incomplete_metadata

    # Do not flag arbitrary untagged prose that merely starts with f2r>.
    free_text = audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\nf2r>not-a-header\n"
    )
    assert structural_errors(free_text) == [], free_text

    # Ordinary untagged metadata must remain ignored, not classified as a row.
    unrelated = audit_text(
        "non-record metadata\n<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
    )
    assert structural_errors(unrelated) == [], unrelated

    # The independent parser comparison previously lost the second row.
    with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
        source = Path(tmp) / "duplicate.ivtff"
        source.write_text(duplicate, encoding="latin-1")
        try:
            compare(source, "synthetic")
        except ValueError as exc:
            assert "duplicate record ID" in str(exc), str(exc)
        else:
            raise AssertionError("EXP-602 silently accepted a repeated record ID")
        source.write_text(
            duplicate.replace("f1r.1,@P0> chedy", "f1r.2,@P0> chedy"),
            encoding="latin-1",
        )
        clean = compare(source, "synthetic")
        assert clean["record_key_counts"] == {
            "only_A": 0, "only_B": 0, "common": 2
        }, clean

    # A slash-prefixed structural tag is not an ordinary continuation:
    # silently skipping it can leave the previous folio active. This
    # regression is synthetic and does not claim an affected source row.
    for broken_page in ("/<f2r>", "/<fRos>", "/<f86v4,>",
                        "/<f٢r>", "/<f2r <! $L=B"):
        report = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_page + "\n<f1r.2,@P0> chedy\n"
        )
        assert report["record_count"] == 2, report
        assert report["malformed_header_count"] == 1, report
        assert report["page_mismatch_count"] == 1, report
        assert report["continuation_lines"] == 0, report
        assert structural_errors(report) == [
            "malformed_header_count=1", "page_mismatch_count=1"
        ], report

    for broken_record in ("/<f1r.2,@P0> chedy",
                          "/ <f1r.2,@P0> chedy"):
        report = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_record + "\n"
        )
        assert report["record_count"] == 1, report
        assert report["malformed_record_count"] == 1, report
        assert report["continuation_lines"] == 0, report
        assert structural_errors(report) == ["malformed_record_count=1"], report

    # A whitespace-prefixed slash is still a slash continuation; previously
    # it bypassed both the column-zero slash guard and the indented-tag guard.
    # These adversarial mutations must not hide a folio boundary or locus.
    for broken_page in (
        " /<f2r>", "\t/<fRos>", " \t/ <f86v4,>",
        " /<f٢r>", " \t/<f2r <! $L=B",
    ):
        report = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_page + "\n<f1r.2,@P0> chedy\n"
        )
        assert report["page_header_count"] == 1, (broken_page, report)
        assert report["record_count"] == 2, (broken_page, report)
        assert report["malformed_header_count"] == 1, (broken_page, report)
        assert report["page_mismatch_count"] == 1, (broken_page, report)
        assert report["continuation_lines"] == 0, (broken_page, report)
        assert report["malformed_headers"][0]["reason"] == (
            "structural page tag after continuation slash"
        ), (broken_page, report)
        assert structural_errors(report) == [
            "malformed_header_count=1", "page_mismatch_count=1"
        ], (broken_page, report)

    for broken_record in (
        " /<f1r.2,@P0> chedy", "\t/ <f1r.2,@P0> chedy",
    ):
        report = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + broken_record + "\n"
        )
        assert report["record_count"] == 1, (broken_record, report)
        assert report["malformed_record_count"] == 1, (broken_record, report)
        assert report["continuation_lines"] == 0, (broken_record, report)
        assert structural_errors(report) == [
            "malformed_record_count=1"
        ], (broken_record, report)

    # Preserve ordinary indented continuation text and inline comments.
    indented_continuations = audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
        " \t/chedy\n \t/<!free text> daiin\n"
    )
    assert indented_continuations["continuation_lines"] == 2, indented_continuations
    assert structural_errors(indented_continuations) == [], indented_continuations

    # Free-form continuation and a slash followed by an inline comment are
    # not structural tags; do not make the audit reject valid continuations.
    ordinary_slashes = audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
        "/chedy\n/<!free text> daiin\n"
    )
    assert ordinary_slashes["continuation_lines"] == 2, ordinary_slashes
    assert structural_errors(ordinary_slashes) == [], ordinary_slashes

    # Regression: the former [^;>] locator pattern silently accepted
    # whitespace and non-ASCII lookalikes as valid three-character codes.
    # These are synthetic mutations, not defects found in the originals.
    for bad_code in ("   ", "\tP0", "éP0", "@\u200b0", "@P\u200b"):
        report = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + f"<f1r.2,{bad_code}> chedy\n"
        )
        assert report["record_count"] == 1, (bad_code, report)
        assert report["malformed_record_count"] == 1, (bad_code, report)
        assert structural_errors(report) == ["malformed_record_count=1"], report

    for bad_transcriber in (" ", "\t", "é", "\u200b"):
        report = audit_text(
            "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
            + f"<f1r.2,@P0;{bad_transcriber}> chedy\n"
        )
        assert report["record_count"] == 1, (bad_transcriber, report)
        assert report["malformed_record_count"] == 1, (bad_transcriber, report)

    # Do not overfit to the most common +P0 code: these are all observed
    # code spellings in the current ZL3b source, plus an ASCII transcriber.
    for idx, code in enumerate(("@P0", "+P0", "&Lz", "/L0", "!Lf", "=P0", "~Lt"), 1):
        report = audit_text(
            "<f1r> <! $L=A>\n" + f"<f1r.{idx},{code}> daiin\n"
        )
        assert structural_errors(report) == [], (code, report)
    assert structural_errors(audit_text(
        "<f1r> <! $L=A>\n<f1r.1,@P0;A> daiin\n"
    )) == []

    # Exercise the guard on the three original sources, without changing them.
    for label, source in SOURCES:
        report = audit_text(source.read_text(encoding="utf-8-sig"))
        assert structural_errors(report) == [], (label, structural_errors(report))
        assert report["duplicate_record_tag_count"] == 0, (
            label, report["duplicate_record_tags"]
        )
    print("IVTFF page/locus and duplicate-ID regression tests passed.")


if __name__ == "__main__":
    main()
