#!/usr/bin/env python3
"""Exploratory max-T sensitivity for EXP-593 on the broader EXP-590 page scope."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/transcriptions/eva_zl3b.txt"
OUT = ROOT / "research/maintenance/2026-11-04-exp593-expanded-population-sensitivity.json"
PAGE_LINE = re.compile(r"^<(f(?:\d+[rv][1-6]?|Ros))\.(\d+),[^>]*>\s*(.*)$")
TOKEN = re.compile(r"[a-z]+")
VARIANTS = ("daiin", "dain", "daiiin")
N_PERM = 5000
SEED = 0x59320261104

class XorShift32:
    def __init__(self, seed: int) -> None:
        self.state = seed & 0xFFFFFFFF
    def random(self) -> float:
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x & 0xFFFFFFFF
        return self.state / 2**32

def parse(raw: bytes) -> list[list[str]]:
    lines = []
    for row in raw.decode("utf-8-sig").splitlines():
        match = PAGE_LINE.match(row)
        if not match:
            continue
        body = re.sub(r"<[^>]*>|\{[^}]*\}|\[[^]]*\]", " ", match.group(3))
        tokens = TOKEN.findall(body.lower())
        if tokens:
            lines.append(tokens)
    return lines

def main() -> None:
    raw = SOURCE.read_bytes()
    lines = parse(raw)
    observed = {w: {"occurrences": 0, "line_initial": 0, "line_final": 0} for w in VARIANTS}
    for tokens in lines:
        for word in VARIANTS:
            observed[word]["occurrences"] += tokens.count(word)
            observed[word]["line_initial"] += int(tokens[0] == word)
            observed[word]["line_final"] += int(tokens[-1] == word)
    rng = XorShift32(SEED)
    null = {word: [] for word in VARIANTS}
    for _ in range(N_PERM):
        counts = {word: 0 for word in VARIANTS}
        for tokens in lines:
            first = tokens[int(rng.random() * len(tokens))]
            for word in VARIANTS:
                counts[word] += int(first == word)
        for word in VARIANTS:
            null[word].append(counts[word])
    means = {w: sum(null[w]) / N_PERM for w in VARIANTS}
    sds = {w: (sum((x - means[w]) ** 2 for x in null[w]) / N_PERM) ** 0.5 for w in VARIANTS}
    def zscore(word: str, value: int | float) -> float:
        return (value - means[word]) / sds[word] if sds[word] else 0.0
    max_null_z = [max(zscore(w, null[w][i]) for w in VARIANTS) for i in range(N_PERM)]
    tests = {}
    for word in VARIANTS:
        exceed = sum(x >= observed[word]["line_initial"] for x in null[word])
        max_exceed = sum(x >= zscore(word, observed[word]["line_initial"]) for x in max_null_z)
        tests[word] = {
            "null_mean_initial": means[word], "null_sd_initial": sds[word],
            "observed_standardized_statistic": zscore(word, observed[word]["line_initial"]),
            "empirical_p": (exceed + 1) / (N_PERM + 1),
            "maxT_adjusted_p": (max_exceed + 1) / (N_PERM + 1),
            "null_exceedances": exceed, "maxT_exceedances": max_exceed,
        }
    result = {
        "status": "EXPLORATORY", "parent_analysis": "EXP-593",
        "scope": "EXP-590 broad page-ID pattern, including numbered pages and fRos",
        "source": "data/transcriptions/eva_zl3b.txt",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "lines": len(lines), "tokens": sum(map(len, lines)),
        "variants": list(VARIANTS), "observed": observed,
        "permutations": N_PERM, "seed": f"0x{SEED:x}", "prng": "xorshift32",
        "null_model": "Synchronized independent uniform token draw per line; distribution-equivalent to within-line shuffle for line-initial counts. max-T uses the maximum per-variant standardized statistic on each replicate.",
        "limitations": [
            "Sensitivity analysis only; does not replace or alter archived EXP-593.",
            "Exploratory variant set and previously selected target words.",
            "Does not test semantics or provide a decipherment.",
            "Alternative PRNG stream is not an exact replay of EXP-593's Python random.shuffle stream.",
            "Current page-ID coverage does not establish full IVTFF conformance."
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
