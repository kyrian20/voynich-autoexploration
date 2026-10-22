"""
exp_209: H382 — Non-Morphological LL Mapping
Test whether mapping ALL LL words to -am with probability p_blind (regardless of morphology)
can close the 3% am_ll gap and whether it preserves or destroys d_ll enrichment.

Architecture: same as exp_186 (cp=0.76, mp=0.9) except:
- cipher_ll_blind: ignores Latin CF morphology; maps LL word to -am with prob p_blind
- Also test cipher_ll_blind_random_onset: same but uses random_eva_word onset instead of LL_ONSETS

Two variant rows per p_blind:
  (A) "ll_onset": am-words get onset from LL_ONSETS (d=0.40, ok=0.15, qok=0.15, ch=0.10)
  (B) "random_onset": am-words get onset from ONSET_WEIGHTS (same as random_eva_word)

Target: am_ll ≈ VMS 6.811× — need p_blind ≈ 0.63 (computed analytically)
Key diagnostic: does d_ll stay near VMS (1.5×) or does it explode?

Pre-registration:
  Variant A (ll_onset): am_ll approaches VMS at p_blind≈0.63 BUT d_ll over-enriched
    (d at LL from am-words = p_blind × 0.40; at p_blind=0.63 → d_ll ≈ 3-4× >> VMS 1.5×)
  Variant B (random_onset): am_ll approaches VMS at same p_blind BUT d_ll under-enriched
    (d at LL = onset_base_rate regardless → d_ll ≈ 1.0×)
  If neither variant reproduces both am_ll ≈ VMS AND d_ll ≈ VMS: the morphological gap is
    informative — the VMS mechanism cannot be a pure position-only rule without onset constraints.

Unfairness check from H382: if the random_onset variant breaks d_ll but a hybrid onset assignment
  (intermediate between ll_onset and random_onset) could reproduce both metrics, then the
  negative result would be implementation-specific. So test both extremes and note if a
  feasible intermediate onset assignment could reconcile both metrics.

Seed base: 209000. N_SIMS=30 per combination (fast — key metric is am_ll and d_ll).
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')

N_SIMS       = 30
TARGET_LINES = 2447
WINDOW       = 20
CP, MP       = 0.76, 0.9   # Fixed from exp_185 best combination

ONSET_WEIGHTS = {
    'qok': 0.121, 'qo': 0.034, 'cth': 0.003, 'ch': 0.064, 'sh': 0.090,
    'ok': 0.066, 'd': 0.068, 's': 0.028, 'y': 0.041, 'k': 0.022,
    't': 0.020, 'l': 0.058, 'other': 0.111,
}
SUFFIX_WEIGHTS = {
    'am': 0.020, 'aiin': 0.103, 'edy': 0.183, 'ain': 0.070, 'ey': 0.040,
    'ol': 0.063, 'or': 0.033, 'al': 0.055, 'ar': 0.074, 'dy': 0.030, 'other': 0.329,
}
LL_ONSETS  = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
EVA_CHARS  = list('acdehiklmnoqrsty')

LATIN_CI_Y = re.compile(r'^[Qq][uU]|^[Nn]o|^[Ee]t\b|^[Aa]t\b', re.I)
LATIN_CI_T = re.compile(r'^[Tt][aeiouAEIOU]', re.I)
LATIN_CI_S = re.compile(r'^[Ss][aeiouAEIOU]', re.I)

def make_word(onset, suffix, rng):
    return onset + rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei']) + suffix

def random_eva_word(rng):
    o = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
    s = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
    return make_word(o, s, rng)

def cipher_lf(w, rng, p=0.90):
    wl = w.lower()
    if LATIN_CI_Y.match(wl) and rng.random() < p:
        return make_word('y', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    elif LATIN_CI_T.match(wl) and rng.random() < p:
        return make_word('t', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    elif LATIN_CI_S.match(wl) and rng.random() < p:
        return make_word('s', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    return random_eva_word(rng)

# Original morphological LL cipher (baseline)
LATIN_CF = re.compile(r'(am|um|us|em|is|ae|orum|bus|unt|it|ant|at)$', re.I)
def cipher_ll_morph(w, rng, p=1.00):
    if LATIN_CF.search(w.lower()) and rng.random() < p:
        onset = rng.choices(list(LL_ONSETS.keys()), weights=list(LL_ONSETS.values()))[0]
        return make_word(onset, 'am', rng)
    return random_eva_word(rng)

# Blind LL cipher variant A: -am words get LL_ONSETS (d=0.40, same as original)
def cipher_ll_blind_ll_onset(rng, p_blind):
    if rng.random() < p_blind:
        onset = rng.choices(list(LL_ONSETS.keys()), weights=list(LL_ONSETS.values()))[0]
        return make_word(onset, 'am', rng)
    return random_eva_word(rng)

# Blind LL cipher variant B: -am words get random_eva_word onset (ONSET_WEIGHTS)
def cipher_ll_blind_random_onset(rng, p_blind):
    if rng.random() < p_blind:
        onset = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
        return make_word(onset, 'am', rng)
    return random_eva_word(rng)

def timm_modify(word, rng):
    if not word: return word
    op = rng.choice(['replace', 'insert', 'delete'])
    pos = rng.randint(0, max(0, len(word)-1))
    if op == 'replace': return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert': return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else: return word[:pos] + word[pos+1:] if len(word)>1 else word

ENGLISH_SW = {'the','and','of','to','a','in','that','is','was','he','it','for','on','are',
              'as','with','his','they','at','be','this','have','from','or','had','by','not',
              'but','what','all','were','we','when','your','can','said','there','use','an',
              'each','which','she','do','how','their','if','will','up','other','about','out',
              'many','then','them','these','so','some','her','would','make','like','him',
              'into','time','has','look','two','more'}

def load_latin(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    words = []
    for p in re.split(r'\n\s*\n', text):
        ws = re.findall(r'\b[a-zA-Z]+\b', p)
        if not ws: continue
        if sum(1 for w in ws if w.lower() in ENGLISH_SW)/len(ws) < 0.08:
            words.extend(ws)
    return words

def run_sim_morph(latin_words, rng, p_ll=1.00):
    """Morphological cipher (baseline from exp_186)."""
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf(word, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_morph(word, rng, p_ll)
            else:
                if buf and rng.random() < CP:
                    ew = timm_modify(rng.choice(list(buf)), rng) if rng.random() < MP else rng.choice(list(buf))
                else:
                    ew = random_eva_word(rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def run_sim_blind(latin_words, rng, p_blind, use_ll_onset=True):
    """Blind LL mapping — ignores morphology, maps LL to -am with probability p_blind."""
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf(word, rng)
            elif i == len(chunk)-1:
                if use_ll_onset:
                    ew = cipher_ll_blind_ll_onset(rng, p_blind)
                else:
                    ew = cipher_ll_blind_random_onset(rng, p_blind)
            else:
                if buf and rng.random() < CP:
                    ew = timm_modify(rng.choice(list(buf)), rng) if rng.random() < MP else rng.choice(list(buf))
                else:
                    ew = random_eva_word(rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def get_onset(w):
    for p in ['qok','qo','cth','ch','sh','ok','d','s','y','k','t','l','r']:
        if w.startswith(p): return p
    return 'other'

def compute_metrics(lines):
    aw = [w for l in lines for w in l]
    n = len(aw)
    if n < 100: return None
    oc = Counter(get_onset(w) for w in aw)
    lf = [l[0] for l in lines if l]
    ll = [l[-1] for l in lines if len(l) > 1]

    # -am metrics
    am_r = sum(1 for w in aw if w.endswith('am')) / n
    ll_am = sum(1 for w in ll if w.endswith('am')) / len(ll) if ll else 0
    am_ll = ll_am / am_r if am_r > 0 else 0

    # d-onset metrics
    d_r = oc.get('d', 0) / n
    ll_d = sum(1 for w in ll if get_onset(w) == 'd') / len(ll) if ll else 0
    d_ll = ll_d / d_r if d_r > 0 else 0

    # y-onset LF
    y_r = oc.get('y', 0) / n
    y_lf = (sum(1 for w in lf if get_onset(w) == 'y') / len(lf)) / y_r if y_r and lf else 0

    # Self-succession
    tb = n - 1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc.get(o, 0) / n
        return bg.get((o, o), 0) / (tb * b * b) if b > 0 and tb > 0 else 1.0
    ss_m = (ss('qok') + ss('ok') + ss('ch')) / 3
    adj = sum(1 for i in range(tb) if aw[i] == aw[i+1]) / max(1, tb)

    # LL onset distribution
    ll_onsets = Counter(get_onset(w) for w in ll)
    ll_n = len(ll)
    d_ll_abs = ll_onsets.get('d', 0) / ll_n if ll_n > 0 else 0
    ok_ll_abs = ll_onsets.get('ok', 0) / ll_n if ll_n > 0 else 0

    return {
        'am_ll': round(am_ll, 4),
        'd_ll': round(d_ll, 4),
        'y_lf': round(y_lf, 4),
        'ss_mean': round(ss_m, 4),
        'adj_rate': round(adj, 5),
        'am_base': round(am_r, 4),
        'd_base': round(d_r, 4),
        'll_am_abs': round(ll_am, 4),
        'll_d_abs': round(ll_d, abs=4) if False else round(ll_d, 4),
    }

VMS = {'am_ll': 6.811, 'd_ll': 1.464, 'y_lf': 3.506, 'ss_mean': 1.465, 'adj_rate': 0.009}

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print(f"  Fixed: cp={CP}, mp={MP} (exp_185 best combination)")
print()

SEED = 209000

def run_batch(config_name, run_fn, n_sims=N_SIMS):
    sims = []
    for i in range(n_sims):
        rng = random.Random(SEED + i)
        lines = run_fn(rng)
        m = compute_metrics(lines)
        if m:
            sims.append(m)
    if not sims:
        return None
    def mc(k):
        v = sorted(x[k] for x in sims)
        mean = sum(v) / len(v)
        lo = v[int(0.05 * len(v))]
        hi = v[int(0.95 * len(v))]
        return mean, lo, hi
    am, _, _ = mc('am_ll')
    dl, _, _ = mc('d_ll')
    y, _, _ = mc('y_lf')
    ss, _, _ = mc('ss_mean')
    adj, _, _ = mc('adj_rate')
    print(f"  {config_name:<40}: am_ll={am:.3f} ({am/VMS['am_ll']*100:.1f}%VMS) "
          f"d_ll={dl:.3f} ({dl/VMS['d_ll']*100:.1f}%VMS) "
          f"y_lf={y:.3f} ss={ss:.3f} adj={adj:.5f}")
    return {'am_ll': am, 'd_ll': dl, 'y_lf': y, 'ss_mean': ss, 'adj_rate': adj}

print("=== Baseline: Morphological LL cipher (p_detect=1.00, exp_186 ceiling) ===")
run_batch("morph_baseline (p_detect=1.00)",
    lambda rng: run_sim_morph(latin, rng, p_ll=1.00))
print(f"  VMS targets:                                  am_ll={VMS['am_ll']:.3f} (100.0%VMS) "
      f"d_ll={VMS['d_ll']:.3f} (100.0%VMS) y_lf={VMS['y_lf']:.3f} ss={VMS['ss_mean']:.3f} adj={VMS['adj_rate']:.5f}")
print()

print("=== Variant A: Blind LL mapping with LL_ONSETS (d=0.40 for am-words) ===")
for p_blind in [0.10, 0.20, 0.40, 0.50, 0.63, 0.80, 1.00]:
    run_batch(f"blind+ll_onset p_blind={p_blind:.2f}",
        lambda rng, pb=p_blind: run_sim_blind(latin, rng, pb, use_ll_onset=True))
print()

print("=== Variant B: Blind LL mapping with ONSET_WEIGHTS (d=6.8% for am-words) ===")
for p_blind in [0.10, 0.20, 0.40, 0.50, 0.63, 0.80, 1.00]:
    run_batch(f"blind+random_onset p_blind={p_blind:.2f}",
        lambda rng, pb=p_blind: run_sim_blind(latin, rng, pb, use_ll_onset=False))
print()

# What p_blind+onset combination can simultaneously reproduce both am_ll and d_ll near VMS?
# Compute analytically:
# LL am rate needed = VMS_am_ll × am_base / (1 - VMS_am_ll × ll_rate + VMS_am_ll × ll_rate)
# Let r_ll = LL fraction of corpus ≈ 0.119; am_base ≈ 0.02
# VMS_am_ll = 6.811: LL_am_rate = VMS_am_ll × am_base (approx) ≈ 0.136
# This is simplified; sim computes it correctly.

print("\n=== Analytical estimates ===")
am_base = 0.02
d_base = 0.068
r_ll = 0.119
r_mid = 0.762
vms_am_ll = 6.811
vms_d_ll = 1.464

# Corpus am = r_ll × LL_am + r_mid × am_base + r_lf × lf_am_base
# Approximation: lf_am_base ≈ 0.02 (y/s/t onset words with any suffix incl am)
corp_am = lambda ll_am: r_ll * ll_am + (1 - r_ll) * am_base
am_ll_fn = lambda ll_am: ll_am / corp_am(ll_am) if corp_am(ll_am) > 0 else 0

print(f"Analytical LL_am_rate needed for am_ll = {vms_am_ll}:")
# Solve: ll_am / (r_ll * ll_am + (1-r_ll) * 0.02) = 6.811
# ll_am = 6.811 * (r_ll * ll_am + (1-r_ll) * 0.02)
# ll_am * (1 - 6.811 * r_ll) = 6.811 * (1-r_ll) * 0.02
# ll_am = 6.811 * (1-r_ll) * 0.02 / (1 - 6.811 * r_ll)
ll_am_needed = vms_am_ll * (1-r_ll) * am_base / (1 - vms_am_ll * r_ll)
print(f"  LL am rate target: {ll_am_needed:.4f} ({ll_am_needed*100:.1f}%)")
print(f"  Corresponds to p_blind: ~{(ll_am_needed - am_base) / (1.0 - am_base):.3f}")

print(f"\nAnalytical LL_d_rate target for d_ll = {vms_d_ll}:")
corp_d = lambda ll_d: r_ll * ll_d + (1 - r_ll) * d_base
d_ll_fn = lambda ll_d: ll_d / corp_d(ll_d) if corp_d(ll_d) > 0 else 0
ll_d_needed = vms_d_ll * (1-r_ll) * d_base / (1 - vms_d_ll * r_ll)
print(f"  LL d rate target: {ll_d_needed:.4f} ({ll_d_needed*100:.1f}%)")

print(f"\nIn Variant A (ll_onset), at p_blind={ll_am_needed:.2f}:")
ll_am = ll_am_needed
ll_d_variant_a = ll_am * LL_ONSETS['d']  # fraction of LL words that are d-onset = p_blind × 0.40
print(f"  LL am rate: {ll_am:.4f}")
print(f"  LL d rate (from am-words): {ll_d_variant_a:.4f} (d is 40% of am-onset)")
# Plus non-am LL words contribute d from ONSET_WEIGHTS
ll_nonam = 1 - ll_am
ll_d_variant_a_total = ll_am * LL_ONSETS['d'] + ll_nonam * d_base
print(f"  LL d total rate: {ll_d_variant_a_total:.4f}")
corp_d_va = r_ll * ll_d_variant_a_total + (1-r_ll) * d_base
print(f"  d_ll enrichment: {ll_d_variant_a_total / corp_d_va:.3f}× (VMS: {vms_d_ll}×)")
