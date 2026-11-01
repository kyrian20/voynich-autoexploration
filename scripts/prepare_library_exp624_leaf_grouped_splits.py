#!/usr/bin/env python3
"""Allocation-only repair for LIB-EXP-624's page-side leakage.

NOT a historical reproduction: the original Library script/results are frozen.
No model is fitted or scored; this is NOT a fresh independent holdout.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

try:
    from scripts import audit_library_exp624_leaf_leakage as historical
except ModuleNotFoundError:
    import audit_library_exp624_leaf_leakage as historical

ROOT = Path(__file__).resolve().parents[1]
STRICT_PAGE = re.compile(r"f([0-9]+)([rv])([1-6])?", re.IGNORECASE)


def physical_page_id(page_id: str) -> tuple[int, str, int | None]:
    """Canonical physical page identity; raw IVTFF page IDs remain unchanged."""
    match = STRICT_PAGE.fullmatch(page_id)
    if not match:
        raise ValueError(f"Unrecognized physical page identifier: {page_id!r}")
    panel = int(match.group(3)) if match.group(3) is not None else None
    return int(match.group(1)), match.group(2).lower(), panel


def leaf_id(page_id: str) -> int:
    return physical_page_id(page_id)[0]


def grouped_splits(pages: list[dict], seed_base: int, repetitions: int) -> list[dict]:
    """Shuffle physical leaves, not page sides, with historical LCG seeds.

    The 70/30 cut is by *leaf count*, not by page count: this is a NEW
    allocation policy, not equivalent to the archived page-side split.
    """
    if type(seed_base) is not int:
        raise ValueError("seed_base must be an integer")
    if type(repetitions) is not int:
        raise ValueError("repetitions must be an integer")
    if repetitions < 1:
        raise ValueError("At least one repetition required")
    # The archived LCG masks its state to 32 bits. Do not issue distinct
    # receipts for modulo-aliased seeds or for a series that wraps.
    if not 0 <= seed_base < 2**32:
        raise ValueError("seed_base outside unsigned 32-bit range")
    if seed_base + 7919 * (repetitions - 1) >= 2**32:
        raise ValueError("seed series exceeds unsigned 32-bit range")
    groups: dict[int, list[str]] = {}
    seen: set[str] = set()
    seen_physical: set[tuple[int, str, int | None]] = set()
    for page in pages:
        page_id = page["id"]
        if page_id in seen:
            raise ValueError(f"Duplicate eligible page ID: {page_id}")
        physical = physical_page_id(page_id)
        if physical in seen_physical:
            raise ValueError(f"Duplicate physical page identity: {page_id}")
        seen.add(page_id)
        seen_physical.add(physical)
        groups.setdefault(physical[0], []).append(page_id)
    leaves = sorted(groups)
    if len(leaves) < 2:
        raise ValueError("At least two distinct physical leaves required")
    cut = int(len(leaves) * 0.7)
    if not 0 < cut < len(leaves):
        raise ValueError("Empty training or test leaf set")
    rows = []
    for i in range(repetitions):
        seed = seed_base + 7919 * i
        order = historical.shuffled(leaves, historical.LCG(seed))
        train, test = sorted(order[:cut]), sorted(order[cut:])
        if set(train) & set(test):
            raise AssertionError("Physical-leaf leakage")
        train_pages = sorted(p for leaf in train for p in groups[leaf])
        test_pages = sorted(p for leaf in test for p in groups[leaf])
        if len(train_pages) + len(test_pages) != len(seen):
            raise AssertionError("Missing or duplicated page allocation")
        rows.append({"seed": seed, "train_leaves": train, "test_leaves": test,
                     "train_page_ids": train_pages, "test_page_ids": test_pages,
                     "train_page_count": len(train_pages), "test_page_count": len(test_pages)})
    return rows


def build(raw_sources: dict[str, bytes]) -> dict:
    if set(raw_sources) != set(historical.SOURCES):
        raise ValueError("Both named frozen transcriptions required")
    results = {}
    page_languages: dict[str, dict[str, str | None]] = {}
    for label, (filename, expected_hash) in historical.SOURCES.items():
        raw = raw_sources[label]
        digest = hashlib.sha256(raw).hexdigest()
        if digest != expected_hash:
            raise ValueError(f"{label}: frozen corpus SHA-256 mismatch: {digest}")
        pages = historical.parse_pages(raw)
        page_languages[label] = {page["id"]: page["lang"] for page in pages}
        if len(pages) != 203:
            raise ValueError(f"{label}: eligible page count drift: {len(pages)}")
        if {k: sum(p["lang"] == k for p in pages) for k in ("A", "B")} != {"A": 114, "B": 81}:
            raise ValueError(f"{label}: Currier page counts drift")
        groups = {"all": grouped_splits(pages, 624010, 8)}
        if label == "ZL3b":
            for lang in ("A", "B"):
                groups[lang] = grouped_splits([p for p in pages if p["lang"] == lang], 625010, 6)
        results[label] = {"path": f"data/transcriptions/{filename}", "sha256": digest,
                          "eligible_page_ids": sorted(p["id"] for p in pages), "groups": groups}
    # Both editions of the same manuscript must share the all-corpus allocation.
    zl = results["ZL3b"]["groups"]["all"]
    it = results["IT2a"]["groups"]["all"]
    if results["ZL3b"]["eligible_page_ids"] != results["IT2a"]["eligible_page_ids"]:
        raise ValueError("Different eligible page IDs between editions")
    # Equal A/B totals do not prove equal page-level Currier assignments.
    # Joint A/B strata are defined on ZL3b; reject an edition disagreement.
    if page_languages["ZL3b"] != page_languages["IT2a"]:
        raise ValueError("Different per-page Currier $L metadata between editions")
    for left, right in zip(zl, it, strict=True):
        if (left["train_leaves"], left["test_leaves"]) != (right["train_leaves"], right["test_leaves"]):
            raise ValueError("Edition-specific physical-leaf allocation drift")
    return {
        "status": "BLOCKED_FOR_SCIENTIFIC_SCORING",
        "purpose": "Corrected grouped allocation only; NOT a rerun of Library EXP-624",
        "historical_script_sha256": historical.LIBRARY_EVIDENCE["script_sha256"],
        "historical_results_sha256": historical.LIBRARY_EVIDENCE["results_sha256"],
        "historical_report_sha256": historical.LIBRARY_EVIDENCE["report_sha256"],
        "model_executed": False, "metrics_rehabilitated": False,
        "policy": "70/30 by physical leaf count; recto/verso/panels grouped; 32-bit LCG Fisher-Yates; historical seed series reused for comparison only",
        "caveats": ["Historical page-side split remains invalid for physical-leaf holdout claims.",
                    "Eligibility mirrors the permissive historical tokenizer, not an adjudicated IVTFF reader.",
                    "Two editions of one manuscript are not independent evidence.",
                    "These leaves have already been inspected; not a fresh prospective blind holdout.",
                    "No model, reference controls, predictive scores, or significance tests run."],
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Exclusive-create JSON allocation evidence")
    args = parser.parse_args()
    sources = {label: (ROOT / "data/transcriptions" / filename).read_bytes()
               for label, (filename, _) in historical.SOURCES.items()}
    result = build(sources)
    serialized = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        with args.out.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized)
    else:
        print(serialized, end="")


if __name__ == "__main__":
    main()
