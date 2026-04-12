"""
exp_360: ch→daiin Sequential Rule (H571)
F361 (exp_359): ch-onset is dominant predecessor of daiin at pre-LL→LL in A-dialect (34.5%).
Is ch→daiin a cross-dialect rule with E significantly above baseline?
Also: is daiin enriched after ch-onset at ALL positions, or just pre-LL→LL?
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

print("=" * 70)
print("ch→daiin SEQUENTIAL RULE (H571)")
print("=" * 70)

for dialect in ['A', 'B']:
    cont_lines = register_lines[dialect]['cont']
    print(f"\n{'='*70}")
    print(f"{dialect}-DIALECT")
    print(f"{'='*70}")

    # All adjacent pairs in continuation lines, with position category
    def pos_cat(i, n):
        if i == 0: return 'LF'
        elif i == 1: return 'pos1'
        elif i == n-1: return 'LL'
        else: return 'MID'

    pairs = []
    for wlist in cont_lines:
        n = len(wlist)
        for i in range(n-1):
            prev = wlist[i]
            nxt = wlist[i+1]
            prev_o = get_onset(prev)
            next_o = get_onset(nxt)
            prev_p = pos_cat(i, n)
            next_p = pos_cat(i+1, n)
            if next_p == 'LL':
                pair_cat = 'pre-LL→LL'
            elif prev_p == 'LF':
                pair_cat = 'LF→pos1'
            elif prev_p == 'pos1':
                pair_cat = 'pos1→next'
            else:
                pair_cat = 'MID_inner'
            pairs.append((prev_o, prev, next_o, nxt, pair_cat))

    total_pairs = len(pairs)
    
    # For each onset class, compute: P(next=daiin | prev=X)
    print(f"\n--- P(next=daiin | prev_onset) across ALL positions ---")
    print(f"{'Onset':<12} {'N_prev':>8} {'→daiin%':>9} {'→daiin_N':>10} {'E vs overall':>13}")
    
    onset_pairs = defaultdict(list)
    for p_o, p, n_o, n_w, pc in pairs:
        onset_pairs[p_o].append(n_w)
    
    overall_daiin_rate = sum(1 for _,_,_,nw,_ in pairs if nw == 'daiin') / max(len(pairs), 1)
    print(f"  Overall daiin rate at next position: {100*overall_daiin_rate:.2f}%")
    print()
    
    for onset in ['ch','sh','d','qok','ok','y','s','ot','ol','qot','cth','k','t','p','f']:
        words = onset_pairs.get(onset, [])
        n = len(words)
        if n < 10: continue
        daiin_cnt = words.count('daiin')
        rate = daiin_cnt / n
        E = rate / max(overall_daiin_rate, 0.001)
        print(f"  {onset:<12} {n:>8} {100*rate:>8.2f}% {daiin_cnt:>10}   {E:>10.2f}×")

    # By position category: for ch-onset specifically
    print(f"\n--- ch→daiin by position category ---")
    print(f"{'Cat':<15} {'N_ch':>7} {'ch→daiin%':>11} {'non_ch→daiin%':>15} {'E':>7}")
    pos_groups = defaultdict(lambda: {'ch_tot':0,'ch_daiin':0,'nch_tot':0,'nch_daiin':0})
    for p_o, p, n_o, n_w, pc in pairs:
        if p_o == 'ch':
            pos_groups[pc]['ch_tot'] += 1
            if n_w == 'daiin': pos_groups[pc]['ch_daiin'] += 1
        else:
            pos_groups[pc]['nch_tot'] += 1
            if n_w == 'daiin': pos_groups[pc]['nch_daiin'] += 1
    
    for cat in ['LF→pos1','pos1→next','MID_inner','pre-LL→LL']:
        g = pos_groups[cat]
        n_ch = g['ch_tot']
        n_nch = g['nch_tot']
        if n_ch == 0: continue
        ch_pct = 100*g['ch_daiin']/n_ch
        nch_pct = 100*g['nch_daiin']/max(n_nch,1)
        E = (g['ch_daiin']/n_ch) / max(g['nch_daiin']/max(n_nch,1), 0.001)
        print(f"  {cat:<15} {n_ch:>7} {ch_pct:>10.1f}% {nch_pct:>14.1f}% {E:>6.2f}×")

    # What specific ch-onset words precede daiin?
    print(f"\n--- Specific ch-onset words preceding daiin ---")
    ch_before_daiin = Counter()
    for p_o, p, n_o, n_w, pc in pairs:
        if p_o == 'ch' and n_w == 'daiin':
            ch_before_daiin[p] += 1
    print(f"  Total ch→daiin pairs: {sum(ch_before_daiin.values())}")
    for word, cnt in ch_before_daiin.most_common(10):
        print(f"  {word:<20}: N={cnt}")

    # What follows ch-onset words? Top 10
    print(f"\n--- Top words following ch-onset (all positions) ---")
    ch_nexts = Counter()
    for p_o, p, n_o, n_w, pc in pairs:
        if p_o == 'ch':
            ch_nexts[n_w] += 1
    total_ch_nexts = sum(ch_nexts.values())
    print(f"  Total ch-onset predecessor pairs: {total_ch_nexts}")
    for word, cnt in ch_nexts.most_common(8):
        onset = get_onset(word)
        print(f"  {word:<15} (onset={onset:<5}): {cnt} ({100*cnt/max(total_ch_nexts,1):.1f}%)")

    # Cross-check: what precedes daiin at LL (all predecessors)?
    print(f"\n--- What precedes daiin at LL (pre-LL→LL only) ---")
    prell_daiin_prev = Counter()
    for p_o, p, n_o, n_w, pc in pairs:
        if n_w == 'daiin' and pc == 'pre-LL→LL':
            prell_daiin_prev[p_o] += 1
    n_prell_daiin = sum(prell_daiin_prev.values())
    print(f"  Total pre-LL→LL daiin pairs: {n_prell_daiin}")
    for onset, cnt in prell_daiin_prev.most_common(8):
        pct = 100*cnt/max(n_prell_daiin,1)
        # Also compute E: baseline for this onset at pre-LL
        prell_prev_all = Counter()
        for p_o, p, n_o, n_w, pc in pairs:
            if pc == 'pre-LL→LL':
                prell_prev_all[p_o] += 1
        baseline_pct = 100*prell_prev_all[onset]/max(sum(prell_prev_all.values()),1)
        E_val = (cnt/max(n_prell_daiin,1)) / max(prell_prev_all[onset]/max(sum(prell_prev_all.values()),1), 0.001)
        print(f"  {onset:<12}: {cnt} ({pct:.1f}%); baseline={baseline_pct:.1f}%; E={E_val:.2f}×")

