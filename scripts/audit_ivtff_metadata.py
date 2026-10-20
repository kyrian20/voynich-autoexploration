#!/usr/bin/env python3
"""Audit IVTFF folio-language metadata without allocating an EXP identifier."""
from __future__ import annotations
import collections, hashlib, json, re
from pathlib import Path

SOURCE = Path("data/transcriptions/eva_zl3b.txt")
HEADER = re.compile(r"^<f(\d+[rv])>\s*(.*)$")
LANGUAGE = re.compile(r"\$L\s*=\s*([AB])(?=\s|>|$)")
QUIRE = re.compile(r"\$Q\s*=\s*([AB])(?=\s|>|$)")

def parse_currier_language(metadata: str) -> str | None:
    """Return Currier language only from IVTFF $L=A/B; never infer it from $Q or $I."""
    match = LANGUAGE.search(metadata)
    return match.group(1) if match else None

def main() -> None:
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8-sig")
    pages = {}
    q_as_language = []
    for row in text.splitlines():
        m = HEADER.match(row)
        if not m:
            continue
        folio, metadata = m.groups()
        lang = parse_currier_language(metadata)
        if lang:
            pages[folio] = lang
        q = QUIRE.search(metadata)
        if q and not lang:
            q_as_language.append(folio)
    counts = collections.Counter(pages.values())
    result = {
        "source": str(SOURCE),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "folio_headers": sum(1 for row in text.splitlines() if HEADER.match(row)),
        "folios_with_currier_language": len(pages),
        "language_counts": dict(sorted(counts.items())),
        "headers_with_AB_quire_but_no_language": q_as_language,
        "interpretation": "$L is Currier language; $Q is quire and must not be used as a substitute.",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not pages or not counts.get("A") or not counts.get("B"):
        raise SystemExit("IVTFF metadata audit failed: expected both Currier A and B in $L.")
    if len(pages) < 100:
        raise SystemExit(f"IVTFF metadata audit failed: only {len(pages)} classified folios.")

if __name__ == "__main__":
    main()
