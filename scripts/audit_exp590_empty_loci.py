#!/usr/bin/env python3
"""Read-only, locus-level reconciliation of EXP-590's non-tokenizing records.

This audits input selection, not historical execution or IVTFF conformance.
Original transcriptions and historical experiment outputs are never modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/transcriptions/eva_zl3b.txt"
SOURCE_SHA256 = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
RECORD = re.compile(
    r"^<(?P<tag>(?P<folio>f(?:\d+[rv][1-6]?|Ros))\.(?P<number>\d+),[^>]*)>\s*(?P<body>.*)$"
)
TOKEN = re.compile(r"[a-z]+")
ANNOTATIONS = re.compile(r"<[^>]*>|\{[^}]*\}|\[[^\]]*\]")
EXPECTED = (5385, 5376, 9, 39594, 853)


def inspect_text(text: str) -> tuple[dict, list[tuple[str, int]]]:
    """Inventory every raw-nonempty locus under the frozen EXP-590 ASCII view."""
    nonempty_body = 0
    total_tokens = 0
    total_daiin = 0
    selected = []
    skipped = []
    for source_line, raw in enumerate(text.splitlines(), 1):
        match = RECORD.match(raw)
        if not match or not match["body"].strip():
            continue
        nonempty_body += 1
        tag, body = match["tag"], match["body"]
        tokens = TOKEN.findall(ANNOTATIONS.sub(" ", body).lower())
        if tokens:
            selected.append((match["folio"], int(match["number"])))
            total_tokens += len(tokens)
            total_daiin += tokens.count("daiin")
        else:
            skipped.append({
                "tag": tag,
                "source_line": source_line,
                "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
                "raw_body": body,
                "reason": "no_ascii_tokens_after_historical_annotation_removal",
            })
    return {
        "records_with_nonempty_raw_body": nonempty_body,
        "records_with_ascii_tokens": len(selected),
        "records_with_no_ascii_tokens": len(skipped),
        "tokens": total_tokens,
        "exact_daiin_occurrences": total_daiin,
        "empty_loci": skipped,
    }, selected


def audit_source(path: Path, *, check_canonical: bool = False) -> dict:
    from scripts.exp590_daiin_position import load_lines
    raw = path.read_bytes()
    sha256 = hashlib.sha256(raw).hexdigest()
    result, expected_selected = inspect_text(raw.decode("utf-8-sig"))
    production_bytes, production_lines = load_lines(path)
    if production_bytes != raw:
        raise ValueError("Production loader read different bytes")
    actual_selected = [(row["folio"], row["line"]) for row in production_lines]
    if expected_selected != actual_selected:
        raise ValueError("EXP-590 locus selection differs from independent inventory")
    if sum(len(row["tokens"]) for row in production_lines) != result["tokens"]:
        raise ValueError("EXP-590 token count differs")
    if sum(row["tokens"].count("daiin") for row in production_lines) != result["exact_daiin_occurrences"]:
        raise ValueError("EXP-590 daiin count differs")
    counts = tuple(result[key] for key in (
        "records_with_nonempty_raw_body", "records_with_ascii_tokens",
        "records_with_no_ascii_tokens", "tokens", "exact_daiin_occurrences"))
    if check_canonical and (sha256 != SOURCE_SHA256 or counts != EXPECTED):
        raise ValueError(f"Frozen ZL3b/EXP-590 coverage changed: sha={sha256}, counts={counts}")
    return {
        "status": "RECONCILED_INPUT_SELECTION_ONLY",
        "source": path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path),
        "source_sha256": sha256,
        "historical_view": "lowercase ASCII runs after removing IVTFF tags, braces, square brackets",
        "scope": "Explains raw-nonempty versus tokenized-record denominator; no historical simulation rerun",
        **result,
        "limitations": [
            "No full IVTFF conformance or independent semantic adjudication.",
            "Empty after historical ASCII filtering does not mean blank manuscript text.",
            "No changes to historical results or original transcriptions.",
            "Counts are for ZL3b, not an independent replication on another manuscript.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--check-canonical", action="store_true")
    args = parser.parse_args()
    result = audit_source(SOURCE, check_canonical=args.check_canonical)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in (
        "source_sha256", "records_with_nonempty_raw_body",
        "records_with_ascii_tokens", "records_with_no_ascii_tokens",
        "tokens", "exact_daiin_occurrences")}, sort_keys=True))


if __name__ == "__main__":
    main()
