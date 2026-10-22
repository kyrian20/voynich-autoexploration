"""
exp_186: Detection Probability Sweep — Can Higher p_detect Close the am_ll Gap? (H352)

Motivation:
  exp_185 established the best joint approximation at cp=0.76, mp=0.9:
  - ss_mean=1.454 (99.2% VMS), adj=0.00425 (below VMS), am_ll=6.460 (94.8% VMS)
  - Primary residual gap: am_ll 5.2% below VMS.

  The LL cipher table detects clause-final Latin words at p_detect=0.90.
  At higher p_detect, more LL words get mapped to -am, raising am_ll.

  Hypothesis: at p_detect=1.00 (ALL clause-final words → -am), am_ll increases to ~6.6-6.8×.
  The am_ll gap (5.2% at p_detect=0.90) may be closable by maximizing LL detection.

Experimental design:
  Fix cp=0.76, mp=0.9 (best joint approximation from exp_185).
  Vary p_detect for LL table: {0.90 (baseline), 0.95, 1.00}.
  Also vary LF p_detect: {0.90 (baseline), 0.95, 1.00} (to see y_lf gap sensitivity).
  6 combinations (3 LL × 2 LF combinations) × 50 sims = 300 runs.

Target-awareness note: increasing p_detect makes the cipher MORE target-aware (more LL words
are forced to map to -am regardless of random variation). At p_detect=1.00 for all CF words,
the mapping is deterministic and fully target-calibrated. The result would be conditional on
this maximally target-aware design.

Pre-registration:
  Expected at p_detect=1.00 LL, p_detect=1.00 LF: am_ll ≈ 6.7-7.0× (approaching VMS 6.811)
  y_lf at p_detect=1.00 LF ≈ 2.6-2.8× (still below VMS 3.506)
  ss_mean and adj_rate: unaffected by p_detect changes (copy component unchanged)

Seed base: 186000.
"""
from pathlib import Path as _RepositoryPath

import os, re, random, json
from collections import Counter, deque

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
OUT_DIR      = os.path.join(REPO_DIR, 'experiments/exp_186_pdetect_sweep/data')
os.makedirs(OUT_DIR, exist_ok=True)

N_SIMS       = 50
TARGET_LINES = 2447
WINDOW       = 20
CP, MP       = 0.76, 0.9   # Fixed at exp_185 best combination

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

LATIN_CF   = re.compile(r'(am|um|us|em|is|ae|orum|bus|unt|it|ant|at)$', re.I)
LATIN_CI_S = re.compile(r'^[Ss][aeiouAEIOU]', re.I)
LATIN_CI_T = re.compile(r'^[Tt][aeiouAEIOU]', re.I)
LATIN_CI_Y = re.compile(r'^[Qq][uU]|^[Nn]o|^[Ee]t\b|^[Aa]t\b', re.I)
LL_ONSETS  = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}

