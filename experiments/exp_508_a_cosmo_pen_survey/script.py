"""
exp_508: A cosmo pen grammar survey + ok→a@pen cross-dialect test

H_new_CO: Does A cosmo (455 lines) have confirmed pen routing rules?
H_new_CN: Is ok→a@pen (B-dialect CONF F459; A herbal_a dir) present manuscript-wide?
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
    sections = defaultdict(list)
    b_folio = defaultdict(list)
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
        # A sections by folio number
        if n <= 56:
            sections['A_herbal_a'].append(words)
        elif n <= 72:
            sections['A_stars'].append(words)
        elif n <= 84:
            sections['A_herbal_b'].append(words)
        elif n <= 102:
            sections['A_cosmo'].append(words)
        # B sections via folio dict for dialect check
        sections[f'folio_{n}'].append(words)

    # Build B sections
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

a_cosmo = sections['A_cosmo']
a_herbal_a = sections['A_herbal_a']
b_herbal = sections['B_herbal']
b_astro = sections['B_astro']
b_pharma = sections['B_pharma']
b_cosmo = sections['B_cosmo']

print(f"A cosmo: {len(a_cosmo)} lines")
print(f"A herbal_a: {len(a_herbal_a)} lines")
print(f"B herbal: {len(b_herbal)} lines")
print(f"B astro: {len(b_astro)} lines")
print(f"B pharma: {len(b_pharma)} lines")

def run_pen_survey(section_lines, label, min_lf=8, top_n=7):
    all_pen = []
    for ln in section_lines:
        if len(ln) >= 3:
            all_pen.append(get_onset(ln[-2]))
    pen_baseline = Counter(all_pen)
    total_pen = sum(pen_baseline.values())

    print(f"\n=== {label} pen survey ===")
    print(f"Lines: {len(section_lines)} | N_pen_elig: {total_pen}")
    print(f"Pen baseline top-8: {sorted(pen_baseline.items(), key=lambda x:-x[1])[:8]}")

    by_lf = defaultdict(list)
    for ln in section_lines:
        lf = get_onset(ln[-1])
        if lf:
            by_lf[lf].append(ln)

    results = []
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
        conf_findings = [(o,n,e,f) for o,n,e,f in row if f]

        print(f"\n  {lf_onset}-LF (N={len(lf_lines)}, N_elig={n_elig}):")
        for onset, obs, E, flag in row[:top_n]:
            base_rate = pen_baseline.get(onset, 0) / total_pen
            marker = f"  *** {flag}" if flag else ""
            print(f"    pen={onset}: obs={obs}/{n_elig} ({obs/n_elig:.1%}) vs base={base_rate:.1%}, E={E:.2f}×{marker}")

        if conf_findings:
            results.append((lf_onset, conf_findings))

    print(f"\n  --- CONF/DIR for {label} ---")
    for lf_onset, findings in results:
        for onset, obs, E, flag in findings:
            print(f"    {lf_onset}-LF → {onset}@pen: E={E:.2f}×/N={obs} [{flag}]")
    return results

# ── PART 1: A cosmo pen survey ──────────────────────────────────────────────
print("\n" + "="*60)
print("PART 1: A cosmo pen survey (H_new_CO)")
a_cosmo_results = run_pen_survey(a_cosmo, "A cosmo", min_lf=8)

# ── PART 2: ok→a@pen cross-dialect scope ────────────────────────────────────
print("\n" + "="*60)
print("PART 2: ok→a@pen cross-dialect scope test (H_new_CN)")

def ok_pen_focused(section_lines, label):
    """Focused ok-LF pen analysis: report ok-self and a-class enrichment."""
    all_pen = []
    for ln in section_lines:
        if len(ln) >= 3:
            all_pen.append(get_onset(ln[-2]))
    pen_baseline = Counter(all_pen)
    total_pen = sum(pen_baseline.values())

    ok_lf = [ln for ln in section_lines if get_onset(ln[-1]) == 'ok']
    elig = [ln for ln in ok_lf if len(ln) >= 3]
    n_elig = len(elig)

    pen_counts = Counter(get_onset(ln[-2]) for ln in elig)

    ok_obs = pen_counts.get('ok', 0)
    ok_base = pen_baseline.get('ok', 0) / total_pen if total_pen > 0 else 0
    ok_E = ok_obs / (ok_base * n_elig) if ok_base * n_elig > 0 else 0

    a_obs = pen_counts.get('a', 0)
    a_base = pen_baseline.get('a', 0) / total_pen if total_pen > 0 else 0
    a_E = a_obs / (a_base * n_elig) if a_base * n_elig > 0 else 0

    ok_flag = "CONF" if ok_E >= 1.5 and ok_obs >= 10 else ("dir" if ok_E >= 2.0 and ok_obs >= 5 else ("(dir)" if ok_E >= 2.0 and ok_obs >= 3 else ""))
    a_flag = "CONF" if a_E >= 1.5 and a_obs >= 10 else ("dir" if a_E >= 2.0 and a_obs >= 5 else ("(dir)" if a_E >= 2.0 and a_obs >= 3 else ""))

    print(f"  {label} ok-LF: N={len(ok_lf)}, N_elig={n_elig}")
    print(f"    ok-self@pen: obs={ok_obs}/{n_elig} ({ok_obs/n_elig:.1%}) vs base={ok_base:.1%}, E={ok_E:.2f}× [{ok_flag}]")
    print(f"    ok→a@pen:    obs={a_obs}/{n_elig} ({a_obs/n_elig:.1%}) vs base={a_base:.1%}, E={a_E:.2f}× [{a_flag}]")
    return (ok_obs, ok_E, ok_flag, a_obs, a_E, a_flag, n_elig)

print()
results_by_section = {}
for label, sec in [
    ("A herbal_a", a_herbal_a),
    ("A cosmo", a_cosmo),
    ("B herbal", b_herbal),
    ("B astro", b_astro),
    ("B pharma", b_pharma),
]:
    r = ok_pen_focused(sec, label)
    results_by_section[label] = r

# Combined manuscript ok-LF a@pen
print("\n  --- Combined manuscript ok-LF → a@pen ---")
all_ok_a_obs = sum(r[3] for r in results_by_section.values())
all_ok_elig = sum(r[6] for r in results_by_section.values())
# For combined, need weighted baseline average
# Use A herbal_a baseline as reference (but note this mixes baselines)
print(f"  Note: combining across sections with different baselines — treat as indicative only.")
print(f"  Total ok-LF elig: {all_ok_elig}")
print(f"  Total ok→a@pen obs: {all_ok_a_obs}")
for label, r in results_by_section.items():
    ok_obs, ok_E, ok_flag, a_obs, a_E, a_flag, n_elig = r
    print(f"    {label}: ok→a E={a_E:.2f}×/N={a_obs} [{a_flag}] | ok-self E={ok_E:.2f}×/N={ok_obs} [{ok_flag}]")

print("\n=== SUMMARY ===")
print("\nA cosmo pen confirmed/dir rules:")
for lf_onset, findings in a_cosmo_results:
    for onset, obs, E, flag in findings:
        print(f"  {lf_onset}-LF → {onset}@pen: E={E:.2f}×/N={obs} [{flag}]")
