"""
exp_506: A herbal_a pen grammar complete survey

Hypothesis H_new_CK: Beyond F474 (cth-LF→d@pen), does A herbal_a have additional
confirmed pen routing rules? Near-threshold directionals from prior experiments:
  - ok-self@pen (E=3.39×/N=7 in F474 context)
  - ot-LF → cth@pen (dir, E=3.70×/N=9 from exp_492)
  - ot-self@pen (E=3.27×/N=6 from F456 context)

Full pen distribution for all major LF classes with min N.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

# ── corpus loading ───────────────────────────────────────────────────────────
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
        # A sections
        if n <= 56:
            sections['A_herbal_a'].append(words)
        elif n <= 72:
            sections['A_stars'].append(words)
        elif n <= 84:
            sections['A_herbal_b'].append(words)
        elif n <= 102:
            sections['A_cosmo'].append(words)
        # B sections (need dialect check — done separately)
        sections[f'folio_{n}'].append(words)
    return sections

sections = parse_corpus()

# Separate B sections by dialect check
b_herbal_lines = []
b_astro_lines = []
b_cosmo_lines = []
b_pharma_lines = []

for folio_key, lines in sections.items():
    m = re.match(r'folio_(\d+)', folio_key)
    if not m:
        continue
    n = int(m.group(1))
    if not is_b_dialect(lines):
        continue
    if n <= 72:
        b_herbal_lines.extend(lines)
    elif n <= 84:
        b_astro_lines.extend(lines)
    elif n <= 102:
        b_cosmo_lines.extend(lines)
    elif n <= 116:
        b_pharma_lines.extend(lines)

a_herbal_a = sections['A_herbal_a']

print(f"A herbal_a: {len(a_herbal_a)} lines")

# ── pen survey ───────────────────────────────────────────────────────────────
def run_pen_survey(section_lines, label, min_lf=8, top_n=7):
    """
    For each LF class with N_lf >= min_lf:
      - Compute pen-specific baseline (distribution of pen onsets across ALL eligible lines)
      - Compute observed pen onset distribution for that LF class
      - Report enrichment E = obs / (base_rate * N_elig)
      - Flag: CONF (E>=1.5 and N>=10), dir (E>=2.0 and N>=5), (dir) (E>=2.0 and N>=3)
    Eligible = len(line) >= 3 (so pen = ws[-2] is not the same as pos1 or LF)
    """
    # Build pen baseline from all eligible lines
    all_pen = []
    for ln in section_lines:
        if len(ln) >= 3:
            all_pen.append(get_onset(ln[-2]))
    pen_baseline = Counter(all_pen)
    total_pen = sum(pen_baseline.values())

    print(f"\n=== {label} pen survey ===")
    print(f"Total lines: {len(section_lines)} | Eligible (len>=3): {total_pen} pen observations")
    print(f"Pen baseline top-10: {sorted(pen_baseline.items(), key=lambda x:-x[1])[:10]}")

    # Group lines by LF onset
    by_lf = defaultdict(list)
    for ln in section_lines:
        lf = get_onset(ln[-1])
        if lf:
            by_lf[lf].append(ln)

    # For each LF class with enough lines
    results = []
    for lf_onset, lf_lines in sorted(by_lf.items(), key=lambda x: -len(x[1])):
        if len(lf_lines) < min_lf:
            continue
        # Eligible for pen analysis
        elig = [ln for ln in lf_lines if len(ln) >= 3]
        n_elig = len(elig)
        if n_elig < 5:
            continue

        pen_counts = Counter(get_onset(ln[-2]) for ln in elig)

        # Compute E for each pen onset
        row = []
        for onset in sorted(pen_counts.keys(), key=lambda o: -pen_counts[o]):
            obs = pen_counts[onset]
            base_rate = pen_baseline.get(onset, 0) / total_pen if total_pen > 0 else 0
            expected = base_rate * n_elig
            E = obs / expected if expected > 0 else float('inf')
            if E >= 2.0 and obs >= 3:
                flag = "CONF" if E >= 1.5 and obs >= 10 else "dir" if obs >= 5 else "(dir)"
            elif E >= 1.5 and obs >= 10:
                flag = "CONF"
            else:
                flag = ""
            row.append((onset, obs, E, flag))

        # Sort by E descending
        row.sort(key=lambda x: -x[2])

        # Print top findings
        conf_findings = [(o,n,e,f) for o,n,e,f in row if f]
        print(f"\n  {lf_onset}-LF (N={len(lf_lines)}, N_elig={n_elig}):")
        # Show top_n by E
        for onset, obs, E, flag in row[:top_n]:
            base_rate = pen_baseline.get(onset, 0) / total_pen
            marker = f"  *** {flag}" if flag else ""
            print(f"    pen={onset}: obs={obs}/{n_elig} ({obs/n_elig:.1%}) vs base={base_rate:.1%}, E={E:.2f}×{marker}")

        if conf_findings:
            results.append((lf_onset, conf_findings))

    print(f"\n  --- CONFIRMED/DIR FINDINGS FOR {label} ---")
    for lf_onset, findings in results:
        for onset, obs, E, flag in findings:
            print(f"  {lf_onset}-LF → {onset}@pen: E={E:.2f}×/N={obs} [{flag}]")

    return results

# Run A herbal_a pen survey
a_herbal_results = run_pen_survey(a_herbal_a, "A herbal_a", min_lf=8)

# Also run B cosmo pen survey (small but completes B-dialect picture)
print("\n" + "="*60)
b_cosmo_results = run_pen_survey(b_cosmo_lines, "B cosmo", min_lf=5)

print("\n=== SUMMARY ===")
print("\nA herbal_a confirmed/directional pen rules:")
for lf_onset, findings in a_herbal_results:
    for onset, obs, E, flag in findings:
        print(f"  {lf_onset}-LF → {onset}@pen: E={E:.2f}×/N={obs} [{flag}]")

print("\nB cosmo confirmed/directional pen rules:")
for lf_onset, findings in b_cosmo_results:
    for onset, obs, E, flag in findings:
        print(f"  {lf_onset}-LF → {onset}@pen: E={E:.2f}×/N={obs} [{flag}]")

# Cross-reference known findings
print("\n=== KNOWN FINDINGS CHECK ===")
print("F474: A herbal_a cth-LF → d@pen (expected CONF, E~1.61×/N~18)")
print("  → should appear above with ~same values")
print("F456 context: ot-LF → cth@pen (dir, E~3.70×/N~9 from exp_492)")
print("  → may reach CONF if N>=10 in this run")
print("F456 context: ok-self@pen (dir, E~3.39×/N~7 from F474 context)")
print("  → check if N>=10 now")
