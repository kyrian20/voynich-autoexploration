"""
exp_368: y-Onset Self-Succession Word-Level Analysis (H581)

H581: y→y self-succession (B=2.71×, A=1.92×) is driven by CLASS-LEVEL onset memory
(different y-onset words), not word-level clustering (same word repeating).

Also:
- What is y-onset's role in the grammar? (LF=5.46×/2.63×, self-succession strong)
- What specific y-onset words form y→y pairs?
- Is y→y succession position-specific (like ok→ok A LL-biased)?
- What are the top y-onset successors across ALL onset classes?

Parallel to exp_361 (ok→ok analysis), now for y-onset.
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
print("y-ONSET SELF-SUCCESSION WORD-LEVEL ANALYSIS (H581)")
print("="*70)

for DIALECT in ('A', 'B'):
    cont_lines = register_lines[DIALECT]['cont']
    print(f"\n{'='*60}")
    print(f"DIALECT {DIALECT}: N_cont_lines={len(cont_lines)}")
    print(f"{'='*60}")

    # Collect all y-onset words with their positions and successors
    y_total_tokens = 0
    yy_pairs = []          # (y_word1, y_word2) pairs
    y_next_onset = Counter()  # successor onset distribution from y-onset words
    y_prev_onset = Counter()  # predecessor onset distribution for y-onset words

    pos_slot_y = {'LF': 0, 'pos1': 0, 'MID_inner': 0, 'pre_LL': 0, 'LL': 0, 'total': 0}
    pos_slot_yy = {'LF→pos1': 0, 'pos1→pos2': 0, 'MID_inner': 0, 'pre_LL→LL': 0}

    all_pairs_total = 0
    all_pairs_y_next = 0

    for words in cont_lines:
        n = len(words)
        all_pairs_total += n - 1

        for idx, w in enumerate(words):
            if get_onset(w) == 'y':
                y_total_tokens += 1
                # Position slot
                pos_slot_y['total'] += 1
                if idx == 0: pos_slot_y['LF'] += 1
                elif idx == 1 and n >= 3: pos_slot_y['pos1'] += 1
                if idx == n - 1: pos_slot_y['LL'] += 1
                elif idx == n - 2 and n >= 3: pos_slot_y['pre_LL'] += 1
                if 2 <= idx <= n - 3 and n >= 5: pos_slot_y['MID_inner'] += 1

                # Successor analysis
                if idx < n - 1:
                    next_w = words[idx + 1]
                    next_onset = get_onset(next_w)
                    y_next_onset[next_onset] += 1
                    if get_onset(next_w) == 'y':
                        yy_pairs.append((w, next_w))
                        # Position of this y→y pair
                        if idx == 0: pos_slot_yy['LF→pos1'] += 1
                        elif idx == 1: pos_slot_yy['pos1→pos2'] += 1
                        elif idx == n - 2: pos_slot_yy['pre_LL→LL'] += 1
                        else: pos_slot_yy['MID_inner'] += 1

                # Predecessor analysis
                if idx > 0:
                    prev_onset = get_onset(words[idx - 1])
                    y_prev_onset[prev_onset] += 1

        # Count y-next for baseline
        for idx in range(n - 1):
            if get_onset(words[idx + 1]) == 'y':
                all_pairs_y_next += 1

    y_baseline = all_pairs_y_next / all_pairs_total if all_pairs_total > 0 else 0

    print(f"\n--- {DIALECT}: y-onset token distribution ---")
    print(f"Total y-onset tokens: {y_total_tokens}")
    total_cont_tokens = sum(len(w) for w in cont_lines)

    # Position distribution of y-onset
    lf_total = sum(1 for words in cont_lines if len(words) >= 1)
    ll_total = sum(1 for words in cont_lines if len(words) >= 2)
    mid_total_tokens = sum(max(0, len(words) - 4) for words in cont_lines if len(words) >= 5)
    print(f"  LF: {pos_slot_y['LF']}/{lf_total} = {pos_slot_y['LF']/lf_total*100:.1f}%")
    if mid_total_tokens > 0:
        print(f"  MID_inner: {pos_slot_y['MID_inner']}/{mid_total_tokens} = {pos_slot_y['MID_inner']/mid_total_tokens*100:.1f}%")
    print(f"  LL: {pos_slot_y['LL']}/{ll_total} = {pos_slot_y['LL']/ll_total*100:.1f}%")

    print(f"\n--- {DIALECT}: y→y self-succession analysis ---")
    yy_total = len(yy_pairs)
    y_as_first = sum(y_next_onset.values())
    yy_rate = yy_total / y_as_first if y_as_first > 0 else 0
    E_yy = yy_rate / y_baseline if y_baseline > 0 else float('nan')
    print(f"y→y pairs: {yy_total}/{y_as_first} = {yy_rate*100:.1f}% (baseline {y_baseline*100:.1f}%, E={E_yy:.2f}×)")

    # Same vs Different word analysis
    same_word_pairs = [(w1, w2) for w1, w2 in yy_pairs if w1 == w2]
    diff_word_pairs = [(w1, w2) for w1, w2 in yy_pairs if w1 != w2]
    print(f"  Same word y→y: {len(same_word_pairs)}/{yy_total} = {len(same_word_pairs)/yy_total*100:.1f}%")
    print(f"  Different word y→y: {len(diff_word_pairs)}/{yy_total} = {len(diff_word_pairs)/yy_total*100:.1f}%")

    # Top y→y pairs
    yy_pair_counts = Counter(yy_pairs)
    print(f"\n  Top y→y word pairs:")
    for (w1, w2), cnt in yy_pair_counts.most_common(15):
        marker = " [SAME]" if w1 == w2 else ""
        print(f"    {w1} → {w2}: {cnt}{marker}")

    # Position gradient of y→y
    print(f"\n  y→y position distribution:")
    for pos, cnt in pos_slot_yy.items():
        print(f"    {pos}: {cnt}")

    # Top y-onset words
    y_word_counts = Counter()
    for words in cont_lines:
        for w in words:
            if get_onset(w) == 'y':
                y_word_counts[w] += 1
    print(f"\n--- {DIALECT}: Top y-onset words (top 20) ---")
    total_y = sum(y_word_counts.values())
    for word, cnt in y_word_counts.most_common(20):
        print(f"  {word}: {cnt} ({cnt/total_y*100:.1f}%)")

    # y-onset successor profile
    print(f"\n--- {DIALECT}: y-onset successor profile (what follows y) ---")
    y_as_first_total = sum(y_next_onset.values())
    all_pairs_cnt = Counter()
    all_total = 0
    for words in cont_lines:
        for idx in range(len(words) - 1):
            all_pairs_cnt[get_onset(words[idx + 1])] += 1
            all_total += 1
    print(f"{'Onset':<8} {'N(y→X)':>8} {'P(y→X)':>9} {'baseline':>10} {'E':>6}")
    for onset in ['d', 'ch', 'sh', 'qok', 'ok', 'ot', 'y', 'ol', 's', 'k', 't', 'p']:
        n_yx = y_next_onset[onset]
        p_yx = n_yx / y_as_first_total if y_as_first_total > 0 else 0
        p_base = all_pairs_cnt[onset] / all_total if all_total > 0 else 0
        E = p_yx / p_base if p_base > 0 else float('nan')
        print(f"{onset:<8} {n_yx:>8} {p_yx*100:>8.1f}%  {p_base*100:>9.1f}%  {E:>5.2f}×")

    # y-onset predecessor profile
    print(f"\n--- {DIALECT}: What precedes y-onset words ---")
    y_prev_total = sum(y_prev_onset.values())
    all_prev_cnt = Counter()
    for words in cont_lines:
        for idx in range(1, len(words)):
            all_prev_cnt[get_onset(words[idx - 1])] += 1
    print(f"{'Onset':<8} {'N(X→y)':>8} {'P(X→y|X)':>11} {'baseline':>10} {'E':>6}")
    # Compute P(y|X) for each X
    x_total = Counter()
    x_y_count = Counter()
    for words in cont_lines:
        for idx in range(len(words) - 1):
            x_total[get_onset(words[idx])] += 1
            if get_onset(words[idx + 1]) == 'y':
                x_y_count[get_onset(words[idx])] += 1
    baseline_y_succ = all_pairs_cnt['y'] / all_total if all_total > 0 else 0
    for onset in ['d', 'ch', 'sh', 'qok', 'ok', 'ot', 'y', 'ol', 's']:
        n_xy = x_y_count[onset]
        n_x = x_total[onset]
        p_xy = n_xy / n_x if n_x > 0 else 0
        E = p_xy / baseline_y_succ if baseline_y_succ > 0 else float('nan')
        print(f"{onset:<8} {n_xy:>8} {p_xy*100:>10.1f}%  {baseline_y_succ*100:>9.1f}%  {E:>5.2f}×")
