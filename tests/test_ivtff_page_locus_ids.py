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
