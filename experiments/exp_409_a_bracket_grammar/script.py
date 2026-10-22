"""
exp_409: A Bracket Grammar for Other LF Classes (H624)

For A continuation lines (≥4 words), for each LF class:
1. Compute pos1 onset distribution (enrichment vs baseline)
2. Compute LL onset distribution (enrichment vs baseline)
3. For each (pos1_onset, LL_onset) pair: compute joint count and expected count under independence
   E_bracket = (joint_count / N_lf) / (pos1_rate × ll_rate)
4. Identify any bracket (pos1=X, LL=Y) with E_bracket ≥ 1.5 and N ≥ 3

We already know: A p → sh-bracket (pos1=sh 1.66×, LL=sh 3.52×, joint E=1.80×, N=3).
H624 asks: do A qot / s / d / y / other LF classes show bracket structure?
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

# Pass 2: collect A cont lines (length >= 4)
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
        if folio_dialect.get(fb, 'A') != 'A':
            continue
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((ln, words))

a_cont_lines = []
for fb, entries in folio_lines.items():
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in entries:
        if ln != min_ln and ln != max_ln and len(words) >= 4:
            a_cont_lines.append(words)

print(f"A cont lines (len>=4): {len(a_cont_lines)}")

# Compute baseline pos1 and LL rates across all A cont lines
baseline_pos1 = Counter()
baseline_ll = Counter()
for words in a_cont_lines:
    onsets = [get_onset(w) for w in words]
    baseline_pos1[onsets[1]] += 1
    baseline_ll[onsets[-1]] += 1

total_p1 = sum(baseline_pos1.values())
total_ll = sum(baseline_ll.values())

# For each LF class: compute pos1, LL, and joint (pos1, LL) distributions
LF_CLASSES = ['d', 'y', 's', 'qok', 'p', 't', 'sh', 'ch', 'o', 'ok', 'qot', 'ot', 'k', 'qo', 'ol', 'other']

lf_counts = Counter()
lf_pos1 = defaultdict(Counter)  # lf -> Counter of pos1 onsets
lf_ll = defaultdict(Counter)    # lf -> Counter of LL onsets
lf_bracket = defaultdict(Counter)  # lf -> Counter of (pos1, LL) pairs

for words in a_cont_lines:
    onsets = [get_onset(w) for w in words]
    lf = onsets[0]
    p1 = onsets[1]
    ll = onsets[-1]
    lf_counts[lf] += 1
    lf_pos1[lf][p1] += 1
    lf_ll[lf][ll] += 1
    lf_bracket[lf][(p1, ll)] += 1

# For each LF class with N >= 10, report pos1/LL enrichment and bracket analysis
print("\n=== Per-LF-class bracket analysis ===")

bracket_threshold_E = 1.5
bracket_threshold_N = 3

for lf in LF_CLASSES:
    n_lf = lf_counts[lf]
    if n_lf < 10:
        continue
    print(f"\n--- LF='{lf}' (N={n_lf}) ---")

    # Top pos1 classes (enriched)
    p1_enriched = []
    for onset, cnt in lf_pos1[lf].most_common(20):
        base = baseline_pos1[onset] / total_p1
        if base == 0:
            continue
        E = (cnt / n_lf) / base
        p1_enriched.append((onset, cnt, E))
    p1_enriched.sort(key=lambda x: -x[2])
    top_p1 = [(o, n, e) for o, n, e in p1_enriched if e >= 1.3 and n >= 2][:5]
    if top_p1:
        print(f"  pos1 enriched: {[(o, n, f'{e:.2f}×') for o, n, e in top_p1]}")

    # Top LL classes (enriched)
    ll_enriched = []
    for onset, cnt in lf_ll[lf].most_common(20):
        base = baseline_ll[onset] / total_ll
        if base == 0:
            continue
        E = (cnt / n_lf) / base
        ll_enriched.append((onset, cnt, E))
    ll_enriched.sort(key=lambda x: -x[2])
    top_ll = [(o, n, e) for o, n, e in ll_enriched if e >= 1.3 and n >= 2][:5]
    if top_ll:
        print(f"  LL enriched: {[(o, n, f'{e:.2f}×') for o, n, e in top_ll]}")

    # Bracket analysis: (pos1, LL) pairs
    brackets = []
    for (p1, ll_onset), cnt in lf_bracket[lf].items():
        if cnt < bracket_threshold_N:
            continue
        # Expected under independence
        rate_p1 = lf_pos1[lf][p1] / n_lf
        rate_ll = lf_ll[lf][ll_onset] / n_lf
        expected = rate_p1 * rate_ll * n_lf
        if expected < 0.5:
            continue
        E_bkt = cnt / expected
        brackets.append((p1, ll_onset, cnt, expected, E_bkt))
    brackets.sort(key=lambda x: -x[4])
    top_brackets = [(b[0], b[1], b[2], f'{b[3]:.1f}', f'{b[4]:.2f}×') for b in brackets
                    if b[4] >= bracket_threshold_E][:6]
    if top_brackets:
        print(f"  BRACKETS (E>=1.5, N>=3): {top_brackets}")
    else:
        print(f"  No strong brackets (E>=1.5, N>=3)")

    # SAME-onset bracket (pos1 = LL = same onset)
    same_onset_brackets = [(p1, c) for (p1, ll_onset), c in lf_bracket[lf].items()
                           if p1 == ll_onset and c >= 2]
    if same_onset_brackets:
        same_onset_brackets.sort(key=lambda x: -x[1])
        print(f"  Same-onset bracket (pos1=LL): {same_onset_brackets[:5]}")

# Summary: all same-onset brackets across LF classes
print("\n=== All same-onset bracket enrichment (pos1=LL=X) per LF class ===")
for lf in LF_CLASSES:
    n_lf = lf_counts[lf]
    if n_lf < 10:
        continue
    for onset in set(lf_pos1[lf].keys()) | set(lf_ll[lf].keys()):
        cnt = lf_bracket[lf].get((onset, onset), 0)
        if cnt < 2:
            continue
        rate_p1 = lf_pos1[lf][onset] / n_lf
        rate_ll = lf_ll[lf][onset] / n_lf
        expected = rate_p1 * rate_ll * n_lf
        if expected < 0.5:
            continue
        E_bkt = cnt / expected
        print(f"  LF={lf}, pos1=LL={onset}: n={cnt}, expected={expected:.1f}, E={E_bkt:.2f}×")

print("\n=== Done ===")
