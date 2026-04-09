"""
exp_102: Content Word Analysis by Section (H193, H194)

H193: Is grammar strictness driven by section or paragraph length?
      Within herbal A, do shorter paragraphs follow grammar less strictly?

H194: Content Word (bare_ch/sh) Vocabulary by Section
      The positional grammar identifies p/k/t/f forms as para-markers,
      y/d+ch as line-openers, and bare_ch/sh as content words.
      Do the content words (bare_ch/sh stems) show section-specific patterns?
"""

import re
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
    if (word.startswith('pch') or word.startswith('psh') or
            (word.startswith('p') and len(word) >= 3)):
        return 'PARA'
    if (word.startswith('fch') or word.startswith('fsh') or
            (word.startswith('f') and len(word) >= 3)):
        return 'PARA'
    if (word.startswith('k') and not word.startswith('kch') and
            not word.startswith('ksh') and len(word) >= 2):
        return 'PARA'
    if (word.startswith('t') and not word.startswith('tch') and
            not word.startswith('tsh') and len(word) >= 2):
        return 'PARA'
    # o-onset PARA forms (from exp_101: olf*, op* contain PARA morphology)
    if word.startswith('olf') and len(word) >= 4:
        return 'PARA'
    if word.startswith('olke') and len(word) >= 5:
        return 'PARA'
    if word.startswith('op') and len(word) >= 3:
        return 'PARA'
    # LINE_OPEN tier
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
    # WEAK_PARA
    if (word.startswith('tch') or word.startswith('tsh')) and len(word) >= 4:
        return 'WEAK_PARA'
    if (word.startswith('kch') or word.startswith('ksh')) and len(word) >= 4:
        return 'WEAK_PARA'
    # MID (content words)
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

    paragraphs = {}
    all_words_by_section = defaultdict(list)
    current_para = None
    para_count = 0

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

            # All words for content analysis
            key = f"{dialect}_{section}"
            all_words_by_section[key].extend(words)

            if is_para_start:
                para_count += 1
                current_para = para_count
                paragraphs[current_para] = {
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'lines': []
                }
            if current_para is not None:
                paragraphs[current_para]['lines'].append(words)

    return paragraphs, all_words_by_section


