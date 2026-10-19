#!/usr/bin/env python3
"""Section-stratified robustness check for exp_589, using no external API."""
from __future__ import annotations
import argparse, collections, hashlib, json, random, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data/transcriptions/eva_zl3b.txt"

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def clean_words(text):
    text = re.sub(r"<!.*?>", " ", text)
    text = re.sub(r"<[^>]*>", " ", text).replace("<$>", " ").replace("<%>", " ")
    text = re.sub(r"\[([^:\]]+):[^\]]*\]", r"\1", text)
    text = re.sub(r"\{[^}]*\}", " ", text)
    text = re.sub(r"@\d+;?", " ", text)
    return [w.lower() for w in re.split(r"[.\s,]+", text) if re.fullmatch(r"[A-Za-z]+", w)]

def folio_range_proxy(folio):
    # Coarse folio-number bins inherited from exp_004; these are not definitive
    # codicological section labels. The aim is sensitivity analysis, not relabeling.
    m = re.match(r"^f(\d+)", folio)
    if not m: return "unknown"
    n = int(m.group(1))
    if n <= 66: return "f001_f066"
    if n <= 73: return "f067_f073"
    if n <= 84: return "f074_f084"
    if n <= 102: return "f085_f102"
    if n <= 116: return "f103_f116"
    return "other"

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
        locus = m.group(1).split(",", 1)[1]
        if not re.match(r"^[+*@]?P", locus): continue
        ws = clean_words(m.group(2))
        if len(ws) < 2: continue
        rows.append({"folio": folio, "currier": currier, "range": folio_range_proxy(folio),
                     "locus": re.sub(r"^[+*@]", "", locus), "words": ws})
    return rows

def analyze(rows, n_perm, seed):
    target = "daiin"
    eligible = [r for r in rows if len(r["words"]) >= 2]
    expected = sum(r["words"].count(target) / len(r["words"]) for r in eligible)
    observed = sum(r["words"][0] == target for r in eligible)
    target_total = sum(r["words"].count(target) for r in eligible)
    out = {"lines": len(eligible), "daiin_tokens": target_total, "first_observed": observed,
           "first_expected": round(expected, 4), "first_enrichment": round(observed/expected, 5) if expected else None,
           "last_observed": sum(r["words"][-1] == target for r in eligible),
           "last_expected_under_exchangeability": round(expected, 4)}
    if len(eligible) < 50:
        out["permutation_status"] = "descriptive_only_fewer_than_50_lines"
        return out
    rng, ge, null_sum = random.Random(seed), 0, 0
    for _ in range(n_perm):
        count = sum(r["words"][rng.randrange(len(r["words"]))] == target for r in eligible)
        null_sum += count
        ge += count >= observed
    out.update({"null_mean": round(null_sum/n_perm, 4),
                "p_one_sided_plus_one": round((ge+1)/(n_perm+1), 6),
                "permutations": n_perm, "seed": seed})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--permutations", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=59020261019)
    args = ap.parse_args()
    if args.permutations < 99: ap.error("--permutations must be >=99")
    rows = parse(CORPUS)
    ranges = sorted({r["range"] for r in rows})
    strata = {}
    for ri, range_name in enumerate(ranges):
        for ci, currier in enumerate(("A", "B")):
            key = f"{range_name}_Currier{currier}"
            group = [r for r in rows if r["range"] == range_name and r["currier"] == currier]
            if group:
                strata[key] = analyze(group, args.permutations, args.seed + ri*10 + ci)
    # Holm correction for the predeclared primary family: all eligible Currier-B
    # folio-range strata. Currier-A ranges are secondary and corrected separately.
    def holm_adjust(pvalues):
        ordered = sorted(pvalues.items(), key=lambda item: item[1])
        adjusted, running = {}, 0.0
        m = len(ordered)
        for rank, (key, pvalue) in enumerate(ordered):
            running = max(running, min(1.0, (m-rank) * pvalue))
            adjusted[key] = round(running, 6)
        return adjusted

    b_p = {k: v["p_one_sided_plus_one"] for k, v in strata.items()
           if k.endswith("_CurrierB") and "p_one_sided_plus_one" in v}
    a_p = {k: v["p_one_sided_plus_one"] for k, v in strata.items()
           if k.endswith("_CurrierA") and "p_one_sided_plus_one" in v}
    for key, value in holm_adjust(b_p).items():
        strata[key]["p_holm_primary_currier_B_family"] = value
    for key, value in holm_adjust(a_p).items():
        strata[key]["p_holm_secondary_currier_A_family"] = value

    # Exact locus subtypes are descriptive; section bins are coarse proxies.
    locus_counts = collections.Counter(r["locus"] for r in rows)
    data = {"experiment": "exp_590_daiin_section_stratification", "protocol_version": 1,
            "source": {"path": "data/transcriptions/eva_zl3b.txt", "bytes": CORPUS.stat().st_size, "sha256": digest(CORPUS)},
            "parser": {"body_locus_regex": "^[+*@]?P", "min_words_per_line": 2,
                       "range_bins_are_coarse_proxies_not_definitive_sections": True},
            "total_body_lines_ge2_tokens": sum(len(r["words"]) >= 2 for r in rows),
            "locus_counts": dict(sorted(locus_counts.items())),
            "strata": strata,
            "notes": ["This is a sensitivity analysis of exp_589, not an independent transcription replication.",
                      "Within-line position draws preserve each line's token composition and length.",
                      "Monte Carlo p-values at 0.0005 are resolution-limited with 2,000 replicates.",
                      "Primary Currier-B folio-range p-values are Holm-adjusted across five strata; Currier-A is a separately adjusted secondary family.",
                      "Section bin labels are heuristic folio-number ranges; do not interpret them as scholarly section adjudications.",
                      "Do not infer semantics or decipherment from positional distributions."]}
    out = ROOT / "experiments/exp_590_daiin_section_stratification/results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({"output": str(out.relative_to(ROOT)), "strata": strata}, indent=2))

if __name__ == "__main__": main()
