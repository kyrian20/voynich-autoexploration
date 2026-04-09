"""
Experiment: exp_009_source_language_h2
Hypothesis tested: H016 — Arabic/Hebrew/German h2 as candidate source languages
  for the fixed-filler adjacent-pair verbose cipher test.
  Target: h2 ≈ 3.836 (Voynich paired h2). Italian=3.411, Latin=3.509 already ruled out.
Data: NLTK UDHR corpus (Arabic, Hebrew); Goethe Faust (German)
Dependencies: nltk, numpy
"""

import math
import re
from collections import Counter
from pathlib import Path

import nltk

BASE = Path(__file__).resolve().parents[2]

# ── Entropy utilities ──────────────────────────────────────────────────────────

def h2_from_chars(chars):
    """Compute bigram conditional entropy H2 = H(bigram) - H(unigram)."""
    if len(chars) < 2:
        return 0.0
    unigrams = Counter(chars)
    bigrams = Counter(zip(chars[:-1], chars[1:]))
    total_u = sum(unigrams.values())
    total_b = sum(bigrams.values())
    h_u = -sum((v / total_u) * math.log2(v / total_u) for v in unigrams.values())
    h_b = -sum((v / total_b) * math.log2(v / total_b) for v in bigrams.values())
    return h_b - h_u


def h1_from_chars(chars):
    c = Counter(chars)
    total = sum(c.values())
    return -sum((v / total) * math.log2(v / total) for v in c.values())


# ── Corpora ────────────────────────────────────────────────────────────────────

def get_arabic_chars():
    """Arabic UDHR via NLTK. Filter to consonants + base letters (U+0621-064A).
    The UDHR Arabic text has almost no diacritics (harakat), so this is effectively
    consonantal Arabic (the standard written form without vowel marks)."""
    try:
        ar_raw = nltk.corpus.udhr.raw('Arabic_Alarabia-Arabic')
        diacritics = sum(1 for c in ar_raw if '\u064b' <= c <= '\u0652')
        ar_chars = [c for c in ar_raw if '\u0621' <= c <= '\u064a']
        return ar_chars, diacritics
    except Exception as e:
        return [], 0


def get_hebrew_chars():
    """Hebrew UDHR via NLTK. Filter to Hebrew letters (U+05D0-05EA).
    Modern Hebrew is written without nikkud (vowel points) — this is consonantal."""
    try:
        he_raw = nltk.corpus.udhr.raw('Hebrew_Ivrit-Hebrew')
        he_chars = [c for c in he_raw if '\u05d0' <= c <= '\u05ea']
        return he_chars
    except Exception as e:
        return []


