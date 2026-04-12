"""
exp_467: B-Dialect Full Section LF-Class Grammar (H_new_AG)
Q: Do B herbal/pharma/cosmo sections have section-specific LF onset markers,
   parallel to B astro qok-LF (F431) and A stars t-LF (F446)?
"""
import re
from collections import defaultdict, Counter

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on): return on
    return 'other'

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

# B section LF grammar
section_lf = defaultdict(Counter)
section_total = defaultdict(int)
section_lf_words = defaultdict(Counter)  # for t-LF word inventory
section_pos2 = defaultdict(Counter)  # for t-LF → pos2
b_overall_lf = Counter()
b_overall_total = 0

for folio, lines in folios.items():
    if dialect_map.get(folio) != 'B': continue
    sec = get_section_b(folio)
    for ws in lines:
        if not ws: continue
        on = get_onset(ws[0])
        if on == 'other': continue
        section_lf[sec][on] += 1
        section_total[sec] += 1
        b_overall_lf[on] += 1
        b_overall_total += 1
        # Track t-LF word inventory and pos2 routing by section
        if on == 't':
            section_lf_words[sec + '_t'][ws[0]] += 1
            if len(ws) >= 2:
                p2_on = get_onset(ws[1])
                section_pos2[sec + '_t'][p2_on] += 1

sections = ['herbal', 'astro', 'pharma', 'cosmo']
print(f"B-dialect section LF-class grammar (exp_467)")
print(f"B-overall N={b_overall_total}")
print(f"  Section counts: " + ", ".join(f"{s}={section_total[s]}" for s in sections))
print()

top_onsets = [x for x, _ in b_overall_lf.most_common(16)]
print(f"{'onset':>6}", end='')
for sec in sections:
    print(f"  {sec:>12}", end='')
print("  B_overall")
print(f"{'':>6}", end='')
for sec in sections:
    print(f"  N={section_total[sec]:>9}", end='')
print()

for on in top_onsets:
    overall_rate = b_overall_lf[on] / b_overall_total if b_overall_total > 0 else 0
    print(f"  {on:>6}", end='')
    for sec in sections:
        sec_n = section_total[sec]
        obs = section_lf[sec][on]
        rate = obs / sec_n if sec_n > 0 else 0
        E = rate / overall_rate if overall_rate > 0 else 0
        mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
        print(f"  {E:.2f}x{mk}({obs})", end='')
    print(f"  {overall_rate*100:.1f}%({b_overall_lf[on]})")

# Formal E for key section LF markers
print("\n\n=== Key section LF markers (formal E vs B-overall) ===")
markers = [
    ('astro', 'qok'), ('astro', 'qot'), ('astro', 'qo'),
    ('herbal', 't'), ('herbal', 'y'), ('herbal', 'ot'),
    ('pharma', 'ok'), ('pharma', 'o'), ('pharma', 'y'),
    ('cosmo', 't'), ('cosmo', 'p'),
]
for sec, on in markers:
    obs = section_lf[sec][on]
    sec_n = section_total[sec]
    overall_rate = b_overall_lf[on] / b_overall_total if b_overall_total > 0 else 0
    exp = sec_n * overall_rate
    E = obs / exp if exp > 0 else 0
    mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
    print(f"  B {sec} {on}-LF: obs={obs}, exp={exp:.1f}, E={E:.2f}x{mk}")

# t-LF word inventory by section
print("\n\n=== B t-LF word inventory by section ===")
for sec in ['herbal', 'cosmo', 'astro', 'pharma']:
    words = section_lf_words[sec + '_t'].most_common(10)
    n_t = section_lf[sec]['t']
    print(f"B {sec} t-LF (N={n_t}): " + ", ".join(f"{w}({c})" for w, c in words[:8]))

# t-LF → pos2 routing
print("\n\n=== B herbal t-LF → pos2 routing ===")
total_herbal_pos2 = sum(section_pos2['herbal_t'].values())
for on, cnt in sorted(section_pos2['herbal_t'].items(), key=lambda x: -x[1])[:8]:
    E = (cnt / total_herbal_pos2) / (b_overall_lf[on] / b_overall_total) if total_herbal_pos2 > 0 and b_overall_lf[on] > 0 else 0
    print(f"  t→{on}: {cnt} ({cnt/total_herbal_pos2*100:.1f}%), E={E:.2f}×")

# LL grammar by section (what comes at LL in each section)
print("\n\n=== B section LL-class grammar (for comparison with LF) ===")
section_ll = defaultdict(Counter)
section_ll_total = defaultdict(int)

for folio, lines in folios.items():
    if dialect_map.get(folio) != 'B': continue
    sec = get_section_b(folio)
    for ws in lines:
        if not ws: continue
        on = get_onset(ws[-1])
        if on == 'other': continue
        section_ll[sec][on] += 1
        section_ll_total[sec] += 1

b_overall_ll = Counter()
b_overall_ll_total = 0
for sec in sections:
    for on, cnt in section_ll[sec].items():
        b_overall_ll[on] += cnt
        b_overall_ll_total += cnt

print(f"{'onset':>6}", end='')
for sec in sections:
    print(f"  {sec:>12}", end='')
print("  B_overall")
for sec in sections:
    print(f"  N={section_ll_total[sec]:>9}", end='')
print()

for on in top_onsets[:12]:
    overall_rate = b_overall_ll[on] / b_overall_ll_total if b_overall_ll_total > 0 else 0
    print(f"  {on:>6}", end='')
    for sec in sections:
        sec_n = section_ll_total[sec]
        obs = section_ll[sec][on]
        rate = obs / sec_n if sec_n > 0 else 0
        E = rate / overall_rate if overall_rate > 0 else 0
        mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
        print(f"  {E:.2f}x{mk}({obs})", end='')
    print(f"  {overall_rate*100:.1f}%({b_overall_ll[on]})")

# Cross-dialect LF comparison summary
print("\n\n=== Cross-dialect LF section summary ===")
print("B herbal t-LF:", section_lf['herbal']['t'], "E=", f"{section_lf['herbal']['t']/(section_total['herbal']*b_overall_lf['t']/b_overall_total):.2f}x")
print("B astro qok-LF:", section_lf['astro']['qok'], "E=", f"{section_lf['astro']['qok']/(section_total['astro']*b_overall_lf['qok']/b_overall_total):.2f}x")
print("B pharma ok-LF:", section_lf['pharma']['ok'], "E=", f"{section_lf['pharma']['ok']/(section_total['pharma']*b_overall_lf['ok']/b_overall_total):.2f}x")
print("B cosmo t-LF:", section_lf['cosmo']['t'], "E=", f"{section_lf['cosmo']['t']/(section_total['cosmo']*b_overall_lf['t']/b_overall_total):.2f}x")
print()
print("A herbal_a qot-LF: E≈1.43x(N=68) [from exp_466]")
print("A stars t-LF: E≈2.12x(N=15) [F446]")
print("A cosmo t-LF: E≈1.63x(N=30) [from exp_466]")
