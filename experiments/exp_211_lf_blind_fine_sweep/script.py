"""
exp_211: H403 — Fine-Grained p_lf_blind Sweep to Precisely Locate y_lf=3.506

Motivation:
  exp_210 (H402) showed:
  - p_lf_blind=0.20 → y_lf=3.364 (96.0%VMS)
  - p_lf_blind=0.30 → y_lf=4.019 (114.5%VMS — overshoots)
  VMS target y_lf=3.506 falls between; interpolation: p_lf_blind ≈ 0.22-0.24

  exp_210 also confirmed:
  - d_am=0.16 → am_ll=6.778 (99.5%VMS) AND d_ll=1.461 (99.8%VMS) simultaneously
  - Best joint (d_am=0.16, p_blind=0.40, p_lf_blind=0.20): all 5 metrics within ~4%VMS

Test: fine-grained sweep p_lf_blind ∈ {0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.27}
  Fixed: d_am=0.16, p_blind=0.40, cp=0.76, mp=0.9
  N=50 sims per configuration (vs N=30 in exp_210 — tighter CIs)

Goal: Identify p_lf_blind that achieves y_lf ≈ 3.506 (VMS). At that value, report whether
  ALL five primary metrics are jointly within ~2% of VMS simultaneously.

Pre-registration:
  p_lf_blind ≈ 0.22-0.23 should produce y_lf ≈ 3.506.
  am_ll and d_ll should remain near-constant across the sweep (LF rule only affects y_lf, not LL mapping).
  ss_mean and adj_rate should remain near-constant (copy component unchanged).

Seed base: 211000. N_SIMS=50 per configuration.
"""

import os, re, random
from collections import Counter, deque

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')

N_SIMS       = 50
TARGET_LINES = 2447
WINDOW       = 20
CP, MP       = 0.76, 0.9   # Fixed from exp_185/209/210
P_BLIND      = 0.40        # Fixed from exp_209/210
D_AM         = 0.16        # Fixed from exp_210 (d_ll calibration)

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

VMS = {'am_ll': 6.811, 'd_ll': 1.464, 'y_lf': 3.506, 'ss_mean': 1.465, 'adj_rate': 0.009}
SEED = 211000

