"""
Experiment: exp_006_gallows_grouping
Hypothesis tested: H008 — Gallows-as-group-initiator: treating each gallows character
  and its following character as a single token raises h2 toward natural-language range.
Also: begins H007 (verbose cipher reversal) with adjacent-pair and adjacent-triple groupings.
Data: data/transcriptions/eva_zl3b.txt
Dependencies: numpy (standard)
"""

import re
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

random.seed(42)
BASE = Path(__file__).resolve().parents[2]

# ── EVA character classes ──────────────────────────────────────────────────────
# In EVA, the gallows characters are: t, k, p, f
# Their "bench" variants (gallows + bench): ct, ck, ch, cf -> in EVA: cth, ckh, cph, cfh
# In plain EVA strings after our preprocessing, the gallows characters appear as: t, k, p, f
# The bench+gallows combinations appear as multi-character sequences in raw EVA, but
# in our preprocessing we split on '.' and space, so words like 'cthol' are single tokens.
# Within a word, the gallows chars t, k, p, f are "simple gallows."
# The compound gallows appear as: cth, ckh, cph, cfh (preserved as substrings within words).

SIMPLE_GALLOWS = set('tkpf')

def is_gallows(c):
    return c in SIMPLE_GALLOWS

def is_compound_gallows_start(word, i):
    """Check if position i in word starts a compound gallows (cth, ckh, cph, cfh)."""
    for g in ['cth', 'ckh', 'cph', 'cfh']:
        if word[i:i+len(g)] == g:
            return len(g)
    return 0


# ── Parser ────────────────────────────────────────────────────────────────────

def parse_eva_zl3b(path):
    words = []
    with open(path, encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^<[^>]+,([^>]+)>\s+(.*)', line)
            if not m:
                continue
            locus, text = m.group(1), m.group(2)
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'@\d+;?', '', text)
            raw_words = re.split(r'[.\s]+', text)
            words.extend(w for w in raw_words if w and re.match(r'^[a-zA-Z]+$', w))
    return words


# ── Entropy utilities ──────────────────────────────────────────────────────────

def shannon_entropy(items):
    c = Counter(items)
    total = sum(c.values())
    if total == 0:
        return 0.0
    return -sum((v/total)*math.log2(v/total) for v in c.values())


