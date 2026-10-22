"""
exp_520: o-LF pos1=y cross-section complete survey + t-LF A stars positional profile

Goals:
1. H_new_EB: Complete o-LF pos1=y survey across ALL sections:
   - A: herbal_a (known dir), herbal_b (known dir), cosmo (known near-threshold), stars (untested)
   - B: pharma (untested), astro (known (dir)), herbal (untested), cosmo (untested)
   Hypothesis: o-LF pos1=y is manuscript-wide (or at least broader than just herbal sections)

2. H_new_EC: ol-LF pos1=y confirmation in A herbal_a: E=1.68×/N=5 (borderline)
   - Can we get closer to dir with exact methodology?
   - Also test ol-LF pos1=y scope in other sections

3. H_new_ED: t-LF positional profile in A stars (t-LF dominant section, F446)
   - A stars t-LF: pos1 dist, pos2 dist, pen dist
   - Compare with A herbal_a t-LF profiles (t-LF pos2: ch flat, y depleted)
   - Does A stars t-LF have any confirmed pos1/pen rules?

4. H_new_EE: ot-LF pos2=y borderline confirmation attempt
   - A herbal_a ot-LF pos2=y: E=3.60×/N=4 ((dir)) — one below dir threshold (needs N=5)
   - Full recount with all A herbal_a ot-LF lines: is N_elig exactly 40? Could it be higher?
   - Also check: does ot-LF pos2=y extend to A herbal_b?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

# ── corpus parser ─────────────────────────────────────────────────────────────
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

ONSET_PRIORITY = ['qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol',
                  'sch','skh','sph','d','s','y','k','t','l','r','p','f','o','e','a','n','m']

def get_onset(word):
    for o in ONSET_PRIORITY:
        if word.startswith(o):
            return o
    return word[0] if word else 'other'

# ── section definitions ────────────────────────────────────────────────────────
def build_sections(folio_lines):
    sections = {}
    # A herbal_a: A-dialect folios 1-56 (exp_511/519 methodology)
    a_ha = {n: ls for n, ls in folio_lines.items()
            if n <= 56 and not is_b_dialect(ls)}
    sections['A herbal_a'] = a_ha

    # A stars: A-dialect folios 57-72 (exp_501 methodology)
    a_st = {n: ls for n, ls in folio_lines.items()
            if 57 <= n <= 72 and not is_b_dialect(ls)}
    sections['A stars'] = a_st

    # A cosmo: A-dialect folios 85-102 (exp_518/519 methodology)
    a_co = {n: ls for n, ls in folio_lines.items()
            if 85 <= n <= 102 and not is_b_dialect(ls)}
    sections['A cosmo'] = a_co

    # B herbal: B-dialect folios 1-72 (exp_515 methodology)
    b_he = {n: ls for n, ls in folio_lines.items()
            if n <= 72 and is_b_dialect(ls)}
    sections['B herbal'] = b_he

    # B astro: B-dialect folios 73-84 (exp_516 methodology)
    b_as = {n: ls for n, ls in folio_lines.items()
            if 73 <= n <= 84 and is_b_dialect(ls)}
    sections['B astro'] = b_as

    # B pharma: B-dialect folios 103-116 (main B pharma content from folio survey)
    b_ph = {n: ls for n, ls in folio_lines.items()
            if 103 <= n <= 116 and is_b_dialect(ls)}
    sections['B pharma'] = b_ph

    # B cosmo: B-dialect folios 85-102 (smaller B cosmo section)
    b_co = {n: ls for n, ls in folio_lines.items()
            if 85 <= n <= 102 and is_b_dialect(ls)}
    sections['B cosmo'] = b_co

    return sections

def get_all_lines(section_dict):
    """Get all lines from section, tagged with LF onset."""
    lines = []
    for n, folio_lines_list in sorted(section_dict.items()):
        for ln in folio_lines_list:
            lines.append(ln)
    return lines

def compute_pos1_y_enrichment(lines, lf_class, min_len=3):
    """
    For lines where LF onset == lf_class and len >= min_len:
    compute E for pos1=y using section-wide pos1 baseline.
    """
    # Section-wide pos1 baseline (all lines len>=2)
    pos1_total = 0
    pos1_y_count = 0
    for ln in lines:
        if len(ln) >= 2:
            pos1 = get_onset(ln[0])
            pos1_total += 1
            if pos1 == 'y':
                pos1_y_count += 1

    if pos1_total == 0:
        return None, None, None, None, None

    base_y_pos1 = pos1_y_count / pos1_total

    # LF-class eligible lines
    elig = [ln for ln in lines if len(ln) >= min_len and get_onset(ln[-1]) == lf_class]
    N = len(elig)
    if N == 0:
        return None, None, None, None, base_y_pos1

    obs = sum(1 for ln in elig if get_onset(ln[0]) == 'y')
    exp = base_y_pos1 * N
    E = obs / exp if exp > 0 else 0.0
    return obs, N, exp, E, base_y_pos1

def pos1_full_dist(lines, lf_class, min_len=3):
    """Get full pos1 distribution for lf_class lines."""
    elig = [ln for ln in lines if len(ln) >= min_len and get_onset(ln[-1]) == lf_class]
    dist = defaultdict(int)
    for ln in elig:
        dist[get_onset(ln[0])] += 1
    return dist, len(elig)

def compute_pos2_enrichment(lines, lf_class, pos2_class, min_len=3):
    """E for pos2=pos2_class in lf_class lines."""
    pos2_total = 0
    pos2_target = 0
    for ln in lines:
        if len(ln) >= 3:
            onset = get_onset(ln[1])
            pos2_total += 1
            if onset == pos2_class:
                pos2_target += 1
    if pos2_total == 0:
        return None, None, None, None, None
    base = pos2_target / pos2_total

    elig = [ln for ln in lines if len(ln) >= min_len and get_onset(ln[-1]) == lf_class]
    N = len(elig)
    if N == 0:
        return None, None, None, None, base
    obs = sum(1 for ln in elig if get_onset(ln[1]) == pos2_class)
    exp = base * N
    E = obs / exp if exp > 0 else 0.0
    return obs, N, exp, E, base

def compute_pen_enrichment(lines, lf_class, pen_class, min_len=3):
    """E for pen=pen_class in lf_class lines."""
    pen_total = 0
    pen_target = 0
    for ln in lines:
        if len(ln) >= 3:
            onset = get_onset(ln[-2])
            pen_total += 1
            if onset == pen_class:
                pen_target += 1
    if pen_total == 0:
        return None, None, None, None, None
    base = pen_target / pen_total

    elig = [ln for ln in lines if len(ln) >= min_len and get_onset(ln[-1]) == lf_class]
    N = len(elig)
    if N == 0:
        return None, None, None, None, base
    obs = sum(1 for ln in elig if get_onset(ln[-2]) == pen_class)
    exp = base * N
    E = obs / exp if exp > 0 else 0.0
    return obs, N, exp, E, base

# ── main ──────────────────────────────────────────────────────────────────────
CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

folio_lines = parse_corpus(CORPUS)
sections = build_sections(folio_lines)

# Print section sizes for verification
print("=== SECTION SIZES ===")
for name, sec in sections.items():
    all_lines = get_all_lines(sec)
    n_words = sum(len(ln) for ln in all_lines)
    print(f"  {name}: {len(sec)} folios, {len(all_lines)} lines, {n_words} words")

print()

# ── H_new_EB: o-LF pos1=y across ALL sections ─────────────────────────────────
print("=== H_new_EB: o-LF pos1=y CROSS-SECTION SURVEY ===")
print(f"{'Section':<15} {'N_elig':>7} {'obs':>5} {'exp':>6} {'E':>6} {'base_y':>7} {'flag'}")
print("-" * 60)

for sec_name, sec_dict in sections.items():
    all_lines = get_all_lines(sec_dict)
    obs, N, exp, E, base = compute_pos1_y_enrichment(all_lines, 'o')
    if N is None or N == 0:
        print(f"  {sec_name:<13} {'---':>7}")
        continue
    flag = ''
    if E and N:
        if E >= 1.5 and N >= 10:
            flag = 'CONF'
        elif E >= 2.0 and N >= 5:
            flag = 'dir'
        elif E >= 2.5 and N >= 3:
            flag = '(dir)'
        elif E >= 2.0:
            flag = 'elevated'
    print(f"  {sec_name:<13} {N:>7} {obs:>5} {exp:>6.2f} {E:>6.2f}x {base:>7.3f} {flag}")

print()

# ── H_new_EC: ol-LF pos1=y cross-section ─────────────────────────────────────
print("=== H_new_EC: ol-LF pos1=y CROSS-SECTION SURVEY ===")
print(f"{'Section':<15} {'N_elig':>7} {'obs':>5} {'exp':>6} {'E':>6} {'flag'}")
print("-" * 55)

for sec_name, sec_dict in sections.items():
    all_lines = get_all_lines(sec_dict)
    obs, N, exp, E, base = compute_pos1_y_enrichment(all_lines, 'ol')
    if N is None or N == 0:
        print(f"  {sec_name:<13} {'---':>7}")
        continue
    flag = ''
    if E and N:
        if E >= 1.5 and N >= 10:
            flag = 'CONF'
        elif E >= 2.0 and N >= 5:
            flag = 'dir'
        elif E >= 2.5 and N >= 3:
            flag = '(dir)'
    print(f"  {sec_name:<13} {N:>7} {obs:>5} {exp:>6.2f} {E:>6.2f}x {flag}")

print()

# ── H_new_ED: t-LF positional profile in A stars ─────────────────────────────
print("=== H_new_ED: t-LF POSITIONAL PROFILE IN A STARS ===")
a_stars_lines = get_all_lines(sections['A stars'])

print("\n--- t-LF pos1 full distribution (A stars) ---")
dist, N_elig = pos1_full_dist(a_stars_lines, 't')
print(f"N_elig (t-LF, len>=3): {N_elig}")
# Also compute baseline
pos1_total = sum(1 for ln in a_stars_lines if len(ln) >= 2)
print(f"Section lines (len>=2): {pos1_total}")
# Compute pos1 baseline
pos1_base = defaultdict(int)
for ln in a_stars_lines:
    if len(ln) >= 2:
        pos1_base[get_onset(ln[0])] += 1

print("\npos1 class | obs | base_rate | E")
for cls in ['y','d','ch','sh','ok','ot','qok','o','k','t']:
    obs = dist.get(cls, 0)
    base_count = pos1_base.get(cls, 0)
    base_rate = base_count / pos1_total if pos1_total > 0 else 0
    exp = base_rate * N_elig
    E = obs / exp if exp > 0 else 0.0
    flag = ''
    if N_elig > 0:
        if E >= 1.5 and obs >= 10:
            flag = 'CONF'
        elif E >= 2.0 and obs >= 5:
            flag = 'dir'
        elif E >= 2.5 and obs >= 3:
            flag = '(dir)'
    print(f"  {cls:<8} {obs:>4} {base_rate:>9.3f} {E:>6.2f}x {flag}")

# t-LF pos2 in A stars
print("\n--- t-LF pos2 distribution (A stars) ---")
pos2_total = sum(1 for ln in a_stars_lines if len(ln) >= 3)
pos2_base = defaultdict(int)
for ln in a_stars_lines:
    if len(ln) >= 3:
        pos2_base[get_onset(ln[1])] += 1

elig_t = [ln for ln in a_stars_lines if len(ln) >= 3 and get_onset(ln[-1]) == 't']
print(f"N_elig (t-LF, len>=3, A stars): {len(elig_t)}")

pos2_dist = defaultdict(int)
for ln in elig_t:
    pos2_dist[get_onset(ln[1])] += 1

print("pos2 class | obs | base_rate | E")
for cls in ['ch','y','ok','ot','d','sh','qok','k','t']:
    obs_p = pos2_dist.get(cls, 0)
    base_count = pos2_base.get(cls, 0)
    base_rate = base_count / pos2_total if pos2_total > 0 else 0
    exp = base_rate * len(elig_t)
    E = obs_p / exp if exp > 0 else 0.0
    flag = ''
    if len(elig_t) > 0:
        if E >= 1.5 and obs_p >= 10:
            flag = 'CONF'
        elif E >= 2.0 and obs_p >= 5:
            flag = 'dir'
        elif E >= 2.5 and obs_p >= 3:
            flag = '(dir)'
    print(f"  {cls:<8} {obs_p:>4} {base_rate:>9.3f} {E:>6.2f}x {flag}")

# t-LF pen in A stars
print("\n--- t-LF pen distribution (A stars) ---")
pen_total = sum(1 for ln in a_stars_lines if len(ln) >= 3)
pen_base = defaultdict(int)
for ln in a_stars_lines:
    if len(ln) >= 3:
        pen_base[get_onset(ln[-2])] += 1

pen_dist = defaultdict(int)
for ln in elig_t:
    pen_dist[get_onset(ln[-2])] += 1

print("pen class  | obs | base_rate | E")
for cls in ['ch','y','ok','ot','d','sh','qok','k','t','cth']:
    obs_p = pen_dist.get(cls, 0)
    base_count = pen_base.get(cls, 0)
    base_rate = base_count / pen_total if pen_total > 0 else 0
    exp = base_rate * len(elig_t)
    E = obs_p / exp if exp > 0 else 0.0
    flag = ''
    if len(elig_t) > 0:
        if E >= 1.5 and obs_p >= 10:
            flag = 'CONF'
        elif E >= 2.0 and obs_p >= 5:
            flag = 'dir'
        elif E >= 2.5 and obs_p >= 3:
            flag = '(dir)'
    print(f"  {cls:<8} {obs_p:>4} {base_rate:>9.3f} {E:>6.2f}x {flag}")

# ── H_new_EE: ot-LF pos2=y scope extension ────────────────────────────────────
print("\n=== H_new_EE: ot-LF pos2=y CROSS-SECTION SURVEY ===")
print(f"{'Section':<15} {'N_elig':>7} {'obs':>5} {'exp':>6} {'E':>6} {'flag'}")
print("-" * 55)

for sec_name, sec_dict in sections.items():
    all_lines = get_all_lines(sec_dict)
    obs, N, exp, E, base = compute_pos2_enrichment(all_lines, 'ot', 'y')
    if N is None or N == 0:
        print(f"  {sec_name:<13} {'---':>7}")
        continue
    flag = ''
    if E and N:
        if E >= 1.5 and N >= 10:
            flag = 'CONF'
        elif E >= 2.0 and N >= 5:
            flag = 'dir'
        elif E >= 2.5 and N >= 3:
            flag = '(dir)'
    print(f"  {sec_name:<13} {N:>7} {obs:>5} {exp:>6.2f} {E:>6.2f}x {flag}")

# ── A herbal_a ot-LF pos2=y exact recount ────────────────────────────────────
print("\n--- A herbal_a ot-LF pos2=y detailed check ---")
a_ha_lines = get_all_lines(sections['A herbal_a'])
ot_elig = [ln for ln in a_ha_lines if len(ln) >= 3 and get_onset(ln[-1]) == 'ot']
print(f"A herbal_a ot-LF N_elig (len>=3): {len(ot_elig)}")
pos2_y_lines = [ln for ln in ot_elig if get_onset(ln[1]) == 'y']
print(f"  pos2=y count: {len(pos2_y_lines)}")
print(f"  pos2=y lines:")
for ln in pos2_y_lines:
    print(f"    {ln}")

# Full pos2 dist for ot-LF A herbal_a
pos2_total_ha = sum(1 for ln in a_ha_lines if len(ln) >= 3)
pos2_base_ha = defaultdict(int)
for ln in a_ha_lines:
    if len(ln) >= 3:
        pos2_base_ha[get_onset(ln[1])] += 1

pos2_ot_dist = defaultdict(int)
for ln in ot_elig:
    pos2_ot_dist[get_onset(ln[1])] += 1

print("\nA herbal_a ot-LF pos2 distribution:")
print(f"{'pos2':<8} {'obs':>5} {'base_rate':>10} {'E':>7}")
for cls in sorted(pos2_ot_dist, key=lambda x: -pos2_ot_dist[x])[:8]:
    obs_p = pos2_ot_dist[cls]
    base_rate = pos2_base_ha[cls] / pos2_total_ha if pos2_total_ha > 0 else 0
    exp = base_rate * len(ot_elig)
    E = obs_p / exp if exp > 0 else 0.0
    print(f"  {cls:<6} {obs_p:>5} {base_rate:>10.3f} {E:>7.2f}x")

# ── Additional: ok-LF pos1=y scope in A herbal_b ─────────────────────────────
print("\n=== BONUS: ok-LF pos1=y cross-section (confirm A herbal_b depletion) ===")
print(f"{'Section':<15} {'N_elig':>7} {'obs':>5} {'exp':>6} {'E':>6} {'flag'}")
print("-" * 55)

for sec_name, sec_dict in [('A herbal_a', sections['A herbal_a']),
                            ('A stars', sections['A stars']),
                            ('A cosmo', sections['A cosmo'])]:
    all_lines = get_all_lines(sec_dict)
    obs, N, exp, E, base = compute_pos1_y_enrichment(all_lines, 'ok')
    if N is None or N == 0:
        print(f"  {sec_name:<13} {'---':>7}")
        continue
    flag = ''
    if E and N:
        if E >= 1.5 and N >= 10:
            flag = 'CONF'
        elif E >= 2.0 and N >= 5:
            flag = 'dir'
        elif E >= 2.5 and N >= 3:
            flag = '(dir)'
        elif E < 0.7:
            flag = 'DEPLETED'
    print(f"  {sec_name:<13} {N:>7} {obs:>5} {exp:>6.2f} {E:>6.2f}x {flag}")

print("\nDone.")
