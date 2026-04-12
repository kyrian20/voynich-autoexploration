"""
exp_231: H431 — LL Non-Blind Onset Fix

Motivation:
  exp_230 (H430 diagnostic) identified the root cause of qok_ll=0.764 failure:
  the non-blind LL fraction (70% of LL words) uses VMS MID onset (qok=14.19%)
  instead of VMS LL onset (qok=7.62%), inflating sim LL qok from target 7.62%
  to actual 9.87%. Additionally, build_ll_onsets() excludes qok from the blind
  LL fraction (qok=0% in ll_onsets).

  Expected sim LL qok = 0.30 × 0% + 0.70 × 14.19% = 9.93% ← confirmed by diagnostic.
  VMS target LL qok = 7.62%.

  Fix (two parts):
  1. Change cipher_ll_blind: non-blind fraction uses onset_ll_vms instead of onset_weights_mid
  2. Fix build_ll_onsets: include qok in the normalized distribution (don't exclude it)
  3. Re-calibrate d_boost for new non-blind d contribution from VMS LL:
     d_boost_new = d_global × [d_ll_target - (1-p_blind) × (VMS_LL_d/d_global)] / p_blind

  Expected qok_ll after fix = 7.62 / 12.80 = 0.595 ← exact VMS target → PASS.

  All other parameters identical to exp_229: cp=0.55, mp=0.90, p_blind=0.30,
  p_lf=1.0, edy-preserving fresh-fallback, VMS MID onset for MID,
  qok→ch Markov at p_qokch=0.12, stutter at p_stutter=0.009.

  Question: Does the LL onset fix bring qok_ll to PASS (128.4%→≤120%) without
  regressing the 14 currently passing metrics?
"""

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIMS_FULL  = 30
TARGET_LINES = 2447
WINDOW       = 20
SEED         = 231000
P_BLIND  = 0.30
P_LF     = 1.0
CP       = 0.55
MP       = 0.90
P_QOKCH  = 0.12
P_STUTTER = 0.009

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

def build_ll_onsets_fixed(onset_ll_vms, d_boost_weight):
    """
    FIXED: Include qok in the normalized distribution (previously excluded).
    Only 'd' is removed and replaced with d_boost_weight.
    """
    remaining_weight = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o != 'd'}  # FIX: keep qok
    base_total = sum(base.values())
    if base_total > 0:
        normalized = {o: v/base_total * remaining_weight for o, v in base.items()}
    else:
        normalized = {}
    normalized['d'] = d_boost_weight
    return normalized

def compute_d_boost_fixed(d_global, d_ll_target, d_ll_non_blind, p_blind):
    """
    Re-calibrate d_boost for new non-blind d contribution from VMS LL.
    d_ll_target = p_blind × d_boost/d_global + (1-p_blind) × d_ll_non_blind
    d_boost = d_global × (d_ll_target - (1-p_blind) × d_ll_non_blind) / p_blind
    where d_ll_non_blind = onset_ll['d'] / d_global = VMS LL d enrichment
    """
    return d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind) / p_blind

def make_word_sim(onset, suffix, rng):
    connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
    return onset + connector + suffix

