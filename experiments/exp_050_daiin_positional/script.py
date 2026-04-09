"""
exp_050: daiin Positional Analysis in Currier A (H060)
Tests whether daiin (A's most frequent word) concentrates at line-final position
like B's -ain words, suggesting A/B functional parallel.
Also: positional analysis of d-stem (bare 'd') and all 'd'-initial A words.
"""

import re
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def clean_text(text):
    text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
    return text

def strip_suffix(word):
    for suf in SUFFIX_LIST:
        if word.endswith(suf) and len(word) > len(suf):
            return (word[:-len(suf)], suf)
    return (word, None)

def parse_lines(path):
    """
    Parse body text lines per Currier dialect.
    Returns list of (line_words, currier, folio, line_type) where:
    - line_words: list of words in the line
    - line_type: 'start' (@P0), 'middle' (+P0), 'paragraph_end' (=Pt)
    """
    lines = []
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue

            m_currier = re.search(r'\$L=([AB])', line)
            if m_currier:
                current_currier = m_currier.group(1)

            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_part = parts[0].strip()
            locus_code = parts[1].strip()

            # Determine line type from locus prefix
            base_locus = locus_code.lstrip('+*@=/~&')
            if not base_locus.startswith('P'):
                continue

            # Line type: @ = first line of paragraph, + = continuation, = = paragraph end/standalone
            if locus_code.startswith('@'):
                line_type = 'para_start'
            elif locus_code.startswith('+'):
                line_type = 'continuation'
            elif locus_code.startswith('=') or base_locus.startswith('Pt'):
                line_type = 'para_end'
            else:
                line_type = 'unknown'

            # Is this line followed by <$> (last line of paragraph)?
            text = line[m.end():].strip()
            has_dollar = '<$>' in text
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]

            if not tokens:
                continue

            fm = re.match(r'^(f\d+[rv]\d*)', folio_part)
            folio = fm.group(1) if fm else 'unknown'

            lines.append({
                'words': tokens,
                'currier': current_currier,
                'folio': folio,
                'line_type': line_type,
                'has_dollar': has_dollar,
                'n_words': len(tokens),
            })

    return lines

def word_position_stats(lines, target_word, currier='A'):
    """
    For a target word, compute its distribution across line positions:
    - first (position 0)
    - last (position -1)
    - not-first-not-last (medial)
    Also normalize by total occurrences at each position.
    """
    pos_first = 0
    pos_last = 0
    pos_medial = 0
    total_occ = 0

    total_first_slots = 0  # total number of line-first positions
    total_last_slots = 0   # total number of line-last positions
    total_medial_slots = 0 # total number of medial positions

    for line_data in lines:
        if line_data['currier'] != currier:
            continue
        words = line_data['words']
        n = len(words)
        if n == 0:
            continue

        total_first_slots += 1
        total_last_slots += 1
        total_medial_slots += max(0, n - 2)

        for i, w in enumerate(words):
            if w == target_word:
                total_occ += 1
                if i == 0:
                    pos_first += 1
                elif i == n - 1:
                    pos_last += 1
                else:
                    pos_medial += 1

    if total_occ == 0:
        return None

    # Rate = (occurrences at position) / (total slots at that position)
    # This normalizes for the different number of slots
    rate_first = pos_first / max(1, total_first_slots)
    rate_last = pos_last / max(1, total_last_slots)
    rate_medial = pos_medial / max(1, total_medial_slots)

    # Fraction of word's own occurrences at each position
    frac_first = pos_first / total_occ
    frac_last = pos_last / total_occ
    frac_medial = pos_medial / total_occ

    return {
        'total_occ': total_occ,
        'frac_first': frac_first,
        'frac_last': frac_last,
        'frac_medial': frac_medial,
        'rate_first': rate_first,
        'rate_last': rate_last,
        'rate_medial': rate_medial,
        'count_first': pos_first,
        'count_last': pos_last,
        'count_medial': pos_medial,
    }

