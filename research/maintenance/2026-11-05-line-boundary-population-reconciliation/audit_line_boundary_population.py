#!/usr/bin/env python3
"""Reconcile historical and corrected line-boundary token populations.

The baseline reader is copied from commit 76717eff613c3235526a3e9097a581149fca5e1b.
The corrected reader is imported from the neighboring analysis directory.
This is a deterministic count audit; it does not fit or score a predictor.
"""
from __future__ import annotations

import collections
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[2]
CORPUS = REPO_ROOT / "data/transcriptions/eva_zl3b.txt"
EXPECTED_CORPUS_SHA256 = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
EXPECTED_CURRENT_READER_SHA256 = "97e5cbc0f63cf3ca52fc555334e595d6f24d94a425e549c0c125d00f5d016059"
BASELINE_COMMIT = "76717eff613c3235526a3e9097a581149fca5e1b"
CURRENT_READER_COMMIT = "60d0bdb64931f1659c5f662a31d7471dbef5058f"

# Exact legacy tokenization and P-row selection from BASELINE_COMMIT.
ROW = re.compile(r"^<(?P<ident>[^>]+)>\s+(?P<body>.*)$")
UNCERTAIN = re.compile(r"\{[^}]*\}|\?")


def legacy_tokens(body: str, policy: str = "primary") -> list[str]:
    body = re.sub(r"<![^>]*>", " ", body)
    body = re.sub(r"<[^>]*>", " ", body)
    body = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", body)
    body = re.sub(r"\[([^\]]*)\]", r"\1", body)
    out: list[str] = []
    for item in re.split(r"[.\s,]+", body):
        if not item or (policy == "drop_uncertain_word" and UNCERTAIN.search(item)):
            continue
        item = re.sub(r"\{[^}]*\}", " ", item)
        item = re.sub(r"@\d+;?", " ", item)
        out.extend(word.lower() for word in re.findall(r"[A-Za-z]+", item))
    return out


def legacy_parse(path: Path) -> dict[str, list[dict[str, object]]]:
    pages: dict[str, list[dict[str, object]]] = collections.defaultdict(list)
    for lineno, raw in enumerate(path.read_text(encoding="latin-1").splitlines(), 1):
        match = ROW.match(raw.strip())
        if not match or "," not in match["ident"]:
            continue
        ident, locus = match["ident"].split(",", 1)
        parts = ident.split(".")
        if len(parts) < 2:
            continue
        page = parts[0]
        page_match = re.fullmatch(r"f(\d+)[rv][1-6]?", page)
        locus_code = re.sub(r"^[+*@=~&!/]+", "", locus.strip())
        if (not page_match and page != "fRos") or not re.fullmatch(r"P(?:0|1|b|c|r|t)", locus_code):
            continue
        words = legacy_tokens(match["body"])
        if words:
            pages[page].append({"words": words, "line": lineno})
    return dict(pages)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def token_count(pages: dict[str, list[dict[str, object]]]) -> int:
    return sum(
        sum(word is not None for word in row["words"])
        for rows in pages.values()
        for row in rows
    )


def line_count(pages: dict[str, list[dict[str, object]]]) -> int:
    return sum(len(rows) for rows in pages.values())


def load_current_reader():
    path = REPO_ROOT / "research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py"
    actual = digest(path)
    if actual != EXPECTED_CURRENT_READER_SHA256:
        raise SystemExit(f"current reader SHA-256 mismatch: {actual}")
    sys.path.insert(0, str(REPO_ROOT))
    spec = importlib.util.spec_from_file_location("line_boundary_replication", path)
    if spec is None or spec.loader is None:
        raise SystemExit("could not load the current line-boundary reader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, actual


def main() -> None:
    source_sha = digest(CORPUS)
    if source_sha != EXPECTED_CORPUS_SHA256:
        raise SystemExit(f"ZL3b SHA-256 mismatch: {source_sha}")
    current, current_sha = load_current_reader()
    baseline = legacy_parse(CORPUS)
    old_tokens = token_count(baseline)
    old_lines = line_count(baseline)
    matrix: dict[str, dict[str, int]] = {}
    for comma_policy in ("quarantine", "split"):
        for ligature_policy in ("quarantine", "expand_ascii"):
            pages = current.parse(
                CORPUS,
                "primary",
                uncertain_space_policy=comma_policy,
                ligature_policy=ligature_policy,
            )
            matrix[f"{comma_policy}+{ligature_policy}"] = {
                "lines": line_count(pages),
                "tokens": token_count(pages),
                "pages": len(pages),
            }
    if old_tokens != 35318 or old_lines != 4130:
        raise SystemExit(f"legacy baseline mismatch: tokens={old_tokens}, lines={old_lines}")
    if any(v["lines"] != 4130 or v["pages"] != 207 for v in matrix.values()):
        raise SystemExit("line/page population changed across reader sensitivity views")
    q = matrix["quarantine+quarantine"]["tokens"]
    q_expand = matrix["quarantine+expand_ascii"]["tokens"]
    split = matrix["split+quarantine"]["tokens"]
    split_expand = matrix["split+expand_ascii"]["tokens"]
    decomposition = {
        "total_legacy_minus_conservative": old_tokens - q,
        "comma_policy_effect_at_quarantined_ligatures": split - q,
        "ascii_ligature_effect_with_comma_quarantine": q_expand - q,
        "comma_ligature_interaction": (split_expand - split) - (q_expand - q),
        "residual_legacy_minus_split_ascii_expansion": old_tokens - split_expand,
    }
    if decomposition != {
        "total_legacy_minus_conservative": 5412,
        "comma_policy_effect_at_quarantined_ligatures": 4603,
        "ascii_ligature_effect_with_comma_quarantine": 252,
        "comma_ligature_interaction": 19,
        "residual_legacy_minus_split_ascii_expansion": 538,
    }:
        raise SystemExit(f"unexpected decomposition: {decomposition}")
    result = {
        "audit_type": "deterministic population reconciliation; no predictor fitting or scoring",
        "baseline_commit": BASELINE_COMMIT,
        "current_reader_commit": CURRENT_READER_COMMIT,
        "current_reader_sha256": current_sha,
        "corpus": {"path": "data/transcriptions/eva_zl3b.txt", "sha256": source_sha, "bytes": CORPUS.stat().st_size},
        "legacy": {"lines": old_lines, "pages": len(baseline), "tokens": old_tokens},
        "current_sensitivity_matrix": matrix,
        "decomposition": decomposition,
        "interpretation": "The 538-token residual is not assigned to individual IVTFF rule classes by this audit.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
