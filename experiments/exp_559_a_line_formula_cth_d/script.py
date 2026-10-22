"""
exp_559: A herbal_a line structure formula test — [qo/qot opener]...[cth word]...[d at LF]
H_new_FV: Test whether [cth at LL][d at LF] is a recurring A structural formula.

Parts:
1. Among A lines with LF=d: fraction containing at least one cth word (and where).
2. Among A lines with LF=cth: fraction followed by d-LF line (within-paragraph).
3. Is [cth][d] predominantly LL+LF? Full position analysis of [cth][d] consecutive pairs.
4. Most common [cth-word][d-word] bigram pairs.
5. Pos1 profile of lines containing the [cth at LL][d at LF] formula.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
ONSET_PRIORITY = ['qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph',
                  'd','s','y','k','t','l','r','p','f','o','e','a','n','m']

def get_onset(w):
    for o in ONSET_PRIORITY:
        if w.startswith(o):
            return o
    return w[0] if w else None

def parse_corpus(filepath):
    lines_A, lines_B = [], []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)', line)
            if not m: continue
            folio_raw, n_str, lc, text = m.group(1), m.group(2), m.group(3), m.group(4)
            lc2 = lc.lstrip('+*=/~&').lstrip('@')
            if not lc2.startswith('P'): continue
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue
            try: n = int(n_str)
            except: continue
            edy_count = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
            is_b = edy_count / len(words) >= 0.05
            if is_b:
                lines_B.append((folio_raw, n, lc2, words))
            else:
                if n <= 56:
                    lines_A.append((folio_raw, n, lc2, words))
    return lines_A, lines_B

lines_A, lines_B = parse_corpus(CORPUS)
print(f"A herbal_a: {len(lines_A)} lines; B all: {len(lines_B)} lines")

# Filter to lines with >= 2 words (needed for positional analysis)
lines_A_multi = [(fo, n, lc, ws) for fo, n, lc, ws in lines_A if len(ws) >= 2]
print(f"A herbal_a multi-word lines: {len(lines_A_multi)}")

# --- Part 1: Among A lines with LF=d, what fraction contain a cth word? ---
print("\n=== PART 1: A lines with LF=d — cth co-occurrence ===")

d_lf_lines = [(fo, n, lc, ws) for fo, n, lc, ws in lines_A_multi if get_onset(ws[-1]) == 'd']
print(f"A lines with LF=d: {len(d_lf_lines)}")

# Among d-LF lines: does any word (excluding LF) have cth onset?
d_lf_has_cth = [(fo, n, lc, ws) for fo, n, lc, ws in d_lf_lines if any(get_onset(w) == 'cth' for w in ws[:-1])]
print(f"d-LF lines with cth word (pre-LF): {len(d_lf_has_cth)} ({100*len(d_lf_has_cth)/len(d_lf_lines):.1f}%)")

# Position of cth within d-LF lines
# For a line of length L, positions: pos1=0, MID=1..L-3, LL=L-2, LF=L-1
cth_positions_in_dlf = Counter()
for fo, n, lc, ws in d_lf_has_cth:
    L = len(ws)
    for i, w in enumerate(ws[:-1]):  # exclude LF position
        if get_onset(w) == 'cth':
            if i == 0:
                cth_positions_in_dlf['pos1'] += 1
            elif i == L - 2:
                cth_positions_in_dlf['LL'] += 1
            else:
                cth_positions_in_dlf['MID'] += 1

print(f"Position of cth within d-LF lines:")
for pos, cnt in sorted(cth_positions_in_dlf.items()):
    print(f"  cth@{pos}: {cnt}")

# Baseline: what fraction of all A multi-word lines contain a cth word (at non-LF position)?
all_has_cth = sum(1 for fo, n, lc, ws in lines_A_multi if any(get_onset(w) == 'cth' for w in ws[:-1]))
baseline_cth_rate = all_has_cth / len(lines_A_multi)
dlf_cth_rate = len(d_lf_has_cth) / len(d_lf_lines)
print(f"\nBaseline A: fraction of multi-word lines with any cth (excl LF): {all_has_cth}/{len(lines_A_multi)} = {baseline_cth_rate:.4f}")
print(f"d-LF lines with cth: {len(d_lf_has_cth)}/{len(d_lf_lines)} = {dlf_cth_rate:.4f}")
print(f"Enrichment E = {dlf_cth_rate/baseline_cth_rate:.2f}×")

# Expected if baseline:
expected_cth_in_dlf = baseline_cth_rate * len(d_lf_lines)
print(f"Expected if baseline: {expected_cth_in_dlf:.1f}")

# --- Part 2: [cth at LL][d at LF] specifically ---
print("\n=== PART 2: [cth at LL][d at LF] — LL+LF formula ===")

cth_ll_d_lf = [(fo, n, lc, ws) for fo, n, lc, ws in lines_A_multi
               if len(ws) >= 2 and get_onset(ws[-2]) == 'cth' and get_onset(ws[-1]) == 'd']
print(f"Lines with [cth@LL][d@LF]: {len(cth_ll_d_lf)}")
print(f"As fraction of d-LF lines: {len(cth_ll_d_lf)}/{len(d_lf_lines)} = {100*len(cth_ll_d_lf)/len(d_lf_lines):.1f}%")

# How does this compare to baseline [X@LL][d@LF]?
# What fraction of d-LF lines have cth specifically at LL vs other classes at LL?
ll_class_before_d = Counter()
for fo, n, lc, ws in d_lf_lines:
    if len(ws) >= 2:
        ll_class_before_d[get_onset(ws[-2])] += 1

print(f"\nLL class distribution for d-LF lines (top 10):")
total_dlf_with_ll = sum(ll_class_before_d.values())
for cls, cnt in ll_class_before_d.most_common(10):
    print(f"  {cls}: {cnt} ({100*cnt/total_dlf_with_ll:.1f}%)")

# MID baseline for LL class in A
mid_counts_A = Counter()
for fo, n, lc, ws in lines_A:
    if len(ws) >= 3:
        for w in ws[1:-1]:  # MID positions
            mid_counts_A[get_onset(w)] += 1
total_mid_A = sum(mid_counts_A.values())

print(f"\nExpected LL=cth if MID baseline: {mid_counts_A['cth']/total_mid_A:.4f} × {total_dlf_with_ll} = {mid_counts_A['cth']/total_mid_A*total_dlf_with_ll:.1f}")
print(f"Observed LL=cth in d-LF lines: {ll_class_before_d['cth']}")
e_cth_ll_dlf = (ll_class_before_d['cth'] / total_dlf_with_ll) / (mid_counts_A['cth'] / total_mid_A)
print(f"E(cth@LL in d-LF lines vs MID baseline) = {e_cth_ll_dlf:.2f}×")

# --- Part 3: [cth-word][d-word] bigram pairs ---
print("\n=== PART 3: [cth-word][d-word] consecutive bigram pairs ===")

cth_d_bigrams = Counter()
for fo, n, lc, ws in lines_A_multi:
    for i in range(len(ws) - 1):
        if get_onset(ws[i]) == 'cth' and get_onset(ws[i+1]) == 'd':
            cth_d_bigrams[(ws[i], ws[i+1])] += 1

print(f"Total [cth→d] bigrams in A: {sum(cth_d_bigrams.values())}")
print(f"Unique [cth→d] pairs: {len(cth_d_bigrams)}")
print(f"Top 15 [cth-word][d-word] pairs:")
for pair, cnt in cth_d_bigrams.most_common(15):
    print(f"  {pair[0]} → {pair[1]}: {cnt}")

# Position of [cth][d] bigrams
cth_d_pos = Counter()
for fo, n, lc, ws in lines_A_multi:
    L = len(ws)
    for i in range(L - 1):
        if get_onset(ws[i]) == 'cth' and get_onset(ws[i+1]) == 'd':
            if i == L - 2:
                cth_d_pos['LL→LF'] += 1
            elif i == 0:
                cth_d_pos['pos1→pos2'] += 1
            else:
                cth_d_pos['MID→MID+1'] += 1

print(f"\nPosition of [cth][d] bigrams:")
for pos, cnt in cth_d_pos.items():
    print(f"  {pos}: {cnt}")

# --- Part 4: Pos1 profile of lines containing [cth@LL][d@LF] ---
print("\n=== PART 4: Pos1 profile of [cth@LL][d@LF] formula lines ===")

formula_lines = [(fo, n, lc, ws) for fo, n, lc, ws in lines_A_multi
                 if len(ws) >= 3 and get_onset(ws[-2]) == 'cth' and get_onset(ws[-1]) == 'd']
print(f"Formula lines [cth@LL][d@LF] with >= 3 words: {len(formula_lines)}")

formula_pos1 = Counter()
for fo, n, lc, ws in formula_lines:
    formula_pos1[get_onset(ws[0])] += 1

# Also get A herbal_a pos1 baseline (all multi-word lines)
a_pos1_baseline = Counter()
for fo, n, lc, ws in lines_A_multi:
    a_pos1_baseline[get_onset(ws[0])] += 1
total_a_pos1 = sum(a_pos1_baseline.values())

print(f"\nPos1 distribution for formula lines (top 10 vs baseline):")
total_formula = sum(formula_pos1.values())
for cls, cnt in formula_pos1.most_common(10):
    baseline_rate = a_pos1_baseline[cls] / total_a_pos1
    obs_rate = cnt / total_formula
    e = obs_rate / baseline_rate if baseline_rate > 0 else float('inf')
    flag = 'CONF' if e >= 1.5 and cnt >= 10 else ('dir' if e >= 2.0 and cnt >= 5 else ('(dir)' if e >= 2.5 and cnt >= 3 else ('DEPL' if e < 0.7 and cnt >= 3 else '')))
    print(f"  {cls}: {cnt} (obs_rate={obs_rate:.3f} vs base={baseline_rate:.3f} → E={e:.2f}×) {flag}")

# --- Part 5: Lines with LF=cth — are they followed by d-LF lines? ---
print("\n=== PART 5: Lines with LF=cth — successor d-LF rate ===")

# Parse corpus preserving order (by folio/paragraph)
# Need to check consecutive lines within same paragraph/CL
# We'll use (folio, n-ordering) to find consecutive lines

# First, group A lines by folio
from collections import defaultdict
folio_lines = defaultdict(list)
for fo, n, lc, ws in lines_A_multi:
    folio_lines[fo].append((n, lc, ws))

# Sort within each folio by line number
for fo in folio_lines:
    folio_lines[fo].sort(key=lambda x: x[0])

cth_lf_count = 0
cth_lf_followed_by_dlf = 0
cth_lf_total_successors = Counter()  # What LF class follows cth-LF lines?

for fo, flines in folio_lines.items():
    for i, (n, lc, ws) in enumerate(flines):
        if get_onset(ws[-1]) == 'cth':
            cth_lf_count += 1
            if i + 1 < len(flines):
                next_ws = flines[i+1][2]
                next_lf = get_onset(next_ws[-1])
                cth_lf_total_successors[next_lf] += 1
                if next_lf == 'd':
                    cth_lf_followed_by_dlf += 1

print(f"A lines with LF=cth: {cth_lf_count}")
print(f"Cth-LF lines with known successor: {sum(cth_lf_total_successors.values())}")
print(f"Cth-LF lines followed by d-LF line: {cth_lf_followed_by_dlf}")
if sum(cth_lf_total_successors.values()) > 0:
    print(f"Rate: {cth_lf_followed_by_dlf}/{sum(cth_lf_total_successors.values())} = {100*cth_lf_followed_by_dlf/sum(cth_lf_total_successors.values()):.1f}%")

# Baseline: what fraction of A lines have LF=d?
total_A_multi = len(lines_A_multi)
d_lf_total = len(d_lf_lines)
baseline_dlf_rate = d_lf_total / total_A_multi
print(f"Baseline A LF=d rate: {d_lf_total}/{total_A_multi} = {baseline_dlf_rate:.4f}")

if sum(cth_lf_total_successors.values()) > 0:
    obs_rate = cth_lf_followed_by_dlf / sum(cth_lf_total_successors.values())
    e = obs_rate / baseline_dlf_rate if baseline_dlf_rate > 0 else float('inf')
    print(f"E(d-LF successor after cth-LF) = {e:.2f}×")

print(f"\nSuccessor LF class distribution after cth-LF lines (top 8):")
total_succ = sum(cth_lf_total_successors.values())
for cls, cnt in cth_lf_total_successors.most_common(8):
    print(f"  {cls}: {cnt} ({100*cnt/total_succ:.1f}%)")

# --- Summary ---
print("\n=== SUMMARY ===")
print(f"d-LF lines: {len(d_lf_lines)}")
print(f"d-LF lines with any cth (pre-LF): {len(d_lf_has_cth)} ({100*len(d_lf_has_cth)/len(d_lf_lines):.1f}%) E={dlf_cth_rate/baseline_cth_rate:.2f}×")
print(f"[cth@LL][d@LF] specifically: {len(cth_ll_d_lf)} ({100*len(cth_ll_d_lf)/len(d_lf_lines):.1f}% of d-LF); E(cth@LL vs MID base)={e_cth_ll_dlf:.2f}×")
print(f"Total [cth→d] consecutive bigrams: {sum(cth_d_bigrams.values())} ({cth_d_pos.get('LL→LF',0)} at LL→LF)")
print(f"Cth-LF followed by d-LF: {cth_lf_followed_by_dlf}/{sum(cth_lf_total_successors.values())} ({100*cth_lf_followed_by_dlf/max(1,sum(cth_lf_total_successors.values())):.1f}%)")
