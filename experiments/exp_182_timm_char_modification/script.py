"""
exp_182: Position-Aware Hybrid — Character-Level Timm Modification

Motivation:
  exp_180 used onset-REPLACING modification (always destroys onset class).
  exp_181 used suffix-REPLACING modification (never destroys onset class, 4/36 viable).
  The Opus meta-review (D3) identified a third variant: the original Timm/Schinner
  algorithm uses single-character replace/insert/delete at a random position in the word.
  This preserves onset class approximately 78% of the time (since the onset region
  occupies ~21% of the mean EVA word length) — intermediate between exp_180 and exp_181.

  The question: does character-level modification in the position-aware hybrid produce
  ss_mean/adj_rate values between exp_180 (0/18) and exp_181 (4/36)? Or does the
  partial onset destruction push it back toward exp_180's territory?

Architecture (identical to exp_180/exp_181 except modification operation):
  LF positions: ALWAYS cipher_lf().  Never copy.
  LL positions: ALWAYS cipher_ll().  Never copy.
  MID positions: With prob COPY_PROB, copy from MID-only buffer.
    → With prob MODIFY_PROB: single-character replace/insert/delete (Timm/Schinner).
    → Otherwise: keep exact copy.
  MID-only buffer: deque of WINDOW=20 MID tokens only.

Modification operation:
  exp_180: replace onset with random onset (onset DESTROYED, ~100% onset class change)
  exp_181: replace suffix with random suffix (onset PRESERVED, ~0% onset class change)
  exp_182: single-char replace/insert/delete (onset preserved ~78% of modifications)
           EVA character pool: {a, c, d, e, h, i, k, l, m, n, o, q, r, s, t, y}

Onset preservation estimate:
  Mean onset length: 1.23 chars (weighted by ONSET_WEIGHTS distribution)
  Mean word length: ~5.7 chars (onset 1.23 + core 1.5 + suffix 3.0)
  P(modification touches onset) ≈ 1.23 / 5.7 ≈ 21.6%
  P(onset preserved) ≈ 78.4% (for replace and delete at non-onset position)
  For insert: onset is always preserved (new char inserted after position 0 of onset
  cannot destroy prefix identity unless inserted AT position 0 of onset).

  Compare: exp_180 ~6-12% onset preservation; exp_181 ~100% onset preservation.
  exp_182 expected ~78% onset preservation → closer to exp_181 but below it.

Pre-registration:
  Expected outcome: Number of viable combinations between 0 (exp_180) and 4 (exp_181).
  Most likely: 1-4 viable. If ss_mean decoupling is nearly as strong as exp_181 (~78%
  onset preservation is enough), expect 2-4 viable. If the partial onset destruction
  substantially suppresses ss_mean, expect 0-1 viable.
  adj_rate behavior: similar to exp_181 (single-char modification almost always changes
  the word, so collision rate ≈ very low, lower than exp_181's ~17% suffix collision).

Grid (same as exp_181):
  COPY_PROB   ∈ {0.2, 0.3, 0.4, 0.5, 0.6, 0.7}
  MODIFY_PROB ∈ {0.3, 0.4, 0.5, 0.6, 0.7, 0.8}
  36 combinations × 50 simulations = 1800 total runs.

Additional metric (identical to exp_181):
  Within-MID-only self-succession (ss_mid).

Viability thresholds (identical to exp_180/exp_181):
  am_ll ≥ 5.0×  AND  ss_mean ∈ [1.2, 1.7]  AND  adj_rate ≤ 0.015

Seed base: 182000 (main); 182999 (verification, 10 sims at best combo).
"""
from pathlib import Path as _RepositoryPath

import os, re, random, json, math
from collections import Counter, deque

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
OUT_DIR      = os.path.join(REPO_DIR, 'experiments/exp_182_timm_char_modification/data')
os.makedirs(OUT_DIR, exist_ok=True)

N_SIMS       = 50
TARGET_LINES = 2447
WINDOW       = 20

