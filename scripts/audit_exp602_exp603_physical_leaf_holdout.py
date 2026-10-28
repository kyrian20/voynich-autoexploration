#!/usr/bin/env python3
"""Hash-gated, read-only reconstruction of historical GH-602/EXP-603 page splits.

No prediction, bootstrap, model fitting, or new use of held-out target labels.
This mirrors the historical Latin-1 parser and does NOT certify IVTFF correctness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = "data/transcriptions/eva_zl3b.txt"
CORPUS_SHA256 = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
FROZEN = {
    "GH-602-HELDOUT-PREDICTION": {
        "script": "experiments/exp_602_heldout_predictive_test/script.py",
        "script_sha256": "5e708a943c8340626ef30b0acf507987e843a27f6217f3f967ebde15d6d53232",
        "results": "experiments/exp_602_heldout_predictive_test/results.json",
        "results_sha256": "1bbba43b704e679289a4a820c887810d86ee2e648d79107b53cd64845f9e9085",
        "experiment": "exp_602_heldout_predictive_test",
        "dialects": ("B",),
        "train_lines": 1797, "test_lines": 528,
        "train_pages": 60, "test_pages": 21,
        "train_leaves": 37, "test_leaves": 18,
        "shared": [34, 39, 43, 50, 55, 66, 81, 84, 86, 94, 95, 105, 111, 113, 114],
    },
    "EXP-603-STRATIFIED-HELDOUT": {
        "script": "experiments/exp_603_stratified_heldout_prediction/script.py",
        "script_sha256": "7577395f6655254f26772fdc84c116f543a7fbcf3cfdf86561b8d7bc8ff36b01",
        "results": "experiments/exp_603_stratified_heldout_prediction/results.json",
        "results_sha256": "b099507e104cab0483cdf646d91ba9bb785ed6217df8d086428bf94bace50c4f",
        "experiment": "exp_603",
        "dialects": ("A", "B"),
        "train_lines": 2928, "test_lines": 919,
        "train_pages": 148, "test_pages": 47,
        "train_leaves": 87, "test_leaves": 39,
        "shared": [5, 9, 11, 17, 18, 21, 27, 28, 30, 32, 34, 37, 39, 42, 43, 44,
                   49, 50, 55, 66, 81, 84, 86, 94, 95, 99, 100, 102, 105, 111, 113, 114],
    },
}
PAGE_RE = re.compile(r"^f([0-9]+)[rv][0-9]*\Z")


def verify_bytes(path: Path, expected: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Frozen source missing or symlinked: {path}")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f"Frozen SHA-256 mismatch: {path}")
    return raw


def physical_leaf(page: str) -> int:
    match = PAGE_RE.fullmatch(page)
    if not match:
        raise ValueError(f"Unsupported historical page identifier: {page}")
    return int(match.group(1))


def eligible_rows(raw: bytes) -> list[tuple[str, str]]:
    """Mirror both historical scripts' page headers, P0 filtering, and cleaning."""
    rows = []
    folio, dialect = "unknown", "unknown"
    for line in raw.decode("latin-1").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if re.match(r"^<f\w+>.*\$", s):
            m = re.match(r"^<(f\w+)>", s)
            if m:
                folio = m.group(1)
            m = re.search(r"\$L=([AB])", s)
            dialect = m.group(1) if m else "unknown"
            continue
        m = re.match(r"^<([^>]+)>\s+(.*)$", s)
        if not m or "," not in m.group(1):
            continue
        slot = m.group(1).split(",", 1)[1]
        if re.sub(r"^[+*@=~&!/]+", "", slot) != "P0":
            continue
        body = re.sub(r"<!.*?>|<[^>]*>", " ", m.group(2))
        body = re.sub(r"\[([^:\]]+):[^\]]*\]", r"\1", body)
        body = re.sub(r"\{[^}]*\}|@\d+;?", " ", body)
        words = [w.lower() for w in re.split(r"[.\s,]+", body)
                 if re.fullmatch(r"[A-Za-z]+", w)]
        if len(words) >= 2 and dialect in ("A", "B"):
            rows.append((folio, dialect))
    return rows


