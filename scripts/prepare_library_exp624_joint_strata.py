#!/usr/bin/env python3
"""Derive cross-stratum-safe allocation from LIB-EXP-624 global leaf splits.

Allocation-only maintenance: not a historical rerun, scientific holdout,
model fit, semantic hypothesis test, or replacement for frozen A/B splits.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from scripts import prepare_library_exp624_leaf_grouped_splits as grouped
except ModuleNotFoundError:
    import prepare_library_exp624_leaf_grouped_splits as grouped

ROOT = Path(__file__).resolve().parents[1]
STRATA = ("A", "B", "unclassified")


def derive_joint_strata(pages: list[dict], global_rows: list[dict]) -> list[dict]:
    """Filter ONE global leaf partition by metadata, never split A/B separately."""
    by_id = {page["id"]: page for page in pages}
    if len(by_id) != len(pages):
        raise ValueError("Duplicate eligible page identifiers")
    physical_ids = [grouped.physical_page_id(page["id"]) for page in pages]
    if len(set(physical_ids)) != len(physical_ids):
        raise ValueError("Duplicate physical page identity in joint allocation")
    result = []
    for row in global_rows:
        train_ids, test_ids = row["train_page_ids"], row["test_page_ids"]
        if (len(set(train_ids)) != len(train_ids) or
                len(set(test_ids)) != len(test_ids) or
                set(train_ids) & set(test_ids) or
                set(train_ids) | set(test_ids) != set(by_id)):
            raise ValueError("Global allocation does not partition eligible pages")
        train_leaves = {grouped.leaf_id(p) for p in train_ids}
        test_leaves = {grouped.leaf_id(p) for p in test_ids}
        if train_leaves & test_leaves:
            raise ValueError("Cross-stratum physical-leaf leakage in global allocation")
        if train_leaves != set(row["train_leaves"]) or test_leaves != set(row["test_leaves"]):
            raise ValueError("Global leaf identities disagree with page allocation")
        # A disjoint partition is not proof that its claimed RNG seed generated it.
        # Validate the complete page assignment against the frozen LCG/Fisher-Yates
        # policy; this API also accepts externally supplied global_rows.
        if type(row.get("seed")) is not int:
            raise ValueError("Global allocation seed must be an integer")
        expected = grouped.grouped_splits(pages, row["seed"], 1)[0]
        if (set(train_ids) != set(expected["train_page_ids"]) or
                set(test_ids) != set(expected["test_page_ids"])):
            raise ValueError("Global allocation does not match deterministic seed")
        strata = {}
        for name in STRATA:
            def in_stratum(page_id: str) -> bool:
                language = by_id[page_id]["lang"]
                return (language == name if name != "unclassified"
                        else language not in ("A", "B"))
            train = [p for p in train_ids if in_stratum(p)]
            test = [p for p in test_ids if in_stratum(p)]
            strata[name] = {
                "train_page_ids": train, "test_page_ids": test,
                "train_page_count": len(train), "test_page_count": len(test),
                "train_leaves": sorted({grouped.leaf_id(p) for p in train}),
                "test_leaves": sorted({grouped.leaf_id(p) for p in test}),
            }
        if sum(v["train_page_count"] + v["test_page_count"] for v in strata.values()) != len(pages):
            raise ValueError("Incomplete stratified allocation")
        result.append({
            "seed": row["seed"], "train_leaves": sorted(train_leaves),
            "test_leaves": sorted(test_leaves), "strata": strata,
            "cross_stratum_shared_train_test_leaves": [],
        })
    return result


def build(raw_sources: dict[str, bytes]) -> dict:
    base = grouped.build(raw_sources)  # SHA-256, eligibility and edition gates
    pages = grouped.historical.parse_pages(raw_sources["ZL3b"])
    global_rows = base["results"]["ZL3b"]["groups"]["all"]
    joint = derive_joint_strata(pages, global_rows)
    if len(joint) != 8:
        raise ValueError("Expected eight global seed allocations")
    for row in joint:
        counts = {name: (part["train_page_count"] + part["test_page_count"])
                  for name, part in row["strata"].items()}
        if counts != {"A": 114, "B": 81, "unclassified": 8}:
            raise ValueError(f"Frozen stratum counts drift: {counts}")
    return {
        "status": "ALLOCATION_ONLY_BLOCKED_FOR_SCIENTIFIC_SCORING",
        "purpose": "Safe combined A/B/unclassified views of one global leaf split",
        "source_sha256": {name: base["results"][name]["sha256"]
                          for name in ("ZL3b", "IT2a")},
        "historical_artifact_sha256": {
            "script": grouped.historical.LIBRARY_EVIDENCE["script_sha256"],
            "results": grouped.historical.LIBRARY_EVIDENCE["results_sha256"],
            "report": grouped.historical.LIBRARY_EVIDENCE["report_sha256"],
        },
        "seed_base": 624010, "seed_step": 7919, "repetitions": 8,
        "policy": "One 70/30 split by physical leaf, then filter A/B/unclassified; no independent A/B shuffles",
        "historical_model_executed": False, "metrics_rehabilitated": False,
        "caveats": [
            "Independent historical A/B split series remain unsafe for combined cross-stratum use.",
            "Source selection reuses permissive historical tokenization, not fully adjudicated IVTFF.",
            "The pages have been inspected; this is not a prospective blind holdout.",
            "ZL3b and IT2a are two editions of the same manuscript, not independent samples.",
            "No predictive score, natural-language control, or decipherment is claimed.",
        ],
        "joint_allocations": joint,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Exclusive-create JSON evidence")
    args = parser.parse_args()
    sources = {name: (ROOT / "data/transcriptions" / filename).read_bytes()
               for name, (filename, _) in grouped.historical.SOURCES.items()}
    report = build(sources)
    serialized = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.out:
        with args.out.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized)
    else:
        print(serialized, end="")


if __name__ == "__main__":
    main()
