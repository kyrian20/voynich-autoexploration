"""
exp_183: Extended MODIFY_PROB Grid — Timm Char Modification in Position-Aware Hybrid

Motivation:
  exp_182 tested MODIFY_PROB ∈ {0.3, 0.4, 0.5, 0.6, 0.7, 0.8} × COPY_PROB ∈ {0.2-0.7}.
  The three VMS-adj_rate-viable combinations (adj_rate ≤ 0.009) were all at MODIFY_PROB ≥ 0.7.
  The trend shows adj_rate decreasing ~0.032 per unit mp increase at cp=0.7; ss_mean
  decreasing ~0.028 per unit mp increase.

  Two open questions from exp_182:
  1. What happens at MODIFY_PROB ∈ {0.9, 1.0} (extreme modification)?
     - At mp=1.0: ALL copies are modified (no exact copies). adj_rate → near-0. What is ss_mean floor?
     - At mp=0.9: very few unmodified copies. adj_rate well below VMS. Does ss_mean stay ≥ 1.2?
  2. What happens at COPY_PROB=0.8 (untested in exp_182)?
     - Higher copying raises ss_mean potential but also adj_rate; high mp might compensate.
     - cp=0.8, mp=0.9 may offer the best ss_mean at VMS-level adj_rate.

Hypothesis:
  (a) At cp=0.7, mp=0.9: ss_mean ≈ 1.33 (extrapolating: 1.368 - 0.028 × 1 step), adj_rate ≈ 0.004.
      Still above ss_mean floor (1.2), still at VMS-level adj_rate. Viable.
  (b) At cp=0.7, mp=1.0: ss_mean ≈ 1.30, adj_rate ≈ 0.001. Still viable.
      The ss_mean floor from pure modification (no exact copies) reveals the onset-preservation
      contribution of Timm modification alone. At mp=1.0, all ss_mean comes from the ~79%
      onset-preserving modifications that produce same onset-class copies.
  (c) At cp=0.8: higher ss_mean at same mp, but also higher adj_rate. With mp=0.9, adj_rate
      should return to ~0.005-0.008 range (VMS-level), while ss_mean exceeds cp=0.7.
  (d) The combination (cp=0.8, mp=0.8) may produce ss_mean > 1.368 (exp_182 best) at adj_rate ≤ 0.009.

Pre-registration:
  Expected viable count (lenient threshold adj_rate ≤ 0.015): 4-8 of 20 combinations.
  Expected VMS-adj_rate viable (adj_rate ≤ 0.009): 4-8 of 20 combinations.
  Expected ss_mean at mp=1.0: ≈ 1.2-1.25 (floor from onset preservation alone).
  Expected: cp=0.8 provides highest ss_mean, cp=0.5 provides lowest adj_rate.

Architecture: identical to exp_182 (MID-only buffer, Timm char modification).

Grid:
  COPY_PROB   ∈ {0.5, 0.6, 0.7, 0.8}          (4 values; focus on the productive range)
  MODIFY_PROB ∈ {0.7, 0.8, 0.9, 1.0}           (4 values; extends exp_182 to 0.9/1.0)
  Note: (0.5, 0.7), (0.6, 0.7), (0.6, 0.8), (0.7, 0.7), (0.7, 0.8) were already in exp_182
  but are REPEATED here for consistency (independent seeds) to verify replication.
  16 combinations × 50 simulations = 800 total runs.

VMS targets: am_ll=6.811, y_lf=3.506, ss_mean=1.465, adj_rate=0.009.
Viability thresholds: am_ll ≥ 5.0 AND ss_mean ∈ [1.2, 1.7] AND adj_rate ≤ 0.015.
VMS-level adj_rate threshold: ≤ 0.009.

Seed base: 183000.
"""

import os, re, random, json
from collections import Counter, deque

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
OUT_DIR      = os.path.join(REPO_DIR, 'experiments/exp_183_timm_char_extended_grid/data')
os.makedirs(OUT_DIR, exist_ok=True)

N_SIMS       = 50
TARGET_LINES = 2447
WINDOW       = 20

# ── EVA vocabulary distributions (identical to exp_177–182) ──────────────────
ONSET_WEIGHTS = {
    'qok': 0.121, 'qo': 0.034, 'cth': 0.003, 'ch': 0.064, 'sh': 0.090,
    'ok': 0.066, 'd': 0.068, 's': 0.028, 'y': 0.041, 'k': 0.022,
    't': 0.020, 'l': 0.058, 'other': 0.111,
}
SUFFIX_WEIGHTS = {
    'am': 0.020, 'aiin': 0.103, 'edy': 0.183, 'ain': 0.070, 'ey': 0.040,
    'ol': 0.063, 'or': 0.033, 'al': 0.055, 'ar': 0.074, 'dy': 0.030, 'other': 0.329,
}
EVA_CHARS = list('acdehiklmnoqrsty')  # 16 characters

