"""
exp_292: Cross-Position Word Identity vs Onset-Class Overlap — H496
How much of the LF/MID/LL vocabulary overlap is:
(a) Identical word types appearing at multiple positions
(b) Different word types from the same onset class

This disambiguates whether positional grammar operates at the WORD level
(specific words belong to specific positions) or the ONSET-CLASS level
(any word from the right onset class can fill any position in that class's allowed range).

Data: eva_zl3b.txt
"""

import os, re
import numpy as np
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
ZL3B_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv][12]?$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_with_position(path, min_len=3, max_len=15):
    """Parse ZL3b with line-position tags."""
    eva_ok = re.compile(r'^[a-z]+$')
    folio_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio = m.group(1).lstrip('+*=&~')
            fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s,]', text)
                     if eva_ok.match(w) and min_len <= len(w) <= max_len]
            for w in words:
                folio_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_stats[fb]['edy'] += 1
    folio_dialect = {fb: classify_dialect(s) for fb, s in folio_stats.items()}

    tokens = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio = m.group(1).lstrip('+*=&~')
            lc = m.group(3).lstrip('+*=/~&@')
            if not lc.startswith('P'): continue
            fb = folio_base(folio)
            dial = folio_dialect.get(fb, 'unknown')
            if dial not in ('A', 'B'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s,]', text)
                     if eva_ok.match(w) and min_len <= len(w) <= max_len]
            if not words: continue
            n = len(words)
            for idx, w in enumerate(words):
                if n == 1: pos = 'LL'
                elif idx == 0: pos = 'LF'
                elif idx == n - 1: pos = 'LL'
                else: pos = 'MID'
                tokens.append((w, dial, pos))
    return tokens

