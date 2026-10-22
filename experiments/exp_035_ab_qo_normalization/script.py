#!/usr/bin/env python3
"""
Experiment exp_035: A/B Divergence After qo-Normalization
Question: Does removing the qo-prefix from Currier B words reduce the measured
A/B vocabulary divergence (Jaccard=0.148, Spearman rho=0.337 from exp_023)?
If qo is a B-dialect marker for A's bare k/t-initial stems, then:
  - B vocabulary with qo stripped should overlap more with A vocabulary
  - Jaccard should increase
  - Rank correlation should increase
"""
from pathlib import Path as _RepositoryPath

import re
import math
from collections import Counter

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

def parse_currier_words(path):
    """Parse words by Currier dialect."""
    words_a = []
    words_b = []
    current_lang = None

    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            if re.match(r'^<f\w+>', line) and '$L=' in line:
                m = re.search(r'\$L=([AB])', line)
                current_lang = m.group(1) if m else None
                continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m or current_lang not in ('A', 'B'):
                continue
            locus = m.group(1).strip()
            if not re.match(r'^[+*@=/~&]?P[0-9]$', locus):
                continue
            content = m.group(2)
            content = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*', '', content)
            for token in re.split(r'[., ]+', content):
                token = token.strip()
                if token and re.match(r'^[a-z\']+$', token) and len(token) >= 2:
                    if current_lang == 'A':
                        words_a.append(token)
                    else:
                        words_b.append(token)
    return words_a, words_b

def spearman_rho(x, y):
    """Spearman rank correlation."""
    n = len(x)
    if n < 3: return 0.0
    ranks_x = {v: i+1 for i, v in enumerate(sorted(x))}
    ranks_y = {v: i+1 for i, v in enumerate(sorted(y))}
    d2_sum = sum((ranks_x[x[i]] - ranks_y[y[i]])**2 for i in range(n))
    return 1 - 6*d2_sum / (n*(n**2-1))

def qo_normalize(words):
    """Replace qo-words with their bare stems."""
    result = []
    for w in words:
        if w.startswith('qo') and len(w) > 2:
            result.append(w[2:])  # strip "qo" prefix
        else:
            result.append(w)
    return result

def jaccard(set_a, set_b):
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0

def rank_correlation_top_n(freq_a, freq_b, n=200):
    """Spearman rank correlation for top-N shared words."""
    # Get top-N words from each
    top_a = [w for w, _ in freq_a.most_common(n)]
    top_b = [w for w, _ in freq_b.most_common(n)]
    shared = set(top_a) & set(top_b)
    if len(shared) < 10:
        return 0.0, len(shared)
    shared_list = sorted(shared)
    ranks_a = {w: i+1 for i, (w,_) in enumerate(freq_a.most_common()) if w in shared}
    ranks_b = {w: i+1 for i, (w,_) in enumerate(freq_b.most_common()) if w in shared}
    x = [ranks_a[w] for w in shared_list]
    y = [ranks_b[w] for w in shared_list]
    rho = spearman_rho(x, y)
    return rho, len(shared)

def vocab_overlap_analysis(words_a, words_b, label):
    freq_a = Counter(words_a)
    freq_b = Counter(words_b)
    vocab_a = set(words_a)
    vocab_b = set(words_b)

    jac = jaccard(vocab_a, vocab_b)
    rho, n_shared = rank_correlation_top_n(freq_a, freq_b, n=200)

    top_a_only = [w for w, _ in freq_a.most_common(30) if w not in vocab_b]
    top_b_only = [w for w, _ in freq_b.most_common(30) if w not in vocab_a]

    print(f"\n{'='*55}")
    print(f"=== {label} ===")
    print(f"  A: {len(words_a)} tokens, {len(vocab_a)} types")
    print(f"  B: {len(words_b)} tokens, {len(vocab_b)} types")
    print(f"  Shared types: {len(vocab_a & vocab_b)}")
    print(f"  Jaccard: {jac:.3f}")
    print(f"  Spearman rho (top-200 shared, n={n_shared}): {rho:.3f}")
    print(f"  Top A-exclusive: {top_a_only[:10]}")
    print(f"  Top B-exclusive: {top_b_only[:10]}")
    return jac, rho

