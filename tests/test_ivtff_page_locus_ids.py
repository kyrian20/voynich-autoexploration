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
            "<f1r> <! $L=A>\\n<f1r.1,@P0> daiin\\n"
            + broken_header + "\\n<f1r.2,@P0> chedy\\n"
        )
        assert comma_boundary["record_count"] == 2, comma_boundary
        assert comma_boundary["malformed_header_count"] == 1, comma_boundary
        assert comma_boundary["malformed_record_count"] == 0, comma_boundary
        assert comma_boundary["page_mismatch_count"] == 1, comma_boundary
        assert comma_boundary["malformed_headers"][0]["reason"] == "comma in page header"
        assert structural_errors(comma_boundary) == [
            "malformed_header_count=1", "page_mismatch_count=1",
        ], comma_boundary

    # A malformed locus containing a comma remains a record error and must
    # not invalidate the active page or be mistaken for a page boundary.
    comma_locus = audit_text(
        "<f1r> <! $L=A>\\n<f1r.1,@P0,> daiin\\n<f1r.2,@P0> chedy\\n"
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
