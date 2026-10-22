#!/usr/bin/env python3
"""
exp_500: A cosmo pos1 Grammar Survey
H_new_CF: Does A cosmo have confirmed pos1 routing rules?
A cosmo pos2 had no confirmed rules (exp_499). Test if pos1 is also weak.
Key test: does ot→y@pos1 (F476 herbal-register-wide) hold in A cosmo?
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
    if obs == 0: return 'zero'
    return ''

def run_pos1_survey(section_lines, label, min_lf=8):
    print(f"\n{'='*60}")
    print(f"=== {label} pos1 Grammar Survey ===")
    print(f"{'='*60}")
    print(f"Total lines: {len(section_lines)}")

    # pos1 baseline (all lines with len>=1, pos1=ws[0])
    pos1_counts = defaultdict(int)
    pos1_total = 0
    for fo, ws in section_lines:
        if len(ws) >= 1:
            o = get_onset(ws[0])
            if o:
                pos1_counts[o] += 1
                pos1_total += 1

    print(f"\npos1 baseline (N={pos1_total}, all lines):")
    pos1_base = {}
    for o in ONSET_PRIORITY:
        c = pos1_counts[o]
        if c > 0:
            pct = c / pos1_total * 100
            pos1_base[o] = c / pos1_total
            if pct >= 1.5:
                print(f"  {o}: {c} ({pct:.1f}%)")

    # LF distribution
    lf_counts = defaultdict(int)
    for fo, ws in section_lines:
        o = get_onset(ws[-1])
        if o: lf_counts[o] += 1
    lf_total = sum(lf_counts.values())
    print(f"\nLF distribution (N={lf_total}, top 10):")
    for o in sorted(lf_counts, key=lambda x: -lf_counts[x])[:10]:
        pct = lf_counts[o] / lf_total * 100
        print(f"  {o}: {lf_counts[o]} ({pct:.1f}%)")

    # pos1 routing for major LF classes
    print(f"\npos1 routing (min LF N={min_lf}):")
    major_lf = [(o, lf_counts[o]) for o in ONSET_PRIORITY if lf_counts[o] >= min_lf]

    summary_selfchain = []

    for lf_onset, lf_n in major_lf:
        lf_lines = [(fo, ws) for fo, ws in section_lines if get_onset(ws[-1]) == lf_onset]
        n_elig = len(lf_lines)  # pos1: all lines eligible (ws[0] always exists)

        pos1_dist = defaultdict(int)
        for fo, ws in lf_lines:
            o = get_onset(ws[0])
            if o: pos1_dist[o] += 1

        # Self-chain
        self_obs = pos1_dist.get(lf_onset, 0)
        self_base = pos1_base.get(lf_onset, 0)
        self_exp = self_base * n_elig if self_base > 0 else 0
        self_E = self_obs / self_exp if self_exp > 0 else 0
        self_flag = flag_cell(self_obs, self_E)
        summary_selfchain.append((lf_onset, lf_n, self_obs, n_elig, self_E, self_flag))

        print(f"\n  {lf_onset}-LF (N_lf={lf_n}, N_elig={n_elig}):")
        rows = []
        for o in ONSET_PRIORITY:
            obs = pos1_dist[o]
            base_rate = pos1_base.get(o, 0)
            if base_rate == 0 and obs == 0: continue
            expected = base_rate * n_elig if base_rate > 0 else 0
            E = obs / expected if expected > 0 else float('inf') if obs > 0 else 0
            rows.append((o, obs, expected, E))
        rows.sort(key=lambda x: (-x[3] if x[3] != float('inf') else 1e9))

        for o, obs, exp, E in rows[:8]:
            flag = flag_cell(obs, E) if E != float('inf') else '(uniq)'
            base_pct = pos1_base.get(o, 0) * 100
            E_str = f"{E:.2f}x" if E != float('inf') else "inf"
            self_mark = " <--SELF" if o == lf_onset else ""
            print(f"    {o:8s}: obs={obs:3d}, exp={exp:.1f} (base={base_pct:.1f}%), E={E_str}  {flag}{self_mark}")

        # Show self if not in top 8
        top8 = [r[0] for r in rows[:8]]
        if lf_onset not in top8:
            self_base_pct = self_base * 100
            print(f"    [{lf_onset}-self]: obs={self_obs}, exp={self_exp:.1f}, E={self_E:.2f}x  {self_flag}")

        # Also show y and ot explicitly for herbal-register context (F476 test)
        for key_onset in ['y', 'ot', 'd']:
            if key_onset not in top8 and key_onset != lf_onset:
                obs = pos1_dist[key_onset]
                base_rate = pos1_base.get(key_onset, 0)
                if base_rate > 0:
                    exp = base_rate * n_elig
                    E = obs / exp if exp > 0 else 0
                    flag = flag_cell(obs, E)
                    print(f"    [{key_onset}@pos1]: obs={obs}, exp={exp:.1f}, E={E:.2f}x  {flag}")

    print(f"\n--- Self-chain summary for {label} ---")
    print(f"{'LF':8s} {'N_lf':6s} {'self':5s} {'N_elig':7s} {'E':8s} {'flag'}")
    for lf_onset, lf_n, self_obs, n_elig, self_E, self_flag in summary_selfchain:
        print(f"{lf_onset:8s} {lf_n:6d} {self_obs:5d} {n_elig:7d} {self_E:8.2f} {self_flag}")

run_pos1_survey(sections['A_cosmo'], 'A cosmo', min_lf=8)

# Also run A herbal_a for comparison (abbreviated)
print("\n\n=== A herbal_a pos1 comparison (key classes only) ===")
herbal_lines = sections['A_herbal_a']
pos1_counts_h = defaultdict(int)
pos1_total_h = 0
for fo, ws in herbal_lines:
    if len(ws) >= 1:
        o = get_onset(ws[0])
        if o:
            pos1_counts_h[o] += 1
            pos1_total_h += 1
pos1_base_h = {o: pos1_counts_h[o]/pos1_total_h for o in pos1_counts_h}

lf_counts_h = defaultdict(int)
for fo, ws in herbal_lines:
    o = get_onset(ws[-1])
    if o: lf_counts_h[o] += 1

print(f"A herbal_a pos1 baseline: y={pos1_counts_h.get('y',0)/pos1_total_h*100:.1f}%, ch={pos1_counts_h.get('ch',0)/pos1_total_h*100:.1f}%")
print(f"A herbal_a LF: d={lf_counts_h.get('d',0)}, ch={lf_counts_h.get('ch',0)}, ok={lf_counts_h.get('ok',0)}, ot={lf_counts_h.get('ot',0)}")
for lf_key in ['ot', 'ok', 'ch', 'd']:
    lf_lines_h = [(fo, ws) for fo, ws in herbal_lines if get_onset(ws[-1]) == lf_key]
    if not lf_lines_h: continue
    y_obs = sum(1 for fo, ws in lf_lines_h if get_onset(ws[0]) == 'y')
    y_base = pos1_base_h.get('y', 0)
    y_exp = y_base * len(lf_lines_h)
    y_E = y_obs / y_exp if y_exp > 0 else 0
    ch_obs = sum(1 for fo, ws in lf_lines_h if get_onset(ws[0]) == 'ch')
    ch_base = pos1_base_h.get('ch', 0)
    ch_exp = ch_base * len(lf_lines_h)
    ch_E = ch_obs / ch_exp if ch_exp > 0 else 0
    print(f"  {lf_key}-LF (N={len(lf_lines_h)}): y@pos1=obs{y_obs}/exp{y_exp:.1f}=E{y_E:.2f}x  ch@pos1=obs{ch_obs}/exp{ch_exp:.1f}=E{ch_E:.2f}x")
