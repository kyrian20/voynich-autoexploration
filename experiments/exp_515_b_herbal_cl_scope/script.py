"""
exp_515: B herbal within-folio CL survey + A cosmo/B herbal scope test for F490/F491
Questions:
  H_new_DD: Does B herbal have confirmed within-folio CL onset coupling rules?
  H_new_CT: Do F490 (qot→ch CL) and F491 (d→qot CL) from A herbal_a appear in A cosmo or B herbal?
Method:
  Within-folio consecutive LF-onset pairs. Section-specific LF baselines.
  E = obs(A→B) / (base_A × base_B × N_pairs)
  Confirmation thresholds: CONF = E≥1.5×/N≥10; dir = E≥2.0×/N≥5; (dir) = E≥2.5×/N≥3
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

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
    folio_lines = defaultdict(list)
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
        folio_lines[n].append(words)
    return folio_lines

folio_lines = parse_corpus()

# Build sections
a_herbal_by_folio = {}
a_cosmo_by_folio = {}
b_herbal_by_folio = {}

for n, lines in folio_lines.items():
    if is_b_dialect(lines):
        if n <= 72:
            b_herbal_by_folio[n] = lines
    else:
        if n <= 56:
            a_herbal_by_folio[n] = lines
        elif 85 <= n <= 102:
            a_cosmo_by_folio[n] = lines

print(f"A herbal_a: {len(a_herbal_by_folio)} folios, {sum(len(v) for v in a_herbal_by_folio.values())} lines")
print(f"A cosmo: {len(a_cosmo_by_folio)} folios, {sum(len(v) for v in a_cosmo_by_folio.values())} lines")
print(f"B herbal: {len(b_herbal_by_folio)} folios, {sum(len(v) for v in b_herbal_by_folio.values())} lines")


def get_within_folio_pairs(section_by_folio):
    pairs = []
    for n in sorted(section_by_folio):
        lines = section_by_folio[n]
        lf_onsets = [get_onset(ln[-1]) for ln in lines if ln]
        for i in range(len(lf_onsets) - 1):
            if lf_onsets[i] and lf_onsets[i+1]:
                pairs.append((lf_onsets[i], lf_onsets[i+1]))
    return pairs


def cl_survey(section_by_folio, label, min_obs=3, min_e=1.5, top_n=15):
    pairs = get_within_folio_pairs(section_by_folio)
    N = len(pairs)
    all_lines = [ln for lines in section_by_folio.values() for ln in lines]
    lf_dist = Counter(get_onset(ln[-1]) for ln in all_lines if ln)
    total_lf = sum(lf_dist.values())

    print(f"\n{'='*60}")
    print(f"{label} — within-folio CL survey")
    print(f"  Folios: {len(section_by_folio)}, Lines: {len(all_lines)}, Pairs: {N}")
    print(f"  Top LF classes: {dict(lf_dist.most_common(8))}")

    pair_counts = Counter(pairs)
    results = []
    for (a, b), obs in pair_counts.items():
        if obs < min_obs:
            continue
        base_a = lf_dist.get(a, 0) / total_lf
        base_b = lf_dist.get(b, 0) / total_lf
        if base_a == 0 or base_b == 0:
            continue
        exp = base_a * base_b * N
        E = obs / exp
        if E < min_e:
            continue
        results.append((a, b, obs, exp, E))

    results.sort(key=lambda x: -x[4])

    print(f"\n  {'A→B':<16} {'obs':>5} {'exp':>6} {'E':>7}  status")
    for a, b, obs, exp, E in results[:top_n]:
        flag = 'CONF' if E >= 1.5 and obs >= 10 else \
               ('dir' if E >= 2.0 and obs >= 5 else \
               '(dir)' if E >= 2.5 and obs >= 3 else '')
        print(f"  {a}→{b:<12} {obs:>5}  {exp:>6.2f}  {E:>6.2f}×  {flag}")

    return results, pairs, lf_dist, N


# Run CL surveys
a_herbal_results, a_herbal_pairs, a_herbal_lf, a_herbal_N = cl_survey(a_herbal_by_folio, "A herbal_a")
a_cosmo_results, a_cosmo_pairs, a_cosmo_lf, a_cosmo_N = cl_survey(a_cosmo_by_folio, "A cosmo")
b_herbal_results, b_herbal_pairs, b_herbal_lf, b_herbal_N = cl_survey(b_herbal_by_folio, "B herbal")


# Focused scope test: F490 (qot→ch) and F491 (d→qot) in A cosmo and B herbal
print("\n\n=== F490/F491 SCOPE TEST ===")
print("A herbal_a rules: F491 d→qot (E=1.64×/N=13,CONF), F490 qot→ch (E=2.00×/N=12,CONF)")

for label, pairs, lf_dist, N in [
    ("A herbal_a", a_herbal_pairs, a_herbal_lf, a_herbal_N),
    ("A cosmo", a_cosmo_pairs, a_cosmo_lf, a_cosmo_N),
    ("B herbal", b_herbal_pairs, b_herbal_lf, b_herbal_N),
]:
    total_lf = sum(lf_dist.values())
    pair_counts = Counter(pairs)
    print(f"\n  {label}:")
    for (a, b) in [('d', 'qot'), ('qot', 'ch'), ('d', 'ch')]:
        obs = pair_counts.get((a, b), 0)
        base_a = lf_dist.get(a, 0) / total_lf
        base_b = lf_dist.get(b, 0) / total_lf
        if base_a == 0 or base_b == 0:
            E = float('nan')
            exp = 0
        else:
            exp = base_a * base_b * N
            E = obs / exp if exp > 0 else float('inf')
        flag = 'CONF' if E >= 1.5 and obs >= 10 else \
               ('dir' if E >= 2.0 and obs >= 5 else \
               '(dir)' if E >= 2.5 and obs >= 3 else '')
        print(f"    {a}→{b}: obs={obs}, exp={exp:.2f}, E={E:.2f}× {flag}")


# B herbal: scope for F444's claimed ok→y and d→sh CL rules (using section-specific baselines)
print("\n\n=== F444 B HERBAL SCOPE (section-specific baseline) ===")
print("F444 claimed: B herbal ok→y CL, d→sh CL (from mixed-section survey)")
b_total_lf = sum(b_herbal_lf.values())
b_pair_counts = Counter(b_herbal_pairs)
for (a, b) in [('ok', 'y'), ('d', 'sh'), ('ch', 'qot'), ('qot', 'ch'), ('ok', 'ch'), ('d', 'ok')]:
    obs = b_pair_counts.get((a, b), 0)
    base_a = b_herbal_lf.get(a, 0) / b_total_lf
    base_b = b_herbal_lf.get(b, 0) / b_total_lf
    if base_a == 0 or base_b == 0:
        print(f"  B herbal {a}→{b}: insufficient LF classes")
        continue
    exp = base_a * base_b * b_herbal_N
    E = obs / exp if exp > 0 else float('inf')
    flag = 'CONF' if E >= 1.5 and obs >= 10 else \
           ('dir' if E >= 2.0 and obs >= 5 else \
           '(dir)' if E >= 2.5 and obs >= 3 else '')
    print(f"  B herbal {a}→{b}: obs={obs}, exp={exp:.2f}, E={E:.2f}× {flag}")


# A/B herbal CL comparison: same LF class pairs, compare E values
print("\n\n=== A/B HERBAL CL COMPARISON (top rules per section) ===")
a_total_lf = sum(a_herbal_lf.values())
a_pair_counts = Counter(a_herbal_pairs)

print(f"\n  A herbal_a top CL rules (E≥1.5×, obs≥5):")
for a, b, obs, exp, E in a_herbal_results[:12]:
    flag = 'CONF' if E >= 1.5 and obs >= 10 else ('dir' if E >= 2.0 and obs >= 5 else '(dir)')
    print(f"    {a}→{b}: E={E:.2f}×/N={obs} {flag}")
    # Check same pair in B herbal
    b_obs = b_pair_counts.get((a, b), 0)
    b_base_a = b_herbal_lf.get(a, 0) / b_total_lf if b_total_lf else 0
    b_base_b = b_herbal_lf.get(b, 0) / b_total_lf if b_total_lf else 0
    if b_base_a > 0 and b_base_b > 0:
        b_exp = b_base_a * b_base_b * b_herbal_N
        b_E = b_obs / b_exp
        print(f"      → B herbal same pair: E={b_E:.2f}×/N={b_obs}")
    else:
        print(f"      → B herbal: insufficient base")
