"""
exp_217: H410 — Expanded Metric Battery for exp_211 Best Configuration

Motivation:
  exp_211 achieved all five primary VMS metrics within 3% simultaneously
  using four target-calibrated parameters (p_blind=0.40, d_am=0.16,
  p_lf_blind=0.22, cp=0.76, mp=0.9). But this joint fit was maximally
  target-aware: every parameter was set by reference to the VMS target it
  controls.

  H410 asks: does exp_211's best config also reproduce VMS structural metrics
  it was NOT calibrated to? If yes, the architecture captures genuine VMS
  structure beyond the 5 trained signals. If no, the fit is narrow — the
  architecture silently fails on other VMS signals.

Test:
  (1) Compute 10 additional metrics from VMS B-dialect corpus (same parser as exp_216)
  (2) Run N=50 simulations at exp_211 best config (p_lf_blind=0.22, everything else fixed)
  (3) For each additional metric, report: VMS value, sim mean, %VMS, pass/fail (within 20%)

Additional metrics (uncalibrated targets):
  1.  qok_lf:      qok-onset LF enrichment (VMS: expected depleted, C003 committed)
  2.  d_lf:        d-onset LF enrichment (B LF top onset: 14.8% of LF words)
  3.  s_lf:        s-onset LF enrichment (B LF: 11.2%)
  4.  ch_ll:       ch-onset LL enrichment (B LL top: 14.5%)
  5.  ok_ll:       ok-onset LL enrichment (B LL: qok=7.6%; ok rate?)
  6.  qok_ll:      qok-onset LL enrichment (B LL: 7.6%)
  7.  ss_d:        d-onset self-succession (B corpus: 1.291x)
  8.  ss_y:        y-onset self-succession (B corpus: 1.955x)
  9.  am_lf:       -am suffix at LF enrichment (should be depleted vs LL)
 10.  am_mid:      -am suffix in MID positions enrichment
 11.  edy_rate:    overall edy-suffix rate (VMS B: 19.40%)
 12.  word_len:    mean word length (VMS: 5.768 chars in B)
 13.  qok_ch_bigram: qok->ch bigram enrichment

The simulation uses fixed params: d_am=0.16, p_blind=0.40, p_lf_blind=0.22,
cp=0.76, mp=0.9. Same architecture as exp_211 but only ONE configuration
(no sweep needed — just the best joint config).
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIMS       = 50
TARGET_LINES = 2447
WINDOW       = 20
CP, MP       = 0.76, 0.9
P_BLIND      = 0.40
D_AM         = 0.16
P_LF_BLIND   = 0.22
SEED         = 217000

# ─── Simulation components (from exp_211) ──────────────────────────────────

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

def make_ll_onsets_recal(d_weight):
    base = {'ok': 0.15, 'qok': 0.15, 'ch': 0.10, 'other': 0.20}
    base_total = sum(base.values())
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
    if rng.random() < P_BLIND:
        onset = rng.choices(list(LL_ONSETS.keys()), weights=list(LL_ONSETS.values()))[0]
        return make_word(onset, 'am', rng)
    return random_eva_word(rng)

def cipher_lf_blind(rng):
    if rng.random() < P_LF_BLIND:
        return make_word('y', rng.choices(list(SUFFIX_WEIGHTS.keys()),
                                          weights=list(SUFFIX_WEIGHTS.values()))[0], rng)
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

def run_sim(latin_words, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf_blind(rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_blind(rng)
            else:
                if buf and rng.random() < CP:
                    ew = timm_modify(rng.choice(list(buf)), rng) if rng.random() < MP else rng.choice(list(buf))
                else:
                    ew = random_eva_word(rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line)
        pos += n
    return lines[:TARGET_LINES]

# ─── Metric computation ─────────────────────────────────────────────────────

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix):
            return label
    return 'other'

def compute_metrics(lines):
    aw = [w for l in lines for w in l]
    n = len(aw)
    if n < 100:
        return None

    lf  = [l[0]  for l in lines if l]
    ll  = [l[-1] for l in lines if len(l) > 1]
    mid = [w for l in lines for w in l[1:-1] if len(l) > 2]

    oc  = Counter(get_onset(w) for w in aw)
    oc_lf  = Counter(get_onset(w) for w in lf)
    oc_ll  = Counter(get_onset(w) for w in ll)

    n_lf, n_ll, n_mid = len(lf), len(ll), len(mid)

    def enr(onset, slot_counter, slot_n, global_rate):
        slot_rate = slot_counter.get(onset, 0) / slot_n if slot_n else 0
        return slot_rate / global_rate if global_rate > 0 else 0

    # ── Primary 5 (from exp_211) ──────────────────────────────────────────
    am_r  = sum(1 for w in aw if w.endswith('am')) / n
    ll_am = sum(1 for w in ll if w.endswith('am')) / n_ll if n_ll else 0
    am_ll = ll_am / am_r if am_r > 0 else 0

    d_r  = oc.get('d', 0) / n
    ll_d = oc_ll.get('d', 0) / n_ll if n_ll else 0
    d_ll = ll_d / d_r if d_r > 0 else 0

    y_r  = oc.get('y', 0) / n
    y_lf = (oc_lf.get('y', 0) / n_lf) / y_r if y_r and n_lf else 0

    tb = n - 1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss_calc(o):
        b = oc.get(o, 0) / n
        return bg.get((o, o), 0) / (tb * b * b) if b > 0 and tb > 0 else 1.0
    ss_mean = (ss_calc('qok') + ss_calc('ok') + ss_calc('ch')) / 3
    adj = sum(1 for i in range(tb) if aw[i] == aw[i+1]) / max(1, tb)

    # ── Additional 13 metrics (uncalibrated) ─────────────────────────────
    qok_r = oc.get('qok', 0) / n
    qok_lf = enr('qok', oc_lf, n_lf, qok_r)   # should be depleted (C003)

    d_lf = enr('d', oc_lf, n_lf, d_r)          # VMS B: ~2.21×

    s_r  = oc.get('s', 0) / n
    s_lf = enr('s', oc_lf, n_lf, s_r)          # VMS B: ~4.0×

    ch_r = oc.get('ch', 0) / n
    ch_ll = enr('ch', oc_ll, n_ll, ch_r)        # VMS B: ~0.94×

    ok_r = oc.get('ok', 0) / n
    ok_ll = enr('ok', oc_ll, n_ll, ok_r)        # VMS B: significant

    qok_ll = enr('qok', oc_ll, n_ll, qok_r)     # VMS B: ~0.59× (from exp_216 ~7.6%/12.1%)

    ss_d = ss_calc('d')                          # VMS B corpus: 1.291×
    ss_y = ss_calc('y')                          # VMS B corpus: 1.955×

    # -am suffix by position
    am_lf_rate = sum(1 for w in lf  if w.endswith('am')) / n_lf  if n_lf  else 0
    am_mid_rate = sum(1 for w in mid if w.endswith('am')) / n_mid if n_mid else 0
    am_lf_enr  = am_lf_rate / am_r  if am_r else 0
    am_mid_enr = am_mid_rate / am_r if am_r else 0

    # edy-suffix overall rate
    edy_rate = sum(1 for w in aw if w.endswith('edy')) / n

    # mean word length
    word_len_mean = sum(len(w) for w in aw) / n

    # qok -> ch bigram enrichment
    qok_ch = bg.get(('qok', 'ch'), 0) / (tb * qok_r * ch_r) if qok_r and ch_r else 0

    return {
        # Primary 5
        'am_ll': am_ll, 'd_ll': d_ll, 'y_lf': y_lf,
        'ss_mean': ss_mean, 'adj_rate': adj,
        # Additional 13
        'qok_lf': qok_lf, 'd_lf': d_lf, 's_lf': s_lf,
        'ch_ll': ch_ll, 'ok_ll': ok_ll, 'qok_ll': qok_ll,
        'ss_d': ss_d, 'ss_y': ss_y,
        'am_lf_enr': am_lf_enr, 'am_mid_enr': am_mid_enr,
        'edy_rate': edy_rate,
        'word_len_mean': word_len_mean,
        'qok_ch': qok_ch,
        # Base rates for debugging
        'am_r': am_r, 'd_r': d_r, 'y_r': y_r, 's_r': s_r,
        'ch_r': ch_r, 'ok_r': ok_r, 'qok_r': qok_r,
    }

# ─── Parse VMS B-dialect corpus (same as exp_216) ───────────────────────────

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0:
        return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_vms_corpus():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'):
                    folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'):
                    folio_word_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    b_lines = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            dialect = folio_dialect.get(fb, 'unknown')
            if dialect != 'B':
                continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            is_body = lc_stripped.lstrip('@').startswith('P')
            if not is_body:
                continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words:
                b_lines.append(words)
    return b_lines

# ─── Main ────────────────────────────────────────────────────────────────────

print("Loading VMS B-dialect corpus...")
vms_b_lines = parse_vms_corpus()
vms_metrics = compute_metrics(vms_b_lines)
n_vms_words = sum(len(l) for l in vms_b_lines)
print(f"  VMS B: {len(vms_b_lines)} lines, {n_vms_words} words")

print("\nVMS B-dialect metric values (targets):")
print("  BASE RATES:")
print(f"    am_r={vms_metrics['am_r']:.4f}  d_r={vms_metrics['d_r']:.4f}  y_r={vms_metrics['y_r']:.4f}")
print(f"    s_r={vms_metrics['s_r']:.4f}   ch_r={vms_metrics['ch_r']:.4f}  ok_r={vms_metrics['ok_r']:.4f}  qok_r={vms_metrics['qok_r']:.4f}")
print()

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

print(f"Running N={N_SIMS} simulations at exp_211 best config:")
print(f"  p_blind={P_BLIND}, d_am={D_AM}, p_lf_blind={P_LF_BLIND}, cp={CP}, mp={MP}")
print()

all_metrics = []
for i in range(N_SIMS):
    rng = random.Random(SEED + i)
    lines = run_sim(latin, rng)
    m = compute_metrics(lines)
    if m:
        all_metrics.append(m)

print(f"  Completed {len(all_metrics)} simulations.")
print()

# ─── Report ──────────────────────────────────────────────────────────────────

def agg(key):
    vals = sorted(x[key] for x in all_metrics)
    mean = sum(vals) / len(vals)
    ci_lo = vals[max(0, int(.05*len(vals)))]
    ci_hi = vals[min(len(vals)-1, int(.95*len(vals)))]
    return mean, ci_lo, ci_hi

METRIC_LABELS = {
    'am_ll':      ('-am LL enrichment',       'CALIBRATED'),
    'd_ll':       ('d-onset LL enrichment',   'CALIBRATED'),
    'y_lf':       ('y-onset LF enrichment',   'CALIBRATED'),
    'ss_mean':    ('onset self-succession',   'CALIBRATED'),
    'adj_rate':   ('exact adj repetition',    'CALIBRATED'),
    'qok_lf':     ('qok LF enrichment',       'uncalibrated'),
    'd_lf':       ('d-onset LF enrichment',   'uncalibrated'),
    's_lf':       ('s-onset LF enrichment',   'uncalibrated'),
    'ch_ll':      ('ch-onset LL enrichment',  'uncalibrated'),
    'ok_ll':      ('ok-onset LL enrichment',  'uncalibrated'),
    'qok_ll':     ('qok-onset LL enrichment', 'uncalibrated'),
    'ss_d':       ('d self-succession',       'uncalibrated'),
    'ss_y':       ('y self-succession',       'uncalibrated'),
    'am_lf_enr':  ('-am LF enrichment',       'uncalibrated'),
    'am_mid_enr': ('-am MID enrichment',      'uncalibrated'),
    'edy_rate':   ('edy-suffix rate',         'uncalibrated'),
    'word_len_mean': ('mean word length',     'uncalibrated'),
    'qok_ch':     ('qok->ch bigram enr',      'uncalibrated'),
}

print("=" * 80)
print("EXPANDED METRIC BATTERY: exp_211 BEST CONFIG vs VMS B-DIALECT")
print("=" * 80)
print(f"{'Metric':<18} {'VMS':>8} {'Sim':>8} {'%VMS':>7} {'CI 5-95':>18} {'Status':<12} {'Cal?'}")
print("-" * 80)

PASS_TOL = 0.20  # within 20% of VMS = pass

calibrated_results = []
uncalibrated_results = []

for key, (label, cal_status) in METRIC_LABELS.items():
    vms_val = vms_metrics.get(key)
    if vms_val is None:
        continue
    sim_mean, ci_lo, ci_hi = agg(key)

    if abs(vms_val) < 1e-8:
        pct = float('inf')
        pass_flag = abs(sim_mean) < 0.002
    else:
        pct = sim_mean / vms_val * 100
        pass_flag = abs(sim_mean - vms_val) / abs(vms_val) <= PASS_TOL

    status = 'PASS' if pass_flag else 'FAIL'
    color_tag = f"[{status}]"

    print(f"  {key:<16} {vms_val:>8.3f} {sim_mean:>8.3f} {pct:>6.1f}% "
          f"  [{ci_lo:.3f},{ci_hi:.3f}] {color_tag:<12} {cal_status}")

    entry = (key, vms_val, sim_mean, pct, pass_flag, cal_status)
    if cal_status == 'CALIBRATED':
        calibrated_results.append(entry)
    else:
        uncalibrated_results.append(entry)

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)

cal_pass = sum(1 for *_, p, _ in calibrated_results if p)
cal_total = len(calibrated_results)
uncal_pass = sum(1 for *_, p, _ in uncalibrated_results if p)
uncal_total = len(uncalibrated_results)

print(f"  Calibrated metrics:   {cal_pass}/{cal_total} pass (within ±20% of VMS)")
print(f"  Uncalibrated metrics: {uncal_pass}/{uncal_total} pass (within ±20% of VMS)")
print()

print("  FAILING uncalibrated metrics:")
for key, vms_val, sim_mean, pct, pass_flag, _ in uncalibrated_results:
    if not pass_flag:
        direction = 'over' if sim_mean > vms_val else 'under'
        print(f"    {key:<18}: VMS={vms_val:.3f}  Sim={sim_mean:.3f}  ({pct:.1f}%  — {direction}produces)")

print()
print("  PASSING uncalibrated metrics:")
for key, vms_val, sim_mean, pct, pass_flag, _ in uncalibrated_results:
    if pass_flag:
        print(f"    {key:<18}: VMS={vms_val:.3f}  Sim={sim_mean:.3f}  ({pct:.1f}%)")

print()
print("  Architectural analysis (predicted vs observed):")
print(f"  LF override (p_lf_blind={P_LF_BLIND}): only y-onset boosted at LF.")
print(f"    → d_lf, s_lf expected to fail (only y is privileged; d/s depleted by override)")
print(f"  LL override (p_blind={P_BLIND}): LL_ONSETS={LL_ONSETS}")
print(f"    → ok_ll, qok_ll, ch_ll boosted; VMS ch_ll may be near-neutral (potential failure)")
