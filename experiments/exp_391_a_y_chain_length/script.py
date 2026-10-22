"""
exp_391: A y Self-Chain Length Distribution (H608)

Analyzes A-dialect y-onset runs (consecutive y-onset positions) in continuation lines.
Tests whether y chain extends to 4+ positions above baseline.
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
    return re.sub(r'[rv]$', '', folio)

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

# Analyze y-run lengths in each dialect
def analyze_y_runs(dialect_target):
    runs = []  # all y-run lengths found
    total_words = 0
    total_y_words = 0
    long_runs = []  # runs of length >= 3

    for fb, lines_list in folio_lines.items():
        if not lines_list:
            continue
        dialect = lines_list[0][2]
        if dialect != dialect_target:
            continue
        line_nums = [ln for ln, _, _ in lines_list]
        min_ln, max_ln = min(line_nums), max(line_nums)
        for ln, words, d in lines_list:
            if ln == min_ln or ln == max_ln:
                continue  # continuation only
            onsets = [get_onset(w) for w in words]
            total_words += len(words)
            total_y_words += sum(1 for o in onsets if o == 'y')
            # Find y-runs
            i = 0
            while i < len(onsets):
                if onsets[i] == 'y':
                    run_start = i
                    while i < len(onsets) and onsets[i] == 'y':
                        i += 1
                    run_len = i - run_start
                    runs.append(run_len)
                    if run_len >= 3:
                        long_runs.append((words[run_start:i], fb, ln))
                else:
                    i += 1

    return runs, total_words, total_y_words, long_runs

print(f"{'='*70}")
print(f"A-DIALECT y-CHAIN LENGTH ANALYSIS")
print(f"{'='*70}")
A_runs, A_total, A_y, A_long = analyze_y_runs('A')
A_run_dist = Counter(A_runs)
print(f"Total A continuation words: {A_total}")
print(f"Total A y words: {A_y} ({A_y/A_total*100:.1f}%)")
print(f"Total A y-runs (consecutive y sequences): {len(A_runs)}")
print(f"\nA y-run length distribution:")
for length in sorted(A_run_dist.keys()):
    count = A_run_dist[length]
    print(f"  Length {length}: {count} runs")

# Expected distribution under random (geometric) model
import math
p_y = A_y / A_total
print(f"\nExpected under random model (P(y)={p_y:.3f}):")
print(f"  Expected P(run>=k) | run starts as:")
total_runs_all = len(A_runs)
for length in range(1, 6):
    expected = total_runs_all * ((p_y ** (length - 1)) * (1 - p_y))
    observed = A_run_dist.get(length, 0)
    print(f"  Length {length}: expected≈{expected:.1f}, observed={observed}")

print(f"\nA y-runs of length ≥ 3:")
for run_words, fb, ln in A_long:
    print(f"  [{fb}/{ln}] {' '.join(run_words)}")

print(f"\n{'='*70}")
print(f"B-DIALECT y-CHAIN LENGTH ANALYSIS (comparison)")
print(f"{'='*70}")
B_runs, B_total, B_y, B_long = analyze_y_runs('B')
B_run_dist = Counter(B_runs)
print(f"Total B continuation words: {B_total}")
print(f"Total B y words: {B_y} ({B_y/B_total*100:.1f}%)")
print(f"Total B y-runs: {len(B_runs)}")
print(f"\nB y-run length distribution:")
for length in sorted(B_run_dist.keys()):
    count = B_run_dist[length]
    print(f"  Length {length}: {count} runs")

print(f"\nB y-runs of length ≥ 3:")
for run_words, fb, ln in B_long:
    print(f"  [{fb}/{ln}] {' '.join(run_words)}")

# Also check y-start runs: consecutive y starting from LF position
print(f"\n{'='*70}")
print(f"y-RUNS STARTING AT LF (both dialects)")
print(f"{'='*70}")
for dialect_target in ['A', 'B']:
    lf_y_runs = []
    for fb, lines_list in folio_lines.items():
        if not lines_list:
            continue
        dialect = lines_list[0][2]
        if dialect != dialect_target:
            continue
        line_nums = [ln for ln, _, _ in lines_list]
        min_ln, max_ln = min(line_nums), max(line_nums)
        for ln, words, d in lines_list:
            if ln == min_ln or ln == max_ln:
                continue
            onsets = [get_onset(w) for w in words]
            if onsets[0] != 'y':
                continue
            run_len = 0
            for o in onsets:
                if o == 'y':
                    run_len += 1
                else:
                    break
            lf_y_runs.append(run_len)
    run_dist = Counter(lf_y_runs)
    print(f"\n{dialect_target}-dialect LF-starting y-runs:")
    for length in sorted(run_dist.keys()):
        print(f"  LF-run length {length}: {run_dist[length]} lines")

