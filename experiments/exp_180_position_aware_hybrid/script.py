"""
exp_180: Position-Aware Hybrid Cipher + Copy Component

Motivation:
  exp_179 tested a hybrid where the copy buffer was POSITION-BLIND — copies
  could fire at any line position, including LF and LL, which diluted the
  -am LL cipher signal. Result: 0/16 viable, with a linear am_ll vs ss_mean
  trade-off across COPY_PROB.

  This experiment tests the POSITION-AWARE hybrid: the architecture that
  exp_179's result.md identified as the "escape hatch" not yet closed.

Architecture:
  LF positions: ALWAYS use position-sensitive cipher (strong calibration, p=0.90).
                Never copy at LF.
  LL positions: ALWAYS use position-sensitive cipher (strong calibration, p=0.90).
                Never copy at LL.
  MID positions: With probability COPY_PROB, copy from a MID-ONLY buffer.
                 With probability (1-COPY_PROB), use the MID cipher table.

Key design difference from exp_179:
  - The copy buffer contains ONLY MID-position tokens (not LF or LL tokens).
  - Copies fire ONLY at MID positions.
  - LF and LL tokens are generated solely by the position-sensitive cipher.

This decouples the two signals:
  - am_ll enrichment: governed entirely by the LL cipher table (uncontaminated by copies)
  - ss_mean: governed by MID copying (copy buffer is pure MID distribution)

Grid: COPY_PROB ∈ {0.2, 0.3, 0.4, 0.5, 0.6, 0.7}
      × MODIFY_PROB ∈ {0.3, 0.4, 0.5}
      = 18 combinations × 50 simulations = 900 total runs.

Viability (same as exp_179):
  am_ll ≥ 5.0×  AND  ss_mean ∈ [1.2, 1.7]  AND  adj_rate ≤ 0.015

Seed base: 180000 (main run); 180999 (verification run, 10 sims at best combo).
"""
from pathlib import Path as _RepositoryPath

import os, re, random, json, math
from collections import Counter, deque

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
OUT_DIR      = os.path.join(REPO_DIR, 'experiments/exp_180_position_aware_hybrid/data')
os.makedirs(OUT_DIR, exist_ok=True)

N_SIMS       = 50
TARGET_LINES = 2447
WINDOW       = 20   # MID-only copy buffer size

# ── EVA vocabulary distributions (identical to exp_177 / exp_179) ────────────
ONSET_WEIGHTS = {
    'qok': 0.121, 'qo': 0.034, 'cth': 0.003, 'ch': 0.064, 'sh': 0.090,
    'ok': 0.066, 'd': 0.068, 's': 0.028, 'y': 0.041, 'k': 0.022,
    't': 0.020, 'l': 0.058, 'other': 0.111,
}
SUFFIX_WEIGHTS = {
    'am': 0.020, 'aiin': 0.103, 'edy': 0.183, 'ain': 0.070, 'ey': 0.040,
    'ol': 0.063, 'or': 0.033, 'al': 0.055, 'ar': 0.074, 'dy': 0.030, 'other': 0.329,
}

# ── Latin morphology patterns (identical to exp_177 / exp_179) ───────────────
LATIN_CLAUSE_FINAL     = re.compile(r'(am|um|us|em|is|ae|orum|bus|unt|it|ant|at)$', re.I)
LATIN_CLAUSE_INITIAL_S = re.compile(r'^[Ss][aeiouAEIOU]', re.I)
LATIN_CLAUSE_INITIAL_T = re.compile(r'^[Tt][aeiouAEIOU]', re.I)
LATIN_CLAUSE_INITIAL_Y = re.compile(r'^[Qq][uU]|^[Nn]o|^[Ee]t\b|^[Aa]t\b', re.I)

def make_word(onset, suffix, rng):
    cores = ['a', 'ai', 'o', 'oi', 'e', 'ei']
    return onset + rng.choice(cores) + suffix

def random_eva_word(rng):
    onset  = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
    suffix = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
    return make_word(onset, suffix, rng)

def cipher_lf(latin_word, rng, p=0.90):
    """LF cipher table: target-aware (y-onset mapping — same as exp_177)."""
    w = latin_word.lower()
    if LATIN_CLAUSE_INITIAL_Y.match(w) and rng.random() < p:
        suf = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
        return make_word('y', suf, rng)
    elif LATIN_CLAUSE_INITIAL_T.match(w) and rng.random() < p:
        suf = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
        return make_word('t', suf, rng)
    elif LATIN_CLAUSE_INITIAL_S.match(w) and rng.random() < p:
        suf = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
        return make_word('s', suf, rng)
    return random_eva_word(rng)

