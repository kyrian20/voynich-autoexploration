"""
exp_176: Timm Algorithm Parameter Sensitivity Sweep

Tests whether the exp_171 falsification of Timm self-citation holds across
the full parameter space, or only for the specific parameters used in exp_171
(WINDOW=50, COPY_PROB=0.85, MODIFY_PROB=0.25).

Grid:
  COPY_PROB ∈ {0.3, 0.5, 0.7, 0.85, 0.95}
  MODIFY_PROB ∈ {0.1, 0.25, 0.4, 0.6, 0.8}
  WINDOW ∈ {10, 30, 50}
  → 5 × 5 × 3 = 75 combinations

Per combination: 20 simulated corpora, 20,000 tokens each.

Key metrics per combination:
  - identical_adj_rate: P(word[i] == word[i-1]) — must be ≤ 1.5× VMS (0.009 × 1.5 = 0.0135)
  - self_succession_mean: average of qok, ok, ch self-succession enrichments — must be ≥ 0.8× VMS range (1.24-1.69)
  - am_ll_enr: -am LL enrichment — VMS target = 6.811
  - y_lf_enr: y-onset LF enrichment — VMS target = 3.506
  - d_ll_enr: d-onset LL enrichment — VMS target = 1.464
  - qok_lf_enr: qok LF enrichment — VMS target = 0.839 (depleted)

Report: is there any parameter combination that simultaneously achieves:
  (A) identical_adj_rate ≤ 1.5× VMS (≤ 0.0135)
  (B) self-succession mean enrichment ≥ 1.1× (minimum consistent with VMS grammar signal)
If yes: "Timm-viable zone" exists; falsification qualified.
If no: falsification holds across full parameter space.
"""

import os, sys, re, random, json, math
from collections import Counter, defaultdict

REPO_DIR = os.path.expanduser('~/voynich-cryptanalyst')
VMS_CORPUS = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
OUT_DIR = os.path.join(REPO_DIR, 'experiments/exp_176_timm_parameter_sweep/data')
os.makedirs(OUT_DIR, exist_ok=True)

N_SIMS_PER_COMBO = 20
TARGET_TOKENS = 20000

# ─── CORPUS PARSING ───────────────────────────────────────────────────────────

def parse_corpus(path):
    lines_by_folio = defaultdict(list)
    with open(path) as f:
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
            if words:
                lines_by_folio[fid].append(words)
    return lines_by_folio

def assign_dialect(lines, min_words=10, threshold=0.05):
    all_words = [w for line in lines for w in line]
    if len(all_words) < min_words:
        return None
    rate = sum(1 for w in all_words if 'edy' in w) / len(all_words)
    return 'B' if rate >= threshold else 'A'

def get_onset(word):
    w = word
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'):  return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('che') or w.startswith('chi'): return 'ch_e'
    if w.startswith('ch'):  return 'ch'
    if w.startswith('sh'):  return 'sh'
    if w.startswith('ok'):  return 'ok'
    if w.startswith('ot'):  return 'ot'
    if w.startswith('ol'):  return 'ol'
    if w.startswith('d'):   return 'd'
    if w.startswith('s'):   return 's'
    if w.startswith('y'):   return 'y'
    if w.startswith('k'):   return 'k'
    if w.startswith('t'):   return 't'
    if w.startswith('l'):   return 'l'
    if w.startswith('r'):   return 'r'
    return 'other'

# ─── LOAD VMS B-DIALECT ───────────────────────────────────────────────────────

print("Loading VMS corpus...")
lines_by_folio = parse_corpus(VMS_CORPUS)

b_words = []
b_lines = []
for fid, lines in lines_by_folio.items():
    if assign_dialect(lines) == 'B':
        b_words.extend(w for line in lines for w in line)
        b_lines.extend(lines)

print(f"B-dialect: {len(b_words)} words, {len(b_lines)} lines")

# VMS target values
VMS_IDENTICAL_ADJ = 0.009
VMS_QOK_SS = 1.239
VMS_OK_SS  = 1.462
VMS_CH_SS  = 1.694
VMS_AM_LL  = 6.811
VMS_Y_LF   = 3.506
VMS_D_LL   = 1.464
VMS_QOK_LF = 0.839

