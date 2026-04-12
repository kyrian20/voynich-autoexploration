#!/usr/bin/env python3
"""
exp_503: F480 Scope — a-LF → y@pos1 in B herbal, B astro, B cosmo
H_new_CI: Is F480 (B pharma a-LF → y@pos1, CONF) B-dialect-wide or B pharma-specific?
Also tests: A herbal_a, A cosmo a-LF → y@pos1 for full picture.
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

def a_lf_pos1_scope(section_lines, label):
    """Focus: a-LF → y@pos1 scope test."""
    # pos1 baseline
    pos1_counts = defaultdict(int)
    pos1_total = 0
    for fo, ws in section_lines:
        o = get_onset(ws[0])
        if o:
            pos1_counts[o] += 1
            pos1_total += 1

    if pos1_total == 0:
        print(f"{label}: NO DATA")
        return

    y_base = pos1_counts['y'] / pos1_total
    y_base_pct = y_base * 100

    # a-LF lines
    a_lf = [(fo, ws) for fo, ws in section_lines if get_onset(ws[-1]) == 'a']
    n_a = len(a_lf)
    if n_a == 0:
        print(f"{label}: a-LF N=0")
        return

    y_obs = sum(1 for fo, ws in a_lf if get_onset(ws[0]) == 'y')
    y_exp = y_base * n_a
    y_E = y_obs / y_exp if y_exp > 0 else 0
    flag = flag_cell(y_obs, y_E)

    # Also check a-self
    a_base = pos1_counts['a'] / pos1_total
    a_self_obs = sum(1 for fo, ws in a_lf if get_onset(ws[0]) == 'a')
    a_self_exp = a_base * n_a
    a_self_E = a_self_obs / a_self_exp if a_self_exp > 0 else 0

    print(f"{label:15s}: a-LF N={n_a:3d} | y@pos1: obs={y_obs}/{n_a} ({y_obs/n_a*100:.1f}%), base={y_base_pct:.1f}%, E={y_E:.2f}x {flag} | a-self: obs={a_self_obs}, E={a_self_E:.2f}x {flag_cell(a_self_obs, a_self_E)}")

    # Print top-5 pos1 for a-LF
    pos1_dist = defaultdict(int)
    for fo, ws in a_lf:
        o = get_onset(ws[0])
        if o: pos1_dist[o] += 1
    rows = []
    for o, cnt in pos1_dist.items():
        base_r = pos1_counts[o] / pos1_total
        E = cnt / (base_r * n_a) if base_r > 0 else float('inf')
        rows.append((o, cnt, E))
    rows.sort(key=lambda x: -x[2])
    top5 = [(o, c, e) for o, c, e in rows[:5]]
    print(f"  Top-5 pos1 for {label} a-LF: " + ", ".join(f"{o}(E={e:.2f}×/N={c})" for o, c, e in top5))

print("=== F480 scope: a-LF → y@pos1 across sections ===\n")
for sec_label in [
    ('A_herbal_a', 'A herbal_a'),
    ('A_cosmo', 'A cosmo'),
    ('A_stars', 'A stars'),
    ('B_herbal', 'B herbal'),
    ('B_pharma', 'B pharma'),
    ('B_astro', 'B astro'),
    ('B_cosmo', 'B cosmo'),
]:
    key, label = sec_label
    if key in sections:
        a_lf_pos1_scope(sections[key], label)
    else:
        print(f"{label:15s}: section not found")

# Also show B combined for a-LF y@pos1
print("\n=== B-dialect combined: a-LF → y@pos1 ===")
b_combined = sections['B_herbal'] + sections['B_pharma'] + sections['B_astro'] + sections['B_cosmo']
a_lf_pos1_scope(b_combined, 'B combined')

print("\n=== A-dialect combined: a-LF → y@pos1 ===")
a_combined = sections['A_herbal_a'] + sections['A_cosmo'] + sections['A_stars']
a_lf_pos1_scope(a_combined, 'A combined')
