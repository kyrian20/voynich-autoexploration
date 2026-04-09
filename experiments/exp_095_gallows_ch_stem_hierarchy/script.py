"""
exp_095: Gallows-ch Stem Hierarchy in A (H172), Internal Gallows Hierarchy (H171),
         Cross-Stem Generalization (H173)

H172: In A, p+ch = para-starter, d+ch/y+ch = line-openers, bare ch = mid-line.
      This would complete the gallows-demotion model for ch-stems:
      bare_ch(7%) < d+ch/y+ch(60-86%) = line-openers < p+ch = para-starters

H171: Internal gallows hierarchy: bare_p > bare_f > bare_t > bare_k?
      Test section-by-section consistency.

H173: Universal stem test — does the gallows-demotion model apply to sh-stems in A?
      p+sh = para-starter? d+sh/y+sh = line-openers? bare sh = mid-line?
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


def get_morphological_class(word):
    """Classify word by gallows-prefix morphology."""
    # Check for prefix + ch-stem
    if word.startswith('pch') and len(word) >= 4:
        return 'p+ch'
    if word.startswith('tch') and len(word) >= 4:
        return 't+ch'
    if word.startswith('kch') and len(word) >= 4:
        return 'k+ch'
    if word.startswith('fch') and len(word) >= 4:
        return 'f+ch'
    if word.startswith('dch') and len(word) >= 4:
        return 'd+ch'
    if word.startswith('ych') and len(word) >= 4:
        return 'y+ch'
    if word.startswith('ch') and len(word) >= 3:
        return 'bare_ch'
    # sh-stem
    if word.startswith('psh') and len(word) >= 4:
        return 'p+sh'
    if word.startswith('tsh') and len(word) >= 4:
        return 't+sh'
    if word.startswith('ksh') and len(word) >= 4:
        return 'k+sh'
    if word.startswith('dsh') and len(word) >= 4:
        return 'd+sh'
    if word.startswith('ysh') and len(word) >= 4:
        return 'y+sh'
    if word.startswith('sh') and len(word) >= 3:
        return 'bare_sh'
    # Bare gallows
    if word.startswith('p') and not word.startswith('pch') and not word.startswith('psh'):
        return 'bare_p_other'
    if word.startswith('t') and not word.startswith('tch') and not word.startswith('tsh'):
        return 'bare_t_other'
    if word.startswith('k') and not word.startswith('kch') and not word.startswith('ksh'):
        return 'bare_k_other'
    if word.startswith('f'):
        return 'bare_f_other'
    # qo-prefix
    if word.startswith('qok') and len(word) >= 4:
        return 'qo+k'
    if word.startswith('qot') and len(word) >= 4:
        return 'qo+t'
    if word.startswith('qo'):
        return 'qo+other'
    # y-gallows
    if word.startswith('yk') and len(word) >= 4:
        return 'y+k'
    if word.startswith('yt') and len(word) >= 4:
        return 'y+t'
    # Other
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
                    'folio': fb,
                    'dialect': dialect,
                    'section': section,
                    'is_para_start': is_para_start and pos == 0,
                    'is_line_first': pos == 0,
                    'is_line_last': pos == len(words) - 1,
                    'word': w,
                    'morph_class': get_morphological_class(w),
                    'line_len': len(words),
                    'pos': pos,
                })

    return records


def h172_gallows_ch_hierarchy(records):
    """H172: p+ch = para-starters in A? Complete gallows-demotion for ch-stems."""
    print("=" * 70)
    print("H172: Gallows-ch Stem Hierarchy in A (Para-Start Analysis)")
    print("=" * 70)

    a_records = [r for r in records if r['dialect'] == 'A']

    # Classes of interest for ch-stems
    ch_classes = ['p+ch', 't+ch', 'k+ch', 'f+ch', 'd+ch', 'y+ch', 'bare_ch']

    # Compute PS rate, LFirst%, LLast% for each ch class
    class_stats = defaultdict(lambda: {'total': 0, 'ps': 0, 'lf': 0, 'll': 0})
    for r in a_records:
        mc = r['morph_class']
        if mc in ch_classes:
            class_stats[mc]['total'] += 1
            if r['is_para_start']:
                class_stats[mc]['ps'] += 1
            if r['is_line_first']:
                class_stats[mc]['lf'] += 1
            if r['is_line_last']:
                class_stats[mc]['ll'] += 1

    print(f"\n--- A Dialect ch-Stem Positional Hierarchy (All Prefixes) ---")
    print(f"{'Class':<12} {'PS%':<10} {'LFirst%':<12} {'LLast%':<12} {'n_tokens':<10} {'Hypothesis'}")

    expected_order = {
        'p+ch': ('PARA-STARTER', '>>para'),
        't+ch': ('gallows-ch?', '?'),
        'k+ch': ('gallows-ch?', '?'),
        'f+ch': ('gallows-ch?', '?'),
        'y+ch': ('LINE-OPENER', '>>line'),
        'd+ch': ('LINE-OPENER', '>>line'),
        'bare_ch': ('MID-LINE', '>>mid'),
    }

    for mc in ['p+ch', 't+ch', 'k+ch', 'f+ch', 'y+ch', 'd+ch', 'bare_ch']:
        stats = class_stats[mc]
        n = stats['total']
        if n == 0:
            print(f"  {mc:<12} (no tokens)")
            continue
        ps = stats['ps'] / n
        lf = stats['lf'] / n
        ll = stats['ll'] / n
        hyp = expected_order.get(mc, ('?', '?'))[0]
        print(f"  {mc:<12} {ps*100:>6.1f}%    {lf*100:>6.1f}%       {ll*100:>6.1f}%       {n:<10} {hyp}")

    # Specific p+ch words
    print(f"\n--- p+ch Words in A (All Tokens) ---")
    pch_words = [(r['word'], r['is_para_start'], r['is_line_first']) for r in a_records if r['morph_class'] == 'p+ch']
    pch_word_counts = Counter(w for w, ps, lf in pch_words)
    pch_ps_counts = Counter(w for w, ps, lf in pch_words if ps)
    pch_lf_counts = Counter(w for w, ps, lf in pch_words if lf)

    for word, cnt in sorted(pch_word_counts.items(), key=lambda x: -x[1]):
        ps = pch_ps_counts.get(word, 0)
        lf = pch_lf_counts.get(word, 0)
        print(f"  {word}: total={cnt}, PS={ps} ({ps/cnt*100:.0f}%), LFirst={lf} ({lf/cnt*100:.0f}%)")

    # t+ch, k+ch, f+ch words
    for prefix_class in ['t+ch', 'k+ch', 'f+ch']:
        prefix_records = [(r['word'], r['is_para_start'], r['is_line_first'])
                         for r in a_records if r['morph_class'] == prefix_class]
        if prefix_records:
            print(f"\n--- {prefix_class} Words in A ---")
            word_counts = Counter(w for w, ps, lf in prefix_records)
            for word, cnt in sorted(word_counts.items(), key=lambda x: -x[1])[:10]:
                ps = sum(1 for w, p, l in prefix_records if w == word and p)
                lf = sum(1 for w, p, l in prefix_records if w == word and l)
                print(f"  {word}: total={cnt}, PS={ps}, LFirst={lf}")


def h171_internal_gallows_hierarchy(records):
    """H171: bare_p > bare_f > bare_t > bare_k? Internal gallows hierarchy."""
    print("\n" + "=" * 70)
    print("H171: Internal Gallows Hierarchy — p > f > t > k?")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_records = [r for r in records if r['dialect'] == dialect]
        print(f"\nDialect {dialect}:")
        print(f"  {'Section':<12} {'bare_p PS%':<14} {'bare_f PS%':<14} {'bare_t PS%':<14} {'bare_k PS%':<14}")

        all_sections = ['herbal', 'pharma', 'astro', 'cosmo', 'stars', 'other']

        for section in all_sections:
            s_records = [r for r in d_records if r['section'] == section]
            if len(s_records) < 10:
                continue
            s_ps = [r for r in s_records if r['is_para_start']]
            s_lf = [r for r in s_records if r['is_line_first']]

            total_ps = len(s_ps)
            total_lf = len(s_lf)

            if total_ps < 2:
                continue

            # Compute PS rate for each gallows class
            def ps_rate(mc_class):
                mc_ps = sum(1 for r in s_ps if r['morph_class'] == mc_class)
                mc_lf = sum(1 for r in s_lf if r['morph_class'] == mc_class)
                if mc_lf == 0:
                    return 0, mc_ps
                return mc_ps / mc_lf, mc_ps  # PSFirst rate among line-first tokens

            p_rate, p_n = ps_rate('bare_p_other')
            f_rate, f_n = ps_rate('bare_f_other')
            t_rate, t_n = ps_rate('bare_t_other')
            k_rate, k_n = ps_rate('bare_k_other')
            print(f"  {section:<12} p={p_rate*100:.0f}%(n={p_n:<3}) f={f_rate*100:.0f}%(n={f_n:<3}) t={t_rate*100:.0f}%(n={t_n:<3}) k={k_rate*100:.0f}%(n={k_n:<3})")


def h173_sh_stem_gallows_hierarchy(records):
    """H173: Does p+sh / t+sh also show para-start enrichment like p+ch?"""
    print("\n" + "=" * 70)
    print("H173: sh-Stem Gallows-Prefix Hierarchy in A")
    print("=" * 70)

    a_records = [r for r in records if r['dialect'] == 'A']

    sh_classes = ['p+sh', 't+sh', 'k+sh', 'd+sh', 'y+sh', 'bare_sh']

    class_stats = defaultdict(lambda: {'total': 0, 'ps': 0, 'lf': 0, 'll': 0})
    for r in a_records:
        mc = r['morph_class']
        if mc in sh_classes:
            class_stats[mc]['total'] += 1
            if r['is_para_start']:
                class_stats[mc]['ps'] += 1
            if r['is_line_first']:
                class_stats[mc]['lf'] += 1
            if r['is_line_last']:
                class_stats[mc]['ll'] += 1

    print(f"\n--- A Dialect sh-Stem Positional Hierarchy ---")
    print(f"{'Class':<12} {'PS%':<10} {'LFirst%':<12} {'LLast%':<12} {'n_tokens':<10}")
    for mc in ['p+sh', 't+sh', 'k+sh', 'y+sh', 'd+sh', 'bare_sh']:
        stats = class_stats[mc]
        n = stats['total']
        if n == 0:
            print(f"  {mc:<12} (no tokens)")
            continue
        ps = stats['ps'] / n
        lf = stats['lf'] / n
        ll = stats['ll'] / n
        print(f"  {mc:<12} {ps*100:>6.1f}%    {lf*100:>6.1f}%       {ll*100:>6.1f}%       {n}")

    # p+sh words
    print(f"\n--- p+sh Words in A ---")
    psh_records = [(r['word'], r['is_para_start'], r['is_line_first']) for r in a_records if r['morph_class'] == 'p+sh']
    psh_word_counts = Counter(w for w, ps, lf in psh_records)
    for word, cnt in sorted(psh_word_counts.items(), key=lambda x: -x[1]):
        ps = sum(1 for w, p, l in psh_records if w == word and p)
        lf = sum(1 for w, p, l in psh_records if w == word and l)
        print(f"  {word}: total={cnt}, PS={ps} ({ps/cnt*100:.0f}%), LFirst={lf} ({lf/cnt*100:.0f}%)")


def h174_complete_prefix_matrix(records):
    """H174: Full cross-tabulation of all prefix × stem combinations."""
    print("\n" + "=" * 70)
    print("H174: Complete Prefix × Stem Class Matrix — A Dialect")
    print("=" * 70)

    a_records = [r for r in records if r['dialect'] == 'A']

    all_classes = [
        ('PARA-LEVEL?', ['p+ch', 'p+sh', 'bare_p_other', 'bare_f_other', 't+ch', 't+sh', 'bare_t_other', 'k+ch', 'k+sh', 'bare_k_other', 'f+ch']),
        ('LINE-OPENER?', ['y+ch', 'd+ch', 'y+sh', 'd+sh', 'y+k', 'y+t']),
        ('MID-LINE?', ['bare_ch', 'bare_sh', 'qo+k', 'qo+t', 'qo+other']),
    ]

    print(f"\n{'Class':<16} {'PS%':<10} {'LFirst%':<12} {'LLast%':<12} {'n':<8}")
    for group_label, classes in all_classes:
        print(f"\n  [{group_label}]")
        for mc in classes:
            n = sum(1 for r in a_records if r['morph_class'] == mc)
            if n == 0:
                continue
            ps = sum(1 for r in a_records if r['morph_class'] == mc and r['is_para_start'])
            lf = sum(1 for r in a_records if r['morph_class'] == mc and r['is_line_first'])
            ll = sum(1 for r in a_records if r['morph_class'] == mc and r['is_line_last'])
            print(f"  {mc:<16} {ps/n*100:>6.1f}%    {lf/n*100:>6.1f}%       {ll/n*100:>6.1f}%       {n}")


def main():
    print("Loading data...")
    records = parse_voynich()
    print(f"Total word tokens: {len(records)}")

    a_tokens = sum(1 for r in records if r['dialect'] == 'A')
    b_tokens = sum(1 for r in records if r['dialect'] == 'B')
    print(f"A tokens: {a_tokens}, B tokens: {b_tokens}")

    print()
    h172_gallows_ch_hierarchy(records)
    h171_internal_gallows_hierarchy(records)
    h173_sh_stem_gallows_hierarchy(records)
    h174_complete_prefix_matrix(records)


if __name__ == '__main__':
    main()
