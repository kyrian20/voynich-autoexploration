"""
exp_175: Long-Range Mutual Information Decay — VMS vs Naibbe vs Timm

Mutual information MI(d) at lag d measures how much knowing position i
reduces uncertainty about position i+d. Natural language shows characteristic
decay patterns: MI is highest at lag 1, decays as lag increases, but shows
elevated tails compared to random (reflecting long-range structure — syntax,
topic, etc.).

Key predictions:
  - Random text / scrambled: MI ≈ 0 for all lags
  - Cipher (letter substitution): MI decay mirrors plaintext (rapid, short-range)
  - Self-citation (Timm): MI at lag 1 is high (local copy) but decays fast
  - Structured language: MI decays slowly, with elevated values at d=2-10+

Method:
  1. Compute MI(d) for VMS A-dialect, B-dialect, word-by-word at lags d=1..20
  2. Compare against Naibbe simulation distribution (from exp_170 data)
  3. Compare against Timm simulation distribution (from exp_171 data)
  4. Compare against shuffled-VMS (within-folio word shuffle, destroys sequence)

MI formula:
  MI(d) = sum_{x,y} P(X=x, Y=y) * log2(P(X=x, Y=y) / (P(X=x) * P(Y=y)))

where X = word at position i, Y = word at position i+d (same line only, no
cross-line MI — this isolates within-line structure from inter-line structure).

Note: We use word-type MI (onset class), not raw word MI, to avoid
vocabulary size effects and make the comparison numerically stable.
"""
from pathlib import Path as _RepositoryPath

import sys
import os
import json
import random
import math

REPO_DIR = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
sys.path.insert(0, os.path.join(REPO_DIR, 'src'))

from collections import defaultdict, Counter

# ─── CORPUS PARSING ───────────────────────────────────────────────────────────

import re

