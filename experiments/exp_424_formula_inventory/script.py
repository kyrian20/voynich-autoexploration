"""
exp_424: Updated B formula type inventory (H646)

Compile the current confirmed B formula type inventory after exp_416-423.
Recompute E_cond and N for all candidate types using the standard cont-line methodology.
Report the formula-typed fraction at N>=5.

Confirmed/candidate types to check:
- qok→sh→k (F416)
- d→ot→ot (F416/F419)
- l→ch→qok (F420/F421)
- d→qok→ol (F424)
- y→sh→ch (F394/F398)
- y→o→ch (F425)
- qok→ch→qo (F416)
- p→sh→ok (F416/F421)
- d→ch→l (F424)
- p→sh→qot (F396/F405) -- borderline
- s→sh→qok (F398)
- s→sh→l (F398)
- qok→sh→l (?)

New candidates from exp_418:
- l→ch→qok, d→qok→ol, y→sh→ch, y→o→ch, qok→ch→qo, d→ch→y (RETRACTED), d→ch→y
"""

import os, re
from collections import Counter, defaultdict

DATA_PATH = os.path.expanduser('~/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = [
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o')
]

def get_onset(word):
    for label, prefix in ONSET_ORDER:
        if word.startswith(prefix):
            return label
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv]\d*$', '', folio)

folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0})
with open(DATA_PATH, 'r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m:
            continue
        folio = m.group(1).lstrip('+*=&~')
        fb = folio_base(folio)
        lc = m.group(3).lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            folio_word_stats[fb]['total'] += 1
            if w.endswith('edy') or w.endswith('eedy'):
                folio_word_stats[fb]['edy'] += 1

folio_dialect = {}
for fb, stats in folio_word_stats.items():
    t = stats['total']
    folio_dialect[fb] = 'B' if t > 0 and stats['edy'] / t >= 0.05 else 'A'

folio_lines = defaultdict(list)
with open(DATA_PATH, 'r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m:
            continue
        folio = m.group(1).lstrip('+*=&~')
        ln = int(m.group(2))
        lc = m.group(3).lstrip('+*=/~&')
        fb = folio_base(folio)
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((ln, words))

cont_lines = {'A': [], 'B': []}
for fb, entries in folio_lines.items():
    dialect = folio_dialect.get(fb, 'A')
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in entries:
        if ln != min_ln and ln != max_ln:
            cont_lines[dialect].append(words)

b_lines = cont_lines['B']
print(f"B cont lines: {len(b_lines)}")

# Build trigram table for B
trigrams = Counter()
bigrams_p1_p2 = Counter()
bigrams_lf_p1 = Counter()
n_valid = 0

for words in b_lines:
    onsets = [get_onset(w) for w in words]
    # Filter 'other' onsets
    onsets_clean = [o for o in onsets if o != 'other']
    if len(onsets_clean) < 3:
        continue
    lf, p1, p2 = onsets_clean[0], onsets_clean[1], onsets_clean[2]
    trigrams[(lf, p1, p2)] += 1
    bigrams_p1_p2[(p1, p2)] += 1
    bigrams_lf_p1[(lf, p1)] += 1
    n_valid += 1

print(f"B lines with valid trigram: {n_valid}")

# Compute E_cond for candidate types
candidates = [
    ('qok', 'sh', 'k'),
    ('d', 'ot', 'ot'),
    ('l', 'ch', 'qok'),
    ('d', 'qok', 'ol'),
    ('y', 'sh', 'ch'),
    ('y', 'o', 'ch'),
    ('qok', 'ch', 'qo'),
    ('p', 'sh', 'ok'),
    ('d', 'ch', 'l'),
    ('p', 'sh', 'qot'),  # borderline
    ('s', 'sh', 'qok'),
    ('s', 'sh', 'l'),
    ('d', 'sh', 'qok'),  # baseline reference
    ('d', 'ch', 'qok'),  # baseline reference
    ('d', 'ch', 'y'),    # retracted, verify N
    ('qok', 'sh', 'l'),
]

print("\n=== B formula type inventory (E_cond analysis) ===")
print(f"{'Trigram':20s}  {'N_tri':5s}  {'N_lf_p1':7s}  {'E_cond':7s}  {'Status'}")
print("-"*65)

for lf, p1, p2 in candidates:
    n_tri = trigrams[(lf, p1, p2)]
    n_lf_p1 = bigrams_lf_p1[(lf, p1)]
    n_p1_total = sum(bigrams_p1_p2[(p1, x)] for x in set(b for a, b in bigrams_p1_p2 if a == p1))
    n_p1_p2 = bigrams_p1_p2[(p1, p2)]
    if n_lf_p1 == 0 or n_p1_total == 0 or n_p1_p2 == 0:
        e_cond = float('inf') if n_tri > 0 else 0
    else:
        p_p2_given_p1 = n_p1_p2 / n_p1_total
        p_p2_given_lf_p1 = n_tri / n_lf_p1
        e_cond = p_p2_given_lf_p1 / p_p2_given_p1 if p_p2_given_p1 > 0 else float('inf')
    status = 'CONFIRMED(N>=5)' if n_tri >= 5 and e_cond >= 2.0 else ('DIR(N<5)' if n_tri > 0 else 'ABSENT')
    label = f"{lf}→{p1}→{p2}"
    print(f"  {label:20s}  {n_tri:5d}  {n_lf_p1:7d}  {e_cond:7.2f}×  {status}")

# Count formula-typed lines at N>=5
n_formula_n5 = sum(1 for words in b_lines
                   for _ in [None]
                   if len([get_onset(w) for w in words if get_onset(w) != 'other']) >= 3
                   and (lambda o: trigrams.get(tuple(o[:3]), 0) >= 5
                        and bigrams_lf_p1.get((o[0], o[1]), 0) > 0
                        and bigrams_p1_p2.get((o[1], o[2]), 0) > 0
                        and (trigrams.get(tuple(o[:3]), 0) / bigrams_lf_p1.get((o[0], o[1]), 1))
                            / (bigrams_p1_p2.get((o[1], o[2]), 1) / sum(bigrams_p1_p2.get((o[1], x), 0) for x in set(b for a, b in bigrams_p1_p2 if a == o[1]))) >= 2.0
                        )([o for o in [get_onset(w) for w in words] if o != 'other']))

# Simpler recount
formula_types_n5 = set()
for (lf, p1, p2), n in trigrams.items():
    if n < 5:
        continue
    n_lf_p1 = bigrams_lf_p1[(lf, p1)]
    n_p1_total = sum(bigrams_p1_p2[(p1, x)] for x in set(b for a, b in bigrams_p1_p2 if a == p1))
    n_p1_p2 = bigrams_p1_p2[(p1, p2)]
    if n_lf_p1 == 0 or n_p1_total == 0 or n_p1_p2 == 0:
        continue
    p_p2_given_p1 = n_p1_p2 / n_p1_total
    e_cond = (n / n_lf_p1) / p_p2_given_p1
    if e_cond >= 2.0:
        formula_types_n5.add((lf, p1, p2))

n_formula_lines = 0
n_total_valid = 0
for words in b_lines:
    onsets_clean = [get_onset(w) for w in words if get_onset(w) != 'other']
    if len(onsets_clean) >= 3:
        n_total_valid += 1
        if tuple(onsets_clean[:3]) in formula_types_n5:
            n_formula_lines += 1

print(f"\nFormula types at N>=5, E>=2.0: {len(formula_types_n5)}")
print(f"Formula-typed lines: {n_formula_lines}/{n_total_valid} = {n_formula_lines/n_total_valid:.3f}")

print(f"\nAll {len(formula_types_n5)} formula types at N>=5, E>=2.0:")
for lf, p1, p2 in sorted(formula_types_n5):
    n = trigrams[(lf, p1, p2)]
    n_lf_p1 = bigrams_lf_p1[(lf, p1)]
    n_p1_total = sum(bigrams_p1_p2[(p1, x)] for x in set(b for a, b in bigrams_p1_p2 if a == p1))
    n_p1_p2 = bigrams_p1_p2[(p1, p2)]
    e = (n/n_lf_p1) / (n_p1_p2/n_p1_total)
    print(f"  {lf}→{p1}→{p2}: E={e:.2f}×  N={n}")

print("\n=== Done ===")
