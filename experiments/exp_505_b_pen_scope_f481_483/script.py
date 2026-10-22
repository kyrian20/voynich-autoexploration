#!/usr/bin/env python3
"""
exp_505: Scope test for F481/F482/F483 — B herbal and B pharma pen
H_new_CJ: Are B astro pen rules (qok→sh, d-self, l→ch) B-dialect-wide?
F460 (ot-self@pen) is B-dialect-wide — is F482 (d-self@pen) similarly broad?
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
    if obs == 0: return 'zero'
    return ''

def pen_rule_test(section_lines, label, lf_onset, pen_target):
    """Test a specific pen routing rule in a section."""
    # pen baseline (len>=3)
    pen_counts = defaultdict(int)
    pen_total = 0
    for fo, ws in section_lines:
        if len(ws) >= 3:
            o = get_onset(ws[-2])
            if o:
                pen_counts[o] += 1
                pen_total += 1

    if pen_total == 0:
        return label, lf_onset, pen_target, 0, 0, 0, 0, ''

    base_rate = pen_counts.get(pen_target, 0) / pen_total
    base_pct = base_rate * 100

    # LF lines
    lf_lines = [(fo, ws) for fo, ws in section_lines if get_onset(ws[-1]) == lf_onset]
    elig = [(fo, ws) for fo, ws in lf_lines if len(ws) >= 3]
    n_elig = len(elig)
    n_lf = len(lf_lines)

    obs = sum(1 for fo, ws in elig if get_onset(ws[-2]) == pen_target)
    exp = base_rate * n_elig
    E = obs / exp if exp > 0 else 0
    flag = flag_cell(obs, E)
    return label, lf_onset, pen_target, n_lf, n_elig, obs, E, flag, base_pct

def run_full_pen_for_class(section_lines, label, lf_onset, top_n=6):
    """Print full pen distribution for a specific LF class."""
    pen_counts = defaultdict(int)
    pen_total = 0
    for fo, ws in section_lines:
        if len(ws) >= 3:
            o = get_onset(ws[-2])
            if o:
                pen_counts[o] += 1
                pen_total += 1
    pen_base = {o: pen_counts[o]/pen_total for o in pen_counts} if pen_total > 0 else {}

    lf_lines = [(fo, ws) for fo, ws in section_lines if get_onset(ws[-1]) == lf_onset]
    elig = [(fo, ws) for fo, ws in lf_lines if len(ws) >= 3]
    n_elig = len(elig)

    pen_dist = defaultdict(int)
    for fo, ws in elig:
        o = get_onset(ws[-2])
        if o: pen_dist[o] += 1

    rows = []
    for o, cnt in pen_dist.items():
        br = pen_base.get(o, 0)
        E = cnt / (br * n_elig) if br > 0 and n_elig > 0 else float('inf')
        rows.append((o, cnt, E))
    rows.sort(key=lambda x: -x[2])

    print(f"  {label} {lf_onset}-LF pen (N_lf={len(lf_lines)}, N_elig={n_elig}):")
    for o, cnt, E in rows[:top_n]:
        br_pct = pen_base.get(o, 0) * 100
        flag = flag_cell(cnt, E) if E != float('inf') else '(uniq)'
        self_mark = ' <--SELF' if o == lf_onset else ''
        print(f"    {o:8s}: obs={cnt:3d}, E={E:.2f}x (base={br_pct:.1f}%)  {flag}{self_mark}")

print("=== F481/F482/F483 Scope Test (B herbal + B pharma pen) ===\n")
print("Target rules:")
print("  F481: qok-LF → sh@pen (E=2.12×/N=20, B astro CONF)")
print("  F482: d-LF → d-self@pen (E=1.96×/N=12, B astro CONF)")
print("  F483: l-LF → ch@pen (E=1.89×/N=22, B astro CONF)")
print()

# Test F481 (qok→sh@pen)
print("--- F481: qok-LF → sh@pen ---")
for sec_key, label in [('B_herbal','B herbal'), ('B_pharma','B pharma'), ('B_astro','B astro')]:
    r = pen_rule_test(sections[sec_key], label, 'qok', 'sh')
    lbl, lf, pen, n_lf, n_elig, obs, E, flag, base_pct = r
    print(f"  {lbl:12s}: qok-LF N={n_lf}, N_elig={n_elig}, sh@pen: obs={obs}, E={E:.2f}x (base={base_pct:.1f}%), {flag}")

# Test F482 (d-self@pen)
print("\n--- F482: d-LF → d-self@pen ---")
for sec_key, label in [('B_herbal','B herbal'), ('B_pharma','B pharma'), ('B_astro','B astro')]:
    r = pen_rule_test(sections[sec_key], label, 'd', 'd')
    lbl, lf, pen, n_lf, n_elig, obs, E, flag, base_pct = r
    print(f"  {lbl:12s}: d-LF N={n_lf}, N_elig={n_elig}, d-self@pen: obs={obs}, E={E:.2f}x (base={base_pct:.1f}%), {flag}")

# B combined d-self@pen
print("  --- B combined d-LF d-self@pen ---")
b_combined = sections['B_herbal'] + sections['B_pharma'] + sections['B_astro'] + sections['B_cosmo']
r = pen_rule_test(b_combined, 'B combined', 'd', 'd')
lbl, lf, pen, n_lf, n_elig, obs, E, flag, base_pct = r
print(f"  {lbl:12s}: d-LF N={n_lf}, N_elig={n_elig}, d-self@pen: obs={obs}, E={E:.2f}x (base={base_pct:.1f}%), {flag}")

# Test F483 (l→ch@pen)
print("\n--- F483: l-LF → ch@pen ---")
for sec_key, label in [('B_herbal','B herbal'), ('B_pharma','B pharma'), ('B_astro','B astro')]:
    r = pen_rule_test(sections[sec_key], label, 'l', 'ch')
    lbl, lf, pen, n_lf, n_elig, obs, E, flag, base_pct = r
    print(f"  {lbl:12s}: l-LF N={n_lf}, N_elig={n_elig}, ch@pen: obs={obs}, E={E:.2f}x (base={base_pct:.1f}%), {flag}")

# Full pen distribution for key classes in B herbal and B pharma
print("\n=== Full pen distributions for key classes ===")
for sec_key, label in [('B_herbal','B herbal'), ('B_pharma','B pharma')]:
    print(f"\n{label}:")
    run_full_pen_for_class(sections[sec_key], label, 'qok')
    run_full_pen_for_class(sections[sec_key], label, 'd')
    run_full_pen_for_class(sections[sec_key], label, 'l')

# F460 verification (ot-self@pen) - check B dialect-wide
print("\n--- F460 verification: ot-LF → ot-self@pen (B-dialect-wide) ---")
for sec_key, label in [('B_herbal','B herbal'), ('B_pharma','B pharma'), ('B_astro','B astro')]:
    r = pen_rule_test(sections[sec_key], label, 'ot', 'ot')
    lbl, lf, pen, n_lf, n_elig, obs, E, flag, base_pct = r
    print(f"  {lbl:12s}: ot-LF N={n_lf}, N_elig={n_elig}, ot-self@pen: obs={obs}, E={E:.2f}x (base={base_pct:.1f}%), {flag}")
