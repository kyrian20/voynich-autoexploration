"""
exp_416: B d→ot chain grammar (H626)

d→ot→ot=3.69×(N=5) is a confirmed N≥5 formula type (F416).
Characterize B d-LF cont lines with ot at pos1:
1. pos2 distribution (confirm ot enrichment)
2. pos3 distribution after d→ot
3. pos3 distribution after d→ot→ot (if any)
4. word tokens for d→ot lines
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

# Pass 2: collect cont lines with folio annotation
folio_lines = defaultdict(list)
line_folio_map = []
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
    dialect = folio_dialect.get(fb, 'A')
    if dialect != 'B':
        continue
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words, folio in entries:
        if ln != min_ln and ln != max_ln:
            cont_lines_b.append((words, folio, ln))

print(f"B cont lines total: {len(cont_lines_b)}")

# Compute B baseline for pos2 given LF=d
b_d_lf_lines = [(words, folio, ln) for words, folio, ln in cont_lines_b
                if len(words) >= 2 and get_onset(words[0]) == 'd']
print(f"B d-LF cont lines: {len(b_d_lf_lines)}")

# pos1 distribution for B d-LF lines (baseline)
pos1_d = Counter(get_onset(words[1]) for words, _, _ in b_d_lf_lines if len(words) >= 2)
total_d_p1 = sum(pos1_d.values())
print(f"\nB d-LF → pos1 distribution (N={total_d_p1}):")
for onset, cnt in sorted(pos1_d.items(), key=lambda x: -x[1])[:10]:
    print(f"  {onset:6s}: n={cnt:4d}  rate={cnt/total_d_p1:.3f}")

# Filter to d→ot lines
b_d_ot_lines = [(words, folio, ln) for words, folio, ln in b_d_lf_lines
                if len(words) >= 2 and get_onset(words[1]) == 'ot']
print(f"\nB d→ot cont lines: {len(b_d_ot_lines)}")

# pos2 distribution for d→ot lines
print(f"\nB d→ot → pos2 distribution:")
pos2_d_ot = Counter(get_onset(words[2]) for words, _, _ in b_d_ot_lines if len(words) >= 3)
total_d_ot_p2 = sum(pos2_d_ot.values())
# Baseline pos2 for B d-LF lines
pos2_d_baseline = Counter(get_onset(words[2]) for words, _, _ in b_d_lf_lines if len(words) >= 3)
total_d_p2 = sum(pos2_d_baseline.values())
for onset, cnt in sorted(pos2_d_ot.items(), key=lambda x: -x[1]):
    base = pos2_d_baseline[onset] / total_d_p2 if total_d_p2 > 0 else 0
    rate = cnt / total_d_ot_p2 if total_d_ot_p2 > 0 else 0
    E = rate / base if base > 0 else float('inf')
    print(f"  {onset:6s}: n={cnt:3d}  rate={rate:.3f}  base={base:.3f}  E={E:.2f}×")

# d→ot→ot lines (ot at pos2)
b_d_ot_ot = [(words, folio, ln) for words, folio, ln in b_d_ot_lines
             if len(words) >= 3 and get_onset(words[2]) == 'ot']
print(f"\nB d→ot→ot lines (N={len(b_d_ot_ot)}):")
for words, folio, ln in b_d_ot_ot:
    onsets = [get_onset(w) for w in words]
    print(f"  {folio}/{ln}: {words} → onsets: {onsets}")

# pos3 distribution after d→ot→ot (if N sufficient)
if b_d_ot_ot:
    pos3_d_ot_ot = Counter(get_onset(words[3]) for words, _, _ in b_d_ot_ot if len(words) >= 4)
    total_d_ot_ot_p3 = sum(pos3_d_ot_ot.values())
    # Baseline pos3 for d-LF lines
    pos3_d_baseline = Counter(get_onset(words[3]) for words, _, _ in b_d_lf_lines if len(words) >= 4)
    total_d_p3 = sum(pos3_d_baseline.values())
    print(f"\nB d→ot→ot → pos3 distribution (N_len4={total_d_ot_ot_p3}):")
    for onset, cnt in sorted(pos3_d_ot_ot.items(), key=lambda x: -x[1]):
        base = pos3_d_baseline[onset] / total_d_p3 if total_d_p3 > 0 else 0
        rate = cnt / total_d_ot_ot_p3 if total_d_ot_ot_p3 > 0 else 0
        E = rate / base if base > 0 else float('inf')
        print(f"  {onset:6s}: n={cnt:3d}  rate={rate:.3f}  base={base:.3f}  E={E:.2f}×")

# Full word tokens for all d→ot lines
print(f"\nAll B d→ot lines (N={len(b_d_ot_lines)}):")
for words, folio, ln in sorted(b_d_ot_lines, key=lambda x: x[1:]):
    onsets = [get_onset(w) for w in words]
    print(f"  {folio}/{ln} (len={len(words)}): {words}")
    print(f"    onsets: {onsets}")

# Compare: B d-LF lines overall pos2 vs d→ot pos2
print("\n=== Summary: ot at pos2 enrichment in d→ot vs d-LF baseline ===")
n_d_ot_p1 = pos1_d.get('ot', 0)
p1_ot_rate = n_d_ot_p1 / total_d_p1 if total_d_p1 > 0 else 0
# Overall B baseline pos1=ot rate
b_all_pos1 = Counter(get_onset(words[1]) for words, _, _ in cont_lines_b if len(words) >= 2)
total_b_all_p1 = sum(b_all_pos1.values())
b_ot_p1_rate = b_all_pos1['ot'] / total_b_all_p1 if total_b_all_p1 > 0 else 0
print(f"B overall pos1=ot rate: {b_ot_p1_rate:.3f}")
print(f"B d-LF pos1=ot rate: {p1_ot_rate:.3f}")
print(f"d-LF pos1=ot enrichment vs overall B: E={p1_ot_rate/b_ot_p1_rate:.2f}×(N={n_d_ot_p1})")

# Check E_cond for d→ot→ot (pos2=ot given pos1=ot in d-LF lines)
n_ot_ot = pos2_d_ot.get('ot', 0)
p_ot_p2_given_d_ot = n_ot_ot / total_d_ot_p2 if total_d_ot_p2 > 0 else 0
# Overall B d-LF pos2=ot rate given pos1=ot
b_d_ot_p2_base = pos2_d_baseline.get('ot', 0) / total_d_p2 if total_d_p2 > 0 else 0
E_cond = p_ot_p2_given_d_ot / b_d_ot_p2_base if b_d_ot_p2_base > 0 else float('inf')
print(f"\nd→ot→ot E_cond: {E_cond:.2f}× (N={n_ot_ot})")

print("\n=== Done ===")
