"""
exp_042: f76r Autocorrelation and Periodic Structure Analysis
H054: f76r has higher within-sequence word-level autocorrelation / periodic structure
than normal bio text, consistent with its "key-like sequence" designation and lowest-TTR status.
Compare: f76r vs f75v (same hand/section), vs 5 other bio folios.
"""

import re
import math
from collections import defaultdict, Counter

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

TARGET_FOLIO = 'f76r'
COMPARISON_FOLIOS = ['f75v', 'f77r', 'f77v', 'f78r', 'f80r', 'f84r', 'f84v']


def parse_folio_body_words(path):
    """Parse all body text words per folio."""
    folio_words = defaultdict(list)
    folio_lines = defaultdict(list)  # words per line (list of lists)
    current_folio = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m2 = re.match(r'^<([^>]+)>', line)
            if not m2:
                continue
            locus_raw = m2.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_part = parts[0].strip()
            locus_code = parts[1].strip()

            # Extract folio ID
            folio_m = re.match(r'^(f\d+[rv]\d*)', folio_part)
            if folio_m:
                current_folio = folio_m.group(1)

            if current_folio is None:
                continue

            # Body text loci: P0 variants
            locus_base = locus_code.lstrip('+*@=/~&')
            if not locus_base.startswith('P'):
                continue

            text = line[m2.end():].strip()
            text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            if tokens:
                folio_words[current_folio].extend(tokens)
                folio_lines[current_folio].append(tokens)

    return folio_words, folio_lines


def word_autocorrelation(words, max_lag=25):
    """Compute word autocorrelation: P(word[i] == word[i+k]) for lag k."""
    n = len(words)
    acf = []
    base_rate = 1.0 / len(set(words)) if words else 0  # expected by chance for uniform dist

    for lag in range(1, min(max_lag + 1, n)):
        matches = sum(1 for i in range(n - lag) if words[i] == words[i + lag])
        rate = matches / (n - lag)
        acf.append((lag, rate, matches, n - lag))
    return acf


def bigram_autocorrelation(words, max_lag=25):
    """Compute bigram (2-word sequence) autocorrelation at lag k."""
    n = len(words)
    bigrams = [(words[i], words[i+1]) for i in range(n-1)]

    acf = []
    for lag in range(1, min(max_lag + 1, len(bigrams))):
        matches = sum(1 for i in range(len(bigrams) - lag)
                      if bigrams[i] == bigrams[i + lag])
        rate = matches / (len(bigrams) - lag)
        acf.append((lag, rate, matches))
    return acf


def line_similarity(lines):
    """Compute pairwise word-overlap between consecutive lines."""
    if len(lines) < 2:
        return []
    sims = []
    for i in range(len(lines) - 1):
        a_set = set(lines[i])
        b_set = set(lines[i + 1])
        union = a_set | b_set
        intersection = a_set & b_set
        j = len(intersection) / len(union) if union else 0
        sims.append(j)
    return sims


def ttr_and_h2(words):
    """Compute TTR and bigram conditional entropy H2."""
    if not words:
        return 0.0, 0.0
    types = len(set(words))
    ttr = types / len(words)
    # H2
    bigram_freq = Counter(zip(words[:-1], words[1:]))
    unigram_freq = Counter(words)
    h2 = 0.0
    for (a, b), cnt in bigram_freq.items():
        p_ab = cnt / (len(words) - 1)
        p_a = unigram_freq[a] / len(words)
        if p_a > 0:
            h2 -= p_ab * math.log2(cnt / unigram_freq[a])
    return ttr, h2


