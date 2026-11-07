#!/usr/bin/env python3
"""Run the isolated Zhang–Sheng v2 filter sensitivity on frozen audit inputs.

From the repository root:
  python research/maintenance/2026-11-01-zs-wordpair-audit/run_v2_sensitivity.py

The historical audit source and results.json remain unchanged.
"""
from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in (HERE, *HERE.parents)
            if (parent / "data/transcriptions/eva_zl3b.txt").exists())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

import near_copy_v2
import wordpair_audit as audit

historical_metric = audit.metric


def v2_metric(*args, **kwargs):
    result = historical_metric(*args, **kwargs)
    result["implementation_choices"]["near_copy_exclusion"] = (
        "literal v2: exclude iff deleting exactly one EVA glyph from each "
        "distinct word type yields equality"
    )
    return result


def main() -> None:
    audit.levenshtein_at_most_one = near_copy_v2.equal_after_one_deletion_each
    audit.metric = v2_metric
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        audit.main()
    payload = json.loads(buffer.getvalue())
    payload["method_change"] = (
        "Only the near-copy predicate changed: literal v2 equal-after-one-deletion "
        "per word, using the isolated near_copy_v2.py function."
    )
    payload["run_design"] = {
        "pages_common": 225,
        "record_categories": ["P", "C", "R"],
        "excluded_pages": ["f116v", "fRos"],
        "uncertain_space_views": ["split", "join"],
        "additional_view": "legacy_ascii",
        "top_k": [150, 300, 600],
        "seeds": [20261101, 20261102, 20261103],
        "shuffles_per_seed": 20,
        "split": "alternating source-order blocks of 10 pages; physical leaves overlap",
        "other_metric_choices": (
            "same explicit additive OLS residualization and randomization "
            "implementation as the 2026-11-01 partial audit"
        ),
    }
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
