"""
exp_388: Cross-Dialectal LF-Enrichment Synthesis Table (H604)

Computes LF-enrichment E for all major onset classes in both A and B dialects.
Identifies which onset classes invert between A and B at LF position.
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

# Collect positional counts for each dialect
for dialect_target in ['A', 'B']:
    onset_pos_counts = defaultdict(Counter)
    total_pos_counts = Counter()

    for fb, lines_list in folio_lines.items():
        if not lines_list:
            continue
        dialect = lines_list[0][2]
        if dialect != dialect_target:
            continue
        line_nums = [ln for ln, _, _ in lines_list]
        min_ln, max_ln = min(line_nums), max(line_nums)
        for ln, words, d in lines_list:
            if ln == min_ln or ln == max_ln:
                continue
            n = len(words)
            for idx, w in enumerate(words):
                pos = pos_category(idx, n)
                onset = get_onset(w)
                onset_pos_counts[onset][pos] += 1
                total_pos_counts[pos] += 1

    total = sum(total_pos_counts.values())

    print(f"\n{'='*95}")
    print(f"FULL POSITIONAL ENRICHMENT TABLE — {dialect_target}-DIALECT (continuation lines)")
    print(f"{'='*95}")

    # All onset classes of interest
    CLASSES = ['d', 's', 'y', 'qot', 'qok', 'ok', 'ot', 'ch', 'sh', 'ol', 'r', 'cth', 'k', 't', 'p', 'f', 'l', 'other']
    POSITIONS = ['LF', 'pos1', 'MID_inner', 'pre_LL', 'LL']

    # Header
    print(f"\n{'Class':<8} {'Total':>7} {'%':>6} | " + " ".join(f"{'E_'+p:>10}" for p in POSITIONS))
    print("-" * (25 + len(POSITIONS) * 11))

    lf_enrichments = {}
    for onset in CLASSES:
        counts = onset_pos_counts[onset]
        n_total = sum(counts.values())
        if n_total == 0:
            continue
        p_overall = n_total / total

        row_cells = []
        for pos in POSITIONS:
            n_pos = counts.get(pos, 0)
            n_pos_total = total_pos_counts.get(pos, 0)
            if n_pos_total == 0:
                row_cells.append(f"{'nan':>10}")
                continue
            p_cond = n_pos / n_pos_total
            p_base = p_overall
            e = p_cond / p_base
            if e >= 2.0:
                row_cells.append(f"{'**'+f'{e:.2f}':>10}")
            elif e >= 1.5:
                row_cells.append(f"{'*'+f'{e:.2f}':>10}")
            elif e <= 0.3:
                row_cells.append(f"{'--'+f'{e:.2f}':>10}")
            elif e <= 0.6:
                row_cells.append(f"{'- '+f'{e:.2f}':>10}")
            else:
                row_cells.append(f"{f'{e:.2f}':>10}")

            if pos == 'LF':
                lf_enrichments[onset] = (e, n_pos, n_total)

        print(f"{onset:<8} {n_total:>7} {p_overall*100:>5.1f}% | " + " ".join(row_cells))

    # LF enrichment summary
    print(f"\n--- {dialect_target} LF Enrichment Ranking ---")
    sorted_lf = sorted(lf_enrichments.items(), key=lambda x: -x[1][0])
    for onset, (e, n_lf, n_total) in sorted_lf:
        flag = ">>LF" if e >= 1.5 else ("<<LF" if e <= 0.5 else "")
        print(f"  {onset:<8}: E={e:.2f}× (N_LF={n_lf}/{n_total}) {flag}")

# Cross-dialectal comparison
print(f"\n{'='*95}")
print(f"CROSS-DIALECTAL LF ENRICHMENT COMPARISON")
print(f"{'='*95}")

# Recompute for both dialects cleanly
lf_data = {}
for dialect_target in ['A', 'B']:
    onset_pos_counts = defaultdict(Counter)
    total_pos_counts = Counter()
    for fb, lines_list in folio_lines.items():
        if not lines_list:
            continue
        dialect = lines_list[0][2]
        if dialect != dialect_target:
            continue
        line_nums = [ln for ln, _, _ in lines_list]
        min_ln, max_ln = min(line_nums), max(line_nums)
        for ln, words, d in lines_list:
            if ln == min_ln or ln == max_ln:
                continue
            n = len(words)
            for idx, w in enumerate(words):
                pos = pos_category(idx, n)
                onset = get_onset(w)
                onset_pos_counts[onset][pos] += 1
                total_pos_counts[pos] += 1
    total = sum(total_pos_counts.values())
    n_lf_total = total_pos_counts.get('LF', 0)
    for onset in ['d', 's', 'y', 'qot', 'qok', 'ok', 'ot', 'ch', 'sh', 'ol', 'r', 'cth', 'k', 't', 'p', 'f']:
        n_total = sum(onset_pos_counts[onset].values())
        n_lf = onset_pos_counts[onset].get('LF', 0)
        if n_total == 0 or n_lf_total == 0:
            continue
        p_cond = n_lf / n_lf_total
        p_base = n_total / total
        e = p_cond / p_base
        lf_data.setdefault(onset, {})[dialect_target] = (e, n_lf, n_total)

CLASSES_CMP = ['d', 's', 'y', 'qot', 'qok', 'ok', 'ot', 'ch', 'sh', 'ol', 'r', 'cth', 'k', 't', 'p', 'f']
print(f"\n{'Class':<8} {'A_LF_E':>8} {'B_LF_E':>8} | {'Direction':>12} | {'Note'}")
print("-" * 70)
for onset in CLASSES_CMP:
    a_data = lf_data.get(onset, {}).get('A')
    b_data = lf_data.get(onset, {}).get('B')
    if a_data is None or b_data is None:
        continue
    a_e, a_n, a_tot = a_data
    b_e, b_n, b_tot = b_data

    if a_e >= 1.3 and b_e >= 1.3:
        direction = "INVARIANT_LF+"
    elif a_e <= 0.7 and b_e <= 0.7:
        direction = "INVARIANT_LF-"
    elif a_e >= 1.3 and b_e <= 0.7:
        direction = "A>B INVERSION"
    elif a_e <= 0.7 and b_e >= 1.3:
        direction = "B>A INVERSION"
    else:
        direction = "mixed/moderate"

    print(f"{onset:<8} {a_e:>8.2f}× {b_e:>8.2f}× | {direction:>12} | A_N={a_n}/{a_tot} B_N={b_n}/{b_tot}")

