"""
exp_289: Hapax Internal Structure — H495
Are hapax legomena structurally different from frequent VMS words?

Measures onset class, suffix, midfix length, and word length distributions
for hapax (freq=1), moderate (freq 5-19), and frequent (freq>=20) word types.

Data: eva_zl3b.txt (ZL3b transcription)
"""
from pathlib import Path as _RepositoryPath

import os, re
import numpy as np
from collections import Counter, defaultdict
from math import log2

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
ZL3B_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

# Onset order from exp_257/288
ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

# Suffix list from exp_288 (longest-match first)
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

def entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*log2(c/total) for c in counts.values() if c > 0)

def kl_divergence(p_counts, q_counts):
    """KL(P||Q) where P and Q are Counter objects (token frequencies)."""
    all_keys = set(p_counts) | set(q_counts)
    p_total = sum(p_counts.values())
    q_total = sum(q_counts.values())
    if p_total == 0 or q_total == 0: return float('inf')
    eps = 1e-10
    kl = 0.0
    for k in all_keys:
        p = p_counts.get(k, 0) / p_total + eps
        q = q_counts.get(k, 0) / q_total + eps
        kl += p * log2(p / q)
    return kl

def folio_base(folio):
    return re.sub(r'[rv][12]?$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_zl3b(path, min_len=3, max_len=15):
    """Parse ZL3b, return (dialect_tag, word) pairs for all body text."""
    eva_ok = re.compile(r'^[a-z]+$')

    # Pass 1: classify dialects
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

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_stats.items()}

    # Pass 2: extract word tokens with dialect tag
    token_dial = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio = m.group(1).lstrip('+*=&~')
            locus_code = m.group(3)
            fb = folio_base(folio)
            dial = folio_dialect.get(fb, 'unknown')
            if dial not in ('A', 'B'): continue
            lc = locus_code.lstrip('+*=/~&@')
            if not lc.startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s,]', text)
                     if eva_ok.match(w) and min_len <= len(w) <= max_len]
            for w in words:
                token_dial.append((w, dial))

    return token_dial

def decompose(w):
    onset = get_onset(w)
    olen  = get_onset_len(w)
    body  = w[olen:]
    suffix = get_suffix(w)
    slen  = len(suffix)
    if slen > 0 and w.endswith(suffix):
        midfix = w[olen:-slen]
    else:
        midfix = body
    return {
        'onset': onset, 'suffix': suffix, 'midfix': midfix,
        'wlen': len(w), 'mlen': len(midfix), 'slen': slen,
        'zero_mid': len(midfix) == 0,
    }

def frequency_tier(freq):
    if freq == 1: return 'hapax'
    if freq <= 4: return 'rare'
    if freq <= 19: return 'moderate'
    return 'frequent'

