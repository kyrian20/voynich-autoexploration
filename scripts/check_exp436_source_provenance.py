#!/usr/bin/env python3
"""Fail-closed source gate for *new* EXP-436 comparisons, not historical replay.

Usage: python scripts/check_exp436_source_provenance.py --latin PATH --italian PATH
No historical results or input files are changed. This only validates identity
against an explicitly supplied SHA-256 allowlist; it does not certify language.
"""
import argparse
import hashlib
import json
from pathlib import Path

# Frozen identities from EXP-436/CORRECTION.md; neither may be presented
# as a verified Latin/Italian historical replay.
KNOWN_INVALID = {
    "eaa456256c46507f872efd965335b370605e6d323ca89ef2012cb71b516183d7":
        "historical Caesar control is an English translation",
}
def inspect(path):
    path = Path(path)
    try:
        is_file = path.is_file()
    except (OSError, RuntimeError) as exc:
        return {"path": str(path), "status": "UNREADABLE",
                "reason": type(exc).__name__}
    if not is_file:
        return {"path": str(path), "status": "MISSING"}
    try:
        hasher = hashlib.sha256()
        total_bytes = 0
        has_non_whitespace = False
        has_nul = False
        has_forbidden_control = False
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                hasher.update(chunk)
                if b"\x00" in chunk:
                    has_nul = True
                if any(byte < 32 and byte not in (9, 10, 11, 12, 13)
                       or byte == 127 for byte in chunk):
                    has_forbidden_control = True
                total_bytes += len(chunk)
                if not has_non_whitespace and chunk.strip(bytes((32, 9, 13, 10, 11, 12))):
                    has_non_whitespace = True
        digest = hasher.hexdigest()
    except (OSError, RuntimeError) as exc:
        return {"path": str(path), "status": "UNREADABLE",
                "reason": type(exc).__name__}
    if has_nul:
        return {"path": str(path), "sha256": digest, "status": "BINARY_SOURCE",
                "reason": "NUL bytes are not valid in a plain-text comparison corpus"}
    if has_forbidden_control:
        return {"path": str(path), "sha256": digest, "status": "BINARY_SOURCE",
                "reason": "Disallowed ASCII control byte in plain-text comparison corpus"}
    if total_bytes == 0:
        return {"path": str(path), "sha256": digest, "status": "EMPTY_SOURCE",
                "reason": "An empty file cannot serve as a comparison corpus"}
    if not has_non_whitespace:
        return {"path": str(path), "sha256": digest, "status": "BLANK_SOURCE",
                "reason": "Whitespace-only input cannot serve as a comparison corpus"}
    return {"path": str(path), "sha256": digest,
            "status": "REJECTED" if digest in KNOWN_INVALID else "UNVERIFIED",
            "reason": KNOWN_INVALID.get(digest)}

def evaluate(latin, italian, approved):
    sources = {"latin": inspect(latin), "italian": inspect(italian)}
    for label, entry in sources.items():
        if entry["status"] == "UNVERIFIED" and approved.get(label) == entry["sha256"]:
            entry["status"] = "HASH_MATCH"
    # Two language roles must not silently reuse identical bytes, even when
    # the caller supplies the same digest as both approvals.
    if (all(x["status"] == "HASH_MATCH" for x in sources.values())
            and sources["latin"]["sha256"] == sources["italian"]["sha256"]):
        for entry in sources.values():
            entry["status"] = "DUPLICATE_SOURCE"
            entry["reason"] = "Latin and Italian controls have identical bytes"
    ok = all(x["status"] == "HASH_MATCH" for x in sources.values())
    return {"ok": ok, "sources": sources,
            "limitation": "Hash match is not language, edition, historical-input or tokenizer certification."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--latin", required=True)
    parser.add_argument("--italian", required=True)
    parser.add_argument("--approved-latin-sha256", required=True)
    parser.add_argument("--approved-italian-sha256", required=True)
    args = parser.parse_args()
    approved = {"latin": args.approved_latin_sha256.lower(),
                "italian": args.approved_italian_sha256.lower()}
    if any(len(v) != 64 or any(c not in "0123456789abcdef" for c in v)
           for v in approved.values()):
        parser.error("approved hashes must be 64 hex characters")
    report = evaluate(args.latin, args.italian, approved)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
