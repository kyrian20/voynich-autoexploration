"""
exp_415: A cth at pos1 Characterization (H630)

A has cth at pos1=4.8% (65 lines in 1360 A cont lines) vs B≈0.1%.
This is a major A/B pos1 asymmetry. Characterize:
1. LF distribution for A cont lines where pos1=cth (what LF classes route to cth?)
2. pos2 distribution after cth at pos1 (what follows cth at pos1 in A?)
3. Any LF→cth→pos2 formula types with E_cond>=2.0?
4. Compare A cth pos1 lines to B cth pos1 lines (B is extremely rare at pos1=cth)
"""

import os, re
from collections import Counter, defaultdict

DATA_PATH = os.path.expanduser('~/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt')

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

# Pass 2: collect cont lines by dialect
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
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((ln, words))

cont_lines = {'A': [], 'B': []}
for fb, entries in folio_lines.items():
    dialect = folio_dialect.get(fb, 'A')
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in entries:
        if ln != min_ln and ln != max_ln:
            cont_lines[dialect].append(words)

# Baseline pos1 rates per dialect
for dialect in ['A', 'B']:
    lines = cont_lines[dialect]
    print(f"\n=== {dialect} baseline pos1 distribution ===")
    pos1_counter = Counter()
    for words in lines:
        if len(words) >= 2:
            pos1_counter[get_onset(words[1])] += 1
    total = sum(pos1_counter.values())
    for onset, cnt in sorted(pos1_counter.items(), key=lambda x: -x[1])[:8]:
        print(f"  {onset}: n={cnt} ({cnt/total:.3f})")

# A cth at pos1: LF distribution and pos2 distribution
print("\n=== A cont lines with cth at pos1 ===")
a_cth_pos1_lines = [(words, get_onset(words[0])) for words in cont_lines['A']
                    if len(words) >= 2 and get_onset(words[1]) == 'cth']
print(f"N cth at pos1 in A: {len(a_cth_pos1_lines)}")

# LF distribution for cth-pos1 lines
lf_counter = Counter(lf for _, lf in a_cth_pos1_lines)
# Baseline LF distribution (all A cont lines)
a_lf_baseline = Counter(get_onset(words[0]) for words in cont_lines['A'] if len(words) >= 1)
total_a = sum(a_lf_baseline.values())
total_cth_p1 = len(a_cth_pos1_lines)

print("\n  LF distribution in A cth-pos1 lines (enrichment vs A baseline):")
for lf, cnt in sorted(lf_counter.items(), key=lambda x: -x[1]):
    base_rate = a_lf_baseline[lf] / total_a
    rate_here = cnt / total_cth_p1
    E = rate_here / base_rate if base_rate > 0 else float('inf')
    print(f"    {lf:6s}: n={cnt:3d}  rate={rate_here:.3f}  base={base_rate:.3f}  E={E:.2f}×")

# pos2 distribution after cth at pos1
print("\n  pos2 distribution after cth at pos1 (N_len3+):")
cth_p1_pos2 = Counter()
n_len3 = 0
for words, lf in a_cth_pos1_lines:
    if len(words) >= 3:
        cth_p1_pos2[get_onset(words[2])] += 1
        n_len3 += 1
# Baseline pos2 rate in A (given pos1=cth - use all A cont lines with len>=3)
a_baseline_pos2 = Counter()
a_baseline_cth_pos2 = Counter()  # pos2 given pos1=cth in ALL A cont lines
for words in cont_lines['A']:
    if len(words) >= 3:
        a_baseline_pos2[get_onset(words[2])] += 1
        if get_onset(words[1]) == 'cth':
            a_baseline_cth_pos2[get_onset(words[2])] += 1
total_p2 = sum(a_baseline_pos2.values())
total_cth_p2 = sum(a_baseline_cth_pos2.values())

print(f"  N with pos2 (len>=3): {n_len3}")
for pos2, cnt in sorted(cth_p1_pos2.items(), key=lambda x: -x[1]):
    base_rate = a_baseline_pos2[pos2] / total_p2 if total_p2 > 0 else 0
    rate_here = cnt / n_len3
    E = rate_here / base_rate if base_rate > 0 else float('inf')
    print(f"    {pos2:6s}: n={cnt:3d}  rate={rate_here:.3f}  base={base_rate:.3f}  E={E:.2f}×")

# Formula types: for each LF with N>=3 in cth-pos1 lines, compute pos2 routing
print("\n  E_cond analysis: LF -> cth[pos1] -> pos2 (looking for formula types E>=2.0):")
for lf, n_lf_cth in sorted(lf_counter.items(), key=lambda x: -x[1]):
    if n_lf_cth < 2:
        continue
    # Count pos2 classes given LF=lf AND pos1=cth
    lf_cth_pos2 = Counter()
    for words, wlf in a_cth_pos1_lines:
        if wlf == lf and len(words) >= 3:
            lf_cth_pos2[get_onset(words[2])] += 1
    n_lf_cth_len3 = sum(lf_cth_pos2.values())
    if n_lf_cth_len3 < 2:
        continue
    print(f"\n    LF={lf} → cth[pos1] (N={n_lf_cth_len3}):")
    for pos2, cnt in sorted(lf_cth_pos2.items(), key=lambda x: -x[1]):
        # E_cond = P(pos2|LF,pos1=cth) / P(pos2|pos1=cth)
        p_pos2_given_lf_cth = cnt / n_lf_cth_len3
        p_pos2_given_cth = a_baseline_cth_pos2[pos2] / total_cth_p2 if total_cth_p2 > 0 else 0
        E_cond = p_pos2_given_lf_cth / p_pos2_given_cth if p_pos2_given_cth > 0 else float('inf')
        if cnt >= 2:
            print(f"      pos2={pos2}: n={cnt}  E_cond={E_cond:.2f}×")

# B comparison: cth at pos1 in B
b_cth_pos1 = [words for words in cont_lines['B'] if len(words) >= 2 and get_onset(words[1]) == 'cth']
print(f"\n=== B cont lines with cth at pos1: N={len(b_cth_pos1)} ===")
if b_cth_pos1:
    b_lf = Counter(get_onset(w[0]) for w in b_cth_pos1)
    print(f"  LF distribution: {dict(sorted(b_lf.items(), key=lambda x: -x[1]))}")
else:
    print("  Very rare in B.")

print("\n=== Done ===")