def make_ll_onsets_recal(d_weight):
    """Create LL_ONSETS with custom d_weight; redistribute remaining weight proportionally."""
    base = {'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
    base_total = sum(base.values())  # 0.60
    scale = (1.0 - d_weight) / base_total
    result = {k: v * scale for k, v in base.items()}
    result['d'] = d_weight
    return result

LL_ONSETS = make_ll_onsets_recal(D_AM)

def make_word(onset, suffix, rng):
    return onset + rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei']) + suffix

def random_eva_word(rng):
    o = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
    s = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
    return make_word(o, s, rng)

def cipher_ll_blind(rng):
    """Blind LL mapping at p_blind=0.40 with recalibrated LL_ONSETS (d=0.16)."""
    if rng.random() < P_BLIND:
        onset = rng.choices(list(LL_ONSETS.keys()), weights=list(LL_ONSETS.values()))[0]
        return make_word(onset, 'am', rng)
    return random_eva_word(rng)

def cipher_lf_blind(rng, p_lf_blind):
    """Blind LF mapping: generates y-onset word with probability p_lf_blind."""
    if rng.random() < p_lf_blind:
        return make_word('y', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
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

def run_sim(latin_words, rng, p_lf_blind):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf_blind(rng, p_lf_blind)
            elif i == len(chunk)-1:
                ew = cipher_ll_blind(rng)
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

def run_batch(p_lf_blind):
    sims = []
    for i in range(N_SIMS):
        rng = random.Random(SEED + i)
        lines = run_sim(latin, rng, p_lf_blind)
        m = compute_metrics(lines)
        if m: sims.append(m)
    if not sims: return None

    def mc(k):
        v = sorted(x[k] for x in sims)
        mean = sum(v)/len(v)
        ci_lo = v[max(0, int(.05*len(v)))]
        ci_hi = v[min(len(v)-1, int(.95*len(v)))]
        return mean, ci_lo, ci_hi

    am, aml, amh = mc('am_ll')
    dl, dll, dlh = mc('d_ll')
    y, yl, yh = mc('y_lf')
    ss, ssl, ssh = mc('ss_mean')
    adj, adjl, adjh = mc('adj_rate')

    am_pct = am / VMS['am_ll'] * 100
    dl_pct = dl / VMS['d_ll'] * 100
    y_pct = y / VMS['y_lf'] * 100
    ss_pct = ss / VMS['ss_mean'] * 100

    am_ok = '✓' if 6.5 <= am <= 7.1 else ' '
    dl_ok = '✓' if 1.2 <= dl <= 1.7 else ' '
    y_ok  = '✓' if 3.2 <= y <= 3.8 else ' '
    ss_ok = '✓' if 1.2 <= ss <= 1.7 else ' '
    adj_ok = '✓' if adj <= 0.009 else ' '

    print(f"  p_lf={p_lf_blind:.2f}: am_ll={am:.3f}({am_pct:.1f}%){am_ok} "
          f"d_ll={dl:.3f}({dl_pct:.1f}%){dl_ok} y_lf={y:.3f}({y_pct:.1f}%){y_ok} "
          f"ss={ss:.3f}({ss_pct:.1f}%){ss_ok} adj={adj:.5f}{adj_ok}")
    print(f"         y_lf CI=[{yl:.3f},{yh:.3f}]  am_ll CI=[{aml:.3f},{amh:.3f}]  d_ll CI=[{dll:.3f},{dlh:.3f}]")
    return {
        'p_lf_blind': p_lf_blind,
        'am_ll': am, 'd_ll': dl, 'y_lf': y, 'ss_mean': ss, 'adj_rate': adj,
        'y_lf_ci': (yl, yh), 'am_ll_ci': (aml, amh), 'd_ll_ci': (dll, dlh),
        'ss_mean_ci': (ssl, ssh),
    }


print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print(f"  Fixed: cp={CP}, mp={MP}, p_blind={P_BLIND}, d_am={D_AM}")
print(f"  LL_ONSETS: {LL_ONSETS}")
print(f"  VMS targets: am_ll={VMS['am_ll']} d_ll={VMS['d_ll']} y_lf={VMS['y_lf']} ss={VMS['ss_mean']} adj={VMS['adj_rate']}")
print(f"  N_SIMS={N_SIMS} per configuration")
print()

print("=== H403: Fine-grained p_lf_blind sweep ===")
print("  [Goal: locate p_lf_blind that achieves y_lf ≈ 3.506 (VMS)]")
print("  [exp_210: p_lf=0.20 → y_lf=3.364 (96%); p_lf=0.30 → y_lf=4.019 (115%)]")
print()

results = []
for p_lf in [0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.27]:
    r = run_batch(p_lf)
    if r:
        results.append(r)
    print()

print()
print("=== Summary: best p_lf_blind for y_lf ===")
if results:
    # Find closest to VMS y_lf target
    best = min(results, key=lambda r: abs(r['y_lf'] - VMS['y_lf']))
    print(f"  Closest to y_lf=3.506: p_lf_blind={best['p_lf_blind']:.2f} → y_lf={best['y_lf']:.3f} ({best['y_lf']/VMS['y_lf']*100:.1f}%VMS)")
    print()
    print("  All-five-metric summary at closest-to-target configuration:")
    print(f"    am_ll = {best['am_ll']:.3f} ({best['am_ll']/VMS['am_ll']*100:.1f}%VMS)")
    print(f"    d_ll  = {best['d_ll']:.3f} ({best['d_ll']/VMS['d_ll']*100:.1f}%VMS)")
    print(f"    y_lf  = {best['y_lf']:.3f} ({best['y_lf']/VMS['y_lf']*100:.1f}%VMS)")
    print(f"    ss_mean = {best['ss_mean']:.3f} ({best['ss_mean']/VMS['ss_mean']*100:.1f}%VMS)")
    print(f"    adj_rate = {best['adj_rate']:.5f} (VMS 0.009, {'✓ below' if best['adj_rate'] <= 0.009 else '✗ above'})")

    # Check if all five within 3% of VMS
    thresholds = [
        abs(best['am_ll'] - VMS['am_ll']) / VMS['am_ll'] < 0.03,
        abs(best['d_ll'] - VMS['d_ll']) / VMS['d_ll'] < 0.03,
        abs(best['y_lf'] - VMS['y_lf']) / VMS['y_lf'] < 0.03,
        abs(best['ss_mean'] - VMS['ss_mean']) / VMS['ss_mean'] < 0.03,
        best['adj_rate'] <= VMS['adj_rate'],
    ]
    n_passing = sum(thresholds)
    print()
    print(f"  All-five within 3%VMS: {n_passing}/5 metrics pass")
    if all(thresholds):
        print("  *** ALL FIVE PRIMARY METRICS WITHIN 3% OF VMS — STRONGEST JOINT RESULT ***")
