"""
exp_509: A stars pen survey + B herbal pen complete survey

H_new_CP: Does A stars (186 lines) have confirmed pen routing rules?
H_new_CQ: Does B herbal (272 lines) have confirmed pen routing rules?
Also: compile cross-section pen grammar summary table.
"""

import re
from collections import defaultdict, Counter

CORPUS = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"
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
        if n <= 56:
            sections['A_herbal_a'].append(words)
        elif n <= 72:
            sections['A_stars'].append(words)
        elif n <= 84:
            sections['A_herbal_b_raw'].append(words)
        elif n <= 102:
            sections['A_cosmo'].append(words)
        sections[f'folio_{n}'].append(words)
    b_herbal, b_astro, b_cosmo, b_pharma = [], [], [], []
    for key, lines in sections.items():
        m = re.match(r'folio_(\d+)', key)
        if not m:
            continue
        n = int(m.group(1))
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
    sections['B_herbal'] = b_herbal
    sections['B_astro'] = b_astro
    sections['B_cosmo'] = b_cosmo
    sections['B_pharma'] = b_pharma
    return sections

sections = parse_corpus()
a_stars = sections['A_stars']
b_herbal = sections['B_herbal']

print(f"A stars: {len(a_stars)} lines")
print(f"B herbal: {len(b_herbal)} lines")

def run_pen_survey(section_lines, label, min_lf=8, top_n=7):
    all_pen = []
    for ln in section_lines:
        if len(ln) >= 3:
            all_pen.append(get_onset(ln[-2]))
    pen_baseline = Counter(all_pen)
    total_pen = sum(pen_baseline.values())

    print(f"\n=== {label} pen survey ===")
    print(f"Lines: {len(section_lines)} | N_pen_elig: {total_pen}")
    print(f"Pen baseline top-6: {sorted(pen_baseline.items(), key=lambda x:-x[1])[:6]}")

    by_lf = defaultdict(list)
    for ln in section_lines:
        lf = get_onset(ln[-1])
        if lf:
            by_lf[lf].append(ln)

    all_conf = []
    for lf_onset, lf_lines in sorted(by_lf.items(), key=lambda x: -len(x[1])):
        if len(lf_lines) < min_lf:
            continue
        elig = [ln for ln in lf_lines if len(ln) >= 3]
        n_elig = len(elig)
        if n_elig < 5:
            continue

        pen_counts = Counter(get_onset(ln[-2]) for ln in elig)
        row = []
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
            row.append((onset, obs, E, flag))

        row.sort(key=lambda x: -x[2])
        conf_findings = [(o, n, e, f) for o, n, e, f in row if f]

        print(f"\n  {lf_onset}-LF (N={len(lf_lines)}, N_elig={n_elig}):")
        for onset, obs, E, flag in row[:top_n]:
            base_rate = pen_baseline.get(onset, 0) / total_pen
            marker = f"  *** {flag}" if flag else ""
            print(f"    {onset}: {obs}/{n_elig} ({obs/n_elig:.1%}) vs {base_rate:.1%}, E={E:.2f}×{marker}")

        if conf_findings:
            all_conf.append((lf_onset, conf_findings))

    print(f"\n  --- CONF/DIR summary for {label} ---")
    if not all_conf:
        print("  (none)")
    for lf_onset, findings in all_conf:
        for onset, obs, E, flag in findings:
            print(f"  {lf_onset}-LF → {onset}@pen: E={E:.2f}×/N={obs} [{flag}]")
    return all_conf

print("\n" + "="*60)
a_stars_results = run_pen_survey(a_stars, "A stars", min_lf=8)

print("\n" + "="*60)
b_herbal_results = run_pen_survey(b_herbal, "B herbal", min_lf=8)

# Also test d-LF pen specifically for B herbal and B pharma to complete picture
print("\n" + "="*60)
print("=== d-LF pen cross-section focused test ===")
for label, sec in [
    ("A herbal_a", sections['A_herbal_a']),
    ("A cosmo", sections['A_cosmo']),
    ("B herbal", sections['B_herbal']),
    ("B astro", sections['B_astro']),
    ("B pharma", sections['B_pharma']),
]:
    all_pen = Counter(get_onset(ln[-2]) for ln in sec if len(ln) >= 3)
    total = sum(all_pen.values())
    d_lf = [ln for ln in sec if get_onset(ln[-1]) == 'd']
    elig = [ln for ln in d_lf if len(ln) >= 3]
    if not elig:
        print(f"  {label}: no d-LF eligible")
        continue
    d_pen = Counter(get_onset(ln[-2]) for ln in elig)
    # Print top 5 by E
    results_d = []
    for onset, obs in d_pen.most_common():
        base = all_pen.get(onset, 0) / total if total > 0 else 0
        E = obs / (base * len(elig)) if base * len(elig) > 0 else 0
        flag = ""
        if E >= 1.5 and obs >= 10:
            flag = "CONF"
        elif E >= 2.0 and obs >= 5:
            flag = "dir"
        elif E >= 2.0 and obs >= 3:
            flag = "(dir)"
        results_d.append((onset, obs, E, flag))
    results_d.sort(key=lambda x: -x[2])
    print(f"\n  {label} d-LF (N={len(d_lf)}, N_elig={len(elig)}):")
    for onset, obs, E, flag in results_d[:5]:
        base = all_pen.get(onset, 0) / total
        marker = f" [{flag}]" if flag else ""
        print(f"    {onset}: {obs}/{len(elig)} E={E:.2f}×{marker}")

print("\n=== CROSS-SECTION PEN GRAMMAR SUMMARY ===")
print("\nConfirmed pen rules by section:")
summary = {
    "A herbal_a": ["F474: cth→d(E=1.70×/N=18)", "F485: ok-self(E=2.73×/N=12)"],
    "A cosmo": ["F486: ch→o(E=2.05×/N=10)", "F487: d→ok(E=1.71×/N=11)", "F488: o→ch(E=2.12×/N=11)"],
    "A stars": [f for _, findings in a_stars_results for onset, obs, E, f_str in findings for f in [f"{_}-LF→{onset}@pen(E={E:.2f}×/N={obs},{f_str})"]],
    "B herbal": [f for _, findings in b_herbal_results for onset, obs, E, f_str in findings for f in [f"{_}-LF→{onset}@pen(E={E:.2f}×/N={obs},{f_str})"]],
    "B astro": ["F481: qok→sh(E=2.12×/N=20)", "F482: d-self(E=1.96×/N=12)", "F483: l→ch(E=1.89×/N=22)"],
    "B pharma": ["F459: ok→a(B-wide)", "F460: ot-self(B-wide)", "F484: l-self(E=2.18×/N=17)"],
    "B cosmo": ["none (too small)"],
}
for sec, rules in summary.items():
    rules_str = "; ".join(rules) if rules else "(none)"
    print(f"  {sec}: {rules_str}")