def tier_stats(token_recs, label):
    """Compare hapax vs moderate vs frequent words on structural dimensions."""
    # Separate by tier
    by_tier = defaultdict(list)
    for rec in token_recs:
        by_tier[rec['tier']].append(rec)

    tiers = ['hapax', 'rare', 'moderate', 'frequent']
    print(f"\n=== {label}: Token Counts by Tier ===")
    for tier in tiers:
        recs = by_tier[tier]
        types = set(r['word'] for r in recs)
        print(f"  {tier:<12}: {len(recs):5d} tokens, {len(types):4d} types")

    # Word length comparison
    print(f"\n=== {label}: Word Length by Tier ===")
    for tier in tiers:
        recs = by_tier[tier]
        if len(recs) < 5: continue
        wlens = [r['wlen'] for r in recs]
        print(f"  {tier:<12}: mean={np.mean(wlens):.2f}, std={np.std(wlens):.2f}, median={np.median(wlens):.1f}")

    # Midfix length comparison
    print(f"\n=== {label}: Midfix Length by Tier ===")
    for tier in tiers:
        recs = by_tier[tier]
        if len(recs) < 5: continue
        mlens = [r['mlen'] for r in recs]
        zero_mid = sum(r['zero_mid'] for r in recs) / len(recs)
        print(f"  {tier:<12}: mean={np.mean(mlens):.2f}, std={np.std(mlens):.2f}, ZeroMid={zero_mid:.3f}")

    # Onset class comparison (top 8)
    print(f"\n=== {label}: Onset Distribution by Tier ===")
    print(f"  {'Onset':<7}", end='')
    for tier in tiers:
        print(f" {tier[:8]:>9}", end='')
    print()
    all_onsets = set()
    for t in tiers:
        for r in by_tier[t]:
            all_onsets.add(r['onset'])
    onset_totals = {t: len(by_tier[t]) for t in tiers}
    for onset in sorted(all_onsets):
        total_count = sum(len([r for r in by_tier[t] if r['onset']==onset]) for t in tiers)
        if total_count < 20: continue
        print(f"  {onset:<7}", end='')
        for tier in tiers:
            n_tier = onset_totals[tier]
            n_onset = sum(1 for r in by_tier[tier] if r['onset'] == onset)
            rate = n_onset / n_tier if n_tier > 0 else 0
            print(f"  {rate:>9.1%}", end='')
        print()

    # KL divergence of onset distribution: hapax vs frequent
    hapax_onset = Counter(r['onset'] for r in by_tier['hapax'])
    freq_onset  = Counter(r['onset'] for r in by_tier['frequent'])
    rare_onset  = Counter(r['onset'] for r in by_tier['rare'])
    mod_onset   = Counter(r['onset'] for r in by_tier['moderate'])
    kl_hf = kl_divergence(hapax_onset, freq_onset)
    kl_hm = kl_divergence(hapax_onset, mod_onset)
    kl_mf = kl_divergence(mod_onset, freq_onset)
    print(f"\n  KL(hapax||frequent)={kl_hf:.4f}, KL(hapax||moderate)={kl_hm:.4f}, KL(moderate||frequent)={kl_mf:.4f}")

    # Suffix distribution comparison
    print(f"\n=== {label}: Suffix Distribution by Tier (top 8 suffixes) ===")
    all_suffs = Counter()
    for t in tiers:
        all_suffs.update(r['suffix'] for r in by_tier[t])
    top_suffs = [s for s,c in all_suffs.most_common(8)]
    print(f"  {'Suffix':<7}", end='')
    for tier in tiers:
        print(f" {tier[:8]:>9}", end='')
    print()
    for suf in top_suffs:
        print(f"  '{suf}'  ", end='')
        for tier in tiers:
            n_tier = len(by_tier[tier])
            n_suf  = sum(1 for r in by_tier[tier] if r['suffix'] == suf)
            rate = n_suf / n_tier if n_tier > 0 else 0
            print(f"  {rate:>9.1%}", end='')
        print()

    # Suffix entropy per tier
    print(f"\n  Suffix entropy by tier:")
    for tier in tiers:
        sc = Counter(r['suffix'] for r in by_tier[tier])
        h = entropy(sc)
        print(f"    {tier:<12}: H={h:.3f} bits ({len(sc)} suffix types)")

    # KL divergence of suffix distribution: hapax vs frequent
    hapax_suf = Counter(r['suffix'] for r in by_tier['hapax'])
    freq_suf  = Counter(r['suffix'] for r in by_tier['frequent'])
    kl_suf = kl_divergence(hapax_suf, freq_suf)
    print(f"  KL(hapax_suf||frequent_suf)={kl_suf:.4f}")

    return by_tier

def null_model_hapax(token_recs, n_iter=200):
    """Estimate expected KL(hapax||frequent) under null model: shuffle frequency assignments."""
    np.random.seed(289)
    words = [r['word'] for r in token_recs]
    freqs = [r['freq'] for r in token_recs]

    kl_null = []
    for _ in range(n_iter):
        shuffled_freqs = np.random.permutation(freqs)
        hapax_onset = Counter()
        freq_onset  = Counter()
        for w, f in zip(words, shuffled_freqs):
            onset = get_onset(w)
            tier  = frequency_tier(f)
            if tier == 'hapax': hapax_onset[onset] += 1
            elif tier == 'frequent': freq_onset[onset] += 1
        kl = kl_divergence(hapax_onset, freq_onset)
        kl_null.append(kl)
    return np.mean(kl_null), np.std(kl_null), np.percentile(kl_null, 95)


