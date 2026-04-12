"""
exp_462: Section-Specificity of B Cross-Line Grammar (H_new_Z)
Q: Are B cross-line onset couplings (F438/F442/F443) section-specific?

Method: Decompose B CL couplings by section (herbal/astro/pharma/bio/text/cosmo).
Compute section-specific E for: ch→qot, s→qok, d→sh, d→qok, ok→y, sh→d, qok→s.
"""
import re
from collections import defaultdict, Counter

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on): return on
    return 'other'

def get_section(folio):
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
target_pairs = [('ch','qot'), ('s','qok'), ('d','sh'), ('d','qok'), ('ok','y'), ('sh','d'), ('qok','s')]

section_cl = defaultdict(lambda: defaultdict(Counter))
section_ll_total = defaultdict(Counter)
section_lf_total = defaultdict(Counter)
section_total_cl = Counter()

for folio, lines in folios.items():
    if dialect_map.get(folio) != 'B': continue
    sec = get_section(folio)
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

sections = ['herbal','astro','pharma','bio','text','cosmo']
print('B-dialect cross-line coupling section analysis')
print(f'{"pair":>10}', end='')
for sec in sections:
    print(f'  {sec:>10}', end='')
print('  overall')
for sec in sections:
    print(f'  N_CL={section_total_cl[sec]}', end='')
print()

for ll_on, lf_on in target_pairs:
    print(f'{ll_on}→{lf_on}:     ', end='')
    total_obs = 0; total_ll = 0; total_lf = 0; total_all = 0
    for sec in sections:
        n_ll = section_ll_total[sec][ll_on]
        obs = section_cl[sec][ll_on][lf_on]
        total_lf_sec = section_lf_total[sec][lf_on]
        total_cl_sec = section_total_cl[sec]
        total_obs += obs; total_ll += n_ll
        total_lf += total_lf_sec; total_all += total_cl_sec
        if n_ll >= 5 and total_cl_sec > 0:
            base_p = total_lf_sec / total_cl_sec
            exp = n_ll * base_p
            E = obs / exp if exp > 0 else 0
            mk = '↑' if E>=1.4 else ('↓' if E<=0.6 else ' ')
            print(f'  {E:.1f}x{mk}(N={obs})', end='')
        else:
            print(f'  dir({obs})', end='')
    if total_ll >= 5:
        base_p = total_lf / total_all if total_all > 0 else 0
        exp = total_ll * base_p
        E = total_obs / exp if exp > 0 else 0
        print(f'  {E:.2f}x(N={total_obs})')
    else:
        print(f'  dir({total_obs})')
