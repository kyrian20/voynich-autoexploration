"""
exp_466: A Stars Section t-LF Grammar (H_new_AF)
Q: Is A stars t-LF elevation (3.3× vs herbal_a) confirmed vs A-dialect overall baseline?
   What t-words dominate? Is there a t→pos2 routing rule (formula-type)?
   Comparison to B astro qok-LF (F431).
"""
import re
from collections import defaultdict, Counter

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on): return on
    return 'other'

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

# Collect A-dialect LF onset distributions by section
section_lf = defaultdict(Counter)
section_lf_words = defaultdict(Counter)  # word-level for stars t-LF
section_pos2 = defaultdict(Counter)  # for t-LF → pos2 analysis
section_total_lines = defaultdict(int)
a_overall_lf = Counter()
a_overall_total = 0

for folio, lines in folios.items():
    if dialect_map.get(folio) != 'A': continue
    sec = get_section_a(folio)
    for ws in lines:
        if not ws: continue
        lf_w = ws[0]
        lf_on = get_onset(lf_w)
        if lf_on == 'other': continue
        section_lf[sec][lf_on] += 1
        section_total_lines[sec] += 1
        a_overall_lf[lf_on] += 1
        a_overall_total += 1
        if sec == 'stars' and lf_on == 't':
            section_lf_words['stars_t'][lf_w] += 1
            if len(ws) >= 2:
                pos2_on = get_onset(ws[1])
                section_pos2['stars_t'][pos2_on] += 1
        if sec == 'herbal_a' and lf_on == 't':
            section_lf_words['herbal_t'][lf_w] += 1

sections_ordered = ['herbal_a', 'stars', 'cosmo', 'herbal_b']

print("=== A-dialect LF-class section distribution ===\n")
print(f"{'onset':>6}", end='')
for sec in sections_ordered:
    print(f"  {sec:>12}", end='')
print("  A_overall")
for sec in sections_ordered:
    print(f"  N={section_total_lines[sec]:>8}", end='')
print(f"  N={a_overall_total:>8}")

top_onsets = [x for x, _ in a_overall_lf.most_common(15)]
for on in top_onsets:
    overall_rate = a_overall_lf[on] / a_overall_total if a_overall_total > 0 else 0
    print(f"  {on:>6}", end='')
    for sec in sections_ordered:
        sec_total = section_total_lines[sec]
        obs = section_lf[sec][on]
        rate = obs / sec_total if sec_total > 0 else 0
        E = rate / overall_rate if overall_rate > 0 else 0
        mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
        print(f"  {E:.2f}x{mk}({obs})", end='')
    print(f"  {overall_rate*100:.1f}%({a_overall_lf[on]})")

# Formal E for stars t-LF
stars_t_obs = section_lf['stars'][t_on := 't']
stars_total = section_total_lines['stars']
overall_t_rate = a_overall_lf['t'] / a_overall_total if a_overall_total > 0 else 0
stars_t_exp = stars_total * overall_t_rate
stars_t_E = stars_t_obs / stars_t_exp if stars_t_exp > 0 else 0
print(f"\nFormal: A stars t-LF: obs={stars_t_obs}, exp={stars_t_exp:.2f}, E={stars_t_E:.2f}× (vs A-overall baseline)")
print(f"  (herbal_a t-LF: obs={section_lf['herbal_a']['t']}, E={section_lf['herbal_a']['t']/(section_total_lines['herbal_a']*overall_t_rate):.2f}×)")
print(f"  (cosmo t-LF: obs={section_lf['cosmo']['t']}, E={section_lf['cosmo']['t']/(section_total_lines['cosmo']*overall_t_rate):.2f}×)")

