"""
exp_393: k-Onset Positional Census in Continuation vs Folio-Opener Lines (H606)

Hypothesis H606: k is not LF-enriched in continuation lines (F392: A=0.80×/B=0.65×)
despite being a folio-opener LF gallows class (F345: 67-70% gallows at folio-first).
Q: Where does k concentrate in continuation lines vs folio-opener lines?

Compare k vs p/t/f positional distributions in continuation vs opener lines.
"""

import os, re
from collections import defaultdict, Counter

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

def pos_category(idx, n):
    if n == 1:
        return 'LL'
    if idx == 0:
        return 'LF'
    if idx == n - 1:
        return 'LL'
    if n >= 4 and idx == n - 2:
        return 'pre_LL'
    if idx == 1:
        return 'pos1'
    return 'MID'

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

# Accumulate positional counts by dialect and line type
TARGET = ['k', 'p', 't', 'f']
POSITIONS = ['LF', 'pos1', 'MID', 'pre_LL', 'LL']

# counts[dialect][line_type][pos][onset]
counts = defaultdict(lambda: defaultdict(lambda: defaultdict(Counter)))
totals = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

for fb, lines_list in folio_lines.items():
    if not lines_list:
        continue
    d = lines_list[0][2]
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln, max_ln = min(line_nums), max(line_nums)
    if min_ln == max_ln:
        continue

    for ln, words, _ in lines_list:
        n = len(words)
        if ln == min_ln:
            lt = 'opener'
        elif ln == max_ln:
            lt = 'closer'
        else:
            lt = 'cont'

        for idx, w in enumerate(words):
            pos = pos_category(idx, n)
            onset = get_onset(w)
            counts[d][lt][pos][onset] += 1
            totals[d][lt][pos] += 1

# Compute E for each onset×position×dialect×line_type
def compute_table(d, lt):
    grand_total = sum(totals[d][lt][p] for p in POSITIONS)
    if grand_total == 0:
        return
    print(f"\nDialect {d} | {lt.upper()} lines (total tokens: {grand_total})")
    header = f"{'Onset':>6} {'Total':>6} {'%':>5} | " + " | ".join(f"{p:>12}" for p in POSITIONS)
    print(header)
    print("-" * len(header))
    for o in TARGET:
        o_total = sum(counts[d][lt][p].get(o, 0) for p in POSITIONS)
        pct = 100 * o_total / grand_total if grand_total else 0
        p_base = o_total / grand_total if grand_total else 0
        vals = []
        for p in POSITIONS:
            n_pos = totals[d][lt][p]
            o_pos = counts[d][lt][p].get(o, 0)
            p_cond = o_pos / n_pos if n_pos else 0
            e = p_cond / p_base if p_base > 0 else float('nan')
            vals.append(f"{e:.2f}×(N={o_pos:>3})")
        print(f"{o:>6} {o_total:>6} {pct:>4.1f}% | " + " | ".join(vals))

for d in ['A', 'B']:
    print(f"\n{'='*70}")
    print(f"DIALECT {d}")
    print(f"{'='*70}")
    for lt in ['cont', 'opener']:
        compute_table(d, lt)

# Summary: concentration ratio LF% for k vs p/t/f in cont lines
print(f"\n\n{'='*70}")
print("SUMMARY: LF% for gallows classes {k, p, t, f} in CONTINUATION lines")
print(f"{'='*70}")
for d in ['A', 'B']:
    print(f"\nDialect {d}:")
    for o in TARGET:
        o_total = sum(counts[d]['cont'][p].get(o, 0) for p in POSITIONS)
        lf_n = counts[d]['cont']['LF'].get(o, 0)
        pos1_n = counts[d]['cont']['pos1'].get(o, 0)
        mid_n = counts[d]['cont']['MID'].get(o, 0)
        pre_ll_n = counts[d]['cont']['pre_LL'].get(o, 0)
        ll_n = counts[d]['cont']['LL'].get(o, 0)
        if o_total == 0:
            print(f"  {o}: 0 tokens")
            continue
        print(f"  {o}: total={o_total:>4}  LF={lf_n:>4}({100*lf_n/o_total:.0f}%)  pos1={pos1_n:>4}({100*pos1_n/o_total:.0f}%)  MID={mid_n:>4}({100*mid_n/o_total:.0f}%)  pre_LL={pre_ll_n:>3}({100*pre_ll_n/o_total:.0f}%)  LL={ll_n:>3}({100*ll_n/o_total:.0f}%)")
