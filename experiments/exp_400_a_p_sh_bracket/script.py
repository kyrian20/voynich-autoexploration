"""
exp_400: A p-Formula Lines sh-Bracket Structure (H622)

F403: A p→sh at pos1=3.60×/N=41 AND A p→sh at LL=3.60×/N=7 — identical E values.
Q: Do A p-LF lines have sh at BOTH pos1 and LL forming a "sh-bracket"?
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

DATA_PATH = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt'))

ONSET_ORDER = [
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o')
]

def get_onset(word):
    for label, prefix in ONSET_ORDER:
        if word.startswith(prefix):
            return label
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0})
with open(DATA_PATH, 'r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m:
            continue
        folio = m.group(1).lstrip('+*=&~')
        fb = folio_base(folio)
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            folio_word_stats[fb]['total'] += 1
            if w.endswith('edy') or w.endswith('eedy'):
                folio_word_stats[fb]['edy'] += 1

folio_dialect = {}
for fb, stats in folio_word_stats.items():
    t = stats['total']
    folio_dialect[fb] = 'B' if t > 0 and stats['edy'] / t >= 0.05 else 'A'

folio_lines = defaultdict(list)
with open(DATA_PATH, 'r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m:
            continue
        folio = m.group(1).lstrip('+*=&~')
        line_num = int(m.group(2))
        locus_code = m.group(3)
        fb = folio_base(folio)
        dialect = folio_dialect.get(fb, 'A')
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((line_num, words, dialect))

# Analyze A (and B for comparison) p-LF lines
for d_target in ['A', 'B']:
    p_lines = []
    all_ll = Counter()
    all_pos1 = Counter()
    total_lines = 0

    for fb, lines_list in folio_lines.items():
        if not lines_list or lines_list[0][2] != d_target:
            continue
        line_nums = [ln for ln, _, _ in lines_list]
        min_ln, max_ln = min(line_nums), max(line_nums)
        for ln, words, _ in lines_list:
            if ln == min_ln or ln == max_ln:
                continue
            n = len(words)
            total_lines += 1
            lf = get_onset(words[0])
            if n >= 2:
                all_pos1[get_onset(words[1])] += 1
            all_ll[get_onset(words[-1])] += 1
            if lf == 'p':
                p_lines.append((fb, ln, words))

    n_p = len(p_lines)
    print(f"\n{'='*60}")
    print(f"DIALECT {d_target}: {n_p} p-LF continuation lines (of {total_lines})")
    print(f"{'='*60}")

    # pos1 and LL distributions for p-LF lines
    p_pos1 = Counter()
    p_ll = Counter()
    for _, _, words in p_lines:
        n = len(words)
        if n >= 2:
            p_pos1[get_onset(words[1])] += 1
        p_ll[get_onset(words[-1])] += 1

    p_pos1_total = sum(p_pos1.values())
    p_ll_total = len(p_lines)

    print(f"\np→pos1 distribution:")
    for pos1, cnt in p_pos1.most_common(6):
        e = (cnt/p_pos1_total) / (all_pos1.get(pos1,0)/total_lines) if all_pos1.get(pos1,0) else float('nan')
        print(f"  {pos1}: {cnt}/{p_pos1_total} ({100*cnt/p_pos1_total:.0f}%) E={e:.2f}×")

    print(f"\np→LL distribution:")
    for ll, cnt in p_ll.most_common(8):
        e = (cnt/p_ll_total) / (all_ll.get(ll,0)/total_lines) if all_ll.get(ll,0) else float('nan')
        print(f"  {ll}: {cnt}/{p_ll_total} ({100*cnt/p_ll_total:.0f}%) E={e:.2f}×")

    # Bracket analysis
    sh_pos1_count = p_pos1.get('sh', 0)
    sh_ll_count = p_ll.get('sh', 0)
    bracket_count = sum(1 for _, _, words in p_lines
                        if len(words) >= 3
                        and get_onset(words[1]) == 'sh'
                        and get_onset(words[-1]) == 'sh')
    n_p_3plus = sum(1 for _, _, words in p_lines if len(words) >= 3)

    p_sh_pos1 = sh_pos1_count / p_pos1_total if p_pos1_total else 0
    p_sh_ll = sh_ll_count / p_ll_total if p_ll_total else 0
    expected_bracket = p_sh_pos1 * p_sh_ll * n_p_3plus

    print(f"\nsh-bracket analysis:")
    print(f"  p→sh at pos1: {sh_pos1_count}/{p_pos1_total} ({100*p_sh_pos1:.1f}%)")
    print(f"  p→sh at LL: {sh_ll_count}/{p_ll_total} ({100*p_sh_ll:.1f}%)")
    print(f"  p→sh at BOTH (N≥3 lines): {bracket_count}/{n_p_3plus}")
    print(f"  Expected under independence: {expected_bracket:.2f}")
    if expected_bracket > 0:
        print(f"  Bracket enrichment: {bracket_count/expected_bracket:.2f}×")

    # Print actual A p-LF lines
    print(f"\nActual p-LF lines:")
    for fb, ln, words in p_lines[:20]:
        n = len(words)
        if n < 2:
            continue
        onsets = ' '.join(get_onset(w) for w in words)
        pos1_on = get_onset(words[1])
        ll_on = get_onset(words[-1])
        bracket = '★' if pos1_on == 'sh' and ll_on == 'sh' else ''
        print(f"  {fb}/{ln}: {' '.join(words)}")
        print(f"    onsets: {onsets} {bracket}")