# ── EVA vocabulary distributions (identical to exp_177–exp_181) ──────────────
ONSET_WEIGHTS = {
    'qok': 0.121, 'qo': 0.034, 'cth': 0.003, 'ch': 0.064, 'sh': 0.090,
    'ok': 0.066, 'd': 0.068, 's': 0.028, 'y': 0.041, 'k': 0.022,
    't': 0.020, 'l': 0.058, 'other': 0.111,
}
SUFFIX_WEIGHTS = {
    'am': 0.020, 'aiin': 0.103, 'edy': 0.183, 'ain': 0.070, 'ey': 0.040,
    'ol': 0.063, 'or': 0.033, 'al': 0.055, 'ar': 0.074, 'dy': 0.030, 'other': 0.329,
}

# EVA individual character pool — characters that appear in onset/core/suffix
# combinations used by make_word(). Used for Timm single-char replacement.
EVA_CHARS = list('acdehiklmnoqrsty')  # 16 characters

def make_word(onset, suffix, rng):
    cores = ['a', 'ai', 'o', 'oi', 'e', 'ei']
    return onset + rng.choice(cores) + suffix

def random_eva_word(rng):
    onset  = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
    suffix = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
    return make_word(onset, suffix, rng)

def cipher_lf(latin_word, rng, p=0.90):
    """LF cipher table (target-aware — y-onset mapping, inherited from exp_177)."""
    LATIN_CLAUSE_INITIAL_S = re.compile(r'^[Ss][aeiouAEIOU]', re.I)
    LATIN_CLAUSE_INITIAL_T = re.compile(r'^[Tt][aeiouAEIOU]', re.I)
    LATIN_CLAUSE_INITIAL_Y = re.compile(r'^[Qq][uU]|^[Nn]o|^[Ee]t\b|^[Aa]t\b', re.I)
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

LATIN_CLAUSE_FINAL = re.compile(r'(am|um|us|em|is|ae|orum|bus|unt|it|ant|at)$', re.I)

def cipher_ll(latin_word, rng, p=0.90):
    """LL cipher table (target-aware — clause-final morphemes → -am, inherited from exp_177)."""
    w = latin_word.lower()
    if LATIN_CLAUSE_FINAL.search(w) and rng.random() < p:
        ll_onsets = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return make_word(onset, 'am', rng)
    return random_eva_word(rng)

def cipher_mid(rng):
    """MID cipher table: uniform random EVA word."""
    return random_eva_word(rng)

# ── Timm/Schinner single-character modification ───────────────────────────────
def timm_modify(word, rng):
    """Single-character replace/insert/delete at random position (Timm/Schinner).

    Algorithm:
    1. Choose operation uniformly: 'replace', 'insert', or 'delete'.
    2. Choose random position in [0, len(word)-1].
    3. Apply operation:
       - replace: substitute character at pos with random EVA character
       - insert:  insert random EVA character at pos
       - delete:  remove character at pos (no-op if word length ≤ 1)

    Effect on onset preservation:
    - The onset region occupies the first ~1.23 chars of a ~5.7-char word.
    - A modification at position > onset_length preserves the onset string.
    - Estimated onset preservation rate: ~78% (for replace/delete; effectively
      ~100% for insert since inserted character is at random interior position
      but does not remove the onset prefix — UNLESS inserted at position 0).

    Effect on adj_rate:
    - Most modifications produce a different word string → do NOT contribute to adj_rate.
    - Collision (same string as original): rare, depends on character; typically < 3%
      (6.25% chance for replace if new_char == old_char, with 1/16 chars = 6.25%).
      Expected collision rate: ~2% overall (vs ~17% for suffix replacement in exp_181).

    Note on insert-at-position-0: If the random position is 0 and the operation is
    'insert', a new character is prepended. This always changes the onset class
    (the new prefix starts with the inserted character). This edge case affects ~3%
    of insert operations (1/len(word) chance of pos=0, for mean len=5.7 → 17.5% of
    inserts land at pos=0). So inserts damage onset class ~5.8% of the time
    (1/3 ops are inserts × 17.5% land at pos=0 = 5.8% of all Timm mods).

    Overall onset destruction rate:
    - Replace: (1.23/5.7) × (1/3) ≈ 7.2% of all mods
    - Delete:  (1.23/5.7) × (1/3) ≈ 7.2% of all mods
    - Insert at pos=0: ~5.8% of all mods (as above)
    Total: ~20.2% of all Timm modifications destroy onset class.
    → ~79.8% of Timm modifications preserve onset class.
    """
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
            return word  # can't delete from single-char word; return unchanged
        return word[:pos] + word[pos+1:]

