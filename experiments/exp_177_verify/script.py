"""
exp_177_verify: Independent reproducibility check for exp_177 strong-calibration result.

Re-runs 100 simulations of the position-sensitive cipher at strong calibration
using a completely different random seed base (999999 offset vs 0 in exp_177).
Checks whether headline -am LL = 5.756 is reproducible within noise.

This is a verification run, not a new experiment. No new design choices.
"""

import os, sys, re, random, json
from collections import Counter

REPO_DIR = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
OUT_DIR = os.path.join(REPO_DIR, 'experiments/exp_177_verify/data')
os.makedirs(OUT_DIR, exist_ok=True)

N_SIMS = 100
TARGET_LINES = 2447

# ── Onset/suffix weights (identical to exp_177) ──────────────────────────────
ONSET_WEIGHTS = {
    'qok': 0.121, 'qo': 0.034, 'cth': 0.003, 'ch': 0.064, 'sh': 0.090,
    'ok': 0.066, 'd': 0.068, 's': 0.028, 'y': 0.041, 'k': 0.022,
    't': 0.020, 'l': 0.058, 'other': 0.111,
}
SUFFIX_WEIGHTS = {
    'am': 0.020, 'aiin': 0.103, 'edy': 0.183, 'ain': 0.070, 'ey': 0.040,
    'ol': 0.063, 'or': 0.033, 'al': 0.055, 'ar': 0.074, 'dy': 0.030, 'other': 0.329,
}

LATIN_CLAUSE_FINAL = re.compile(r'(am|um|us|em|is|ae|orum|bus|unt|it|ant|at)$', re.I)
LATIN_CLAUSE_INITIAL_S = re.compile(r'^[Ss][aeiouAEIOU]', re.I)
LATIN_CLAUSE_INITIAL_T = re.compile(r'^[Tt][aeiouAEIOU]', re.I)
LATIN_CLAUSE_INITIAL_Y_ANALOG = re.compile(r'^[Qq][uU]|^[Nn]o|^[Ee]t\b|^[Aa]t\b', re.I)

def make_word(onset, suffix):
    cores = ['a', 'ai', 'o', 'oi', 'e', 'ei']
    core = random.choice(cores)
    return onset + core + suffix

def random_eva_word(rng):
    onset = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
    suffix = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
    return make_word(onset, suffix)

def extract_latin_sentences(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    english_stopwords = {'the', 'and', 'of', 'to', 'a', 'in', 'that', 'is', 'was', 'he',
                         'it', 'for', 'on', 'are', 'as', 'with', 'his', 'they', 'at',
                         'be', 'this', 'have', 'from', 'or', 'had', 'by', 'not', 'but',
                         'what', 'all', 'were', 'we', 'when', 'your', 'can', 'said',
                         'there', 'use', 'an', 'each', 'which', 'she', 'do', 'how',
                         'their', 'if', 'will', 'up', 'other', 'about', 'out', 'many',
                         'then', 'them', 'these', 'so', 'some', 'her', 'would', 'make',
                         'like', 'him', 'into', 'time', 'has', 'look', 'two', 'more'}
    paragraphs = re.split(r'\n\s*\n', text)
    latin_words = []
    for para in paragraphs:
        words = re.findall(r'\b[a-zA-Z]+\b', para)
        if not words:
            continue
        english_ratio = sum(1 for w in words if w.lower() in english_stopwords) / len(words)
        if english_ratio < 0.08:
            latin_words.extend(words)
    sentences = []
    i = 0
    while i < len(latin_words) - 3:
        n = random.randint(8, 15)
        sentences.append(latin_words[i:i+n])
        i += n
    return sentences

def cipher_lf_word(latin_word, rng):
    p = 0.90  # strong calibration
    w = latin_word.lower()
    if LATIN_CLAUSE_INITIAL_Y_ANALOG.match(w):
        if rng.random() < p:
            return make_word('y', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0])
    elif LATIN_CLAUSE_INITIAL_T.match(w):
        if rng.random() < p:
            return make_word('t', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0])
    elif LATIN_CLAUSE_INITIAL_S.match(w):
        if rng.random() < p:
            return make_word('s', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0])
    return random_eva_word(rng)

def cipher_ll_word(latin_word, rng):
    p = 0.90  # strong calibration
    w = latin_word.lower()
    if LATIN_CLAUSE_FINAL.search(w):
        if rng.random() < p:
            ll_onsets = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
            onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
            return make_word(onset, 'am')
    return random_eva_word(rng)

def cipher_mid_word(latin_word, rng):
    return random_eva_word(rng)

