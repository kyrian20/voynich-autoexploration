#!/usr/bin/env python3
"""
exp_477: A/B t-LF pos1 Inversion Verification
H_new_AN: A dialect routes t-LF → o-gallows (ot/ol) at pos1;
           B dialect routes t-LF → template class (qok) at pos1.
Verify across all available sections with sufficient N.
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
    return 'other_a'

def get_section_b(folio):
    n = folio_num(folio)
    if n <= 72: return 'herbal'
    if n <= 84: return 'astro'
    if n <= 102: return 'cosmo'
    if n <= 116: return 'pharma'
    if n <= 170: return 'bio'
    return 'text'

# Parse corpus
folios = defaultdict(list)  # folio -> list of lines (each line = list of words)

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

# Separate A and B dialect folios, classify sections
a_by_section = defaultdict(list)  # section -> list of lines
b_by_section = defaultdict(list)

for folio, lines in folios.items():
    all_words = [w for line in lines for w in line]
    if is_b_dialect(all_words):
        sec = get_section_b(folio)
        for line in lines:
            b_by_section[sec].append((folio, line))
    else:
        sec = get_section_a(folio)
        for line in lines:
            a_by_section[sec].append((folio, line))

def compute_routing(section_lines, lf_onset, label):
    """Compute t-LF pos1/pos2/LL routing with section-specific baselines."""
    # Gather ALL lines for baseline
    all_lines = [ws for _, ws in section_lines]
    N_base = len(all_lines)

    # Build positional baselines
    pos1_base = defaultdict(int)
    pos2_base = defaultdict(int)
    ll_base = defaultdict(int)

    for ws in all_lines:
        if len(ws) >= 1:
            pos1_base[get_onset(ws[0])] += 1
        if len(ws) >= 2:
            # pos1 (index 0) and pos2 (index 1) — note: LF is last word
            # We use word position after LF:
            # LF = ws[-1], pos1 = ws[0], pos2 = ws[1]
            # For baseline, we need: what is distribution of pos1,pos2,LL ACROSS all lines
            pass
        ll_base[get_onset(ws[-1])] += 1

    # Actually: positional baseline = distribution of each position across all lines
    # For pos1: ws[0] over all lines with len >= 1
    # For pos2: ws[1] over all lines with len >= 2 (in context of LF being last word,
    #   actual pos1 after LF would be ws[0], pos2 = ws[1])
    # Let's use: pos1 = ws[0], pos2 = ws[1], LL = ws[-1] across all lines

    pos1_base = defaultdict(int)
    pos2_base = defaultdict(int)
    ll_base_cnt = defaultdict(int)
    n1, n2, nLL = 0, 0, 0
    for ws in all_lines:
        if len(ws) >= 1:
            pos1_base[get_onset(ws[0])] += 1
            n1 += 1
        if len(ws) >= 2:
            pos2_base[get_onset(ws[1])] += 1
            n2 += 1
        ll_base_cnt[get_onset(ws[-1])] += 1
        nLL += 1

    # t-LF lines
    lf_lines = [(folio, ws) for folio, ws in section_lines
                if ws and get_onset(ws[-1]) == lf_onset and len(ws) >= 2]
    N_lf = len(lf_lines)

    if N_lf == 0:
        print(f"\n{label}: N=0 t-LF lines, skipping")
        return

    print(f"\n{'='*60}")
    print(f"{label}: N={N_lf} t-LF lines / {N_base} total lines in section")
    print(f"  LF fraction: {N_lf/N_base:.1%}")

    # LF word inventory
    lf_words = defaultdict(int)
    for _, ws in lf_lines:
        lf_words[ws[-1]] += 1
    top_lf = sorted(lf_words.items(), key=lambda x: -x[1])[:8]
    print(f"  LF words: {', '.join(f'{w}({c})' for w,c in top_lf)}")

    # pos1 routing
    pos1_obs = defaultdict(int)
    n1_lf = 0
    for _, ws in lf_lines:
        if len(ws) >= 2:
            pos1_obs[get_onset(ws[0])] += 1
            n1_lf += 1

    print(f"\n  pos1 routing (N={n1_lf}):")
    pos1_results = []
    for onset, obs in sorted(pos1_obs.items(), key=lambda x: -x[1]):
        exp = pos1_base.get(onset, 0) / n1 * n1_lf if n1 > 0 else 0
        E = obs / exp if exp > 0 else float('inf')
        pos1_results.append((onset, obs, exp, E))

    # Focus: ot, ol, qok, qot, ch
    focus = ['ot','ol','qok','qot','ch','ok','sh','t','d','cth']
    print(f"  {'onset':<8} {'obs':>5} {'exp':>6} {'E':>6} {'flag':>8}")
    for onset in focus:
        obs = pos1_obs.get(onset, 0)
        exp = pos1_base.get(onset, 0) / n1 * n1_lf if n1 > 0 else 0
        E = obs / exp if exp > 0 else float('inf')
        flag = ''
        if obs >= 10 and E >= 1.5: flag = 'CONFIRMED'
        elif obs >= 5 and E >= 2.0: flag = 'dir'
        elif obs >= 3 and E >= 2.0: flag = '(dir)'
        print(f"  {onset:<8} {obs:>5} {exp:>6.1f} {E:>6.2f}x {flag:>8}")

    # Also show top elevated onsets not in focus
    print(f"  --- top elevated (all onsets) ---")
    for onset, obs, exp, E in sorted(pos1_results, key=lambda x: -x[3])[:5]:
        if onset not in focus and obs >= 3:
            flag = ''
            if obs >= 10 and E >= 1.5: flag = 'CONFIRMED'
            elif obs >= 5 and E >= 2.0: flag = 'dir'
            elif obs >= 3 and E >= 2.0: flag = '(dir)'
            print(f"  {onset:<8} {obs:>5} {exp:>6.1f} {E:>6.2f}x {flag:>8}")

    # pos2 routing (lines with len >= 3)
    pos2_obs = defaultdict(int)
    n2_lf = 0
    for _, ws in lf_lines:
        if len(ws) >= 3:
            pos2_obs[get_onset(ws[1])] += 1
            n2_lf += 1

    if n2_lf > 0:
        print(f"\n  pos2 routing (N={n2_lf}):")
        for onset in ['ot','ol','qok','qot','ch','ok','sh','t','d','cth']:
            obs = pos2_obs.get(onset, 0)
            exp = pos2_base.get(onset, 0) / n2 * n2_lf if n2 > 0 else 0
            E = obs / exp if exp > 0 else float('inf')
            flag = ''
            if obs >= 10 and E >= 1.5: flag = 'CONFIRMED'
            elif obs >= 5 and E >= 2.0: flag = 'dir'
            elif obs >= 3 and E >= 2.0: flag = '(dir)'
            print(f"  {onset:<8} {obs:>5} {exp:>6.1f} {E:>6.2f}x {flag:>8}")

    # LL routing
    ll_obs = defaultdict(int)
    n_ll_lf = 0
    for _, ws in lf_lines:
        if len(ws) >= 3:
            ll_obs[get_onset(ws[-1])] += 1  # this IS the LF word
            # Actually LL = second-to-last word? No:
            # Convention: LF = last word of previous line (ws[-1])
            # pos1 = ws[0], pos2 = ws[1], LL = ws[-2] (second-to-last of CURRENT line)?
            # No — in this framework, LF=last word, LL=last word. So LF IS the LL.
            # LL routing means: given LF word's onset, what is at LL of NEXT line?
            # But in our formula analysis: LF = line-final (ws[-1]); pos1 = ws[0];
            # "LL routing" = where does the within-line formula END?
            # In exp_472 and exp_473, LL routing was: what onset appears at ws[-1]
            # We need to be careful:
            # Actually in exp_472, the LF is the onset of the whole line (ws[-1]),
            # and LL routing asked: in t-LF lines, what onsets appear at LL?
            # But LL IS the LF word. So "LL routing" from exp_472 means something different.
            # Let me re-read: in exp_472 the formula for B herbal t-LF showed o→LL (2.02×/N=5)
            # That must mean: within the line, the LAST word (LL) is an o-onset...
            # But the LF is t-onset. So LL ≠ LF? Unless LL refers to the SECOND-to-last.
            # Actually I think there's a convention confusion. Let me use:
            # LF word = ws[-1] (last word on line) — this is what we filter on
            # pos1 = ws[0] (first word), pos2 = ws[1], penultimate = ws[-2]
            # "LL routing" in prior exps means the LL of the FOLLOWING line (cross-line coupling)
            # OR the penultimate position within the current line?
            # From exp_472 result: "B herbal t-LF: qok→pos1(2.28×/N=6,dir), o→pos2(2.69×/N=5,dir), o→LL(2.02×/N=5,dir)"
            # These are all WITHIN line positions. pos1=first, pos2=second, LL=last.
            # But last IS the LF word (t-class). So o→LL means o appears at last position?
            # That would mean last word is o-class AND t-class simultaneously, which is impossible.
            # UNLESS LL means the word just BEFORE the LF (penultimate = ws[-2]).
            # Let me check exp_472 script logic...
        pass

    # Based on re-reading exp_472/473: LL routing = penultimate word (ws[-2])
    # pos1=ws[0], pos2=ws[1], LL=ws[-2] (second to last, with last being LF=ws[-1])
    ll_obs2 = defaultdict(int)
    n_ll_lf2 = 0
    for _, ws in lf_lines:
        if len(ws) >= 3:  # need at least LF + 1 other position for penultimate
            ll_obs2[get_onset(ws[-2])] += 1
            n_ll_lf2 += 1

    if n_ll_lf2 > 0:
        print(f"\n  penultimate (LL, ws[-2]) routing (N={n_ll_lf2}):")
        penult_base = defaultdict(int)
        np = 0
        for ws in all_lines:
            if len(ws) >= 2:
                penult_base[get_onset(ws[-2])] += 1
                np += 1
        for onset in ['ot','ol','qok','qot','ch','ok','sh','t','d','cth','o']:
            obs = ll_obs2.get(onset, 0)
            exp = penult_base.get(onset, 0) / np * n_ll_lf2 if np > 0 else 0
            E = obs / exp if exp > 0 else float('inf')
            flag = ''
            if obs >= 10 and E >= 1.5: flag = 'CONFIRMED'
            elif obs >= 5 and E >= 2.0: flag = 'dir'
            elif obs >= 3 and E >= 2.0: flag = '(dir)'
            print(f"  {onset:<8} {obs:>5} {exp:>6.1f} {E:>6.2f}x {flag:>8}")

# Section sizes
print("=== CORPUS OVERVIEW ===")
for sec in ['herbal_a','stars','cosmo','herbal_b']:
    n = len(a_by_section[sec])
    t_lf = sum(1 for _, ws in a_by_section[sec] if ws and get_onset(ws[-1]) == 't')
    print(f"  A {sec}: {n} lines, t-LF={t_lf}")
for sec in ['herbal','astro','cosmo','pharma']:
    n = len(b_by_section[sec])
    t_lf = sum(1 for _, ws in b_by_section[sec] if ws and get_onset(ws[-1]) == 't')
    print(f"  B {sec}: {n} lines, t-LF={t_lf}")

print("\n=== A DIALECT t-LF ROUTING ===")
compute_routing(a_by_section['herbal_a'], 't', 'A herbal_a t-LF')
compute_routing(a_by_section['cosmo'], 't', 'A cosmo t-LF')
compute_routing(a_by_section['stars'], 't', 'A stars t-LF')

print("\n\n=== B DIALECT t-LF ROUTING ===")
compute_routing(b_by_section['herbal'], 't', 'B herbal t-LF')
compute_routing(b_by_section['cosmo'], 't', 'B cosmo t-LF')
compute_routing(b_by_section['astro'], 't', 'B astro t-LF')

print("\n\n=== CROSS-DIALECT COMPARISON SUMMARY ===")
print("Focus: is ot/ol elevated at pos1 in A but not B?")
print("       is qok elevated at pos1 in B but not A?")