def make_word(onset, suffix, rng):
    cores = ['a', 'ai', 'o', 'oi', 'e', 'ei']
    return onset + rng.choice(cores) + suffix

def random_eva_word(rng):
    onset  = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
    suffix = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
    return make_word(onset, suffix, rng)

# ── Cipher tables (identical to exp_177–182) ──────────────────────────────────
LATIN_CLAUSE_INITIAL_S = re.compile(r'^[Ss][aeiouAEIOU]', re.I)
LATIN_CLAUSE_INITIAL_T = re.compile(r'^[Tt][aeiouAEIOU]', re.I)
LATIN_CLAUSE_INITIAL_Y = re.compile(r'^[Qq][uU]|^[Nn]o|^[Ee]t\b|^[Aa]t\b', re.I)
LATIN_CLAUSE_FINAL     = re.compile(r'(am|um|us|em|is|ae|orum|bus|unt|it|ant|at)$', re.I)

def cipher_lf(latin_word, rng, p=0.90):
    """LF cipher table — target-aware (y-onset mapping from exp_177)."""
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
    """LL cipher table — target-aware (clause-final → -am from exp_177)."""
    w = latin_word.lower()
    if LATIN_CLAUSE_FINAL.search(w) and rng.random() < p:
        ll_onsets = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return make_word(onset, 'am', rng)
    return random_eva_word(rng)

def cipher_mid(rng):
    return random_eva_word(rng)

# ── Timm/Schinner single-character modification (identical to exp_182) ────────
def timm_modify(word, rng):
    """Single-char replace/insert/delete at random position."""
    if not word or len(word) < 1:
        return word
    op  = rng.choice(['replace', 'insert', 'delete'])
    pos = rng.randint(0, max(0, len(word) - 1))
    if op == 'replace':
        new_char = rng.choice(EVA_CHARS)
        return word[:pos] + new_char + word[pos+1:]
    elif op == 'insert':
        new_char = rng.choice(EVA_CHARS)
        return word[:pos] + new_char + word[pos:]
    else:  # delete
        if len(word) <= 1:
            return word
        return word[:pos] + word[pos+1:]

# ── Latin corpus loader (identical to exp_177–182) ────────────────────────────
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

# ── Position-aware corpus generator (MID: Timm char modification) ─────────────
def generate_position_aware_corpus(sentences, rng, copy_prob, modify_prob):
    all_latin = [w for sent in sentences for w in sent if re.match(r'[a-zA-Z]', w)]
    rng.shuffle(all_latin)

    lines      = []
    mid_buffer = deque(maxlen=WINDOW)
    pos        = 0

    while len(lines) < TARGET_LINES and pos < len(all_latin) - 2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = all_latin[pos:pos+n]
        if len(chunk) < 2:
            pos += len(chunk)
            continue

        eva_line = []
        for i, latin_word in enumerate(chunk):
            is_lf  = (i == 0)
            is_ll  = (i == len(chunk) - 1)
            is_mid = (not is_lf and not is_ll)

            if is_lf and len(chunk) > 1:
                eva_word = cipher_lf(latin_word, rng)
            elif is_ll or len(chunk) == 1:
                eva_word = cipher_ll(latin_word, rng)
            else:
                assert is_mid
                if mid_buffer and rng.random() < copy_prob:
                    copied = rng.choice(list(mid_buffer))
                    if rng.random() < modify_prob:
                        eva_word = timm_modify(copied, rng)
                    else:
                        eva_word = copied
                else:
                    eva_word = cipher_mid(rng)
                mid_buffer.append(eva_word)

            eva_line.append(eva_word)

        lines.append(eva_line)
        pos += n

    return lines[:TARGET_LINES]

