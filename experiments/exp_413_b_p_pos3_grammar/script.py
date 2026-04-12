"""
exp_413: B p-Formula pos3 Grammar (H623)

For B continuation lines with p at LF (N~229):
1. For all B p-LF lines with >=4 words: compute pos3 onset distribution
   conditioned on pos2 class (pos2->pos3 routing within p-formula lines).
2. Specifically: for p->sh->qot[pos2], what is pos3?
3. Compare pos3 distribution in p-LF lines to B baseline pos3 distribution.
4. Also compute: for each formula-type (p->sh, p->o, p->ch, etc.),
   what is the pos3 distribution?
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

b_cont_lines = []
b_p_lf_lines = []  # B cont lines with p at LF
for fb, entries in folio_lines.items():
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in entries:
        if ln != min_ln and ln != max_ln:
            b_cont_lines.append(words)
            if len(words) >= 1 and get_onset(words[0]) == 'p':
                b_p_lf_lines.append(words)

print(f"B cont lines: {len(b_cont_lines)}")
print(f"B p-LF cont lines: {len(b_p_lf_lines)}")

# Baseline: pos3 distribution across ALL B cont lines (len>=4)
baseline_pos3 = Counter()
for words in b_cont_lines:
    if len(words) >= 4:
        baseline_pos3[get_onset(words[3])] += 1
total_p3 = sum(baseline_pos3.values())

# For B p-LF lines with >=4 words: pos3 distribution
p_lf_pos3 = Counter()
# Also condition on pos1 and pos2
p_lf_pos1_pos2_pos3 = Counter()  # (pos1, pos2, pos3)
p_lf_pos2_pos3 = Counter()  # (pos2, pos3) for all p-LF lines

p_lf_len4_total = 0
for words in b_p_lf_lines:
    if len(words) < 4:
        continue
    o1 = get_onset(words[1])
    o2 = get_onset(words[2])
    o3 = get_onset(words[3])
    p_lf_pos3[o3] += 1
    p_lf_pos1_pos2_pos3[(o1, o2, o3)] += 1
    p_lf_pos2_pos3[(o2, o3)] += 1
    p_lf_len4_total += 1

print(f"\nB p-LF lines with >=4 words: {p_lf_len4_total}")

# Baseline pos2->pos3 conditional across all B cont lines (len>=4)
b_cont_pos2_pos3 = Counter()
b_cont_pos2_total = Counter()
for words in b_cont_lines:
    if len(words) >= 4:
        o2 = get_onset(words[2])
        o3 = get_onset(words[3])
        b_cont_pos2_pos3[(o2, o3)] += 1
        b_cont_pos2_total[o2] += 1

# Report: B p-LF pos3 distribution vs baseline
print("\n=== B p-LF pos3 distribution vs baseline (len>=4) ===")
p3_items = sorted(p_lf_pos3.items(), key=lambda x: -x[1])[:12]
for onset, cnt in p3_items:
    rate_p = cnt / p_lf_len4_total
    rate_b = baseline_pos3[onset] / total_p3 if total_p3 > 0 else 0
    E = rate_p / rate_b if rate_b > 0 else float('inf')
    print(f"  {onset:6s}: n={cnt:3d}  rate={rate_p:.3f}  baseline={rate_b:.3f}  E={E:.2f}×")

# Report: B p-LF pos2->pos3 routing (given pos2 class in p-LF lines)
print("\n=== B p-LF: pos2 -> pos3 routing (E vs B baseline pos2->pos3) ===")
# Focus on top pos2 classes in p-LF lines
p_lf_pos2_total = Counter()
for (o2, o3), cnt in p_lf_pos2_pos3.items():
    p_lf_pos2_total[o2] += cnt

for pos2 in ['sh', 'o', 'ch', 'ot', 'ok', 'qot']:
    n_p2 = p_lf_pos2_total[pos2]
    if n_p2 < 3:
        continue
    print(f"\n  pos2={pos2} (N={n_p2} in p-LF lines):")
    p2_p3_items = [(o3, p_lf_pos2_pos3[(pos2, o3)]) for o3 in set(baseline_pos3.keys())
                   if p_lf_pos2_pos3[(pos2, o3)] > 0]
    p2_p3_items.sort(key=lambda x: -x[1])
    for o3, cnt in p2_p3_items[:8]:
        rate_p = cnt / n_p2
        # Baseline: pos2->pos3 in ALL B cont lines
        b_p2_total = b_cont_pos2_total[pos2]
        rate_b = b_cont_pos2_pos3[(pos2, o3)] / b_p2_total if b_p2_total > 0 else 0
        E = rate_p / rate_b if rate_b > 0 else float('inf')
        print(f"    {o3:6s}: n={cnt:3d}  rate={rate_p:.3f}  base={rate_b:.3f}  E={E:.2f}×")

# Special: p -> sh -> qot -> pos3
print("\n=== B p->sh->qot: pos3 routing (N available) ===")
p_sh_qot_pos3 = Counter()
for words in b_p_lf_lines:
    if len(words) >= 4:
        if get_onset(words[1]) == 'sh' and get_onset(words[2]) == 'qot':
            p_sh_qot_pos3[get_onset(words[3])] += 1

n_p_sh_qot = sum(p_sh_qot_pos3.values())
print(f"p->sh->qot lines with >=4 words: {n_p_sh_qot}")
for onset, cnt in sorted(p_sh_qot_pos3.items(), key=lambda x: -x[1]):
    rate_p = cnt / n_p_sh_qot if n_p_sh_qot > 0 else 0
    # Baseline: qot->pos3 in B cont lines
    b_qot_total = b_cont_pos2_total['qot']
    rate_b = b_cont_pos2_pos3[('qot', onset)] / b_qot_total if b_qot_total > 0 else 0
    E = rate_p / rate_b if rate_b > 0 else float('inf')
    print(f"  {onset:6s}: n={cnt}  rate={rate_p:.3f}  base={rate_b:.3f}  E={E:.2f}×")

# Also show p -> o -> pos3 (new formula type from F409)
print("\n=== B p->o (pos1=o): pos2->pos3 routing (N p-o lines) ===")
p_o_lines = [w for w in b_p_lf_lines if len(w) >= 3 and get_onset(w[1]) == 'o']
print(f"p->o lines: {len(p_o_lines)}")
p_o_pos2 = Counter(get_onset(w[2]) for w in p_o_lines)
for pos2_onset, cnt in p_o_pos2.most_common(6):
    rate_here = cnt / len(p_o_lines)
    # Baseline: o->pos2 in B cont lines
    b_o_total = sum(b_cont_pos2_pos3.get(('o', o), 0) for o in set(baseline_pos3.keys()))
    # Actually need pos1->pos2, not pos2->pos3. Let me use simple b pos2 rate
    print(f"  pos2={pos2_onset}: n={cnt}  rate={rate_here:.3f}")

print("\n=== Done ===")