def parse_corpus(path):
    lines_by_folio = defaultdict(list)
    with open(path, encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw or raw.startswith('#'):
                continue
            parts = raw.split(None, 1)
            if len(parts) < 2:
                continue
            locus_raw, text = parts
            lparts = locus_raw.split(',')
            if len(lparts) < 2:
                continue
            lt = lparts[1].rstrip('>').lstrip('@+*=~&')
            if not lt.startswith('P'):
                continue
            folio_base = lparts[0].split('.')[0].lstrip('<')
            m = re.match(r'f(\d+)', folio_base)
            if not m:
                continue
            fid = int(m.group(1))
            words = [w for w in text.split('.') if w and re.match(r'[a-z]', w) and not w.startswith('<')]
            if not words:
                continue
            lines_by_folio[fid].append(words)
    return lines_by_folio

def assign_dialect(lines, min_words=10, threshold=0.05):
    all_words = [w for line in lines for w in line]
    if len(all_words) < min_words:
        return None
    edy_count = sum(1 for w in all_words if 'edy' in w or 'eedy' in w)
    rate = edy_count / len(all_words)
    return 'B' if rate >= threshold else 'A'

# ─── ONSET TAXONOMY ───────────────────────────────────────────────────────────

def get_onset(word):
    w = word
    for prefix in ['qok', 'qot', 'qo']:
        if w.startswith(prefix):
            return prefix
    if w.startswith('cth'):
        return 'cth'
    if w.startswith('che') or w.startswith('chi'):
        return 'ch_e'
    if w.startswith('ch'):
        return 'ch'
    if w.startswith('sh'):
        return 'sh'
    for prefix in ['ok', 'ot', 'ol', 'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f']:
        if w.startswith(prefix):
            return prefix
    return 'other'

def get_suffix(word):
    for suf in ['am', 'aiin', 'edy', 'eedy', 'ol', 'or', 'al', 'ar']:
        if word.endswith(suf):
            return suf
    return 'other'

def get_word_class(word):
    """Coarser classification: onset + suffix for MI computation."""
    return get_onset(word)  # Use onset class for stability

# ─── MUTUAL INFORMATION ───────────────────────────────────────────────────────

def compute_mi(lines, max_lag=15, class_fn=get_onset):
    """
    Compute within-line MI at lags 1..max_lag.
    Returns dict: lag -> MI value (bits).
    """
    mis = {}
    for lag in range(1, max_lag + 1):
        joint_counts = defaultdict(int)
        marg_x = defaultdict(int)
        marg_y = defaultdict(int)
        total = 0
        for line in lines:
            classes = [class_fn(w) for w in line]
            n = len(classes)
            for i in range(n - lag):
                x = classes[i]
                y = classes[i + lag]
                joint_counts[(x, y)] += 1
                marg_x[x] += 1
                marg_y[y] += 1
                total += 1

        if total == 0:
            mis[lag] = 0.0
            continue

        mi = 0.0
        for (x, y), c_xy in joint_counts.items():
            p_xy = c_xy / total
            p_x = marg_x[x] / total
            p_y = marg_y[y] / total
            if p_xy > 0 and p_x > 0 and p_y > 0:
                mi += p_xy * math.log2(p_xy / (p_x * p_y))
        mis[lag] = mi
    return mis

def shuffle_within_lines(lines, seed=42):
    """Shuffle words within each line (destroys sequence order, preserves line structure)."""
    rng = random.Random(seed)
    result = []
    for line in lines:
        shuffled = line[:]
        rng.shuffle(shuffled)
        result.append(shuffled)
    return result

def shuffle_across_lines(lines, seed=42):
    """Shuffle all words across all lines and reassign to same line lengths."""
    rng = random.Random(seed)
    all_words = [w for line in lines for w in line]
    rng.shuffle(all_words)
    result = []
    pos = 0
    for line in lines:
        n = len(line)
        result.append(all_words[pos:pos+n])
        pos += n
    return result

# ─── NAIBBE SIMULATION ────────────────────────────────────────────────────────

def simulate_naibbe_mi(n_sims=100, max_lag=15):
    """
    Load exp_170 simulation data and compute MI for each Naibbe simulation.
    Returns dict: lag -> list of MI values across simulations.
    """
    data_path = os.path.join(REPO_DIR, 'experiments/exp_170_naibbe_simulation/data/simulation_results.json')
    if not os.path.exists(data_path):
        print("  [WARNING] exp_170 simulation_results.json not found — skipping Naibbe MI")
        return None

    with open(data_path) as f:
        sim_data = json.load(f)

    # The saved data contains metric summaries, not raw line data
    # We need to reconstruct lines. Since raw tokens aren't saved, we'll note this
    # and compute from what we have. Since the raw lines weren't saved, return None
    print("  [INFO] exp_170 data contains metric summaries only (not raw token lines)")
    print("  [INFO] Skipping Naibbe MI decay — would require re-running exp_170 to save raw tokens")
    return None

# ─── TIMM SIMULATION ─────────────────────────────────────────────────────────

def generate_timm_corpus_for_mi(seed, target_tokens=20000, line_length_mean=8.4):
    """Generate a Timm corpus and break into lines for MI computation."""
    # Re-implement core Timm algorithm for MI comparison
    # Seeds from B-dialect top-200 words

    # Load B-dialect words from corpus to get seed vocabulary
    path = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
    lines_by_folio = parse_corpus(path)

    b_words = []
    for fid, flines in lines_by_folio.items():
        if assign_dialect(flines) == 'B':
            b_words.extend(w for line in flines for w in line)

    # Top-200 B-dialect words
    word_counts = Counter(b_words)
    seed_words = [w for w, _ in word_counts.most_common(200)]
    seed_probs = [word_counts[w] for w in seed_words]
    total = sum(seed_probs)
    seed_probs = [p / total for p in seed_probs]

    WINDOW_SIZE = 50
    COPY_PROB = 0.85
    MODIFY_PROB = 0.25

    def modify_word(word, rng):
        if len(word) <= 2:
            return word
        op = rng.choice(['replace', 'delete', 'insert'])
        chars = list(word)
        idx = rng.randint(0, len(chars) - 1)
        eva_chars = list('qotpckhsdar')
        if op == 'replace':
            chars[idx] = rng.choice(eva_chars)
        elif op == 'delete':
            chars.pop(idx)
        elif op == 'insert':
            chars.insert(idx, rng.choice(eva_chars))
        return ''.join(chars)

    rng = random.Random(seed)

    tokens = []
    for _ in range(min(WINDOW_SIZE, 20)):
        w = rng.choices(seed_words, weights=seed_probs)[0]
        tokens.append(w)

    while len(tokens) < target_tokens:
        if rng.random() < COPY_PROB and len(tokens) >= WINDOW_SIZE:
            start = max(0, len(tokens) - WINDOW_SIZE)
            source = rng.choice(tokens[start:])
        else:
            source = rng.choices(seed_words, weights=seed_probs)[0]
        if rng.random() < MODIFY_PROB:
            source = modify_word(source, rng)
        tokens.append(source)

    tokens = tokens[:target_tokens]

    # Break into lines using approximate VMS B-dialect line lengths
    ll_mean = 8.4
    ll_std = 3.0
    lines = []
    pos = 0
    while pos < len(tokens):
        n = max(2, min(20, round(rng.gauss(ll_mean, ll_std))))
        lines.append(tokens[pos:pos+n])
        pos += n
    return lines

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    path = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
    lines_by_folio = parse_corpus(path)

    A_lines = []
    B_lines = []
    for fid, lines in lines_by_folio.items():
        dialect = assign_dialect(lines)
        if dialect == 'A':
            A_lines.extend(lines)
        elif dialect == 'B':
            B_lines.extend(lines)

    print(f"A-dialect: {sum(len(l) for l in A_lines)} words, {len(A_lines)} lines")
    print(f"B-dialect: {sum(len(l) for l in B_lines)} words, {len(B_lines)} lines")

    MAX_LAG = 12

    print("\n" + "="*70)
    print("WITHIN-LINE ONSET-CLASS MI DECAY (lags 1-12)")
    print("="*70)

    for dialect_name, all_lines in [('A', A_lines), ('B', B_lines)]:
        print(f"\n─── {dialect_name}-dialect ───")

        # VMS real
        mi_vms = compute_mi(all_lines, max_lag=MAX_LAG)

        # Within-line shuffled (destroys sequence, preserves line membership)
        mi_shuffle_within = compute_mi(shuffle_within_lines(all_lines), max_lag=MAX_LAG)

        # Across-line shuffled (destroys all structure)
        mi_shuffle_across = compute_mi(shuffle_across_lines(all_lines), max_lag=MAX_LAG)

        print(f"  {'Lag':>4} {'VMS':>8} {'ShufWithin':>12} {'ShufAcross':>12} {'VMS/Within':>12} {'VMS/Across':>12}")
        for lag in range(1, MAX_LAG + 1):
            v = mi_vms[lag]
            sw = mi_shuffle_within[lag]
            sa = mi_shuffle_across[lag]
            ratio_w = v / sw if sw > 0 else float('inf')
            ratio_a = v / sa if sa > 0 else float('inf')
            print(f"  {lag:>4} {v:>8.4f} {sw:>12.4f} {sa:>12.4f} {ratio_w:>12.3f} {ratio_a:>12.3f}")

    print("\n" + "="*70)
    print("TIMM SIMULATION MI DECAY (20 simulations, B-dialect comparison)")
    print("="*70)

    # Run 20 Timm simulations for MI comparison
    N_TIMM = 20
    timm_mi_by_lag = defaultdict(list)
    print(f"  Running {N_TIMM} Timm simulations...")
    for sim_i in range(N_TIMM):
        if sim_i % 5 == 0:
            print(f"    sim {sim_i}/{N_TIMM}")
        timm_lines = generate_timm_corpus_for_mi(seed=sim_i + 1000)
        mi_timm = compute_mi(timm_lines, max_lag=MAX_LAG)
        for lag, val in mi_timm.items():
            timm_mi_by_lag[lag].append(val)

    mi_b = compute_mi(B_lines, max_lag=MAX_LAG)

    print(f"\n  {'Lag':>4} {'VMS-B':>8} {'Timm mean':>10} {'Timm lo':>9} {'Timm hi':>9} {'VMS vs Timm':>12}")
    for lag in range(1, MAX_LAG + 1):
        v = mi_b[lag]
        vals = sorted(timm_mi_by_lag[lag])
        n = len(vals)
        lo = vals[max(0, int(n * 0.025))]
        hi = vals[min(n - 1, int(n * 0.975))]
        mean = sum(vals) / n
        if v > hi:
            status = "ABOVE"
        elif v < lo:
            status = "BELOW"
        else:
            status = "inside"
        print(f"  {lag:>4} {v:>8.4f} {mean:>10.4f} {lo:>9.4f} {hi:>9.4f} {status:>12}")

    print("\n" + "="*70)
    print("INTERPRETATION SUMMARY")
    print("="*70)
    print("\nKey questions:")
    print("1. Does VMS MI decay slowly (grammar/language) or sharply (cipher/random)?")
    print("2. Is VMS lag-1 MI similar to or higher than Timm (local coherence)?")
    print("3. Does VMS maintain elevated MI at lags 3-10 vs Timm?")
    print("4. Does within-line shuffle destroy MI (confirming sequence matters)?")
    print("\nSee result.md for interpretation.")
    print("\nDone.")

if __name__ == '__main__':
    main()
