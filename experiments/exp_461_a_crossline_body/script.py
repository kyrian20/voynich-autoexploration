"""
exp_461: A-Dialect Cross-Line Body-Conditional Rules Beyond ch+edy (H_new_V)
Q: Does A ok+edy→y drive the ok→y CL? Does A d+aiin→sh extend to A (parallel B F441)?
   Does A sh+edy CL differ from B sh+edy CL (B: →d; A: ?)

Method: Body-conditional CL analysis for ok/sh/d/qok/ol onset classes in A-dialect.
Parallel to exp_457 but for A-dialect.
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
    return body[0] if body else '_'

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

# A-dialect cross-line body-conditional
cl_body = defaultdict(Counter)
ll_body_total = Counter()
lf_onset_total = Counter()
total_cl = 0

for folio, lines in folios.items():
    if dialect_map.get(folio) != 'A': continue
    n = len(lines)
    if n < 3: continue
    cont = lines[1:-1]
    for ci in range(len(cont)-1):
        ll = cont[ci][-1]; lf = cont[ci+1][0]
        ll_on = get_onset(ll); lf_on = get_onset(lf)
        if ll_on == 'other' or lf_on == 'other': continue
        ll_bc = get_first_body_char(ll, ll_on)
        cl_body[(ll_on,ll_bc)][lf_on] += 1
        ll_body_total[(ll_on,ll_bc)] += 1
        lf_onset_total[lf_on] += 1
        total_cl += 1

print(f'A-dialect total CL pairs: {total_cl}')
print()
for onset in ['ok','sh','d','qok','ol']:
    body_keys = [(on,bc) for (on,bc) in ll_body_total if on==onset]
    body_keys.sort(key=lambda k: -ll_body_total[k])
    onset_total = sum(ll_body_total[k] for k in body_keys)
    if onset_total < 10: continue
    print(f'--- {onset.upper()} at LL (N={onset_total}) ---')
    all_after = Counter()
    for bk in body_keys:
        all_after.update(cl_body[bk])
    top_lf = [lf for lf,_ in all_after.most_common(5)]
    header = f'  body   N(LL)'
    for lf in top_lf: header += f'  ->{lf}'
    print(header)
    for (on,bc) in body_keys[:6]:
        n = ll_body_total[(on,bc)]
        if n < 5: continue
        row = f"  '{bc}':  {n}"
        for lf in top_lf:
            obs = cl_body[(on,bc)][lf]
            base_p = lf_onset_total[lf]/total_cl
            exp = n*base_p
            if exp >= 0.8:
                E = obs/exp
                mk = '↑' if E>=1.4 else ('↓' if E<=0.6 else ' ')
                row += f'  {E:.2f}x{mk}(N={obs})'
            else:
                row += f'  dir({obs})'
        print(row)
    print()
