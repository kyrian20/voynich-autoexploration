#!/usr/bin/env python3
"""Version 2 of prospective leaf manifest: panel-aware; preserves v1 assignments.

This corrects a real v1 omission: IVTFF folio IDs such as <f67r1.1,...>
were not recognized. The v1 script and manifest remain unchanged for provenance.
No manuscript text is interpreted, no candidate rule is evaluated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from prepare_prospective_leaf_holdout import ROOT, SOURCE_NAMES, SALT, partition

# Optional numeric panel after recto/verso; leaf 67r1 and 67r2 are leaf 67.
HEADER_V2 = re.compile(r"^<f(\d+)[rv]\d*(?:[.,][^>]*)?>")


def leaves_from_bytes(raw: bytes) -> set[int]:
    leaves = set()
    for line in raw.decode("utf-8-sig").splitlines():
        match = HEADER_V2.match(line)
        if match:
            leaves.add(int(match.group(1)))
    if not leaves:
        raise ValueError("No folio headers found")
    return leaves


def build_manifest(source_bytes: dict[str, bytes]) -> dict:
    if set(source_bytes) != set(SOURCE_NAMES):
        raise ValueError("Both named transcriptions required")
    sources = {name: leaves_from_bytes(source_bytes[name]) for name in SOURCE_NAMES}
    shared = sources[SOURCE_NAMES[0]] & sources[SOURCE_NAMES[1]]
    if len(shared) < 50:
        raise ValueError("Fewer than 50 common leaves")
    groups = {group: sorted(n for n in shared if partition(n, SALT) == group)
              for group in ("train", "development", "test")}
    if any(len(group) < 5 for group in groups.values()):
        raise ValueError("Fewer than five leaves in a partition")
    if sum(map(len, groups.values())) != len(shared):
        raise AssertionError("Partition not exhaustive")
    return {
        "schema_version": 2,
        "status": "PROPOSED_FOR_FUTURE_RULES",
        "supersedes": "research/decipherment/2026-10-23-prospective-leaf-holdout/manifest.json",
        "correction": "Include optional numeric panels after r/v in IVTFF folio headers",
        "salt": SALT,
        "unit": "physical_leaf_number; recto and verso and panels grouped",
        "allocation": {"train": 0.70, "development": 0.15, "test": 0.15},
        "selection": "shared leaves in both editions; panel-aware header IDs only",
        "caveat": "Not a historically untouched holdout; previously inspected leaves remain exposed.",
        "corpora": {
            name: {
                "path": f"data/transcriptions/{name}",
                "sha256": hashlib.sha256(source_bytes[name]).hexdigest(),
                "leaf_count": len(sources[name]),
            }
            for name in SOURCE_NAMES
        },
        "source_only_leaves": {
            name: sorted(sources[name] - shared) for name in SOURCE_NAMES
        },
        "eligible_count": len(shared),
        "partitions": groups,
        "counts": {name: len(values) for name, values in groups.items()},
        "forbidden": [
            "selecting rules on test folios",
            "tuning on test outcomes",
            "claiming a historically independent or semantic validation",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    raw = {name: (ROOT / "data/transcriptions" / name).read_bytes()
           for name in SOURCE_NAMES}
    output = json.dumps(build_manifest(raw), ensure_ascii=False, indent=2,
                        sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
