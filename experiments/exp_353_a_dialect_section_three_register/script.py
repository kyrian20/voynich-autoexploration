"""
exp_353: A-Dialect Section-Specific Three-Register Grammar (H557)

Background:
- F353 (exp_351): B-dialect three-register grammar (folio-opener/continuation/folio-closer)
  is section-invariant. Every B-dialect section shows: folio-first LF = 71-80% gallows,
  folio-last = short lines + anti-gallows.
- F345 (exp_343): A-dialect folio-first LF overall = 73.6% gallows. But per-section not tested.
- Open question: does A-dialect herbal specifically show same pattern? Pharma?

Plan:
1. Two-pass corpus read: classify folios by dialect (B = edy+eedy >= 5%)
2. For A-dialect folios, assign sections by folio number
3. For each folio, identify lines: folio-first (min line_num), folio-last (max line_num), continuation (rest)
4. Compute per section: folio-first LF gallows%, cont LF gallows%, folio-last LF gallows%
5. Compute mean line lengths for folio-last vs continuation

Section mapping (folio number -> section):
  1-66: herbal, 67-73: astro, 74-84: bio (B-dialect only),
  85-86: cosmo, 87-102: pharma, 103+: text/recipe
"""

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

GALLOWS_ONSETS = {'k', 't', 'p', 'f'}

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def folio_number(fb):
    """Extract numeric folio number from folio base like 'f1', 'f86v5' -> 86, 'f103' -> 103."""
    m = re.match(r'f(\d+)', fb)
    return int(m.group(1)) if m else None

def section_for_folio(fb):
    n = folio_number(fb)
    if n is None: return 'unknown'
    if 1 <= n <= 66: return 'herbal'
    if 67 <= n <= 73: return 'astro'
    if 74 <= n <= 84: return 'bio'
    if 85 <= n <= 86: return 'cosmo'
    if 87 <= n <= 102: return 'pharma'
    if n >= 103: return 'text'
    return 'unknown'

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

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

def is_gallows(word):
    onset = get_onset(word)
    return onset in GALLOWS_ONSETS

# Pass 1: classify folios
folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m: continue
        folio = m.group(1).lstrip('+*=&~')
        fb = folio_base(folio)
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            folio_word_stats[fb]['total'] += 1
            if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
            elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1

folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

# Pass 2: collect lines per folio
# folio_lines[fb] = list of (line_num, words)
folio_lines = defaultdict(list)

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m: continue
        folio = m.group(1).lstrip('+*=&~')
        line_num = int(m.group(2))
        locus_code = m.group(3)
        fb = folio_base(folio)
        dialect = folio_dialect.get(fb, 'unknown')
        if dialect not in ('A', 'B'): continue
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'): continue  # paragraph text only
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if len(words) < 2: continue
        folio_lines[fb].append((line_num, words, dialect))

# For each folio, classify lines as first/last/continuation
# Data structure: {section -> dialect -> {register -> [(LF_word, line_len)]}}

from collections import namedtuple
LineData = namedtuple('LineData', ['lf_word', 'n_words'])

section_register_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
# section_register_data[section][dialect][register] = list of LineData

for fb, lines_list in folio_lines.items():
    if not lines_list: continue
    dialect = lines_list[0][2]
    section = section_for_folio(fb)
    if section == 'unknown': continue

    line_nums = [ln for ln, _, _ in lines_list]
    min_ln = min(line_nums)
    max_ln = max(line_nums)

    for ln, words, d in lines_list:
        lf_word = words[0]
        n_words = len(words)
        if ln == min_ln:
            register = 'folio_first'
        elif ln == max_ln:
            register = 'folio_last'
        else:
            register = 'continuation'
        section_register_data[section][dialect][register].append(LineData(lf_word, n_words))

# Analysis
print("=" * 70)
print("A-DIALECT: THREE-REGISTER GRAMMAR BY SECTION")
print("=" * 70)

A_SECTIONS = ['herbal', 'astro', 'pharma', 'cosmo']