def suffix_positional_rates(lines, suffix, currier='B'):
    """Compute positional rates (first/last/medial) for all words with a given suffix."""
    pos_first = 0
    pos_last = 0
    pos_medial = 0
    total_occ = 0

    total_first_slots = 0
    total_last_slots = 0
    total_medial_slots = 0

    for line_data in lines:
        if line_data['currier'] != currier:
            continue
        words = line_data['words']
        n = len(words)
        if n == 0:
            continue

        total_first_slots += 1
        total_last_slots += 1
        total_medial_slots += max(0, n - 2)

        for i, w in enumerate(words):
            if w.endswith(suffix):
                total_occ += 1
                if i == 0:
                    pos_first += 1
                elif i == n - 1:
                    pos_last += 1
                else:
                    pos_medial += 1

    if total_occ == 0:
        return None

    rate_first = pos_first / max(1, total_first_slots)
    rate_last = pos_last / max(1, total_last_slots)
    rate_medial = pos_medial / max(1, total_medial_slots)
    frac_first = pos_first / total_occ
    frac_last = pos_last / total_occ
    frac_medial = pos_medial / total_occ

    return {
        'total_occ': total_occ,
        'frac_first': frac_first,
        'frac_last': frac_last,
        'frac_medial': frac_medial,
        'rate_first': rate_first,
        'rate_last': rate_last,
        'rate_medial': rate_medial,
    }

