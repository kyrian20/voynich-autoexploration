#!/usr/bin/env python3
"""Experiment 623: held-out word-order permutation control for Voynich EVA.

Reads the repository's ZL3b and IT2a IVTFF transcriptions. It uses folio-level
70/30 train/test splits, fits a smoothed unigram model and a 50/50 interpolated
unigram/bigram model on training folios, then compares held-out loss on the
original token order with token permutations performed independently inside
each locus. Each permutation preserves each locus's token multiset and length.

This is an exploratory falsification test, not a decipherment test. The two
transcriptions are alternate readings of the same manuscript, not independent
samples. Overlapping random splits are descriptive and do not yield an ordinary
independent-sample p-value.
"""
from __future__ import annotations
import argparse
import json
import math
import re
from pathlib import Path

class LCG:
    """Small deterministic RNG matching the JS LCG used for the recorded run."""
    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF
    def random(self) -> float:
        self.state = (1664525 * self.state + 1013904223) & 0xFFFFFFFF
        return self.state / 4294967296.0

def fy_shuffle(items, rng: LCG):
    out = list(items)
    for i in range(len(out) - 1, 0, -1):
        j = int(rng.random() * (i + 1))
        out[i], out[j] = out[j], out[i]
    return out

def parse_corpus(path: Path):
    pages = {}
    vocab = set()
    loci = tokens = 0
    locus_re = re.compile(r"^<([^>.]+)\.[^>]*>\s*(.*)$")
    for line in path.read_text(encoding="utf-8").splitlines():
        m = locus_re.match(line)
        if not m:
            continue
        body = re.sub(r"<[^>]*>", " ", m.group(2))
        body = re.sub(r"\[([^\]]+)\]", lambda x: x.group(1).split(":")[0], body)
        body = re.sub(r"\{[^}]*\}", " ", body)
        seq = re.findall(r"[a-z]+", body.lower())
        if not seq:
            continue
        vocab.update(seq)
        pages.setdefault(m.group(1), []).append(seq)
        loci += 1
        tokens += len(seq)
    if not pages:
        raise ValueError(f"No text loci parsed from {path}")
    return {"pages": pages, "vocab": vocab, "loci": loci, "tokens": tokens}

def train_model(sequences, vocab_size: int, alpha: float = 0.1):
    unigram = {}
    bigram = {}
    outgoing = {}
    n = 0
    for seq in sequences:
        for i, token in enumerate(seq):
            unigram[token] = unigram.get(token, 0) + 1
            n += 1
            if i:
                prev = seq[i - 1]
                key = prev + "\x01" + token
                bigram[key] = bigram.get(key, 0) + 1
                outgoing[prev] = outgoing.get(prev, 0) + 1
    return {"unigram": unigram, "bigram": bigram, "outgoing": outgoing,
            "N": n, "V": vocab_size, "alpha": alpha}

def score(sequences, model, permute=False, rng=None):
    loss = unigram_loss = 0.0
    n = 0
    unigram_den = model["N"] + model["alpha"] * model["V"]
    for original in sequences:
        seq = fy_shuffle(original, rng) if permute else original
        prev = None
        for token in seq:
            p_uni = (model["unigram"].get(token, 0) + model["alpha"]) / unigram_den
            p = p_uni
            if prev is not None:
                key = prev + "\x01" + token
                p_bi = (model["bigram"].get(key, 0) + model["alpha"]) / (
                    model["outgoing"].get(prev, 0) + model["alpha"] * model["V"])
                p = 0.5 * p_uni + 0.5 * p_bi
            loss -= math.log2(p)
            unigram_loss -= math.log2(p_uni)
            n += 1
            prev = token
    return {"bits_per_token": loss / n, "unigram_bits_per_token": unigram_loss / n, "n_tokens": n}

def mean(values):
    return sum(values) / len(values)

def sample_sd(values):
    m = mean(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / (len(values) - 1)) if len(values) > 1 else 0.0

def percentile_sorted(values, p):
    return values[int((len(values) - 1) * p)]

