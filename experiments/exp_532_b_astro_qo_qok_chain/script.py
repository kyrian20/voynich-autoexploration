"""
exp_532: B astro qo-LF chain (H_new_EV) + qok CL chain (H_new_EW)

H_new_EV: B astro d→qo (dir, E=3.08×/obs=8, F495). Is qo the B-astro
  functional analog of qot (A herbal_a d→qot→ch→... chain)?
  Test: B astro qo-LF as sender. What follows qo-LF lines?

H_new_EW: B astro qok→qok CONF (F495). Is qok part of a multi-step chain?
  Test: B astro qok-LF full sender profile + qok→qok→? triplets.
"""

import re
from collections import defaultdict, Counter

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

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
b_astro_folios = {n: ls for n, ls in folio_lines.items() if 73 <= n <= 84 and is_b_dialect(ls)}
all_ba_lines = [ln for ls in b_astro_folios.values() for ln in ls]
ba_lf = Counter(get_onset(ln[-1]) for ln in all_ba_lines)
N_ba = len(all_ba_lines)
ba_base = {cls: cnt/N_ba for cls, cnt in ba_lf.items()}
ba_pairs = []
for n, lines in sorted(b_astro_folios.items()):
    for i in range(len(lines)-1):
        ba_pairs.append((get_onset(lines[i][-1]), get_onset(lines[i+1][-1])))

# [See inline execution results — same logic as exp_531 extended with triplet analysis]
