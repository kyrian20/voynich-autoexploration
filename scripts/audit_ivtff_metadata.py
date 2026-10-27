#!/usr/bin/env python3
"""Audit IVTFF folio-language metadata without allocating an EXP identifier."""
from __future__ import annotations
import collections, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/transcriptions/eva_zl3b.txt"
HEADER = re.compile(r"^<(f(?:\d+[rv][1-6]?|Ros))>\s*(.*)$")
LANGUAGE = re.compile(r"\$L\s*=\s*([AB])(?=\s|>|$)")
QUIRE = re.compile(r"\$Q\s*=\s*([AB])(?=\s|>|$)")

def parse_currier_language(metadata: str) -> str | None:
    """Return Currier language only from IVTFF $L=A/B; never infer it from $Q or $I."""
    values = set(re.findall(r"\$L\s*=\s*([^\s>]+)", metadata))
    if len(values) > 1:
        raise ValueError(f"Conflicting IVTFF $L assignments: {sorted(values)}")
    match = LANGUAGE.search(metadata)
    return match.group(1) if match else None

def collect_folio_languages(text: str) -> tuple[dict[str, str], list[str], int]:
    """Count each physical folio header once; never silently overwrite its $L.

    Duplicate headers can otherwise change Currier A/B counts depending on
    source order. This is a metadata guard, not full IVTFF conformance.
    """
    pages: dict[str, str] = {}
    seen: set[str] = set()
    q_as_language: list[str] = []
    for line_no, row in enumerate(text.splitlines(), 1):
        m = HEADER.match(row)
        if not m:
            continue
        folio, metadata = m.groups()
        if folio in seen:
            raise ValueError(f"Duplicate IVTFF folio header {folio} at line {line_no}")
        seen.add(folio)
        lang = parse_currier_language(metadata)
        if lang:
            pages[folio] = lang
        q = QUIRE.search(metadata)
        if q and not lang:
            q_as_language.append(folio)
    return pages, q_as_language, len(seen)


def main() -> None:
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8-sig")
    pages, q_as_language, header_count = collect_folio_languages(text)
    counts = collections.Counter(pages.values())
    result = {
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "folio_headers": header_count,
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
