"""
exp_422: B y→o→ch grammar — y-LF lines with o at pos1 (H643)

F421: y→o→ch=2.45×(N=6) alongside y→sh→ch=2.53×(N=8).
Both y-LF formula paths route to ch at pos2, but via different pos1 classes.
Characterize:
1. y→o lines: pos2 routing, section distribution
2. Compare y→sh→ch vs y→o→ch: different sections? Different words?
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

def folio_section(fb):
    num = re.sub(r'[^0-9]', '', fb)
    if not num:
        return 'unknown'
    n = int(num)
    if n <= 72:
        return 'herbal'
    elif n <= 84:
        return 'astro'
    elif n <= 102:
        return 'bio'
    elif n <= 116:
        return 'pharma'
    else:
        return 'text'

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
        folio_lines[fb].append((ln, words, folio))

cont_lines_b = []
for fb, entries in folio_lines.items():
    if folio_dialect.get(fb, 'A') != 'B':
        continue
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words, folio in entries:
        if ln != min_ln and ln != max_ln:
            cont_lines_b.append((words, fb, ln))

# B y-LF lines
b_y_lf = [(words, fb, ln) for words, fb, ln in cont_lines_b
          if len(words) >= 2 and get_onset(words[0]) == 'y']
print(f"B y-LF cont lines: {len(b_y_lf)}")

# Baseline pos2 given pos1=o in B
b_p2_given_o = Counter(get_onset(words[2]) for words, _, _ in cont_lines_b
                        if len(words) >= 3 and get_onset(words[1]) == 'o')
total_b_p2_o = sum(b_p2_given_o.values())
# Baseline pos2 given pos1=sh in B
b_p2_given_sh = Counter(get_onset(words[2]) for words, _, _ in cont_lines_b
                         if len(words) >= 3 and get_onset(words[1]) == 'sh')
total_b_p2_sh = sum(b_p2_given_sh.values())

# y→o lines
b_y_o = [(words, fb, ln) for words, fb, ln in b_y_lf
         if len(words) >= 3 and get_onset(words[1]) == 'o']
print(f"\nB y→o cont lines (N={len(b_y_o)}):")
pos2_y_o = Counter(get_onset(words[2]) for words, fb, ln in b_y_o)
total_y_o_p2 = sum(pos2_y_o.values())
for onset, cnt in sorted(pos2_y_o.items(), key=lambda x: -x[1]):
    base = b_p2_given_o[onset] / total_b_p2_o if total_b_p2_o > 0 else 0
    rate = cnt / total_y_o_p2 if total_y_o_p2 > 0 else 0
    E = rate / base if base > 0 else float('inf')
    print(f"  {onset:6s}: n={cnt:3d}  rate={rate:.3f}  base(pos1=o)={base:.3f}  E={E:.2f}×")

print(f"\ny→o→ch lines (those routing to ch):")
for words, fb, ln in b_y_o:
    if len(words) >= 3 and get_onset(words[2]) == 'ch':
        onsets = [get_onset(w) for w in words]
        print(f"  {fb}/{ln}: {words} → {onsets}")

# y→sh lines
b_y_sh = [(words, fb, ln) for words, fb, ln in b_y_lf
          if len(words) >= 3 and get_onset(words[1]) == 'sh']
print(f"\nB y→sh cont lines (N={len(b_y_sh)}):")
pos2_y_sh = Counter(get_onset(words[2]) for words, fb, ln in b_y_sh)
total_y_sh_p2 = sum(pos2_y_sh.values())
for onset, cnt in sorted(pos2_y_sh.items(), key=lambda x: -x[1]):
    base = b_p2_given_sh[onset] / total_b_p2_sh if total_b_p2_sh > 0 else 0
    rate = cnt / total_y_sh_p2 if total_y_sh_p2 > 0 else 0
    E = rate / base if base > 0 else float('inf')
    if cnt >= 2:
        print(f"  {onset:6s}: n={cnt:3d}  rate={rate:.3f}  base(pos1=sh)={base:.3f}  E={E:.2f}×")

# Section distribution: y→o→ch vs y→sh→ch
y_o_ch = [(words, fb, ln) for words, fb, ln in b_y_o if len(words) >= 3 and get_onset(words[2]) == 'ch']
y_sh_ch = [(words, fb, ln) for words, fb, ln in b_y_sh if len(words) >= 3 and get_onset(words[2]) == 'ch']

print(f"\nSection distribution — y→o→ch (N={len(y_o_ch)}) vs y→sh→ch (N={len(y_sh_ch)}):")
for label, lines in [('y→o→ch', y_o_ch), ('y→sh→ch', y_sh_ch)]:
    sec_dist = Counter(folio_section(fb) for _, fb, _ in lines)
    print(f"  {label}: {dict(sorted(sec_dist.items()))}")

# Print all y→sh→ch lines
print(f"\nAll y→sh→ch lines:")
for words, fb, ln in y_sh_ch:
    onsets = [get_onset(w) for w in words]
    print(f"  {fb}/{ln}: {words[:6]} → {onsets[:6]}")

# Compare words at each position
print(f"\ny→o pos1 word tokens:")
print(f"  {Counter(words[1] for words, _, _ in b_y_o).most_common(10)}")
print(f"y→sh pos1 word tokens:")
print(f"  {Counter(words[1] for words, _, _ in b_y_sh).most_common(10)}")

print("\n=== Done ===")