def random_eva_word(onset_weights, suffix_weights, rng):
    onset  = rng.choices(list(onset_weights.keys()),  weights=list(onset_weights.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_ll_blind_fixed(onset_weights_mid, suffix_weights, ll_onsets, onset_ll_vms, p_blind, rng):
    """
    FIXED LL generator:
    - Blind fraction: onset from ll_onsets (d-boosted VMS LL, now with qok), suffix='am'
    - Non-blind fraction: onset from onset_ll_vms (VMS LL distribution)  ← FIX: was onset_weights_mid
    """
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return make_word_sim(onset, 'am', rng)
    # FIX: use VMS LL onset (not MID) for non-blind LL
    onset  = rng.choices(list(onset_ll_vms.keys()), weights=list(onset_ll_vms.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
    return make_word_sim(onset, suffix, rng)

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

def run_sim(latin_words, onset_weights_mid, suffix_weights, ll_onsets, onset_lf_vms, onset_ll_vms,
            cp, mp, p_qokch, p_stutter, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None
    prev_word  = None
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf_vms(onset_weights_mid, suffix_weights, onset_lf_vms, P_LF, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_blind_fixed(onset_weights_mid, suffix_weights, ll_onsets,
                                           onset_ll_vms, P_BLIND, rng)
            else:
                if prev_word is not None and p_stutter > 0 and rng.random() < p_stutter:
                    ew = prev_word
                elif buf and rng.random() < cp:
                    src = draw_from_buffer(buf, prev_onset, p_qokch, rng)
                    if rng.random() < mp:
                        ew = timm_modify_edy_preserving_fresh_fallback(
                            src, onset_weights_mid, suffix_weights, rng)
                    else:
                        ew = src
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_weights, rng)
                buf.append(ew)
            prev_onset = get_onset(ew)
            prev_word  = ew
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def compute_metrics(lines, vms):
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

    # Extra diagnostics
    ll_qok_actual = oc_ll.get('qok',0)/n_ll if n_ll else 0
    global_qok_actual = oc_all.get('qok',0)/n

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch,
                _ll_qok=ll_qok_actual, _global_qok=global_qok_actual)

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
onset_ll_vms = dict(vms['onset_ll'])

# NEW: compute d_boost using VMS LL d for non-blind fraction
vms_ll_d_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0  # d enrichment at LL
d_boost_new = compute_d_boost_fixed(d_global, d_ll_target, vms_ll_d_enr, P_BLIND)

print(f"\n  d_boost calibration:")
print(f"    VMS d_ll_target = {d_ll_target:.4f}")
print(f"    VMS LL d rate = {onset_ll_vms.get('d',0)*100:.2f}%")
print(f"    VMS LL d enrichment = {vms_ll_d_enr:.4f}")
print(f"    d_global = {d_global*100:.2f}%")
print(f"    OLD d_boost (non-blind uses MID) = {d_global * (d_ll_target - (1-P_BLIND)) / P_BLIND * 100:.2f}%")
print(f"    NEW d_boost (non-blind uses VMS LL) = {d_boost_new*100:.2f}%")

ll_onsets   = build_ll_onsets_fixed(onset_ll_vms, d_boost_new)
onset_lf_vms = dict(vms['onset_lf'])
suffix_weights = dict(vms['suffix_global'])
onset_weights_mid = dict(vms['onset_mid'])

# Verify qok in ll_onsets
ll_qok_in_blind = ll_onsets.get('qok', 0)
ll_qok_in_nonblind = onset_ll_vms.get('qok', 0)
expected_ll_qok = P_BLIND * ll_qok_in_blind + (1-P_BLIND) * ll_qok_in_nonblind
print(f"\n  Expected LL qok rates:")
print(f"    Blind fraction (p={P_BLIND}): ll_onsets qok = {ll_qok_in_blind*100:.2f}%")
print(f"    Non-blind fraction (p={1-P_BLIND}): onset_ll_vms qok = {ll_qok_in_nonblind*100:.2f}%")
print(f"    Expected combined LL qok = {expected_ll_qok*100:.2f}% (VMS target = {onset_ll_vms.get('qok',0)*100:.2f}%)")
expected_qokll = expected_ll_qok / vms['onset_global'].get('qok', 0.001)
print(f"    Expected qok_ll = {expected_qokll:.3f} (VMS = {onset_ll_vms.get('qok',0)/vms['onset_global'].get('qok',0.001):.3f})")

print(f"\n  p_blind={P_BLIND}, d_boost_new={d_boost_new*100:.2f}%, p_lf={P_LF}")
print(f"  cp={CP}, mp={MP}, p_qokch={P_QOKCH}, p_stutter={P_STUTTER}")
print(f"  KEY FIX: non-blind LL uses onset_ll_vms (qok={ll_qok_in_nonblind*100:.2f}%) instead of MID")
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

EXP229_REF = {
    'am_ll': 6.234, 'd_ll': 1.225, 'y_lf': 3.488, 'ss_mean': 1.336, 'adj_rate': 0.010,
    'qok_lf': 0.758, 'd_lf': 2.308, 's_lf': 5.062, 'ch_ll': 0.990, 'ok_ll': 1.058,
    'qok_ll': 0.764, 'ss_d': 1.533, 'ss_y': 1.759, 'am_lf_enr': 0.404, 'am_mid_enr': 0.278,
    'edy_rate': 0.186, 'word_len_mean': 6.625, 'qok_ch': 1.177,
}

METRIC_LABELS = [
    ('am_ll', 'CALIBRATED'), ('d_ll', 'CALIBRATED'), ('y_lf', 'VMS-DIRECT'),
    ('ss_mean', 'CALIBRATED (cp/mp)'), ('adj_rate', 'TARGET METRIC'),
    ('qok_lf', 'VMS-DIRECT'), ('d_lf', 'VMS-DIRECT'), ('s_lf', 'VMS-DIRECT'),
    ('ch_ll', 'VMS-DIRECT'), ('ok_ll', 'VMS-DIRECT'), ('qok_ll', 'TARGET METRIC'),
    ('ss_d', 'uncalibrated'), ('ss_y', 'uncalibrated'), ('am_lf_enr', 'uncalibrated'),
    ('am_mid_enr', 'uncalibrated'), ('edy_rate', 'TARGET METRIC'),
    ('word_len_mean', 'uncalibrated'), ('qok_ch', 'TARGET METRIC'),
]

print(f"{'='*105}")
print(f"FULL RUN: N={N_SIMS_FULL}")
print(f"Fix: non-blind LL uses onset_ll_vms; qok included in ll_onsets; d_boost recalibrated")
print(f"{'='*105}")

full_metrics = []
for i in range(N_SIMS_FULL):
    rng = random.Random(SEED + i)
    lines = run_sim(latin, onset_weights_mid, suffix_weights, ll_onsets, onset_lf_vms, onset_ll_vms,
                    CP, MP, P_QOKCH, P_STUTTER, rng)
    m = compute_metrics(lines, vms)
    if m: full_metrics.append(m)

print(f"  Completed {len(full_metrics)} simulations.")
print()

PASS_TOL = 0.20
pass_count = 0; total = 0
print(f"  {'Metric':<16} {'VMS':>8} {'E231':>8} {'%':>7} {'P?':<4}  E229    delta")
print(f"  {'-'*80}")
for key, cat in METRIC_LABELS:
    vms_val = VMS_REF.get(key)
    if vms_val is None: continue
    sim_mean, ci_lo, ci_hi = agg(full_metrics, key)
    pct = sim_mean/vms_val*100 if abs(vms_val)>1e-6 else float('inf')
    pass_f = abs(sim_mean-vms_val)/abs(vms_val) <= PASS_TOL if abs(vms_val)>1e-6 else abs(sim_mean)<0.002
    status = 'P' if pass_f else 'F'
    e229 = EXP229_REF.get(key, float('nan'))
    delta = sim_mean - e229
    print(f"  {key:<16} {vms_val:>8.3f} {sim_mean:>8.3f} {pct:>6.1f}% {status}    {e229:>7.3f}  {delta:>+7.3f}  [{cat}]")
    total += 1
    if pass_f: pass_count += 1

print()
print(f"  Pass count:  E231={pass_count}/{total}  |  E229 (baseline)=14/18")
print()

# Diagnostic: verify LL and global qok rates
ll_qok_actual = sum(agg(full_metrics, '_ll_qok')[0] for _ in [None])/1
ll_qok_m = sum(m['_ll_qok'] for m in full_metrics)/len(full_metrics)
glob_qok_m = sum(m['_global_qok'] for m in full_metrics)/len(full_metrics)
print(f"  qok_ll diagnostic:")
print(f"    Actual LL qok = {ll_qok_m*100:.2f}% (VMS LL qok = {onset_ll_vms.get('qok',0)*100:.2f}%)")
print(f"    Global qok    = {glob_qok_m*100:.2f}% (VMS global qok = {vms['onset_global'].get('qok',0)*100:.2f}%)")
print(f"    Derived qok_ll = {ll_qok_m/glob_qok_m:.3f} (VMS = {VMS_REF['qok_ll']:.3f})")
print()
print(f"  Key tracking (qok_ll fix progress):")
for k in ['qok_ll', 'd_ll', 'am_ll', 'ss_mean', 'adj_rate']:
    vv = VMS_REF[k]
    m231, _, _ = agg(full_metrics, k)
    m229 = EXP229_REF[k]
    p231 = 'P' if abs(m231-vv)/abs(vv) <= PASS_TOL else 'F'
    p229 = 'P' if abs(m229-vv)/abs(vv) <= PASS_TOL else 'F'
    print(f"    {k:<16}: VMS={vv:.4f}  E229={m229:.4f}[{p229}]  E231={m231:.4f}[{p231}]  delta={m231-m229:+.4f}")