def bigram_conditional_entropy(tokens):
    if len(tokens) < 2:
        return 0.0
    bigrams = [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
    return shannon_entropy(bigrams) - shannon_entropy(tokens)


def h2_from_words(words):
    """Compute h2 treating the concatenated character stream of all words."""
    chars = list(''.join(words))
    return bigram_conditional_entropy(chars), len(chars)


# ── Grouping schemes ──────────────────────────────────────────────────────────

def group_adjacent_pairs(words):
    """
    Verbose cipher test: merge every pair of adjacent characters within each word.
    If word has odd length, last character is a singleton.
    Returns new "word" list with merged tokens.
    """
    grouped = []
    for w in words:
        tokens = []
        i = 0
        while i < len(w) - 1:
            tokens.append(w[i:i+2])
            i += 2
        if i < len(w):
            tokens.append(w[i])
        grouped.append(tokens)
    return grouped  # list of token-lists (one per word)


def group_adjacent_triples(words):
    """Merge every triple of adjacent characters."""
    grouped = []
    for w in words:
        tokens = []
        i = 0
        while i < len(w) - 2:
            tokens.append(w[i:i+3])
            i += 3
        while i < len(w):
            tokens.append(w[i])
            i += 1
        grouped.append(tokens)
    return grouped


def group_gallows_plus_next(words):
    """
    H008: Treat each simple gallows character (t, k, p, f) plus its immediately
    following character as a single two-character token.
    Everything else is a single-character token.
    """
    grouped = []
    for w in words:
        tokens = []
        i = 0
        while i < len(w):
            if i < len(w) - 1 and is_gallows(w[i]):
                tokens.append(w[i:i+2])  # gallows + next char
                i += 2
            else:
                tokens.append(w[i])
                i += 1
        grouped.append(tokens)
    return grouped


def group_compound_gallows_as_unit(words):
    """
    Alternative: treat compound gallows (cth, ckh, cph, cfh) as single units.
    In our tokenized words, these appear as substrings.
    """
    grouped = []
    for w in words:
        tokens = []
        i = 0
        while i < len(w):
            glen = is_compound_gallows_start(w, i)
            if glen > 0:
                tokens.append(w[i:i+glen])
                i += glen
            elif i < len(w) - 1 and is_gallows(w[i]):
                tokens.append(w[i:i+2])
                i += 2
            else:
                tokens.append(w[i])
                i += 1
        grouped.append(tokens)
    return grouped


def compute_grouped_h2(grouped_words):
    """
    Compute h2 on the token stream from grouped words.
    Tokens within a word are treated as a sequence; word boundaries are preserved.
    """
    all_tokens = []
    for word_tokens in grouped_words:
        all_tokens.extend(word_tokens)
    h_token = shannon_entropy(all_tokens)
    if len(all_tokens) < 2:
        return 0.0, 0, 0
    bigrams = [(all_tokens[i], all_tokens[i+1]) for i in range(len(all_tokens)-1)]
    h_bigram = shannon_entropy(bigrams)
    h2 = h_bigram - h_token
    n_unique_tokens = len(set(all_tokens))
    return h2, len(all_tokens), n_unique_tokens


def compare_grouping(name, words, grouped_fn):
    grouped = grouped_fn(words)
    h2, n_tokens, n_unique = compute_grouped_h2(grouped)
    avg_tokens_per_word = n_tokens / max(len(words), 1)
    print(f"\n  {name}:")
    print(f"    Tokens: {n_tokens:,}  Unique: {n_unique}  Avg/word: {avg_tokens_per_word:.2f}")
    print(f"    H2 (post-grouping): {h2:.4f} bits")
    # Most common tokens
    all_tokens = [t for word_tokens in grouped for t in word_tokens]
    top = Counter(all_tokens).most_common(8)
    print(f"    Top tokens: {[(t, c) for t, c in top]}")
    return h2, n_unique


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Experiment exp_006: Gallows Grouping and Verbose Cipher Tests")
    print("Date: 2026-04-09\n")

    words = parse_eva_zl3b(BASE / 'data/transcriptions/eva_zl3b.txt')
    print(f"Total words: {len(words):,}")

    # Baseline h2 (character level)
    baseline_h2, n_chars = h2_from_words(words)
    print(f"Baseline h2 (characters): {baseline_h2:.4f} bits  (N={n_chars:,})")

    print(f"\n{'='*60}")
    print("GROUPING SCHEME COMPARISON")
    print(f"{'='*60}")
    print(f"\nBaseline (no grouping):  h2 = {baseline_h2:.4f}")

    results = {}
    results['baseline'] = baseline_h2

    # ── Gallows-specific schemes ──
    h2_g1, nu1 = compare_grouping("H008: Gallows + next char (simple gallows only)", words, group_gallows_plus_next)
    h2_g2, nu2 = compare_grouping("H008v2: Compound gallows as unit + simple gallows + next", words, group_compound_gallows_as_unit)
    results['gallows_plus_next'] = h2_g1
    results['compound_gallows_unit'] = h2_g2

    # ── Adjacent pair/triple groupings (H007 subset) ──
    h2_p2, nup2 = compare_grouping("H007: Adjacent pairs (every 2 chars)", words, group_adjacent_pairs)
    h2_p3, nup3 = compare_grouping("H007: Adjacent triples (every 3 chars)", words, group_adjacent_triples)
    results['adjacent_pairs'] = h2_p2
    results['adjacent_triples'] = h2_p3

    # ── Analysis of gallows character behavior ──
    print(f"\n{'='*60}")
    print("GALLOWS CHARACTER ANALYSIS")
    print(f"{'='*60}")

    # What follows a gallows character within words?
    gallows_followers = Counter()
    gallows_total = 0
    non_gallows_chars = Counter()
    for w in words:
        for i, c in enumerate(w):
            if is_gallows(c):
                gallows_total += 1
                if i < len(w) - 1:
                    gallows_followers[w[i+1]] += 1
            else:
                non_gallows_chars[c] += 1

    total_chars = sum(len(w) for w in words)
    gallows_pct = 100 * gallows_total / total_chars
    print(f"\n  Simple gallows chars (t,k,p,f): {gallows_total:,} ({gallows_pct:.1f}% of all chars)")
    print(f"\n  What follows a gallows char?")
    total_fol = sum(gallows_followers.values())
    for c, cnt in gallows_followers.most_common(10):
        print(f"    '{c}': {cnt:5d} ({100*cnt/total_fol:.1f}%)")

    # Gallows character distribution by word position
    print(f"\n  Gallows chars by word position (pos 0-7):")
    gallows_by_pos = Counter()
    total_by_pos = Counter()
    for w in words:
        for i, c in enumerate(w):
            total_by_pos[i] += 1
            if is_gallows(c):
                gallows_by_pos[i] += 1
    for pos in range(8):
        if total_by_pos[pos] > 0:
            pct = 100 * gallows_by_pos.get(pos, 0) / total_by_pos[pos]
            print(f"    pos {pos}: {pct:.1f}% gallows ({gallows_by_pos.get(pos,0):,}/{total_by_pos[pos]:,})")

    # ── What is the H2 gain from each grouping? ──
    print(f"\n{'='*60}")
    print("SUMMARY: H2 COMPARISON ACROSS GROUPING SCHEMES")
    print(f"{'='*60}")
    print(f"  Target range for natural language: ~3.0-3.5 bits")
    print(f"  {'Scheme':<40} {'H2':>7} {'Gain':>7}")
    print(f"  {'-'*55}")
    for name, h2 in results.items():
        gain = h2 - baseline_h2
        print(f"  {name:<40} {h2:>7.4f} {gain:>+7.4f}")

    print("\nDone.")
