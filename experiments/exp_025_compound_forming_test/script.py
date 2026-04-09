"""
Experiment: exp_025_compound_forming_test
Hypothesis: H022
Goal: Test whether f66r column 2's presence/absence of EVA single characters has
a statistically significant anti-correlation with "compound-forming" frequency.

Operationalization: For each of the 25 EVA single chars, compute:
  - compound_rate = (times char appears inside a known compound) / (total occurrences)
  - in_col2 = 1 if char appears in f66r column 2, 0 if not

Test: do chars with high compound_rate have in_col2=0? (Fisher's exact test)
"""

import re
import math
import json
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path(__file__).resolve().parents[2]
CORPUS = BASE / 'data/transcriptions/eva_zl3b.txt'

# f66r column 2 membership (from exp_012)
# Present (11 types): c d f l o p r s t x y
# Absent: a e g h i k m n q v (and other rare chars)
F66R_COL2_CHARS = set('cdfloprst xy'.split()) | {'c','d','f','l','o','p','r','s','t','x','y'}

# Known compound forms in EVA (bigrams/trigrams that occur as structural units)
# These are standard EVA compound forms with their constituent chars
COMPOUNDS = {
    'ch': ['c', 'h'],   # extremely common
    'sh': ['s', 'h'],
    'ee': ['e', 'e'],
    'aiin': ['a', 'i', 'i', 'n'],
    'ain': ['a', 'i', 'n'],
    'qo': ['q', 'o'],
    'ck': ['c', 'k'],
    'kh': ['k', 'h'],
    'cph': ['c', 'p', 'h'],
    'cth': ['c', 't', 'h'],
    'ckh': ['c', 'k', 'h'],
    'ii': ['i', 'i'],
    'iii': ['i', 'i', 'i'],
    'eee': ['e', 'e', 'e'],
    'iin': ['i', 'i', 'n'],
    'iiin': ['i', 'i', 'i', 'n'],
}

# Which chars primarily appear IN compounds vs standalone?
# We compute: for each char, what fraction of its occurrences are within a compound pattern?
COMPOUND_FORMING_CHARS = {
    'e': ['ee', 'eee'],
    'h': ['ch', 'sh', 'cth', 'ckh', 'cph', 'kh'],
    'a': ['ain', 'aiin'],
    'i': ['ii', 'iii', 'iiin', 'ain', 'aiin', 'iin'],
    'k': ['ck', 'ckh', 'kh'],
    'n': ['ain', 'aiin', 'iin', 'iiin'],
    'q': ['qo'],
}


def parse_body_words(path):
    """Extract all body text word tokens from ZL3b."""
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
            text = re.sub(r'\[[^\]]+\]', 'X', text)
            raw_words = re.split(r'[.\s,]+', text)
            for w in raw_words:
                w = w.strip()
                if w and re.match(r'^[a-z]', w):
                    words.append(w)
    return words


def count_compound_occurrences(words, compound_patterns):
    """For each char, count total occurrences and occurrences inside compounds."""
    total_char = Counter()
    in_compound = Counter()

    for word in words:
        # Mark positions covered by each compound
        covered = [False] * len(word)
        # Find all compound occurrences in the word (longest match first)
        for compound in sorted(compound_patterns, key=len, reverse=True):
            for i in range(len(word) - len(compound) + 1):
                if word[i:i+len(compound)] == compound:
                    for j in range(i, i+len(compound)):
                        covered[j] = True

        # Count each char
        for i, ch in enumerate(word):
            if re.match(r'[a-z]', ch):
                total_char[ch] += 1
                if covered[i]:
                    in_compound[ch] += 1

    return total_char, in_compound


def fisher_exact_2x2(a, b, c, d):
    """Fisher's exact test for 2x2 table (one-tailed, testing positive association).
    a = compound-forming AND in_col2
    b = compound-forming AND NOT in_col2
    c = not compound-forming AND in_col2
    d = not compound-forming AND NOT in_col2
    Tests H1: compound-forming chars are less likely to be in col2.
    Returns: odds ratio, p-value (one-tailed, less likely)
    """
    n = a + b + c + d
    # Hypergeometric: P(X <= a) where X = number of compound-forming chars in col2
    # X ~ HyperGeometric(N=n, K=a+b, n=a+c)
    K = a + b  # compound-forming total
    n_draw = a + c  # in col2 total
    # P(X <= a) = sum_{i=0}^{a} C(K,i)*C(n-K, n_draw-i) / C(n, n_draw)
    p = 0.0
    for i in range(a + 1):
        try:
            p += math.comb(K, i) * math.comb(n-K, n_draw-i) / math.comb(n, n_draw)
        except ValueError:
            pass
    if a + b == 0 or a + c == 0:
        odds = float('inf')
    else:
        odds = (a * d) / (b * c) if b > 0 and c > 0 else float('inf')
    return odds, p


