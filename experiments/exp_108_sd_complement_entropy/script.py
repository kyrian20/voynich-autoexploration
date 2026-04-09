"""
exp_108: s/d-Onset Complementary Distribution (H208) + Suffix Entropy by Onset Class (H210)

H208: Are s-onset and d-onset line-openers in complementary or competing distribution?
      Does dialect determine which line-opener is used?

H210: Do grammar words have lower suffix entropy than content words?
      Quantify the grammar/content distinction via suffix Shannon entropy.
"""

import re
import math
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'


def folio_base(folio):
    return re.sub(r'\.\d+$', '', folio)


def classify_dialect(folio_stats):
    total = folio_stats.get('total', 0)
    if total == 0:
        return 'unknown'
    rate = (folio_stats.get('edy', 0) + folio_stats.get('eedy', 0)) / total
    return 'B' if rate >= 0.05 else 'A'


def classify_section(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if not m:
        return 'unknown'
    n = int(m.group(1))
    if n <= 57:
        return 'herbal'
    if 67 <= n <= 73:
        return 'astro'
    if 75 <= n <= 84:
        return 'cosmo'
    if 87 <= n <= 102:
        return 'pharma'
    if 103 <= n <= 116:
        return 'stars'
    return 'other'


def get_suffix(word):
    for suf in ['eedy', 'edy', 'eey', 'aiin', 'ain', 'ey', 'ol', 'or', 'dy', 'al', 'ar', 'y', 'n', 'r', 'l']:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return 'other'


def parse_voynich():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'):
                    folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'):
                    folio_word_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    # Parse with line context
    records = []
    line_records = []

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            dialect = folio_dialect.get(fb, 'unknown')
            section = classify_section(fb)

            lc_stripped = locus_code.lstrip('+*=/~&')
            is_para_start = lc_stripped.startswith('@')
            is_body = lc_stripped.lstrip('@').startswith('P')
            if not is_body:
                continue

            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue

            line_idx = len(line_records)
            line_records.append({
                'dialect': dialect,
                'section': section,
                'folio': fb,
                'words': words,
                'first_word': words[0],
                'last_word': words[-1],
                'is_para_start': is_para_start,
            })

            for pos, w in enumerate(words):
                records.append({
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'word': w,
                    'is_para_start': is_para_start and pos == 0,
                    'is_line_first': pos == 0,
                    'is_line_last': pos == len(words) - 1,
                    'pos': pos,
                    'line_idx': line_idx,
                })

    return records, line_records


def h208_sd_complementary_distribution(records, line_records):
    """H208: Are s/d line-openers complementary?"""
    print("=" * 70)
    print("H208: s/d-Onset Complementary Distribution Analysis")
    print("=" * 70)

    n_total_lines = len(line_records)
    print(f"\nTotal body lines: {n_total_lines}")

    # Classify each line by its opener type
    s_opener_lines = []
    d_opener_lines = []
    sd_both_lines = []  # lines that have BOTH s and d words (not just first word)
    neither_lines = []

    for line in line_records:
        first = line['first_word']
        words = line['words']
        has_s_first = first.startswith('s')
        has_d_first = (first.startswith('d') and
                       not first.startswith('dch') and not first.startswith('dsh'))

        # Does line have ANY s-onset word?
        has_any_s = any(w.startswith('s') for w in words)
        has_any_d = any(w.startswith('d') and not w.startswith('dch') and not w.startswith('dsh')
                        for w in words)

        if has_s_first and has_d_first:
            sd_both_lines.append(line)  # (this can't happen since first word is unique)
        elif has_s_first:
            s_opener_lines.append(line)
        elif has_d_first:
            d_opener_lines.append(line)
        else:
            neither_lines.append(line)

    print(f"\nLine-opener classification:")
    print(f"  s-onset opener: {len(s_opener_lines)} ({len(s_opener_lines)/n_total_lines*100:.1f}%)")
    print(f"  d-onset opener (bare): {len(d_opener_lines)} ({len(d_opener_lines)/n_total_lines*100:.1f}%)")
    print(f"  neither: {len(neither_lines)} ({len(neither_lines)/n_total_lines*100:.1f}%)")

    # Co-occurrence: on s-opener lines, how much d-content? And vice versa?
    print(f"\n--- Co-occurrence of s and d on same line ---")

    def count_d_on_line(line):
        return sum(1 for w in line['words'] if w.startswith('d') and
                   not w.startswith('dch') and not w.startswith('dsh'))

    def count_s_on_line(line):
        return sum(1 for w in line['words'] if w.startswith('s'))

    s_lines_d_count = [count_d_on_line(l) for l in s_opener_lines]
    d_lines_s_count = [count_s_on_line(l) for l in d_opener_lines]
    neither_s_count = [count_s_on_line(l) for l in neither_lines]
    neither_d_count = [count_d_on_line(l) for l in neither_lines]

    def avg_and_frac_nonzero(counts):
        if not counts:
            return 0, 0
        avg = sum(counts) / len(counts)
        frac = sum(1 for c in counts if c > 0) / len(counts)
        return avg, frac

    avg_d_on_s, frac_d_on_s = avg_and_frac_nonzero(s_lines_d_count)
    avg_s_on_d, frac_s_on_d = avg_and_frac_nonzero(d_lines_s_count)
    avg_s_on_n, frac_s_on_n = avg_and_frac_nonzero(neither_s_count)
    avg_d_on_n, frac_d_on_n = avg_and_frac_nonzero(neither_d_count)

    print(f"  On s-opener lines ({len(s_opener_lines)} lines):")
    print(f"    Average d-words per line: {avg_d_on_s:.2f}")
    print(f"    Fraction with ANY d-word: {frac_d_on_s*100:.1f}%")
    print(f"  On d-opener lines ({len(d_opener_lines)} lines):")
    print(f"    Average s-words per line: {avg_s_on_d:.2f}")
    print(f"    Fraction with ANY s-word: {frac_s_on_d*100:.1f}%")
    print(f"  On neither-opener lines ({len(neither_lines)} lines):")
    print(f"    Average s-words: {avg_s_on_n:.2f}, frac with s: {frac_s_on_n*100:.1f}%")
    print(f"    Average d-words: {avg_d_on_n:.2f}, frac with d: {frac_d_on_n*100:.1f}%")

    # Test complementarity: does s-opener → fewer d words (vs baseline)?
    baseline_d_per_line = sum(count_d_on_line(l) for l in line_records) / n_total_lines
    baseline_s_per_line = sum(count_s_on_line(l) for l in line_records) / n_total_lines
    print(f"\n  Baseline d-words per line (all lines): {baseline_d_per_line:.2f}")
    print(f"  Baseline s-words per line (all lines): {baseline_s_per_line:.2f}")
    print(f"  s-opener lines d-suppression: {avg_d_on_s/baseline_d_per_line:.2f}× baseline")
    print(f"  d-opener lines s-suppression: {avg_s_on_d/baseline_s_per_line:.2f}× baseline")

    # By dialect
    print(f"\n--- s vs d opener use by dialect ---")
    for dialect in ['A', 'B']:
        d_lines = [l for l in line_records if l['dialect'] == dialect]
        s_op = sum(1 for l in d_lines if l['first_word'].startswith('s'))
        d_op = sum(1 for l in d_lines if l['first_word'].startswith('d') and
                   not l['first_word'].startswith('dch') and not l['first_word'].startswith('dsh'))
        n = len(d_lines)
        print(f"  {dialect}: n_lines={n}, s-opener={s_op} ({s_op/n*100:.1f}%), d-opener={d_op} ({d_op/n*100:.1f}%)")

    # By section
    print(f"\n--- s vs d opener use by section ---")
    section_stats = defaultdict(lambda: {'n': 0, 's': 0, 'd': 0})
    for line in line_records:
        sect = line['section']
        section_stats[sect]['n'] += 1
        if line['first_word'].startswith('s'):
            section_stats[sect]['s'] += 1
        if (line['first_word'].startswith('d') and
                not line['first_word'].startswith('dch') and not line['first_word'].startswith('dsh')):
            section_stats[sect]['d'] += 1

    for sect, stats in sorted(section_stats.items(), key=lambda x: -x[1]['n']):
        n = stats['n']
        if n < 50:
            continue
        s_rate = stats['s'] / n
        d_rate = stats['d'] / n
        print(f"  {sect}: n={n}, s-opener={stats['s']} ({s_rate*100:.1f}%), d-opener={stats['d']} ({d_rate*100:.1f}%), s/d ratio={s_rate/d_rate:.2f}×")

    # Perfect complementarity test: lines where BOTH s and d appear as openers at pos>0
    print(f"\n--- Within-line s/d co-occurrence ---")
    lines_with_both = 0
    lines_with_s_only = 0
    lines_with_d_only = 0
    lines_with_neither = 0
    for line in line_records:
        w = line['words']
        has_s = any(wd.startswith('s') and len(wd) >= 2 for wd in w)
        has_d = any(wd.startswith('d') and not wd.startswith('dch') and not wd.startswith('dsh') and len(wd) >= 2 for wd in w)
        if has_s and has_d:
            lines_with_both += 1
        elif has_s:
            lines_with_s_only += 1
        elif has_d:
            lines_with_d_only += 1
        else:
            lines_with_neither += 1

    print(f"  Lines with BOTH s and d tokens: {lines_with_both} ({lines_with_both/n_total_lines*100:.1f}%)")
    print(f"  Lines with s-only: {lines_with_s_only} ({lines_with_s_only/n_total_lines*100:.1f}%)")
    print(f"  Lines with d-only: {lines_with_d_only} ({lines_with_d_only/n_total_lines*100:.1f}%)")
    print(f"  Lines with neither: {lines_with_neither} ({lines_with_neither/n_total_lines*100:.1f}%)")

    # Expected co-occurrence under independence
    p_s = (lines_with_both + lines_with_s_only) / n_total_lines
    p_d = (lines_with_both + lines_with_d_only) / n_total_lines
    expected_both = p_s * p_d * n_total_lines
    print(f"\n  Expected BOTH under independence: {expected_both:.0f}")
    print(f"  Observed BOTH: {lines_with_both}")
    print(f"  Co-occurrence ratio (obs/expected): {lines_with_both/expected_both:.2f}×")


def h210_suffix_entropy_by_class(records):
    """H210: Suffix entropy by onset class — grammar vs content words."""
    print("\n" + "=" * 70)
    print("H210: Suffix Entropy by Onset Class")
    print("=" * 70)

    # Define onset classes
    def get_onset_class(word):
        if word.startswith('dch') or word.startswith('dsh'):
            return 'd+gallows'
        if word.startswith('ych') or word.startswith('ysh') or word.startswith('yk') or word.startswith('yt'):
            return 'y+gallows'
        if word.startswith('pch') or word.startswith('psh'):
            return 'p+gallows'
        if word.startswith('tch') or word.startswith('tsh') or word.startswith('kch') or word.startswith('ksh'):
            return 'tk+gallows'
        if word.startswith('ch') and len(word) >= 3:
            return 'bare_ch'
        if word.startswith('sh') and len(word) >= 3:
            return 'bare_sh'
        if word.startswith('qo') and len(word) >= 4:
            return 'qo+stem'
        if word.startswith('ok'):
            return 'o+k'
        if word.startswith('ot'):
            return 'o+t'
        if word.startswith('ol') and len(word) >= 3:
            return 'o+l'
        if word.startswith('p') and len(word) >= 3 and not word.startswith('pch'):
            return 'bare_p'
        if word.startswith('f') and len(word) >= 3:
            return 'bare_f'
        if word.startswith('k') and len(word) >= 2:
            return 'bare_k'
        if word.startswith('t') and len(word) >= 2:
            return 'bare_t'
        if word.startswith('d') and len(word) >= 2:
            return 'bare_d'
        if word.startswith('s') and len(word) >= 2:
            return 'bare_s'
        if word.startswith('o') and len(word) >= 3:
            return 'o+other'
        return 'other'

    def shannon_entropy(counts):
        total = sum(counts.values())
        if total == 0:
            return 0
        return -sum((c/total) * math.log2(c/total) for c in counts.values() if c > 0)

    # Compute per-onset-class suffix distribution and entropy
    onset_suffix_data = defaultdict(Counter)
    for r in records:
        oc = get_onset_class(r['word'])
        suf = get_suffix(r['word'])
        onset_suffix_data[oc][suf] += 1

    print(f"\nSuffix entropy by onset class:")
    print(f"{'Onset class':<18} {'N':>7} {'H(suffix)':>10} {'Top suffix':>12} {'Top%':>7} {'Note'}")
    print("-" * 70)

    results = []
    for oc, suf_counts in sorted(onset_suffix_data.items(),
                                   key=lambda x: shannon_entropy(x[1])):
        n = sum(suf_counts.values())
        if n < 20:
            continue
        h = shannon_entropy(suf_counts)
        top_suf = max(suf_counts, key=suf_counts.get)
        top_rate = suf_counts[top_suf] / n
        results.append((oc, n, h, top_suf, top_rate, suf_counts))

    for oc, n, h, top_suf, top_rate, suf_counts in sorted(results, key=lambda x: x[2]):
        print(f"  {oc:<18} {n:>7} {h:>10.3f} {top_suf:>12} {top_rate*100:>6.1f}%")

    # Detailed breakdown for key classes
    print(f"\n--- Detailed: grammar-role classes (expected low entropy) ---")
    grammar_classes = ['bare_d', 'd+gallows', 'bare_p', 'bare_k', 'bare_t', 'bare_s', 'p+gallows']
    print(f"{'Class':<18} {'N':>6} {'H':>6} | {'aiin':>6} {'al':>6} {'ar':>6} {'edy':>6} {'eedy':>6} {'ol':>6} {'or':>6} {'y':>6} {'ey':>6}")
    for oc in grammar_classes:
        suf_counts = onset_suffix_data[oc]
        n = sum(suf_counts.values())
        if n < 10:
            continue
        h = shannon_entropy(suf_counts)
        def rate(s): return suf_counts.get(s, 0)/n*100 if n > 0 else 0
        print(f"  {oc:<18} {n:>6} {h:>6.3f} | "
              f"{rate('aiin'):>5.1f}% {rate('al'):>5.1f}% {rate('ar'):>5.1f}% "
              f"{rate('edy'):>5.1f}% {rate('eedy'):>5.1f}% {rate('ol'):>5.1f}% "
              f"{rate('or'):>5.1f}% {rate('y'):>5.1f}% {rate('ey'):>5.1f}%")

    print(f"\n--- Detailed: content-role classes (expected high entropy) ---")
    content_classes = ['bare_ch', 'bare_sh', 'qo+stem', 'o+k', 'o+t', 'y+gallows']
    for oc in content_classes:
        suf_counts = onset_suffix_data[oc]
        n = sum(suf_counts.values())
        if n < 10:
            continue
        h = shannon_entropy(suf_counts)
        def rate(s): return suf_counts.get(s, 0)/n*100 if n > 0 else 0
        print(f"  {oc:<18} {n:>6} {h:>6.3f} | "
              f"{rate('aiin'):>5.1f}% {rate('al'):>5.1f}% {rate('ar'):>5.1f}% "
              f"{rate('edy'):>5.1f}% {rate('eedy'):>5.1f}% {rate('ol'):>5.1f}% "
              f"{rate('or'):>5.1f}% {rate('y'):>5.1f}% {rate('ey'):>5.1f}%")

    # Entropy by word frequency tier
    print(f"\n--- Suffix entropy by word frequency tier ---")
    word_freq = Counter(r['word'] for r in records)
    freq_tiers = [
        ('hapax (freq=1)', lambda f: f == 1),
        ('low-freq (2-5)', lambda f: 2 <= f <= 5),
        ('medium-freq (6-20)', lambda f: 6 <= f <= 20),
        ('high-freq (21-100)', lambda f: 21 <= f <= 100),
        ('very-high-freq (>100)', lambda f: f > 100),
    ]
    for tier_name, freq_filter in freq_tiers:
        tier_words = {w for w, f in word_freq.items() if freq_filter(f)}
        tier_records = [r for r in records if r['word'] in tier_words]
        tier_suf = Counter(get_suffix(r['word']) for r in tier_records)
        n = sum(tier_suf.values())
        h = shannon_entropy(tier_suf)
        top = max(tier_suf, key=tier_suf.get) if tier_suf else 'N/A'
        top_rate = tier_suf.get(top, 0)/n if n > 0 else 0
        print(f"  {tier_name:<30}: n={n:>6}, H={h:.3f} bits, top_suffix='{top}' ({top_rate*100:.1f}%)")

    # Individual highly-formulaic words (low entropy = mostly one suffix)
    print(f"\n--- Most suffix-constrained frequent words (entropy by individual word) ---")
    # For words with multiple occurrences, compute their token-level entropy
    # (a word form itself has a fixed suffix, so this is more interesting for stem-level analysis)
    # Instead: group by STEM (strip suffix) and compute suffix diversity per stem
    stem_suffixes = defaultdict(Counter)
    for r in records:
        word = r['word']
        suf = get_suffix(word)
        if suf != 'other' and len(word) > len(suf):
            stem = word[:-len(suf)]
            stem_suffixes[stem][suf] += 1
        else:
            stem_suffixes[word]['other'] += 1

    # Find stems with most and least suffix diversity
    stem_entropy = []
    for stem, suf_counts in stem_suffixes.items():
        n_stem = sum(suf_counts.values())
        if n_stem < 10:
            continue
        h = shannon_entropy(suf_counts)
        stem_entropy.append((stem, n_stem, h, suf_counts))

    print(f"\nMost suffix-CONSTRAINED stems (low entropy, productive forms):")
    print(f"{'Stem':<15} {'n':>5} {'H':>6} {'Suffixes (top 3)'}")
    for stem, n, h, suf_counts in sorted(stem_entropy, key=lambda x: x[2])[:20]:
        top3 = suf_counts.most_common(3)
        top3_str = ', '.join(f"{s}={c}" for s, c in top3)
        print(f"  {stem:<15} {n:>5} {h:>6.3f}  {top3_str}")

    print(f"\nMost suffix-DIVERSE stems (high entropy, content word paradigms):")
    for stem, n, h, suf_counts in sorted(stem_entropy, key=lambda x: -x[2])[:20]:
        top3 = suf_counts.most_common(3)
        top3_str = ', '.join(f"{s}={c}" for s, c in top3)
        print(f"  {stem:<15} {n:>5} {h:>6.3f}  {top3_str}")


def main():
    print("Loading data...")
    records, line_records = parse_voynich()
    print(f"Total body tokens: {len(records)}")
    print(f"Total body lines: {len(line_records)}")

    h208_sd_complementary_distribution(records, line_records)
    h210_suffix_entropy_by_class(records)


if __name__ == '__main__':
    main()
