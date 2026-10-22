#!/usr/bin/env python3
"""
exp_478: B pharma LF-class Self-Succession at pos1
H_new_AR: Does B pharma have a general rule where LF-class X → X at pos1?
From exp_477: B pharma t-LF → t at pos1 (E=7.99×/N=3, dir).
Test all major LF classes: ok, o, y, t, l, d, sh, ch.
Also compare to B herbal for the same classes.
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

def analyze_self_succession(section_lines, label):
    """For each LF class X, compute E for X at pos1 in X-LF lines."""
    all_lines = [ws for _, ws in section_lines]
    N_total = len(all_lines)
    
    # Build pos1 baseline
    pos1_base = defaultdict(int)
    n1 = 0
    for ws in all_lines:
        if len(ws) >= 2:
            pos1_base[get_onset(ws[0])] += 1
            n1 += 1
    
    # LF-class distribution
    lf_dist = defaultdict(int)
    for ws in all_lines:
        lf_dist[get_onset(ws[-1])] += 1
    
    print(f"\n{'='*60}")
    print(f"{label}: N={N_total} total lines")
    print(f"\nLF-class distribution (top 10):")
    for onset, cnt in sorted(lf_dist.items(), key=lambda x: -x[1])[:10]:
        print(f"  {onset:<6} {cnt:>4} ({cnt/N_total:.1%})")
    
    print(f"\nLF-class self-succession at pos1:")
    print(f"  {'LF':<6} {'N_lf':>6} {'X_obs':>6} {'X_exp':>6} {'E':>6}  {'flag'}")
    
    # Test onset classes with N_lf >= 5
    results = []
    for lf_onset in sorted(lf_dist.keys(), key=lambda x: -lf_dist[x]):
        if lf_dist[lf_onset] < 5:
            continue
        
        # Lines with this LF onset that have >= 2 words
        lf_lines = [(f, ws) for f, ws in section_lines
                    if ws and get_onset(ws[-1]) == lf_onset and len(ws) >= 2]
        N_lf = len(lf_lines)
        if N_lf < 5:
            continue
        
        # Count self at pos1
        obs_self = sum(1 for _, ws in lf_lines if get_onset(ws[0]) == lf_onset)
        
        # Expected: base rate of lf_onset at pos1 * N_lf
        exp_self = pos1_base.get(lf_onset, 0) / n1 * N_lf if n1 > 0 else 0
        
        E = obs_self / exp_self if exp_self > 0 else float('inf')
        
        flag = ''
        if obs_self >= 10 and E >= 1.5: flag = 'CONFIRMED'
        elif obs_self >= 5 and E >= 2.0: flag = 'dir'
        elif obs_self >= 3 and E >= 2.0: flag = '(dir)'
        elif E < 0.5 and obs_self >= 0: flag = 'depleted'
        
        results.append((lf_onset, N_lf, obs_self, exp_self, E, flag))
        print(f"  {lf_onset:<6} {N_lf:>6} {obs_self:>6} {exp_self:>6.1f} {E:>6.2f}x  {flag}")
    
    return results

def analyze_pos1_routing_full(section_lines, lf_onset, label):
    """Full pos1 routing for a specific LF onset (top elevated onsets)."""
    all_lines = [ws for _, ws in section_lines]
    N_total = len(all_lines)
    
    pos1_base = defaultdict(int)
    n1 = 0
    for ws in all_lines:
        if len(ws) >= 2:
            pos1_base[get_onset(ws[0])] += 1
            n1 += 1
    
    lf_lines = [(f, ws) for f, ws in section_lines
                if ws and get_onset(ws[-1]) == lf_onset and len(ws) >= 2]
    N_lf = len(lf_lines)
    
    if N_lf < 5:
        return
    
    pos1_obs = defaultdict(int)
    for _, ws in lf_lines:
        pos1_obs[get_onset(ws[0])] += 1
    
    print(f"\n  {label} (N_lf={N_lf}) — pos1 routing (top 8 elevated):")
    results = []
    for onset, obs in pos1_obs.items():
        exp = pos1_base.get(onset, 0) / n1 * N_lf if n1 > 0 else 0
        E = obs / exp if exp > 0 else float('inf')
        results.append((onset, obs, exp, E))
    for onset, obs, exp, E in sorted(results, key=lambda x: -x[3])[:8]:
        if obs >= 2:
            flag = ''
            if obs >= 10 and E >= 1.5: flag = 'CONFIRMED'
            elif obs >= 5 and E >= 2.0: flag = 'dir'
            elif obs >= 3 and E >= 2.0: flag = '(dir)'
            print(f"    {onset:<6} obs={obs:>3} exp={exp:>5.1f} E={E:>6.2f}x {flag}")

# Main analysis
print("=== B PHARMA: LF-CLASS SELF-SUCCESSION AT pos1 ===")
pharma_results = analyze_self_succession(b_by_section['pharma'], 'B pharma')

print("\n\n=== B HERBAL: LF-CLASS SELF-SUCCESSION AT pos1 (COMPARISON) ===")
herbal_results = analyze_self_succession(b_by_section['herbal'], 'B herbal')

# Full pos1 routing for top pharma LF classes (N_lf >= 15)
print("\n\n=== B PHARMA: FULL pos1 ROUTING FOR MAJOR LF CLASSES ===")
for lf_onset in ['ok','o','y','d','ch','sh','l','s','qok']:
    analyze_pos1_routing_full(b_by_section['pharma'], lf_onset, f'B pharma {lf_onset}-LF')

# Cross-comparison: self-succession in pharma vs herbal
print("\n\n=== CROSS-COMPARISON: PHARMA vs HERBAL SELF-SUCCESSION ===")
print(f"{'LF onset':<8} {'pharma_E':>10} {'pharma_N':>10} {'herbal_E':>10} {'herbal_N':>10}")
# Build dicts from results
p_dict = {r[0]: r for r in pharma_results}
h_dict = {r[0]: r for r in herbal_results}
for onset in ['ok','o','y','d','ch','sh','l','s','qok','t']:
    pr = p_dict.get(onset)
    hr = h_dict.get(onset)
    p_str = f"{pr[4]:.2f}×(N={pr[2]})" if pr else "—"
    h_str = f"{hr[4]:.2f}×(N={hr[2]})" if hr else "—"
    print(f"  {onset:<8} {p_str:>14} {h_str:>14}")