def run_experiment(corpus, seed_base, n_splits=20, n_shuffles=50):
    pages = sorted(corpus["pages"])
    deltas = []
    original_losses = []
    shuffled_means = []
    unigram_losses = []
    shuffled_lower_count = 0
    total_shuffles = 0
    unigram_shuffle_differences = []
    shuffle_lower_counts_by_split = []
    test_token_counts = []

    for split_idx in range(n_splits):
        order = fy_shuffle(pages, LCG(seed_base + split_idx * 9973))
        n_train = int(len(order) * 0.7)
        train_pages = set(order[:n_train])
        train, test = [], []
        for page, loci in corpus["pages"].items():
            (train if page in train_pages else test).extend(loci)
        model = train_model(train, len(corpus["vocab"]))
        original = score(test, model)
        shuffled_losses = []
        lower = 0
        for shuffle_idx in range(n_shuffles):
            rng = LCG(seed_base + split_idx * 1000003 + shuffle_idx * 9176 + 31)
            permuted = score(test, model, permute=True, rng=rng)
            shuffled_losses.append(permuted["bits_per_token"])
            if permuted["bits_per_token"] < original["bits_per_token"]:
                lower += 1
            unigram_shuffle_differences.append(abs(permuted["unigram_bits_per_token"] - original["unigram_bits_per_token"]))
        sh_mean = mean(shuffled_losses)
        deltas.append(sh_mean - original["bits_per_token"])
        original_losses.append(original["bits_per_token"])
        shuffled_means.append(sh_mean)
        unigram_losses.append(original["unigram_bits_per_token"])
        shuffled_lower_count += lower
        total_shuffles += n_shuffles
        shuffle_lower_counts_by_split.append(lower)
        test_token_counts.append(original["n_tokens"])

    sorted_deltas = sorted(deltas)
    return {
        "pages_with_loci": len(pages),
        "loci": corpus["loci"],
        "tokens": corpus["tokens"],
        "vocabulary_types": len(corpus["vocab"]),
        "n_splits": n_splits,
        "n_shuffles_per_split": n_shuffles,
        "mean_unigram_bits_per_token": mean(unigram_losses),
        "mean_original_interpolated_bits_per_token": mean(original_losses),
        "mean_shuffled_interpolated_bits_per_token": mean(shuffled_means),
        "mean_delta_shuffled_minus_original_bits_per_token": mean(deltas),
        "sd_delta_across_overlapping_splits": sample_sd(deltas),
        "delta_p10": percentile_sorted(sorted_deltas, 0.10),
        "delta_median": percentile_sorted(sorted_deltas, 0.50),
        "delta_p90": percentile_sorted(sorted_deltas, 0.90),
        "splits_where_original_mean_loss_is_lower": sum(x > 0 for x in deltas),
        "splits_where_shuffle_mean_loss_is_lower": sum(x < 0 for x in deltas),
        "fraction_random_shuffles_with_lower_loss_than_original": shuffled_lower_count / total_shuffles,
        "max_unigram_loss_change_under_shuffle": max(unigram_shuffle_differences, default=0.0),
        "test_tokens_min": min(test_token_counts),
        "test_tokens_max": max(test_token_counts),
        "split_deltas": [round(x, 6) for x in deltas],
        "shuffle_lower_counts_by_split": shuffle_lower_counts_by_split,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zl3b", default="data/transcriptions/eva_zl3b.txt")
    parser.add_argument("--it2a", default="data/transcriptions/eva_it2a.txt")
    parser.add_argument("--splits", type=int, default=20)
    parser.add_argument("--shuffles", type=int, default=50)
    parser.add_argument("--seed-zl3b", type=int, default=623101)
    parser.add_argument("--seed-it2a", type=int, default=623102)
    parser.add_argument("--output", default="results/exp623_shuffle_holdout.json")
    args = parser.parse_args()
    outputs = {}
    for name, filename, seed in (("ZL3b", args.zl3b, args.seed_zl3b), ("IT2a", args.it2a, args.seed_it2a)):
        path = Path(filename)
        corpus = parse_corpus(path)
        outputs[name] = {"source_file": str(path), **run_experiment(corpus, seed, args.splits, args.shuffles)}
    payload = {"experiment": "exp623_word_order_shuffle_holdout", "alpha": 0.1,
               "interpolation_weight_unigram": 0.5, "interpolation_weight_bigram": 0.5,
               "train_fraction": 0.7, "results": outputs}
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(text, end="")
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()