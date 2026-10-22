"""
exp_396: A dialect sh-pos1 LF×pos2 Matrix (H616)

Analogous to exp_394 but for A-dialect.
Q: Does A dialect sh-pos1 grammar have the same five formula-typed LF grammar types as B?
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

# Main: collect A (and B for comparison) sh-pos1 LF×pos2 and ch-pos1 LF×pos2
for d_target in ['A', 'B']:
    lf_pos2_sh = defaultdict(Counter)
    sh_baseline_pos2 = Counter()
    lf_pos2_ch = defaultdict(Counter)
    ch_baseline_pos2 = Counter()

    for fb, lines_list in folio_lines.items():
        if not lines_list:
            continue
        d = lines_list[0][2]
        if d != d_target:
            continue
        line_nums = [ln for ln, _, _ in lines_list]
        min_ln, max_ln = min(line_nums), max(line_nums)
        for ln, words, _ in lines_list:
            if ln == min_ln or ln == max_ln:
                continue
            n = len(words)
            if n < 3:
                continue
            lf_onset = get_onset(words[0])
            p1_onset = get_onset(words[1])
            p2_onset = get_onset(words[2])
            if p1_onset == 'sh':
                lf_pos2_sh[lf_onset][p2_onset] += 1
                sh_baseline_pos2[p2_onset] += 1
            if p1_onset == 'ch':
                lf_pos2_ch[lf_onset][p2_onset] += 1
                ch_baseline_pos2[p2_onset] += 1

    print(f"\n{'='*80}")
    print(f"DIALECT {d_target}: sh-pos1 LF×pos2 matrix")
    print(f"{'='*80}")

    total_sh = sum(sh_baseline_pos2.values())
    top_pos2_sh = [p for p, _ in sh_baseline_pos2.most_common(9)]
    lf_totals_sh = {lf: sum(v.values()) for lf, v in lf_pos2_sh.items()}
    top_lf_sh = sorted(lf_totals_sh, key=lambda x: -lf_totals_sh[x])

    header = f"{'LF':>6} {'N':>4} | " + " | ".join(f"{p:>13}" for p in top_pos2_sh)
    print(f"Total sh-pos1 lines (with pos2): {total_sh}")
    print(f"Top pos2 distribution: {dict(sh_baseline_pos2.most_common(5))}")
    print()
    print(header)
    print("-" * len(header))
    # Baseline
    b_row = f"{'BASE':>6} {total_sh:>4} | "
    b_row += " | ".join(f"{100*sh_baseline_pos2.get(p,0)/total_sh:.1f}%(N={sh_baseline_pos2.get(p,0):>3})" for p in top_pos2_sh)
    print(b_row)
    print()
    for lf in top_lf_sh:
        n = lf_totals_sh[lf]
        if n < 3:
            continue
        row = f"{lf:>6} {n:>4} | "
        cols = []
        for p2 in top_pos2_sh:
            n_cond = lf_pos2_sh[lf].get(p2, 0)
            p_cond = n_cond / n if n else 0
            p_base = sh_baseline_pos2.get(p2, 0) / total_sh if total_sh else 0
            e = p_cond / p_base if p_base > 0 else float('nan')
            cols.append(f"{e:4.2f}×(N={n_cond:>2})")
        row += " | ".join(cols)
        print(row)

    # Top enriched pairs
    print(f"\nTop enriched (LF,pos2) pairs for {d_target} sh-pos1 lines (N≥3):")
    enrichments = []
    for lf, pos2_counts in lf_pos2_sh.items():
        row_total = sum(pos2_counts.values())
        if row_total < 5:
            continue
        for p2, n in pos2_counts.items():
            p_cond = n / row_total
            p_base = sh_baseline_pos2.get(p2, 0) / total_sh if total_sh else 0
            if p_base > 0 and n >= 3:
                e = p_cond / p_base
                enrichments.append((e, lf, p2, n, row_total))
    enrichments.sort(reverse=True)
    print(f"{'LF':>6} {'pos2':>6} {'E':>6} {'N':>4} {'LF_N':>6}")
    for e, lf, p2, n, tot in enrichments[:15]:
        print(f"{lf:>6} {p2:>6} {e:6.2f}× {n:>4} {tot:>6}")
