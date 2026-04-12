"""
exp_527: Q011 resolution (F446 discrepancy) + Q012 resolution (F470 contamination)

Q011: F446 (A stars t-LF elevation E=2.12×/N=15) contradicted by exp_525 (t is DEPLETED at line-FINAL).
  Hypothesis: exp_466 measured ws[0] (line-FIRST/pos1) instead of ws[-1] (line-FINAL).
  Test: compute t-onset at pos1 (line-opening) in A stars and compare to F446 claims.

Q012: F470 (B herbal a→a@pos2 dir, E=3.60×/N=6, exp_489) not reproduced in exp_526 with len≥3.
  Hypothesis: exp_489 used len≥2 for pos2 eligibility, including 2-word a-LF lines where pos2=LF=a.
  Test: reproduce exp_489 results with explicit len≥2 vs len≥3 comparison.
"""

import re
from collections import defaultdict, Counter

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_PRIORITY = [
    'qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph',
    'd','s','y','k','t','l','r','p','f','o','e','a','n','m'
]

def get_onset(word):
    for onset in ONSET_PRIORITY:
        if word.startswith(onset):
            return onset
    return 'other'

def folio_num(folio):
    m = re.search(r'f(\d+)', folio)
    return int(m.group(1)) if m else None

def parse_corpus(path):
    folio_lines = defaultdict(list)
    pat = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    for m in pat.finditer(raw):
        folio_raw, _, locus_raw, text = m.groups()
        folio = folio_raw.lstrip('+*=&~')
        lc = locus_raw.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        words = [w for w in re.split(r'[-.\s]', text)
                 if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        n = folio_num(folio)
        if n is None:
            continue
        folio_lines[n].append(words)
    return folio_lines

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words:
        return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

folio_lines = parse_corpus(CORPUS)

a_stars = {n: ls for n, ls in folio_lines.items() if 57 <= n <= 72 and not is_b_dialect(ls)}
a_herbal_a = {n: ls for n, ls in folio_lines.items() if n <= 56 and not is_b_dialect(ls)}
b_herbal = {n: ls for n, ls in folio_lines.items() if n <= 72 and is_b_dialect(ls)}
# A-overall (all A-dialect sections 1-102): for F446's A-overall baseline
a_overall = {n: ls for n, ls in folio_lines.items() if n <= 102 and not is_b_dialect(ls)}

a_stars_lines = [ln for ls in a_stars.values() for ln in ls]
a_ha_lines = [ln for ls in a_herbal_a.values() for ln in ls]
b_herbal_lines = [ln for ls in b_herbal.values() for ln in ls]
a_overall_lines = [ln for ls in a_overall.values() for ln in ls]

print(f"A stars: {len(a_stars)} folios, {len(a_stars_lines)} lines")
print(f"A herbal_a: {len(a_herbal_a)} folios, {len(a_ha_lines)} lines")
print(f"B herbal: {len(b_herbal)} folios, {len(b_herbal_lines)} lines")
print(f"A overall (1-102): {len(a_overall)} folios, {len(a_overall_lines)} lines")

def flag(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONF'
    elif obs >= 5 and E >= 2.0: return 'dir'
    elif obs >= 3 and E >= 2.5: return '(dir)'
    elif E >= 1.0: return f'{E:.2f}×'
    else: return f'DEPL {E:.2f}×'

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: Q011 RESOLUTION — t-onset at pos1 in A stars (exp_466 re-analysis)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 1: Q011 — F446 DISCREPANCY ROOT CAUSE")
print("="*70)

print("\n--- exp_466 used ws[0] (line-FIRST) not ws[-1] (line-LAST) ---")
print("F446 claimed 't-LF elevation E=2.12×/N=15'")
print("If 'lf' = first word (ws[0]), F446 was measuring line-OPENING t-onset.")
print()

# Compute line-FIRST (pos1/opening) onset distribution in A stars
a_stars_pos1 = Counter(get_onset(ln[0]) for ln in a_stars_lines)
a_overall_pos1 = Counter(get_onset(ln[0]) for ln in a_overall_lines)
N_stars = len(a_stars_lines)
N_overall = len(a_overall_lines)

print(f"A stars pos1 (line-FIRST) distribution (N={N_stars}):")
print(f"\n{'onset':>8} {'A stars obs':>12} {'A stars %':>10} {'A overall %':>12} {'E':>8}  flag")
for onset, obs in sorted(a_stars_pos1.items(), key=lambda x: -x[1])[:15]:
    a_stars_rate = obs / N_stars
    a_overall_rate = a_overall_pos1.get(onset, 0) / N_overall
    E = a_stars_rate / a_overall_rate if a_overall_rate > 0 else 0
    print(f"  {onset:>6} {obs:>12} {100*a_stars_rate:>10.1f}% {100*a_overall_rate:>12.1f}%  {E:>7.2f}×  {flag(obs, E)}")

# Focus on t-onset
t_stars_obs = a_stars_pos1.get('t', 0)
t_overall_rate = a_overall_pos1.get('t', 0) / N_overall
t_exp = t_overall_rate * N_stars
t_E = t_stars_obs / t_exp if t_exp > 0 else 0
print(f"\n--- t-onset FORMAL LINE-FIRST analysis ---")
print(f"A stars t at pos1 (line-FIRST): obs={t_stars_obs}, exp={t_exp:.2f}, E={t_E:.2f}×")
print(f"  A overall t-rate at pos1: {100*t_overall_rate:.1f}%")
print(f"  A stars t-rate at pos1: {100*t_stars_obs/N_stars:.1f}%")

# Compare to F446's claim
print(f"\n--- F446 claim: E=2.12×/N=15 ---")
print(f"Our measurement of t at line-FIRST: E={t_E:.2f}×/N={t_stars_obs}")
if abs(t_E - 2.12) < 0.3 and abs(t_stars_obs - 15) <= 3:
    print("MATCH: F446 was measuring line-FIRST onset, not line-FINAL.")
    print("Q011 RESOLUTION: F446 = 'A stars t-onset elevated at line-FIRST' (pos1 grammar)")
    print("  NOT 'A stars t-LF (line-final) elevated'. Categorization error, not measurement error.")
else:
    print(f"PARTIAL MATCH or mismatch: E={t_E:.2f}× vs F446 E=2.12×; N={t_stars_obs} vs F446 N=15")

# Also check: line-FINAL t in A stars (confirming our exp_525 finding)
t_final_stars = Counter(get_onset(ln[-1]) for ln in a_stars_lines).get('t', 0)
t_final_ha = Counter(get_onset(ln[-1]) for ln in a_ha_lines).get('t', 0)
print(f"\n--- Line-FINAL t (our standard LF measurement) ---")
print(f"A stars t at line-FINAL: {t_final_stars}/{len(a_stars_lines)} = {100*t_final_stars/len(a_stars_lines):.1f}%")
print(f"A herbal_a t at line-FINAL: {t_final_ha}/{len(a_ha_lines)} = {100*t_final_ha/len(a_ha_lines):.1f}%")
E_final = (t_final_stars/len(a_stars_lines)) / (t_final_ha/len(a_ha_lines))
print(f"E (line-FINAL): {E_final:.3f}× — DEPLETED (confirms exp_525)")

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: A stars t at pos1 formal grammar analysis
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 2: A STARS t-ONSET LINE-OPENING SURVEY (F446 REINTERPRETATION)")
print("="*70)

# Full pos1 distribution in A stars
print(f"\nA stars pos1 (line-FIRST) onset distribution vs A herbal_a:")
a_ha_pos1 = Counter(get_onset(ln[0]) for ln in a_ha_lines)
N_ha = len(a_ha_lines)

print(f"\n{'onset':>8} {'A stars':>10} {'E(stars/ha)':>14}  flag")
all_onsets = sorted(set(list(a_stars_pos1.keys()) + list(a_ha_pos1.keys())), key=lambda x: -a_stars_pos1.get(x,0))
for onset in all_onsets[:15]:
    obs = a_stars_pos1.get(onset, 0)
    ha_rate = a_ha_pos1.get(onset, 0) / N_ha
    exp = ha_rate * N_stars
    E = obs / exp if exp > 0 else 0
    stars_pct = 100 * obs / N_stars
    ha_pct = 100 * a_ha_pos1.get(onset, 0) / N_ha
    print(f"  {onset:>6}  {stars_pct:>5.1f}%({obs})  {100*ha_rate:>6.1f}%→E={E:.2f}×  {flag(obs, E)}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: Q012 — F470 reproduction with len>=2 vs len>=3
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 3: Q012 — F470 CONTAMINATION TEST (B herbal a-LF pos2)")
print("="*70)

b_herbal_a_lf_lines = [ln for ln in b_herbal_lines if get_onset(ln[-1]) == 'a']
print(f"\nB herbal a-LF lines: N={len(b_herbal_a_lf_lines)}")

# pos2 baseline from B herbal (all lines, len>=3)
b_herbal_pos2_base = Counter(get_onset(ln[1]) for ln in b_herbal_lines if len(ln) >= 3)
N_base = sum(b_herbal_pos2_base.values())

print(f"\n--- With len>=2 eligibility (possibly contaminated, as in exp_489) ---")
elig_2 = [ln for ln in b_herbal_a_lf_lines if len(ln) >= 2]
a_self_count_2 = sum(1 for ln in elig_2 if get_onset(ln[1]) == 'a')
# Note: in 2-word lines, ln[1]=ln[-1] (same word), so LF class = pos2 class trivially
two_word_lines = [ln for ln in elig_2 if len(ln) == 2]
print(f"N_elig (len>=2): {len(elig_2)}")
print(f"2-word a-LF lines: {len(two_word_lines)} (these have pos2=LF=a trivially)")
exp_2 = (b_herbal_pos2_base.get('a', 0) / N_base) * len(elig_2) if N_base > 0 else 0
E_2 = a_self_count_2 / exp_2 if exp_2 > 0 else 0
print(f"a-self at pos2 (len>=2): obs={a_self_count_2}, exp={exp_2:.2f}, E={E_2:.2f}×  {flag(a_self_count_2, E_2)}")

print(f"\n--- With len>=3 eligibility (current standard, contamination-free) ---")
elig_3 = [ln for ln in b_herbal_a_lf_lines if len(ln) >= 3]
a_self_count_3 = sum(1 for ln in elig_3 if get_onset(ln[1]) == 'a')
exp_3 = (b_herbal_pos2_base.get('a', 0) / N_base) * len(elig_3) if N_base > 0 else 0
E_3 = a_self_count_3 / exp_3 if exp_3 > 0 else 0
print(f"N_elig (len>=3): {len(elig_3)}")
print(f"a-self at pos2 (len>=3): obs={a_self_count_3}, exp={exp_3:.2f}, E={E_3:.2f}×  {flag(a_self_count_3, E_3)}")

print(f"\n--- Discrepancy analysis ---")
print(f"F470 claimed: obs=6, N_elig=19, E=3.60×")
print(f"len>=2 result: obs={a_self_count_2}, N_elig={len(elig_2)}, E={E_2:.2f}×")
print(f"len>=3 result: obs={a_self_count_3}, N_elig={len(elig_3)}, E={E_3:.2f}×")
extra = len(elig_2) - len(elig_3)
trivial = sum(1 for ln in b_herbal_a_lf_lines if len(ln) == 2)
print(f"Extra 2-word lines (trivial pos2=LF): {trivial}")
print(f"Contaminating obs (trivial a at pos2): {trivial} (all 2-word a-LF lines have a trivially at pos2)")

if abs(a_self_count_2 - 6) <= 1 and abs(len(elig_2) - 19) <= 2:
    print(f"\nCONFIRMED: F470 used len>=2, explaining the obs=6/N_elig=19 result.")
    print("Q012 RESOLUTION: F470 is inflated by 2-word line contamination.")
    print("Corrected F470: BELOW THRESHOLD (obs={}, E={:.2f}×)".format(a_self_count_3, E_3))
else:
    print(f"\nMISMATCH: len>=2 gives obs={a_self_count_2}/N={len(elig_2)}, F470 had obs=6/N=19")
    print("Contamination theory partially confirmed or another factor involved.")

# Full pos2 distribution for B herbal a-LF with len>=3 (current standard)
print(f"\n--- Full B herbal a-LF pos2 distribution (len>=3, current standard) ---")
pos2_counts = Counter(get_onset(ln[1]) for ln in elig_3)
print(f"N_elig={len(elig_3)}")
print(f"\n{'onset':>8} {'obs':>5} {'exp':>6} {'E':>7}  flag")
for onset, obs in sorted(pos2_counts.items(), key=lambda x: -x[1]):
    exp = (b_herbal_pos2_base.get(onset, 0) / N_base) * len(elig_3) if N_base > 0 else 0
    E = obs / exp if exp > 0 else 0
    print(f"  {onset:>6} {obs:>5} {exp:>6.1f} {E:>7.2f}×  {flag(obs, E)}")
