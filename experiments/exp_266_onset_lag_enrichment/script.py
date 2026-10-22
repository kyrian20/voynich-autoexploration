"""
exp_266: H468 — Onset Lag-2/Lag-3 Enrichment Analysis

Question: Does sh→qok enrichment persist beyond lag-1 (adjacent MID succession)?
Does it appear at lag-2 (sh, X, qok) or lag-3 (sh, X, X, qok)?

If sh→qok is lag-1 only: mechanism is immediate succession (consistent with Markov buffer).
If it persists at lag-2/lag-3: longer-range dependency beyond what buffer-Markov can model.

Compare with:
- qok→ch (known Markov rule): should be lag-1 dominant, diminish at lag-2
- y→y (onset persistence rule): should be strongest at lag-1
- o→o (onset persistence rule): same as y→y

Design:
- MID-only bigrams at lag k: collect all (onset_i, onset_{i+k}) pairs where both i and i+k
  are MID positions in the same line
- Compute E_k(x, y) = P(onset_{i+k}=y | onset_i=x) / P(onset_j=y) for k=1,2,3
- Compute same for simulation baseline (use A-dialect 13-mechanism sim from exp_264)
- Report VMS and Sim E_k values for key pairs
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

EVA_CHARS = set('acdehiklmnoqrsty')

def clean_token(tok):
    tok = re.sub(r'<[^>]+>', '', tok)
    tok = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', tok)
    tok = re.sub(r'\{([^}]*)\}', r'\1', tok)
    tok = re.sub(r'[!?,*\-=@#$%^&|~]', '', tok)
    tok = tok.strip()
    if not tok: return None
    if not all(c in EVA_CHARS for c in tok): return None
    return tok

def parse_vms_a():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1
    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}
    a_lines = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            if folio_dialect.get(fb, 'unknown') != 'A': continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: a_lines.append(words)
    return a_lines

def compute_lag_enrichments(lines, max_lag=3):
    """
    Compute lag-k onset enrichment E_k(x, y) = P(onset_{i+k}=y | onset_i=x) / P(onset_j=y)
    for MID-MID pairs only (positions 1..N-2 within each line).

    Returns:
    - onset_counts: Counter of MID onset frequencies (marginal)
    - lag_bigrams: dict of lag -> Counter of (onset_x, onset_y) counts
    - n_mid: total MID word count
    """
    onset_counts = Counter()
    lag_bigrams = {k: Counter() for k in range(1, max_lag+1)}
    n_mid = 0

    for line in lines:
        nn = len(line)
        # MID positions: 1 .. nn-2 (0 = LF, nn-1 = LL)
        mid_indices = list(range(1, nn-1))
        mid_onsets = [get_onset(line[i]) for i in mid_indices]
        n_mid += len(mid_onsets)
        for onset in mid_onsets:
            onset_counts[onset] += 1
        # Lag-k bigrams: (mid_onsets[i], mid_onsets[i+k]) for i < len(mid_onsets)-k
        for k in range(1, max_lag+1):
            for i in range(len(mid_onsets) - k):
                lag_bigrams[k][(mid_onsets[i], mid_onsets[i+k])] += 1

    return onset_counts, lag_bigrams, n_mid

def compute_E(x, y, onset_counts, lag_bigrams, k, n_mid):
    """E_k(x, y) = P(y|x, lag=k) / P(y)"""
    total_lag_k = sum(lag_bigrams[k].values())
    if total_lag_k == 0: return float('nan')
    py = onset_counts.get(y, 0) / n_mid if n_mid > 0 else 0
    if py == 0: return float('nan')
    # P(y | onset_i = x, lag=k) = count(x,y at lag k) / count(x appears as onset_i at any lag)
    # Denominator: number of times x appears as the "source" onset at lag k
    count_x_source = sum(v for (ox, oy), v in lag_bigrams[k].items() if ox == x)
    if count_x_source == 0: return float('nan')
    pyx = lag_bigrams[k].get((x, y), 0) / count_x_source
    return pyx / py

# ── Main ─────────────────────────────────────────────────────────────────────

print("Parsing VMS A-dialect corpus...")
a_lines = parse_vms_a()
print(f"  A-dialect: {len(a_lines)} lines")

print("\nComputing VMS lag enrichments...")
vms_onset_counts, vms_lag_bigrams, vms_n_mid = compute_lag_enrichments(a_lines, max_lag=3)
print(f"  VMS MID onset count: {vms_n_mid}")
for k in range(1, 4):
    print(f"  Lag-{k} bigrams: {sum(vms_lag_bigrams[k].values())}")

# ── VMS lag enrichment table ──────────────────────────────────────────────────

print(f"\n{'='*70}")
print("VMS A-DIALECT: ONSET LAG ENRICHMENT E_k(x, y) FOR KEY PAIRS")
print(f"{'='*70}")

KEY_PAIRS = [
    ('sh', 'qok', 'sh→qok (unmodeled gap)'),
    ('qok', 'ch',  'qok→ch (Markov rule p_qokch=0.12)'),
    ('y',  'y',    'y→y (Markov rule p_y_y=0.10)'),
    ('o',  'o',    'o→o (Markov rule p_o_o=0.10)'),
    ('ch', 'qok',  'ch→qok (known B-dialect rule; A-dialect depleted)'),
    ('sh', 'sh',   'sh→sh (self-succession; VMS depleted E<1)'),
    ('d',  'd',    'd→d (d self-succession; buffer dynamic)'),
]

print(f"\n  {'Pair':>15}  {'N_lag1':>7}  {'E_lag1':>7}  {'E_lag2':>7}  {'E_lag3':>7}  {'Lag2/Lag1':>10}")
print(f"  {'-'*65}")

for x, y, label in KEY_PAIRS:
    n_lag1 = vms_lag_bigrams[1].get((x, y), 0)
    e1 = compute_E(x, y, vms_onset_counts, vms_lag_bigrams, 1, vms_n_mid)
    e2 = compute_E(x, y, vms_onset_counts, vms_lag_bigrams, 2, vms_n_mid)
    e3 = compute_E(x, y, vms_onset_counts, vms_lag_bigrams, 3, vms_n_mid)
    ratio = e2/e1 if (e1 == e1 and e2 == e2 and e1 > 0) else float('nan')
    e1_s = f'{e1:7.3f}' if e1==e1 else '    n/a'
    e2_s = f'{e2:7.3f}' if e2==e2 else '    n/a'
    e3_s = f'{e3:7.3f}' if e3==e3 else '    n/a'
    r_s  = f'{ratio:10.3f}' if ratio==ratio else '         n/a'
    print(f"  {x}→{y:>3s} ({label[:18]:18s})  {n_lag1:7d}  {e1_s}  {e2_s}  {e3_s}  {r_s}")

# ── Decay analysis for sh→qok ─────────────────────────────────────────────────

print(f"\n{'='*70}")
print("SH→QOK LAG DECAY ANALYSIS (VMS A-DIALECT)")
print(f"{'='*70}")
print(f"\n  sh→qok by lag:")
x, y = 'sh', 'qok'
for k in range(1, 4):
    n = vms_lag_bigrams[k].get((x, y), 0)
    total_sh = sum(v for (ox, oy), v in vms_lag_bigrams[k].items() if ox == x)
    e = compute_E(x, y, vms_onset_counts, vms_lag_bigrams, k, vms_n_mid)
    p_qok_given_sh = n / total_sh if total_sh > 0 else 0
    p_qok = vms_onset_counts.get(y, 0) / vms_n_mid
    print(f"    Lag {k}: n={n}, total_sh_source={total_sh}, P(qok|sh,lag={k})={p_qok_given_sh:.4f}, "
          f"P(qok)={p_qok:.4f}, E_lag{k}={e:.3f}")

# ── B-dialect comparison ──────────────────────────────────────────────────────
# Parse B-dialect and compute same
def parse_vms_b():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1
    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}
    b_lines = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            if folio_dialect.get(fb, 'unknown') != 'B': continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: b_lines.append(words)
    return b_lines

print("\n\nParsing VMS B-dialect corpus...")
b_lines = parse_vms_b()
print(f"  B-dialect: {len(b_lines)} lines")

print("\nComputing B-dialect lag enrichments...")
b_onset_counts, b_lag_bigrams, b_n_mid = compute_lag_enrichments(b_lines, max_lag=3)
print(f"  B-dialect MID onset count: {b_n_mid}")

print(f"\n{'='*70}")
print("VMS B-DIALECT: ONSET LAG ENRICHMENT E_k(x, y) FOR KEY PAIRS")
print(f"{'='*70}")

B_KEY_PAIRS = [
    ('sh', 'qok', 'sh→qok (unmodeled, E_mid=1.967)'),
    ('qok', 'ch',  'qok→ch (Markov rule p_qokch=0.12)'),
    ('ch', 'qok',  'ch→qok (Markov rule p_chqok=0.12)'),
    ('y',  'y',    'y→y (self-succession)'),
    ('d',  'd',    'd→d (self-succession)'),
    ('sh', 'sh',   'sh→sh (depleted in VMS)'),
]

print(f"\n  {'Pair':>15}  {'N_lag1':>7}  {'E_lag1':>7}  {'E_lag2':>7}  {'E_lag3':>7}  {'Lag2/Lag1':>10}")
print(f"  {'-'*65}")

for x, y, label in B_KEY_PAIRS:
    n_lag1 = b_lag_bigrams[1].get((x, y), 0)
    e1 = compute_E(x, y, b_onset_counts, b_lag_bigrams, 1, b_n_mid)
    e2 = compute_E(x, y, b_onset_counts, b_lag_bigrams, 2, b_n_mid)
    e3 = compute_E(x, y, b_onset_counts, b_lag_bigrams, 3, b_n_mid)
    ratio = e2/e1 if (e1 == e1 and e2 == e2 and e1 > 0) else float('nan')
    e1_s = f'{e1:7.3f}' if e1==e1 else '    n/a'
    e2_s = f'{e2:7.3f}' if e2==e2 else '    n/a'
    e3_s = f'{e3:7.3f}' if e3==e3 else '    n/a'
    r_s  = f'{ratio:10.3f}' if ratio==ratio else '         n/a'
    print(f"  {x}→{y:>3s} ({label[:18]:18s})  {n_lag1:7d}  {e1_s}  {e2_s}  {e3_s}  {r_s}")

# ── A vs B comparison for sh→qok ─────────────────────────────────────────────

print(f"\n{'='*70}")
print("A vs B DIALECT COMPARISON: sh→qok LAG ENRICHMENT")
print(f"{'='*70}")
for dialect_label, onset_counts, lag_bigrams, n_mid in [
        ('A', vms_onset_counts, vms_lag_bigrams, vms_n_mid),
        ('B', b_onset_counts, b_lag_bigrams, b_n_mid)]:
    x, y = 'sh', 'qok'
    print(f"\n  {dialect_label}-dialect (N_mid={n_mid}):")
    for k in range(1, 4):
        e = compute_E(x, y, onset_counts, lag_bigrams, k, n_mid)
        n = lag_bigrams[k].get((x, y), 0)
        print(f"    Lag {k}: E={e:.3f} (N={n})")

print(f"\nDone.")
