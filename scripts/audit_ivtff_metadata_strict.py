#!/usr/bin/env python3
"""Reject contradictory $L metadata on repeated page headers without editing history.

This is an additive validation gate. The historical audit_ivtff_metadata.py
remains byte-identical because its SHA-256 is a dependency of archived
EXP-173 reader-bridge snapshots.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import audit_ivtff_metadata as legacy

SOURCE = legacy.SOURCE


def validate(source: Path = SOURCE) -> dict:
    raw = source.read_bytes()
    seen: dict[str, str] = {}
    headers = 0
    repeated_consistent = 0
    for lineno, line in enumerate(raw.decode("utf-8-sig").splitlines(), 1):
        match = legacy.HEADER.match(line)
        if not match:
            continue
        headers += 1
        page, metadata = match.groups()
        language = legacy.parse_currier_language(metadata)
        if language is None:
            continue
        prior = seen.get(page)
        if prior is not None and prior != language:
            raise ValueError(
                f"Conflicting Currier $L across headers for {page} at line "
                f"{lineno}: {prior} versus {language}"
            )
        if prior is not None:
            repeated_consistent += 1
        seen[page] = language
    return {
        "audit": "ivtff_duplicate_currier_language_guard",
        "source": str(source),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "folio_headers": headers,
        "folios_with_language": len(seen),
        "consistent_repeated_language_headers": repeated_consistent,
        "contradictory_repeated_language_headers": 0,
        "scope": "Same page identifier with contradictory $L; not full IVTFF conformance",
    }


def main() -> None:
    print(json.dumps(validate(SOURCE), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
