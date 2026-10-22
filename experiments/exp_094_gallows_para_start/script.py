"""
exp_094: Gallows Character Positional System (H167, H168)

H167: k-onset A para-start words — identify specific forms; B k-onset para-start (9.91×!) words
H168: f-onset also para-start enriched? p/k/t/f = complete gallows class = PARA-LEVEL markers

The gallows characters in EVA are: k (regular gallows), t (regular gallows),
p (platform gallows), f (platform gallows). ALL four should show para-start enrichment
if the gallows-class = para-level marker hypothesis is correct.

Also test: qo+gallows words (qok, qot) — are they para-start SUPPRESSED?
And: y+gallows compounds (ykaiin, yteedy) — do they show 0% PS rate like y+ch?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')


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


def get_onset_class(word):
    """Extended onset with gallows detection."""
    # Gallows characters: p, f, k, t (and their qo-prefixed versions)
    for prefix in ['qo', 'ch', 'sh']:
        if word.startswith(prefix):
            return prefix
    if word.startswith('f'):
        return 'f'
    if word.startswith('p'):
        return 'p'
    if word.startswith('k'):
        return 'k'
    if word.startswith('t'):
        return 't'
    if word[0] in 'dsyo':
        return word[0]
    return 'other'


def is_y_compound(word):
    if not word.startswith('y') or len(word) < 4:
        return False
    rest = word[1:]
    return rest[0] in ('c', 's', 'k', 't')


def is_y_gallows(word):
    """y+gallows compound: y+k or y+t initial."""
    if not word.startswith('y') or len(word) < 4:
        return False
    rest = word[1:]
    return rest[0] in ('k', 't', 'p', 'f')


def is_qo_gallows(word):
    """qo+gallows: qok, qot, qop, qof initial."""
    if not word.startswith('qo') or len(word) < 4:
        return False
    rest = word[2:]
    return rest[0] in ('k', 't', 'p', 'f')


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

            # Track ALL word positions for position analysis
            for pos, w in enumerate(words):
                records.append({
                    'folio': fb,
                    'dialect': dialect,
                    'section': section,
                    'is_para_start': is_para_start and pos == 0,
                    'is_line_first': pos == 0,
                    'is_line_last': pos == len(words) - 1,
                    'word': w,
                    'onset': get_onset_class(w),
                    'line_words': len(words),
                })

    return records


def h167_k_onset_para_start(records):
    """H167: k-onset para-start vocabulary in A and B."""
    print("=" * 70)
    print("H167: k-Onset Para-Start Words (A and B)")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_records = [r for r in records if r['dialect'] == dialect]
        d_ps = [r for r in d_records if r['is_para_start']]
        d_wp = [r for r in d_records if r['is_line_first'] and not r['is_para_start']]
        total_ps = len(d_ps)
        total_wp = len(d_wp)

        # k-onset words
        k_ps_words = Counter(r['word'] for r in d_ps if r['onset'] == 'k')
        k_wp_words = Counter(r['word'] for r in d_wp if r['onset'] == 'k')

        print(f"\n{'='*50}")
        print(f"Dialect {dialect} — k-onset PS words (total PS={total_ps}, WP={total_wp})")

        all_k = set(list(k_ps_words.keys()) + list(k_wp_words.keys()))
        scored = []
        for w in all_k:
            ps = k_ps_words.get(w, 0)
            wp = k_wp_words.get(w, 0)
            total_w = ps + wp
            ps_rate = ps / total_ps if total_ps else 0
            wp_rate = wp / total_wp if total_wp else 0
            enr = ps_rate / wp_rate if wp_rate > 0 else float('inf')
            ps_frac = ps / total_w if total_w > 0 else 0
            scored.append((w, ps, wp, total_w, ps_frac, enr))

        scored.sort(key=lambda x: -x[5])
        print(f"  {'Word':<16} {'PS_n':<8} {'WP_n':<8} {'Total':<8} {'PSFirst%':<12} {'Enrichment'}")
        for w, ps, wp, total_w, ps_frac, enr in scored[:20]:
            enr_str = f"{enr:.2f}×" if enr != float('inf') else "inf×"
            print(f"  {w:<16} {ps:<8} {wp:<8} {total_w:<8} {ps_frac*100:>6.1f}%      {enr_str}")


def h168_full_gallows_system(records):
    """H168: f-onset and full gallows class para-start profile."""
    print("\n" + "=" * 70)
    print("H168: Full Gallows Character Class — Para-Start Profile (p/k/t/f)")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_records = [r for r in records if r['dialect'] == dialect]
        d_ps = [r for r in d_records if r['is_para_start']]
        d_wp = [r for r in d_records if r['is_line_first'] and not r['is_para_start']]
        total_ps = len(d_ps)
        total_wp = len(d_wp)

        print(f"\n{'='*50}")
        print(f"Dialect {dialect} — Gallows/Non-Gallows Para-Start Profile")
        print(f"(total PS={total_ps}, WP={total_wp})")

        onsets = ['p', 'k', 't', 'f', 'ch', 'sh', 'qo', 'y', 'd', 's', 'o', 'other']
        onset_ps = Counter(r['onset'] for r in d_ps)
        onset_wp = Counter(r['onset'] for r in d_wp)

        print(f"  {'Onset':<10} {'PS%':<10} {'WP%':<10} {'Enrichment':<12} {'Gallows?'}")
        for onset in onsets:
            pp = onset_ps.get(onset, 0) / total_ps if total_ps else 0
            wp = onset_wp.get(onset, 0) / total_wp if total_wp else 0
            enr = pp / wp if wp > 0 else float('inf')
            gallows = "GALLOWS" if onset in ('p', 'k', 't', 'f') else ""
            enr_str = f"{enr:.2f}×" if enr != float('inf') else "inf×"
            print(f"  {onset:<10} {pp*100:>6.1f}%    {wp*100:>6.1f}%    {enr_str:<12} {gallows}")

    # f-onset word details
    print(f"\n--- f-Onset Words (all dialects) ---")
    f_words = Counter(r['word'] for r in records if r['onset'] == 'f')
    f_ps = Counter(r['word'] for r in records if r['onset'] == 'f' and r['is_para_start'])
    f_lf = Counter(r['word'] for r in records if r['onset'] == 'f' and r['is_line_first'])

    print(f"Total f-onset word tokens: {sum(f_words.values())}")
    print(f"f-onset para-start tokens: {sum(f_ps.values())}")
    print(f"f-onset line-first tokens: {sum(f_lf.values())}")
    print(f"Top f-onset words: {f_words.most_common(10)}")
    print(f"f-onset PS words: {f_ps.most_common(10)}")


def h169_qo_gallows_suppression(records):
    """H169: qo+gallows words at para-starts — expected SUPPRESSED."""
    print("\n" + "=" * 70)
    print("H169: qo+gallows and y+gallows at Para-Starts")
    print("=" * 70)

    for dialect in ['A', 'B']:
        d_records = [r for r in records if r['dialect'] == dialect]
        d_ps = [r for r in d_records if r['is_para_start']]
        d_wp = [r for r in d_records if r['is_line_first'] and not r['is_para_start']]
        total_ps = len(d_ps)
        total_wp = len(d_wp)

        qo_g_ps = sum(1 for r in d_ps if is_qo_gallows(r['word']))
        qo_g_wp = sum(1 for r in d_wp if is_qo_gallows(r['word']))
        y_g_ps = sum(1 for r in d_ps if is_y_gallows(r['word']))
        y_g_wp = sum(1 for r in d_wp if is_y_gallows(r['word']))

        qo_g_ps_rate = qo_g_ps / total_ps if total_ps else 0
        qo_g_wp_rate = qo_g_wp / total_wp if total_wp else 0
        y_g_ps_rate = y_g_ps / total_ps if total_ps else 0
        y_g_wp_rate = y_g_wp / total_wp if total_wp else 0

        print(f"\nDialect {dialect}:")
        print(f"  qo+gallows at PS: {qo_g_ps}/{total_ps} = {qo_g_ps_rate*100:.1f}%")
        print(f"  qo+gallows at WP: {qo_g_wp}/{total_wp} = {qo_g_wp_rate*100:.1f}%")
        if qo_g_wp_rate > 0:
            print(f"  qo+gallows PS/WP ratio: {qo_g_ps_rate/qo_g_wp_rate:.2f}×")
        print(f"  y+gallows at PS: {y_g_ps}/{total_ps} = {y_g_ps_rate*100:.1f}%")
        print(f"  y+gallows at WP: {y_g_wp}/{total_wp} = {y_g_wp_rate*100:.1f}%")
        if y_g_wp_rate > 0:
            print(f"  y+gallows PS/WP ratio: {y_g_ps_rate/y_g_wp_rate:.2f}×")

    # Check bare gallows vs qo+gallows vs y+gallows positional profiles
    print(f"\n--- Gallows Morphological Forms: Positional Profiles (B dialect) ---")
    b_records = [r for r in records if r['dialect'] == 'B']
    b_ps = [r for r in b_records if r['is_para_start']]
    b_lf = [r for r in b_records if r['is_line_first'] and not r['is_para_start']]
    b_ll = [r for r in b_records if r['is_line_last']]
    b_mid = [r for r in b_records if not r['is_line_first'] and not r['is_line_last']]

    total_ps = len(b_ps)
    total_lf = len(b_lf)
    total_ll = len(b_ll)
    total_mid = len(b_mid)

    categories = {
        'bare_k': lambda w: w[0] == 'k' and not is_qo_gallows(w) and not is_y_gallows(w),
        'bare_t': lambda w: w[0] == 't' and not is_qo_gallows(w) and not is_y_gallows(w),
        'bare_p': lambda w: w[0] == 'p' and not is_qo_gallows(w),
        'qo+k': lambda w: w.startswith('qok') and len(w) >= 4,
        'qo+t': lambda w: w.startswith('qot') and len(w) >= 4,
        'y+k': lambda w: w.startswith('yk') and len(w) >= 4,
        'y+t': lambda w: w.startswith('yt') and len(w) >= 4,
    }

    print(f"  {'Category':<12} {'PS%':<10} {'LF%':<10} {'MID%':<10} {'LL%':<10} {'PS_n':<8}")
    for cat_name, cat_fn in categories.items():
        cat_ps = sum(1 for r in b_ps if cat_fn(r['word']))
        cat_lf = sum(1 for r in b_lf if cat_fn(r['word']))
        cat_mid = sum(1 for r in b_mid if cat_fn(r['word']))
        cat_ll = sum(1 for r in b_ll if cat_fn(r['word']))

        pp = cat_ps / total_ps if total_ps else 0
        lf = cat_lf / total_lf if total_lf else 0
        mid = cat_mid / total_mid if total_mid else 0
        ll = cat_ll / total_ll if total_ll else 0
        print(f"  {cat_name:<12} {pp*100:>6.1f}%    {lf*100:>6.1f}%    {mid*100:>6.1f}%    {ll*100:>6.1f}%    {cat_ps}")


def h170_gallows_positional_hierarchy(records):
    """H170: Complete gallows positional hierarchy across ALL positions."""
    print("\n" + "=" * 70)
    print("H170: Gallows Positional Hierarchy — Morphological Form vs Position")
    print("=" * 70)

    # Token-level analysis: for each word token, what is its line position?
    # Group by word morphological class and compute % at each position
    for dialect in ['A', 'B']:
        d_records = [r for r in records if r['dialect'] == dialect]

        # For each word, compute line position as fraction (0=first, 1=last)
        # Simplified: just compute % at first, last, middle

        word_classes = {
            'bare_k': lambda w: w[0] == 'k' and not w.startswith('qok'),
            'bare_t': lambda w: w[0] == 't' and not w.startswith('qot'),
            'bare_p': lambda w: w[0] == 'p',
            'bare_f': lambda w: w[0] == 'f',
            'qo+k': lambda w: w.startswith('qok') and len(w) >= 4,
            'qo+t': lambda w: w.startswith('qot') and len(w) >= 4,
            'y+k': lambda w: w.startswith('yk') and len(w) >= 4,
            'y+t': lambda w: w.startswith('yt') and len(w) >= 4,
            'bare_ch': lambda w: w.startswith('ch') and len(w) >= 3,
            'bare_sh': lambda w: w.startswith('sh') and len(w) >= 3,
        }

        print(f"\nDialect {dialect} — Line Position Profiles by Gallows Form")
        print(f"  {'Class':<12} {'PS%':<8} {'LFirst%':<10} {'LLast%':<10} {'n_tokens':<10}")

        d_ps_set = {id(r) for r in d_records if r['is_para_start']}
        d_lf_set = {id(r) for r in d_records if r['is_line_first']}
        d_ll_set = {id(r) for r in d_records if r['is_line_last']}

        for class_name, class_fn in word_classes.items():
            class_records = [r for r in d_records if class_fn(r['word'])]
            n = len(class_records)
            if n == 0:
                continue
            ps = sum(1 for r in class_records if r['is_para_start'])
            lf = sum(1 for r in class_records if r['is_line_first'])
            ll = sum(1 for r in class_records if r['is_line_last'])
            print(f"  {class_name:<12} {ps/n*100:>4.1f}%   {lf/n*100:>6.1f}%    {ll/n*100:>6.1f}%    {n}")


def main():
    print("Loading data...")
    records = parse_voynich()
    print(f"Total word tokens: {len(records)}")

    a_count = sum(1 for r in records if r['dialect'] == 'A' and r['is_line_first'])
    b_count = sum(1 for r in records if r['dialect'] == 'B' and r['is_line_first'])
    print(f"A dialect line-first tokens: {a_count}, B dialect: {b_count}")

    print()
    h167_k_onset_para_start(records)
    h168_full_gallows_system(records)
    h169_qo_gallows_suppression(records)
    h170_gallows_positional_hierarchy(records)


if __name__ == '__main__':
    main()