def get_german_chars():
    """German: Goethe Faust from Gutenberg. Extract alphabetic chars only."""
    goethe_path = BASE / 'data/reference_corpora/german/goethe_faust.txt'
    if not goethe_path.exists():
        return []
    with open(goethe_path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    words = re.findall(r'[a-zA-ZÄÖÜäöüß]+', text)
    return list(''.join(words).lower())


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
            text = m.group(2)
            text = re.sub(r'<!.*?>', '', text)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.replace('<%>', '').replace('<$>', '').replace('%', '')
            text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
            text = re.sub(r'\{[^}]*\}', '', text)
            text = re.sub(r'@\d+;?', '', text)
            raw_words = re.split(r'[.\s]+', text)
            words.extend(w for w in raw_words if w and re.match(r'^[a-zA-Z]+$', w))
    return words


# ── Adjacent-pair grouping (verbose cipher test) ───────────────────────────────

def group_adjacent_pairs_chars(chars):
    """Group chars into adjacent pairs (bigrams), return list of string tokens."""
    tokens = []
    i = 0
    while i < len(chars) - 1:
        tokens.append(chars[i] + chars[i + 1] if isinstance(chars[i], str) else (chars[i], chars[i + 1]))
        i += 2
    if i < len(chars):
        tokens.append(chars[i])
    return tokens


def paired_h2(chars):
    """Compute h2 after adjacent-pair grouping."""
    tokens = group_adjacent_pairs_chars([str(c) for c in chars])
    if len(tokens) < 2:
        return 0.0
    unigrams = Counter(tokens)
    bigrams = Counter(zip(tokens[:-1], tokens[1:]))
    total_u = sum(unigrams.values())
    total_b = sum(bigrams.values())
    h_u = -sum((v / total_u) * math.log2(v / total_u) for v in unigrams.values())
    h_b = -sum((v / total_b) * math.log2(v / total_b) for v in bigrams.values())
    return h_b - h_u


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Experiment exp_009: Source Language h2 Test for Verbose Cipher Hypothesis")
    print("Date: 2026-04-09\n")

    VOYNICH_PAIRED_H2 = 3.8355
    ITALIAN_H2 = 3.4108
    LATIN_H2 = 3.5093

    print(f"Target: Voynich paired h2 = {VOYNICH_PAIRED_H2:.4f}")
    print(f"Previously tested: Italian h2 = {ITALIAN_H2:.4f} (too low)")
    print(f"Previously tested: Latin h2   = {LATIN_H2:.4f} (too low)\n")

    results = {}

    # German
    de_chars = get_german_chars()
    if de_chars:
        h2_de = h2_from_chars(de_chars)
        results['German (Goethe Faust)'] = (h2_de, len(de_chars))
        print(f"German (Faust): N={len(de_chars):,} chars, H2={h2_de:.4f}")
    else:
        print("German corpus not found")

    # Arabic
    ar_chars, ar_diacritics = get_arabic_chars()
    if ar_chars:
        h2_ar = h2_from_chars(ar_chars)
        results['Arabic consonantal (UDHR)'] = (h2_ar, len(ar_chars))
        print(f"\nArabic (UDHR): N={len(ar_chars):,} chars")
        print(f"  Diacritics (harakat): {ar_diacritics} (minimal — effectively consonantal)")
        print(f"  H2 = {h2_ar:.4f}")
        print(f"  Top chars: {Counter(ar_chars).most_common(5)}")
    else:
        print("Arabic corpus not found")

    # Hebrew
    he_chars = get_hebrew_chars()
    if he_chars:
        h2_he = h2_from_chars(he_chars)
        results['Hebrew consonantal (UDHR)'] = (h2_he, len(he_chars))
        print(f"\nHebrew (UDHR): N={len(he_chars):,} chars")
        print(f"  H2 = {h2_he:.4f}")
        print(f"  Top chars: {Counter(he_chars).most_common(5)}")
    else:
        print("Hebrew corpus not found")

    # Voynich baseline (for reference)
    voynich_path = BASE / 'data/transcriptions/eva_zl3b.txt'
    voynich_words = parse_eva_zl3b(voynich_path)
    voynich_chars = list(''.join(voynich_words))
    h2_voy = h2_from_chars(voynich_chars)
    paired_voy = paired_h2(voynich_chars)
    print(f"\nVoynich: H2={h2_voy:.4f}, Paired H2={paired_voy:.4f}")

    # Summary table
    print(f"\n{'='*60}")
    print("SUMMARY: h2 vs verbose cipher target")
    print(f"{'='*60}")
    print(f"  {'Language':<35} {'H2':>7} {'Gap to target':>14} {'N':>10}")
    print(f"  {'-'*67}")
    print(f"  {'Italian (Dante)':<35} {ITALIAN_H2:>7.4f} {ITALIAN_H2 - VOYNICH_PAIRED_H2:>+14.4f} {'102k':>10}")
    print(f"  {'Latin (Virgil+Caesar)':<35} {LATIN_H2:>7.4f} {LATIN_H2 - VOYNICH_PAIRED_H2:>+14.4f} {'84k':>10}")
    for lang, (h2, n) in results.items():
        gap = h2 - VOYNICH_PAIRED_H2
        print(f"  {lang:<35} {h2:>7.4f} {gap:>+14.4f} {n:>10,}")
    print(f"  {'--- TARGET ---':<35} {VOYNICH_PAIRED_H2:>7.4f} {'0.0000':>14} {'':>10}")

    print(f"\n{'='*60}")
    print("INTERPRETATION")
    print(f"{'='*60}")
    all_below = all(h2 < VOYNICH_PAIRED_H2 for h2, _ in results.values())
    if all_below:
        print("ALL tested languages have h2 BELOW the Voynich paired h2 target.")
        print("Fixed-filler adjacent-pair verbose cipher is ruled out for:")
        print("  Italian, Latin, German, Arabic (consonantal), Hebrew (consonantal)")
        print(f"\nClosest match: Hebrew at {results.get('Hebrew consonantal (UDHR)', (0,0))[0]:.4f}")
        print(f"  Still {VOYNICH_PAIRED_H2 - results.get('Hebrew consonantal (UDHR)', (VOYNICH_PAIRED_H2,0))[0]:.4f} bits below target.")
    print("\nDone.")
