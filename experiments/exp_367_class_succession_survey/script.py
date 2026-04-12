"""
exp_367: Onset-Class Self-Succession Survey (H580)

H580: Is onset-class self-succession (X→X enrichment) a UNIVERSAL property of all
onset classes, or is it selective (only ok/qok/d)?

We know:
- ok→ok: A=1.93×, B=1.32× (F363)
- qok→qok: 1.32× both dialects (F326)
- d→d: A=1.61×, B=1.54× (F368)

Do ch/sh/ot/ol/s/y/k/t/p/f also show self-succession?

Also: compute the FULL 7×7 onset succession matrix for CONTINUATION LINES ONLY
(F326 was all lines; this isolates the continuation-line grammar).

And test: does the overall bigram structure change when restricted to continuation lines?
"""

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
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

# Pass 2: collect lines
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
        if not lc.lstrip('@').startswith('P'): continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if len(words) < 2: continue
        folio_lines[fb].append((line_num, words, dialect))

# Register classification
register_lines = defaultdict(lambda: defaultdict(list))
for fb, lines_list in folio_lines.items():
    if not lines_list: continue
    dialect = lines_list[0][2]
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln = min(line_nums)
    max_ln = max(line_nums)
    for ln, words, d in lines_list:
        if ln == min_ln: reg = 'opener'
        elif ln == max_ln: reg = 'closer'
        else: reg = 'cont'
        register_lines[dialect][reg].append(words)

print("="*70)
print("ONSET-CLASS SELF-SUCCESSION SURVEY (H580)")
print("All results from CONTINUATION LINES ONLY")
print("="*70)

# Onset classes to analyze (excluding rare ones)
MAIN_ONSETS = ['qok', 'qot', 'ch', 'sh', 'ok', 'ot', 'ol', 'd', 's', 'y', 'k', 't', 'p', 'f', 'other']

for DIALECT in ('A', 'B'):
    cont_lines = register_lines[DIALECT]['cont']
    print(f"\n{'='*60}")
    print(f"DIALECT {DIALECT}: N_cont_lines={len(cont_lines)}")
    print(f"{'='*60}")

    # Collect all adjacent pairs
    all_pairs = []
    for words in cont_lines:
        for i in range(len(words) - 1):
            all_pairs.append((get_onset(words[i]), get_onset(words[i+1])))

    total_pairs = len(all_pairs)

    # Marginal distributions
    first_counts = Counter(o1 for o1, o2 in all_pairs)
    second_counts = Counter(o2 for o1, o2 in all_pairs)

    # Pair counts
    pair_counts = Counter(all_pairs)

    print(f"Total adjacent pairs: {total_pairs}")
    print(f"\n--- Self-Succession E-values (X→X / baseline) ---")
    print(f"{'Onset':<8} {'N(X→X)':>8} {'N(X→any)':>10} {'P(X→X)%':>10} {'P(X)%_base':>12} {'E':>6} {'N(any→X)':>10}")
    print('-'*70)

    results = []
    for onset in MAIN_ONSETS:
        n_x_x = pair_counts[(onset, onset)]
        n_x_any = first_counts[onset]
        n_any_x = second_counts[onset]
        if n_x_any == 0: continue
        p_x_x = n_x_x / n_x_any  # P(next=X | prev=X)
        # Baseline: P(next=X) = n_any_x / total_pairs
        p_x_base = n_any_x / total_pairs
        E = p_x_x / p_x_base if p_x_base > 0 else float('nan')
        results.append((onset, n_x_x, n_x_any, p_x_x, p_x_base, E, n_any_x))
        print(f"{onset:<8} {n_x_x:>8} {n_x_any:>10} {p_x_x*100:>9.1f}% {p_x_base*100:>11.1f}% {E:>5.2f}×  {n_any_x:>8}")

    # Sort by E value descending
    results_sorted = sorted(results, key=lambda x: x[5], reverse=True)
    print(f"\n--- Ranked by E (self-succession enrichment) ---")
    print(f"{'Onset':<8} {'E':>6} {'P(X→X)':>9} {'baseline':>10} {'N':>6}")
    for onset, n_xx, n_xany, p_xx, p_base, E, n_anyx in results_sorted:
        print(f"{onset:<8} {E:>5.2f}×  {p_xx*100:>8.1f}%  {p_base*100:>9.1f}%  {n_xx:>6}")

    # Full bigram matrix (top onsets × top onsets)
    print(f"\n--- Full 8×8 Bigram Matrix (E values, continuation lines only) ---")
    TOP8 = ['d', 'ch', 'sh', 'qok', 'ok', 'ot', 'y', 'ol']
    print(f"{'prev\\next':<10}", end='')
    for o in TOP8:
        print(f"  {o:<6}", end='')
    print()
    print('-'*70)
    for o1 in TOP8:
        n_o1 = first_counts[o1]
        if n_o1 == 0: continue
        print(f"{o1:<10}", end='')
        for o2 in TOP8:
            n_o2 = second_counts[o2]
            n_o1_o2 = pair_counts[(o1, o2)]
            p_o1_o2 = n_o1_o2 / n_o1
            p_base = n_o2 / total_pairs
            E = p_o1_o2 / p_base if p_base > 0 else float('nan')
            print(f"  {E:4.2f}×", end='')
        print()

    # Cross-onset elevated pairs (E > 1.5×, N >= 5)
    print(f"\n--- {DIALECT}: Elevated cross-onset bigrams (E>1.5×, N≥5) ---")
    elevated = []
    for (o1, o2), cnt in pair_counts.items():
        if o1 == o2: continue  # Skip self-succession
        if cnt < 5: continue
        n_o1 = first_counts[o1]
        n_o2 = second_counts[o2]
        if n_o1 == 0: continue
        p_cond = cnt / n_o1
        p_base = n_o2 / total_pairs
        E = p_cond / p_base if p_base > 0 else 0
        if E > 1.5:
            elevated.append((o1, o2, cnt, p_cond, p_base, E))
    elevated.sort(key=lambda x: x[5], reverse=True)
    print(f"{'Onset→Onset':<16} {'N':>5} {'P(cond)':>9} {'baseline':>10} {'E':>6}")
    for o1, o2, cnt, p_cond, p_base, E in elevated[:20]:
        print(f"{o1}→{o2:<12} {cnt:>5} {p_cond*100:>8.1f}%  {p_base*100:>9.1f}%  {E:>5.2f}×")

    # Depleted cross-onset pairs (E < 0.5×, N >= 10)
    print(f"\n--- {DIALECT}: Depleted cross-onset bigrams (E<0.5×, N≥10) ---")
    depleted = []
    for (o1, o2), cnt in pair_counts.items():
        if o1 == o2: continue
        if cnt < 10: continue
        n_o1 = first_counts[o1]
        n_o2 = second_counts[o2]
        if n_o1 == 0: continue
        p_cond = cnt / n_o1
        p_base = n_o2 / total_pairs
        E = p_cond / p_base if p_base > 0 else 0
        if E < 0.5:
            depleted.append((o1, o2, cnt, p_cond, p_base, E))
    depleted.sort(key=lambda x: x[5])
    print(f"{'Onset→Onset':<16} {'N':>5} {'P(cond)':>9} {'baseline':>10} {'E':>6}")
    for o1, o2, cnt, p_cond, p_base, E in depleted[:20]:
        print(f"{o1}→{o2:<12} {cnt:>5} {p_cond*100:>8.1f}%  {p_base*100:>9.1f}%  {E:>5.2f}×")
