"""
exp_294: qok A vs B Cross-Dialect Asymmetry — H498
exp_288 found: qok midfix in A-dialect averages 1.34 chars vs B-dialect 0.52 chars (2.6× gap).
This experiment characterizes the specific midfix sequences, suffix distributions, and word-type
inventories for qok-onset words in A vs B, looking for what drives the asymmetry.

Key questions:
1. What specific midfix sequences does A-qok use that B-qok doesn't?
2. Does B-qok have a different suffix paradigm (is B-qok a pure template qo-stem + k + suffix)?
3. Is the A-qok midfix asymmetry driven by a few very long words or many moderately long words?
4. What is the full word-type inventory for qok in A vs B?

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


def analyze_onset_class(words, onset_label, label):
    """Full characterization of a given onset class in a given dialect."""
    # Filter to this onset class
    qok_words = [w for w in words if get_onset(w) == onset_label]
    if not qok_words:
        print(f"\n  {label}: No {onset_label}-onset words found.")
        return

    n = len(qok_words)
    token_counts = Counter(qok_words)

    # Decompose each token
    midfixes = []
    suffixes = []
    mlens = []
    zero_mids = 0

    for w in qok_words:
        olen = get_onset_len(w)
        suf  = get_suffix(w)
        slen = len(suf)
        mfix = w[olen:-slen] if slen > 0 else w[olen:]
        midfixes.append(mfix)
        suffixes.append(suf)
        mlens.append(len(mfix))
        if len(mfix) == 0: zero_mids += 1

    print(f"\n{'='*60}")
    print(f"  {label}: {onset_label}-onset class  (N={n} tokens, {len(token_counts)} types)")
    print(f"{'='*60}")

    # Basic stats
    print(f"\n  Word length: mean={np.mean([len(w) for w in qok_words]):.2f}, "
          f"std={np.std([len(w) for w in qok_words]):.2f}")
    print(f"  Midfix length: mean={np.mean(mlens):.2f}, std={np.std(mlens):.2f}, "
          f"ZeroMid={zero_mids/n:.1%}")

    # Midfix length distribution
    mlen_dist = Counter(mlens)
    print(f"\n  Midfix length distribution:")
    for ml in sorted(mlen_dist.keys()):
        bar = '#' * int(mlen_dist[ml]/n*50)
        print(f"    MLen={ml}: {mlen_dist[ml]:4d} ({mlen_dist[ml]/n:5.1%}) {bar}")

    # Top suffixes
    suf_counts = Counter(suffixes)
    print(f"\n  Top suffixes (N={n}):")
    for suf, c in suf_counts.most_common(15):
        display = f"'{suf}'" if suf else "''"
        print(f"    {display:10} {c:4d} ({c/n:5.1%})")

    # Top midfix sequences
    mfix_counts = Counter(midfixes)
    print(f"\n  Top midfix sequences (total unique: {len(mfix_counts)}):")
    for mfix, c in mfix_counts.most_common(20):
        display = f"'{mfix}'" if mfix else "''"
        print(f"    {display:12} {c:4d} ({c/n:5.1%})")

    # Top word types
    print(f"\n  Top 25 word types:")
    for w, c in token_counts.most_common(25):
        olen = get_onset_len(w)
        suf  = get_suffix(w)
        slen = len(suf)
        mfix = w[olen:-slen] if slen > 0 else w[olen:]
        print(f"    {w:15} {c:4d} ({c/n:5.1%}) | mfix='{mfix}' suf='{suf}'")

    # Suffix entropy
    print(f"\n  Suffix entropy: {entropy(suf_counts):.3f} bits")
    print(f"  Midfix entropy: {entropy(mfix_counts):.3f} bits")
    print(f"  Word-type entropy: {entropy(token_counts):.3f} bits")

    # Types exclusive to this dialect (will be compared externally)
    return token_counts, Counter(midfixes), Counter(suffixes)


def compare_midfix_distributions(mfix_A, mfix_B, onset_label):
    """Compare midfix distributions between A and B."""
    n_A = sum(mfix_A.values())
    n_B = sum(mfix_B.values())
    all_mfix = set(mfix_A.keys()) | set(mfix_B.keys())

    print(f"\n{'='*60}")
    print(f"  Cross-Dialect Midfix Comparison: {onset_label}-onset")
    print(f"{'='*60}")
    print(f"  A: {len(mfix_A)} unique midfixes from {n_A} tokens")
    print(f"  B: {len(mfix_B)} unique midfixes from {n_B} tokens")

    # A-exclusive midfixes (appear in A but not B)
    a_only = {mf: mfix_A[mf] for mf in mfix_A if mf not in mfix_B and mfix_A[mf] >= 2}
    b_only = {mf: mfix_B[mf] for mf in mfix_B if mf not in mfix_A and mfix_B[mf] >= 2}

    print(f"\n  A-exclusive midfixes (A-only, count ≥ 2), top 20:")
    for mf, c in sorted(a_only.items(), key=lambda x: -x[1])[:20]:
        display = f"'{mf}'" if mf else "''"
        rate_a = mfix_A[mf]/n_A
        print(f"    {display:12} A={c} ({rate_a:.2%})")

    print(f"\n  B-exclusive midfixes (B-only, count ≥ 2), top 20:")
    for mf, c in sorted(b_only.items(), key=lambda x: -x[1])[:20]:
        display = f"'{mf}'" if mf else "''"
        rate_b = mfix_B[mf]/n_B
        print(f"    {display:12} B={c} ({rate_b:.2%})")

    # Shared midfixes with A/B rate comparison
    shared = {mf for mf in all_mfix if mf in mfix_A and mf in mfix_B}
    print(f"\n  Shared midfixes (appear in both A and B), sorted by A rate:")
    shared_data = [(mf, mfix_A[mf], mfix_A[mf]/n_A, mfix_B[mf], mfix_B[mf]/n_B)
                   for mf in shared]
    for mf, cA, rA, cB, rB in sorted(shared_data, key=lambda x: -x[2])[:20]:
        display = f"'{mf}'" if mf else "''"
        ratio = rA/rB if rB > 0 else float('inf')
        print(f"    {display:12} A={cA:3d}({rA:.2%}) B={cB:3d}({rB:.2%}) A/B={ratio:.2f}×")


if __name__ == '__main__':
    print("=" * 70)
    print("exp_294: qok Dialect Asymmetry (H498)")
    print("=" * 70)

    words_A, words_B = parse_both_dialects(ZL3B_PATH)
    print(f"\nLoaded: A={len(words_A)}, B={len(words_B)} total words")

    # Analyze qok in each dialect
    result_A = analyze_onset_class(words_A, 'qok', 'A-dialect')
    result_B = analyze_onset_class(words_B, 'qok', 'B-dialect')

    if result_A and result_B:
        tok_A, mfix_A, suf_A = result_A
        tok_B, mfix_B, suf_B = result_B

        # Cross-dialect comparison
        compare_midfix_distributions(mfix_A, mfix_B, 'qok')

        # Also compare suffix distributions
        print(f"\n{'='*60}")
        print("  Cross-Dialect Suffix Comparison: qok-onset")
        print(f"{'='*60}")
        n_A = sum(suf_A.values())
        n_B = sum(suf_B.values())
        all_suf = set(suf_A.keys()) | set(suf_B.keys())
        print(f"\n  {'Suffix':<10} {'A_count':>8} {'A_%':>7} {'B_count':>8} {'B_%':>7} | {'A/B':>6}")
        for suf in sorted(all_suf, key=lambda x: -suf_A.get(x,0)/n_A):
            cA = suf_A.get(suf, 0)
            cB = suf_B.get(suf, 0)
            rA = cA/n_A
            rB = cB/n_B
            if rA + rB < 0.005: continue
            ratio = rA/rB if rB > 0 else float('inf')
            display = f"'{suf}'" if suf else "''"
            print(f"  {display:<10} {cA:>8} {rA:>7.2%} {cB:>8} {rB:>7.2%} | {ratio:>6.2f}×")

        # Vocabulary comparison: types in A vs B
        n_tok_A = sum(tok_A.values())
        n_tok_B = sum(tok_B.values())
        types_A = set(tok_A.keys())
        types_B = set(tok_B.keys())
        shared_types = types_A & types_B
        a_only_types = types_A - types_B
        b_only_types = types_B - types_A

        print(f"\n  qok Vocabulary Overlap:")
        print(f"    A: {len(types_A)} types, {n_tok_A} tokens")
        print(f"    B: {len(types_B)} types, {n_tok_B} tokens")
        print(f"    Shared types: {len(shared_types)}")
        print(f"    A-exclusive: {len(a_only_types)}, B-exclusive: {len(b_only_types)}")
        print(f"    Jaccard: {len(shared_types)/len(types_A|types_B):.3f}")

    # Also: compare ok, ot onset classes (also sparse) for cross-onset reference
    print(f"\n{'='*70}")
    print("COMPARATIVE: ok-onset and ot-onset (other sparse classes)")
    print("=" * 70)
    for onset in ['ok', 'ot']:
        ok_A = [w for w in words_A if get_onset(w) == onset]
        ok_B = [w for w in words_B if get_onset(w) == onset]

        def mean_mlen(wlist):
            if not wlist: return 0.0
            mlens = []
            for w in wlist:
                olen = get_onset_len(w)
                suf  = get_suffix(w)
                slen = len(suf)
                mfix = w[olen:-slen] if slen > 0 else w[olen:]
                mlens.append(len(mfix))
            return np.mean(mlens)

        mla = mean_mlen(ok_A)
        mlb = mean_mlen(ok_B)
        ratio = mla/mlb if mlb > 0 else float('inf')
        print(f"\n  {onset}-onset: A={len(ok_A)} tokens (mlen={mla:.2f}), "
              f"B={len(ok_B)} tokens (mlen={mlb:.2f}), A/B ratio={ratio:.2f}×")

        # Top words in each dialect
        cA = Counter(ok_A)
        cB = Counter(ok_B)
        print(f"    A top-5: {[(w,c) for w,c in cA.most_common(5)]}")
        print(f"    B top-5: {[(w,c) for w,c in cB.most_common(5)]}")