def generate_cipher_corpus(sentences, rng):
    lines = []
    all_words = [w for sent in sentences for w in sent if re.match(r'[a-zA-Z]', w)]
    rng.shuffle(all_words)
    pos = 0
    while len(lines) < TARGET_LINES and pos < len(all_words) - 2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = all_words[pos:pos+n]
        if len(chunk) < 2:
            pos += len(chunk)
            continue
        eva_line = []
        for i, w in enumerate(chunk):
            if i == 0:
                eva_line.append(cipher_lf_word(w, rng))
            elif i == len(chunk) - 1:
                eva_line.append(cipher_ll_word(w, rng))
            else:
                eva_line.append(cipher_mid_word(w, rng))
        lines.append(eva_line)
        pos += n
    return lines[:TARGET_LINES]

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
    return 'other'

def compute_metrics(lines):
    all_words = [w for line in lines for w in line]
    n = len(all_words)
    onset_counts = Counter(get_onset(w) for w in all_words)
    lf_words = [line[0] for line in lines if line]
    ll_words = [line[-1] for line in lines if len(line) > 1]
    n_lf, n_ll = len(lf_words), len(ll_words)

    def pos_enr(words_at_pos, test_fn, baseline_rate, n_pos):
        if n_pos == 0 or baseline_rate == 0: return 1.0
        return (sum(1 for w in words_at_pos if test_fn(w)) / n_pos) / baseline_rate

    am_ll = pos_enr(ll_words, lambda w: w.endswith('am'),
                    sum(1 for w in all_words if w.endswith('am')) / n, n_ll)
    y_lf  = pos_enr(lf_words, lambda w: get_onset(w) == 'y', onset_counts['y'] / n, n_lf)

    total_bg = len(all_words) - 1
    bg_onset = Counter((get_onset(all_words[i]), get_onset(all_words[i+1])) for i in range(total_bg))
    def ss_enr(onset):
        base = onset_counts[onset] / n
        return bg_onset[(onset, onset)] / (total_bg * base * base) if base > 0 else 1.0
    ss_mean = (ss_enr('qok') + ss_enr('ok') + ss_enr('ch')) / 3

    return {'am_ll': am_ll, 'y_lf': y_lf, 'ss_mean': ss_mean}

# ── Main ──────────────────────────────────────────────────────────────────────
print("Extracting Latin sentences (same corpus as exp_177)...")
random.seed(42)
sentences = extract_latin_sentences(LATIN_CORPUS)
print(f"Extracted {len(sentences)} pseudo-sentences")

print(f"\nRunning {N_SIMS} independent simulations (strong calibration, seed base=999999)...")
sim_metrics = []
for sim_i in range(N_SIMS):
    # Completely different seed base from exp_177 (which used sim_i * 1000)
    rng = random.Random(999999 + sim_i)
    lines = generate_cipher_corpus(sentences, rng)
    m = compute_metrics(lines)
    sim_metrics.append(m)

am_vals = sorted(m['am_ll'] for m in sim_metrics)
y_vals  = sorted(m['y_lf']  for m in sim_metrics)
ss_vals = sorted(m['ss_mean'] for m in sim_metrics)

n = len(am_vals)
am_mean = sum(am_vals) / n
am_lo, am_hi = am_vals[int(n*0.025)], am_vals[int(n*0.975)]
y_mean  = sum(y_vals) / n
y_lo, y_hi = y_vals[int(n*0.025)], y_vals[int(n*0.975)]
ss_mean_v = sum(ss_vals) / n

print(f"\nVERIFICATION RESULTS (independent run, n={n})")
print(f"{'='*60}")
print(f"  -am LL:    {am_mean:.3f}  [95% CI: {am_lo:.3f}, {am_hi:.3f}]")
print(f"  y-LF:      {y_mean:.3f}  [95% CI: {y_lo:.3f}, {y_hi:.3f}]")
print(f"  ss_mean:   {ss_mean_v:.3f}")
print(f"{'='*60}")
print(f"\nexp_177 original (seed base 0): am_ll=5.756 [5.458, 5.996]")
print(f"Difference in am_ll mean:        {am_mean - 5.756:+.3f}")
print(f"\nConclusion: {'REPRODUCIBLE' if abs(am_mean - 5.756) < 0.3 else 'DISCREPANT — INVESTIGATE'}")

with open(os.path.join(OUT_DIR, 'verify_results.json'), 'w') as f:
    json.dump({'am_ll_mean': am_mean, 'am_ll_lo': am_lo, 'am_ll_hi': am_hi,
               'y_lf_mean': y_mean, 'y_lf_lo': y_lo, 'y_lf_hi': y_hi,
               'ss_mean': ss_mean_v, 'n_sims': n,
               'original_am_ll': 5.756, 'delta': am_mean - 5.756}, f, indent=2)
print("Saved to data/verify_results.json")
