"""
exp_239: H439 — A-Dialect y→y Markov Succession Mechanism

Question: Does adding a y→y Markov bias (analogous to qok→ch in B-dialect) fix the
ss_y failure in A-dialect (76.5% FAIL, target 1.5874) without regressing the 18 passing
metrics from exp_238?

Design:
  Same architecture as exp_238 (18/19 A-dialect PASS), single addition:
  - p_y_y parameter in draw_from_buffer: when prev_onset='y', boost probability
    of drawing y-onset word from buffer.

  Pre-sweep (N=8 inline, prior session):
    p_y_y=0.00: ss_y=1.336 (84.1%)
    p_y_y=0.05: ss_y=1.493 (94.0%) PASS
    p_y_y=0.10: ss_y=1.685 (106.1%) PASS ← centered in [1.270, 1.905]
    p_y_y=0.15: ss_y=1.881 (118.5%) PASS
    p_y_y=0.20+: FAIL (>120%)

  Sweep (N=5): p_y_y ∈ {0.04, 0.06, 0.08, 0.10, 0.12, 0.15}
  Full run (N=30): best p_y_y by ss_y closest to target center (1.587)

Exp_238 parameters (FIXED):
  p_blind=0.0505, d_boost=24.30%, r_lf=0.266, r_mid=0.87, p_stutter=0.002
  mu_len=5.64 (A-dialect line length)
  cp=0.55, mp=0.90, p_qokch=0.12, p_lf=1.0 (TRANSFERRED)

H439 predicts: ss_y 76.5% → PASS, all 18 other metrics remain PASS → 19/19.
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SWEEP  = 5
N_FULL   = 30
WINDOW   = 20
SEED     = 239000
PASS_TOL = 0.20

# ─── Exp_238 fixed parameters ──────────────────────────────────────────────────
P_BLIND_A   = 0.0505
D_BOOST_A   = 0.2430      # 24.30% (analytical)
R_LF_A      = 0.266
R_MID_A     = 0.87
P_STUTTER   = 0.002       # A-dialect (smaller vocabulary → less stutter)
MU_LEN_A    = 5.64        # A-dialect average words/line
SIGMA_LEN   = 2.5         # kept from exp_236
CP          = 0.55
MP          = 0.90
P_QOKCH     = 0.12
P_LF        = 1.0

# p_y_y sweep values
P_Y_Y_VALUES = [0.04, 0.06, 0.08, 0.10, 0.12, 0.15]

EVA_CHARS = list('acdehiklmnoqrsty')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

METRIC_LABELS = [
    'am_ll', 'd_ll', 'y_lf', 'ss_mean', 'adj_rate',
    'qok_lf', 'd_lf', 's_lf', 'ch_ll', 'ok_ll', 'qok_ll',
    'ss_d', 'ss_y', 'am_lf_enr', 'am_mid_enr',
    'edy_rate', 'word_len_mean', 'qok_ch', 'global_am_rate',
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

def parse_vms_a_dialect():
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
    a_lines = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            if folio_dialect.get(fb, 'unknown') != 'A': continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: a_lines.append(words)
    return a_lines

def compute_vms_targets(dialect_lines):
    all_words = [w for l in dialect_lines for w in l]
    lf_words  = [l[0]  for l in dialect_lines if l]
    ll_words  = [l[-1] for l in dialect_lines if len(l) > 1]
    mid_words = [w for l in dialect_lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words); n_mid = max(1, len(mid_words))

    oc_all = Counter(get_onset(w) for w in all_words)
    oc_lf  = Counter(get_onset(w) for w in lf_words)
    oc_ll  = Counter(get_onset(w) for w in ll_words)
    oc_mid = Counter(get_onset(w) for w in mid_words)

    SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']
    suf_ctr = Counter()
    for w in all_words:
        matched = False
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf):
                suf_ctr[suf] += 1; matched = True; break
        if not matched: suf_ctr['other'] += 1
    suffix_global = {suf: cnt/n for suf, cnt in suf_ctr.items()}

    am_r     = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am_r  = sum(1 for w in ll_words  if w.endswith('am')) / len(ll_words)
    lf_am_r  = sum(1 for w in lf_words  if w.endswith('am')) / len(lf_words)
    mid_am_r = sum(1 for w in mid_words if w.endswith('am')) / n_mid

    def enr(onset, ctr_s, n_s, ctr_a, n_a):
        s = ctr_s.get(onset, 0)/n_s if n_s else 0
        g = ctr_a.get(onset, 0)/n_a if n_a else 0
        return s/g if g>0 else 0

    tb = n - 1
    bg = Counter((get_onset(all_words[i]), get_onset(all_words[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o, 0)/n
        return bg.get((o,o),0)/(tb*b*b) if b>0 else 1.0

    return {
        'onset_global': {o: cnt/n for o, cnt in oc_all.items()},
        'onset_lf':     {o: cnt/len(lf_words) for o, cnt in oc_lf.items()},
        'onset_ll':     {o: cnt/len(ll_words)  for o, cnt in oc_ll.items()},
        'onset_mid':    {o: cnt/n_mid for o, cnt in oc_mid.items()},
        'suffix_global': suffix_global,
        'n_lines': len(dialect_lines),
        # Metric targets
        'am_ll':          ll_am_r / am_r if am_r else 0,
        'd_ll':           enr('d', oc_ll, len(ll_words), oc_all, n),
        'y_lf':           enr('y', oc_lf, len(lf_words), oc_all, n),
        'ss_mean':        (ss('qok')+ss('ok')+ss('ch'))/3,
        'adj_rate':       sum(1 for i in range(tb) if all_words[i]==all_words[i+1])/max(1,tb),
        'qok_lf':         enr('qok', oc_lf, len(lf_words), oc_all, n),
        'd_lf':           enr('d',   oc_lf, len(lf_words), oc_all, n),
        's_lf':           enr('s',   oc_lf, len(lf_words), oc_all, n),
        'ch_ll':          enr('ch',  oc_ll, len(ll_words),  oc_all, n),
        'ok_ll':          enr('ok',  oc_ll, len(ll_words),  oc_all, n),
        'qok_ll':         enr('qok', oc_ll, len(ll_words),  oc_all, n),
        'ss_d':           ss('d'),
        'ss_y':           ss('y'),
        'am_lf_enr':      lf_am_r / am_r if am_r else 0,
        'am_mid_enr':     mid_am_r / am_r if am_r else 0,
        'edy_rate':       sum(1 for w in all_words if w.endswith('edy'))/n,
        'word_len_mean':  sum(len(w) for w in all_words)/n,
        'qok_ch':         bg.get(('qok','ch'),0)/(tb*(oc_all.get('qok',0)/n)*(oc_all.get('ch',0)/n))
                          if oc_all.get('qok',0) and oc_all.get('ch',0) else 0,
        'global_am_rate': am_r,
        # Derived for calibration
        'am_r': am_r, 'll_am_rate': ll_am_r, 'lf_am_rate': lf_am_r, 'mid_am_rate': mid_am_r,
    }

def make_suppressed_suffix(suffix_global, r_am):
    am_w = suffix_global.get('am', 0.0)
    new_am = am_w * r_am
    delta = am_w - new_am
    non_am_total = 1.0 - am_w
    suppressed = {}
    for suf, w in suffix_global.items():
        if suf == 'am':
            suppressed[suf] = new_am
        else:
            suppressed[suf] = w + (w / non_am_total) * delta if non_am_total > 0 else w
    return suppressed

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    remaining = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o != 'd'}
    base_total = sum(base.values())
    norm = {o: v/base_total * remaining for o, v in base.items()} if base_total > 0 else {}
    norm['d'] = d_boost_weight
    return norm

def make_word_sim(onset, suffix, rng):
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
        return onset + connector + suffix
    return onset + suffix

def random_eva_word(onset_w, suffix_w, rng):
    onset  = rng.choices(list(onset_w.keys()),  weights=list(onset_w.values()))[0]
    suffix = rng.choices(list(suffix_w.keys()), weights=list(suffix_w.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_ll(onset_w_mid, suffix_global, ll_onsets, onset_ll_vms, p_blind, rng):
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return onset + 'am'
    onset  = rng.choices(list(onset_ll_vms.keys()), weights=list(onset_ll_vms.values()))[0]
    suffix = rng.choices(list(suffix_global.keys()), weights=list(suffix_global.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_lf(onset_w, suffix_lf, onset_lf_vms, p_lf, rng):
    if rng.random() < p_lf:
        onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
        suffix = rng.choices(list(suffix_lf.keys()), weights=list(suffix_lf.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_w, suffix_lf, rng)

def timm_modify(word, onset_w, suffix_mid, rng):
    if not word: return word
    onset_len = get_onset_len(word); edy_len = get_edy_suffix_len(word)
    mod_start = onset_len; mod_end = len(word) - edy_len
    if mod_start >= mod_end:
        return random_eva_word(onset_w, suffix_mid, rng)
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

def draw_buf(buf, prev_onset, p_qokch, p_y_y, rng):
    """Copy buffer draw with qok→ch and y→y Markov biases."""
    bl = list(buf)
    # qok→ch Markov (TRANSFERRED from B-dialect)
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    # y→y Markov (NEW for A-dialect, H439)
    if prev_onset == 'y' and p_y_y > 0 and rng.random() < p_y_y:
        yw = [w for w in bl if get_onset(w) == 'y']
        if yw: return rng.choice(yw)
    return rng.choice(bl)

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf, onset_ll, p_blind, target_lines, p_y_y, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    while len(lines) < target_lines and pos < len(w) - 2:
        n_words = max(2, min(20, round(rng.gauss(MU_LEN_A, SIGMA_LEN))))
        chunk = w[pos:pos+n_words]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf(onset_mid, suffix_lf_sup, onset_lf, P_LF, rng)
            elif i == len(chunk) - 1:
                ew = cipher_ll(onset_mid, suffix_global, ll_onsets, onset_ll, p_blind, rng)
            else:
                if prev_word is not None and P_STUTTER > 0 and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf(buf, prev_onset, P_QOKCH, p_y_y, rng)
                    if rng.random() < MP:
                        ew = timm_modify(src, onset_mid, suffix_mid_sup, rng)
                    else:
                        ew = src
                else:
                    ew = random_eva_word(onset_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n_words
    return lines[:target_lines]

def compute_metrics(lines):
    aw  = [w for l in lines for w in l]; n = len(aw)
    if n < 100: return None
    lf  = [l[0]  for l in lines if l]
    ll  = [l[-1] for l in lines if len(l) > 1]
    mid = [w for l in lines for w in l[1:-1] if len(l) > 2]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf  = Counter(get_onset(w) for w in lf)
    oc_ll  = Counter(get_onset(w) for w in ll)
    n_lf, n_ll, n_mid = len(lf), len(ll), max(1, len(mid))

    def enr(onset, cs, ns, ca, na):
        s = cs.get(onset, 0)/ns if ns else 0
        g = ca.get(onset, 0)/na if na else 0
        return s/g if g > 0 else 0

    am_r    = sum(1 for w in aw if w.endswith('am')) / n
    ll_am   = sum(1 for w in ll if w.endswith('am')) / n_ll
    lf_am   = sum(1 for w in lf if w.endswith('am')) / n_lf
    mid_am  = sum(1 for w in mid if w.endswith('am')) / n_mid
    am_ll   = ll_am / am_r if am_r else 0

    tb = n - 1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o, 0) / n
        return bg.get((o, o), 0) / (tb * b * b) if b > 0 else 1.0
    ss_mean = (ss('qok') + ss('ok') + ss('ch')) / 3
    adj     = sum(1 for i in range(tb) if aw[i] == aw[i+1]) / max(1, tb)

    d_ll   = enr('d', oc_ll, n_ll, oc_all, n)
    y_lf   = enr('y', oc_lf, n_lf, oc_all, n)
    qok_lf = enr('qok', oc_lf, n_lf, oc_all, n)
    d_lf   = enr('d',   oc_lf, n_lf, oc_all, n)
    s_lf   = enr('s',   oc_lf, n_lf, oc_all, n)
    ch_ll  = enr('ch',  oc_ll, n_ll, oc_all, n)
    ok_ll  = enr('ok',  oc_ll, n_ll, oc_all, n)
    qok_ll = enr('qok', oc_ll, n_ll, oc_all, n)
    ss_d   = ss('d'); ss_y = ss('y')

    am_lf_enr  = lf_am  / am_r if am_r else 0
    am_mid_enr = mid_am / am_r if am_r else 0
    edy_rate   = sum(1 for w in aw if w.endswith('edy')) / n
    word_len   = sum(len(w) for w in aw) / n

    qok_r = oc_all.get('qok', 0)/n; ch_r = oc_all.get('ch', 0)/n
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch, global_am_rate=am_r,
                _ll_am=ll_am*100, _lf_am=lf_am*100, _mid_am=mid_am*100)

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

def agg_mean(ms, k): return sum(x[k] for x in ms) / len(ms)
def pct(s, r): return s/r*100 if r else 0
def pf(s, r, tol=PASS_TOL): return 'P' if r > 0 and abs(s-r)/r <= tol else 'F'

# ─── Parse A-dialect corpus ────────────────────────────────────────────────────

print("Parsing A-dialect VMS corpus...")
a_lines = parse_vms_a_dialect()
print(f"  {len(a_lines)} lines, {sum(len(l) for l in a_lines)} words")

vms = compute_vms_targets(a_lines)
TARGET_LINES = vms['n_lines']

# A-dialect targets (all 19 metrics)
VMS_A = {k: vms[k] for k in METRIC_LABELS}

print(f"\nA-dialect VMS targets:")
for k in METRIC_LABELS:
    print(f"  {k:<18} {VMS_A[k]:.4f}")

# ─── Build fixed parameter set (exp_238) ──────────────────────────────────────

print("\nBuilding exp_238 parameter set...")
onset_lf  = dict(vms['onset_lf'])
onset_ll  = dict(vms['onset_ll'])
onset_mid = dict(vms['onset_mid'])
suffix    = dict(vms['suffix_global'])

ll_onsets    = build_ll_onsets(onset_ll, D_BOOST_A)
suffix_lf_s  = make_suppressed_suffix(suffix, R_LF_A)
suffix_mid_s = make_suppressed_suffix(suffix, R_MID_A)

print(f"  p_blind={P_BLIND_A}, d_boost={D_BOOST_A*100:.2f}%, r_lf={R_LF_A}, r_mid={R_MID_A}")
print(f"  p_stutter={P_STUTTER}, mu_len={MU_LEN_A}, cp={CP}, mp={MP}")
print(f"  p_qokch={P_QOKCH} (transferred), p_lf={P_LF}")

# ─── Load Latin corpus ─────────────────────────────────────────────────────────

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} words")

# ─── p_y_y sweep (N=5 per value) ──────────────────────────────────────────────

print("\n" + "="*80)
print(f"p_y_y SWEEP (N={N_SWEEP} each, scoring on ss_y proximity to target)")
print("="*80)
print(f"\n  {'p_y_y':>6} {'ss_y_sim':>10} {'%tgt':>7} {'P?':>3}  "
      f"{'ss_mean':>8} {'P?':>3}  {'ss_d':>7} {'P?':>3}  {'global_am':>10} {'P?':>3}")

sweep_results = {}
for pyy in P_Y_Y_VALUES:
    mets = []
    for i in range(N_SWEEP):
        seed_val = SEED + 10000 + int(pyy * 1000) * 10 + i
        rng = random.Random(seed_val)
        lines = run_sim(latin, onset_mid, suffix, suffix_lf_s, suffix_mid_s,
                        ll_onsets, onset_lf, onset_ll, P_BLIND_A, TARGET_LINES, pyy, rng)
        m = compute_metrics(lines)
        if m: mets.append(m)
    sweep_results[pyy] = mets
    if not mets: continue
    ss_y_m  = agg_mean(mets, 'ss_y');    ss_m    = agg_mean(mets, 'ss_mean')
    ss_d_m  = agg_mean(mets, 'ss_d');    gam_m   = agg_mean(mets, 'global_am_rate')
    t_ssy   = VMS_A['ss_y'];             t_ssm   = VMS_A['ss_mean']
    t_ssd   = VMS_A['ss_d'];             t_gam   = VMS_A['global_am_rate']
    print(f"  {pyy:>6.2f} {ss_y_m:>10.4f} {pct(ss_y_m,t_ssy):>6.1f}% {pf(ss_y_m,t_ssy):>3}  "
          f"{ss_m:>8.4f} {pf(ss_m,t_ssm):>3}  "
          f"{ss_d_m:>7.4f} {pf(ss_d_m,t_ssd):>3}  "
          f"{gam_m*100:>9.2f}% {pf(gam_m,t_gam):>3}")

# Pick best p_y_y: maximize ss_y PASS rate; among passing, closest to target center
def score_pyy(pyy):
    mets = sweep_results.get(pyy, [])
    if not mets: return (9, float('inf'))
    ss_y_m = agg_mean(mets, 'ss_y')
    t = VMS_A['ss_y']
    passes = 1 if pf(ss_y_m, t) == 'P' else 0
    dist = abs(ss_y_m - t) / t
    return (1 - passes, dist)

best_pyy = min(P_Y_Y_VALUES, key=lambda p: score_pyy(p))
print(f"\n  → Best p_y_y = {best_pyy} (ss_y closest to target center in pass zone)")

# ─── Full run (N=30) with best p_y_y ──────────────────────────────────────────

print()
print("="*80)
print(f"FULL RUN: p_y_y={best_pyy}, N={N_FULL}, A-dialect {TARGET_LINES} lines each")
print("="*80)

full_mets = []
for i in range(N_FULL):
    rng = random.Random(SEED + 200000 + i)
    lines = run_sim(latin, onset_mid, suffix, suffix_lf_s, suffix_mid_s,
                    ll_onsets, onset_lf, onset_ll, P_BLIND_A, TARGET_LINES, best_pyy, rng)
    m = compute_metrics(lines)
    if m: full_mets.append(m)

print(f"\n  {'Metric':<18} {'A-target':>10} {'Sim':>10} {'%':>7} {'P?':>3}")
print(f"  {'-'*55}")
n_pass = 0
for ml in METRIC_LABELS:
    t = VMS_A[ml]; s = agg_mean(full_mets, ml)
    flag = pf(s, t)
    if flag == 'P': n_pass += 1
    marker = ' ← FIXED' if ml == 'ss_y' and flag == 'P' else ''
    marker = ' ← FAIL' if ml == 'ss_y' and flag == 'F' else marker
    print(f"  {ml:<18} {t:>10.4f} {s:>10.4f} {pct(s,t):>6.1f}% {flag:>3}{marker}")

print(f"\n  PASS: {n_pass}/19 with p_y_y={best_pyy}")

print(f"\n  -am diagnostics:")
print(f"    Global am    = {agg_mean(full_mets,'global_am_rate')*100:.2f}%  (VMS A: {VMS_A['global_am_rate']*100:.2f}%)")
print(f"    am_mid_enr   = {agg_mean(full_mets,'am_mid_enr'):.3f}  (VMS A: {VMS_A['am_mid_enr']:.3f})")
print(f"    am_ll        = {agg_mean(full_mets,'am_ll'):.3f}  (VMS A: {VMS_A['am_ll']:.3f})")
print(f"\n  ss diagnostics:")
print(f"    ss_y         = {agg_mean(full_mets,'ss_y'):.4f}  (VMS A: {VMS_A['ss_y']:.4f}, tgt [{VMS_A['ss_y']*0.8:.4f}, {VMS_A['ss_y']*1.2:.4f}])")
print(f"    ss_mean      = {agg_mean(full_mets,'ss_mean'):.4f}  (VMS A: {VMS_A['ss_mean']:.4f})")
print(f"    ss_d         = {agg_mean(full_mets,'ss_d'):.4f}  (VMS A: {VMS_A['ss_d']:.4f})")
print(f"\n  N simulations completed: {len(full_mets)}")

print()
print("Done.")
