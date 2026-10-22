"""
exp_295: Suffix-Onset Paradigm Across Dialects (H497 + generalization of H498)
H497: Suffix entropy vs hapax rate per onset class — is suffix entropy the key discriminant
of hapax-producing onset classes?

Also: Does the A>B morphological standardization seen in qok (exp_294) extend to all
major onset classes? Do all onset classes in B show more concentrated suffix paradigms than A?

Key questions:
1. For each onset class: suffix entropy, top suffix, suffix concentration (top-1 fraction)
2. A vs B comparison: is B uniformly more concentrated than A?
3. Is suffix entropy predictive of onset class hapax rate?
4. What is the "closed paradigm" size for each B-dialect onset class?

Data: eva_zl3b.txt
"""
from pathlib import Path as _RepositoryPath

import os, re
import numpy as np
from collections import Counter, defaultdict
from math import log2

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
ZL3B_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]
SUFFIX_LIST = [
    'eedy', 'eey', 'edy', 'aiin', 'oldy', 'oly', 'ory',
    'ain', 'ol', 'or', 'al', 'ar', 'ey', 'dy', 'ay',
    'am', 'an', 'in', 'y', 'n', 'l', 'r',
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0

def get_suffix(w):
    for s in SUFFIX_LIST:
        if w.endswith(s) and len(w) > len(s):
            return s
    return ''

def folio_base(folio):
    return re.sub(r'[rv][12]?$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*log2(c/total) for c in counts.values() if c > 0)

def parse_both_dialects(path, min_len=3, max_len=15):
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

    words_A, words_B = [], []
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
            target = words_A if dial == 'A' else words_B
            target.extend(words)
    return words_A, words_B


def onset_class_suffix_analysis(words, dial_label):
    """For each onset class: suffix entropy, top suffix, concentration, hapax rate."""
    # Global hapax classification
    global_freq = Counter(words)

    onset_data = defaultdict(lambda: {
        'tokens': [], 'suffixes': Counter(), 'types': Counter()
    })

    for w in words:
        onset = get_onset(w)
        suf   = get_suffix(w)
        olen  = get_onset_len(w)
        slen  = len(suf)
        mfix  = w[olen:-slen] if slen > 0 else w[olen:]

        onset_data[onset]['tokens'].append(w)
        onset_data[onset]['suffixes'][suf] += 1
        onset_data[onset]['types'][w] += 1

    print(f"\n{'='*80}")
    print(f"  {dial_label}: Suffix-Onset Paradigm Analysis")
    print(f"{'='*80}")
    print(f"\n  {'Onset':<7} {'N':>6} {'Types':>6} {'SufH':>7} {'Top1_suf':>12} {'Top1%':>7} {'Top3%':>7} {'HapaxR':>8} {'TTR':>7}")
    print('  ' + '-'*80)

    results = {}
    for onset in [o for _, o in ONSET_ORDER] + ['other']:
        d = onset_data[onset]
        n = len(d['tokens'])
        if n < 20: continue

        suf_counts = d['suffixes']
        tok_counts = d['types']
        n_types = len(tok_counts)
        ttr = n_types / n

        suf_h = entropy(suf_counts)
        hapax_rate = sum(1 for w in d['tokens'] if global_freq[w] == 1) / n

        # Top suffix
        top_suf = suf_counts.most_common(1)
        top1_suf = top_suf[0][0] if top_suf else ''
        top1_pct = top_suf[0][1] / n if top_suf else 0

        # Top 3 coverage
        top3 = sum(c for _, c in suf_counts.most_common(3))
        top3_pct = top3 / n

        display_suf = f"'{top1_suf}'" if top1_suf else "''"
        print(f"  {onset:<7} {n:>6} {n_types:>6} {suf_h:>7.3f} {display_suf:>12} {top1_pct:>7.1%} {top3_pct:>7.1%} {hapax_rate:>8.1%} {ttr:>7.3f}")

        results[onset] = {
            'n': n, 'n_types': n_types, 'ttr': ttr,
            'suf_h': suf_h, 'hapax_rate': hapax_rate,
            'top1_suf': top1_suf, 'top1_pct': top1_pct, 'top3_pct': top3_pct,
            'suf_counts': suf_counts, 'tok_counts': tok_counts,
        }

    return results


def cross_dialect_comparison(res_A, res_B):
    """Compare suffix paradigm standardization between A and B."""
    print(f"\n{'='*80}")
    print("  CROSS-DIALECT COMPARISON: Is B More Concentrated Than A?")
    print('='*80)
    print(f"\n  {'Onset':<7} {'A_SufH':>8} {'B_SufH':>8} {'B-A_diff':>10} | {'A_Top1%':>8} {'B_Top1%':>8} {'B/A':>6} | {'A_HapaxR':>9} {'B_HapaxR':>9}")
    print('  ' + '-'*85)

    common_onsets = set(res_A.keys()) & set(res_B.keys())
    # Sort by B suffix entropy
    for onset in sorted(common_onsets, key=lambda x: res_B[x]['suf_h']):
        a = res_A[onset]
        b = res_B[onset]
        delta_h = b['suf_h'] - a['suf_h']
        ratio_top1 = b['top1_pct'] / a['top1_pct'] if a['top1_pct'] > 0 else float('inf')
        print(f"  {onset:<7} {a['suf_h']:>8.3f} {b['suf_h']:>8.3f} {delta_h:>+10.3f} | "
              f"{a['top1_pct']:>8.1%} {b['top1_pct']:>8.1%} {ratio_top1:>6.2f}× | "
              f"{a['hapax_rate']:>9.1%} {b['hapax_rate']:>9.1%}")

    # Summary stats
    b_higher_h = sum(1 for o in common_onsets
                     if o in res_B and o in res_A
                     and res_B[o]['suf_h'] > res_A[o]['suf_h'])
    b_higher_top1 = sum(1 for o in common_onsets
                        if o in res_B and o in res_A
                        and res_B[o]['top1_pct'] > res_A[o]['top1_pct'])
    print(f"\n  Summary: B has HIGHER suffix entropy than A in {b_higher_h}/{len(common_onsets)} onset classes")
    print(f"          B has HIGHER top-1 suffix concentration than A in {b_higher_top1}/{len(common_onsets)} onset classes")


def hapax_vs_suffix_entropy(results, label):
    """Test H497: is suffix entropy correlated with hapax rate?"""
    onsets = [o for o, d in results.items() if d['n'] >= 50]
    suf_hs = [results[o]['suf_h'] for o in onsets]
    hapax_rs = [results[o]['hapax_rate'] for o in onsets]
    top1_pcts = [results[o]['top1_pct'] for o in onsets]

    if len(onsets) < 3:
        return

    # Spearman correlation
    def spearman(x, y):
        n = len(x)
        rx = [sorted(x).index(v) for v in x]
        ry = [sorted(y).index(v) for v in y]
        d2 = sum((a-b)**2 for a,b in zip(rx, ry))
        return 1 - 6*d2/(n*(n**2-1))

    rho_h = spearman(suf_hs, hapax_rs)
    rho_t = spearman(top1_pcts, hapax_rs)

    print(f"\n  {label}: H497 Test — Suffix Entropy vs Hapax Rate")
    print(f"    Spearman(suf_entropy, hapax_rate): ρ = {rho_h:+.3f}")
    print(f"    Spearman(top1_concentration, hapax_rate): ρ = {rho_t:+.3f}")
    print(f"    (N={len(onsets)} onset classes with ≥50 tokens)")
    print(f"\n    {'Onset':<7} {'SufH':>7} {'Top1%':>7} {'Hapax%':>8}")
    for o in sorted(onsets, key=lambda x: -results[x]['hapax_rate']):
        print(f"    {o:<7} {results[o]['suf_h']:>7.3f} {results[o]['top1_pct']:>7.1%} {results[o]['hapax_rate']:>8.1%}")


def closed_paradigm_size(results, label, target_coverage=0.90):
    """For each onset class, how many word types cover 90% of tokens?"""
    print(f"\n{'='*60}")
    print(f"  {label}: Closed Paradigm Size (Types for 90% Token Coverage)")
    print('='*60)
    print(f"\n  {'Onset':<7} {'N_tok':>6} {'N_types':>8} | {'90%_types':>10} {'90%_frac':>10} | {'Top word':>15} {'Top%':>7}")
    print('  ' + '-'*70)

    for onset in [o for _, o in ONSET_ORDER] + ['other']:
        if onset not in results: continue
        d = results[onset]
        n = d['n']
        if n < 30: continue

        # Sort types by frequency
        sorted_types = d['tok_counts'].most_common()
        cumsum = 0
        n90 = 0
        for word, count in sorted_types:
            cumsum += count
            n90 += 1
            if cumsum / n >= target_coverage:
                break

        top_word = sorted_types[0][0] if sorted_types else ''
        top_pct  = sorted_types[0][1] / n if sorted_types else 0
        frac90   = n90 / d['n_types']

        print(f"  {onset:<7} {n:>6} {d['n_types']:>8} | {n90:>10} {frac90:>10.1%} | {top_word:>15} {top_pct:>7.1%}")


if __name__ == '__main__':
    print("=" * 80)
    print("exp_295: Suffix-Onset Paradigm (H497 + generalization of H498)")
    print("=" * 80)

    words_A, words_B = parse_both_dialects(ZL3B_PATH)
    print(f"\nLoaded: A={len(words_A)}, B={len(words_B)} total words")

    # Main analysis
    res_A = onset_class_suffix_analysis(words_A, 'A-dialect')
    res_B = onset_class_suffix_analysis(words_B, 'B-dialect')

    # Cross-dialect comparison
    cross_dialect_comparison(res_A, res_B)

    # H497 test
    hapax_vs_suffix_entropy(res_A, 'A-dialect')
    hapax_vs_suffix_entropy(res_B, 'B-dialect')

    # Closed paradigm analysis
    closed_paradigm_size(res_A, 'A-dialect')
    closed_paradigm_size(res_B, 'B-dialect')
