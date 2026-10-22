"""
exp_040: Currier A Suffix Paradigm — Does A Have a Parallel to B's 9-Form System?
H040: Currier A has a structural parallel to B's -edy/-ain suffix paradigm.
Method: Same suffix_group() as exp_038, applied only to Currier A body text.
"""
from pathlib import Path as _RepositoryPath

import re
import sys
from collections import defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

# Same suffix priority list as exp_038 (longest match first)
SUFFIXES = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y',
            'ol', 'or', 'al', 'ar', 'iin', 'in', 'on', 'an', 'ly', 'ry', 'ny',
            'ol', 'al', 'el']

# Deduplicate preserving order
seen = set()
SUFFIXES_DEDUP = []
for s in SUFFIXES:
    if s not in seen:
        seen.add(s)
        SUFFIXES_DEDUP.append(s)
SUFFIXES = SUFFIXES_DEDUP

# Core suffixes for paradigm detection (same as exp_038 for comparison)
CORE_SUFFIXES = ['aiin', 'ain', 'eedy', 'edy', 'dy', 'chy', 'eey', 'ey', 'y',
                 'ol', 'or', 'al', 'ar', 'iin', 'in']


def suffix_group(word):
    """Returns (suffix, stem) by longest-match. Returns (None, word) if no suffix matches."""
    for sfx in SUFFIXES:
        if word.endswith(sfx) and len(word) > len(sfx):
            return sfx, word[:-len(sfx)]
    return None, word


def parse_words_by_currier(path):
    """Parse body text tokens separated by Currier dialect (A/B)."""
    words_a = []
    words_b = []
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Detect folio header lines with Currier language
            m = re.search(r'\$L=([AB])', line)
            if m:
                current_currier = m.group(1)
            # Skip locus lines (not body text)
            m2 = re.match(r'^<([^>]+)>', line)
            if not m2:
                continue
            locus = m2.group(1)
            # Extract locus code (after comma)
            parts = locus.split(',')
            if len(parts) < 2:
                continue
            locus_code = parts[1].strip()
            # Body text loci: P0 variants
            locus_base = locus_code.lstrip('+*@=/~&')
            if not locus_base.startswith('P'):
                continue
            # Get text after locus
            text = line[m2.end():].strip()
            # Clean markup
            text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
            # Tokenize on dots/spaces
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            if current_currier == 'A':
                words_a.extend(tokens)
            elif current_currier == 'B':
                words_b.extend(tokens)

    return words_a, words_b


def analyze_paradigm(words, dialect_label):
    """Perform full suffix paradigm analysis on a word list."""
    print(f"\n{'='*60}")
    print(f"CURRIER {dialect_label} SUFFIX PARADIGM ANALYSIS")
    print(f"Total tokens: {len(words)}")

    # Suffix frequency
    suffix_freq = defaultdict(int)
    stem_suffix_map = defaultdict(lambda: defaultdict(int))

    for word in words:
        sfx, stem = suffix_group(word)
        if sfx and len(stem) >= 1:
            suffix_freq[sfx] += 1
            stem_suffix_map[stem][sfx] += 1

    # Top suffixes
    top_sfx = sorted(suffix_freq.items(), key=lambda x: -x[1])[:15]
    print(f"\nTop 15 suffixes:")
    for sfx, cnt in top_sfx:
        pct = 100.0 * cnt / len(words)
        print(f"  -{sfx}: {cnt} ({pct:.1f}%)")

    # Stems with multiple suffix variants
    multi_suffix_stems = {stem: d for stem, d in stem_suffix_map.items()
                          if len(d) >= 2}
    print(f"\nStems with 2+ suffix variants: {len(multi_suffix_stems)}")

    # Stems with core edy/ain/aiin variants
    core_set = {'edy', 'ain', 'aiin', 'eedy', 'dy', 'chy', 'eey', 'ey', 'y'}
    paradigm_stems = {stem: d for stem, d in stem_suffix_map.items()
                      if len({s for s in d if s in core_set}) >= 2}
    print(f"Stems with 2+ core-suffix variants {{{','.join(sorted(core_set))}}}: {len(paradigm_stems)}")

    # Top productive stems
    print(f"\nTop 10 most productive stems (by total token count):")
    stem_totals = {stem: sum(d.values()) for stem, d in stem_suffix_map.items()
                   if len(d) >= 2}
    top_stems = sorted(stem_totals.items(), key=lambda x: -x[1])[:10]
    for stem, total in top_stems:
        d = stem_suffix_map[stem]
        variants = ', '.join(f"-{s}({n})" for s, n in sorted(d.items(), key=lambda x: -x[1]))
        print(f"  '{stem}': {total} tokens, {len(d)} suffix forms — {variants}")

    # Suffix-specific positional analysis (line position)
    return stem_suffix_map, suffix_freq


