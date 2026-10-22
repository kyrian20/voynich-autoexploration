"""
exp_276: H477 — Word Repetition Distance Distribution

Question: Does the copy-buffer architecture produce VMS-like short MID word repetition distances?

Background:
- exp_265 (F265): 66-74% of MID tokens use LF/LL word types; low MID TTR confirms recycling.
- Copy-buffer with r_mid controls buffer retention: A r_mid=0.87 (high retention, words stay
  in buffer longer), B r_mid=0.25 (low retention, buffer turns over faster).
- Prediction: if r_mid controls recycling, A-dialect MID words should have shorter inter-repetition
  distances than B-dialect (A buffer retains words longer, so they recur sooner).
- Compare to simulation output and to shuffled-text baseline.

Metrics:
1. For each unique word type appearing ≥5 times in MID position:
   - Compute all inter-repetition distances (word positions between consecutive occurrences)
   - Median and mean distance
   - Distribution shape (CDF at distance buckets 1-5, 6-20, 21-50, 51+)
2. Compare A vs B dialect on median/mean distance (directionality test)
3. Compare VMS to simulation on distribution shape
4. Compare to shuffled-MID baseline (global frequency preserved, order randomized)

Design:
- Simulation uses B-dialect 12-mechanism parameters (exp_257, frozen)
- N=10 simulation runs for distribution averaging
- Word repetition distance = number of intervening MID words between two occurrences of same type
- Distance 1 = adjacent repetition; distance N = N-1 words between them

Note: per H477, inter-repetition distances should be shorter for A (r_mid=0.87 → bigger effective
buffer → more recycling) than B (r_mid=0.25 → words exit buffer quickly). But actually: r_mid
is the probability a buffer word is RE-DRAWN at each MID step (not retention duration). Lower r_mid
means less recycling per step → longer expected repetition distance in B. Direction: A should have
shorter distances than B.
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR   = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
DATA_PATH  = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
SEED       = 276000

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def folio_base(folio): return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

def folio_number(folio_tag):
    base = re.sub(r'[rv]$', '', folio_tag)
    try: return int(re.sub(r'[a-z]', '', base))
    except: return -1

def get_section(fb):
    fnum = folio_number(fb)
    if 1 <= fnum <= 65: return 'herbal'
    if 66 <= fnum <= 74: return 'astro'
    if 75 <= fnum <= 81: return 'bio'
    if 82 <= fnum <= 102: return 'cosmo'
    if 103 <= fnum <= 116: return 'recipes'
    if 116 <= fnum <= 120: return 'stars'
    return 'other'

def parse_vms():
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

    records = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words:
                dialect = folio_dialect.get(fb, 'unknown')
                section = get_section(fb)
                records.append({'dialect': dialect, 'section': section, 'fb': fb, 'words': words})
    return records, folio_dialect

def extract_mid_words(records, dialect_filter=None):
    """Extract all MID words (words[1:-1]) from lines, filtered by dialect."""
    mid_words = []
    for rec in records:
        if dialect_filter and rec['dialect'] != dialect_filter: continue
        ws = rec['words']
        mid = ws[1:-1] if len(ws) > 2 else []
        mid_words.extend(mid)
    return mid_words

def compute_repetition_distances(word_seq, min_count=5):
    """
    For each word type appearing >= min_count times, compute inter-repetition distances.
    Distance = number of words (of any type) between two consecutive occurrences.
    Returns dict: word -> list of distances.
    """
    positions = defaultdict(list)
    for i, w in enumerate(word_seq):
        positions[w].append(i)

    distances = {}
    for w, poslist in positions.items():
        if len(poslist) < min_count: continue
        dists = [poslist[i+1] - poslist[i] - 1 for i in range(len(poslist)-1)]
        distances[w] = dists
    return distances

def distance_stats(dist_dict):
    """Compute aggregate statistics across all word types."""
    all_dists = []
    for dists in dist_dict.values():
        all_dists.extend(dists)
    if not all_dists:
        return {'n': 0, 'mean': float('nan'), 'median': float('nan'),
                'p25': float('nan'), 'p75': float('nan'),
                'frac_le5': 0, 'frac_le20': 0, 'frac_le50': 0}
    all_dists_sorted = sorted(all_dists)
    n = len(all_dists_sorted)
    mean = sum(all_dists_sorted) / n
    median = all_dists_sorted[n//2]
    p25 = all_dists_sorted[n//4]
    p75 = all_dists_sorted[3*n//4]
    frac_le5  = sum(1 for d in all_dists_sorted if d <= 5) / n
    frac_le20 = sum(1 for d in all_dists_sorted if d <= 20) / n
    frac_le50 = sum(1 for d in all_dists_sorted if d <= 50) / n
    return {'n': n, 'mean': mean, 'median': median, 'p25': p25, 'p75': p75,
            'frac_le5': frac_le5, 'frac_le20': frac_le20, 'frac_le50': frac_le50}

def word_type_stats(dist_dict):
    """Per-word-type median distances."""
    result = {}
    for w, dists in dist_dict.items():
        ds = sorted(dists)
        result[w] = ds[len(ds)//2]
    return result

def shuffle_mid(mid_words, seed):
    """Shuffle MID word sequence preserving global frequency distribution."""
    rng = random.Random(seed)
    shuffled = mid_words[:]
    rng.shuffle(shuffled)
    return shuffled

# ── Simulation ────────────────────────────────────────────────────────────────

def get_suffix(w):
    for s in SUFFIX_PATTERNS:
        if w.endswith(s): return s
    return 'other'

def build_distributions(mid_words, lf_words, ll_words):
    """Build onset and suffix distributions for simulation."""
    def build_onset_dist(words):
        cnt = Counter(get_onset(w) for w in words if get_onset(w) != 'other')
        total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}
    def build_suffix_dist(words):
        cnt = Counter(get_suffix(w) for w in words)
        total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}
    return {
        'onset_mid': build_onset_dist(mid_words),
        'onset_lf':  build_onset_dist(lf_words),
        'onset_ll':  build_onset_dist(ll_words),
        'suffix_mid': build_suffix_dist(mid_words),
        'suffix_lf':  build_suffix_dist(lf_words),
        'suffix_ll':  build_suffix_dist(ll_words),
    }

def weighted_choice(rng, dist):
    r = rng.random()
    cum = 0.0
    for k, v in dist.items():
        cum += v
        if r < cum: return k
    return list(dist.keys())[-1]

def make_word(rng, onset, suffix_dist):
    onset_str = onset
    suffix = weighted_choice(rng, suffix_dist)
    if suffix == 'other': suffix = 'eedy'
    return onset_str + suffix

def simulate_mid_words(rng, n_words, onset_mid_dist, suffix_mid_dist,
                       r_mid=0.25, p_qokch=0.12, p_chqok=0.12,
                       p_stutter=0.006, p_y_y=0.0):
    """Simplified B-dialect MID simulation."""
    buf = deque(maxlen=20)
    words = []
    prev_onset = None
    for _ in range(n_words):
        # Draw from buffer or fresh
        use_buf = (len(buf) > 0) and (rng.random() < r_mid)
        if use_buf:
            word = rng.choice(list(buf))
        else:
            onset = weighted_choice(rng, onset_mid_dist)
            # Onset Markov rules
            if prev_onset == 'qok' and rng.random() < p_qokch:
                onset = 'ch'
            elif prev_onset == 'ch' and rng.random() < p_chqok:
                onset = 'qok'
            elif prev_onset == onset and rng.random() < p_stutter:
                pass  # keep same onset
            word = make_word(rng, onset, suffix_mid_dist)
        buf.appendleft(word)
        words.append(word)
        prev_onset = get_onset(word)
    return words

def run_simulation_mid(records, folio_dialect, n_sims=5, seed=SEED):
    """Run simulation and extract MID words."""
    # Extract B-dialect corpus statistics
    mid_b = []; lf_b = []; ll_b = []
    for rec in records:
        if rec['dialect'] != 'B': continue
        ws = rec['words']
        if len(ws) >= 1: lf_b.append(ws[0])
        if len(ws) >= 2: ll_b.append(ws[-1])
        mid_b.extend(ws[1:-1] if len(ws) > 2 else [])

    dists_b = build_distributions(mid_b, lf_b, ll_b)

    rng = random.Random(seed)
    all_mid_words = []
    for _ in range(n_sims):
        n = len(mid_b)
        words = simulate_mid_words(rng, n, dists_b['onset_mid'], dists_b['suffix_mid'],
                                   r_mid=0.25, p_qokch=0.12, p_chqok=0.12,
                                   p_stutter=0.006, p_y_y=0.0)
        all_mid_words.extend(words)
    return all_mid_words

def run_simulation_mid_a(records, folio_dialect, n_sims=5, seed=SEED+1):
    """Run simulation for A-dialect MID words."""
    mid_a = []; lf_a = []; ll_a = []
    for rec in records:
        if rec['dialect'] != 'A': continue
        ws = rec['words']
        if len(ws) >= 1: lf_a.append(ws[0])
        if len(ws) >= 2: ll_a.append(ws[-1])
        mid_a.extend(ws[1:-1] if len(ws) > 2 else [])

    dists_a = build_distributions(mid_a, lf_a, ll_a)

    rng = random.Random(seed)
    all_mid_words = []
    for _ in range(n_sims):
        n = len(mid_a)
        words = simulate_mid_words(rng, n, dists_a['onset_mid'], dists_a['suffix_mid'],
                                   r_mid=0.87, p_qokch=0.0, p_chqok=0.0,
                                   p_stutter=0.006, p_y_y=0.10)
        all_mid_words.extend(words)
    return all_mid_words

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    rng_global = random.Random(SEED)
    print("exp_276: H477 — Word Repetition Distance Distribution")
    print("=" * 60)

    records, folio_dialect = parse_vms()

    # Extract MID words by dialect
    mid_a = extract_mid_words(records, 'A')
    mid_b = extract_mid_words(records, 'B')

    print(f"\nCorpus sizes: A MID={len(mid_a)}, B MID={len(mid_b)}")
    print(f"A unique types: {len(set(mid_a))}, B unique types: {len(set(mid_b))}")

    # Word type frequency threshold
    MIN_COUNT = 5
    cnt_a = Counter(mid_a); cnt_b = Counter(mid_b)
    eligible_a = [w for w, c in cnt_a.items() if c >= MIN_COUNT]
    eligible_b = [w for w, c in cnt_b.items() if c >= MIN_COUNT]
    print(f"\nWord types with ≥{MIN_COUNT} occurrences: A={len(eligible_a)}, B={len(eligible_b)}")

    # Compute repetition distances
    print("\n--- VMS Repetition Distance Analysis ---")
    dist_a = compute_repetition_distances(mid_a, MIN_COUNT)
    dist_b = compute_repetition_distances(mid_b, MIN_COUNT)

    stats_a = distance_stats(dist_a)
    stats_b = distance_stats(dist_b)

    print(f"\nA-dialect MID:")
    print(f"  Word types measured: {len(dist_a)}, Total distance observations: {stats_a['n']}")
    print(f"  Mean dist: {stats_a['mean']:.2f}, Median: {stats_a['median']:.1f}")
    print(f"  P25={stats_a['p25']:.1f}, P75={stats_a['p75']:.1f}")
    print(f"  Frac ≤5: {stats_a['frac_le5']:.3f}, ≤20: {stats_a['frac_le20']:.3f}, ≤50: {stats_a['frac_le50']:.3f}")

    print(f"\nB-dialect MID:")
    print(f"  Word types measured: {len(dist_b)}, Total distance observations: {stats_b['n']}")
    print(f"  Mean dist: {stats_b['mean']:.2f}, Median: {stats_b['median']:.1f}")
    print(f"  P25={stats_b['p25']:.1f}, P75={stats_b['p75']:.1f}")
    print(f"  Frac ≤5: {stats_b['frac_le5']:.3f}, ≤20: {stats_b['frac_le20']:.3f}, ≤50: {stats_b['frac_le50']:.3f}")

    # Top 10 words by frequency and their median distances
    print("\n--- Top 15 B-dialect MID words: frequency vs median repetition distance ---")
    print(f"{'Word':<15} {'Count':>6} {'Median dist':>12} {'Mean dist':>10}")
    top_b = sorted([(w, cnt_b[w]) for w in dist_b], key=lambda x: -x[1])[:15]
    for w, cnt in top_b:
        ds = sorted(dist_b[w])
        med = ds[len(ds)//2]; mean_d = sum(ds)/len(ds)
        print(f"  {w:<15} {cnt:>6}  {med:>12.1f} {mean_d:>10.1f}")

    print("\n--- Top 15 A-dialect MID words: frequency vs median repetition distance ---")
    print(f"{'Word':<15} {'Count':>6} {'Median dist':>12} {'Mean dist':>10}")
    top_a = sorted([(w, cnt_a[w]) for w in dist_a], key=lambda x: -x[1])[:15]
    for w, cnt in top_a:
        ds = sorted(dist_a[w])
        med = ds[len(ds)//2]; mean_d = sum(ds)/len(ds)
        print(f"  {w:<15} {cnt:>6}  {med:>12.1f} {mean_d:>10.1f}")

    # Shuffled baseline
    print("\n--- Shuffled Baseline (global frequencies preserved) ---")
    mid_a_shuf = shuffle_mid(mid_a, SEED+10)
    mid_b_shuf = shuffle_mid(mid_b, SEED+11)
    dist_a_shuf = compute_repetition_distances(mid_a_shuf, MIN_COUNT)
    dist_b_shuf = compute_repetition_distances(mid_b_shuf, MIN_COUNT)
    stats_a_shuf = distance_stats(dist_a_shuf)
    stats_b_shuf = distance_stats(dist_b_shuf)
    print(f"A shuffled: Mean={stats_a_shuf['mean']:.2f}, Median={stats_a_shuf['median']:.1f}, "
          f"≤5: {stats_a_shuf['frac_le5']:.3f}, ≤20: {stats_a_shuf['frac_le20']:.3f}")
    print(f"B shuffled: Mean={stats_b_shuf['mean']:.2f}, Median={stats_b_shuf['median']:.1f}, "
          f"≤5: {stats_b_shuf['frac_le5']:.3f}, ≤20: {stats_b_shuf['frac_le20']:.3f}")

    # Simulation
    print("\n--- Simulation (B-dialect 12-mech, r_mid=0.25, N=5 runs) ---")
    sim_mid_b = run_simulation_mid(records, folio_dialect, n_sims=5, seed=SEED)
    dist_b_sim = compute_repetition_distances(sim_mid_b, min_count=5*MIN_COUNT)
    stats_b_sim = distance_stats(dist_b_sim)
    print(f"B sim: N words={len(sim_mid_b)}, word types={len(dist_b_sim)}")
    print(f"  Mean={stats_b_sim['mean']:.2f}, Median={stats_b_sim['median']:.1f}, "
          f"≤5: {stats_b_sim['frac_le5']:.3f}, ≤20: {stats_b_sim['frac_le20']:.3f}, ≤50: {stats_b_sim['frac_le50']:.3f}")

    print("\n--- Simulation (A-dialect 13-mech, r_mid=0.87, N=5 runs) ---")
    sim_mid_a = run_simulation_mid_a(records, folio_dialect, n_sims=5, seed=SEED+1)
    dist_a_sim = compute_repetition_distances(sim_mid_a, min_count=5*MIN_COUNT)
    stats_a_sim = distance_stats(dist_a_sim)
    print(f"A sim: N words={len(sim_mid_a)}, word types={len(dist_a_sim)}")
    print(f"  Mean={stats_a_sim['mean']:.2f}, Median={stats_a_sim['median']:.1f}, "
          f"≤5: {stats_a_sim['frac_le5']:.3f}, ≤20: {stats_a_sim['frac_le20']:.3f}, ≤50: {stats_a_sim['frac_le50']:.3f}")

    # Distance bucket comparison table
    print("\n--- Distance Bucket Comparison Table ---")
    print(f"{'Source':<25} {'Mean':>7} {'Median':>8} {'≤5':>7} {'≤20':>7} {'≤50':>7}")
    print("-" * 60)
    def print_row(label, st):
        if st['n'] == 0:
            print(f"  {label:<23} {'—':>7} {'—':>8} {'—':>7} {'—':>7} {'—':>7}")
        else:
            print(f"  {label:<23} {st['mean']:>7.1f} {st['median']:>8.1f} "
                  f"{st['frac_le5']:>7.3f} {st['frac_le20']:>7.3f} {st['frac_le50']:>7.3f}")
    print_row("VMS A-dialect", stats_a)
    print_row("VMS A shuffled", stats_a_shuf)
    print_row("Sim A (r_mid=0.87)", stats_a_sim)
    print_row("VMS B-dialect", stats_b)
    print_row("VMS B shuffled", stats_b_shuf)
    print_row("Sim B (r_mid=0.25)", stats_b_sim)

    # A vs B directionality test
    print("\n--- A vs B Directionality (H477 prediction: A < B in mean/median distance) ---")
    a_mean = stats_a['mean']; b_mean = stats_b['mean']
    a_med = stats_a['median']; b_med = stats_b['median']
    sim_a_mean = stats_a_sim['mean']; sim_b_mean = stats_b_sim['mean']
    print(f"VMS:  A mean={a_mean:.2f}, B mean={b_mean:.2f} → A{'<' if a_mean<b_mean else '>'}B "
          f"({'CORRECT' if a_mean<b_mean else 'WRONG'} direction)")
    print(f"VMS:  A median={a_med:.1f}, B median={b_med:.1f} → A{'<' if a_med<b_med else '>'}B "
          f"({'CORRECT' if a_med<b_med else 'WRONG'} direction)")
    print(f"Sim:  A mean={sim_a_mean:.2f}, B mean={sim_b_mean:.2f} → A{'<' if sim_a_mean<sim_b_mean else '>'}B "
          f"({'CORRECT' if sim_a_mean<sim_b_mean else 'WRONG'} direction)")

    # Short-distance fraction: fraction ≤5 words apart
    print(f"\nFrac ≤5 words: VMS-A={stats_a['frac_le5']:.3f}, VMS-B={stats_b['frac_le5']:.3f}, "
          f"Shuf-A={stats_a_shuf['frac_le5']:.3f}, Shuf-B={stats_b_shuf['frac_le5']:.3f}")
    print(f"Frac ≤5 words: Sim-A={stats_a_sim['frac_le5']:.3f}, Sim-B={stats_b_sim['frac_le5']:.3f}")

    # Distribution shape: bucket counts
    def bucket_distribution(dist_dict):
        all_dists = []
        for dists in dist_dict.values():
            all_dists.extend(dists)
        if not all_dists: return {}
        n = len(all_dists)
        buckets = {'1': 0, '2-5': 0, '6-20': 0, '21-50': 0, '51+': 0}
        for d in all_dists:
            if d == 1: buckets['1'] += 1
            elif d <= 5: buckets['2-5'] += 1
            elif d <= 20: buckets['6-20'] += 1
            elif d <= 50: buckets['21-50'] += 1
            else: buckets['51+'] += 1
        return {k: v/n for k, v in buckets.items()}

    print("\n--- Distribution Shape (fraction of distances in each bucket) ---")
    print(f"{'Bucket':<10} {'VMS-A':>8} {'VMS-B':>8} {'Shuf-A':>8} {'Shuf-B':>8} {'Sim-A':>8} {'Sim-B':>8}")
    bk_a = bucket_distribution(dist_a)
    bk_b = bucket_distribution(dist_b)
    bk_as = bucket_distribution(dist_a_shuf)
    bk_bs = bucket_distribution(dist_b_shuf)
    bk_asim = bucket_distribution(dist_a_sim)
    bk_bsim = bucket_distribution(dist_b_sim)
    for bucket in ['1', '2-5', '6-20', '21-50', '51+']:
        print(f"  {bucket:<8} {bk_a.get(bucket,0):>8.3f} {bk_b.get(bucket,0):>8.3f} "
              f"{bk_as.get(bucket,0):>8.3f} {bk_bs.get(bucket,0):>8.3f} "
              f"{bk_asim.get(bucket,0):>8.3f} {bk_bsim.get(bucket,0):>8.3f}")

    print("\nDone.")

if __name__ == '__main__':
    main()
