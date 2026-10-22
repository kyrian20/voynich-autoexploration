"""
exp_411: Trigram Formula-Typed Fraction in Reference Corpora (H631)

Question: Is VMS's 9.3% B / 7.6% A formula-typed fraction distinctive relative
to natural language (Latin, Italian)?

Method:
1. Apply the same trigram E_cond methodology (E_cond = P(pos2|LF,pos1)/P(pos2|pos1))
   to reference corpus "lines" (sentences/verses).
2. For reference corpora: onset class = first letter of word (26 classes).
3. For VMS: onset class = EVA syllabic onset (20 classes, used in F405/F406).
4. Also test a within-line shuffle control (should give ~0% formula-typed).
5. Compare formula-typed fraction across:
   - VMS B cont lines (known: 9.3%)
   - VMS A cont lines (known: 7.6%)
   - Latin Caesar (prose)
   - Italian Dante (verse)
   - Shuffled VMS B (control)

Note: Onset class granularity differs (VMS: 20 classes; Latin/Italian: 26 letters).
More classes → smaller base rates → potentially higher E_cond → potentially higher
formula-typed fraction. This is a methodological limitation (stated in result).
To address it, also run VMS with first-letter onset (same grain as reference).
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, defaultdict
from itertools import chain

# ---- VMS setup ----
VMS_PATH = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt'))
LATIN_PATH = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2] / 'data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt'))
ITALIAN_PATH = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2] / 'data/reference_corpora/italian/dante_divina_commedia.txt'))

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

def get_onset_letter(word):
    """First letter onset for reference corpora."""
    w = word.lower()
    if w and w[0].isalpha():
        return w[0]
    return None

def folio_base(folio):
    return re.sub(r'[rv]\d*$', '', folio)

def formula_fraction(lines, onset_fn, min_n=3, e_thresh=2.0):
    """
    Compute formula-typed trigram fraction.
    lines: list of word lists
    onset_fn: function word -> onset class
    Returns (formula_frac, n_formula_lines, n_total_lines, top_trigrams)
    """
    # Filter lines to >= 3 words with valid onsets
    valid_lines = []
    for words in lines:
        onsets = [onset_fn(w) for w in words]
        onsets = [o for o in onsets if o is not None and o != 'other']
        if len(onsets) >= 3:
            valid_lines.append(onsets)

    if not valid_lines:
        return 0.0, 0, 0, []

    # Count trigrams and bigrams
    trigrams = Counter()
    lf_p1_counts = Counter()
    p1_p2_counts = Counter()
    p1_total = Counter()

    for onsets in valid_lines:
        lf = onsets[0]
        p1 = onsets[1]
        p2 = onsets[2]
        trigrams[(lf, p1, p2)] += 1
        lf_p1_counts[(lf, p1)] += 1
        p1_p2_counts[(p1, p2)] += 1
        p1_total[p1] += 1

    # Compute E_cond for each trigram
    e_cond_dict = {}
    for (lf, p1, p2), n in trigrams.items():
        n_lf_p1 = lf_p1_counts[(lf, p1)]
        n_p1_p2 = p1_p2_counts[(p1, p2)]
        n_p1 = p1_total[p1]
        if n_lf_p1 == 0 or n_p1 == 0 or n_p1_p2 == 0:
            continue
        # E_cond = P(pos2|LF,pos1) / P(pos2|pos1)
        p_p2_given_lf_p1 = n / n_lf_p1
        p_p2_given_p1 = n_p1_p2 / n_p1
        e_cond = p_p2_given_lf_p1 / p_p2_given_p1
        e_cond_dict[(lf, p1, p2)] = e_cond

    # Formula-typed trigrams
    formula_trigrams = {k for k, e in e_cond_dict.items()
                       if e >= e_thresh and trigrams[k] >= min_n}

    # Count formula-typed lines
    n_formula = sum(1 for onsets in valid_lines
                   if (onsets[0], onsets[1], onsets[2]) in formula_trigrams)
    n_total = len(valid_lines)

    # Top trigrams by E_cond (N >= min_n)
    top = sorted([(k, e, trigrams[k]) for k, e in e_cond_dict.items()
                  if trigrams[k] >= min_n],
                 key=lambda x: -x[1])[:10]

    return n_formula / n_total if n_total > 0 else 0.0, n_formula, n_total, top

# ====== Load VMS B and A cont lines ======
folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0})
with open(VMS_PATH, 'r', encoding='utf-8') as fh:
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

folio_lines_vms = defaultdict(list)
with open(VMS_PATH, 'r', encoding='utf-8') as fh:
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
        folio_lines_vms[fb].append((ln, words))

vms_cont = {'A': [], 'B': []}
for fb, entries in folio_lines_vms.items():
    dialect = folio_dialect.get(fb, 'A')
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in entries:
        if ln != min_ln and ln != max_ln:
            vms_cont[dialect].append(words)

# ====== Load Latin (Caesar) ======
with open(LATIN_PATH, 'r', encoding='utf-8', errors='replace') as fh:
    latin_text = fh.read()

# Strip Project Gutenberg header/footer
# Find start of Latin text (look for lowercase latin words)
# Split into sentences by . ; :
latin_text = latin_text.lower()
# Extract only alphabetic words
latin_sentences_raw = re.split(r'[.;:\n]+', latin_text)
latin_lines = []
for sent in latin_sentences_raw:
    words = re.findall(r'[a-z]+', sent)
    words = [w for w in words if len(w) >= 2]
    if len(words) >= 3:
        latin_lines.append(words)

# ====== Load Italian (Dante) ======
with open(ITALIAN_PATH, 'r', encoding='utf-8', errors='replace') as fh:
    dante_text = fh.read()

dante_text = dante_text.lower()
# Dante has verse lines — use those directly
dante_verse_raw = dante_text.split('\n')
dante_lines = []
for verse in dante_verse_raw:
    words = re.findall(r'[a-zàáèéìíòóùú]+', verse)
    words = [w for w in words if len(w) >= 2]
    if len(words) >= 3:
        dante_lines.append(words)

# ====== Shuffled VMS B control ======
random.seed(42)
shuffled_b = []
for words in vms_cont['B']:
    shuffled = words[:]
    random.shuffle(shuffled)
    shuffled_b.append(shuffled)

# ====== Compute formula fractions ======
print("=== Trigram Formula-Typed Fraction (E_cond >= 2.0, N >= 3) ===\n")

corpora = [
    ("VMS B cont (EVA onset)", vms_cont['B'], get_onset_vms),
    ("VMS A cont (EVA onset)", vms_cont['A'], get_onset_vms),
    ("VMS B cont (first-letter onset)", vms_cont['B'], get_onset_letter),
    ("VMS A cont (first-letter onset)", vms_cont['A'], get_onset_letter),
    ("Latin Caesar (first-letter)", latin_lines, get_onset_letter),
    ("Italian Dante (first-letter)", dante_lines, get_onset_letter),
    ("VMS B shuffled control (EVA)", shuffled_b, get_onset_vms),
]

results = {}
for name, lines, onset_fn in corpora:
    frac, n_formula, n_total, top = formula_fraction(lines, onset_fn)
    results[name] = (frac, n_formula, n_total)
    print(f"{name}:")
    print(f"  Lines (len>=3): {n_total}")
    print(f"  Formula-typed: N={n_formula} ({frac*100:.1f}%)")
    print(f"  Top trigrams (E>=2.0, N>=3):")
    for (lf, p1, p2), e, n in top[:5]:
        print(f"    ({lf},{p1},{p2}): E={e:.2f}×, N={n}")
    print()

# ====== Summary table ======
print("\n=== Summary ===")
print(f"{'Corpus':<40} {'%formula':>10} {'N_lines':>8} {'N_formula':>10}")
print("-" * 72)
for name, (frac, n_formula, n_total) in results.items():
    print(f"{name:<40} {frac*100:>9.1f}% {n_total:>8d} {n_formula:>10d}")

print("\n=== Done ===")
