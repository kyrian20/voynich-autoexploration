"""
exp_177: Position-Sensitive Cipher Simulation

Tests whether a polyalphabetic cipher with separate encoding tables for
line-first (LF), middle (MID), and line-final (LL) positions can reproduce
the VMS positional grammar findings that the position-blind Naibbe cipher failed on.

Design:
  Three cipher tables, each mapping Latin word-type features to EVA onset+suffix classes.
  - LF table: calibrated to map clause-initial Latin word types to y/s/t-onset EVA words
  - MID table: uniform mapping (like Naibbe)
  - LL table: calibrated to map Latin clause-final morphemes (-am, -um, -us, -ae) to EVA -am words

Latin plaintext source: Cicero De Officiis (Latin text extracted from bilingual edition).

Method:
  1. Parse Latin text into sentences
  2. Break each sentence into simulated "lines" using VMS B-dialect length distribution
  3. Apply position-sensitive cipher: LF words → LF table, LL words → LL table, MID → MID table
  4. Measure same four core positional metrics used in exp_170 and exp_176
  5. Compare against VMS B-dialect values

Three calibration levels tested for the LL table:
  - STRONG: 90% of LL words ending in Latin clause-final morphemes → EVA -am words
  - MODERATE: 50% of LL words ending in Latin clause-final morphemes → EVA -am words
  - WEAK: 20% of LL words ending in Latin clause-final morphemes → EVA -am words

This tests whether ANY level of position-sensitive encoding can reproduce
the VMS -am LL enrichment of 6.811×.
"""

import os, sys, re, random, json
from collections import Counter, defaultdict

REPO_DIR = os.path.expanduser('~/voynich-cryptanalyst')
VMS_CORPUS = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
OUT_DIR = os.path.join(REPO_DIR, 'experiments/exp_177_position_sensitive_cipher/data')
os.makedirs(OUT_DIR, exist_ok=True)

N_SIMS = 100
TARGET_LINES = 2447  # Match VMS B-dialect line count

# ─── ONSET/SUFFIX EVA VOCABULARY ──────────────────────────────────────────────
# Build a synthetic EVA vocabulary from VMS B-dialect statistics
# Onset classes with their approximate B-dialect frequencies
ONSET_WEIGHTS = {
    'qok': 0.121, 'qo': 0.034, 'cth': 0.003, 'ch': 0.064, 'sh': 0.090,
    'ok': 0.066, 'd': 0.068, 's': 0.028, 'y': 0.041, 'k': 0.022,
    't': 0.020, 'l': 0.058, 'other': 0.111,
}

# Suffix classes with approximate B-dialect frequencies
SUFFIX_WEIGHTS = {
    'am': 0.020,     # -am: the target LL suffix
    'aiin': 0.103,
    'edy': 0.183,
    'ain': 0.070,
    'ey': 0.040,
    'ol': 0.063,
    'or': 0.033,
    'al': 0.055,
    'ar': 0.074,
    'dy': 0.030,
    'other': 0.329,
}

def make_word(onset, suffix):
    """Construct a synthetic EVA word from onset + core + suffix."""
    cores = ['a', 'ai', 'o', 'oi', 'e', 'ei']
    core = random.choice(cores)
    return onset + core + suffix