def analyze_folio(folio_id, words, lines, max_lag=25):
    """Full analysis of one folio."""
    print(f"\n{'='*55}")
    print(f"FOLIO: {folio_id} ({len(words)} tokens, {len(lines)} lines, "
          f"{len(set(words))} types)")

    ttr, h2 = ttr_and_h2(words)
    print(f"TTR={ttr:.3f}, word-H2={h2:.3f} bits")

    # Word autocorrelation
    acf = word_autocorrelation(words, max_lag=max_lag)
    # Baseline: chance match rate
    freq = Counter(words)
    n = len(words)
    baseline = sum((c/n)**2 for c in freq.values())

    print(f"Baseline autocorrelation (same-word by chance): {baseline:.4f}")
    print(f"Word autocorrelation (lag: rate, ratio to baseline):")
    sig_lags = []
    for lag, rate, matches, denom in acf[:20]:
        ratio = rate / baseline if baseline > 0 else 0
        flag = " ***" if ratio > 2.0 else (" **" if ratio > 1.5 else "")
        print(f"  lag {lag:2d}: {rate:.4f} ({matches}/{denom}) ratio={ratio:.2f}{flag}")
        if ratio > 2.0:
            sig_lags.append(lag)

    if sig_lags:
        print(f"  Significant lags (ratio > 2.0): {sig_lags}")
    else:
        print(f"  No significant autocorrelation lags found")

    # Peak lag
    if acf:
        peak_lag, peak_rate, _, _ = max(acf, key=lambda x: x[1])
        peak_ratio = peak_rate / baseline if baseline > 0 else 0
        print(f"Peak autocorrelation: lag={peak_lag}, rate={peak_rate:.4f}, ratio={peak_ratio:.2f}")

    # Line similarity
    sims = line_similarity(lines)
    if sims:
        mean_sim = sum(sims) / len(sims)
        max_sim = max(sims)
        print(f"Consecutive-line Jaccard similarity: mean={mean_sim:.3f}, max={max_sim:.3f}")

    return acf, baseline, ttr, h2


if __name__ == '__main__':
    print("Loading ZL3b corpus...")
    folio_words, folio_lines = parse_folio_body_words(DATA_PATH)
    print(f"Loaded {len(folio_words)} folios")

    # Analyze target folio
    target_words = folio_words.get(TARGET_FOLIO, [])
    target_lines = folio_lines.get(TARGET_FOLIO, [])
    print(f"\nTarget folio {TARGET_FOLIO}: {len(target_words)} tokens, {len(target_lines)} lines")

    target_acf, target_baseline, target_ttr, target_h2 = analyze_folio(
        TARGET_FOLIO, target_words, target_lines)

    # Analyze comparison folios
    comparison_results = {}
    for folio_id in COMPARISON_FOLIOS:
        w = folio_words.get(folio_id, [])
        l = folio_lines.get(folio_id, [])
        if w:
            acf, baseline, ttr, h2 = analyze_folio(folio_id, w, l)
            comparison_results[folio_id] = (acf, baseline, ttr, h2)

    # Summary comparison
    print(f"\n{'='*55}")
    print("SUMMARY COMPARISON")
    print(f"{'Folio':<10} {'Tokens':>8} {'TTR':>7} {'H2':>7} {'Baseline':>10} "
          f"{'Max ACF ratio':>14}")

    def max_ratio(acf, baseline):
        if not acf or baseline == 0:
            return 0.0
        return max(r / baseline for _, r, _, _ in acf)

    # Target
    mr_target = max_ratio(target_acf, target_baseline)
    print(f"{TARGET_FOLIO:<10} {len(target_words):>8} {target_ttr:>7.3f} {target_h2:>7.3f} "
          f"{target_baseline:>10.4f} {mr_target:>14.2f}")

    for folio_id, (acf, baseline, ttr, h2) in comparison_results.items():
        mr = max_ratio(acf, baseline)
        print(f"{folio_id:<10} {len(folio_words[folio_id]):>8} {ttr:>7.3f} {h2:>7.3f} "
              f"{baseline:>10.4f} {mr:>14.2f}")

    # Specific test: does f76r have significant repeating structure?
    print(f"\n{'='*55}")
    print("SPECIFIC CYCLES TEST — f76r")
    print("Testing if any lag k shows significantly elevated autocorrelation")
    print("(f57v has 17-token cycle; what period does f76r show, if any?)")

    # Sort f76r ACF by ratio
    if target_acf and target_baseline > 0:
        sorted_acf = sorted(target_acf, key=lambda x: -x[1]/target_baseline)
        print(f"\nTop 5 lags by ratio in f76r:")
        for lag, rate, matches, denom in sorted_acf[:5]:
            ratio = rate / target_baseline
            print(f"  lag={lag}: rate={rate:.4f}, ratio={ratio:.2f}, matches={matches}/{denom}")

    # Word frequency in f76r vs manuscript
    print(f"\nTop 20 words in f76r (showing repetition structure):")
    freq = Counter(target_words)
    for word, cnt in freq.most_common(20):
        pct = 100.0 * cnt / len(target_words)
        print(f"  {word}: {cnt} ({pct:.1f}%)")
