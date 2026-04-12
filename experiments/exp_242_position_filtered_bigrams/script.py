"""
exp_242: H445 — Position-Filtered Bigram Analysis

Question: Are the significant bigram enrichments found in exp_241 (sh→qok, p→sh,
s→sh) genuine within-MID succession rules, or are they cross-position artifacts
(e.g., LF→MID[1] or MID[last]→LL transitions)?

Design:
  Reanalyze the onset bigram matrix using three position-filtered bigram sets:
  (A) Global: all consecutive word pairs (exp_241 method)
  (B) MID-only: consecutive MID words only (within a line, both words in positions 1..n-2)
  (C) Cross-position: LF→MID[1], MID[last]→LL only

  Key pairs to resolve: sh→qok (B: 1.91×), p→sh (B: 2.06×, A: 2.52×), s→sh (B: 1.92×)

  If enrichment is similar in Global and MID-only → genuine within-MID grammar
  If enrichment disappears in MID-only but is high in Cross-position → artifact

  Also compare simulation bigrams (exp_236/239 params) using same three filters
  to see which position contexts the copy buffer captures vs misses.
"""

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

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

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_vms_both_dialects():
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
    lines_by_dialect = {'A': [], 'B': []}
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            dialect = folio_dialect.get(fb, 'unknown')
            if dialect not in ('A', 'B'): continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: lines_by_dialect[dialect].append(words)
    return lines_by_dialect

def compute_position_bigrams(dialect_lines):
    """
    Return three bigram sets:
    - global: all consecutive pairs (entire line sequence)
    - mid_only: within-MID consecutive pairs (i, i+1 both in MID positions)
    - cross_pos: LF→MID[1] pairs and MID[last]→LL pairs
    """
    all_words = [w for l in dialect_lines for w in l]
    n_all = len(all_words)
    oc_all = Counter(get_onset(w) for w in all_words)
    rates_all = {o: c/n_all for o, c in oc_all.items()}

    # Global bigrams (same as exp_241)
    global_bg = Counter()
    global_pairs = 0

    # MID-only bigrams (both words in MID positions)
    mid_bg = Counter()
    mid_pairs = 0
    mid_words_all = []

    # Cross-position bigrams
    cross_bg = Counter()
    cross_pairs = 0

    for line in dialect_lines:
        n = len(line)
        onsets = [get_onset(w) for w in line]

        # Global: all consecutive pairs in this line
        for i in range(n - 1):
            global_bg[(onsets[i], onsets[i+1])] += 1
            global_pairs += 1

        # MID-only: both positions i and i+1 are MID (i.e., 1 <= i < n-2)
        # MID positions: indices 1 to n-2 inclusive (not LF=0, not LL=n-1)
        if n >= 4:  # need at least 4 words to have 2 consecutive MID positions
            for i in range(1, n - 2):  # i is MID, i+1 is also MID
                mid_bg[(onsets[i], onsets[i+1])] += 1
                mid_pairs += 1

        # Collect MID words for rate computation
        if n >= 3:
            for i in range(1, n-1):
                mid_words_all.append(line[i])

        # Cross-position: LF→first_MID (i=0→i=1), last_MID→LL (i=n-2→i=n-1)
        if n >= 3:
            cross_bg[(onsets[0], onsets[1])] += 1   # LF→MID[1]
            cross_bg[(onsets[-2], onsets[-1])] += 1  # MID[last]→LL
            cross_pairs += 2
        elif n == 2:
            cross_bg[(onsets[0], onsets[1])] += 1   # LF→LL direct
            cross_pairs += 1

    # Compute enrichments
    def enrichment(bg, pairs, rate_x, rate_y, x, y):
        pxy = bg.get((x,y), 0) / pairs if pairs > 0 else 0
        px = rate_x.get(x, 0)
        py = rate_y.get(y, 0)
        return pxy / (px * py) if px * py > 0 else 0

    # For MID-only, use MID-specific rates
    n_mid = len(mid_words_all)
    oc_mid = Counter(get_onset(w) for w in mid_words_all)
    rates_mid = {o: c/n_mid for o, c in oc_mid.items()} if n_mid else {}

    return {
        'global_bg': global_bg, 'global_n': global_pairs, 'global_rates': rates_all,
        'mid_bg': mid_bg, 'mid_n': mid_pairs, 'mid_rates': rates_mid,
        'cross_bg': cross_bg, 'cross_n': cross_pairs,
        'all_rates': rates_all,
    }