# ── Metrics (identical to exp_182) ────────────────────────────────────────────
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

    lf_words = [line[0]  for line in lines if line]
    ll_words = [line[-1] for line in lines if len(line) > 1]
    n_lf, n_ll = len(lf_words), len(ll_words)

    def pos_enr(words_at, fn, base_rate, n_pos):
        if n_pos == 0 or base_rate == 0:
            return 1.0
        return (sum(1 for w in words_at if fn(w)) / n_pos) / base_rate

    # am_ll enrichment
    am_rate = sum(1 for w in all_words if w.endswith('am')) / n
    am_ll   = pos_enr(ll_words, lambda w: w.endswith('am'), am_rate, n_ll)

    # y-onset LF enrichment
    y_rate = sum(1 for w in all_words if get_onset(w) == 'y') / n
    y_lf   = pos_enr(lf_words, lambda w: get_onset(w) == 'y', y_rate, n_lf)

    # Full-corpus self-succession — MUST match exp_182 computation:
    #   ss(onset) = P(onset_A, onset_B both == onset) / P(onset)^2
    #             = bg[(onset,onset)] / (total_bg * base^2)
    #   ss_mean   = average of qok, ok, ch ONLY (the three classes in VMS committed claims)
    onset_counts = Counter(get_onset(w) for w in all_words)
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

    # Within-MID-only self-succession (identical to exp_182)
    mid_bg        = Counter()
    mid_onset_cnt = Counter()
    for line in lines:
        if len(line) < 3:
            continue
        mid_words = line[1:-1]
        for w in mid_words:
            mid_onset_cnt[get_onset(w)] += 1
        for j in range(len(mid_words) - 1):
            mid_bg[(get_onset(mid_words[j]), get_onset(mid_words[j+1]))] += 1
    n_mid    = sum(mid_onset_cnt.values())
    n_mid_bg = sum(mid_bg.values())
    def ss_mid_only(onset):
        base = mid_onset_cnt[onset] / n_mid if n_mid > 0 else 0
        return (mid_bg[(onset, onset)] / (n_mid_bg * base * base)
                if base > 0 and n_mid_bg > 0 else 1.0)
    ss_mid = (ss_mid_only('qok') + ss_mid_only('ok') + ss_mid_only('ch')) / 3

    # Identical adjacent word rate
    pairs = [(all_words[i], all_words[i+1]) for i in range(len(all_words)-1)]
    adj_rate = sum(1 for a, b in pairs if a == b) / max(1, len(pairs))

    return {
        'am_ll': round(am_ll, 4),
        'y_lf':  round(y_lf, 4),
        'ss_mean': round(ss_mean, 4),
        'ss_mid':  round(ss_mid, 4),
        'adj_rate': round(adj_rate, 5),
    }

# ── Parameter grid ─────────────────────────────────────────────────────────────
COPY_PROBS   = [0.5, 0.6, 0.7, 0.8]
MODIFY_PROBS = [0.7, 0.8, 0.9, 1.0]

# VMS targets and viability thresholds
VMS = {'am_ll': 6.811, 'y_lf': 3.506, 'ss_mean': 1.465, 'adj_rate': 0.009}
LENIENT_THRESH = {'am_ll_min': 5.0, 'ss_min': 1.2, 'ss_max': 1.7, 'adj_max': 0.015}

# ── Main run ───────────────────────────────────────────────────────────────────
print("Loading Latin corpus...")
sentences = extract_latin_sentences(LATIN_CORPUS)
print(f"  {len(sentences)} pseudo-sentences loaded from Cicero De Officiis")

all_results = []
seed_base = 183000

combos = [(cp, mp) for cp in COPY_PROBS for mp in MODIFY_PROBS]
print(f"\nRunning {len(combos)} combinations × {N_SIMS} sims = {len(combos)*N_SIMS} total runs")
print(f"VMS targets: am_ll={VMS['am_ll']}, ss_mean={VMS['ss_mean']}, adj_rate={VMS['adj_rate']}")
print(f"Lenient thresholds: am_ll≥{LENIENT_THRESH['am_ll_min']}, ss∈[{LENIENT_THRESH['ss_min']},{LENIENT_THRESH['ss_max']}], adj≤{LENIENT_THRESH['adj_max']}")
print()

