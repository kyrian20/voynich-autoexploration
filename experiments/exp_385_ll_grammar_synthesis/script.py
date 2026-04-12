"""
exp_385: A-Dialect LL Grammar Synthesis — Complete Pre_LL→LL Routing Matrix (H599)

Computes the full pre_LL→LL bigram matrix for both dialects.
All pre_LL onset classes × all LL onset classes.
Cross-validates all individual-experiment LL routing claims.
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

# Collect all bigrams
A_bigrams = []
B_bigrams = []

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
        for i in range(n - 1):
            pw = words[i]
            nw = words[i + 1]
            pp = pos_category(i, n)
            np_ = pos_category(i + 1, n)
            pp_label = f"{pp}→{np_}"
            if dialect == 'A':
                A_bigrams.append((pw, nw, pp_label))
            else:
                B_bigrams.append((pw, nw, pp_label))

print(f"A cont bigrams: {len(A_bigrams)}")
print(f"B cont bigrams: {len(B_bigrams)}")

# === PRE_LL → LL ROUTING MATRIX ===
# Pre_LL classes to characterize
PRE_LL_CLASSES = ['qot', 'qok', 'ok', 'ot', 'ch', 'sh', 'd', 'y', 's', 'cth', 'r', 'ol', 'other']
LL_CLASSES = ['d', 'ch', 'sh', 'qok', 'ok', 'ot', 'qot', 'ol', 'y', 's', 'r', 'other']

for dialect, bigrams_list in [('A', A_bigrams), ('B', B_bigrams)]:
    print(f"\n{'='*80}")
    print(f"PRE_LL → LL ROUTING MATRIX — {dialect}-DIALECT")
    print(f"{'='*80}")

    # Get all pre_LL→LL pairs
    ll_bigrams = [(pw, nw, pp) for pw, nw, pp in bigrams_list if 'pre_LL→LL' in pp]
    total_ll = len(ll_bigrams)

    # Baseline LL onset distribution
    all_ll_onset = Counter(get_onset(nw) for pw, nw, pp in ll_bigrams)
    print(f"\nTotal pre_LL→LL pairs: {total_ll}")
    print(f"LL baseline distribution:")
    for onset in LL_CLASSES:
        n = all_ll_onset.get(onset, 0)
        print(f"  {onset}: {n} ({n/total_ll*100:.1f}%)")

    print(f"\n{'Pre_LL':<10} {'N':>5} | " + " ".join(f"{c:>6}" for c in LL_CLASSES))
    print("-" * (16 + len(LL_CLASSES) * 7))

    for pre_class in PRE_LL_CLASSES:
        pre_rows = [(pw, nw, pp) for pw, nw, pp in ll_bigrams if get_onset(pw) == pre_class]
        n_pre = len(pre_rows)
        if n_pre == 0:
            print(f"{pre_class:<10} {n_pre:>5} | " + " ".join(f"{'---':>6}" for _ in LL_CLASSES))
            continue

        ll_onset_counts = Counter(get_onset(nw) for pw, nw, pp in pre_rows)
        row = f"{pre_class:<10} {n_pre:>5} | "
        cells = []
        for ll_class in LL_CLASSES:
            n_hit = ll_onset_counts.get(ll_class, 0)
            n_base = all_ll_onset.get(ll_class, 0)
            if n_base == 0:
                cells.append(f"{'nan':>6}")
                continue
            p_cond = n_hit / n_pre
            p_base = n_base / total_ll
            e = p_cond / p_base
            if e >= 2.0:
                cells.append(f"{'**'+f'{e:.1f}':>6}")
            elif e >= 1.5:
                cells.append(f"{'*'+f'{e:.1f}':>6}")
            elif e <= 0.3:
                cells.append(f"{'--'+f'{e:.1f}':>6}")
            else:
                cells.append(f"{f'{e:.2f}':>6}")
        print(row + " ".join(cells))

    # === PRIMARY ROUTING TABLE ===
    print(f"\n--- Primary routing for each pre_LL class ({dialect}-dialect) ---")
    print(f"{'Pre_LL':<10} {'N':>5}  {'Top LL class':<12} {'E':>6}  {'N_hit':>6}")
    for pre_class in PRE_LL_CLASSES:
        pre_rows = [(pw, nw, pp) for pw, nw, pp in ll_bigrams if get_onset(pw) == pre_class]
        n_pre = len(pre_rows)
        if n_pre == 0:
            print(f"{pre_class:<10} {n_pre:>5}  {'(none)':12}")
            continue
        ll_onset_counts = Counter(get_onset(nw) for pw, nw, pp in pre_rows)
        best_e, best_class, best_n = 0, None, 0
        for ll_class in LL_CLASSES:
            n_hit = ll_onset_counts.get(ll_class, 0)
            n_base = all_ll_onset.get(ll_class, 0)
            if n_base == 0 or n_hit == 0:
                continue
            e = (n_hit / n_pre) / (n_base / total_ll)
            if e > best_e:
                best_e, best_class, best_n = e, ll_class, n_hit
        if best_class:
            print(f"{pre_class:<10} {n_pre:>5}  {best_class:<12} {best_e:>6.2f}×  {best_n:>6}/{n_pre}")
        else:
            print(f"{pre_class:<10} {n_pre:>5}  {'(no strong)':12}")

    # === PRIMARY PREDECESSOR TABLE (from LL terminal perspective) ===
    print(f"\n--- Primary predecessor for each LL onset class ({dialect}-dialect) ---")
    print(f"{'LL onset':<10} {'Total':>6}  {'Top pre_LL':>12} {'E':>6}  {'N_hit':>6}")
    for ll_class in ['d', 'ch', 'ol', 'r', 'ot', 'sh', 'qok', 'y']:
        ll_rows = [(pw, nw, pp) for pw, nw, pp in ll_bigrams if get_onset(nw) == ll_class]
        n_ll = len(ll_rows)
        if n_ll == 0:
            print(f"{ll_class:<10} {n_ll:>6}")
            continue
        pre_counts = Counter(get_onset(pw) for pw, nw, pp in ll_rows)
        # Compute E for each pre class
        best_e, best_class, best_n = 0, None, 0
        for pre_class in PRE_LL_CLASSES:
            n_hit = pre_counts.get(pre_class, 0)
            # Count how many pre_LL bigrams from this pre_class total
            pre_total = sum(1 for pw, nw, pp in ll_bigrams if get_onset(pw) == pre_class)
            if pre_total == 0 or n_hit == 0:
                continue
            p_cond = n_hit / pre_total
            p_base = n_ll / total_ll
            e = p_cond / p_base
            if e > best_e:
                best_e, best_class, best_n = e, pre_class, n_hit
        print(f"{ll_class:<10} {n_ll:>6}  {best_class or '':>12} {best_e:>6.2f}×  {best_n:>6}/{n_ll if n_ll>0 else 1}")

    # === TOP WORD PAIRS ===
    print(f"\n--- Top {dialect}-dialect pre_LL→LL word pairs (N≥3) ---")
    pair_counts = Counter((get_onset(pw)+':'+pw, get_onset(nw)+':'+nw) for pw, nw, pp in ll_bigrams)
    for (pw, nw), cnt in pair_counts.most_common(25):
        if cnt >= 2:
            print(f"  {pw} → {nw}: {cnt}")
