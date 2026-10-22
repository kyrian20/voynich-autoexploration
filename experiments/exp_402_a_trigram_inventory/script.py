"""
exp_402: A Continuation Line Opening Trigram Inventory (H627)

Parallel to exp_401 but for A dialect.
Enumerate all (LF, pos1, pos2) trigrams in A continuation lines (>=3 words).
Report counts, E values for the top trigrams.
Characterize what fraction of lines are formula-typed (E_cond>=2.0) vs near-Markovian.
Compare A formula-typed fraction to B's 9.3% (exp_401/F405).
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

DATA_PATH = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt'))

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

# Pass 1: folio dialect classification
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
        locus_code = m.group(3).lstrip('+*=/~&')
        if not locus_code.lstrip('@').startswith('P'):
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

# Pass 2: collect lines
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
        line_num = int(m.group(2))
        locus_code = m.group(3).lstrip('+*=/~&')
        fb = folio_base(folio)
        dialect = folio_dialect.get(fb, 'A')
        if dialect != 'A':
            continue
        if not locus_code.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((line_num, words))

# Collect B continuation lines (not min or max line per folio, >=3 words)
b_cont_lines = []
for fb, line_list in folio_lines.items():
    if not line_list:
        continue
    lns = [l[0] for l in line_list]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in line_list:
        if ln == min_ln or ln == max_ln:
            continue
        if len(words) < 3:
            continue
        b_cont_lines.append(words)

total = len(b_cont_lines)
print(f"B continuation lines (>=3 words): {total}")

# Extract trigrams
trigrams = Counter()
lf_counts = Counter()
pos1_counts = Counter()
pos2_counts = Counter()
lf_pos1_counts = Counter()
lf_pos1_pos2_counts = Counter()
pos1_pos2_counts = Counter()
pos1_total = Counter()

for words in b_cont_lines:
    o0 = get_onset(words[0])
    o1 = get_onset(words[1])
    o2 = get_onset(words[2])
    trigrams[(o0, o1, o2)] += 1
    lf_counts[o0] += 1
    pos1_counts[o1] += 1
    pos2_counts[o2] += 1
    lf_pos1_counts[(o0, o1)] += 1
    lf_pos1_pos2_counts[(o0, o1, o2)] += 1
    pos1_pos2_counts[(o1, o2)] += 1
    pos1_total[o1] += 1

print(f"\nLF class distribution:")
for lf, n in lf_counts.most_common():
    e_baseline = (n / total) / (pos1_counts.get(lf, 0) / total) if pos1_counts.get(lf, 0) > 0 else float('nan')
    print(f"  {lf:<8} LF={n:>5} ({100*n/total:.1f}%)")

print(f"\npos1 class distribution:")
for p1, n in pos1_counts.most_common():
    print(f"  {p1:<8} pos1={n:>5} ({100*n/total:.1f}%)")

# Compute E values for all trigrams
print(f"\n--- Top 40 most frequent (LF, pos1, pos2) trigrams ---")
print(f"{'Trigram':<32} {'N':>5}  {'E_joint':>8}  {'E_cond':>8}")
print("-"*60)

e_cond_dict = {}
for (lf, p1, p2), n in trigrams.items():
    n_lf_p1 = lf_pos1_counts[(lf, p1)]
    n_p1 = pos1_total[p1]
    n_p1_p2 = pos1_pos2_counts[(p1, p2)]
    if n_lf_p1 > 0 and n_p1 > 0 and n_p1_p2 > 0:
        e_cond = (n / n_lf_p1) / (n_p1_p2 / n_p1)
        e_cond_dict[(lf, p1, p2)] = e_cond

for (lf, p1, p2), n in trigrams.most_common(40):
    pct = 100 * n / total
    p_lf = lf_counts[lf] / total
    p_p1 = pos1_counts[p1] / total
    p_p2 = pos2_counts[p2] / total
    e_joint = (n / total) / (p_lf * p_p1 * p_p2)
    e_cond = e_cond_dict.get((lf, p1, p2), float('nan'))
    print(f"{lf:>6}→{p1:>6}→{p2:<12} {n:>5}  {e_joint:>8.2f}×  {e_cond:>8.2f}×")

# Formula-typed classification
formula_thresh = 2.0
min_n = 3
formula_trigrams = {k for k, v in e_cond_dict.items() if v >= formula_thresh and trigrams[k] >= min_n}

formula_count = sum(1 for words in b_cont_lines
    if (get_onset(words[0]), get_onset(words[1]), get_onset(words[2])) in formula_trigrams)

print(f"\n--- Formula-type summary ---")
print(f"Formula-typed lines (E_cond>=2.0, N>=3): {formula_count} ({100*formula_count/total:.1f}%)")
print(f"Markovian/other lines: {total-formula_count} ({100*(total-formula_count)/total:.1f}%)")
print(f"Distinct formula trigrams: {len(formula_trigrams)}")

print(f"\n--- All formula-typed trigrams (E_cond>=2.0, N>=3), sorted by E ---")
formula_list = sorted([(k, trigrams[k], e_cond_dict[k]) for k in formula_trigrams], key=lambda x: -x[2])
for (lf, p1, p2), n, ec in formula_list:
    print(f"  {lf:>6}→{p1:>6}→{p2:<12} N={n:>4}  E={ec:.2f}×")

# Additional: LF×pos1 bigram E values (for reference)
print(f"\n--- Top 20 LF→pos1 bigrams by E ---")
lf_p1_e = {}
for (lf, p1), n in lf_pos1_counts.items():
    base_p1 = pos1_counts[p1] / total
    base_lf = lf_counts[lf] / total
    e = (n / total) / (base_lf * base_p1)
    lf_p1_e[(lf, p1)] = (n, e)
for (lf, p1), (n, e) in sorted(lf_p1_e.items(), key=lambda x: -x[1][1])[:20]:
    print(f"  {lf:>6}→{p1:<10} N={n:>4}  E={e:.2f}×")
