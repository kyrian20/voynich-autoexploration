#!/usr/bin/env python3
"""Descriptive, source-locked census of comma-policy population differences.

No model is fitted, no held-out labels or scores are inspected, and the
historical (pre-correction) predictor is NOT re-executed.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL_PATH = HERE / "line_boundary_replication.py"

spec = importlib.util.spec_from_file_location("line_boundary_replication_audit", MODEL_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load the current line-boundary reader")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)

# These numbers are published in REPORT.md for the *earlier* reader.
# They are references, NOT reconstructed historical outputs.
ARCHIVED_REPORTED_COUNTS = {"ZL3b": 35318, "IT2a": 34510}
EXPECTED = {
    "ZL3b": {
        "rows": 4130, "raw_comma_rows": 1700, "changed_rows": 1697,
        "quarantine": {"slots": 34092, "accepted": 29906, "barriers": 4186},
        "split": {"slots": 36555, "accepted": 34509, "barriers": 2046},
        "accepted_delta_split_minus_quarantine": 4603,
        "archived_minus_quarantine": 5412, "archived_minus_split": 809,
    },
    "IT2a": {
        "rows": 4118, "raw_comma_rows": 0, "changed_rows": 0,
        "quarantine": {"slots": 36035, "accepted": 34411, "barriers": 1624},
        "split": {"slots": 36035, "accepted": 34411, "barriers": 1624},
        "accepted_delta_split_minus_quarantine": 0,
        "archived_minus_quarantine": 99, "archived_minus_split": 99,
    },
}


def _rows(path: Path, policy: str) -> dict[tuple[str, int], list[str | None]]:
    # Reuse the *same* audited parser as the corrected predictor; no
    # independent regex approximation may silently change the population.
    pages = reader.parse(path, "primary", uncertain_space_policy=policy)
    return {(page, row["line"]): row["words"]
            for page, records in pages.items() for row in records}


def _count(words: list[list[str | None]]) -> dict[str, int]:
    slots = sum(len(row) for row in words)
    accepted = sum(sum(word is not None for word in row) for row in words)
    return {"slots": slots, "accepted": accepted, "barriers": slots - accepted}


def census(label: str, path: Path) -> dict:
    actual_hash = reader.sha(path)
    expected_hash = reader.EXPECTED_SHA256[label]
    if actual_hash != expected_hash:
        raise ValueError(f"{label}: source SHA-256 mismatch: {actual_hash}")

    quarantine = _rows(path, "quarantine")
    split = _rows(path, "split")
    if quarantine.keys() != split.keys():
        raise ValueError(f"{label}: comma policies disagree on admitted source rows")
    keys = sorted(quarantine)
    q_counts = _count([quarantine[k] for k in keys])
    s_counts = _count([split[k] for k in keys])
    delta = s_counts["accepted"] - q_counts["accepted"]
    changed = sum(
        sum(w is not None for w in split[k])
        != sum(w is not None for w in quarantine[k]) for k in keys
    )
    # Count source rows with a literal comma, including those where it is
    # inside an annotation; only changed_rows measures actual policy impact.
    physical = dict(reader.checked_physical_lines(path.read_text(encoding="latin-1")))
    raw_comma_rows = 0
    for _, line in keys:
        match = reader.ROW.match(physical[line].strip())
        if match is None:
            raise ValueError(f"{label}: source row {line} is no longer a locus")
        raw_comma_rows += "," in (match["body"] or "")
    archived = ARCHIVED_REPORTED_COUNTS[label]
    return {
        "source_sha256": actual_hash,
        "rows": len(keys),
        "raw_comma_rows": raw_comma_rows,
        "changed_rows": changed,
        "quarantine": q_counts,
        "split": s_counts,
        "accepted_delta_split_minus_quarantine": delta,
        "archived_reported_not_reproduced": archived,
        "archived_minus_quarantine": archived - q_counts["accepted"],
        "archived_minus_split": archived - s_counts["accepted"],
    }


def compute() -> dict:
    result = {
        "audit": "line_boundary_comma_population_sensitivity",
        "status": "DESCRIPTIVE_NOT_HISTORICAL_REPLAY",
        "random_seed": None,
        "reads_heldout_labels_or_predictor_scores": False,
        "limitations": [
            "The split view is a counterfactual of the CURRENT reader, not the old reader.",
            "The archived counts are quoted from REPORT.md, not regenerated.",
            "A numerical difference of 809/99 is not an identified historical cause.",
            "This does not validate IVTFF semantics, scientific predictions, or translation.",
        ],
        "sources": {},
    }
    for label, path in reader.INPUTS.items():
        result["sources"][label] = census(label, path)
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="Reject changes to the frozen descriptive census")
    args = ap.parse_args()
    result = compute()
    if args.check:
        for label, expected in EXPECTED.items():
            observed = result["sources"][label]
            for key, value in expected.items():
                if observed[key] != value:
                    raise SystemExit(
                        f"{label}.{key}: expected {value!r}, got {observed[key]!r}"
                    )
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
