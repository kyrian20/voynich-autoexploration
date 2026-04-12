"""
exp_395: B t→{pos1}→{pos2} Full Trigram Analysis (H609/H610)

t is LF-enriched in B (3.59×) with 205 LF tokens.
From exp_394: B t→sh=35 lines, t→ch=38 lines.
Q: What is the full t→pos1 distribution, and what does t produce at pos2 for each pos1?
Is there a third gallows formula type (t→{ch or sh}→pos2 distinct from p→sh→qot and y→sh→ch)?
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

# Main analysis
# For each dialect: when t at LF, collect pos1 distribution
# Then for each pos1 class, collect pos2 distribution

for d_target in ['A', 'B']:
    print(f"\n{'='*70}")
    print(f"DIALECT {d_target} — t at LF analysis")
    print(f"{'='*70}")

    t_lf_pos1 = Counter()      # pos1 when LF=t
    t_lf_p1_p2 = defaultdict(Counter)  # pos2 when LF=t, given pos1
    baseline_pos1 = Counter()  # all LF→pos1 transitions for baseline
    total_lf = 0

    # Also collect per-pos1 baseline pos2
    baseline_pos2_given_pos1 = defaultdict(Counter)

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
            if n < 2:
                continue
            lf_onset = get_onset(words[0])
            p1_onset = get_onset(words[1])
            total_lf += 1
            baseline_pos1[p1_onset] += 1

            if n >= 3:
                p2_onset = get_onset(words[2])
                baseline_pos2_given_pos1[p1_onset][p2_onset] += 1

            if lf_onset == 't':
                t_lf_pos1[p1_onset] += 1
                if n >= 3:
                    p2_onset = get_onset(words[2])
                    t_lf_p1_p2[p1_onset][p2_onset] += 1

    t_total = sum(t_lf_pos1.values())
    print(f"\n--- t→pos1 distribution (N={t_total} t-LF lines) ---")
    print(f"{'pos1':>8} {'N':>4} {'%t':>6} {'E':>6}")
    for p1, n in t_lf_pos1.most_common():
        pct_t = 100 * n / t_total if t_total else 0
        p_base = baseline_pos1.get(p1, 0) / total_lf if total_lf else 0
        e = (n / t_total) / p_base if p_base > 0 else float('nan')
        print(f"{p1:>8} {n:>4} {pct_t:>5.1f}% {e:>5.2f}×")

    # For top pos1 classes after t, show pos2 distribution
    print(f"\n--- t→pos1→pos2 trigram distributions ---")
    for p1, cnt in t_lf_pos1.most_common(8):
        if cnt < 3:
            continue
        p2_dist = t_lf_p1_p2[p1]
        p2_total = sum(p2_dist.values())
        if p2_total < 3:
            continue
        print(f"\n  t→{p1} (N={cnt}), pos2 distribution (N={p2_total}):")
        base_p2 = baseline_pos2_given_pos1[p1]
        base_p2_total = sum(base_p2.values())
        for p2, n2 in p2_dist.most_common(8):
            p_cond = n2 / p2_total
            p_base_p2 = base_p2.get(p2, 0) / base_p2_total if base_p2_total else 0
            e = p_cond / p_base_p2 if p_base_p2 > 0 else float('nan')
            print(f"    {p2:>8}: N={n2:>3}  E={e:.2f}×")

# Print actual t-LF lines in B for the most common pos1 classes
print(f"\n\n{'='*70}")
print("ACTUAL B t-LF lines (sample)")
print(f"{'='*70}")
sample_lines = []
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
        if len(words) < 3:
            continue
        lf_onset = get_onset(words[0])
        if lf_onset != 't':
            continue
        p1_onset = get_onset(words[1])
        sample_lines.append((p1_onset, fb, ln, words))

# Show 15 examples across pos1 classes
from itertools import groupby
sample_lines.sort(key=lambda x: x[0])
shown = 0
for p1, group in groupby(sample_lines, key=lambda x: x[0]):
    group = list(group)
    for _, fb, ln, words in group[:3]:
        onsets = ' '.join(get_onset(w) for w in words[:6])
        print(f"  {fb}/{ln}: {' '.join(words[:6])}")
        print(f"    onsets: {onsets}")
    shown += 1
    if shown >= 8:
        break
