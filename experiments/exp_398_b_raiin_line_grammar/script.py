"""
exp_398: B raiin Line Continuation Grammar (H612)

F394: raiin=40%(N=6/15) dominates B pos1 r. Actual lines showed ch/qok continuation.
Q: Full line structure after raiin at pos1.
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

# Collect B continuation lines with raiin at pos1
raiin_lines = []
all_b_pos2_baseline = Counter()
all_b_ll_baseline = Counter()
all_b_cont_n = 0

for fb, lines_list in folio_lines.items():
    if not lines_list or lines_list[0][2] != 'B':
        continue
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln, max_ln = min(line_nums), max(line_nums)
    for ln, words, _ in lines_list:
        if ln == min_ln or ln == max_ln:
            continue
        n = len(words)
        if n < 2:
            continue
        all_b_cont_n += 1
        if n >= 3:
            all_b_pos2_baseline[get_onset(words[2])] += 1
        all_b_ll_baseline[get_onset(words[-1])] += 1

        if n >= 2 and words[1] == 'raiin':
            raiin_lines.append((fb, ln, words))

# Print raiin line analysis
print(f"B continuation lines with raiin at pos1: {len(raiin_lines)}")
print(f"B total continuation lines: {all_b_cont_n}")

# LF distribution
lf_dist = Counter(get_onset(words[0]) for _, _, words in raiin_lines)
print(f"\nLF onset distribution for raiin-pos1 lines:")
for o, n in lf_dist.most_common():
    print(f"  {o}: {n} ({100*n/len(raiin_lines):.1f}%)")

# pos2 distribution (when n>=3)
pos2_dist = Counter()
ll_dist = Counter()
for _, _, words in raiin_lines:
    n = len(words)
    if n >= 3:
        pos2_dist[get_onset(words[2])] += 1
    ll_dist[get_onset(words[-1])] += 1

total_pos2_raiin = sum(pos2_dist.values())
total_ll_raiin = len(raiin_lines)
total_b_pos2 = sum(all_b_pos2_baseline.values())
total_b_ll = sum(all_b_ll_baseline.values())

print(f"\npos2 distribution (N={total_pos2_raiin} raiin-pos1 lines with ≥3 words):")
print(f"{'pos2':>8} {'N':>4} {'%':>6} {'E':>6}")
for p2, n in pos2_dist.most_common():
    pct = 100 * n / total_pos2_raiin if total_pos2_raiin else 0
    p_base = all_b_pos2_baseline.get(p2, 0) / total_b_pos2 if total_b_pos2 else 0
    e = (n / total_pos2_raiin) / p_base if p_base > 0 else float('nan')
    print(f"{p2:>8} {n:>4} {pct:>5.1f}% {e:>5.2f}×")

print(f"\nLL onset distribution (N={total_ll_raiin} raiin-pos1 lines):")
print(f"{'LL':>8} {'N':>4} {'%':>6} {'E':>6}")
for p, n in ll_dist.most_common():
    pct = 100 * n / total_ll_raiin if total_ll_raiin else 0
    p_base = all_b_ll_baseline.get(p, 0) / total_b_ll if total_b_ll else 0
    e = (n / total_ll_raiin) / p_base if p_base > 0 else float('nan')
    print(f"{p:>8} {n:>4} {pct:>5.1f}% {e:>5.2f}×")

# Print actual lines
print(f"\nActual raiin-pos1 lines:")
for fb, ln, words in raiin_lines:
    onsets = ' '.join(get_onset(w) for w in words)
    print(f"  {fb}/{ln}: {' '.join(words)}")
    print(f"         {onsets}")
