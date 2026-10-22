"""
exp_043: Cross-Folio Parallel Passages — Repeated Word N-grams Across Folios
H052: High within-section cross-folio bigram/trigram repetition; bio section highest.
Tests for "parallel passages" — identical word sequences on multiple folios.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

SECTION_MAP = {
    'H': 'herbal', 'P': 'pharma', 'A': 'astro', 'B': 'bio',
    'Z': 'zodiac', 'C': 'cosmo', 'S': 'special', 'T': 'text'
}

# Folio → section mapping (using known ranges from prior experiments)
def get_section(folio_id):
    # Extract folio number
    m = re.match(r'f(\d+)([rv])(\d*)', folio_id)
    if not m:
        return 'unknown'
    n = int(m.group(1))
    # Approximate section classification from folio number
    if 1 <= n <= 66:
        return 'herbal'
    elif 67 <= n <= 73:
        return 'astro'
    elif 75 <= n <= 84:
        return 'bio'
    elif 85 <= n <= 102:
        return 'pharma'
    elif 103 <= n <= 116:
        return 'special'
    else:
        return 'other'


def parse_folio_body_words(path):
    """Parse body text words per folio with section metadata."""
    folio_words = defaultdict(list)
    current_folio = None
    folio_currier = {}
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Detect Currier language from header
            m_cur = re.search(r'\$L=([AB])', line)
            if m_cur:
                current_currier = m_cur.group(1)

            m2 = re.match(r'^<([^>]+)>', line)
            if not m2:
                continue
            locus_raw = m2.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_part = parts[0].strip()
            locus_code = parts[1].strip()

            folio_m = re.match(r'^(f\d+[rv]\d*)', folio_part)
            if folio_m:
                current_folio = folio_m.group(1)
                if current_currier and current_folio not in folio_currier:
                    folio_currier[current_folio] = current_currier

            if current_folio is None:
                continue

            locus_base = locus_code.lstrip('+*@=/~&')
            if not locus_base.startswith('P'):
                continue

            text = line[m2.end():].strip()
            text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            folio_words[current_folio].extend(tokens)

    return folio_words, folio_currier


def extract_ngrams(words, n):
    """Extract all n-grams from a word list."""
    return [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]


def cross_folio_ngram_analysis(folio_words, n=2, min_count=2):
    """Find n-grams that appear on multiple distinct folios."""
    # Map ngram → set of folios containing it
    ngram_folios = defaultdict(set)
    ngram_total = Counter()

    for folio, words in folio_words.items():
        ngrams = extract_ngrams(words, n)
        for ng in ngrams:
            ngram_folios[ng].add(folio)
            ngram_total[ng] += 1

    # Filter: n-grams on 2+ folios
    cross_folio = {ng: folios for ng, folios in ngram_folios.items()
                   if len(folios) >= min_count}

    return cross_folio, ngram_total


def section_analysis(cross_folio_ngrams, folio_words, n=2):
    """Analyze cross-folio n-grams by section."""
    section_pairs = defaultdict(int)  # (section_a, section_b) → shared ngrams
    within_section = defaultdict(int)  # section → within-section cross-folio ngrams
    total_within_section_possible = defaultdict(int)

    for ng, folios in cross_folio_ngrams.items():
        folio_list = list(folios)
        for i in range(len(folio_list)):
            for j in range(i + 1, len(folio_list)):
                s1 = get_section(folio_list[i])
                s2 = get_section(folio_list[j])
                if s1 == s2:
                    within_section[s1] += 1
                else:
                    key = tuple(sorted([s1, s2]))
                    section_pairs[key] += 1

    return within_section, section_pairs


if __name__ == '__main__':
    print("Loading ZL3b corpus...")
    folio_words, folio_currier = parse_folio_body_words(DATA_PATH)

    # Filter to folios with sufficient tokens
    folio_words_filtered = {f: w for f, w in folio_words.items() if len(w) >= 30}
    print(f"Folios with ≥30 tokens: {len(folio_words_filtered)}")
    total_tokens = sum(len(w) for w in folio_words_filtered.values())
    print(f"Total body text tokens: {total_tokens}")

    # Bigram analysis
    print(f"\n{'='*60}")
    print(f"CROSS-FOLIO WORD BIGRAM ANALYSIS")
    cross_bi, bi_total = cross_folio_ngram_analysis(folio_words_filtered, n=2, min_count=2)
    total_bigram_types = len(set(ng for f, w in folio_words_filtered.items()
                                  for ng in extract_ngrams(w, 2)))

    print(f"Total distinct word bigram types in corpus: {total_bigram_types}")
    print(f"Bigrams on 2+ distinct folios: {len(cross_bi)} "
          f"({100*len(cross_bi)/max(total_bigram_types,1):.1f}%)")
    print(f"Bigrams on 3+ distinct folios: "
          f"{sum(1 for v in cross_bi.values() if len(v) >= 3)}")
    print(f"Bigrams on 5+ distinct folios: "
          f"{sum(1 for v in cross_bi.values() if len(v) >= 5)}")
    print(f"Bigrams on 10+ distinct folios: "
          f"{sum(1 for v in cross_bi.values() if len(v) >= 10)}")

    # Most widespread bigrams
    print(f"\nTop 20 most widespread word bigrams (most folios):")
    top_bi = sorted(cross_bi.items(), key=lambda x: -len(x[1]))[:20]
    for ng, folios in top_bi:
        sections = set(get_section(f) for f in folios)
        print(f"  {' '.join(ng)}: {len(folios)} folios, {bi_total[ng]} total — "
              f"sections: {','.join(sorted(sections))}")

    # Section analysis for bigrams
    within_sect_bi, cross_sect_bi = section_analysis(cross_bi, folio_words_filtered, n=2)
    print(f"\nWithin-section cross-folio bigrams:")
    for sect, count in sorted(within_sect_bi.items(), key=lambda x: -x[1]):
        # Normalize by number of folio pairs in this section
        section_folios = [f for f in folio_words_filtered if get_section(f) == sect]
        n_pairs = len(section_folios) * (len(section_folios) - 1) // 2
        rate = count / max(n_pairs, 1)
        print(f"  {sect}: {count} bigrams across {len(section_folios)} folios ({n_pairs} pairs) "
              f"— rate {rate:.1f} shared bigrams/pair")

    print(f"\nTop 10 cross-section bigram pairs:")
    top_cross = sorted(cross_sect_bi.items(), key=lambda x: -x[1])[:10]
    for (s1, s2), count in top_cross:
        print(f"  {s1}↔{s2}: {count} shared bigrams")

    # Trigram analysis
    print(f"\n{'='*60}")
    print(f"CROSS-FOLIO WORD TRIGRAM ANALYSIS")
    cross_tri, tri_total = cross_folio_ngram_analysis(folio_words_filtered, n=3, min_count=2)
    total_trigram_types = len(set(ng for f, w in folio_words_filtered.items()
                                   for ng in extract_ngrams(w, 3)))

    print(f"Total distinct word trigram types in corpus: {total_trigram_types}")
    print(f"Trigrams on 2+ distinct folios: {len(cross_tri)} "
          f"({100*len(cross_tri)/max(total_trigram_types,1):.2f}%)")
    print(f"Trigrams on 3+ distinct folios: "
          f"{sum(1 for v in cross_tri.values() if len(v) >= 3)}")

    print(f"\nTop 20 most widespread word trigrams (most folios):")
    top_tri = sorted(cross_tri.items(), key=lambda x: -len(x[1]))[:20]
    for ng, folios in top_tri:
        sections = set(get_section(f) for f in folios)
        print(f"  {' '.join(ng)}: {len(folios)} folios, {tri_total[ng]} total — "
              f"sections: {','.join(sorted(sections))}")

    # Cross-section trigrams
    within_sect_tri, cross_sect_tri = section_analysis(cross_tri, folio_words_filtered, n=3)
    print(f"\nWithin-section cross-folio trigrams:")
    for sect, count in sorted(within_sect_tri.items(), key=lambda x: -x[1]):
        section_folios = [f for f in folio_words_filtered if get_section(f) == sect]
        n_pairs = len(section_folios) * (len(section_folios) - 1) // 2
        rate = count / max(n_pairs, 1)
        print(f"  {sect}: {count} trigrams across {len(section_folios)} folios "
              f"({n_pairs} pairs) — rate {rate:.1f} shared trigrams/pair")

    # Cross-section trigrams (the interesting case)
    cross_sect_tri_nonzero = [(k, v) for k, v in cross_sect_tri.items() if v > 0]
    print(f"\nCross-section trigram sharing:")
    for (s1, s2), count in sorted(cross_sect_tri_nonzero, key=lambda x: -x[1])[:10]:
        print(f"  {s1}↔{s2}: {count} shared trigrams")

    # Find any cross-section trigrams (interpret what they are)
    print(f"\nTop cross-section trigrams (most interesting finding):")
    cross_section_trigrams = {}
    for ng, folios in cross_tri.items():
        sections = set(get_section(f) for f in folios)
        if len(sections) > 1:
            cross_section_trigrams[ng] = (folios, sections)
    top_cross_tri = sorted(cross_section_trigrams.items(),
                           key=lambda x: -len(x[1][0]))[:20]
    for ng, (folios, sections) in top_cross_tri:
        print(f"  {' '.join(ng)}: {len(folios)} folios, sections: {','.join(sorted(sections))}")
