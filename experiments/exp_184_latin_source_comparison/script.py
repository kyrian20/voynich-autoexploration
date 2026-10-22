"""
exp_184: Position-Sensitive Cipher — Different Latin Source Comparison

Motivation:
  exp_177 used Cicero's De Officiis as the Latin source, achieving am_ll=5.756× at
  strong calibration (90% clause-final detection). The Opus phase-3 review (item 3)
  identified this as a gap: "Testing pharmaceutical Latin, liturgical Latin, or Italian
  would be informative." The residual gap (5.756× vs VMS 6.811×) may be source-dependent.

  Key question: Does the clause-final morpheme density in the source text affect am_ll?
  If Virgil's Aeneid (poetry, more accusative endings due to meter) or Caesar's Gallic
  Wars (military prose, frequent -um/-is/-us in tactical descriptions) has higher
  clause-final morpheme density, the cipher might produce higher am_ll.

  Also testing: What is the actual clause-final morpheme rate in each source?
  This directly determines how many LL words get mapped to -am.
  At 90% detection with rate R, expected -am LL rate ≈ 0.9×R + 0.1×base_am_rate.

Hypothesis:
  H_a: Virgil Aeneid has higher clause-final rate than Cicero De Officiis (poetic meter
       forces accusative endings at line-ends more consistently than prose).
  H_b: Caesar Gallic Wars has similar or lower clause-final rate than Cicero
       (military prose uses more nominative/ablative constructions).
  H_c: The source-text effect on am_ll is ≤ 0.5× (the cipher table calibration dominates
       over source text morphology at p=0.90).

Methodology:
  Replicates exp_177 (strong calibration, p=0.90) with three sources:
  1. Cicero De Officiis (exp_177 baseline, re-run for comparison with same seed base)
  2. Virgil Aeneid (virgil_aeneid_latin.txt — poetic Latin, hexameter verse)
  3. Caesar Gallic Wars (caesar_de_bello_gallico_latin.txt — military prose)

  Each source: 100 simulations × TARGET_LINES=2447 (matching VMS B-dialect line count).

  Metrics: am_ll, y_lf, ss_mean, adj_rate (identical to exp_177).

  Additional measurement: ACTUAL clause-final morpheme rate in each source text
  (fraction of words ending in -am, -um, -us, -em, -is, -ae, -orum, -bus, -unt, -it, -ant, -at).
  This allows attribution of am_ll differences to source vs calibration effects.

Target-awareness note (inherited from exp_177):
  The LL cipher table is EXPLICITLY calibrated to -am: all Latin clause-final morphemes
  (-am, -um, -us, -em, -is, -ae, -orum, -bus, -unt, -it, -ant, -at) are mapped to EVA -am
  with p=0.90. The am_ll metric is conditional on this calibration.
  The LF table is also target-aware (y-onset mapping for conjunctions/s/t-initial words).
  Results should be interpreted as: 'under maximal target-aware calibration, does source
  text affect am_ll enrichment?'

Seed base: 184000 (Cicero replication), 184100 (Virgil), 184200 (Caesar).
"""
from pathlib import Path as _RepositoryPath

import os, re, random, json
from collections import Counter, deque

REPO_DIR   = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
OUT_DIR    = os.path.join(REPO_DIR, 'experiments/exp_184_latin_source_comparison/data')
os.makedirs(OUT_DIR, exist_ok=True)

SOURCES = {
    'cicero':  os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt'),
    'virgil':  os.path.join(REPO_DIR, 'data/reference_corpora/latin/virgil_aeneid_latin.txt'),
    'caesar':  os.path.join(REPO_DIR, 'data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt'),
}
SEED_BASES = {'cicero': 184000, 'virgil': 184100, 'caesar': 184200}
N_SIMS      = 100
TARGET_LINES = 2447

# ── EVA vocabulary distributions (identical to exp_177) ───────────────────────
ONSET_WEIGHTS = {
    'qok': 0.121, 'qo': 0.034, 'cth': 0.003, 'ch': 0.064, 'sh': 0.090,
    'ok': 0.066, 'd': 0.068, 's': 0.028, 'y': 0.041, 'k': 0.022,
    't': 0.020, 'l': 0.058, 'other': 0.111,
}
SUFFIX_WEIGHTS = {
    'am': 0.020, 'aiin': 0.103, 'edy': 0.183, 'ain': 0.070, 'ey': 0.040,
    'ol': 0.063, 'or': 0.033, 'al': 0.055, 'ar': 0.074, 'dy': 0.030, 'other': 0.329,
}

