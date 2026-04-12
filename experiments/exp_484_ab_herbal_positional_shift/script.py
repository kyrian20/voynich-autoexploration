#!/usr/bin/env python3
"""
exp_484: A/B Herbal Positional Shift — Line Length Artifact or Grammar Rule?
H_new_BA: Does the A(pen) vs B(pos2) grammar-pair position difference reflect
line length differences, or is it a genuine grammatical difference?

Tests:
1. Line length distributions: A herbal_a vs B herbal
2. For ch-LF and d-LF: compare ch/sh enrichment at pos2 vs pen in both sections
3. Length-controlled analysis: lines ≥5 words only
"""

import re
from collections import defaultdict
from statistics import mean, median

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
    return 'other'

def get_section_a(folio):
    n = folio_num(folio)
    if n <= 56: return 'herbal_a'
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

a_herbal = []
b_herbal = []

for folio, lines in folios.items():
    all_words = [w for line in lines for w in line]
    if is_b_dialect(all_words):
        if get_section_b(folio) == 'herbal':
            for line in lines:
                b_herbal.append((folio, line))
    else:
        if get_section_a(folio) == 'herbal_a':
            for line in lines:
                a_herbal.append((folio, line))

print(f"A herbal_a: {len(a_herbal)} lines from {len(set(f for f,_ in a_herbal))} folios")
print(f"B herbal:   {len(b_herbal)} lines from {len(set(f for f,_ in b_herbal))} folios")

# ============================================================
# 1. LINE LENGTH DISTRIBUTIONS
# ============================================================
print("\n" + "="*60)
print("1. LINE LENGTH DISTRIBUTIONS")
print("="*60)

