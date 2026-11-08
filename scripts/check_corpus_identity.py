#!/usr/bin/env python3
"""Verify frozen identities of excluded reference corpora without rewriting them."""
import argparse
import hashlib
import json
from pathlib import Path


def audit(root: Path, manifest: Path) -> list[str]:
    data = json.loads(manifest.read_text(encoding="utf-8"))
    errors = []
    for entry in data["excluded_from_new_language_baselines"]:
        rel = Path(entry["path"])
        if rel.is_absolute() or ".." in rel.parts:
            errors.append(f"{rel}: unsafe path")
            continue
        path = root / rel
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
