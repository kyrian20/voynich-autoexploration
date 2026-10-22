"""
exp_403: B pos3 Grammar — After (LF, pos1, pos2), What Happens at pos3? (H628)

For B continuation lines with >=4 words:
1. Compute pos2→pos3 bigram E values (unconditional on LF)
2. Compute (LF, pos1, pos2, pos3) 4-grams for formula-typed trigrams
3. Check whether formula-typed lines (y→sh→ch, p→sh→qot, qok→sh→k, etc.)
   have distinctive pos3 routing vs baseline pos3 given pos2

Key question: does LF-conditional structure at pos2 extend to pos3?
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

# Pass 2: collect B continuation lines >=4 words
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

b_cont_4 = []  # lines >=4 words
for fb, line_list in folio_lines.items():
    lns = [l[0] for l in line_list]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in line_list:
        if ln == min_ln or ln == max_ln:
            continue
        if len(words) >= 4:
            b_cont_4.append(words)

total4 = len(b_cont_4)
print(f"B continuation lines (>=4 words): {total4}")

# Compute pos2→pos3 bigram E values (unconditional on LF)
p2_counts = Counter()
p3_counts = Counter()
p2_p3_counts = Counter()
for words in b_cont_4:
    p2 = get_onset(words[2])
    p3 = get_onset(words[3])
    p2_counts[p2] += 1
    p3_counts[p3] += 1
    p2_p3_counts[(p2, p3)] += 1

print(f"\n--- pos2→pos3 bigram enrichments (unconditional on LF, top by E) ---")
print(f"{'Bigram':<20} {'N':>5}  {'E':>7}")
p2_p3_e = {}
for (p2, p3), n in p2_p3_counts.items():
    if n < 3:
        continue
    e = (n / total4) / ((p2_counts[p2] / total4) * (p3_counts[p3] / total4))
    p2_p3_e[(p2, p3)] = (n, e)
for (p2, p3), (n, e) in sorted(p2_p3_e.items(), key=lambda x: -x[1][1])[:20]:
    print(f"  {p2:>6}→{p3:<12} {n:>5}  {e:>7.2f}×")

# Compute LF-conditional pos3: for each formula trigram, compute pos3 distribution
# Known B formula trigrams from exp_401 (E_cond >= 2.0, N >= 5):
FORMULA_TRIGRAMS = [
    ('y', 'sh', 'ch'),   # 2.88×, N=8
    ('p', 'sh', 'qot'),  # 2.04×, N=8
    ('qok', 'ch', 'qo'), # 2.62×, N=8
    ('qok', 'sh', 'k'),  # 4.16×, N=5
    ('l', 'ch', 'qok'),  # 2.96×, N=5
    ('qok', 'ch', 'ol'), # 2.31×, N=5
    ('qok', 'l', 'qok'), # 2.09×, N=5
    ('s', 'sh', 'l'),    # 2.06×, N=6
    ('p', 'sh', 'qot'),  # already included
    ('d', 'ot', 'ot'),   # 4.13×, N=5
]

print(f"\n--- Formula-typed trigram pos3 routing ---")
print(f"For each formula trigram (LF, pos1, pos2), compute pos3 distribution")
print(f"Baseline: unconditional pos3 given pos2 only")
print()

# For formula trigram lines, collect (pos2, pos3) and compare to baseline
for (lf, p1, p2) in FORMULA_TRIGRAMS:
    formula_pos3 = Counter()
    formula_n = 0
    for words in b_cont_4:
        if (get_onset(words[0]) == lf and get_onset(words[1]) == p1 and get_onset(words[2]) == p2):
            formula_pos3[get_onset(words[3])] += 1
            formula_n += 1

    if formula_n == 0:
        continue

    # Baseline: given pos2=p2, what is pos3?
    p2_baseline = p2_p3_counts  # unconditional pos2→pos3
    p2_total = p2_counts[p2]

    print(f"  {lf}→{p1}→{p2}: N={formula_n} lines with pos3 data")
    for cls, n3 in formula_pos3.most_common(5):
        if p2_total > 0:
            baseline_rate = p2_p3_counts.get((p2, cls), 0) / p2_total
        else:
            baseline_rate = 0.0
        formula_rate = n3 / formula_n
        e_p3 = formula_rate / baseline_rate if baseline_rate > 0 else float('nan')
        print(f"    pos3={cls}: {n3}/{formula_n} ({100*formula_rate:.0f}%)  baseline={100*baseline_rate:.0f}%  E={e_p3:.2f}×")
    print()

# Also: compute overall pos3 distribution for ALL B cont lines >= 4 words
print(f"\n--- Overall B pos3 class distribution (N={total4} lines) ---")
p3_all = Counter(get_onset(words[3]) for words in b_cont_4)
for cls, n in p3_all.most_common(12):
    print(f"  {cls:<8} {n:>5}  ({100*n/total4:.1f}%)")

# Compare pos3 to pos2 and pos1 distributions
print(f"\n--- Pos1/Pos2/Pos3 distribution comparison (B cont lines) ---")
p1_all = Counter(get_onset(words[1]) for words in b_cont_4)
p2_all = Counter(get_onset(words[2]) for words in b_cont_4)
print(f"{'Class':<8} {'pos1%':>7}  {'pos2%':>7}  {'pos3%':>7}")
all_classes = sorted(set(p1_all.keys()) | set(p2_all.keys()) | set(p3_all.keys()))
for cls in all_classes:
    r1 = 100 * p1_all.get(cls, 0) / total4
    r2 = 100 * p2_all.get(cls, 0) / total4
    r3 = 100 * p3_all.get(cls, 0) / total4
    if r1 > 0.5 or r2 > 0.5 or r3 > 0.5:
        print(f"  {cls:<8} {r1:>7.1f}%  {r2:>7.1f}%  {r3:>7.1f}%")
