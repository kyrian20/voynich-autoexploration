"""
exp_405: B p-Formula Complete Structure (H620)

For B continuation lines with p at LF (N~229):
1. Full pos1 distribution (which pos1 classes does p route to?)
2. For top pos1 classes, pos2 distribution
3. Line length distribution for p-LF lines vs all B cont lines
4. MID onset composition (positions 2 to n-3 for lines with n>=5)
5. LL class distribution (already known from F403, but recompute here for consistency)
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

# Pass 1: folio dialect
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

# Pass 2: collect B cont lines
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
        if folio_dialect.get(fb, 'A') != 'B':
            continue
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((ln, words))

p_lines = []
all_cont = []
for fb, line_list in folio_lines.items():
    lns = [l[0] for l in line_list]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in line_list:
        if ln == min_ln or ln == max_ln:
            continue
        all_cont.append(words)
        if get_onset(words[0]) == 'p':
            p_lines.append(words)

total = len(all_cont)
n_p = len(p_lines)
print(f"B cont lines total: {total}")
print(f"B cont lines with p at LF: {n_p} ({100*n_p/total:.1f}%)")

# 1. pos1 distribution for p-LF lines
p1_baseline = Counter(get_onset(w[1]) for w in all_cont if len(w) >= 2)
p1_p = Counter(get_onset(w[1]) for w in p_lines if len(w) >= 2)
p1_p_total = sum(p1_p.values())

print(f"\n--- B p-LF pos1 distribution vs baseline ---")
print(f"{'pos1':<8} {'N_p':>5}  {'%_p':>6}  {'N_base%':>8}  {'E':>6}")
for cls, n in p1_p.most_common():
    pct_p = 100 * n / p1_p_total if p1_p_total > 0 else 0
    pct_base = 100 * p1_baseline[cls] / total
    e = (n / p1_p_total) / (p1_baseline[cls] / total) if p1_baseline[cls] > 0 else float('nan')
    if n >= 2 or pct_base > 1.0:
        print(f"  {cls:<8} {n:>5}  {pct_p:>5.1f}%  {pct_base:>7.1f}%  {e:>6.2f}×")

# 2. pos2 for each pos1 class (top 3 pos1 classes)
print(f"\n--- B p-LF: pos2 distribution for top pos1 classes ---")
p2_baseline = Counter(get_onset(w[2]) for w in all_cont if len(w) >= 3)
p2_base_total = sum(p2_baseline.values())

for target_p1 in ['sh', 'qok', 'other', 'ch']:
    p2_p = Counter(get_onset(w[2]) for w in p_lines if len(w) >= 3 and get_onset(w[1]) == target_p1)
    n_sub = sum(p2_p.values())
    if n_sub < 3:
        continue
    print(f"\n  p→{target_p1}→pos2  (N={n_sub})")
    for cls, n in p2_p.most_common(6):
        pct = 100 * n / n_sub
        base_rate = p2_baseline[cls] / p2_base_total if p2_base_total > 0 else 0
        e = (n / n_sub) / base_rate if base_rate > 0 else float('nan')
        print(f"    pos2={cls:<8} {n:>3}/{n_sub}  ({pct:.0f}%)  baseline={100*base_rate:.0f}%  E={e:.2f}×")

# 3. Line length distribution
print(f"\n--- Line length distribution ---")
len_p = Counter(len(w) for w in p_lines)
len_all = Counter(len(w) for w in all_cont)
print(f"  p-LF lines: mean={sum(k*v for k,v in len_p.items())/sum(len_p.values()):.1f} words")
print(f"  All B cont: mean={sum(k*v for k,v in len_all.items())/sum(len_all.values()):.1f} words")
print(f"  p-LF length distribution:")
for n in range(1, 16):
    count_p = len_p.get(n, 0)
    count_all = len_all.get(n, 0)
    pct_p = 100 * count_p / sum(len_p.values())
    pct_all = 100 * count_all / sum(len_all.values())
    if pct_p > 0.5 or pct_all > 0.5:
        e = pct_p / pct_all if pct_all > 0 else float('nan')
        print(f"    n={n:>2}  p:{count_p:>3}({pct_p:.0f}%)  all:{count_all:>4}({pct_all:.0f}%)  E={e:.2f}×")

# 4. MID onset composition (positions 2 to n-3 for lines n>=5)
print(f"\n--- MID onset composition (positions 2 to n-3, lines n>=5) ---")
mid_p = Counter()
mid_all = Counter()
for words in p_lines:
    if len(words) >= 5:
        for w in words[2:-2]:
            mid_p[get_onset(w)] += 1
for words in all_cont:
    if len(words) >= 5:
        for w in words[2:-2]:
            mid_all[get_onset(w)] += 1
mid_p_total = sum(mid_p.values())
mid_all_total = sum(mid_all.values())
print(f"  p-LF MID tokens: {mid_p_total}  all B MID tokens: {mid_all_total}")
print(f"{'Class':<8} {'p_MID%':>8}  {'all_MID%':>9}  {'E':>6}")
for cls, n in mid_p.most_common(12):
    pct_p = 100 * n / mid_p_total if mid_p_total > 0 else 0
    pct_all = 100 * mid_all[cls] / mid_all_total if mid_all_total > 0 else 0
    e = pct_p / pct_all if pct_all > 0 else float('nan')
    print(f"  {cls:<8} {pct_p:>7.1f}%  {pct_all:>8.1f}%  {e:>6.2f}×")

# 5. LL distribution for p-LF lines
print(f"\n--- B p-LF LL distribution vs baseline ---")
ll_baseline = Counter(get_onset(w[-1]) for w in all_cont if len(w) >= 2)
ll_p = Counter(get_onset(w[-1]) for w in p_lines if len(w) >= 2)
ll_p_total = sum(ll_p.values())
print(f"{'LL class':<8} {'N_p':>5}  {'%_p':>6}  {'baseline%':>10}  {'E':>6}")
for cls, n in ll_p.most_common(12):
    pct_p = 100 * n / ll_p_total
    pct_base = 100 * ll_baseline[cls] / total
    e = (n / ll_p_total) / (ll_baseline[cls] / total)
    if n >= 2:
        print(f"  {cls:<8} {n:>5}  {pct_p:>5.1f}%  {pct_base:>9.1f}%  {e:>6.2f}×")