for section in A_SECTIONS:
    d_data = section_register_data[section].get('A', {})
    first_data = d_data.get('folio_first', [])
    cont_data = d_data.get('continuation', [])
    last_data = d_data.get('folio_last', [])

    n_first = len(first_data)
    n_cont = len(cont_data)
    n_last = len(last_data)

    g_first = sum(1 for ld in first_data if is_gallows(ld.lf_word))
    g_cont = sum(1 for ld in cont_data if is_gallows(ld.lf_word))
    g_last = sum(1 for ld in last_data if is_gallows(ld.lf_word))

    pct_first = 100 * g_first / n_first if n_first > 0 else 0
    pct_cont = 100 * g_cont / n_cont if n_cont > 0 else 0
    pct_last = 100 * g_last / n_last if n_last > 0 else 0

    e_first = (g_first / n_first) / (g_cont / n_cont) if n_cont > 0 and g_cont > 0 else float('inf')
    e_last = (g_last / n_last) / (g_cont / n_cont) if n_cont > 0 and g_cont > 0 else float('inf')

    len_first = sum(ld.n_words for ld in first_data) / n_first if n_first > 0 else 0
    len_cont = sum(ld.n_words for ld in cont_data) / n_cont if n_cont > 0 else 0
    len_last = sum(ld.n_words for ld in last_data) / n_last if n_last > 0 else 0

    print(f"\nSection: {section.upper()} (A-dialect)")
    print(f"  Folio-first LF: {g_first}/{n_first} = {pct_first:.1f}% gallows  E={e_first:.2f}×  mean_len={len_first:.2f}")
    print(f"  Continuation LF: {g_cont}/{n_cont} = {pct_cont:.1f}% gallows  (baseline)")
    print(f"  Folio-last LF:  {g_last}/{n_last} = {pct_last:.1f}% gallows  E={e_last:.2f}×  mean_len={len_last:.2f}")
    print(f"  Continuation mean_len: {len_cont:.2f}")

print("\n" + "=" * 70)
print("FULL SUMMARY TABLE: A-DIALECT vs B-DIALECT PER SECTION")
print("=" * 70)
print(f"\n{'Section':<12} {'Dialect':<8} {'First%':>8} {'Cont%':>8} {'Last%':>8} {'E_first':>8} {'E_last':>8} {'Len_last':>9} {'Len_cont':>9} {'N_first':>8}")

ALL_SECTIONS = ['herbal', 'astro', 'pharma', 'cosmo', 'bio', 'text']
for section in ALL_SECTIONS:
    for dialect in ['A', 'B']:
        d_data = section_register_data[section].get(dialect, {})
        first_data = d_data.get('folio_first', [])
        cont_data = d_data.get('continuation', [])
        last_data = d_data.get('folio_last', [])

        n_first = len(first_data)
        n_cont = len(cont_data)
        n_last = len(last_data)

        if n_first == 0 and n_cont == 0: continue

        g_first = sum(1 for ld in first_data if is_gallows(ld.lf_word))
        g_cont = sum(1 for ld in cont_data if is_gallows(ld.lf_word))
        g_last = sum(1 for ld in last_data if is_gallows(ld.lf_word))

        pct_first = 100 * g_first / n_first if n_first > 0 else 0
        pct_cont = 100 * g_cont / n_cont if n_cont > 0 else 0
        pct_last = 100 * g_last / n_last if n_last > 0 else 0

        e_first = (g_first / n_first) / (g_cont / n_cont) if n_cont > 0 and g_cont > 0 else float('inf')
        e_last = (g_last / n_last) / (g_cont / n_cont) if n_cont > 0 and g_cont > 0 else float('inf')

        len_last = sum(ld.n_words for ld in last_data) / n_last if n_last > 0 else 0
        len_cont = sum(ld.n_words for ld in cont_data) / n_cont if n_cont > 0 else 0

        e_first_s = f"{e_first:.2f}×" if e_first != float('inf') else "inf"
        e_last_s = f"{e_last:.2f}×" if e_last != float('inf') else "inf"

        print(f"  {section:<10} {dialect:<8} {pct_first:>7.1f}%  {pct_cont:>7.1f}%  {pct_last:>7.1f}%  {e_first_s:>8}  {e_last_s:>8}  {len_last:>8.2f}  {len_cont:>8.2f}  {n_first:>8}")

# Detailed A-dialect herbal folio-first LF words
print("\n" + "=" * 70)
print("A-DIALECT HERBAL: FOLIO-FIRST LF WORD DISTRIBUTION")
print("=" * 70)
herbal_a_first = section_register_data['herbal'].get('A', {}).get('folio_first', [])
herbal_a_cont = section_register_data['herbal'].get('A', {}).get('continuation', [])

