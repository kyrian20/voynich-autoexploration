#!/usr/bin/env python3
"""
exp_491: A herbal_a pos1 Self-Chaining Survey
H_new_BP: Is pos1 self-chaining universal (like pos2) or partial in A herbal_a?
Compare pos1 vs pos2 self-chaining for each LF class.
Also test pos1 cross-class routing vs self-chaining coexistence.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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

def get_section_a(folio):
    n = folio_num(folio)
    if n <= 56: return 'herbal_a'
    if n <= 72: return 'stars'
    if n <= 84: return 'herbal_b'
    if n <= 102: return 'cosmo'
    return 'other'

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
    else:
        sec = 'A_' + get_section_a(folio)
        for line in lines:
            sections[sec].append((folio, line))

def flag_cell(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONFIRMED'
    if obs >= 5  and E >= 2.0: return 'dir'
    if obs >= 3  and E >= 2.0: return '(dir)'
    return ''

a_herbal = sections['A_herbal_a']
all_ws_a = [ws for _, ws in a_herbal]

# pos1 and pos2 baselines
p1_base = defaultdict(int); n_p1 = 0
p2_base = defaultdict(int); n_p2 = 0
for ws in all_ws_a:
    if len(ws) >= 1:
        p1_base[get_onset(ws[0])] += 1; n_p1 += 1
    if len(ws) >= 2:
        p2_base[get_onset(ws[1])] += 1; n_p2 += 1

print("A herbal_a pos1 baseline (top 10):")
for o, n in sorted(p1_base.items(), key=lambda x: -x[1])[:10]:
    print(f"  {o:<6}: {n/n_p1:.3f} ({n/n_p1*100:.1f}%)")
print()
print("A herbal_a pos2 baseline (top 10):")
for o, n in sorted(p2_base.items(), key=lambda x: -x[1])[:10]:
    print(f"  {o:<6}: {n/n_p2:.3f} ({n/n_p2*100:.1f}%)")
print()

# LF distribution
lf_dist = defaultdict(int)
for _, ws in a_herbal:
    if ws:
        lf_dist[get_onset(ws[-1])] += 1

print("="*70)
print("A herbal_a pos1 vs pos2 self-chaining comparison")
print("="*70)
print(f"{'LF onset':<8} {'N_lf':>5} | {'pos1':>13} | {'pos2':>13} | {'pos1 vs pos2'}")
print(f"{'':>8} {'':>5} | {'obs E flag':>13} | {'obs E flag':>13}")
print("-"*70)

for lf_onset in sorted(lf_dist.keys(), key=lambda x: -lf_dist[x]):
    N_lf = lf_dist[lf_onset]
    if N_lf < 10:
        continue
    lf_lines = [(f, ws) for f, ws in a_herbal
                if ws and get_onset(ws[-1]) == lf_onset]

    # pos1 self-chaining
    elig1 = [(f, ws) for f, ws in lf_lines if len(ws) >= 1]
    obs1 = sum(1 for _, ws in elig1 if get_onset(ws[0]) == lf_onset)
    base1 = p1_base.get(lf_onset, 0) / n_p1 if n_p1 > 0 else 0
    E1 = obs1 / (base1 * len(elig1)) if base1 * len(elig1) > 0 else float('inf')
    flg1 = flag_cell(obs1, E1)

    # pos2 self-chaining
    elig2 = [(f, ws) for f, ws in lf_lines if len(ws) >= 2]
    obs2 = sum(1 for _, ws in elig2 if get_onset(ws[1]) == lf_onset)
    base2 = p2_base.get(lf_onset, 0) / n_p2 if n_p2 > 0 else 0
    E2 = obs2 / (base2 * len(elig2)) if base2 * len(elig2) > 0 else float('inf')
    flg2 = flag_cell(obs2, E2)

    # Comparison
    if flg2 in ('CONFIRMED', 'dir') and flg1 == '':
        compare = 'pos2>pos1'
    elif flg1 in ('CONFIRMED', 'dir') and flg2 == '':
        compare = 'pos1>pos2'
    elif flg1 in ('CONFIRMED', 'dir') and flg2 in ('CONFIRMED', 'dir'):
        compare = 'BOTH'
    elif flg1 == '' and flg2 == '':
        compare = 'neither'
    else:
        compare = '—'

    p1_str = f"{obs1}/{len(elig1)} {E1:.2f}× {flg1}"
    p2_str = f"{obs2}/{len(elig2)} {E2:.2f}× {flg2}"
    print(f"  {lf_onset:<8} {N_lf:>5} | {p1_str:>13} | {p2_str:>13} | {compare}")

print()
print("="*70)
print("Full pos1 distribution for each LF class")
print("="*70)

for lf_onset in sorted(lf_dist.keys(), key=lambda x: -lf_dist[x]):
    N_lf = lf_dist[lf_onset]
    if N_lf < 10:
        continue
    lf_lines = [(f, ws) for f, ws in a_herbal
                if ws and get_onset(ws[-1]) == lf_onset]
    elig1 = [(f, ws) for f, ws in lf_lines if len(ws) >= 1]
    N_elig = len(elig1)

    obs_by = defaultdict(int)
    for _, ws in elig1:
        obs_by[get_onset(ws[0])] += 1

    rows = []
    for onset, obs in sorted(obs_by.items(), key=lambda x: -x[1]):
        if obs < 2: continue
        base = p1_base.get(onset, 0) / n_p1
        exp = base * N_elig
        E = obs / exp if exp > 0 else float('inf')
        flg = flag_cell(obs, E)
        rows.append((onset, obs, N_elig, base, E, flg))
    rows.sort(key=lambda x: -x[4])

    self_obs = obs_by.get(lf_onset, 0)
    self_base = p1_base.get(lf_onset, 0) / n_p1
    self_E = self_obs / (self_base * N_elig) if self_base * N_elig > 0 else float('inf')
    self_flg = flag_cell(self_obs, self_E)

    print(f"\n  {lf_onset}-LF pos1 (N_elig={N_elig}):")
    print(f"  SELF: {lf_onset} obs={self_obs}/{N_elig} ({self_obs/N_elig*100:.1f}%) E={self_E:.2f}× {self_flg}")
    for onset, obs, n, base, E, flg in rows[:5]:
        marker = ' <-- SELF' if onset == lf_onset else ''
        print(f"    {onset:<6} obs={obs:>3}/{n} ({obs/n*100:.1f}%) base={base*100:.1f}% E={E:>5.2f}× {flg}{marker}")