def held_out(page: str) -> bool:
    return int(hashlib.sha256(("voynich-exp602:" + page).encode("ascii"))
               .hexdigest()[:8], 16) % 5 == 0


def allocation(rows: list[tuple[str, str]], dialects: tuple[str, ...]) -> dict:
    selected = [(page, lang) for page, lang in rows if lang in dialects]
    train = [page for page, _ in selected if not held_out(page)]
    test = [page for page, _ in selected if held_out(page)]
    train_pages, test_pages = set(train), set(test)
    if train_pages & test_pages:
        raise ValueError("A page side crossed the historical split")
    train_leaves = {physical_leaf(page) for page in train_pages}
    test_leaves = {physical_leaf(page) for page in test_pages}
    shared = sorted(train_leaves & test_leaves)
    return {
        "train_lines": len(train), "test_lines": len(test),
        "train_pages": len(train_pages), "test_pages": len(test_pages),
        "train_leaves": len(train_leaves), "test_leaves": len(test_leaves),
        "shared": shared, "shared_count": len(shared),
        "unseen_test_leaves": sorted(test_leaves - train_leaves),
        "train_page_ids": sorted(train_pages), "test_page_ids": sorted(test_pages),
    }


def check_snapshot(observed: dict, expected: dict) -> None:
    for key in ("train_lines", "test_lines", "train_pages", "test_pages",
                "train_leaves", "test_leaves", "shared"):
        if observed[key] != expected[key]:
            raise ValueError(f"Historical {key} drift: {observed[key]} != {expected[key]}")


def audit(root: Path = ROOT) -> dict:
    raw = verify_bytes(root / CORPUS, CORPUS_SHA256)
    rows = eligible_rows(raw)
    output = {}
    for name, frozen in FROZEN.items():
        verify_bytes(root / frozen["script"], frozen["script_sha256"])
        archived = json.loads(verify_bytes(root / frozen["results"], frozen["results_sha256"]))
        if archived.get("experiment") != frozen["experiment"]:
            raise ValueError(f"{name}: archived experiment identity drift")
        if "source_sha256" in archived and archived["source_sha256"] != CORPUS_SHA256:
            raise ValueError(f"{name}: archived source identity drift")
        result = allocation(rows, frozen["dialects"])
        check_snapshot(result, frozen)
        for key, archive_key in (("train_lines", "train_lines"), ("test_lines", "test_lines"),
                                 ("train_pages", "train_folios"), ("test_pages", "test_folios")):
            if result[key] != archived[archive_key]:
                raise ValueError(f"{name}: archived {archive_key} drift")
        output[name] = {
            "historical_script": frozen["script"],
            "historical_script_sha256": frozen["script_sha256"],
            "historical_results": frozen["results"],
            "historical_results_sha256": frozen["results_sha256"],
            "dialects": list(frozen["dialects"]),
            **result,
        }
    return {
        "status": "INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY",
        "corpus": CORPUS, "corpus_sha256": CORPUS_SHA256,
        "historical_split": "SHA256('voynich-exp602:' + page_side) first 8 hex modulo 5 == 0",
        "studies": output,
        "limitations": [
            "Metadata-only reconstruction; predictive scores and historical bootstraps not reproduced.",
            "The reported held-out pages were never a completely independent physical-leaf holdout.",
            "Historical Latin-1 regex parser deliberately mirrored; IVTFF conformance remains unresolved.",
            "The negative GH-602 primary outcome is not converted into a positive result.",
            "The extent of performance bias is unknown; no semantic or decipherment claim.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="New JSON path; existing files are never overwritten")
    args = parser.parse_args()
    result = audit()
    if args.out:
        with args.out.open("x", encoding="utf-8") as f:
            json.dump(result, f, indent=2, sort_keys=True, ensure_ascii=False)
            f.write("\n")
    print(json.dumps({k: {"shared": v["shared_count"],
                          "test_leaves": v["test_leaves"],
                          "train_lines": v["train_lines"], "test_lines": v["test_lines"]}
                      for k, v in result["studies"].items()}, sort_keys=True))


if __name__ == "__main__":
    main()
