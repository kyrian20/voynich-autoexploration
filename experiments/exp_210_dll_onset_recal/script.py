"""
exp_210: H401 — LL_ONSETS Recalibration to jointly reproduce am_ll AND d_ll

Motivation:
  exp_209 showed:
  - Blind LL mapping at p_blind=0.40 achieves am_ll=6.817 (100.1% VMS)
  - BUT LL_ONSETS[d]=0.40 overproduces d_ll (2.30× vs VMS 1.464×)
  - Variant B (random onset, d=0.068) underproduces d_ll (1.18× vs VMS)
  - VMS d_ll requires d_am_weight ≈ 0.16 (analytically)

Test: sweep d_am_weight ∈ {0.05, 0.08, 0.10, 0.12, 0.15, 0.16, 0.20, 0.25, 0.30, 0.40}
  at p_blind=0.40 (blind LL mapping that achieves am_ll ≈ VMS).
  For each d_am_weight, redistribute remaining LL_ONSETS weight proportionally
  across other LL onset classes (ok, qok, ch, other).

Also test: blind LF mapping (analogous to H402) — sweep p_lf_blind to target y_lf ≈ VMS.
  Base LF mapping targets y-onset specifically; a blind LF mapping uses p_lf_blind
  probability of mapping ALL LF words to y-onset (instead of checking Latin CI patterns).

Pre-registration:
  d_am_weight ≈ 0.16 should produce d_ll ≈ 1.464× while preserving am_ll ≈ 6.817×
  ss_mean and adj_rate: unaffected (copy unchanged)
  y_lf gap: tested separately in the blind LF section

Seed base: 210000. N_SIMS=30 per configuration.
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')

N_SIMS       = 30
TARGET_LINES = 2447
WINDOW       = 20
CP, MP       = 0.76, 0.9   # Fixed from exp_185/209

ONSET_WEIGHTS = {
    'qok': 0.121, 'qo': 0.034, 'cth': 0.003, 'ch': 0.064, 'sh': 0.090,
    'ok': 0.066, 'd': 0.068, 's': 0.028, 'y': 0.041, 'k': 0.022,
    't': 0.020, 'l': 0.058, 'other': 0.111,
}
SUFFIX_WEIGHTS = {
    'am': 0.020, 'aiin': 0.103, 'edy': 0.183, 'ain': 0.070, 'ey': 0.040,
    'ol': 0.063, 'or': 0.033, 'al': 0.055, 'ar': 0.074, 'dy': 0.030, 'other': 0.329,
}
EVA_CHARS  = list('acdehiklmnoqrsty')

# Original LL_ONSETS (exp_182-186): d=0.40 (overproduces d_ll)
LL_ONSETS_ORIG = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}

# LF patterns (from exp_186)
LATIN_CI_Y = re.compile(r'^[Qq][uU]|^[Nn]o|^[Ee]t\b|^[Aa]t\b', re.I)
LATIN_CI_T = re.compile(r'^[Tt][aeiouAEIOU]', re.I)
LATIN_CI_S = re.compile(r'^[Ss][aeiouAEIOU]', re.I)

def make_word(onset, suffix, rng):
    return onset + rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei']) + suffix

def random_eva_word(rng):
    o = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
    s = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
    return make_word(o, s, rng)

def cipher_lf_morph(w, rng, p=0.90):
    wl = w.lower()
    if LATIN_CI_Y.match(wl) and rng.random() < p:
        return make_word('y', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    elif LATIN_CI_T.match(wl) and rng.random() < p:
        return make_word('t', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    elif LATIN_CI_S.match(wl) and rng.random() < p:
        return make_word('s', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    return random_eva_word(rng)

def cipher_lf_blind(rng, p_lf_blind):
    """Blind LF mapping: maps all LF words to y-onset with probability p_lf_blind."""
    if rng.random() < p_lf_blind:
        return make_word('y', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    return random_eva_word(rng)

def make_ll_onsets_recal(d_weight):
    """Create LL_ONSETS with custom d_weight; redistribute remaining weight proportionally."""
    base = {'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
    base_total = sum(base.values())  # 0.60
    scale = (1.0 - d_weight) / base_total
    result = {k: v * scale for k, v in base.items()}
    result['d'] = d_weight
    return result

def cipher_ll_blind(rng, p_blind, ll_onsets):
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
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

def run_sim(latin_words, rng, p_blind, ll_onsets, lf_fn):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = lf_fn(word, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_blind(rng, p_blind, ll_onsets)
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

    am_r = sum(1 for w in aw if w.endswith('am')) / n
    ll_am = sum(1 for w in ll if w.endswith('am')) / len(ll) if ll else 0
    am_ll = ll_am / am_r if am_r > 0 else 0

    d_r = oc.get('d', 0) / n
    ll_d = sum(1 for w in ll if get_onset(w) == 'd') / len(ll) if ll else 0
    d_ll = ll_d / d_r if d_r > 0 else 0

    y_r = oc.get('y', 0) / n
    y_lf = (sum(1 for w in lf if get_onset(w) == 'y') / len(lf)) / y_r if y_r and lf else 0

    tb = n - 1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc.get(o, 0) / n
        return bg.get((o, o), 0) / (tb * b * b) if b > 0 and tb > 0 else 1.0
    ss_m = (ss('qok') + ss('ok') + ss('ch')) / 3
    adj = sum(1 for i in range(tb) if aw[i] == aw[i+1]) / max(1, tb)

    return {'am_ll': round(am_ll, 4), 'd_ll': round(d_ll, 4),
            'y_lf': round(y_lf, 4), 'ss_mean': round(ss_m, 4),
            'adj_rate': round(adj, 5)}

VMS = {'am_ll': 6.811, 'd_ll': 1.464, 'y_lf': 3.506, 'ss_mean': 1.465, 'adj_rate': 0.009}
SEED = 210000

def run_batch(config_name, p_blind, ll_onsets, lf_fn):
    sims = []
    for i in range(N_SIMS):
        rng = random.Random(SEED + i)
        lines = run_sim(latin, rng, p_blind, ll_onsets, lf_fn)
        m = compute_metrics(lines)
        if m: sims.append(m)
    if not sims: return None
    def mc(k):
        v = sorted(x[k] for x in sims)
        return sum(v)/len(v), v[int(.05*len(v))], v[int(.95*len(v))]
    am, aml, amh = mc('am_ll')
    dl, dll, dlh = mc('d_ll')
    y, yl, yh = mc('y_lf')
    ss, _, _ = mc('ss_mean')
    adj, _, _ = mc('adj_rate')
    am_ok = '✓' if 6.5 <= am <= 7.1 else ' '
    dl_ok = '✓' if 1.2 <= dl <= 1.7 else ' '
    y_ok = '✓' if y >= 3.0 else ' '
    print(f"  {config_name:<40}: am_ll={am:.3f}{am_ok} d_ll={dl:.3f}{dl_ok} y_lf={y:.3f}{y_ok} ss={ss:.3f} adj={adj:.5f}")
    return {'am_ll': am, 'd_ll': dl, 'y_lf': y, 'ss_mean': ss, 'adj_rate': adj}

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print(f"  Fixed: cp={CP}, mp={MP}, p_blind=0.40 (from exp_209)")
print(f"  VMS: am_ll={VMS['am_ll']} d_ll={VMS['d_ll']} y_lf={VMS['y_lf']} ss={VMS['ss_mean']} adj={VMS['adj_rate']}")
print(f"  Mark: ✓ = within acceptable range for metric")
print()

lf_morph = lambda w, rng: cipher_lf_morph(w, rng, 0.90)

print("=== H401: d_am_weight sweep (p_blind=0.40 fixed) ===")
print("  [Target: am_ll ≈ 6.811, d_ll ≈ 1.464]")
best_both = None
for d_w in [0.05, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.25, 0.30, 0.40]:
    ll_onsets = make_ll_onsets_recal(d_w)
    res = run_batch(f"d_am={d_w:.2f} (p_blind=0.40)", 0.40, ll_onsets, lf_morph)
    if res and 6.5 <= res['am_ll'] <= 7.1 and 1.2 <= res['d_ll'] <= 1.7:
        if best_both is None or abs(res['am_ll'] - VMS['am_ll']) + abs(res['d_ll'] - VMS['d_ll']) < \
           abs(best_both['am_ll'] - VMS['am_ll']) + abs(best_both['d_ll'] - VMS['d_ll']):
            best_both = res
            best_both['d_w'] = d_w

print()
if best_both:
    print(f"  Best joint (am_ll+d_ll): d_am={best_both['d_w']:.2f} → am_ll={best_both['am_ll']:.3f}, d_ll={best_both['d_ll']:.3f}")
else:
    print("  No configuration simultaneously satisfies am_ll and d_ll within range.")

print()
print("=== H402: Blind LF mapping sweep (d_am=0.16, p_blind=0.40 fixed) ===")
print("  [Target: y_lf ≈ 3.506 — can a blind LF rule close the y_lf gap?]")
ll_onsets_cal = make_ll_onsets_recal(0.16)  # recalibrated from H401
for p_lf_blind in [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00]:
    lf_blind = lambda w, rng, p=p_lf_blind: cipher_lf_blind(rng, p)
    run_batch(f"blind_lf p_lf={p_lf_blind:.2f} (d_am=0.16, p_bl=0.40)",
        0.40, ll_onsets_cal, lf_blind)

print()
print("=== Best achievable: d_am=0.16, p_blind=0.40, p_lf=0.90 (morph LF baseline) ===")
run_batch("d_am=0.16, p_blind=0.40, morph_lf (best expected joint)", 0.40, ll_onsets_cal, lf_morph)

print()
print("=== Analytical check ===")
r_ll = 0.119
am_base = 0.02
d_base = 0.068
for d_w in [0.10, 0.16, 0.20, 0.30, 0.40]:
    ll_am_rate = 0.40 * 1.0 + 0.60 * am_base  # p_blind=0.40
    ll_d_rate = 0.40 * d_w + 0.60 * d_base
    corp_am = r_ll * ll_am_rate + (1-r_ll) * am_base
    corp_d = r_ll * ll_d_rate + (1-r_ll) * d_base
    am_enr = ll_am_rate / corp_am if corp_am > 0 else 0
    d_enr = ll_d_rate / corp_d if corp_d > 0 else 0
    print(f"  d_am={d_w:.2f}: analytical am_ll={am_enr:.3f}, d_ll={d_enr:.3f}")
