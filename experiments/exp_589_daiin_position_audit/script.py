#!/usr/bin/env python3
"""API-free, reproducible positional audit for EVA daiin in IVTFF files."""
from __future__ import annotations
import argparse, collections, hashlib, json, random, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = [("ZL3b", ROOT / "data/transcriptions/eva_zl3b.txt"),
         ("ZL3a", ROOT / "data/transcriptions/zl3a.txt")]
CONTROLS = ("aiin", "chedy", "dain", "saiin", "qokaiin")

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def clean_words(text):
    text = re.sub(r"<!.*?>", " ", text)
    text = re.sub(r"<[^>]*>", " ", text).replace("<%>", " ").replace("<$>", " ")
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
        if not m: continue
        locus_and_line, body = m.group(1), m.group(2)
        if "," not in locus_and_line: continue
        locus = locus_and_line.split(",", 1)[1]
        words = clean_words(body)
        if not words: continue
        rows.append({"folio": folio, "currier": currier, "locus": locus, "words": words,
                     "is_body": bool(re.match(r"^[+*@]?P", locus))})
    return rows

def permutation_test(lines, target, n_perm, seed):
    eligible = [list(line) for line in lines if len(line) >= 2]
    observed = sum(line[0] == target for line in eligible)
    if not eligible:
        return {"eligible_lines": 0, "observed_first": 0, "p_one_sided_plus_one": None}
    rng, null, ge = random.Random(seed), [], 0
    for _ in range(n_perm):
        # For this statistic, a single uniform position per line has the same
        # null distribution as a full shuffle, without shuffling every token.
        count = 0
        for line in eligible:
            count += line[rng.randrange(len(line))] == target
        null.append(count)
        ge += count >= observed
    expected = sum(line.count(target) / len(line) for line in eligible)
    return {
        "eligible_lines": len(eligible),
        "eligible_tokens": sum(map(len, eligible)),
        "observed_first": observed,
        "observed_last": sum(line[-1] == target for line in eligible),
        "target_tokens_in_eligible_lines": sum(line.count(target) for line in eligible),
        "expected_first_under_exchangeability": round(expected, 4),
        "null_mean_simulated": round(sum(null) / n_perm, 4),
        "enrichment_observed_vs_expected": round(observed / expected, 5) if expected else None,
        "p_one_sided_plus_one": round((ge + 1) / (n_perm + 1), 6),
        "permutations": n_perm, "seed": seed
    }

def summarize(path, label, n_perm, seed):
    rows = parse(path)
    body = [r for r in rows if r["is_body"]]
    groups = {
        "body_all": [r["words"] for r in body],
        "body_currier_A": [r["words"] for r in body if r["currier"] == "A"],
        "body_currier_B": [r["words"] for r in body if r["currier"] == "B"],
    }
    counts = collections.Counter(w for r in body for w in r["words"])
    total = sum(counts.values())
    return {
        "transcription": label, "path": str(path.relative_to(ROOT)), "file_bytes": path.stat().st_size,
        "sha256": sha256(path), "parsed_line_records": len(rows), "body_lines": len(body),
        "body_tokens": total, "daiin_tokens_body": counts["daiin"],
        "daiin_rate_per_10000_tokens": round(10000 * counts["daiin"] / total, 4) if total else None,
        "control_counts_body": {w: counts[w] for w in CONTROLS},
        "position_tests": {name: permutation_test(lines, "daiin", n_perm, seed + i)
                           for i, (name, lines) in enumerate(groups.items())}
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--permutations", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=58920261019)
    args = ap.parse_args()
    if args.permutations < 99: ap.error("--permutations must be >= 99")
    results = []
    for i, (name, path) in enumerate(FILES):
        results.append(summarize(path, name, args.permutations, args.seed + i*100)
                       if path.exists() else {"transcription": name, "missing_file": str(path.relative_to(ROOT))})
    out = ROOT / "experiments/exp_589_daiin_position_audit/results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    data = {"experiment": "exp_589_daiin_position_audit", "protocol_version": 1,
            "notes": ["Exploratory positional audit; no semantic claim.",
                      "Within-line permutations preserve line composition and length.",
                      "The single preregistered target is daiin; controls are descriptive.",
                      "Parser and cleanup rules define the operational corpus."],
            "results": results}
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({"output": str(out.relative_to(ROOT)), "results": results}, indent=2))

if __name__ == "__main__": main()
