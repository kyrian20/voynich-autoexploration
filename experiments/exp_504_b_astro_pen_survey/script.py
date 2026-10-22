#!/usr/bin/env python3
"""
exp_504: B astro pen Grammar Survey
H_new_CE: Is B astro pen grammar stronger than its weak pos2?
F459 (ok→a@pen) is B-dialect-wide — test if it holds + find other rules.
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

def run_pen_survey(section_lines, label, min_lf=10):
    print(f"\n{'='*60}")
    print(f"=== {label} pen Grammar Survey ===")
    print(f"{'='*60}")
    print(f"Total lines: {len(section_lines)}")

    # pen baseline (len>=3, pen=ws[-2])
    pen_counts = defaultdict(int)
    pen_total = 0
    for fo, ws in section_lines:
        if len(ws) >= 3:
            o = get_onset(ws[-2])
            if o:
                pen_counts[o] += 1
                pen_total += 1

    print(f"\npen baseline (N={pen_total}, len>=3 lines):")
    pen_base = {}
    for o in ONSET_PRIORITY:
        c = pen_counts[o]
        if c > 0:
            pct = c / pen_total * 100
            pen_base[o] = c / pen_total
            if pct >= 1.5:
                print(f"  {o}: {c} ({pct:.1f}%)")

    lf_counts = defaultdict(int)
    for fo, ws in section_lines:
        o = get_onset(ws[-1])
        if o: lf_counts[o] += 1
    lf_total = sum(lf_counts.values())
    print(f"\nLF distribution (N={lf_total}, top 10):")
    for o in sorted(lf_counts, key=lambda x: -lf_counts[x])[:10]:
        pct = lf_counts[o] / lf_total * 100
        print(f"  {o}: {lf_counts[o]} ({pct:.1f}%)")

    print(f"\npen routing (min LF N={min_lf}):")
    major_lf = [(o, lf_counts[o]) for o in ONSET_PRIORITY if lf_counts[o] >= min_lf]

    summary_selfchain = []

    for lf_onset, lf_n in major_lf:
        lf_lines = [(fo, ws) for fo, ws in section_lines if get_onset(ws[-1]) == lf_onset]
        elig = [(fo, ws) for fo, ws in lf_lines if len(ws) >= 3]
        n_elig = len(elig)

        pen_dist = defaultdict(int)
        for fo, ws in elig:
            o = get_onset(ws[-2])
            if o: pen_dist[o] += 1

        self_obs = pen_dist.get(lf_onset, 0)
        self_base = pen_base.get(lf_onset, 0)
        self_exp = self_base * n_elig if self_base > 0 else 0
        self_E = self_obs / self_exp if self_exp > 0 else 0
        self_flag = flag_cell(self_obs, self_E)
        summary_selfchain.append((lf_onset, lf_n, self_obs, n_elig, self_E, self_flag))

        print(f"\n  {lf_onset}-LF (N_lf={lf_n}, N_elig={n_elig}):")
        rows = []
        for o in ONSET_PRIORITY:
            obs = pen_dist[o]
            base_rate = pen_base.get(o, 0)
            if base_rate == 0 and obs == 0: continue
            expected = base_rate * n_elig if base_rate > 0 else 0
            E = obs / expected if expected > 0 else float('inf') if obs > 0 else 0
            rows.append((o, obs, expected, E))
        rows.sort(key=lambda x: (-x[3] if x[3] != float('inf') else 1e9))

        for o, obs, exp, E in rows[:6]:
            flag = flag_cell(obs, E) if E != float('inf') else '(uniq)'
            base_pct = pen_base.get(o, 0) * 100
            E_str = f"{E:.2f}x" if E != float('inf') else "inf"
            self_mark = " <--SELF" if o == lf_onset else ""
            print(f"    {o:8s}: obs={obs:3d}, exp={exp:.1f} (base={base_pct:.1f}%), E={E_str}  {flag}{self_mark}")

        top6 = [r[0] for r in rows[:6]]
        if lf_onset not in top6:
            self_base_pct = self_base * 100
            print(f"    [{lf_onset}-self]: obs={self_obs}, exp={self_exp:.1f}, E={self_E:.2f}x  {self_flag}")

        # Show a@pen explicitly for F459 context (ok→a@pen)
        if 'a' not in top6 and lf_onset == 'ok':
            obs_a = pen_dist['a']
            base_a = pen_base.get('a', 0)
            if base_a > 0:
                exp_a = base_a * n_elig
                E_a = obs_a / exp_a
                print(f"    [a@pen]: obs={obs_a}, exp={exp_a:.1f}, E={E_a:.2f}x  {flag_cell(obs_a,E_a)}")
        # Show ot@pen for F460 context (ot→ot@pen)
        if lf_onset == 'ot' and 'ot' not in top6:
            obs_ot = pen_dist.get('ot', 0)
            base_ot = pen_base.get('ot', 0)
            if base_ot > 0:
                exp_ot = base_ot * n_elig
                E_ot = obs_ot / exp_ot
                print(f"    [ot-self@pen]: obs={obs_ot}, exp={exp_ot:.1f}, E={E_ot:.2f}x  {flag_cell(obs_ot,E_ot)}")

    print(f"\n--- Self-chain summary for {label} ---")
    print(f"{'LF':8s} {'N_lf':6s} {'self':5s} {'N_elig':7s} {'E':8s} {'flag'}")
    for lf_onset, lf_n, self_obs, n_elig, self_E, self_flag in summary_selfchain:
        print(f"{lf_onset:8s} {lf_n:6d} {self_obs:5d} {n_elig:7d} {self_E:8.2f} {self_flag}")

run_pen_survey(sections['B_astro'], 'B astro', min_lf=10)