def analyze_cth_cluster(words_a):
    """Analyze whether cth- in Currier A functions as a prefix morpheme."""
    print(f"\n{'='*60}")
    print("CTH- CLUSTER ANALYSIS IN CURRIER A")

    cth_words = [w for w in words_a if w.startswith('cth')]
    non_cth_words = [w for w in words_a if not w.startswith('cth')]

    print(f"cth- words: {len(cth_words)} ({100*len(cth_words)/len(words_a):.1f}% of A)")

    # Strip 'cth' prefix and check stems
    cth_stems = [w[3:] for w in cth_words if len(w) > 3]
    cth_stem_freq = defaultdict(int)
    for s in cth_stems:
        cth_stem_freq[s] += 1

    print(f"\nTop 15 cth-stripped stems (cth+?):")
    for stem, cnt in sorted(cth_stem_freq.items(), key=lambda x: -x[1])[:15]:
        print(f"  cth+'{stem}': {cnt}")

    # Check if cth-stripped stems appear as free words in A
    free_word_freq = defaultdict(int)
    for w in non_cth_words:
        free_word_freq[w] += 1

    in_free_vocab = sum(1 for s in set(cth_stems) if s in free_word_freq)
    total_cth_stems = len(set(cth_stems))
    print(f"\ncth-stripped stems in A free vocabulary: {in_free_vocab}/{total_cth_stems} "
          f"({100*in_free_vocab/max(total_cth_stems,1):.1f}%)")
    # Compare to qo analysis: 52.6% of qo-stripped stems in free vocab (exp_031)

    # Onset distribution of cth-stripped stems vs free words
    import math
    cth_stem_onsets = defaultdict(int)
    for s in cth_stems:
        if s:
            cth_stem_onsets[s[0]] += 1

    free_onsets = defaultdict(int)
    for w in non_cth_words:
        if w:
            free_onsets[w[0]] += 1

    print(f"\ncth-stem onset distribution (top chars):")
    total_cs = sum(cth_stem_onsets.values())
    for ch, cnt in sorted(cth_stem_onsets.items(), key=lambda x: -x[1])[:8]:
        print(f"  '{ch}': {cnt} ({100*cnt/total_cs:.1f}%)")

    # KL divergence: cth-stem initials vs free-word initials
    all_chars = set(cth_stem_onsets) | set(free_onsets)
    total_free = sum(free_onsets.values())
    kl = 0.0
    for ch in all_chars:
        p = cth_stem_onsets.get(ch, 0) / max(total_cs, 1)
        q = free_onsets.get(ch, 0) / max(total_free, 1)
        if p > 0 and q > 0:
            kl += p * math.log2(p / q)

    print(f"\nKL(cth-stem initials || free-word initials) = {kl:.3f} bits")
    print(f"  (Compare: qo-stem vs free-word KL = 2.96 bits from exp_031)")
    print(f"  Low KL → cth-stems have similar onset distribution to free words (prefix-like)")
    print(f"  High KL → cth-stems are a constrained class (stem-like)")

    # H_initial of cth-stripped stems
    h_cth = -sum((cnt/total_cs) * math.log2(cnt/total_cs)
                 for cnt in cth_stem_onsets.values() if cnt > 0)
    h_free = -sum((cnt/total_free) * math.log2(cnt/total_free)
                  for cnt in free_onsets.values() if cnt > 0)
    print(f"\nH_initial of cth-stripped stems: {h_cth:.3f} bits")
    print(f"H_initial of A free words: {h_free:.3f} bits")
    print(f"  (Compare from exp_031: qo-stripped H_initial=1.931, free-word H_initial=3.027)")

    return cth_stem_freq, free_word_freq


def compare_suffix_profiles(stem_map_a, stem_map_b):
    """Compare which suffixes dominate in A vs B."""
    print(f"\n{'='*60}")
    print("SUFFIX COMPARISON: A vs B")

    # Aggregate suffix counts
    sfx_a = defaultdict(int)
    sfx_b = defaultdict(int)
    for stem, d in stem_map_a.items():
        for sfx, cnt in d.items():
            sfx_a[sfx] += cnt
    for stem, d in stem_map_b.items():
        for sfx, cnt in d.items():
            sfx_b[sfx] += cnt

    total_a = sum(sfx_a.values())
    total_b = sum(sfx_b.values())

    all_sfx = set(sfx_a) | set(sfx_b)
    print(f"\n{'Suffix':<12} {'A count':>10} {'A%':>8} {'B count':>10} {'B%':>8} {'B/A ratio':>10}")
    print('-' * 60)
    for sfx in sorted(all_sfx, key=lambda s: -(sfx_b.get(s,0)/max(total_b,1))):
        ca = sfx_a.get(sfx, 0)
        cb = sfx_b.get(sfx, 0)
        pa = 100.0 * ca / max(total_a, 1)
        pb = 100.0 * cb / max(total_b, 1)
        ratio = (cb / max(total_b, 1)) / max(ca / max(total_a, 1), 0.0001)
        print(f"-{sfx:<11} {ca:>10} {pa:>8.1f} {cb:>10} {pb:>8.1f} {ratio:>10.1f}")


if __name__ == '__main__':
    print("Loading ZL3b corpus...")
    words_a, words_b = parse_words_by_currier(DATA_PATH)
    print(f"Currier A tokens: {len(words_a)}")
    print(f"Currier B tokens: {len(words_b)}")

    # Full suffix paradigm analysis on A
    stem_map_a, sfx_freq_a = analyze_paradigm(words_a, 'A')

    # Full suffix paradigm analysis on B (for comparison)
    stem_map_b, sfx_freq_b = analyze_paradigm(words_b, 'B')

    # Compare suffix profiles across A and B
    compare_suffix_profiles(stem_map_a, stem_map_b)

    # cth- cluster analysis in A
    analyze_cth_cluster(words_a)

    print(f"\n{'='*60}")
    print("DONE")