# ── Latin corpus loader (identical to exp_177–exp_181) ───────────────────────
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

# ── Position-aware corpus generator (MID uses Timm character-level modification)
def generate_position_aware_corpus(sentences, rng, copy_prob, modify_prob):
    """
    LF: always cipher_lf().  Never copy.  Not added to MID buffer.
    LL: always cipher_ll().  Never copy.  Not added to MID buffer.
    MID: copy from MID-only buffer with prob copy_prob.
         Modification: single-char replace/insert/delete (Timm) — onset preserved ~79%.
         If no copy: cipher_mid().
         MID tokens added to MID buffer after generation.
    """
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
            is_lf   = (i == 0)
            is_ll   = (i == len(chunk) - 1)
            is_only = (len(chunk) == 1)
            is_mid  = (not is_lf and not is_ll)

            if is_lf and not is_only:
                eva_word = cipher_lf(latin_word, rng)

            elif is_ll or is_only:
                eva_word = cipher_ll(latin_word, rng)

            else:
                assert is_mid
                if mid_buffer and rng.random() < copy_prob:
                    copied = rng.choice(list(mid_buffer))
                    if rng.random() < modify_prob:
                        # KEY DIFFERENCE: Timm single-char replace/insert/delete
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

    # am_ll enrichment
    am_rate = sum(1 for w in all_words if w.endswith('am')) / n
    am_ll   = pos_enr(ll_words, lambda w: w.endswith('am'), am_rate, n_ll)

    # y-onset LF enrichment
    y_rate = onset_counts['y'] / n
    y_lf   = pos_enr(lf_words, lambda w: get_onset(w) == 'y', y_rate, n_lf)

    # Full-corpus self-succession
    total_bg = len(all_words) - 1
    bg = Counter(
        (get_onset(all_words[i]), get_onset(all_words[i+1]))
        for i in range(total_bg)
    )
    def ss(onset):
        base = onset_counts[onset] / n
        return bg[(onset, onset)] / (total_bg * base * base) if base > 0 and total_bg > 0 else 1.0

    ss_mean = (ss('qok') + ss('ok') + ss('ch')) / 3
    ss_detail = {onset: ss(onset) for onset in ['qok', 'ok', 'ch', 'sh', 'd', 'y']}

    # Within-MID-only self-succession (Opus D4)
    mid_bg          = Counter()
    mid_onset_cnt   = Counter()
    for line in lines:
        if len(line) < 3:
            continue
        mid_words = line[1:-1]
        for w in mid_words:
            mid_onset_cnt[get_onset(w)] += 1
        for j in range(len(mid_words) - 1):
            o1 = get_onset(mid_words[j])
            o2 = get_onset(mid_words[j+1])
            mid_bg[(o1, o2)] += 1

    n_mid    = sum(mid_onset_cnt.values())
    n_mid_bg = sum(mid_bg.values())

    def ss_mid_only(onset):
        base = mid_onset_cnt[onset] / n_mid if n_mid > 0 else 0
        return (mid_bg[(onset, onset)] / (n_mid_bg * base * base)
                if base > 0 and n_mid_bg > 0 else 1.0)

    ss_mean_mid = (ss_mid_only('qok') + ss_mid_only('ok') + ss_mid_only('ch')) / 3
    ss_detail_mid = {o: ss_mid_only(o) for o in ['qok', 'ok', 'ch', 'sh', 'd', 'y']}

    # Identical adjacent word rate
    adj_same = sum(1 for i in range(total_bg) if all_words[i] == all_words[i+1])
    adj_rate = adj_same / total_bg if total_bg > 0 else 0

    return {
        'am_ll': am_ll, 'y_lf': y_lf,
        'ss_mean': ss_mean, 'ss_detail': ss_detail,
        'ss_mean_mid': ss_mean_mid, 'ss_detail_mid': ss_detail_mid,
        'adj_rate': adj_rate,
    }