if __name__ == "__main__":
    print("Experiment exp_025: Compound-Forming Character Test (H022)")
    print("Date: 2026-04-09\n")

    words = parse_body_words(CORPUS)
    print(f"Total body text words: {len(words):,}")

    compound_patterns = list(COMPOUNDS.keys())
    total_char, in_compound = count_compound_occurrences(words, compound_patterns)

    print(f"\n=== Compound-Forming Rate per Character ===")
    print(f"{'Char':<6} {'Total':>8} {'In compound':>12} {'Rate':>8} {'In f66r col2':>13} {'Compound-forming?':>18}")
    print("-" * 70)

    # Classify chars as "compound-forming" if compound rate > 50%
    char_data = []
    for ch in sorted(total_char.keys()):
        if total_char[ch] < 10:  # skip very rare chars
            continue
        total = total_char[ch]
        in_cpd = in_compound.get(ch, 0)
        rate = in_cpd / total
        in_col2 = 1 if ch in F66R_COL2_CHARS else 0
        is_compound_forming = 1 if rate > 0.4 else 0  # threshold: >40% compound
        char_data.append({
            'char': ch, 'total': total, 'in_compound': in_cpd, 'rate': rate,
            'in_col2': in_col2, 'is_compound_forming': is_compound_forming
        })
        print(f"  {ch:<5} {total:>8,} {in_cpd:>12,} {rate:>8.3f} {'YES':>13} {'COMPOUND':>18}"
              if in_col2 and is_compound_forming else
              f"  {ch:<5} {total:>8,} {in_cpd:>12,} {rate:>8.3f} {'YES':>13} {'-':>18}"
              if in_col2 else
              f"  {ch:<5} {total:>8,} {in_cpd:>12,} {rate:>8.3f} {'NO':>13} {'COMPOUND':>18}"
              if is_compound_forming else
              f"  {ch:<5} {total:>8,} {in_cpd:>12,} {rate:>8.3f} {'NO':>13} {'-':>18}")

    # Build 2x2 table: compound-forming vs in_col2
    print(f"\n=== 2x2 Contingency Table: Compound-Forming vs In f66r Col2 ===")
    a = sum(1 for d in char_data if d['is_compound_forming'] and d['in_col2'])
    b = sum(1 for d in char_data if d['is_compound_forming'] and not d['in_col2'])
    c = sum(1 for d in char_data if not d['is_compound_forming'] and d['in_col2'])
    d = sum(1 for d in char_data if not d['is_compound_forming'] and not d['in_col2'])

    print(f"{'':>20} {'In f66r col2':>15} {'Not in f66r col2':>18}")
    print(f"  {'Compound-forming':<18} {a:>15} {b:>18}")
    print(f"  {'Standalone':<18} {c:>15} {d:>18}")

    odds, p = fisher_exact_2x2(a, b, c, d)
    print(f"\nFisher exact test (one-tailed, compound chars LESS likely in col2):")
    print(f"  Odds ratio: {odds:.3f}" if isinstance(odds, float) else f"  Odds ratio: inf")
    print(f"  P-value: {p:.6f}")

    # Rank chars by compound rate
    print(f"\n=== Summary: Clear Pattern? ===")
    char_data.sort(key=lambda x: -x['rate'])
    print("Chars by compound rate (high → low), with col2 membership:")
    for d in char_data:
        marker = "IN_COL2" if d['in_col2'] else "ABSENT"
        print(f"  '{d['char']}': compound_rate={d['rate']:.3f} → {marker}")

    # Expected vs actual
    compound_forming_set = {d['char'] for d in char_data if d['is_compound_forming']}
    standalone_set = {d['char'] for d in char_data if not d['is_compound_forming']}
    col2_set = {d['char'] for d in char_data if d['in_col2']}

    print(f"\n  Compound-forming chars: {sorted(compound_forming_set)}")
    print(f"  Standalone chars: {sorted(standalone_set)}")
    print(f"  Chars in f66r col2: {sorted(col2_set)}")
    print(f"  Compound-forming IN col2: {sorted(compound_forming_set & col2_set)}")
    print(f"  Standalone IN col2: {sorted(standalone_set & col2_set)}")
    print(f"  Compound-forming ABSENT from col2: {sorted(compound_forming_set - col2_set)}")

    # Save
    output = {
        'char_data': char_data,
        'contingency': {'a': a, 'b': b, 'c': c, 'd': d},
        'fisher_p': round(p, 6),
        'fisher_odds': round(odds, 3) if isinstance(odds, float) and odds != float('inf') else None,
        'compound_forming_set': sorted(compound_forming_set),
        'standalone_set': sorted(standalone_set),
        'col2_set': sorted(col2_set),
    }
    out_path = Path(__file__).parent / 'data.json'
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")
    print("Done.")
