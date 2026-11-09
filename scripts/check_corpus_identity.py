#!/usr/bin/env python3
"""Verify frozen identities of excluded reference corpora without rewriting them."""
import argparse
import hashlib
import json
from pathlib import Path


# Independently pinned membership: the manifest must not silently drop exclusions.
FROZEN_EXCLUDED_PATHS = frozenset({
    "data/reference_corpora/arabic/quran_arabic.txt",
    "data/reference_corpora/english/kjv_bible.txt",
    "data/reference_corpora/latin/caesar_gallic_wars.txt",
    "data/reference_corpora/latin/cicero_caesar_latin.txt",
    "data/reference_corpora/latin/cicero_de_officiis_latin.txt",
    "data/reference_corpora/latin/vulgate.txt",
})


def audit(root: Path, manifest: Path) -> list[str]:
    data = json.loads(manifest.read_text(encoding="utf-8"))
    errors = []
    entries = data["excluded_from_new_language_baselines"]
    paths = [entry["path"] for entry in entries]
    if len(paths) != len(set(paths)):
        errors.append("manifest: duplicate excluded corpus path")
    if set(paths) != FROZEN_EXCLUDED_PATHS:
        errors.append("manifest: excluded corpus membership mismatch")
    resolved_root = root.resolve()
    for entry in data["excluded_from_new_language_baselines"]:
        rel = Path(entry["path"])
        if rel.is_absolute() or ".." in rel.parts:
            errors.append(f"{rel}: unsafe path")
            continue
        path = root / rel
        if not path.resolve().is_relative_to(resolved_root):
            errors.append(f"{rel}: unsafe path (symlink escapes repository)")
            continue
        if not path.is_file():
            errors.append(f"{rel}: missing; cannot verify historical identity")
            continue
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != entry["sha256"] or len(raw) != entry["bytes"]:
            errors.append(f"{rel}: manifest identity mismatch (sha256/bytes)")
        for line in entry.get("header_title", []) + entry.get("header_language", []):
            if line.encode("utf-8") not in raw[:16384]:
                errors.append(f"{rel}: missing recorded header {line!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--manifest", type=Path, default=Path("research/CORPUS_IDENTITY_REVIEW.json"))
    args = parser.parse_args()
    errors = audit(args.root, args.root / args.manifest)
    for error in errors:
        print("FAIL:", error)
    if errors:
        return 1
    print("PASS: excluded corpus bytes and recorded headers match inventory; exclusion still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
