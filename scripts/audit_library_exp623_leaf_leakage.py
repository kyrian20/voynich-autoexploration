#!/usr/bin/env python3
"""Read-only audit of physical-leaf leakage in two archived Library EXP-623 pilots.

This reimplements only their *folio eligibility and allocation*, not their
predictive metrics. No tokens are scored and no held-out rule is selected.
Library scripts are external, hash-identified sources; this is not a rerun of
their historical JavaScript pilots or a semantic validation.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

# Share the strict physical-row contract with other IVTFF metadata auditors.
# str.splitlines() treats eight non-physical Unicode/control separators as rows.
if __package__:
    from .ivtff_physical_rows import checked_physical_lines
else:
    from ivtff_physical_rows import checked_physical_lines

ROOT = Path(__file__).resolve().parents[1]
CORPORA = {
    "ZL3b": ("eva_zl3b.txt", "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc", 623101),
    "IT2a": ("eva_it2a.txt", "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5", 623102),
}
LIBRARY_SCRIPT_SHA256 = {
    "A_all_tokens": "c4bb8e7fb44632b93979a26bb88c49264c3fb7c4c2d3685a59d72958f902b070",
    "B_interior_tokens": "ea51e67e6f36b8c651231262cb22ebbb5ef9f98cd31c4673924e33d6a3627010",
}
B_SEEDS = (623, 701, 809, 907, 1009, 1103, 1201, 1301, 1409, 1511)
# Frozen independent checkpoint from source-blob/JS algorithm audit on 2026-10-28.
EXPECTED_OVERLAP = {
    "ZL3b": {
        "A_all_tokens": (51, 57, 48, 45, 52, 46, 42, 49, 48, 47, 41, 48, 55, 50, 53, 54, 51, 44, 43, 49),
        "B_interior_tokens": (44, 48, 44, 40, 31, 44, 38, 40, 45, 41),
    },
    "IT2a": {
        "A_all_tokens": (45, 53, 45, 42, 47, 50, 51, 47, 43, 52, 48, 49, 46, 49, 38, 44, 48, 49, 50, 53),
        "B_interior_tokens": (44, 48, 44, 40, 31, 44, 38, 40, 45, 41),
    },
}
# Canonical JSON SHA-256 of each full row series in the verified, post-merge
# PR #126 CI artifact (run 40695242744, artifact 12819575881). Unlike the
# historical overlap counts, these lock seed, train/test sizes and the exact
# identities of shared physical leaves. This is an integrity checkpoint of
# our reconstruction, NOT independent verification of the Library pilots.
EXPECTED_SPLIT_SHA256 = {
    "ZL3b": {
        "A_all_tokens": "cf0300ffdc468930c99c1e4e6622611062467eff9c9a524390bf6dd508f4415d",
        "B_interior_tokens": "07d3fbfeafdacfa4c8c801ee19fe188ac5d312f3f73b0c0ef302ee031d6435df",
    },
    "IT2a": {
        "A_all_tokens": "48bea7c3f3e07df730ce08830ce4b1f7a6f48ca808b144bb176e6995a144d6b8",
        "B_interior_tokens": "07d3fbfeafdacfa4c8c801ee19fe188ac5d312f3f73b0c0ef302ee031d6435df",
    },
}

# Independently checked against the two hash-identified transcriptions.
# These eight eligible page-sides have no $L= metadata and were included by
# the historical B pilot as a third '?' stratum, not as Currier A or B.
EXPECTED_B_STRATA = {
    name: {
        "counts": {"A": 114, "B": 81, "?": 8},
        "unclassified": ["f65v", "f67r1", "f67r2", "f68r1", "f68r2",
                         "f68v3", "f68v2", "f69r"],
    }
    for name in CORPORA
}

FOLIO_HEADER = re.compile(r"^<(f\d+[rv]\d*)>\s*(.*)$", re.I)
ANY_TAG = re.compile(r"^<([^>]+)>\s*(.*)$")
A_LOCUS = re.compile(r"^<([^>.]+)\.[^>]*>\s*(.*)$")
LEAF = re.compile(r"^f([0-9]+)[rv]", re.I)


class LCG:
    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF

    def random(self) -> float:
        self.state = (1664525 * self.state + 1013904223) & 0xFFFFFFFF
        return self.state / 4294967296.0


class Mulberry32:
    def __init__(self, seed: int):
        self.a = int(seed)

    def random(self) -> float:
        self.a += 0x6D2B79F5
        t = self.a & 0xFFFFFFFF
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        inner = ((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF
        t = (t ^ ((t + inner) & 0xFFFFFFFF)) & 0xFFFFFFFF
        t = (t ^ (t >> 14)) & 0xFFFFFFFF
        return t / 4294967296.0


def shuffled(items: list[str], rng) -> list[str]:
    result = list(items)
    for i in range(len(result) - 1, 0, -1):
        j = int(rng.random() * (i + 1))
        result[i], result[j] = result[j], result[i]
    return result


def eligible_a(text: str) -> list[str]:
    """LIB A: any locus with at least one [a-z]+ token; page-side IDs."""
    pages = set()
    for _, line in checked_physical_lines(text):
        match = A_LOCUS.match(line)
        if not match:
            continue
        body = re.sub(r"<[^>]*>", " ", match.group(2))
        body = re.sub(r"\[([^\]]+)\]", lambda m: m.group(1).split(":")[0], body)
        body = re.sub(r"\{[^}]*\}", " ", body)
        if re.findall(r"[a-z]+", body.lower()):
            pages.add(match.group(1))
    return sorted(pages)


def eligible_b(text: str) -> tuple[list[str], dict[str, str]]:
    """LIB B: P0 loci with >=2 clean tokens; preserve first-seen page order."""
    labels = {}
    folios = []
    seen = set()
    current_folio = None
    for _, line in checked_physical_lines(text):
        header = FOLIO_HEADER.match(line)
        if header:
            current_folio = header.group(1)
            label = re.search(r"\$L=([A-Z])", header.group(2))
            labels[current_folio] = label.group(1) if label else "?"
            continue
        match = ANY_TAG.match(line)
        if not match or current_folio is None or not re.search(r"P0(?:>|$)", match.group(1)):
            continue
        body = re.sub(r"<[^>]*>", " ", match.group(2).lower())
        body = re.sub(r"@\d+;", " ", body)
        words = [part for part in re.split(r"[.,\s]+", body)
                 if part and not re.search(r"[\[\]{}?]", part) and re.fullmatch(r"[a-z]+", part)]
        if len(words) >= 2 and current_folio not in seen:
            seen.add(current_folio)
            folios.append(current_folio)
    return folios, labels


def physical_leaf(folio: str) -> int | None:
    match = LEAF.match(folio)
    return int(match.group(1)) if match else None


def overlap(train: set[str], test: set[str]) -> list[int]:
    train_leaves = {physical_leaf(folio) for folio in train} - {None}
    test_leaves = {physical_leaf(folio) for folio in test} - {None}
    return sorted(train_leaves & test_leaves)


def currier_strata(folios: list[str], labels: dict[str, str]) -> tuple[dict[str, int], list[str]]:
    """Report every actual B-pilot group; never silently call '?' Currier A/B."""
    counts: dict[str, int] = {}
    unknown: list[str] = []
    for folio in folios:
        label = labels.get(folio, "?")
        counts[label] = counts.get(label, 0) + 1
        if label not in ("A", "B"):
            unknown.append(folio)
    return counts, unknown


def splits_a(pages: list[str], base_seed: int) -> list[dict]:
    result = []
    for index in range(20):
        seed = base_seed + index * 9973
        order = shuffled(pages, LCG(seed))
        n_train = int(len(order) * 0.7)
        train, test = set(order[:n_train]), set(order[n_train:])
        result.append({"seed": seed, "train_page_ids": len(train), "test_page_ids": len(test),
                       "shared_physical_leaves": overlap(train, test)})
    return result


def splits_b(folios: list[str], labels: dict[str, str]) -> list[dict]:
    groups = defaultdict(list)
    for folio in folios:
        groups[labels.get(folio, "?")].append(folio)
    result = []
    for seed in B_SEEDS:
        rng = Mulberry32(seed)
        train, test = set(), set()
        for group in groups.values():
            order = shuffled(group, rng)
            n_test = max(1, round(len(order) * 0.30))
            test.update(order[:n_test])
            train.update(order[n_test:])
        result.append({"seed": seed, "train_page_ids": len(train), "test_page_ids": len(test),
                       "shared_physical_leaves": overlap(train, test)})
    return result


def analyze(name: str, raw: bytes) -> dict:
    filename, expected_sha, base_seed = CORPORA[name]
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != expected_sha:
        raise ValueError(f"{name}: source SHA-256 mismatch")
    text = raw.decode("utf-8")
    pages = eligible_a(text)
    folios, labels = eligible_b(text)
    strata_counts, unclassified = currier_strata(folios, labels)
    a = splits_a(pages, base_seed)
    b = splits_b(folios, labels)
    return {
        "source": f"data/transcriptions/{filename}", "sha256": actual_sha,
        "A_eligible_page_ids": len(pages), "B_eligible_page_ids": len(folios),
        "B_currier_group_counts": strata_counts,
        "B_unclassified_folios": unclassified,
        "A_all_tokens": a, "B_interior_tokens": b,
    }


def split_sha256(rows: list[dict]) -> str:
    """Lock exact row membership and metadata, not just aggregate counts."""
    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def check_expected(results: dict) -> None:
    for name, expected in EXPECTED_B_STRATA.items():
        actual = results[name]
        if (actual.get("B_currier_group_counts") != expected["counts"] or
                actual.get("B_unclassified_folios") != expected["unclassified"]):
            raise ValueError(f"{name}: Currier stratum drift (including unclassified folios)")
    for name, methods in EXPECTED_OVERLAP.items():
        for method, expected in methods.items():
            rows = results[name][method]
            observed = tuple(len(row["shared_physical_leaves"]) for row in rows)
            if observed != expected:
                raise ValueError(f"{name}/{method}: overlap counts drift: {observed} != {expected}")
            digest = split_sha256(rows)
            frozen = EXPECTED_SPLIT_SHA256[name][method]
            if digest != frozen:
                raise ValueError(f"{name}/{method}: split evidence drift: {digest} != {frozen}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check independently frozen overlap counts")
    parser.add_argument("--out", type=Path, help="Exclusively create full per-seed overlap evidence; never overwrite")
    args = parser.parse_args()
    results = {name: analyze(name, (ROOT / "data/transcriptions" / entry[0]).read_bytes())
               for name, entry in CORPORA.items()}
    if args.check:
        check_expected(results)
    payload = {
        "status": "INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY",
        "scope": "Metadata split replay, not historical predictive-score reproduction",
        "library_script_sha256": LIBRARY_SCRIPT_SHA256,
        "sources": results,
        "limitations": [
            "Library scripts not copied into GitHub; algorithm reconstructed from hash-identified files.",
            "No tokens scored, no semantic inference, no historical JS pilot rerun.",
            "The leaked-leaf count is not an estimate of predictive-score inflation.",
            "These page-side splits do not qualify as independent physical-leaf holdouts.",
        ],
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        # An audit receipt is evidence: never truncate an earlier run, even
        # when a caller accidentally reuses its path or points to a symlink.
        with args.out.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps({"status": payload["status"], "check": args.check,
                      "overlap_counts": {name: {method: [len(x["shared_physical_leaves"]) for x in results[name][method]]
                                                for method in ("A_all_tokens", "B_interior_tokens")}
                                         for name in results}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
