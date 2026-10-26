#!/usr/bin/env python3
"""Independent *coverage* audit of the frozen prospective physical-leaf holdout.

Do not treat named/non-numeric loci as test leaves. No tokens are decoded, no
scientific hypothesis is evaluated, and no historical manifest is rewritten.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json"
SOURCE_NAMES = ("eva_zl3b.txt", "eva_it2a.txt")
# Historical split identity is frozen independently of the manifest and its
# generator: an internally consistent but reassigned manifest must fail.
FROZEN_SALT = "VOYNICH-FUTURE-RULES-2026-10-23-v1"
# Independent IVTFF-shaped tag checks: do not count a prefix match as a
# complete header or locus. This is a coverage audit, not full IVTFF parsing.
PAGE_ID = re.compile(r"^f(?:[0-9]+[rv][1-6]?|Ros)$")
RECORD_ID = re.compile(
    r"^(f(?:[0-9]+[rv][1-6]?|Ros))\.[0-9]{1,3},[^;>]{3}(?:;[^;>])?$"
)


def inspect_source(raw: bytes) -> dict:
    leaves: set[int] = set()
    named_headers: Counter[str] = Counter()
    named_loci: Counter[str] = Counter()
    numeric_tags = numeric_headers = numeric_loci = 0
    active_page = None
    for line_no, line in enumerate(raw.decode("utf-8-sig").splitlines(), 1):
        if not line.startswith("<f"):
            continue
        end = line.find(">")
        if end < 0 or (end + 1 < len(line) and line[end + 1] not in " \t"):
            raise ValueError(f"Malformed folio tag boundary at source line {line_no}")
        tag = line[1:end]
        is_header = PAGE_ID.fullmatch(tag) is not None
        locus = RECORD_ID.fullmatch(tag)
        if not is_header and locus is None:
            kind = "numeric" if len(line) > 2 and line[2].isdigit() else "named"
            raise ValueError(f"Unparsed {kind} folio header at source line {line_no}")
        page = tag if is_header else locus.group(1)
        if is_header:
            active_page = page
        elif page != active_page:
            raise ValueError(f"Orphan or mismatched locus at source line {line_no}")
        if page == "fRos":
            if is_header:
                named_headers["Ros"] += 1
            else:
                named_loci["Ros"] += 1
            continue
        leaf = int(re.match(r"^f([0-9]+)", page).group(1))
        if leaf <= 0:
            raise ValueError(f"Nonpositive physical leaf at source line {line_no}")
        numeric_tags += 1
        if is_header:
            numeric_headers += 1
        else:
            numeric_loci += 1
        leaves.add(leaf)
    if not leaves:
        raise ValueError("No numeric physical leaves found")
    return {
        "numeric_tag_count": numeric_tags,
        "numeric_page_header_count": numeric_headers,
        "numeric_locus_record_count": numeric_loci,
        "numeric_leaves": sorted(leaves),
        "named_tag_count": sum(named_headers.values()) + sum(named_loci.values()),
        "named_page_headers": dict(sorted(named_headers.items())),
        "named_page_header_count": sum(named_headers.values()),
        "named_locus_records": dict(sorted(named_loci.items())),
        "named_locus_record_count": sum(named_loci.values()),
    }


def locked_partition(leaf: int) -> str:
    """Independently replay the committed SHA-256 physical-leaf allocation."""
    digest = hashlib.sha256(f"{FROZEN_SALT}:{leaf}".encode("utf-8")).digest()
    value = int.from_bytes(digest[:8], "big") % 10000
    return "train" if value < 7000 else ("development" if value < 8500 else "test")


def audit(source_bytes: dict[str, bytes], manifest: dict) -> dict:
    if manifest.get("schema_version") != 2:
        raise ValueError("Requires frozen v2 holdout manifest")
    if manifest.get("salt") != FROZEN_SALT:
        raise ValueError("Frozen partition salt mismatch")
    if set(source_bytes) != set(SOURCE_NAMES) or set(manifest["corpora"]) != set(SOURCE_NAMES):
        raise ValueError("Unexpected or missing source edition")
    coverage = {}
    for name in SOURCE_NAMES:
        record = inspect_source(source_bytes[name])
        expected = manifest["corpora"][name]
        sha = hashlib.sha256(source_bytes[name]).hexdigest()
        if expected["path"] != f"data/transcriptions/{name}" or expected["sha256"] != sha:
            raise ValueError(f"Source provenance mismatch for {name}")
        if expected["leaf_count"] != len(record["numeric_leaves"]):
            raise ValueError(f"Leaf count mismatch for {name}")
        coverage[name] = {"sha256": sha, **record}

    shared = set(coverage[SOURCE_NAMES[0]]["numeric_leaves"]) & set(coverage[SOURCE_NAMES[1]]["numeric_leaves"])
    groups = manifest["partitions"]
    if set(groups) != {"train", "development", "test"}:
        raise ValueError("Partition names differ")
    assigned = []
    for group in ("train", "development", "test"):
        values = groups[group]
        if any(type(n) is not int or n <= 0 for n in values) or len(values) != len(set(values)):
            raise ValueError(f"Invalid or duplicated leaves in {group}")
        if manifest["counts"][group] != len(values):
            raise ValueError(f"Count mismatch in {group}")
        assigned.extend(values)
    if len(assigned) != len(set(assigned)) or set(assigned) != shared:
        raise ValueError("Assigned leaves differ from the intersection of source numeric leaves")
    # Counts, uniqueness and coverage alone cannot detect a same-size swap
    # between train and test. Recompute each assignment from the frozen salt.
    for group in ("train", "development", "test"):
        if groups[group] != sorted(groups[group]):
            raise ValueError(f"Unsorted frozen partition: {group}")
        for leaf in groups[group]:
            if locked_partition(leaf) != group:
                raise ValueError(f"Partition hash assignment mismatch: leaf {leaf} in {group}")
    if manifest["eligible_count"] != len(shared):
        raise ValueError("Eligible count mismatch")
    for name in SOURCE_NAMES:
        expected_only = sorted(set(coverage[name]["numeric_leaves"]) - shared)
        if manifest["source_only_leaves"][name] != expected_only:
            raise ValueError(f"Source-only leaves mismatch for {name}")

    return {
        "status": "COVERAGE_VERIFIED_NOT_IVTFF_OR_SEMANTIC_VALIDATION",
        "manifest": "research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json",
        "eligible_numeric_physical_leaves": len(shared),
        "partitions": {key: len(groups[key]) for key in ("train", "development", "test")},
        "source_coverage": coverage,
        "named_loci_holdout_status": "EXCLUDED_UNASSIGNED_NOT_VALID_TEST_FOLIOS",
        "limitations": [
            "Named folios (e.g. Ros) cannot be mapped to a physical-leaf split by this manifest.",
            "Numeric folio recognition is a header coverage check, not full IVTFF conformity.",
            "A future model must explicitly reject named/unassigned loci from confirmatory evaluation.",
            "The numeric test leaves were previously inspected historically; this is not a blind semantic validation.",
            "The source transcriptions are two editions of the same manuscript, not independent replications.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sources = {name: (ROOT / "data/transcriptions" / name).read_bytes() for name in SOURCE_NAMES}
    result = audit(sources, manifest)
    output = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "eligible_numeric_physical_leaves": result["eligible_numeric_physical_leaves"],
        "named_locus_records": {k: v["named_locus_records"] for k, v in result["source_coverage"].items()},
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
