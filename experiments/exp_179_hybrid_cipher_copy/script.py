"""
exp_179: Hybrid Position-Sensitive Cipher + Copy Component

Tests whether combining exp_177's position-sensitive cipher (strong calibration)
with a Timm-style local copy buffer can simultaneously satisfy the dual constraint:
  (1) Position-sensitive grammar: -am LL ≥ 5.0×, y-onset LF ≥ 2.0×
  (2) Sequential structure:       ss_mean ∈ [1.2, 1.7], adj_rate ≤ 0.015

Design:
  For each word to generate, with probability COPY_PROB:
    → Draw from a recent WINDOW=20 word buffer (Timm-style copy)
    → With probability MODIFY_PROB, replace the onset of the copied word
  Otherwise:
    → Apply position-sensitive cipher (LF/MID/LL tables from exp_177 strong calibration)

This tests whether a hybrid mechanism can satisfy constraints that neither
pure substitution (exp_177) nor pure copying (Timm) can satisfy alone.

Grid: COPY_PROB ∈ {0.2, 0.3, 0.4, 0.5} × MODIFY_PROB ∈ {0.3, 0.4, 0.5, 0.6}
      = 16 combinations × 50 simulations each = 800 total runs.

Three-constraint viability:
  -am LL ≥ 5.0×  AND  ss_mean ∈ [1.2, 1.7]  AND  adj_rate ≤ 0.015
"""
from pathlib import Path as _RepositoryPath

import os, re, random, json, math
from collections import Counter, deque

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
OUT_DIR   = os.path.join(REPO_DIR, 'experiments/exp_179_hybrid_cipher_copy/data')
os.makedirs(OUT_DIR, exist_ok=True)

N_SIMS       = 50
TARGET_LINES = 2447
WINDOW       = 20   # Copy buffer size (same as Timm default-ish)

# ── EVA vocabulary distributions (identical to exp_177) ─────────────────────
ONSET_WEIGHTS = {
    'qok': 0.121, 'qo': 0.034, 'cth': 0.003, 'ch': 0.064, 'sh': 0.090,
    'ok': 0.066, 'd': 0.068, 's': 0.028, 'y': 0.041, 'k': 0.022,
    't': 0.020, 'l': 0.058, 'other': 0.111,
}
SUFFIX_WEIGHTS = {
    'am': 0.020, 'aiin': 0.103, 'edy': 0.183, 'ain': 0.070, 'ey': 0.040,
    'ol': 0.063, 'or': 0.033, 'al': 0.055, 'ar': 0.074, 'dy': 0.030, 'other': 0.329,
}

# ── Latin morphology patterns (identical to exp_177) ─────────────────────────
LATIN_CLAUSE_FINAL         = re.compile(r'(am|um|us|em|is|ae|orum|bus|unt|it|ant|at)$', re.I)
LATIN_CLAUSE_INITIAL_S     = re.compile(r'^[Ss][aeiouAEIOU]', re.I)
LATIN_CLAUSE_INITIAL_T     = re.compile(r'^[Tt][aeiouAEIOU]', re.I)
LATIN_CLAUSE_INITIAL_Y     = re.compile(r'^[Qq][uU]|^[Nn]o|^[Ee]t\b|^[Aa]t\b', re.I)

def make_word(onset, suffix, rng):
    cores = ['a', 'ai', 'o', 'oi', 'e', 'ei']
    return onset + rng.choice(cores) + suffix

def random_eva_word(rng):
    onset  = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
    suffix = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
    return make_word(onset, suffix, rng)

def cipher_lf(latin_word, rng, p=0.90):
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
    w = latin_word.lower()
    if LATIN_CLAUSE_FINAL.search(w) and rng.random() < p:
        ll_onsets = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return make_word(onset, 'am', rng)
    return random_eva_word(rng)

# ── Latin corpus loader (identical to exp_177) ────────────────────────────────
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

