"""
exp_355: A-Dialect Folio-Closer y→ch Onset Sequence (H562)

Background:
- F356 (exp_354): A-dialect folio-closer pos1 (second word) = ch dominant (40%).
  LF onsets: y=23%, d=19%, ch=13%. The question: is the ch dominance at pos1
  specifically driven by y-onset LF words being followed by ch at pos1, or is
  this a general folio-closer rule where any LF onset is followed by ch?

Plan:
1. Collect A-dialect folio-closer lines with at least 2 words
2. Compute P(pos1_onset | LF_onset) as conditional table
3. Compare to continuation line P(next_word_onset | prev_word_onset)
4. Focus on: when LF=y, what onset follows? When LF=d/ch/s, what follows?
5. Also check: in continuation lines, does y→ch succession appear at LF→pos1?
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
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

# Pass 2: collect line data
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
        if dialect != 'A': continue
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'): continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if len(words) < 2: continue
        folio_lines[fb].append((line_num, words))

# Classify lines
closer_lines = []   # (words,)
cont_lines = []     # (words,)

for fb, lines_list in folio_lines.items():
    line_nums = [ln for ln, _ in lines_list]
    min_ln = min(line_nums)
    max_ln = max(line_nums)

    for ln, words in lines_list:
        if ln == max_ln and ln != min_ln:
            closer_lines.append(words)
        elif ln != min_ln:
            cont_lines.append(words)

print(f"A-dialect folio-closer lines: N={len(closer_lines)}")
print(f"A-dialect continuation lines: N={len(cont_lines)}")

# Analysis 1: Conditional P(pos1_onset | LF_onset) for folio-closer
print("\n" + "=" * 65)
print("A-DIALECT FOLIO-CLOSER: P(pos1_onset | LF_onset)")
print("=" * 65)

# Group closer lines by LF onset
lf_cond_closer = defaultdict(list)
for words in closer_lines:
    lf_onset = get_onset(words[0])
    pos1_onset = get_onset(words[1])
    lf_cond_closer[lf_onset].append(pos1_onset)

# Also compute marginal distribution of pos1 onset (unconditional)
all_pos1_closer = [get_onset(words[1]) for words in closer_lines if len(words) >= 2]
pos1_marginal_closer = Counter(all_pos1_closer)
n_closer = len(all_pos1_closer)

print(f"\nUnconditional pos1 onset distribution (N={n_closer}):")
for onset, cnt in sorted(pos1_marginal_closer.items(), key=lambda x: -x[1]):
    pct = 100*cnt/n_closer
    if pct >= 2:
        print(f"  {onset:<8} {cnt:>3} ({pct:.1f}%)")

# Compare to continuation line P(next_word | LF) distribution
# To be comparable, we look at the second word of continuation lines
all_pos1_cont = [get_onset(words[1]) for words in cont_lines if len(words) >= 2]
pos1_marginal_cont = Counter(all_pos1_cont)
n_pos1_cont = len(all_pos1_cont)

print(f"\nCont lines pos1 onset distribution (N={n_pos1_cont}):")
for onset, cnt in sorted(pos1_marginal_cont.items(), key=lambda x: -x[1])[:8]:
    pct = 100*cnt/n_pos1_cont
    if pct >= 2:
        print(f"  {onset:<8} {cnt:>3} ({pct:.1f}%)")

# Conditional tables for top LF onsets
top_lf_onsets = ['y', 'd', 'ch', 's', 'o', 'p', 'k', 't']

print(f"\nConditional P(pos1 onset | LF onset) — FOLIO-CLOSER lines:")
print(f"{'LF_onset':<10} {'N_lines':>8} {'ch_pct':>10} {'d_pct':>8} {'y_pct':>8} {'s_pct':>8} {'other_top':>15}")
for lf_onset in top_lf_onsets:
    pos1_list = lf_cond_closer.get(lf_onset, [])
    n = len(pos1_list)
    if n == 0:
        print(f"  {lf_onset:<10} {n:>8} {'—':>10}")
        continue
    pos1_c = Counter(pos1_list)
    ch_pct = 100 * pos1_c.get('ch', 0) / n
    d_pct = 100 * pos1_c.get('d', 0) / n
    y_pct = 100 * pos1_c.get('y', 0) / n
    s_pct = 100 * pos1_c.get('s', 0) / n
    top2 = pos1_c.most_common(2)
    other_top = f"{top2[0][0]}={100*top2[0][1]/n:.0f}%"
    print(f"  {lf_onset:<10} {n:>8} {ch_pct:>9.1f}%  {d_pct:>7.1f}%  {y_pct:>7.1f}%  {s_pct:>7.1f}%  {other_top:>15}")

# For continuation lines, compute same conditional
lf_cond_cont = defaultdict(list)
for words in cont_lines:
    lf_onset = get_onset(words[0])
    pos1_onset = get_onset(words[1])
    lf_cond_cont[lf_onset].append(pos1_onset)

print(f"\nConditional P(pos1 onset | LF onset) — CONTINUATION lines:")
print(f"{'LF_onset':<10} {'N_lines':>8} {'ch_pct':>10} {'d_pct':>8} {'y_pct':>8} {'s_pct':>8} {'other_top':>15}")
for lf_onset in top_lf_onsets:
    pos1_list = lf_cond_cont.get(lf_onset, [])
    n = len(pos1_list)
    if n == 0:
        continue
    pos1_c = Counter(pos1_list)
    ch_pct = 100 * pos1_c.get('ch', 0) / n
    d_pct = 100 * pos1_c.get('d', 0) / n
    y_pct = 100 * pos1_c.get('y', 0) / n
    s_pct = 100 * pos1_c.get('s', 0) / n
    top2 = pos1_c.most_common(2)
    other_top = f"{top2[0][0]}={100*top2[0][1]/n:.0f}%"
    print(f"  {lf_onset:<10} {n:>8} {ch_pct:>9.1f}%  {d_pct:>7.1f}%  {y_pct:>7.1f}%  {s_pct:>7.1f}%  {other_top:>15}")

# Analysis 2: Overall onset bigram y→ch in continuation vs closer
print("\n" + "=" * 65)
print("y→ch ONSET BIGRAM: FOLIO-CLOSER vs CONTINUATION vs WITHIN-LINE MID")
print("=" * 65)

# For all adjacent word pairs in folio-closer lines
closer_bigrams = []
for words in closer_lines:
    for i in range(len(words)-1):
        o1 = get_onset(words[i])
        o2 = get_onset(words[i+1])
        closer_bigrams.append((o1, o2))

cont_bigrams = []
for words in cont_lines:
    for i in range(len(words)-1):
        o1 = get_onset(words[i])
        o2 = get_onset(words[i+1])
        cont_bigrams.append((o1, o2))

# y→ch enrichment
n_closer_bg = len(closer_bigrams)
n_cont_bg = len(cont_bigrams)

closer_bg_c = Counter(closer_bigrams)
cont_bg_c = Counter(cont_bigrams)

def bg_enr(bg_c, target, n_total):
    # Expected under independence: P(o1) * P(o2) * n
    o1, o2 = target
    p_o1 = sum(cnt for (a,b), cnt in bg_c.items() if a == o1) / n_total
    p_o2 = sum(cnt for (a,b), cnt in bg_c.items() if b == o2) / n_total
    expected = p_o1 * p_o2 * n_total
    observed = bg_c.get(target, 0)
    e = observed / expected if expected > 0 else 0
    return observed, expected, e

targets = [('y','ch'), ('y','d'), ('d','ch'), ('ch','ch'), ('s','ch'), ('o','ch')]
print(f"\n{'Bigram':<12} {'Closer_obs':>12} {'Closer_E':>10} | {'Cont_obs':>10} {'Cont_E':>10}")
for target in targets:
    c_obs, c_exp, c_e = bg_enr(closer_bg_c, target, n_closer_bg)
    co_obs, co_exp, co_e = bg_enr(cont_bg_c, target, n_cont_bg)
    print(f"  {target[0]}→{target[1]:<8} {c_obs:>5}/{c_exp:>5.1f}={c_e:>5.2f}×  |  {co_obs:>5}/{co_exp:>5.1f}={co_e:>5.2f}×")

# Analysis 3: Show full folio-closer line word sequences for y-onset LF
print("\n" + "=" * 65)
print("A-DIALECT FOLIO-CLOSER LINES WITH y-ONSET LF: FULL SEQUENCES")
print("=" * 65)
y_closer_lines = [words for words in closer_lines if get_onset(words[0]) == 'y']
print(f"\nN={len(y_closer_lines)} folio-closer lines with y-onset LF:")
for words in y_closer_lines:
    onsets = [get_onset(w) for w in words]
    print(f"  {' '.join(words):<50} onsets: {' '.join(onsets)}")

# Analysis 4: Show continuation lines with y-onset LF for comparison
print("\n" + "=" * 65)
print("A-DIALECT CONTINUATION LINES WITH y-ONSET LF (SAMPLE)")
print("=" * 65)
y_cont_lines = [words for words in cont_lines if get_onset(words[0]) == 'y']
print(f"\nN={len(y_cont_lines)} continuation lines with y-onset LF:")
for words in y_cont_lines[:15]:
    onsets = [get_onset(w) for w in words]
    print(f"  {' '.join(words[:6]):<55} onsets: {' '.join(onsets[:6])}")

# Compute: for y-onset LF lines, what fraction has ch at pos1?
print(f"\nConditional ch at pos1 given y-onset LF:")
n_y_closer = len(y_closer_lines)
n_y_cont = len(y_cont_lines)
ch_y_closer = sum(1 for words in y_closer_lines if len(words)>=2 and get_onset(words[1])=='ch')
ch_y_cont = sum(1 for words in y_cont_lines if len(words)>=2 and get_onset(words[1])=='ch')
print(f"  Folio-closer: {ch_y_closer}/{n_y_closer} = {100*ch_y_closer/n_y_closer:.1f}%")
print(f"  Continuation: {ch_y_cont}/{n_y_cont} = {100*ch_y_cont/n_y_cont:.1f}%")
# Baseline ch at pos1 (all LF types)
ch_pos1_baseline_closer = sum(1 for words in closer_lines if len(words)>=2 and get_onset(words[1])=='ch')
ch_pos1_baseline_cont = sum(1 for words in cont_lines if len(words)>=2 and get_onset(words[1])=='ch')
print(f"  Folio-closer ALL LF types: {ch_pos1_baseline_closer}/{len(closer_lines)} = {100*ch_pos1_baseline_closer/len(closer_lines):.1f}%")
print(f"  Continuation ALL LF types: {ch_pos1_baseline_cont}/{len(cont_lines)} = {100*ch_pos1_baseline_cont/len(cont_lines):.1f}%")
