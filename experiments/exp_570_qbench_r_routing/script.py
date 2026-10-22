"""
exp_570: B q-bench → r routing universality (H_new_GH)
Test whether qo→r joins qok→r CONF (F620) and qot→r CONF (F632) as a universal q-bench routing rule in B.
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
all_B_words = [w for fo, ws in lines_B for w in ws]
total_B = len(all_B_words)
onset_counts_B = Counter(get_onset(w) for w in all_B_words)

print(f"B all: {len(lines_B)} lines, {total_B} words")

# Collect all bigrams in B
bigrams_B = []
for fo, ws in lines_B:
    for i in range(len(ws)-1):
        bigrams_B.append((get_onset(ws[i]), get_onset(ws[i+1])))

total_bigrams = len(bigrams_B)

# Q-bench classes
q_bench = ['qok', 'qot', 'qo']
# Terminal targets for comparison
targets = ['r', 'l', 'ol', 'o', 'a']

print("\n=== B q-bench → terminal routing ===")
print(f"\n{'Class':6} | {'→r':20} | {'→l':20} | {'→ol':20} | {'→o':20} | {'→a':20}")
print("-" * 110)

for sender in q_bench:
    sender_bigrams = [(a, b) for a, b in bigrams_B if a == sender]
    sender_total = len(sender_bigrams)
    if sender_total == 0:
        print(f"{sender:6} | no bigrams")
        continue
    
    row = f"{sender:6}"
    for target in targets:
        cnt = sum(1 for a, b in sender_bigrams if b == target)
        target_freq = onset_counts_B.get(target, 0) / total_B
        exp = sender_total * target_freq
        e = cnt/exp if exp > 0 else 0
        flag = 'CONF' if e>=1.5 and cnt>=10 else 'dir' if e>=2.0 and cnt>=5 else '(dir)' if e>=2.5 and cnt>=3 else 'DEPL' if e<0.7 and cnt>=3 else '-'
        row += f" | {cnt}/{exp:.1f}={e:.2f}×{flag:5}"
    print(row)
    print(f"       (sender_total={sender_total})")

# Combined q-bench → r
print("\n=== COMBINED q-bench → r ===")
combined_bigrams = [(a, b) for a, b in bigrams_B if a in q_bench]
combined_total = len(combined_bigrams)
combined_r = sum(1 for a, b in combined_bigrams if b == 'r')
r_freq = onset_counts_B.get('r', 0) / total_B
combined_exp = combined_total * r_freq
combined_e = combined_r / combined_exp if combined_exp > 0 else 0
flag = 'CONF' if combined_e>=1.5 and combined_r>=10 else 'dir' if combined_e>=2.0 and combined_r>=5 else ''
print(f"All q-bench → r: obs={combined_r}, exp={combined_exp:.1f}, E={combined_e:.2f}× {flag} (combined_total={combined_total})")

# Compare to non-q-bench → r
non_q_bigrams = [(a, b) for a, b in bigrams_B if a not in q_bench]
non_q_r = sum(1 for a, b in non_q_bigrams if b == 'r')
non_q_total = len(non_q_bigrams)
non_q_exp = non_q_total * r_freq
non_q_e = non_q_r / non_q_exp if non_q_exp > 0 else 0
print(f"Non-q-bench → r: obs={non_q_r}, exp={non_q_exp:.1f}, E={non_q_e:.2f}×")

# Per-class summary with full breakdown
print("\n=== FULL q-bench outgoing profile in B ===")
for sender in q_bench:
    sender_bigrams = [(a, b) for a, b in bigrams_B if a == sender]
    sender_total = len(sender_bigrams)
    target_counts = Counter(b for a, b in sender_bigrams)
    print(f"\n{sender} (sender_total={sender_total}):")
    for target, cnt in sorted(target_counts.items(), key=lambda x: -x[1]):
        if cnt < 2: continue
        target_freq = onset_counts_B.get(target, 0) / total_B
        exp = sender_total * target_freq
        e = cnt/exp if exp > 0 else 0
        flag = 'CONF' if e>=1.5 and cnt>=10 else 'dir' if e>=2.0 and cnt>=5 else '(dir)' if e>=2.5 and cnt>=3 else 'DEPL' if e<0.7 and cnt>=3 else ''
        print(f"  {sender}→{target}: obs={cnt}, exp={exp:.1f}, E={e:.2f}× {flag}")
