"""
exp_229: H429 — adj_rate Stutter Mechanism

Motivation:
  exp_228 (Mode B best, 13/18) has adj_rate=0.003 (36.0% of VMS 0.009 — FAIL).
  The ±20% pass zone for adj_rate is [0.0072, 0.0108]. The simulation produces
  adj_rate≈0.003 across all tested architectures — structural to the onset+edy-
  preserving modification regime where fresh-word diversity prevents exact consecutive
  copies.

  Fix: add a stutter mechanism. With probability p_stutter, repeat the previous
  word verbatim in the current MID position (instead of drawing from buffer or
  generating fresh). This models scribal repetition habits (occasional identical
  consecutive words). Expected adj_rate ≈ baseline(0.003) + p_stutter.

  For target adj_rate ∈ [0.0072, 0.0108]: p_stutter ∈ [0.0042, 0.0078].
  Sweep p_stutter ∈ {0.003, 0.005, 0.006, 0.007, 0.009} at N=10.
  Full run N=30 at best value.

  All other parameters identical to exp_228: cp=0.55, mp=0.90, p_blind=0.30,
  p_lf=1.0, edy-preserving fresh-fallback, VMS MID onset for MID,
  qok→ch Markov bias at p_qokch=0.12.

  Question: Does the stutter mechanism fix adj_rate (36.0%→PASS) without
  regressing the 13 currently passing metrics?
"""

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIMS_SWEEP = 10
N_SIMS_FULL  = 30
TARGET_LINES = 2447
WINDOW       = 20
SEED         = 229000
P_BLIND  = 0.30
P_LF     = 1.0
CP       = 0.55
MP       = 0.90
P_QOKCH  = 0.12   # from exp_228

# Stutter sweep values
P_STUTTER_VALUES = [0.000, 0.003, 0.005, 0.006, 0.007, 0.009]

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

def parse_vms_corpus():
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
            dialect = folio_dialect.get(fb, 'unknown')
            if dialect != 'B': continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: b_lines.append(words)
    return b_lines

def compute_vms_distributions(b_lines):
    all_words = [w for l in b_lines for w in l]
    lf_words  = [l[0]  for l in b_lines if l]
    ll_words  = [l[-1] for l in b_lines if len(l) > 1]
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words)
    n_mid = len(mid_words)

    oc_all = Counter(get_onset(w) for w in all_words)
    oc_lf  = Counter(get_onset(w) for w in lf_words)
    oc_ll  = Counter(get_onset(w) for w in ll_words)
    oc_mid = Counter(get_onset(w) for w in mid_words)

    onset_global = {o: cnt/n for o, cnt in oc_all.items()}
    onset_lf     = {o: cnt/len(lf_words) for o, cnt in oc_lf.items()}
    onset_ll     = {o: cnt/len(ll_words) for o, cnt in oc_ll.items()}
    onset_mid    = {o: cnt/n_mid for o, cnt in oc_mid.items()} if n_mid else {}

    SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']
    suf_ctr = Counter()
    for w in all_words:
        matched = False
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf):
                suf_ctr[suf] += 1; matched = True; break
        if not matched: suf_ctr['other'] += 1
    suffix_global = {suf: cnt/n for suf, cnt in suf_ctr.items()}

    am_r  = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words)
    d_r   = oc_all.get('d', 0) / n
    ll_d  = oc_ll.get('d', 0) / len(ll_words)

    return {
        'onset_global': onset_global,
        'onset_lf': onset_lf,
        'onset_ll': onset_ll,
        'onset_mid': onset_mid,
        'suffix_global': suffix_global,
        'am_r': am_r, 'am_ll_target': ll_am/am_r,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words),
    }

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    remaining_weight = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o not in ('d', 'qok')}
    base_total = sum(base.values())
    if base_total > 0:
        normalized = {o: v/base_total * remaining_weight for o, v in base.items()}
    else:
        normalized = {}
    normalized['d'] = d_boost_weight
    return normalized

def make_word_sim(onset, suffix, rng):
    connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
    return onset + connector + suffix