def cipher_ll(latin_word, rng, p=0.90):
    """LL cipher table: target-aware (all clause-final morphemes → -am suffix — same as exp_177).
    NOTE: This is an explicitly target-aware mapping. All Latin clause-final morphemes
    (-um, -us, -em, -is, -ae, -orum, -bus, -unt, -it, -ant, -at) map to EVA -am.
    The code comment in exp_177 explicitly labels -am as 'the target LL suffix'.
    This is carried forward unchanged from exp_177/exp_179.
    """
    w = latin_word.lower()
    if LATIN_CLAUSE_FINAL.search(w) and rng.random() < p:
        # -am: the target LL suffix (target-aware, inherited from exp_177)
        ll_onsets = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return make_word(onset, 'am', rng)
    return random_eva_word(rng)

def cipher_mid(rng):
    """MID cipher table: uniform random EVA word (position-insensitive).
    NOT calibrated to any VMS MID-position target metric.
    """
    return random_eva_word(rng)

# ── Latin corpus loader (identical to exp_177 / exp_179) ─────────────────────
def extract_latin_sentences(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    english_stopwords = {
        'the','and','of','to','a','in','that','is','was','he','it','for','on','are',
        'as','with','his','they','at','be','this','have','from','or','had','by','not',
        'but','what','all','were','we','when','your','can','said','there','use','an',
        'each','which','she','do','how','their','if','will','up','other','about','out',
        'many','then','them','these','so','some','her','would','make','like','him',
        'into','time','has','look','two','more',
    }
    paragraphs = re.split(r'\n\s*\n', text)
    latin_words = []
    for para in paragraphs:
        words = re.findall(r'\b[a-zA-Z]+\b', para)
        if not words:
            continue
        eng_ratio = sum(1 for w in words if w.lower() in english_stopwords) / len(words)
        if eng_ratio < 0.08:
            latin_words.extend(words)
    sentences = []
    i = 0
    while i < len(latin_words) - 3:
        n = random.randint(8, 15)
        sentences.append(latin_words[i:i+n])
        i += n
    return sentences

# ── Position-aware hybrid corpus generator ────────────────────────────────────
def generate_position_aware_corpus(sentences, rng, copy_prob, modify_prob):
    """
    Position-aware hybrid:
      LF (i==0):              ALWAYS cipher_lf(). Never copy.
      LL (i==len(chunk)-1):   ALWAYS cipher_ll(). Never copy.
      MID (0 < i < len-1):   With prob copy_prob, copy from MID-ONLY buffer.
                              Otherwise: cipher_mid() (random EVA word).

    Buffer management:
      ONLY MID-position tokens are added to the buffer.
      LF and LL tokens are NEVER added.
      This ensures that copy events draw from the MID distribution only.

    Note on "only" words (single-word lines, len==1):
      If a line has exactly one word (i==0 AND i==len(chunk)-1), it is both
      LF and LL. We apply cipher_ll() for these (prioritize LL table).
      These tokens are NOT added to the MID buffer.
    """
    all_latin = [w for sent in sentences for w in sent if re.match(r'[a-zA-Z]', w)]
    rng.shuffle(all_latin)

    lines      = []
    mid_buffer = deque(maxlen=WINDOW)   # MID-only buffer — critical design choice
    pos        = 0

    while len(lines) < TARGET_LINES and pos < len(all_latin) - 2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = all_latin[pos:pos+n]
        if len(chunk) < 2:
            pos += len(chunk)
            continue

        eva_line = []
        for i, latin_word in enumerate(chunk):
            is_lf   = (i == 0)
            is_ll   = (i == len(chunk) - 1)
            is_only = (len(chunk) == 1)    # single-word line: both LF and LL
            is_mid  = (not is_lf and not is_ll)

            if is_lf and not is_only:
                # LF: always use cipher, never copy
                eva_word = cipher_lf(latin_word, rng)
                # LF tokens NOT added to MID buffer

            elif is_ll or is_only:
                # LL (or single-word): always use cipher, never copy
                eva_word = cipher_ll(latin_word, rng)
                # LL tokens NOT added to MID buffer

            else:
                # MID: position-aware copying only here
                assert is_mid
                if mid_buffer and rng.random() < copy_prob:
                    # Copy from MID-only buffer
                    copied = rng.choice(list(mid_buffer))
                    if rng.random() < modify_prob:
                        # Modify: replace onset with a random onset
                        new_onset = rng.choices(
                            list(ONSET_WEIGHTS.keys()),
                            weights=list(ONSET_WEIGHTS.values())
                        )[0]
                        for prefix in sorted(ONSET_WEIGHTS.keys(), key=len, reverse=True):
                            if copied.startswith(prefix):
                                suffix_part = copied[len(prefix):]
                                copied = new_onset + suffix_part
                                break
                    eva_word = copied
                else:
                    # No copy: use MID cipher (random EVA word)
                    eva_word = cipher_mid(rng)
                # MID tokens added to MID buffer
                mid_buffer.append(eva_word)

            eva_line.append(eva_word)

        lines.append(eva_line)
        pos += n

    return lines[:TARGET_LINES]

# ── Metrics (identical to exp_179) ────────────────────────────────────────────
def get_onset(word):
    for prefix in ['qok', 'qo', 'cth', 'ch', 'sh', 'ok', 'd', 's', 'y', 'k', 't', 'l', 'r']:
        if word.startswith(prefix):
            return prefix
    return 'other'

def compute_metrics(lines):
    all_words = [w for line in lines for w in line]
    n = len(all_words)
    if n < 100:
        return None

    onset_counts = Counter(get_onset(w) for w in all_words)
    lf_words = [line[0]  for line in lines if line]
    ll_words = [line[-1] for line in lines if len(line) > 1]
    n_lf, n_ll = len(lf_words), len(ll_words)

    def pos_enr(words_at, fn, base_rate, n_pos):
        if n_pos == 0 or base_rate == 0: return 1.0
        return (sum(1 for w in words_at if fn(w)) / n_pos) / base_rate

    am_rate  = sum(1 for w in all_words if w.endswith('am')) / n
    am_ll    = pos_enr(ll_words, lambda w: w.endswith('am'), am_rate, n_ll)
    y_rate   = onset_counts['y'] / n
    y_lf     = pos_enr(lf_words, lambda w: get_onset(w) == 'y', y_rate, n_lf)

    # Self-succession: enrichment of consecutive same-onset bigrams
    total_bg = len(all_words) - 1
    bg = Counter(
        (get_onset(all_words[i]), get_onset(all_words[i+1]))
        for i in range(total_bg)
    )
    def ss(onset):
        base = onset_counts[onset] / n
        return bg[(onset, onset)] / (total_bg * base * base) if base > 0 and total_bg > 0 else 1.0
    ss_mean = (ss('qok') + ss('ok') + ss('ch')) / 3

    # Per-onset self-succession breakdown
    ss_detail = {onset: ss(onset) for onset in ['qok', 'ok', 'ch', 'sh', 'd', 'y']}

    # Identical adjacent word rate
    adj_same = sum(1 for i in range(total_bg) if all_words[i] == all_words[i+1])
    adj_rate = adj_same / total_bg if total_bg > 0 else 0

    return {
        'am_ll': am_ll, 'y_lf': y_lf,
        'ss_mean': ss_mean, 'ss_detail': ss_detail,
        'adj_rate': adj_rate
    }

# ── Latin corpus setup ────────────────────────────────────────────────────────
print("Extracting Latin sentences...")
random.seed(42)
sentences = extract_latin_sentences(LATIN_CORPUS)
print(f"Extracted {len(sentences)} pseudo-sentences ({sum(len(s) for s in sentences)} words)")

# ── Parameter grid ────────────────────────────────────────────────────────────
COPY_PROBS   = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
MODIFY_PROBS = [0.3, 0.4, 0.5]

VMS = {'am_ll': 6.811, 'y_lf': 3.506, 'ss_mean': 1.465, 'adj_rate': 0.009}
VIABLE_AM_LL   = 5.0
VIABLE_SS_LO   = 1.2
VIABLE_SS_HI   = 1.7
VIABLE_ADJ_MAX = 0.015

# ── Main sweep ────────────────────────────────────────────────────────────────
print(f"\nRunning main sweep ({len(COPY_PROBS)*len(MODIFY_PROBS)} combinations × {N_SIMS} sims = "
      f"{len(COPY_PROBS)*len(MODIFY_PROBS)*N_SIMS} total runs). Seed base: 180000")

all_results  = {}
combo_count  = 0
total_combos = len(COPY_PROBS) * len(MODIFY_PROBS)

SEED_BASE = 180000  # Documented in result.md

for cp in COPY_PROBS:
    for mp in MODIFY_PROBS:
        key = f"cp={cp},mp={mp}"
        combo_count += 1
        print(f"  [{combo_count}/{total_combos}] {key} ...", end=' ', flush=True)

        sim_metrics = []
        for sim_i in range(N_SIMS):
            seed = SEED_BASE + sim_i * 1000 + int(cp * 100) + int(mp * 10)
            rng  = random.Random(seed)
            lines = generate_position_aware_corpus(sentences, rng, cp, mp)
            m = compute_metrics(lines)
            if m:
                sim_metrics.append(m)

        if not sim_metrics:
            print("no data")
            continue

        def ci95(vals):
            s = sorted(vals)
            n = len(s)
            return s[int(n*0.025)], s[int(n*0.975)]

        avg = {k: sum(s[k] for s in sim_metrics) / len(sim_metrics)
               for k in sim_metrics[0] if k != 'ss_detail'}
        cis = {k: ci95([s[k] for s in sim_metrics])
               for k in sim_metrics[0] if k != 'ss_detail'}
        # Per-onset ss means
        ss_detail_mean = {}
        for onset in ['qok', 'ok', 'ch', 'sh', 'd', 'y']:
            vals = [s['ss_detail'][onset] for s in sim_metrics]
            ss_detail_mean[onset] = sum(vals) / len(vals)

        viable = (avg['am_ll'] >= VIABLE_AM_LL and
                  VIABLE_SS_LO <= avg['ss_mean'] <= VIABLE_SS_HI and
                  avg['adj_rate'] <= VIABLE_ADJ_MAX)

        all_results[key] = {
            'copy_prob': cp, 'modify_prob': mp,
            'avg': avg,
            'ci': {k: list(v) for k, v in cis.items()},
            'ss_detail_mean': ss_detail_mean,
            'n': len(sim_metrics),
            'viable': viable
        }
        print(f"am_ll={avg['am_ll']:.3f} ss={avg['ss_mean']:.3f} adj={avg['adj_rate']:.4f} "
              f"{'*** VIABLE ***' if viable else ''}")

# ── Verification run ──────────────────────────────────────────────────────────
# Find best combination by joint score (am_ll × ss_mean)
def joint_score(r):
    v = r['avg']
    return v['am_ll'] * v['ss_mean']

best_key  = max(all_results, key=lambda k: joint_score(all_results[k]))
best_r    = all_results[best_key]
best_cp   = best_r['copy_prob']
best_mp   = best_r['modify_prob']

print(f"\n{'='*80}")
print(f"VERIFICATION RUN: best combination = {best_key}")
print(f"  Main run: am_ll={best_r['avg']['am_ll']:.4f}, ss_mean={best_r['avg']['ss_mean']:.4f}")
print(f"  Running 10 sims with seed base 180999...")

VERIFY_SEED_BASE = 180999
N_VERIFY = 10
verify_metrics = []
for sim_i in range(N_VERIFY):
    seed = VERIFY_SEED_BASE + sim_i
    rng  = random.Random(seed)
    lines = generate_position_aware_corpus(sentences, rng, best_cp, best_mp)
    m = compute_metrics(lines)
    if m:
        verify_metrics.append(m)

verify_am_ll  = sum(m['am_ll']  for m in verify_metrics) / len(verify_metrics)
verify_ss     = sum(m['ss_mean'] for m in verify_metrics) / len(verify_metrics)
verify_adj    = sum(m['adj_rate'] for m in verify_metrics) / len(verify_metrics)
delta_am_ll   = verify_am_ll - best_r['avg']['am_ll']
delta_ss      = verify_ss    - best_r['avg']['ss_mean']
print(f"  Verify:   am_ll={verify_am_ll:.4f} (Δ={delta_am_ll:+.4f}), "
      f"ss_mean={verify_ss:.4f} (Δ={delta_ss:+.4f}), adj={verify_adj:.4f}")

all_results['_verification'] = {
    'best_key': best_key,
    'best_cp': best_cp, 'best_mp': best_mp,
    'main_am_ll': best_r['avg']['am_ll'],
    'main_ss_mean': best_r['avg']['ss_mean'],
    'verify_am_ll': verify_am_ll,
    'verify_ss_mean': verify_ss,
    'verify_adj_rate': verify_adj,
    'delta_am_ll': delta_am_ll,
    'delta_ss_mean': delta_ss,
    'n_verify': len(verify_metrics),
    'seed_base': VERIFY_SEED_BASE,
}

# Save
with open(os.path.join(OUT_DIR, 'position_aware_results.json'), 'w') as f:
    json.dump(all_results, f, indent=2)

# ── Report ────────────────────────────────────────────────────────────────────
print(f"\n{'='*80}")
print("POSITION-AWARE HYBRID CIPHER-COPY: RESULTS SUMMARY")
print(f"{'='*80}")
print(f"\nVMS targets: am_ll={VMS['am_ll']}, y_lf={VMS['y_lf']}, "
      f"ss_mean={VMS['ss_mean']:.3f}, adj_rate={VMS['adj_rate']}")
print(f"Viability thresholds: am_ll≥{VIABLE_AM_LL}, ss∈[{VIABLE_SS_LO},{VIABLE_SS_HI}], "
      f"adj≤{VIABLE_ADJ_MAX}")

print(f"\n{'cp':>5} {'mp':>5} {'am_ll':>8} {'y_lf':>8} {'ss_mean':>8} {'adj_rate':>10} {'viable':>8}")
print("-" * 60)
for key, r in sorted(all_results.items(), key=lambda kv: (kv[1].get('copy_prob', 99), kv[1].get('modify_prob', 99))):
    if key == '_verification': continue
    v = r['avg']
    print(f"{r['copy_prob']:>5.1f} {r['modify_prob']:>5.1f} "
          f"{v['am_ll']:>8.3f} {v['y_lf']:>8.3f} {v['ss_mean']:>8.3f} "
          f"{v['adj_rate']:>10.4f} {'YES' if r['viable'] else 'no':>8}")

viable_combos = [(k, r) for k, r in all_results.items() if k != '_verification' and r.get('viable')]
print(f"\nViable combinations (all 3 constraints met): {len(viable_combos)}/{total_combos}")
if viable_combos:
    print("Viable combinations:")
    for k, r in sorted(viable_combos, key=lambda kr: -joint_score(kr[1])):
        v = r['avg']
        ci = r['ci']
        print(f"  {k}: am_ll={v['am_ll']:.3f} [{ci['am_ll'][0]:.3f},{ci['am_ll'][1]:.3f}], "
              f"ss={v['ss_mean']:.3f} [{ci['ss_mean'][0]:.3f},{ci['ss_mean'][1]:.3f}], "
              f"adj={v['adj_rate']:.4f}")

# Effect of copy_prob on each metric
print(f"\n--- Effect of COPY_PROB on metrics (mean across MODIFY_PROB) ---")
print(f"{'cp':>5} {'am_ll_mean':>12} {'ss_mean_mean':>14} {'adj_rate_mean':>15}")
for cp in COPY_PROBS:
    matches = [r for k, r in all_results.items() if k != '_verification' and r.get('copy_prob') == cp]
    if matches:
        am_m  = sum(r['avg']['am_ll']    for r in matches) / len(matches)
        ss_m  = sum(r['avg']['ss_mean']  for r in matches) / len(matches)
        adj_m = sum(r['avg']['adj_rate'] for r in matches) / len(matches)
        print(f"{cp:>5.1f} {am_m:>12.3f} {ss_m:>14.3f} {adj_m:>15.4f}")

# Comparison to exp_179 (position-blind hybrid) at matched COPY_PROB values
print(f"\n--- Comparison to exp_179 (position-blind) at matched COPY_PROB values ---")
# exp_179 results at MODIFY_PROB=0.3 (only shared MODIFY_PROB value for comparison)
EXP_179_AT_MP03 = {
    0.2: {'am_ll': 4.804, 'ss_mean': 1.075},
    0.3: {'am_ll': 4.306, 'ss_mean': 1.114},
    0.4: {'am_ll': 3.826, 'ss_mean': 1.163},
    0.5: {'am_ll': 3.359, 'ss_mean': 1.217},
}
print(f"{'cp':>5} {'E179_am':>10} {'E180_am':>10} {'Δam_ll':>10}  "
      f"{'E179_ss':>10} {'E180_ss':>10} {'Δss':>10}")
for cp in [0.2, 0.3, 0.4, 0.5]:
    key180 = f"cp={cp},mp=0.3"
    if key180 in all_results and cp in EXP_179_AT_MP03:
        e179   = EXP_179_AT_MP03[cp]
        e180_v = all_results[key180]['avg']
        print(f"{cp:>5.1f} {e179['am_ll']:>10.3f} {e180_v['am_ll']:>10.3f} "
              f"{e180_v['am_ll']-e179['am_ll']:>+10.3f}  "
              f"{e179['ss_mean']:>10.3f} {e180_v['ss_mean']:>10.3f} "
              f"{e180_v['ss_mean']-e179['ss_mean']:>+10.3f}")

print(f"\nDone. Results saved to data/position_aware_results.json")