for cp, mp in combos:
    sim_results = []
    for sim_i in range(N_SIMS):
        seed = seed_base + int(cp * 1000) + int(mp * 100) + sim_i
        rng = random.Random(seed)
        lines = generate_position_aware_corpus(sentences, rng, cp, mp)
        m = compute_metrics(lines)
        if m:
            sim_results.append(m)

    if not sim_results:
        continue

    # Aggregate
    def mean_ci(vals, k):
        v = sorted(x[k] for x in vals)
        m_v = sum(v) / len(v)
        lo  = v[int(0.05 * len(v))]
        hi  = v[int(0.95 * len(v))]
        return m_v, lo, hi

    am_m, am_lo, am_hi     = mean_ci(sim_results, 'am_ll')
    y_m, y_lo, y_hi        = mean_ci(sim_results, 'y_lf')
    ss_m, ss_lo, ss_hi     = mean_ci(sim_results, 'ss_mean')
    ss_mid_m, _, _         = mean_ci(sim_results, 'ss_mid')
    adj_m, adj_lo, adj_hi  = mean_ci(sim_results, 'adj_rate')

    viable = (am_m >= LENIENT_THRESH['am_ll_min'] and
              LENIENT_THRESH['ss_min'] <= ss_m <= LENIENT_THRESH['ss_max'] and
              adj_m <= LENIENT_THRESH['adj_max'])
    vms_adj = adj_m <= VMS['adj_rate']
    vms_viable = (am_m >= LENIENT_THRESH['am_ll_min'] and
                  ss_m >= LENIENT_THRESH['ss_min'] and
                  vms_adj)

    rec = {
        'cp': cp, 'mp': mp,
        'am_ll': am_m, 'am_ll_ci': [am_lo, am_hi],
        'y_lf': y_m, 'y_lf_ci': [y_lo, y_hi],
        'ss_mean': ss_m, 'ss_mean_ci': [ss_lo, ss_hi],
        'ss_mid': ss_mid_m,
        'adj_rate': adj_m, 'adj_rate_ci': [adj_lo, adj_hi],
        'viable_lenient': viable,
        'vms_adj_rate': vms_adj,
        'vms_viable': vms_viable,
        'pct_vms_am': round(am_m / VMS['am_ll'] * 100, 1),
        'pct_vms_ss': round(ss_m / VMS['ss_mean'] * 100, 1),
    }
    all_results.append(rec)

    flag = ""
    if vms_viable:    flag = " ← VMS-VIABLE (adj ≤ VMS)"
    elif viable:      flag = " ← viable (lenient)"
    elif vms_adj:     flag = " (adj ≤ VMS but ss<1.2)"

    print(f"cp={cp:.1f} mp={mp:.1f}: am_ll={am_m:.3f} y_lf={y_m:.3f} "
          f"ss={ss_m:.3f} ss_mid={ss_mid_m:.3f} adj={adj_m:.5f}{flag}")

# ── Summary ────────────────────────────────────────────────────────────────────
lenient_viable = [r for r in all_results if r['viable_lenient']]
vms_viable_all = [r for r in all_results if r['vms_viable']]

print(f"\n{'='*70}")
print(f"SUMMARY: {len(lenient_viable)}/{len(all_results)} lenient viable | "
      f"{len(vms_viable_all)}/{len(all_results)} VMS-adj_rate viable (ss≥1.2, am≥5, adj≤0.009)")
print()

if vms_viable_all:
    print("VMS-adj_rate viable combinations (adj ≤ 0.009, ss ≥ 1.2, am_ll ≥ 5.0):")
    for r in sorted(vms_viable_all, key=lambda x: -x['ss_mean']):
        print(f"  cp={r['cp']:.1f} mp={r['mp']:.1f}: am_ll={r['am_ll']:.3f} "
              f"({r['pct_vms_am']:.1f}% VMS), ss_mean={r['ss_mean']:.3f} "
              f"({r['pct_vms_ss']:.1f}% VMS), adj={r['adj_rate']:.5f}")

if lenient_viable:
    print("\nBest lenient-viable by ss_mean:")
    best = max(lenient_viable, key=lambda x: x['ss_mean'])
    print(f"  cp={best['cp']:.1f} mp={best['mp']:.1f}: am_ll={best['am_ll']:.3f}, "
          f"ss_mean={best['ss_mean']:.3f} ({best['pct_vms_ss']:.1f}% VMS), adj={best['adj_rate']:.5f}")

# mp=1.0 row (pure modification floor)
mp1_rows = [r for r in all_results if r['mp'] == 1.0]
if mp1_rows:
    print("\nmp=1.0 (pure modification — adj_rate floor):")
    for r in sorted(mp1_rows, key=lambda x: x['cp']):
        print(f"  cp={r['cp']:.1f}: ss_mean={r['ss_mean']:.3f}, adj={r['adj_rate']:.5f}")

# Save results
out_path = os.path.join(OUT_DIR, 'extended_grid_results.json')
with open(out_path, 'w') as f:
    json.dump({'results': all_results, 'vms_targets': VMS, 'lenient_thresh': LENIENT_THRESH,
               'n_sims': N_SIMS, 'window': WINDOW, 'source': 'cicero_de_officiis'}, f, indent=2)
print(f"\nResults saved to {out_path}")