def length_stats(lines, label):
    lengths = [len(ws) for _, ws in lines]
    from collections import Counter
    c = Counter(lengths)
    N = len(lengths)
    print(f"\n{label} (N={N}):")
    print(f"  Mean: {mean(lengths):.2f}, Median: {median(lengths):.1f}")
    print(f"  Length distribution:")
    for l in sorted(c.keys()):
        if l <= 12 or c[l] > 2:
            bar = '#' * (c[l] * 30 // max(c.values()))
            print(f"    {l:>3} words: {c[l]:>4} ({c[l]/N:.1%})  {bar}")
    # Fraction where pos2 == pen (i.e., len == 3)
    len3 = c[3] / N
    len4 = c[4] / N
    print(f"  3-word lines (pos2==pen): {len3:.1%}")
    print(f"  4-word lines (pos2≠pen, but short): {len4:.1%}")
    print(f"  ≥5-word lines: {sum(c[l] for l in c if l >= 5)/N:.1%}")
    return lengths

a_lengths = length_stats(a_herbal, "A herbal_a")
b_lengths = length_stats(b_herbal, "B herbal")

# ============================================================
# 2. POSITIONAL ANALYSIS: ch enrichment at pos2 vs pen for ch-LF
# ============================================================
print("\n" + "="*60)
print("2. ch ENRICHMENT AT pos2 vs pen IN ch-LF LINES")
print("="*60)

def analyze_positions(section_lines, lf_onset, target_onset, label):
    all_ws = [ws for _, ws in section_lines]

    # Build pos2 and pen baselines
    pos2_base = defaultdict(int); n_p2 = 0
    pen_base  = defaultdict(int); n_pn = 0
    for ws in all_ws:
        if len(ws) >= 2: pos2_base[get_onset(ws[1])] += 1; n_p2 += 1
        if len(ws) >= 3: pen_base[get_onset(ws[-2])] += 1; n_pn += 1

    lf_lines = [(f, ws) for f, ws in section_lines
                if ws and get_onset(ws[-1]) == lf_onset]
    N_lf = len(lf_lines)

    # All lines (any length)
    p2_obs = sum(1 for _, ws in lf_lines if len(ws) >= 2 and get_onset(ws[1]) == target_onset)
    p2_N   = sum(1 for _, ws in lf_lines if len(ws) >= 2)
    p2_exp = pos2_base.get(target_onset, 0) / n_p2 * p2_N if n_p2 > 0 else 0
    p2_E   = p2_obs / p2_exp if p2_exp > 0 else 0

    pn_obs = sum(1 for _, ws in lf_lines if len(ws) >= 3 and get_onset(ws[-2]) == target_onset)
    pn_N   = sum(1 for _, ws in lf_lines if len(ws) >= 3)
    pn_exp = pen_base.get(target_onset, 0) / n_pn * pn_N if n_pn > 0 else 0
    pn_E   = pn_obs / pn_exp if pn_exp > 0 else 0

    print(f"\n{label} {lf_onset}-LF (N_lf={N_lf}):")
    print(f"  ALL LENGTHS:")
    print(f"    pos2: obs={p2_obs}/{p2_N} ({p2_obs/p2_N:.1%}) exp={p2_exp:.1f} E={p2_E:.2f}×")
    print(f"    pen:  obs={pn_obs}/{pn_N} ({pn_obs/pn_N:.1%}) exp={pn_exp:.1f} E={pn_E:.2f}×")

    # Long lines only (≥5 words, where pos2 and pen are distinct)
    long_lines = [(f, ws) for f, ws in lf_lines if len(ws) >= 5]
    N_long = len(long_lines)

    if N_long >= 3:
        # For long lines only — build separate baseline from long lines
        # Actually use the same section baseline (adjusted for N_long)
        lp2 = sum(1 for _, ws in long_lines if get_onset(ws[1]) == target_onset)
        lpn = sum(1 for _, ws in long_lines if get_onset(ws[-2]) == target_onset)
        lp2_exp = pos2_base.get(target_onset, 0) / n_p2 * N_long if n_p2 > 0 else 0
        lpn_exp = pen_base.get(target_onset, 0) / n_pn * N_long if n_pn > 0 else 0
        lp2_E = lp2 / lp2_exp if lp2_exp > 0 else 0
        lpn_E = lpn / lpn_exp if lpn_exp > 0 else 0

        print(f"  LONG LINES (≥5 words, N={N_long}):")
        print(f"    pos2: obs={lp2}/{N_long} ({lp2/N_long:.1%}) exp={lp2_exp:.1f} E={lp2_E:.2f}×")
        print(f"    pen:  obs={lpn}/{N_long} ({lpn/N_long:.1%}) exp={lpn_exp:.1f} E={lpn_E:.2f}×")
    else:
        print(f"  LONG LINES (≥5 words): N={N_long} (too few)")

    # 3-word lines: pos2 == pen (word index 1 == word index -2 for len=3)
    three_word = [(f, ws) for f, ws in lf_lines if len(ws) == 3]
    N_3 = len(three_word)
    t_obs = sum(1 for _, ws in three_word if get_onset(ws[1]) == target_onset)
    print(f"  3-WORD LINES (pos2=pen=same word): N={N_3}, {target_onset}@pos2=pen: {t_obs}")

# ch in ch-LF lines
analyze_positions(a_herbal, 'ch', 'ch', 'A herbal_a')
analyze_positions(b_herbal, 'ch', 'ch', 'B herbal')

# sh in d-LF lines
print("\n")
analyze_positions(a_herbal, 'd', 'sh', 'A herbal_a')
analyze_positions(b_herbal, 'd', 'sh', 'B herbal')

# ============================================================
# 3. POSITION PROFILE: pos2 vs pen vs other for key LF classes
# ============================================================
print("\n" + "="*60)
print("3. POSITION PROFILE (pos2, pos3, pen-1, pen) FOR ch-LF AND d-LF")
print("  [For lines ≥6 words: pos2=ws[1], pos3=ws[2], pen-1=ws[-3], pen=ws[-2]]")
print("="*60)

def position_profile(section_lines, lf_onset, target_onset, label):
    all_ws = [ws for _, ws in section_lines]

    # Baselines for each position
    bases = {}
    for pos_name, idx in [('pos2', 1), ('pos3', 2), ('pen', -2)]:
        b = defaultdict(int); nb = 0
        for ws in all_ws:
            if (idx >= 0 and len(ws) > idx) or (idx < 0 and len(ws) >= abs(idx) + 1):
                b[get_onset(ws[idx])] += 1; nb += 1
        bases[pos_name] = (b, nb)

    # Long lines ≥6 words
    lf_lines = [(f, ws) for f, ws in section_lines
                if ws and get_onset(ws[-1]) == lf_onset and len(ws) >= 6]
    N = len(lf_lines)
    if N < 3:
        print(f"\n{label} {lf_onset}-LF (≥6 words): N={N} (too few)")
        return

    print(f"\n{label} {lf_onset}-LF (≥6 words, N={N}):")
    for pos_name, idx in [('pos2', 1), ('pos3', 2), ('pen-1', -3), ('pen', -2)]:
        obs = sum(1 for _, ws in lf_lines if get_onset(ws[idx]) == target_onset)
        b, nb = bases.get('pen' if pos_name == 'pen-1' else pos_name, ({}, 1))
        if pos_name == 'pen-1':
            # pen-1 = ws[-3], use pos3 baseline as proxy
            b2, nb2 = bases.get('pos3', ({}, 1))
            exp = b2.get(target_onset, 0) / nb2 * N if nb2 > 0 else 0
        else:
            exp = b.get(target_onset, 0) / nb * N if nb > 0 else 0
        E = obs / exp if exp > 0 else 0
        print(f"  {pos_name:<6}: obs={obs:>3}/{N} ({obs/N:.1%}) exp={exp:.1f} E={E:.2f}×")

position_profile(a_herbal, 'ch', 'ch', 'A herbal_a')
position_profile(b_herbal, 'ch', 'ch', 'B herbal')
print()
position_profile(a_herbal, 'd', 'sh', 'A herbal_a')
position_profile(b_herbal, 'd', 'sh', 'B herbal')
