"""
exp_366: A-Dialect Positional Onset-Class Enrichment Matrix (H579)

Tests: For A-dialect continuation lines, compute P(onset_class at position) for each
position category. Specifically:
1. Full onset × position enrichment matrix (E = P(onset at slot) / P(onset at MID_inner))
2. d-onset decomposition: is LL enrichment from daiin alone, or all d-onset words?
3. d→d succession E in continuation lines (class-level memory test)
4. B-dialect comparison for contrast

H541 (open): A-dialect daiin LL enrichment — is it word-specific or class-wide?
H579 (new): Full A-dialect onset positional matrix; d-class LL affinity vs daiin formula.
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
print("A-DIALECT POSITIONAL ONSET-CLASS ENRICHMENT MATRIX (H579/H541)")
print("="*70)

KEY_ONSETS = ['d', 'ch', 'sh', 'qok', 'ok', 'ot', 'qot', 'y', 'ol', 's', 'k', 'p', 't', 'f', 'other']

for DIALECT in ('A', 'B'):
    cont_lines = register_lines[DIALECT]['cont']
    print(f"\n{'='*60}")
    print(f"DIALECT {DIALECT}: N_cont_lines={len(cont_lines)}")
    print(f"{'='*60}")

    # Collect words by position category
    pos_words = {'LF': [], 'pos1': [], 'MID_inner': [], 'pre_LL': [], 'LL': []}

    for words in cont_lines:
        n = len(words)
        if n < 2:
            continue
        for idx, w in enumerate(words):
            if idx == 0:
                pos_words['LF'].append(w)
            if idx == 1 and n >= 3:
                pos_words['pos1'].append(w)
            if idx == n - 1:
                pos_words['LL'].append(w)
            if idx == n - 2 and n >= 3:
                pos_words['pre_LL'].append(w)
            if 2 <= idx <= n - 3 and n >= 5:
                pos_words['MID_inner'].append(w)

    # MID_inner baseline
    mid_total = len(pos_words['MID_inner'])
    mid_counts = Counter(get_onset(w) for w in pos_words['MID_inner'])

    print(f"\nPosition counts: LF={len(pos_words['LF'])}, pos1={len(pos_words['pos1'])}, "
          f"MID={mid_total}, pre_LL={len(pos_words['pre_LL'])}, LL={len(pos_words['LL'])}")

    print(f"\n{'Onset':<8}", end='')
    for pos in ['LF', 'pos1', 'MID_inner', 'pre_LL', 'LL']:
        print(f"  {pos:<12}", end='')
    print()
    print('-'*72)

    for onset in KEY_ONSETS:
        baseline_p = mid_counts[onset] / mid_total if mid_total > 0 else 0
        print(f"{onset:<8}", end='')
        for pos in ['LF', 'pos1', 'MID_inner', 'pre_LL', 'LL']:
            pos_cnt = Counter(get_onset(w) for w in pos_words[pos])
            pos_total = len(pos_words[pos])
            p = pos_cnt[onset] / pos_total if pos_total > 0 else 0
            if baseline_p > 0:
                e = p / baseline_p
                print(f"  {p*100:4.1f}%({e:4.2f}×)", end='')
            else:
                print(f"  {p*100:4.1f}%(  -  )", end='')
        print()

    # d-onset decomposition at each position
    print(f"\n--- {DIALECT}: d-onset decomposition (daiin vs d-not-daiin) ---")
    for d_sub in ['daiin', 'd_not_daiin']:
        print(f"  {d_sub:<16}", end='')
        for pos in ['LF', 'pos1', 'MID_inner', 'pre_LL', 'LL']:
            pos_total = len(pos_words[pos])
            if d_sub == 'daiin':
                cnt = sum(1 for w in pos_words[pos] if w == 'daiin')
            else:
                cnt = sum(1 for w in pos_words[pos] if get_onset(w) == 'd' and w != 'daiin')
            p = cnt / pos_total * 100 if pos_total > 0 else 0
            print(f"  {cnt:4d}({p:4.1f}%)", end='')
        print()

    # E values for daiin vs d-not-daiin
    mid_total_val = len(pos_words['MID_inner'])
    ll_total = len(pos_words['LL'])
    daiin_mid = sum(1 for w in pos_words['MID_inner'] if w == 'daiin')
    d_other_mid = sum(1 for w in pos_words['MID_inner'] if get_onset(w) == 'd' and w != 'daiin')
    daiin_ll = sum(1 for w in pos_words['LL'] if w == 'daiin')
    d_other_ll = sum(1 for w in pos_words['LL'] if get_onset(w) == 'd' and w != 'daiin')

    if daiin_mid > 0 and ll_total > 0:
        E_daiin = (daiin_ll / ll_total) / (daiin_mid / mid_total_val)
        print(f"  daiin LL/MID enrichment: E={E_daiin:.2f}× ({daiin_ll/ll_total*100:.1f}% vs {daiin_mid/mid_total_val*100:.1f}%)")
    if d_other_mid > 0 and ll_total > 0:
        E_d_other = (d_other_ll / ll_total) / (d_other_mid / mid_total_val)
        print(f"  d-other LL/MID enrichment: E={E_d_other:.2f}× ({d_other_ll/ll_total*100:.1f}% vs {d_other_mid/mid_total_val*100:.1f}%)")

    # Top d words at each position
    print(f"\n  {DIALECT}: Top d-onset words at LL:")
    d_at_ll = [w for w in pos_words['LL'] if get_onset(w) == 'd']
    for word, cnt in Counter(d_at_ll).most_common(10):
        print(f"    {word}: {cnt} ({cnt/ll_total*100:.1f}%)")

    print(f"\n  {DIALECT}: Top d-onset words at LF:")
    d_at_lf = [w for w in pos_words['LF'] if get_onset(w) == 'd']
    lf_total = len(pos_words['LF'])
    for word, cnt in Counter(d_at_lf).most_common(8):
        print(f"    {word}: {cnt} ({cnt/lf_total*100:.1f}%)")

    print(f"\n  {DIALECT}: Top d-onset words at MID_inner:")
    d_at_mid = [w for w in pos_words['MID_inner'] if get_onset(w) == 'd']
    for word, cnt in Counter(d_at_mid).most_common(8):
        print(f"    {word}: {cnt} ({cnt/mid_total_val*100:.1f}%)")

    # d→d succession test
    print(f"\n--- {DIALECT}: d-onset succession in continuation lines ---")
    d_next_total = 0
    d_next_d = 0
    daiin_next_total = 0
    daiin_next_d = 0
    top_d_pairs = Counter()
    for words in cont_lines:
        for i in range(len(words) - 1):
            if get_onset(words[i]) == 'd':
                d_next_total += 1
                if get_onset(words[i+1]) == 'd':
                    d_next_d += 1
                    top_d_pairs[(words[i], words[i+1])] += 1
            if words[i] == 'daiin':
                daiin_next_total += 1
                if get_onset(words[i+1]) == 'd':
                    daiin_next_d += 1

    d_baseline = mid_counts['d'] / mid_total if mid_total > 0 else 0
    if d_next_total > 0:
        d_succ_rate = d_next_d / d_next_total
        E_d_succ = d_succ_rate / d_baseline if d_baseline > 0 else float('nan')
        print(f"  d→d: {d_next_d}/{d_next_total} = {d_succ_rate*100:.1f}% (MID baseline {d_baseline*100:.1f}%, E={E_d_succ:.2f}×)")
    if daiin_next_total > 0:
        daiin_d_rate = daiin_next_d / daiin_next_total
        print(f"  daiin→d: {daiin_next_d}/{daiin_next_total} = {daiin_d_rate*100:.1f}%")
    print(f"  Top d→d pairs: {top_d_pairs.most_common(5)}")

print("\n" + "="*70)
print("CROSS-DIALECT SUMMARY: d-class LL vs MID enrichment")
print("="*70)
for DIALECT in ('A', 'B'):
    cont_lines = register_lines[DIALECT]['cont']
    mid_words = []
    ll_words = []
    for words in cont_lines:
        n = len(words)
        if n < 2: continue
        ll_words.append(words[-1])
        for idx, w in enumerate(words):
            if 2 <= idx <= n-3 and n >= 5:
                mid_words.append(w)
    if not mid_words: continue
    mid_d = sum(1 for w in mid_words if get_onset(w) == 'd')
    ll_d = sum(1 for w in ll_words if get_onset(w) == 'd')
    mid_daiin = sum(1 for w in mid_words if w == 'daiin')
    ll_daiin = sum(1 for w in ll_words if w == 'daiin')
    mid_d_other = mid_d - mid_daiin
    ll_d_other = ll_d - ll_daiin
    mt, lt = len(mid_words), len(ll_words)
    E_d = (ll_d/lt) / (mid_d/mt) if mid_d > 0 else float('nan')
    E_daiin = (ll_daiin/lt) / (mid_daiin/mt) if mid_daiin > 0 else float('nan')
    E_d_oth = (ll_d_other/lt) / (mid_d_other/mt) if mid_d_other > 0 else float('nan')
    print(f"{DIALECT}: d-class E(LL/MID)={E_d:.2f}×  daiin E={E_daiin:.2f}×  d-other E={E_d_oth:.2f}×")
    print(f"   d at LL={ll_d/lt*100:.1f}% ({ll_d}/{lt}), MID={mid_d/mt*100:.1f}% ({mid_d}/{mt})")
    print(f"   daiin at LL={ll_daiin/lt*100:.1f}%, MID={mid_daiin/mt*100:.1f}%")
    print(f"   d-other at LL={ll_d_other/lt*100:.1f}%, MID={mid_d_other/mt*100:.1f}%")
