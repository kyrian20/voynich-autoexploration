"""
exp_566: ch-onset full characterization (H_new_GD)
ch = words starting with "ch" (after cth/ckh/cph in ONSET_PRIORITY)
Parts:
1. Vocabulary (top-20 ch words, A and B)
2. Positional distribution (pos1/MID/LL/LF vs baseline)
3. ch within-line bigrams (outgoing and incoming)
4. ch-LF pos1 profile
5. ch-pos1 line structure (lines opened by ch — underpowered expected)
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter

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
print("\n=== PART 1: ch vocabulary ===")
for words, label in [(all_A_words, "A herbal_a"), (all_B_words, "B all")]:
    total = len(words)
    ch_words = [w for w in words if get_onset(w) == 'ch']
    print(f"\n{label}: {len(ch_words)} ch tokens ({100*len(ch_words)/total:.2f}% of {total})")
    wc = Counter(ch_words)
    print(f"  Unique types: {len(wc)}")
    print(f"  Top-20:")
    for w, c in wc.most_common(20):
        print(f"    {w}: {c} ({100*c/len(ch_words):.1f}%)")

# --- Part 2: Positional distribution ---
print("\n=== PART 2: ch positional distribution ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    pos_counts = {'pos1': 0, 'MID': 0, 'LL': 0, 'LF': 0}
    total_counts = {'pos1': 0, 'MID': 0, 'LL': 0, 'LF': 0}

    for fo, ws in lines:
        L = len(ws)
        if L < 1: continue
        onsets = [get_onset(w) for w in ws]

        total_counts['pos1'] += 1
        if onsets[0] == 'ch': pos_counts['pos1'] += 1

        if L >= 2:
            total_counts['LF'] += 1
            if onsets[-1] == 'ch': pos_counts['LF'] += 1
            total_counts['LL'] += 1
            if onsets[-2] == 'ch': pos_counts['LL'] += 1

        for i in range(1, L-1):
            total_counts['MID'] += 1
            if onsets[i] == 'ch': pos_counts['MID'] += 1

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
print("\n=== PART 3: ch bigrams ===")
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
            if get_onset(ws[i]) == 'ch':
                outgoing[get_onset(ws[i+1])] += 1
                n_sender += 1

    incoming = Counter()
    n_receiver = 0
    for fo, ws in lines:
        for i in range(1, len(ws)):
            if get_onset(ws[i]) == 'ch':
                incoming[get_onset(ws[i-1])] += 1
                n_receiver += 1

    overall = Counter(get_onset(w) for w in all_words)
    total_overall = len(all_words)

    print(f"\n{label} (sender={n_sender}, receiver={n_receiver}, MID_baseline={total_mid}):")
    print(f"  Outgoing ch→X (top 15):")
    for cls, obs in outgoing.most_common(15):
        exp = (mid_counts[cls] / total_mid) * n_sender if total_mid > 0 else 0
        e = obs / exp if exp > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"    ch→{cls}: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")

    print(f"  Incoming X→ch (top 15):")
    for cls, obs in incoming.most_common(15):
        exp = (overall[cls] / total_overall) * n_receiver if total_overall > 0 else 0
        e = obs / exp if exp > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"    {cls}→ch: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")

# --- Part 4: ch-LF pos1 profile ---
print("\n=== PART 4: ch-LF pos1 profile ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    ch_lf = [(fo, ws) for fo, ws in lines if len(ws) >= 2 and get_onset(ws[-1]) == 'ch']
    print(f"\n{label}: ch-LF lines: {len(ch_lf)}")
    if len(ch_lf) < 5:
        print(f"  Underpowered.")
        continue

    pos1_counts = Counter()
    for fo, ws in ch_lf:
        pos1_counts[get_onset(ws[0])] += 1

    a_pos1 = Counter()
    for fo, ws in lines:
        if len(ws) >= 2:
            a_pos1[get_onset(ws[0])] += 1
    total_base = sum(a_pos1.values())
    total_ch_lf = sum(pos1_counts.values())

    print(f"  Pos1 distribution (top 12):")
    for cls, obs in pos1_counts.most_common(12):
        base = a_pos1[cls] / total_base if total_base > 0 else 0
        obs_rate = obs / total_ch_lf
        e = obs_rate / base if base > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"    {cls}@pos1: {obs} (E={e:.2f}×) {flag}")

# --- Part 5: ch self-succession and chain analysis ---
print("\n=== PART 5: ch-LF LL class (penultimate before ch-terminal) ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    ch_lf = [(fo, ws) for fo, ws in lines if len(ws) >= 3 and get_onset(ws[-1]) == 'ch']
    print(f"\n{label}: ch-LF lines (len≥3): {len(ch_lf)}")
    if len(ch_lf) < 5:
        print(f"  Underpowered.")
        continue
    ll_counts = Counter()
    for fo, ws in ch_lf:
        ll_counts[get_onset(ws[-2])] += 1
    # baseline: overall LL distribution
    ll_base = Counter()
    for fo, ws in lines:
        if len(ws) >= 3:
            ll_base[get_onset(ws[-2])] += 1
    total_ll_base = sum(ll_base.values())
    total_ch_lf_ll = sum(ll_counts.values())
    print(f"  LL class in ch-LF lines (top 10):")
    for cls, obs in ll_counts.most_common(10):
        base = ll_base[cls] / total_ll_base if total_ll_base > 0 else 0
        obs_rate = obs / total_ch_lf_ll
        e = obs_rate / base if base > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"    {cls}@LL: {obs} (E={e:.2f}×) {flag}")