# ── Latin corpus setup ────────────────────────────────────────────────────────
print("Extracting Latin sentences...")
random.seed(42)
sentences = extract_latin_sentences(LATIN_CORPUS)
print(f"Extracted {len(sentences)} pseudo-sentences ({sum(len(s) for s in sentences)} words)")

# ── Parameter grid ────────────────────────────────────────────────────────────
COPY_PROBS   = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
MODIFY_PROBS = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

VMS = {'am_ll': 6.811, 'y_lf': 3.506, 'ss_mean': 1.465, 'adj_rate': 0.009}
VIABLE_AM_LL   = 5.0
VIABLE_SS_LO   = 1.2
VIABLE_SS_HI   = 1.7
VIABLE_ADJ_MAX = 0.015

total_combos = len(COPY_PROBS) * len(MODIFY_PROBS)
print(f"\nRunning main sweep ({total_combos} combos × {N_SIMS} sims = {total_combos*N_SIMS} runs). "
      f"Seed base: 182000")

SEED_BASE   = 182000
all_results = {}
combo_count = 0

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
            return s[max(0, int(n*0.025))], s[min(n-1, int(n*0.975))]

        scalar_keys = ['am_ll', 'y_lf', 'ss_mean', 'ss_mean_mid', 'adj_rate']
        avg = {k: sum(s[k] for s in sim_metrics) / len(sim_metrics) for k in scalar_keys}
        cis = {k: ci95([s[k] for s in sim_metrics]) for k in scalar_keys}

        ss_detail_mean = {}
        ss_detail_mid_mean = {}
        for onset in ['qok', 'ok', 'ch', 'sh', 'd', 'y']:
            ss_detail_mean[onset]     = sum(s['ss_detail'][onset]     for s in sim_metrics) / len(sim_metrics)
            ss_detail_mid_mean[onset] = sum(s['ss_detail_mid'][onset] for s in sim_metrics) / len(sim_metrics)

        viable = (avg['am_ll'] >= VIABLE_AM_LL and
                  VIABLE_SS_LO <= avg['ss_mean'] <= VIABLE_SS_HI and
                  avg['adj_rate'] <= VIABLE_ADJ_MAX)

        all_results[key] = {
            'copy_prob': cp, 'modify_prob': mp,
            'avg': avg,
            'ci': {k: list(v) for k, v in cis.items()},
            'ss_detail_mean': ss_detail_mean,
            'ss_detail_mid_mean': ss_detail_mid_mean,
            'n': len(sim_metrics),
            'viable': viable,
        }
        flag = '*** VIABLE ***' if viable else ''
        print(f"am_ll={avg['am_ll']:.3f} y_lf={avg['y_lf']:.3f} "
              f"ss={avg['ss_mean']:.3f} ss_mid={avg['ss_mean_mid']:.3f} "
              f"adj={avg['adj_rate']:.4f} {flag}")

# ── Verification run ──────────────────────────────────────────────────────────
def joint_score(r):
    return r['avg']['am_ll'] * r['avg']['ss_mean']

best_key = max(all_results, key=lambda k: joint_score(all_results[k]))
best_r   = all_results[best_key]
best_cp, best_mp = best_r['copy_prob'], best_r['modify_prob']

print(f"\n{'='*80}")
print(f"VERIFICATION RUN: best combination = {best_key}")
print(f"  Main run: am_ll={best_r['avg']['am_ll']:.4f}, ss_mean={best_r['avg']['ss_mean']:.4f}, "
      f"adj={best_r['avg']['adj_rate']:.4f}")
