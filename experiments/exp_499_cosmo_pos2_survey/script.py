#!/usr/bin/env python3
"""
exp_499: A cosmo + B cosmo pos2 Grammar Survey
H_new_CC: Do cosmological sections have confirmed pos2 routing rules?
Completes pos2 survey coverage: herbal_a(strong), herbal(moderate), pharma/astro/stars(weak),
cosmo(this exp).
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

def run_pos2_survey(section_lines, label, min_lf=8):
    print(f"\n{'='*60}")
    print(f"=== {label} pos2 Grammar Survey ===")
    print(f"{'='*60}")
    print(f"Total lines: {len(section_lines)}")

    # pos2 baseline (len>=3)
    pos2_counts = defaultdict(int)
    pos2_total = 0
    for fo, ws in section_lines:
        if len(ws) >= 3:
            o = get_onset(ws[1])
            if o:
                pos2_counts[o] += 1
                pos2_total += 1

    print(f"\npos2 baseline (N={pos2_total}, len>=3 lines):")
    pos2_base = {}
    for o in ONSET_PRIORITY:
        c = pos2_counts[o]
        if c > 0:
            pct = c / pos2_total * 100
            pos2_base[o] = c / pos2_total
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

    # pos2 routing for major LF classes
    print(f"\npos2 routing (min LF N={min_lf}):")
    major_lf = [(o, lf_counts[o]) for o in ONSET_PRIORITY if lf_counts[o] >= min_lf]

    summary_selfchain = []

    for lf_onset, lf_n in major_lf:
        lf_lines = [(fo, ws) for fo, ws in section_lines if get_onset(ws[-1]) == lf_onset]
        elig = [(fo, ws) for fo, ws in lf_lines if len(ws) >= 3]
        n_elig = len(elig)

        pos2_dist = defaultdict(int)
        for fo, ws in elig:
            o = get_onset(ws[1])
            if o: pos2_dist[o] += 1

        # Self-chain
        self_obs = pos2_dist.get(lf_onset, 0)
        self_base = pos2_base.get(lf_onset, 0)
        self_exp = self_base * n_elig if self_base > 0 else 0
        self_E = self_obs / self_exp if self_exp > 0 else 0
        self_flag = flag_cell(self_obs, self_E)
        summary_selfchain.append((lf_onset, lf_n, self_obs, n_elig, self_E, self_flag))

        print(f"\n  {lf_onset}-LF (N_lf={lf_n}, N_elig={n_elig}):")
        rows = []
        for o in ONSET_PRIORITY:
            obs = pos2_dist[o]
            base_rate = pos2_base.get(o, 0)
            if base_rate == 0 and obs == 0: continue
            expected = base_rate * n_elig if base_rate > 0 else 0
            E = obs / expected if expected > 0 else float('inf') if obs > 0 else 0
            rows.append((o, obs, expected, E))
        rows.sort(key=lambda x: (-x[3] if x[3] != float('inf') else 1e9))

        for o, obs, exp, E in rows[:6]:
            flag = flag_cell(obs, E) if E != float('inf') else '(uniq)'
            base_pct = pos2_base.get(o, 0) * 100
            E_str = f"{E:.2f}x" if E != float('inf') else "inf"
            self_mark = " <--SELF" if o == lf_onset else ""
            print(f"    {o:8s}: obs={obs:3d}, exp={exp:.1f} (base={base_pct:.1f}%), E={E_str}  {flag}{self_mark}")

        # Show self if not in top 6
        top6 = [r[0] for r in rows[:6]]
        if lf_onset not in top6:
            self_base_pct = self_base * 100
            print(f"    [{lf_onset}-self]: obs={self_obs}, exp={self_exp:.1f}, E={self_E:.2f}x  {self_flag}")

    print(f"\n--- Self-chain summary for {label} ---")
    print(f"{'LF':8s} {'N_lf':6s} {'self':5s} {'N_elig':7s} {'E':8s} {'flag'}")
    for lf_onset, lf_n, self_obs, n_elig, self_E, self_flag in summary_selfchain:
        print(f"{lf_onset:8s} {lf_n:6d} {self_obs:5d} {n_elig:7d} {self_E:8.2f} {self_flag}")

# Print section counts
print("\n=== Section line counts ===")
for k in sorted(sections.keys()):
    print(f"  {k}: {len(sections[k])} lines")

run_pos2_survey(sections['A_cosmo'], 'A cosmo', min_lf=8)
run_pos2_survey(sections['B_cosmo'], 'B cosmo', min_lf=8)