def main():
    lines = parse_lines(DATA_PATH)
    print(f"Parsed {len(lines)} body text lines")

    # Count lines per dialect
    a_lines = [l for l in lines if l['currier'] == 'A']
    b_lines = [l for l in lines if l['currier'] == 'B']
    print(f"Currier A lines: {len(a_lines)}, Currier B lines: {len(b_lines)}")

    # Overall word frequency in A
    a_words = []
    for l in a_lines:
        a_words.extend(l['words'])
    a_freq = Counter(a_words)
    print(f"\nTotal Currier A tokens: {len(a_words)}")
    print("Top 20 Currier A words:")
    for w, c in a_freq.most_common(20):
        print(f"  {w}: {c} ({100*c/len(a_words):.2f}%)")

    # === 1. daiin positional analysis in Currier A ===
    print(f"\n{'='*60}")
    print("POSITIONAL ANALYSIS: daiin (Currier A)")
    print(f"{'='*60}")

    daiin_stats = word_position_stats(lines, 'daiin', 'A')
    if daiin_stats:
        print(f"Total daiin occurrences in A: {daiin_stats['total_occ']}")
        print(f"  First (line-initial): {daiin_stats['count_first']} ({100*daiin_stats['frac_first']:.1f}%)")
        print(f"  Last (line-final):    {daiin_stats['count_last']} ({100*daiin_stats['frac_last']:.1f}%)")
        print(f"  Medial:               {daiin_stats['count_medial']} ({100*daiin_stats['frac_medial']:.1f}%)")
        print(f"  Rate at first slots:  {100*daiin_stats['rate_first']:.2f}%")
        print(f"  Rate at last slots:   {100*daiin_stats['rate_last']:.2f}%")
        print(f"  Rate at medial slots: {100*daiin_stats['rate_medial']:.2f}%")

    # Baseline: average word position rates in A
    baseline_first = sum(1 for l in a_lines for i, w in enumerate(l['words']) if i == 0) / max(1, sum(l['n_words'] for l in a_lines))
    baseline_last = sum(1 for l in a_lines for i, w in enumerate(l['words']) if i == l['n_words'] - 1) / max(1, sum(l['n_words'] for l in a_lines))
    print(f"\nBaseline rates in Currier A:")
    print(f"  First-slot rate: {100*baseline_first:.2f}% of tokens are line-initial")
    print(f"  Last-slot rate:  {100*baseline_last:.2f}% of tokens are line-final")

    # === 2. Compare: -ain suffix in Currier B ===
    print(f"\n{'='*60}")
    print("POSITIONAL ANALYSIS: -ain suffix (Currier B)")
    print(f"{'='*60}")

    ain_stats = suffix_positional_rates(lines, 'ain', 'B')
    if ain_stats:
        print(f"Total -ain tokens in B: {ain_stats['total_occ']}")
        print(f"  First:  {100*ain_stats['frac_first']:.1f}%")
        print(f"  Last:   {100*ain_stats['frac_last']:.1f}%")
        print(f"  Medial: {100*ain_stats['frac_medial']:.1f}%")
        print(f"  Rate at last slots: {100*ain_stats['rate_last']:.2f}%")

    # -aiin suffix in Currier A (parallel test)
    aiin_a = suffix_positional_rates(lines, 'aiin', 'A')
    if aiin_a:
        print(f"\n-aiin in Currier A: n={aiin_a['total_occ']}")
        print(f"  First: {100*aiin_a['frac_first']:.1f}%, Last: {100*aiin_a['frac_last']:.1f}%, Medial: {100*aiin_a['frac_medial']:.1f}%")

    # === 3. Top A words by line-final concentration ===
    print(f"\n{'='*60}")
    print("TOP CURRIER A WORDS BY LINE-FINAL CONCENTRATION")
    print(f"{'='*60}")
    print(f"(words with ≥20 occurrences, sorted by fraction of occurrences that are line-final)")

    top_a_words = [w for w, c in a_freq.most_common(60) if c >= 20]
    word_stats_list = []
    for w in top_a_words:
        stats = word_position_stats(lines, w, 'A')
        if stats:
            word_stats_list.append((w, stats))

    word_stats_list.sort(key=lambda x: -x[1]['frac_last'])
    print(f"\n{'Word':<15} {'N':>6} {'First%':>8} {'Last%':>8} {'Medial%':>8}")
    for w, stats in word_stats_list[:25]:
        print(f"{w:<15} {stats['total_occ']:>6} {100*stats['frac_first']:>7.1f}% {100*stats['frac_last']:>7.1f}% {100*stats['frac_medial']:>7.1f}%")

    # === 4. 'd' stem analysis in Currier A ===
    print(f"\n{'='*60}")
    print("d-STEM WORDS IN CURRIER A")
    print(f"{'='*60}")
    d_stem_words = [(w, c) for w, c in a_freq.most_common() if w == 'd' or (w.startswith('d') and w != 'daiin')]
    print(f"Top d-initial words in A (excluding daiin):")
    for w, c in d_stem_words[:20]:
        stem, suf = strip_suffix(w)
        root = stem[1:] if stem.startswith('d') else stem
        print(f"  {w}: {c} (stem='{stem}', suf='{suf}')")

    # Does bare 'd' appear in A?
    bare_d = a_freq.get('d', 0)
    print(f"\nBare 'd' in Currier A: {bare_d} occurrences")

    # === 5. daiin vs -ain comparison ===
    print(f"\n{'='*60}")
    print("A/B POSITIONAL PARALLEL: daiin (A) vs -ain words (B)")
    print(f"{'='*60}")
    if daiin_stats and ain_stats:
        print(f"{'':20} {'daiin (A)':>15} {'-ain words (B)':>15}")
        print(f"{'Line-first %':20} {100*daiin_stats['frac_first']:>14.1f}% {100*ain_stats['frac_first']:>14.1f}%")
        print(f"{'Line-last %':20} {100*daiin_stats['frac_last']:>14.1f}% {100*ain_stats['frac_last']:>14.1f}%")
        print(f"{'Medial %':20} {100*daiin_stats['frac_medial']:>14.1f}% {100*ain_stats['frac_medial']:>14.1f}%")

    # === 6. Line-final rates for all top A words ===
    print(f"\n{'='*60}")
    print("CURRIER A: WORDS MOST CONCENTRATED AT LINE-FINAL POSITION")
    print(f"{'='*60}")
    # Include daiin explicitly
    target_words_a = ['daiin', 'or', 'ol', 'chor', 'chol', 'dar', 'cthy', 'cthor', 'cthol', 'shor', 'shol']
    for w in target_words_a:
        stats = word_position_stats(lines, w, 'A')
        if stats and stats['total_occ'] >= 5:
            print(f"  {w:<12}: n={stats['total_occ']:>4}, first={100*stats['frac_first']:.1f}%, last={100*stats['frac_last']:.1f}%, medial={100*stats['frac_medial']:.1f}%")

if __name__ == '__main__':
    main()
