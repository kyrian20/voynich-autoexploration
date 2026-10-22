"""
exp_522: o-LF pos2/pen grammar (A herbal_a + A stars) + A stars t-LF pos1/pos2 grammar
Hypotheses:
  H_new_EI: o-LF pos2 and pen — full within-line grammar for o-LF (y-opening vs standard subtypes)
  H_new_EJ: A stars t-LF pos1/pos2 routing — what is the positional grammar of A stars' dominant LF class?
  H_new_AH (open): A stars t-LF → pos2=ot (E=4.93×/N=3, dir) — confirm or not?
  H_new_CW (open): B astro F469/F471 — do sh-LF and ol-LF pos2 self-chains survive 2-word-line correction?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words:
        return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

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

folio_lines = parse_corpus(CORPUS)

# Section definitions
a_ha = {n: ls for n, ls in folio_lines.items() if n <= 56 and not is_b_dialect(ls)}
a_st = {n: ls for n, ls in folio_lines.items() if 57 <= n <= 72 and not is_b_dialect(ls)}
b_as = {n: ls for n, ls in folio_lines.items() if 73 <= n <= 84 and is_b_dialect(ls)}

print(f"A herbal_a: {len(a_ha)} folios")
print(f"A stars: {len(a_st)} folios")
print(f"B astro: {len(b_as)} folios")

def all_lines(section):
    return [ln for ls in section.values() for ln in ls]

def flag(obs, E):
    if obs >= 10 and E >= 1.5:
        return 'CONF'
    elif obs >= 5 and E >= 2.0:
        return 'dir'
    elif obs >= 3 and E >= 2.5:
        return '(dir)'
    elif E >= 1.0:
        return f'E={E:.2f}×/N={obs}'
    else:
        return f'DEPLETED E={E:.2f}×/N={obs}'

# ─────────────────────────────────────────────────────────
# PART 1: o-LF pos2 and pen grammar (H_new_EI)
# A herbal_a and A stars
# ─────────────────────────────────────────────────────────

def compute_positional_profile(lines_section, lf_class, min_len_pos2=3, min_len_pen=3):
    """
    For lines where LF onset == lf_class:
    - pos1 distribution (len >= 2)
    - pos2 distribution (len >= 3)
    - pen distribution (len >= 3, pen = words[-2])
    Returns: (pos1_counts, pos1_N, pos2_counts, pos2_N, pen_counts, pen_N)
    """
    pos1_counts = defaultdict(int)
    pos2_counts = defaultdict(int)
    pen_counts = defaultdict(int)
    pos1_N = 0
    pos2_N = 0
    pen_N = 0

    for ln in lines_section:
        if len(ln) < 2:
            continue
        lf = get_onset(ln[-1])
        if lf != lf_class:
            continue
        pos1 = get_onset(ln[0])
        pos1_counts[pos1] += 1
        pos1_N += 1
        if len(ln) >= 3:
            pos2 = get_onset(ln[1])
            pos2_counts[pos2] += 1
            pos2_N += 1
            pen = get_onset(ln[-2])
            pen_counts[pen] += 1
            pen_N += 1
    return pos1_counts, pos1_N, pos2_counts, pos2_N, pen_counts, pen_N

def compute_section_baselines(lines_section):
    """Compute pos1, pos2, pen baselines for a section."""
    pos1_b = defaultdict(int); pos1_N = 0
    pos2_b = defaultdict(int); pos2_N = 0
    pen_b = defaultdict(int); pen_N = 0
    for ln in lines_section:
        if len(ln) >= 2:
            pos1_b[get_onset(ln[0])] += 1
            pos1_N += 1
        if len(ln) >= 3:
            pos2_b[get_onset(ln[1])] += 1
            pos2_N += 1
            pen_b[get_onset(ln[-2])] += 1
            pen_N += 1
    return pos1_b, pos1_N, pos2_b, pos2_N, pen_b, pen_N

def report_positional_grammar(section_name, section_dict, lf_class, top_n=6):
    lines = all_lines(section_dict)
    p1_b, p1_N, p2_b, p2_N, pen_b, pen_N = compute_section_baselines(lines)
    p1_c, p1_lf_N, p2_c, p2_lf_N, pen_c, pen_lf_N = compute_positional_profile(lines, lf_class)

    print(f"\n=== {section_name} {lf_class}-LF (N_elig pos1={p1_lf_N}, pos2={p2_lf_N}) ===")

    for pos_name, counts, lf_count, base_counts, base_N in [
        ('pos1', p1_c, p1_lf_N, p1_b, p1_N),
        ('pos2', p2_c, p2_lf_N, p2_b, p2_N),
        ('pen', pen_c, pen_lf_N, pen_b, pen_N),
    ]:
        if lf_count == 0:
            print(f"  {pos_name}: N=0")
            continue
        results = []
        for onset, obs in sorted(counts.items(), key=lambda x: -x[1]):
            base_rate = base_counts.get(onset, 0) / base_N if base_N > 0 else 0
            exp_val = base_rate * lf_count
            E = obs / exp_val if exp_val > 0 else 0
            results.append((onset, obs, exp_val, E))
        results.sort(key=lambda x: -x[3])
        print(f"  {pos_name} (N={lf_count}):")
        for onset, obs, exp_val, E in results[:top_n]:
            f = flag(obs, E)
            print(f"    {onset}: obs={obs}, exp={exp_val:.1f}, E={E:.2f}× [{f}]")


# Report o-LF pos1/pos2/pen for A herbal_a and A stars
report_positional_grammar("A herbal_a", a_ha, 'o')
report_positional_grammar("A stars", a_st, 'o')

# ─────────────────────────────────────────────────────────
# PART 2: y-opening subtype analysis for o-LF (H_new_EI extension)
# Compare pen grammar between y-opening vs standard o-LF lines
# ─────────────────────────────────────────────────────────

def y_opening_subtype_pen(section_name, section_dict, lf_class):
    lines = all_lines(section_dict)
    _, _, _, _, pen_b, pen_N = compute_section_baselines(lines)

    y_open_pen = defaultdict(int)
    std_pen = defaultdict(int)
    y_open_N = 0
    std_N = 0

    for ln in lines:
        if len(ln) < 3:
            continue
        if get_onset(ln[-1]) != lf_class:
            continue
        is_y_open = (get_onset(ln[0]) == 'y')
        pen_onset = get_onset(ln[-2])
        if is_y_open:
            y_open_pen[pen_onset] += 1
            y_open_N += 1
        else:
            std_pen[pen_onset] += 1
            std_N += 1

    print(f"\n=== {section_name} {lf_class}-LF y-opening vs standard pen grammar ===")
    print(f"y-opening lines (pos1=y): N={y_open_N}")
    print(f"standard lines (pos1≠y): N={std_N}")

    for subtype_name, counts, sub_N in [('y-opening', y_open_pen, y_open_N), ('standard', std_pen, std_N)]:
        if sub_N == 0:
            continue
        results = []
        for onset, obs in sorted(counts.items(), key=lambda x: -x[1]):
            base_rate = pen_b.get(onset, 0) / pen_N if pen_N > 0 else 0
            exp_val = base_rate * sub_N
            E = obs / exp_val if exp_val > 0 else 0
            results.append((onset, obs, exp_val, E))
        results.sort(key=lambda x: -x[3])
        print(f"  {subtype_name}:")
        for onset, obs, exp_val, E in results[:5]:
            f = flag(obs, E)
            print(f"    {onset}: obs={obs}, exp={exp_val:.1f}, E={E:.2f}× [{f}]")


y_opening_subtype_pen("A herbal_a", a_ha, 'o')
y_opening_subtype_pen("A stars", a_st, 'o')

# ─────────────────────────────────────────────────────────
# PART 3: A stars t-LF pos1/pos2 grammar (H_new_EJ + H_new_AH)
# ─────────────────────────────────────────────────────────

report_positional_grammar("A stars", a_st, 't')

# Also report full A stars LF class profile at pos1 for comparison
print("\n=== A stars full LF pos1 survey (all classes with N>=3) ===")
lines_ast = all_lines(a_st)
p1_b_ast, p1_N_ast, _, _, _, _ = compute_section_baselines(lines_ast)

# Get LF class distribution
lf_counts_ast = defaultdict(int)
for ln in lines_ast:
    if len(ln) >= 2:
        lf_counts_ast[get_onset(ln[-1])] += 1

for lf_cls, lf_cnt in sorted(lf_counts_ast.items(), key=lambda x: -x[1]):
    if lf_cnt < 3:
        continue
    # compute pos1=y enrichment specifically
    obs_y = 0
    N_elig = 0
    for ln in lines_ast:
        if len(ln) < 2:
            continue
        if get_onset(ln[-1]) != lf_cls:
            continue
        N_elig += 1
        if get_onset(ln[0]) == 'y':
            obs_y += 1
    base_y = p1_b_ast.get('y', 0) / p1_N_ast if p1_N_ast > 0 else 0
    exp_y = base_y * N_elig
    E_y = obs_y / exp_y if exp_y > 0 else 0
    f_y = flag(obs_y, E_y)
    print(f"  {lf_cls}-LF (N={lf_cnt}): y@pos1 obs={obs_y}/N_elig={N_elig}, E={E_y:.2f}× [{f_y}]")

# ─────────────────────────────────────────────────────────
# PART 4: H_new_CW — B astro F469/F471 2-word-line artifact check
# F469: sh-LF → sh@pos2 (E=1.59×/N=10, claimed CONF from exp_490)
# F471: ol-LF → ol@pos2 (E=1.54×/N=15, claimed CONF from exp_490)
# Test with len>=3 filter to check if 2-word lines inflate the count
# ─────────────────────────────────────────────────────────

print("\n=== H_new_CW: B astro F469/F471 2-word-line artifact check ===")

lines_bas = all_lines(b_as)
_, _, p2_b_bas, p2_N_bas, _, _ = compute_section_baselines(lines_bas)

for lf_class in ['sh', 'ol']:
    print(f"\nB astro {lf_class}-LF pos2=self:")
    for min_len, label in [(2, 'len>=2 (original)'), (3, 'len>=3 (corrected)')]:
        obs = 0
        N_elig = 0
        for ln in lines_bas:
            if len(ln) < min_len:
                continue
            if get_onset(ln[-1]) != lf_class:
                continue
            N_elig += 1
            if len(ln) >= 3 and get_onset(ln[1]) == lf_class:
                obs += 1
        base_rate = p2_b_bas.get(lf_class, 0) / p2_N_bas if p2_N_bas > 0 else 0
        exp_val = base_rate * N_elig
        E = obs / exp_val if exp_val > 0 else 0
        f = flag(obs, E)
        print(f"  {label}: N_elig={N_elig}, obs={obs}, exp={exp_val:.1f}, E={E:.2f}× [{f}]")

# ─────────────────────────────────────────────────────────
# PART 5: o-LF cross-line coupling — what does a line with o at LL predict for next LF?
# This is complementary to F502 (within-line y@pos1 for o-LF)
# ─────────────────────────────────────────────────────────

print("\n=== o-LF cross-line coupling (A herbal_a, within-folio pairs) ===")

lines_aha = all_lines(a_ha)

# Compute CL baseline for A herbal_a
lf_base = defaultdict(int)
lf_base_N = 0
for ln in lines_aha:
    if len(ln) >= 1:
        lf_base[get_onset(ln[-1])] += 1
        lf_base_N += 1

# Compute next_LF baseline
next_lf_base = defaultdict(int)
next_lf_N = 0
for folnum, fol_lines in a_ha.items():
    for i in range(len(fol_lines) - 1):
        ln_next = fol_lines[i + 1]
        if len(ln_next) >= 1:
            next_lf_base[get_onset(ln_next[-1])] += 1
            next_lf_N += 1

# For o-LL → next LF pairs
o_ll_to_lf = defaultdict(int)
o_ll_N = 0
for folnum, fol_lines in a_ha.items():
    for i in range(len(fol_lines) - 1):
        ln_curr = fol_lines[i]
        ln_next = fol_lines[i + 1]
        if len(ln_curr) >= 1 and get_onset(ln_curr[-1]) == 'o':
            if len(ln_next) >= 1:
                o_ll_to_lf[get_onset(ln_next[-1])] += 1
                o_ll_N += 1

print(f"A herbal_a o-LL lines → next LF: N_pairs={o_ll_N}")
next_lf_total = sum(next_lf_base.values())
results_cl = []
for onset, obs in sorted(o_ll_to_lf.items(), key=lambda x: -x[1]):
    base_rate = next_lf_base.get(onset, 0) / next_lf_total if next_lf_total > 0 else 0
    exp_val = base_rate * o_ll_N
    E = obs / exp_val if exp_val > 0 else 0
    results_cl.append((onset, obs, exp_val, E))
results_cl.sort(key=lambda x: -x[3])
for onset, obs, exp_val, E in results_cl[:8]:
    f = flag(obs, E)
    print(f"  o-LL → next LF={onset}: obs={obs}, exp={exp_val:.1f}, E={E:.2f}× [{f}]")

# Also: preceding LL → o-LF (what comes before o-LF lines?)
print(f"\nA herbal_a prev LL → o-LF:")
prev_ll_N = 0
prev_ll_counts = defaultdict(int)
for folnum, fol_lines in a_ha.items():
    for i in range(1, len(fol_lines)):
        ln_curr = fol_lines[i]
        ln_prev = fol_lines[i - 1]
        if len(ln_curr) >= 1 and get_onset(ln_curr[-1]) == 'o':
            if len(ln_prev) >= 1:
                prev_ll_counts[get_onset(ln_prev[-1])] += 1
                prev_ll_N += 1

print(f"  (N_pairs={prev_ll_N})")
prev_total = sum(lf_base.values())
results_prev = []
for onset, obs in sorted(prev_ll_counts.items(), key=lambda x: -x[1]):
    base_rate = lf_base.get(onset, 0) / prev_total if prev_total > 0 else 0
    exp_val = base_rate * prev_ll_N
    E = obs / exp_val if exp_val > 0 else 0
    results_prev.append((onset, obs, exp_val, E))
results_prev.sort(key=lambda x: -x[3])
for onset, obs, exp_val, E in results_prev[:6]:
    f = flag(obs, E)
    print(f"  prev LL={onset} → o-LF: obs={obs}, exp={exp_val:.1f}, E={E:.2f}× [{f}]")

print("\n[exp_522 done]")
