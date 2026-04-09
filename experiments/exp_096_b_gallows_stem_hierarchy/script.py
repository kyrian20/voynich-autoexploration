"""
exp_096: B Dialect Gallows+Stem Para-Start Hierarchy (H175), k-onset Line-Position Analysis (H176),
         Cross-Dialect Gallows Grammar Unification (H177)

H175: Does B show p+ch/f+ch = para-starters, y+k/qo+k = line-opener/mid-line?
      Test the B analog of A's gallows-demotion model.

H176: B k-onset is more concentrated at line-first generally (not just para-starts)?
      Is the B k-onset 9.91× enrichment at para-starts driven by para-specificity
      or by general line-initial concentration?

H177: Unified cross-dialect gallows grammar model — are the positional functions
      identical across A and B, with different stem preferences as the only difference?
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


def get_morph_class(word):
    """Morphological classification with gallows prefix detection."""
    # Gallows + ch stem
    if word.startswith('pch') and len(word) >= 4:
        return 'p+ch'
    if word.startswith('fch') and len(word) >= 4:
        return 'f+ch'
    if word.startswith('tch') and len(word) >= 4:
        return 't+ch'
    if word.startswith('kch') and len(word) >= 4:
        return 'k+ch'
    # Gallows + sh stem
    if word.startswith('psh') and len(word) >= 4:
        return 'p+sh'
    if word.startswith('fsh') and len(word) >= 4:
        return 'f+sh'
    if word.startswith('tsh') and len(word) >= 4:
        return 't+sh'
    if word.startswith('ksh') and len(word) >= 4:
        return 'k+sh'
    # Gallows + k/t stem (double gallows)
    if word.startswith('pk') and len(word) >= 4:
        return 'p+k'
    if word.startswith('pt') and len(word) >= 4:
        return 'p+t'
    if word.startswith('fk') and len(word) >= 4:
        return 'f+k'
    if word.startswith('ft') and len(word) >= 4:
        return 'f+t'
    # y + gallows
    if word.startswith('yk') and len(word) >= 4:
        return 'y+k'
    if word.startswith('yt') and len(word) >= 4:
        return 'y+t'
    if word.startswith('ych') and len(word) >= 4:
        return 'y+ch'
    if word.startswith('ysh') and len(word) >= 4:
        return 'y+sh'
    # d + stem
    if word.startswith('dch') and len(word) >= 4:
        return 'd+ch'
    if word.startswith('dsh') and len(word) >= 4:
        return 'd+sh'
    # qo + gallows
    if word.startswith('qok') and len(word) >= 4:
        return 'qo+k'
    if word.startswith('qot') and len(word) >= 4:
        return 'qo+t'
    if word.startswith('qop') and len(word) >= 4:
        return 'qo+p'
    if word.startswith('qof') and len(word) >= 4:
        return 'qo+f'
    if word.startswith('qo'):
        return 'qo+other'
    # Bare gallows
    if word.startswith('p') and len(word) >= 2:
        return 'bare_p'
    if word.startswith('f') and len(word) >= 2:
        return 'bare_f'
    if word.startswith('t') and not word.startswith('tch') and not word.startswith('tsh') and len(word) >= 2:
        return 'bare_t'
    if word.startswith('k') and not word.startswith('kch') and not word.startswith('ksh') and len(word) >= 2:
        return 'bare_k'
    # ch/sh
    if word.startswith('ch'):
        return 'bare_ch'
    if word.startswith('sh'):
        return 'bare_sh'
    # Others
    if word.startswith('y'):
        return 'y+other'
    if word.startswith('d'):
        return 'd+other'
    if word.startswith('s'):
        return 's'
    if word.startswith('o'):
        return 'o'
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
                    'morph_class': get_morph_class(w),
                    'pos': pos,
                    'line_len': len(words),
                })

    return records


def h175_b_gallows_stem_hierarchy(records):
    """H175: B dialect gallows+stem para-start hierarchy."""
    print("=" * 70)
    print("H175: B Dialect Gallows+Stem Para-Start Hierarchy")
    print("=" * 70)

    b_records = [r for r in records if r['dialect'] == 'B']

    # All morphological classes
    all_classes = [
        # Para-level candidates
        'bare_p', 'bare_f', 'bare_t', 'bare_k',
        'p+ch', 'f+ch', 't+ch', 'k+ch',
        'p+sh', 'f+sh', 't+sh', 'k+sh',
        'p+k', 'p+t', 'f+k', 'f+t',
        # Line-opener candidates
        'y+k', 'y+t', 'y+ch', 'y+sh',
        'd+ch', 'd+sh',
        # Mid-line candidates
        'qo+k', 'qo+t', 'qo+other',
        'bare_ch', 'bare_sh',
    ]

    class_stats = {}
    for mc in all_classes:
        mc_recs = [r for r in b_records if r['morph_class'] == mc]
        n = len(mc_recs)
        if n == 0:
            continue
        ps = sum(1 for r in mc_recs if r['is_para_start'])
        lf = sum(1 for r in mc_recs if r['is_line_first'])
        ll = sum(1 for r in mc_recs if r['is_line_last'])
        class_stats[mc] = {'n': n, 'ps': ps, 'lf': lf, 'll': ll,
                           'ps_rate': ps/n, 'lf_rate': lf/n, 'll_rate': ll/n}

    print(f"\n--- B Dialect All Gallows×Stem Positional Profiles ---")
    print(f"{'Class':<14} {'PS%':<10} {'LFirst%':<12} {'LLast%':<10} {'n':<8} {'Tier?'}")

    def tier(mc, stats):
        ps = stats['ps_rate']
        lf = stats['lf_rate']
        if ps >= 0.10:
            return 'PARA-LEVEL'
        elif ps >= 0.02:
            return 'weak-para'
        elif lf >= 0.30:
            return 'LINE-OPENER'
        elif lf >= 0.15:
            return 'line-moderate'
        else:
            return 'MID-LINE'

    sorted_classes = sorted(class_stats.keys(), key=lambda x: -class_stats[x]['ps_rate'])
    for mc in sorted_classes:
        stats = class_stats[mc]
        t = tier(mc, stats)
        print(f"  {mc:<12} {stats['ps_rate']*100:>6.1f}%    {stats['lf_rate']*100:>6.1f}%      {stats['ll_rate']*100:>6.1f}%    {stats['n']:<8} {t}")

    # Compare directly to A hierarchy
    print(f"\n--- Cross-Dialect Comparison: Same Morphological Class ---")
    a_records = [r for r in records if r['dialect'] == 'A']

    shared_classes = ['p+ch', 'f+ch', 't+ch', 'k+ch', 'y+ch', 'd+ch', 'bare_ch',
                      'y+k', 'y+t', 'qo+k', 'qo+t', 'bare_p', 'bare_t', 'bare_k']

    print(f"{'Class':<14} {'A PS%':<10} {'A LFirst':<12} {'B PS%':<10} {'B LFirst'}")
    for mc in shared_classes:
        a_recs = [r for r in a_records if r['morph_class'] == mc]
        b_recs = [r for r in b_records if r['morph_class'] == mc]
        na = len(a_recs)
        nb = len(b_recs)
        if na == 0 and nb == 0:
            continue
        a_ps = sum(1 for r in a_recs if r['is_para_start']) / na if na > 0 else 0
        a_lf = sum(1 for r in a_recs if r['is_line_first']) / na if na > 0 else 0
        b_ps = sum(1 for r in b_recs if r['is_para_start']) / nb if nb > 0 else 0
        b_lf = sum(1 for r in b_recs if r['is_line_first']) / nb if nb > 0 else 0
        print(f"  {mc:<12} {a_ps*100:>6.1f}%(n={na:<4}) {a_lf*100:>6.1f}%    {b_ps*100:>6.1f}%(n={nb:<4}) {b_lf*100:.1f}%")


def h176_b_k_onset_line_concentration(records):
    """H176: Is B k-onset concentrated at para-start specifically or line-first generally?"""
    print("\n" + "=" * 70)
    print("H176: B k-Onset Line Position Analysis")
    print("=" * 70)

    b_records = [r for r in records if r['dialect'] == 'B']
    a_records = [r for r in records if r['dialect'] == 'A']

    total_b = len(b_records)
    total_a = len(a_records)

    print(f"\n--- B dialect k-onset position distribution ---")
    for onset_prefix in ['bare_k', 'qo+k', 'y+k', 'k+ch']:
        recs = [r for r in b_records if r['morph_class'] == onset_prefix]
        n = len(recs)
        if n == 0:
            continue
        ps = sum(1 for r in recs if r['is_para_start'])
        lf = sum(1 for r in recs if r['is_line_first'])
        ll = sum(1 for r in recs if r['is_line_last'])
        mid = n - lf - ll + sum(1 for r in recs if r['is_line_first'] and r['is_line_last'])
        print(f"  {onset_prefix}: n={n}, PS={ps/n*100:.1f}%, LFirst={lf/n*100:.1f}%, LLast={ll/n*100:.1f}%, Mid={mid/n*100:.1f}%")

    print(f"\n--- A vs B: k-onset (all forms) concentration at para-start vs line-first ---")
    for dialect, drecs in [('A', a_records), ('B', b_records)]:
        k_recs = [r for r in drecs if r['morph_class'] in ('bare_k', 'k+ch', 'k+sh')]
        n = len(k_recs)
        if n == 0:
            continue
        ps = sum(1 for r in k_recs if r['is_para_start'])
        lf = sum(1 for r in k_recs if r['is_line_first'])
        print(f"  {dialect}: bare_k/k+ch/k+sh total={n}, PS={ps/n*100:.1f}%, LFirst={lf/n*100:.1f}%")

    # Para-start: how much of k-onset PS rate is "special" vs general line-first?
    print(f"\n--- B k-onset: Para-start vs within-para line-first ---")
    b_bare_k = [r for r in b_records if r['morph_class'] == 'bare_k']
    n = len(b_bare_k)
    ps = sum(1 for r in b_bare_k if r['is_para_start'])
    lf_total = sum(1 for r in b_bare_k if r['is_line_first'])
    lf_wp = sum(1 for r in b_bare_k if r['is_line_first'] and not r['is_para_start'])
    print(f"  bare_k total: {n}")
    print(f"  At para-start line: {ps} ({ps/n*100:.1f}%)")
    print(f"  At within-para line-first: {lf_wp} ({lf_wp/n*100:.1f}%)")
    print(f"  At any line-first: {lf_total} ({lf_total/n*100:.1f}%)")
    print(f"  At mid/last: {n-lf_total} ({(n-lf_total)/n*100:.1f}%)")


def h177_unified_grammar_model(records):
    """H177: Unified cross-dialect grammar model."""
    print("\n" + "=" * 70)
    print("H177: Unified Cross-Dialect Gallows Grammar Model")
    print("=" * 70)

    print(f"\n--- Positional Tier Summary (by morphological class) ---")
    print(f"{'Tier':<20} {'A classes (PS%)':<45} {'B classes (PS%)'}")
    print(f"\nPARA-LEVEL tier:")

    for dialect, drecs, label in [('A', [r for r in records if r['dialect'] == 'A'], 'A'),
                                   ('B', [r for r in records if r['dialect'] == 'B'], 'B')]:
        # Para-level: PS > 10%
        para_classes = []
        for mc in set(r['morph_class'] for r in drecs):
            mc_recs = [r for r in drecs if r['morph_class'] == mc]
            n = len(mc_recs)
            ps = sum(1 for r in mc_recs if r['is_para_start'])
            if n >= 5 and ps/n >= 0.08:
                para_classes.append((mc, ps/n, n))
        para_classes.sort(key=lambda x: -x[1])
        print(f"  {label}: {[(mc, f'{ps*100:.0f}%', n) for mc, ps, n in para_classes[:8]]}")

    print(f"\nLINE-OPENER tier:")
    for dialect, drecs, label in [('A', [r for r in records if r['dialect'] == 'A'], 'A'),
                                   ('B', [r for r in records if r['dialect'] == 'B'], 'B')]:
        line_classes = []
        for mc in set(r['morph_class'] for r in drecs):
            mc_recs = [r for r in drecs if r['morph_class'] == mc]
            n = len(mc_recs)
            ps = sum(1 for r in mc_recs if r['is_para_start'])
            lf = sum(1 for r in mc_recs if r['is_line_first'])
            if n >= 5 and ps/n < 0.04 and lf/n >= 0.30:
                line_classes.append((mc, lf/n, n))
        line_classes.sort(key=lambda x: -x[1])
        print(f"  {label}: {[(mc, f'LFirst={lf*100:.0f}%', n) for mc, lf, n in line_classes[:8]]}")

    print(f"\nMID-LINE tier:")
    for dialect, drecs, label in [('A', [r for r in records if r['dialect'] == 'A'], 'A'),
                                   ('B', [r for r in records if r['dialect'] == 'B'], 'B')]:
        mid_classes = []
        for mc in set(r['morph_class'] for r in drecs):
            mc_recs = [r for r in drecs if r['morph_class'] == mc]
            n = len(mc_recs)
            ps = sum(1 for r in mc_recs if r['is_para_start'])
            lf = sum(1 for r in mc_recs if r['is_line_first'])
            if n >= 20 and ps/n < 0.02 and lf/n < 0.20:
                mid_classes.append((mc, lf/n, n))
        mid_classes.sort(key=lambda x: x[1])
        print(f"  {label}: {[(mc, f'LFirst={lf*100:.0f}%', n) for mc, lf, n in mid_classes[:8]]}")


def main():
    print("Loading data...")
    records = parse_voynich()
    print(f"Total word tokens: {len(records)}")

    a_count = sum(1 for r in records if r['dialect'] == 'A' and r['is_line_first'])
    b_count = sum(1 for r in records if r['dialect'] == 'B' and r['is_line_first'])
    print(f"A dialect line-first: {a_count}, B dialect: {b_count}")

    print()
    h175_b_gallows_stem_hierarchy(records)
    h176_b_k_onset_line_concentration(records)
    h177_unified_grammar_model(records)


if __name__ == '__main__':
    main()
