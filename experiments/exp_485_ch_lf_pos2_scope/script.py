#!/usr/bin/env python3
"""
exp_485: ch-LF → ch at pos2 Scope Test Across All Major Sections
H_new_BB: Is ch self-chaining at pos2 (F461+F458) herbal-specific or universal?

Tests: B pharma, B astro, A stars, A cosmo, B cosmo, A herbal_b
Also: d-LF → ch at pos2 (B herbal F457 uses sh at pos2; does A herbal_a d-LF have anything at pos2?)
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

# Build section corpora
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

# Print section sizes
print("Section sizes:")
for sec, lines in sorted(sections.items()):
    print(f"  {sec}: {len(lines)} lines from {len(set(f for f,_ in lines))} folios")

def flag_cell(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONFIRMED'
    if obs >= 5  and E >= 2.0: return 'dir'
    if obs >= 3  and E >= 2.0: return '(dir)'
    return ''

def analyze_ch_pos2(section_lines, section_label):
    """Compute ch-LF → ch at pos2 with section-specific pos2 baseline."""
    all_ws = [ws for _, ws in section_lines]
    N_total = len(all_ws)

    # pos2 baseline (ws[1]) for all lines with >= 2 words
    pos2_base = defaultdict(int); n_p2 = 0
    for ws in all_ws:
        if len(ws) >= 2:
            pos2_base[get_onset(ws[1])] += 1; n_p2 += 1

    ch_base_p2 = pos2_base.get('ch', 0) / n_p2 if n_p2 > 0 else 0

    # ch-LF lines
    ch_lf = [(f, ws) for f, ws in section_lines
             if ws and get_onset(ws[-1]) == 'ch']
    N_lf = len(ch_lf)

    if N_lf < 5:
        print(f"\n  {section_label}: ch-LF N={N_lf} (skip)")
        return None

    # ch at pos2 in ch-LF lines
    p2_eligible = [(f, ws) for f, ws in ch_lf if len(ws) >= 2]
    N_p2 = len(p2_eligible)
    ch_obs = sum(1 for _, ws in p2_eligible if get_onset(ws[1]) == 'ch')
    ch_exp = ch_base_p2 * N_p2
    ch_E = ch_obs / ch_exp if ch_exp > 0 else 0
    flg = flag_cell(ch_obs, ch_E)

    print(f"\n  {section_label}: ch-LF (N_lf={N_lf}, N_total={N_total})")
    print(f"    pos2 ch baseline: {ch_base_p2:.3f} ({ch_base_p2*100:.1f}%)")
    print(f"    ch at pos2: obs={ch_obs}/{N_p2} ({ch_obs/N_p2*100:.1f}%) exp={ch_exp:.1f} E={ch_E:.2f}× {flg}")

    # Also show top pos2 onsets for context
    obs_by_onset = defaultdict(int)
    for _, ws in p2_eligible:
        obs_by_onset[get_onset(ws[1])] += 1
    top_onsets = sorted(obs_by_onset.items(), key=lambda x: -x[1])[:5]
    top_str = ' | '.join(f"{o}:{n}" for o, n in top_onsets)
    print(f"    pos2 distribution: {top_str}")

    return (N_lf, ch_obs, ch_exp, ch_E, flg)

# ============================================================
print("\n" + "="*60)
print("1. ch-LF → ch at pos2: SCOPE TEST ACROSS ALL SECTIONS")
print("="*60)
print("  Known: A herbal_a F461 E=1.60×/N=94 | B herbal F458 E=1.74×/N=19")

results = {}
for sec_label in ['A_herbal_a', 'B_herbal', 'B_pharma', 'B_astro', 'A_stars', 'A_cosmo', 'B_cosmo', 'A_herbal_b']:
    if sec_label in sections:
        r = analyze_ch_pos2(sections[sec_label], sec_label)
        if r: results[sec_label] = r

# Summary table
print("\n\nSUMMARY TABLE: ch-LF → ch at pos2")
print(f"{'Section':<16} {'N_lf':>6} {'obs':>5} {'exp':>6} {'E':>6}  {'Flag'}")
print("-"*55)
known = {
    'A_herbal_a': (178, 94, 58.7, 1.60, 'CONFIRMED (F461)'),
    'B_herbal':   (48, 19, 10.9, 1.74, 'CONFIRMED (F458)'),
}
for sec, (N, obs, exp, E, flg) in known.items():
    print(f"  {sec:<14} {N:>6} {obs:>5} {exp:>6.1f} {E:>6.2f}×  {flg}")
for sec, (N, obs, exp, E, flg) in results.items():
    if sec not in known:
        status = flg if flg else f'E={E:.2f}×'
        print(f"  {sec:<14} {N:>6} {obs:>5} {exp:>6.1f} {E:>6.2f}×  {status}")

# ============================================================
print("\n\n" + "="*60)
print("2. ALSO: B pharma ch-LF pos1 self-succession (F449 replication)")
print("   and full pos2 profile for B pharma ch-LF")
print("="*60)

def full_pos_profile(section_lines, lf_onset, section_label, positions=None):
    """Full positional profile for lf_onset lines."""
    all_ws = [ws for _, ws in section_lines]

    if positions is None:
        positions = [('pos1', 0), ('pos2', 1), ('pen', -2)]

    # Baselines
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
        print(f"  {section_label} {lf_onset}-LF: N={N_lf} (skip)")
        return

    print(f"\n  {section_label} {lf_onset}-LF (N={N_lf}):")

    for pos_name, idx in positions:
        eligible = [(f, ws) for f, ws in lf_lines
                    if (idx >= 0 and len(ws) > idx) or (idx < 0 and len(ws) >= abs(idx) + 1)]
        N_elig = len(eligible)
        obs_by = defaultdict(int)
        for _, ws in eligible:
            obs_by[get_onset(ws[idx])] += 1

        b, nb = bases[pos_name]
        rows = []
        for onset, obs in obs_by.items():
            if obs < 2: continue
            exp = b.get(onset, 0) / nb * N_elig if nb > 0 else 0
            E = obs / exp if exp > 0 else float('inf')
            rows.append((onset, obs, exp, E, flag_cell(obs, E)))
        rows.sort(key=lambda x: -x[3])

        print(f"    {pos_name} (N_elig={N_elig}):")
        for onset, obs, exp, E, flg in rows[:5]:
            print(f"      {onset:<6} obs={obs:>3} exp={exp:>5.1f} E={E:>5.2f}× {flg}")

full_pos_profile(sections.get('B_pharma', []), 'ch', 'B pharma', [('pos1',0),('pos2',1)])

# ============================================================
print("\n\n" + "="*60)
print("3. A herbal_a d-LF FULL PEN PROFILE (correct ws[-2] baseline)")
print("   Testing: what IS at pen for d-LF lines with correct baselines?")
print("="*60)

def full_pen_profile(section_lines, lf_onset, section_label):
    """Full pen (ws[-2]) onset profile for lf_onset lines with correct pen baseline."""
    all_ws = [ws for _, ws in section_lines]

    # Correct pen baseline: ws[-2] for lines with >= 3 words
    pen_base = defaultdict(int); n_pen = 0
    for ws in all_ws:
        if len(ws) >= 3:
            pen_base[get_onset(ws[-2])] += 1; n_pen += 1

    # LF lines with >= 3 words (pen-eligible)
    lf_lines = [(f, ws) for f, ws in section_lines
                if ws and get_onset(ws[-1]) == lf_onset and len(ws) >= 3]
    N_lf = len(lf_lines)

    if N_lf < 5:
        print(f"  {section_label} {lf_onset}-LF pen: N={N_lf} (skip)")
        return

    obs_by = defaultdict(int)
    for _, ws in lf_lines:
        obs_by[get_onset(ws[-2])] += 1

    rows = []
    for onset, obs in obs_by.items():
        if obs < 2: continue
        exp = pen_base.get(onset, 0) / n_pen * N_lf if n_pen > 0 else 0
        E = obs / exp if exp > 0 else float('inf')
        rows.append((onset, obs, exp, E, flag_cell(obs, E)))
    rows.sort(key=lambda x: -x[3])

    # Print pen baseline for key onsets
    print(f"\n  {section_label} {lf_onset}-LF (pen-eligible N={N_lf}):")
    print(f"  Pen baseline (ws[-2] distribution, top onsets):")
    top_base = sorted(pen_base.items(), key=lambda x: -x[1])[:8]
    base_str = ' | '.join(f"{o}:{pen_base[o]/n_pen:.3f}" for o,_ in top_base)
    print(f"    {base_str}")
    print(f"  Pen enrichment (all obs >= 2):")
    for onset, obs, exp, E, flg in rows[:10]:
        print(f"    {onset:<6} obs={obs:>3}/{N_lf} ({obs/N_lf*100:.1f}%) exp={exp:>5.1f} ({exp/N_lf*100:.1f}%) E={E:>5.2f}× {flg}")

full_pen_profile(sections.get('A_herbal_a', []), 'd', 'A herbal_a')
full_pen_profile(sections.get('A_herbal_a', []), 'ch', 'A herbal_a')

# ============================================================
print("\n\n" + "="*60)
print("4. B pharma F450/F451/F452 VALIDATION with correct pen baseline")
print("   (ws[-2] pen baseline)")
print("="*60)

full_pen_profile(sections.get('B_pharma', []), 'ot', 'B pharma')
full_pen_profile(sections.get('B_pharma', []), 'l', 'B pharma')
full_pen_profile(sections.get('B_pharma', []), 'ok', 'B pharma')
