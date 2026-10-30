#!/usr/bin/env python3
"""Read-only replay of Library EXP-624 page allocation; no model scoring.

The archived Library script is NOT executed or replaced. This implementation
mirrors only its parsing, eligibility, LCG shuffle and 70/30 page split.
It tests the *physical-leaf* independence of those page-side partitions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "ZL3b": ("eva_zl3b.txt", "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"),
    "IT2a": ("eva_it2a.txt", "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"),
}
LIBRARY_EVIDENCE = {
    "script_sha256": "1f00846ab8e91cefd07bc2dcd26ad12cf8a7c4bc7b2478d480afec391a13f3a9",
    "results_sha256": "d6e1b7490e563c96367ff10ab56feb5487d6b2775a885494f249c89f87bd4bab",
    "report_sha256": "7de18cce59ea21598af7958a7ded3e05b03e305e8a6cc84c0740917b807447c4",
}
# Independently observed against both frozen corpora and the hash-identified
# Library script's deterministic split. These are physical-leaf intersections,
# NOT performance metrics and NOT a historical rerun of the model.
EXPECTED = {
    "ZL3b": {
        "all": (37, 46, 38, 39, 40, 43, 36, 39),
        "A": (23, 25, 27, 24, 22, 20),
        "B": (23, 15, 18, 14, 16, 19),
    },
    "IT2a": {"all": (37, 46, 38, 39, 40, 43, 36, 39)},
}
EXPECTED_LEAKED_TEST_PAGES = {
    "ZL3b": {
        "all": (40, 49, 41, 43, 44, 47, 36, 39),
        "A": (23, 25, 27, 25, 23, 21),
        "B": (23, 15, 18, 18, 17, 20),
    },
    "IT2a": {"all": (40, 49, 41, 43, 44, 47, 36, 39)},
}


def parse_pages(raw: bytes) -> list[dict]:
    """Reproduce only Library exp624_positional_holdout.py's page selection.

    Keep the original permissive tokenizer for a faithful eligibility replay.
    This is NOT an endorsed IVTFF parser for new scientific experiments.
    """
    pages: dict[str, dict] = {}
    current_language = None
    for line in raw.decode("utf-8").splitlines():
        header = re.match(r"^<([^>.]+)>\s*<!([^>]*)>", line)
        if header:
            page_id = header.group(1)
            lm = re.search(r"\$L=([AB])", header.group(2))
            current_language = lm.group(1) if lm else None
            if page_id not in pages:
                pages[page_id] = {"id": page_id, "lang": current_language, "words": []}
            elif current_language:
                pages[page_id]["lang"] = current_language
            continue
        m = re.match(r"^<([^>.]+)\.([^,>]+),([^>]+)>\s*(.*)$", line)
        if not m or not re.search(r"(?:P0|Pt)", m.group(3)):
            continue
        page_id, body = m.group(1), m.group(4)
        if page_id not in pages:
            pages[page_id] = {"id": page_id, "lang": current_language, "words": []}
        body = re.sub(r"<[^>]*>", " ", body)
        body = re.sub(r"\[([^\]]+)\]", lambda x: x.group(1).split(":")[0], body)
        body = re.sub(r"\{[^}]*\}", " ", body).lower()
        pages[page_id]["words"].extend(re.findall(r"[a-z]+", body))
    # Original parse_corpus first excludes empty pages. run_mode then excludes
    # pages with no word of 2..12 units. Both raw/glyph views have same page
    # eligibility in the two frozen inputs; pin and report only the raw view.
    return [p for p in pages.values() if p["words"] and
            any(2 <= len(w) <= 12 for w in p["words"])]


class LCG:
    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF

    def random(self) -> float:
        self.state = (1664525 * self.state + 1013904223) & 0xFFFFFFFF
        return self.state / 4294967296.0


def shuffled(items: list, rng: LCG) -> list:
    out = list(items)
    for i in range(len(out) - 1, 0, -1):
        j = int(rng.random() * (i + 1))
        out[i], out[j] = out[j], out[i]
    return out


def physical_leaf(page_id: str) -> int | None:
    m = re.match(r"^f(\d+)[rv]", page_id, re.IGNORECASE)
    return int(m.group(1)) if m else None


def splits(pages: list[dict], seed_base: int, repetitions: int) -> list[dict]:
    rows = []
    for i in range(repetitions):
        seed = seed_base + i * 7919
        ordered = shuffled(pages, LCG(seed))
        cut = int(len(ordered) * 0.7)
        train, test = ordered[:cut], ordered[cut:]
        train_leaves = {physical_leaf(p["id"]) for p in train} - {None}
        test_leaves = {physical_leaf(p["id"]) for p in test} - {None}
        shared = sorted(train_leaves & test_leaves)
        leaked_test_ids = sorted(p["id"] for p in test if physical_leaf(p["id"]) in train_leaves)
        rows.append({"seed": seed, "train_pages": len(train), "test_pages": len(test),
                     "train_leaves": len(train_leaves), "test_leaves": len(test_leaves),
                     "shared_physical_leaves": shared,
                     "leaked_test_page_ids": leaked_test_ids})
    return rows


def analyze(label: str, raw: bytes) -> dict:
    filename, expected_sha = SOURCES[label]
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected_sha:
        raise ValueError(f"{label}: frozen corpus SHA-256 mismatch: {actual}")
    pages = parse_pages(raw)
    groups = {"all": splits(pages, 624010, 8)}
    if label == "ZL3b":
        for language in ("A", "B"):
            groups[language] = splits([p for p in pages if p["lang"] == language], 625010, 6)
    return {"path": f"data/transcriptions/{filename}", "sha256": actual,
            "eligible_page_ids": len(pages),
            "currier_page_counts": {lang: sum(p["lang"] == lang for p in pages)
                                    for lang in ("A", "B")},
            "unclassified_page_ids": sum(p["lang"] not in ("A", "B") for p in pages),
            "groups": groups}


def check(results: dict) -> None:
    for label, expected_groups in EXPECTED.items():
        row = results[label]
        if row["eligible_page_ids"] != 203 or row["currier_page_counts"] != {"A": 114, "B": 81} or row["unclassified_page_ids"] != 8:
            raise ValueError(f"{label}: historical page eligibility drift")
        for group, expected in expected_groups.items():
            rows = row["groups"][group]
            shared = tuple(len(r["shared_physical_leaves"]) for r in rows)
            leaked = tuple(len(r["leaked_test_page_ids"]) for r in rows)
            if shared != expected or leaked != EXPECTED_LEAKED_TEST_PAGES[label][group]:
                raise ValueError(f"{label}/{group}: physical-leaf split drift: {shared}; {leaked}")
            if any(not r["shared_physical_leaves"] for r in rows):
                raise ValueError(f"{label}/{group}: unexpectedly independent physical-leaf split")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify frozen expected split identities/counts")
    parser.add_argument("--out", type=Path, help="Write new evidence JSON (exclusive create)")
    args = parser.parse_args()
    results = {label: analyze(label, (ROOT / "data/transcriptions" / entry[0]).read_bytes())
               for label, entry in SOURCES.items()}
    if args.check:
        check(results)
    evidence = {"status": "INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY",
                "historical_model_reexecuted": False,
                "scope": "Replay of Library EXP-624 page eligibility and deterministic split only; no predictive scores",
                "library_artifact_sha256": LIBRARY_EVIDENCE,
                "results": results,
                "limitations": ["Page-side holdout still has a descriptive interpretation, not a physical-leaf holdout.",
                                "The amount of metric inflation is not estimated.",
                                "The archived Library script/results/report are preserved; no exact JS pilot rerun.",
                                "A/B page labels are source metadata, not independent manuscripts."]}
    if args.out:
        with args.out.open("x", encoding="utf-8") as f:
            json.dump(evidence, f, ensure_ascii=False, sort_keys=True, indent=2)
            f.write("\n")
    print(json.dumps({"status": evidence["status"], "checked": args.check,
                      "overlap_counts": {label: {group: [len(r["shared_physical_leaves"]) for r in rows]
                                                for group, rows in record["groups"].items()}
                                         for label, record in results.items()}}, sort_keys=True))


if __name__ == "__main__":
    main()