def random_eva_word(onset_weights=None, suffix_weights=None, rng=None):
    """Generate a random EVA word from onset/suffix distributions."""
    if rng is None:
        rng = random
    if onset_weights is None:
        onset_weights = ONSET_WEIGHTS
    if suffix_weights is None:
        suffix_weights = SUFFIX_WEIGHTS
    onset = rng.choices(list(onset_weights.keys()), weights=list(onset_weights.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
    return make_word(onset, suffix)

# ─── LATIN MORPHOLOGY DETECTION ───────────────────────────────────────────────

# Latin clause-final morphemes (accusative, nominative, genitive)
# These are the forms that commonly appear at end of Latin clauses/sentences
LATIN_CLAUSE_FINAL = re.compile(r'(am|um|us|em|is|ae|orum|bus|unt|it|ant|at)$', re.I)

# Latin clause-initial patterns (common Latin sentence starters)
# Simple initial consonant patterns that correspond to y/s/t-onset EVA words
LATIN_CLAUSE_INITIAL_S = re.compile(r'^[Ss][aeiouAEIOU]', re.I)  # s-initial → s-onset EVA
LATIN_CLAUSE_INITIAL_T = re.compile(r'^[Tt][aeiouAEIOU]', re.I)  # t-initial → t-onset EVA
LATIN_CLAUSE_INITIAL_Y_ANALOG = re.compile(r'^[Qq][uU]|^[Nn]o|^[Ee]t\b|^[Aa]t\b', re.I)  # conjunctions → y-onset

LF_ONSET_MAP = {
    'S_INITIAL': ('s', 0.80),    # s-initial Latin → s-onset EVA (prob)
    'T_INITIAL': ('t', 0.80),    # t-initial Latin → t-onset EVA
    'Y_ANALOG':  ('y', 0.85),    # conjunctions → y-onset (strongest LF preference in VMS)
    'OTHER':     (None, 0.0),    # other → random from MID table
}

# ─── PARSE LATIN CORPUS ───────────────────────────────────────────────────────

def extract_latin_sentences(path):
    """Extract Latin text from Cicero bilingual edition. Latin lines follow book headers."""
    sentences = []
    current = []

    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()

    # Extract only the Latin portions — lines between LIBER markers before English paragraphs
    # Strategy: take all words from the text, filter to Latin-looking words (no English stopwords)
    # Simple heuristic: Latin text has many -um, -us, -am, -is endings; English does not
    english_stopwords = {'the', 'and', 'of', 'to', 'a', 'in', 'that', 'is', 'was', 'he',
                         'it', 'for', 'on', 'are', 'as', 'with', 'his', 'they', 'at',
                         'be', 'this', 'have', 'from', 'or', 'had', 'by', 'not', 'but',
                         'what', 'all', 'were', 'we', 'when', 'your', 'can', 'said',
                         'there', 'use', 'an', 'each', 'which', 'she', 'do', 'how',
                         'their', 'if', 'will', 'up', 'other', 'about', 'out', 'many',
                         'then', 'them', 'these', 'so', 'some', 'her', 'would', 'make',
                         'like', 'him', 'into', 'time', 'has', 'look', 'two', 'more'}

    # Split into paragraphs; keep paragraphs with low English stopword density
    paragraphs = re.split(r'\n\s*\n', text)
    latin_words = []
    for para in paragraphs:
        words = re.findall(r'\b[a-zA-Z]+\b', para)
        if not words:
            continue
        english_ratio = sum(1 for w in words if w.lower() in english_stopwords) / len(words)
        if english_ratio < 0.08:  # Low English stopword density → likely Latin
            latin_words.extend(words)

    # Group into pseudo-sentences of 8-15 words (VMS line-analogous chunks)
    i = 0
    while i < len(latin_words) - 3:
        n = random.randint(8, 15)
        sentences.append(latin_words[i:i+n])
        i += n

    return sentences

# ─── POSITION-SENSITIVE CIPHER ────────────────────────────────────────────────

def cipher_lf_word(latin_word, rng, calibration_strength):
    """
    Map a Latin line-first word to an EVA word.
    calibration_strength: 'strong'=high prob of preferred onset, 'weak'=low prob.
    """
    probs = {'strong': 0.90, 'moderate': 0.60, 'weak': 0.30}
    p = probs.get(calibration_strength, 0.60)

    w = latin_word.lower()
    if LATIN_CLAUSE_INITIAL_Y_ANALOG.match(w):
        if rng.random() < p:
            return make_word('y', rng.choices(list(SUFFIX_WEIGHTS.keys()),
                                              weights=list(SUFFIX_WEIGHTS.values()))[0])
    elif LATIN_CLAUSE_INITIAL_T.match(w):
        if rng.random() < p:
            return make_word('t', rng.choices(list(SUFFIX_WEIGHTS.keys()),
                                              weights=list(SUFFIX_WEIGHTS.values()))[0])
    elif LATIN_CLAUSE_INITIAL_S.match(w):
        if rng.random() < p:
            return make_word('s', rng.choices(list(SUFFIX_WEIGHTS.keys()),
                                              weights=list(SUFFIX_WEIGHTS.values()))[0])
    # Default: random from general distribution
    return random_eva_word(rng=rng)

def cipher_ll_word(latin_word, rng, calibration_strength):
    """
    Map a Latin line-last word to an EVA word.
    If word has clause-final morpheme, map to -am with calibrated probability.
    """
    probs = {'strong': 0.90, 'moderate': 0.50, 'weak': 0.20}
    p = probs.get(calibration_strength, 0.50)

    w = latin_word.lower()
    if LATIN_CLAUSE_FINAL.search(w):
        if rng.random() < p:
            # Map to -am suffix with onset from qok/ok/d (most common LL onsets in VMS)
            ll_onsets = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
            onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
            return make_word(onset, 'am')
    # Default: random from general distribution
    return random_eva_word(rng=rng)

def cipher_mid_word(latin_word, rng):
    """Map a Latin mid-line word to an EVA word (position-blind, like Naibbe)."""
    return random_eva_word(rng=rng)

def generate_cipher_corpus(sentences, rng, calibration_strength, target_lines):
    """
    Apply position-sensitive cipher to Latin sentences, breaking into lines
    matching VMS B-dialect length distribution.
    """
    lines = []
    ll_mean, ll_std = 8.4, 3.0

    # Flatten sentences into word stream
    all_words = [w for sent in sentences for w in sent if re.match(r'[a-zA-Z]', w)]
    rng.shuffle(all_words)  # Randomize order to avoid sentence-boundary artifacts

    pos = 0
    while len(lines) < target_lines and pos < len(all_words) - 2:
        n = max(2, min(20, round(rng.gauss(ll_mean, ll_std))))
        chunk = all_words[pos:pos+n]
        if len(chunk) < 2:
            pos += len(chunk)
            continue

        # Apply position-sensitive cipher
        eva_line = []
        for i, latin_word in enumerate(chunk):
            if i == 0:
                eva_word = cipher_lf_word(latin_word, rng, calibration_strength)
            elif i == len(chunk) - 1:
                eva_word = cipher_ll_word(latin_word, rng, calibration_strength)
            else:
                eva_word = cipher_mid_word(latin_word, rng)
            eva_line.append(eva_word)

        lines.append(eva_line)
        pos += n

    return lines[:target_lines]

# ─── VMS METRICS ──────────────────────────────────────────────────────────────

def get_onset(word):
    w = word
    if w.startswith('qok'): return 'qok'
    if w.startswith('qo'):  return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('ch'):  return 'ch'
    if w.startswith('sh'):  return 'sh'
    if w.startswith('ok'):  return 'ok'
    if w.startswith('d'):   return 'd'
    if w.startswith('s'):   return 's'
    if w.startswith('y'):   return 'y'
    if w.startswith('t'):   return 't'
    if w.startswith('l'):   return 'l'
    return 'other'

def compute_metrics(lines):
    all_words = [w for line in lines for w in line]
    n = len(all_words)
    if n < 100:
        return None

    onset_counts = Counter(get_onset(w) for w in all_words)
    lf_words = [line[0] for line in lines if line]
    ll_words = [line[-1] for line in lines if len(line) > 1]
    n_lf = len(lf_words)
    n_ll = len(ll_words)

    def pos_enr(words_at_pos, test_fn, baseline_rate, n_pos):
        if n_pos == 0 or baseline_rate == 0:
            return 1.0
        obs = sum(1 for w in words_at_pos if test_fn(w))
        return (obs / n_pos) / baseline_rate

    am_ll = pos_enr(ll_words, lambda w: w.endswith('am'),
                    sum(1 for w in all_words if w.endswith('am')) / n, n_ll)
    y_lf  = pos_enr(lf_words, lambda w: get_onset(w) == 'y',
                    onset_counts['y'] / n, n_lf)
    d_ll  = pos_enr(ll_words, lambda w: get_onset(w) == 'd',
                    onset_counts['d'] / n, n_ll)
    qok_lf = pos_enr(lf_words, lambda w: get_onset(w) == 'qok',
                     onset_counts['qok'] / n, n_lf)

    # Self-succession
    total_bg = len(all_words) - 1
    bg_onset = Counter((get_onset(all_words[i]), get_onset(all_words[i+1]))
                       for i in range(total_bg))
    def ss_enr(onset):
        base = onset_counts[onset] / n
        return bg_onset[(onset, onset)] / (total_bg * base * base) if base > 0 and total_bg > 0 else 1.0

    qok_ss = ss_enr('qok')
    ok_ss  = ss_enr('ok')
    ch_ss  = ss_enr('ch')
    ss_mean = (qok_ss + ok_ss + ch_ss) / 3

    # Identical adjacent word rate
    adj_same = sum(1 for i in range(total_bg) if all_words[i] == all_words[i+1])
    ident_adj = adj_same / total_bg if total_bg > 0 else 0

    return {
        'am_ll': am_ll, 'y_lf': y_lf, 'd_ll': d_ll, 'qok_lf': qok_lf,
        'qok_ss': qok_ss, 'ok_ss': ok_ss, 'ch_ss': ch_ss, 'ss_mean': ss_mean,
        'ident_adj': ident_adj,
    }

# ─── MAIN ─────────────────────────────────────────────────────────────────────

print("Extracting Latin sentences from Cicero corpus...")
random.seed(42)
sentences = extract_latin_sentences(LATIN_CORPUS)
print(f"Extracted {len(sentences)} pseudo-sentences ({sum(len(s) for s in sentences)} words)")

# VMS B-dialect targets
VMS = {
    'am_ll': 6.811, 'y_lf': 3.506, 'd_ll': 1.464, 'qok_lf': 0.839,
    'ss_mean': (1.239 + 1.462 + 1.694) / 3,
}

calibration_levels = ['strong', 'moderate', 'weak']
all_results = {}

for cal in calibration_levels:
    print(f"\nRunning {N_SIMS} simulations (calibration={cal})...")
    sim_metrics = []
    for sim_i in range(N_SIMS):
        rng = random.Random(sim_i * 1000 + hash(cal) % 1000)
        lines = generate_cipher_corpus(sentences, rng, cal, TARGET_LINES)
        m = compute_metrics(lines)
        if m:
            sim_metrics.append(m)

    if sim_metrics:
        keys = sim_metrics[0].keys()
        avg = {k: sum(s[k] for s in sim_metrics) / len(sim_metrics) for k in keys}
        # Compute 95% CI
        def ci(vals):
            vals_sorted = sorted(vals)
            n = len(vals_sorted)
            lo = vals_sorted[max(0, int(n * 0.025))]
            hi = vals_sorted[min(n-1, int(n * 0.975))]
            return lo, hi
        ci_dict = {k: ci([s[k] for s in sim_metrics]) for k in keys}
        all_results[cal] = {'avg': avg, 'ci': ci_dict, 'n': len(sim_metrics)}

# Save results
out_path = os.path.join(OUT_DIR, 'cipher_results.json')
with open(out_path, 'w') as f:
    json.dump({k: {'avg': v['avg'], 'ci': {m: list(v['ci'][m]) for m in v['ci']}, 'n': v['n']}
               for k, v in all_results.items()}, f, indent=2)

# ─── REPORT ───────────────────────────────────────────────────────────────────

print(f"\n{'='*80}")
print("POSITION-SENSITIVE CIPHER: RESULTS")
print(f"{'='*80}")

print(f"\n{'Metric':<12} {'VMS':>8}", end='')
for cal in calibration_levels:
    print(f" {'Cipher-'+cal:>20}", end='')
print()
print("-" * (12 + 8 + 20 * len(calibration_levels) + 3))

metrics_to_show = [
    ('am_ll', '-am LL'),
    ('y_lf', 'y-onset LF'),
    ('d_ll', 'd-onset LL'),
    ('qok_lf', 'qok LF'),
    ('ss_mean', 'ss_mean'),
    ('ident_adj', 'adj_rate'),
]

for key, label in metrics_to_show:
    vms_val = VMS.get(key, 0.009 if key == 'ident_adj' else None)
    print(f"{label:<12}", end='')
    if vms_val is not None:
        print(f" {vms_val:>8.3f}", end='')
    else:
        print(f" {'?':>8}", end='')
    for cal in calibration_levels:
        if cal in all_results:
            avg = all_results[cal]['avg'].get(key, 0)
            lo, hi = all_results[cal]['ci'].get(key, (0, 0))
            # Status: is VMS inside CI?
            if vms_val is not None:
                if vms_val > hi:
                    status = "ABOVE"
                elif vms_val < lo:
                    status = "BELOW"
                else:
                    status = "inside"
            else:
                status = "?"
            print(f" {avg:>6.3f}[{lo:.3f},{hi:.3f}]{status:>6}", end='')
    print()

print(f"\n{'='*80}")
print("KEY QUESTION: Can any calibration level reproduce -am LL enrichment ≥ 3.0×?")
print(f"{'='*80}")
for cal in calibration_levels:
    if cal in all_results:
        am = all_results[cal]['avg']['am_ll']
        lo, hi = all_results[cal]['ci']['am_ll']
        print(f"  {cal:>10}: am_ll = {am:.3f} [95% CI: {lo:.3f}, {hi:.3f}]  (VMS = 6.811)")

print(f"\nConclusion:")
best_am = max(all_results[cal]['avg']['am_ll'] for cal in calibration_levels if cal in all_results)
print(f"  Best -am LL enrichment achieved: {best_am:.3f} vs VMS 6.811")
if best_am >= 3.0:
    print("  → Position-sensitive cipher PARTIALLY reproduces -am LL (≥ 3.0×)")
    print("  → Check if other metrics also satisfied")
else:
    print("  → Position-sensitive cipher DOES NOT reproduce -am LL enrichment at VMS level")
    print("  → Strong calibration (90% LL -am mapping) required to approach VMS values")

print("\nDone.")