def main():
    print("Parsing Currier A and B words...")
    words_a, words_b = parse_currier_words(ZL3B)
    print(f"A: {len(words_a)} tokens; B: {len(words_b)} tokens")

    # Baseline (reproduces exp_023)
    jac_orig, rho_orig = vocab_overlap_analysis(words_a, words_b, "BASELINE (original)")

    # Test 1: qo-normalize B only
    words_b_normalized = qo_normalize(words_b)
    jac_norm_b, rho_norm_b = vocab_overlap_analysis(words_a, words_b_normalized, "B qo-NORMALIZED")

    # Test 2: qo-normalize both A and B
    words_a_normalized = qo_normalize(words_a)
    jac_norm_both, rho_norm_both = vocab_overlap_analysis(words_a_normalized, words_b_normalized,
                                                           "BOTH A+B qo-NORMALIZED")

    # Test 3: qo-normalize B, then check if qo-stripped B top words now overlap with A
    print("\n=== qo-NORMALIZATION IMPACT SUMMARY ===")
    print(f"{'Condition':>30} | {'Jaccard':>8} | {'Spearman rho':>14}")
    print("-" * 60)
    print(f"{'Baseline':>30} | {jac_orig:>8.3f} | {rho_orig:>14.3f}")
    print(f"{'B qo-normalized':>30} | {jac_norm_b:>8.3f} | {rho_norm_b:>14.3f}")
    print(f"{'Both qo-normalized':>30} | {jac_norm_both:>8.3f} | {rho_norm_both:>14.3f}")

    delta_jac_b = jac_norm_b - jac_orig
    delta_rho_b = rho_norm_b - rho_orig
    print(f"\n  Delta (B normalized): Jaccard={delta_jac_b:+.3f}, rho={delta_rho_b:+.3f}")
    print(f"  Delta (both normalized): Jaccard={jac_norm_both-jac_orig:+.3f}, rho={rho_norm_both-rho_orig:+.3f}")

    # Check what fraction of B-exclusive words are qo-words
    freq_a = Counter(words_a)
    freq_b = Counter(words_b)
    vocab_a = set(words_a)
    vocab_b = set(words_b)
    b_exclusive = set(w for w in vocab_b if w not in vocab_a)
    qo_in_b_exclusive = set(w for w in b_exclusive if w.startswith('qo'))
    print(f"\n=== qo-WORDS IN B-EXCLUSIVE VOCABULARY ===")
    print(f"  B-exclusive vocab types: {len(b_exclusive)}")
    print(f"  Of those, qo-words: {len(qo_in_b_exclusive)} ({100*len(qo_in_b_exclusive)/len(b_exclusive):.1f}%)")
    print(f"  Of those, qo-words in top-100 B frequency: ")
    top_b_excl_qo = [(w, freq_b[w]) for w in qo_in_b_exclusive]
    top_b_excl_qo.sort(key=lambda x: -x[1])
    for w, cnt in top_b_excl_qo[:15]:
        stem = w[2:]
        in_a = stem in vocab_a
        print(f"    {w} ({cnt}x) → stem '{stem}' in A: {'YES' if in_a else 'no'}")

    # Entropy before/after
    print(f"\n=== ENTROPY AFTER qo-NORMALIZATION ===")
    def h2_flat(tokens):
        bg = Counter()
        ug = Counter()
        for w in tokens:
            for i in range(len(w)-1):
                bg[(w[i],w[i+1])] += 1
                ug[w[i]] += 1
        if not bg: return 0.0
        total = sum(bg.values())
        h = 0.0
        for (a,b),cnt in bg.items():
            p = cnt/total
            h -= p * math.log2(cnt/ug[a])
        return h

    print(f"  A original H2: {h2_flat(words_a):.3f}")
    print(f"  B original H2: {h2_flat(words_b):.3f}")
    print(f"  B qo-normalized H2: {h2_flat(words_b_normalized):.3f}")

if __name__ == '__main__':
    main()
