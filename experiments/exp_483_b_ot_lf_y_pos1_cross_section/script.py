#!/usr/bin/env python3
"""
exp_483: Cross-section ot-LF → y at pos1 test (B pharma + B astro)
Also: ok → a at pen as B-dialect-wide rule (B herbal + B pharma combined)
H_new_AZ: Does B pharma ot-LF → y at pos1 (confirmation of cross-dialectal ot/y rule)?
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

b_by_section = defaultdict(list)
for folio, lines in folios.items():
    all_words = [w for line in lines for w in line]
    if is_b_dialect(all_words):
        sec = get_section_b(folio)
        for line in lines:
            b_by_section[sec].append((folio, line))

def flag_cell(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONFIRMED'
    if obs >= 5  and E >= 2.0: return 'dir'
    if obs >= 3  and E >= 2.0: return '(dir)'
    return ''

def analyze_lf_pos1(section_lines, lf_onset, section_label, focus_onset='y'):
    """Full pos1 routing for lf_onset lines, highlighting focus_onset."""
    all_ws = [ws for _, ws in section_lines]
    N_total = len(all_ws)

    # pos1 baseline
    pos1_base = defaultdict(int); n_base = 0
    for ws in all_ws:
        if len(ws) >= 1:
            pos1_base[get_onset(ws[0])] += 1; n_base += 1

    # LF lines
    lf_lines = [(f, ws) for f, ws in section_lines
                if ws and get_onset(ws[-1]) == lf_onset and len(ws) >= 2]
    N_lf = len(lf_lines)

    if N_lf < 5:
        print(f"  {section_label} {lf_onset}-LF: N={N_lf} (skip)")
        return None

    # Pos1 obs
    p1_obs = defaultdict(int)
    for _, ws in lf_lines:
        p1_obs[get_onset(ws[0])] += 1

    # Compute all enrichments
    rows = []
    for onset, obs in p1_obs.items():
        if obs < 2: continue
        exp = pos1_base.get(onset, 0) / n_base * N_lf if n_base > 0 else 0
        E = obs / exp if exp > 0 else float('inf')
        rows.append((onset, obs, exp, E, flag_cell(obs, E)))
    rows.sort(key=lambda x: -x[3])

    print(f"\n  {section_label} {lf_onset}-LF (N_lf={N_lf}, N_total={N_total}):")
    for onset, obs, exp, E, flg in rows[:6]:
        marker = ' <<<' if onset == focus_onset else ''
        print(f"    {onset:<6} obs={obs:>3} exp={exp:>5.1f} E={E:>5.2f}× {flg}{marker}")

    # Explicit focus onset
    fo_obs = p1_obs.get(focus_onset, 0)
    fo_exp = pos1_base.get(focus_onset, 0) / n_base * N_lf if n_base > 0 else 0
    fo_E = fo_obs / fo_exp if fo_exp > 0 else float('inf')
    if focus_onset not in dict((r[0],r) for r in rows[:6]):
        flg = flag_cell(fo_obs, fo_E)
        print(f"    {focus_onset:<6} obs={fo_obs:>3} exp={fo_exp:>5.1f} E={fo_E:>5.2f}× {flg}  (focus)")

    return (N_lf, fo_obs, fo_exp, fo_E)

def analyze_lf_pen(section_lines, lf_onset, section_label, focus_onset='a'):
    """Pen routing for lf_onset lines, highlighting focus_onset."""
    all_ws = [ws for _, ws in section_lines]
    N_total = len(all_ws)

    # pen baseline
    pen_base = defaultdict(int); n_base = 0
    for ws in all_ws:
        if len(ws) >= 3:
            pen_base[get_onset(ws[-2])] += 1; n_base += 1

    # LF lines with >= 3 words
    lf_lines = [(f, ws) for f, ws in section_lines
                if ws and get_onset(ws[-1]) == lf_onset and len(ws) >= 3]
    N_lf = len(lf_lines)

    if N_lf < 5:
        print(f"  {section_label} {lf_onset}-LF pen: N={N_lf} (skip)")
        return None

    # Pen obs
    pn_obs = defaultdict(int)
    for _, ws in lf_lines:
        pn_obs[get_onset(ws[-2])] += 1

    rows = []
    for onset, obs in pn_obs.items():
        if obs < 2: continue
        exp = pen_base.get(onset, 0) / n_base * N_lf if n_base > 0 else 0
        E = obs / exp if exp > 0 else float('inf')
        rows.append((onset, obs, exp, E, flag_cell(obs, E)))
    rows.sort(key=lambda x: -x[3])

    print(f"\n  {section_label} {lf_onset}-LF pen (N_pen_eligible={N_lf}):")
    for onset, obs, exp, E, flg in rows[:6]:
        marker = ' <<<' if onset == focus_onset else ''
        print(f"    {onset:<6} obs={obs:>3} exp={exp:>5.1f} E={E:>5.2f}× {flg}{marker}")

    fo_obs = pn_obs.get(focus_onset, 0)
    fo_exp = pen_base.get(focus_onset, 0) / n_base * N_lf if n_base > 0 else 0
    fo_E = fo_obs / fo_exp if fo_exp > 0 else float('inf')
    if focus_onset not in dict((r[0],r) for r in rows[:6]):
        flg = flag_cell(fo_obs, fo_E)
        print(f"    {focus_onset:<6} obs={fo_obs:>3} exp={fo_exp:>5.1f} E={fo_E:>5.2f}× {flg}  (focus)")

    return (N_lf, fo_obs, fo_exp, fo_E)

# ==============================================================
print("=" * 60)
print("TEST 1: ot-LF → y at pos1 across B sections")
print("=" * 60)
print("\nPrior results:")
print("  A herbal_a ot-LF → y pos1: E=1.83×/N=11 (CONFIRMED, F456)")
print("  B herbal   ot-LF → y pos1: E=2.67×/N=6  (dir, exp_482)")

for sec in ['pharma', 'astro', 'cosmo', 'bio']:
    analyze_lf_pos1(b_by_section[sec], 'ot', f'B {sec}', focus_onset='y')

# Also B-overall (all B sections)
all_b = []
for sec in ['herbal', 'astro', 'cosmo', 'pharma', 'bio']:
    all_b.extend(b_by_section[sec])
print("\n  --- B-dialect COMBINED:")
analyze_lf_pos1(all_b, 'ot', 'B combined', focus_onset='y')

# ==============================================================
print("\n\n" + "=" * 60)
print("TEST 2: ok-LF → a at pen across B sections")
print("=" * 60)
print("\nPrior results:")
print("  B pharma ok-LF → a pen: E=2.04×/N=11 (CONFIRMED, F452)")
print("  B herbal ok-LF → a pen: E=2.73×/N=6  (dir, exp_482)")

for sec in ['astro', 'cosmo', 'bio']:
    analyze_lf_pen(b_by_section[sec], 'ok', f'B {sec}', focus_onset='a')

# B herbal re-confirm
analyze_lf_pen(b_by_section['herbal'], 'ok', 'B herbal', focus_onset='a')
analyze_lf_pen(b_by_section['pharma'], 'ok', 'B pharma', focus_onset='a')

# B-overall combined
print("\n  --- B-dialect COMBINED ok-LF → a pen:")
analyze_lf_pen(all_b, 'ok', 'B combined', focus_onset='a')

# ==============================================================
print("\n\n" + "=" * 60)
print("TEST 3: ot-LF → ot at pen (F450 replication check)")
print("=" * 60)
print("F450: B pharma ot-LF → ot at pen (E=1.94×/N=15, CONFIRMED)")
analyze_lf_pen(b_by_section['pharma'], 'ot', 'B pharma', focus_onset='ot')
analyze_lf_pen(b_by_section['herbal'], 'ot', 'B herbal', focus_onset='ot')
analyze_lf_pen(all_b, 'ot', 'B combined', focus_onset='ot')

# Summary table
print("\n\n" + "=" * 60)
print("SUMMARY: ot-LF y@pos1 and ok-LF a@pen across sections")
print("=" * 60)
print(f"\n{'Section':<12} {'ot-LF N':>8} {'y@pos1 E':>10} {'y@pos1 N':>10} | {'ok-LF N':>8} {'a@pen E':>10} {'a@pen N':>10}")
print("-" * 75)

for sec_label, sec_key in [('A herbal_a','aherbal_ref'), ('B herbal','herbal'),
                             ('B pharma','pharma'), ('B astro','astro'), ('B combined','combined')]:
    if sec_key == 'aherbal_ref':
        print(f"  {'A herbal_a':<12} {'43':>8} {'1.83×':>10} {'11(CONF)':>10} | {'53':>8} {'baseline':>10} {'(F455 pos1)':>10}")
        continue
    sec_lines = all_b if sec_key == 'combined' else b_by_section[sec_key]
    if not sec_lines:
        continue

    all_ws = [ws for _, ws in sec_lines]

    # ot-LF y@pos1
    pos1_b = defaultdict(int); nb1 = 0
    for ws in all_ws:
        if len(ws) >= 1: pos1_b[get_onset(ws[0])] += 1; nb1 += 1
    ot_lf = [(f,ws) for f,ws in sec_lines if ws and get_onset(ws[-1])=='ot' and len(ws)>=2]
    N_ot = len(ot_lf)
    y_obs = sum(1 for _,ws in ot_lf if get_onset(ws[0])=='y')
    y_exp = pos1_b.get('y',0)/nb1*N_ot if nb1 > 0 else 0
    y_E = y_obs/y_exp if y_exp > 0 else 0
    y_f = flag_cell(y_obs, y_E)

    # ok-LF a@pen
    pen_b = defaultdict(int); nbp = 0
    for ws in all_ws:
        if len(ws) >= 3: pen_b[get_onset(ws[-2])] += 1; nbp += 1
    ok_lf = [(f,ws) for f,ws in sec_lines if ws and get_onset(ws[-1])=='ok' and len(ws)>=3]
    N_ok = len(ok_lf)
    a_obs = sum(1 for _,ws in ok_lf if get_onset(ws[-2])=='a')
    a_exp = pen_b.get('a',0)/nbp*N_ok if nbp > 0 else 0
    a_E = a_obs/a_exp if a_exp > 0 else 0
    a_f = flag_cell(a_obs, a_E)

    print(f"  {sec_label:<12} {N_ot:>8} {f'{y_E:.2f}×({y_f})':>10} {y_obs:>10} | {N_ok:>8} {f'{a_E:.2f}×({a_f})':>10} {a_obs:>10}")
