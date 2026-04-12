"""
exp_364: Comprehensive pre-LL → LL Grammar (H576)
F362: ch→daiin E=1.69× and qot→daiin E=2.50× at pre-LL→LL in A-dialect.
F339: am is the sole LL-terminal in B-dialect (6.49×).
This experiment computes full P(LL_word | prev_onset) for all top LL words
and P(LL_onset | prev_onset) in both dialects.
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

# Register classification — keep only continuation lines
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
print("PRE-LL → LL GRAMMAR: COMPREHENSIVE ANALYSIS")
print("=" * 70)

for dialect in ['A', 'B']:
    cont_lines = register_lines[dialect]['cont']
    print(f"\n{'='*70}")
    print(f"{dialect}-DIALECT (N_cont_lines={len(cont_lines)})")
    print(f"{'='*70}")

    # Collect pre-LL → LL pairs
    prell_pairs = []  # (prev_onset, prev_word, ll_onset, ll_word)
    for wlist in cont_lines:
        n = len(wlist)
        if n < 2: continue
        ll_word = wlist[-1]
        prell_word = wlist[-2]
        prell_pairs.append((get_onset(prell_word), prell_word, get_onset(ll_word), ll_word))

    total_prell = len(prell_pairs)
    print(f"pre-LL→LL pairs: {total_prell}")

    # Overall LL word frequency
    print(f"\n--- Top LL words (overall) ---")
    ll_words = Counter(lw for _,_,_,lw in prell_pairs)
    total_ll = sum(ll_words.values())
    print(f"{'Word':<15} {'N':>6} {'%':>7} {'onset':>8}")
    for word, cnt in ll_words.most_common(15):
        print(f"  {word:<15} {cnt:>6} {100*cnt/total_ll:>6.1f}%  {get_onset(word)}")

    # Overall pre-LL onset frequency
    print(f"\n--- pre-LL onset distribution ---")
    prell_onsets = Counter(po for po,_,_,_ in prell_pairs)
    for onset, cnt in sorted(prell_onsets.items(), key=lambda x: -x[1]):
        if cnt < 5: continue
        print(f"  {onset:<10}: {cnt} ({100*cnt/total_prell:.1f}%)")

    # For each top LL word: what precedes it at pre-LL?
    top_ll_words = [w for w, _ in ll_words.most_common(8)]
    print(f"\n--- For each top LL word: pre-LL onset distribution ---")
    for ll_target in top_ll_words:
        target_pairs = [(po, pw) for po, pw, lo, lw in prell_pairs if lw == ll_target]
        n_target = len(target_pairs)
        if n_target < 3: continue
        prev_onset_cnt = Counter(po for po, pw in target_pairs)
        print(f"\n  LL word = '{ll_target}' (N={n_target}, {100*n_target/total_prell:.1f}% of LL)")
        print(f"  {'prev_onset':<12} {'N':>5} {'% of this LL':>14} {'baseline%':>11} {'E':>7}")
        for onset, cnt in prev_onset_cnt.most_common(8):
            baseline = prell_onsets.get(onset, 0) / total_prell
            target_rate = cnt / n_target
            E = target_rate / max(baseline, 0.001)
            print(f"    {onset:<12} {cnt:>5} {100*target_rate:>13.1f}% {100*baseline:>10.1f}% {E:>6.2f}×")

    # For each pre-LL onset: what LL words does it predict?
    print(f"\n--- For each pre-LL onset class: top LL words ---")
    onset_to_ll = defaultdict(Counter)
    for po, pw, lo, lw in prell_pairs:
        onset_to_ll[po][lw] += 1
    
    for onset in ['ch','sh','d','qok','ok','y','qot','ot','cth','s']:
        ll_dist = onset_to_ll[onset]
        n_onset = sum(ll_dist.values())
        if n_onset < 10: continue
        print(f"\n  pre-LL onset={onset} (N={n_onset})")
        for word, cnt in ll_dist.most_common(5):
            onset_w = get_onset(word)
            print(f"    {word:<12} (onset={onset_w:<5}): {cnt} ({100*cnt/n_onset:.1f}%)")

    # Specific: qot-onset pre-LL → LL (qot→daiin E=2.50× from F362)
    print(f"\n--- qot-onset words preceding daiin at LL ---")
    qot_before_daiin = [(pw, lw) for po, pw, lo, lw in prell_pairs if po == 'qot' and lw == 'daiin']
    qot_total = sum(1 for po,_,_,_ in prell_pairs if po == 'qot')
    print(f"  qot pre-LL total: {qot_total}")
    print(f"  qot→daiin at LL: {len(qot_before_daiin)} ({100*len(qot_before_daiin)/max(qot_total,1):.1f}%)")
    qot_words = Counter(pw for pw, lw in qot_before_daiin)
    for word, cnt in qot_words.most_common():
        print(f"    {word}: N={cnt}")