# Seed vocabulary: top-200 B-dialect words
word_counts = Counter(b_words)
seed_words = [w for w, _ in word_counts.most_common(200)]
seed_probs_raw = [word_counts[w] for w in seed_words]
total = sum(seed_probs_raw)
seed_probs = [p / total for p in seed_probs_raw]

# B-dialect baseline rates for metrics
b_all = b_words
b_n = len(b_all)
b_onset_counts = Counter(get_onset(w) for w in b_all)
b_lf_words = [line[0] for line in b_lines if line]
b_ll_words = [line[-1] for line in b_lines if len(line) > 1]
b_lf_n = len(b_lf_words)
b_ll_n = len(b_ll_words)

b_am_base  = sum(1 for w in b_all if w.endswith('am')) / b_n
b_y_base   = b_onset_counts['y'] / b_n
b_d_base   = b_onset_counts['d'] / b_n
b_qok_base = b_onset_counts['qok'] / b_n

# ─── TIMM GENERATOR ───────────────────────────────────────────────────────────

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

def generate_timm(seed, copy_prob, modify_prob, window):
    rng = random.Random(seed)
    tokens = [rng.choices(seed_words, weights=seed_probs)[0]
              for _ in range(min(window, 20))]
    while len(tokens) < TARGET_TOKENS:
        if rng.random() < copy_prob and len(tokens) >= window:
            start = max(0, len(tokens) - window)
            source = rng.choice(tokens[start:])
        else:
            source = rng.choices(seed_words, weights=seed_probs)[0]
        if rng.random() < modify_prob:
            source = modify_word(source, rng)
        tokens.append(source)
    return tokens[:TARGET_TOKENS]

def tokens_to_lines(tokens, rng_seed=0):
    """Break token sequence into lines using VMS B-dialect length distribution."""
    rng = random.Random(rng_seed)
    ll_mean, ll_std = 8.4, 3.0
    lines = []
    pos = 0
    while pos < len(tokens):
        n = max(2, min(20, round(rng.gauss(ll_mean, ll_std))))
        lines.append(tokens[pos:pos+n])
        pos += n
    return lines

# ─── METRICS ──────────────────────────────────────────────────────────────────

def compute_metrics(tokens, lines):
    n = len(tokens)
    if n < 100:
        return None

    # Identical adjacent word rate
    adj_same = sum(1 for i in range(len(tokens)-1) if tokens[i] == tokens[i+1])
    identical_adj = adj_same / (len(tokens) - 1)

    # Self-succession enrichments
    onset_counts_total = Counter(get_onset(w) for w in tokens)
    bigram_counts = Counter((get_onset(tokens[i]), get_onset(tokens[i+1]))
                             for i in range(len(tokens)-1))
    total_bigrams = sum(bigram_counts.values())

    def ss_enr(onset):
        baseline = onset_counts_total[onset] / n
        obs = bigram_counts[(onset, onset)]
        expected = total_bigrams * baseline * baseline
        return obs / expected if expected > 0 else 1.0

    qok_ss = ss_enr('qok')
    ok_ss  = ss_enr('ok')
    ch_ss  = ss_enr('ch')

    # Positional metrics
    lf_words = [line[0] for line in lines if line]
    ll_words = [line[-1] for line in lines if len(line) > 1]
    n_lf = len(lf_words)
    n_ll = len(ll_words)

    def pos_enr(words_at_pos, test_fn, baseline_rate, n_pos):
        if n_pos == 0 or baseline_rate == 0:
            return 1.0
        obs = sum(1 for w in words_at_pos if test_fn(w))
        return (obs / n_pos) / baseline_rate

    am_ll  = pos_enr(ll_words, lambda w: w.endswith('am'), b_am_base, n_ll)
    y_lf   = pos_enr(lf_words, lambda w: get_onset(w) == 'y', b_y_base, n_lf)
    d_ll   = pos_enr(ll_words, lambda w: get_onset(w) == 'd', b_d_base, n_ll)
    qok_lf = pos_enr(lf_words, lambda w: get_onset(w) == 'qok', b_qok_base, n_lf)

    return {
        'identical_adj': identical_adj,
        'qok_ss': qok_ss,
        'ok_ss': ok_ss,
        'ch_ss': ch_ss,
        'ss_mean': (qok_ss + ok_ss + ch_ss) / 3,
        'am_ll': am_ll,
        'y_lf': y_lf,
        'd_ll': d_ll,
        'qok_lf': qok_lf,
    }

