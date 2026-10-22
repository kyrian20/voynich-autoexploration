"""
exp_568: ot-onset full characterization (H_new_GF)
ot = words starting with "ot" (after qot in ONSET_PRIORITY)
4-part methodology: (1) vocabulary; (2) positional; (3) bigrams; (4) ot-LF pos1 profile
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
                lines_B.append((folio_raw, words))
            else:
                if n <= 56:
                    lines_A.append((folio_raw, words))
    return lines_A, lines_B

lines_A, lines_B = parse_corpus(CORPUS)
all_A_words = [w for fo, ws in lines_A for w in ws]
all_B_words = [w for fo, ws in lines_B for w in ws]

print(f"A herbal_a: {len(lines_A)} lines; B all: {len(lines_B)} lines")
print(f"A total words: {len(all_A_words)}; B total words: {len(all_B_words)}")

# ── PART 1: VOCABULARY ──────────────────────────────────────────────────────
print("\n=== PART 1: VOCABULARY ===")
for words, label in [(all_A_words, "A herbal_a"), (all_B_words, "B all")]:
    total = len(words)
    ot_words = [w for w in words if get_onset(w) == 'ot']
    wc = Counter(ot_words)
    print(f"\n{label}: {len(ot_words)} ot tokens ({100*len(ot_words)/total:.2f}%); {len(wc)} types")
    print(f"  Top-15: {', '.join(f'{w}:{c}({100*c/len(ot_words):.1f}%)' for w,c in wc.most_common(15))}")

# ── PART 2: POSITIONAL DISTRIBUTION ─────────────────────────────────────────
print("\n=== PART 2: POSITIONAL DISTRIBUTION ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    pos1_c = mid_c = ll_c = lf_c = 0
    total_pos1 = total_mid = total_ll = total_lf = 0
    for fo, ws in lines:
        L = len(ws)
        for i, w in enumerate(ws):
            onset = get_onset(w)
            if i == 0:
                total_pos1 += 1
                if onset == 'ot': pos1_c += 1
            elif i == L - 1:
                total_lf += 1
                if onset == 'ot': lf_c += 1
            elif L >= 3 and i == L - 2:
                total_ll += 1
                if onset == 'ot': ll_c += 1
            else:
                total_mid += 1
                if onset == 'ot': mid_c += 1
    total_words = total_pos1 + total_mid + total_ll + total_lf
    ot_total = pos1_c + mid_c + ll_c + lf_c
    baseline = ot_total / total_words
    print(f"\n{label}: ot baseline={100*baseline:.2f}%")
    for slot, cnt, tot in [('pos1', pos1_c, total_pos1), ('MID', mid_c, total_mid),
                            ('LL', ll_c, total_ll), ('LF', lf_c, total_lf)]:
        exp = baseline * tot
        e = cnt/exp if exp > 0 else 0
        print(f"  {slot}: obs={cnt}, expected={exp:.1f}, E={e:.2f}×")

# ── PART 3: BIGRAMS ──────────────────────────────────────────────────────────
print("\n=== PART 3: BIGRAMS (MID-baseline outgoing; overall-baseline incoming) ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    words_all = [w for fo, ws in lines for w in ws]
    total = len(words_all)
    onset_counts = Counter(get_onset(w) for w in words_all)

    # MID-only tokens for sender baseline
    mid_tokens = []
    for fo, ws in lines:
        L = len(ws)
        for i, w in enumerate(ws):
            if i > 0 and i < L-1:  # MID positions (not pos1, not LF)
                mid_tokens.append(w)
    mid_total = len(mid_tokens)
    mid_onset = Counter(get_onset(w) for w in mid_tokens)

    # Collect bigrams
    bigrams = []
    for fo, ws in lines:
        L = len(ws)
        for i in range(L-1):
            bigrams.append((get_onset(ws[i]), get_onset(ws[i+1])))

    # Outgoing from ot (ot at pos i, using MID baseline for sender)
    ot_sender_bigrams = [(a, b) for a, b in bigrams if a == 'ot']
    ot_sender_total = len(ot_sender_bigrams)
    ot_receiver_counts = Counter(b for a, b in ot_sender_bigrams)
    ot_mid_freq = mid_onset.get('ot', 0) / mid_total if mid_total > 0 else 0

    print(f"\n{label} — Outgoing from ot (MID-baseline; ot_sender={ot_sender_total})")
    print(f"  (ot MID baseline={100*ot_mid_freq:.2f}%)")
    for target, cnt in sorted(ot_receiver_counts.items(), key=lambda x: -x[1]):
        if cnt < 2: continue
        target_freq = onset_counts.get(target, 0) / total
        exp = ot_sender_total * target_freq
        e = cnt/exp if exp > 0 else 0
        flag = 'CONF' if e>=1.5 and cnt>=10 else 'dir' if e>=2.0 and cnt>=5 else '(dir)' if e>=2.5 and cnt>=3 else 'DEPL' if e<0.7 and cnt>=3 else ''
        print(f"    ot→{target}: obs={cnt}, exp={exp:.1f}, E={e:.2f}× {flag}")

    # Incoming to ot (X→ot, using overall baseline for sender)
    ot_recv_bigrams = [(a, b) for a, b in bigrams if b == 'ot']
    ot_recv_total = len(ot_recv_bigrams)
    ot_sender_counts = Counter(a for a, b in ot_recv_bigrams)

    print(f"\n{label} — Incoming to ot (overall-baseline; ot_receiver={ot_recv_total})")
    for sender, cnt in sorted(ot_sender_counts.items(), key=lambda x: -x[1]):
        if cnt < 2: continue
        sender_freq = onset_counts.get(sender, 0) / total
        exp = ot_recv_total * sender_freq
        e = cnt/exp if exp > 0 else 0
        flag = 'CONF' if e>=1.5 and cnt>=10 else 'dir' if e>=2.0 and cnt>=5 else '(dir)' if e>=2.5 and cnt>=3 else 'DEPL' if e<0.7 and cnt>=3 else ''
        print(f"    {sender}→ot: obs={cnt}, exp={exp:.1f}, E={e:.2f}× {flag}")

    # Self-succession
    ss = sum(1 for a, b in bigrams if a == 'ot' and b == 'ot')
    total_bigrams = len(bigrams)
    ot_freq = onset_counts.get('ot', 0) / total
    ss_exp = total_bigrams * ot_freq * ot_freq
    print(f"\n  {label} ot self-succession: obs={ss}, exp={ss_exp:.1f}, E={ss/ss_exp:.2f}×")

# ── PART 4: ot-LF POS1 PROFILE ───────────────────────────────────────────────
print("\n=== PART 4: ot-LF POS1 PROFILE ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    words_all = [w for fo, ws in lines for w in ws]
    total = len(words_all)
    onset_counts = Counter(get_onset(w) for w in words_all)
    total_lines = len(lines)

    ot_lf_lines = [(fo, ws) for fo, ws in lines if get_onset(ws[-1]) == 'ot']
    N_ot_lf = len(ot_lf_lines)
    print(f"\n{label}: {N_ot_lf} ot-LF lines (out of {total_lines})")

    pos1_onsets = Counter(get_onset(ws[0]) for fo, ws in ot_lf_lines if len(ws) >= 1)
    all_pos1_onsets = Counter(get_onset(ws[0]) for fo, ws in lines)
    total_pos1 = sum(all_pos1_onsets.values())

    for onset, cnt in sorted(pos1_onsets.items(), key=lambda x: -x[1]):
        if cnt < 2: continue
        baseline_frac = all_pos1_onsets.get(onset, 0) / total_pos1
        exp = N_ot_lf * baseline_frac
        e = cnt/exp if exp > 0 else 0
        flag = 'CONF' if e>=1.5 and cnt>=10 else 'dir' if e>=2.0 and cnt>=5 else '(dir)' if e>=2.5 and cnt>=3 else 'DEPL' if e<0.7 and cnt>=3 else ''
        print(f"  {onset}@pos1: obs={cnt}, exp={exp:.1f}, E={e:.2f}× {flag}")
