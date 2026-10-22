"""
exp_397: A y→{pos1}→{pos2} Full Trigram Grammar (H619)

F400: A y→sh→ch=0.62×(depleted) vs B y→sh→ch=2.94× — cross-dialectal inversion.
F393: A y→y→y=2.15× (directional) — y self-chain extends in A.
Q: What is A y's full trigram grammar? Is A y "y-self-chain dominant" while B y is "sh→ch dominant"?

Compare A and B y LF trigram distributions side by side.
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

for d_target in ['A', 'B']:
    print(f"\n{'='*70}")
    print(f"DIALECT {d_target} — y at LF trigram analysis")
    print(f"{'='*70}")

    y_lf_pos1 = Counter()
    y_lf_p1_p2 = defaultdict(Counter)
    baseline_pos1 = Counter()
    baseline_pos2_given_pos1 = defaultdict(Counter)
    total_lf = 0

    for fb, lines_list in folio_lines.items():
        if not lines_list:
            continue
        d = lines_list[0][2]
        if d != d_target:
            continue
        line_nums = [ln for ln, _, _ in lines_list]
        min_ln, max_ln = min(line_nums), max(line_nums)
        for ln, words, _ in lines_list:
            if ln == min_ln or ln == max_ln:
                continue
            n = len(words)
            if n < 2:
                continue
            lf_onset = get_onset(words[0])
            p1_onset = get_onset(words[1])
            total_lf += 1
            baseline_pos1[p1_onset] += 1
            if n >= 3:
                p2_onset = get_onset(words[2])
                baseline_pos2_given_pos1[p1_onset][p2_onset] += 1
            if lf_onset == 'y':
                y_lf_pos1[p1_onset] += 1
                if n >= 3:
                    p2_onset = get_onset(words[2])
                    y_lf_p1_p2[p1_onset][p2_onset] += 1

    y_total = sum(y_lf_pos1.values())
    print(f"\n--- y→pos1 distribution (N={y_total} y-LF lines) ---")
    print(f"{'pos1':>8} {'N':>4} {'%y':>6} {'E':>6}")
    for p1, n in y_lf_pos1.most_common():
        pct_t = 100 * n / y_total if y_total else 0
        p_base = baseline_pos1.get(p1, 0) / total_lf if total_lf else 0
        e = (n / y_total) / p_base if p_base > 0 else float('nan')
        print(f"{p1:>8} {n:>4} {pct_t:>5.1f}% {e:>5.2f}×")

    print(f"\n--- y→pos1→pos2 trigram distributions ---")
    for p1, cnt in y_lf_pos1.most_common(8):
        if cnt < 3:
            continue
        p2_dist = y_lf_p1_p2[p1]
        p2_total = sum(p2_dist.values())
        if p2_total < 3:
            continue
        print(f"\n  y→{p1} (N={cnt}), pos2 distribution (N={p2_total}):")
        base_p2 = baseline_pos2_given_pos1[p1]
        base_p2_total = sum(base_p2.values())
        for p2, n2 in p2_dist.most_common(8):
            p_cond = n2 / p2_total
            p_base_p2 = base_p2.get(p2, 0) / base_p2_total if base_p2_total else 0
            e = p_cond / p_base_p2 if p_base_p2 > 0 else float('nan')
            print(f"    {p2:>8}: N={n2:>3}  E={e:.2f}×")

# Cross-dialect comparison table
print(f"\n\n{'='*70}")
print("CROSS-DIALECT COMPARISON: y at LF pos1 distribution")
print(f"{'='*70}")

y_pos1 = {}
y_totals_d = {}
bl_pos1 = {}
bl_totals_d = {}
for d_target in ['A', 'B']:
    y_pos1[d_target] = Counter()
    bl_pos1[d_target] = Counter()
    total = 0
    for fb, lines_list in folio_lines.items():
        if not lines_list or lines_list[0][2] != d_target:
            continue
        line_nums = [ln for ln, _, _ in lines_list]
        min_ln, max_ln = min(line_nums), max(line_nums)
        for ln, words, _ in lines_list:
            if ln == min_ln or ln == max_ln:
                continue
            n = len(words)
            if n < 2:
                continue
            lf_onset = get_onset(words[0])
            p1_onset = get_onset(words[1])
            total += 1
            bl_pos1[d_target][p1_onset] += 1
            if lf_onset == 'y':
                y_pos1[d_target][p1_onset] += 1
    y_totals_d[d_target] = sum(y_pos1[d_target].values())
    bl_totals_d[d_target] = total

all_pos1 = set(y_pos1['A'].keys()) | set(y_pos1['B'].keys())
print(f"{'pos1':>8} | {'A N':>6} {'A E':>6} | {'B N':>6} {'B E':>6}")
print("-" * 40)
for p1 in sorted(all_pos1, key=lambda x: -(y_pos1['A'].get(x, 0) + y_pos1['B'].get(x, 0))):
    rows = []
    for d in ['A', 'B']:
        n = y_pos1[d].get(p1, 0)
        p_base = bl_pos1[d].get(p1, 0) / bl_totals_d[d] if bl_totals_d[d] else 0
        e = (n / y_totals_d[d]) / p_base if p_base > 0 and y_totals_d[d] else float('nan')
        rows.append((n, e))
    print(f"{p1:>8} | {rows[0][0]:>6} {rows[0][1]:>5.2f}× | {rows[1][0]:>6} {rows[1][1]:>5.2f}×")
