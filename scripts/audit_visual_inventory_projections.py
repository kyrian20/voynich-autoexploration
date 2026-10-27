#!/usr/bin/env python3
"""Replay every archived L/R inventory projection from source-bound raw payloads.

Maintenance only: the archived inventory, corpus, manifest and original
tokenizers are immutable. Replaying a policy is NOT independent IVTFF
conformance or a semantic evaluation on held-out leaves.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_visual_inventory_completeness import audit as audit_completeness
from scripts.ivtff_lossless import lex
from scripts.ivtff_rows import tokens_rows
from scripts.select_visual_pilot_v2 import load_unique_inventory, load_verified_frozen_manifest

INVENTORY = Path("research/decipherment/2026-10-25-label-inventory/inventory.json.gz")
MANIFEST = Path("research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json")
POLICIES = tuple(product(
    ("split", "join"), ("primary", "exclude_word"), ("expand", "opaque")
))


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def replay(inventory: dict, manifest: dict, root: Path) -> dict:
    """Fail closed on changed stored views, diagnostics or semantic eligibility.

    The precondition audits bind every selected row to original source bytes
    and independently census all L/R physical rows. This routine checks the
    DERIVED fields that those two audits deliberately do not inspect.
    """
    completeness = audit_completeness(inventory, manifest, root)
    counts = Counter()
    expected_keys = {
        f"{space}/{alternative}/{ligature}"
        for space, alternative, ligature in POLICIES
    }
    for row in inventory["records"]:
        key = row["occurrence_id"]
        if (row.get("eligible_for_semantic_evaluation") is not False
                or row.get("visual_category") is not None
                or row.get("external_referent") is not None
                or row.get("independent_annotation_source") is not None
                or "no_independent_visual_referent_annotation"
                not in row.get("exclusion_reasons", [])):
            raise ValueError(f"Unreviewed inventory row promoted to semantic evidence: {key}")

        payload = lex(row["raw_body"])
        if row.get("lexer_diagnostics") != payload.diagnostics:
            raise ValueError(f"Archived lexer diagnostics differ from replay: {key}")
        views = row.get("views")
        if not isinstance(views, dict) or set(views) != expected_keys:
            raise ValueError(f"Archived projection policy set differs from replay: {key}")
        for space, alternative, ligature in POLICIES:
            policy = f"{space}/{alternative}/{ligature}"
            try:
                projected = tokens_rows(
                    [payload], uncertain_space=space,
                    alternatives=alternative, ligatures=ligature
                )
                expected = {"tokens": projected, "error": None}
            except ValueError as exc:
                expected = {"tokens": None, "error": str(exc)}
            if views[policy] != expected:
                raise ValueError(f"Archived projection differs from replay: {key}: {policy}")
            counts["views_checked"] += 1
            if expected["error"] is not None:
                counts["views_with_errors"] += 1
        counts["rows_checked"] += 1
        if payload.diagnostics:
            counts["rows_with_lexer_diagnostics"] += 1

    if counts["rows_checked"] != completeness["selected_total"]:
        raise ValueError("Projection replay count differs from physical L/R census")
    return {
        "status": "ARCHIVED_PROJECTIONS_REPLAYED_NOT_IVTFF_OR_SEMANTIC_VALIDATION",
        "rows_checked": counts["rows_checked"],
        "views_checked": counts["views_checked"],
        "views_with_errors": counts["views_with_errors"],
        "rows_with_lexer_diagnostics": counts["rows_with_lexer_diagnostics"],
        "source_sha256": completeness["source_sha256"],
        "policy_names": sorted(expected_keys),
        "limitations": [
            "Uses the same lexer and row projector as the original builder: agreement is reproducibility, not independent IVTFF conformance.",
            "The source-row binding and physical-line L/R census are checked first; the original archive is never modified.",
            "Existing derived views are inspected solely for byte/field integrity, not fitted or scored against meanings.",
            "No semantic annotation, image alignment, historically blind holdout, language identification or translation is established."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--inventory", type=Path, default=INVENTORY)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    inventory_bytes = (root / args.inventory).read_bytes()
    manifest_bytes = (root / args.manifest).read_bytes()
    inventory = load_unique_inventory(inventory_bytes)
    manifest = load_verified_frozen_manifest(manifest_bytes, root)
    result = replay(inventory, manifest, root)
    result["input_sha256"] = {
        "inventory_gzip": sha256(inventory_bytes),
        "manifest": sha256(manifest_bytes),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in (
        "status", "rows_checked", "views_checked", "views_with_errors"
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
