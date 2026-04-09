"""
exp_105: "OTHER" Vocabulary Tier Analysis (H200) + Zipf's Law (H199) + Universal Vocabulary (H201)

H200: What are the mid-line words not classified by the positional grammar (OTHER tier)?
H199: Does Voynichese word frequency follow Zipf's law? What is the Zipf exponent α?
H201: Are there universal words appearing in ALL sections with high frequency?
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


def classify_tier_v3(word):
    """v3 classifier: PARA = {p,f,k,t}+anything + olf*/olke*/op*."""
    if word.startswith('pch') or word.startswith('psh') or (word.startswith('p') and len(word) >= 3):
        return 'PARA'
    if word.startswith('fch') or word.startswith('fsh') or (word.startswith('f') and len(word) >= 3):
        return 'PARA'
    if word.startswith('k') and not word.startswith('kch') and not word.startswith('ksh') and len(word) >= 2:
        return 'PARA'
    if word.startswith('t') and not word.startswith('tch') and not word.startswith('tsh') and len(word) >= 2:
        return 'PARA'
    if word.startswith('olf') and len(word) >= 4:
        return 'PARA'
    if word.startswith('olke') and len(word) >= 5:
        return 'PARA'
    if word.startswith('op') and len(word) >= 3:
        return 'PARA'
    if word.startswith('ych') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('dch') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('ysh') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('dsh') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('yk') and len(word) >= 4:
        return 'LINE_OPEN'
    if word.startswith('yt') and len(word) >= 4:
        return 'LINE_OPEN'
    if (word.startswith('tch') or word.startswith('tsh')) and len(word) >= 4:
        return 'WEAK_PARA'
    if (word.startswith('kch') or word.startswith('ksh')) and len(word) >= 4:
        return 'WEAK_PARA'
    if word.startswith('ch') and len(word) >= 3:
        return 'MID'
    if word.startswith('sh') and len(word) >= 3:
        return 'MID'
    if word.startswith('qo') and len(word) >= 4:
        return 'MID'
    return 'OTHER'


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

    records = []
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

            for pos, w in enumerate(words):
                records.append({
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'word': w,
                    'tier': classify_tier_v3(w),
                    'is_para_start': is_para_start and pos == 0,
                    'is_line_first': pos == 0,
                    'is_line_last': pos == len(words) - 1,
                    'pos': pos,
                })

    return records


def h200_other_vocab_analysis(records):
    """H200: What are the OTHER-tier mid-line words?"""
    print("=" * 70)
    print("H200: 'OTHER' Vocabulary Tier Analysis")
    print("=" * 70)

    other_records = [r for r in records if r['tier'] == 'OTHER']
    all_records = records

    print(f"\nTier composition overall:")
    tier_counts = Counter(r['tier'] for r in records)
    n_total = len(records)
    for tier, cnt in sorted(tier_counts.items(), key=lambda x: -x[1]):
        print(f"  {tier}: {cnt} ({cnt/n_total*100:.1f}%)")

    print(f"\n--- OTHER tier: onset distribution ---")
    other_onsets = Counter(r['word'][:2] for r in other_records)
    all_onsets = Counter(r['word'][:2] for r in all_records)
    n_other = len(other_records)
    n_all = len(all_records)

    print(f"Top 20 bigram onsets in OTHER tier (with enrichment vs all text):")
    print(f"{'Onset':<10} {'OTHER_n':>8} {'OTHER%':>8} {'All%':>8} {'Enrich':>8}")
    for onset, cnt in other_onsets.most_common(20):
        other_rate = cnt / n_other
        all_rate = all_onsets.get(onset, 0) / n_all
        enrich = other_rate / all_rate if all_rate > 0 else float('inf')
        enr_str = f"{enrich:.2f}×"
        print(f"  {onset:<10} {cnt:>8} {other_rate*100:>7.1f}% {all_rate*100:>7.1f}% {enr_str:>8}")

    print(f"\n--- OTHER tier: word length distribution ---")
    other_lengths = Counter(len(r['word']) for r in other_records)
    all_lengths = Counter(len(r['word']) for r in all_records)
    print(f"{'Length':<8} {'OTHER_n':>8} {'OTHER%':>8} {'All%':>7} {'Enrich':>8}")
    for length in sorted(other_lengths.keys()):
        cnt = other_lengths[length]
        other_rate = cnt / n_other
        all_rate = all_lengths.get(length, 0) / n_all
        enrich = other_rate / all_rate if all_rate > 0 else float('inf')
        print(f"  {length:<8} {cnt:>8} {other_rate*100:>7.1f}% {all_rate*100:>7.1f}% {enrich:>8.2f}×")

    print(f"\n--- OTHER tier: most frequent words ---")
    other_freq = Counter(r['word'] for r in other_records)
    all_freq = Counter(r['word'] for r in all_records)
    print(f"Top 40 OTHER words:")
    print(f"{'Word':<15} {'n_other':>8} {'n_all':>8} {'OTHER_rate‰':>12} {'Pos':>6}")
    for word, cnt in other_freq.most_common(40):
        word_records = [r for r in other_records if r['word'] == word]
        all_n = all_freq[word]
        lf = sum(1 for r in word_records if r['is_line_first']) / cnt
        ll = sum(1 for r in word_records if r['is_line_last']) / cnt
        print(f"  {word:<15} {cnt:>8} {all_n:>8}   LF={lf*100:.0f}% LL={ll*100:.0f}%")

    print(f"\n--- OTHER tier: onset sub-classification ---")
    # Classify OTHER words into sub-categories
    def classify_other_sub(word):
        if word.startswith('o'):
            if word.startswith('ok'):
                return 'o+k'
            if word.startswith('ot'):
                return 'o+t'
            if word.startswith('or'):
                return 'o+r'
            if word.startswith('ol'):
                return 'o+l'
            if word.startswith('od'):
                return 'o+d'
            if word.startswith('os'):
                return 'o+s'
            return 'o+other'
        if word.startswith('d') and len(word) <= 4:
            return 'd_short'
        if word.startswith('d'):
            return 'd_long'
        if word.startswith('s'):
            return 's_onset'
        if word.startswith('a'):
            return 'a_onset'
        if word.startswith('e'):
            return 'e_onset'
        if word.startswith('y'):
            return 'y_onset'
        if len(word) <= 3:
            return 'short_other'
        return 'other_long'

    sub_counts = Counter(classify_other_sub(r['word']) for r in other_records)
    print(f"OTHER sub-categories:")
    for cat, cnt in sorted(sub_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {cnt} ({cnt/n_other*100:.1f}%)")

    # Per-dialect OTHER analysis
    print(f"\n--- OTHER tier by dialect ---")
    for dialect in ['A', 'B']:
        d_other = [r for r in other_records if r['dialect'] == dialect]
        d_all = [r for r in records if r['dialect'] == dialect]
        n_d_other = len(d_other)
        n_d_all = len(d_all)
        if n_d_all == 0:
            continue
        d_freq = Counter(r['word'] for r in d_other)
        print(f"\n  Dialect {dialect}: OTHER={n_d_other}/{n_d_all} ({n_d_other/n_d_all*100:.1f}%)")
        print(f"  Top 20 {dialect} OTHER words:")
        for word, cnt in d_freq.most_common(20):
            word_records = [r for r in d_other if r['word'] == word]
            lf = sum(1 for r in word_records if r['is_line_first']) / cnt
            ll = sum(1 for r in word_records if r['is_line_last']) / cnt
            print(f"    {word}({cnt}): LF={lf*100:.0f}% LL={ll*100:.0f}%")


def h199_zipf_law(records):
    """H199: Does Voynichese follow Zipf's law?"""
    print("\n" + "=" * 70)
    print("H199: Zipf's Law — Word Rank-Frequency Distribution")
    print("=" * 70)

    def fit_zipf(counts_sorted):
        """Fit f(r) = C * r^(-alpha) on log-log using OLS."""
        n = len(counts_sorted)
        if n < 10:
            return None, None
        # Use ranks 1..n, frequencies counts_sorted
        log_r = [math.log(r + 1) for r in range(n)]
        log_f = [math.log(c) for c in counts_sorted]
        # OLS on log-log: skip top 10 (Zipf break) and bottom 10% (noise)
        start = 10
        end = max(start + 10, int(n * 0.7))
        log_r_s = log_r[start:end]
        log_f_s = log_f[start:end]
        n_pts = len(log_r_s)
        if n_pts < 5:
            return None, None
        mean_x = sum(log_r_s) / n_pts
        mean_y = sum(log_f_s) / n_pts
        num = sum((log_r_s[i] - mean_x) * (log_f_s[i] - mean_y) for i in range(n_pts))
        den = sum((log_r_s[i] - mean_x) ** 2 for i in range(n_pts))
        alpha = -num / den if den > 0 else 0  # negative slope → positive alpha
        log_C = mean_y + alpha * mean_x
        C = math.exp(log_C)
        return alpha, C

    # Overall Zipf
    all_freq = Counter(r['word'] for r in records)
    counts_sorted = sorted(all_freq.values(), reverse=True)
    alpha, C = fit_zipf(counts_sorted)
    n_words = len(counts_sorted)
    n_tokens = sum(counts_sorted)
    print(f"\nOverall: {n_tokens} tokens, {n_words} types")
    print(f"Zipf alpha = {alpha:.3f} (expected for NL: α≈1.0-1.5)")
    print(f"Heaps-Zipf consistency: expected alpha ≈ 1/β where β_herbal≈0.744 → predicted α≈1.34")

    # Sample rank-frequency
    print(f"\nTop 30 words (rank vs frequency):")
    print(f"{'Rank':>5} {'Word':<15} {'Freq':>6} {'Pred_f':>8} (C={C:.0f}, α={alpha:.3f})")
    for rank, (word, cnt) in enumerate(all_freq.most_common(30)):
        pred = C * ((rank + 1) ** (-alpha)) if alpha else 0
        print(f"  {rank+1:>5} {word:<15} {cnt:>6} {pred:>8.0f}")

    # By dialect
    print(f"\n--- Zipf's law by dialect ---")
    for dialect in ['A', 'B']:
        d_records = [r for r in records if r['dialect'] == dialect]
        d_freq = Counter(r['word'] for r in d_records)
        d_sorted = sorted(d_freq.values(), reverse=True)
        a, c = fit_zipf(d_sorted)
        print(f"  {dialect}: N={len(d_records)}, V={len(d_sorted)}, alpha={a:.3f}")

    # By section
    print(f"\n--- Zipf's law by section (dialect_section) ---")
    section_words = defaultdict(list)
    for r in records:
        key = f"{r['dialect']}_{r['section']}"
        section_words[key].append(r['word'])

    for key in sorted(section_words.keys()):
        words = section_words[key]
        if len(words) < 300:
            continue
        freq = Counter(words)
        sorted_counts = sorted(freq.values(), reverse=True)
        a, c = fit_zipf(sorted_counts)
        if a is None:
            continue
        print(f"  {key:<22}: N={len(words)}, V={len(sorted_counts)}, alpha={a:.3f}")


