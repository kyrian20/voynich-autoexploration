"""
exp_533: H_new_ES — A stars cross-LF-class a-onset positional role

Two signals from exp_526: sh-LF pen=a (dir, F519) and ot-LF pos2=a (dir, F520).
Is a-onset elevated at specific positions ACROSS multiple LF classes in A stars?
Or are these two signals isolated LF-class-specific rules?

Tests:
1. A stars overall: a-onset rates at pos1, pos2, pen, LF vs A herbal_a baseline
2. Per-LF-class: which LF classes show elevated a-onset at pen or pos2?
3. Within-section E: a@pos1 vs equal-position null hypothesis
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

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

def flag(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONF'
    elif obs >= 5 and E >= 2.0: return 'dir'
    elif obs >= 3 and E >= 2.5: return '(dir)'
    elif E >= 1.0: return f'{E:.2f}×'
    else: return f'DEPL {E:.2f}×'

folio_lines = parse_corpus(CORPUS)

a_stars_folios = {n: ls for n, ls in folio_lines.items() if 57 <= n <= 72 and not is_b_dialect(ls)}
a_ha_folios = {n: ls for n, ls in folio_lines.items() if n <= 56 and not is_b_dialect(ls)}

a_stars_lines = [ln for ls in a_stars_folios.values() for ln in ls]
a_ha_lines = [ln for ls in a_ha_folios.values() for ln in ls]

print(f"A stars: {len(a_stars_lines)} lines")
print(f"A herbal_a: {len(a_ha_lines)} lines")

def positional_baselines(lines, label):
    pos1 = Counter(); pos2 = Counter(); pen = Counter(); lf = Counter()
    N_p1 = N_p2 = N_pe = 0
    for ln in lines:
        lf[get_onset(ln[-1])] += 1
        if len(ln) >= 2:
            pos1[get_onset(ln[0])] += 1; N_p1 += 1
        if len(ln) >= 3:
            pos2[get_onset(ln[1])] += 1; N_p2 += 1
            pen[get_onset(ln[-2])] += 1; N_pe += 1
    print(f"\n{label}: pos1={N_p1}, pos2={N_p2}, pen={N_pe}, lf={len(lines)}")
    print(f"  a-onset: pos1={100*pos1['a']/N_p1:.1f}%, pos2={100*pos2['a']/N_p2:.1f}%, pen={100*pen['a']/N_pe:.1f}%, LF={100*lf['a']/len(lines):.1f}%")
    return pos1, pos2, pen, lf, N_p1, N_p2, N_pe

st_p1, st_p2, st_pe, st_lf, N_st_p1, N_st_p2, N_st_pe = positional_baselines(a_stars_lines, "A stars")
ha_p1, ha_p2, ha_pe, ha_lf, N_ha_p1, N_ha_p2, N_ha_pe = positional_baselines(a_ha_lines, "A herbal_a")

print("\nA stars a-onset E vs A herbal_a baseline:")
for pos_name, st_cnt, st_N, ha_cnt, ha_N in [
    ('pos1', st_p1['a'], N_st_p1, ha_p1['a'], N_ha_p1),
    ('pos2', st_p2['a'], N_st_p2, ha_p2['a'], N_ha_p2),
    ('pen',  st_pe['a'], N_st_pe, ha_pe['a'], N_ha_pe),
    ('LF',   st_lf['a'], len(a_stars_lines), ha_lf['a'], len(a_ha_lines)),
]:
    ha_rate = ha_cnt / ha_N if ha_N > 0 else 0
    E = (st_cnt / st_N) / ha_rate if ha_rate > 0 else 0
    print(f"  {pos_name}: A stars {st_cnt}/{st_N}={100*st_cnt/st_N:.1f}% vs A herbal_a {100*ha_rate:.1f}% → E={E:.2f}×  {flag(st_cnt, E)}")

# Per-LF-class
a_base_pos2 = st_p2['a'] / N_st_p2
a_base_pen  = st_pe['a'] / N_st_pe
print(f"\nSection-wide A stars: a@pos2={100*a_base_pos2:.1f}%, a@pen={100*a_base_pen:.1f}%")
print(f"\n{'LF':>6} {'N':>4} {'a@pos2':>8} {'E_p2':>7} {'a@pen':>7} {'E_pe':>7}")
for lf_cls in ['d','ch','a','o','sh','ok','ot','ol','y','s']:
    lf_lines = [ln for ln in a_stars_lines if get_onset(ln[-1]) == lf_cls]
    elig3 = [ln for ln in lf_lines if len(ln) >= 3]
    N_elig = len(elig3)
    if N_elig == 0: continue
    p2_a = sum(1 for ln in elig3 if get_onset(ln[1]) == 'a')
    pe_a = sum(1 for ln in elig3 if get_onset(ln[-2]) == 'a')
    E_p2 = (p2_a/N_elig) / a_base_pos2 if a_base_pos2 > 0 else 0
    E_pe = (pe_a/N_elig) / a_base_pen if a_base_pen > 0 else 0
    print(f"{lf_cls:>6} {len(lf_lines):>4} {p2_a:>3}/{N_elig:<3}E={E_p2:>5.2f}× {pe_a:>3}/{N_elig:<3}E={E_pe:>5.2f}×  {flag(p2_a,E_p2)} / {flag(pe_a,E_pe)}")
