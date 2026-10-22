"""
exp_386: LF-Formula Class → pos1 Response Matrix (H600)

Computes the full LF→pos1 bigram matrix for both dialects.
Identifies which pos1 classes follow each LF-formula class.
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
    return re.sub(r'[rv]$', '', folio)

# Pass 1: dialect classification
folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
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
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            folio_word_stats[fb]['total'] += 1
            if w.endswith('eedy'):
                folio_word_stats[fb]['eedy'] += 1
            elif w.endswith('edy'):
                folio_word_stats[fb]['edy'] += 1

def classify_dialect(stats):
    total = stats['total']
    if total == 0:
        return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

# Pass 2: collect continuation lines
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
        locus_code = m.group(3)
        fb = folio_base(folio)
        dialect = folio_dialect.get(fb, 'unknown')
        if dialect not in ('A', 'B'):
            continue
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if len(words) < 1:
            continue
        folio_lines[fb].append((line_num, words, dialect))

def pos_category(idx, n):
    if idx == 0:
        return "LF"
    if idx == 1:
        return "pos1"
    if idx == n - 1:
        return "LL"
    if n >= 4 and idx == n - 2:
        return "pre_LL"
    return "MID_inner"

# Collect LF→pos1 bigrams
A_lf_bigrams = []
B_lf_bigrams = []

for fb, lines_list in folio_lines.items():
    if not lines_list:
        continue
    dialect = lines_list[0][2]
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln, max_ln = min(line_nums), max(line_nums)

    for ln, words, d in lines_list:
        if ln == min_ln or ln == max_ln:
            continue  # continuation lines only
        n = len(words)
        if n >= 2:
            pw = words[0]  # LF word
            nw = words[1]  # pos1 word
            if dialect == 'A':
                A_lf_bigrams.append((pw, nw))
            else:
                B_lf_bigrams.append((pw, nw))

print(f"A cont LF→pos1 pairs: {len(A_lf_bigrams)}")
print(f"B cont LF→pos1 pairs: {len(B_lf_bigrams)}")

# LF classes and pos1 classes
LF_CLASSES = ['d', 's', 'y', 'qot', 'qok', 'ok', 'ot', 'ch', 'sh', 'ol', 'r', 'cth', 'other']
POS1_CLASSES = ['ch', 'sh', 'd', 'qok', 'ok', 'ot', 'qot', 'ol', 'y', 's', 'r', 'cth', 'other']

for dialect, bigrams in [('A', A_lf_bigrams), ('B', B_lf_bigrams)]:
    print(f"\n{'='*85}")
    print(f"LF → POS1 BIGRAM MATRIX — {dialect}-DIALECT")
    print(f"{'='*85}")

    total = len(bigrams)
    # Baseline pos1 distribution
    pos1_all = Counter(get_onset(nw) for pw, nw in bigrams)
    lf_all = Counter(get_onset(pw) for pw, nw in bigrams)

    print(f"\nTotal LF→pos1 pairs: {total}")
    print(f"\npos1 baseline distribution:")
    for c in POS1_CLASSES:
        n = pos1_all.get(c, 0)
        print(f"  {c}: {n} ({n/total*100:.1f}%)")

    print(f"\nLF distribution:")
    for c in LF_CLASSES:
        n = lf_all.get(c, 0)
        print(f"  {c}: {n} ({n/total*100:.1f}%)")

    # Full matrix
    print(f"\n{'LF':<10} {'N':>5} | " + " ".join(f"{c:>6}" for c in POS1_CLASSES))
    print("-" * (17 + len(POS1_CLASSES) * 7))

    for lf_class in LF_CLASSES:
        lf_rows = [(pw, nw) for pw, nw in bigrams if get_onset(pw) == lf_class]
        n_lf = len(lf_rows)
        if n_lf == 0:
            print(f"{lf_class:<10} {n_lf:>5} | " + " ".join(f"{'---':>6}" for _ in POS1_CLASSES))
            continue

        pos1_counts = Counter(get_onset(nw) for pw, nw in lf_rows)
        cells = []
        for p1_class in POS1_CLASSES:
            n_hit = pos1_counts.get(p1_class, 0)
            n_base = pos1_all.get(p1_class, 0)
            if n_base == 0:
                cells.append(f"{'nan':>6}")
                continue
            p_cond = n_hit / n_lf
            p_base = n_base / total
            e = p_cond / p_base
            if e >= 2.0:
                cells.append(f"{'**'+f'{e:.1f}':>6}")
            elif e >= 1.5:
                cells.append(f"{'*'+f'{e:.1f}':>6}")
            elif e <= 0.3:
                cells.append(f"{'--'+f'{e:.1f}':>6}")
            elif n_hit == 0:
                cells.append(f"{'0':>6}")
            else:
                cells.append(f"{f'{e:.2f}':>6}")
        print(f"{lf_class:<10} {n_lf:>5} | " + " ".join(cells))

    # Focus: LF-formula classes (d, s, y) → pos1 distribution
    print(f"\n--- {dialect}: LF-Formula Classes → pos1 Detail ---")
    for lf_class in ['d', 's', 'y', 'qot', 'qok', 'ok']:
        lf_rows = [(pw, nw) for pw, nw in bigrams if get_onset(pw) == lf_class]
        n_lf = len(lf_rows)
        if n_lf < 5:
            print(f"\n{lf_class} at LF: N={n_lf} (too small)")
            continue
        pos1_counts = Counter(get_onset(nw) for pw, nw in lf_rows)
        print(f"\n{lf_class} at LF (N={n_lf}), top pos1 onset classes:")
        for p1_class in ['ch', 'sh', 'd', 'qok', 'ok', 'ot', 'qot', 'ol', 'y', 's']:
            n_hit = pos1_counts.get(p1_class, 0)
            n_base = pos1_all.get(p1_class, 0)
            if n_hit == 0 and n_base < 5:
                continue
            if n_base == 0:
                continue
            p_cond = n_hit / n_lf
            p_base = n_base / total
            e = p_cond / p_base
            print(f"  {p1_class}: {n_hit}/{n_lf} ({p_cond*100:.1f}%), baseline={p_base*100:.1f}%, E={e:.2f}×")

        # Top word pairs
        pair_counts = Counter((pw, nw) for pw, nw in lf_rows)
        top = pair_counts.most_common(5)
        print(f"  Top word pairs: {', '.join(f'{pw}→{nw}({c})' for (pw,nw),c in top)}")