def overlap_analysis(tokens, dial_filter, label):
    """
    For a given dialect, compute:
    1. Word type sets per position (LF, MID, LL)
    2. Type-level overlap between positions
    3. For overlapping words: how many are from the same onset class vs identical word?
    4. Onset-class level overlap (if onset class appears at both positions)
    """
    # Filter to dialect
    toks = [(w, p) for w, d, p in tokens if d == dial_filter]
    n_total = len(toks)

    # Word type sets by position
    pos_types = defaultdict(set)
    pos_counts = defaultdict(Counter)
    pos_onset_counts = defaultdict(Counter)
    for w, p in toks:
        pos_types[p].add(w)
        pos_counts[p][w] += 1
        pos_onset_counts[p][get_onset(w)] += 1

    print(f"\n=== {label} ===")
    for pos in ['LF', 'MID', 'LL']:
        types = pos_types[pos]
        n_tok = sum(pos_counts[pos].values())
        print(f"  {pos}: {n_tok} tokens, {len(types)} types, hapax_rate={sum(1 for w,c in pos_counts[pos].items() if c==1)/len(types):.1%}")

    # Pairwise type overlaps
    print(f"\n  Pairwise TYPE-level overlap:")
    for p1, p2 in [('LF','MID'), ('MID','LL'), ('LF','LL')]:
        t1 = pos_types[p1]
        t2 = pos_types[p2]
        shared = t1 & t2
        jaccard = len(shared) / len(t1 | t2)
        n1_tok = sum(pos_counts[p1].values())
        n2_tok = sum(pos_counts[p2].values())
        # Token coverage: what fraction of p1 tokens are from shared types?
        p1_shared_tokens = sum(c for w,c in pos_counts[p1].items() if w in shared)
        p2_shared_tokens = sum(c for w,c in pos_counts[p2].items() if w in shared)
        print(f"  {p1}∩{p2}: {len(shared)} shared types | Jaccard={jaccard:.3f} | "
              f"{p1}_token_cov={p1_shared_tokens/n1_tok:.1%} | {p2}_token_cov={p2_shared_tokens/n2_tok:.1%}")

    # Pairwise ONSET-CLASS overlaps
    print(f"\n  Pairwise ONSET-CLASS-level overlap:")
    for p1, p2 in [('LF','MID'), ('MID','LL'), ('LF','LL')]:
        onsets1 = set(pos_onset_counts[p1].keys())
        onsets2 = set(pos_onset_counts[p2].keys())
        shared_oc = onsets1 & onsets2
        # What fraction of p1 tokens have onset class also in p2?
        n1 = sum(pos_onset_counts[p1].values())
        n2 = sum(pos_onset_counts[p2].values())
        p1_oc_tok = sum(c for o,c in pos_onset_counts[p1].items() if o in shared_oc)
        p2_oc_tok = sum(c for o,c in pos_onset_counts[p2].items() if o in shared_oc)
        print(f"  {p1}∩{p2} (onset class): {len(shared_oc)}/{len(onsets1|onsets2)} classes | "
              f"{p1}_onset_token_cov={p1_oc_tok/n1:.1%} | {p2}_onset_token_cov={p2_oc_tok/n2:.1%}")

    # KEY QUESTION: For MID tokens that also appear in LF/LL, decompose into:
    # (a) Same word type (identical repetition)
    # (b) Different word type from same onset class
    # (c) Different word and different onset class
    print(f"\n  KEY: What fraction of MID tokens are from LF∩MID shared types?")
    lf_types = pos_types['LF']
    ll_types = pos_types['LL']
    lf_onset_classes = {get_onset(w) for w in lf_types}
    ll_onset_classes = {get_onset(w) for w in ll_types}

    mid_token_count = sum(pos_counts['MID'].values())
    # Category A: MID token is identical word also in LF
    catA_lf = sum(c for w,c in pos_counts['MID'].items() if w in lf_types)
    # Category B: MID token not in LF but same onset class as some LF word
    catB_lf = sum(c for w,c in pos_counts['MID'].items()
                  if w not in lf_types and get_onset(w) in lf_onset_classes)
    # Category C: MID token not in LF and different onset class
    catC_lf = mid_token_count - catA_lf - catB_lf
    print(f"\n  LF vs MID decomposition ({mid_token_count} MID tokens):")
    print(f"    (A) Identical word also at LF: {catA_lf:5d} ({catA_lf/mid_token_count:.1%})")
    print(f"    (B) Same onset class, diff word: {catB_lf:5d} ({catB_lf/mid_token_count:.1%})")
    print(f"    (C) Different onset class: {catC_lf:5d} ({catC_lf/mid_token_count:.1%})")
    print(f"    -- (A+B) position-grammar-compatible: {(catA_lf+catB_lf)/mid_token_count:.1%}")

    catA_ll = sum(c for w,c in pos_counts['MID'].items() if w in ll_types)
    catB_ll = sum(c for w,c in pos_counts['MID'].items()
                  if w not in ll_types and get_onset(w) in ll_onset_classes)
    catC_ll = mid_token_count - catA_ll - catB_ll
    print(f"\n  LL vs MID decomposition ({mid_token_count} MID tokens):")
    print(f"    (A) Identical word also at LL: {catA_ll:5d} ({catA_ll/mid_token_count:.1%})")
    print(f"    (B) Same onset class, diff word: {catB_ll:5d} ({catB_ll/mid_token_count:.1%})")
    print(f"    (C) Different onset class: {catC_ll:5d} ({catC_ll/mid_token_count:.1%})")
    print(f"    -- (A+B) position-grammar-compatible: {(catA_ll+catB_ll)/mid_token_count:.1%}")

    # Top words shared across all positions
    print(f"\n  Top 15 words appearing in ALL THREE positions:")
    all3 = pos_types['LF'] & pos_types['MID'] & pos_types['LL']
    all3_freq = {w: pos_counts['LF'].get(w,0)+pos_counts['MID'].get(w,0)+pos_counts['LL'].get(w,0)
                 for w in all3}
    for w, tot in sorted(all3_freq.items(), key=lambda x: -x[1])[:15]:
        print(f"    {w:12} LF={pos_counts['LF'].get(w,0):3d} MID={pos_counts['MID'].get(w,0):4d} LL={pos_counts['LL'].get(w,0):3d} | onset={get_onset(w)}")

    # Onset-class enrichment per position (top 8)
    print(f"\n  Onset class distribution: enrichment ratio (LF vs MID vs LL):")
    n_lf = sum(pos_onset_counts['LF'].values())
    n_mid = sum(pos_onset_counts['MID'].values())
    n_ll  = sum(pos_onset_counts['LL'].values())
    all_ons = set()
    for p in ['LF','MID','LL']: all_ons |= set(pos_onset_counts[p].keys())
    print(f"  {'Onset':<7} {'LF_rate':>8} {'MID_rate':>9} {'LL_rate':>9} | {'LF/MID':>7} {'LL/MID':>7}")
    for onset in sorted(all_ons, key=lambda x: -pos_onset_counts['MID'].get(x,0)):
        lf_r  = pos_onset_counts['LF'].get(onset,0)/n_lf
        mid_r = pos_onset_counts['MID'].get(onset,0)/n_mid
        ll_r  = pos_onset_counts['LL'].get(onset,0)/n_ll
        if lf_r + mid_r + ll_r < 0.01: continue
        lf_enr = lf_r / mid_r if mid_r > 0 else float('inf')
        ll_enr = ll_r / mid_r if mid_r > 0 else float('inf')
        print(f"  {onset:<7} {lf_r:>8.2%} {mid_r:>9.2%} {ll_r:>9.2%} | {lf_enr:>7.2f}× {ll_enr:>7.2f}×")

    return pos_types, pos_counts, pos_onset_counts


if __name__ == '__main__':
    print("=" * 70)
    print("exp_292: Cross-Position Word Identity vs Onset-Class Overlap")
    print("=" * 70)

    tokens = parse_with_position(ZL3B_PATH)
    print(f"\nTotal tokens: {len(tokens)}")

    # Analyze per dialect
    overlap_analysis(tokens, 'A', 'A-dialect')
    overlap_analysis(tokens, 'B', 'B-dialect')

    # Summary: is positional grammar driven by WORD-LEVEL or ONSET-CLASS-LEVEL rules?
    print(f"\n" + "=" * 70)
    print("SUMMARY INTERPRETATION")
    print("=" * 70)
    print("""
  If (A) >> (B): positional grammar is word-specific — specific word types
    are assigned to specific positions (word-level lexical grammar)
  If (B) >> (A): positional grammar is onset-class-level — onset classes
    can use any word type at their preferred positions (onset-class grammar)
  If (A) + (B) ≈ total: onset class captures essentially all position variation
    (onset class alone determines position compatibility)
  If (C) is large: many MID words come from onset classes absent from LF/LL —
    MID has a truly distinct onset vocabulary
""")
