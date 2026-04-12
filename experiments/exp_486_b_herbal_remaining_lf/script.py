#!/usr/bin/env python3
"""
exp_486: B herbal Remaining LF Classes — d-LF, y-LF, ok-LF pos1/pos2 Routing
H_new_BF: Cross-dialectal conservation tests for A herbal_a F453 (d→ot@pos1), F448 (y→ok@pos2), F455 (ok→y@pos1)
Also: A herbal_a sh-LF and qot-LF complete routing (H_new_BG)
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

a_herbal = []
b_herbal = []

for folio, lines in folios.items():
    all_words = [w for line in lines for w in line]
    n = folio_num(folio)
    if is_b_dialect(all_words):
        if n <= 72:
            for line in lines:
                b_herbal.append((folio, line))
    else:
        if n <= 56:
            for line in lines:
                a_herbal.append((folio, line))

print(f"A herbal_a: {len(a_herbal)} lines from {len(set(f for f,_ in a_herbal))} folios")
print(f"B herbal:   {len(b_herbal)} lines from {len(set(f for f,_ in b_herbal))} folios")

def flag_cell(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONFIRMED'
    if obs >= 5  and E >= 2.0: return 'dir'
    if obs >= 3  and E >= 2.0: return '(dir)'
    return ''

def full_routing(section_lines, lf_onset, section_label,
                 positions=None, min_obs=2):
    """Full pos1/pos2/pen routing for lf_onset lines with section-specific baselines."""
    all_ws = [ws for _, ws in section_lines]
    N_total = len(all_ws)

    if positions is None:
        positions = [('pos1', 0), ('pos2', 1), ('pen', -2)]

    # Build position-specific baselines
    bases = {}
    for pos_name, idx in positions:
        b = defaultdict(int); nb = 0
        for ws in all_ws:
            if (idx >= 0 and len(ws) > idx) or (idx < 0 and len(ws) >= abs(idx) + 1):
                b[get_onset(ws[idx])] += 1; nb += 1
        bases[pos_name] = (b, nb)

    # LF lines
    lf_lines = [(f, ws) for f, ws in section_lines
                if ws and get_onset(ws[-1]) == lf_onset]
    N_lf = len(lf_lines)

    if N_lf < 5:
        print(f"\n  {section_label} {lf_onset}-LF: N={N_lf} (skip)")
        return {}

    print(f"\n  {section_label} {lf_onset}-LF (N_lf={N_lf}, N_total={N_total}):")

    results = {}
    for pos_name, idx in positions:
        eligible = [(f, ws) for f, ws in lf_lines
                    if (idx >= 0 and len(ws) > idx) or (idx < 0 and len(ws) >= abs(idx) + 1)]
        N_elig = len(eligible)
        if N_elig < 3:
            continue

        obs_by = defaultdict(int)
        for _, ws in eligible:
            obs_by[get_onset(ws[idx])] += 1

        b, nb = bases[pos_name]
        rows = []
        for onset, obs in obs_by.items():
            if obs < min_obs: continue
            exp = b.get(onset, 0) / nb * N_elig if nb > 0 else 0
            E = obs / exp if exp > 0 else float('inf')
            rows.append((onset, obs, exp, E, flag_cell(obs, E)))
        rows.sort(key=lambda x: -x[3])

        print(f"    {pos_name} (N_elig={N_elig}):")
        for onset, obs, exp, E, flg in rows[:6]:
            print(f"      {onset:<6} obs={obs:>3} exp={exp:>5.1f} E={E:>5.2f}× {flg}")

        results[pos_name] = rows

    return results

# ============================================================
print("\n" + "="*60)
print("1. B HERBAL REMAINING LF CLASSES")
print("="*60)
print("\nKnown B herbal confirmed: d→sh(pos2,F457), ch→ch(pos2,F458)")
print("Testing: d-LF pos1 (A has ot, F453), y-LF pos2 (A has ok, F448), ok-LF pos1/pos2")
print("Also: ot-LF pos1 (directional in exp_482)")

print("\n--- B herbal d-LF ---")
full_routing(b_herbal, 'd', 'B herbal')

print("\n--- B herbal y-LF ---")
full_routing(b_herbal, 'y', 'B herbal')

print("\n--- B herbal ok-LF ---")
full_routing(b_herbal, 'ok', 'B herbal')

print("\n--- B herbal ot-LF ---")
full_routing(b_herbal, 'ot', 'B herbal')

# ============================================================
print("\n\n" + "="*60)
print("2. A/B HERBAL CROSS-DIALECTAL COMPARISON TABLE")
print("="*60)
print("\n  Comparing known A herbal_a rules vs B herbal:")
print("  F453: A d-LF → ot@pos1 (1.59×/N=22, CONF)")
print("  F448: A y-LF → ok@pos2 (2.25×/N=20, CONF)")
print("  F455: A ok-LF → y@pos1 (1.62×/N=12, CONF)")

# Compute summary comparison: A vs B for each LF class and position
print("\n  Direct cross-dialectal comparison:")
for lf in ['d', 'y', 'ok', 'ot']:
    for pos_name, idx, key_onset in [('pos1', 0, {'d':'ot','y':'ch','ok':'y','ot':'y'}[lf]),
                                      ('pos2', 1, {'d':'sh','y':'ok','ok':'ok','ot':'sh'}[lf])]:
        for sect_label, sect_lines in [('A herbal_a', a_herbal), ('B herbal', b_herbal)]:
            all_ws = [ws for _, ws in sect_lines]
            b_dist = defaultdict(int); nb = 0
            for ws in all_ws:
                if (idx >= 0 and len(ws) > idx) or (idx < 0 and len(ws) >= abs(idx) + 1):
                    b_dist[get_onset(ws[idx])] += 1; nb += 1

            lf_lines = [(f, ws) for f, ws in sect_lines
                        if ws and get_onset(ws[-1]) == lf]
            eligible = [(f, ws) for f, ws in lf_lines
                        if (idx >= 0 and len(ws) > idx) or (idx < 0 and len(ws) >= abs(idx) + 1)]
            N_elig = len(eligible)
            obs = sum(1 for _, ws in eligible if get_onset(ws[idx]) == key_onset)
            exp = b_dist.get(key_onset, 0) / nb * N_elig if nb > 0 else 0
            E = obs / exp if exp > 0 else float('inf')
            flg = flag_cell(obs, E)
            if N_elig >= 3:
                print(f"  {lf}-LF {key_onset}@{pos_name}: {sect_label}: obs={obs}/{N_elig} E={E:.2f}× {flg}")

# ============================================================
print("\n\n" + "="*60)
print("3. A herbal_a sh-LF AND qot-LF COMPLETE ROUTING")
print("="*60)

print("\n--- A herbal_a sh-LF ---")
full_routing(a_herbal, 'sh', 'A herbal_a')

print("\n--- A herbal_a qot-LF ---")
full_routing(a_herbal, 'qot', 'A herbal_a')

print("\n--- A herbal_a s-LF (bonus: small class) ---")
full_routing(a_herbal, 's', 'A herbal_a')

print("\n--- A herbal_a o-LF ---")
full_routing(a_herbal, 'o', 'A herbal_a')
