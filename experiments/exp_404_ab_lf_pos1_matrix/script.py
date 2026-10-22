"""
exp_404: A vs B LF→pos1 Matrix Comparison (H629)

Compute LF × pos1 bigram E matrix for both A and B dialects.
Identify structural sources of A pos1=ch=28.6% vs B=19.0%;
A pos1=qok=4.6% vs B=12.3%.
Which LF classes drive the A/B pos1 divergence?
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
    return re.sub(r'[rv]\d*$', '', folio)

# Pass 1: folio dialect classification
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
        lc = m.group(3).lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
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

# Pass 2: collect continuation lines for both dialects
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
        ln = int(m.group(2))
        lc = m.group(3).lstrip('+*=/~&')
        fb = folio_base(folio)
        d = folio_dialect.get(fb, 'A')
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((ln, words, d))

# Collect LF→pos1 pairs for each dialect
lf_p1 = {'A': defaultdict(Counter), 'B': defaultdict(Counter)}
lf_totals = {'A': Counter(), 'B': Counter()}
p1_totals = {'A': Counter(), 'B': Counter()}
total_lines = {'A': 0, 'B': 0}

for fb, line_list in folio_lines.items():
    if not line_list:
        continue
    lns = [l[0] for l in line_list]
    min_ln, max_ln = min(lns), max(lns)
    d = line_list[0][2]
    for ln, words, _ in line_list:
        if ln == min_ln or ln == max_ln:
            continue
        if len(words) < 2:
            continue
        lf = get_onset(words[0])
        p1 = get_onset(words[1])
        lf_p1[d][lf][p1] += 1
        lf_totals[d][lf] += 1
        p1_totals[d][p1] += 1
        total_lines[d] += 1

print(f"B continuation lines (>=2 words): {total_lines['B']}")
print(f"A continuation lines (>=2 words): {total_lines['A']}")

# Print overall pos1 distributions
for d in ['A', 'B']:
    print(f"\n--- {d} dialect pos1 class distribution ---")
    tot = total_lines[d]
    for cls, n in p1_totals[d].most_common():
        if 100*n/tot > 0.5:
            print(f"  {cls:<8} {n:>5}  ({100*n/tot:.1f}%)")

# KEY TABLE: For each pos1 class, compute E for each LF class in A vs B
# This reveals which LF classes drive the A/B pos1 divergence
KEY_P1 = ['ch', 'sh', 'qok', 'd', 'ok', 'cth', 'ol']

print(f"\n--- LF-conditional pos1 rates: E(pos1=X | LF=Y) for key pos1 classes ---")
print(f"Format: E(A)× / E(B)×; N_A | N_B")
print()

for p1 in KEY_P1:
    p1_rate_a = p1_totals['A'][p1] / total_lines['A']
    p1_rate_b = p1_totals['B'][p1] / total_lines['B']
    print(f"pos1={p1}  [A baseline: {100*p1_rate_a:.1f}%  B baseline: {100*p1_rate_b:.1f}%]")
    print(f"  {'LF':<8} {'E(A)':>7}  {'N_A':>5}  |  {'E(B)':>7}  {'N_B':>5}  {'A-B diff':>10}")

    rows = []
    for lf in ['d', 'y', 's', 'qok', 'p', 't', 'sh', 'ch', 'o', 'ok', 'qot', 'ot', 'k']:
        n_a = lf_p1['A'][lf][p1]
        n_b = lf_p1['B'][lf][p1]
        tot_a = lf_totals['A'][lf]
        tot_b = lf_totals['B'][lf]
        if tot_a == 0 and tot_b == 0:
            continue
        rate_a = n_a / tot_a if tot_a > 0 else 0
        rate_b = n_b / tot_b if tot_b > 0 else 0
        e_a = rate_a / p1_rate_a if p1_rate_a > 0 else float('nan')
        e_b = rate_b / p1_rate_b if p1_rate_b > 0 else float('nan')
        rows.append((lf, e_a, n_a, e_b, n_b))

    # Sort by |E_A - E_B| to highlight biggest differences
    rows.sort(key=lambda x: -abs(x[1]-x[3]))
    for lf, e_a, n_a, e_b, n_b in rows[:8]:
        diff_str = f"A{'>' if e_a > e_b else '<'}B({abs(e_a-e_b):.2f})"
        print(f"  {lf:<8} {e_a:>7.2f}×  {n_a:>5}  |  {e_b:>7.2f}×  {n_b:>5}  {diff_str:>10}")
    print()

# Summary table: for each LF class, what is the dominant pos1 in A vs B?
print(f"\n--- LF-class dominant pos1 for A vs B ---")
print(f"{'LF':<8}  A dominant pos1  |  B dominant pos1")
print("-"*55)
for lf in ['d', 'y', 's', 'qok', 'p', 't', 'sh', 'ch', 'o', 'ok', 'qot', 'ot', 'k']:
    dom_a = lf_p1['A'][lf].most_common(2) if lf_totals['A'][lf] > 0 else []
    dom_b = lf_p1['B'][lf].most_common(2) if lf_totals['B'][lf] > 0 else []
    a_str = ' / '.join([f"{c}({n}/{lf_totals['A'][lf]})" for c,n in dom_a[:2]])
    b_str = ' / '.join([f"{c}({n}/{lf_totals['B'][lf]})" for c,n in dom_b[:2]])
    same = dom_a[0][0] == dom_b[0][0] if dom_a and dom_b else True
    marker = '   ' if same else '***'
    print(f"{lf:<8}  {a_str:<25} |  {b_str:<25} {marker}")