def make_word(onset, suffix, rng):
    cores = ['a', 'ai', 'o', 'oi', 'e', 'ei']
    return onset + rng.choice(cores) + suffix

def random_eva_word(rng):
    onset  = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
    suffix = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
    return make_word(onset, suffix, rng)

# ── Cipher tables (identical to exp_177 strong calibration) ───────────────────
LATIN_CLAUSE_FINAL     = re.compile(r'(am|um|us|em|is|ae|orum|bus|unt|it|ant|at)$', re.I)
LATIN_CLAUSE_INITIAL_S = re.compile(r'^[Ss][aeiouAEIOU]', re.I)
LATIN_CLAUSE_INITIAL_T = re.compile(r'^[Tt][aeiouAEIOU]', re.I)
LATIN_CLAUSE_INITIAL_Y = re.compile(r'^[Qq][uU]|^[Nn]o|^[Ee]t\b|^[Aa]t\b', re.I)
P_STRONG = 0.90

def cipher_lf(latin_word, rng):
    """LF table: y/s/t-onset mapping (target-aware, p=0.90)."""
    w = latin_word.lower()
    if LATIN_CLAUSE_INITIAL_Y.match(w) and rng.random() < P_STRONG:
        suf = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
        return make_word('y', suf, rng)
    elif LATIN_CLAUSE_INITIAL_T.match(w) and rng.random() < P_STRONG:
        suf = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
        return make_word('t', suf, rng)
    elif LATIN_CLAUSE_INITIAL_S.match(w) and rng.random() < P_STRONG:
        suf = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
        return make_word('s', suf, rng)
    return random_eva_word(rng)

def cipher_ll(latin_word, rng):
    """LL table: clause-final morphemes → -am (target-aware, p=0.90)."""
    w = latin_word.lower()
    if LATIN_CLAUSE_FINAL.search(w) and rng.random() < P_STRONG:
        ll_onsets = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return make_word(onset, 'am', rng)
    return random_eva_word(rng)

def cipher_mid(rng):
    """MID table: uniform random EVA word (no positional calibration)."""
    return random_eva_word(rng)

# ── Latin corpus loader ────────────────────────────────────────────────────────
ENGLISH_SW = {
    'the','and','of','to','a','in','that','is','was','he','it','for','on','are',
    'as','with','his','they','at','be','this','have','from','or','had','by','not',
    'but','what','all','were','we','when','your','can','said','there','use','an',
    'each','which','she','do','how','their','if','will','up','other','about','out',
    'many','then','them','these','so','some','her','would','make','like','him',
    'into','time','has','look','two','more',
}

