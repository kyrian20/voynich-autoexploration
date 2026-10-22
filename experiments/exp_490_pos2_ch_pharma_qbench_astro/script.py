#!/usr/bin/env python3
"""
exp_490: B pharma ch@pos2 universality + B astro q-bench pos2 self-chaining
H_new_BO: Is ch@pos2 universally elevated in B pharma regardless of LF class?
H_new_BN: Does pos2 self-chaining hold for B astro q-bench (qok/qot/qo) LF classes?
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

# ============================================================
print("="*65)
print("1. B PHARMA ch@pos2: Universal for all LF classes? (H_new_BO)")
print("   Hypothesis: ch appears at pos2 above baseline in EVERY LF class")
print("   (B pharma's mirror-opposite to A herbal_a's self-chaining)")
print("="*65)

b_pharma = sections['B_pharma']
all_ws_bp = [ws for _, ws in b_pharma]
p2_base_bp = defaultdict(int); n_p2_bp = 0
for ws in all_ws_bp:
    if len(ws) >= 2:
        p2_base_bp[get_onset(ws[1])] += 1; n_p2_bp += 1

ch_base_bp = p2_base_bp.get('ch', 0) / n_p2_bp
print(f"B pharma pos2 ch baseline rate: {ch_base_bp:.4f} ({ch_base_bp*100:.2f}%)")
print()

lf_dist_bp = defaultdict(int)
for _, ws in b_pharma:
    if ws:
        lf_dist_bp[get_onset(ws[-1])] += 1

print(f"{'LF onset':<8} {'N_lf':>6} {'N_elig':>7} {'obs_ch':>7} {'base%':>7} {'E':>7}  {'flag'}")
print("-"*60)

b_pharma_ch_results = []
for lf_onset in sorted(lf_dist_bp.keys(), key=lambda x: -lf_dist_bp[x]):
    N_lf = lf_dist_bp[lf_onset]
    if N_lf < 8:
        continue
    lf_lines = [(f, ws) for f, ws in b_pharma
                if ws and get_onset(ws[-1]) == lf_onset]
    elig = [(f, ws) for f, ws in lf_lines if len(ws) >= 2]
    N_elig = len(elig)
    if N_elig < 5:
        continue
    obs = sum(1 for _, ws in elig if get_onset(ws[1]) == 'ch')
    exp = ch_base_bp * N_elig
    E = obs / exp if exp > 0 else float('inf')
    flg = flag_cell(obs, E)
    marker = ''
    if flg == 'CONFIRMED': marker = ' CONFIRMED'
    elif flg == 'dir': marker = ' dir'
    elif flg == '(dir)': marker = ' (dir)'
    self_note = ' [ch is LF]' if lf_onset == 'ch' else ''
    print(f"  {lf_onset:<8} {N_lf:>6} {N_elig:>7} {obs:>7} {ch_base_bp*100:>6.2f}% {E:>6.2f}×{marker}{self_note}")
    b_pharma_ch_results.append((lf_onset, N_lf, N_elig, obs, E, flg))

# Summary
n_conf = sum(1 for _, _, _, _, E, flg in b_pharma_ch_results if flg == 'CONFIRMED')
n_dir = sum(1 for _, _, _, _, E, flg in b_pharma_ch_results if flg in ('dir', '(dir)'))
n_below = sum(1 for _, _, _, _, E, flg in b_pharma_ch_results if flg == '')
print(f"\nSummary: CONFIRMED={n_conf}, dir/dir={n_dir}, below threshold={n_below}")
print(f"ch@pos2 E≥1.5× in {sum(1 for _,_,_,_,E,_ in b_pharma_ch_results if E>=1.5)} of {len(b_pharma_ch_results)} tested LF classes")

# ============================================================
print("\n\n" + "="*65)
print("2. B ASTRO pos2 Self-Chaining: q-bench classes (H_new_BN)")
print("   Known: sh→sh@pos2 CONF (F469)")
print("   Test: qok/qot/qo/s/d LF pos2 self-chaining")
print("="*65)

b_astro = sections['B_astro']
all_ws_ba = [ws for _, ws in b_astro]
p2_base_ba = defaultdict(int); n_p2_ba = 0
for ws in all_ws_ba:
    if len(ws) >= 2:
        p2_base_ba[get_onset(ws[1])] += 1; n_p2_ba += 1

print(f"B astro pos2 baseline (top 8):")
for o, n in sorted(p2_base_ba.items(), key=lambda x: -x[1])[:8]:
    print(f"  {o:<6}: {n/n_p2_ba:.3f} ({n/n_p2_ba*100:.1f}%)")

lf_dist_ba = defaultdict(int)
for _, ws in b_astro:
    if ws:
        lf_dist_ba[get_onset(ws[-1])] += 1

print(f"\nB astro LF distribution (top 8):")
for o, n in sorted(lf_dist_ba.items(), key=lambda x: -x[1])[:8]:
    print(f"  {o:<6}: {n}")

print()
print(f"{'LF onset':<8} {'N_lf':>6} {'N_elig':>7} {'obs':>5} {'base%':>7} {'E':>7}  {'flag'}")
print("-"*60)

for lf_onset in sorted(lf_dist_ba.keys(), key=lambda x: -lf_dist_ba[x]):
    N_lf = lf_dist_ba[lf_onset]
    if N_lf < 5:
        continue
    lf_lines = [(f, ws) for f, ws in b_astro
                if ws and get_onset(ws[-1]) == lf_onset]
    elig = [(f, ws) for f, ws in lf_lines if len(ws) >= 2]
    N_elig = len(elig)
    if N_elig < 5:
        continue
    obs = sum(1 for _, ws in elig if get_onset(ws[1]) == lf_onset)
    base_rate = p2_base_ba.get(lf_onset, 0) / n_p2_ba if n_p2_ba > 0 else 0
    exp = base_rate * N_elig
    E = obs / exp if exp > 0 else float('inf')
    flg = flag_cell(obs, E)
    marker = ''
    if flg == 'CONFIRMED': marker = ' CONFIRMED'
    elif flg == 'dir': marker = ' dir'
    elif flg == '(dir)': marker = ' (dir)'
    known = ' (F469)' if lf_onset == 'sh' else ''
    print(f"  {lf_onset:<8} {N_lf:>6} {N_elig:>7} {obs:>5} {base_rate*100:>6.1f}% {E:>6.2f}×{marker}{known}")

# Full pos2 distribution for qok-LF (largest B astro class)
print()
print("="*65)
print("B astro qok-LF: Full pos2 distribution (N=149, largest class)")
print("="*65)
qok_lf_ba = [(f, ws) for f, ws in b_astro if ws and get_onset(ws[-1]) == 'qok']
qok_elig_ba = [(f, ws) for f, ws in qok_lf_ba if len(ws) >= 2]
print(f"N_lf={len(qok_lf_ba)}, N_elig={len(qok_elig_ba)}")

obs_qok = defaultdict(int)
for _, ws in qok_elig_ba:
    obs_qok[get_onset(ws[1])] += 1

rows = []
for onset, obs in sorted(obs_qok.items(), key=lambda x: -x[1]):
    if obs < 2: continue
    base = p2_base_ba.get(onset, 0) / n_p2_ba
    exp = base * len(qok_elig_ba)
    E = obs / exp if exp > 0 else float('inf')
    flg = flag_cell(obs, E)
    rows.append((onset, obs, exp, E, flg))

print(f"{'onset':<6} {'obs':>4} {'exp':>6} {'E':>6}  flag")
for onset, obs, exp, E, flg in rows:
    marker = ' <-- SELF' if onset == 'qok' else ''
    print(f"  {onset:<6} {obs:>4} {exp:>6.1f} {E:>6.2f}×  {flg}{marker}")

# ============================================================
print("\n\n" + "="*65)
print("3. A herbal_a pos2 baseline comparison: what IS at pos2?")
print("   Context: A herbal_a self-chains; what does pos2 look like globally?")
print("="*65)

a_herbal = sections['A_herbal_a']
all_ws_ah = [ws for _, ws in a_herbal]
p2_base_ah = defaultdict(int); n_p2_ah = 0
for ws in all_ws_ah:
    if len(ws) >= 2:
        p2_base_ah[get_onset(ws[1])] += 1; n_p2_ah += 1

print("A herbal_a pos2 distribution vs B pharma pos2 distribution:")
print(f"{'onset':<6} {'A herbal_a':>12} {'B pharma':>10}")
all_onsets = sorted(set(list(p2_base_ah.keys()) + list(p2_base_bp.keys())),
                    key=lambda x: -(p2_base_ah.get(x, 0)/n_p2_ah + p2_base_bp.get(x,0)/n_p2_bp)/2)[:12]
for onset in all_onsets:
    ra = p2_base_ah.get(onset, 0) / n_p2_ah
    rb = p2_base_bp.get(onset, 0) / n_p2_bp
    print(f"  {onset:<6} {ra*100:>10.1f}% {rb*100:>8.1f}%")
