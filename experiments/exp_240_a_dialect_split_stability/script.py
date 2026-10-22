"""
exp_240: H440 — A-Dialect Corpus-Split Stability

Question: Does the exp_239 A-dialect 19/19 architecture generalize to independent
odd-folio and even-folio halves of the A-dialect corpus, or is the 19/19 result
a full-corpus overfitting artifact?

Design:
  Analogous to exp_223 (B-dialect corpus-split stability, "STRONGEST VALIDATION
  in the experimental program"). Split A-dialect by folio parity (odd vs even).
  ALL parameters FROZEN at exp_239 values — no recalibration.

  Three conditions:
  (A) Full A-dialect corpus (exp_239 result for reference)
  (B) Odd-folio A-dialect (parameter freeze)
  (C) Even-folio A-dialect (parameter freeze)

  For each: compute 19-metric targets from that corpus slice, run N=30 with
  frozen exp_239 parameters, report pass count.

  Key question: Are VMS half-targets stable (within ±20% of full-corpus targets)?
  If yes, the mechanism reproduces stable structural properties, not corpus-specific noise.

Exp_239 frozen parameters:
  p_blind=0.0505, d_boost=24.30%, r_lf=0.266, r_mid=0.87, p_stutter=0.002
  mu_len=5.64, p_y_y=0.10, cp=0.55, mp=0.90, p_qokch=0.12, p_lf=1.0

H440 predicts: ≥17/19 PASS in both halves; VMS targets stable across halves.
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_FULL   = 30
WINDOW   = 20
SEED     = 240000
PASS_TOL = 0.20

# ─── Exp_239 frozen parameters ─────────────────────────────────────────────────
P_BLIND_A  = 0.0505
D_BOOST_A  = 0.2430
R_LF_A     = 0.266
R_MID_A    = 0.87
P_STUTTER  = 0.002
MU_LEN_A   = 5.64
SIGMA_LEN  = 2.5
P_Y_Y      = 0.10
CP         = 0.55
MP         = 0.90
P_QOKCH    = 0.12
P_LF       = 1.0

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

def parse_vms_a_dialect_by_parity():
    """Parse A-dialect corpus, splitting by odd/even folio number."""
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    folio_lines = defaultdict(list)

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
            folio_lines[fb].append((line, m.group(3), words))

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    # Assign parity by extracting numeric portion of folio base
    def folio_parity(fb):
        digits = re.findall(r'\d+', fb)
        if digits:
            return 'odd' if int(digits[-1]) % 2 == 1 else 'even'
        return 'even'  # default

    sets = {'all': [], 'odd': [], 'even': []}

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
            if words:
                sets['all'].append(words)
                parity = folio_parity(fb)
                sets[parity].append(words)

    return sets

def compute_vms_targets(dialect_lines):
    all_words = [w for l in dialect_lines for w in l]
    lf_words  = [l[0]  for l in dialect_lines if l]
    ll_words  = [l[-1] for l in dialect_lines if len(l) > 1]
    mid_words = [w for l in dialect_lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words); n_mid = max(1, len(mid_words))

    if n < 500: return None  # insufficient data

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
    ll_am_r  = sum(1 for w in ll_words  if w.endswith('am')) / len(ll_words) if ll_words else 0
    lf_am_r  = sum(1 for w in lf_words  if w.endswith('am')) / len(lf_words) if lf_words else 0
    mid_am_r = sum(1 for w in mid_words if w.endswith('am')) / n_mid

    def enr(onset, cs, ns, ca, na):
        s = cs.get(onset, 0)/ns if ns else 0
        g = ca.get(onset, 0)/na if na else 0
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
        'n_lines': len(dialect_lines), 'n_words': n,
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
        # For building sim parameters
        'am_r': am_r, 'll_am_rate': ll_am_r,
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

def cipher_ll(onset_mid, suffix_global, ll_onsets, onset_ll, p_blind, rng):
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return onset + 'am'
    onset  = rng.choices(list(onset_ll.keys()), weights=list(onset_ll.values()))[0]
    suffix = rng.choices(list(suffix_global.keys()), weights=list(suffix_global.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_lf(onset_mid, suffix_lf, onset_lf, p_lf, rng):
    if rng.random() < p_lf:
        onset = rng.choices(list(onset_lf.keys()), weights=list(onset_lf.values()))[0]
        suffix = rng.choices(list(suffix_lf.keys()), weights=list(suffix_lf.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_mid, suffix_lf, rng)

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
    bl = list(buf)
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'y' and p_y_y > 0 and rng.random() < p_y_y:
        yw = [w for w in bl if get_onset(w) == 'y']
        if yw: return rng.choice(yw)
    return rng.choice(bl)

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf, onset_ll, p_blind, target_lines, rng):
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
                    src = draw_buf(buf, prev_onset, P_QOKCH, P_Y_Y, rng)
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
                qok_ch=qok_ch, global_am_rate=am_r)

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

# ─── Parse corpus ──────────────────────────────────────────────────────────────

print("Parsing A-dialect VMS corpus by folio parity...")
corpus_splits = parse_vms_a_dialect_by_parity()

for split_name in ['all', 'odd', 'even']:
    ls = corpus_splits[split_name]
    words = sum(len(l) for l in ls)
    print(f"  {split_name}: {len(ls)} lines, {words} words")

# Compute VMS targets for each split
print("\nComputing VMS targets for each split...")
vms = {}
for split_name in ['all', 'odd', 'even']:
    vms[split_name] = compute_vms_targets(corpus_splits[split_name])
    if vms[split_name] is None:
        print(f"  WARNING: {split_name} corpus too small (< 500 words) — skipping")

# ─── Print target comparison ───────────────────────────────────────────────────

print("\n" + "="*90)
print("VMS TARGET STABILITY ACROSS SPLITS")
print("="*90)
print(f"\n  {'Metric':<18} {'Full':>10} {'Odd':>10} {'%Full':>7} {'Even':>10} {'%Full':>7} {'Stable?'}")
print(f"  {'-'*75}")

for ml in METRIC_LABELS:
    t_all  = vms['all'][ml]
    t_odd  = vms['odd'][ml]  if vms['odd']  else 0
    t_even = vms['even'][ml] if vms['even'] else 0
    pct_odd  = pct(t_odd,  t_all)
    pct_even = pct(t_even, t_all)
    # Both stable if each half within ±20% of full target
    stable_odd  = abs(t_odd  - t_all) / t_all <= 0.20 if t_all else True
    stable_even = abs(t_even - t_all) / t_all <= 0.20 if t_all else True
    stable = 'STABLE' if (stable_odd and stable_even) else 'UNSTABLE'
    print(f"  {ml:<18} {t_all:>10.4f} {t_odd:>10.4f} {pct_odd:>6.1f}% {t_even:>10.4f} {pct_even:>6.1f}% {stable}")

# ─── Load Latin ────────────────────────────────────────────────────────────────

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} words")

# ─── Build frozen parameter set (exp_239) ─────────────────────────────────────

def build_sim_params(v):
    """Build simulation parameter objects from a VMS corpus stats dict."""
    onset_lf  = dict(v['onset_lf'])
    onset_ll  = dict(v['onset_ll'])
    onset_mid = dict(v['onset_mid'])
    suffix    = dict(v['suffix_global'])
    ll_onsets    = build_ll_onsets(onset_ll, D_BOOST_A)
    suffix_lf_s  = make_suppressed_suffix(suffix, R_LF_A)
    suffix_mid_s = make_suppressed_suffix(suffix, R_MID_A)
    return onset_lf, onset_ll, onset_mid, suffix, ll_onsets, suffix_lf_s, suffix_mid_s

# ─── Run simulations for each split ───────────────────────────────────────────

print("\n" + "="*90)
print("SIMULATION RESULTS — FROZEN EXP_239 PARAMETERS")
print("="*90)
print(f"  Parameters: p_blind={P_BLIND_A}, d_boost={D_BOOST_A*100:.2f}%, r_lf={R_LF_A}, r_mid={R_MID_A}")
print(f"              p_stutter={P_STUTTER}, mu_len={MU_LEN_A}, p_y_y={P_Y_Y}")
print(f"              cp={CP}, mp={MP}, p_qokch={P_QOKCH}, p_lf={P_LF}")
print(f"  N={N_FULL} per split")

results = {}
for split_idx, split_name in enumerate(['all', 'odd', 'even']):
    if vms[split_name] is None:
        print(f"\n  SKIP: {split_name} (insufficient data)")
        results[split_name] = []
        continue

    v = vms[split_name]
    onset_lf, onset_ll, onset_mid, suffix, ll_onsets, suffix_lf_s, suffix_mid_s = build_sim_params(v)
    target_lines = v['n_lines']

    print(f"\n  Running {split_name} split ({target_lines} lines per sim)...")
    mets = []
    for i in range(N_FULL):
        rng = random.Random(SEED + split_idx * 100000 + i)
        lines = run_sim(latin, onset_mid, suffix, suffix_lf_s, suffix_mid_s,
                        ll_onsets, onset_lf, onset_ll, P_BLIND_A, target_lines, rng)
        m = compute_metrics(lines)
        if m: mets.append(m)
    results[split_name] = mets
    print(f"  {len(mets)}/{N_FULL} runs completed.")

# ─── Print comparison table ────────────────────────────────────────────────────

print("\n" + "="*90)
print("PASS COMPARISON: Full vs Odd vs Even halves (frozen exp_239 parameters)")
print("="*90)

def print_split_table(split_name, label):
    mets = results[split_name]
    v = vms[split_name]
    if not mets or v is None:
        print(f"\n  {label}: NO DATA")
        return 0
    print(f"\n  {label} ({v['n_lines']} lines, {v['n_words']} words):")
    print(f"  {'Metric':<18} {'VMS_tgt':>10} {'Sim':>10} {'%':>7} {'P?':>3}")
    print(f"  {'-'*50}")
    n_pass = 0
    for ml in METRIC_LABELS:
        t = v[ml]; s = agg_mean(mets, ml)
        flag = pf(s, t)
        if flag == 'P': n_pass += 1
        print(f"  {ml:<18} {t:>10.4f} {s:>10.4f} {pct(s,t):>6.1f}% {flag:>3}")
    print(f"\n  PASS: {n_pass}/19")
    return n_pass

passes = {}
for split_name, label in [('all', 'FULL CORPUS (exp_239 reference)'),
                           ('odd', 'ODD FOLIOS'),
                           ('even', 'EVEN FOLIOS')]:
    passes[split_name] = print_split_table(split_name, label)

# ─── Summary ──────────────────────────────────────────────────────────────────

print()
print("="*90)
print("STABILITY VERDICT")
print("="*90)
print(f"\n  Full corpus:  {passes.get('all', 0)}/19 PASS (exp_239 reference)")
print(f"  Odd folios:   {passes.get('odd', 0)}/19 PASS")
print(f"  Even folios:  {passes.get('even', 0)}/19 PASS")
print(f"\n  Odd corpus:   {len(corpus_splits['odd'])} lines")
print(f"  Even corpus:  {len(corpus_splits['even'])} lines")
print()
all_pass = passes.get('all', 0)
odd_pass  = passes.get('odd', 0)
even_pass = passes.get('even', 0)

if odd_pass >= 17 and even_pass >= 17:
    print("  VERDICT: STABLE — 19/19 A-dialect result generalizes to independent corpus halves.")
elif odd_pass >= 15 and even_pass >= 15:
    print("  VERDICT: PARTIALLY STABLE — some metrics sensitive to corpus half.")
else:
    print("  VERDICT: UNSTABLE — 19/19 result does not generalize to both halves.")

print()
print("Done.")
