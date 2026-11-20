#!/usr/bin/env python3
"""Reconcile EXP-590/EXP-593 physical-line populations and exact null tails."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

EXPECTED_SHA256 = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
VARIANTS = ("daiin", "dain", "daiiin")
TOKEN = re.compile(r"[a-z]+")
# These are the line-ID patterns in the archived experiment scripts.
BROAD = re.compile(r"^<(f(?:\d+[rv][1-6]?|Ros))\.(\d+),[^>]*>\s*(.*)$")
RESTRICTED = re.compile(r"^<f(\d+[rv])\.(\d+),[^>]*>\s*(.*)$")


def parse(path: Path, pattern: re.Pattern[str], add_f_prefix: bool) -> dict:
    rows = {}
    for raw in path.read_bytes().decode("utf-8-sig").splitlines():
        match = pattern.match(raw)
        if not match:
            continue
        folio, line_no, body = match.groups()
        locus = ("f" if add_f_prefix else "") + folio + "." + line_no
        body = re.sub(r"<[^>]*>|\{[^}]*\}|\[[^\]]*\]", " ", body)
        tokens = TOKEN.findall(body.lower())
        if not tokens:
            continue
        if locus in rows:
            raise ValueError(f"duplicate nonempty physical locus: {locus}")
        rows[locus] = (raw, tokens)
    return rows


def exact_tail(rows: dict, word: str) -> dict:
    observed = sum(tokens[0] == word for _, tokens in rows.values())
    occurrences = sum(tokens.count(word) for _, tokens in rows.values())
    # Under within-line exchangeability, each line contributes an independent
    # Bernoulli draw with p=count(word)/line_length. The final DP cell stores
    # P(X >= observed), yielding the exact Poisson-binomial tail distribution.
    dp = [1.0]
    for _, tokens in rows.values():
        p = tokens.count(word) / len(tokens)
        next_dp = [0.0] * (min(len(dp), observed) + 1)
        for count, mass in enumerate(dp):
            next_dp[count] += mass * (1.0 - p)
            next_dp[min(count + 1, observed)] += mass * p
        dp = next_dp
    tail = dp[observed] if observed < len(dp) else 0.0
    return {
        "occurrences": occurrences,
        "line_initial": observed,
        "line_final": sum(tokens[-1] == word for _, tokens in rows.values()),
        "exact_one_sided_p": tail,
    }


def holm(p_values: dict[str, float]) -> dict[str, float]:
    ordered = sorted(p_values, key=p_values.get)
    adjusted = {}
    running = 0.0
    for index, word in enumerate(ordered):
        running = max(running, min(1.0, (len(ordered) - index) * p_values[word]))
        adjusted[word] = running
    return adjusted


def summarize(rows: dict) -> dict:
    stats = {word: exact_tail(rows, word) for word in VARIANTS}
    corrected = holm({word: stats[word]["exact_one_sided_p"] for word in VARIANTS})
    return {
        "nonempty_lines": len(rows),
        "tokens": sum(len(tokens) for _, tokens in rows.values()),
        "variants": {
            word: {**stats[word], "holm_adjusted_p": corrected[word]}
            for word in VARIANTS
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    source = parser.parse_args().source
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"source SHA-256 mismatch: {digest}")

    broad = parse(source, BROAD, add_f_prefix=False)
    restricted = parse(source, RESTRICTED, add_f_prefix=True)
    broad_ids, restricted_ids = set(broad), set(restricted)
    shared = broad_ids & restricted_ids
    only_broad, only_restricted = broad_ids - restricted_ids, restricted_ids - broad_ids
    if only_restricted:
        raise SystemExit(f"restricted population is not a subset: {len(only_restricted)} loci")
    if any(broad[locus] != restricted[locus] for locus in shared):
        raise SystemExit("shared raw source rows or token sequences differ")

    types = collections.Counter()
    for locus in only_broad:
        folio = locus.split(".", 1)[0]
        if folio == "fRos":
            types["fRos"] += 1
        elif re.fullmatch(r"f\d+[rv][1-6]", folio):
            types["numbered_subfolio"] += 1
        else:
            types["other"] += 1

    result = {
        "audit": "EXP-590/EXP-593 exact population reconciliation",
        "status": "REPRODUCED",
        "source": "data/transcriptions/eva_zl3b.txt",
        "source_sha256": digest,
        "parser_scope": {
            "EXP-590": "fNNr/v with optional numbered subfolio suffix, plus fRos",
            "EXP-593": "fNNr/v only",
        },
        "locus_reconciliation": {
            "broad": summarize(broad),
            "restricted": summarize(restricted),
            "shared_loci": len(shared),
            "shared_raw_rows_and_tokens_identical": True,
            "only_broad_loci": len(only_broad),
            "only_broad_tokens": sum(len(broad[locus][1]) for locus in only_broad),
            "only_broad_by_folio_type": dict(sorted(types.items())),
            "only_restricted_loci": 0,
            "duplicate_nonempty_loci": 0,
        },
        "null_model": (
            "Independent within-line exchangeability: each line's first token is "
            "drawn uniformly from its observed token multiset. Exact Poisson-binomial "
            "upper tails with Holm correction over the three historically selected variants."
        ),
        "limitations": [
            "The three-word family was selected in earlier exploratory work; Holm correction covers these variants only, not historical target selection or all prior analyses.",
            "The null preserves each line's token multiset but discards order; it is not a language or random-text control.",
            "ZL3b is one transcription of one manuscript; this audit establishes no semantics or decipherment.",
            "The parser reproduces the two archived line patterns and tokenization; it is not a full independent IVTFF conformance audit.",
            "These exact-tail calculations are a new sensitivity analysis and do not overwrite either frozen experiment archive.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
