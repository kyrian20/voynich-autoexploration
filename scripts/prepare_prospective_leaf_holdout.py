#!/usr/bin/env python3
"""Prospective, deterministic physical-leaf split; not a decipherment experiment.

Existing Voynich leaves have been studied before: this split is NOT an untouched
historical blind test. It is only a locked partition for future candidate rules.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_NAMES = ("eva_zl3b.txt", "eva_it2a.txt")
SALT = "VOYNICH-FUTURE-RULES-2026-10-23-v1"
HEADER = re.compile(r"^<f(\d+)[rv](?:[.,][^>]*)?>")

def leaves_from_bytes(raw: bytes) -> set[int]:
    leaves = set()
    for line in raw.decode("utf-8-sig").splitlines():
        match = HEADER.match(line)
        if match:
            leaves.add(int(match.group(1)))
    if not leaves:
        raise ValueError("No folio headers found: cannot construct a split")
    return leaves

def partition(leaf: int, salt: str = SALT) -> str:
    if leaf < 1:
        raise ValueError("Leaf numbers must be positive")
    value = int.from_bytes(hashlib.sha256(f"{salt}:{leaf}".encode()).digest()[:8], "big") % 10000
    return "train" if value < 7000 else ("development" if value < 8500 else "test")

def build_manifest(source_bytes: dict[str, bytes], salt: str = SALT) -> dict:
    if set(source_bytes) != set(SOURCE_NAMES):
        raise ValueError("Both named sources are required; do not silently substitute editions")
    sources = {name: leaves_from_bytes(source_bytes[name]) for name in SOURCE_NAMES}
    shared = sources[SOURCE_NAMES[0]] & sources[SOURCE_NAMES[1]]
    if len(shared) < 50:
        raise ValueError("Too few common physical leaves for a meaningful partition")
    groups = {name: sorted(leaf for leaf in shared if partition(leaf, salt) == name)
              for name in ("train", "development", "test")}
    if any(len(group) < 5 for group in groups.values()):
        raise ValueError("Partition has fewer than five physical leaves in a group")
    assert set().union(*map(set, groups.values())) == shared
    assert not any(set(groups[a]) & set(groups[b]) for a,b in
                   (("train","development"), ("train","test"), ("development","test")))
    return {
        "schema_version": 1,
        "status": "PROPOSED_FOR_FUTURE_RULES",
        "salt": salt,
        "unit": "physical_leaf_number; recto and verso always grouped",
        "allocation": {"train": 0.70, "development": 0.15, "test": 0.15},
        "selection": "shared leaves present in both editions, from header identifiers only",
        "caveat": "Not a historically untouched holdout; previous analyses have inspected these leaves.",
        "corpora": {
            name: {"path": f"data/transcriptions/{name}",
                   "sha256": hashlib.sha256(source_bytes[name]).hexdigest(),
                   "leaf_count": len(sources[name])}
            for name in SOURCE_NAMES
        },
        "source_only_leaves": {
            name: sorted(sources[name] - shared) for name in SOURCE_NAMES
        },
        "eligible_count": len(shared),
        "partitions": groups,
        "counts": {name: len(values) for name, values in groups.items()},
        "forbidden": ["selecting rules on test folios", "tuning on test outcomes",
                      "claiming a historically independent or semantic validation"]
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, help="Write stable JSON manifest to this path")
    args = parser.parse_args()
    raw = {name: (ROOT / "data/transcriptions" / name).read_bytes() for name in SOURCE_NAMES}
    payload = json.dumps(build_manifest(raw), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

if __name__ == "__main__":
    main()
