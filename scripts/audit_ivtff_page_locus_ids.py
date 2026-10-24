#!/usr/bin/env python3
"""Non-destructive structural audit of IVTFF page and locus identifiers.

Checks page headers, locus-ID shape, active-page agreement, numeric locus range,
and record coverage. It does not alter transcriptions or certify every IVTFF
semantic rule. Special foldout page names (including f86v4/f86v5/f86v6) and
the combined Rosettes page fRos are explicitly supported.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("ZL3b", ROOT / "data/transcriptions/eva_zl3b.txt"),
    ("ZL3a", ROOT / "data/transcriptions/zl3a.txt"),
    ("IT2a", ROOT / "data/transcriptions/eva_it2a.txt"),
]
PAGE_RE = re.compile(r"^f(?:\d+[rv][1-6]?|Ros)$")
LOCUS_RE = re.compile(
    r"^(?P<page>f(?:\d+[rv][1-6]?|Ros))\."
    r"(?P<num>\d{1,3}),(?P<code>[^;>]{3})(?:;(?P<transcriber>[^;>]))?$"
)
# Catch a damaged locus prefix before the generic non-record skip below.
# This does not treat arbitrary free-text metadata as an IVTFF record.
MISSING_OPEN_LOCUS_RE = re.compile(r"^f(?:\d+[rv][1-6]?|Ros)\.\d+,")


def audit_text(text: str) -> dict:
    active_page = None
    headers = []
    records = []
    seen_record_tags = {}
    duplicate_record_tags = []
    malformed_headers = []
    malformed_records = []
    page_mismatches = []
    out_of_range = []
    ignored_comments = 0
    continuation_lines = 0

    for line_no, raw in enumerate(text.splitlines(), 1):
        if raw.startswith("#"):
            ignored_comments += 1
            continue
        if raw.startswith("/"):
            continuation_lines += 1
            continue
        if not raw.startswith("<"):
            # Only a column-zero tag is a structural row. Previously an
            # indented, otherwise valid locus/header vanished silently.
            # Do not promote it to a valid row: fail closed and retain evidence.
            stripped = raw.lstrip(" \t")
            if stripped.startswith("<"):
                candidate = stripped[1:].split(">", 1)[0]
                if LOCUS_RE.fullmatch(candidate) or MISSING_OPEN_LOCUS_RE.match(candidate):
                    malformed_records.append({
                        "line": line_no, "raw": raw[:180],
                        "reason": "leading whitespace before locus <",
                    })
                elif PAGE_RE.fullmatch(candidate):
                    malformed_headers.append({"line": line_no, "page": candidate})
                    active_page = None
            elif MISSING_OPEN_LOCUS_RE.match(stripped):
                malformed_records.append({
                    "line": line_no, "raw": raw[:180], "reason": "missing opening <",
                })
            continue
        end = raw.find(">")
        if end < 0:
            malformed_records.append({"line": line_no, "raw": raw[:180], "reason": "missing >"})
            continue
        tag = raw[1:end]
        if "," not in tag:
            if not PAGE_RE.fullmatch(tag):
                malformed_headers.append({"line": line_no, "page": tag})
                active_page = None
            else:
                active_page = tag
                headers.append({"line": line_no, "page": tag})
            continue

        match = LOCUS_RE.fullmatch(tag)
        if not match:
            malformed_records.append({"line": line_no, "tag": tag, "reason": "invalid locus-ID shape"})
            continue
        rec = match.groupdict()
        rec["line"] = line_no
        records.append(rec)
        if tag in seen_record_tags:
            duplicate_record_tags.append({
                "tag": tag,
                "first_line": seen_record_tags[tag],
                "repeated_line": line_no,
            })
        else:
            seen_record_tags[tag] = line_no
        if active_page is None:
            page_mismatches.append({"line": line_no, "id_page": rec["page"], "active_page": None})
        elif rec["page"] != active_page:
            page_mismatches.append({"line": line_no, "id_page": rec["page"], "active_page": active_page})
        num = int(rec["num"])
        if not 1 <= num <= 160:
            out_of_range.append({"line": line_no, "id": tag, "number": num})

    return {
        "page_header_count": len(headers),
        "distinct_page_headers": len({h["page"] for h in headers}),
        "record_count": len(records),
        "duplicate_record_tags": duplicate_record_tags[:50],
        "duplicate_record_tag_count": len(duplicate_record_tags),
        "ignored_comment_lines": ignored_comments,
        "continuation_lines": continuation_lines,
        "malformed_headers": malformed_headers[:50],
        "malformed_header_count": len(malformed_headers),
        "malformed_records": malformed_records[:50],
        "malformed_record_count": len(malformed_records),
        "page_mismatches": page_mismatches[:50],
        "page_mismatch_count": len(page_mismatches),
        "locus_numbers_outside_1_to_160": out_of_range[:50],
        "locus_number_out_of_range_count": len(out_of_range),
        "page_names": sorted({h["page"] for h in headers}),
    }



def structural_errors(report: dict) -> list[str]:
    """Reject observed structural anomalies rather than merely listing them."""
    errors = []
    for key in (
        "malformed_header_count",
        "malformed_record_count",
        "page_mismatch_count",
        "locus_number_out_of_range_count",
        "duplicate_record_tag_count",
    ):
        if report[key]:
            errors.append(f"{key}={report[key]}")
    if report["page_header_count"] == 0:
        errors.append("page_header_count=0")
    if report["record_count"] == 0:
        errors.append("record_count=0")
    return errors


def main() -> None:
    files = []
    for label, path in SOURCES:
        if not path.is_file():
            raise FileNotFoundError(f"Required transcription missing; refusing partial audit: {path}")
        raw = path.read_bytes()
        report = audit_text(raw.decode("utf-8-sig"))
        files.append({
            "transcription": label,
            "source": str(path.relative_to(ROOT)),
            "source_bytes": len(raw),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            **report,
        })
    print(json.dumps({
        "audit": "ivtff_page_and_locus_id_coverage",
        "version": 1,
        "specification_reference": "IVTFF format 2.0.2, §§4.2, 5.4, 6.3–6.5",
        "purpose": "Structural inventory only; source files and historical experiment outputs remain unchanged.",
        "limitations": [
            "This is not a complete implementation of every IVTFF semantic constraint.",
            "The expected locus-number ceiling of 160 is a corpus sanity check based on the current format documentation, not a universal rule for future files.",
            "ZL3a and ZL3b are related transcriptions, not independent samples.",
        ],
        "files": files,
    }, indent=2, ensure_ascii=False))
    failures = [
        f"{item['transcription']}: {error}"
        for item in files
        for error in structural_errors(item)
    ]
    if failures:
        raise SystemExit("IVTFF structural audit failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
