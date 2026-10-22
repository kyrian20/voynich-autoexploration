"""
exp_464: Section-Specificity of A-Dialect Cross-Line Grammar (H_new_AB)
Q: Are A cross-line onset couplings (ch→ch, ok→y, s→qot, s→s, sh→d) section-specific,
paralleling B section grammar found in exp_462?

A-dialect sections: herbal_a (f1-56), stars (f57-72), herbal_b (f73-84), cosmo (f85-102), other_a (f103+)
"""
from pathlib import Path as _RepositoryPath
import re
from collections import defaultdict, Counter

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on): return on
    return 'other'

def get_section_a(folio):
    """A-dialect section classifier by folio number."""
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

# Count dialect folios
n_a = sum(1 for d in dialect_map.values() if d == 'A')
n_b = sum(1 for d in dialect_map.values() if d == 'B')
print(f"Folio counts: A={n_a}, B={n_b}")

target_pairs = [
    ('ch', 'ch'),
    ('ok', 'y'),
    ('s', 'qot'),
    ('s', 's'),
    ('d', 'sh'),
    ('sh', 'd'),
    ('qok', 's'),
    ('qok', 'ch'),
    ('d', 'qok'),
    ('qot', 'ch'),
]

section_cl = defaultdict(lambda: defaultdict(Counter))
section_ll_total = defaultdict(Counter)
section_lf_total = defaultdict(Counter)
section_total_cl = Counter()

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

sections = ['herbal_a', 'stars', 'herbal_b', 'cosmo', 'other_a']
print('\nA-dialect cross-line coupling section analysis')
print(f'{"pair":>10}', end='')
for sec in sections:
    print(f'  {sec:>12}', end='')
print('  overall')
print(f'{"":>10}', end='')
for sec in sections:
    print(f'  N={section_total_cl[sec]:>9}', end='')
print()

for ll_on, lf_on in target_pairs:
    print(f'{ll_on}→{lf_on}:  ', end='')
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
            print(f'  dir(N={obs})', end='')
    if total_ll >= 5:
        base_p = total_lf / total_all if total_all > 0 else 0
        exp = total_ll * base_p
        E = total_obs / exp if exp > 0 else 0
        print(f'  {E:.2f}x(N={total_obs})')
    else:
        print(f'  dir(N={total_obs})')

# Detailed word-level for s→qot to compare with F443/exp_460
print('\n\nDetailed: s→qot CL cases by folio')
sq_cases = []
for folio, lines in folios.items():
    if dialect_map.get(folio) != 'A': continue
    sec = get_section_a(folio)
    n = len(lines)
    if n < 3: continue
    cont = lines[1:-1]
    for ci in range(len(cont)-1):
        ll_words = cont[ci]; lf_words = cont[ci+1]
        if not ll_words or not lf_words: continue
        ll_w = ll_words[-1]; lf_w = lf_words[0]
        if get_onset(ll_w) == 's' and get_onset(lf_w) == 'qot':
            sq_cases.append((folio, sec, ll_w, lf_w))
for case in sq_cases:
    print(f'  {case}')

# Full cross-line matrix for A-dialect (top pairs by count)
print('\n\nA-dialect CL onset matrix (total across all sections):')
all_cl = defaultdict(Counter)
all_ll_total = Counter()
all_lf_total = Counter()
total_all_cl = 0
for folio, lines in folios.items():
    if dialect_map.get(folio) != 'A': continue
    n = len(lines)
    if n < 3: continue
    cont = lines[1:-1]
    for ci in range(len(cont)-1):
        ll = cont[ci][-1]; lf = cont[ci+1][0]
        ll_on = get_onset(ll); lf_on = get_onset(lf)
        if ll_on == 'other' or lf_on == 'other': continue
        all_cl[ll_on][lf_on] += 1
        all_ll_total[ll_on] += 1
        all_lf_total[lf_on] += 1
        total_all_cl += 1

print(f'Total A CL pairs: {total_all_cl}')
top_ll = [x for x, _ in all_ll_total.most_common(10)]
top_lf = [x for x, _ in all_lf_total.most_common(8)]
print(f'{"ll\\lf":>8}', end='')
for lf in top_lf:
    print(f'  {lf:>6}', end='')
print()
for ll in top_ll:
    print(f'{ll:>8}', end='')
    for lf in top_lf:
        obs = all_cl[ll][lf]
        n_ll = all_ll_total[ll]
        base_p = all_lf_total[lf] / total_all_cl
        exp = n_ll * base_p
        E = obs / exp if exp > 0 else 0
        if obs >= 3:
            mk = '↑' if E>=1.4 else ('↓' if E<=0.6 else ' ')
            print(f'  {E:.1f}{mk}({obs})', end='')
        else:
            print(f'  dir({obs})', end='')
    print()
