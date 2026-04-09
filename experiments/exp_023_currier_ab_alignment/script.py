"""
Experiment: exp_023_currier_ab_alignment
Hypothesis: H004
Goal: Test whether Currier A and B subcorpora represent the same system by:
1. Shared vocabulary analysis (what words appear in both vs exclusively)
2. Frequency rank Spearman correlation for shared vocabulary
3. Co-occurrence context vector alignment (top-N words)
4. Proportion of aligned pairs that are identical tokens vs. cross-aligned

If A and B encode the same underlying content, aligned words should be
identical tokens (same Voynich word = same meaning in both dialects).
If different systems, alignment should fail (cross-aligning different tokens).
"""

import re
import math
import json
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path(__file__).resolve().parents[2]
CORPUS = BASE / 'data/transcriptions/eva_zl3b.txt'


def parse_currier_words(path):
    """Parse body text words from ZL3b, tagged by Currier dialect (A/B)."""
    words_a = []
    words_b = []
    current_currier = None

    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Folio header — extract Currier tag
            if re.match(r'^<f\w+>', line) and '$' in line:
                m = re.search(r'\$L=([AB])', line)
                if m:
                    current_currier = m.group(1)
            # Body text line
            m = re.match(r'^<([^>]+),([^>]+P\d)>\s*(.*)', line)
            if not m:
                continue
            text = m.group(3)
            # Strip metadata
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            # Tokenize on dots, spaces, commas
            raw_words = re.split(r'[.\s,]+', text)
            words = []
            for w in raw_words:
                w = w.strip()
                if not w or w.startswith('@') and len(w) < 3:
                    continue
                # Normalize: lowercase, strip uncertainty brackets
                w = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', w)
                if re.match(r'^[a-zA-Z]{2,}', w):
                    words.append(w.lower())
            if current_currier == 'A':
                words_a.extend(words)
            elif current_currier == 'B':
                words_b.extend(words)

    return words_a, words_b


