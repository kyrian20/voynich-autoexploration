#!/usr/bin/env python3
"""Additive duplicate-page guard; leave frozen EXP-173 dependencies unchanged.

This checks uniqueness under the historical metadata HEADER pattern, not
complete IVTFF conformance, row-to-folio association or semantic meaning.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_ivtff_metadata import HEADER, SOURCE
from scripts.ivtff_physical_rows import checked_physical_lines


def physical_header_identity(page: str) -> tuple:
    """Compare numeric folios as physical pages, not zero-padded strings.

    Keep the historical HEADER extractor unchanged; reject non-ASCII digits
    that its broad \\d pattern might otherwise admit.
    """
    if page == "fRos":
        return ("Ros",)
    match = re.fullmatch(r"f([0-9]+)([rv])([1-6]?)", page)
    if match is None:
        raise ValueError(f"Invalid IVTFF physical folio header: {page}")
    return (int(match.group(1)), match.group(2), match.group(3))


def audit_unique_page_headers(text: str) -> dict:
    """Reject repeated physical page headers before any A/B summary is trusted."""
    first_line: dict[tuple, int] = {}
    for line_no, row in checked_physical_lines(text):
        match = HEADER.match(row)
        if match is None:
            continue
        page = match.group(1)
        identity = physical_header_identity(page)
        if identity in first_line:
            raise ValueError(
                f"Duplicate IVTFF folio header {page} at line {line_no}; "
                f"first seen at line {first_line[identity]}"
            )
        first_line[identity] = line_no
    return {
        "status": "UNIQUE_HEADERS_UNDER_HISTORICAL_PATTERN_NOT_FULL_IVTFF_CONFORMANCE",
        "folio_headers": len(first_line),
        "distinct_folio_ids": len(first_line),
    }


def main() -> None:
    raw = SOURCE.read_bytes()
    result = audit_unique_page_headers(raw.decode("utf-8-sig"))
    result["source"] = str(SOURCE.relative_to(ROOT))
    result["source_sha256"] = hashlib.sha256(raw).hexdigest()
    if result["folio_headers"] != 227:
        raise SystemExit(
            f"Frozen ZL3b header census changed: {result['folio_headers']} != 227"
        )
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
