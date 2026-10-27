#!/usr/bin/env python3
"""Additive duplicate-page guard; leave frozen EXP-173 dependencies unchanged.

This checks uniqueness under the historical metadata HEADER pattern, not
complete IVTFF conformance, row-to-folio association or semantic meaning.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_ivtff_metadata import HEADER, SOURCE
from scripts.ivtff_physical_rows import checked_physical_lines


def audit_unique_page_headers(text: str) -> dict:
    """Reject repeated physical page headers before any A/B summary is trusted."""
    first_line: dict[str, int] = {}
    for line_no, row in checked_physical_lines(text):
        match = HEADER.match(row)
        if match is None:
            continue
        page = match.group(1)
        if page in first_line:
            raise ValueError(
                f"Duplicate IVTFF folio header {page} at line {line_no}; "
                f"first seen at line {first_line[page]}"
            )
        first_line[page] = line_no
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
