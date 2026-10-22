#!/usr/bin/env python3
"""
exp_496: Combined Herbal pos1 Grammar — Cross-Dialectal Confirmation for ot-LF→y?
H_new_BZ: Pool A herbal_a + B herbal ot-LF and ok-LF to test cross-dialectal confirmation.
Also: B astro pos1 grammar survey (H_new_BY, opportunistic).
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

a_herbal = sections['A_herbal_a']
b_herbal = sections['B_herbal']
b_astro = sections['B_astro']

print(f"A herbal_a: {len(a_herbal)} lines")
print(f"B herbal: {len(b_herbal)} lines")
print(f"B astro: {len(b_astro)} lines")

def flag_cell(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONFIRMED'
    if obs >= 5  and E >= 2.0: return 'dir'
    if obs >= 3  and E >= 2.0: return '(dir)'
    if obs == 0: return 'zero'
    return ''

def pos1_survey(section_lines, lf_onset, label, pos1_base):
    lf_lines = [(fo, ws) for fo, ws in section_lines if get_onset(ws[-1]) == lf_onset]
    elig = [(fo, ws) for fo, ws in lf_lines if len(ws) >= 2]
    n_elig = len(elig)
    pos1_dist = defaultdict(int)
    for fo, ws in elig:
        o = get_onset(ws[0])
        if o:
            pos1_dist[o] += 1
    return lf_lines, elig, n_elig, pos1_dist

# ==== PART 1: Combined herbal ot-LF and ok-LF ====

print("\n\n=== PART 1: Combined Herbal pos1 Grammar ===")
print("Combining A herbal_a + B herbal for ot-LF and ok-LF to test herbal-register rules")

# Combined herbal pos1 baseline
combined_herbal = a_herbal + b_herbal
pos1_total_comb = 0
pos1_counts_comb = defaultdict(int)
for folio, words in combined_herbal:
    o = get_onset(words[0])
    if o:
        pos1_counts_comb[o] += 1
        pos1_total_comb += 1

pos1_base_comb = {o: c/pos1_total_comb for o, c in pos1_counts_comb.items()}
print(f"\nCombined herbal pos1 baseline (N={pos1_total_comb}):")
for o in ONSET_PRIORITY:
    c = pos1_counts_comb.get(o, 0)
    if c > 0:
        pct = c/pos1_total_comb*100
        if pct >= 1.0:
            print(f"  {o}: {c} ({pct:.1f}%)")

for lf_onset in ['ot', 'ok']:
    # A herbal_a only
    ah_lf, ah_elig, ah_n_elig, ah_pos1 = pos1_survey(a_herbal, lf_onset, 'A_herbal_a', pos1_base_comb)
    # B herbal only
    bh_lf, bh_elig, bh_n_elig, bh_pos1 = pos1_survey(b_herbal, lf_onset, 'B_herbal', pos1_base_comb)
    # Combined
    comb_lf = ah_lf + bh_lf
    comb_elig = ah_elig + bh_elig
    comb_n_elig = ah_n_elig + bh_n_elig
    comb_pos1 = defaultdict(int)
    for o, c in ah_pos1.items():
        comb_pos1[o] += c
    for o, c in bh_pos1.items():
        comb_pos1[o] += c

    print(f"\n--- {lf_onset}-LF pos1: A herbal_a + B herbal combined ---")
    print(f"A herbal_a: N_lf={len(ah_lf)}, N_elig={ah_n_elig}")
    print(f"B herbal:   N_lf={len(bh_lf)}, N_elig={bh_n_elig}")
    print(f"Combined:   N_lf={len(comb_lf)}, N_elig={comb_n_elig}")

    # Key onset: y
    for target_onset in ['y', 'ot', 'd', 'ch', 'qok', 'sh']:
        a_obs = ah_pos1.get(target_onset, 0)
        b_obs = bh_pos1.get(target_onset, 0)
        c_obs = comb_pos1.get(target_onset, 0)
        base_rate = pos1_base_comb.get(target_onset, 0)

        a_exp = base_rate * ah_n_elig if ah_n_elig > 0 else 0
        b_exp = base_rate * bh_n_elig if bh_n_elig > 0 else 0
        c_exp = base_rate * comb_n_elig if comb_n_elig > 0 else 0

        a_E = a_obs/a_exp if a_exp > 0 else 0
        b_E = b_obs/b_exp if b_exp > 0 else 0
        c_E = c_obs/c_exp if c_exp > 0 else 0

        a_flag = flag_cell(a_obs, a_E)
        b_flag = flag_cell(b_obs, b_E)
        c_flag = flag_cell(c_obs, c_E)

        print(f"  {target_onset:8s}: A({a_obs}/{ah_n_elig},E={a_E:.2f}x{' '+a_flag if a_flag else ''}) "
              f"B({b_obs}/{bh_n_elig},E={b_E:.2f}x{' '+b_flag if b_flag else ''}) "
              f"COMB({c_obs}/{comb_n_elig},E={c_E:.2f}x{' '+c_flag if c_flag else ''})")

# ==== PART 2: B astro pos1 grammar survey ====

print("\n\n=== PART 2: B astro pos1 Grammar Survey ===")
print(f"B astro: {len(b_astro)} lines")

# B astro pos1 baseline
pos1_total_bast = 0
pos1_counts_bast = defaultdict(int)
for folio, words in b_astro:
    o = get_onset(words[0])
    if o:
        pos1_counts_bast[o] += 1
        pos1_total_bast += 1

print(f"\nB astro pos1 baseline (N={pos1_total_bast}):")
pos1_base_bast = {}
for o in ONSET_PRIORITY:
    c = pos1_counts_bast[o]
    if c > 0:
        pct = c / pos1_total_bast * 100
        pos1_base_bast[o] = c / pos1_total_bast
        if pct >= 1.0:
            print(f"  {o}: {c} ({pct:.1f}%)")

# B astro LF distribution
lf_counts_bast = defaultdict(int)
for folio, words in b_astro:
    o = get_onset(words[-1])
    if o:
        lf_counts_bast[o] += 1
lf_total_bast = sum(lf_counts_bast.values())

print(f"\nB astro LF distribution (N={lf_total_bast}, top 10):")
for o in sorted(lf_counts_bast, key=lambda x: -lf_counts_bast[x])[:10]:
    pct = lf_counts_bast[o] / lf_total_bast * 100
    print(f"  {o}: {lf_counts_bast[o]} ({pct:.1f}%)")

# pos1 routing for each major B astro LF class
MIN_LF = 8
print(f"\nB astro pos1 routing (min LF N={MIN_LF}):")
major_lf_bast = [(o, lf_counts_bast[o]) for o in ONSET_PRIORITY if lf_counts_bast[o] >= MIN_LF]

for lf_onset, lf_n in major_lf_bast:
    lf_lines = [(fo, ws) for fo, ws in b_astro if get_onset(ws[-1]) == lf_onset]
    elig = [(fo, ws) for fo, ws in lf_lines if len(ws) >= 2]
    n_elig = len(elig)

    pos1_dist = defaultdict(int)
    for fo, ws in elig:
        o = get_onset(ws[0])
        if o:
            pos1_dist[o] += 1

    print(f"\n  {lf_onset}-LF (N_lf={lf_n}, N_elig={n_elig}):")
    rows = []
    for o in ONSET_PRIORITY:
        obs = pos1_dist[o]
        base_rate = pos1_base_bast.get(o, 0)
        if base_rate == 0 and obs == 0:
            continue
        expected = base_rate * n_elig if base_rate > 0 else 0
        E = obs / expected if expected > 0 else float('inf') if obs > 0 else 0
        rows.append((o, obs, expected, E))
    rows.sort(key=lambda x: (-x[3] if x[3] != float('inf') else 1e9))

    for o, obs, exp, E in rows[:6]:
        flag = flag_cell(obs, E) if E != float('inf') else '(uniq)'
        base_pct = pos1_base_bast.get(o, 0) * 100
        E_str = f"{E:.2f}x" if E != float('inf') else "inf"
        print(f"    {o:8s}: obs={obs:3d}, exp={exp:.1f} (base={base_pct:.1f}%), E={E_str}  {flag}")

    # Self-chain
    top6 = [r[0] for r in rows[:6]]
    if lf_onset not in top6:
        self_obs = pos1_dist.get(lf_onset, 0)
        self_base = pos1_base_bast.get(lf_onset, 0)
        self_exp = self_base * n_elig if self_base > 0 else 0
        self_E = self_obs / self_exp if self_exp > 0 else 0
        flag = flag_cell(self_obs, self_E)
        print(f"    [{lf_onset}-self]: obs={self_obs}, exp={self_exp:.1f}, E={self_E:.2f}x  {flag}")
