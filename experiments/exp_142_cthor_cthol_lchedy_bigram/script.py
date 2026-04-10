#!/usr/bin/env python3
"""
exp_142: cthor vs cthol positional+bigram analysis (H281)
         lchedy vs cthol bigram equivalence after dialect normalization (H282)
"""

import re
from collections import Counter, defaultdict

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

SECTION_MAP = {}
for f in range(1, 58):    SECTION_MAP[f] = 'herbal'
for f in range(67, 74):   SECTION_MAP[f] = 'astro'
for f in range(75, 85):   SECTION_MAP[f] = 'cosmo'
for f in range(87, 103):  SECTION_MAP[f] = 'pharma'
for f in range(103, 117): SECTION_MAP[f] = 'stars'

ONSET_CLASSES = {
    "qok": re.compile(r'^qok'),
    "qot": re.compile(r'^qot'),
    "qo":  re.compile(r'^qo(?![kt])'),
    "cth": re.compile(r'^cth'),
    "ch":  re.compile(r'^ch(?!e)'),
    "ch_e":re.compile(r'^che'),
    "sh":  re.compile(r'^sh'),
    "ok":  re.compile(r'^ok'),
    "ot":  re.compile(r'^ot'),
    "ol":  re.compile(r'^ol'),
    "d":   re.compile(r'^d'),
    "s":   re.compile(r'^s'),
    "y":   re.compile(r'^y'),
    "k":   re.compile(r'^k'),
    "t":   re.compile(r'^t'),
    "l":   re.compile(r'^l'),
    "r":   re.compile(r'^r'),
    "p":   re.compile(r'^p'),
    "f":   re.compile(r'^f'),
}


def get_onset(word):
    for name, pat in ONSET_CLASSES.items():
        if pat.match(word):
            return name
    return 'other'


