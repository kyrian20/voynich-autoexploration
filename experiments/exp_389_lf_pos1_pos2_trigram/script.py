"""
exp_389: LF→pos1→pos2 Trigram Structure (H603)

Tests whether B-dialect line grammar is Markovian at bigram level.
For frequent (LF class, pos1 class) pairs, computes P(pos2 | LF, pos1) 
and compares to P(pos2 | pos1) alone.
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

# Pass 2: collect continuation lines with ≥3 words
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

# Collect trigrams (LF, pos1, pos2) for lines with ≥3 words
A_trigrams = []  # (lf_onset, p1_onset, p2_onset)
B_trigrams = []

for fb, lines_list in folio_lines.items():
    if not lines_list:
        continue
    dialect = lines_list[0][2]
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln, max_ln = min(line_nums), max(line_nums)
    for ln, words, d in lines_list:
        if ln == min_ln or ln == max_ln:
            continue  # continuation only
        if len(words) < 3:
            continue
        lf = get_onset(words[0])
        p1 = get_onset(words[1])
        p2 = get_onset(words[2])
        if dialect == 'A':
            A_trigrams.append((lf, p1, p2))
        else:
            B_trigrams.append((lf, p1, p2))

print(f"A trigrams (LF, pos1, pos2): {len(A_trigrams)}")
print(f"B trigrams (LF, pos1, pos2): {len(B_trigrams)}")

def analyze_trigrams(trigrams, label):
    print(f"\n{'='*80}")
    print(f"TRIGRAM ANALYSIS — {label}")
    print(f"{'='*80}")

    total = len(trigrams)
    # Baseline: pos2 distribution (unconditional)
    p2_all = Counter(p2 for _, _, p2 in trigrams)
    # pos1 → pos2 bigram distribution
    p1_p2_bigram = defaultdict(Counter)
    for lf, p1, p2 in trigrams:
        p1_p2_bigram[p1][p2] += 1
    # LF, pos1 → pos2 trigram distribution
    lf_p1_p2_trigram = defaultdict(Counter)
    for lf, p1, p2 in trigrams:
        lf_p1_p2_trigram[(lf, p1)][p2] += 1

    # for each (LF, pos1) pair, compute P(pos2) vs P(pos2 | pos1 only)
    lf_p1_counts = Counter((lf, p1) for lf, p1, _ in trigrams)

    # Focus on the most frequent (LF, pos1) pairs
    print(f"\n--- Top (LF, pos1) pairs ---")
    top_pairs = lf_p1_counts.most_common(15)
    for (lf, p1), n in top_pairs:
        print(f"  ({lf},{p1}): N={n}")

    # For key pairs, compare P(pos2 | LF, pos1) vs P(pos2 | pos1)
    KEY_POS2_CLASSES = ['ch', 'sh', 'qok', 'd', 'ok', 'ot', 'y', 's', 'ol', 'cth']

    print(f"\n--- Bigram vs Trigram Comparison for Key (LF, pos1) Pairs ---")
    print(f"Testing: does LF class add predictive power beyond pos1 class for pos2?\n")

    for (lf, p1), n_pair in lf_p1_counts.most_common(20):
        if n_pair < 15:
            break
        # pos2 from trigram (conditioned on LF AND pos1)
        p2_given_lf_p1 = Counter(p2 for lf2, p1_2, p2 in trigrams if lf2 == lf and p1_2 == p1)
        # pos2 from bigram (conditioned on pos1 only)
        p2_given_p1 = p1_p2_bigram[p1]
        n_p1 = sum(p2_given_p1.values())

        print(f"\n(LF={lf}, pos1={p1}), N_trigram={n_pair}, N_bigram={n_p1}:")
        for p2_class in KEY_POS2_CLASSES:
            n_trigram = p2_given_lf_p1.get(p2_class, 0)
            n_bigram_p2 = p2_given_p1.get(p2_class, 0)
            if n_trigram == 0 and n_bigram_p2 == 0:
                continue
            p_trigram = n_trigram / n_pair if n_pair > 0 else 0
            p_bigram = n_bigram_p2 / n_p1 if n_p1 > 0 else 0
            ratio = p_trigram / p_bigram if p_bigram > 0 else float('inf')
            if abs(ratio - 1.0) > 0.3 or n_trigram >= 3:  # only report notable differences
                flag = "  <<DIFF" if abs(ratio - 1.0) > 0.5 else ""
                print(f"  pos2={p2_class}: trigram={p_trigram:.2f}(N={n_trigram}/{n_pair}) vs bigram={p_bigram:.2f}(N={n_bigram_p2}/{n_p1}) ratio={ratio:.2f}{flag}")

    # Summary: how often does LF conditioning change pos2 prediction substantially?
    print(f"\n--- Summary: LF conditioning effect on pos2 ---")
    diffs = []
    for (lf, p1), n_pair in lf_p1_counts.items():
        if n_pair < 10:
            continue
        p2_given_lf_p1 = Counter(p2 for lf2, p1_2, p2 in trigrams if lf2 == lf and p1_2 == p1)
        p2_given_p1 = p1_p2_bigram[p1]
        n_p1 = sum(p2_given_p1.values())
        # Jensen-Shannon-like: TVD between P(pos2|LF,p1) and P(pos2|p1)
        all_classes = set(p2_given_lf_p1.keys()) | set(p2_given_p1.keys())
        tvd = 0
        for c in all_classes:
            p_tri = p2_given_lf_p1.get(c, 0) / n_pair
            p_bi = p2_given_p1.get(c, 0) / n_p1 if n_p1 > 0 else 0
            tvd += abs(p_tri - p_bi)
        tvd /= 2  # normalize to [0,1]
        diffs.append(((lf, p1), n_pair, tvd))

    diffs.sort(key=lambda x: -x[2])
    print(f"Pairs with highest LF-conditioning effect (TVD between P(pos2|LF,p1) vs P(pos2|p1)):")
    for (lf, p1), n, tvd in diffs[:15]:
        print(f"  ({lf},{p1}) N={n}: TVD={tvd:.3f}")

    # y-chain test: (y, y) → pos2 vs (*, y) → pos2
    if ('y', 'y') in lf_p1_counts:
        n_yy = lf_p1_counts[('y', 'y')]
        p2_yy = Counter(p2 for lf2, p1_2, p2 in trigrams if lf2 == 'y' and p1_2 == 'y')
        p2_xxy = p1_p2_bigram['y']
        n_xxy = sum(p2_xxy.values())
        print(f"\ny self-chain test: (y at LF, y at pos1) → pos2?")
        print(f"N(y,y)→*={n_yy}, N(*,y)→*={n_xxy}")
        for p2_class in ['y', 'ch', 'sh', 'qok', 'd', 'k', 't']:
            n_t = p2_yy.get(p2_class, 0)
            n_b = p2_xxy.get(p2_class, 0)
            p_t = n_t / n_yy if n_yy > 0 else 0
            p_b = n_b / n_xxy if n_xxy > 0 else 0
            ratio = p_t / p_b if p_b > 0 else float('inf')
            print(f"  pos2={p2_class}: (y,y)→{p_t:.3f}(N={n_t}) vs (*,y)→{p_b:.3f}(N={n_b}) ratio={ratio:.2f}")

analyze_trigrams(A_trigrams, "A-DIALECT")
analyze_trigrams(B_trigrams, "B-DIALECT")

