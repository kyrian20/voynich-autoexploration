"""
exp_564: sh-onset full characterization (H_new_GB)
sh = words starting with "sh" (after sch, skh, sph in ONSET_PRIORITY)
Parts:
1. Vocabulary (top-20 sh words, A and B)
2. Positional distribution (pos1/MID/LL/LF vs baseline)
3. sh within-line bigrams (outgoing and incoming)
4. sh-LF pos1 profile (lines ending in sh)
5. sh pos1 profile — lines opened by sh (opener check)
"""

import re
from collections import Counter

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
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
                lines_B.append((folio_raw, words))
            else:
                if n <= 56:
                    lines_A.append((folio_raw, words))
    return lines_A, lines_B

lines_A, lines_B = parse_corpus(CORPUS)
print(f"A herbal_a: {len(lines_A)} lines; B all: {len(lines_B)} lines")

all_A_words = [w for fo, ws in lines_A for w in ws]
all_B_words = [w for fo, ws in lines_B for w in ws]

# --- Part 1: Vocabulary ---
print("\n=== PART 1: sh vocabulary ===")
for words, label in [(all_A_words, "A herbal_a"), (all_B_words, "B all")]:
    total = len(words)
    sh_words = [w for w in words if get_onset(w) == 'sh']
    print(f"\n{label}: {len(sh_words)} sh tokens ({100*len(sh_words)/total:.2f}% of {total})")
    wc = Counter(sh_words)
    print(f"  Unique types: {len(wc)}")
    print(f"  Top-20:")
    for w, c in wc.most_common(20):
        print(f"    {w}: {c} ({100*c/len(sh_words):.1f}%)")

# --- Part 2: Positional distribution ---
print("\n=== PART 2: sh positional distribution ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    pos_counts = {'pos1': 0, 'MID': 0, 'LL': 0, 'LF': 0}
    total_counts = {'pos1': 0, 'MID': 0, 'LL': 0, 'LF': 0}

    for fo, ws in lines:
        L = len(ws)
        if L < 1: continue
        onsets = [get_onset(w) for w in ws]

        total_counts['pos1'] += 1
        if onsets[0] == 'sh': pos_counts['pos1'] += 1

        if L >= 2:
            total_counts['LF'] += 1
            if onsets[-1] == 'sh': pos_counts['LF'] += 1
            total_counts['LL'] += 1
            if onsets[-2] == 'sh': pos_counts['LL'] += 1

        for i in range(1, L-1):
            total_counts['MID'] += 1
            if onsets[i] == 'sh': pos_counts['MID'] += 1

    mid_rate = pos_counts['MID'] / total_counts['MID'] if total_counts['MID'] > 0 else 0
    print(f"\n{label} (MID baseline: {pos_counts['MID']}/{total_counts['MID']} = {mid_rate:.4f}):")
    for pos in ['pos1', 'LL', 'LF']:
        obs = pos_counts[pos]
        tot = total_counts[pos]
        if tot == 0: continue
        exp = mid_rate * tot
        e = (obs/tot) / mid_rate if mid_rate > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"  {pos}: obs={obs}/{tot}, exp={exp:.1f}, E={e:.2f}× {flag}")

# --- Part 3: bigrams ---
print("\n=== PART 3: sh bigrams ===")
for lines, all_words, label in [(lines_A, all_A_words, "A herbal_a"), (lines_B, all_B_words, "B all")]:
    mid_counts = Counter()
    total_mid = 0
    for fo, ws in lines:
        L = len(ws)
        for i in range(1, L-1):
            mid_counts[get_onset(ws[i])] += 1
            total_mid += 1

    outgoing = Counter()
    n_sender = 0
    for fo, ws in lines:
        for i in range(len(ws) - 1):
            if get_onset(ws[i]) == 'sh':
                outgoing[get_onset(ws[i+1])] += 1
                n_sender += 1

    incoming = Counter()
    n_receiver = 0
    for fo, ws in lines:
        for i in range(1, len(ws)):
            if get_onset(ws[i]) == 'sh':
                incoming[get_onset(ws[i-1])] += 1
                n_receiver += 1

    overall = Counter(get_onset(w) for w in all_words)
    total_overall = len(all_words)

    print(f"\n{label} (sender={n_sender}, receiver={n_receiver}, MID_baseline={total_mid}):")
    print(f"  Outgoing sh→X (top 15):")
    for cls, obs in outgoing.most_common(15):
        exp = (mid_counts[cls] / total_mid) * n_sender if total_mid > 0 else 0
        e = obs / exp if exp > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"    sh→{cls}: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")

    print(f"  Incoming X→sh (top 15):")
    for cls, obs in incoming.most_common(15):
        exp = (overall[cls] / total_overall) * n_receiver if total_overall > 0 else 0
        e = obs / exp if exp > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"    {cls}→sh: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")

