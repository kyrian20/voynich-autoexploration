"""
exp_465: A-dialect cth→sh CL section-specificity and body-conditional breakdown (H_new_AC)
Q: Is the A cth→sh CL (E=1.9×/N=12) section-specific? Which body class drives it?
Also: A stars section paragraph structure (H_new_AD component — short paragraphs?)
"""
import re
from collections import defaultdict, Counter

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on): return on
    return 'other'

def get_first_body_char(word, onset):
    body = word[len(onset):]
    if not body: return '_'
    return body[0]

def get_section_a(folio):
    num = ''
    for c in folio:
        if c.isdigit(): num += c
        elif num: break
    if not num: return 'other'
    n = int(num)
    if n <= 56: return 'herbal_a'
    elif n <= 72: return 'stars'
    elif n <= 84: return 'herbal_b'
    elif n <= 102: return 'cosmo'
    else: return 'other_a'

def parse_corpus():
    pattern = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    folios = defaultdict(list)
    with open(ZL3B, encoding='utf-8') as f:
        for line in f:
            for m in pattern.finditer(line):
                folio = m.group(1).lstrip('+*=&~')
                lc = m.group(3).lstrip('+*=/~&')
                if not lc.lstrip('@').startswith('P'): continue
                text = m.group(4).strip()
                words = [w for w in re.split(r'[-.\s]', text)
                         if re.match(r'^[a-z]+$', w) and len(w) >= 2]
                if words: folios[folio].append(words)
    return folios

