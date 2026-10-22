#!/usr/bin/env python3
"""
exp_492: A herbal_a pen Position Survey + ch-LF pos1 Scope
H_new_BR: Any confirmed pen routing rules in A herbal_a with correct ws[-2] baselines?
H_new_BS: Does ch-LF → ch@pos1 extend to B herbal, B astro, A cosmo?
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

# ============================================================
print("="*70)
print("1. A herbal_a pen POSITION SURVEY (H_new_BR)")
print("   Using ws[-2] pen baseline (CORRECT methodology)")
print("="*70)

a_herbal = sections['A_herbal_a']
all_ws_a = [ws for _, ws in a_herbal]

# Correct pen baseline: ws[-2] distribution
pen_base_a = defaultdict(int); n_pen_a = 0
for ws in all_ws_a:
    if len(ws) >= 2:  # penultimate exists
        pen_base_a[get_onset(ws[-2])] += 1; n_pen_a += 1

print(f"A herbal_a pen baseline (from ws[-2], N={n_pen_a}):")
for o, n in sorted(pen_base_a.items(), key=lambda x: -x[1])[:10]:
    print(f"  {o:<6}: {n/n_pen_a:.4f} ({n/n_pen_a*100:.2f}%)")
print()

# Also note: pen baseline INCLUDES lines with only 1 word (pen=LF for single-word lines)
# For the routing test, we want lines where pen != LF, i.e., len(ws) >= 3
# (so penultimate is ws[-2] and LF is ws[-1], distinct positions)
# Let's compute pen baseline from lines with len >= 3 (pen is truly a different position)
pen_base_a3 = defaultdict(int); n_pen_a3 = 0
for ws in all_ws_a:
    if len(ws) >= 3:
        pen_base_a3[get_onset(ws[-2])] += 1; n_pen_a3 += 1

print(f"A herbal_a pen baseline from lines len>=3 (N={n_pen_a3}):")
for o, n in sorted(pen_base_a3.items(), key=lambda x: -x[1])[:10]:
    print(f"  {o:<6}: {n/n_pen_a3:.4f} ({n/n_pen_a3*100:.2f}%)")
print()

lf_dist_a = defaultdict(int)
for _, ws in a_herbal:
    if ws:
        lf_dist_a[get_onset(ws[-1])] += 1

print(f"A herbal_a pen routing survey (correct ws[-2] baseline):")
print(f"{'LF onset':<8} {'N_lf':>6} {'N_elig':>7}")
print("(top 3 pen onsets per LF class, E-sorted)")
print("-"*70)

for lf_onset in sorted(lf_dist_a.keys(), key=lambda x: -lf_dist_a[x]):
    N_lf = lf_dist_a[lf_onset]
    if N_lf < 10:
        continue

    lf_lines = [(f, ws) for f, ws in a_herbal
                if ws and get_onset(ws[-1]) == lf_onset]
    # Pen-eligible: len >= 3 (pen != LF)
    elig = [(f, ws) for f, ws in lf_lines if len(ws) >= 3]
    N_elig = len(elig)
    if N_elig < 5:
        print(f"  {lf_onset:<8} {N_lf:>6} {N_elig:>7}  (skip, N_elig<5)")
        continue

    obs_by = defaultdict(int)
    for _, ws in elig:
        obs_by[get_onset(ws[-2])] += 1

    rows = []
    for onset, obs in obs_by.items():
        base = pen_base_a3.get(onset, 0) / n_pen_a3
        exp = base * N_elig
        E = obs / exp if exp > 0 else float('inf')
        flg = flag_cell(obs, E)
        rows.append((onset, obs, N_elig, base, E, flg))
    rows.sort(key=lambda x: -x[4])

    print(f"\n  {lf_onset}-LF pen (N_lf={N_lf}, N_elig={N_elig}):")
    for onset, obs, n, base, E, flg in rows[:3]:
        self_mark = ' <-- SELF' if onset == lf_onset else ''
        print(f"    {onset:<6} obs={obs:>3}/{n} ({obs/n*100:.1f}%) base={base*100:.1f}% E={E:>5.2f}× {flg}{self_mark}")

# ============================================================
print("\n\n" + "="*70)
print("2. ch-LF → ch@pos1 SCOPE: B herbal, B astro, A cosmo (H_new_BS)")
print("   Known CONF: A herbal_a (F473, E=1.58×/N=30), B pharma (F449, E=1.64×/N=15)")
print("="*70)

for sec_label in ['B_herbal', 'B_astro', 'A_cosmo', 'A_stars']:
    if sec_label not in sections:
        continue
    sec_lines = sections[sec_label]
    all_ws_s = [ws for _, ws in sec_lines]

    # pos1 baseline
    p1_base_s = defaultdict(int); n_p1_s = 0
    for ws in all_ws_s:
        if len(ws) >= 1:
            p1_base_s[get_onset(ws[0])] += 1; n_p1_s += 1

    ch_base = p1_base_s.get('ch', 0) / n_p1_s if n_p1_s > 0 else 0

    # ch-LF lines
    ch_lf = [(f, ws) for f, ws in sec_lines if ws and get_onset(ws[-1]) == 'ch']
    N_lf = len(ch_lf)
    elig = [(f, ws) for f, ws in ch_lf if len(ws) >= 1]
    N_elig = len(elig)

    if N_lf < 5:
        print(f"\n  {sec_label}: ch-LF N={N_lf} (skip)")
        continue

    obs = sum(1 for _, ws in elig if get_onset(ws[0]) == 'ch')
    exp = ch_base * N_elig
    E = obs / exp if exp > 0 else float('inf')
    flg = flag_cell(obs, E)

    print(f"\n  {sec_label} (total={len(sec_lines)}, ch-LF N_lf={N_lf}, N_elig={N_elig}):")
    print(f"    ch baseline at pos1: {ch_base*100:.2f}%")
    print(f"    ch@pos1 in ch-LF: obs={obs}/{N_elig} ({obs/N_elig*100:.1f}%) E={E:.2f}× {flg}")

    # Top pos1 onsets for ch-LF
    obs_by = defaultdict(int)
    for _, ws in elig:
        obs_by[get_onset(ws[0])] += 1
    top = sorted(obs_by.items(), key=lambda x: -x[1])[:5]
    print(f"    Top pos1 onsets: {', '.join(f'{o}({n})' for o, n in top)}")

# ============================================================
print("\n\n" + "="*70)
print("3. B herbal ch-LF full pos1 distribution")
print("="*70)

b_herbal = sections['B_herbal']
all_ws_bh = [ws for _, ws in b_herbal]
p1_base_bh = defaultdict(int); n_p1_bh = 0
for ws in all_ws_bh:
    if len(ws) >= 1:
        p1_base_bh[get_onset(ws[0])] += 1; n_p1_bh += 1

print(f"B herbal pos1 baseline (top 8):")
for o, n in sorted(p1_base_bh.items(), key=lambda x: -x[1])[:8]:
    print(f"  {o:<6}: {n/n_p1_bh:.3f} ({n/n_p1_bh*100:.1f}%)")

bh_ch_lf = [(f, ws) for f, ws in b_herbal if ws and get_onset(ws[-1]) == 'ch']
bh_ch_elig = [(f, ws) for f, ws in bh_ch_lf if len(ws) >= 1]
print(f"\nB herbal ch-LF: N_lf={len(bh_ch_lf)}, N_elig={len(bh_ch_elig)}")

obs_bh = defaultdict(int)
for _, ws in bh_ch_elig:
    obs_bh[get_onset(ws[0])] += 1

rows = []
for onset, obs in sorted(obs_bh.items(), key=lambda x: -x[1]):
    if obs < 2: continue
    base = p1_base_bh.get(onset, 0) / n_p1_bh
    exp = base * len(bh_ch_elig)
    E = obs / exp if exp > 0 else float('inf')
    flg = flag_cell(obs, E)
    rows.append((onset, obs, exp, E, flg))
rows.sort(key=lambda x: -x[3])

print(f"B herbal ch-LF pos1 distribution:")
for onset, obs, exp, E, flg in rows:
    marker = ' <-- SELF' if onset == 'ch' else ''
    print(f"  {onset:<6} obs={obs:>3}/{len(bh_ch_elig)} ({obs/len(bh_ch_elig)*100:.1f}%) exp={exp:.1f} E={E:.2f}× {flg}{marker}")