print(f"  Running 10 sims with seed base 182999...")

VERIFY_SEED_BASE = 182999
N_VERIFY = 10
verify_metrics = []
for sim_i in range(N_VERIFY):
    rng   = random.Random(VERIFY_SEED_BASE + sim_i)
    lines = generate_position_aware_corpus(sentences, rng, best_cp, best_mp)
    m     = compute_metrics(lines)
    if m:
        verify_metrics.append(m)

verify_am = sum(m['am_ll']    for m in verify_metrics) / len(verify_metrics)
verify_ss = sum(m['ss_mean']  for m in verify_metrics) / len(verify_metrics)
verify_aj = sum(m['adj_rate'] for m in verify_metrics) / len(verify_metrics)
d_am = verify_am - best_r['avg']['am_ll']
d_ss = verify_ss - best_r['avg']['ss_mean']
print(f"  Verify: am_ll={verify_am:.4f} (Δ={d_am:+.4f}), "
      f"ss_mean={verify_ss:.4f} (Δ={d_ss:+.4f}), adj={verify_aj:.4f}")

all_results['_verification'] = {
    'best_key': best_key, 'best_cp': best_cp, 'best_mp': best_mp,
    'main_am_ll': best_r['avg']['am_ll'], 'main_ss_mean': best_r['avg']['ss_mean'],
    'main_adj_rate': best_r['avg']['adj_rate'],
    'verify_am_ll': verify_am, 'verify_ss_mean': verify_ss, 'verify_adj_rate': verify_aj,
    'delta_am_ll': d_am, 'delta_ss_mean': d_ss,
    'n_verify': len(verify_metrics), 'seed_base': VERIFY_SEED_BASE,
}

# ── Save ──────────────────────────────────────────────────────────────────────
with open(os.path.join(OUT_DIR, 'timm_char_results.json'), 'w') as f:
    json.dump(all_results, f, indent=2)

# ── Report ────────────────────────────────────────────────────────────────────
print(f"\n{'='*80}")
print("EXP_182: CHARACTER-LEVEL TIMM MODIFICATION — RESULTS SUMMARY")
print(f"{'='*80}")
print(f"VMS targets: am_ll={VMS['am_ll']}, y_lf={VMS['y_lf']}, "
      f"ss_mean={VMS['ss_mean']:.3f}, adj_rate={VMS['adj_rate']}")
print(f"Viability: am_ll≥{VIABLE_AM_LL}, ss∈[{VIABLE_SS_LO},{VIABLE_SS_HI}], adj≤{VIABLE_ADJ_MAX}")

print(f"\n{'cp':>5} {'mp':>5} {'am_ll':>8} {'y_lf':>7} {'ss_full':>9} {'ss_mid':>8} {'adj':>9} {'viable':>8}")
print("-" * 68)
for key, r in sorted(all_results.items(),
                     key=lambda kv: (kv[1].get('copy_prob', 99), kv[1].get('modify_prob', 99))):
    if key == '_verification': continue
    v = r['avg']
    mark = ' ***' if r['viable'] else ''
    print(f"{r['copy_prob']:>5.1f} {r['modify_prob']:>5.1f} "
          f"{v['am_ll']:>8.3f} {v['y_lf']:>7.3f} {v['ss_mean']:>9.3f} "
          f"{v['ss_mean_mid']:>8.3f} {v['adj_rate']:>9.4f}{mark}")

viable_list = [(k, r) for k, r in all_results.items()
               if k != '_verification' and r.get('viable')]
