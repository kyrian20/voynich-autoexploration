#!/usr/bin/env python3
"""Classify LIB-EXP-624 Library JSON against the archived script's output contract.

Read-only. This does not execute the model or assert historical reproducibility.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
from pathlib import Path

EXPECTED_SHA256 = {
    "script": "1f00846ab8e91cefd07bc2dcd26ad12cf8a7c4bc7b2478d480afec391a13f3a9",
    "results": "d6e1b7490e563c96367ff10ab56feb5487d6b2775a885494f249c89f87bd4bab",
    "report": "7de18cce59ea21598af7958a7ded3e05b03e305e8a6cc84c0740917b807447c4",
}
EXPECTED_SUMMARY_KEYS = {"experiment", "date", "source_data", "method", "ZL3b", "IT2a", "interpretation"}


def strict_json(data: bytes) -> dict:
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError(f"Non-finite JSON constant: {value}")

    obj = json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                     parse_constant=reject_constant)
    if not isinstance(obj, dict):
        raise ValueError("JSON root must be an object")
    return obj


def native_root_keys(script: str) -> set[str]:
    """Read the literal output schema in main(), without importing/executing code."""
    tree = ast.parse(script)
    main = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                 and n.name == "main"), None)
    if main is None:
        raise ValueError("Historical script lacks main()")
    roots = [value for node in main.body if isinstance(node, ast.Assign)
             for target in node.targets if isinstance(target, ast.Name)
             and target.id == "results" for value in [node.value]]
    if len(roots) != 1 or not isinstance(roots[0], ast.Dict):
        raise ValueError("Cannot prove native output schema from main()")
    keys = set()
    for key in roots[0].keys:
        if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
            raise ValueError("Dynamic native output key")
        keys.add(key.value)
    if len(keys) != len(roots[0].keys) or "datasets" not in keys:
        raise ValueError("Unexpected native output contract")
    return keys


def validate_summary(summary: dict) -> dict:
    if set(summary) != EXPECTED_SUMMARY_KEYS:
        raise ValueError("Unexpected curated-summary top-level keys")
    if summary["experiment"] != "exp624_position_conditioned_character_model":
        raise ValueError("Wrong experiment")
    counts = {}
    for edition in ("ZL3b", "IT2a"):
        section = summary[edition]
        if section["parsed_folios_with_body"] != 203:
            raise ValueError(f"{edition}: unexpected eligible page count")
        groups = [("all", row) for row in section["results"]]
        if len(section["results"]) != 2:
            raise ValueError(f"{edition}: expected two overall tokenizers")
        if edition == "ZL3b":
            strata = section["currier_strata"]
            if len(strata) != 4 or sorted((x["currier"], x["tokenizer"]) for x in strata) != [
                ("A", "glyph"), ("A", "raw"), ("B", "glyph"), ("B", "raw")
            ]:
                raise ValueError("Wrong Currier strata")
            groups += [(row["currier"], row) for row in strata]
        for label, row in groups:
            expected_splits = 8 if label == "all" else 6
            deltas = row["split_deltas"]
            if (not isinstance(deltas, list) or len(deltas) != expected_splits
                    or row["splits_total"] != expected_splits):
                raise ValueError(f"{edition}/{label}: split count drift")
            if any(isinstance(x, bool) or not isinstance(x, (float, int))
                   or not math.isfinite(x) for x in deltas):
                raise ValueError(f"{edition}/{label}: invalid split delta")
            mean_delta = row["mean_null_minus_real_bits_per_unit"]
            if abs(sum(deltas) / len(deltas) - mean_delta) > 1.1e-6:
                raise ValueError(f"{edition}/{label}: delta mean inconsistent")
            if abs(row["mean_null_holdout_bits_per_unit"] -
                   row["mean_real_holdout_bits_per_unit"] - mean_delta) > 1e-6:
                raise ValueError(f"{edition}/{label}: means inconsistent")
            if abs(min(deltas) - row["split_delta_min"]) > 1.1e-6 or abs(max(deltas) - row["split_delta_max"]) > 1.1e-6:
                raise ValueError(f"{edition}/{label}: extrema inconsistent")
        counts[edition] = {"overall_rows": 2, "stratum_rows": len(groups) - 2,
                           "split_deltas_checked": sum(len(row["split_deltas"]) for _, row in groups)}
    return counts


def audit(script: bytes, results: bytes, report: bytes, expected_hashes: dict = EXPECTED_SHA256) -> dict:
    inputs = {"script": script, "results": results, "report": report}
    digests = {name: hashlib.sha256(raw).hexdigest() for name, raw in inputs.items()}
    for name, digest in digests.items():
        if digest != expected_hashes[name]:
            raise ValueError(f"{name}: SHA-256 mismatch: {digest}")
    native = native_root_keys(script.decode("utf-8"))
    summary = strict_json(results)
    if set(summary) == native:
        raise ValueError("This input is native output, not the pinned Library curated summary")
    counts = validate_summary(summary)
    return {"status": "ARCHIVED_CURATED_SUMMARY_NOT_NATIVE_SCRIPT_OUTPUT",
            "historical_reproduction": False, "model_executed": False,
            "sha256": digests, "native_root_keys": sorted(native),
            "archive_root_keys": sorted(summary), "checked_rows": counts,
            "limitations": ["Schema difference does not prove numeric fabrication or error.",
                            "No raw per-seed native output or run receipt authenticated.",
                            "Original files preserved; physical-leaf leakage remains separately adjudicated."]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--script", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    evidence = audit(args.script.read_bytes(), args.results.read_bytes(), args.report.read_bytes())
    print(json.dumps(evidence, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
