"""
exp_392: B p→sh Line Structure Analysis (H607)

Analyzes B continuation lines with p-onset at LF, sh at pos1.
Compares pos2-through-LL distribution vs (all LF, pos1=sh) baseline.
Tests whether p→sh lines have distinct gallows-specific grammar.
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

folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
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
            if w.endswith('eedy'):
                folio_word_stats[fb]['eedy'] += 1
            elif w.endswith('edy'):
                folio_word_stats[fb]['edy'] += 1

def classify_dialect(stats):
    total = stats['total']
    if total == 0:
        return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

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
        dialect = folio_dialect.get(fb, 'unknown')
        if dialect not in ('A', 'B'):
            continue
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if len(words) < 1:
            continue
        folio_lines[fb].append((line_num, words, dialect))

# B lines with p at LF, sh at pos1 — and comparison groups
p_sh_lines = []  # (words, fb, ln)
sh_pos1_lines = []  # any LF → sh at pos1
b_sh_baseline_pos2 = Counter()  # pos2 class when pos1=sh (any LF)

for fb, lines_list in folio_lines.items():
    if not lines_list:
        continue
    dialect = lines_list[0][2]
    if dialect != 'B':
        continue
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln, max_ln = min(line_nums), max(line_nums)
    for ln, words, d in lines_list:
        if ln == min_ln or ln == max_ln:
            continue
        n = len(words)
        if n < 2:
            continue
        lf_onset = get_onset(words[0])
        if n >= 1:
            p1_onset = get_onset(words[1]) if n >= 2 else None
            if p1_onset == 'sh':
                sh_pos1_lines.append((words, fb, ln))
                if n >= 3:
                    p2_onset = get_onset(words[2])
                    b_sh_baseline_pos2[p2_onset] += 1
                if lf_onset == 'p':
                    p_sh_lines.append((words, fb, ln))

print(f"B continuation lines with sh at pos1: {len(sh_pos1_lines)}")
print(f"B continuation lines with p at LF and sh at pos1: {len(p_sh_lines)}")

# pos2 distribution for p→sh lines
p_sh_pos2 = Counter()
p_sh_ll = Counter()
p_sh_lengths = Counter()
for words, fb, ln in p_sh_lines:
    n = len(words)
    p_sh_lengths[n] += 1
    if n >= 3:
        p2_onset = get_onset(words[2])
        p_sh_pos2[p2_onset] += 1
    ll_word = words[-1]
    p_sh_ll[get_onset(ll_word)] += 1

print(f"\n--- p→sh line statistics ---")
print(f"N p→sh lines: {len(p_sh_lines)}")
print(f"Length distribution: {dict(sorted(p_sh_lengths.items()))}")

print(f"\n--- pos2 class distribution: p→sh lines vs sh baseline ---")
total_p_sh_p2 = sum(p_sh_pos2.values())
total_sh_baseline = sum(b_sh_baseline_pos2.values())
print(f"N p→sh lines with pos2: {total_p_sh_p2}, N sh baseline with pos2: {total_sh_baseline}")

CLASSES = ['ch', 'sh', 'qok', 'ok', 'ot', 'qot', 'd', 's', 'y', 'ol', 'r', 'p', 't', 'k', 'other']
print(f"\n{'pos2':<8} {'p→sh':>8} {'%':>6} | {'sh_base':>8} {'%':>6} | E")
for c in CLASSES:
    n_p = p_sh_pos2.get(c, 0)
    n_b = b_sh_baseline_pos2.get(c, 0)
    if n_p == 0 and n_b == 0:
        continue
    p_p = n_p / total_p_sh_p2 if total_p_sh_p2 > 0 else 0
    p_b = n_b / total_sh_baseline if total_sh_baseline > 0 else 0
    e = p_p / p_b if p_b > 0 else float('inf')
    print(f"{c:<8} {n_p:>8} {p_p*100:>5.1f}% | {n_b:>8} {p_b*100:>5.1f}% | {e:.2f}×")

print(f"\n--- LL distribution for p→sh lines ---")
total_p_sh_ll = sum(p_sh_ll.values())
for c in CLASSES:
    n = p_sh_ll.get(c, 0)
    if n > 0:
        print(f"  LL={c}: {n}/{total_p_sh_ll} ({n/total_p_sh_ll*100:.1f}%)")

# Compare LF-class breakdown of sh-pos1 lines
print(f"\n--- p→sh vs other LF-class→sh lines: pos2 ch rate ---")
lf_sh_pos2_ch = {}  # LF onset → (n_ch_at_p2, n_total_p2)
for words, fb, ln in sh_pos1_lines:
    n = len(words)
    if n < 3:
        continue
    lf_onset = get_onset(words[0])
    p2_onset = get_onset(words[2])
    if lf_onset not in lf_sh_pos2_ch:
        lf_sh_pos2_ch[lf_onset] = [0, 0]
    lf_sh_pos2_ch[lf_onset][1] += 1
    if p2_onset == 'ch':
        lf_sh_pos2_ch[lf_onset][0] += 1

print(f"\nLF onset | N   | pos2=ch rate | baseline sh→ch")
for onset in ['p', 'y', 'd', 's', 'qok', 'ch', 'sh', 't', 'k']:
    if onset in lf_sh_pos2_ch:
        n_ch, n_total = lf_sh_pos2_ch[onset]
        rate = n_ch / n_total if n_total > 0 else 0
        baseline = b_sh_baseline_pos2.get('ch', 0) / total_sh_baseline if total_sh_baseline > 0 else 0
        e = rate / baseline if baseline > 0 else float('inf')
        print(f"  {onset:<8} {n_total:>5} | {n_ch}/{n_total}={rate*100:.1f}% | baseline={baseline*100:.1f}% | E={e:.2f}×")

# Print actual p→sh lines
print(f"\n--- Actual B p→sh continuation lines ---")
for words, fb, ln in p_sh_lines[:20]:
    onsets = [get_onset(w) for w in words]
    print(f"  [{fb}/{ln}] {' '.join(words[:8])}")
    print(f"    onsets: {' '.join(onsets[:8])}")

