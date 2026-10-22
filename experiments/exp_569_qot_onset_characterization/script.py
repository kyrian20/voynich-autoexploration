"""
exp_569: qot-onset full characterization (H_new_GG)
qot = words starting with "qot" (highest priority in ONSET_PRIORITY after qok)
4-part methodology: (1) vocabulary; (2) positional; (3) bigrams; (4) qot-LF pos1 profile
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
all_A_words = [w for fo, ws in lines_A for w in ws]
all_B_words = [w for fo, ws in lines_B for w in ws]

print(f"A herbal_a: {len(lines_A)} lines; B all: {len(lines_B)} lines")
print(f"A total words: {len(all_A_words)}; B total words: {len(all_B_words)}")

# ── PART 1: VOCABULARY ──────────────────────────────────────────────────────
print("\n=== PART 1: VOCABULARY ===")
for words, label in [(all_A_words, "A herbal_a"), (all_B_words, "B all")]:
    total = len(words)
    qot_words = [w for w in words if get_onset(w) == 'qot']
    wc = Counter(qot_words)
    print(f"\n{label}: {len(qot_words)} qot tokens ({100*len(qot_words)/total:.2f}%); {len(wc)} types")
    print(f"  Top-15: {', '.join(f'{w}:{c}({100*c/len(qot_words):.1f}%)' for w,c in wc.most_common(15))}")

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
                if onset == 'qot': pos1_c += 1
            elif i == L - 1:
                total_lf += 1
                if onset == 'qot': lf_c += 1
            elif L >= 3 and i == L - 2:
                total_ll += 1
                if onset == 'qot': ll_c += 1
            else:
                total_mid += 1
                if onset == 'qot': mid_c += 1
    total_words = total_pos1 + total_mid + total_ll + total_lf
    qot_total = pos1_c + mid_c + ll_c + lf_c
    baseline = qot_total / total_words
    print(f"\n{label}: qot baseline={100*baseline:.2f}%")
    for slot, cnt, tot in [('pos1', pos1_c, total_pos1), ('MID', mid_c, total_mid),
                            ('LL', ll_c, total_ll), ('LF', lf_c, total_lf)]:
        exp = baseline * tot
        e = cnt/exp if exp > 0 else 0
        flag = 'CONF' if e>=1.5 and cnt>=10 else 'dir' if e>=2.0 and cnt>=5 else '(dir)' if e>=2.5 and cnt>=3 else 'DEPL' if e<0.7 and cnt>=3 else ''
        print(f"  {slot}: obs={cnt}, expected={exp:.1f}, E={e:.2f}× {flag}")

# ── PART 3: BIGRAMS ──────────────────────────────────────────────────────────
print("\n=== PART 3: BIGRAMS (MID-baseline outgoing; overall-baseline incoming) ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    words_all = [w for fo, ws in lines for w in ws]
    total = len(words_all)
    onset_counts = Counter(get_onset(w) for w in words_all)

    mid_tokens = []
    for fo, ws in lines:
        L = len(ws)
        for i, w in enumerate(ws):
            if i > 0 and i < L-1:
                mid_tokens.append(w)
    mid_total = len(mid_tokens)
    mid_onset = Counter(get_onset(w) for w in mid_tokens)

    bigrams = []
    for fo, ws in lines:
        L = len(ws)
        for i in range(L-1):
            bigrams.append((get_onset(ws[i]), get_onset(ws[i+1])))

    # Outgoing from qot (MID baseline)
    qot_sender_bigrams = [(a, b) for a, b in bigrams if a == 'qot']
    qot_sender_total = len(qot_sender_bigrams)
    qot_receiver_counts = Counter(b for a, b in qot_sender_bigrams)
    qot_mid_freq = mid_onset.get('qot', 0) / mid_total if mid_total > 0 else 0

    print(f"\n{label} — Outgoing from qot (MID-baseline; qot_sender={qot_sender_total})")
    print(f"  (qot MID baseline={100*qot_mid_freq:.2f}%)")
    for target, cnt in sorted(qot_receiver_counts.items(), key=lambda x: -x[1]):
        if cnt < 2: continue
        target_freq = onset_counts.get(target, 0) / total
        exp = qot_sender_total * target_freq
        e = cnt/exp if exp > 0 else 0
        flag = 'CONF' if e>=1.5 and cnt>=10 else 'dir' if e>=2.0 and cnt>=5 else '(dir)' if e>=2.5 and cnt>=3 else 'DEPL' if e<0.7 and cnt>=3 else ''
        print(f"    qot→{target}: obs={cnt}, exp={exp:.1f}, E={e:.2f}× {flag}")

    # Incoming to qot (overall baseline)
    qot_recv_bigrams = [(a, b) for a, b in bigrams if b == 'qot']
    qot_recv_total = len(qot_recv_bigrams)
    qot_sender_counts = Counter(a for a, b in qot_recv_bigrams)

    print(f"\n{label} — Incoming to qot (overall-baseline; qot_receiver={qot_recv_total})")
    for sender, cnt in sorted(qot_sender_counts.items(), key=lambda x: -x[1]):
        if cnt < 2: continue
        sender_freq = onset_counts.get(sender, 0) / total
        exp = qot_recv_total * sender_freq
        e = cnt/exp if exp > 0 else 0
        flag = 'CONF' if e>=1.5 and cnt>=10 else 'dir' if e>=2.0 and cnt>=5 else '(dir)' if e>=2.5 and cnt>=3 else 'DEPL' if e<0.7 and cnt>=3 else ''
        print(f"    {sender}→qot: obs={cnt}, exp={exp:.1f}, E={e:.2f}× {flag}")

    # Self-succession
    ss = sum(1 for a, b in bigrams if a == 'qot' and b == 'qot')
    total_bigrams = len(bigrams)
    qot_freq = onset_counts.get('qot', 0) / total
    ss_exp = total_bigrams * qot_freq * qot_freq
    print(f"\n  {label} qot self-succession: obs={ss}, exp={ss_exp:.1f}, E={ss/ss_exp:.2f}×")

# ── PART 4: qot-LF POS1 PROFILE ─────────────────────────────────────────────
print("\n=== PART 4: qot-LF POS1 PROFILE ===")
for lines, label in [(lines_A, "A herbal_a"), (lines_B, "B all")]:
    words_all = [w for fo, ws in lines for w in ws]
    total = len(words_all)
    onset_counts = Counter(get_onset(w) for w in words_all)
    total_lines = len(lines)

    qot_lf_lines = [(fo, ws) for fo, ws in lines if get_onset(ws[-1]) == 'qot']
    N_qot_lf = len(qot_lf_lines)
    print(f"\n{label}: {N_qot_lf} qot-LF lines (out of {total_lines})")

    pos1_onsets = Counter(get_onset(ws[0]) for fo, ws in qot_lf_lines if len(ws) >= 1)
    all_pos1_onsets = Counter(get_onset(ws[0]) for fo, ws in lines)
    total_pos1 = sum(all_pos1_onsets.values())

    for onset, cnt in sorted(pos1_onsets.items(), key=lambda x: -x[1]):
        if cnt < 2: continue
        baseline_frac = all_pos1_onsets.get(onset, 0) / total_pos1
        exp = N_qot_lf * baseline_frac
        e = cnt/exp if exp > 0 else 0
        flag = 'CONF' if e>=1.5 and cnt>=10 else 'dir' if e>=2.0 and cnt>=5 else '(dir)' if e>=2.5 and cnt>=3 else 'DEPL' if e<0.7 and cnt>=3 else ''
        print(f"  {onset}@pos1: obs={cnt}, exp={exp:.1f}, E={e:.2f}× {flag}")
