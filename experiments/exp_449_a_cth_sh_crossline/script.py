"""
exp_449: A cth→sh Cross-Line Section Analysis (H_new_L)
Q: Is A cth(LL)→sh(LF) E=1.93×/N=12 section-specific?
Also examine A s→s cross-line (E=2.57×/N=8) section distribution.
"""
from pathlib import Path as _RepositoryPath
import re
from collections import defaultdict, Counter

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def parse_corpus():
    pattern = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    folios = defaultdict(list)
    with open(ZL3B, encoding='utf-8') as f:
        for line in f:
            for m in pattern.finditer(line):
                folio = m.group(1).lstrip('+*=&~')
                lc = m.group(3).lstrip('+*=/~&')
                if not lc.lstrip('@').startswith('P'):
                    continue
                text = m.group(4).strip()
                words = [w for w in re.split(r'[-.\s]', text)
                         if re.match(r'^[a-z]+$', w) and len(w) >= 2]
                if words:
                    folios[folio].append(words)
    return folios

def classify_dialects(folios):
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for ws in lines)
        if total == 0: continue
        edy = sum(1 for ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def get_section(folio):
    digits = re.sub(r'[^0-9]', '', folio)
    if not digits:
        return 'unknown'
    f = int(digits[:3]) if len(digits) >= 3 else int(digits)
    if f <= 72:
        return 'herbal'
    elif f <= 84:
        return 'astro'
    elif f <= 102:
        return 'bio'
    elif f <= 116:
        return 'pharma'
    else:
        return 'other'

folios = parse_corpus()
dialect_map = classify_dialects(folios)

# Collect A-dialect cross-line pairs with section info
cl_data = []
for folio, lines in folios.items():
    if folio not in dialect_map or dialect_map[folio] != 'A':
        continue
    n = len(lines)
    if n < 3:
        continue
    cont_lines = lines[1:-1]
    cn = len(cont_lines)
    section = get_section(folio)
    for ci in range(cn - 1):
        ll_word = cont_lines[ci][-1]
        lf_word = cont_lines[ci+1][0]
        ll_on = get_onset(ll_word)
        lf_on = get_onset(lf_word)
        if ll_on != 'other' and lf_on != 'other':
            cl_data.append((section, folio, ll_word, lf_word, ll_on, lf_on))

# A cth→sh cross-line
print("=== A cth(LL)→sh(LF) cross-line pairs (N=12) ===")
cth_sh = [(r[0], r[1], r[2], r[3]) for r in cl_data if r[4]=='cth' and r[5]=='sh']
print(f"N = {len(cth_sh)}")
section_ct = Counter(r[0] for r in cth_sh)
print("Section distribution:", dict(section_ct))
print("\nPairs:")
for sec, folio, ll_w, lf_w in cth_sh:
    print(f"  {folio}({sec}): {ll_w} → {lf_w}")

# Compare: cth at LL total distribution by section
print("\n=== A cth at LL by section (all cross-line pairs) ===")
cth_ll_sec = Counter(r[0] for r in cl_data if r[4]=='cth')
sh_lf_sec = Counter(r[0] for r in cl_data if r[5]=='sh')
total_sec = Counter(r[0] for r in cl_data)
for sec in ['herbal','astro','bio','pharma']:
    cth_cnt = cth_ll_sec[sec]
    total = total_sec[sec]
    if total > 0:
        print(f"  {sec}: cth-LL={cth_cnt}/{total} ({cth_cnt/total*100:.1f}%)")

# A s→s cross-line
print("\n=== A s→s cross-line pairs ===")
s_s = [(r[0], r[1], r[2], r[3]) for r in cl_data if r[4]=='s' and r[5]=='s']
print(f"N = {len(s_s)}")
section_ct2 = Counter(r[0] for r in s_s)
print("Section distribution:", dict(section_ct2))
for sec, folio, ll_w, lf_w in s_s:
    print(f"  {folio}({sec}): {ll_w} → {lf_w}")

# A o→s cross-line (E=2.21×/N=8) — the other strong A-specific rule
print("\n=== A o→s cross-line pairs (E=2.21×) ===")
o_s = [(r[0], r[1], r[2], r[3]) for r in cl_data if r[4]=='o' and r[5]=='s']
print(f"N = {len(o_s)}")
section_ct3 = Counter(r[0] for r in o_s)
print("Section distribution:", dict(section_ct3))