if herbal_a_first:
    onset_c = Counter(get_onset(ld.lf_word) for ld in herbal_a_first)
    n = len(herbal_a_first)
    print(f"\nTop onsets at A-herbal folio-first LF (N={n}):")
    for onset, cnt in sorted(onset_c.items(), key=lambda x: -x[1]):
        pct = 100 * cnt / n
        if pct >= 2:
            print(f"  {onset:<8} {cnt:>4} ({pct:.1f}%)")

    word_c = Counter(ld.lf_word for ld in herbal_a_first)
    print(f"\nTop 20 words at A-herbal folio-first LF:")
    for w, cnt in word_c.most_common(20):
        onset = get_onset(w)
        g = '*' if is_gallows(w) else ''
        print(f"  {w:<20} {cnt:>3}  onset={onset}  {g}")

# A-dialect pharma folio-first LF words
print("\n" + "=" * 70)
print("A-DIALECT PHARMA: FOLIO-FIRST LF WORD DISTRIBUTION")
print("=" * 70)
pharma_a_first = section_register_data['pharma'].get('A', {}).get('folio_first', [])
if pharma_a_first:
    onset_c = Counter(get_onset(ld.lf_word) for ld in pharma_a_first)
    n = len(pharma_a_first)
    print(f"\nOnsets at A-pharma folio-first LF (N={n}):")
    for onset, cnt in sorted(onset_c.items(), key=lambda x: -x[1]):
        pct = 100 * cnt / n
        print(f"  {onset:<8} {cnt:>3} ({pct:.1f}%)")

    word_c = Counter(ld.lf_word for ld in pharma_a_first)
    print(f"\nAll words at A-pharma folio-first LF:")
    for w, cnt in word_c.most_common(20):
        onset = get_onset(w)
        g = '*gallows*' if is_gallows(w) else ''
        print(f"  {w:<20} {cnt:>3}  onset={onset}  {g}")

# A-dialect folio-last LF vocabulary
print("\n" + "=" * 70)
print("A-DIALECT: FOLIO-LAST LF WORD DISTRIBUTION BY SECTION")
print("=" * 70)
for section in A_SECTIONS:
    last_data = section_register_data[section].get('A', {}).get('folio_last', [])
    if not last_data: continue
    n = len(last_data)
    word_c = Counter(ld.lf_word for ld in last_data)
    onset_c = Counter(get_onset(ld.lf_word) for ld in last_data)
    print(f"\n  {section.upper()} folio-last LF (N={n}):")
    print(f"  Top onset classes:")
    for onset, cnt in sorted(onset_c.items(), key=lambda x: -x[1])[:5]:
        pct = 100*cnt/n
        print(f"    {onset:<8} {cnt:>3} ({pct:.1f}%)")
    print(f"  Top words: ", end='')
    print(', '.join(f"{w}({cnt})" for w, cnt in word_c.most_common(8)))

# Cross-dialect comparison: folio-last LF onset distribution
print("\n" + "=" * 70)
print("CROSS-DIALECT FOLIO-LAST LF: TOP ONSET CLASSES")
print("=" * 70)
for dialect in ['A', 'B']:
    all_last = []
    all_cont = []
    for section in ALL_SECTIONS:
        all_last.extend(section_register_data[section].get(dialect, {}).get('folio_last', []))
        all_cont.extend(section_register_data[section].get(dialect, {}).get('continuation', []))
    if not all_last: continue
    n_last = len(all_last)
    n_cont = len(all_cont)
    print(f"\n{dialect}-dialect folio-last LF (N={n_last}) top onset classes vs continuation (N={n_cont}):")
    onset_last = Counter(get_onset(ld.lf_word) for ld in all_last)
    onset_cont = Counter(get_onset(ld.lf_word) for ld in all_cont)
    rows = []
    for onset in sorted(set(list(onset_last.keys()) + list(onset_cont.keys()))):
        pl = onset_last.get(onset, 0) / n_last
        pc = onset_cont.get(onset, 0) / n_cont if n_cont > 0 else 0
        e = pl / pc if pc > 0 else float('inf')
        rows.append((onset, onset_last.get(onset,0), pl, onset_cont.get(onset,0), pc, e))
    rows.sort(key=lambda x: -x[5])
    print(f"  {'Onset':<8} {'N_last':>8} {'Last%':>8} {'N_cont':>8} {'Cont%':>8} {'E':>8}")
    for onset, nl, pl, nc, pc, e in rows:
        if pl > 0.01 or pc > 0.01:
            es = f"{e:.2f}×" if e != float('inf') else "inf"
            print(f"  {onset:<8} {nl:>8} {100*pl:>7.1f}%  {nc:>8} {100*pc:>7.1f}%  {es:>8}")
