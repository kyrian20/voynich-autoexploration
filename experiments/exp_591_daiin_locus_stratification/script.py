#!/usr/bin/env python3
"""Exact IVTFF-locus subtype audit for the daiin line-initial effect."""
from __future__ import annotations
import argparse, collections, hashlib, json, random, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data/transcriptions/eva_zl3b.txt"

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""): h.update(block)
    return h.hexdigest()

def clean_words(text):
    text = re.sub(r"<!.*?>", " ", text)
    text = re.sub(r"<[^>]*>", " ", text).replace("<$>", " ").replace("<%>", " ")
    text = re.sub(r"\[([^:\]]+):[^\]]*\]", r"\1", text)
    text = re.sub(r"\{[^}]*\}", " ", text)
    text = re.sub(r"@\d+;?", " ", text)
    return [w.lower() for w in re.split(r"[.\s,]+", text) if re.fullmatch(r"[A-Za-z]+", w)]

def parse(path):
    rows, folio, currier = [], "unknown", "unknown"
    for raw in path.read_text(encoding="latin-1").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"): continue
        if re.match(r"^<f\w+>.*\$", line):
            m = re.match(r"^<(f\w+)>", line)
            if m: folio = m.group(1)
            m = re.search(r"\$L=([AB])", line)
            if m: currier = m.group(1)
            continue
        m = re.match(r"^<([^>]+)>\s+(.*)$", line)
        if not m or "," not in m.group(1): continue
        locus_raw = m.group(1).split(",", 1)[1]
        if not re.match(r"^[+*@]?P", locus_raw): continue
        locus = re.sub(r"^[+*@]", "", locus_raw)
        words = clean_words(m.group(2))
        if len(words) < 2: continue
        rows.append({"folio": folio, "currier": currier, "locus": locus, "words": words})
    return rows

def analyze(rows, n_perm, seed):
    eligible = [r for r in rows if len(r["words"]) >= 2]
    expected = sum(r["words"].count("daiin") / len(r["words"]) for r in eligible)
    observed = sum(r["words"][0] == "daiin" for r in eligible)
    target_count = sum(r["words"].count("daiin") for r in eligible)
    out = {"lines": len(eligible), "daiin_tokens": target_count, "first_observed": observed,
           "first_expected": round(expected, 4),
           "first_enrichment": round(observed / expected, 5) if expected else None,
           "last_observed": sum(r["words"][-1] == "daiin" for r in eligible),
           "last_expected_under_exchangeability": round(expected, 4)}
    if len(eligible) < 50:
        out["status"] = "descriptive_only_fewer_than_50_lines"
        return out
    rng, ge, null_sum = random.Random(seed), 0, 0
    for _ in range(n_perm):
        # For the first-position count, choosing one uniform token per line is
        # exactly distribution-equivalent to shuffling every line.
        count = sum(r["words"][rng.randrange(len(r["words"]))] == "daiin" for r in eligible)
        null_sum += count
        ge += count >= observed
    out.update({"null_mean": round(null_sum / n_perm, 4),
                "p_one_sided_plus_one": round((ge + 1) / (n_perm + 1), 6),
                "permutations": n_perm, "seed": seed})
    return out

def holm_adjust(pvalues):
    ordered = sorted(pvalues.items(), key=lambda item: item[1])
    adjusted, running = {}, 0.0
    for rank, (key, pvalue) in enumerate(ordered):
        running = max(running, min(1.0, (len(ordered) - rank) * pvalue))
        adjusted[key] = round(running, 6)
    return adjusted

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--permutations", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=59120261019)
    args = ap.parse_args()
    if args.permutations < 99: ap.error("--permutations must be >=99")
    rows = parse(CORPUS)
    loci = sorted({r["locus"] for r in rows})
    strata = {}
    for li, locus in enumerate(loci):
        for di, dialect in enumerate(("A", "B")):
            group = [r for r in rows if r["locus"] == locus and r["currier"] == dialect]
            if group:
                key = f"{dialect}_{locus}"
                strata[key] = analyze(group, args.permutations, args.seed + li*10 + di)
    b_p = {k: v["p_one_sided_plus_one"] for k, v in strata.items()
           if k.startswith("B_") and "p_one_sided_plus_one" in v}
    a_p = {k: v["p_one_sided_plus_one"] for k, v in strata.items()
           if k.startswith("A_") and "p_one_sided_plus_one" in v}
    for key, value in holm_adjust(b_p).items():
        strata[key]["p_holm_primary_currier_B_locus_family"] = value
    for key, value in holm_adjust(a_p).items():
        strata[key]["p_holm_secondary_currier_A_locus_family"] = value
    data = {
        "experiment": "exp_591_daiin_locus_stratification",
        "protocol_version": 1,
        "source": {"path": "data/transcriptions/eva_zl3b.txt", "bytes": CORPUS.stat().st_size, "sha256": digest(CORPUS)},
        "parser": {"body_locus_regex": "^[+*@]?P", "minimum_words_per_line": 2,
                   "locus_codes_kept_verbatim_after_prefix_removal": loci},
        "all_body_lines_ge2_tokens": len(rows),
        "locus_token_counts": dict(sorted(collections.Counter(r["locus"] for r in rows).items())),
        "strata": strata,
        "notes": [
            "Follow-up sensitivity analysis of exp_589; ZL3b only, not an independent transcription replication.",
            "Primary family: eligible Currier-B locus subtypes, Holm-adjusted among all B strata with at least 50 lines.",
            "Currier-A locus subtypes form a separately adjusted secondary family.",
            "Locus codes are reported verbatim; no grammatical interpretation is assigned.",
            "Monte Carlo p=0.0005 is the resolution floor for 2,000 replicates.",
            "This is a position-only analysis and does not decipher the manuscript."
        ]
    }
    out = ROOT / "experiments/exp_591_daiin_locus_stratification/results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out.relative_to(ROOT)), "strata": strata}, indent=2))

if __name__ == "__main__": main()
