"""
exp_507: A herbal ot-LF pen scope test

Hypothesis H_new_CM: ot-LF → cth@pen (E=3.58×/N=9, dir) and ot-self@pen (E=3.51×/N=8, dir)
are both one step below N=10 confirmation. Can A herbal_b (n=57-84) contribute additional
ot-LF lines to push these over threshold?

NOTE: A sections are identified by folio number ONLY (no B-dialect filter for A sections).
B-dialect filter is applied only to B-range folios (n=73+) to separate B sub-sections.
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
    """Parse corpus using established approach:
    - A sections: classified by folio number (no dialect filter needed)
    - B sections: classified by folio number + B-dialect check
    """
    a_sections = defaultdict(list)  # keyed by folio n
    b_folio_lines = defaultdict(list)  # keyed by folio n

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
        # A sections by folio number (no dialect check)
        if n <= 102:
            a_sections[n].append(words)
        else:
            b_folio_lines[n].append(words)

    # A sections by folio range
    a_herbal_a = []  # n <= 56
    a_stars = []     # n = 57-72
    a_herbal_b = []  # n = 73-84 (labeled herbal_b in prior work)
    a_cosmo = []     # n = 85-102

    # Actually: A sections follow folio ranges from SOUL.md:
    # A_herbal_a: n<=56, A_stars: n<=72, A_herbal_b: n<=84, A_cosmo: n<=102
    # But 57-72 = stars, 73-84 = herbal_b, 85-102 = cosmo
    for n, lines in a_sections.items():
        if n <= 56:
            a_herbal_a.extend(lines)
        elif n <= 72:
            a_stars.extend(lines)
        elif n <= 84:
            a_herbal_b.extend(lines)
        elif n <= 102:
            a_cosmo.extend(lines)

    # B sections: need dialect check to distinguish from A-like folios in B range
    b_herbal = []
    b_astro = []
    b_cosmo = []
    b_pharma = []

    for n, lines in b_folio_lines.items():
        if not is_b_dialect(lines):
            continue
        if n <= 72:
            b_herbal.extend(lines)
        elif n <= 84:
            b_astro.extend(lines)
        elif n <= 102:
            b_cosmo.extend(lines)
        elif n <= 116:
            b_pharma.extend(lines)

    return {
        'A_herbal_a': a_herbal_a,
        'A_stars': a_stars,
        'A_herbal_b': a_herbal_b,
        'A_cosmo': a_cosmo,
        'B_herbal': b_herbal,
        'B_astro': b_astro,
        'B_cosmo': b_cosmo,
        'B_pharma': b_pharma,
    }

sections = parse_corpus()
a_herbal_a = sections['A_herbal_a']
a_herbal_b = sections['A_herbal_b']
a_herbal_combined = a_herbal_a + a_herbal_b

print("Section sizes:")
for k, v in sections.items():
    print(f"  {k}: {len(v)} lines")
print(f"  A_herbal_combined: {len(a_herbal_combined)} lines")

def focused_pen_test(section_lines, label, lf_onset, targets=None):
    # Build pen baseline from all eligible lines in this section
    all_pen = []
    for ln in section_lines:
        if len(ln) >= 3:
            all_pen.append(get_onset(ln[-2]))
    pen_baseline = Counter(all_pen)
    total_pen = sum(pen_baseline.values())

    lf_lines = [ln for ln in section_lines if get_onset(ln[-1]) == lf_onset]
    elig = [ln for ln in lf_lines if len(ln) >= 3]
    n_elig = len(elig)

    print(f"\n{label} — {lf_onset}-LF (N_lf={len(lf_lines)}, N_elig={n_elig})")
    print(f"  Pen baseline (total {total_pen} obs): "
          f"ch={pen_baseline.get('ch',0)/total_pen:.1%} "
          f"d={pen_baseline.get('d',0)/total_pen:.1%} "
          f"cth={pen_baseline.get('cth',0)/total_pen:.1%} "
          f"ot={pen_baseline.get('ot',0)/total_pen:.1%}")

    pen_counts = Counter(get_onset(ln[-2]) for ln in elig)

    results = []
    for onset, obs in pen_counts.most_common():
        base_rate = pen_baseline.get(onset, 0) / total_pen if total_pen > 0 else 0
        expected = base_rate * n_elig
        E = obs / expected if expected > 0 else float('inf')
        flag = ""
        if E >= 1.5 and obs >= 10:
            flag = "CONF"
        elif E >= 2.0 and obs >= 5:
            flag = "dir"
        elif E >= 2.0 and obs >= 3:
            flag = "(dir)"
        results.append((onset, obs, E, flag))

    results.sort(key=lambda x: -x[2])
    for onset, obs, E, flag in results[:8]:
        base_rate = pen_baseline.get(onset, 0) / total_pen
        marker = f"  *** {flag}" if flag else ""
        print(f"    {onset}: obs={obs}/{n_elig} ({obs/n_elig:.1%}) vs base={base_rate:.1%}, E={E:.2f}×{marker}")

    if targets:
        print(f"  Focus targets:")
        for t in targets:
            row = next((r for r in results if r[0] == t), None)
            if row:
                base_rate = pen_baseline.get(t, 0) / total_pen
                print(f"    {t}: obs={row[1]}/{n_elig} ({row[1]/n_elig:.1%}) vs {base_rate:.1%}, E={row[2]:.2f}× [{row[3] if row[3] else 'none'}]")
            else:
                print(f"    {t}: obs=0/{n_elig}, E=0×")
    return results

print("\n" + "="*60)
print("A herbal_a ot-LF pen (exp_506 replication check)")
r_ah_a_ot = focused_pen_test(a_herbal_a, "A herbal_a", "ot", ["cth", "ot"])

print("\n" + "="*60)
print("A herbal_b ot-LF pen (n=73-84, A-dialect)")
r_ah_b_ot = focused_pen_test(a_herbal_b, "A herbal_b", "ot", ["cth", "ot"])

print("\n" + "="*60)
print("A herbal combined (a+b) ot-LF pen")
r_ah_comb_ot = focused_pen_test(a_herbal_combined, "A herbal combined", "ot", ["cth", "ot"])

print("\n" + "="*60)
print("A herbal combined ok-LF pen (F485 scope)")
r_ah_comb_ok = focused_pen_test(a_herbal_combined, "A herbal combined", "ok", ["ok", "a"])

print("\n=== SUMMARY ===")
print("\not-LF pen summary:")
for label, results, n_elig_direct in [
    ("A herbal_a",
     r_ah_a_ot,
     len([ln for ln in a_herbal_a if get_onset(ln[-1])=='ot' and len(ln)>=3])),
    ("A herbal_b",
     r_ah_b_ot,
     len([ln for ln in a_herbal_b if get_onset(ln[-1])=='ot' and len(ln)>=3])),
    ("A herbal combined",
     r_ah_comb_ot,
     len([ln for ln in a_herbal_combined if get_onset(ln[-1])=='ot' and len(ln)>=3])),
]:
    cth = next((r for r in results if r[0]=='cth'), None)
    ot = next((r for r in results if r[0]=='ot'), None)
    cth_str = f"cth: {cth[1]}/{n_elig_direct} E={cth[2]:.2f}× [{cth[3] or 'none'}]" if cth else "cth: 0"
    ot_str = f"ot-self: {ot[1]}/{n_elig_direct} E={ot[2]:.2f}× [{ot[3] or 'none'}]" if ot else "ot-self: 0"
    print(f"  {label}: N_elig={n_elig_direct} | {cth_str} | {ot_str}")

print("\nok-LF pen summary (A herbal combined):")
ok_comb = r_ah_comb_ok
ok_self = next((r for r in ok_comb if r[0]=='ok'), None)
ok_a = next((r for r in ok_comb if r[0]=='a'), None)
n_ok_elig = len([ln for ln in a_herbal_combined if get_onset(ln[-1])=='ok' and len(ln)>=3])
print(f"  N_ok_elig={n_ok_elig}")
if ok_self: print(f"  ok-self: obs={ok_self[1]}/{n_ok_elig} E={ok_self[2]:.2f}× [{ok_self[3] or 'none'}]")
if ok_a: print(f"  ok→a: obs={ok_a[1]}/{n_ok_elig} E={ok_a[2]:.2f}× [{ok_a[3] or 'none'}]")
