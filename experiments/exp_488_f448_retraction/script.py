#!/usr/bin/env python3
"""
exp_488: F448 Retraction Investigation — y-LF N Discrepancy
H_new_BJ: Does exp_476's y-LF N=124 and ok@pos2 obs=20 reproduce with correct methodology?
Definitive: reproduce exp_487 methodology exactly for y-LF, show N_lf and pos2 distribution.
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

# Parse corpus — identical to exp_487
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
print(f"A herbal_a total lines: {len(a_herbal)}")

# Compute y-LF count
y_lf_lines = [(f, ws) for f, ws in a_herbal if ws and get_onset(ws[-1]) == 'y']
print(f"y-LF lines (onset of ws[-1] == 'y'): N = {len(y_lf_lines)}")
print(f"  This is {len(y_lf_lines)/len(a_herbal)*100:.1f}% of A herbal_a lines")
print()

# Show sample y-LF words
from collections import Counter
lf_words = Counter(ws[-1] for _, ws in y_lf_lines)
print("Top y-LF words:")
for w, n in lf_words.most_common(15):
    print(f"  {w}: {n} (onset={get_onset(w)})")
print()

# pos2 baseline for A herbal_a
all_ws_a = [ws for _, ws in a_herbal]
p2_base = defaultdict(int); n_p2 = 0
for ws in all_ws_a:
    if len(ws) >= 2:
        p2_base[get_onset(ws[1])] += 1; n_p2 += 1

print(f"A herbal_a pos2 baseline (total with len>=2): {n_p2}")
print(f"  ok baseline rate: {p2_base['ok']/n_p2:.4f} ({p2_base['ok']/n_p2*100:.2f}%)")
print(f"  y  baseline rate: {p2_base['y']/n_p2:.4f} ({p2_base['y']/n_p2*100:.2f}%)")
print()

# y-LF pos2 distribution — full breakdown
y_elig = [(f, ws) for f, ws in y_lf_lines if len(ws) >= 2]
print(f"y-LF lines with len>=2 (eligible for pos2): N = {len(y_elig)}")

obs_by_onset = defaultdict(int)
for _, ws in y_elig:
    obs_by_onset[get_onset(ws[1])] += 1

# Show all pos2 onsets
rows = []
for onset, obs in sorted(obs_by_onset.items(), key=lambda x: -x[1]):
    base_rate = p2_base.get(onset, 0) / n_p2
    exp = base_rate * len(y_elig)
    E = obs / exp if exp > 0 else float('inf')
    rows.append((onset, obs, exp, E))

print(f"\nFull pos2 distribution for y-LF (N_elig={len(y_elig)}):")
print(f"{'onset':<8} {'obs':>4} {'exp':>6} {'E':>6}  {'flag'}")
print("-"*45)
for onset, obs, exp, E in rows:
    flag = ''
    if obs >= 10 and E >= 1.5: flag = 'CONFIRMED'
    elif obs >= 5 and E >= 2.0: flag = 'dir'
    elif obs >= 3 and E >= 2.0: flag = '(dir)'
    marker = ' <-- SELF' if onset == 'y' else (' <-- WAS F448' if onset == 'ok' else '')
    print(f"  {onset:<6} {obs:>4} {exp:>6.1f} {E:>6.2f}×  {flag}{marker}")

print()
print("="*55)
print("F448 CHECK: ok at pos2 in y-LF lines:")
ok_obs = obs_by_onset.get('ok', 0)
ok_base = p2_base.get('ok', 0) / n_p2
ok_exp = ok_base * len(y_elig)
ok_E = ok_obs / ok_exp if ok_exp > 0 else float('inf')
print(f"  obs={ok_obs}, exp={ok_exp:.1f}, E={ok_E:.2f}×")
print(f"  F448 claimed: obs=20, E=2.25× (CONFIRMED)")
print(f"  Actual: obs={ok_obs} — {'MATCHES F448' if ok_obs >= 15 else 'DOES NOT MATCH F448 (F448 INCORRECT)'}")

print()
print("="*55)
print("y-SELF CHECK: y at pos2 in y-LF lines:")
y_obs = obs_by_onset.get('y', 0)
y_base = p2_base.get('y', 0) / n_p2
y_exp = y_base * len(y_elig)
y_E = y_obs / y_exp if y_exp > 0 else float('inf')
print(f"  obs={y_obs}, exp={y_exp:.1f}, E={y_E:.2f}×")
flag = ''
if y_obs >= 10 and y_E >= 1.5: flag = 'CONFIRMED'
elif y_obs >= 5 and y_E >= 2.0: flag = 'dir'
elif y_obs >= 3 and y_E >= 2.0: flag = '(dir)'
print(f"  Flag: {flag if flag else 'below threshold'}")
print(f"  exp_487 reported: E=7.87×/N=8 (directional)")

print()
print("="*55)
print("FOLIO DIVERSITY CHECK:")
folios_in_y = set(f for f, _ in y_lf_lines)
print(f"  y-LF lines span {len(folios_in_y)} distinct folios")
print(f"  Folios: {sorted(folios_in_y)}")

# Also: what did exp_476 mean by N=124?
# Check: how many lines in A herbal_a have at LEAST ONE y-onset word anywhere?
lines_with_y = [(f, ws) for f, ws in a_herbal
                if any(get_onset(w) == 'y' for w in ws)]
print()
print("="*55)
print("ALTERNATIVE CLASSIFICATIONS (possible exp_476 bugs):")
print(f"  Lines with ANY y-word: {len(lines_with_y)} ({len(lines_with_y)/len(a_herbal)*100:.1f}%)")

# Lines where y appears at pos1 (first word) — maybe exp_476 confused LF with LL?
y_pos1 = [(f, ws) for f, ws in a_herbal if ws and get_onset(ws[0]) == 'y']
print(f"  Lines with y at pos1: {len(y_pos1)}")

# Lines where y appears as LL (next-to-last, i.e., ws[-2]) — maybe confused LF with penultimate?
y_pen = [(f, ws) for f, ws in a_herbal if len(ws) >= 2 and get_onset(ws[-2]) == 'y']
print(f"  Lines with y at pen (ws[-2]): {len(y_pen)}")

# Lines where y appears anywhere except LF (could be a mis-split or routing issue)
# What if exp_476 used LF as the LAST onset word INCLUDING the LF word itself in the pos2 search?
print()
print("Hypothesis: if exp_476 searched ok at pos2 among ALL lines where y appears at LF")
print("  but accidentally included the LF word itself in pos2 computation...")
# Actually the simplest explanation: maybe exp_476 used full-line baseline (not pos2-specific)
# and a y-LF definition that included more lines (e.g., y appears anywhere in line)
