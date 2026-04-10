"""
exp_109: -am Closed Class Dialect Split (H211), 4-gram Repetition (H212), cth-Cluster Analysis (H213)

H211: Are -am words dialect/section-specific, or universal function words?
H212: Are there verbatim 4-word sequences repeated across multiple folios?
H213: Is cth- a productive morphological prefix parallel to qo- and o-?
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
    line_records = []  # For 4-gram analysis

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

            line_records.append({
                'dialect': dialect, 'section': section,
                'folio': fb, 'words': words, 'is_para_start': is_para_start
            })

            for pos, w in enumerate(words):
                records.append({
                    'dialect': dialect, 'section': section, 'folio': fb,
                    'word': w,
                    'is_para_start': is_para_start and pos == 0,
                    'is_line_first': pos == 0,
                    'is_line_last': pos == len(words) - 1,
                    'pos': pos,
                })

    return records, line_records


def h211_am_class_dialect_split(records):
    """H211: Dialect/section distribution of -am closed class."""
    print("=" * 70)
    print("H211: -am Closed Class Dialect and Section Distribution")
    print("=" * 70)

    # Identify -am words (words ending in 'am' that are NOT suffix=am — these ARE the word form)
    am_records = [r for r in records if r['word'].endswith('am') and len(r['word']) >= 3]
    oly_records = [r for r in records if r['word'] in ('oly', 'oldy', 'olal', 'olam')]
    all_records = records

    n_a = sum(1 for r in records if r['dialect'] == 'A')
    n_b = sum(1 for r in records if r['dialect'] == 'B')
    n_total = len(records)

    print(f"\nTotal body tokens: {n_total} (A={n_a}, B={n_b})")
    print(f"-am words (ending 'am', len>=3): {len(am_records)}")
    print(f"oly/oldy: {len(oly_records)}")

    # -am word dialect distribution
    print(f"\n--- -am words by dialect ---")
    am_a = [r for r in am_records if r['dialect'] == 'A']
    am_b = [r for r in am_records if r['dialect'] == 'B']
    print(f"  A: {len(am_a)} ({len(am_a)/n_a*100:.1f}% of A tokens)")
    print(f"  B: {len(am_b)} ({len(am_b)/n_b*100:.1f}% of B tokens)")
    print(f"  Dialect ratio A/B: {(len(am_a)/n_a)/(len(am_b)/n_b):.2f}×")

    # Individual -am words by A vs B rate
    print(f"\n--- Individual -am words: A vs B rate ---")
    am_a_freq = Counter(r['word'] for r in am_a)
    am_b_freq = Counter(r['word'] for r in am_b)
    all_am_words = set(list(am_a_freq.keys()) + list(am_b_freq.keys()))

    print(f"{'Word':<14} {'A_n':>5} {'A_rate‰':>9} {'B_n':>5} {'B_rate‰':>9} {'A/B':>6} {'LF%':>6} {'LL%':>6}")
    for word in sorted(all_am_words, key=lambda w: -(am_a_freq.get(w, 0) + am_b_freq.get(w, 0))):
        an = am_a_freq.get(word, 0)
        bn = am_b_freq.get(word, 0)
        if an + bn < 3:
            continue
        ar = an / n_a * 1000
        br = bn / n_b * 1000
        ratio = ar / br if br > 0 else float('inf')
        ratio_s = f"{ratio:.1f}×" if ratio != float('inf') else "∞"
        # Positional
        word_recs = [r for r in am_records if r['word'] == word]
        n = len(word_recs)
        lf = sum(1 for r in word_recs if r['is_line_first']) / n
        ll = sum(1 for r in word_recs if r['is_line_last']) / n
        print(f"  {word:<14} {an:>5} {ar:>8.2f}‰ {bn:>5} {br:>8.2f}‰ {ratio_s:>6} {lf*100:>5.0f}% {ll*100:>5.0f}%")

    # -am section distribution
    print(f"\n--- -am words: section distribution ---")
    section_totals = Counter(r['section'] for r in records)
    am_sections = Counter(r['section'] for r in am_records)
    for sect, cnt in sorted(am_sections.items(), key=lambda x: -x[1]):
        tot = section_totals.get(sect, 0)
        rate = cnt / tot * 1000 if tot > 0 else 0
        print(f"  {sect}: {cnt}/{tot} ({rate:.2f}‰)")

    # Compare -am vs oly/oldy by dialect
    print(f"\n--- -am vs oly/oldy complementarity by dialect ---")
    oly_a = [r for r in oly_records if r['dialect'] == 'A']
    oly_b = [r for r in oly_records if r['dialect'] == 'B']
    print(f"  -am: A={len(am_a)/n_a*1000:.2f}‰, B={len(am_b)/n_b*1000:.2f}‰, A/B={len(am_a)/n_a / (len(am_b)/n_b):.2f}×")
    print(f"  oly/oldy: A={len(oly_a)/n_a*1000:.2f}‰, B={len(oly_b)/n_b*1000:.2f}‰, B/A={len(oly_b)/n_b / max(len(oly_a)/n_a, 0.001):.2f}×")


def h212_fourgram_repetition(records, line_records):
    """H212: 4-gram cross-folio repetition."""
    print("\n" + "=" * 70)
    print("H212: 4-gram Cross-Folio Repetition Analysis")
    print("=" * 70)

    # Extract all 4-grams with folio tracking
    fourgram_folios = defaultdict(set)   # 4-gram → set of folios it appears on
    fourgram_counts = defaultdict(int)   # 4-gram → total occurrences

    for line in line_records:
        words = line['words']
        folio = line['folio']
        for i in range(len(words) - 3):
            fg = tuple(words[i:i+4])
            fourgram_folios[fg].add(folio)
            fourgram_counts[fg] += 1

    total_4grams = sum(fourgram_counts.values())
    unique_4grams = len(fourgram_counts)
    multi_folio_4grams = {fg: folios for fg, folios in fourgram_folios.items() if len(folios) >= 2}

    print(f"\nTotal 4-gram tokens: {total_4grams}")
    print(f"Unique 4-gram types: {unique_4grams}")
    print(f"4-grams appearing on 2+ distinct folios: {len(multi_folio_4grams)}")
    print(f"% of unique 4-grams that repeat across folios: {len(multi_folio_4grams)/unique_4grams*100:.3f}%")

    # Sort by number of folios, then by total count
    print(f"\n--- Top 30 cross-folio 4-grams (most folios) ---")
    print(f"{'4-gram':<45} {'n_folios':>8} {'n_total':>8} {'sections'}")
    for fg, folios in sorted(multi_folio_4grams.items(),
                              key=lambda x: (-len(x[1]), -fourgram_counts[x[0]]))[:30]:
        fg_str = ' '.join(fg)
        n_total = fourgram_counts[fg]
        # What sections?
        fg_sections = set()
        for line in line_records:
            words = line['words']
            for i in range(len(words) - 3):
                if tuple(words[i:i+4]) == fg:
                    fg_sections.add(line['section'])
        print(f"  {fg_str:<45} {len(folios):>8} {n_total:>8}  {', '.join(sorted(fg_sections))}")

    # By section
    print(f"\n--- 4-gram repetition by section ---")
    section_4gram_folios = defaultdict(lambda: defaultdict(set))
    for line in line_records:
        words = line['words']
        sect = line['section']
        folio = line['folio']
        for i in range(len(words) - 3):
            fg = tuple(words[i:i+4])
            section_4gram_folios[sect][fg].add(folio)

    for sect in sorted(section_4gram_folios.keys()):
        multi = sum(1 for fg, folios in section_4gram_folios[sect].items() if len(folios) >= 2)
        total = sum(len(folios) for folios in section_4gram_folios[sect].values())
        unique = len(section_4gram_folios[sect])
        pct = multi/unique*100 if unique > 0 else 0
        print(f"  {sect}: unique 4-grams={unique}, cross-folio={multi} ({pct:.3f}%)")

    # How many folios does the most repeated 4-gram span?
    max_folios = max(len(folios) for folios in multi_folio_4grams.values()) if multi_folio_4grams else 0
    print(f"\nMaximum folios spanned by a single 4-gram: {max_folios}")

    # 5-gram repetition
    print(f"\n--- 5-gram cross-folio repetition ---")
    fivegram_folios = defaultdict(set)
    for line in line_records:
        words = line['words']
        folio = line['folio']
        for i in range(len(words) - 4):
            fg = tuple(words[i:i+5])
            fivegram_folios[fg].add(folio)

    multi_folio_5grams = {fg: folios for fg, folios in fivegram_folios.items() if len(folios) >= 2}
    total_5g = sum(1 for _ in fivegram_folios)
    print(f"Unique 5-gram types: {total_5g}")
    print(f"5-grams on 2+ distinct folios: {len(multi_folio_5grams)}")

    if multi_folio_5grams:
        print(f"\nTop 10 cross-folio 5-grams:")
        for fg, folios in sorted(multi_folio_5grams.items(), key=lambda x: -len(x[1]))[:10]:
            fg_str = ' '.join(fg)
            print(f"  {fg_str}: {len(folios)} folios")


def h213_cth_cluster_analysis(records):
    """H213: cth- prefix — parallel to qo- and o-?"""
    print("\n" + "=" * 70)
    print("H213: cth- Cluster Analysis")
    print("=" * 70)

    # Extract cth-onset words (starts with 'cth')
    cth_records = [r for r in records if r['word'].startswith('cth')]
    all_records = records

    n_total = len(all_records)
    n_cth = len(cth_records)
    n_a = sum(1 for r in records if r['dialect'] == 'A')
    n_b = sum(1 for r in records if r['dialect'] == 'B')

    print(f"\nTotal body tokens: {n_total}")
    print(f"cth-onset words: {n_cth} ({n_cth/n_total*100:.2f}%)")

    # Dialect distribution
    cth_a = [r for r in cth_records if r['dialect'] == 'A']
    cth_b = [r for r in cth_records if r['dialect'] == 'B']
    print(f"\nDialect distribution:")
    print(f"  A: {len(cth_a)} ({len(cth_a)/n_a*1000:.2f}‰, {len(cth_a)/n_cth*100:.1f}% of cth)")
    print(f"  B: {len(cth_b)} ({len(cth_b)/n_b*1000:.2f}‰, {len(cth_b)/n_cth*100:.1f}% of cth)")
    print(f"  A/B rate ratio: {(len(cth_a)/n_a)/(len(cth_b)/n_b):.2f}×")

    # Top cth words
    print(f"\n--- Top cth words ---")
    cth_freq = Counter(r['word'] for r in cth_records)
    cth_a_freq = Counter(r['word'] for r in cth_a)
    cth_b_freq = Counter(r['word'] for r in cth_b)

    print(f"{'Word':<15} {'Total':>6} {'A':>5} {'B':>5} {'A_rate‰':>9} {'B_rate‰':>9} {'A/B':>6}")
    for word, total in cth_freq.most_common(25):
        an = cth_a_freq.get(word, 0)
        bn = cth_b_freq.get(word, 0)
        ar = an / n_a * 1000
        br = bn / n_b * 1000
        ratio = ar / br if br > 0 else float('inf')
        ratio_s = f"{ratio:.1f}×" if ratio != float('inf') else "∞"
        print(f"  {word:<15} {total:>6} {an:>5} {bn:>5} {ar:>8.2f}‰ {br:>8.2f}‰ {ratio_s:>6}")

    # Positional profile
    print(f"\n--- cth positional profile ---")
    def pos_prof(recs, label):
        n = len(recs)
        if n == 0:
            return
        ps = sum(1 for r in recs if r['is_para_start']) / n
        lf = sum(1 for r in recs if r['is_line_first']) / n
        ll = sum(1 for r in recs if r['is_line_last']) / n
        print(f"  {label}: n={n}, PS={ps*100:.1f}%, LFirst={lf*100:.1f}%, LLast={ll*100:.1f}%")

    pos_prof(cth_records, "cth ALL")
    pos_prof(cth_a, "cth A")
    pos_prof(cth_b, "cth B")

    # Suffix distribution for cth
    print(f"\n--- cth suffix distribution ---")
    def get_suffix(word):
        for suf in ['eedy', 'edy', 'eey', 'aiin', 'ain', 'ey', 'ol', 'or', 'dy', 'al', 'ar', 'y', 'n', 'r', 'l']:
            if word.endswith(suf) and len(word) > len(suf):
                return suf
        return 'other'

    cth_suffixes = Counter(get_suffix(r['word']) for r in cth_records)
    all_suffixes = Counter(get_suffix(r['word']) for r in all_records)
    n_all_suf = n_total

    print(f"{'Suffix':<10} {'cth_n':>6} {'cth%':>7} {'all%':>7} {'Enrich':>8}")
    for suf, cnt in sorted(cth_suffixes.items(), key=lambda x: -x[1]):
        cth_rate = cnt / n_cth
        all_rate = all_suffixes.get(suf, 0) / n_all_suf
        enrich = cth_rate / all_rate if all_rate > 0 else float('inf')
        enr_s = f"{enrich:.2f}×"
        print(f"  {suf:<10} {cnt:>6} {cth_rate*100:>6.1f}% {all_rate*100:>6.1f}% {enr_s:>8}")

    # Stem analysis: strip 'cth' and examine stems
    print(f"\n--- cth stem analysis (strip 'cth' prefix) ---")
    cth_stems = Counter(r['word'][3:] for r in cth_records)  # strip 'cth'
    # Do these stems appear as free words?
    all_word_freq = Counter(r['word'] for r in all_records)
    qo_word_freq = Counter(r['word'][2:] for r in all_records if r['word'].startswith('qo') and len(r['word']) >= 4)

    print(f"\nTop cth-stems (cth stripped):")
    for stem, cnt in cth_stems.most_common(20):
        # Is this stem a free word?
        free_cnt = all_word_freq.get(stem, 0)
        # Is this stem also a qo-stem?
        qo_cnt = qo_word_freq.get(stem, 0)
        # Does stem start with o/y/e (as expected for cth- as prefix)?
        onset_ok = stem[:1] in 'oyeaiurnl' if stem else False
        print(f"  cth+'{stem}' ({cnt}): free_word={free_cnt}, qo+'{stem}'={qo_cnt}, o/y/e-initial={onset_ok}")

    # Compare to qo- and o- prefix systems
    print(f"\n--- cth- vs qo- vs o- comparison ---")
    qo_records = [r for r in records if r['word'].startswith('qo') and len(r['word']) >= 4]
    o_records = [r for r in records if r['word'].startswith('o') and len(r['word']) >= 3 and
                 not r['word'].startswith('ok') and not r['word'].startswith('ot')]

    # Stem overlap: cth-stems ∩ qo-stems ∩ o-stems
    cth_stem_set = set(r['word'][3:] for r in cth_records)
    qo_stem_set = set(r['word'][2:] for r in qo_records)
    o_stem_set = set(r['word'][1:] for r in o_records)

    cth_qo = cth_stem_set & qo_stem_set
    cth_o = cth_stem_set & o_stem_set
    all_three = cth_stem_set & qo_stem_set & o_stem_set

    print(f"\n  cth-stems: {len(cth_stem_set)}")
    print(f"  qo-stems: {len(qo_stem_set)}")
    print(f"  o-stems: {len(o_stem_set)}")
    print(f"  cth ∩ qo stems: {len(cth_qo)} ({len(cth_qo)/len(cth_stem_set)*100:.1f}% of cth-stems)")
    print(f"  cth ∩ o stems: {len(cth_o)} ({len(cth_o)/len(cth_stem_set)*100:.1f}% of cth-stems)")
    print(f"  All three: {len(all_three)}")

    if cth_qo:
        print(f"\n  Shared cth∩qo stems (top by cth count):")
        for stem in sorted(cth_qo, key=lambda s: -cth_stems.get(s, 0))[:10]:
            cth_cnt = cth_stems.get(stem, 0)
            qo_cnt = qo_word_freq.get(stem, 0)
            print(f"    stem='{stem}': cth+stem={cth_cnt}, qo+stem={qo_cnt}")

    # Section distribution
    print(f"\n--- cth section distribution ---")
    cth_sections = Counter(r['section'] for r in cth_records)
    section_totals = Counter(r['section'] for r in records)
    for sect, cnt in sorted(cth_sections.items(), key=lambda x: -x[1]):
        tot = section_totals.get(sect, 0)
        rate = cnt / tot * 1000 if tot > 0 else 0
        print(f"  {sect}: {cnt}/{tot} ({rate:.2f}‰)")


def main():
    print("Loading data...")
    records, line_records = parse_voynich()
    print(f"Total body tokens: {len(records)}")
    print(f"Total body lines: {len(line_records)}")

    h211_am_class_dialect_split(records)
    h212_fourgram_repetition(records, line_records)
    h213_cth_cluster_analysis(records)


if __name__ == '__main__':
    main()
