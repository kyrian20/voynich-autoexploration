"""
exp_419: B ot self-stickiness across all positions (H639)

F419 (exp_416): given pos1=ot in d-LF lines, pos2=ot E=6.34×(N=5).
Is ot self-succession generally elevated in B?
Compare onset self-succession bigrams across all positions in B cont lines
and check ot run-length distribution vs geometric expectation.
"""
from pathlib import Path as _RepositoryPath

import os, re, math
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

# Pass 2: cont lines
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
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        folio_lines[fb].append((ln, words))

cont_lines = {'A': [], 'B': []}
for fb, entries in folio_lines.items():
    dialect = folio_dialect.get(fb, 'A')
    lns = [e[0] for e in entries]
    min_ln, max_ln = min(lns), max(lns)
    for ln, words in entries:
        if ln != min_ln and ln != max_ln:
            cont_lines[dialect].append(words)

# ===== Analysis for each dialect =====
for dialect in ['A', 'B']:
    lines = cont_lines[dialect]
    print(f"\n{'='*60}")
    print(f"=== {dialect} dialect: onset self-succession analysis ===")

    # Collect all bigrams across all positions within lines
    bigrams = Counter()
    onset_total = Counter()
    for words in lines:
        onsets = [get_onset(w) for w in words]
        for o in onsets:
            if o != 'other':
                onset_total[o] += 1
        for i in range(len(onsets)-1):
            o1, o2 = onsets[i], onsets[i+1]
            if o1 != 'other' and o2 != 'other':
                bigrams[(o1, o2)] += 1

    total_bigrams = sum(bigrams.values())
    total_tokens = sum(onset_total.values())

    # Self-succession rate for each onset class
    print(f"\nOnset self-succession rates (E vs independence under marginal frequencies):")
    print(f"{'Onset':6s}  {'N':5s}  {'f':6s}  {'self_n':6s}  {'self_rate':9s}  {'exp_rate':9s}  {'E':6s}")
    for onset in sorted(onset_total.keys(), key=lambda x: -onset_total[x]):
        n_onset = onset_total[onset]
        freq = n_onset / total_tokens
        self_n = bigrams[(onset, onset)]
        # Rate of self-succession: P(next=onset | current=onset)
        n_following_onset = sum(bigrams[(onset, x)] for x in onset_total if x != 'other')
        if n_following_onset == 0:
            continue
        self_rate = self_n / n_following_onset
        # Expected rate under independence = f(onset)
        E = self_rate / freq if freq > 0 else float('inf')
        print(f"  {onset:6s}  {n_onset:5d}  {freq:.4f}  {self_n:6d}  {self_rate:.4f}    {freq:.4f}    {E:.2f}×")

    # ot run-length distribution
    print(f"\not run-length distribution in {dialect} cont lines:")
    ot_runs = Counter()
    ot_run_locations = []
    for words in lines:
        onsets = [get_onset(w) for w in words]
        i = 0
        while i < len(onsets):
            if onsets[i] == 'ot':
                run_len = 1
                while i + run_len < len(onsets) and onsets[i + run_len] == 'ot':
                    run_len += 1
                ot_runs[run_len] += 1
                if run_len >= 2:
                    ot_run_locations.append((run_len, words[i:i+run_len]))
                i += run_len
            else:
                i += 1

    total_ot_runs = sum(ot_runs.values())
    p_ot = onset_total['ot'] / total_tokens if total_tokens > 0 else 0
    print(f"  Overall ot frequency: {p_ot:.4f}")
    print(f"  Total ot runs: {total_ot_runs}")
    print(f"  Run-length distribution:")
    for run_len in sorted(ot_runs.keys()):
        n = ot_runs[run_len]
        # Expected under geometric distribution
        # P(run_len=k) = p_ot^(k-1) * (1-p_ot) if we treat each position as independent
        # But more precisely: a run starting at length k has probability ≈ p_self^(k-1) * (1-p_self)
        # where p_self = P(next=ot | current=ot)
        print(f"  len={run_len}: n={n}  fraction={n/total_ot_runs:.3f}")

    # Compare ot self-succession to y self-succession (known super-geometric from F395)
    ot_self_rate = bigrams[('ot','ot')] / sum(bigrams[('ot',x)] for x in onset_total) if sum(bigrams[('ot',x)] for x in onset_total) > 0 else 0
    y_self_rate = bigrams[('y','y')] / sum(bigrams[('y',x)] for x in onset_total) if sum(bigrams[('y',x)] for x in onset_total) > 0 else 0
    ok_self_rate = bigrams[('ok','ok')] / sum(bigrams[('ok',x)] for x in onset_total) if sum(bigrams[('ok',x)] for x in onset_total) > 0 else 0
    print(f"\n  ot self-succession rate: {ot_self_rate:.4f}")
    print(f"  y self-succession rate:  {y_self_rate:.4f}")
    print(f"  ok self-succession rate: {ok_self_rate:.4f}")
    print(f"  ot freq: {p_ot:.4f}  (E_self = {ot_self_rate/p_ot:.2f}×)")
    p_y = onset_total['y'] / total_tokens
    p_ok = onset_total['ok'] / total_tokens
    print(f"  y freq: {p_y:.4f}   (E_self = {y_self_rate/p_y:.2f}×)")
    print(f"  ok freq: {p_ok:.4f}  (E_self = {ok_self_rate/p_ok:.2f}×)")

    # Long ot runs (≥3)
    if any(ot_runs[k] > 0 for k in ot_runs if k >= 3):
        print(f"\n  Long ot runs (len≥3) in {dialect}:")
        for run_len, words_snippet in ot_run_locations:
            if run_len >= 3:
                print(f"    len={run_len}: {words_snippet}")

print("\n=== Done ===")
