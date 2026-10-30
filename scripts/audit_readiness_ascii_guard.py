#!/usr/bin/env python3
"""Fail-closed ASCII-numeral gate before the frozen readiness reader runs.

This is additive: audit_research_readiness.py is a historical SHA-256
dependency of EXP-173 and must remain byte-identical. This gate checks
candidate row identifiers, not full IVTFF conformance or semantic validity.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("eva_zl3b.txt", "zl3a.txt", "eva_it2a.txt")
# Broad diagnostic match: Python \d intentionally includes Unicode decimals.
# Acceptance of identifiers by the frozen reader is NOT delegated to this regex.
ROW_PREFIX = re.compile(r"^<f(?:\d+[rv]\d*|Ros)\.\d+,")
ASCII = frozenset("0123456789")


def scan_text(text: str, source: str = "<fixture>") -> int:
    """Count candidate records and reject non-ASCII decimal numerals in IDs."""
    count = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        match = ROW_PREFIX.match(line)
        if match is None:
            continue
        count += 1
        prefix = match.group(0)
        if any(ch.isdecimal() and ch not in ASCII for ch in prefix):
            raise ValueError(
                f"{source}:{lineno}: non-ASCII decimal numeral in IVTFF row ID: {prefix!r}"
            )
    return count


def audit_sources(root: Path = ROOT) -> dict:
    files = []
    for filename in SOURCES:
        path = root / "data" / "transcriptions" / filename
        raw = path.read_bytes()  # Missing input must fail; never skip it.
        files.append({
            "source": str(path.relative_to(root)),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "source_bytes": len(raw),
            "candidate_row_prefixes_checked": scan_text(raw.decode("utf-8-sig"), filename),
        })
    return {
        "audit": "readiness_ascii_numeral_preflight",
        "version": 1,
        "status": "PASS",
        "scope": "Candidate IVTFF row ID prefixes only; not complete IVTFF conformance",
        "frozen_reader": "scripts/audit_research_readiness.py (not modified)",
        "files": files,
    }


def main() -> None:
    print(json.dumps(audit_sources(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
