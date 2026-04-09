"""
Experiment: exp_024_lingua_ignota
Hypothesis: H005
Goal: Compare phonotactic profiles of Voynichese and Hildegard's Lingua Ignota.
Metrics: word-initial entropy, word-length distribution, suffix/onset constraint.

NOTE: Only the first 30+ words of Lingua Ignota are publicly available.
Full 1011-word list is in Higley (2007) scholarly edition (print only).
This experiment uses the available sample and notes where full data would change results.
"""

import re
import math
import json
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parents[2]
CORPUS = BASE / 'data/transcriptions/eva_zl3b.txt'

# Lingua Ignota word list — all publicly documented words
# Sources: Wikipedia, HandWiki (first 30 from glossary), libarynth/Higley sentence examples
LINGUA_IGNOTA_WORDS = [
    # First 30 from glossary (Riesencodex, entries 1-30)
    'aigonz', 'aieganz', 'zuuenz', 'liuionz', 'diueliz',
    'ispariz', 'inimois', 'jur', 'vanix', 'peuearrez',
    'korzinthio', 'falschin', 'sonziz', 'linschiol', 'zanziuer',
    'vrizoil', 'jugiza', 'pangizo', 'kulzphazur', 'phazur',
    'peueriz', 'maiz', 'hilzpeueriz', 'hilzmaiz', 'scirizin',
    'hilzscifriz', 'limzkil', 'zains', 'zunzial', 'bischiniz',
    # Additional attested words from Hildegard's own sentence usage
    'orzchis', 'caldemia', 'loifol', 'crizanta', 'chorzta',
]

LINGUA_IGNOTA_N = 1011  # total documented words (Higley 2007)
SAMPLE_N = len(LINGUA_IGNOTA_WORDS)


def entropy(counter):
    total = sum(counter.values())
    if total == 0:
        return 0.0
    return -sum((c/total) * math.log2(c/total) for c in counter.values() if c > 0)


def parse_voynich_words(path):
    """Extract all body text words from ZL3b."""
    words = []
    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            m = re.match(r'^<([^>]+),([^>]*P\d)>\s*(.*)', line)
            if not m:
                continue
            text = m.group(3)
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            raw_words = re.split(r'[.\s,]+', text)
            for w in raw_words:
                w = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', w)
                w = w.strip()
                if w and len(w) >= 2 and re.match(r'^[a-z]', w):
                    words.append(w)
    return words


def parse_reference_words(path, min_len=2):
    """Extract words from a reference text corpus."""
    words = []
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            raw = re.findall(r'[a-zA-Z]+', line.lower())
            words.extend(w for w in raw if len(w) >= min_len)
    return words