def random_eva_word(onset_weights, suffix_weights, rng):
    onset  = rng.choices(list(onset_weights.keys()),  weights=list(onset_weights.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_ll_blind(onset_weights, suffix_weights, ll_onsets, p_blind, rng):
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return make_word_sim(onset, 'am', rng)
    return random_eva_word(onset_weights, suffix_weights, rng)

def cipher_lf_vms(onset_weights, suffix_weights, onset_lf_vms, p_lf, rng):
    if rng.random() < p_lf:
        onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
        suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_weights, suffix_weights, rng)

def timm_modify_edy_preserving_fresh_fallback(word, onset_weights, suffix_weights, rng):
    if not word: return word
    onset_len = get_onset_len(word)
    edy_len   = get_edy_suffix_len(word)
    mod_start = onset_len
    mod_end   = len(word) - edy_len
    if mod_start >= mod_end:
        return random_eva_word(onset_weights, suffix_weights, rng)
    op = rng.choice(['replace', 'insert', 'delete'])
    if op == 'replace':
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(mod_start, mod_end)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:
        if mod_end - mod_start <= 1:
            pos = mod_start
            return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + word[pos+1:]

def draw_from_buffer(buf, prev_onset, p_qokch, rng):
    buf_list = list(buf)
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words:
            return rng.choice(ch_words)
    return rng.choice(buf_list)

def run_sim(latin_words, onset_weights, suffix_weights, ll_onsets, onset_lf_vms,
            cp, mp, p_qokch, p_stutter, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None  # Markov state
    prev_word  = None  # Stutter state
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf_vms(onset_weights, suffix_weights, onset_lf_vms, P_LF, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_blind(onset_weights, suffix_weights, ll_onsets, P_BLIND, rng)
            else:
                # Stutter check: with p_stutter, repeat previous word verbatim
                if prev_word is not None and p_stutter > 0 and rng.random() < p_stutter:
                    ew = prev_word
                elif buf and rng.random() < cp:
                    src = draw_from_buffer(buf, prev_onset, p_qokch, rng)
                    if rng.random() < mp:
                        ew = timm_modify_edy_preserving_fresh_fallback(
                            src, onset_weights, suffix_weights, rng)
                    else:
                        ew = src
                else:
                    ew = random_eva_word(onset_weights, suffix_weights, rng)
                buf.append(ew)
            prev_onset = get_onset(ew)
            prev_word  = ew
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def compute_metrics(lines):
    aw  = [w for l in lines for w in l]
    n   = len(aw)
    if n < 100: return None
    lf  = [l[0]  for l in lines if l]
    ll  = [l[-1] for l in lines if len(l) > 1]
    mid = [w for l in lines for w in l[1:-1] if len(l) > 2]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf  = Counter(get_onset(w) for w in lf)
    oc_ll  = Counter(get_onset(w) for w in ll)
    n_lf, n_ll, n_mid = len(lf), len(ll), len(mid)

    def enr(onset, ctr_slot, n_slot, ctr_all, n_all):
        s = ctr_slot.get(onset, 0)/n_slot if n_slot else 0
        g = ctr_all.get(onset, 0)/n_all if n_all else 0
        return s/g if g>0 else 0

    am_r   = sum(1 for w in aw if w.endswith('am')) / n
    ll_am  = sum(1 for w in ll if w.endswith('am')) / n_ll if n_ll else 0
    am_ll  = ll_am / am_r if am_r else 0
    d_ll   = enr('d', oc_ll, n_ll, oc_all, n)
    y_lf   = enr('y', oc_lf, n_lf, oc_all, n)

    tb = n-1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o, 0)/n
        return bg.get((o,o),0)/(tb*b*b) if b>0 else 1.0
    ss_mean = (ss('qok')+ss('ok')+ss('ch'))/3
    adj = sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)

    qok_lf = enr('qok', oc_lf, n_lf, oc_all, n)
    d_lf   = enr('d',   oc_lf, n_lf, oc_all, n)
    s_lf   = enr('s',   oc_lf, n_lf, oc_all, n)
    ch_ll  = enr('ch',  oc_ll, n_ll, oc_all, n)
    ok_ll  = enr('ok',  oc_ll, n_ll, oc_all, n)
    qok_ll = enr('qok', oc_ll, n_ll, oc_all, n)
    ss_d   = ss('d');  ss_y = ss('y')
    am_lf_enr  = (sum(1 for w in lf if w.endswith('am'))/n_lf) / am_r if am_r else 0
    am_mid_enr = (sum(1 for w in mid if w.endswith('am'))/n_mid / am_r) if (n_mid and am_r) else 0
    edy_rate   = sum(1 for w in aw if w.endswith('edy'))/n
    word_len   = sum(len(w) for w in aw)/n
    qok_r  = oc_all.get('qok', 0)/n
    ch_r   = oc_all.get('ch', 0)/n
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch)

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

def agg(metrics_list, key):
    vals = sorted(x[key] for x in metrics_list)
    mean = sum(vals)/len(vals)
    ci_lo = vals[max(0, int(.05*len(vals)))]
    ci_hi = vals[min(len(vals)-1, int(.95*len(vals)))]
    return mean, ci_lo, ci_hi

# ─── Main ─────────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus...")
vms_b_lines = parse_vms_corpus()
vms = compute_vms_distributions(vms_b_lines)
print(f"  VMS B: {len(vms_b_lines)} lines, {vms['n']} words")

