"""
exp_420: B l-onset grammar characterization (H641 + H644)

F421: l→ch→qok=2.72×(N=5) is a confirmed formula type.
F422: B l self-succession E=2.35×(N=102) is the highest in B.

Characterize:
1. B l-LF prevalence and pos1 routing
2. B l self-succession by position pair
3. Section distribution of l-dense lines
4. l-run characteristics (longest chains, where they occur)
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

# Folio section classification (approximate from known VMS section boundaries)
def folio_section(fb):
    # Simple numeric extraction for section classification
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

# Pass 2: cont lines with folio info
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

print(f"B cont lines total: {len(cont_lines_b)}")

# B overall LF distribution (baseline)
b_lf_base = Counter(get_onset(words[0]) for words, _, _ in cont_lines_b if len(words) >= 1)
total_b_lf = sum(b_lf_base.values())
print(f"\nB LF distribution (top 10):")
for onset, cnt in sorted(b_lf_base.items(), key=lambda x: -x[1])[:10]:
    print(f"  {onset:6s}: n={cnt:4d}  rate={cnt/total_b_lf:.4f}")

# B l-LF lines
b_l_lf = [(words, fb, ln) for words, fb, ln in cont_lines_b if len(words) >= 2 and get_onset(words[0]) == 'l']
print(f"\nB l-LF cont lines: {len(b_l_lf)}")
n_l_lf = b_lf_base.get('l', 0)
print(f"l at LF rate: {n_l_lf/total_b_lf:.4f}")

# pos1 distribution for B l-LF lines
pos1_l = Counter(get_onset(words[1]) for words, _, _ in b_l_lf)
total_l_p1 = sum(pos1_l.values())
# Overall B pos1 baseline
b_pos1_base = Counter(get_onset(words[1]) for words, _, _ in cont_lines_b if len(words) >= 2)
total_b_p1 = sum(b_pos1_base.values())
print(f"\nB l-LF → pos1 distribution (N={total_l_p1}):")
for onset, cnt in sorted(pos1_l.items(), key=lambda x: -x[1]):
    base = b_pos1_base[onset] / total_b_p1 if total_b_p1 > 0 else 0
    rate = cnt / total_l_p1 if total_l_p1 > 0 else 0
    E = rate / base if base > 0 else float('inf')
    print(f"  {onset:6s}: n={cnt:3d}  rate={rate:.3f}  base={base:.3f}  E={E:.2f}×")

# For l→ch lines: pos2 distribution (check l→ch→qok formula type)
b_l_ch = [(words, fb, ln) for words, fb, ln in b_l_lf if len(words) >= 3 and get_onset(words[1]) == 'ch']
print(f"\nB l→ch lines (N={len(b_l_ch)}):")
pos2_l_ch = Counter(get_onset(words[2]) for words, _, _ in b_l_ch)
total_l_ch_p2 = sum(pos2_l_ch.values())
# Baseline pos2 given pos1=ch in B
b_p2_given_ch = Counter(get_onset(words[2]) for words, _, _ in cont_lines_b
                        if len(words) >= 3 and get_onset(words[1]) == 'ch')
total_b_p2_ch = sum(b_p2_given_ch.values())
for onset, cnt in sorted(pos2_l_ch.items(), key=lambda x: -x[1]):
    base = b_p2_given_ch[onset] / total_b_p2_ch if total_b_p2_ch > 0 else 0
    rate = cnt / total_l_ch_p2 if total_l_ch_p2 > 0 else 0
    E = rate / base if base > 0 else float('inf')
    print(f"  {onset:6s}: n={cnt:3d}  rate={rate:.3f}  base={base:.3f}  E={E:.2f}×")

# l self-succession by position pair
print("\nB l self-succession by position pair:")
pos_pairs = [(0,1,'LF→pos1'), (1,2,'pos1→pos2'), (2,3,'pos2→pos3'), (3,4,'pos3→pos4')]
for i, j, label in pos_pairs:
    l_given_l = sum(1 for words, _, _ in cont_lines_b
                    if len(words) > j and get_onset(words[i]) == 'l' and get_onset(words[j]) == 'l')
    l_i = sum(1 for words, _, _ in cont_lines_b if len(words) > i and get_onset(words[i]) == 'l')
    # All successors from position i
    all_j = sum(1 for words, _, _ in cont_lines_b if len(words) > j)
    l_j = sum(1 for words, _, _ in cont_lines_b if len(words) > j and get_onset(words[j]) == 'l')
    if l_i > 0 and all_j > 0 and l_j > 0:
        p_l_given_l = l_given_l / l_i if l_i > 0 else 0
        p_l_base = l_j / all_j
        E = p_l_given_l / p_l_base if p_l_base > 0 else float('inf')
        print(f"  {label}: n(l→l)={l_given_l}  N(l at pos{i})={l_i}  P(l|l)={p_l_given_l:.3f}  base={p_l_base:.3f}  E={E:.2f}×")

# l self-succession in MID positions
l_mid_self = 0
l_mid_total = 0
for words, _, _ in cont_lines_b:
    if len(words) >= 5:
        mid_onsets = [get_onset(words[k]) for k in range(2, len(words)-2)]
        for k in range(len(mid_onsets)-1):
            if mid_onsets[k] != 'other':
                l_mid_total += 1 if mid_onsets[k] == 'l' else 0
                if mid_onsets[k] == 'l' and mid_onsets[k+1] == 'l':
                    l_mid_self += 1
# Baseline l freq in MID
l_mid_freq = sum(1 for words, _, _ in cont_lines_b if len(words) >= 5
                 for w in words[2:-2] if get_onset(w) == 'l')
all_mid_tokens = sum(len(words)-4 for words, _, _ in cont_lines_b if len(words) >= 5)
l_mid_base = l_mid_freq / all_mid_tokens if all_mid_tokens > 0 else 0
l_mid_self_rate = l_mid_self / l_mid_total if l_mid_total > 0 else 0
E_l_mid = l_mid_self_rate / l_mid_base if l_mid_base > 0 else float('inf')
print(f"\n  MID→next (positions 2..n-3): n(l→l)={l_mid_self}  N(l in MID)={l_mid_total}  P(l|l)={l_mid_self_rate:.3f}  base={l_mid_base:.3f}  E={E_l_mid:.2f}×")

# Section distribution of l-onset dense lines
print("\nSection distribution of B cont lines (l-onset at any position):")
section_l_count = Counter()
section_total = Counter()
for words, fb, ln in cont_lines_b:
    sec = folio_section(fb)
    section_total[sec] += 1
    l_count = sum(1 for w in words if get_onset(w) == 'l')
    if l_count >= 3:
        section_l_count[sec] += 1

for sec in ['herbal', 'astro', 'bio', 'pharma', 'text']:
    n_total = section_total.get(sec, 0)
    n_l = section_l_count.get(sec, 0)
    rate = n_l / n_total if n_total > 0 else 0
    print(f"  {sec:8s}: l-dense lines(≥3 l-words) = {n_l}/{n_total}  ({rate:.3f})")

# Longest l-chains and their lines
print("\nLongest consecutive l-onset runs in B cont lines:")
l_runs = []
for words, fb, ln in cont_lines_b:
    onsets = [get_onset(w) for w in words]
    i = 0
    while i < len(onsets):
        if onsets[i] == 'l':
            run_len = 1
            while i + run_len < len(onsets) and onsets[i+run_len] == 'l':
                run_len += 1
            if run_len >= 2:
                l_runs.append((run_len, fb, ln, words[i:i+run_len], i))
            i += run_len
        else:
            i += 1

l_runs.sort(reverse=True)
for run_len, fb, ln, words_snippet, pos in l_runs[:10]:
    print(f"  len={run_len} at pos{pos} in {fb}/{ln}: {words_snippet}")

print("\n=== Done ===")
