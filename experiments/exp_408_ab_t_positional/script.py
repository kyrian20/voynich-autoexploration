"""
exp_408: A/B t-onset Full Positional Characterization (H613)

For both dialects, compute:
1. t positional distribution: rate at LF, pos1, pos2, pos3, MID, pre_LL, LL
   vs. baseline for that position (how enriched/depleted is t?)
2. For continuation lines only:
   - When t appears at pos0 (LF), what is pos1 distribution?
   - When t appears in MID (idx 2..n-3), what comes next (successor)?
   - When t appears at pre_LL (idx n-2), what comes at LL?
3. Compare t profile to p profile (p is STRONG-FORMULA gallows)
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
    return re.sub(r'[rv]\d*$', '', folio)

# Pass 1: folio dialect
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
        lc = m.group(3).lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
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

# Pass 2: collect lines by folio/line number for continuation detection
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
        ln = int(m.group(2))
        lc = m.group(3).lstrip('+*=/~&')
        fb = folio_base(folio)
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((ln, words))

# Identify continuation lines per folio (not min or max ln)
cont_lines_by_dialect = {'A': [], 'B': []}
all_lines_by_dialect = {'A': [], 'B': []}
for fb, entries in folio_lines.items():
    dialect = folio_dialect.get(fb, 'A')
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in entries:
        all_lines_by_dialect[dialect].append(words)
        if ln != min_ln and ln != max_ln:
            cont_lines_by_dialect[dialect].append(words)

print("=== Dataset sizes ===")
for d in ['A', 'B']:
    print(f"  {d}: all_lines={len(all_lines_by_dialect[d])}, cont_lines={len(cont_lines_by_dialect[d])}")

# ---- Analysis ----
# Position categories for a line of length n:
# LF = idx 0
# pos1 = idx 1 (if n >= 2)
# pos2 = idx 2 (if n >= 3)
# pos3 = idx 3 (if n >= 4)
# MID = indices 2..n-3 (if n >= 5)
# pre_LL = idx n-2 (if n >= 4)
# LL = idx n-1 (if n >= 2)

def analyze_positional(lines, onset_target):
    """For each line, for each token, determine its position category and onset.
    Accumulate:
    - pos_count[pos_label][onset] = count of 'onset' appearing at 'pos_label'
    - total at each pos_label
    Also for continuation-style analysis:
    - lf_to_pos1[onset_lf][onset_p1] = count (for lines where lf matches target)
    - mid_to_succ[onset_mid][onset_succ] = count (for MID occurrences of target)
    - preLl_to_ll[onset_preLL][onset_ll] = count (for pre_LL occurrences of target)
    """
    pos_counts = defaultdict(Counter)  # pos_label -> Counter of onsets
    # For target onset at LF: what is pos1?
    target_lf_pos1 = Counter()
    target_lf_pos1_total = 0
    # For target onset at MID: what is successor?
    target_mid_succ = Counter()
    target_mid_succ_total = 0
    # For target onset at pre_LL: what is LL?
    target_preLL_ll = Counter()
    target_preLL_ll_total = 0
    # Baseline: all pos1, MID, LL
    baseline_pos1 = Counter()
    baseline_mid = Counter()
    baseline_ll = Counter()
    baseline_mid_succ = Counter()  # All MID successors regardless of onset

    for words in lines:
        n = len(words)
        if n < 2:
            continue
        onsets = [get_onset(w) for w in words]

        # LF
        pos_counts['LF'][onsets[0]] += 1
        # pos1
        if n >= 2:
            pos_counts['pos1'][onsets[1]] += 1
            baseline_pos1[onsets[1]] += 1
        # pos2
        if n >= 3:
            pos_counts['pos2'][onsets[2]] += 1
        # pos3
        if n >= 4:
            pos_counts['pos3'][onsets[3]] += 1
        # LL
        pos_counts['LL'][onsets[-1]] += 1
        baseline_ll[onsets[-1]] += 1
        # pre_LL
        if n >= 4:
            pos_counts['pre_LL'][onsets[-2]] += 1

        # MID tokens (indices 2..n-3, requiring n >= 5)
        if n >= 5:
            for idx in range(2, n - 2):
                pos_counts['MID'][onsets[idx]] += 1
                baseline_mid[onsets[idx]] += 1
                # MID successor
                pos_counts['MID_succ'][onsets[idx+1]] += 1
                baseline_mid_succ[onsets[idx+1]] += 1

        # LF target: pos1 routing
        if n >= 2 and onsets[0] == onset_target:
            target_lf_pos1[onsets[1]] += 1
            target_lf_pos1_total += 1

        # MID target: successor
        if n >= 5:
            for idx in range(2, n - 2):
                if onsets[idx] == onset_target:
                    target_mid_succ[onsets[idx+1]] += 1
                    target_mid_succ_total += 1

        # pre_LL target: LL routing
        if n >= 4 and onsets[-2] == onset_target:
            target_preLL_ll[onsets[-1]] += 1
            target_preLL_ll_total += 1

    return (pos_counts, baseline_pos1, baseline_mid, baseline_ll, baseline_mid_succ,
            target_lf_pos1, target_lf_pos1_total,
            target_mid_succ, target_mid_succ_total,
            target_preLL_ll, target_preLL_ll_total)

for target, dialect_pairs in [('t', 'AB'), ('p', 'AB')]:
    for dialect in ['A', 'B']:
        lines = cont_lines_by_dialect[dialect]
        (pos_counts, baseline_pos1, baseline_mid, baseline_ll, baseline_mid_succ,
         target_lf_pos1, target_lf_pos1_total,
         target_mid_succ, target_mid_succ_total,
         target_preLL_ll, target_preLL_ll_total) = analyze_positional(lines, target)

        # Compute positional rates for target onset
        print(f"\n=== {dialect} onset='{target}' positional profile ===")
        total_at_pos = {pos: sum(pos_counts[pos].values()) for pos in pos_counts}
        for pos in ['LF', 'pos1', 'pos2', 'pos3', 'MID', 'pre_LL', 'LL']:
            if pos not in total_at_pos or total_at_pos[pos] == 0:
                continue
            n_target = pos_counts[pos][target]
            rate = n_target / total_at_pos[pos]
            # Baseline rate of target across all positions
            all_tokens = sum(sum(pos_counts[p].values()) for p in pos_counts if p not in ('MID_succ',))
            all_target = sum(pos_counts[p][target] for p in pos_counts if p not in ('MID_succ',))
            global_rate = all_target / all_tokens if all_tokens > 0 else 0
            E = rate / global_rate if global_rate > 0 else float('inf')
            print(f"  {pos:8s}: n={n_target:4d}/{total_at_pos[pos]:5d}  rate={rate:.3f}  E={E:.2f}×")

        # LF→pos1 routing (when LF=target)
        if target_lf_pos1_total > 0:
            print(f"\n  LF='{target}' → pos1 routing (N={target_lf_pos1_total}):")
            # baseline pos1 rates
            total_p1 = sum(baseline_pos1.values())
            top_p1 = sorted(target_lf_pos1.items(), key=lambda x: -x[1])[:8]
            for onset, cnt in top_p1:
                rate_here = cnt / target_lf_pos1_total
                base_rate = baseline_pos1[onset] / total_p1 if total_p1 > 0 else 0
                E = rate_here / base_rate if base_rate > 0 else float('inf')
                print(f"    {onset:6s}: n={cnt:3d}  rate={rate_here:.3f}  base={base_rate:.3f}  E={E:.2f}×")

        # MID→successor routing (when MID position has target)
        if target_mid_succ_total > 0:
            print(f"\n  MID='{target}' → successor (N={target_mid_succ_total}):")
            total_ms = sum(baseline_mid_succ.values())
            top_ms = sorted(target_mid_succ.items(), key=lambda x: -x[1])[:8]
            for onset, cnt in top_ms:
                rate_here = cnt / target_mid_succ_total
                base_rate = baseline_mid_succ[onset] / total_ms if total_ms > 0 else 0
                E = rate_here / base_rate if base_rate > 0 else float('inf')
                print(f"    {onset:6s}: n={cnt:3d}  rate={rate_here:.3f}  base={base_rate:.3f}  E={E:.2f}×")

        # pre_LL → LL routing (when pre_LL has target)
        if target_preLL_ll_total > 0:
            print(f"\n  pre_LL='{target}' → LL (N={target_preLL_ll_total}):")
            total_ll = sum(baseline_ll.values())
            top_ll = sorted(target_preLL_ll.items(), key=lambda x: -x[1])[:8]
            for onset, cnt in top_ll:
                rate_here = cnt / target_preLL_ll_total
                base_rate = baseline_ll[onset] / total_ll if total_ll > 0 else 0
                E = rate_here / base_rate if base_rate > 0 else float('inf')
                print(f"    {onset:6s}: n={cnt:3d}  rate={rate_here:.3f}  base={base_rate:.3f}  E={E:.2f}×")

print("\n=== Done ===")
