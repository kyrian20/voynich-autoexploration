"""
exp_343: Folio-Opener Formula Words — What Appears at LF of Folio-First Lines?

Background:
- F344 (exp_342): B-dialect daiin AVOIDS folio-first lines (0/73=0%). daiin is a
  continuation-line LF formula only.
- exp_342 inline analysis suggested folio-first lines use p-onset/t-onset (gallows
  compound) words in B-dialect and p/k/ch/sh-onset words in A-dialect.
- This experiment formally characterizes the folio-opener LF formula words for
  both dialects and compares the onset distributions.

Plan:
1. Classify folios as A/B dialect via edy/eedy rate
2. For each folio, identify first-line LF word (folio-opener) vs continuation LF words
3. Build onset-class frequency tables for both categories, both dialects
4. Compare: what fraction of folio-opener LF words have p/t/k/gallows onsets?
"""

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = [
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o')
]

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

def get_onset(word):
    for label, prefix in ONSET_ORDER:
        if word.startswith(prefix):
            return label
    return 'other'

def onset_class(onset):
    """Map specific onset to broad class."""
    if onset in ('qok','qot'): return 'qok-class'
    if onset == 'qo': return 'qo'
    if onset == 'cth': return 'cth'
    if onset in ('ch',): return 'ch'
    if onset in ('sh',): return 'sh'
    if onset in ('ok',): return 'ok'
    if onset in ('ot',): return 'ot'
    if onset in ('ol',): return 'ol'
    if onset in ('d',): return 'd'
    if onset in ('s',): return 's'
    if onset in ('y',): return 'y'
    if onset in ('k',): return 'k'
    if onset in ('t',): return 't'
    if onset in ('l',): return 'l'
    if onset in ('r',): return 'r'
    if onset in ('p',): return 'p'
    if onset in ('f',): return 'f'
    if onset in ('o',): return 'o'
    return 'other'

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

# Pass 2: collect lines per folio with positional info
# Track which line number within each folio each line is
folio_lines = defaultdict(list)  # fb -> list of (line_num, words, locus_code)

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m: continue
        folio = m.group(1)
        line_num = int(m.group(2))
        locus_code = m.group(3)
        folio = folio.lstrip('+*=&~')
        fb = folio_base(folio)
        dialect = folio_dialect.get(fb, 'unknown')
        if dialect not in ('A', 'B'): continue
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'): continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if len(words) < 2: continue
        folio_lines[fb].append((line_num, words, dialect))

# For each folio, find minimum line_num = folio-first line
folio_first_lf = {}   # fb -> LF word of first line
folio_cont_lf = []    # list of (word, dialect)

folio_first_words = {}  # fb -> (LF_word, dialect)

for fb, lines_list in folio_lines.items():
    if not lines_list: continue
    dialect = lines_list[0][2]
    min_line = min(ln for ln, _, _ in lines_list)
    first_lines = [(ln, words) for ln, words, _ in lines_list if ln == min_line]
    cont_lines = [(ln, words) for ln, words, _ in lines_list if ln != min_line]
    # LF word = first word of the line
    for ln, words in first_lines:
        lf_word = words[0]
        folio_first_words[fb] = (lf_word, dialect)
    for ln, words in cont_lines:
        lf_word = words[0]
        folio_cont_lf.append((lf_word, dialect))

