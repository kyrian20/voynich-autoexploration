#!/usr/bin/env python3
"""
exp_493: A herbal_a Formula Frame Validation + B herbal pen Survey
H_new_BT: cth↔ot pen relationship; co-occurrence rates for formula frames
H_new_BU: B herbal pen routing with correct ws[-2] baselines
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

# Build baselines
p1_base = defaultdict(int); n_p1 = 0
p2_base = defaultdict(int); n_p2 = 0
pen_base = defaultdict(int); n_pen = 0  # ws[-2] from len>=3 lines
for ws in all_ws_a:
    if len(ws) >= 1:
        p1_base[get_onset(ws[0])] += 1; n_p1 += 1
    if len(ws) >= 2:
        p2_base[get_onset(ws[1])] += 1; n_p2 += 1
    if len(ws) >= 3:
        pen_base[get_onset(ws[-2])] += 1; n_pen += 1

# ============================================================
print("="*70)
print("1. ot-LF FORMULA FRAME: y[pos1] → ? → cth[pen] → ot[LF]")
print("="*70)

ot_lf = [(f, ws) for f, ws in a_herbal if ws and get_onset(ws[-1]) == 'ot']
print(f"A herbal_a ot-LF: N={len(ot_lf)}")

# Lines with pen eligible (len >= 3)
ot_pen_elig = [(f, ws) for f, ws in ot_lf if len(ws) >= 3]
ot_pos1_elig = [(f, ws) for f, ws in ot_lf if len(ws) >= 1]
ot_pos2_elig = [(f, ws) for f, ws in ot_lf if len(ws) >= 2]

print(f"N_pen_elig(len>=3): {len(ot_pen_elig)}")
print()

# Frame co-occurrence: y at pos1 AND cth at pen (in same line)
both_y_cth = [(f, ws) for f, ws in ot_pen_elig
              if len(ws) >= 3 and get_onset(ws[0]) == 'y' and get_onset(ws[-2]) == 'cth']
only_y = [(f, ws) for f, ws in ot_pen_elig
          if len(ws) >= 3 and get_onset(ws[0]) == 'y' and get_onset(ws[-2]) != 'cth']
only_cth = [(f, ws) for f, ws in ot_pen_elig
            if len(ws) >= 3 and get_onset(ws[0]) != 'y' and get_onset(ws[-2]) == 'cth']
neither = [(f, ws) for f, ws in ot_pen_elig
           if len(ws) >= 3 and get_onset(ws[0]) != 'y' and get_onset(ws[-2]) != 'cth']

print(f"ot-LF co-occurrence (N_elig={len(ot_pen_elig)}):")
print(f"  y@pos1 AND cth@pen: {len(both_y_cth)} ({len(both_y_cth)/len(ot_pen_elig)*100:.1f}%)")
print(f"  y@pos1 only: {len(only_y)}")
print(f"  cth@pen only: {len(only_cth)}")
print(f"  neither: {len(neither)}")
print()

# Baseline expected co-occurrence
y_base = p1_base.get('y', 0) / n_p1
cth_pen_base = pen_base.get('cth', 0) / n_pen
exp_both = y_base * cth_pen_base * len(ot_pen_elig)
print(f"Expected co-occurrence if independent: {exp_both:.2f}")
print(f"Observed: {len(both_y_cth)} — {'CO-OCCURRING' if len(both_y_cth) > exp_both*1.5 else 'near baseline'}")

# pos2 in ot-LF lines with y@pos1
print(f"\nIn ot-LF lines with y at pos1 (N={sum(1 for f,ws in ot_pos2_elig if get_onset(ws[0])=='y')}):")
ot_y_pos1_lines = [(f, ws) for f, ws in ot_pos2_elig if get_onset(ws[0]) == 'y']
if ot_y_pos1_lines:
    obs_p2 = defaultdict(int)
    for _, ws in ot_y_pos1_lines:
        if len(ws) >= 2:
            obs_p2[get_onset(ws[1])] += 1
    for o, n in sorted(obs_p2.items(), key=lambda x: -x[1])[:5]:
        base = p2_base.get(o, 0) / n_p2
        E = (n/len(ot_y_pos1_lines)) / base if base > 0 else float('inf')
        print(f"  pos2 {o}: {n}/{len(ot_y_pos1_lines)} (E={E:.2f}×)")

# ============================================================
print("\n\n" + "="*70)
print("2. cth-LF FORMULA FRAME: qo[pos1](dir) → cth[pos2](CONF) → d[pen](CONF) → cth[LF]")
print("="*70)

cth_lf = [(f, ws) for f, ws in a_herbal if ws and get_onset(ws[-1]) == 'cth']
cth_frame_elig = [(f, ws) for f, ws in cth_lf if len(ws) >= 3]
print(f"A herbal_a cth-LF: N={len(cth_lf)}, N_frame_elig(len>=3): {len(cth_frame_elig)}")

# Co-occurrence: cth at pos2 AND d at pen
both_cth_d = [(f, ws) for f, ws in cth_frame_elig
              if get_onset(ws[1]) == 'cth' and get_onset(ws[-2]) == 'd']
only_cth_p2 = [(f, ws) for f, ws in cth_frame_elig
               if get_onset(ws[1]) == 'cth' and get_onset(ws[-2]) != 'd']
only_d_pen = [(f, ws) for f, ws in cth_frame_elig
              if get_onset(ws[1]) != 'cth' and get_onset(ws[-2]) == 'd']
neither2 = [(f, ws) for f, ws in cth_frame_elig
            if get_onset(ws[1]) != 'cth' and get_onset(ws[-2]) != 'd']

print(f"cth-LF co-occurrence (N_elig={len(cth_frame_elig)}):")
print(f"  cth@pos2 AND d@pen: {len(both_cth_d)} ({len(both_cth_d)/len(cth_frame_elig)*100:.1f}%)")
print(f"  cth@pos2 only: {len(only_cth_p2)}")
print(f"  d@pen only: {len(only_d_pen)}")
print(f"  neither: {len(neither2)}")
cth_p2_base = p2_base.get('cth', 0) / n_p2
d_pen_base = pen_base.get('d', 0) / n_pen
exp_both2 = cth_p2_base * d_pen_base * len(cth_frame_elig)
print(f"Expected co-occurrence if independent: {exp_both2:.2f}")
print(f"Observed: {len(both_cth_d)}")

# qo at pos1 in cth-LF
print(f"\nqo at pos1 in cth-LF lines:")
cth_qo_p1 = [(f, ws) for f, ws in cth_lf if get_onset(ws[0]) == 'qo']
print(f"  Lines with qo at pos1: {len(cth_qo_p1)}/{len(cth_lf)}")

# ============================================================
print("\n\n" + "="*70)
print("3. d-LF / ot / cth TRIANGULAR RELATIONSHIP")
print("   d-LF starts with ot (F453); cth-LF has d at pen (F474); ot-LF has cth at pen (dir)")
print("="*70)

d_lf = [(f, ws) for f, ws in a_herbal if ws and get_onset(ws[-1]) == 'd']
print(f"d-LF: N={len(d_lf)}")

# In d-LF lines, do any have cth at pen?
d_cth_pen = [(f, ws) for f, ws in d_lf if len(ws) >= 3 and get_onset(ws[-2]) == 'cth']
d_pen_elig = [(f, ws) for f, ws in d_lf if len(ws) >= 3]
d_cth_base = pen_base.get('cth', 0) / n_pen
d_exp_cth = d_cth_base * len(d_pen_elig)
d_E_cth = len(d_cth_pen) / d_exp_cth if d_exp_cth > 0 else float('inf')
print(f"d-LF cth at pen: obs={len(d_cth_pen)}/{len(d_pen_elig)} E={d_E_cth:.2f}×")

# In cth-LF lines, do any have ot at pos1?
cth_ot_p1 = [(f, ws) for f, ws in cth_lf if get_onset(ws[0]) == 'ot']
cth_ot_base = p1_base.get('ot', 0) / n_p1
cth_ot_exp = cth_ot_base * len(cth_lf)
cth_ot_E = len(cth_ot_p1) / cth_ot_exp if cth_ot_exp > 0 else float('inf')
print(f"cth-LF ot at pos1: obs={len(cth_ot_p1)}/{len(cth_lf)} E={cth_ot_E:.2f}×")

# Summary of triangular relationships
print("\nTriangular onset relationships in A herbal_a:")
print("  d-LF → ot[pos1](CONF,F453): d-lines OPEN with ot")
print("  ot-LF → cth[pen](dir,E=3.70×/N=9): ot-lines CLOSE with cth before ot")
print("  cth-LF → d[pen](CONF,F474): cth-lines CLOSE with d before cth")
print("  → Chain: d opens ot-type lines; ot closes before cth; cth closes before d-type pen")
print("  → Possible cyclic marker: d → ot → cth → d (onset-class rotation in multi-line formulas?)")

# ============================================================
print("\n\n" + "="*70)
print("4. B HERBAL pen SURVEY (H_new_BU)")
print("="*70)

b_herbal = sections['B_herbal']
all_ws_bh = [ws for _, ws in b_herbal]

# Correct pen baseline: ws[-2] from len>=3 lines
pen_base_bh = defaultdict(int); n_pen_bh = 0
for ws in all_ws_bh:
    if len(ws) >= 3:
        pen_base_bh[get_onset(ws[-2])] += 1; n_pen_bh += 1

print(f"B herbal pen baseline (from ws[-2], len>=3, N={n_pen_bh}):")
for o, n in sorted(pen_base_bh.items(), key=lambda x: -x[1])[:10]:
    print(f"  {o:<6}: {n/n_pen_bh:.4f} ({n/n_pen_bh*100:.2f}%)")
print()

lf_dist_bh = defaultdict(int)
for _, ws in b_herbal:
    if ws:
        lf_dist_bh[get_onset(ws[-1])] += 1

print("B herbal pen routing (top pen onsets per LF class, E-sorted):")
print("-"*65)

for lf_onset in sorted(lf_dist_bh.keys(), key=lambda x: -lf_dist_bh[x]):
    N_lf = lf_dist_bh[lf_onset]
    if N_lf < 5:
        continue
    lf_lines = [(f, ws) for f, ws in b_herbal
                if ws and get_onset(ws[-1]) == lf_onset]
    elig = [(f, ws) for f, ws in lf_lines if len(ws) >= 3]
    N_elig = len(elig)
    if N_elig < 3:
        continue

    obs_by = defaultdict(int)
    for _, ws in elig:
        obs_by[get_onset(ws[-2])] += 1

    rows = []
    for onset, obs in obs_by.items():
        base = pen_base_bh.get(onset, 0) / n_pen_bh
        exp = base * N_elig
        E = obs / exp if exp > 0 else float('inf')
        flg = flag_cell(obs, E)
        rows.append((onset, obs, N_elig, base, E, flg))
    rows.sort(key=lambda x: -x[4])

    print(f"\n  {lf_onset}-LF pen (N_lf={N_lf}, N_elig={N_elig}):")
    for onset, obs, n, base, E, flg in rows[:3]:
        self_mark = ' <-- SELF' if onset == lf_onset else ''
        a_check = ' (cf. F459)' if lf_onset == 'ok' and onset == 'a' else ''
        ot_check = ' (cf. F460)' if lf_onset == 'ot' and onset == 'ot' else ''
        print(f"    {onset:<6} obs={obs:>3}/{n} ({obs/n*100:.1f}%) base={base*100:.1f}% E={E:>5.2f}× {flg}{self_mark}{a_check}{ot_check}")
