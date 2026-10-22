#!/usr/bin/env python3
"""Regression fixtures for IVTFF page and locus-ID structural coverage."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_ivtff_page_locus_ids import audit_text


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
    print("IVTFF page/locus identifier regression tests passed.")


if __name__ == "__main__":
    main()