# Stars qot/ot depletion
print(f"\nA stars qot-LF: obs={section_lf['stars']['qot']}, rate={section_lf['stars']['qot']/stars_total*100:.1f}%, E={section_lf['stars']['qot']/(stars_total*a_overall_lf['qot']/a_overall_total):.2f}×")
print(f"A stars ot-LF: obs={section_lf['stars']['ot']}, rate={section_lf['stars']['ot']/stars_total*100:.1f}%, E={section_lf['stars']['ot']/(stars_total*a_overall_lf['ot']/a_overall_total):.2f}×")

# t-word inventory in stars
print("\n\nA stars t-LF word inventory:")
for word, cnt in section_lf_words['stars_t'].most_common(20):
    print(f"  {word}: {cnt}")
print(f"\nA herbal_a t-LF word inventory:")
for word, cnt in section_lf_words['herbal_t'].most_common(10):
    print(f"  {word}: {cnt}")

# t-LF pos2 routing in stars (formula-type check)
print(f"\n\nA stars t-LF → pos2 routing (N_total={sum(section_pos2['stars_t'].values())}):")
total_pos2 = sum(section_pos2['stars_t'].values())
for on, cnt in sorted(section_pos2['stars_t'].items(), key=lambda x: -x[1]):
    stars_pos2_E = (cnt / total_pos2) / (a_overall_lf[on] / a_overall_total) if total_pos2 > 0 and a_overall_lf[on] > 0 else 0
    print(f"  {on}: {cnt} ({cnt/total_pos2*100:.1f}%), E={stars_pos2_E:.2f}×")

# Comparison to B astro qok-LF (F431)
print("\n\n=== Comparison: A stars t-LF vs B astro qok-LF (F431) ===")
# B astro qok-LF from F431
print("B astro: qok-LF = 19.6% vs A-overall baseline ~5.6% → E=1.91×")
print(f"A stars: t-LF = {stars_t_obs/stars_total*100:.1f}% vs A-overall {overall_t_rate*100:.1f}% → E={stars_t_E:.2f}×")
print(f"  B astro uses qok as section LF marker (E=1.91×, N=all astro lines)")
print(f"  A stars uses t as section LF marker (E={stars_t_E:.2f}×, N={stars_t_obs})")
print(f"  A/B astronomical section LF marker: DIFFERENT onset classes (t vs qok)")

# Also check B astro t-LF for comparison
b_section_lf = defaultdict(Counter)
b_section_total = defaultdict(int)
b_overall_lf = Counter()
b_overall_total = 0
def get_section_b(folio):
    num = ''
    for c in folio:
        if c.isdigit(): num += c
        elif num: break
    if not num: return 'other'
    n = int(num)
    if n <= 72: return 'herbal'
    elif n <= 84: return 'astro'
    elif n <= 102: return 'cosmo'
    elif n <= 116: return 'pharma'
    elif n <= 170: return 'bio'
    else: return 'text'
for folio, lines in folios.items():
    if dialect_map.get(folio) != 'B': continue
    sec = get_section_b(folio)
    for ws in lines:
        if not ws: continue
        lf_on = get_onset(ws[0])
        if lf_on == 'other': continue
        b_section_lf[sec][lf_on] += 1
        b_section_total[sec] += 1
        b_overall_lf[lf_on] += 1
        b_overall_total += 1

b_astro_t_rate = b_section_lf['astro']['t'] / b_section_total['astro'] if b_section_total['astro'] > 0 else 0
b_t_overall_rate = b_overall_lf['t'] / b_overall_total if b_overall_total > 0 else 0
print(f"\nB astro t-LF: obs={b_section_lf['astro']['t']}, rate={b_astro_t_rate*100:.1f}%, E={b_astro_t_rate/b_t_overall_rate:.2f}× (t in B astro)")
b_astro_qok_rate = b_section_lf['astro']['qok'] / b_section_total['astro']
b_qok_overall_rate = b_overall_lf['qok'] / b_overall_total
print(f"B astro qok-LF: obs={b_section_lf['astro']['qok']}, rate={b_astro_qok_rate*100:.1f}%, E={b_astro_qok_rate/b_qok_overall_rate:.2f}× (confirming F431)")
