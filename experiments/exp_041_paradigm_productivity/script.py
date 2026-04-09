"""
exp_041: Suffix Paradigm Productivity — Is the 9-Form System Generative or Lexically Listed?
H041: The 9-form suffix paradigm is productive. Prediction:
  (a) Stem frequency predicts number of suffix variants (Pearson r > 0.5)
  (b) "Missing" suffix forms for singleton stems appear at near-zero frequency, not absolute zero
  (c) If productive, the paradigm can be modeled as: P(stem takes suffix S) ~ P(S in corpus)
"""

import re
import math
from collections import defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

SUFFIXES = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y',
            'ol', 'or', 'al', 'ar', 'iin', 'in', 'on', 'an']

seen = set()
SUFFIXES_DEDUP = []
for s in SUFFIXES:
    if s not in seen:
        seen.add(s)
        SUFFIXES_DEDUP.append(s)
SUFFIXES = SUFFIXES_DEDUP

CORE_SUFFIXES_B = {'aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y'}
CORE_SUFFIXES_A = {'aiin', 'ain', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or'}


def suffix_group(word):
    for sfx in SUFFIXES:
        if word.endswith(sfx) and len(word) > len(sfx):
            return sfx, word[:-len(sfx)]
    return None, word


def parse_words_by_currier(path):
    words_a = []
    words_b = []
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.search(r'\$L=([AB])', line)
            if m:
                current_currier = m.group(1)
            m2 = re.match(r'^<([^>]+)>', line)
            if not m2:
                continue
            locus = m2.group(1)
            parts = locus.split(',')
            if len(parts) < 2:
                continue
            locus_base = parts[1].strip().lstrip('+*@=/~&')
            if not locus_base.startswith('P'):
                continue
            text = line[m2.end():].strip()
            text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            if current_currier == 'A':
                words_a.extend(tokens)
            elif current_currier == 'B':
                words_b.extend(tokens)
    return words_a, words_b


def analyze_productivity(words, dialect, core_suffixes):
    """Test whether stem frequency predicts number of suffix variants."""
    print(f"\n{'='*60}")
    print(f"PARADIGM PRODUCTIVITY TEST — CURRIER {dialect}")
    print(f"Total tokens: {len(words)}")

    # Build stem→suffix→count map
    stem_suffix_map = defaultdict(lambda: defaultdict(int))
    for w in words:
        sfx, stem = suffix_group(w)
        if sfx and sfx in core_suffixes and len(stem) >= 1:
            stem_suffix_map[stem][sfx] += 1

    # Add stems from non-core suffixes (to get total stem frequency)
    stem_total_freq = defaultdict(int)
    for w in words:
        sfx, stem = suffix_group(w)
        if sfx and len(stem) >= 1:
            stem_total_freq[stem] += 1
        elif not sfx:
            stem_total_freq[w] += 1

    # Filter: stems with any core suffix at all
    paradigm_stems = dict(stem_suffix_map)

    n_variants = {stem: len(d) for stem, d in paradigm_stems.items()}
    total_freq = {stem: stem_total_freq.get(stem, 0) for stem in paradigm_stems}

    # Sort by frequency
    stems_sorted = sorted(paradigm_stems.keys(), key=lambda s: -total_freq[s])

    # Distribution of variant counts
    variant_dist = defaultdict(int)
    for v in n_variants.values():
        variant_dist[v] += 1

    print(f"\nDistribution of suffix variant counts (core suffixes only):")
    for v in sorted(variant_dist.keys()):
        print(f"  {v} variants: {variant_dist[v]} stems")

    # Singletons (1 core suffix observed)
    singletons = [s for s, d in paradigm_stems.items() if len(d) == 1]
    print(f"\nSingleton stems (only 1 core suffix): {len(singletons)}")
    print(f"Multi-suffix stems (2+ core suffixes): {len(paradigm_stems) - len(singletons)}")

    # Test (a): Pearson correlation between stem frequency and variant count
    stems_list = list(paradigm_stems.keys())
    freqs = [total_freq[s] for s in stems_list]
    variants = [n_variants[s] for s in stems_list]

    n = len(stems_list)
    mean_f = sum(freqs) / n
    mean_v = sum(variants) / n
    cov = sum((freqs[i] - mean_f) * (variants[i] - mean_v) for i in range(n)) / n
    std_f = (sum((f - mean_f)**2 for f in freqs) / n) ** 0.5
    std_v = (sum((v - mean_v)**2 for v in variants) / n) ** 0.5
    pearson_r = cov / (std_f * std_v + 1e-10)

    print(f"\n(a) Pearson r (stem_freq vs n_variants): {pearson_r:.3f}")
    print(f"   Threshold for productivity: r > 0.5 (high), 0.3-0.5 (moderate), < 0.3 (weak)")

    # Also test with log frequency
    import math
    log_freqs = [math.log2(f + 1) for f in freqs]
    mean_lf = sum(log_freqs) / n
    cov_log = sum((log_freqs[i] - mean_lf) * (variants[i] - mean_v) for i in range(n)) / n
    std_lf = (sum((lf - mean_lf)**2 for lf in log_freqs) / n) ** 0.5
    pearson_r_log = cov_log / (std_lf * std_v + 1e-10)
    print(f"   Pearson r (log2(stem_freq) vs n_variants): {pearson_r_log:.3f}")

    # Test (b): For singleton stems, do the "missing" core suffixes appear at near-zero counts?
    # Check: for each singleton stem, what is the total corpus count of stem+other_suffix tokens?
    print(f"\n(b) Singleton stems — do missing suffix forms appear at all?")

    # Get the most common singleton (high frequency singleton = strongest test)
    singleton_freq = [(s, total_freq[s]) for s in singletons]
    singleton_freq.sort(key=lambda x: -x[1])

    print(f"Top 15 singleton stems by frequency:")
    for stem, freq in singleton_freq[:15]:
        observed_sfx = list(paradigm_stems[stem].keys())[0]
        # Check all core suffixes for this stem
        missing = []
        for sfx in core_suffixes:
            if sfx != observed_sfx:
                # Check if stem+sfx exists anywhere in corpus
                count = stem_suffix_map[stem].get(sfx, 0)
                if count > 0:
                    missing.append(f"+{sfx}({count})")
        present = f"-{observed_sfx}({list(paradigm_stems[stem].values())[0]})"
        print(f"  '{stem}': freq={freq}, {present}" + (", also: " + ", ".join(missing) if missing else ", NO other core suffixes"))

    # Test (c): Expected vs observed suffix distribution per stem
    # Under full productivity: P(stem takes sfx S) = P(S in corpus) * total stem tokens
    # Under lexical listing: stems have fixed suffix inventories

    # Compute corpus-level suffix probabilities (marginal)
    total_core_tokens = sum(sum(d.values()) for d in paradigm_stems.values())
    sfx_marginal = defaultdict(int)
    for d in paradigm_stems.values():
        for sfx, cnt in d.items():
            sfx_marginal[sfx] += cnt
    sfx_prob = {sfx: cnt / total_core_tokens for sfx, cnt in sfx_marginal.items()}

    # For top-20 multi-suffix stems, compute observed vs expected distribution
    multi_stems = [(s, total_freq[s]) for s, d in paradigm_stems.items() if len(d) >= 3]
    multi_stems.sort(key=lambda x: -x[1])

    print(f"\n(c) Observed vs Expected suffix distributions for top-5 multi-suffix stems:")
    print(f"(Expected = marginal corpus suffix probabilities; KL measures deviation)")
    for stem, freq in multi_stems[:5]:
        d = paradigm_stems[stem]
        stem_total = sum(d.values())
        # KL from expected (marginal) to observed
        kl = 0.0
        for sfx in core_suffixes:
            obs = d.get(sfx, 0) / stem_total
            exp = sfx_prob.get(sfx, 1e-10)
            if obs > 0:
                kl += obs * math.log2(obs / exp)
        print(f"  '{stem}': {stem_total} core-sfx tokens, {len(d)} variants, KL from marginal = {kl:.3f} bits")
        obs_str = ', '.join(f"-{s}({n})" for s, n in sorted(d.items(), key=lambda x: -x[1]))
        print(f"    Observed: {obs_str}")

    print(f"\n  If KL ≈ 0 for all stems: pure productivity (stems sample global suffix distribution)")
    print(f"  If KL >> 0 for top stems: stem-specific suffix preferences (partially productive)")

    return pearson_r, pearson_r_log, singletons, paradigm_stems


if __name__ == '__main__':
    words_a, words_b = parse_words_by_currier(DATA_PATH)

    pearson_b, pearson_log_b, singletons_b, pmap_b = analyze_productivity(
        words_b, 'B', CORE_SUFFIXES_B)
    pearson_a, pearson_log_a, singletons_a, pmap_a = analyze_productivity(
        words_a, 'A', CORE_SUFFIXES_A)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"Currier B: Pearson r (freq vs variants) = {pearson_b:.3f}, "
          f"log version = {pearson_log_b:.3f}")
    print(f"Currier A: Pearson r (freq vs variants) = {pearson_a:.3f}, "
          f"log version = {pearson_log_a:.3f}")
    print(f"\nB singletons: {len(singletons_b)} | multi-suffix: {len(pmap_b)-len(singletons_b)}")
    print(f"A singletons: {len(singletons_a)} | multi-suffix: {len(pmap_a)-len(singletons_a)}")
    print()
    print("Interpretation guide:")
    print("  r > 0.7 → Strongly productive (frequency determines paradigm completeness)")
    print("  0.4-0.7 → Moderately productive (some frequency effect)")
    print("  < 0.4   → Low productivity (paradigm completeness not frequency-driven)")
    print("  KL ≈ 0  → Pure productivity (stems sample global suffix distribution uniformly)")
    print("  KL > 1  → Stem-specific suffix preferences (partial productivity / lexical listing)")