# --- Part 4: sh-LF pos1 profile ---
print("\n=== PART 4: sh-LF pos1 profile ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    sh_lf = [(fo, ws) for fo, ws in lines if len(ws) >= 2 and get_onset(ws[-1]) == 'sh']
    print(f"\n{label}: sh-LF lines: {len(sh_lf)}")
    if len(sh_lf) < 5:
        print(f"  Underpowered.")
        continue

    pos1_counts = Counter()
    for fo, ws in sh_lf:
        pos1_counts[get_onset(ws[0])] += 1

    a_pos1 = Counter()
    for fo, ws in lines:
        if len(ws) >= 2:
            a_pos1[get_onset(ws[0])] += 1
    total_base = sum(a_pos1.values())
    total_sh_lf = sum(pos1_counts.values())

    print(f"  Pos1 distribution (top 10):")
    for cls, obs in pos1_counts.most_common(10):
        base = a_pos1[cls] / total_base if total_base > 0 else 0
        obs_rate = obs / total_sh_lf
        e = obs_rate / base if base > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"    {cls}@pos1: {obs} (E={e:.2f}×) {flag}")

# --- Part 5: sh-pos1 (opener profile — lines starting with sh) ---
print("\n=== PART 5: sh-pos1 line structure ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    sh_pos1 = [(fo, ws) for fo, ws in lines if len(ws) >= 2 and get_onset(ws[0]) == 'sh']
    print(f"\n{label}: sh-pos1 lines: {len(sh_pos1)}")
    if len(sh_pos1) < 3:
        print(f"  Underpowered.")
        continue
    # LF class of sh-opener lines
    lf_counts = Counter()
    for fo, ws in sh_pos1:
        lf_counts[get_onset(ws[-1])] += 1
    total_sh_pos1 = sum(lf_counts.values())
    # baseline LF distribution
    lf_base = Counter()
    for fo, ws in lines:
        if len(ws) >= 2:
            lf_base[get_onset(ws[-1])] += 1
    total_lf_base = sum(lf_base.values())
    print(f"  LF class distribution for sh-opener lines (top 10):")
    for cls, obs in lf_counts.most_common(10):
        base = lf_base[cls] / total_lf_base if total_lf_base > 0 else 0
        obs_rate = obs / total_sh_pos1
        e = obs_rate / base if base > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"    {cls}@LF: {obs} (E={e:.2f}×) {flag}")
    # pos2 class of sh-opener lines
    pos2_counts = Counter()
    for fo, ws in sh_pos1:
        if len(ws) >= 2:
            pos2_counts[get_onset(ws[1])] += 1
    total_pos2 = sum(pos2_counts.values())
    mid_base_pos2 = Counter()
    mid_total_pos2 = 0
    for fo, ws in lines:
        L = len(ws)
        for i in range(1, L-1):
            mid_base_pos2[get_onset(ws[i])] += 1
            mid_total_pos2 += 1
    print(f"  Pos2 class for sh-opener lines (top 10):")
    for cls, obs in pos2_counts.most_common(10):
        exp = (mid_base_pos2[cls] / mid_total_pos2) * total_pos2 if mid_total_pos2 > 0 else 0
        e = obs / exp if exp > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"    {cls}@pos2: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")
