"""
exp_185: Fine-Grained COPY_PROB Grid to Localize VMS ss_mean Crossover (H350)

Motivation:
  exp_183 (extended grid) reveals:
  - cp=0.7, mp=0.8: ss_mean=1.380 (94.2% of VMS 1.465), adj=0.00692 ≤ VMS ✓
  - cp=0.8, mp=0.8: ss_mean=1.570 (107.2% of VMS), adj=0.00798 ≤ VMS ✓
  The VMS ss_mean target (1.465) lies between these two points. Linear interpolation:
  cp_optimal ≈ 0.7 + 0.1 × (1.465 - 1.380) / (1.570 - 1.380) ≈ 0.745.

  This experiment tests cp ∈ {0.70, 0.72, 0.74, 0.76, 0.78, 0.80} × mp ∈ {0.7, 0.8, 0.9}
  to directly locate the cp value that jointly satisfies:
  - ss_mean closest to VMS target (1.465)
  - adj_rate ≤ VMS (≤ 0.009)
  - am_ll ≥ 5.0

Pre-registration:
  Expected: ss_mean ≈ 1.465 (VMS target) at cp≈0.745, mp=0.8 or 0.9.
  Expected: am_ll increases linearly from ~6.30 (cp=0.7) to ~6.50 (cp=0.8).
  At optimal cp (≈0.745): am_ll ≈ 6.40 (93.9% VMS) — establishing the final residual gap.
  adj_rate at optimal cp: ≈ 0.007 (well below VMS threshold).

Architecture: identical to exp_182/183 (MID-only buffer, Timm char modification, exp_177 tables).
Grid: cp ∈ {0.70, 0.72, 0.74, 0.76, 0.78, 0.80} × mp ∈ {0.7, 0.8, 0.9} = 18 combinations × 50 sims.
Seed base: 185000.
"""
from pathlib import Path as _RepositoryPath

import os, re, random, json
from collections import Counter, deque

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
OUT_DIR      = os.path.join(REPO_DIR, 'experiments/exp_185_timm_char_cp_fine_grid/data')
os.makedirs(OUT_DIR, exist_ok=True)

N_SIMS       = 50
TARGET_LINES = 2447
WINDOW       = 20

ONSET_WEIGHTS = {
    'qok': 0.121, 'qo': 0.034, 'cth': 0.003, 'ch': 0.064, 'sh': 0.090,
    'ok': 0.066, 'd': 0.068, 's': 0.028, 'y': 0.041, 'k': 0.022,
    't': 0.020, 'l': 0.058, 'other': 0.111,
}
SUFFIX_WEIGHTS = {
    'am': 0.020, 'aiin': 0.103, 'edy': 0.183, 'ain': 0.070, 'ey': 0.040,
    'ol': 0.063, 'or': 0.033, 'al': 0.055, 'ar': 0.074, 'dy': 0.030, 'other': 0.329,
}
EVA_CHARS = list('acdehiklmnoqrsty')

def make_word(onset, suffix, rng):
    return onset + rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei']) + suffix

def random_eva_word(rng):
    o = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
    s = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
    return make_word(o, s, rng)

LATIN_CF    = re.compile(r'(am|um|us|em|is|ae|orum|bus|unt|it|ant|at)$', re.I)
LATIN_CI_S  = re.compile(r'^[Ss][aeiouAEIOU]', re.I)
LATIN_CI_T  = re.compile(r'^[Tt][aeiouAEIOU]', re.I)
LATIN_CI_Y  = re.compile(r'^[Qq][uU]|^[Nn]o|^[Ee]t\b|^[Aa]t\b', re.I)

