"""
exp_394: Complete B sh-pos1 LF×pos2 Matrix (H611)

For all major LF classes in B continuation lines with sh at pos1,
compute the full pos2 onset distribution and E values vs sh-pos1 baseline.

Also includes: B ch-pos1 LF×pos2 matrix for comparison.

Target LF classes: y, p, d, s, t, qok, sh (self-chain), ol, r
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
    return re.sub(r'[rv]$', '', folio)

# Pass 1: dialect classification
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

# Pass 2: collect folio lines
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
        dialect = folio_dialect.get(fb, 'A')
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((line_num, words, dialect))

# Collect B continuation lines: LF → pos1 → pos2 trigrams
# Main: pos1=sh; secondary: pos1=ch (for comparison)
# lf_pos2_sh[lf_onset][pos2_onset] += 1 for lines with pos1=sh
# lf_pos2_ch[lf_onset][pos2_onset] += 1 for lines with pos1=ch

lf_pos2_sh = defaultdict(Counter)  # B sh-pos1 lines: LF→pos2
lf_pos2_ch = defaultdict(Counter)  # B ch-pos1 lines: LF→pos2
sh_baseline_pos2 = Counter()        # all B sh-pos1 lines pos2 (any LF)
ch_baseline_pos2 = Counter()        # all B ch-pos1 lines pos2 (any LF)
lf_baseline = Counter()             # all B cont lines LF onset
pos1_baseline = Counter()           # all B cont lines pos1 onset

for fb, lines_list in folio_lines.items():
    if not lines_list:
        continue
    d = lines_list[0][2]
    if d != 'B':
        continue
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln, max_ln = min(line_nums), max(line_nums)
    for ln, words, _ in lines_list:
        if ln == min_ln or ln == max_ln:
            continue
        n = len(words)
        if n < 2:
            continue
        lf_onset = get_onset(words[0])
        p1_onset = get_onset(words[1])
        lf_baseline[lf_onset] += 1
        pos1_baseline[p1_onset] += 1

        if n >= 3:
            p2_onset = get_onset(words[2])
            if p1_onset == 'sh':
                lf_pos2_sh[lf_onset][p2_onset] += 1
                sh_baseline_pos2[p2_onset] += 1
            if p1_onset == 'ch':
                lf_pos2_ch[lf_onset][p2_onset] += 1
                ch_baseline_pos2[p2_onset] += 1

# Display function
def show_matrix(title, lf_pos2_dict, baseline_pos2):
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}")

    # Get LF classes ordered by frequency
    lf_totals = {lf: sum(v.values()) for lf, v in lf_pos2_dict.items()}
    top_lf = sorted(lf_totals, key=lambda x: -lf_totals[x])

    total_baseline = sum(baseline_pos2.values())
    top_pos2 = [p2 for p2, _ in baseline_pos2.most_common(10)]

    # Header
    header = f"{'LF':>6} {'N':>4} | " + " | ".join(f"{p2:>14}" for p2 in top_pos2)
    print(header)
    print("-" * len(header))

    # Baseline row
    b_row = f"{'BASE':>6} {total_baseline:>4} | "
    cols = []
    for p2 in top_pos2:
        n = baseline_pos2.get(p2, 0)
        pct = 100 * n / total_baseline if total_baseline else 0
        cols.append(f"{pct:4.1f}%(N={n:>3})")
    b_row += " | ".join(cols)
    print(b_row)
    print()

    # Each LF class
    for lf in top_lf:
        if lf_totals[lf] < 3:
            continue
        row_total = lf_totals[lf]
        p_base = row_total / total_baseline if total_baseline else 0
        # Actually we want E = P(pos2=X | LF=lf, pos1=sh) / P(pos2=X | pos1=sh)
        row = f"{lf:>6} {row_total:>4} | "
        cols = []
        for p2 in top_pos2:
            n_cond = lf_pos2_dict[lf].get(p2, 0)
            p_cond = n_cond / row_total if row_total else 0
            p_base_p2 = baseline_pos2.get(p2, 0) / total_baseline if total_baseline else 0
            e = p_cond / p_base_p2 if p_base_p2 > 0 else float('nan')
            cols.append(f"{e:4.2f}×(N={n_cond:>2})")
        row += " | ".join(cols)
        print(row)

show_matrix("B CONT LINES: pos1=sh — Full LF×pos2 Matrix (E vs sh-pos1 baseline)",
            lf_pos2_sh, sh_baseline_pos2)

show_matrix("B CONT LINES: pos1=ch — Full LF×pos2 Matrix (E vs ch-pos1 baseline)",
            lf_pos2_ch, ch_baseline_pos2)

# Summary: most distinctive (LF,pos2) pairs for sh vs ch
print(f"\n\n{'='*80}")
print("SUMMARY: Top enriched (LF, pos2) pairs for B sh-pos1 lines")
print(f"{'='*80}")
total_sh = sum(sh_baseline_pos2.values())
enrichments = []
for lf, pos2_counts in lf_pos2_sh.items():
    row_total = sum(pos2_counts.values())
    if row_total < 5:
        continue
    for p2, n in pos2_counts.items():
        p_cond = n / row_total
        p_base = sh_baseline_pos2.get(p2, 0) / total_sh if total_sh else 0
        if p_base > 0:
            e = p_cond / p_base
            if n >= 3:
                enrichments.append((e, lf, p2, n, row_total))

enrichments.sort(reverse=True)
print(f"{'LF':>6} {'pos2':>6} {'E':>6} {'N':>4} {'LF_N':>6}")
for e, lf, p2, n, tot in enrichments[:20]:
    print(f"{lf:>6} {p2:>6} {e:6.2f}× {n:>4} {tot:>6}")

print(f"\nTop depleted (LF, pos2) pairs for B sh-pos1 lines:")
depletions = [(e, lf, p2, n, tot) for e, lf, p2, n, tot in enrichments if e < 0.5]
depletions.sort()
print(f"{'LF':>6} {'pos2':>6} {'E':>6} {'N':>4} {'LF_N':>6}")
for e, lf, p2, n, tot in depletions[:10]:
    print(f"{lf:>6} {p2:>6} {e:6.2f}× {n:>4} {tot:>6}")
