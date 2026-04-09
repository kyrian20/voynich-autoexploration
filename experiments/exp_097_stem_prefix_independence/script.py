"""
exp_097: Stem × Prefix Independence Test (H178), f+ch Cross-Dialect (H179)

H178: If prefix=position and stem=content, then the SAME stems should appear
      with p-, y-, d-, and bare-prefix forms. Test stem reuse across prefix classes.
      Are p+ch and y+ch using the SAME underlying ch-stems?

H179: Why is f+ch para-level in A but mid-line in B? Check folio distribution.
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


def extract_ch_stem(word):
    """Strip prefix to get bare ch-stem."""
    if word.startswith('pch'):
        return word[1:]  # pchor -> chor
    if word.startswith('fch'):
        return word[1:]  # fchor -> chor
    if word.startswith('tch'):
        return word[1:]  # tchor -> chor
    if word.startswith('kch'):
        return word[1:]  # kchor -> chor
    if word.startswith('ych'):
        return word[1:]  # ychor -> chor
    if word.startswith('dch'):
        return word[1:]  # dchor -> chor
    if word.startswith('ch'):
        return word  # chor -> chor
    return None


def extract_sh_stem(word):
    """Strip prefix to get bare sh-stem."""
    if word.startswith('psh'):
        return word[1:]  # pshol -> shol
    if word.startswith('ysh'):
        return word[1:]
    if word.startswith('dsh'):
        return word[1:]
    if word.startswith('tsh'):
        return word[1:]
    if word.startswith('ksh'):
        return word[1:]
    if word.startswith('sh'):
        return word
    return None


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
                ch_stem = extract_ch_stem(w)
                sh_stem = extract_sh_stem(w)
                prefix_type = 'bare'
                if w.startswith('p') and len(w) >= 3:
                    prefix_type = 'p'
                elif w.startswith('f') and len(w) >= 3:
                    prefix_type = 'f'
                elif w.startswith('t') and len(w) >= 3:
                    prefix_type = 't'
                elif w.startswith('k') and len(w) >= 3 and not w.startswith('kch') and not w.startswith('ksh'):
                    prefix_type = 'k'
                elif w.startswith('y') and len(w) >= 3:
                    prefix_type = 'y'
                elif w.startswith('d') and len(w) >= 3:
                    prefix_type = 'd'
                elif w.startswith('qo') and len(w) >= 4:
                    prefix_type = 'qo'

                records.append({
                    'folio': fb,
                    'dialect': dialect,
                    'section': section,
                    'is_para_start': is_para_start and pos == 0,
                    'is_line_first': pos == 0,
                    'is_line_last': pos == len(words) - 1,
                    'word': w,
                    'ch_stem': ch_stem,
                    'sh_stem': sh_stem,
                    'prefix_type': prefix_type,
                })

    return records


def h178_stem_prefix_independence(records):
    """H178: Do the same ch-stems appear with p-, y-, d-, and bare-prefix?"""
    print("=" * 70)
    print("H178: Stem × Prefix Independence — Do Same Stems Reuse Across Prefix Classes?")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_records = [r for r in records if r['dialect'] == dialect]
        ch_records = [r for r in d_records if r['ch_stem'] is not None]

        print(f"\n{'='*50}")
        print(f"Dialect {dialect} — ch-stem × prefix distribution")

        # For each prefix class, what stems appear?
        prefix_stems = {}
        for prefix in ['p', 'y', 'd', 'bare']:
            if prefix == 'p':
                recs = [r for r in ch_records if r['word'].startswith('pch')]
            elif prefix == 'y':
                recs = [r for r in ch_records if r['word'].startswith('ych')]
            elif prefix == 'd':
                recs = [r for r in ch_records if r['word'].startswith('dch')]
            else:
                recs = [r for r in ch_records if r['word'].startswith('ch')]

            stem_counts = Counter(r['ch_stem'] for r in recs)
            prefix_stems[prefix] = stem_counts

        # Find stems that appear in all 4 prefix classes
        all_stems = set()
        for sc in prefix_stems.values():
            all_stems.update(sc.keys())

        print(f"\nTotal unique ch-stems in {dialect}: {len(all_stems)}")

        stems_in_all = [s for s in all_stems if all(s in prefix_stems[p] for p in ['p', 'y', 'd', 'bare'])]
        stems_in_3 = [s for s in all_stems if sum(1 for p in ['p', 'y', 'd', 'bare'] if s in prefix_stems[p]) == 3]
        stems_in_2 = [s for s in all_stems if sum(1 for p in ['p', 'y', 'd', 'bare'] if s in prefix_stems[p]) == 2]
        stems_in_1 = [s for s in all_stems if sum(1 for p in ['p', 'y', 'd', 'bare'] if s in prefix_stems[p]) == 1]

        print(f"Stems in ALL 4 prefix classes (p, y, d, bare): {len(stems_in_all)} → {sorted(stems_in_all)}")
        print(f"Stems in exactly 3 prefix classes: {len(stems_in_3)}")
        print(f"Stems in exactly 2 prefix classes: {len(stems_in_2)}")
        print(f"Stems in exactly 1 prefix class: {len(stems_in_1)}")

        # Show the shared-stem table
        if stems_in_all:
            print(f"\n--- Stems in ALL 4 prefix classes (p+ch, y+ch, d+ch, bare_ch) ---")
            print(f"{'Stem':<12} {'p+stem n':<12} {'y+stem n':<12} {'d+stem n':<12} {'bare n':<12}")
            for stem in sorted(stems_in_all, key=lambda s: -prefix_stems['bare'].get(s, 0)):
                print(f"  {stem:<10} {prefix_stems['p'].get(stem,0):<12} {prefix_stems['y'].get(stem,0):<12} {prefix_stems['d'].get(stem,0):<12} {prefix_stems['bare'].get(stem,0):<12}")

        # Top stems by prefix class
        print(f"\n--- Top stems by prefix class ---")
        for prefix in ['p', 'y', 'd', 'bare']:
            top = prefix_stems[prefix].most_common(5)
            print(f"  {prefix}+ch: {top}")

        # Overall stem reuse rate
        n_reused = len([s for s in all_stems if sum(1 for p in ['p', 'y', 'd', 'bare'] if s in prefix_stems[p]) >= 2])
        n_exclusive = len(stems_in_1)
        print(f"\nStem reuse: {n_reused}/{len(all_stems)} stems appear in 2+ prefix classes ({n_reused/len(all_stems)*100:.1f}%)")
        print(f"Exclusive stems: {n_exclusive}/{len(all_stems)} stems appear in only 1 prefix class ({n_exclusive/len(all_stems)*100:.1f}%)")


def h179_f_ch_cross_dialect(records):
    """H179: Why is f+ch para-level in A but mid-line in B?"""
    print("\n" + "=" * 70)
    print("H179: f+ch Cross-Dialect Asymmetry Analysis")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_records = [r for r in records if r['dialect'] == dialect]
        fch_records = [r for r in d_records if r['word'].startswith('fch') and len(r['word']) >= 4]

        print(f"\n--- f+ch in Dialect {dialect} ---")
        n = len(fch_records)
        if n == 0:
            print(f"  (no f+ch tokens)")
            continue

        ps = sum(1 for r in fch_records if r['is_para_start'])
        lf = sum(1 for r in fch_records if r['is_line_first'])
        ll = sum(1 for r in fch_records if r['is_line_last'])

        print(f"  Total f+ch tokens: {n}")
        print(f"  PS: {ps} ({ps/n*100:.1f}%), LFirst: {lf} ({lf/n*100:.1f}%), LLast: {ll} ({ll/n*100:.1f}%)")

        # Section distribution
        section_counts = Counter(r['section'] for r in fch_records)
        ps_by_section = Counter(r['section'] for r in fch_records if r['is_para_start'])
        print(f"\n  Section distribution:")
        for sect, cnt in sorted(section_counts.items(), key=lambda x: -x[1]):
            ps_cnt = ps_by_section.get(sect, 0)
            print(f"    {sect}: {cnt} tokens ({ps_cnt} at para-start)")

        # Word forms
        word_counts = Counter(r['word'] for r in fch_records)
        word_ps = Counter(r['word'] for r in fch_records if r['is_para_start'])
        print(f"\n  f+ch word forms:")
        for word, cnt in sorted(word_counts.items(), key=lambda x: -x[1]):
            ps_cnt = word_ps.get(word, 0)
            print(f"    {word}: {cnt} tokens ({ps_cnt} PS)")

        # Folio distribution
        folio_counts = Counter(r['folio'] for r in fch_records)
        print(f"\n  Folio distribution: {folio_counts.most_common(8)}")


def h180_stem_productivity_by_prefix(records):
    """H180: Are some stems 'productive' (appear with many prefixes) vs 'fixed' (prefix-specific)?"""
    print("\n" + "=" * 70)
    print("H180: Stem Productivity — Multi-Prefix vs Single-Prefix ch-Stems")
    print("=" * 70)

    # Focus on A dialect where we have most data
    a_records = [r for r in records if r['dialect'] == 'A']
    ch_records = [r for r in a_records if r['ch_stem'] is not None]

    # For each stem, count how many prefix forms it appears in
    stem_prefix_sets = defaultdict(set)
    stem_prefix_counts = defaultdict(lambda: defaultdict(int))

    for r in ch_records:
        stem = r['ch_stem']
        word = r['word']
        if word.startswith('pch'):
            prefix = 'p'
        elif word.startswith('ych'):
            prefix = 'y'
        elif word.startswith('dch'):
            prefix = 'd'
        elif word.startswith('ch'):
            prefix = 'bare'
        elif word.startswith('tch'):
            prefix = 't'
        elif word.startswith('kch'):
            prefix = 'k'
        elif word.startswith('fch'):
            prefix = 'f'
        else:
            prefix = 'other'

        stem_prefix_sets[stem].add(prefix)
        stem_prefix_counts[stem][prefix] += 1

    # Categorize stems
    print(f"\n--- Stem Productivity Distribution (A dialect, ch-stems) ---")
    print(f"(by number of distinct prefix classes the stem appears with)")

    for n_prefixes in range(7, 0, -1):
        stems = [s for s, pset in stem_prefix_sets.items() if len(pset) == n_prefixes]
        total_tokens = sum(sum(stem_prefix_counts[s].values()) for s in stems)
        if stems:
            print(f"\n  Stems with {n_prefixes} prefix classes (n={len(stems)}, total_tokens={total_tokens}):")
            for s in sorted(stems, key=lambda x: -sum(stem_prefix_counts[x].values()))[:10]:
                counts = {p: stem_prefix_counts[s].get(p, 0) for p in ['p', 'y', 'd', 'bare', 't', 'k', 'f']}
                print(f"    {s}: {counts}")

    # Summary statistics
    print(f"\n--- Summary ---")
    stem_n_prefixes = {s: len(pset) for s, pset in stem_prefix_sets.items()}
    for n in range(1, 8):
        count = sum(1 for v in stem_n_prefixes.values() if v == n)
        print(f"  {n} prefix class(es): {count} stems")


def main():
    print("Loading data...")
    records = parse_voynich()
    print(f"Total word tokens: {len(records)}")

    a_count = sum(1 for r in records if r['dialect'] == 'A' and r['is_line_first'])
    b_count = sum(1 for r in records if r['dialect'] == 'B' and r['is_line_first'])
    print(f"A dialect line-first: {a_count}, B dialect: {b_count}")

    print()
    h178_stem_prefix_independence(records)
    h179_f_ch_cross_dialect(records)
    h180_stem_productivity_by_prefix(records)


if __name__ == '__main__':
    main()
