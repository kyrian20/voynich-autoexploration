"""
exp_390: B r at pos1 — Word-Level Analysis (H602)

Extracts all B continuation lines where pos1-onset = r.
Analyzes: which LF words produce r at pos1, which r words appear at pos1,
line structure after r at pos1.
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

# Collect B continuation lines with r at pos1
b_r_pos1_lines = []
b_all_pos1_lf = Counter()
b_r_pos1_lf = Counter()
b_r_pos1_word = Counter()
b_r_pos1_ll = Counter()  # LL word when r at pos1
b_lf_all = Counter()

for fb, lines_list in folio_lines.items():
    if not lines_list:
        continue
    dialect = lines_list[0][2]
    if dialect != 'B':
        continue
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln, max_ln = min(line_nums), max(line_nums)
    for ln, words, d in lines_list:
        if ln == min_ln or ln == max_ln:
            continue
        n = len(words)
        if n < 2:
            continue
        lf_word = words[0]
        lf_onset = get_onset(lf_word)
        b_lf_all[lf_onset] += 1
        p1_word = words[1]
        p1_onset = get_onset(p1_word)
        b_all_pos1_lf[lf_onset] += 1
        if p1_onset == 'r':
            b_r_pos1_lf[lf_onset] += 1
            b_r_pos1_word[p1_word] += 1
            ll_word = words[-1] if n >= 2 else None
            if ll_word:
                b_r_pos1_ll[ll_word] += 1
            b_r_pos1_lines.append((lf_word, words, fb, ln))

print(f"B continuation lines: {sum(b_all_pos1_lf.values())}")
print(f"B lines with r at pos1: {sum(b_r_pos1_lf.values())}")
print(f"Total B lines: {sum(b_all_pos1_lf.values())}")
print(f"B pos1 r rate: {sum(b_r_pos1_lf.values())/sum(b_all_pos1_lf.values())*100:.2f}%")

print(f"\n--- B r at pos1: Which LF onsets produce r at pos1? ---")
total_r_pos1 = sum(b_r_pos1_lf.values())
total_lines = sum(b_all_pos1_lf.values())
print(f"LF onset | r@pos1 N | total LF N | r@pos1 rate | baseline r@pos1 | E")
for onset in ['qok', 'qot', 'ok', 'ot', 's', 'y', 'd', 'ch', 'sh', 'ol', 'p', 't', 'k', 'f', 'r']:
    n_r = b_r_pos1_lf.get(onset, 0)
    n_total_lf = b_all_pos1_lf.get(onset, 0)
    if n_total_lf == 0:
        continue
    rate = n_r / n_total_lf
    baseline = total_r_pos1 / total_lines
    e = rate / baseline if baseline > 0 else float('nan')
    flag = "**" if e >= 2.0 else ("*" if e >= 1.5 else ("" if e >= 0.5 else "--"))
    print(f"  {onset:<8} {n_r:>8} {n_total_lf:>12} {rate*100:>12.1f}% {baseline*100:>16.1f}% {e:>6.2f} {flag}")

print(f"\n--- B r pos1 word inventory ---")
print(f"Total r words at pos1: {total_r_pos1}")
for word, count in b_r_pos1_word.most_common(20):
    print(f"  {word}: {count} ({count/total_r_pos1*100:.1f}%)")

# Compare r words at pos1 vs r words at LL
print(f"\n--- Compare B r vocab: pos1 vs LL ---")
# Collect r at LL
b_r_ll_word = Counter()
for fb, lines_list in folio_lines.items():
    if not lines_list:
        continue
    dialect = lines_list[0][2]
    if dialect != 'B':
        continue
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln, max_ln = min(line_nums), max(line_nums)
    for ln, words, d in lines_list:
        if ln == min_ln or ln == max_ln:
            continue
        n = len(words)
        ll_word = words[-1] if n >= 1 else None
        if ll_word and get_onset(ll_word) == 'r':
            b_r_ll_word[ll_word] += 1

print(f"B r words at LL: {sum(b_r_ll_word.values())}")
print("Top B r LL words:")
for word, count in b_r_ll_word.most_common(10):
    print(f"  {word}: {count}")

print(f"\nTop B r pos1 words vs LL words overlap:")
all_r_words = set(b_r_pos1_word.keys()) | set(b_r_ll_word.keys())
for w in sorted(all_r_words, key=lambda x: -(b_r_pos1_word.get(x, 0) + b_r_ll_word.get(x, 0))):
    n_p1 = b_r_pos1_word.get(w, 0)
    n_ll = b_r_ll_word.get(w, 0)
    if n_p1 + n_ll >= 2:
        print(f"  {w}: pos1={n_p1}, LL={n_ll}")

# Print actual lines with r at pos1 for specific LF classes
print(f"\n--- Actual lines with r at pos1 (LF onset in qok/qot/y) ---")
for lf_word, words, fb, ln in b_r_pos1_lines:
    lf_onset = get_onset(lf_word)
    if lf_onset in ('qok', 'qot', 'y', 'ol', 'r'):
        onset_seq = [get_onset(w) for w in words]
        print(f"  [{fb}/{ln}] LF_onset={lf_onset}: {' '.join(words[:min(8,len(words))])}")
        print(f"    onsets: {' '.join(onset_seq[:min(8,len(words))])}")

