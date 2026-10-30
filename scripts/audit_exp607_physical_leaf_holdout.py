#!/usr/bin/env python3
"""Read-only, hash-gated audit of physical-leaf leakage in historical EXP-607.

Reconstruct only eligibility and the frozen page-side allocation. No model is
trained, no test token is scored, and no historical artifact is overwritten.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_SCRIPT = "experiments/exp_607_heldout_bigram_prediction/script.py"
HISTORICAL_RESULTS = "experiments/exp_607_heldout_bigram_prediction/results.json"
SCRIPT_SHA256 = "a991bf0b3a3b209a542b071da1b800d23eeb662990482413b57089ad848cbc97"
RESULTS_SHA256 = "d6aa4cb01c066cf3a25bc8c07ce90840a0dde3084bb4178696c94a1ce96b5218"
CORPORA = {
    "ZL3b": {
        "path": "data/transcriptions/eva_zl3b.txt",
        "sha256": "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
        "train_folios": 152, "test_folios": 32,
        "train_lines": 3139, "test_lines": 600,
        "shared_physical_leaves": [5, 6, 8, 10, 13, 14, 18, 21, 25, 30, 33, 34, 41, 42,
                                   43, 44, 50, 51, 55, 57, 58, 73, 78, 100, 101, 111, 114, 116],
    },
    "IT2a": {
        "path": "data/transcriptions/eva_it2a.txt",
        "sha256": "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
        "train_folios": 151, "test_folios": 32,
        "train_lines": 3138, "test_lines": 597,
        "shared_physical_leaves": [5, 6, 8, 10, 13, 14, 18, 21, 25, 30, 33, 34, 41, 42,
                                   43, 44, 50, 51, 55, 57, 58, 73, 78, 100, 101, 111, 114],
    },
}
ROW_RE = re.compile(r"^<(f\d+[rv])\.\d+,[^>]*>\s*(.*)$")
TOKEN_RE = re.compile(r"[a-z]{2,}")
LEAF_RE = re.compile(r"f([0-9]+)[rv]\Z")


def verify_bytes(path: Path, expected: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing or symlinked frozen source: {path}")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f"Frozen SHA-256 mismatch: {path}")
    return raw


def eligible_pages(raw: bytes) -> dict[str, int]:
    """Mirror historical Latin-1/regex eligibility, not a corrected IVTFF reader."""
    pages: dict[str, int] = {}
    for line in raw.decode("latin-1").splitlines():
        match = ROW_RE.match(line.strip())
        if not match:
            continue
        folio, body = match.groups()
        body = re.sub(r"<[^>]*>|\{[^}]*\}|\[[^]]*\]|\$[^ ]*|@\d+;?", " ", body)
        if len(TOKEN_RE.findall(body.lower())) >= 2:
            pages[folio] = pages.get(folio, 0) + 1
    return pages


def leaf(folio: str) -> int:
    match = LEAF_RE.fullmatch(folio)
    if not match:
        raise ValueError(f"Invalid historical page-side identifier: {folio}")
    return int(match.group(1))


def allocation(pages: dict[str, int]) -> dict:
    train, test = [], []
    for folio in sorted(pages):
        bucket = int(hashlib.sha256(folio.encode("ascii")).hexdigest()[:8], 16) % 5
        (test if bucket == 0 else train).append(folio)
    train_leaves, test_leaves = {leaf(f) for f in train}, {leaf(f) for f in test}
    return {
        "train_page_ids": train, "test_page_ids": test,
        "train_folios": len(train), "test_folios": len(test),
        "train_lines": sum(pages[f] for f in train),
        "test_lines": sum(pages[f] for f in test),
        "train_physical_leaves": len(train_leaves),
        "test_physical_leaves": len(test_leaves),
        "shared_physical_leaves": sorted(train_leaves & test_leaves),
        "test_leaves_exposed_to_train": len(train_leaves & test_leaves),
        "test_leaves_unseen_in_train": len(test_leaves - train_leaves),
    }


def audit(root: Path = ROOT) -> dict:
    verify_bytes(root / HISTORICAL_SCRIPT, SCRIPT_SHA256)
    old = json.loads(verify_bytes(root / HISTORICAL_RESULTS, RESULTS_SHA256))
    if old.get("experiment") != "exp_607_heldout_bigram_prediction":
        raise ValueError("Historical result identity drift")
    previous = {x["label"]: x for x in old["sources"]}
    if set(previous) != set(CORPORA):
        raise ValueError("Historical result sources drift")
    results = {}
    for name, expected in CORPORA.items():
        raw = verify_bytes(root / expected["path"], expected["sha256"])
        old_record = previous[name]
        if old_record["sha256"] != expected["sha256"]:
            raise ValueError(f"{name}: archived corpus identity drift")
        rows = allocation(eligible_pages(raw))
        for field in ("train_folios", "test_folios", "train_lines", "test_lines",
                      "shared_physical_leaves"):
            if rows[field] != expected[field]:
                raise ValueError(f"{name}: {field} drift: {rows[field]} != {expected[field]}")
        for field in ("train_folios", "test_folios", "train_lines", "test_lines"):
            if rows[field] != old_record[field]:
                raise ValueError(f"{name}: historical JSON {field} drift")
        results[name] = {"source": expected["path"], "source_sha256": expected["sha256"], **rows}
    return {
        "status": "INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY",
        "audit": "EXP-607 historical page-side split; metadata-only replay",
        "historical_script_sha256": SCRIPT_SHA256,
        "historical_results_sha256": RESULTS_SHA256,
        "sources": results,
        "limitations": [
            "No predictive scores or null controls rerun; original positive gains remain archived.",
            "Page-side split is not a physically independent leaf holdout.",
            "Related transcriptions are not independent replications.",
            "The shared-leaf count cannot quantify bias in the reported predictive gains.",
            "Historical Latin-1 and regex eligibility intentionally mirrored; no IVTFF adjudication.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Write evidence only to a new file")
    args = parser.parse_args()
    result = audit()
    if args.out:
        with args.out.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
    print(json.dumps({"status": result["status"],
                      "sources": {name: {k: record[k] for k in (
                          "train_folios", "test_folios", "train_lines", "test_lines",
                          "train_physical_leaves", "test_physical_leaves", "shared_physical_leaves")}
                          for name, record in result["sources"].items()}}, sort_keys=True))


if __name__ == "__main__":
    main()