def cipher_lf(w, rng, p=0.90):
    wl = w.lower()
    if LATIN_CI_Y.match(wl) and rng.random() < p:
        return make_word('y', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    elif LATIN_CI_T.match(wl) and rng.random() < p:
        return make_word('t', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    elif LATIN_CI_S.match(wl) and rng.random() < p:
        return make_word('s', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    return random_eva_word(rng)

def cipher_ll(w, rng, p=0.90):
    if LATIN_CF.search(w.lower()) and rng.random() < p:
        ll_onsets = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
        return make_word(rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0], 'am', rng)
    return random_eva_word(rng)

def cipher_mid(rng):
    return random_eva_word(rng)

def timm_modify(word, rng):
    if not word: return word
    op  = rng.choice(['replace', 'insert', 'delete'])
    pos = rng.randint(0, max(0, len(word) - 1))
    if op == 'replace':
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:
        return word[:pos] + word[pos+1:] if len(word) > 1 else word

ENGLISH_SW = {
    'the','and','of','to','a','in','that','is','was','he','it','for','on','are',
    'as','with','his','they','at','be','this','have','from','or','had','by','not',
    'but','what','all','were','we','when','your','can','said','there','use','an',
    'each','which','she','do','how','their','if','will','up','other','about','out',
    'many','then','them','these','so','some','her','would','make','like','him',
    'into','time','has','look','two','more',
}

def load_latin(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    paragraphs = re.split(r'\n\s*\n', text)
    words = []
    for p in paragraphs:
        ws = re.findall(r'\b[a-zA-Z]+\b', p)
        if not ws: continue
        if sum(1 for w in ws if w.lower() in ENGLISH_SW) / len(ws) < 0.08:
            words.extend(ws)
    return words

def make_sents(words, rng):
    s = list(words)
    rng.shuffle(s)
    sents, i = [], 0
    while i < len(s) - 3:
        n = rng.randint(8, 15)
        sents.append(s[i:i+n])
        i += n
    return sents

def run_sim(sents, rng, cp, mp):
    all_latin = [w for s in sents for w in s if re.match(r'[a-zA-Z]', w)]
    rng.shuffle(all_latin)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(all_latin) - 2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = all_latin[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, w in enumerate(chunk):
            if i == 0 and len(chunk) > 1:
                ew = cipher_lf(w, rng)
            elif i == len(chunk) - 1 or len(chunk) == 1:
                ew = cipher_ll(w, rng)
            else:
                if buf and rng.random() < cp:
                    ew = timm_modify(rng.choice(list(buf)), rng) if rng.random() < mp else rng.choice(list(buf))
                else:
                    ew = cipher_mid(rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line)
        pos += n
    return lines[:TARGET_LINES]

def get_onset(w):
    for p in ['qok', 'qo', 'cth', 'ch', 'sh', 'ok', 'd', 's', 'y', 'k', 't', 'l', 'r']:
        if w.startswith(p): return p
    return 'other'

def metrics(lines):
    all_w = [w for l in lines for w in l]
    n = len(all_w)
    if n < 100: return None
    oc = Counter(get_onset(w) for w in all_w)
    lf = [l[0] for l in lines if l]
    ll = [l[-1] for l in lines if len(l) > 1]
    am_r = sum(1 for w in all_w if w.endswith('am')) / n
    am_ll = (sum(1 for w in ll if w.endswith('am')) / len(ll)) / am_r if am_r and ll else 1.0
    y_r  = oc['y'] / n
    y_lf = (sum(1 for w in lf if get_onset(w)=='y') / len(lf)) / y_r if y_r and lf else 1.0
    tb = n - 1
    bg = Counter((get_onset(all_w[i]), get_onset(all_w[i+1])) for i in range(tb))
    def ss(o):
        b = oc[o] / n
        return bg[(o,o)] / (tb * b * b) if b > 0 and tb > 0 else 1.0
    ss_m = (ss('qok') + ss('ok') + ss('ch')) / 3
    mid_bg, mid_oc = Counter(), Counter()
    for l in lines:
        if len(l) < 3: continue
        mw = l[1:-1]
        for w in mw: mid_oc[get_onset(w)] += 1
        for j in range(len(mw)-1): mid_bg[(get_onset(mw[j]), get_onset(mw[j+1]))] += 1
    nm = sum(mid_oc.values()); nb = sum(mid_bg.values())
    def ss_mid(o):
        b = mid_oc[o]/nm if nm else 0
        return mid_bg[(o,o)]/(nb*b*b) if b>0 and nb>0 else 1.0
    ss_mid_m = (ss_mid('qok') + ss_mid('ok') + ss_mid('ch')) / 3
    adj = sum(1 for i in range(tb) if all_w[i]==all_w[i+1]) / max(1, tb)
    return {'am_ll': round(am_ll, 4), 'y_lf': round(y_lf, 4),
            'ss_mean': round(ss_m, 4), 'ss_mid': round(ss_mid_m, 4),
            'adj_rate': round(adj, 5)}

VMS   = {'am_ll': 6.811, 'ss_mean': 1.465, 'adj_rate': 0.009}
SEED  = 185000

print("Loading corpus...")
latin_words = load_latin(LATIN_CORPUS)
print(f"  {len(latin_words)} words")

COPY_PROBS   = [0.70, 0.72, 0.74, 0.76, 0.78, 0.80]
MODIFY_PROBS = [0.7, 0.8, 0.9]

all_results = []
print(f"\nRunning {len(COPY_PROBS)*len(MODIFY_PROBS)} combinations × {N_SIMS} sims")
print(f"VMS: ss={VMS['ss_mean']}, adj={VMS['adj_rate']}, am_ll={VMS['am_ll']}")

for cp in COPY_PROBS:
    for mp in MODIFY_PROBS:
        sims = []
        for i in range(N_SIMS):
            rng = random.Random(SEED + int(cp*10000) + int(mp*100) + i)
            sents = make_sents(latin_words, rng)
            m = metrics(run_sim(sents, rng, cp, mp))
            if m: sims.append(m)
        if not sims: continue
        def mc(k): v=sorted(x[k] for x in sims); m=sum(v)/len(v); return m,v[int(.05*len(v))],v[int(.95*len(v))]
        am,_,_  = mc('am_ll')
        y,_,_   = mc('y_lf')
        ss,_,_  = mc('ss_mean')
        ssm,_,_ = mc('ss_mid')
        adj,_,_ = mc('adj_rate')
        vms_viable = adj <= VMS['adj_rate'] and ss >= 1.2 and am >= 5.0
        flag = " ← VMS-viable" if vms_viable else ""
        dist_to_vms = abs(ss - VMS['ss_mean'])
        rec = {'cp': cp, 'mp': mp, 'am_ll': am, 'y_lf': y, 'ss_mean': ss, 'ss_mid': ssm,
               'adj_rate': adj, 'vms_viable': vms_viable, 'dist_to_vms_ss': round(dist_to_vms, 4),
               'pct_vms_ss': round(ss/VMS['ss_mean']*100, 1), 'pct_vms_am': round(am/VMS['am_ll']*100, 1)}
        all_results.append(rec)
        print(f"cp={cp:.2f} mp={mp:.1f}: am_ll={am:.3f} ({rec['pct_vms_am']:.1f}%) "
              f"ss={ss:.3f} ({rec['pct_vms_ss']:.1f}%) adj={adj:.5f}{flag}")

print("\n" + "="*70)
# Find closest to VMS ss_mean at VMS adj_rate
vms_viable = [r for r in all_results if r['vms_viable']]
if vms_viable:
    best = min(vms_viable, key=lambda x: x['dist_to_vms_ss'])
    print(f"Closest to VMS ss_mean among VMS-viable: cp={best['cp']:.2f} mp={best['mp']:.1f}")
    print(f"  ss_mean={best['ss_mean']:.4f} ({best['pct_vms_ss']:.1f}% VMS)")
    print(f"  am_ll  ={best['am_ll']:.4f}  ({best['pct_vms_am']:.1f}% VMS)")
    print(f"  adj    ={best['adj_rate']:.5f} (VMS: {VMS['adj_rate']})")

# Crossover table at mp=0.8
print(f"\nCrossover at mp=0.8 (ss_mean vs VMS target {VMS['ss_mean']}):")
for r in sorted([x for x in all_results if x['mp']==0.8], key=lambda x: x['cp']):
    marker = " ← crossover region" if abs(r['ss_mean'] - VMS['ss_mean']) < 0.05 else ""
    print(f"  cp={r['cp']:.2f}: ss={r['ss_mean']:.4f} ({r['pct_vms_ss']:.1f}%), "
          f"am={r['am_ll']:.4f} ({r['pct_vms_am']:.1f}%), adj={r['adj_rate']:.5f}{marker}")

out = os.path.join(OUT_DIR, 'fine_grid_results.json')
with open(out, 'w') as f:
    json.dump({'results': all_results, 'vms': VMS, 'n_sims': N_SIMS}, f, indent=2)
print(f"\nSaved: {out}")
