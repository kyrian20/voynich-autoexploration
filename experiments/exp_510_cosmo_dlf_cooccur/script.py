"""
exp_510: A cosmo d-LF three-position co-occurrence test (H_new_CR)
CORRECTED parsing: B-dialect folio check applied before section assignment.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
ONSET_PRIORITY = [
    'qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol',
    'sch','skh','sph','d','s','y','k','t','l','r','p','f','o','e','a','n','m'
]

def get_onset(word):
    for o in ONSET_PRIORITY:
        if word.startswith(o):
            return o
    return word[0] if word else None

def folio_num(folio):
    m = re.search(r'f(\d+)', folio)
    return int(m.group(1)) if m else None

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words: return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

def parse_corpus():
    """Established approach: A sections by folio number (no dialect check needed),
    B sections by folio number + B-dialect check."""
    sections = defaultdict(list)
    pat = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    with open(CORPUS, encoding='utf-8') as f:
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
        # Standard A section classification (by position in manuscript)
        if n <= 56:
            sections['A_herbal_a'].append(words)
        elif n <= 72:
            sections['A_stars'].append(words)
        elif n <= 84:
            # A_herbal_b range — may include B_astro folios; DON'T assign here
            pass
        elif n <= 102:
            sections['A_cosmo'].append(words)
        # Also build by folio for B-dialect check
        sections[f'folio_{n}'].append(words)

    # B sections: use folio-level dialect check
    b_herbal, b_astro, b_cosmo, b_pharma = [], [], [], []
    for key, lines in sections.items():
        m = re.match(r'folio_(\d+)', key)
        if not m: continue
        n = int(m.group(1))
        if not is_b_dialect(lines): continue
        if n <= 72:
            b_herbal.extend(lines)
        elif n <= 84:
            b_astro.extend(lines)
        elif n <= 102:
            b_cosmo.extend(lines)
        elif n <= 116:
            b_pharma.extend(lines)

    sections['B_herbal'] = b_herbal
    sections['B_astro'] = b_astro
    sections['B_cosmo'] = b_cosmo
    sections['B_pharma'] = b_pharma
    return sections

sections = parse_corpus()
a_cosmo = sections['A_cosmo']
a_herbal_a = sections['A_herbal_a']

print(f"A cosmo: {len(a_cosmo)} lines")
print(f"A herbal_a: {len(a_herbal_a)} lines")

def cooccur_test(section_lines, label, lf_onset, pos_rule1, target1, pos_rule2, target2):
    """Test co-occurrence of two positional rules in LF-class lines."""
    def get_pos(ln, pos):
        if pos == 'pos1': return ln[0] if ln else None
        if pos == 'pos2': return ln[1] if len(ln) >= 2 else None
        if pos == 'pen': return ln[-2] if len(ln) >= 3 else None
        return None

    # Eligibility: need len>=3 (covers pos1, pos2 without LF contamination, pen)
    lf_lines = [ln for ln in section_lines if get_onset(ln[-1]) == lf_onset]
    elig = [ln for ln in lf_lines if len(ln) >= 3]
    n_elig = len(elig)

    hits1 = [ln for ln in elig if get_onset(get_pos(ln, pos_rule1)) == target1]
    hits2 = [ln for ln in elig if get_onset(get_pos(ln, pos_rule2)) == target2]
    hits12 = [ln for ln in elig
              if get_onset(get_pos(ln, pos_rule1)) == target1
              and get_onset(get_pos(ln, pos_rule2)) == target2]

    n1, n2, n12 = len(hits1), len(hits2), len(hits12)
    p1 = n1 / n_elig if n_elig > 0 else 0
    p2 = n2 / n_elig if n_elig > 0 else 0
    expected = p1 * p2 * n_elig

    # Section-specific baselines
    all_p1 = [get_onset(get_pos(ln, pos_rule1)) for ln in section_lines if len(ln) >= 3]
    all_p2 = [get_onset(get_pos(ln, pos_rule2)) for ln in section_lines if len(ln) >= 3]
    base1 = Counter(all_p1).get(target1, 0) / len(all_p1) if all_p1 else 0
    base2 = Counter(all_p2).get(target2, 0) / len(all_p2) if all_p2 else 0
    E1 = p1 / base1 if base1 > 0 else float('inf')
    E2 = p2 / base2 if base2 > 0 else float('inf')

    E_cooccur = n12 / expected if expected > 0 else float('inf')
    flag1 = "CONF" if E1 >= 1.5 and n1 >= 10 else ("dir" if E1 >= 2.0 and n1 >= 5 else "")
    flag2 = "CONF" if E2 >= 1.5 and n2 >= 10 else ("dir" if E2 >= 2.0 and n2 >= 5 else "")

    print(f"\n{label} — {lf_onset}-LF: {pos_rule1}={target1} AND {pos_rule2}={target2}")
    print(f"  N_lf={len(lf_lines)}, N_elig={n_elig}")
    print(f"  {pos_rule1}={target1}: obs={n1}/{n_elig} ({p1:.1%}), base={base1:.1%}, E1={E1:.2f}× {flag1}")
    print(f"  {pos_rule2}={target2}: obs={n2}/{n_elig} ({p2:.1%}), base={base2:.1%}, E2={E2:.2f}× {flag2}")
    print(f"  Co-occurrence: obs={n12}/{n_elig}, expected={expected:.2f}, E_cooccur={E_cooccur:.2f}×")

    if E_cooccur >= 2.0 and n12 >= 3:
        status = f"ELEVATED (dir)"
    elif E_cooccur >= 1.5 and n12 >= 5:
        status = f"ELEVATED (CONF)"
    elif E_cooccur <= 0.5:
        status = "DEPLETED"
    else:
        status = "INDEPENDENT"
    print(f"  → {status}")
    return n1, n2, n12, expected, E_cooccur, n_elig

print("\n" + "="*60)
print("PART 1: A cosmo d-LF — y@pos1 AND ok@pen co-occurrence")
r1 = cooccur_test(a_cosmo, "A cosmo", "d", "pos1", "y", "pen", "ok")

print("\n" + "="*60)
print("PART 2: A herbal_a d-LF — ot@pos1 AND d-self@pos2 co-occurrence")
r2 = cooccur_test(a_herbal_a, "A herbal_a", "d", "pos1", "ot", "pos2", "d")

print("\n" + "="*60)
print("PART 3: A herbal_a ch-LF — ch@pos1 AND ch@pos2 co-occurrence")
r3 = cooccur_test(a_herbal_a, "A herbal_a", "ch", "pos1", "ch", "pos2", "ch")

print("\n" + "="*60)
print("PART 4: A herbal_a cth-LF — cth@pos2 AND d@pen (control)")
r4 = cooccur_test(a_herbal_a, "A herbal_a", "cth", "pos2", "cth", "pen", "d")

print("\n" + "="*60)
# Also test A cosmo d-LF pos1 specifically to verify F479
d_lf_cosmo = [ln for ln in a_cosmo if get_onset(ln[-1]) == 'd']
all_pos1_cosmo = Counter(get_onset(ln[0]) for ln in a_cosmo)
total_pos1_cosmo = sum(all_pos1_cosmo.values())
print(f"\nA cosmo d-LF: N={len(d_lf_cosmo)}, pos1 distribution:")
pos1_d = Counter(get_onset(ln[0]) for ln in d_lf_cosmo)
for onset, obs in sorted(pos1_d.items(), key=lambda x: -x[1])[:6]:
    base = all_pos1_cosmo.get(onset, 0) / total_pos1_cosmo
    E = (obs / len(d_lf_cosmo)) / base if base > 0 else 0
    flag = "CONF" if E >= 1.5 and obs >= 10 else ("dir" if E >= 2.0 and obs >= 5 else "")
    print(f"  {onset}: {obs}/{len(d_lf_cosmo)} ({obs/len(d_lf_cosmo):.1%}) vs {base:.1%}, E={E:.2f}× {flag}")

# And pen
all_pen_cosmo = Counter(get_onset(ln[-2]) for ln in a_cosmo if len(ln) >= 3)
total_pen_cosmo = sum(all_pen_cosmo.values())
elig_d_cosmo = [ln for ln in d_lf_cosmo if len(ln) >= 3]
pen_d = Counter(get_onset(ln[-2]) for ln in elig_d_cosmo)
print(f"\nA cosmo d-LF pen (N_elig={len(elig_d_cosmo)}):")
for onset, obs in sorted(pen_d.items(), key=lambda x: -x[1])[:6]:
    base = all_pen_cosmo.get(onset, 0) / total_pen_cosmo
    E = (obs / len(elig_d_cosmo)) / base if base > 0 else 0
    flag = "CONF" if E >= 1.5 and obs >= 10 else ("dir" if E >= 2.0 and obs >= 5 else "")
    print(f"  {onset}: {obs}/{len(elig_d_cosmo)} ({obs/len(elig_d_cosmo):.1%}) vs {base:.1%}, E={E:.2f}× {flag}")

print("\n=== SUMMARY ===")
tests = [
    ("A cosmo d-LF: y@pos1 AND ok@pen", r1),
    ("A herbal_a d-LF: ot@pos1 AND d-self@pos2", r2),
    ("A herbal_a ch-LF: ch@pos1 AND ch@pos2", r3),
    ("A herbal_a cth-LF: cth@pos2 AND d@pen", r4),
]
for label, (n1, n2, n12, expected, E, n_elig) in tests:
    if E >= 2.0 and n12 >= 3:
        status = "ELEVATED"
    elif E <= 0.5:
        status = "DEPLETED"
    else:
        status = "INDEPENDENT"
    print(f"  {label}: obs={n12}/{n_elig}, exp={expected:.2f}, E={E:.2f}× → {status}")