def classify_dialects(folios):
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for ws in lines)
        if total == 0: continue
        edy = sum(1 for ws in lines for w in ws if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

folios = parse_corpus()
dialect_map = classify_dialects(folios)

# Part 1: cth→sh CL section specificity and body-conditional breakdown
print("=== Part 1: A cth→sh CL section specificity ===\n")

section_cl = defaultdict(lambda: defaultdict(Counter))
section_ll_total = defaultdict(Counter)
section_lf_total = defaultdict(Counter)
section_total_cl = Counter()

# Also track body-conditional
cth_body_cl = defaultdict(Counter)  # body_char -> lf_onset
cth_body_total = Counter()  # body_char -> total
cth_sh_cases = []  # (folio, sec, ll_word, lf_word)

for folio, lines in folios.items():
    if dialect_map.get(folio) != 'A': continue
    sec = get_section_a(folio)
    n = len(lines)
    if n < 3: continue
    cont = lines[1:-1]
    for ci in range(len(cont)-1):
        ll = cont[ci][-1]; lf = cont[ci+1][0]
        ll_on = get_onset(ll); lf_on = get_onset(lf)
        if ll_on == 'other' or lf_on == 'other': continue

        section_cl[sec][ll_on][lf_on] += 1
        section_ll_total[sec][ll_on] += 1
        section_lf_total[sec][lf_on] += 1
        section_total_cl[sec] += 1

        if ll_on == 'cth':
            bc = get_first_body_char(ll, 'cth')
            cth_body_cl[bc][lf_on] += 1
            cth_body_total[bc] += 1
            if lf_on == 'sh':
                cth_sh_cases.append((folio, sec, ll, lf))

# Section breakdown for cth→sh
sections = ['herbal_a', 'stars', 'cosmo', 'herbal_b']
print(f"{'pair':>12} ", end='')
for sec in sections:
    print(f"  {sec:<20}", end='')
print("  overall")
for sec in sections:
    print(f"  N={section_total_cl[sec]:<8}", end='')
print()

# cth→sh
total_obs = 0; total_ll = 0; total_lf = 0; total_all_cl = sum(section_total_cl.values())
total_lf_count = sum(section_lf_total[s]['sh'] for s in sections)
print(f"{'cth→sh':>12} ", end='')
for sec in sections:
    n_ll = section_ll_total[sec]['cth']
    obs = section_cl[sec]['cth']['sh']
    lf_n = section_lf_total[sec]['sh']
    cl_n = section_total_cl[sec]
    total_obs += obs; total_ll += n_ll
    if n_ll >= 5 and cl_n > 0:
        base_p = lf_n / cl_n
        exp = n_ll * base_p
        E = obs / exp if exp > 0 else 0
        mk = '↑' if E>=1.4 else ('↓' if E<=0.6 else ' ')
        print(f"  {E:.1f}x{mk}(N={obs})", end='')
    else:
        print(f"  dir(N={obs})", end='')
# Overall
all_lf_sh = sum(section_lf_total[s]['sh'] for s in sections)
all_cl = sum(section_total_cl[s] for s in sections)
base_overall = all_lf_sh / all_cl if all_cl > 0 else 0
exp_overall = total_ll * base_overall
E_overall = total_obs / exp_overall if exp_overall > 0 else 0
print(f"  {E_overall:.2f}x(N={total_obs})")

# Also show other top cth CL targets for context
print("\nA cth at LL → top 5 targets (section-pooled):")
all_cth_lf = Counter()
all_cth_total = 0
for sec in sections:
    for lf, cnt in section_cl[sec]['cth'].items():
        all_cth_lf[lf] += cnt
    all_cth_total += section_ll_total[sec]['cth']
# Base rates
all_lf_total = Counter()
for sec in sections:
    for lf, cnt in section_lf_total[sec].items():
        all_lf_total[lf] += cnt
for lf, obs in all_cth_lf.most_common(8):
    base_p = all_lf_total[lf] / all_cl if all_cl > 0 else 0
    exp = all_cth_total * base_p
    E = obs / exp if exp > 0 else 0
    print(f"  cth→{lf}: obs={obs}, E={E:.2f}x")

# Body-conditional for cth CL
print("\n\nA cth body-class CL breakdown:")
print(f"  {'body':>6}  {'N_ll':>5}  {'→sh':>8}  {'E_sh':>6}  {'top_lf':}")
for bc, n_ll in sorted(cth_body_total.items(), key=lambda x: -x[1]):
    obs_sh = cth_body_cl[bc]['sh']
    # overall sh base rate
    base_p_sh = all_lf_total['sh'] / all_cl if all_cl > 0 else 0
    exp_sh = n_ll * base_p_sh
    E_sh = obs_sh / exp_sh if exp_sh > 0 else 0
    top_lf = [(lf, cth_body_cl[bc][lf]) for lf in sorted(cth_body_cl[bc], key=lambda x: -cth_body_cl[bc][x])][:3]
    top_str = ', '.join(f"{lf}={cnt}" for lf, cnt in top_lf)
    print(f"  {bc:>6}  {n_ll:>5}  {obs_sh:>8}  {E_sh:>6.2f}x  {top_str}")

# Detailed cases
print(f"\ncth→sh CL cases (N={len(cth_sh_cases)}):")
for case in cth_sh_cases:
    print(f"  {case}")

# Part 2: A stars section paragraph structure (H_new_AD component)
print("\n\n=== Part 2: A stars section paragraph structure ===\n")
stars_folio_stats = []
for folio, lines in folios.items():
    if dialect_map.get(folio) != 'A': continue
    sec = get_section_a(folio)
    if sec != 'stars': continue
    n_lines = len(lines)
    n_cont = max(0, n_lines - 2)
    n_words = sum(len(ws) for ws in lines)
    stars_folio_stats.append((folio, n_lines, n_cont, n_words))

stars_folio_stats.sort()
print(f"A stars folios (f57-72): N={len(stars_folio_stats)}")
print(f"{'folio':>8}  {'n_lines':>8}  {'n_cont':>8}  {'n_words':>9}")
for folio, nl, nc, nw in stars_folio_stats:
    print(f"  {folio:>8}  {nl:>8}  {nc:>8}  {nw:>9}")

total_stars_cont = sum(nc for _, _, nc, _ in stars_folio_stats)
total_stars_lines = sum(nl for _, nl, _, _ in stars_folio_stats)
print(f"\nTotal: lines={total_stars_lines}, cont={total_stars_cont}, CL_pairs={max(0,total_stars_cont-len(stars_folio_stats))}")
avg_lines = total_stars_lines / len(stars_folio_stats) if stars_folio_stats else 0
print(f"Mean lines per folio: {avg_lines:.1f}")

# Compare with herbal_a
herbal_folio_stats = []
for folio, lines in folios.items():
    if dialect_map.get(folio) != 'A': continue
    sec = get_section_a(folio)
    if sec != 'herbal_a': continue
    n_lines = len(lines)
    herbal_folio_stats.append(n_lines)
avg_herbal = sum(herbal_folio_stats) / len(herbal_folio_stats) if herbal_folio_stats else 0
print(f"A herbal_a: N={len(herbal_folio_stats)} folios, mean lines={avg_herbal:.1f}")

# Stars within-line formula analysis
# Count stars formula-typed lines (LF-conditional pos1 E≥2)
print("\n\nA stars within-line: LF-class distribution vs herbal_a")
stars_lf = Counter()
herbal_lf = Counter()
for folio, lines in folios.items():
    if dialect_map.get(folio) != 'A': continue
    sec = get_section_a(folio)
    for ws in lines:
        if len(ws) < 2: continue
        lf_on = get_onset(ws[0])
        if lf_on == 'other': continue
        if sec == 'stars': stars_lf[lf_on] += 1
        elif sec == 'herbal_a': herbal_lf[lf_on] += 1

total_stars_lf = sum(stars_lf.values())
total_herbal_lf = sum(herbal_lf.values())
print(f"Stars LF total: {total_stars_lf}; Herbal LF total: {total_herbal_lf}")
print(f"{'onset':>6}  {'stars%':>8}  {'herbal%':>8}  {'ratio':>6}")
top_onsets = [x for x, _ in (herbal_lf + stars_lf).most_common(12)]
for on in top_onsets:
    s_pct = 100*stars_lf[on]/total_stars_lf if total_stars_lf > 0 else 0
    h_pct = 100*herbal_lf[on]/total_herbal_lf if total_herbal_lf > 0 else 0
    ratio = s_pct/h_pct if h_pct > 0 else float('inf')
    print(f"  {on:>6}  {s_pct:>7.1f}%  {h_pct:>7.1f}%  {ratio:>5.2f}x")