# ─── PARAMETER GRID ───────────────────────────────────────────────────────────

COPY_PROBS   = [0.3, 0.5, 0.7, 0.85, 0.95]
MODIFY_PROBS = [0.1, 0.25, 0.4, 0.6, 0.8]
WINDOWS      = [10, 30, 50]

results = {}
n_combos = len(COPY_PROBS) * len(MODIFY_PROBS) * len(WINDOWS)
combo_idx = 0

print(f"\nRunning {n_combos} parameter combinations × {N_SIMS_PER_COMBO} sims each...")
print(f"Total simulations: {n_combos * N_SIMS_PER_COMBO}")

for cp in COPY_PROBS:
    for mp in MODIFY_PROBS:
        for win in WINDOWS:
            combo_idx += 1
            if combo_idx % 15 == 1:
                print(f"  combo {combo_idx}/{n_combos} (cp={cp}, mp={mp}, win={win})...")

            key = f"cp{cp}_mp{mp}_win{win}"
            sim_results = []
            for sim_i in range(N_SIMS_PER_COMBO):
                seed = combo_idx * 1000 + sim_i
                tokens = generate_timm(seed, cp, mp, win)
                lines = tokens_to_lines(tokens, rng_seed=seed + 99999)
                m = compute_metrics(tokens, lines)
                if m:
                    sim_results.append(m)

            if sim_results:
                # Average across simulations
                keys = sim_results[0].keys()
                avg = {k: sum(s[k] for s in sim_results) / len(sim_results) for k in keys}
                results[key] = {
                    'copy_prob': cp,
                    'modify_prob': mp,
                    'window': win,
                    **avg,
                    'n_sims': len(sim_results),
                }

# Save raw results
out_path = os.path.join(OUT_DIR, 'sweep_results.json')
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to {out_path}")

# ─── ANALYSIS ─────────────────────────────────────────────────────────────────

print(f"\n{'='*80}")
print("PARAMETER SWEEP ANALYSIS")
print(f"{'='*80}")
print(f"\nVMS targets:")
print(f"  identical_adj:  {VMS_IDENTICAL_ADJ:.4f} (threshold for 'viable': ≤ {1.5*VMS_IDENTICAL_ADJ:.4f})")
print(f"  qok_ss:         {VMS_QOK_SS:.3f}")
print(f"  ok_ss:          {VMS_OK_SS:.3f}")
print(f"  ch_ss:          {VMS_CH_SS:.3f}")
print(f"  ss_mean:        {(VMS_QOK_SS+VMS_OK_SS+VMS_CH_SS)/3:.3f}")
print(f"  am_ll:          {VMS_AM_LL:.3f}")
print(f"  y_lf:           {VMS_Y_LF:.3f}")
print(f"  d_ll:           {VMS_D_LL:.3f}")
print(f"  qok_lf:         {VMS_QOK_LF:.3f}")

VMS_SS_MEAN = (VMS_QOK_SS + VMS_OK_SS + VMS_CH_SS) / 3

VIABLE_ADJ_THRESH = 1.5 * VMS_IDENTICAL_ADJ   # ≤ 0.0135
VIABLE_SS_THRESH  = 1.1                         # ss_mean ≥ 1.1

viable_combos = []
for key, r in results.items():
    crit_a = r['identical_adj'] <= VIABLE_ADJ_THRESH
    crit_b = r['ss_mean'] >= VIABLE_SS_THRESH
    if crit_a and crit_b:
        viable_combos.append((key, r))

print(f"\n── VIABLE ZONE (adj_rate ≤ {VIABLE_ADJ_THRESH:.4f} AND ss_mean ≥ {VIABLE_SS_THRESH:.2f}) ──")
print(f"Combinations meeting BOTH criteria: {len(viable_combos)} / {len(results)}")