def h193_section_vs_length(paragraphs):
    """H193: Is grammar strictness driven by section or length?"""
    print("=" * 70)
    print("H193: Section vs Length — Grammar Strictness Within Sections")
    print("=" * 70)

    # Focus on herbal A (large enough for sub-binning)
    sections_to_test = [
        ('A', 'herbal', 'Herbal A (expected: strict grammar)'),
        ('A', 'pharma', 'Pharma A (expected: intermediate)'),
        ('B', 'stars', 'Stars B (expected: very long, strict)'),
        ('B', 'cosmo', 'Cosmo B (expected: long, strict)'),
    ]

    for dialect, section, label in sections_to_test:
        sect_paras = {pid: p for pid, p in paragraphs.items()
                      if p['dialect'] == dialect and p['section'] == section and p['lines']}
        if len(sect_paras) < 5:
            continue

        print(f"\n--- {label} (n={len(sect_paras)}) ---")
        lengths = [len(p['lines']) for p in sect_paras.values()]
        print(f"  Length range: {min(lengths)}-{max(lengths)}, mean={sum(lengths)/len(lengths):.1f}")

        # Split by median
        median_len = sorted(lengths)[len(lengths)//2]
        short_paras = {pid: p for pid, p in sect_paras.items() if len(p['lines']) <= median_len}
        long_paras = {pid: p for pid, p in sect_paras.items() if len(p['lines']) > median_len}

        for label2, bin_paras in [('short(≤median)', short_paras), ('long(>median)', long_paras)]:
            if not bin_paras:
                continue
            ps_words = [p['lines'][0][0] for p in bin_paras.values()
                        if p['lines'] and p['lines'][0]]
            wp_words = [lines[0] for p in bin_paras.values()
                        for lines in p['lines'][1:] if lines]
            n_ps = len(ps_words)
            n_wp = len(wp_words)
            if n_ps == 0:
                continue

            para_ps = sum(1 for w in ps_words if classify_tier_v3(w) == 'PARA')
            lo_ps = sum(1 for w in ps_words if classify_tier_v3(w) == 'LINE_OPEN')
            other_ps = sum(1 for w in ps_words if classify_tier_v3(w) == 'OTHER')
            para_wp = sum(1 for w in wp_words if classify_tier_v3(w) == 'PARA')

            para_enrich = (para_ps/n_ps) / (para_wp/n_wp) if para_wp > 0 and n_wp > 0 else float('inf')
            bin_lengths = [len(p['lines']) for p in bin_paras.values()]
            mean_len = sum(bin_lengths) / len(bin_lengths)

            print(f"  {label2:<20} n={len(bin_paras):2d} (mean_len={mean_len:.1f}): "
                  f"PARA={para_ps/n_ps*100:.1f}%, LO={lo_ps/n_ps*100:.1f}%, "
                  f"OTHER={other_ps/n_ps*100:.1f}%, enrich={para_enrich:.2f}×")


def h194_content_word_analysis(all_words_by_section):
    """H194: Content word (bare_ch/sh) vocabulary by section."""
    print("\n" + "=" * 70)
    print("H194: Content Word (bare_ch/sh) Vocabulary Analysis by Section")
    print("=" * 70)

    # Content words = words classified as MID tier (bare_ch, bare_sh, qo+gallows)
    # Focus on bare_ch (most common mid-line content words)

    section_ch_words = {}
    section_all_words = {}

    for key, words in all_words_by_section.items():
        ch_words = [w for w in words if w.startswith('ch') and len(w) >= 3]
        sh_words = [w for w in words if w.startswith('sh') and len(w) >= 3]
        section_ch_words[key] = Counter(ch_words)
        section_all_words[key] = Counter(words)

    print("\n--- Top bare_ch Words by Section ---")
    for key in sorted(section_ch_words.keys()):
        ch_counter = section_ch_words[key]
        total_words = sum(section_all_words[key].values())
        total_ch = sum(ch_counter.values())
        if total_ch < 10:
            continue
        top = ch_counter.most_common(8)
        top_str = ', '.join(f"{w}({n})" for w, n in top)
        ch_rate = total_ch / total_words * 100
        print(f"\n  {key} (total={total_words}, ch={total_ch} ({ch_rate:.1f}%)):")
        print(f"    Top: {top_str}")

    # Cross-section ch-stem comparison
    # What are the most section-distinctive ch words?
    print("\n--- Section-Distinctive ch-Words (present in one section but not others) ---")

    # Focus on A sections
    a_sections = {k: v for k, v in section_ch_words.items() if k.startswith('A_')}
    b_sections = {k: v for k, v in section_ch_words.items() if k.startswith('B_')}

    all_a_ch = Counter()
    for counter in a_sections.values():
        all_a_ch.update(counter)

    print("\nA dialect ch-words by section:")
    for key, counter in sorted(a_sections.items()):
        if sum(counter.values()) < 20:
            continue
        # Words enriched in this section vs other A sections
        enriched = []
        total_this = sum(counter.values())
        total_other = sum((all_a_ch - counter).values())
        for word, count in counter.most_common(50):
            other_count = all_a_ch.get(word, 0) - count
            rate_this = count / total_this if total_this > 0 else 0
            rate_other = other_count / total_other if total_other > 0 else 0
            enrich = rate_this / rate_other if rate_other > 0 else float('inf')
            if count >= 3 and enrich >= 2.0:
                enriched.append((word, count, enrich))
        enriched.sort(key=lambda x: -x[2])
        print(f"\n  {key}: section-enriched ch-words:")
        for word, cnt, enrich in enriched[:10]:
            enr_str = f"{enrich:.1f}×" if enrich != float('inf') else "∞"
            print(f"    {word}: {cnt} ({enr_str} over other A)")

    all_b_ch = Counter()
    for counter in b_sections.values():
        all_b_ch.update(counter)

    print("\nB dialect ch-words by section:")
    for key, counter in sorted(b_sections.items()):
        if sum(counter.values()) < 20:
            continue
        enriched = []
        total_this = sum(counter.values())
        total_other = sum((all_b_ch - counter).values())
        for word, count in counter.most_common(50):
            other_count = all_b_ch.get(word, 0) - count
            rate_this = count / total_this if total_this > 0 else 0
            rate_other = other_count / total_other if total_other > 0 else 0
            enrich = rate_this / rate_other if rate_other > 0 else float('inf')
            if count >= 3 and enrich >= 2.0:
                enriched.append((word, count, enrich))
        enriched.sort(key=lambda x: -x[2])
        print(f"\n  {key}: section-enriched ch-words:")
        for word, cnt, enrich in enriched[:10]:
            enr_str = f"{enrich:.1f}×" if enrich != float('inf') else "∞"
            print(f"    {word}: {cnt} ({enr_str} over other B)")

    # Tier distribution by section
    print("\n--- Tier Distribution by Section ---")
    print(f"{'Section':<20} {'PARA%':>7} {'LO%':>7} {'WEAK%':>6} {'MID%':>6} {'OTHER%':>7} {'n':>7}")
    for key in sorted(all_words_by_section.keys()):
        words = all_words_by_section[key]
        if len(words) < 100:
            continue
        tier_counts = Counter(classify_tier_v3(w) for w in words)
        n = len(words)
        print(f"  {key:<20} "
              f"{tier_counts.get('PARA',0)/n*100:>6.1f}% "
              f"{tier_counts.get('LINE_OPEN',0)/n*100:>6.1f}% "
              f"{tier_counts.get('WEAK_PARA',0)/n*100:>5.1f}% "
              f"{tier_counts.get('MID',0)/n*100:>5.1f}% "
              f"{tier_counts.get('OTHER',0)/n*100:>6.1f}% "
              f"{n:>7}")


def main():
    print("Loading data...")
    paragraphs, all_words_by_section = parse_voynich()
    n_a = sum(1 for p in paragraphs.values() if p['dialect'] == 'A')
    n_b = sum(1 for p in paragraphs.values() if p['dialect'] == 'B')
    print(f"Total paragraphs: {len(paragraphs)} (A={n_a}, B={n_b})")

    h193_section_vs_length(paragraphs)
    h194_content_word_analysis(all_words_by_section)


if __name__ == '__main__':
    main()