def parse_corpus():
    lines = []
    with open(CORPUS, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m:
                continue
            locus_raw, text = m.group(1), m.group(2).strip()
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_str = parts[0]
            locus_type_raw = parts[1]
            locus_type = locus_type_raw.lstrip('@+*=~&')
            if not re.match(r'P', locus_type):
                continue
            folio_base = folio_str.split('.')[0]
            m2 = re.match(r'f(\d+)', folio_base)
            if not m2:
                continue
            folio_num = int(m2.group(1))
            section = SECTION_MAP.get(folio_num)
            if section is None:
                continue
            words = [w for w in text.split('.') if re.match(r'[a-z]', w)]
            if not words:
                continue
            lines.append({'folio_base': folio_base, 'folio_num': folio_num,
                          'section': section, 'words': words})
    return lines


def get_folio_dialect(lines):
    folio_counts = defaultdict(lambda: {'edy': 0, 'eedy': 0, 'total': 0})
    for rec in lines:
        fb = rec['folio_base']
        for w in rec['words']:
            folio_counts[fb]['total'] += 1
            if w.endswith('eedy'): folio_counts[fb]['eedy'] += 1
            elif w.endswith('edy'): folio_counts[fb]['edy'] += 1
    dialect = {}
    for fb, cnts in folio_counts.items():
        if cnts['total'] < 10:
            dialect[fb] = 'unknown'
        else:
            rate = (cnts['edy'] + cnts['eedy']) / cnts['total']
            dialect[fb] = 'B' if rate >= 0.05 else 'A'
    return dialect


def positional_slot(i, n):
    if n == 1: return 'only'
    if i == 0: return 'LF'
    if i == n - 1: return 'LL'
    return 'MID'


def analyze_cthor_cthol(lines, folio_dialect):
    """H281: cthor vs cthol positional and bigram analysis."""
    print("="*60)
    print("H281: cthor vs cthol — POSITIONAL AND BIGRAM ANALYSIS")
    print("="*60)

    # Collect bigrams and positions for cthor and cthol separately
    cthor_pos = Counter()
    cthol_pos = Counter()
    cthor_before = Counter(); cthor_after = Counter()
    cthol_before = Counter(); cthol_after = Counter()
    cthor_by_pos = defaultdict(Counter)  # pos -> what follows cthor
    cthol_by_pos = defaultdict(Counter)  # pos -> what follows cthol
    # Separate LF vs non-LF contexts for cthor
    cthor_lf_after = Counter()
    cthor_mid_after = Counter()

    n_cthor = 0; n_cthol = 0

    for rec in lines:
        fb = rec['folio_base']
        d = folio_dialect.get(fb, 'unknown')
        if d != 'A':
            continue
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            slot = positional_slot(i, n)
            if w == 'cthor':
                cthor_pos[slot] += 1
                n_cthor += 1
                if i > 0: cthor_before[get_onset(words[i-1])] += 1
                if i < n-1:
                    nxt = get_onset(words[i+1])
                    cthor_after[nxt] += 1
                    cthor_by_pos[slot][nxt] += 1
                    if slot == 'LF':
                        cthor_lf_after[nxt] += 1
                    else:
                        cthor_mid_after[nxt] += 1
            elif w == 'cthol':
                cthol_pos[slot] += 1
                n_cthol += 1
                if i > 0: cthol_before[get_onset(words[i-1])] += 1
                if i < n-1:
                    nxt = get_onset(words[i+1])
                    cthol_after[nxt] += 1
                    cthol_by_pos[slot][nxt] += 1

    # Compute A-dialect onset baseline
    a_onset_baseline = Counter()
    a_total = 0
    for rec in lines:
        fb = rec['folio_base']
        if folio_dialect.get(fb) == 'A':
            for w in rec['words']:
                a_onset_baseline[get_onset(w)] += 1
                a_total += 1

    print(f"\ncthor total: {n_cthor}, cthol total: {n_cthol}")

    # Positional comparison
    print(f"\n--- Positional distribution ---")
    print(f"{'Slot':8s}  {'cthor%':8s}  {'cthol%':8s}")
    for slot in ['LF','MID','LL','only']:
        r_cthor = cthor_pos.get(slot,0)/n_cthor if n_cthor > 0 else 0
        r_cthol = cthol_pos.get(slot,0)/n_cthol if n_cthol > 0 else 0
        print(f"  {slot:8s}  {r_cthor:.1%}   {r_cthol:.1%}")

    # Bigram context before cthor vs cthol
    print(f"\n--- What onset PRECEDES cthor vs cthol? (raw% and enrichment vs A baseline) ---")
    print(f"{'Onset':10s}  {'before_cthor':14s}  {'enr':6s}  {'before_cthol':14s}  {'enr':6s}")
    t_bcthor = sum(cthor_before.values()); t_bcthol = sum(cthol_before.values())
    all_onsets = set(list(cthor_before.keys()) + list(cthol_before.keys()))
    for onset in sorted(all_onsets, key=lambda o: -(cthor_before.get(o,0)/t_bcthor if t_bcthor>0 else 0)):
        if cthor_before.get(onset,0) < 2 and cthol_before.get(onset,0) < 2: continue
        r_cthor = cthor_before.get(onset,0)/t_bcthor if t_bcthor > 0 else 0
        r_cthol = cthol_before.get(onset,0)/t_bcthol if t_bcthol > 0 else 0
        base = a_onset_baseline.get(onset,0)/a_total if a_total > 0 else 0
        enr_cthor = f"{r_cthor/base:.2f}×" if base > 0 else "inf"
        enr_cthol = f"{r_cthol/base:.2f}×" if base > 0 else "inf"
        print(f"  {onset:10s}  {r_cthor:.1%} ({cthor_before.get(onset,0):3d})  {enr_cthor:6s}  {r_cthol:.1%} ({cthol_before.get(onset,0):3d})  {enr_cthol:6s}")

    # What follows cthor at LF vs MID
    print(f"\n--- What follows cthor at LF vs MID positions? ---")
    t_lf = sum(cthor_lf_after.values()); t_mid = sum(cthor_mid_after.values())
    print(f"  cthor at LF (n={t_lf} following words):")
    for onset, c in cthor_lf_after.most_common(8):
        base = a_onset_baseline.get(onset,0)/a_total if a_total > 0 else 0
        r = c/t_lf; enr = f"{r/base:.2f}×" if base > 0 else "inf"
        print(f"    {onset:10s}  {r:.1%} ({c})  {enr}")
    print(f"  cthor at MID (n={t_mid} following words):")
    for onset, c in cthor_mid_after.most_common(8):
        base = a_onset_baseline.get(onset,0)/a_total if a_total > 0 else 0
        r = c/t_mid; enr = f"{r/base:.2f}×" if base > 0 else "inf"
        print(f"    {onset:10s}  {r:.1%} ({c})  {enr}")


def analyze_lchedy_cthol_normalized(lines, folio_dialect):
    """H282: lchedy vs cthol bigram context after dialect normalization."""
    print("\n" + "="*60)
    print("H282: lchedy vs cthol — DIALECT-NORMALIZED BIGRAM CONTEXT")
    print("="*60)

    lchedy_before = Counter(); lchedy_after = Counter()
    cthol_before = Counter(); cthol_after = Counter()
    n_lchedy = 0; n_cthol = 0

    # Dialect onset baselines
    a_baseline = Counter(); a_total = 0
    b_baseline = Counter(); b_total = 0

    for rec in lines:
        fb = rec['folio_base']
        d = folio_dialect.get(fb, 'unknown')
        words = rec['words']
        n = len(words)

        for w in words:
            onset = get_onset(w)
            if d == 'A':
                a_baseline[onset] += 1; a_total += 1
            elif d == 'B':
                b_baseline[onset] += 1; b_total += 1

        for i, w in enumerate(words):
            if d == 'A' and w == 'cthol':
                n_cthol += 1
                if i > 0: cthol_before[get_onset(words[i-1])] += 1
                if i < n-1: cthol_after[get_onset(words[i+1])] += 1
            elif d == 'B' and w == 'lchedy':
                n_lchedy += 1
                if i > 0: lchedy_before[get_onset(words[i-1])] += 1
                if i < n-1: lchedy_after[get_onset(words[i+1])] += 1

    print(f"\ncthol in A-dialect: {n_cthol} tokens")
    print(f"lchedy in B-dialect: {n_lchedy} tokens")

    # Normalized enrichment comparison
    print(f"\n--- Bigram BEFORE: enrichment vs respective dialect baseline ---")
    print(f"{'Onset':10s}  {'cthol_raw':10s}  {'cthol_enr':10s}  {'lchedy_raw':10s}  {'lchedy_enr':10s}")
    t_cthol_b = sum(cthol_before.values()); t_lchedy_b = sum(lchedy_before.values())
    all_onsets = set(list(cthol_before.keys()) + list(lchedy_before.keys()))
    for onset in sorted(all_onsets, key=lambda o: -(cthol_before.get(o,0)/t_cthol_b if t_cthol_b>0 else 0)):
        if cthol_before.get(onset,0) < 2 and lchedy_before.get(onset,0) < 2: continue
        r_c = cthol_before.get(onset,0)/t_cthol_b if t_cthol_b > 0 else 0
        r_l = lchedy_before.get(onset,0)/t_lchedy_b if t_lchedy_b > 0 else 0
        base_a = a_baseline.get(onset,0)/a_total if a_total > 0 else 0
        base_b = b_baseline.get(onset,0)/b_total if b_total > 0 else 0
        enr_c = f"{r_c/base_a:.2f}×" if base_a > 0 else "inf"
        enr_l = f"{r_l/base_b:.2f}×" if base_b > 0 else "inf"
        print(f"  {onset:10s}  {r_c:.1%} ({cthol_before.get(onset,0):3d})  {enr_c:10s}  {r_l:.1%} ({lchedy_before.get(onset,0):3d})  {enr_l:10s}")

    print(f"\n--- Bigram AFTER: enrichment vs respective dialect baseline ---")
    print(f"{'Onset':10s}  {'cthol_raw':10s}  {'cthol_enr':10s}  {'lchedy_raw':10s}  {'lchedy_enr':10s}")
    t_cthol_a = sum(cthol_after.values()); t_lchedy_a = sum(lchedy_after.values())
    all_onsets_a = set(list(cthol_after.keys()) + list(lchedy_after.keys()))
    for onset in sorted(all_onsets_a, key=lambda o: -(cthol_after.get(o,0)/t_cthol_a if t_cthol_a>0 else 0)):
        if cthol_after.get(onset,0) < 2 and lchedy_after.get(onset,0) < 2: continue
        r_c = cthol_after.get(onset,0)/t_cthol_a if t_cthol_a > 0 else 0
        r_l = lchedy_after.get(onset,0)/t_lchedy_a if t_lchedy_a > 0 else 0
        base_a = a_baseline.get(onset,0)/a_total if a_total > 0 else 0
        base_b = b_baseline.get(onset,0)/b_total if b_total > 0 else 0
        enr_c = f"{r_c/base_a:.2f}×" if base_a > 0 else "inf"
        enr_l = f"{r_l/base_b:.2f}×" if base_b > 0 else "inf"
        print(f"  {onset:10s}  {r_c:.1%} ({cthol_after.get(onset,0):3d})  {enr_c:10s}  {r_l:.1%} ({lchedy_after.get(onset,0):3d})  {enr_l:10s}")

    # Summary: top enriched onsets before each word
    print(f"\n--- Summary: top enriched onsets BEFORE cthol (A) vs BEFORE lchedy (B) ---")
    print(f"  cthol: " + ", ".join(
        f"{o}({cthol_before.get(o,0)/t_cthol_b:.1%}, {(cthol_before.get(o,0)/t_cthol_b)/(a_baseline.get(o,1)/a_total):.1f}×)"
        for o in sorted(cthol_before, key=lambda o: -cthol_before.get(o,0)/t_cthol_b)[:5]
        if t_cthol_b > 0
    ))
    print(f"  lchedy: " + ", ".join(
        f"{o}({lchedy_before.get(o,0)/t_lchedy_b:.1%}, {(lchedy_before.get(o,0)/t_lchedy_b)/(b_baseline.get(o,1)/b_total):.1f}×)"
        for o in sorted(lchedy_before, key=lambda o: -lchedy_before.get(o,0)/t_lchedy_b)[:5]
        if t_lchedy_b > 0
    ))

    print(f"\n--- Summary: top enriched onsets AFTER cthol (A) vs AFTER lchedy (B) ---")
    print(f"  cthol: " + ", ".join(
        f"{o}({cthol_after.get(o,0)/t_cthol_a:.1%}, {(cthol_after.get(o,0)/t_cthol_a)/(a_baseline.get(o,1)/a_total):.1f}×)"
        for o in sorted(cthol_after, key=lambda o: -cthol_after.get(o,0)/t_cthol_a)[:5]
        if t_cthol_a > 0
    ))
    print(f"  lchedy: " + ", ".join(
        f"{o}({lchedy_after.get(o,0)/t_lchedy_a:.1%}, {(lchedy_after.get(o,0)/t_lchedy_a)/(b_baseline.get(o,1)/b_total):.1f}×)"
        for o in sorted(lchedy_after, key=lambda o: -lchedy_after.get(o,0)/t_lchedy_a)[:5]
        if t_lchedy_a > 0
    ))


if __name__ == '__main__':
    print("Loading corpus...")
    lines = parse_corpus()
    print(f"Loaded {len(lines)} lines")
    folio_dialect = get_folio_dialect(lines)
    analyze_cthor_cthol(lines, folio_dialect)
    analyze_lchedy_cthol_normalized(lines, folio_dialect)
