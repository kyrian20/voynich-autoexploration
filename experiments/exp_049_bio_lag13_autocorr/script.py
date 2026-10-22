"""
exp_049: Bio Section Lag-13 Autocorrelation (H055)
exp_042 found f84v and f75v (bio) both have word autocorrelation peaks at lag=13
(ratios 2.30 and 2.22 vs baseline). Is this systematic across the bio section,
or a 2-folio coincidence?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def parse_per_folio(path):
    """Parse body text per folio with section metadata."""
    folio_words = defaultdict(list)
    folio_section = {}
    current_folio = None
    current_section = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue

            m_sec = re.search(r'\$I=([A-Z]+)', line)
            if m_sec:
                current_section = m_sec.group(1)

            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_part = parts[0].strip()
            locus_code = parts[1].strip()

            fm = re.match(r'^(f\d+[rv]\d*)', folio_part)
            if fm:
                current_folio = fm.group(1)
                if current_section and current_folio not in folio_section:
                    folio_section[current_folio] = current_section

            if current_folio is None:
                continue
            if not is_body_locus(locus_code):
                continue

            text = line[m.end():].strip()
            text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            folio_words[current_folio].extend(tokens)

    return folio_words, folio_section

def word_autocorrelation(words, max_lag=20):
    """
    Compute P(word[i] == word[i+lag]) at each lag vs baseline P(same by chance).
    Returns list of (lag, match_rate, expected, ratio).
    """
    n = len(words)
    if n < 2:
        return []

    # Baseline: expected probability of same word at random
    word_counts = Counter(words)
    expected = sum((c/n)**2 for c in word_counts.values())

    results = []
    for lag in range(1, min(max_lag+1, n)):
        matches = sum(1 for i in range(n - lag) if words[i] == words[i + lag])
        n_pairs = n - lag
        match_rate = matches / n_pairs
        ratio = match_rate / expected if expected > 0 else 0.0
        results.append((lag, match_rate, expected, ratio))

    return results

def main():
    folio_words, folio_section = parse_per_folio(DATA_PATH)
    print(f"Loaded {len(folio_words)} folios")

    # Get bio section folios
    bio_folios = [f for f, s in folio_section.items() if s == 'B']
    bio_folios.sort()
    print(f"Bio section folios: {len(bio_folios)}")

    # Also sample non-bio for comparison
    herbal_folios = [f for f, s in folio_section.items() if s == 'H']
    herbal_folios.sort()

    MIN_TOKENS = 50  # require at least 50 tokens per folio
    MAX_LAG = 20

    # Analyze bio folios
    print(f"\n{'='*70}")
    print("BIO SECTION: Per-folio word autocorrelation at lag=13")
    print(f"{'='*70}")
    print(f"{'Folio':<10} {'N':>6} {'lag13_ratio':>12} {'lag13_rate':>11} {'expected':>10} {'peak_lag':>10} {'peak_ratio':>11}")

    bio_lag13_ratios = []
    bio_peak_ratios = []
    n_bio_tested = 0

    for folio in bio_folios:
        words = folio_words[folio]
        if len(words) < MIN_TOKENS:
            continue
        n_bio_tested += 1

        acf = word_autocorrelation(words, MAX_LAG)
        if not acf:
            continue

        # Find lag=13 result
        lag13 = next((x for x in acf if x[0] == 13), None)
        if lag13 is None:
            continue
        lag13_ratio = lag13[3]

        # Find peak lag and ratio
        peak = max(acf, key=lambda x: x[3])
        peak_lag = peak[0]
        peak_ratio = peak[3]

        bio_lag13_ratios.append(lag13_ratio)
        bio_peak_ratios.append(peak_ratio)

        flag = "***" if lag13_ratio > 2.0 else ("**" if lag13_ratio > 1.5 else ("*" if lag13_ratio > 1.2 else ""))
        print(f"{folio:<10} {len(words):>6} {lag13_ratio:>12.2f}{flag} {lag13[1]:>11.4f} {lag13[2]:>10.4f} {peak_lag:>10} {peak_ratio:>11.2f}")

    if bio_lag13_ratios:
        mean_ratio = sum(bio_lag13_ratios) / len(bio_lag13_ratios)
        n_above_2 = sum(1 for r in bio_lag13_ratios if r > 2.0)
        n_above_15 = sum(1 for r in bio_lag13_ratios if r > 1.5)
        print(f"\nBio section lag=13 summary ({n_bio_tested} folios with ≥{MIN_TOKENS} tokens):")
        print(f"  Mean lag=13 ratio: {mean_ratio:.2f}")
        print(f"  Folios with ratio > 2.0: {n_above_2}/{n_bio_tested}")
        print(f"  Folios with ratio > 1.5: {n_above_15}/{n_bio_tested}")

    # Compare: herbal section
    print(f"\n{'='*70}")
    print("HERBAL SECTION: Per-folio word autocorrelation at lag=13 (sample)")
    print(f"{'='*70}")
    print(f"{'Folio':<10} {'N':>6} {'lag13_ratio':>12} {'peak_lag':>10} {'peak_ratio':>11}")

    herbal_lag13_ratios = []
    n_herbal_tested = 0

    for folio in herbal_folios[:30]:  # first 30 herbal folios
        words = folio_words[folio]
        if len(words) < MIN_TOKENS:
            continue
        n_herbal_tested += 1

        acf = word_autocorrelation(words, MAX_LAG)
        if not acf:
            continue

        lag13 = next((x for x in acf if x[0] == 13), None)
        if lag13 is None:
            continue
        lag13_ratio = lag13[3]

        peak = max(acf, key=lambda x: x[3])
        herbal_lag13_ratios.append(lag13_ratio)

        flag = "***" if lag13_ratio > 2.0 else ("**" if lag13_ratio > 1.5 else ("*" if lag13_ratio > 1.2 else ""))
        print(f"{folio:<10} {len(words):>6} {lag13_ratio:>12.2f}{flag} {peak[0]:>10} {peak[3]:>11.2f}")

    if herbal_lag13_ratios:
        mean_herbal = sum(herbal_lag13_ratios) / len(herbal_lag13_ratios)
        n_herbal_above_2 = sum(1 for r in herbal_lag13_ratios if r > 2.0)
        print(f"\nHerbal section lag=13 summary ({n_herbal_tested} folios):")
        print(f"  Mean lag=13 ratio: {mean_herbal:.2f}")
        print(f"  Folios with ratio > 2.0: {n_herbal_above_2}/{n_herbal_tested}")

    # Full ACF profile for bio folios with high lag=13
    print(f"\n{'='*70}")
    print("FULL ACF PROFILE for bio folios with lag=13 ratio > 1.5")
    print(f"{'='*70}")
    for folio in bio_folios:
        words = folio_words[folio]
        if len(words) < MIN_TOKENS:
            continue
        acf = word_autocorrelation(words, MAX_LAG)
        lag13 = next((x for x in acf if x[0] == 13), None)
        if lag13 and lag13[3] > 1.5:
            print(f"\n{folio} (n={len(words)}):")
            for lag, rate, exp, ratio in acf:
                bar = "#" * int(ratio * 5)
                print(f"  lag={lag:>2}: ratio={ratio:.2f} {bar}")

    # Histogram of lag=13 ratios: bio vs herbal
    print(f"\n{'='*70}")
    print("DISTRIBUTION COMPARISON: lag=13 ratios")
    print(f"{'='*70}")
    if bio_lag13_ratios:
        sorted_bio = sorted(bio_lag13_ratios)
        print(f"Bio lag=13 ratios: min={min(bio_lag13_ratios):.2f}, median={sorted_bio[len(sorted_bio)//2]:.2f}, max={max(bio_lag13_ratios):.2f}")
    if herbal_lag13_ratios:
        sorted_h = sorted(herbal_lag13_ratios)
        print(f"Herbal lag=13 ratios: min={min(herbal_lag13_ratios):.2f}, median={sorted_h[len(sorted_h)//2]:.2f}, max={max(herbal_lag13_ratios):.2f}")

if __name__ == '__main__':
    main()
