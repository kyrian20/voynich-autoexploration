"""
exp_354: Folio-Closer Vocabulary — What Specific Words Appear at Folio-Last LF?
(H558 + H560)

Background:
- F351: B-dialect folio-last LF: l(3.87×), ol(3.38×), ot(3.94×) enriched
- exp_353: A-dialect folio-last LF: y(1.60×), s(2.14×), ch(1.79×) enriched
- A folio-closer top word: ycheor(3); A folio-last LL: sh-enriched (B: E=3.45×)
- Open: what are the specific B-dialect folio-last LF words? Is there a formula word?
- Also: what appears at folio-last LL in A-dialect? Is it different from continuation LL?

Plan:
1. Classify folios, collect folio-first/last/continuation line data
2. Compute B folio-last LF: top words, onset classes with enrichment
3. Compute A folio-last LF: full word list
4. Compute both dialects folio-last LL: top words vs continuation LL
5. Compute folio-last line word-by-word position profiles (LF, word 1, word 2, ..., LL)
   to understand the folio-closer as a 4-5 word sequence
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

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
    return get_onset(word) in ('k', 't', 'p', 'f')

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

# Pass 2: collect full line data (all words per line)
# Data structure: (fb, dialect, line_num, words)
all_line_data = []

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
        if not lc.lstrip('@').startswith('P'): continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if len(words) < 2: continue
        all_line_data.append((fb, dialect, line_num, words))

# Group by folio, classify lines
folio_to_lines = defaultdict(list)
for fb, dialect, line_num, words in all_line_data:
    folio_to_lines[fb].append((line_num, words, dialect))

# Collect folio-last and continuation words
folio_last_lf = defaultdict(list)    # dialect -> list of lf_word
folio_last_ll = defaultdict(list)    # dialect -> list of ll_word
folio_last_full = defaultdict(list)  # dialect -> list of word lists (full line)
cont_lf = defaultdict(list)
cont_ll = defaultdict(list)
folio_first_lf = defaultdict(list)

for fb, lines_list in folio_to_lines.items():
    if not lines_list: continue
    dialect = lines_list[0][2]
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln = min(line_nums)
    max_ln = max(line_nums)

    for ln, words, d in lines_list:
        lf = words[0]
        ll = words[-1]
        if ln == min_ln:
            folio_first_lf[dialect].append(lf)
        elif ln == max_ln:
            folio_last_lf[dialect].append(lf)
            folio_last_ll[dialect].append(ll)
            folio_last_full[dialect].append(words)
        else:
            cont_lf[dialect].append(lf)
            cont_ll[dialect].append(ll)

# Analysis
print("=" * 70)
print("B-DIALECT: FOLIO-LAST LF WORD VOCABULARY")
print("=" * 70)

for dialect in ['B', 'A']:
    last_lf_words = folio_last_lf[dialect]
    cont_lf_words = cont_lf[dialect]
    n_last = len(last_lf_words)
    n_cont = len(cont_lf_words)
    print(f"\n{dialect}-dialect folio-last LF (N={n_last}):")

    # Top 25 words with onset
    word_c = Counter(last_lf_words)
    print(f"  Top 25 words at folio-last LF:")
    for w, cnt in word_c.most_common(25):
        pct = 100*cnt/n_last
        onset = get_onset(w)
        g = '[gallows]' if is_gallows(w) else ''
        print(f"    {w:<22} {cnt:>3} ({pct:.1f}%)  onset={onset}  {g}")

    # Hapax rate
    hapax = sum(1 for w, cnt in word_c.items() if cnt == 1)
    print(f"\n  Hapax rate at folio-last LF: {hapax}/{len(word_c)} types = {100*hapax/len(word_c):.1f}% of types")
    print(f"  Hapax tokens: {hapax}/{n_last} = {100*hapax/n_last:.1f}% of tokens")

    # Onset enrichment vs continuation LF
    onset_last = Counter(get_onset(w) for w in last_lf_words)
    onset_cont = Counter(get_onset(w) for w in cont_lf_words)
    print(f"\n  Onset enrichment vs continuation LF:")
    rows = []
    for onset in sorted(set(list(onset_last.keys()) + list(onset_cont.keys()))):
        pl = onset_last.get(onset,0)/n_last
        pc = onset_cont.get(onset,0)/n_cont if n_cont > 0 else 0
        e = pl/pc if pc > 0 else (float('inf') if pl > 0 else 1.0)
        rows.append((onset, onset_last.get(onset,0), pl, onset_cont.get(onset,0), pc, e))
    rows.sort(key=lambda x: -x[5])
    for onset, nl, pl, nc, pc, e in rows:
        if pl > 0.01 or pc > 0.01:
            es = f"{e:.2f}×"
            print(f"    {onset:<8} {nl:>4}/{n_last:<4} {100*pl:>6.1f}%  vs  {nc:>5}/{n_cont:<5} {100*pc:>6.1f}%  E={es}")

print("\n" + "=" * 70)
print("FOLIO-LAST LL: WHAT APPEARS AT THE END OF THE FOLIO-CLOSER LINE?")
print("=" * 70)

for dialect in ['B', 'A']:
    last_ll_words = folio_last_ll[dialect]
    cont_ll_words = cont_ll[dialect]
    n_last = len(last_ll_words)
    n_cont = len(cont_ll_words)
    print(f"\n{dialect}-dialect folio-last LL (N={n_last}):")

    word_c = Counter(last_ll_words)
    print(f"  Top 20 words at folio-last LL:")
    for w, cnt in word_c.most_common(20):
        pct = 100*cnt/n_last
        onset = get_onset(w)
        print(f"    {w:<22} {cnt:>3} ({pct:.1f}%)  onset={onset}")

    # Onset enrichment vs continuation LL
    onset_last = Counter(get_onset(w) for w in last_ll_words)
    onset_cont = Counter(get_onset(w) for w in cont_ll_words)
    print(f"\n  Onset enrichment at folio-last LL vs continuation LL:")
    rows = []
    for onset in sorted(set(list(onset_last.keys()) + list(onset_cont.keys()))):
        pl = onset_last.get(onset,0)/n_last
        pc = onset_cont.get(onset,0)/n_cont if n_cont > 0 else 0
        e = pl/pc if pc > 0 else (float('inf') if pl > 0 else 1.0)
        rows.append((onset, onset_last.get(onset,0), pl, onset_cont.get(onset,0), pc, e))
    rows.sort(key=lambda x: -x[5])
    for onset, nl, pl, nc, pc, e in rows:
        if pl > 0.01 or pc > 0.01:
            es = f"{e:.2f}×"
            print(f"    {onset:<8} {nl:>4}/{n_last:<4} {100*pl:>6.1f}%  vs  {nc:>5}/{n_cont:<5} {100*pc:>6.1f}%  E={es}")

print("\n" + "=" * 70)
print("FOLIO-CLOSER LINE STRUCTURE: POSITIONAL WORD PROFILE")
print("=" * 70)

# For each dialect, look at the distribution of words by position within folio-last lines
# Position 0=LF, 1=word1, 2=word2, ..., last=LL
for dialect in ['B', 'A']:
    last_lines = folio_last_full[dialect]
    if not last_lines: continue

    print(f"\n{dialect}-dialect folio-closer word onset by position (0=LF, last=LL):")

    # Collect by position
    pos_data = defaultdict(list)
    for line_words in last_lines:
        n = len(line_words)
        for i, w in enumerate(line_words):
            if i == 0:
                pos_data['LF'].append(w)
            elif i == n - 1:
                pos_data['LL'].append(w)
            elif i == 1:
                pos_data['pos1'].append(w)
            elif i == 2:
                pos_data['pos2'].append(w)
            else:
                pos_data['MID_rest'].append(w)

    print(f"  {'Position':<12} {'N':>6} {'gallows%':>10} {'top_onset':>12}")
    for pos in ['LF', 'pos1', 'pos2', 'MID_rest', 'LL']:
        words = pos_data[pos]
        if not words: continue
        n = len(words)
        onset_c = Counter(get_onset(w) for w in words)
        g_pct = 100 * sum(1 for w in words if is_gallows(w)) / n
        top = onset_c.most_common(1)[0][0] if onset_c else '?'
        top_pct = 100 * onset_c.most_common(1)[0][1] / n if onset_c else 0
        print(f"  {pos:<12} {n:>6} {g_pct:>9.1f}%  {top}={top_pct:.0f}%")

    # Look at folio-closer LF→LL bigram (what onset follows the LF word?)
    print(f"\n  {dialect}-dialect folio-closer LF→pos1 onset bigram:")
    lf_pos1_pairs = []
    for line_words in last_lines:
        if len(line_words) >= 2:
            lf_pos1_pairs.append((get_onset(line_words[0]), get_onset(line_words[1])))
    lf_onset_c = Counter(o1 for o1, o2 in lf_pos1_pairs)
    p1_onset_c = Counter(o2 for o1, o2 in lf_pos1_pairs)
    bigram_c = Counter(lf_pos1_pairs)
    n_pairs = len(lf_pos1_pairs)
    print(f"  Top LF onsets: " + ", ".join(f"{o}={100*cnt/len(lf_pos1_pairs):.0f}%" for o, cnt in lf_onset_c.most_common(5)))
    print(f"  Top pos1 onsets: " + ", ".join(f"{o}={100*cnt/len(lf_pos1_pairs):.0f}%" for o, cnt in p1_onset_c.most_common(5)))

print("\n" + "=" * 70)
print("B-DIALECT: FOLIO-LAST LF l/ol/ot WORDS (THE FOLIO-CLOSER FORMULA)")
print("=" * 70)

b_last_lf = folio_last_lf['B']
b_lol_ot_words = [w for w in b_last_lf if get_onset(w) in ('l', 'ol', 'ot')]
b_lol_ot_c = Counter(b_lol_ot_words)
n_b_last = len(b_last_lf)
print(f"\nB folio-last LF words with l/ol/ot onset (N={len(b_lol_ot_words)}/{n_b_last} = {100*len(b_lol_ot_words)/n_b_last:.1f}%):")
for w, cnt in b_lol_ot_c.most_common(20):
    onset = get_onset(w)
    print(f"  {w:<22} {cnt:>3}  onset={onset}")

print("\n" + "=" * 70)
print("A-DIALECT: FOLIO-LAST LF y/s/ch WORDS (THE A-DIALECT FORMULA)")
print("=" * 70)

a_last_lf = folio_last_lf['A']
a_formula_words = [w for w in a_last_lf if get_onset(w) in ('y', 's', 'ch')]
a_formula_c = Counter(a_formula_words)
n_a_last = len(a_last_lf)
print(f"\nA folio-last LF words with y/s/ch onset (N={len(a_formula_words)}/{n_a_last} = {100*len(a_formula_words)/n_a_last:.1f}%):")
for w, cnt in a_formula_c.most_common(20):
    onset = get_onset(w)
    print(f"  {w:<22} {cnt:>3}  onset={onset}")

# Cross-check: compare folio-last LF vs folio-first LF hapax rates
print("\n" + "=" * 70)
print("HAPAX RATES COMPARISON: FOLIO-FIRST vs FOLIO-LAST vs CONTINUATION LF")
print("=" * 70)
for dialect in ['B', 'A']:
    first_words = folio_first_lf[dialect]
    last_words = folio_last_lf[dialect]
    cont_words = cont_lf[dialect]

    for label, words in [('folio-first LF', first_words), ('folio-last LF', last_words), ('continuation LF', cont_words)]:
        n = len(words)
        types = len(set(words))
        hapax = sum(1 for w, cnt in Counter(words).items() if cnt == 1)
        hapax_tok = hapax
        print(f"  {dialect}-{label}: N={n}, types={types}, hapax_types={hapax}, hapax_tok_pct={100*hapax_tok/n:.1f}%")
