"""
exp_055: Bathing-Pool Folio Phrase Structures + y-Initial Section Correlation (H059, H063)
H059: Do f75v, f82v, f84v (bio folios with lag=13 autocorrelation signal) share a
      distinctive phrase structure that explains the lag-13 repeat?
H063: Are y-initial line-opening words concentrated in specific sections or manuscript regions?
"""

import re
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def parse_per_folio_lines(path):
    """Parse body text lines per folio, tracking section and Currier."""
    folio_lines = defaultdict(list)
    folio_section = {}
    folio_currier = {}
    current_folio = None
    current_section = None
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue

            m_sec = re.search(r'\$I=([A-Z]+)', line)
            if m_sec:
                current_section = m_sec.group(1)
            m_cur = re.search(r'\$L=([AB])', line)
            if m_cur:
                current_currier = m_cur.group(1)

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
                if current_currier and current_folio not in folio_currier:
                    folio_currier[current_folio] = current_currier

            if current_folio is None or not is_body_locus(locus_code):
                continue

            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]

            if tokens:
                folio_lines[current_folio].append(tokens)

    return folio_lines, folio_section, folio_currier

def extract_ngrams(words, n):
    return [tuple(words[i:i+n]) for i in range(len(words)-n+1)]

def word_autocorrelation_at_lag(words, lag):
    n = len(words)
    if n <= lag:
        return None
    matches = sum(1 for i in range(n - lag) if words[i] == words[i + lag])
    match_rate = matches / (n - lag)
    word_counts = Counter(words)
    expected = sum((c/n)**2 for c in word_counts.values())
    ratio = match_rate / expected if expected > 0 else 0.0
    return match_rate, expected, ratio

def main():
    folio_lines, folio_section, folio_currier = parse_per_folio_lines(DATA_PATH)
    print(f"Loaded {len(folio_lines)} folios")

    # ===== H059: Bathing-pool folios phrase structures =====
    print("\n" + "=" * 70)
    print("H059: Bathing-Pool Folio Phrase Analysis (f75v, f82v, f84v)")
    print("=" * 70)

    target_folios = ['f75v', 'f82v', 'f84v']
    reference_bio = [f for f, s in folio_section.items() if s == 'B' and f not in target_folios]

    # Get word sequences for each folio
    folio_words = {f: [w for lines in folio_lines[f] for w in lines] for f in folio_lines}

    # For target folios: find what repeats at lag=13
    print("\nPairs of words appearing at lag=13 in target folios:")
    for folio in target_folios:
        words = folio_words.get(folio, [])
        if len(words) < 15:
            continue

        lag_13_pairs = []
        for i in range(len(words) - 13):
            if words[i] == words[i + 13]:
                lag_13_pairs.append((words[i], i))

        print(f"\n{folio} (n={len(words)}, lag=13 matches: {len(lag_13_pairs)}):")
        if lag_13_pairs:
            word_freqs = Counter(w for w, _ in lag_13_pairs)
            for w, c in word_freqs.most_common(10):
                print(f"  '{w}' repeats at lag=13: {c} times")

    # Cross-folio phrase sharing among target folios
    print(f"\nBigram sharing among target folios:")
    folio_bigrams = {}
    for folio in target_folios:
        words = folio_words.get(folio, [])
        folio_bigrams[folio] = set(extract_ngrams(words, 2))

    for i, f1 in enumerate(target_folios):
        for f2 in target_folios[i+1:]:
            shared = folio_bigrams[f1] & folio_bigrams[f2]
            print(f"  {f1} ∩ {f2}: {len(shared)} shared bigrams")
            for bg in sorted(shared)[:10]:
                print(f"    {' '.join(bg)}")

    # Compare with cross-folio sharing among other bio folios
    print(f"\nFor comparison — cross-folio bigram sharing among random bio pairs:")
    import random
    random.seed(42)
    sample_bio = random.sample(reference_bio, min(6, len(reference_bio)))
    for i in range(min(3, len(sample_bio)-1)):
        f1, f2 = sample_bio[i], sample_bio[i+1]
        bg1 = set(extract_ngrams(folio_words.get(f1, []), 2))
        bg2 = set(extract_ngrams(folio_words.get(f2, []), 2))
        print(f"  {f1} ∩ {f2}: {len(bg1 & bg2)} shared bigrams")

    # What are the most distinctive bigrams of the pool folios?
    print(f"\nMost common bigrams across all 3 pool folios (appearing in 2+):")
    all_pool_bigrams = defaultdict(int)
    for folio in target_folios:
        words = folio_words.get(folio, [])
        for bg in set(extract_ngrams(words, 2)):
            all_pool_bigrams[bg] += 1
    pool_shared = {bg: c for bg, c in all_pool_bigrams.items() if c >= 2}
    for bg, c in sorted(pool_shared.items(), key=lambda x: -x[1])[:15]:
        print(f"  '{' '.join(bg)}': appears in {c}/3 pool folios")

    # ===== H063: y-Initial by section/folio =====
    print("\n\n" + "=" * 70)
    print("H063: y-Initial Line-Opening Words by Section and Folio Range")
    print("=" * 70)

    # Per-section y-initial rate at line beginnings
    section_stats = defaultdict(lambda: {'total_lines': 0, 'y_starts': 0, 'para_starts': 0, 'y_para_starts': 0})

    for folio, lines in folio_lines.items():
        sec = folio_section.get(folio, '?')
        for line in lines:
            if not line:
                continue
            section_stats[sec]['total_lines'] += 1
            if line[0].startswith('y'):
                section_stats[sec]['y_starts'] += 1

    print(f"\n{'Section':<10} {'Lines':>8} {'y-initial%':>12} {'y-initial N':>12}")
    for sec in sorted(section_stats.keys()):
        st = section_stats[sec]
        rate = st['y_starts'] / max(1, st['total_lines'])
        print(f"{sec:<10} {st['total_lines']:>8} {100*rate:>11.1f}% {st['y_starts']:>12}")

    # Per-folio y-initial rate for Currier A folios
    print(f"\nPer-folio y-initial rate (Currier A folios with ≥20 lines):")
    folio_y_rates = []
    for folio, lines in folio_lines.items():
        if folio_currier.get(folio) != 'A':
            continue
        if len(lines) < 20:
            continue
        y_starts = sum(1 for line in lines if line and line[0].startswith('y'))
        rate = y_starts / len(lines)
        folio_y_rates.append((folio, len(lines), y_starts, rate, folio_section.get(folio, '?')))

    folio_y_rates.sort(key=lambda x: -x[3])
    print(f"{'Folio':<10} {'Lines':>6} {'y-starts':>9} {'y-rate%':>9} {'Section':>9}")
    for folio, n_lines, y_starts, rate, sec in folio_y_rates[:20]:
        print(f"{folio:<10} {n_lines:>6} {y_starts:>9} {100*rate:>8.1f}% {sec:>9}")

    # Is y-initial enriched in specific folio ranges?
    print(f"\nFolio number distribution of high y-initial rate (>20%):")
    high_y = [(folio, rate, sec) for folio, _, _, rate, sec in folio_y_rates if rate > 0.20]
    for folio, rate, sec in high_y:
        print(f"  {folio}: {100*rate:.1f}% y-initial ({sec})")

if __name__ == '__main__':
    main()
