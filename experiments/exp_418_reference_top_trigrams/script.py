"""
exp_418: VMS-Specific Formula Types vs Reference Corpora (H636)

F415 showed formula-typed fraction is not discriminating. But the SPECIFIC formula types
may be VMS-specific. Compare top formula trigrams from:
- VMS B (EVA onset) — confirmed types: qok→sh→k, y→sh→ch, d→ot→ot, qok→ch→qo
- Latin Caesar (first-letter onset)
- Italian Dante (first-letter onset)

Question: are the structural patterns different? Do Latin/Italian formula types
reflect syntactic units (determiner→noun→verb)? Do VMS types reflect onset-class grammar?
"""

import os, re
from collections import Counter, defaultdict

DATA_PATH = os.path.expanduser('~/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt')
LATIN_PATH = os.path.expanduser('~/voynich-cryptanalyst/data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt')
ITALIAN_PATH = os.path.expanduser('~/voynich-cryptanalyst/data/reference_corpora/italian/dante_divina_commedia.txt')

# ===== VMS onset function =====
ONSET_ORDER = [
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o')
]

def get_onset_vms(word):
    for label, prefix in ONSET_ORDER:
        if word.startswith(prefix):
            return label
    return 'other'

def get_onset_fl(word):
    """First-letter onset for reference corpora."""
    word = word.lower().strip()
    if not word or not word[0].isalpha():
        return None
    return word[0]

def folio_base(folio):
    return re.sub(r'[rv]\d*$', '', folio)

# ===== VMS B cont lines =====
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

b_cont_lines = []
for fb, entries in folio_lines.items():
    if folio_dialect.get(fb, 'A') != 'B':
        continue
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in entries:
        if ln != min_ln and ln != max_ln:
            b_cont_lines.append(words)

# ===== Reference corpus line reading =====
def read_ref_corpus_lines(path, min_words=3):
    lines = []
    with open(path, 'r', encoding='latin-1') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            words = [w.lower() for w in re.split(r'[\s,;:.!?()]+', line)
                     if re.match(r'^[a-zA-Z]+$', w) and len(w) >= 2]
            if len(words) >= min_words:
                lines.append(words)
    return lines

latin_lines = read_ref_corpus_lines(LATIN_PATH)
italian_lines = read_ref_corpus_lines(ITALIAN_PATH)
print(f"VMS B cont lines: {len(b_cont_lines)}")
print(f"Latin lines: {len(latin_lines)}")
print(f"Italian lines: {len(italian_lines)}")

# ===== Formula analysis function =====
def top_formula_trigrams(lines, onset_fn, min_n=5, e_thresh=2.0, top_n=15):
    """
    For each line, extract (lf, pos1, pos2) trigram.
    Compute E_cond = P(pos2|lf,pos1) / P(pos2|pos1).
    Return top_n by E_cond with n >= min_n.
    """
    trigrams = Counter()
    bigrams_p1_p2 = Counter()
    bigrams_lf_p1 = Counter()
    total_lines = 0

    for words in lines:
        onsets = []
        for w in words:
            o = onset_fn(w)
            if o is not None and o != 'other':
                onsets.append(o)
        if len(onsets) < 3:
            continue
        lf, p1, p2 = onsets[0], onsets[1], onsets[2]
        trigrams[(lf, p1, p2)] += 1
        bigrams_p1_p2[(p1, p2)] += 1
        bigrams_lf_p1[(lf, p1)] += 1
        total_lines += 1

    # Compute E_cond for each trigram
    results = []
    for (lf, p1, p2), n_tri in trigrams.items():
        n_p1_total = sum(bigrams_p1_p2[(p1, x)] for x in set(b for a, b in bigrams_p1_p2 if a == p1))
        n_p1_p2 = bigrams_p1_p2[(p1, p2)]
        if n_p1_total < 5 or n_p1_p2 == 0:
            continue
        p_p2_given_p1 = n_p1_p2 / n_p1_total
        n_lf_p1_total = bigrams_lf_p1[(lf, p1)]
        if n_lf_p1_total == 0:
            continue
        p_p2_given_lf_p1 = n_tri / n_lf_p1_total
        E_cond = p_p2_given_lf_p1 / p_p2_given_p1 if p_p2_given_p1 > 0 else float('inf')
        results.append((E_cond, n_tri, lf, p1, p2))

    results.sort(reverse=True)
    formula_types = [(e, n, lf, p1, p2) for e, n, lf, p1, p2 in results if e >= e_thresh and n >= min_n]
    return formula_types[:top_n], total_lines

print("\n=== VMS B (EVA onset) top formula trigrams at N≥5, E≥2.0 ===")
vms_types, vms_total = top_formula_trigrams(b_cont_lines, get_onset_vms, min_n=5)
print(f"Total lines: {vms_total}")
for e, n, lf, p1, p2 in vms_types:
    print(f"  {lf}→{p1}→{p2}: E={e:.2f}×  N={n}")

print("\n=== Latin Caesar (first-letter onset) top formula trigrams at N≥5, E≥2.0 ===")
lat_types, lat_total = top_formula_trigrams(latin_lines, get_onset_fl, min_n=5)
print(f"Total lines: {lat_total}")
for e, n, lf, p1, p2 in lat_types:
    print(f"  {lf}→{p1}→{p2}: E={e:.2f}×  N={n}")

print("\n=== Italian Dante (first-letter onset) top formula trigrams at N≥5, E≥2.0 ===")
ita_types, ita_total = top_formula_trigrams(italian_lines, get_onset_fl, min_n=5)
print(f"Total lines: {ita_total}")
for e, n, lf, p1, p2 in ita_types:
    print(f"  {lf}→{p1}→{p2}: E={e:.2f}×  N={n}")

# Check for VMS-like structural pattern: same-class formula types (p1=p2 or p1 appears twice)
def classify_trigram(lf, p1, p2):
    if p1 == p2:
        return 'self-chain(p1=p2)'
    if lf == p1:
        return 'self-chain(lf=p1)'
    if lf == p2:
        return 'loop(lf=p2)'
    return 'hetero-class'

print("\n=== Structural classification of formula trigrams ===")
print("VMS B:")
for e, n, lf, p1, p2 in vms_types:
    print(f"  {lf}→{p1}→{p2}: {classify_trigram(lf,p1,p2)}")
print("Latin Caesar:")
for e, n, lf, p1, p2 in lat_types[:15]:
    print(f"  {lf}→{p1}→{p2}: {classify_trigram(lf,p1,p2)}")
print("Italian Dante:")
for e, n, lf, p1, p2 in ita_types[:15]:
    print(f"  {lf}→{p1}→{p2}: {classify_trigram(lf,p1,p2)}")

print("\n=== Done ===")