# ── Hybrid corpus generator ───────────────────────────────────────────────────
def generate_hybrid_corpus(sentences, rng, copy_prob, modify_prob):
    """
    For each word position:
      With prob COPY_PROB: copy a word from a recent WINDOW-word buffer.
        → With prob MODIFY_PROB: replace the onset of the copied word.
      Otherwise: apply position-sensitive cipher (strong calibration).
    """
    all_latin = [w for sent in sentences for w in sent if re.match(r'[a-zA-Z]', w)]
    rng.shuffle(all_latin)

    lines  = []
    buffer = deque(maxlen=WINDOW)   # Recent word buffer for copying
    pos    = 0

    while len(lines) < TARGET_LINES and pos < len(all_latin) - 2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = all_latin[pos:pos+n]
        if len(chunk) < 2:
            pos += len(chunk)
            continue

        eva_line = []
        for i, latin_word in enumerate(chunk):
            # Decide: copy from buffer or use cipher?
            if buffer and rng.random() < copy_prob:
                # Copy a recent word
                copied = rng.choice(list(buffer))
                if rng.random() < modify_prob:
                    # Modify: replace onset with a random onset
                    new_onset = rng.choices(list(ONSET_WEIGHTS.keys()),
                                            weights=list(ONSET_WEIGHTS.values()))[0]
                    # Extract suffix from copied word (everything after onset)
                    for prefix in sorted(ONSET_WEIGHTS.keys(), key=len, reverse=True):
                        if copied.startswith(prefix):
                            suffix_part = copied[len(prefix):]
                            copied = new_onset + suffix_part
                            break
                eva_word = copied
            else:
                # Use position-sensitive cipher
                if i == 0:
                    eva_word = cipher_lf(latin_word, rng)
                elif i == len(chunk) - 1:
                    eva_word = cipher_ll(latin_word, rng)
                else:
                    eva_word = random_eva_word(rng)

            eva_line.append(eva_word)
            buffer.append(eva_word)

        lines.append(eva_line)
        pos += n

    return lines[:TARGET_LINES]

# ── Metrics ───────────────────────────────────────────────────────────────────
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

    # Self-succession
    total_bg = len(all_words) - 1
    bg = Counter((get_onset(all_words[i]), get_onset(all_words[i+1]))
                 for i in range(total_bg))
    def ss(onset):
        base = onset_counts[onset] / n
        return bg[(onset, onset)] / (total_bg * base * base) if base > 0 and total_bg > 0 else 1.0
    ss_mean = (ss('qok') + ss('ok') + ss('ch')) / 3

    # Identical adjacent word rate
    adj_same = sum(1 for i in range(total_bg) if all_words[i] == all_words[i+1])
    adj_rate = adj_same / total_bg if total_bg > 0 else 0

    return {'am_ll': am_ll, 'y_lf': y_lf, 'ss_mean': ss_mean, 'adj_rate': adj_rate}

# ── Main sweep ────────────────────────────────────────────────────────────────
print("Extracting Latin sentences...")
random.seed(42)
sentences = extract_latin_sentences(LATIN_CORPUS)
print(f"Extracted {len(sentences)} pseudo-sentences ({sum(len(s) for s in sentences)} words)")

COPY_PROBS   = [0.2, 0.3, 0.4, 0.5]
MODIFY_PROBS = [0.3, 0.4, 0.5, 0.6]

# VMS targets
VMS = {'am_ll': 6.811, 'y_lf': 3.506, 'ss_mean': 1.465, 'adj_rate': 0.009}
# Three-constraint viability thresholds
VIABLE_AM_LL   = 5.0
VIABLE_SS_LO   = 1.2
VIABLE_SS_HI   = 1.7
VIABLE_ADJ_MAX = 0.015

all_results = {}
combo_count = 0
total_combos = len(COPY_PROBS) * len(MODIFY_PROBS)

for cp in COPY_PROBS:
    for mp in MODIFY_PROBS:
        key = f"cp={cp},mp={mp}"
        combo_count += 1
        print(f"  [{combo_count}/{total_combos}] {key} ...", end=' ', flush=True)

        sim_metrics = []
        for sim_i in range(N_SIMS):
            rng = random.Random(sim_i * 100 + int(cp * 1000) + int(mp * 10000))
            lines = generate_hybrid_corpus(sentences, rng, cp, mp)
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

        avg = {k: sum(s[k] for s in sim_metrics) / len(sim_metrics) for k in sim_metrics[0]}
        cis = {k: ci95([s[k] for s in sim_metrics]) for k in sim_metrics[0]}

        viable = (avg['am_ll'] >= VIABLE_AM_LL and
                  VIABLE_SS_LO <= avg['ss_mean'] <= VIABLE_SS_HI and
                  avg['adj_rate'] <= VIABLE_ADJ_MAX)

        all_results[key] = {
            'copy_prob': cp, 'modify_prob': mp,
            'avg': avg, 'ci': {k: list(v) for k, v in cis.items()},
            'n': len(sim_metrics), 'viable': viable
        }
        print(f"am_ll={avg['am_ll']:.3f} ss={avg['ss_mean']:.3f} adj={avg['adj_rate']:.4f} "
              f"{'*** VIABLE ***' if viable else ''}")