def cosine_sim(vec_a, vec_b, vocab):
    """Cosine similarity between two Counter-based vectors over vocab."""
    dot = sum(vec_a.get(v, 0) * vec_b.get(v, 0) for v in vocab)
    mag_a = math.sqrt(sum(v**2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v**2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def build_context_vectors(word_list, target_words, window=2):
    """Build co-occurrence context vectors for each target word.
    Context = counts of words appearing within ±window positions."""
    n = len(word_list)
    vectors = defaultdict(Counter)
    for i, word in enumerate(word_list):
        if word not in target_words:
            continue
        for j in range(max(0, i-window), min(n, i+window+1)):
            if j != i and word_list[j] in target_words:
                vectors[word][word_list[j]] += 1
    return dict(vectors)


def spearman_rho(x, y):
    """Compute Spearman rank correlation between two equal-length lists."""
    n = len(x)
    if n < 3:
        return 0.0, 1.0

    def rank(lst):
        sorted_lst = sorted(enumerate(lst), key=lambda t: t[1])
        ranks = [0] * n
        for rank_val, (idx, _) in enumerate(sorted_lst, 1):
            ranks[idx] = rank_val
        return ranks

    rx = rank(x)
    ry = rank(y)
    d_sq = sum((rx[i] - ry[i])**2 for i in range(n))
    rho = 1 - 6 * d_sq / (n * (n**2 - 1))
    # Approximate t-statistic
    t = rho * math.sqrt((n - 2) / max(1e-10, 1 - rho**2))
    return rho, t


if __name__ == "__main__":
    print("Experiment exp_023: Currier A vs B Unsupervised Alignment")
    print("Hypothesis: H004")
    print("Date: 2026-04-09\n")

    words_a, words_b = parse_currier_words(CORPUS)
    freq_a = Counter(words_a)
    freq_b = Counter(words_b)

    print(f"Currier A: {len(words_a):,} tokens, {len(freq_a):,} types")
    print(f"Currier B: {len(words_b):,} tokens, {len(freq_b):,} types")

    # 1. Vocabulary overlap
    vocab_a = set(freq_a.keys())
    vocab_b = set(freq_b.keys())
    shared = vocab_a & vocab_b
    only_a = vocab_a - vocab_b
    only_b = vocab_b - vocab_a

    print(f"\n=== Vocabulary Overlap ===")
    print(f"  Shared types: {len(shared):,}")
    print(f"  Only in A: {len(only_a):,}")
    print(f"  Only in B: {len(only_b):,}")
    print(f"  Jaccard (types): {len(shared)/len(vocab_a|vocab_b):.3f}")

    # Tokens in shared vs exclusive vocab
    tok_a_shared = sum(freq_a[w] for w in shared)
    tok_b_shared = sum(freq_b[w] for w in shared)
    print(f"  A tokens in shared vocab: {tok_a_shared:,} / {len(words_a):,} = {100*tok_a_shared/len(words_a):.1f}%")
    print(f"  B tokens in shared vocab: {tok_b_shared:,} / {len(words_b):,} = {100*tok_b_shared/len(words_b):.1f}%")

    # 2. Top-N words in each dialect
    top_a = freq_a.most_common(50)
    top_b = freq_b.most_common(50)
    set_top_a = {w for w, _ in top_a}
    set_top_b = {w for w, _ in top_b}

    print(f"\n=== Top-50 Word Overlap ===")
    top_shared = set_top_a & set_top_b
    print(f"  Words in BOTH top-50 lists: {len(top_shared)}")
    print(f"  Shared top words: {sorted(top_shared)}")
    print(f"  Only in A top-50: {sorted(set_top_a - set_top_b)}")
    print(f"  Only in B top-50: {sorted(set_top_b - set_top_a)}")

    print(f"\n  Top 20 A: {[w for w,_ in top_a[:20]]}")
    print(f"  Top 20 B: {[w for w,_ in top_b[:20]]}")

    # 3. Frequency rank correlation for shared top-200 words
    top200_a = {w: r for r, (w, _) in enumerate(freq_a.most_common(200), 1)}
    top200_b = {w: r for r, (w, _) in enumerate(freq_b.most_common(200), 1)}
    shared_top200 = set(top200_a.keys()) & set(top200_b.keys())

    print(f"\n=== Frequency Rank Correlation (top-200 of each, shared={len(shared_top200)}) ===")
    if len(shared_top200) >= 5:
        shared_list = sorted(shared_top200)
        ranks_a = [top200_a[w] for w in shared_list]
        ranks_b = [top200_b[w] for w in shared_list]
        rho, t = spearman_rho(ranks_a, ranks_b)
        print(f"  Spearman ρ (rank in A vs rank in B): {rho:.3f}, t={t:.2f}")
        print(f"  (ρ≈1 means A and B rank shared words the same; ρ≈0 means opposite rank ordering)")

    # 4. Context vector alignment (top-100 words combined)
    top100_a = {w for w, _ in freq_a.most_common(100)}
    top100_b = {w for w, _ in freq_b.most_common(100)}
    target_all = top100_a | top100_b

    print(f"\n=== Context Vector Alignment (top-100 per dialect) ===")
    print(f"  Building A context vectors on {len(words_a):,} tokens...")
    ctx_a = build_context_vectors(words_a, target_all, window=2)
    print(f"  Building B context vectors on {len(words_b):,} tokens...")
    ctx_b = build_context_vectors(words_b, target_all, window=2)

    # Context vocab = all context words that appear in both dialects
    ctx_vocab = set()
    for v in ctx_a.values():
        ctx_vocab |= set(v.keys())
    for v in ctx_b.values():
        ctx_vocab |= set(v.keys())

    # Compute similarity matrix for top-100 A words vs top-100 B words
    top100_a_list = [w for w, _ in freq_a.most_common(100)]
    top100_b_list = [w for w, _ in freq_b.most_common(100)]

    # Greedy alignment: for each A word, find best matching B word
    alignment = {}
    sim_scores = {}
    used_b = set()

    for w_a in top100_a_list:
        vec_a = ctx_a.get(w_a, Counter())
        best_b, best_sim = None, -1
        for w_b in top100_b_list:
            if w_b in used_b:
                continue
            vec_b = ctx_b.get(w_b, Counter())
            sim = cosine_sim(vec_a, vec_b, ctx_vocab)
            if sim > best_sim:
                best_sim = sim
                best_b = w_b
        if best_b is not None:
            alignment[w_a] = best_b
            sim_scores[w_a] = best_sim
            used_b.add(best_b)

    # Alignment quality metrics
    identical_pairs = [(a, b) for a, b in alignment.items() if a == b]
    n_identical = len(identical_pairs)
    n_aligned = len(alignment)
    mean_sim = sum(sim_scores.values()) / len(sim_scores) if sim_scores else 0

    print(f"\n  Greedy alignment results:")
    print(f"  Total aligned pairs: {n_aligned}")
    print(f"  Identical token pairs (A word == B word): {n_identical} / {n_aligned} = {100*n_identical/n_aligned:.1f}%")
    print(f"  Mean cosine similarity of aligned pairs: {mean_sim:.4f}")
    print(f"  Null expectation (random alignment): ~{100*len(top_shared)/100:.1f}% identical if shared vocab randomly distributed")

    print(f"\n  Top aligned pairs (highest cosine similarity):")
    sorted_pairs = sorted(alignment.items(), key=lambda kv: sim_scores[kv[0]], reverse=True)
    for a, b in sorted_pairs[:25]:
        marker = "==IDENTICAL==" if a == b else ""
        print(f"    A:'{a}' → B:'{b}' (sim={sim_scores[a]:.4f}) {marker}")

    print(f"\n  All identical aligned pairs:")
    for a, b in identical_pairs:
        rank_a = top200_a.get(a, '?')
        rank_b = top200_b.get(b, '?')
        freq_a_word = freq_a.get(a, 0)
        freq_b_word = freq_b.get(b, 0)
        print(f"    '{a}': A rank={rank_a} (freq={freq_a_word}), B rank={rank_b} (freq={freq_b_word})")

    # 5. Most A-exclusive and B-exclusive high-frequency words
    print(f"\n=== High-Frequency Dialect-Exclusive Words ===")
    # Words in top-200 A but not top-200 B
    a_exclusive = [(w, freq_a[w]) for w in top200_a if w not in top200_b]
    a_exclusive.sort(key=lambda x: -x[1])
    print(f"  A-exclusive top words (not in B's top-200): {a_exclusive[:15]}")

    b_exclusive = [(w, freq_b[w]) for w in top200_b if w not in top200_a]
    b_exclusive.sort(key=lambda x: -x[1])
    print(f"  B-exclusive top words (not in A's top-200): {b_exclusive[:15]}")

    # Save results
    output = {
        'currier_a_tokens': len(words_a),
        'currier_b_tokens': len(words_b),
        'currier_a_types': len(freq_a),
        'currier_b_types': len(freq_b),
        'shared_types': len(shared),
        'only_a_types': len(only_a),
        'only_b_types': len(only_b),
        'vocab_jaccard': round(len(shared)/len(vocab_a|vocab_b), 4),
        'top50_shared_count': len(top_shared),
        'top50_shared': sorted(top_shared),
        'top50_only_a': sorted(set_top_a - set_top_b),
        'top50_only_b': sorted(set_top_b - set_top_a),
        'top_shared200': len(shared_top200),
        'rank_corr_rho': round(rho, 4) if 'rho' in dir() else None,
        'rank_corr_t': round(t, 3) if 't' in dir() else None,
        'alignment_identical_count': n_identical,
        'alignment_identical_pct': round(100*n_identical/n_aligned, 1),
        'alignment_mean_sim': round(mean_sim, 4),
        'identical_pairs': identical_pairs,
        'top_aligned_pairs': [(a, b, round(sim_scores[a], 4)) for a, b in sorted_pairs[:25]],
        'a_exclusive_top15': a_exclusive[:15],
        'b_exclusive_top15': b_exclusive[:15],
    }

    out_path = Path(__file__).parent / 'data.json'
    with open(out_path, 'w') as fj:
        json.dump(output, fj, indent=2)
    print(f"\nSaved to {out_path}")
    print("Done.")
