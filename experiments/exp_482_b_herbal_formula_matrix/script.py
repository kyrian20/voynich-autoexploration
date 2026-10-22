#!/usr/bin/env python3
"""
exp_482: B herbal Full Formula Grammar Matrix
H_new_AX: Systematic pos1/pos2/pen routing for all major B herbal LF classes.
H_new_AW (embedded): Does B herbal ok-LF and ot-LF → y at pos1 (as in A herbal_a F455/F456)?
If yes: y/ok and y/ot opener is cross-dialectal.
If no: F455/F456 are A-herbal_a-specific.
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

# Classify B dialect, section=herbal
herbal_lines = []  # list of (folio, wordlist)
for folio, lines in folios.items():
    all_words = [w for line in lines for w in line]
    if is_b_dialect(all_words) and get_section_b(folio) == 'herbal':
        for line in lines:
            herbal_lines.append((folio, line))

print(f"B herbal: {len(herbal_lines)} lines from {len(set(f for f,_ in herbal_lines))} folios")

all_ws = [ws for _, ws in herbal_lines]
N_total = len(all_ws)

# Build section-specific baselines
pos1_base = defaultdict(int); n_pos1 = 0
pos2_base = defaultdict(int); n_pos2 = 0
pen_base  = defaultdict(int); n_pen  = 0

for ws in all_ws:
    if len(ws) >= 1:
        pos1_base[get_onset(ws[0])] += 1; n_pos1 += 1
    if len(ws) >= 2:
        pos2_base[get_onset(ws[1])] += 1; n_pos2 += 1
    if len(ws) >= 3:
        pen_base[get_onset(ws[-2])] += 1; n_pen += 1

print(f"\nTotal: {n_pos1} pos1, {n_pos2} pos2, {n_pen} pen measurements")

# LF distribution
lf_dist = defaultdict(int)
for ws in all_ws:
    lf_dist[get_onset(ws[-1])] += 1

print("\nB herbal LF-class distribution:")
for onset, cnt in sorted(lf_dist.items(), key=lambda x: -x[1])[:12]:
    print(f"  {onset:<6} {cnt:>4} ({cnt/N_total:.1%})")

def flag_cell(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONFIRMED'
    if obs >= 5  and E >= 2.0: return 'dir'
    if obs >= 3  and E >= 2.0: return '(dir)'
    return ''

def analyze_lf_class(lf_onset, lf_name):
    """Full pos1/pos2/pen routing for a specific LF onset in B herbal."""
    lf_lines = [(f, ws) for f, ws in herbal_lines
                if ws and get_onset(ws[-1]) == lf_onset]
    N_lf = len(lf_lines)
    if N_lf < 5:
        print(f"\n{lf_name} (N={N_lf}): too small, skip")
        return

    # Collect pos1, pos2, pen observations
    p1_obs = defaultdict(int); n1 = 0
    p2_obs = defaultdict(int); n2 = 0
    pn_obs = defaultdict(int); nn = 0

    for _, ws in lf_lines:
        if len(ws) >= 1:
            p1_obs[get_onset(ws[0])] += 1; n1 += 1
        if len(ws) >= 2:
            p2_obs[get_onset(ws[1])] += 1; n2 += 1
        if len(ws) >= 3:
            pn_obs[get_onset(ws[-2])] += 1; nn += 1

    # Top LF words
    lf_words = defaultdict(int)
    for _, ws in lf_lines:
        lf_words[ws[-1]] += 1
    top_lf = sorted(lf_words.items(), key=lambda x: -x[1])[:5]
    top_lf_str = ', '.join(f"{w}({c})" for w, c in top_lf)

    print(f"\n{'='*60}")
    print(f"{lf_name} (N={N_lf}): LF words: {top_lf_str}")

    # Print enrichment table for each position
    for pos_label, obs_d, base_d, n_base, n_obs in [
        ('pos1', p1_obs, pos1_base, n_pos1, n1),
        ('pos2', p2_obs, pos2_base, n_pos2, n2),
        ('pen',  pn_obs, pen_base,  n_pen,  nn),
    ]:
        if n_obs < 1:
            continue
        rows = []
        for onset, obs in obs_d.items():
            if obs < 2: continue
            exp = base_d.get(onset, 0) / n_base * n_obs if n_base > 0 else 0
            E = obs / exp if exp > 0 else float('inf')
            flg = flag_cell(obs, E)
            rows.append((onset, obs, exp, E, flg))
        # Sort by E, show elevated (E>=1.4×)
        rows.sort(key=lambda x: -x[3])
        elevated = [r for r in rows if r[3] >= 1.4 and r[1] >= 3]
        if elevated:
            print(f"  {pos_label} (N_lines={n_obs}):")
            for onset, obs, exp, E, flg in elevated[:6]:
                print(f"    {onset:<6} obs={obs:>3} exp={exp:>5.1f} E={E:>5.2f}× {flg}")

    # Specific cross-dialectal test: y at pos1
    y_obs_p1 = p1_obs.get('y', 0)
    y_exp_p1 = pos1_base.get('y', 0) / n_pos1 * n1 if n_pos1 > 0 else 0
    y_E_p1 = y_obs_p1 / y_exp_p1 if y_exp_p1 > 0 else float('inf')
    print(f"  [A-parallel check] y at pos1: obs={y_obs_p1}, exp={y_exp_p1:.1f}, E={y_E_p1:.2f}×  {flag_cell(y_obs_p1, y_E_p1)}")

# Analyze all major B herbal LF classes
print("\n\n=== B HERBAL FORMULA GRAMMAR MATRIX ===")
for lf_onset in ['t','y','ch','ok','ot','d','sh','o','s','l','qok']:
    if lf_dist.get(lf_onset, 0) >= 10:
        analyze_lf_class(lf_onset, f'B herbal {lf_onset}-LF')

# Summary matrix
print("\n\n=== SUMMARY: B herbal LF FORMULA MATRIX ===")
print(f"{'LF':<6} {'N':>5} | {'pos1 top (E>=1.4)':<35} | {'pos2 top (E>=1.4)':<35} | {'pen top (E>=1.4)':<35}")
print("-" * 120)

for lf_onset in ['t','y','ch','ok','ot','d','sh','o','s','l','qok']:
    N_lf = lf_dist.get(lf_onset, 0)
    if N_lf < 10:
        continue
    lf_lines = [(f, ws) for f, ws in herbal_lines
                if ws and get_onset(ws[-1]) == lf_onset]

    def top_elevated(obs_d, base_d, n_base, n_obs, top_n=2):
        rows = []
        for onset, obs in obs_d.items():
            if obs < 2: continue
            exp = base_d.get(onset, 0) / n_base * n_obs if n_base > 0 else 0
            E = obs / exp if exp > 0 else float('inf')
            if E >= 1.4:
                rows.append((onset, obs, E))
        rows.sort(key=lambda x: -x[2])
        return rows[:top_n]

    p1_obs_d = defaultdict(int); n1 = 0
    p2_obs_d = defaultdict(int); n2 = 0
    pn_obs_d = defaultdict(int); nn = 0
    for _, ws in lf_lines:
        if len(ws) >= 1: p1_obs_d[get_onset(ws[0])] += 1; n1 += 1
        if len(ws) >= 2: p2_obs_d[get_onset(ws[1])] += 1; n2 += 1
        if len(ws) >= 3: pn_obs_d[get_onset(ws[-2])] += 1; nn += 1

    def fmt(rows):
        if not rows: return 'flat'
        return '; '.join(f"{o}({E:.2f}×/N={obs})" for o, obs, E in rows)

    p1_str = fmt(top_elevated(p1_obs_d, pos1_base, n_pos1, n1))
    p2_str = fmt(top_elevated(p2_obs_d, pos2_base, n_pos2, n2))
    pn_str = fmt(top_elevated(pn_obs_d, pen_base,  n_pen,  nn))
    print(f"{lf_onset:<6} {N_lf:>5} | {p1_str:<35} | {p2_str:<35} | {pn_str:<35}")
