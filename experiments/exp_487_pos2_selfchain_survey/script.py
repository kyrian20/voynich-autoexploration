#!/usr/bin/env python3
"""
exp_487: A herbal_a pos2 Self-Chaining Survey + Scope Tests for sh/o
H_new_BH: Is pos2 self-chaining universal across all A herbal_a LF classes?
H_new_BI: Are sh→sh@pos2 and o→o@pos2 herbal-section-specific (like ch)?
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

def pos2_selfchain(section_lines, lf_onset, section_label):
    """Test: LF-onset self-chaining at pos2 with section-specific pos2 baseline."""
    all_ws = [ws for _, ws in section_lines]

    # pos2 baseline
    p2_base = defaultdict(int); n_p2 = 0
    for ws in all_ws:
        if len(ws) >= 2:
            p2_base[get_onset(ws[1])] += 1; n_p2 += 1

    base_rate = p2_base.get(lf_onset, 0) / n_p2 if n_p2 > 0 else 0

    # LF lines
    lf_lines = [(f, ws) for f, ws in section_lines
                if ws and get_onset(ws[-1]) == lf_onset]
    N_lf = len(lf_lines)

    # Eligible for pos2 (len >= 2)
    elig = [(f, ws) for f, ws in lf_lines if len(ws) >= 2]
    N_elig = len(elig)

    if N_elig < 5:
        return (lf_onset, N_lf, 0, 0, 0, 0, '')

    obs = sum(1 for _, ws in elig if get_onset(ws[1]) == lf_onset)
    exp = base_rate * N_elig
    E = obs / exp if exp > 0 else float('inf')
    flg = flag_cell(obs, E)

    return (lf_onset, N_lf, obs, N_elig, base_rate, E, flg)

# ============================================================
print("="*70)
print("1. A herbal_a pos2 SELF-CHAINING: ALL LF CLASSES")
print("="*70)
print("Testing: does LF-onset appear at pos2 above baseline for every LF class?")
print("Known CONFIRMED: ch(E=1.60×/N=94), sh(E=2.64×/N=12), o(E=7.03×/N=10)")
print()

a_herbal = sections['A_herbal_a']
all_ws_a = [ws for _, ws in a_herbal]

# pos2 baseline for A herbal_a
p2_base_a = defaultdict(int); n_p2_a = 0
for ws in all_ws_a:
    if len(ws) >= 2:
        p2_base_a[get_onset(ws[1])] += 1; n_p2_a += 1

print("A herbal_a pos2 baseline (top onsets):")
top_p2 = sorted(p2_base_a.items(), key=lambda x: -x[1])[:10]
for o, n in top_p2:
    print(f"  {o:<6}: {n/n_p2_a:.3f} ({n/n_p2_a*100:.1f}%)")

print()
print(f"{'LF onset':<8} {'N_lf':>6} {'obs':>5} {'N_elig':>7} {'base%':>7} {'E':>6}  {'Flag'}")
print("-"*60)

lf_classes = []
for lf_onset, count in sorted(((get_onset(ws[-1]), 1) for _, ws in a_herbal if ws),
                                 key=lambda x: x[0]):
    pass

# Get LF distribution
lf_dist = defaultdict(int)
for _, ws in a_herbal:
    if ws:
        lf_dist[get_onset(ws[-1])] += 1

for lf_onset in sorted(lf_dist.keys(), key=lambda x: -lf_dist[x]):
    if lf_dist[lf_onset] < 10:
        continue
    result = pos2_selfchain(a_herbal, lf_onset, 'A herbal_a')
    lf_onset, N_lf, obs, N_elig, base_rate, E, flg = result
    marker = ' *** CONFIRMED' if flg == 'CONFIRMED' else (' dir' if flg == 'dir' else (' (dir)' if flg == '(dir)' else ''))
    print(f"  {lf_onset:<8} {N_lf:>6} {obs:>5} {N_elig:>7} {base_rate*100:>6.1f}% {E:>6.2f}×{marker}")

# ============================================================
print("\n\n" + "="*70)
print("2. SCOPE TEST: sh/o pos2 self-chaining across sections")
print("="*70)
print("Testing: B pharma, B astro, A cosmo, B herbal for sh-LF and o-LF")

for lf_onset in ['sh', 'o']:
    print(f"\n  LF onset: {lf_onset}")
    print(f"  {'Section':<16} {'N_lf':>6} {'obs':>5} {'N_elig':>7} {'base%':>7} {'E':>6}  {'Flag'}")
    print("  " + "-"*58)

    for sec_label in ['A_herbal_a', 'B_herbal', 'B_pharma', 'B_astro', 'A_cosmo', 'B_cosmo']:
        if sec_label not in sections:
            continue
        result = pos2_selfchain(sections[sec_label], lf_onset, sec_label)
        lfo, N_lf, obs, N_elig, base_rate, E, flg = result
        if N_lf < 5:
            print(f"  {sec_label:<16} {N_lf:>6} (skip)")
            continue
        marker = ' *** CONFIRMED' if flg == 'CONFIRMED' else (' dir' if flg == 'dir' else (' (dir)' if flg == '(dir)' else ''))
        print(f"  {sec_label:<16} {N_lf:>6} {obs:>5} {N_elig:>7} {base_rate*100:>6.1f}% {E:>6.2f}×{marker}")

# ============================================================
print("\n\n" + "="*70)
print("3. FULL pos2 DISTRIBUTION for key LF classes (all onsets at pos2)")
print("   For LF classes WITHOUT self-chaining: what IS at pos2?")
print("="*70)

def pos2_full(section_lines, lf_onset, section_label):
    """Show top pos2 onsets for given LF class."""
    all_ws = [ws for _, ws in section_lines]
    p2_base = defaultdict(int); n_p2 = 0
    for ws in all_ws:
        if len(ws) >= 2:
            p2_base[get_onset(ws[1])] += 1; n_p2 += 1

    lf_lines = [(f, ws) for f, ws in section_lines
                if ws and get_onset(ws[-1]) == lf_onset and len(ws) >= 2]
    N_elig = len(lf_lines)
    if N_elig < 5:
        return

    obs_by = defaultdict(int)
    for _, ws in lf_lines:
        obs_by[get_onset(ws[1])] += 1

    rows = []
    for onset, obs in obs_by.items():
        if obs < 2: continue
        exp = p2_base.get(onset, 0) / n_p2 * N_elig if n_p2 > 0 else 0
        E = obs / exp if exp > 0 else float('inf')
        rows.append((onset, obs, exp, E, flag_cell(obs, E)))
    rows.sort(key=lambda x: -x[3])

    self_obs = obs_by.get(lf_onset, 0)
    self_base = p2_base.get(lf_onset, 0) / n_p2 if n_p2 > 0 else 0
    self_exp = self_base * N_elig
    self_E = self_obs / self_exp if self_exp > 0 else float('inf')

    print(f"\n  {section_label} {lf_onset}-LF pos2 (N={N_elig}):")
    print(f"  Self ({lf_onset}) at pos2: obs={self_obs}/{N_elig} ({self_obs/N_elig*100:.1f}%) E={self_E:.2f}×")
    for onset, obs, exp, E, flg in rows[:6]:
        marker = ' <-- self' if onset == lf_onset else ''
        print(f"    {onset:<6} obs={obs:>3}/{N_elig} ({obs/N_elig*100:.1f}%) exp={exp:>5.1f} E={E:>5.2f}× {flg}{marker}")

for lf_onset in ['d', 'y', 'ok', 'ot', 'qot']:
    pos2_full(a_herbal, lf_onset, 'A herbal_a')