d_global    = vms['onset_global'].get('d', 0)
d_ll_target = vms['d_ll_target']
d_boost     = d_global * (d_ll_target - (1-P_BLIND)) / P_BLIND
ll_onsets   = build_ll_onsets(vms['onset_ll'], d_boost)
onset_lf_vms = dict(vms['onset_lf'])
suffix_weights = dict(vms['suffix_global'])
onset_weights_mid = dict(vms['onset_mid'])

print(f"  p_blind={P_BLIND}, d_boost={d_boost*100:.2f}%, p_lf={P_LF}")
print(f"  cp={CP}, mp={MP}, p_qokch={P_QOKCH}")
print()

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

VMS_REF = {
    'am_ll':       vms['am_ll_target'],
    'd_ll':        vms['d_ll_target'],
    'y_lf':        vms['onset_lf'].get('y',0) / vms['onset_global'].get('y',0.001),
    'ss_mean':     1.164,
    'adj_rate':    0.009,
    'qok_lf':      vms['onset_lf'].get('qok',0) / vms['onset_global'].get('qok',0.001),
    'd_lf':        vms['onset_lf'].get('d',0) / vms['onset_global'].get('d',0.001),
    's_lf':        vms['onset_lf'].get('s',0) / vms['onset_global'].get('s',0.001),
    'ch_ll':       vms['onset_ll'].get('ch',0) / vms['onset_global'].get('ch',0.001),
    'ok_ll':       vms['onset_ll'].get('ok',0) / vms['onset_global'].get('ok',0.001),
    'qok_ll':      vms['onset_ll'].get('qok',0) / vms['onset_global'].get('qok',0.001),
    'ss_d':        1.291, 'ss_y': 1.955,
    'am_lf_enr':   (sum(1 for w in [l[0] for l in vms_b_lines if l] if w.endswith('am'))
                    / len([l[0] for l in vms_b_lines if l])) / vms['am_r'],
    'am_mid_enr':  0.195,
    'edy_rate':    sum(vms['suffix_global'].get(s,0) for s in ['edy','eedy']),
    'word_len_mean': 5.400,
    'qok_ch':      1.267,
}

EXP228_REF = {
    'am_ll': 6.247, 'd_ll': 1.238, 'y_lf': 3.419, 'ss_mean': 1.276, 'adj_rate': 0.003,
    'qok_lf': 0.778, 'd_lf': 2.318, 's_lf': 5.063, 'ch_ll': 0.992, 'ok_ll': 1.071,
    'qok_ll': 0.755, 'ss_d': 1.430, 'ss_y': 1.643, 'am_lf_enr': 0.400, 'am_mid_enr': 0.277,
    'edy_rate': 0.187, 'word_len_mean': 6.628, 'qok_ch': 1.180,
}

METRIC_LABELS = [
    ('am_ll', 'CALIBRATED'), ('d_ll', 'CALIBRATED'), ('y_lf', 'VMS-DIRECT'),
    ('ss_mean', 'CALIBRATED (cp/mp)'), ('adj_rate', 'TARGET METRIC'),
    ('qok_lf', 'VMS-DIRECT'), ('d_lf', 'VMS-DIRECT'), ('s_lf', 'VMS-DIRECT'),
    ('ch_ll', 'VMS-DIRECT'), ('ok_ll', 'VMS-DIRECT'), ('qok_ll', 'partial'),
    ('ss_d', 'uncalibrated'), ('ss_y', 'uncalibrated'), ('am_lf_enr', 'uncalibrated'),
    ('am_mid_enr', 'uncalibrated'), ('edy_rate', 'TARGET METRIC'),
    ('word_len_mean', 'uncalibrated'), ('qok_ch', 'TARGET METRIC'),
]

PASS_TOL = 0.20

# ─── Phase 1: Sweep ────────────────────────────────────────────────────────────

print(f"{'='*90}")
print(f"PHASE 1: Parameter Sweep — p_stutter ∈ {P_STUTTER_VALUES}, N={N_SIMS_SWEEP} each")
print(f"Key metrics: adj_rate (target=0.009), ss_mean (target=1.164), qok_ch (target=1.267)")
print(f"{'='*90}")