def compute_E(bg, n, rates_x, rates_y, x, y):
    pxy = bg.get((x, y), 0) / n if n > 0 else 0
    px = rates_x.get(x, 0); py = rates_y.get(y, 0)
    return pxy / (px * py) if px * py > 0 else 0

def compute_E_all(data, x, y):
    """Return (E_global, E_mid, E_cross) for pair (x, y)."""
    E_g = compute_E(data['global_bg'], data['global_n'], data['global_rates'], data['global_rates'], x, y)
    E_m = compute_E(data['mid_bg'], data['mid_n'], data['mid_rates'], data['mid_rates'], x, y)
    E_c = compute_E(data['cross_bg'], data['cross_n'], data['all_rates'], data['all_rates'], x, y)
    return E_g, E_m, E_c

# ─── Parse ────────────────────────────────────────────────────────────────────

print("Parsing VMS corpora...")
lines_by_dialect = parse_vms_both_dialects()

print(f"  B-dialect: {len(lines_by_dialect['B'])} lines")
print(f"  A-dialect: {len(lines_by_dialect['A'])} lines")

B_data = compute_position_bigrams(lines_by_dialect['B'])
A_data = compute_position_bigrams(lines_by_dialect['A'])

print(f"\nB-dialect bigram contexts:")
print(f"  Global pairs: {B_data['global_n']}")
print(f"  MID-only pairs: {B_data['mid_n']}")
print(f"  Cross-position pairs: {B_data['cross_n']}")

print(f"\nA-dialect bigram contexts:")
print(f"  Global pairs: {A_data['global_n']}")
print(f"  MID-only pairs: {A_data['mid_n']}")
print(f"  Cross-position pairs: {A_data['cross_n']}")

# ─── Key pairs analysis ────────────────────────────────────────────────────────

print("\n" + "="*90)
print("POSITION-FILTERED ANALYSIS — KEY PAIRS FROM EXP_241")
print("="*90)

KEY_PAIRS_B = [
    ('sh', 'qok'),  # B-specific, missed in exp_241
    ('p', 'sh'),    # Cross-dialect, missed
    ('s', 'sh'),    # B-specific, missed
    ('qok', 'ch'),  # B: known Markov rule — should stay enriched
    ('y', 'y'),     # B: natural copy buffer (no p_y_y)
    ('ot', 'ot'),   # B: self-succession missed
    ('l', 'l'),     # B: self-succession missed
    ('d', 'd'),     # B: self-succession (should pass)
    ('ok', 'ok'),   # B: self-succession (captured)
    ('qok', 'qok'), # B: self-succession (should pass)
]

KEY_PAIRS_A = [
    ('p', 'sh'),    # Cross-dialect, missed
    ('y', 'y'),     # A: explicit p_y_y mechanism
    ('sh', 'qo'),   # A: missed
    ('ot', 'ot'),   # A: self-succession missed
    ('o', 'o'),     # A: self-succession missed
    ('d', 'd'),     # A: self-succession (captured)
    ('qok', 'ch'),  # A: Markov rule (transferred)
    ('qok', 'qok'), # A: self-succession
    ('ok', 'ok'),   # A: self-succession
]

