"""
exp_421: B d→qok→ol and d→ch→y grammar (H642)

F421: d→qok→ol=2.61×(N=6) and d→ch→y=2.23×(N=5).
Characterize:
1. d→qok lines: pos2 distribution (confirm ol enrichment)
2. d→ch lines: pos2 distribution (confirm y enrichment)
3. Word tokens for these sub-types
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
            cont_lines_b.append((words, folio, ln))

# B d-LF lines
b_d_lf = [(words, folio, ln) for words, folio, ln in cont_lines_b
          if len(words) >= 2 and get_onset(words[0]) == 'd']
print(f"B d-LF cont lines: {len(b_d_lf)}")

# Baseline pos2 for B d-LF lines
b_d_pos2_base = Counter(get_onset(words[2]) for words, _, _ in b_d_lf if len(words) >= 3)
total_d_p2 = sum(b_d_pos2_base.values())

# d→qok lines
b_d_qok = [(words, folio, ln) for words, folio, ln in b_d_lf
           if len(words) >= 2 and get_onset(words[1]) == 'qok']
print(f"\nB d→qok cont lines (N={len(b_d_qok)}):")

pos2_d_qok = Counter(get_onset(words[2]) for words, _, _ in b_d_qok if len(words) >= 3)
total_d_qok_p2 = sum(pos2_d_qok.values())
# Baseline: given pos1=qok in B all lines
b_pos1_qok_p2 = Counter(get_onset(words[2]) for words, _, _ in cont_lines_b
                         if len(words) >= 3 and get_onset(words[1]) == 'qok')
total_b_qok_p2 = sum(b_pos1_qok_p2.values())

print(f"pos2 distribution for d→qok lines (N={total_d_qok_p2}):")
for onset, cnt in sorted(pos2_d_qok.items(), key=lambda x: -x[1]):
    base_d = b_d_pos2_base[onset] / total_d_p2 if total_d_p2 > 0 else 0
    base_qok = b_pos1_qok_p2[onset] / total_b_qok_p2 if total_b_qok_p2 > 0 else 0
    rate = cnt / total_d_qok_p2 if total_d_qok_p2 > 0 else 0
    E_vs_d = rate / base_d if base_d > 0 else float('inf')
    E_vs_qok = rate / base_qok if base_qok > 0 else float('inf')
    print(f"  {onset:6s}: n={cnt:3d}  rate={rate:.3f}  E_vs_d-baseline={E_vs_d:.2f}×  E_vs_qok-baseline={E_vs_qok:.2f}×")

print(f"\nAll d→qok lines:")
for words, folio, ln in b_d_qok:
    onsets = [get_onset(w) for w in words]
    print(f"  {folio}/{ln}: {words[:5]} ... → {onsets[:5]}")

# d→ch lines
b_d_ch = [(words, folio, ln) for words, folio, ln in b_d_lf
          if len(words) >= 2 and get_onset(words[1]) == 'ch']
print(f"\nB d→ch cont lines (N={len(b_d_ch)}):")

pos2_d_ch = Counter(get_onset(words[2]) for words, _, _ in b_d_ch if len(words) >= 3)
total_d_ch_p2 = sum(pos2_d_ch.values())
# Baseline: given pos1=ch in B all lines
b_pos1_ch_p2 = Counter(get_onset(words[2]) for words, _, _ in cont_lines_b
                        if len(words) >= 3 and get_onset(words[1]) == 'ch')
total_b_ch_p2 = sum(b_pos1_ch_p2.values())

print(f"pos2 distribution for d→ch lines (N={total_d_ch_p2}):")
for onset, cnt in sorted(pos2_d_ch.items(), key=lambda x: -x[1]):
    base_d = b_d_pos2_base[onset] / total_d_p2 if total_d_p2 > 0 else 0
    base_ch = b_pos1_ch_p2[onset] / total_b_ch_p2 if total_b_ch_p2 > 0 else 0
    rate = cnt / total_d_ch_p2 if total_d_ch_p2 > 0 else 0
    E_vs_d = rate / base_d if base_d > 0 else float('inf')
    E_vs_ch = rate / base_ch if base_ch > 0 else float('inf')
    if cnt >= 2:
        print(f"  {onset:6s}: n={cnt:3d}  rate={rate:.3f}  E_vs_d-baseline={E_vs_d:.2f}×  E_vs_ch-baseline={E_vs_ch:.2f}×")

# Find the d→ch→y lines specifically
d_ch_y = [(words, folio, ln) for words, folio, ln in b_d_ch
          if len(words) >= 3 and get_onset(words[2]) == 'y']
print(f"\nd→ch→y lines (N={len(d_ch_y)}):")
for words, folio, ln in d_ch_y:
    onsets = [get_onset(w) for w in words]
    print(f"  {folio}/{ln}: {words} → {onsets}")

print("\n=== Done ===")