sweep_results = {}
for pst in P_STUTTER_VALUES:
    metrics_list = []
    for i in range(N_SIMS_SWEEP):
        rng = random.Random(SEED + i)
        lines = run_sim(latin, onset_weights_mid, suffix_weights, ll_onsets, onset_lf_vms,
                        CP, MP, P_QOKCH, pst, rng)
        m = compute_metrics(lines)
        if m: metrics_list.append(m)
    sweep_results[pst] = metrics_list
    adj_mean, _, _ = agg(metrics_list, 'adj_rate')
    ss_mean, _, _  = agg(metrics_list, 'ss_mean')
    qc_mean, _, _  = agg(metrics_list, 'qok_ch')
    adj_pct = adj_mean/VMS_REF['adj_rate']*100
    ss_pct  = ss_mean/VMS_REF['ss_mean']*100
    qc_pct  = qc_mean/VMS_REF['qok_ch']*100
    adj_pass = 'P' if abs(adj_mean-VMS_REF['adj_rate'])/VMS_REF['adj_rate'] <= PASS_TOL else 'F'
    ss_pass  = 'P' if abs(ss_mean-VMS_REF['ss_mean'])/VMS_REF['ss_mean'] <= PASS_TOL else 'F'
    qc_pass  = 'P' if abs(qc_mean-VMS_REF['qok_ch'])/VMS_REF['qok_ch'] <= PASS_TOL else 'F'
    print(f"  p_stutter={pst:.3f}: adj={adj_mean:.4f} ({adj_pct:.1f}% [{adj_pass}])  "
          f"ss_mean={ss_mean:.3f} ({ss_pct:.1f}% [{ss_pass}])  "
          f"qok_ch={qc_mean:.3f} ({qc_pct:.1f}% [{qc_pass}])")

print()

# Find best p_stutter: adj_rate in pass zone [0.0072, 0.0108], closest to VMS 0.009
best_pst = None
best_dist = float('inf')
for pst, mlist in sweep_results.items():
    adj, _, _ = agg(mlist, 'adj_rate')
    dist = abs(adj - VMS_REF['adj_rate'])
    in_pass = VMS_REF['adj_rate']*0.8 <= adj <= VMS_REF['adj_rate']*1.2
    if in_pass and dist < best_dist:
        best_dist = dist
        best_pst = pst

if best_pst is None:
    best_pst = min(P_STUTTER_VALUES, key=lambda pst:
                   abs(agg(sweep_results[pst], 'adj_rate')[0] - VMS_REF['adj_rate']))

print(f"Best p_stutter from sweep: {best_pst:.3f}")
print()

# ─── Phase 2: Full Run ─────────────────────────────────────────────────────────

print(f"{'='*105}")
print(f"PHASE 2: Full Run at p_stutter={best_pst:.3f}, N={N_SIMS_FULL}")
print(f"Mode B + edy-preserving fresh-fallback + qok→ch Markov (p_qokch={P_QOKCH}) + stutter")
print(f"p_blind={P_BLIND}, d_boost={d_boost*100:.2f}%, p_lf={P_LF}, cp={CP}, mp={MP}")
print(f"{'='*105}")

full_metrics = []
for i in range(N_SIMS_FULL):
    rng = random.Random(SEED + 1000 + i)
    lines = run_sim(latin, onset_weights_mid, suffix_weights, ll_onsets, onset_lf_vms,
                    CP, MP, P_QOKCH, best_pst, rng)
    m = compute_metrics(lines)
    if m: full_metrics.append(m)

print(f"  Completed {len(full_metrics)} simulations.")
print()

pass_count = 0; total = 0
print(f"  {'Metric':<16} {'VMS':>8} {'E229':>8} {'%':>7} {'P?':<4}  E228    delta")
print(f"  {'-'*80}")
for key, cat in METRIC_LABELS:
    vms_val = VMS_REF.get(key)
    if vms_val is None: continue
    sim_mean, ci_lo, ci_hi = agg(full_metrics, key)
    pct = sim_mean/vms_val*100 if abs(vms_val)>1e-6 else float('inf')
    pass_f = abs(sim_mean-vms_val)/abs(vms_val) <= PASS_TOL if abs(vms_val)>1e-6 else abs(sim_mean)<0.002
    status = 'P' if pass_f else 'F'
    e228 = EXP228_REF.get(key, float('nan'))
    delta = sim_mean - e228
    print(f"  {key:<16} {vms_val:>8.3f} {sim_mean:>8.3f} {pct:>6.1f}% {status}    {e228:>7.3f}  {delta:>+7.3f}  [{cat}]")
    total += 1
    if pass_f: pass_count += 1

print()
print(f"  Pass count:  E229={pass_count}/{total}  |  E228 (baseline)=13/18")
print()
print(f"  Key tracking (adj_rate fix progress):")
for k in ['adj_rate', 'ss_mean', 'qok_ch', 'edy_rate']:
    vv = VMS_REF[k]
    m229, _, _ = agg(full_metrics, k)
    m228 = EXP228_REF[k]
    p229 = 'P' if abs(m229-vv)/abs(vv) <= PASS_TOL else 'F'
    p228 = 'P' if abs(m228-vv)/abs(vv) <= PASS_TOL else 'F'
    print(f"    {k:<16}: VMS={vv:.4f}  E228={m228:.4f}[{p228}]  E229={m229:.4f}[{p229}]  delta={m229-m228:+.4f}")

print()
print(f"  p_stutter={best_pst:.3f}: with probability {best_pst:.3f}, current MID word = previous word verbatim")
