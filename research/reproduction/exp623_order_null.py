#!/usr/bin/env python3
"""EXP-623: held-out word-bigram predictability against endpoint-preserving nulls.

Standard-library only. Intended to run from the repository root:
  python research/exp623_order_null.py

Input files are the repository's ZL3b and IT2a IVTFF/EVA transcriptions.
The two files are alternative transcriptions of the same manuscript, not
independent manuscripts. This experiment measures sequence predictability;
it does not decode or assign meanings to words.
"""
from __future__ import annotations
import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_SEEDS = [623, 701, 809, 907, 1009, 1103, 1201, 1301, 1409, 1511]
MASK32 = 0xFFFFFFFF

class Mulberry32:
    """Small deterministic PRNG matching the JavaScript implementation used in the pilot."""
    def __init__(self, seed: int):
        self.a = int(seed)

    def random(self) -> float:
        self.a += 0x6D2B79F5
        t = self.a & MASK32
        t = ((t ^ (t >> 15)) * (t | 1)) & MASK32
        inner = (((t ^ (t >> 7)) * (t | 61)) & MASK32)
        t = (t ^ ((t + inner) & MASK32)) & MASK32
        t = (t ^ (t >> 14)) & MASK32
        return t / 4294967296.0


def parse_ivtff(path: Path) -> dict:
    """Read P0 body loci; discard tokens with uncertain-reading markup."""
    folio_label: dict[str, str] = {}
    loci: list[dict] = []
    current_folio: str | None = None
    folio_header = re.compile(r"^<(f\d+[rv]\d*)>\s*(.*)$", re.I)
    any_tag = re.compile(r"^<([^>]+)>\s*(.*)$")
    for line in path.read_text(encoding="utf-8").splitlines():
        m = folio_header.match(line)
        if m:
            current_folio = m.group(1)
            label = re.search(r"\$L=([A-Z])", m.group(2))
            folio_label[current_folio] = label.group(1) if label else "?"
            continue
        m = any_tag.match(line)
        if not m or current_folio is None or not re.search(r"P0(?:>|$)", m.group(1)):
            continue
        body = re.sub(r"<[^>]*>", " ", m.group(2).lower())
        body = re.sub(r"@\d+;", " ", body)
        words = []
        for part in re.split(r"[.,\s]+", body):
            if not part or re.search(r"[\[\]{}?]", part):
                continue
            if re.fullmatch(r"[a-z]+", part):
                words.append(part)
        if len(words) >= 2:
            loci.append({"folio": current_folio, "words": words})
    return {"loci": loci, "folio_label": folio_label}


def stratified_holdout(data: dict, seed: int, test_fraction: float = 0.30) -> tuple[set, set]:
    folios_in_text = list(dict.fromkeys(locus["folio"] for locus in data["loci"]))
    groups: dict[str, list[str]] = defaultdict(list)
    for folio in folios_in_text:
        groups[data["folio_label"].get(folio, "?")].append(folio)
    rng = Mulberry32(seed)
    train, test = set(), set()
    for folios in groups.values():
        shuffled = list(folios)
        for i in range(len(shuffled) - 1, 0, -1):
            j = int(rng.random() * (i + 1))
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        n_test = max(1, round(len(shuffled) * test_fraction))
        test.update(shuffled[:n_test])
        train.update(shuffled[n_test:])
    return train, test


def shuffle_interior(loci: list[dict], rng: Mulberry32) -> list[dict]:
    """Shuffle positions 2..n-1; keep first and last tokens and the token bag fixed."""
    out = []
    for locus in loci:
        words = list(locus["words"])
        for i in range(len(words) - 2, 1, -1):
            j = 1 + int(rng.random() * i)
            words[i], words[j] = words[j], words[i]
        out.append({"folio": locus["folio"], "words": words})
    return out


def score_gain(train_loci: list[dict], test_loci: list[dict], alpha: float = 0.1,
               interpolation: float = 0.5) -> dict:
    """Return unigram minus interpolated-bigram test cross-entropy in bits/token."""
    word_counts = Counter()
    bigram_counts = Counter()
    previous_counts = Counter()
    total_train_tokens = 0
    for locus in train_loci:
        words = locus["words"]
        word_counts.update(words)
        total_train_tokens += len(words)
        for prev, word in zip(words, words[1:]):
            bigram_counts[(prev, word)] += 1
            previous_counts[prev] += 1
    vocab_size = len(word_counts) + 1  # one UNK symbol
    unigram_denominator = total_train_tokens + alpha * vocab_size
    unk = "__UNK__"
    unigram_loss = 0.0
    mixed_loss = 0.0
    n_test = 0
    for locus in test_loci:
        words = locus["words"]
        for i, raw_word in enumerate(words):
            word = raw_word if raw_word in word_counts else unk
            p_uni = (word_counts.get(word, 0) + alpha) / unigram_denominator
            p = p_uni
            if i > 0:
                raw_prev = words[i - 1]
                prev = raw_prev if raw_prev in word_counts else unk
                p_bigram = (bigram_counts.get((prev, word), 0) + alpha) / (
                    previous_counts.get(prev, 0) + alpha * vocab_size
                )
                p = interpolation * p_bigram + (1.0 - interpolation) * p_uni
            unigram_loss -= math.log2(p_uni)
            mixed_loss -= math.log2(p)
            n_test += 1
    return {
        "gain_bits_per_token": (unigram_loss - mixed_loss) / n_test,
        "unigram_bits_per_token": unigram_loss / n_test,
        "interpolated_bigram_bits_per_token": mixed_loss / n_test,
        "test_tokens": n_test,
        "train_vocabulary": len(word_counts),
    }


