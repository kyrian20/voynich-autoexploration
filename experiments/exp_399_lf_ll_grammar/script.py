"""
exp_399: B LF→LL Grammar — Does LF Class Affect LL Beyond pre_LL Mediation? (H617)

For B (and A) continuation lines, compute (LF onset, LL onset) pairs.
Compare to unconditional LL distribution to find LF-conditional LL enrichments.
Also compute LF→pre_LL→LL trigram to distinguish direct vs pre_LL-mediated LF effects.
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

for d_target in ['A', 'B']:
    print(f"\n{'='*70}")
    print(f"DIALECT {d_target} — LF→LL grammar")
    print(f"{'='*70}")

    lf_ll = defaultdict(Counter)      # lf → ll distribution
    ll_baseline = Counter()            # unconditional ll
    lf_counts = Counter()              # how many lines with each LF
    # For pre_LL mediation test: (lf, pre_ll) → ll
    lf_prell_ll = defaultdict(Counter)  # (lf, pre_ll) → ll
    prell_ll_baseline = defaultdict(Counter)  # pre_ll → ll (any lf)

    for fb, lines_list in folio_lines.items():
        if not lines_list or lines_list[0][2] != d_target:
            continue
        line_nums = [ln for ln, _, _ in lines_list]
        min_ln, max_ln = min(line_nums), max(line_nums)
        for ln, words, _ in lines_list:
            if ln == min_ln or ln == max_ln:
                continue
            n = len(words)
            if n < 2:
                continue
            lf = get_onset(words[0])
            ll = get_onset(words[-1])
            lf_ll[lf][ll] += 1
            ll_baseline[ll] += 1
            lf_counts[lf] += 1

            if n >= 4:
                pre_ll = get_onset(words[-2])
                lf_prell_ll[(lf, pre_ll)][ll] += 1
                prell_ll_baseline[pre_ll][ll] += 1

    total_lines = sum(ll_baseline.values())
    top_ll = [ll for ll, _ in ll_baseline.most_common(8)]

    print(f"\nTotal continuation lines: {total_lines}")
    print(f"LL baseline: {dict(ll_baseline.most_common(6))}")
    print()

    # LF×LL matrix
    header = f"{'LF':>6} {'N':>5} | " + " | ".join(f"{p:>12}" for p in top_ll)
    print(header)
    print("-" * len(header))

    # Baseline row
    b_row = f"{'BASE':>6} {total_lines:>5} | "
    b_row += " | ".join(f"{100*ll_baseline.get(p,0)/total_lines:.1f}%(N={ll_baseline.get(p,0):>3})" for p in top_ll)
    print(b_row)
    print()

    for lf, n in sorted(lf_counts.items(), key=lambda x: -x[1]):
        if n < 10:
            continue
        row = f"{lf:>6} {n:>5} | "
        cols = []
        for p in top_ll:
            n_cond = lf_ll[lf].get(p, 0)
            p_cond = n_cond / n if n else 0
            p_base = ll_baseline.get(p, 0) / total_lines if total_lines else 0
            e = p_cond / p_base if p_base > 0 else float('nan')
            cols.append(f"{e:4.2f}×(N={n_cond:>3})")
        row += " | ".join(cols)
        print(row)

    # Most enriched (LF, LL) pairs
    print(f"\nTop enriched (LF, LL) pairs (N≥5):")
    enrichments = []
    for lf, ll_counts in lf_ll.items():
        n_lf = lf_counts[lf]
        for ll, n in ll_counts.items():
            p_cond = n / n_lf
            p_base = ll_baseline.get(ll, 0) / total_lines if total_lines else 0
            if p_base > 0 and n >= 5:
                e = p_cond / p_base
                enrichments.append((e, lf, ll, n, n_lf))
    enrichments.sort(reverse=True)
    print(f"{'LF':>6} {'LL':>6} {'E':>6} {'N':>5} {'LF_N':>6}")
    for e, lf, ll, n, n_lf in enrichments[:15]:
        print(f"{lf:>6} {ll:>6} {e:6.2f}× {n:>5} {n_lf:>6}")

    # Most depleted
    print(f"\nTop depleted (LF, LL) pairs (N≥5 expected):")
    depletions = [(e, lf, ll, n, n_lf) for e, lf, ll, n, n_lf in enrichments]
    depletions.sort()
    for e, lf, ll, n, n_lf in depletions[:10]:
        print(f"{lf:>6} {ll:>6} {e:6.2f}× {n:>5} {n_lf:>6}")