if __name__ == '__main__':
    print("=" * 70)
    print("exp_289: Hapax Internal Structure")
    print("=" * 70)

    # Load corpus
    token_dial = parse_zl3b(ZL3B_PATH)
    print(f"\nTotal tokens: {len(token_dial)}")

    # Compute global word frequencies (across both dialects)
    global_freq = Counter(w for w, d in token_dial)
    total_types = len(global_freq)
    hapax_count = sum(1 for c in global_freq.values() if c == 1)
    print(f"Total word types: {total_types}")
    print(f"Hapax types: {hapax_count} ({hapax_count/total_types:.1%} of types)")
    print(f"Token coverage by hapaxes: {hapax_count}/{len(token_dial)} = {hapax_count/len(token_dial):.1%}")

    # Frequency distribution
    freq_dist = Counter(global_freq.values())
    print(f"\nFrequency distribution:")
    for f in sorted(freq_dist.keys())[:10]:
        print(f"  freq={f}: {freq_dist[f]} types ({freq_dist[f]/total_types:.1%})")
    high_freq = sum(c for f,c in freq_dist.items() if f >= 20)
    print(f"  freq>=20: {high_freq} types ({high_freq/total_types:.1%})")

    # Build token records with decomposition
    all_recs_A, all_recs_B = [], []
    for w, dial in token_dial:
        freq = global_freq[w]
        tier = frequency_tier(freq)
        dec  = decompose(w)
        rec  = {'word': w, 'dial': dial, 'freq': freq, 'tier': tier, **dec}
        if dial == 'A': all_recs_A.append(rec)
        else: all_recs_B.append(rec)

    # Stats per dialect
    by_tier_A = tier_stats(all_recs_A, 'A-dialect')
    by_tier_B = tier_stats(all_recs_B, 'B-dialect')

    # Null model KL for A-dialect
    print(f"\n=== Null Model: KL(hapax||frequent) under Shuffled Frequencies (A-dialect) ===")
    null_mean_A, null_std_A, null_p95_A = null_model_hapax(all_recs_A)
    print(f"  Observed KL(hapax||frequent) onset: ", end='')
    hapax_onset_A = Counter(r['onset'] for r in by_tier_A['hapax'])
    freq_onset_A  = Counter(r['onset'] for r in by_tier_A['frequent'])
    obs_kl_A = kl_divergence(hapax_onset_A, freq_onset_A)
    print(f"{obs_kl_A:.4f}")
    print(f"  Null model: mean={null_mean_A:.4f}, std={null_std_A:.4f}, p95={null_p95_A:.4f}")
    print(f"  Z-score: {(obs_kl_A - null_mean_A)/null_std_A:.2f}")

    print(f"\n=== Null Model: KL(hapax||frequent) under Shuffled Frequencies (B-dialect) ===")
    null_mean_B, null_std_B, null_p95_B = null_model_hapax(all_recs_B)
    print(f"  Observed KL(hapax||frequent) onset: ", end='')
    hapax_onset_B = Counter(r['onset'] for r in by_tier_B['hapax'])
    freq_onset_B  = Counter(r['onset'] for r in by_tier_B['frequent'])
    obs_kl_B = kl_divergence(hapax_onset_B, freq_onset_B)
    print(f"{obs_kl_B:.4f}")
    print(f"  Null model: mean={null_mean_B:.4f}, std={null_std_B:.4f}, p95={null_p95_B:.4f}")
    print(f"  Z-score: {(obs_kl_B - null_mean_B)/null_std_B:.2f}")

    # Summary comparison: hapax vs frequent structural differences
    print(f"\n=== SUMMARY: Hapax vs Frequent Structural Comparison ===")
    for dialect, by_tier in [('A', by_tier_A), ('B', by_tier_B)]:
        hapax = by_tier['hapax']
        freq  = by_tier['frequent']
        if not hapax or not freq: continue
        h_wlen = np.mean([r['wlen'] for r in hapax])
        f_wlen = np.mean([r['wlen'] for r in freq])
        h_mlen = np.mean([r['mlen'] for r in hapax])
        f_mlen = np.mean([r['mlen'] for r in freq])
        h_zero = np.mean([r['zero_mid'] for r in hapax])
        f_zero = np.mean([r['zero_mid'] for r in freq])
        h_suff_h = entropy(Counter(r['suffix'] for r in hapax))
        f_suff_h = entropy(Counter(r['suffix'] for r in freq))
        print(f"\n{dialect}-dialect:")
        print(f"  WLen:    hapax={h_wlen:.2f}, frequent={f_wlen:.2f}, diff={h_wlen-f_wlen:+.2f}")
        print(f"  MLen:    hapax={h_mlen:.2f}, frequent={f_mlen:.2f}, diff={h_mlen-f_mlen:+.2f}")
        print(f"  ZeroMid: hapax={h_zero:.3f}, frequent={f_zero:.3f}, diff={h_zero-f_zero:+.3f}")
        print(f"  SuffH:   hapax={h_suff_h:.3f}, frequent={f_suff_h:.3f}, diff={h_suff_h-f_suff_h:+.3f}")

    # Top hapax onset vs top frequent onset
    print(f"\n=== Most Common Onset Class in Hapax vs Frequent Words ===")
    for dialect, by_tier in [('A', by_tier_A), ('B', by_tier_B)]:
        print(f"\n{dialect}-dialect:")
        for tier in ['hapax', 'frequent']:
            onset_c = Counter(r['onset'] for r in by_tier[tier])
            total = len(by_tier[tier])
            top3 = onset_c.most_common(3)
            top_str = ', '.join(f"{o}={c/total:.1%}" for o,c in top3)
            print(f"  {tier:<12}: {top_str}")
