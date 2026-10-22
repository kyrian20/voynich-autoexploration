"""
exp_560: sch-onset full characterization (H_new_FW)
sch was discovered as A pos1 CONF (3.91x/15, F599) in exp_557.
Parts:
1. Vocabulary (top-20 sch words, A and B)
2. Positional distribution (pos1/MID/LL/LF vs baseline, both dialects)
3. sch within-line bigrams (sch→X outgoing; X→sch incoming)
4. sch-LF pos1 profile
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

# --- Part 1: sch vocabulary ---
print("\n=== PART 1: sch vocabulary ===")

def vocab_stats(lines, label):
    all_words = [w for fo, ws in lines for w in ws]
    total = len(all_words)
    sch_words = [w for w in all_words if get_onset(w) == 'sch']
    print(f"\n{label}: {len(sch_words)} sch tokens ({100*len(sch_words)/total:.2f}% of {total} words)")
    if len(sch_words) == 0:
        print(f"  No sch words found.")
        return
    wc = Counter(sch_words)
    print(f"  Unique sch types: {len(wc)}")
    print(f"  Top-20 sch words:")
    for w, c in wc.most_common(20):
        print(f"    {w}: {c} ({100*c/len(sch_words):.1f}%)")

vocab_stats(lines_A, "A herbal_a")
vocab_stats(lines_B, "B all")

# --- Part 2: sch positional distribution ---
print("\n=== PART 2: sch positional distribution ===")

def positional_stats(lines, label):
    pos_counts = {'pos1': 0, 'MID': 0, 'LL': 0, 'LF': 0}
    total_counts = {'pos1': 0, 'MID': 0, 'LL': 0, 'LF': 0}

    for fo, ws in lines:
        L = len(ws)
        if L < 1: continue

        onsets = [get_onset(w) for w in ws]

        if L == 1:
            total_counts['pos1'] += 1
            total_counts['LF'] += 1  # single-word: same word at both positions (overlap)
            if onsets[0] == 'sch':
                pos_counts['pos1'] += 1
        else:
            # pos1
            total_counts['pos1'] += 1
            if onsets[0] == 'sch': pos_counts['pos1'] += 1
            # LF
            total_counts['LF'] += 1
            if onsets[-1] == 'sch': pos_counts['LF'] += 1

            if L >= 2:
                # LL (penultimate)
                total_counts['LL'] += 1
                if onsets[-2] == 'sch': pos_counts['LL'] += 1

            # MID (positions 1 to L-2 inclusive)
            for i in range(1, L-1):
                total_counts['MID'] += 1
                if onsets[i] == 'sch': pos_counts['MID'] += 1

    # MID baseline
    mid_total = total_counts['MID']
    mid_sch = pos_counts['MID']
    mid_rate = mid_sch / mid_total if mid_total > 0 else 0

    print(f"\n{label}:")
    print(f"  MID baseline: {mid_sch}/{mid_total} = {mid_rate:.4f}")
    for pos in ['pos1', 'LL', 'LF']:
        obs = pos_counts[pos]
        total = total_counts[pos]
        if total == 0: continue
        exp = mid_rate * total
        e = (obs/total) / mid_rate if mid_rate > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"  {pos}: obs={obs}, total={total}, exp={exp:.1f}, E={e:.2f}× {flag}")

positional_stats(lines_A, "A herbal_a")
positional_stats(lines_B, "B all")

# --- Part 3: sch within-line bigrams ---
print("\n=== PART 3: sch within-line bigrams ===")

def bigram_stats(lines, label):
    # MID baseline
    mid_counts = Counter()
    total_mid = 0
    for fo, ws in lines:
        L = len(ws)
        for i in range(1, L-1):  # MID positions: index 1 to L-2
            mid_counts[get_onset(ws[i])] += 1
            total_mid += 1

    print(f"\n{label} (MID baseline: {total_mid} words)")

    # Outgoing: sch → X (what follows sch?)
    outgoing = Counter()
    n_sch_sender = 0
    for fo, ws in lines:
        for i in range(len(ws) - 1):
            if get_onset(ws[i]) == 'sch':
                outgoing[get_onset(ws[i+1])] += 1
                n_sch_sender += 1

    print(f"  sch-sender bigrams: {n_sch_sender}")
    if n_sch_sender > 0:
        print(f"  Outgoing sch→X (top 10):")
        for cls, obs in outgoing.most_common(10):
            exp = (mid_counts[cls] / total_mid) * n_sch_sender if total_mid > 0 else 0
            e = obs / exp if exp > 0 else float('inf')
            flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
            print(f"    sch→{cls}: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")

    # Incoming: X → sch (what precedes sch?)
    incoming = Counter()
    n_sch_receiver = 0
    for fo, ws in lines:
        for i in range(1, len(ws)):
            if get_onset(ws[i]) == 'sch':
                incoming[get_onset(ws[i-1])] += 1
                n_sch_receiver += 1

    # Sender baseline: overall onset distribution (for incoming bigrams)
    overall_counts = Counter()
    total_overall = 0
    for fo, ws in lines:
        for w in ws:
            overall_counts[get_onset(w)] += 1
            total_overall += 1

    sch_rate_overall = overall_counts['sch'] / total_overall if total_overall > 0 else 0

    print(f"  sch-receiver bigrams: {n_sch_receiver}")
    if n_sch_receiver > 0:
        print(f"  Incoming X→sch (top 10):")
        for cls, obs in incoming.most_common(10):
            # Expected: sender_rate(cls) * n_sch_receiver... but should use MID baseline for receiver context
            # Use: how many sch words are at MID/LL/LF (not pos1) — any of these can have a predecessor
            # Simplest: use overall sender rate × number of sch words with predecessors
            exp = (overall_counts[cls] / total_overall) * n_sch_receiver if total_overall > 0 else 0
            e = obs / exp if exp > 0 else float('inf')
            flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
            print(f"    {cls}→sch: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")

bigram_stats(lines_A, "A herbal_a")
bigram_stats(lines_B, "B all")

# --- Part 4: sch-LF pos1 profile ---
print("\n=== PART 4: sch-LF pos1 profile ===")

def lf_pos1_profile(lines, label):
    sch_lf_lines = [(fo, ws) for fo, ws in lines if len(ws) >= 2 and get_onset(ws[-1]) == 'sch']
    print(f"\n{label}: sch-LF lines: {len(sch_lf_lines)}")
    if len(sch_lf_lines) < 3:
        print(f"  Underpowered (N<3); no analysis.")
        return

    pos1_counts = Counter()
    for fo, ws in sch_lf_lines:
        pos1_counts[get_onset(ws[0])] += 1

    # Baseline: A pos1 distribution from all multi-word lines
    all_multiword = [(fo, ws) for fo, ws in lines if len(ws) >= 2]
    baseline_pos1 = Counter()
    for fo, ws in all_multiword:
        baseline_pos1[get_onset(ws[0])] += 1
    total_base = sum(baseline_pos1.values())

    total_sch_lf = sum(pos1_counts.values())
    print(f"  Total sch-LF lines with opener: {total_sch_lf}")
    print(f"  Pos1 distribution for sch-LF lines:")
    for cls, obs in pos1_counts.most_common(10):
        base_rate = baseline_pos1[cls] / total_base if total_base > 0 else 0
        obs_rate = obs / total_sch_lf
        e = obs_rate / base_rate if base_rate > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
        print(f"    {cls}@pos1: obs={obs} (rate={obs_rate:.3f} vs base={base_rate:.3f} → E={e:.2f}×) {flag}")

lf_pos1_profile(lines_A, "A herbal_a")
lf_pos1_profile(lines_B, "B all")

print("\n=== SUMMARY ===")
# Quick totals
all_A_words = [w for fo, ws in lines_A for w in ws]
all_B_words = [w for fo, ws in lines_B for w in ws]
sch_A = [w for w in all_A_words if get_onset(w) == 'sch']
sch_B = [w for w in all_B_words if get_onset(w) == 'sch']
print(f"A sch tokens: {len(sch_A)} ({100*len(sch_A)/len(all_A_words):.2f}% of {len(all_A_words)})")
print(f"B sch tokens: {len(sch_B)} ({100*len(sch_B)/len(all_B_words):.2f}% of {len(all_B_words)})")
