"""
exp_187: Italian Source Text (Dante) in Position-Aware Hybrid Architecture (H351)

Motivation:
  exp_186 established the am_ll ceiling at 97.1% VMS for the Cicero Latin source
  (CF_rate=34.2%, architecture-limited). H351 asks: does Italian (Dante Divina Commedia)
  produce a higher am_ll, given Italian's different morphological structure?

  Algebraic prediction: Italian narrow CF_rate ≈ 5.5% (vs Latin 34-37%),
  giving am_ll ≈ 2.6× (well below Latin 5.57-6.61×, far below VMS 6.811×).
  Italian is an analytic language — morphological clause-boundary signals are weaker.

Experimental design:
  Use the position-aware hybrid architecture (cp=0.76, mp=0.9 — best from exp_185)
  with Italian Dante corpus. Two Italian CF patterns tested:
  - Narrow: accented verb endings (à, ò, ì, ù, ono, ano, endo, ando)
  - Broad: + past participles/infinitives (ato, uto, ito, are, ere, ire, ete)
  Also run a "broad vowel" pattern (words ending in vowels — linguistically unmotivated but tests ceiling).
  50 sims per pattern, p_detect=0.90, seeds 187000+.

Pre-registration:
  Expected: narrow CF_rate ≈ 5.5% → am_ll ≈ 2.5-3.0× (well below VMS).
  Expected: broad CF_rate ≈ 7% → am_ll slightly higher but still far below VMS.
  Expected: broad-vowel CF_rate ≈ 70% → am_ll ≈ 6.5-7× (but linguistically unmotivated).
  Italian does NOT produce better am_ll than Latin for any linguistically motivated CF pattern.

Seed: 187000.
"""
from pathlib import Path as _RepositoryPath

import os, re, random, json
from collections import Counter, deque

REPO_DIR      = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
ITALIAN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/italian/dante_divina_commedia.txt')
OUT_DIR       = os.path.join(REPO_DIR, 'experiments/exp_187_italian_source/data')
os.makedirs(OUT_DIR, exist_ok=True)

N_SIMS       = 50
TARGET_LINES = 2447
WINDOW       = 20
CP, MP       = 0.76, 0.9
P_DETECT     = 0.90

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
LL_ONSETS  = {'d': 0.40, 'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}

# Italian CI patterns (matching Latin LF calibration approximately)
ITALIAN_CI_Y = re.compile(r'^[Qq]u[aeiou]|^[Ee]t\b|^[Aa]nd\b|^[Mm]a\b|^[Ee]\b', re.I)
ITALIAN_CI_S = re.compile(r'^[Ss][aeiouAEIOU]', re.I)
ITALIAN_CI_T = re.compile(r'^[Tt][aeiouAEIOU]', re.I)

# Italian clause-final patterns (three variants)
CF_PATTERNS = {
    'narrow':      re.compile(r'(à|ò|ì|ù|ono|ano|endo|ando|ete|aste|iste)$', re.UNICODE),
    'broad':       re.compile(r'(à|ò|ì|ù|ono|ano|endo|ando|ato|uto|ito|are|ere|ire|ete)$', re.UNICODE),
    'broad_vowel': re.compile(r'[aeiouàáèéìíòóùú]$', re.UNICODE),
}

def make_word(onset, suffix, rng):
    return onset + rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei']) + suffix

def random_eva_word(rng):
    o = rng.choices(list(ONSET_WEIGHTS.keys()), weights=list(ONSET_WEIGHTS.values()))[0]
    s = rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0]
    return make_word(o, s, rng)

def cipher_lf(w, rng, p):
    wl = w.lower()
    if ITALIAN_CI_Y.match(wl) and rng.random() < p:
        return make_word('y', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    elif ITALIAN_CI_T.match(wl) and rng.random() < p:
        return make_word('t', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    elif ITALIAN_CI_S.match(wl) and rng.random() < p:
        return make_word('s', rng.choices(list(SUFFIX_WEIGHTS.keys()), weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
    return random_eva_word(rng)

def cipher_ll(w, rng, p, cf_pattern):
    if cf_pattern.search(w.lower()) and rng.random() < p:
        onset = rng.choices(list(LL_ONSETS.keys()), weights=list(LL_ONSETS.values()))[0]
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

def load_italian(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    words = []
    for p in re.split(r'\n\s*\n', text):
        ws = re.findall(r"[a-zA-ZàáâãäåæçèéêëìíîïòóôõöùúûüýÀÈÉÌÒÓÙ]+", p)
        if not ws: continue
        if sum(1 for w in ws if w.lower() in ENGLISH_SW)/len(ws) < 0.08:
            words.extend(ws)
    return words

def run_sim(italian_words, rng, cp, mp, p, cf_pattern):
    w = list(italian_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0 and len(chunk) > 1:
                ew = cipher_lf(word, rng, p)
            elif i == len(chunk)-1 or len(chunk)==1:
                ew = cipher_ll(word, rng, p, cf_pattern)
            else:
                if buf and rng.random() < cp:
                    ew = timm_modify(rng.choice(list(buf)), rng) if rng.random() < mp else rng.choice(list(buf))
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

print("Loading Italian corpus (Dante Divina Commedia)...")
italian = load_italian(ITALIAN_CORPUS)
print(f"  {len(italian)} filtered words")

# Measure CF_rate for each pattern
for name, pattern in CF_PATTERNS.items():
    rate = sum(1 for w in italian if pattern.search(w.lower())) / len(italian)
    print(f"  {name} CF_rate: {rate:.3f}")

print(f"\nFixed: cp={CP}, mp={MP}, p_detect={P_DETECT}")
print(f"Latin comparison (exp_186): CF=0.342, am_ll=6.42 (94.3% VMS) at p=0.90")
print()

SEED = 187000
all_results = []

for pattern_name, cf_pattern in CF_PATTERNS.items():
    cf_rate = sum(1 for w in italian if cf_pattern.search(w.lower())) / len(italian)
    sims = []
    for i in range(N_SIMS):
        rng = random.Random(SEED + hash(pattern_name) % 1000 + i)
        m = compute_metrics(run_sim(italian, rng, CP, MP, P_DETECT, cf_pattern))
        if m: sims.append(m)
    if not sims: continue
    def mc(k): v=sorted(x[k] for x in sims); m=sum(v)/len(v); return m,v[int(.05*len(v))],v[int(.95*len(v))]
    am,_,_ = mc('am_ll'); y,_,_ = mc('y_lf'); ss,_,_ = mc('ss_mean'); adj,_,_ = mc('adj_rate')
    rec = {'pattern':pattern_name,'cf_rate':round(cf_rate,4),'am_ll':round(am,4),'y_lf':round(y,4),
           'ss_mean':round(ss,4),'adj_rate':round(adj,5),
           'pct_vms_am':round(am/VMS['am_ll']*100,1), 'pct_vms_ss':round(ss/VMS['ss_mean']*100,1)}
    all_results.append(rec)
    print(f"{pattern_name} (CF={cf_rate:.3f}): am_ll={am:.4f} ({rec['pct_vms_am']:.1f}%) "
          f"y_lf={y:.4f} ss={ss:.4f} adj={adj:.5f}")

print(f"\nVMS targets: am_ll=6.811 (100%), ss=1.465, adj=0.009, y_lf=3.506")

out = os.path.join(OUT_DIR, 'italian_results.json')
with open(out, 'w') as f: json.dump({'results': all_results, 'vms': VMS, 'cp': CP, 'mp': MP, 'p_detect': P_DETECT}, f, indent=2)
print(f"\nSaved: {out}")
