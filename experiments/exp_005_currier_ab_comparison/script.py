"""
Experiment: exp_005_currier_ab_comparison
Hypothesis tested: H004 (partial) — Are Currier A and B structurally similar (dialects) or different systems?
Approach: Detailed structural and distributional comparison of A vs B subcorpora.
Full embedding-based alignment (the original H004 plan) is saved for a follow-up experiment.
Data: data/transcriptions/eva_zl3b.txt
"""

import re
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

random.seed(42)
BASE = Path(__file__).resolve().parents[2]

LOCUS_CATEGORIES = {
    'P': 'body', 'L': 'label', 'R': 'rider', 'C': 'circular',
}

def classify_section(folio_str):
    m = re.match(r'f(\d+)', folio_str)
    if not m:
        return 'unknown'
    n = int(m.group(1))
    if n <= 66: return 'herbal_A'
    elif 67 <= n <= 73: return 'astro'
    elif 74 <= n <= 84: return 'bio'
    elif 85 <= n <= 102: return 'pharma'
    elif 103 <= n <= 116: return 'recipes'
    else: return 'misc'


def parse_eva_with_context(path):
    records = []
    current_folio = 'unknown'
    current_currier = 'unknown'
    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if re.match(r'^<f\w+>', line) and '$' in line:
                fmatch = re.match(r'^<(f\w+)>', line)
                if fmatch:
                    current_folio = fmatch.group(1)
                lmatch = re.search(r'\$L=([AB])', line)
                if lmatch:
                    current_currier = lmatch.group(1)
                continue
            if line.startswith('#'):
                continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus, text = m.group(1), m.group(2)
            locus_clean = re.sub(r'^[^A-Za-z]+', '', locus)
            cat_char = locus_clean[0].upper() if locus_clean else '?'
            category = LOCUS_CATEGORIES.get(cat_char, 'other')
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'@\d+;?', '', text)
            raw_words = re.split(r'[.\s]+', text)
            for w in raw_words:
                if w and re.match(r'^[a-zA-Z]+$', w):
                    records.append({
                        'folio': current_folio,
                        'section': classify_section(current_folio),
                        'currier': current_currier,
                        'locus': category,
                        'word': w,
                    })
    return records


def shannon_entropy(items):
    c = Counter(items)
    total = sum(c.values())
    if total == 0:
        return 0.0
    return -sum((v/total)*math.log2(v/total) for v in c.values())


def bigram_conditional_entropy(chars):
    if len(chars) < 2:
        return 0.0
    bigrams = [(chars[i], chars[i+1]) for i in range(len(chars)-1)]
    return shannon_entropy(bigrams) - shannon_entropy(chars)


def positional_entropy_from_start(words, max_pos=9, min_words=50):
    results = []
    for pos in range(max_pos):
        chars_at = [w[pos] for w in words if len(w) > pos]
        if len(chars_at) < min_words:
            break
        results.append((pos, shannon_entropy(chars_at), len(chars_at)))
    return results


def positional_entropy_from_end(words, max_pos=6, min_words=50):
    results = []
    for pos in range(1, max_pos+1):
        chars_at = [w[-pos] for w in words if len(w) >= pos]
        if len(chars_at) < min_words:
            break
        results.append((pos, shannon_entropy(chars_at), len(chars_at)))
    return results


def mutual_information_word_currier(records_body):
    """
    Compute MI between word identity and Currier label.
    MI(W; C) = H(W) - H(W|C)
    A high MI means word choice is strongly predictive of Currier language.
    """
    words = [r['word'] for r in records_body]
    H_w = shannon_entropy(words)

    by_lang = defaultdict(list)
    for r in records_body:
        by_lang[r['currier']].append(r['word'])

    total = len(words)
    H_w_given_c = 0.0
    for lang, lang_words in by_lang.items():
        p_lang = len(lang_words) / total
        H_w_given_c += p_lang * shannon_entropy(lang_words)

    mi = H_w - H_w_given_c
    return H_w, H_w_given_c, mi


