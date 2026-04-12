"""
exp_538: H_new_FA — qok→qot CONF triplet structure
A herbal_a: qok→qot CONF (E=2.22×/obs=12, F542). Does this form a triplet?
What comes after qot in qok→qot→X sequences?
Also: check qot→qok asymmetry and section scope.
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
        if word.startswith(onset): return onset
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
        if not lc.lstrip('@').startswith('P'): continue
        words = [w for w in re.split(r'[-.\s]', text)
                 if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words: continue
        n = folio_num(folio)
        if n is None: continue
        folio_lines[n].append(words)
    return folio_lines

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words: return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

def flag(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONF'
    elif obs >= 5 and E >= 2.0: return 'dir'
    elif obs >= 3 and E >= 2.5: return '(dir)'
    elif E >= 1.0: return f'{E:.2f}×'
    else: return f'DEPL {E:.2f}×'

folio_lines = parse_corpus(CORPUS)
a_ha_folios = {n: ls for n, ls in folio_lines.items() if n <= 56 and not is_b_dialect(ls)}
a_ha_lines = [ln for ls in a_ha_folios.values() for ln in ls]

a_stars_folios = {n: ls for n, ls in folio_lines.items() if 57 <= n <= 72 and not is_b_dialect(ls)}
a_stars_lines = [ln for ls in a_stars_folios.values() for ln in ls]

a_cosmo_folios = {n: ls for n, ls in folio_lines.items() if 85 <= n <= 102 and not is_b_dialect(ls)}
a_cosmo_lines = [ln for ls in a_cosmo_folios.values() for ln in ls]

print(f"A herbal_a: {len(a_ha_lines)} lines")
print(f"A stars: {len(a_stars_lines)} lines")
print(f"A cosmo: {len(a_cosmo_lines)} lines")

# Part 1: qok→qot→X triplets in A herbal_a
print("\n" + "="*60)
print("PART 1: qok→qot→X TRIPLETS (A herbal_a)")
print("="*60)

triplet_targets = Counter()
triplet_lines = []
for ln in a_ha_lines:
    for i in range(len(ln)-2):
        if get_onset(ln[i]) == 'qok' and get_onset(ln[i+1]) == 'qot':
            tgt = get_onset(ln[i+2])
            triplet_targets[tgt] += 1
            triplet_lines.append(ln)

# baseline for position i+2: all words at position after any bigram
all_pos2_after_bigram = Counter()
all_bigrams = 0
for ln in a_ha_lines:
    for i in range(len(ln)-2):
        all_pos2_after_bigram[get_onset(ln[i+2])] += 1
        all_bigrams += 1

N_triplets = sum(triplet_targets.values())
print(f"qok→qot pairs: {N_triplets}")
if N_triplets > 0:
    for tgt, obs in triplet_targets.most_common():
        base_rate = all_pos2_after_bigram[tgt] / all_bigrams if all_bigrams > 0 else 0
        cond_rate = obs / N_triplets
        E = cond_rate / base_rate if base_rate > 0 else 0
        print(f"  qok→qot→{tgt}: {obs}/{N_triplets} E={E:.2f}× {flag(obs, E)}")
    print("\nSample lines with qok→qot:")
    seen = set()
    for ln in triplet_lines[:5]:
        key = tuple(ln)
        if key not in seen:
            seen.add(key)
            print(f"  {' '.join(ln)}")

# Part 2: qot→qok asymmetry check in A herbal_a
print("\n" + "="*60)
print("PART 2: qot→qok vs qok→qot ASYMMETRY (A herbal_a)")
print("="*60)

all_bigrams_data = Counter()
total_bg = 0
qot_targets = Counter()
qok_targets = Counter()
N_qot_send = 0; N_qok_send = 0

for ln in a_ha_lines:
    for i in range(len(ln)-1):
        total_bg += 1
        succ = get_onset(ln[i+1])
        all_bigrams_data[succ] += 1
        if get_onset(ln[i]) == 'qot':
            N_qot_send += 1
            qot_targets[succ] += 1
        if get_onset(ln[i]) == 'qok':
            N_qok_send += 1
            qok_targets[succ] += 1

base_qok = all_bigrams_data['qok'] / total_bg
base_qot = all_bigrams_data['qot'] / total_bg
print(f"qot→qok: obs={qot_targets['qok']}/{N_qot_send} E={(qot_targets['qok']/N_qot_send)/base_qok:.2f}× {flag(qot_targets['qok'], (qot_targets['qok']/N_qot_send)/base_qok)}")
print(f"qok→qot: obs={qok_targets['qot']}/{N_qok_send} E={(qok_targets['qot']/N_qok_send)/base_qot:.2f}× {flag(qok_targets['qot'], (qok_targets['qot']/N_qok_send)/base_qot)}")
print(f"Asymmetric? qok→qot CONF but qot→qok sub-CONF suggests DIRECTED coupling")

# Part 3: qok→qot scope check in A stars and A cosmo
print("\n" + "="*60)
print("PART 3: qok→qot SCOPE CHECK (A stars, A cosmo)")
print("="*60)

for label, lines in [("A herbal_a", a_ha_lines), ("A stars", a_stars_lines), ("A cosmo", a_cosmo_lines)]:
    all_bg = Counter()
    total_bg2 = 0
    qok_tgts = Counter()
    N_qok = 0
    for ln in lines:
        for i in range(len(ln)-1):
            total_bg2 += 1
            all_bg[get_onset(ln[i+1])] += 1
            if get_onset(ln[i]) == 'qok':
                N_qok += 1
                qok_tgts[get_onset(ln[i+1])] += 1
    base = all_bg['qot'] / total_bg2 if total_bg2 > 0 else 0
    obs = qok_tgts['qot']
    E = (obs/N_qok) / base if N_qok > 0 and base > 0 else 0
    print(f"{label}: qok→qot obs={obs}/{N_qok} E={E:.2f}× {flag(obs, E)}")
