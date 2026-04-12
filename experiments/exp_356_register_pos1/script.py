"""
exp_356: Register pos1 Distribution (H563 + H564)

Background:
- F357 (exp_355): A-dialect folio-closer pos1 = ch elevated (E=1.34×), sh depleted (E=0.16×)
- H563: What onset follows the gallows LF word at folio-opener pos1?
- H564: Does B-dialect folio-closer also show elevated ch and depleted sh at pos1?

Plan:
1. Collect all three registers (opener, continuation, closer) for both dialects
2. For each register and each dialect, compute pos1 onset distribution
3. Cross-register and cross-dialect comparison table
4. Also compute the pos1 onset conditional on LF onset for folio-opener (is t excluded?)
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

def is_gallows(word):
    return get_onset(word) in ('k', 't', 'p', 'f')

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
folio_lines = defaultdict(list)  # fb -> list of (line_num, words, dialect)

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

# Classify lines into registers
# register_data[dialect][register] = list of word lists
register_data = defaultdict(lambda: defaultdict(list))

for fb, lines_list in folio_lines.items():
    if not lines_list: continue
    dialect = lines_list[0][2]
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln = min(line_nums)
    max_ln = max(line_nums)

    for ln, words, d in lines_list:
        if ln == min_ln:
            register_data[dialect]['opener'].append(words)
        elif ln == max_ln:
            register_data[dialect]['closer'].append(words)
        else:
            register_data[dialect]['cont'].append(words)

# Core analysis: pos1 onset distribution by register and dialect
print("=" * 70)
print("pos1 ONSET DISTRIBUTION BY REGISTER AND DIALECT")
print("=" * 70)

KEY_ONSETS = ['ch', 'sh', 'd', 'k', 'y', 's', 'cth', 'qok', 'ok', 'ot', 'ol', 'l', 'p', 't', 'other']

for dialect in ['A', 'B']:
    print(f"\n{'='*70}")
    print(f"{dialect}-DIALECT pos1 DISTRIBUTION BY REGISTER")
    print(f"{'='*70}")

    for register in ['opener', 'cont', 'closer']:
        lines = register_data[dialect][register]
        if not lines: continue
        pos1_words = [words[1] for words in lines if len(words) >= 2]
        n = len(pos1_words)
        onset_c = Counter(get_onset(w) for w in pos1_words)

        print(f"\n  {dialect} {register} pos1 (N={n}):")
        for onset in KEY_ONSETS:
            cnt = onset_c.get(onset, 0)
            pct = 100 * cnt / n if n > 0 else 0
            if pct >= 1.5 or onset in ('ch', 'sh', 'd'):
                print(f"    {onset:<8} {cnt:>4} ({pct:.1f}%)")

# Comparative table: ch and sh at pos1 across all 6 register×dialect combinations
print("\n" + "=" * 70)
print("COMPARATIVE TABLE: ch% and sh% at pos1 ACROSS REGISTERS")
print("=" * 70)
print(f"\n  {'Dialect':<8} {'Register':<12} {'N':>6} {'ch%':>8} {'sh%':>8} {'ch/sh_ratio':>12} {'d%':>7} {'cth%':>7} {'k%':>7}")
for dialect in ['A', 'B']:
    for register in ['opener', 'cont', 'closer']:
        lines = register_data[dialect][register]
        if not lines: continue
        pos1_words = [words[1] for words in lines if len(words) >= 2]
        n = len(pos1_words)
        if n == 0: continue
        onset_c = Counter(get_onset(w) for w in pos1_words)
        ch_pct = 100 * onset_c.get('ch', 0) / n
        sh_pct = 100 * onset_c.get('sh', 0) / n
        d_pct = 100 * onset_c.get('d', 0) / n
        cth_pct = 100 * onset_c.get('cth', 0) / n
        k_pct = 100 * onset_c.get('k', 0) / n
        ratio = ch_pct / sh_pct if sh_pct > 0 else float('inf')
        print(f"  {dialect:<8} {register:<12} {n:>6} {ch_pct:>7.1f}%  {sh_pct:>7.1f}%  {ratio:>11.2f}  {d_pct:>6.1f}%  {cth_pct:>6.1f}%  {k_pct:>6.1f}%")

# For folio-opener pos1: check t-onset exclusion (paragraph grammar has 0/258 at pos=1)
print("\n" + "=" * 70)
print("FOLIO-OPENER pos1: t-ONSET EXCLUSION TEST (cf. paragraph-level 0/258)")
print("=" * 70)
for dialect in ['A', 'B']:
    opener_lines = register_data[dialect]['opener']
    pos1_words = [words[1] for words in opener_lines if len(words) >= 2]
    n = len(pos1_words)
    t_count = sum(1 for w in pos1_words if get_onset(w) == 't')
    p_count = sum(1 for w in pos1_words if get_onset(w) == 'p')
    k_count = sum(1 for w in pos1_words if get_onset(w) == 'k')
    f_count = sum(1 for w in pos1_words if get_onset(w) == 'f')
    print(f"\n{dialect}-dialect folio-opener pos1 (N={n}):")
    print(f"  t: {t_count}/{n} = {100*t_count/n:.1f}%")
    print(f"  p: {p_count}/{n} = {100*p_count/n:.1f}%")
    print(f"  k: {k_count}/{n} = {100*k_count/n:.1f}%")
    print(f"  f: {f_count}/{n} = {100*f_count/n:.1f}%")
    all_gallows = t_count + p_count + k_count + f_count
    print(f"  all gallows: {all_gallows}/{n} = {100*all_gallows/n:.1f}%")

    # Onset distribution
    onset_c = Counter(get_onset(w) for w in pos1_words)
    print(f"\n  Full pos1 onset distribution:")
    for onset, cnt in sorted(onset_c.items(), key=lambda x: -x[1]):
        pct = 100 * cnt / n
        if pct >= 2:
            print(f"    {onset:<8} {cnt:>4} ({pct:.1f}%)")

# Folio-opener pos1 conditioned on LF onset
print("\n" + "=" * 70)
print("FOLIO-OPENER pos1 CONDITIONAL ON LF ONSET (cross-register comparison)")
print("=" * 70)

for dialect in ['A', 'B']:
    print(f"\n{dialect}-dialect: P(pos1_onset | LF_onset)")
    for register in ['opener', 'cont', 'closer']:
        lines = register_data[dialect][register]
        if not lines: continue
        pairs = [(get_onset(words[0]), get_onset(words[1]))
                 for words in lines if len(words) >= 2]
        n_pairs = len(pairs)
        pair_c = Counter(pairs)
        lf_c = Counter(o1 for o1, o2 in pairs)
        p1_c = Counter(o2 for o1, o2 in pairs)

        print(f"\n  {register} (N={n_pairs}):")
        print(f"  LF onset profile: " + ", ".join(f"{o}={100*cnt/n_pairs:.0f}%" for o, cnt in lf_c.most_common(6)))
        print(f"  pos1 ch: {100*p1_c.get('ch',0)/n_pairs:.1f}%  sh: {100*p1_c.get('sh',0)/n_pairs:.1f}%  d: {100*p1_c.get('d',0)/n_pairs:.1f}%")

# B-dialect folio-closer: full positional profile
print("\n" + "=" * 70)
print("B-DIALECT FOLIO-CLOSER: COMPLETE POSITIONAL PROFILE")
print("=" * 70)

closer_B = register_data['B']['closer']
print(f"\nB-dialect folio-closer lines (N={len(closer_B)}):")

pos_data = defaultdict(list)
for words in closer_B:
    n = len(words)
    for i, w in enumerate(words):
        if i == 0:
            pos_data['LF'].append(w)
        elif i == n - 1:
            pos_data['LL'].append(w)
        elif i == 1:
            pos_data['pos1'].append(w)
        elif i == 2:
            pos_data['pos2'].append(w)
        else:
            pos_data['MID_rest'].append(w)

print(f"\n{'Position':<12} {'N':>6} {'ch%':>8} {'sh%':>8} {'gallows%':>10} {'top_onset':>14}")
for pos in ['LF', 'pos1', 'pos2', 'MID_rest', 'LL']:
    words = pos_data[pos]
    if not words: continue
    n = len(words)
    onset_c = Counter(get_onset(w) for w in words)
    ch_pct = 100 * onset_c.get('ch', 0) / n
    sh_pct = 100 * onset_c.get('sh', 0) / n
    g_pct = 100 * sum(1 for w in words if is_gallows(w)) / n
    top = onset_c.most_common(1)[0][0]
    top_pct = 100 * onset_c.most_common(1)[0][1] / n
    print(f"  {pos:<12} {n:>6} {ch_pct:>7.1f}%  {sh_pct:>7.1f}%  {g_pct:>9.1f}%  {top}={top_pct:.0f}%")

# Compute B folio-closer sh at pos1 conditional on LF onset
print("\n  B-dialect folio-closer: sh at pos1 conditional on LF onset:")
lf_sh_closer_B = defaultdict(lambda: [0, 0])  # lf_onset -> [sh_count, total]
for words in closer_B:
    if len(words) >= 2:
        lf_onset = get_onset(words[0])
        pos1_onset = get_onset(words[1])
        lf_sh_closer_B[lf_onset][1] += 1
        if pos1_onset == 'sh':
            lf_sh_closer_B[lf_onset][0] += 1

for lf_onset, (sh_cnt, tot) in sorted(lf_sh_closer_B.items(), key=lambda x: -x[1][1]):
    if tot >= 2:
        print(f"    LF={lf_onset}: {sh_cnt}/{tot} = {100*sh_cnt/tot:.1f}% sh at pos1")