def vocabulary_analysis(words_a, words_b, top_n=20):
    """Analyze vocabulary differences between two subcorpora."""
    freq_a = Counter(words_a)
    freq_b = Counter(words_b)
    all_words = set(words_a) | set(words_b)
    total_a = len(words_a)
    total_b = len(words_b)

    # Words significantly skewed toward A or B
    # Use ratio of normalized frequencies
    a_specific = []
    b_specific = []
    for w in all_words:
        fa = freq_a.get(w, 0) / total_a
        fb = freq_b.get(w, 0) / total_b
        if fa + fb < 1e-5:
            continue
        ratio = (fa + 1e-6) / (fb + 1e-6)
        if ratio > 5:
            a_specific.append((w, fa, fb, ratio, freq_a[w]))
        elif ratio < 0.2:
            b_specific.append((w, fa, fb, ratio, freq_b[w]))

    a_specific.sort(key=lambda x: -x[4])  # sort by raw count in A
    b_specific.sort(key=lambda x: -x[4])  # sort by raw count in B

    return a_specific[:top_n], b_specific[:top_n]


if __name__ == "__main__":
    print("Experiment exp_005: Currier A vs B Subcorpus Comparison")
    print("Date: 2026-04-09\n")

    records = parse_eva_with_context(BASE / 'data/transcriptions/eva_zl3b.txt')
    body_records = [r for r in records if r['locus'] == 'body']
    A_records = [r for r in body_records if r['currier'] == 'A']
    B_records = [r for r in body_records if r['currier'] == 'B']

    words_A = [r['word'] for r in A_records]
    words_B = [r['word'] for r in B_records]

    print(f"Currier A body words: {len(words_A):,}")
    print(f"Currier B body words: {len(words_B):,}")

    # ── Basic entropy comparison ──
    print("\n" + "="*60)
    print("BASIC ENTROPY COMPARISON: A vs B")
    print("="*60)
    for lang, words in [('A', words_A), ('B', words_B)]:
        chars = list(''.join(words))
        h1 = shannon_entropy(chars)
        h2 = bigram_conditional_entropy(chars)
        h_init = shannon_entropy([w[0] for w in words])
        h_final = shannon_entropy([w[-1] for w in words])
        ttr = len(set(words)) / max(len(words), 1)
        avg_len = sum(len(w) for w in words) / max(len(words), 1)
        print(f"\n  Currier {lang}: {len(words):,} tokens, {len(set(words)):,} types")
        print(f"    TTR: {ttr:.4f}  Avg word len: {avg_len:.2f}")
        print(f"    H1: {h1:.4f}  H2: {h2:.4f}  H_init: {h_init:.4f}  H_final: {h_final:.4f}")

    # ── Mutual information ──
    print("\n" + "="*60)
    print("MUTUAL INFORMATION: WORD IDENTITY vs CURRIER LANGUAGE")
    print("="*60)
    H_w, H_w_given_c, mi = mutual_information_word_currier(body_records)
    print(f"  H(word) = {H_w:.4f} bits")
    print(f"  H(word | currier) = {H_w_given_c:.4f} bits")
    print(f"  MI(word; currier) = {mi:.4f} bits")
    print(f"  MI as fraction of H(word): {mi/H_w*100:.1f}%")

    # ── Vocabulary A-specific and B-specific words ──
    print("\n" + "="*60)
    print("VOCABULARY SPECIFICITY: Words strongly associated with A or B")
    print("="*60)
    a_words, b_words = vocabulary_analysis(words_A, words_B)
    print(f"\n  TOP A-SPECIFIC WORDS (freq ratio A/B > 5:1):")
    print(f"  {'Word':<12} {'%inA':>6} {'%inB':>6} {'Ratio':>7} {'CountA':>7}")
    for w, fa, fb, ratio, cnt in a_words[:15]:
        print(f"  {w:<12} {100*fa:>6.2f} {100*fb:>6.2f} {ratio:>7.1f}x {cnt:>7}")

    print(f"\n  TOP B-SPECIFIC WORDS (freq ratio B/A > 5:1):")
    print(f"  {'Word':<12} {'%inB':>6} {'%inA':>6} {'Ratio':>7} {'CountB':>7}")
    for w, fa, fb, ratio, cnt in b_words[:15]:
        print(f"  {w:<12} {100*fb:>6.2f} {100*fa:>6.2f} {1/ratio:>7.1f}x {cnt:>7}")

    # ── Positional entropy comparison: A vs B ──
    print("\n" + "="*60)
    print("POSITIONAL ENTROPY: A vs B (from start)")
    print("="*60)
    a_pos = positional_entropy_from_start(words_A)
    b_pos = positional_entropy_from_start(words_B)
    fmt = "{:<6} {:>10} {:>10}"
    print(fmt.format("Pos", "Currier_A", "Currier_B"))
    for i, (pos, h_a, _) in enumerate(a_pos):
        h_b = b_pos[i][1] if i < len(b_pos) else float('nan')
        print(fmt.format(pos, f"{h_a:.4f}", f"{h_b:.4f}"))

    print("\nPositional entropy from END: A vs B")
    a_end = positional_entropy_from_end(words_A)
    b_end = positional_entropy_from_end(words_B)
    for i, (pos, h_a, _) in enumerate(a_end):
        h_b = b_end[i][1] if i < len(b_end) else float('nan')
        print(f"  pos -{pos}: A={h_a:.4f}  B={h_b:.4f}")

    # ── Word length distributions ──
    print("\n" + "="*60)
    print("WORD LENGTH DISTRIBUTION: A vs B")
    print("="*60)
    len_a = Counter(len(w) for w in words_A)
    len_b = Counter(len(w) for w in words_B)
    total_a = len(words_A)
    total_b = len(words_B)
    print(f"  {'Length':>7}  {'A%':>6}  {'B%':>6}")
    for length in range(1, 14):
        pa = 100 * len_a.get(length, 0) / total_a
        pb = 100 * len_b.get(length, 0) / total_b
        print(f"  {length:>7}  {pa:>6.1f}  {pb:>6.1f}")

    # ── Character unigram comparison: KL divergence ──
    print("\n" + "="*60)
    print("CHARACTER DISTRIBUTION COMPARISON (KL divergence A→B and B→A)")
    print("="*60)
    chars_A = Counter(''.join(words_A))
    chars_B = Counter(''.join(words_B))
    total_ca = sum(chars_A.values())
    total_cb = sum(chars_B.values())
    all_chars = set(chars_A.keys()) | set(chars_B.keys())

    kl_ab = sum((chars_A.get(c, 0)/total_ca) * math.log2((chars_A.get(c, 0)/total_ca + 1e-10) /
                                                            (chars_B.get(c, 0)/total_cb + 1e-10))
               for c in all_chars if chars_A.get(c, 0) > 0)
    kl_ba = sum((chars_B.get(c, 0)/total_cb) * math.log2((chars_B.get(c, 0)/total_cb + 1e-10) /
                                                            (chars_A.get(c, 0)/total_ca + 1e-10))
               for c in all_chars if chars_B.get(c, 0) > 0)
    print(f"  KL(A||B) = {kl_ab:.4f} bits")
    print(f"  KL(B||A) = {kl_ba:.4f} bits")
    print(f"  Symmetric KL = {(kl_ab+kl_ba)/2:.4f} bits")

    print(f"\n  Character frequency table (sorted by A frequency):")
    print(f"  {'Char':>5} {'A%':>6} {'B%':>6} {'Diff':>7}")
    sorted_chars = sorted(all_chars, key=lambda c: -chars_A.get(c,0)/total_ca)
    for c in sorted_chars[:20]:
        pa = chars_A.get(c, 0) / total_ca
        pb = chars_B.get(c, 0) / total_cb
        print(f"  {repr(c):>5} {100*pa:>6.2f} {100*pb:>6.2f} {100*(pa-pb):>+7.2f}")

    print("\nDone.")