# Save
with open(os.path.join(OUT_DIR, 'hybrid_results.json'), 'w') as f:
    json.dump(all_results, f, indent=2)

# ── Report ────────────────────────────────────────────────────────────────────
print(f"\n{'='*80}")
print("HYBRID CIPHER-COPY: RESULTS SUMMARY")
print(f"{'='*80}")
print(f"\nVMS targets: am_ll={VMS['am_ll']}, y_lf={VMS['y_lf']}, "
      f"ss_mean={VMS['ss_mean']:.3f}, adj_rate={VMS['adj_rate']}")
print(f"Viability thresholds: am_ll≥{VIABLE_AM_LL}, ss∈[{VIABLE_SS_LO},{VIABLE_SS_HI}], "
      f"adj≤{VIABLE_ADJ_MAX}")

print(f"\n{'cp':>5} {'mp':>5} {'am_ll':>8} {'y_lf':>8} {'ss_mean':>8} {'adj_rate':>10} {'viable':>8}")
print("-" * 60)
for key, r in sorted(all_results.items()):
    v = r['avg']
    print(f"{r['copy_prob']:>5.1f} {r['modify_prob']:>5.1f} "
          f"{v['am_ll']:>8.3f} {v['y_lf']:>8.3f} {v['ss_mean']:>8.3f} "
          f"{v['adj_rate']:>10.4f} {'YES' if r['viable'] else 'no':>8}")

viable_combos = [k for k, r in all_results.items() if r['viable']]
print(f"\nViable combinations (all 3 constraints met): {len(viable_combos)}/{total_combos}")
if viable_combos:
    print("Viable:")
    for k in viable_combos:
        r = all_results[k]
        print(f"  {k}: am_ll={r['avg']['am_ll']:.3f}, ss={r['avg']['ss_mean']:.3f}, "
              f"adj={r['avg']['adj_rate']:.4f}")

# Trade-off analysis
print(f"\n--- Closest to satisfying all 3 constraints ---")
def distance_to_viable(r):
    v = r['avg']
    d_am  = max(0, VIABLE_AM_LL - v['am_ll'])
    d_ss  = max(0, VIABLE_SS_LO - v['ss_mean']) + max(0, v['ss_mean'] - VIABLE_SS_HI)
    d_adj = max(0, v['adj_rate'] - VIABLE_ADJ_MAX)
    return d_am + d_ss * 5 + d_adj * 50   # weight adj heavily

ranked = sorted(all_results.items(), key=lambda kv: distance_to_viable(kv[1]))
for k, r in ranked[:5]:
    v = r['avg']
    print(f"  {k}: am_ll={v['am_ll']:.3f}, ss={v['ss_mean']:.3f}, adj={v['adj_rate']:.4f}")

# Effect of copy_prob on each metric
print(f"\n--- Effect of COPY_PROB on metrics (mean across MODIFY_PROB) ---")
print(f"{'cp':>5} {'am_ll_mean':>12} {'ss_mean_mean':>14} {'adj_rate_mean':>15}")
for cp in COPY_PROBS:
    matches = [r for r in all_results.values() if r['copy_prob'] == cp]
    if matches:
        am_m  = sum(r['avg']['am_ll']    for r in matches) / len(matches)
        ss_m  = sum(r['avg']['ss_mean']  for r in matches) / len(matches)
        adj_m = sum(r['avg']['adj_rate'] for r in matches) / len(matches)
        print(f"{cp:>5.1f} {am_m:>12.3f} {ss_m:>14.3f} {adj_m:>15.4f}")

print(f"\nDone. Results saved to data/hybrid_results.json")
