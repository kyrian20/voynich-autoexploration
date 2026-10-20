#!/usr/bin/env python3
"""EXP-623: replicate the ch/sh context-specificity interaction in IT2a transcription.

Uses IVTFF text rows from ZL3b. Matched strata are folio × token length ×
digraph character position, and only strata containing both ch and sh are kept.
Primary statistic: within-stratum (sh−ch) vowel-rate difference after the
digraph minus the same difference before it. A within-stratum permutation
shuffles ch/sh labels, preserving each stratum's label counts.
"""
from __future__ import annotations
import collections, hashlib, json, random, re
from pathlib import Path

SOURCE = Path("data/transcriptions/eva_it2a.txt")
OUT = Path("research/experiments/exp_623_it2a_ch_sh_specificity_replication")
VOWELS = set("aeiouy")
ROW = re.compile(r"^<f(\d+[rv])\.\d+[^>]*>\s*(.*)$")
DIGRAPH = re.compile(r"ch|sh")

def parse():
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8-sig")
    rows = []
    for line in text.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        folio, body = m.groups()
        # Remove transcription/editorial markup rather than treating it as EVA.
        body = re.sub(r"<[^>]*>|\[[^\]]*\]|\{[^}]*\}|@[0-9]+;", " ", body)
        body = body.replace("%", " ").replace("$", " ")
        for token in re.findall(r"[A-Za-z]+", body.lower()):
            for hit in DIGRAPH.finditer(token):
                start, end = hit.span()
                if start == 0 or end >= len(token):
                    continue
                rows.append({
                    "folio": folio, "length": len(token), "position": start,
                    "label": hit.group(), "prev_vowel": token[start-1] in VOWELS,
                    "next_vowel": token[end] in VOWELS,
                })
    return raw, rows

def interaction(records):
    cells = collections.defaultdict(list)
    for r in records:
        cells[(r["folio"], r["length"], r["position"])].append(r)
    contrasts = []
    for cell in cells.values():
        ch = [r for r in cell if r["label"] == "ch"]
        sh = [r for r in cell if r["label"] == "sh"]
        if not ch or not sh:
            continue
        next_diff = sum(r["next_vowel"] for r in sh)/len(sh) - sum(r["next_vowel"] for r in ch)/len(ch)
        prev_diff = sum(r["prev_vowel"] for r in sh)/len(sh) - sum(r["prev_vowel"] for r in ch)/len(ch)
        contrasts.append((cell, next_diff - prev_diff, next_diff, prev_diff))
    return contrasts

def main():
    raw, records = parse()
    contrasts = interaction(records)
    if len(contrasts) < 10:
        raise SystemExit(f"Too few matched strata: {len(contrasts)}")
    observed = sum(x[1] for x in contrasts) / len(contrasts)
    rng = random.Random(6232026)
    B = 10000
    exceed = 0
    for _ in range(B):
        shuffled = []
        for cell, *_ in contrasts:
            labels = [r["label"] for r in cell]
            rng.shuffle(labels)
            for r, label in zip(cell, labels):
                shuffled.append({**r, "label": label})
        stat_cells = interaction(shuffled)
        stat = sum(x[1] for x in stat_cells) / len(stat_cells) if stat_cells else 0.0
        if abs(stat) >= abs(observed):
            exceed += 1
    p = (exceed + 1) / (B + 1)
    summary = {
        "experiment": 623,
        "title": "IT2a replication of ch/sh following-vs-preceding vowel specificity interaction",
        "source": str(SOURCE),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "parser": "IVTFF text rows; strip angle, square-bracket and brace annotations; alphabetic tokenization; only ch/sh occurrences with both adjacent characters",
        "vowels": sorted(VOWELS),
        "occurrences_with_two_neighbors": len(records),
        "matched_strata": len(contrasts),
        "folios_in_matched_strata": len({r["folio"] for c, *_ in contrasts for r in c}),
        "mean_matched_stratum_next_sh_minus_ch": sum(x[2] for x in contrasts)/len(contrasts),
        "mean_matched_stratum_prev_sh_minus_ch": sum(x[3] for x in contrasts)/len(contrasts),
        "interaction_next_minus_prev": observed,
        "permutation_replicates": B,
        "two_sided_permutation_p": p,
        "permutation_exceedances": exceed,
        "interpretation": "A positive interaction would support greater ch/sh separation after than before the digraph under this matched-cell null; a null result would weaken outcome-specific claims. This is exploratory and not a decipherment result.",
        "limitations": [
            "ZL3b is one transcription, not an independent manuscript.",
            "The parser is deliberately simple and needs independent parser conformance testing.",
            "Matching by observed token length and position does not eliminate all lexical-template confounding.",
            "This test was motivated by earlier exploratory results and is not preregistered."
        ]
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md = f"""# EXP-623 — IT2a replication of ch/sh context-specificity interaction

## Question
Is the observed ch/sh vowel-rate contrast larger for the character after the digraph than for the character before it, after matching folio, exact token length, and digraph position?

## Method
Source: `{SOURCE}` (SHA-256 `{summary['source_sha256']}`). A simple parser extracts text rows and alphabetic tokens, then retains ch/sh occurrences with a character on both sides. Matched strata contain both digraphs. The statistic is the equally weighted mean across strata of [(sh−ch) following-vowel rate] − [(sh−ch) preceding-vowel rate]. The two-sided permutation test shuffles ch/sh labels within strata for {B:,} replicates, preserving the label count per stratum.

## Results
- Occurrences with both neighbors: {len(records):,}
- Matched strata: {len(contrasts):,}
- Folios represented: {summary['folios_in_matched_strata']}
- Mean following-character contrast (sh−ch): {summary['mean_matched_stratum_next_sh_minus_ch']*100:.2f} percentage points
- Mean preceding-character contrast (sh−ch): {summary['mean_matched_stratum_prev_sh_minus_ch']*100:.2f} percentage points
- Interaction (following minus preceding): {observed*100:.2f} percentage points
- Two-sided permutation p: {p:.5f} ({exceed} exceedances / {B:,})

## Interpretation and limits
This is a transcription-sensitivity replication of the diagnostic specificity test motivated by EXP-619, where the preceding-character control was not uniformly smaller than the primary contrast. A positive interaction supports a larger contrast after than before the digraph under this null; a non-positive or uncertain result does not support an outcome-specific claim. This remains exploratory, not a phonetic, semantic, language-identification, or decipherment result. ZL3b and IT2a are alternative transcriptions of the same manuscript; this experiment uses ZL3b only. The simple parser and the conditioning strategy leave possible lexical-template confounding.

See `results.json` for machine-readable details.
"""
    (OUT / "result.md").write_text(md, encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
