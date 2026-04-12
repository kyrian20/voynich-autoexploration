"""
exp_361: ok→ok Self-Succession Drivers (H570)
F326: ok→ok is elevated (B: 1.96×, A: 1.32×) - the highest onset self-succession
besides qok. Is this driven by specific ok-word clusters (word-level) or
a broad ok onset-class memory?
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
print("ok→ok SELF-SUCCESSION DRIVERS (H570)")
print("=" * 70)

for dialect in ['A', 'B']:
    cont_lines = register_lines[dialect]['cont']
    print(f"\n{'='*70}")
    print(f"{dialect}-DIALECT")
    print(f"{'='*70}")

    # Collect all ok-onset adjacent pairs
    ok_pairs = []  # (prev_word, next_word, next_onset)
    non_ok_to_ok_pairs = []  # (prev_onset, next_word) when next is ok
    all_pairs_count = 0
    ok_to_ok_same = 0  # same exact word
    ok_to_ok_diff = 0  # different ok word

    for wlist in cont_lines:
        n = len(wlist)
        for i in range(n-1):
            prev = wlist[i]
            nxt = wlist[i+1]
            prev_o = get_onset(prev)
            next_o = get_onset(nxt)
            all_pairs_count += 1
            if prev_o == 'ok':
                ok_pairs.append((prev, nxt, next_o))
            if next_o == 'ok':
                non_ok_to_ok_pairs.append((prev_o, prev, nxt))

    # Overall ok→ok
    ok_to_ok = sum(1 for p,n,no in ok_pairs if no == 'ok')
    total_ok_prev = len(ok_pairs)
    ok_to_ok_same_word = sum(1 for p,n,no in ok_pairs if no == 'ok' and p == n)
    ok_to_ok_diff_word = ok_to_ok - ok_to_ok_same_word
    baseline_ok_rate = total_ok_prev / max(all_pairs_count, 1)

    print(f"Continuation lines: N={len(cont_lines)}")
    print(f"Total adjacent pairs: {all_pairs_count}")
    print(f"ok-onset prev pairs: {total_ok_prev}")
    print(f"ok→ok: {ok_to_ok}/{total_ok_prev}={100*ok_to_ok/max(total_ok_prev,1):.1f}%")
    print(f"ok→ok SAME word: {ok_to_ok_same_word} ({100*ok_to_ok_same_word/max(ok_to_ok,1):.0f}% of ok→ok)")
    print(f"ok→ok DIFFERENT ok word: {ok_to_ok_diff_word} ({100*ok_to_ok_diff_word/max(ok_to_ok,1):.0f}% of ok→ok)")
    
    # Baseline ok rate
    all_next_onsets = Counter(no for p,n,no in ok_pairs)
    overall_ok_next_baseline = sum(1 for _,_,no in [('',(),(x)) for _,_,x in ok_pairs] if False)  # dummy
    # Compute properly
    all_ok_as_next = sum(1 for po,p,nxt in non_ok_to_ok_pairs)  # all pairs where next=ok
    total_non_ok_prev = all_pairs_count - total_ok_prev
    non_ok_to_ok = len(non_ok_to_ok_pairs) - ok_to_ok  # subtract ok→ok from all ok-as-next
    non_ok_prev_to_ok = sum(1 for po,p,nxt in non_ok_to_ok_pairs if po != 'ok')
    print(f"\nBaseline: non-ok prev → ok next: {non_ok_prev_to_ok}/{total_non_ok_prev}={100*non_ok_prev_to_ok/max(total_non_ok_prev,1):.1f}%")
    E_self_succ = (ok_to_ok/max(total_ok_prev,1)) / max(non_ok_prev_to_ok/max(total_non_ok_prev,1), 0.001)
    print(f"ok→ok E: {E_self_succ:.2f}×")

    # Top ok words by frequency
    print(f"\n--- Top ok-onset words (frequency) ---")
    ok_words = Counter()
    for wlist in cont_lines:
        for w in wlist:
            if get_onset(w) == 'ok':
                ok_words[w] += 1
    total_ok_words = sum(ok_words.values())
    print(f"Total ok-onset tokens: {total_ok_words}")
    print(f"{'Word':<15} {'Count':>7} {'%':>7} {'CP90_running':>15}")
    running = 0
    for word, cnt in ok_words.most_common(15):
        running += cnt
        print(f"  {word:<15} {cnt:>7} {100*cnt/max(total_ok_words,1):>6.1f}% {100*running/max(total_ok_words,1):>14.1f}%")

    # Word-level ok→ok self-succession
    print(f"\n--- Top ok→ok pairs ---")
    ok_ok_pairs = Counter()
    for p, n, no in ok_pairs:
        if no == 'ok':
            ok_ok_pairs[(p, n)] += 1
    print(f"{'Pair':<35} {'Count':>7}")
    for (pw, nw), cnt in ok_ok_pairs.most_common(15):
        same_marker = " [SAME]" if pw == nw else ""
        print(f"  {pw:<15} → {nw:<15} {cnt:>7}{same_marker}")

    # For each top ok word, compute ok→same_word vs ok→any_ok vs baseline
    print(f"\n--- Per ok-word self-succession ---")
    print(f"{'Word':<15} {'N_prev':>8} {'→same%':>8} {'→any_ok%':>10} {'baseline_ok%':>14} {'E_self':>8}")
    baseline_ok_pct = 100 * (non_ok_prev_to_ok / max(total_non_ok_prev, 1))
    for word, freq in ok_words.most_common(10):
        # When this specific word is prev, how often does ok or same follow?
        word_prev_pairs = [(p,n,no) for p,n,no in ok_pairs if p == word]
        n_word_prev = len(word_prev_pairs)
        if n_word_prev < 3: continue
        same_cnt = sum(1 for p,n,no in word_prev_pairs if n == word)
        any_ok_cnt = sum(1 for p,n,no in word_prev_pairs if no == 'ok')
        E_self = (same_cnt / max(n_word_prev, 1)) / max(freq/max(total_ok_words, 1), 0.001) if freq > 0 else 0
        print(f"  {word:<15} {n_word_prev:>8} {100*same_cnt/max(n_word_prev,1):>7.1f}% {100*any_ok_cnt/max(n_word_prev,1):>9.1f}% {baseline_ok_pct:>13.1f}% {E_self:>7.2f}×")

    # Folio-level clustering: how many ok→ok pairs are within the same folio?
    print(f"\n--- ok→ok by position in line ---")
    pos_ok_ok = Counter()
    pos_ok_nonok = Counter()
    for wlist in cont_lines:
        n = len(wlist)
        for i in range(n-1):
            prev = wlist[i]
            nxt = wlist[i+1]
            if get_onset(prev) != 'ok': continue
            pos = 'LF' if i == 0 else ('LL' if i == n-2 else 'MID')
            if get_onset(nxt) == 'ok':
                pos_ok_ok[pos] += 1
            else:
                pos_ok_nonok[pos] += 1
    
    print(f"{'Position':<12} {'ok→ok':>8} {'ok→non-ok':>11} {'ok→ok%':>9}")
    for pos in ['LF','MID','LL']:
        a = pos_ok_ok[pos]
        b = pos_ok_nonok[pos]
        tot = a + b
        print(f"  {pos:<12} {a:>8} {b:>11} {100*a/max(tot,1):>8.1f}%")