def one_split(data: dict, seed: int, permutations: int) -> dict:
    train_folios, test_folios = stratified_holdout(data, seed)
    train = [x for x in data["loci"] if x["folio"] in train_folios]
    test = [x for x in data["loci"] if x["folio"] in test_folios]
    observed = score_gain(train, test)
    null_gains = []
    for replicate in range(permutations):
        rng = Mulberry32(seed * 1009 + replicate + 17)
        null_train = shuffle_interior(train, rng)
        null_test = shuffle_interior(test, rng)
        null_gains.append(score_gain(null_train, null_test)["gain_bits_per_token"])
    ordered = sorted(null_gains)
    null_mean = sum(null_gains) / len(null_gains)
    q95 = ordered[min(len(ordered) - 1, math.floor(0.95 * (len(ordered) - 1)))]
    return {
        "seed": seed,
        "train_folios": len(train_folios),
        "test_folios": len(test_folios),
        "train_loci": len(train),
        "test_loci": len(test),
        "train_tokens": sum(len(x["words"]) for x in train),
        "test_tokens": sum(len(x["words"]) for x in test),
        "observed": observed,
        "null_permutations": permutations,
        "null_mean_gain": null_mean,
        "null_q95_gain": q95,
        "null_max_gain": ordered[-1],
        "delta_observed_minus_null_mean": observed["gain_bits_per_token"] - null_mean,
        "observed_above_null_q95": observed["gain_bits_per_token"] > q95,
        "observed_above_null_max": observed["gain_bits_per_token"] > ordered[-1],
        "empirical_randomization_p": (1 + sum(x >= observed["gain_bits_per_token"] for x in null_gains)) / (permutations + 1),
    }


def summarize(path: Path, seeds: list[int], permutations: int) -> dict:
    data = parse_ivtff(path)
    results = [one_split(data, seed, permutations) for seed in seeds]
    deltas = [x["delta_observed_minus_null_mean"] for x in results]
    ordered = sorted(deltas)
    return {
        "source_file": str(path),
        "loci": len(data["loci"]),
        "folios_with_eligible_loci": len(set(x["folio"] for x in data["loci"])),
        "tokens": sum(len(x["words"]) for x in data["loci"]),
        "loci_with_shufflable_interior": sum(len(x["words"]) >= 4 for x in data["loci"]),
        "split_count": len(results),
        "permutations_per_split": permutations,
        "mean_delta": sum(deltas) / len(deltas),
        "median_delta": ordered[len(ordered) // 2],
        "min_delta": min(deltas),
        "max_delta": max(deltas),
        "positive_splits": sum(x > 0 for x in deltas),
        "observed_above_null_q95_splits": sum(x["observed_above_null_q95"] for x in results),
        "observed_above_null_max_splits": sum(x["observed_above_null_max"] for x in results),
        "by_split": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zl3b", default="data/transcriptions/eva_zl3b.txt")
    parser.add_argument("--it2a", default="data/transcriptions/eva_it2a.txt")
    parser.add_argument("--seeds", default=",".join(map(str, DEFAULT_SEEDS)))
    parser.add_argument("--permutations", type=int, default=39)
    parser.add_argument("--output", default="research/results/exp623_order_null.json")
    args = parser.parse_args()
    seeds = [int(x.strip()) for x in args.seeds.split(",") if x.strip()]
    if not seeds or args.permutations < 1:
        parser.error("Provide at least one seed and at least one permutation.")
    result = {
        "experiment": "EXP-623",
        "protocol": {
            "loci": "IVTFF P0 paragraph-body loci only; loci with fewer than two clean tokens excluded",
            "cleaning": "remove inline <...> tags and @number; split on period/comma/whitespace; discard any token containing [], {}, or ?; retain only [a-z]+",
            "holdout": "70/30 folio split stratified by $L label; seed-specific, no folio crosses train/test",
            "model": "unigram versus 50/50 interpolated word-bigram; add-alpha=0.1; transitions never cross locus boundaries; test OOV mapped to UNK",
            "null": "within each locus independently shuffle only interior tokens, positions 2..n-1; preserve first and last token, locus length, token multiset, folio assignment, and line order",
            "metric": "unigram test cross-entropy minus interpolated-bigram test cross-entropy, bits/token; positive means bigram improves held-out prediction",
            "interpretation": "tests whether internal word order adds predictive information beyond locus token bags and fixed endpoints; not a decipherment test",
        },
        "seeds": seeds,
        "permutations_per_split": args.permutations,
        "ZL3b": summarize(Path(args.zl3b), seeds, args.permutations),
        "IT2a": summarize(Path(args.it2a), seeds, args.permutations),
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "experiment": result["experiment"],
        "output": str(out),
        "ZL3b": {k: result["ZL3b"][k] for k in ("loci", "folios_with_eligible_loci", "tokens", "mean_delta", "median_delta", "min_delta", "max_delta", "positive_splits", "observed_above_null_q95_splits", "observed_above_null_max_splits")},
        "IT2a": {k: result["IT2a"][k] for k in ("loci", "folios_with_eligible_loci", "tokens", "mean_delta", "median_delta", "min_delta", "max_delta", "positive_splits", "observed_above_null_q95_splits", "observed_above_null_max_splits")},
    }, indent=2))

if __name__ == "__main__":
    main()