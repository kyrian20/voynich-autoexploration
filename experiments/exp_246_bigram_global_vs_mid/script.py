"""
exp_246: Verify exp_245 Diagnostic — Global vs MID-Only Bigram Enrichments in Full sim

Question: Does the full exp_236 B-dialect architecture (19/19 PASS) over-produce
self-succession in MID-only context and under-produce it in global context?
This directly tests the exp_245 analytical prediction.

Design:
  Run exp_236 architecture (N=15 for speed) and compute:
  - Global E(X→Y) for key pairs (same as exp_241)
  - MID-only E(X→Y) for same pairs (new)
  - VMS E_global and E_mid for same pairs (for comparison)

  Key pairs:
  - Self-succession: ot→ot, l→l, ok→ok, y→y, d→d, qok→qok, o→o, ol→ol
  - Cross-onset: qok→ch (known Markov), sh→qok (architecture gap), s→sh (artifact)
  - Compare: if E_mid_sim > VMS_E_mid → sim over-produces in MID
             if E_global_sim < VMS_E_global → measurement artifact confirmed

  Prediction from exp_245:
  - ot→ot: E_mid_sim ≈ 2.2, VMS E_mid = 1.887 → SIM OVER-PRODUCES in MID
  - E_global_sim(ot→ot) ≈ 1.88, matching VMS E_global = 1.886
  - This would confirm exp_241 MISSED was an artifact
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_TRIALS = 15
TARGET_LINES = 2447
WINDOW   = 20
SEED     = 246000

# exp_236 frozen parameters
P_BLIND   = 0.115
P_LF      = 1.0
CP        = 0.55
MP        = 0.90
P_QOKCH   = 0.12
P_STUTTER = 0.006
R_LF      = 0.12
R_MID     = 0.25
MU_LEN    = 8.4

EVA_CHARS = list('acdehiklmnoqrsty')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0

def get_edy_suffix_len(w):
    if w.endswith('eedy'): return 4
    if w.endswith('edy'):  return 3
    return 0

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_vms_b():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}
    b_lines = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            if folio_dialect.get(fb, 'unknown') != 'B': continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: b_lines.append(words)
    return b_lines

def make_suppressed_suffix(suffix_global, r_am):
    am_weight = suffix_global.get('am', 0.0)
    new_am = am_weight * r_am
    delta = am_weight - new_am
    non_am_total = 1.0 - am_weight
    suppressed = {}
    for suf, w in suffix_global.items():
        if suf == 'am':
            suppressed[suf] = new_am
        else:
            suppressed[suf] = w + (w / non_am_total) * delta if non_am_total > 0 else w
    return suppressed

def build_ll_onsets_fixed(onset_ll_vms, d_boost_weight):
    remaining_weight = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o != 'd'}
    base_total = sum(base.values())
    normalized = {o: v/base_total * remaining_weight for o, v in base.items()} if base_total > 0 else {}
    normalized['d'] = d_boost_weight
    return normalized

def compute_d_boost_fixed(d_global, d_ll_target, d_ll_non_blind, p_blind):
    return d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind) / p_blind

def make_word_sim(onset, suffix, rng):
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset + rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei']) + suffix
    return onset + suffix

def random_eva_word(ow, sw, rng):
    o = rng.choices(list(ow.keys()), weights=list(ow.values()))[0]
    s = rng.choices(list(sw.keys()), weights=list(sw.values()))[0]
    return make_word_sim(o, s, rng)

def cipher_ll(onset_weights_mid, suffix_global, ll_onsets, onset_ll_vms, rng):
    if rng.random() < P_BLIND:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return onset + 'am'
    onset  = rng.choices(list(onset_ll_vms.keys()), weights=list(onset_ll_vms.values()))[0]
    suffix = rng.choices(list(suffix_global.keys()), weights=list(suffix_global.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_lf(onset_weights_mid, suffix_lf, onset_lf_vms, rng):
    if rng.random() < P_LF:
        onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
        suffix = rng.choices(list(suffix_lf.keys()), weights=list(suffix_lf.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_weights_mid, suffix_lf, rng)

def timm_modify(word, onset_weights_mid, suffix_mid, rng):
    if not word: return word
    onset_len = get_onset_len(word); edy_len = get_edy_suffix_len(word)
    mod_start = onset_len; mod_end = len(word) - edy_len
    if mod_start >= mod_end:
        return random_eva_word(onset_weights_mid, suffix_mid, rng)
    op = rng.choice(['replace', 'insert', 'delete'])
    if op == 'replace':
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(mod_start, mod_end)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:
        if mod_end - mod_start <= 1:
            return word[:mod_start] + rng.choice(EVA_CHARS) + word[mod_start+1:]
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + word[pos+1:]

def draw_buf(buf, prev_onset, rng):
    buf_list = list(buf)
    if prev_onset == 'qok' and rng.random() < P_QOKCH:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words: return rng.choice(ch_words)
    return rng.choice(buf_list)

def run_sim(latin_words, onset_weights_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(MU_LEN, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf(onset_weights_mid, suffix_lf_sup, onset_lf_vms, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll(onset_weights_mid, suffix_global, ll_onsets, onset_ll_vms, rng)
            else:
                if prev_word is not None and P_STUTTER > 0 and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf(buf, prev_onset, rng)
                    ew = timm_modify(src, onset_weights_mid, suffix_mid_sup, rng) if rng.random() < MP else src
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def compute_bigram_enrichments(lines):
    """Compute both global and MID-only bigram enrichments."""
    all_words = [w for l in lines for w in l]
    mid_words = [w for l in lines for w in l[1:-1] if len(l) > 2]
    n_all = len(all_words); n_mid = len(mid_words)

    oc_all = Counter(get_onset(w) for w in all_words)
    oc_mid = Counter(get_onset(w) for w in mid_words)
    rates_all = {o: c/n_all for o, c in oc_all.items()}
    rates_mid = {o: c/n_mid for o, c in oc_mid.items()}

    # Global bigrams
    global_bg = Counter()
    global_n = 0
    for line in lines:
        n = len(line)
        for i in range(n-1):
            global_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1
            global_n += 1

    # MID-only bigrams
    mid_bg = Counter()
    mid_n = 0
    for line in lines:
        n = len(line)
        if n < 4:
            continue
        for i in range(1, n-2):
            mid_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1
            mid_n += 1

    def E_global(x, y):
        pxy = global_bg.get((x,y), 0)/global_n if global_n>0 else 0
        px = rates_all.get(x,0); py = rates_all.get(y,0)
        return pxy/(px*py) if px*py>0 else 0

    def E_mid(x, y):
        pxy = mid_bg.get((x,y), 0)/mid_n if mid_n>0 else 0
        px = rates_mid.get(x,0); py = rates_mid.get(y,0)
        return pxy/(px*py) if px*py>0 else 0

    return E_global, E_mid, global_n, mid_n

ENGLISH_SW = {'the','and','of','to','a','in','that','is','was','he','it','for','on','are',
              'as','with','his','they','at','be','this','have','from','or','had','by','not',
              'but','what','all','were','we'}
def load_latin(path):
    with open(path, encoding='utf-8', errors='replace') as f: text = f.read()
    words = []
    for p in re.split(r'\n\s*\n', text):
        ws = re.findall(r'\b[a-zA-Z]+\b', p)
        if not ws: continue
        if sum(1 for w in ws if w.lower() in ENGLISH_SW)/len(ws) < 0.08: words.extend(ws)
    return words

# ─── Setup ────────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect...")
b_lines = parse_vms_b()
all_vms = [w for l in b_lines for w in l]
mid_vms = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
n_vms = len(all_vms); n_vms_mid = len(mid_vms)

oc_vms_all = Counter(get_onset(w) for w in all_vms)
oc_vms_mid = Counter(get_onset(w) for w in mid_vms)
vms_rates_all = {o: c/n_vms for o, c in oc_vms_all.items()}
vms_rates_mid = {o: c/n_vms_mid for o, c in oc_vms_mid.items()}

vms_global_bg = Counter()
vms_global_n = 0
for line in b_lines:
    n = len(line)
    for i in range(n-1):
        vms_global_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1
        vms_global_n += 1

vms_mid_bg = Counter()
vms_mid_n = 0
for line in b_lines:
    n = len(line)
    if n < 4: continue
    for i in range(1, n-2):
        vms_mid_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1
        vms_mid_n += 1

def vms_E_global(x, y):
    pxy = vms_global_bg.get((x,y), 0)/vms_global_n if vms_global_n>0 else 0
    px = vms_rates_all.get(x,0); py = vms_rates_all.get(y,0)
    return pxy/(px*py) if px*py>0 else 0

def vms_E_mid(x, y):
    pxy = vms_mid_bg.get((x,y), 0)/vms_mid_n if vms_mid_n>0 else 0
    px = vms_rates_mid.get(x,0); py = vms_rates_mid.get(y,0)
    return pxy/(px*py) if px*py>0 else 0

print(f"  VMS: {len(b_lines)} lines, {n_vms} words ({n_vms_mid} MID, {vms_global_n} global pairs, {vms_mid_n} MID pairs)")

# Setup distributions (exp_236 parameters)
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']
suf_ctr = Counter()
for w in all_vms:
    matched = False
    for suf in SUFFIX_PATTERNS:
        if w.endswith(suf): suf_ctr[suf] += 1; matched = True; break
    if not matched: suf_ctr['other'] += 1
suffix_global = {suf: c/n_vms for suf, c in suf_ctr.items()}

lf_vms = [l[0] for l in b_lines if l]
ll_vms = [l[-1] for l in b_lines if len(l)>1]
oc_lf = Counter(get_onset(w) for w in lf_vms)
oc_ll = Counter(get_onset(w) for w in ll_vms)
onset_lf_vms = {o: c/len(lf_vms) for o, c in oc_lf.items()}
onset_ll_vms = {o: c/len(ll_vms) for o, c in oc_ll.items()}
onset_weights_mid = dict(vms_rates_mid)

d_global = vms_rates_all.get('d', 0)
d_ll_target = (oc_ll.get('d',0)/len(ll_vms)) / d_global if d_global else 0
vms_ll_d_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0
d_boost = compute_d_boost_fixed(d_global, d_ll_target, vms_ll_d_enr, P_BLIND)
ll_onsets = build_ll_onsets_fixed(onset_ll_vms, d_boost)
suffix_lf_sup  = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} words")

# ─── Run simulation ────────────────────────────────────────────────────────────

KEY_PAIRS = [
    ('ot', 'ot', 'ot→ot (self)'),
    ('l', 'l', 'l→l (self)'),
    ('ok', 'ok', 'ok→ok (self)'),
    ('y', 'y', 'y→y (self)'),
    ('d', 'd', 'd→d (self)'),
    ('qok', 'qok', 'qok→qok (self)'),
    ('ol', 'ol', 'ol→ol (self)'),
    ('o', 'o', 'o→o (self)'),
    ('ch', 'ch', 'ch→ch (self)'),
    ('sh', 'sh', 'sh→sh (self)'),
    ('qok', 'ch', 'qok→ch (Markov)'),
    ('sh', 'qok', 'sh→qok (gap)'),
    ('s', 'sh', 's→sh (artifact)'),
]

print(f"\n{'='*90}")
print(f"RUNNING {N_TRIALS} SIMULATIONS — GLOBAL vs MID-ONLY BIGRAM ENRICHMENTS")
print(f"{'='*90}")

all_E_global = {(x,y): [] for x,y,_ in KEY_PAIRS}
all_E_mid = {(x,y): [] for x,y,_ in KEY_PAIRS}

for trial in range(N_TRIALS):
    rng_t = random.Random(SEED + trial * 100)
    lines = run_sim(latin, onset_weights_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf_vms, onset_ll_vms, rng_t)
    E_g_fn, E_m_fn, gn, mn = compute_bigram_enrichments(lines)
    for x, y, _ in KEY_PAIRS:
        all_E_global[(x,y)].append(E_g_fn(x, y))
        all_E_mid[(x,y)].append(E_m_fn(x, y))
    if (trial+1) % 5 == 0:
        print(f"  Trial {trial+1}/{N_TRIALS} done")

print(f"\n{'='*90}")
print("RESULTS: VMS vs SIM (GLOBAL AND MID-ONLY ENRICHMENTS)")
print(f"{'='*90}")
print(f"\n  {'Pair':<14} {'VMS_Eg':>8} {'Sim_Eg':>8} {'VMS_Em':>8} {'Sim_Em':>8}  "
      f"{'Eg_verdict':>15}  {'Em_verdict':>15}")
print(f"  {'-'*85}")

for x, y, label in KEY_PAIRS:
    vEg = vms_E_global(x, y)
    vEm = vms_E_mid(x, y)
    sEg = sum(all_E_global[(x,y)])/len(all_E_global[(x,y)])
    sEm = sum(all_E_mid[(x,y)])/len(all_E_mid[(x,y)])
    Eg_vert = 'SIM>VMS' if sEg > vEg * 1.1 else ('SIM<VMS' if sEg < vEg * 0.9 else 'match')
    Em_vert = 'SIM>VMS' if sEm > vEm * 1.1 else ('SIM<VMS' if sEm < vEm * 0.9 else 'match')
    cnt_g = vms_global_bg.get((x,y), 0)
    cnt_m = vms_mid_bg.get((x,y), 0)
    print(f"  {x}→{y:<8} {vEg:>8.3f} {sEg:>8.3f} {vEm:>8.3f} {sEm:>8.3f}  "
          f"{Eg_vert:>15}  {Em_vert:>15}  (N_g={cnt_g},N_m={cnt_m})")

print(f"\n  {'='*90}")
print(f"  Prediction from exp_245: ot→ot Sim_Em >> VMS_Em ≈ 1.887")
print(f"  If confirmed: exp_241 MISSED was a global bigram measurement artifact")
print(f"  If not confirmed: exp_245 diagnostic was wrong (simplified sim)")

print("\nDone.")