if viable_combos:
    print("\nViable combinations:")
    print(f"  {'Key':<25} {'adj_rate':>9} {'ss_mean':>8} {'am_ll':>7} {'y_lf':>7} {'d_ll':>7} {'qok_lf':>8}")
    for key, r in sorted(viable_combos, key=lambda x: x[1]['identical_adj']):
        print(f"  {key:<25} {r['identical_adj']:>9.4f} {r['ss_mean']:>8.3f} "
              f"{r['am_ll']:>7.3f} {r['y_lf']:>7.3f} {r['d_ll']:>7.3f} {r['qok_lf']:>8.3f}")

    # Do any viable combos also reproduce positional metrics?
    pos_viable = [(k, r) for k, r in viable_combos
                  if r['am_ll'] >= 3.0 or r['y_lf'] >= 2.0 or r['d_ll'] >= 1.3]
    print(f"\nViable combos that ALSO approach positional metrics (am_ll≥3 or y_lf≥2 or d_ll≥1.3): {len(pos_viable)}")
else:
    print("  → NO viable zone exists. Falsification holds across full parameter space.")

# Summary table: best identicalAdj and best ss_mean, by copy_prob
print(f"\n── SUMMARY BY COPY_PROB (averaged over modify_prob × window) ──")
print(f"  {'cp':>5} {'adj_rate mean':>14} {'adj_rate min':>13} {'ss_mean mean':>13}")
for cp in COPY_PROBS:
    subset = [r for r in results.values() if r['copy_prob'] == cp]
    if subset:
        adj_mean = sum(r['identical_adj'] for r in subset) / len(subset)
        adj_min  = min(r['identical_adj'] for r in subset)
        ss_mean  = sum(r['ss_mean'] for r in subset) / len(subset)
        print(f"  {cp:>5} {adj_mean:>14.4f} {adj_min:>13.4f} {ss_mean:>13.3f}")

print(f"\n── SUMMARY BY MODIFY_PROB (averaged over copy_prob × window) ──")
print(f"  {'mp':>5} {'adj_rate mean':>14} {'adj_rate min':>13} {'ss_mean mean':>13}")
for mp in MODIFY_PROBS:
    subset = [r for r in results.values() if r['modify_prob'] == mp]
    if subset:
        adj_mean = sum(r['identical_adj'] for r in subset) / len(subset)
        adj_min  = min(r['identical_adj'] for r in subset)
        ss_mean  = sum(r['ss_mean'] for r in subset) / len(subset)
        print(f"  {mp:>5} {adj_mean:>14.4f} {adj_min:>13.4f} {ss_mean:>13.3f}")

print(f"\n── POSITIONAL METRICS ACROSS ALL COMBOS ──")
am_vals = [r['am_ll'] for r in results.values()]
y_vals  = [r['y_lf']  for r in results.values()]
d_vals  = [r['d_ll']  for r in results.values()]
print(f"  -am LL: min={min(am_vals):.3f}, max={max(am_vals):.3f}, mean={sum(am_vals)/len(am_vals):.3f}  (VMS={VMS_AM_LL:.3f})")
print(f"  y-LF:   min={min(y_vals):.3f}, max={max(y_vals):.3f}, mean={sum(y_vals)/len(y_vals):.3f}  (VMS={VMS_Y_LF:.3f})")
print(f"  d-LL:   min={min(d_vals):.3f}, max={max(d_vals):.3f}, mean={sum(d_vals)/len(d_vals):.3f}  (VMS={VMS_D_LL:.3f})")

print(f"\n── PARADOX DEMONSTRATION: adj_rate vs ss_mean trade-off ──")
print("The key prediction: reducing COPY_PROB reduces adj_rate but also reduces ss_mean.")
print("If VMS requires ss_mean ≥ 1.1 AND adj_rate ≤ 0.0135, no Timm combo can do both.")
print(f"\nBest combos by lowest adj_rate:")
sorted_adj = sorted(results.values(), key=lambda r: r['identical_adj'])
for r in sorted_adj[:5]:
    print(f"  cp={r['copy_prob']}, mp={r['modify_prob']}, win={r['window']}: "
          f"adj={r['identical_adj']:.4f}, ss_mean={r['ss_mean']:.3f}")
print(f"\nBest combos by highest ss_mean:")
sorted_ss = sorted(results.values(), key=lambda r: -r['ss_mean'])
for r in sorted_ss[:5]:
    print(f"  cp={r['copy_prob']}, mp={r['modify_prob']}, win={r['window']}: "
          f"adj={r['identical_adj']:.4f}, ss_mean={r['ss_mean']:.3f}")

print("\nDone.")