def h201_universal_vocabulary(records):
    """H201: Words appearing in ALL sections at high frequency."""
    print("\n" + "=" * 70)
    print("H201: Universal Vocabulary — Words Appearing in ALL Sections")
    print("=" * 70)

    # Define sections of interest (large sections only)
    target_sections = [
        ('A', 'herbal'), ('A', 'pharma'),
        ('B', 'cosmo'), ('B', 'stars'), ('B', 'herbal')
    ]

    section_data = {}
    for dialect, section in target_sections:
        key = f"{dialect}_{section}"
        sec_records = [r for r in records if r['dialect'] == dialect and r['section'] == section]
        n = len(sec_records)
        if n == 0:
            continue
        freq = Counter(r['word'] for r in sec_records)
        # Rate in per-mille (‰)
        rates = {word: cnt / n * 1000 for word, cnt in freq.items()}
        section_data[key] = {'n': n, 'freq': freq, 'rates': rates}

    # Find words appearing in ALL 5 sections at rate > 0.3‰ (at least 1 token per ~3000 words)
    threshold_perm = 0.3
    threshold_abs = 3  # at least 3 tokens per section

    keys = list(section_data.keys())
    universal_words = set()
    for word in set(r['word'] for r in records):
        appears_in_all = all(
            section_data.get(k, {}).get('freq', {}).get(word, 0) >= threshold_abs
            for k in keys
        )
        if appears_in_all:
            universal_words.add(word)

    print(f"\nSections analyzed: {keys}")
    print(f"Threshold: >= {threshold_abs} tokens in EACH of {len(keys)} sections")
    print(f"Universal words (in all sections, n>={threshold_abs}): {len(universal_words)}")

    # For each universal word, show its rate in each section
    # Rank by total frequency
    total_freq = Counter(r['word'] for r in records)
    universal_sorted = sorted(universal_words, key=lambda w: -total_freq[w])

    print(f"\n{'Word':<15} {'Total':>6} {'Tier':<12}", end="")
    for k in keys:
        print(f" {k:>12}", end="")
    print()
    for word in universal_sorted[:50]:
        tier = classify_tier_v3(word)
        print(f"  {word:<15} {total_freq[word]:>6} {tier:<12}", end="")
        for k in keys:
            rate = section_data.get(k, {}).get('rates', {}).get(word, 0)
            print(f" {rate:>12.1f}", end="")
        print()

    # Breakdown by tier
    print(f"\n--- Universal words by tier ---")
    tier_breakdown = Counter(classify_tier_v3(w) for w in universal_words)
    for tier, cnt in sorted(tier_breakdown.items(), key=lambda x: -x[1]):
        pct = cnt / len(universal_words) * 100 if universal_words else 0
        print(f"  {tier}: {cnt} ({pct:.1f}%)")

    # Section-specific vocabulary: words appearing in ONLY ONE section
    print(f"\n--- Section-exclusive vocabulary (appears in only 1 of {len(keys)} sections with n>={threshold_abs}) ---")
    for k in keys:
        exclusive = []
        for word, cnt in section_data[k]['freq'].items():
            if cnt < threshold_abs:
                continue
            appears_in_others = any(
                section_data.get(k2, {}).get('freq', {}).get(word, 0) >= threshold_abs
                for k2 in keys if k2 != k
            )
            if not appears_in_others:
                exclusive.append((word, cnt, classify_tier_v3(word)))
        exclusive.sort(key=lambda x: -x[1])
        print(f"\n  {k}: {len(exclusive)} exclusive words")
        for word, cnt, tier in exclusive[:20]:
            rate = section_data[k]['rates'][word]
            print(f"    {word}({cnt}, {rate:.1f}‰, {tier})")

    # What fraction of each section's token stream is universal vs exclusive?
    print(f"\n--- Token composition: universal vs exclusive vs shared ---")
    for k in keys:
        sec_records = [r for r in records if r['dialect'] == k.split('_')[0] and r['section'] == k.split('_')[1]]
        n = len(sec_records)
        n_universal = sum(1 for r in sec_records if r['word'] in universal_words)
        print(f"  {k}: N={n}, universal={n_universal} ({n_universal/n*100:.1f}%), other={n-n_universal} ({(n-n_universal)/n*100:.1f}%)")


def main():
    print("Loading data...")
    records = parse_voynich()
    print(f"Total word tokens: {len(records)}")

    h200_other_vocab_analysis(records)
    h199_zipf_law(records)
    h201_universal_vocabulary(records)


if __name__ == '__main__':
    main()