def extract_latin_words(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    paragraphs = re.split(r'\n\s*\n', text)
    latin_words = []
    clause_final_count = 0
    total_words = 0
    for para in paragraphs:
        words = re.findall(r'\b[a-zA-Z]+\b', para)
        if not words:
            continue
        eng_ratio = sum(1 for w in words if w.lower() in ENGLISH_SW) / len(words)
        if eng_ratio < 0.08:
            latin_words.extend(words)
            clause_final_count += sum(1 for w in words if LATIN_CLAUSE_FINAL.search(w.lower()))
            total_words += len(words)
    clause_final_rate = clause_final_count / total_words if total_words > 0 else 0.0
    return latin_words, clause_final_rate, total_words

def make_sentences(latin_words, rng):
    shuffled = list(latin_words)
    rng.shuffle(shuffled)
    sentences = []
    i = 0
    while i < len(shuffled) - 3:
        n = rng.randint(8, 15)
        sentences.append(shuffled[i:i+n])
        i += n
    return sentences

# ── Corpus generator (position-sensitive cipher only, no copy component) ──────
def generate_cipher_corpus(sentences, rng, target_lines):
    """Apply position-sensitive cipher: LF→LF table, LL→LL table, MID→MID table."""
    all_latin = [w for sent in sentences for w in sent if re.match(r'[a-zA-Z]', w)]
    lines = []
    pos   = 0

    while len(lines) < target_lines and pos < len(all_latin) - 2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = all_latin[pos:pos+n]
        if len(chunk) < 2:
            pos += len(chunk)
            continue

        eva_line = []
        for i, latin_word in enumerate(chunk):
            if i == 0 and len(chunk) > 1:
                eva_word = cipher_lf(latin_word, rng)
            elif i == len(chunk) - 1 or len(chunk) == 1:
                eva_word = cipher_ll(latin_word, rng)
            else:
                eva_word = cipher_mid(rng)
            eva_line.append(eva_word)

        lines.append(eva_line)
        pos += n

    return lines[:target_lines]

# ── Metrics (identical to exp_177/182) ────────────────────────────────────────
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
        if n_pos == 0 or base_rate == 0:
            return 1.0
        return (sum(1 for w in words_at if fn(w)) / n_pos) / base_rate

    am_rate = sum(1 for w in all_words if w.endswith('am')) / n
    am_ll   = pos_enr(ll_words, lambda w: w.endswith('am'), am_rate, n_ll)

    y_rate = onset_counts['y'] / n
    y_lf   = pos_enr(lf_words, lambda w: get_onset(w) == 'y', y_rate, n_lf)

    # Self-succession: average of qok, ok, ch (per exp_182 convention)
    total_bg = len(all_words) - 1
    bg = Counter(
        (get_onset(all_words[i]), get_onset(all_words[i+1]))
        for i in range(total_bg)
    )
    def ss(onset):
        base = onset_counts[onset] / n
        return (bg[(onset, onset)] / (total_bg * base * base)
                if base > 0 and total_bg > 0 else 1.0)
    ss_mean = (ss('qok') + ss('ok') + ss('ch')) / 3

    total_pairs = len(all_words) - 1
    adj_rate = sum(1 for i in range(total_pairs) if all_words[i] == all_words[i+1]) / max(1, total_pairs)

    return {
        'am_ll': round(am_ll, 4),
        'y_lf':  round(y_lf, 4),
        'ss_mean': round(ss_mean, 4),
        'adj_rate': round(adj_rate, 5),
    }

# ── Main run ───────────────────────────────────────────────────────────────────
print("=" * 70)
print("exp_184: Position-Sensitive Cipher — Latin Source Comparison")
print(f"Strong calibration (p={P_STRONG}) | N_SIMS={N_SIMS}")
print(f"VMS targets: am_ll=6.811, y_lf=3.506, ss_mean=1.465, adj_rate=0.009")
print(f"exp_177 baseline: am_ll=5.756, y_lf=2.395, ss_mean≈1.00, adj_rate≈0.003")
print("=" * 70)

all_source_results = {}

for source_name, source_path in SOURCES.items():
    print(f"\n--- SOURCE: {source_name.upper()} ---")
    latin_words, cf_rate, n_latin_words = extract_latin_words(source_path)
    print(f"  {n_latin_words} Latin words extracted, clause-final rate = {cf_rate:.3f}")
    print(f"  Expected LL hit rate ≈ {P_STRONG * cf_rate:.3f} (90% detection × {cf_rate:.3f} CF rate)")

    seed_base = SEED_BASES[source_name]
    sim_results = []

    for sim_i in range(N_SIMS):
        rng = random.Random(seed_base + sim_i)
        sentences = make_sentences(latin_words, rng)
        lines = generate_cipher_corpus(sentences, rng, TARGET_LINES)
        m = compute_metrics(lines)
        if m:
            sim_results.append(m)

    if not sim_results:
        print(f"  No results for {source_name}!")
        continue

    def mean_ci(vals, k):
        v = sorted(x[k] for x in vals)
        m_v = sum(v) / len(v)
        lo  = v[int(0.025 * len(v))]
        hi  = v[int(0.975 * len(v))]
        return m_v, lo, hi

    am_m, am_lo, am_hi    = mean_ci(sim_results, 'am_ll')
    y_m, y_lo, y_hi       = mean_ci(sim_results, 'y_lf')
    ss_m, ss_lo, ss_hi    = mean_ci(sim_results, 'ss_mean')
    adj_m, adj_lo, adj_hi = mean_ci(sim_results, 'adj_rate')

    print(f"  am_ll   = {am_m:.4f} 95%CI [{am_lo:.4f}, {am_hi:.4f}]  (VMS: 6.811, pct: {100*am_m/6.811:.1f}%)")
    print(f"  y_lf    = {y_m:.4f} 95%CI [{y_lo:.4f}, {y_hi:.4f}]  (VMS: 3.506)")
    print(f"  ss_mean = {ss_m:.4f} 95%CI [{ss_lo:.4f}, {ss_hi:.4f}]  (VMS: 1.465)")
    print(f"  adj     = {adj_m:.5f} 95%CI [{adj_lo:.5f}, {adj_hi:.5f}] (VMS: 0.009)")

    all_source_results[source_name] = {
        'clause_final_rate': round(cf_rate, 4),
        'n_latin_words': n_latin_words,
        'expected_ll_hit_rate': round(P_STRONG * cf_rate, 4),
        'am_ll': am_m, 'am_ll_ci': [am_lo, am_hi],
        'y_lf': y_m,   'y_lf_ci': [y_lo, y_hi],
        'ss_mean': ss_m, 'ss_mean_ci': [ss_lo, ss_hi],
        'adj_rate': adj_m, 'adj_rate_ci': [adj_lo, adj_hi],
        'pct_vms_am': round(am_m / 6.811 * 100, 1),
    }

# ── Cross-source comparison ────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("CROSS-SOURCE COMPARISON (strong calibration, p=0.90)")
print(f"{'Source':<10} {'CF_rate':>8} {'am_ll':>8} {'%VMS':>6} {'y_lf':>8} {'ss_mean':>8} {'adj_rate':>9}")
print("-" * 62)
for src, rec in all_source_results.items():
    print(f"{src:<10} {rec['clause_final_rate']:>8.3f} {rec['am_ll']:>8.4f} {rec['pct_vms_am']:>5.1f}%"
          f" {rec['y_lf']:>8.4f} {rec['ss_mean']:>8.4f} {rec['adj_rate']:>9.5f}")
print(f"{'VMS target':<10} {'---':>8} {'6.8110':>8} {'100.0':>5}%"
      f" {'3.5060':>8} {'1.4650':>8} {'0.00900':>9}")
print(f"{'exp_177'::<10} {'---':>8} {'5.7560':>8} {'84.5':>5}%"
      f" {'2.3950':>8} {'1.0000':>8} {'0.00300':>9}")

# Source effect analysis
if len(all_source_results) >= 2:
    print("\nSource effect on am_ll (relative to Cicero baseline):")
    cic_am = all_source_results.get('cicero', {}).get('am_ll', None)
    for src, rec in all_source_results.items():
        if src == 'cicero':
            continue
        delta = rec['am_ll'] - cic_am if cic_am else 0
        print(f"  {src}: {rec['am_ll']:.4f} ({delta:+.4f} vs Cicero)")
    if cic_am:
        print(f"\n  Higher clause-final rate = higher LL hit rate = higher am_ll enrichment")
        print(f"  Δam_ll per Δcf_rate (rough estimate for source effect):")
        for src, rec in all_source_results.items():
            if src == 'cicero':
                continue
            d_cf = rec['clause_final_rate'] - all_source_results['cicero']['clause_final_rate']
            d_am = rec['am_ll'] - cic_am
            if abs(d_cf) > 0.001:
                print(f"    {src}: Δcf={d_cf:+.3f} → Δam_ll={d_am:+.4f} (ratio={d_am/d_cf:.2f}×)")

# Save results
out_path = os.path.join(OUT_DIR, 'source_comparison_results.json')
with open(out_path, 'w') as f:
    json.dump({
        'results': all_source_results,
        'exp_177_baseline': {'am_ll': 5.756, 'y_lf': 2.395, 'ss_mean': 1.00, 'adj_rate': 0.003},
        'vms_targets': {'am_ll': 6.811, 'y_lf': 3.506, 'ss_mean': 1.465, 'adj_rate': 0.009},
        'p_strong': P_STRONG, 'n_sims': N_SIMS,
    }, f, indent=2)
print(f"\nResults saved to {out_path}")