if __name__ == "__main__":
    print("Experiment exp_024: Lingua Ignota Phonotactic Comparison")
    print("Hypothesis: H005")
    print("Date: 2026-04-09\n")

    print(f"Note: Using {SAMPLE_N}/{LINGUA_IGNOTA_N} documented Lingua Ignota words")
    print(f"(Full list only in Higley 2007 scholarly edition, not publicly available)\n")

    # === Lingua Ignota Analysis ===
    li_words = LINGUA_IGNOTA_WORDS

    li_lengths = Counter(len(w) for w in li_words)
    li_initials = Counter(w[0] for w in li_words if w)
    li_finals = Counter(w[-1] for w in li_words if w)

    # Bigrams (within word)
    li_bigrams = Counter()
    for w in li_words:
        for i in range(len(w) - 1):
            li_bigrams[w[i:i+2]] += 1

    print(f"=== Lingua Ignota (sample n={SAMPLE_N}) ===")
    print(f"Word lengths: {dict(sorted(li_lengths.items()))}")
    print(f"Mean length: {sum(len(w) for w in li_words)/len(li_words):.2f}")
    print(f"Min: {min(len(w) for w in li_words)}, Max: {max(len(w) for w in li_words)}")
    print(f"Initial char entropy: {entropy(li_initials):.3f} bits")
    print(f"Final char entropy: {entropy(li_finals):.3f} bits")
    print(f"Bigram entropy: {entropy(li_bigrams):.3f} bits")
    print(f"Initial char distribution: {dict(li_initials.most_common(10))}")
    print(f"Final char distribution: {dict(li_finals.most_common(10))}")

    # Top initial chars and coverage
    total_li = len(li_words)
    top4_li_initials = li_initials.most_common(4)
    top4_coverage = sum(c for _, c in top4_li_initials) / total_li
    print(f"Top 4 initials cover: {100*top4_coverage:.1f}% of words")

    # Suffix patterns
    li_suffixes_2 = Counter(w[-2:] for w in li_words if len(w) >= 2)
    li_suffixes_3 = Counter(w[-3:] for w in li_words if len(w) >= 3)
    print(f"Top 5 2-char suffixes: {li_suffixes_2.most_common(5)}")
    print(f"Top 5 3-char suffixes: {li_suffixes_3.most_common(5)}")

    # === Voynich Analysis ===
    print(f"\n=== Voynich (ZL3b body text) ===")
    voynich_words = parse_voynich_words(CORPUS)
    print(f"Total words: {len(voynich_words):,}")

    v_lengths = Counter(len(w) for w in voynich_words)
    v_initials = Counter(w[0] for w in voynich_words if w)
    v_finals = Counter(w[-1] for w in voynich_words if w)
    v_bigrams = Counter()
    for w in voynich_words:
        for i in range(len(w) - 1):
            v_bigrams[w[i:i+2]] += 1

    print(f"Mean length: {sum(len(w) for w in voynich_words)/len(voynich_words):.2f}")
    print(f"Initial char entropy: {entropy(v_initials):.3f} bits")
    print(f"Final char entropy: {entropy(v_finals):.3f} bits")
    print(f"Bigram entropy: {entropy(v_bigrams):.3f} bits")
    print(f"Initial char distribution (top 6): {dict(v_initials.most_common(6))}")
    print(f"Final char distribution (top 6): {dict(v_finals.most_common(6))}")

    top4_v_initials = v_initials.most_common(4)
    top4_v_coverage = sum(c for _, c in top4_v_initials) / len(voynich_words)
    print(f"Top 4 initials cover: {100*top4_v_coverage:.1f}% of words")
    top4_li = [ch for ch, _ in top4_li_initials]
    top4_v = [ch for ch, _ in top4_v_initials]
    print(f"Top 4 Voynich initials: {top4_v}")
    print(f"Top 4 Lingua Ignota initials: {top4_li}")

    v_suffixes_2 = Counter(w[-2:] for w in voynich_words if len(w) >= 2)
    v_suffixes_3 = Counter(w[-3:] for w in voynich_words if len(w) >= 3)
    print(f"Top 5 2-char Voynich suffixes: {v_suffixes_2.most_common(5)}")
    print(f"Top 5 3-char Voynich suffixes: {v_suffixes_3.most_common(5)}")

    # === Latin Reference ===
    print(f"\n=== Latin Reference (Virgil+Caesar) ===")
    latin_path = BASE / 'data/reference_corpora/latin/virgil_aeneid_latin.txt'
    latin_words = parse_reference_words(latin_path)
    print(f"Total words: {len(latin_words):,}")
    l_initials = Counter(w[0] for w in latin_words if w)
    l_finals = Counter(w[-1] for w in latin_words if w)
    l_bigrams = Counter()
    for w in latin_words:
        for i in range(len(w) - 1):
            l_bigrams[w[i:i+2]] += 1

    print(f"Mean length: {sum(len(w) for w in latin_words)/len(latin_words):.2f}")
    print(f"Initial char entropy: {entropy(l_initials):.3f} bits")
    print(f"Final char entropy: {entropy(l_finals):.3f} bits")
    print(f"Bigram entropy: {entropy(l_bigrams):.3f} bits")
    top4_l_initials = l_initials.most_common(4)
    top4_l_coverage = sum(c for _, c in top4_l_initials) / len(latin_words)
    print(f"Top 4 initials cover: {100*top4_l_coverage:.1f}% of words")

    # === German Reference ===
    print(f"\n=== German Reference (Goethe Faust) ===")
    german_path = BASE / 'data/reference_corpora/german/goethe_faust.txt'
    german_words = parse_reference_words(german_path)
    print(f"Total words: {len(german_words):,}")
    g_initials = Counter(w[0] for w in german_words if w)
    g_finals = Counter(w[-1] for w in german_words if w)
    g_bigrams = Counter()
    for w in german_words:
        for i in range(len(w) - 1):
            g_bigrams[w[i:i+2]] += 1

    print(f"Mean length: {sum(len(w) for w in german_words)/len(german_words):.2f}")
    print(f"Initial char entropy: {entropy(g_initials):.3f} bits")
    print(f"Final char entropy: {entropy(g_finals):.3f} bits")
    print(f"Bigram entropy: {entropy(g_bigrams):.3f} bits")
    top4_g_initials = g_initials.most_common(4)
    top4_g_coverage = sum(c for _, c in top4_g_initials) / len(german_words)
    print(f"Top 4 initials cover: {100*top4_g_coverage:.1f}% of words")

    # === Comparison Table ===
    print(f"\n=== Comparison Table ===")
    print(f"{'Metric':<35} {'Lingua Ignota':>14} {'Voynich':>9} {'Latin':>7} {'German':>8}")
    print(f"{'─'*75}")

    li_h_init = entropy(li_initials)
    v_h_init = entropy(v_initials)
    l_h_init = entropy(l_initials)
    g_h_init = entropy(g_initials)
    print(f"{'Initial char entropy (bits)':<35} {li_h_init:>14.3f} {v_h_init:>9.3f} {l_h_init:>7.3f} {g_h_init:>8.3f}")

    li_h_final = entropy(li_finals)
    v_h_final = entropy(v_finals)
    l_h_final = entropy(l_finals)
    g_h_final = entropy(g_finals)
    print(f"{'Final char entropy (bits)':<35} {li_h_final:>14.3f} {v_h_final:>9.3f} {l_h_final:>7.3f} {g_h_final:>8.3f}")

    li_h_bigram = entropy(li_bigrams)
    v_h_bigram = entropy(v_bigrams)
    l_h_bigram = entropy(l_bigrams)
    g_h_bigram = entropy(g_bigrams)
    print(f"{'Bigram entropy (bits)':<35} {li_h_bigram:>14.3f} {v_h_bigram:>9.3f} {l_h_bigram:>7.3f} {g_h_bigram:>8.3f}")

    li_mean_len = sum(len(w) for w in li_words)/len(li_words)
    v_mean_len = sum(len(w) for w in voynich_words)/len(voynich_words)
    l_mean_len = sum(len(w) for w in latin_words)/len(latin_words)
    g_mean_len = sum(len(w) for w in german_words)/len(german_words)
    print(f"{'Mean word length (chars)':<35} {li_mean_len:>14.2f} {v_mean_len:>9.2f} {l_mean_len:>7.2f} {g_mean_len:>8.2f}")
    print(f"{'Top-4 initials coverage (%)':<35} {100*top4_coverage:>14.1f} {100*top4_v_coverage:>9.1f} {100*top4_l_coverage:>7.1f} {100*top4_g_coverage:>8.1f}")

    # Save results
    output = {
        'sample_note': f'{SAMPLE_N}/{LINGUA_IGNOTA_N} words available (full list in Higley 2007)',
        'lingua_ignota': {
            'n': SAMPLE_N, 'mean_len': round(li_mean_len, 2),
            'h_initial': round(li_h_init, 3), 'h_final': round(li_h_final, 3),
            'h_bigram': round(li_h_bigram, 3),
            'top4_initial_coverage': round(top4_coverage, 4),
            'top_initials': dict(li_initials.most_common(10)),
            'top_finals': dict(li_finals.most_common(10)),
        },
        'voynich': {
            'n': len(voynich_words), 'mean_len': round(v_mean_len, 2),
            'h_initial': round(v_h_init, 3), 'h_final': round(v_h_final, 3),
            'h_bigram': round(v_h_bigram, 3),
            'top4_initial_coverage': round(top4_v_coverage, 4),
            'top_initials': dict(v_initials.most_common(10)),
        },
        'latin': {
            'n': len(latin_words), 'mean_len': round(l_mean_len, 2),
            'h_initial': round(l_h_init, 3), 'h_final': round(l_h_final, 3),
            'h_bigram': round(l_h_bigram, 3),
            'top4_initial_coverage': round(top4_l_coverage, 4),
        },
        'german': {
            'n': len(german_words), 'mean_len': round(g_mean_len, 2),
            'h_initial': round(g_h_init, 3), 'h_final': round(g_h_final, 3),
            'h_bigram': round(g_h_bigram, 3),
            'top4_initial_coverage': round(top4_g_coverage, 4),
        },
    }

    out_path = Path(__file__).parent / 'data.json'
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")
    print("Done.")