print(f"\nViable combinations: {len(viable_list)}/{total_combos}")
if viable_list:
    print("Viable:")
    for k, r in sorted(viable_list, key=lambda kr: -joint_score(kr[1])):
        v, ci = r['avg'], r['ci']
        print(f"  {k}: am_ll={v['am_ll']:.3f}[{ci['am_ll'][0]:.3f},{ci['am_ll'][1]:.3f}], "
              f"ss={v['ss_mean']:.3f}[{ci['ss_mean'][0]:.3f},{ci['ss_mean'][1]:.3f}], "
              f"adj={v['adj_rate']:.4f}[{ci['adj_rate'][0]:.4f},{ci['adj_rate'][1]:.4f}]")

# Three-way comparison: exp_180 vs exp_182 vs exp_181
print(f"\n--- Three-way comparison: exp_180 (onset-replace) vs exp_182 (Timm) vs exp_181 (suffix-replace) ---")
EXP_180_MATCHED = {
    (0.3, 0.5): {'ss_mean': 1.045, 'adj_rate': 0.0092},
    (0.5, 0.5): {'ss_mean': 1.094, 'adj_rate': 0.0156},
    (0.6, 0.5): {'ss_mean': 1.108, 'adj_rate': 0.0198},
    (0.7, 0.5): {'ss_mean': 1.148, 'adj_rate': 0.0248},
}
EXP_181_MATCHED = {
    (0.3, 0.5): {'ss_mean': 1.114, 'adj_rate': 0.0097},
    (0.5, 0.5): {'ss_mean': 1.264, 'adj_rate': 0.0171},
    (0.6, 0.5): {'ss_mean': 1.401, 'adj_rate': 0.0220},
    (0.7, 0.5): {'ss_mean': 1.574, 'adj_rate': 0.0283},
}
print(f"{'cp':>5} {'mp':>5} "
      f"{'E180_ss':>9} {'E182_ss':>9} {'E181_ss':>9}  "
      f"{'E180_adj':>10} {'E182_adj':>10} {'E181_adj':>10}")
for (cp_val, mp_val) in [(0.3, 0.5), (0.5, 0.5), (0.6, 0.5), (0.7, 0.5)]:
    k182 = f"cp={cp_val},mp={mp_val}"
    if (cp_val, mp_val) in EXP_180_MATCHED and k182 in all_results:
        e80 = EXP_180_MATCHED[(cp_val, mp_val)]
        e82v = all_results[k182]['avg']
        e81 = EXP_181_MATCHED[(cp_val, mp_val)]
        print(f"{cp_val:>5.1f} {mp_val:>5.1f} "
              f"{e80['ss_mean']:>9.3f} {e82v['ss_mean']:>9.3f} {e81['ss_mean']:>9.3f}  "
              f"{e80['adj_rate']:>10.4f} {e82v['adj_rate']:>10.4f} {e81['adj_rate']:>10.4f}")

# Estimate onset preservation fraction from ss_mean ordering
print(f"\n--- Interpolation position of exp_182 between exp_180 and exp_181 ---")
print(f"  For each (cp, mp=0.5), compute fraction f = (ss_182 - ss_180) / (ss_181 - ss_180)")
print(f"  f=0 → identical to onset-replacing; f=1 → identical to suffix-replacing")
print(f"{'cp':>5} {'mp':>5} {'ss_180':>9} {'ss_182':>9} {'ss_181':>9} {'f':>8}")
for (cp_val, mp_val) in [(0.3, 0.5), (0.5, 0.5), (0.6, 0.5), (0.7, 0.5)]:
    k182 = f"cp={cp_val},mp={mp_val}"
    if (cp_val, mp_val) in EXP_180_MATCHED and k182 in all_results:
        s80 = EXP_180_MATCHED[(cp_val, mp_val)]['ss_mean']
        s82 = all_results[k182]['avg']['ss_mean']
        s81 = EXP_181_MATCHED[(cp_val, mp_val)]['ss_mean']
        if s81 - s80 > 0:
            f = (s82 - s80) / (s81 - s80)
            print(f"{cp_val:>5.1f} {mp_val:>5.1f} {s80:>9.3f} {s82:>9.3f} {s81:>9.3f} {f:>8.3f}")

print(f"\nDone. Results saved to data/timm_char_results.json")
