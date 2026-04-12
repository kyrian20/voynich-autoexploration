#!/usr/bin/env python3
"""
exp_497: B herbal pos2 Full Survey
H_new_BX: Does B herbal have confirmed pos2 routing rules beyond F457/F458 (ch→ch, d→sh)?
"""

import re
from collections import defaultdict

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_PRIORITY = ['qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol',
                  'sch','skh','sph','d','s','y','k','t','l','r','p','f','o','e','a','n','m']

def get_onset(word):
    for o in ONSET_PRIORITY:
        if word.startswith(o):
            return o
    return word[0] if word else ''

def folio_num(folio):
    m = re.match(r'f(\d+)', folio)
    return int(m.group(1)) if m else 999

def is_b_dialect(words):
    return sum(1 for w in words if w.endswith('edy') or w.endswith('eedy')) / max(len(words),1) >= 0.05

def get_section_b(folio):
    n = folio_num(folio)
    if n <= 72: return 'herbal'
    if n <= 84: return 'astro'
    if n <= 102: return 'cosmo'
    if n <= 116: return 'pharma'
    if n <= 170: return 'bio'
    return 'text'

# Parse corpus
folios = defaultdict(list)
with open(ZL3B) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)', line)
        if not m:
            continue
        folio_raw, _, locus, text = m.group(1), m.group(2), m.group(3), m.group(4)
        folio = folio_raw.lstrip('+*=&~')
        lc = locus.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        words = [w for w in re.split(r'[-.\s]', text)
                 if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if words:
            folios[folio].append(words)

sections = defaultdict(list)
for folio, lines in folios.items():
    all_words = [w for line in lines for w in line]
    if is_b_dialect(all_words):
        sec = 'B_' + get_section_b(folio)
        for line in lines:
            sections[sec].append((folio, line))

b_herbal = sections['B_herbal']
print(f"B herbal lines: {len(b_herbal)}")

def flag_cell(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONFIRMED'
    if obs >= 5  and E >= 2.0: return 'dir'
    if obs >= 3  and E >= 2.0: return '(dir)'
    if obs == 0: return 'zero'
    return ''

# B herbal pos2 baseline (lines with len>=3, so pos2 != LF)
pos2_total = 0
pos2_counts = defaultdict(int)
for folio, words in b_herbal:
    if len(words) >= 3:
        o = get_onset(words[1])
        if o:
            pos2_counts[o] += 1
            pos2_total += 1

print(f"\nB herbal pos2 baseline (N={pos2_total}, lines with len>=3):")
pos2_base = {}
for o in ONSET_PRIORITY:
    c = pos2_counts[o]
    if c > 0:
        pct = c / pos2_total * 100
        pos2_base[o] = c / pos2_total
        if pct >= 1.0:
            print(f"  {o}: {c} ({pct:.1f}%)")

# B herbal LF distribution
lf_counts = defaultdict(int)
for folio, words in b_herbal:
    o = get_onset(words[-1])
    if o:
        lf_counts[o] += 1
lf_total = sum(lf_counts.values())

print(f"\nB herbal LF distribution (N={lf_total}):")
for o in sorted(lf_counts, key=lambda x: -lf_counts[x])[:12]:
    pct = lf_counts[o] / lf_total * 100
    print(f"  {o}: {lf_counts[o]} ({pct:.1f}%)")

# pos2 routing for each major LF class
MIN_LF = 8
print(f"\n=== B herbal pos2 routing (min LF N={MIN_LF}) ===")
print(f"Thresholds: CONFIRMED=E>=1.5x,N>=10; dir=E>=2.0x,N>=5; (dir)=E>=2.0x,N>=3")
print(f"Known confirmed: d-LF→sh@pos2(E=1.73×/N=10,F457), ch-LF→ch@pos2(E=1.74×/N=19,F458)")

major_lf = [(o, lf_counts[o]) for o in ONSET_PRIORITY if lf_counts[o] >= MIN_LF]

for lf_onset, lf_n in major_lf:
    lf_lines = [(fo, ws) for fo, ws in b_herbal if get_onset(ws[-1]) == lf_onset]
    # pos2 eligible: lines with len>=3 (pos2 different from both pos1 and LF)
    elig = [(fo, ws) for fo, ws in lf_lines if len(ws) >= 3]
    n_elig = len(elig)

    pos2_dist = defaultdict(int)
    for fo, ws in elig:
        o = get_onset(ws[1])
        if o:
            pos2_dist[o] += 1

    print(f"\n{lf_onset}-LF (N_lf={lf_n}, N_elig={n_elig}):")

    rows = []
    for o in ONSET_PRIORITY:
        obs = pos2_dist[o]
        base_rate = pos2_base.get(o, 0)
        if base_rate == 0 and obs == 0:
            continue
        expected = base_rate * n_elig if base_rate > 0 else 0
        E = obs / expected if expected > 0 else float('inf') if obs > 0 else 0
        rows.append((o, obs, expected, E))

    rows.sort(key=lambda x: (-x[3] if x[3] != float('inf') else 1e9))
    for o, obs, exp, E in rows[:7]:
        flag = flag_cell(obs, E) if E != float('inf') else '(uniq)'
        base_pct = pos2_base.get(o, 0) * 100
        E_str = f"{E:.2f}x" if E != float('inf') else "inf"
        print(f"  {o:8s}: obs={obs:3d}, exp={exp:.1f} (base={base_pct:.1f}%), E={E_str}  {flag}")

    # Self-chain E explicitly if not in top 7
    top7 = [r[0] for r in rows[:7]]
    if lf_onset not in top7:
        self_obs = pos2_dist.get(lf_onset, 0)
        self_base = pos2_base.get(lf_onset, 0)
        self_exp = self_base * n_elig if self_base > 0 else 0
        self_E = self_obs / self_exp if self_exp > 0 else 0
        flag = flag_cell(self_obs, self_E)
        print(f"  [{lf_onset}-self]: obs={self_obs}, exp={self_exp:.1f}, E={self_E:.2f}x  {flag}")

print("\n=== Comparison with A herbal_a pos2 self-chaining (F468) ===")
print("A herbal_a: ALL LF classes self-chain at pos2 (universal, F468)")
print("B herbal confirmed: ch→ch@pos2(F458,E=1.74×/N=19), d→sh@pos2(F457,E=1.73×/N=10)")
print("Checking B herbal self-chain rates for all major classes:")

for lf_onset, lf_n in major_lf:
    lf_lines = [(fo, ws) for fo, ws in b_herbal if get_onset(ws[-1]) == lf_onset]
    elig = [(fo, ws) for fo, ws in lf_lines if len(ws) >= 3]
    n_elig = len(elig)
    self_obs = sum(1 for fo, ws in elig if get_onset(ws[1]) == lf_onset)
    self_base = pos2_base.get(lf_onset, 0)
    self_exp = self_base * n_elig if self_base > 0 else 0
    self_E = self_obs / self_exp if self_exp > 0 else 0
    flag = flag_cell(self_obs, self_E)
    print(f"  {lf_onset:8s}: self@pos2 = {self_obs}/{n_elig}, E={self_E:.2f}x (base={self_base*100:.1f}%)  {flag}")
