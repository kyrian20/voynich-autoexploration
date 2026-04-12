"""
exp_359: y→d Coupling Decomposition (H569)
Is y→d (B: 1.49×, A: 1.37× from F326) primarily y→daiin, and at which position pair?
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
        if ln == min_ln:
            register_lines[dialect]['opener'].append(words)
        elif ln == max_ln:
            register_lines[dialect]['closer'].append(words)
        else:
            register_lines[dialect]['cont'].append(words)

print("=" * 70)
print("y→d COUPLING DECOMPOSITION (H569)")
print("=" * 70)

for dialect in ['A', 'B']:
    cont_lines = register_lines[dialect]['cont']
    print(f"\n{'='*70}")
    print(f"{dialect}-DIALECT")
    print(f"{'='*70}")

    total_cont_words = sum(len(l) for l in cont_lines)
    total_d_onset = sum(1 for l in cont_lines for w in l if get_onset(w) == 'd')
    total_daiin = sum(1 for l in cont_lines for w in l if w == 'daiin')
    print(f"Continuation lines: N={len(cont_lines)}, total words={total_cont_words}")
    print(f"d-onset words: {total_d_onset} ({100*total_d_onset/max(total_cont_words,1):.1f}%)")
    print(f"daiin specifically: {total_daiin} ({100*total_daiin/max(total_cont_words,1):.1f}%)")
    print(f"daiin as fraction of d-onset: {100*total_daiin/max(total_d_onset,1):.1f}%")

    # Collect all adjacent pairs with position category
    def pos_category(word_idx, line_len):
        if word_idx == 0: return 'LF'
        elif word_idx == 1: return 'pos1'
        elif word_idx == line_len - 1: return 'LL'
        else: return 'MID'

    pairs = []
    for wlist in cont_lines:
        n = len(wlist)
        for i in range(n - 1):
            prev = wlist[i]
            nxt = wlist[i+1]
            prev_o = get_onset(prev)
            next_o = get_onset(nxt)
            prev_pos = pos_category(i, n)
            next_pos = pos_category(i+1, n)
            if prev_pos in ('LF','pos1','MID','LL') and next_pos in ('LF','pos1','MID','LL'):
                # Simplify category
                if next_pos == 'LL':
                    cat = 'pre-LL→LL'
                elif prev_pos == 'LF':
                    cat = 'LF→pos1'
                elif prev_pos == 'pos1':
                    cat = 'pos1→next'
                else:
                    cat = 'MID_inner'
            else:
                cat = 'other'
            pairs.append((prev_o, prev, next_o, nxt, cat))

    # Overall y→d enrichment
    y_prev = [(p, n_o, n_w, pc) for p_o, p, n_o, n_w, pc in pairs if p_o == 'y']
    non_y_prev = [(p, n_o, n_w, pc) for p_o, p, n_o, n_w, pc in pairs if p_o != 'y']

    y_to_d = sum(1 for p,n_o,n_w,pc in y_prev if n_o == 'd')
    y_to_daiin = sum(1 for p,n_o,n_w,pc in y_prev if n_w == 'daiin')
    y_to_d_not_daiin = y_to_d - y_to_daiin
    nony_to_d = sum(1 for p,n_o,n_w,pc in non_y_prev if n_o == 'd')
    nony_to_daiin = sum(1 for p,n_o,n_w,pc in non_y_prev if n_w == 'daiin')

    N_y = len(y_prev)
    N_nony = len(non_y_prev)

    print(f"\n--- Overall y→d and y→daiin ---")
    print(f"y-prev pairs: N={N_y}")
    print(f"  y→d: {y_to_d}/{N_y}={100*y_to_d/max(N_y,1):.1f}%")
    print(f"  y→daiin: {y_to_daiin}/{N_y}={100*y_to_daiin/max(N_y,1):.1f}%  ({100*y_to_daiin/max(y_to_d,1):.0f}% of y→d)")
    print(f"  y→d_not_daiin: {y_to_d_not_daiin}/{N_y}={100*y_to_d_not_daiin/max(N_y,1):.1f}%")
    print(f"non-y-prev pairs: N={N_nony}")
    print(f"  non-y→d: {nony_to_d}/{N_nony}={100*nony_to_d/max(N_nony,1):.1f}%")
    print(f"  non-y→daiin: {nony_to_daiin}/{N_nony}={100*nony_to_daiin/max(N_nony,1):.1f}%")

    E_yd = (y_to_d/max(N_y,1)) / max(nony_to_d/max(N_nony,1), 0.001)
    E_ydaiin = (y_to_daiin/max(N_y,1)) / max(nony_to_daiin/max(N_nony,1), 0.001)
    E_yd_notdaiin = (y_to_d_not_daiin/max(N_y,1)) / max((nony_to_d - nony_to_daiin)/max(N_nony,1), 0.001)
    print(f"  E(y→d): {E_yd:.2f}×")
    print(f"  E(y→daiin specifically): {E_ydaiin:.2f}×")
    print(f"  E(y→d_not_daiin): {E_yd_notdaiin:.2f}×")

    # By position category
    print(f"\n--- y→daiin and y→d by position category ---")
    pos_groups = defaultdict(lambda: {'y_d':0,'y_daiin':0,'y_tot':0,'ny_d':0,'ny_daiin':0,'ny_tot':0})
    for p_o, p, n_o, n_w, pc in pairs:
        cat = pc
        if p_o == 'y':
            pos_groups[cat]['y_tot'] += 1
            if n_o == 'd': pos_groups[cat]['y_d'] += 1
            if n_w == 'daiin': pos_groups[cat]['y_daiin'] += 1
        else:
            pos_groups[cat]['ny_tot'] += 1
            if n_o == 'd': pos_groups[cat]['ny_d'] += 1
            if n_w == 'daiin': pos_groups[cat]['ny_daiin'] += 1

    print(f"{'Cat':<16} {'N_y':>6} {'y→daiin%':>10} {'ny→daiin%':>11} {'E_daiin':>9} {'y→d%':>7} {'E_d':>7}")
    for cat in ['LF→pos1','pos1→next','MID_inner','pre-LL→LL']:
        g = pos_groups[cat]
        n_y = g['y_tot']
        n_ny = g['ny_tot']
        if n_y == 0: continue
        y_daiin_pct = 100*g['y_daiin']/n_y
        ny_daiin_pct = 100*g['ny_daiin']/max(n_ny,1)
        E_d = (g['y_d']/n_y) / max(g['ny_d']/max(n_ny,1), 0.001)
        E_daiin = (g['y_daiin']/n_y) / max(g['ny_daiin']/max(n_ny,1), 0.001)
        y_d_pct = 100*g['y_d']/n_y
        print(f"{cat:<16} {n_y:>6} {y_daiin_pct:>9.1f}% {ny_daiin_pct:>10.1f}% {E_daiin:>9.2f}× {y_d_pct:>6.1f}% {E_d:>6.2f}×")

    # Top d-onset words appearing after y-onset
    print(f"\n--- Top next-words after y-onset (d-onset only, all positions) ---")
    y_to_d_words = Counter()
    for p_o, p, n_o, n_w, pc in pairs:
        if p_o == 'y' and n_o == 'd':
            y_to_d_words[n_w] += 1
    total_y_to_d_cnt = sum(y_to_d_words.values())
    print(f"  {'Word':<15} {'Count':>7} {'% of y→d':>10}")
    for word, cnt in y_to_d_words.most_common(10):
        print(f"  {word:<15} {cnt:>7} {100*cnt/max(total_y_to_d_cnt,1):>9.1f}%")

    # y→daiin at each position: what y-words precede daiin?
    print(f"\n--- y-onset words preceding daiin (all positions) ---")
    y_words_before_daiin = Counter()
    for p_o, p, n_o, n_w, pc in pairs:
        if p_o == 'y' and n_w == 'daiin':
            y_words_before_daiin[p] += 1
    for word, cnt in y_words_before_daiin.most_common(8):
        print(f"  {word:<15} → daiin: N={cnt}")

    # Compare: what fraction of all daiin tokens are preceded by y-onset?
    total_daiin_pairs = sum(1 for p_o, p, n_o, n_w, pc in pairs if n_w == 'daiin')
    y_before_daiin = sum(1 for p_o, p, n_o, n_w, pc in pairs if n_w == 'daiin' and p_o == 'y')
    print(f"\n  daiin in pairs: {total_daiin_pairs}")
    print(f"  y-onset preceding daiin: {y_before_daiin} ({100*y_before_daiin/max(total_daiin_pairs,1):.1f}%)")

    # Also: MID positions specifically (most likely position for y→daiin coupling)
    print(f"\n--- At pre-LL→LL: what precedes daiin? ---")
    prell_daiin_prev = Counter()
    for p_o, p, n_o, n_w, pc in pairs:
        if n_w == 'daiin' and pc == 'pre-LL→LL':
            prell_daiin_prev[p_o] += 1
    total_prell_daiin = sum(prell_daiin_prev.values())
    print(f"  Total pre-LL→LL pairs where LL=daiin: {total_prell_daiin}")
    for onset, cnt in prell_daiin_prev.most_common(8):
        print(f"  prev_onset={onset:<10}: {cnt} ({100*cnt/max(total_prell_daiin,1):.1f}%)")
