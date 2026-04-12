"""
exp_198: Positional Grammar Summary + Aiin-Dom Folio Boundary

H194: Cross-sectional positional grammar summary — complete tier × position table.

H131 (computational portion): Is the aiin-dom/y-dom register split folio-based?
     Is there a clear boundary at f16/f17 in suffix paradigms?
"""

import re
import math
from collections import Counter, defaultdict

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'


def folio_base(folio):
    return re.sub(r'\.\d+$', '', folio)


def folio_num(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if m:
        return (int(m.group(1)), m.group(2))
    return (999, 'z')


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


def get_onset(word):
    w = word.lower()
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('ch'): return 'ch'
    if w.startswith('sh'): return 'sh'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    if w.startswith('d'): return 'd'
    if w.startswith('s'): return 's'
    if w.startswith('y'): return 'y'
    if w.startswith('k'): return 'k'
    if w.startswith('t'): return 't'
    if w.startswith('l'): return 'l'
    if w.startswith('r'): return 'r'
    if w.startswith('p'): return 'p'
    if w.startswith('f'): return 'f'
    if w.startswith('o'): return 'o'
    return 'other'


def classify_tier(word):
    """v2 positional tier classifier."""
    if not word:
        return 'OTHER'
    onset = get_onset(word)
    if onset in ('p', 'k', 't', 'f'):
        return 'PARA'
    # LINE_OPEN: y+ch/sh, d+ch/sh, s+h, bare qok, bare qot — length ≥ 3
    w = word.lower()
    if len(word) >= 3 and (w.startswith('ych') or w.startswith('ysh') or
                            w.startswith('dch') or w.startswith('dsh') or
                            w.startswith('sch')):
        return 'LINE_OPEN'
    if onset in ('qok', 'qot'):
        return 'LINE_OPEN'
    # MID: ch, sh, qo — bare or with simple suffix
    if onset in ('ch', 'sh', 'qo'):
        return 'MID'
    return 'OTHER'


def parse_corpus():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0,
                                            'am': 0, 'aiin': 0, 'daiin': 0, 'ol': 0})
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
                if w.endswith('am'):
                    folio_word_stats[fb]['am'] += 1
                if w == 'aiin':
                    folio_word_stats[fb]['aiin'] += 1
                if w == 'daiin':
                    folio_word_stats[fb]['daiin'] += 1
                if w.endswith('ol'):
                    folio_word_stats[fb]['ol'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    paragraphs = []
    current_para = None

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

            if is_para_start:
                current_para = {
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'lines': []
                }
                paragraphs.append(current_para)

            if current_para is not None:
                current_para['lines'].append(words)

    return paragraphs, folio_dialect, folio_word_stats


def h194_positional_grammar_summary(paragraphs):
    """H194: Complete positional grammar table."""
    print("=" * 70)
    print("H194: Complete Positional Grammar Summary")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_paras = [p for p in paragraphs if p['dialect'] == dialect]

        # Position categories: PS (para-start LF), WP-LF (within-para LF),
        # MID, LL (line-last), PF-LL (para-final line's last word)
        PS_first = []       # first word of para-start line
        WP_LF = []          # first word of non-PS lines
        MID_words = []      # mid-line words
        LL_words = []       # last word of any line (non-para-final)
        PF_LL = []          # last word of para-final line
        WP_LL = []          # last word of non-para-final lines

        for p in d_paras:
            lines = p['lines']
            n = len(lines)
            for i, line in enumerate(lines):
                if not line:
                    continue
                # First word
                if i == 0:
                    PS_first.append(line[0])
                else:
                    WP_LF.append(line[0])
                # Mid-line words
                for j in range(1, len(line) - 1):
                    MID_words.append(line[j])
                # Last word
                if len(line) > 1:
                    if i == n - 1:
                        PF_LL.append(line[-1])
                    else:
                        WP_LL.append(line[-1])
                    LL_words.append(line[-1])

        # Compute tier rates by position
        positions = {
            'PS': PS_first,
            'WP-LF': WP_LF,
            'MID': MID_words,
            'WP-LL': WP_LL,
            'PF-LL': PF_LL,
        }

        print(f"\n--- Dialect {dialect}: Tier Distribution by Position ---")
        print(f"{'Position':<10} {'n':>6} {'PARA%':>8} {'LINOP%':>8} {'MID%':>8} {'OTHER%':>8}")
        print('-' * 55)

        for pos_name, words in positions.items():
            n = len(words)
            if n == 0:
                continue
            tier_counts = Counter(classify_tier(w) for w in words)
            para_pct = tier_counts.get('PARA', 0) / n
            linop_pct = tier_counts.get('LINE_OPEN', 0) / n
            mid_pct = tier_counts.get('MID', 0) / n
            other_pct = tier_counts.get('OTHER', 0) / n
            print(f"{pos_name:<10} {n:>6} {para_pct:>8.1%} {linop_pct:>8.1%} {mid_pct:>8.1%} {other_pct:>8.1%}")

        # Onset-level detail at PS
        print(f"\n  Onset distribution at PS (n={len(PS_first)}):")
        ps_onset = Counter(get_onset(w) for w in PS_first)
        total_ps = len(PS_first)
        for onset in sorted(ps_onset, key=lambda x: -ps_onset[x]):
            cnt = ps_onset[onset]
            if cnt >= 2:
                print(f"    {onset}: {cnt} ({cnt/total_ps:.1%})")

        # Key onset enrichment at PS vs WP-LF
        print(f"\n  Key onset enrichments at PS vs WP-LF:")
        wp_onset = Counter(get_onset(w) for w in WP_LF)
        total_wplf = len(WP_LF)
        for onset in ['p', 'k', 't', 'f', 'ch', 'sh', 'y', 'd', 'o', 'ok']:
            ps_rate = ps_onset.get(onset, 0) / total_ps
            wp_rate = wp_onset.get(onset, 0) / total_wplf if total_wplf else 0
            enrich = ps_rate / wp_rate if wp_rate > 0.001 else (float('inf') if ps_onset.get(onset, 0) > 0 else 0)
            print(f"    {onset:<5}: PS={ps_rate:.1%}, WP-LF={wp_rate:.1%}, enrich={enrich:.2f}×")

        # Para-final LL onset enrichment
        print(f"\n  Para-final LL onset enrichment vs within-para LL:")
        pf_onset = Counter(get_onset(w) for w in PF_LL)
        wp_ll_onset = Counter(get_onset(w) for w in WP_LL)
        total_pf = len(PF_LL)
        total_wp_ll = len(WP_LL)
        for onset in ['p', 'f', 'k', 't', 'd', 'ch', 'o', 'ok', 'sh', 'ol', 'qo']:
            pf_rate = pf_onset.get(onset, 0) / total_pf if total_pf else 0
            wp_rate = wp_ll_onset.get(onset, 0) / total_wp_ll if total_wp_ll else 0
            enrich = pf_rate / wp_rate if wp_rate > 0.001 else (float('inf') if pf_onset.get(onset, 0) > 0 else 0)
            print(f"    {onset:<5}: PF-LL={pf_rate:.1%}, WP-LL={wp_rate:.1%}, enrich={enrich:.2f}×")

        # Section-specific grammar strictness
        print(f"\n  PARA% at PS by section (dialect {dialect}):")
        sections = ['herbal', 'pharma', 'cosmo', 'stars', 'astro']
        for sect in sections:
            sect_paras = [p for p in d_paras if p['section'] == sect]
            if len(sect_paras) < 3:
                continue
            ps_words = [p['lines'][0][0] for p in sect_paras if p['lines'] and p['lines'][0]]
            para_pct = sum(1 for w in ps_words if classify_tier(w) == 'PARA') / len(ps_words) if ps_words else 0
            print(f"    {sect}: {para_pct:.1%} PARA at PS (n={len(ps_words)})")


def h131_aiin_dom_boundary(paragraphs, folio_word_stats):
    """H131: Computational test of aiin-dom/y-dom folio boundary."""
    print("\n" + "=" * 70)
    print("H131: Aiin-Dom Folio Boundary Analysis (Herbal A)")
    print("=" * 70)

    # Collect herbal A folios with their word stats
    herbal_a_folios = {}
    for p in paragraphs:
        if p['dialect'] == 'A' and p['section'] == 'herbal':
            fb = p['folio']
            if fb not in herbal_a_folios:
                herbal_a_folios[fb] = Counter()
            for line in p['lines']:
                for w in line:
                    herbal_a_folios[fb][w] += 1

    # For each folio, compute:
    # 1. daiin rate (A aiin-dom indicator)
    # 2. y-dom indicator (rate of y-initial words)
    # 3. ol/or suffix rate (aiin-dom) vs ey/eey suffix rate (y-dom)
    # 4. she-word rate

    print(f"\nHerbal A folios by folio number: rate metrics")
    print(f"{'Folio':<8} {'n':>5} {'daiin%':>8} {'aiin%':>7} {'y_onset%':>9} {'ol_suf%':>9} {'ey_suf%':>9} {'she%':>7}")
    print('-' * 67)

    # Sort folios by folio number
    folio_data = []
    for fb, word_counts in herbal_a_folios.items():
        total = sum(word_counts.values())
        if total < 20:
            continue
        daiin_rate = word_counts.get('daiin', 0) / total
        aiin_rate = word_counts.get('aiin', 0) / total
        y_rate = sum(v for w, v in word_counts.items() if w.startswith('y')) / total
        ol_rate = sum(v for w, v in word_counts.items() if w.endswith('ol') or w.endswith('or')) / total
        ey_rate = sum(v for w, v in word_counts.items() if w.endswith('ey') or w.endswith('eey')) / total
        she_rate = sum(v for w, v in word_counts.items() if w.startswith('she') and len(w) >= 4) / total
        folio_data.append((fb, total, daiin_rate, aiin_rate, y_rate, ol_rate, ey_rate, she_rate))

    folio_data.sort(key=lambda x: folio_num(x[0]))

    for fb, total, daiin_rate, aiin_rate, y_rate, ol_rate, ey_rate, she_rate in folio_data:
        # Flag as aiin-dom if daiin > 3%
        flag = ' ◄' if daiin_rate > 0.03 else ''
        print(f"{fb:<8} {total:>5} {daiin_rate:>8.2%} {aiin_rate:>7.2%} {y_rate:>9.2%} {ol_rate:>9.2%} {ey_rate:>9.2%} {she_rate:>7.2%}{flag}")

    # Compute aggregate stats for f1-f16 vs f17+
    early = [d for d in folio_data if folio_num(d[0])[0] <= 16]
    late = [d for d in folio_data if folio_num(d[0])[0] > 16]

    def avg(data_list, idx):
        return sum(d[idx] for d in data_list) / len(data_list) if data_list else 0

    print(f"\nAggregate comparison: f1-f16 vs f17+")
    print(f"  Folios: f1-f16 n={len(early)}, f17+ n={len(late)}")
    print(f"  {'Metric':<12} {'f1-f16':>10} {'f17+':>10} {'ratio':>8}")
    print('-' * 44)
    metrics = [
        ('daiin%', 2), ('aiin%', 3), ('y_onset%', 4), ('ol_suf%', 5), ('ey_suf%', 6), ('she%', 7)
    ]
    for name, idx in metrics:
        early_avg = avg(early, idx)
        late_avg = avg(late, idx)
        ratio = early_avg / late_avg if late_avg > 0.001 else float('inf')
        print(f"  {name:<12} {early_avg:>10.2%} {late_avg:>10.2%} {ratio:>8.2f}×")


def main():
    print("Loading corpus...")
    paragraphs, folio_dialect, folio_word_stats = parse_corpus()

    total = len(paragraphs)
    a = sum(1 for p in paragraphs if p['dialect'] == 'A')
    b = sum(1 for p in paragraphs if p['dialect'] == 'B')
    print(f"Total paragraphs: {total} (A={a}, B={b})")

    h194_positional_grammar_summary(paragraphs)
    h131_aiin_dom_boundary(paragraphs, folio_word_stats)


if __name__ == '__main__':
    main()