# Analyze
for dialect in ['B', 'A']:
    print(f"\n{'='*60}")
    print(f"{dialect}-DIALECT FOLIO-FIRST LINE LF WORDS")
    print(f"{'='*60}")
    first_lf_words = [w for fb, (w, d) in folio_first_words.items() if d == dialect]
    cont_lf_words = [w for w, d in folio_cont_lf if d == dialect]

    n_first = len(first_lf_words)
    n_cont = len(cont_lf_words)
    print(f"Folio-first LF tokens: {n_first}")
    print(f"Continuation LF tokens: {n_cont}")

    # Top 20 folio-first LF words
    first_c = Counter(first_lf_words)
    print(f"\nTop 20 folio-FIRST LF words:")
    for w, cnt in first_c.most_common(20):
        pct = 100*cnt/n_first
        onset = get_onset(w)
        print(f"  {w:<20} {cnt:>4} ({pct:.1f}%)  onset={onset}")

    # Onset-class distribution for folio-first LF
    first_onset_c = Counter(onset_class(get_onset(w)) for w in first_lf_words)
    cont_onset_c = Counter(onset_class(get_onset(w)) for w in cont_lf_words)

    print(f"\nOnset-class distribution (folio-first vs continuation LF):")
    print(f"{'Onset':<15} {'First%':>8} {'Cont%':>8} {'E(First/Cont)':>14}")
    all_classes = sorted(set(list(first_onset_c.keys()) + list(cont_onset_c.keys())))
    for oc in all_classes:
        fp = first_onset_c.get(oc, 0) / n_first if n_first > 0 else 0
        cp = cont_onset_c.get(oc, 0) / n_cont if n_cont > 0 else 0
        enr = fp / cp if cp > 0 else float('inf')
        if fp > 0.005 or cp > 0.005:
            print(f"  {oc:<13} {100*fp:>7.1f}%  {100*cp:>7.1f}%  {enr:>12.2f}×")

    # Top 20 continuation LF words
    cont_c = Counter(cont_lf_words)
    print(f"\nTop 20 continuation LF words:")
    for w, cnt in cont_c.most_common(20):
        pct = 100*cnt/n_cont
        onset = get_onset(w)
        print(f"  {w:<20} {cnt:>4} ({pct:.1f}%)  onset={onset}")

# Gallows-compound analysis: how many folio-first LF words start with p/t/k/f?
print(f"\n{'='*60}")
print("GALLOWS-BEARING ONSET FRACTION (p/t/k/f) IN FOLIO-FIRST LF")
print(f"{'='*60}")
gallows_onsets = {'p','t','k','f'}
for dialect in ['B','A']:
    first_lf_words = [w for fb, (w, d) in folio_first_words.items() if d == dialect]
    cont_lf_words = [w for w, d in folio_cont_lf if d == dialect]
    n_first = len(first_lf_words)
    n_cont = len(cont_lf_words)
    g_first = sum(1 for w in first_lf_words if get_onset(w) in gallows_onsets)
    g_cont = sum(1 for w in cont_lf_words if get_onset(w) in gallows_onsets)
    p_first = g_first/n_first if n_first > 0 else 0
    p_cont = g_cont/n_cont if n_cont > 0 else 0
    enr = p_first/p_cont if p_cont > 0 else float('inf')
    print(f"  {dialect}: first={g_first}/{n_first} ({100*p_first:.1f}%)  cont={g_cont}/{n_cont} ({100*p_cont:.1f}%)  E={enr:.2f}×")

# What are unique folio-first LF onsets (not seen in cont top-20)?
print(f"\n{'='*60}")
print("FOLIO-FIRST LF ONSET ENRICHMENT DETAIL")
print(f"{'='*60}")
for dialect in ['B','A']:
    first_lf_words = [w for fb, (w, d) in folio_first_words.items() if d == dialect]
    cont_lf_words = [w for w, d in folio_cont_lf if d == dialect]
    n_first = len(first_lf_words)
    n_cont = len(cont_lf_words)
    # All onsets in folio-first with enrichment vs cont
    first_onset = Counter(get_onset(w) for w in first_lf_words)
    cont_onset = Counter(get_onset(w) for w in cont_lf_words)
    print(f"\n{dialect}-dialect: folio-first LF onset enrichment vs continuation:")
    rows = []
    for onset in sorted(set(list(first_onset.keys()) + list(cont_onset.keys()))):
        fp = first_onset.get(onset,0)/n_first if n_first > 0 else 0
        cp = cont_onset.get(onset,0)/n_cont if n_cont > 0 else 0
        enr = fp/cp if cp > 0 else float('inf') if fp > 0 else 1.0
        rows.append((onset, first_onset.get(onset,0), fp, cont_onset.get(onset,0), cp, enr))
    rows.sort(key=lambda x: -x[5])
    print(f"  {'Onset':<8} {'N_first':>8} {'First%':>8} {'N_cont':>8} {'Cont%':>8} {'E':>8}")
    for onset, nf, fp, nc, cp, enr in rows:
        if fp > 0.01 or cp > 0.01:
            enr_s = f"{enr:.2f}×" if enr != float('inf') else "inf"
            print(f"  {onset:<8} {nf:>8} {100*fp:>7.1f}%  {nc:>8} {100*cp:>7.1f}%  {enr_s:>8}")