def cipher_lf(w, rng, p):
    wl = w.lower()
    if LATIN_CI_Y.match(wl) and rng.random() < p:
        return make_word('y', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    elif LATIN_CI_T.match(wl) and rng.random() < p:
        return make_word('t', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    elif LATIN_CI_S.match(wl) and rng.random() < p:
        return make_word('s', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    return random_eva_word(rng)

def cipher_ll(w, rng, p):
    if LATIN_CF.search(w.lower()) and rng.random() < p:
        onset = rng.choices(list(LL_ONSETS.keys()), weights=list(LL_ONSETS.values()))[0]
        return make_word(onset, 'am', rng)
    return random_eva_word(rng)

def cipher_mid(rng):
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

def run_sim(latin_words, rng, cp, mp, p_ll, p_lf):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0 and len(chunk) > 1:
                ew = cipher_lf(word, rng, p_lf)
            elif i == len(chunk)-1 or len(chunk)==1:
                ew = cipher_ll(word, rng, p_ll)
            else:
                if buf and rng.random() < cp:
                    ew = timm_modify(rng.choice(list(buf)), rng) if rng.random() < mp else rng.choice(list(buf))
                else:
                    ew = cipher_mid(rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def get_onset(w):
    for p in ['qok','qo','cth','ch','sh','ok','d','s','y','k','t','l','r']:
        if w.startswith(p): return p
    return 'other'

def compute_metrics(lines):
    aw = [w for l in lines for w in l]; n = len(aw)
    if n < 100: return None
    oc = Counter(get_onset(w) for w in aw)
    lf = [l[0] for l in lines if l]; ll = [l[-1] for l in lines if len(l)>1]
    am_r = sum(1 for w in aw if w.endswith('am'))/n
    am_ll = (sum(1 for w in ll if w.endswith('am'))/len(ll))/am_r if am_r and ll else 1.0
    y_r = oc['y']/n
    y_lf = (sum(1 for w in lf if get_onset(w)=='y')/len(lf))/y_r if y_r and lf else 1.0
    tb = n-1
    bg = Counter((get_onset(aw[i]),get_onset(aw[i+1])) for i in range(tb))
    def ss(o): b=oc[o]/n; return bg[(o,o)]/(tb*b*b) if b>0 and tb>0 else 1.0
    ss_m = (ss('qok')+ss('ok')+ss('ch'))/3
    adj = sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)
    return {'am_ll': round(am_ll,4),'y_lf': round(y_lf,4),'ss_mean': round(ss_m,4),'adj_rate': round(adj,5)}

VMS = {'am_ll':6.811,'ss_mean':1.465,'adj_rate':0.009,'y_lf':3.506}

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} words | cp={CP}, mp={MP} (fixed from exp_185)")
print(f"  Sweeping: p_ll ∈ {{0.90, 0.95, 1.00}} × p_lf ∈ {{0.90, 1.00}}")
print()

combos = [(p_ll, p_lf) for p_ll in [0.90, 0.95, 1.00] for p_lf in [0.90, 1.00]]
all_results = []
SEED = 186000

for p_ll, p_lf in combos:
    sims = []
    for i in range(N_SIMS):
        rng = random.Random(SEED + int(p_ll*1000) + int(p_lf*100) + i)
        m = compute_metrics(run_sim(latin, rng, CP, MP, p_ll, p_lf))
        if m: sims.append(m)
    if not sims: continue
    def mc(k): v=sorted(x[k] for x in sims); m=sum(v)/len(v); return m,v[int(.05*len(v))],v[int(.95*len(v))]
    am,_,_ = mc('am_ll'); y,_,_ = mc('y_lf'); ss,_,_ = mc('ss_mean'); adj,_,_ = mc('adj_rate')
    rec = {'p_ll':p_ll,'p_lf':p_lf,'am_ll':am,'y_lf':y,'ss_mean':ss,'adj_rate':adj,
           'pct_vms_am':round(am/VMS['am_ll']*100,1), 'pct_vms_y':round(y/VMS['y_lf']*100,1),
           'pct_vms_ss':round(ss/VMS['ss_mean']*100,1)}
    all_results.append(rec)
    print(f"p_ll={p_ll:.2f} p_lf={p_lf:.2f}: am_ll={am:.4f} ({rec['pct_vms_am']:.1f}%) "
          f"y_lf={y:.4f} ({rec['pct_vms_y']:.1f}%) ss={ss:.4f} adj={adj:.5f}")

print("\n" + "="*70)
print(f"Baseline (exp_185): am_ll=6.460 (94.8%), y_lf=~2.4 (68%), ss=1.454 (99.2%), adj=0.00425")
print(f"VMS targets:        am_ll=6.811 (100%),  y_lf=3.506,        ss=1.465,        adj=0.009")
print()

# Gain per unit p_detect increase
print("am_ll gain from p_detect increase:")
base_am = next((r['am_ll'] for r in all_results if r['p_ll']==0.90 and r['p_lf']==0.90), None)
for r in all_results:
    if r['p_lf'] == 0.90 and base_am:
        delta = r['am_ll'] - base_am
        print(f"  p_ll={r['p_ll']:.2f}: am_ll={r['am_ll']:.4f} ({r['pct_vms_am']:.1f}% VMS), Δ={delta:+.4f}")

out = os.path.join(OUT_DIR, 'pdetect_results.json')
with open(out, 'w') as f: json.dump({'results': all_results, 'vms': VMS, 'cp': CP, 'mp': MP}, f, indent=2)
print(f"\nSaved: {out}")
