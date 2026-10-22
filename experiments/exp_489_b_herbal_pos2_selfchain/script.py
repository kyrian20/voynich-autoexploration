#!/usr/bin/env python3
"""
exp_489: B herbal pos2 Self-Chaining Survey
H_new_BK: Does pos2 self-chaining extend universally to B herbal (as it does in A herbal_a)?
Known B herbal pos2: ch→ch(F458,CONF), d→sh(F457,CONF,cross-class). Test all LF classes.
Also run B pharma pos2 self-chaining survey (H_new_BL).
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

def get_section_a(folio):
    n = folio_num(folio)
    if n <= 56: return 'herbal_a'
    if n <= 72: return 'stars'
    if n <= 84: return 'herbal_b'
    if n <= 102: return 'cosmo'
    return 'other'

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

def pos2_selfchain_survey(section_lines, section_label, min_lf=5):
    """Survey pos2 self-chaining for all LF classes in a section."""
    all_ws = [ws for _, ws in section_lines]

    # pos2 baseline
    p2_base = defaultdict(int); n_p2 = 0
    for ws in all_ws:
        if len(ws) >= 2:
            p2_base[get_onset(ws[1])] += 1; n_p2 += 1

    # LF distribution
    lf_dist = defaultdict(int)
    for _, ws in section_lines:
        if ws:
            lf_dist[get_onset(ws[-1])] += 1

    print(f"\n{'='*65}")
    print(f"Section: {section_label} (total lines: {len(section_lines)}, pos2 eligible: {n_p2})")
    print(f"{'='*65}")
    print(f"{'LF onset':<8} {'N_lf':>6} {'N_elig':>7} {'obs':>5} {'base%':>7} {'E':>7}  {'flag'}")
    print("-"*60)

    results = []
    for lf_onset in sorted(lf_dist.keys(), key=lambda x: -lf_dist[x]):
        N_lf = lf_dist[lf_onset]
        if N_lf < min_lf:
            continue

        lf_lines = [(f, ws) for f, ws in section_lines
                    if ws and get_onset(ws[-1]) == lf_onset]
        elig = [(f, ws) for f, ws in lf_lines if len(ws) >= 2]
        N_elig = len(elig)
        if N_elig < 3:
            continue

        # Self-chaining
        obs = sum(1 for _, ws in elig if get_onset(ws[1]) == lf_onset)
        base_rate = p2_base.get(lf_onset, 0) / n_p2 if n_p2 > 0 else 0
        exp = base_rate * N_elig
        E = obs / exp if exp > 0 else float('inf')
        flg = flag_cell(obs, E)

        # Also compute cross-class pos2 enrichment for comparison
        # (what IS at pos2 if not self?)
        cross_obs = defaultdict(int)
        for _, ws in elig:
            o2 = get_onset(ws[1])
            if o2 != lf_onset:
                cross_obs[o2] += 1
        top_cross = [(o, n) for o, n in sorted(cross_obs.items(), key=lambda x: -x[1])][:2]
        cross_str = ', '.join(f"{o}({n})" for o, n in top_cross)

        marker = ''
        if flg == 'CONFIRMED': marker = ' CONFIRMED'
        elif flg == 'dir': marker = ' dir'
        elif flg == '(dir)': marker = ' (dir)'

        print(f"  {lf_onset:<8} {N_lf:>6} {N_elig:>7} {obs:>5} {base_rate*100:>6.1f}% {E:>6.2f}×{marker}")
        if cross_str:
            print(f"           top non-self pos2: {cross_str}")

        results.append((lf_onset, N_lf, N_elig, obs, base_rate, E, flg))

    return results

# ============================================================
print("="*65)
print("1. B HERBAL pos2 SELF-CHAINING SURVEY (H_new_BK)")
print("   Known: ch→ch(F458,CONF), d→sh(F457,CONF,cross-class)")
print("   Test: does pos2 self-chaining also hold for d-SELF, ok, ot, sh, y, t?")
print("="*65)

b_herbal = sections['B_herbal']
b_herbal_results = pos2_selfchain_survey(b_herbal, 'B herbal')

# ============================================================
print("\n\n" + "="*65)
print("2. B PHARMA pos2 SELF-CHAINING SURVEY (H_new_BL)")
print("   Known: ch→ch@pos2 below threshold (E=1.30×, F462). Test others.")
print("="*65)

b_pharma = sections['B_pharma']
b_pharma_results = pos2_selfchain_survey(b_pharma, 'B pharma')

# ============================================================
print("\n\n" + "="*65)
print("3. CROSS-SECTION COMPARISON: A herbal_a vs B herbal vs B pharma")
print("   For common LF classes: is pos2 self-chaining universal across sections?")
print("="*65)

a_herbal = sections['A_herbal_a']

# Compare the same LF classes across sections
compare_onsets = ['d', 'ch', 'ok', 'ot', 'sh', 'y', 't', 'qok', 'o', 'cth']

for sec_label, sec_lines in [('A herbal_a', a_herbal), ('B herbal', b_herbal), ('B pharma', b_pharma)]:
    all_ws = [ws for _, ws in sec_lines]
    p2_base = defaultdict(int); n_p2 = 0
    for ws in all_ws:
        if len(ws) >= 2:
            p2_base[get_onset(ws[1])] += 1; n_p2 += 1

    lf_dist = defaultdict(int)
    for _, ws in sec_lines:
        if ws:
            lf_dist[get_onset(ws[-1])] += 1

    print(f"\n{sec_label} (N={len(sec_lines)}):")
    print(f"  {'onset':<6} {'N_lf':>5} {'obs':>5} {'E':>7}  flag")

    for onset in compare_onsets:
        N_lf = lf_dist.get(onset, 0)
        if N_lf < 3:
            continue
        lf_lines = [(f, ws) for f, ws in sec_lines
                    if ws and get_onset(ws[-1]) == onset]
        elig = [(f, ws) for f, ws in lf_lines if len(ws) >= 2]
        N_elig = len(elig)
        if N_elig < 3:
            continue
        obs = sum(1 for _, ws in elig if get_onset(ws[1]) == onset)
        base_rate = p2_base.get(onset, 0) / n_p2 if n_p2 > 0 else 0
        exp = base_rate * N_elig
        E = obs / exp if exp > 0 else float('inf')
        flg = flag_cell(obs, E)
        marker = f' {flg}' if flg else ''
        print(f"  {onset:<6} {N_lf:>5} {obs:>5} {E:>6.2f}×{marker}")

# ============================================================
print("\n\n" + "="*65)
print("4. B HERBAL d-LF: SELF vs CROSS-CLASS at pos2")
print("   F457: d-LF → sh at pos2 (CONF). Does d-SELF also appear at pos2?")
print("="*65)

b_herbal_d_lf = [(f, ws) for f, ws in b_herbal if ws and get_onset(ws[-1]) == 'd']
b_herbal_d_elig = [(f, ws) for f, ws in b_herbal_d_lf if len(ws) >= 2]

all_ws_bh = [ws for _, ws in b_herbal]
p2_base_bh = defaultdict(int); n_p2_bh = 0
for ws in all_ws_bh:
    if len(ws) >= 2:
        p2_base_bh[get_onset(ws[1])] += 1; n_p2_bh += 1

print(f"B herbal d-LF: N_lf={len(b_herbal_d_lf)}, N_elig={len(b_herbal_d_elig)}")
obs_d2 = defaultdict(int)
for _, ws in b_herbal_d_elig:
    obs_d2[get_onset(ws[1])] += 1

rows = []
for onset, obs in sorted(obs_d2.items(), key=lambda x: -x[1]):
    base = p2_base_bh.get(onset, 0) / n_p2_bh
    exp = base * len(b_herbal_d_elig)
    E = obs / exp if exp > 0 else float('inf')
    flg = flag_cell(obs, E)
    rows.append((onset, obs, exp, E, flg))

print(f"Full pos2 distribution for B herbal d-LF:")
print(f"  {'onset':<6} {'obs':>4} {'exp':>6} {'E':>6}  flag")
for onset, obs, exp, E, flg in rows:
    marker = ' <-- F457' if onset == 'sh' else (' <-- SELF' if onset == 'd' else '')
    print(f"  {onset:<6} {obs:>4} {exp:>6.1f} {E:>6.2f}×  {flg}{marker}")