def print_pair_analysis(label, data, pairs):
    print(f"\n{label}:")
    print(f"  {'Pair':<14} {'E_global':>10} {'E_mid':>10} {'E_cross':>10} {'MID_cnt':>8}  {'Verdict'}")
    print(f"  {'-'*75}")
    for x, y in pairs:
        Eg, Em, Ec = compute_E_all(data, x, y)
        cnt_mid = data['mid_bg'].get((x, y), 0)
        # Verdict: is Em similar to Eg? (real MID grammar) or very different (artifact)?
        if Eg > 1.2 and Em > 1.2:
            verdict = 'MID grammar (genuine)'
        elif Eg > 1.2 and Em < 0.9:
            verdict = 'CROSS-POS ARTIFACT'
        elif Eg > 1.2:
            verdict = 'partially genuine'
        elif Eg < 0.8:
            verdict = 'depleted (global)'
        else:
            verdict = 'near-baseline'
        print(f"  {x}→{y:<10} {Eg:>10.3f} {Em:>10.3f} {Ec:>10.3f} {cnt_mid:>8}  {verdict}")

print_pair_analysis("B-DIALECT KEY PAIRS", B_data, KEY_PAIRS_B)
print_pair_analysis("A-DIALECT KEY PAIRS", A_data, KEY_PAIRS_A)

# ─── Full MID-only enrichment matrix (top pairs) ─────────────────────────────

print("\n" + "="*90)
print("MID-ONLY ONSET BIGRAM ENRICHMENTS — TOP 30 ENRICHED PAIRS")
print("="*90)

MIN_RATE = 0.01
THRESHOLD = 0.30  # higher threshold for MID-only to reduce noise

for dialect_name, data in [('B-DIALECT', B_data), ('A-DIALECT', A_data)]:
    print(f"\n{dialect_name}:")
    print(f"  {'Pair':<14} {'E_global':>10} {'E_mid_only':>10} {'MID_cnt':>8}  {'Verdict'}")
    print(f"  {'-'*60}")

    sig = {}
    rates = data['mid_rates']
    for x, rate_x in rates.items():
        if rate_x < MIN_RATE: continue
        for y, rate_y in rates.items():
            if rate_y < MIN_RATE: continue
            E_m = compute_E(data['mid_bg'], data['mid_n'], rates, rates, x, y)
            E_g = compute_E(data['global_bg'], data['global_n'],
                           data['global_rates'], data['global_rates'], x, y)
            cnt = data['mid_bg'].get((x, y), 0)
            if abs(E_m - 1) > THRESHOLD:
                sig[(x, y)] = (E_g, E_m, cnt)

    sorted_pairs = sorted(sig.items(), key=lambda kv: kv[1][1], reverse=True)
    for (x, y), (Eg, Em, cnt) in sorted_pairs[:30]:
        verdict = 'MID grammar' if Em > 1.0 and Eg > 1.0 else 'MID depleted'
        print(f"  {x}→{y:<10} {Eg:>10.3f} {Em:>10.3f} {cnt:>8}  {verdict}")

# ─── Verdict ─────────────────────────────────────────────────────────────────

print("\n" + "="*90)
print("POSITION CONFOUND VERDICT")
print("="*90)

print("\n  Key diagnostic pairs:")

TARGET_PAIRS = [
    ('B', B_data, 'sh', 'qok', 'sh→qok (B, VMS E=1.91)'),
    ('B', B_data, 'p',  'sh',  'p→sh (B, VMS E=2.06)'),
    ('A', A_data, 'p',  'sh',  'p→sh (A, VMS E=2.52)'),
    ('B', B_data, 's',  'sh',  's→sh (B, VMS E=1.92)'),
]

for dialect, data, x, y, label in TARGET_PAIRS:
    Eg, Em, Ec = compute_E_all(data, x, y)
    cnt_m = data['mid_bg'].get((x, y), 0)
    if Em > 1.3:
        verdict = 'GENUINE MID GRAMMAR'
    elif Em > 1.0 and Eg > 1.3:
        verdict = 'mostly genuine (Em moderate)'
    elif Eg > 1.3 and Em < 1.0:
        verdict = 'CROSS-POSITION ARTIFACT'
    else:
        verdict = f'unclear (Em={Em:.2f})'
    print(f"\n  {label}:")
    print(f"    E_global={Eg:.3f}  E_mid_only={Em:.3f}  E_cross={Ec:.3f}  MID_count={cnt_m}")
    print(f"    → {verdict}")

print()
print("Done.")
