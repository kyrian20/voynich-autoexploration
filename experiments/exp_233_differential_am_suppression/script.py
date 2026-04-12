"""
exp_233: H433 — Differential -am Suppression (r_lf ≠ r_mid)

Motivation:
  exp_232 (H432 NEGATIVE) showed that uniform suppression (r_lf=r_mid=r) cannot
  simultaneously achieve am_lf_enr PASS and am_mid_enr PASS because:
    (1) Copy buffer modification erosion reduces equilibrium MID am ~16% below
        fresh MID am, causing MID to overshoot further than LF under uniform r.
    (2) Both metrics share the same global_am denominator, making joint calibration
        structurally impossible with a single suppression factor.

  Analytical derivation (exp_232 F232 Finding 5):
    r_lf ≈ 0.33 (LF only): LF_am = 0.33 × 2.03% ≈ 0.67%
    r_mid ≈ 0.70 (MID only): fresh MID am = 0.70 × 1.55% ≈ 1.09%;
                              equilibrium MID am ≈ 0.70 × 1.55% × 0.84 ≈ 1.05%
    global_am ≈ 0.129 × 0.67% + 0.742 × 1.05% + 0.129 × 31.39% ≈ 4.91%
    am_lf_enr ≈ 0.67/4.91 = 0.136 → PASS [0.098, 0.146]
    am_mid_enr ≈ 1.05/4.91 = 0.214 → PASS [0.156, 0.234]
    am_ll ≈ 31.39/4.91 = 6.39 → PASS [5.24, 7.86]

  Fix (this experiment):
  Apply INDEPENDENT suppression factors:
    - r_lf for the LF fresh-word suffix distribution only
    - r_mid for the MID fresh-word suffix distribution only (random_eva_word
      and the edy-modification fresh-word fallback)
  LL non-blind fraction continues to use suffix_global (unchanged).

  Sweep grid: r_lf ∈ {0.25, 0.33, 0.40} × r_mid ∈ {0.60, 0.70, 0.80}
  = 9 combinations at N=5 each. Full N=30 at best (r_lf, r_mid).

  Selection criterion: minimize (am_lf_enr/VMS - 1)^2 + (am_mid_enr/VMS - 1)^2
  subject to: am_lf_enr ∈ [0.098, 0.146] AND am_mid_enr ∈ [0.156, 0.234]
              AND am_ll ∈ [5.24, 7.86] (pass zone).

  All other parameters identical to exp_231:
  cp=0.55, mp=0.90, p_blind=0.30, p_lf=1.0, p_qokch=0.12, p_stutter=0.009,
  d_boost=9.13%, VMS LL onset for non-blind LL.

  Question: Does differential -am suppression (separate r_lf and r_mid) bring
  am_lf_enr and am_mid_enr to PASS without regressing any of the 15 currently
  passing metrics from exp_231?
"""

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SWEEP  = 5     # sims per (r_lf, r_mid) combination in sweep
N_FULL   = 30    # full run at best combination
TARGET_LINES = 2447
WINDOW   = 20
SEED     = 233000

P_BLIND   = 0.30
P_LF      = 1.0
CP        = 0.55
MP        = 0.90
P_QOKCH   = 0.12
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

def make_suppressed_suffix(suffix_global, r_am):
    """
    Create a modified suffix distribution with -am weight multiplied by r_am.
    All other suffixes renormalized so total sums to 1.
    r_am=1.0 → unchanged; r_am=0.0 → no -am at all.
    """
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
    if base_total > 0:
        normalized = {o: v/base_total * remaining_weight for o, v in base.items()}
    else:
        normalized = {}
    normalized['d'] = d_boost_weight
    return normalized

def compute_d_boost_fixed(d_global, d_ll_target, d_ll_non_blind, p_blind):
    return d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind) / p_blind

def make_word_sim(onset, suffix, rng):
    connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
    return onset + connector + suffix

def random_eva_word(onset_weights, suffix_weights, rng):
    onset  = rng.choices(list(onset_weights.keys()),  weights=list(onset_weights.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_ll_blind_fixed(onset_weights_mid, suffix_global, ll_onsets, onset_ll_vms, p_blind, rng):
    """LL generator — uses GLOBAL suffix for non-blind LL (unchanged from exp_231/232)."""
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return make_word_sim(onset, 'am', rng)
    onset  = rng.choices(list(onset_ll_vms.keys()), weights=list(onset_ll_vms.values()))[0]
    suffix = rng.choices(list(suffix_global.keys()), weights=list(suffix_global.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_lf_vms(onset_weights, suffix_lf, onset_lf_vms, p_lf, rng):
    """LF generator — uses suffix_lf (LF-specific suppressed suffix)."""
    if rng.random() < p_lf:
        onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
        suffix = rng.choices(list(suffix_lf.keys()), weights=list(suffix_lf.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_weights, suffix_lf, rng)

def timm_modify_edy_preserving_fresh_fallback(word, onset_weights, suffix_mid, rng):
    """Modification: onset-preserving, edy-suffix-preserving, fresh-fallback.
    Fresh fallback uses suffix_mid (MID-specific suppressed suffix)."""
    if not word: return word
    onset_len = get_onset_len(word)
    edy_len   = get_edy_suffix_len(word)
    mod_start = onset_len
    mod_end   = len(word) - edy_len
    if mod_start >= mod_end:
        return random_eva_word(onset_weights, suffix_mid, rng)
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

def run_sim(latin_words, onset_weights_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms, cp, mp, p_qokch, p_stutter, rng):
    """
    suffix_lf_sup:  used for LF fresh words only (r_lf applied)
    suffix_mid_sup: used for fresh MID words and edy fresh-fallback (r_mid applied)
    suffix_global:  used for LL non-blind fraction (unchanged)
    """
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
                # LF: use LF-specific suppressed suffix
                ew = cipher_lf_vms(onset_weights_mid, suffix_lf_sup, onset_lf_vms, P_LF, rng)
            elif i == len(chunk)-1:
                # LL: unchanged — uses global suffix for non-blind fraction
                ew = cipher_ll_blind_fixed(onset_weights_mid, suffix_global, ll_onsets,
                                           onset_ll_vms, P_BLIND, rng)
            else:
                if prev_word is not None and p_stutter > 0 and rng.random() < p_stutter:
                    ew = prev_word
                elif buf and rng.random() < cp:
                    src = draw_from_buffer(buf, prev_onset, p_qokch, rng)
                    if rng.random() < mp:
                        # Fresh fallback in edy modification uses MID-specific suppressed suffix
                        ew = timm_modify_edy_preserving_fresh_fallback(
                            src, onset_weights_mid, suffix_mid_sup, rng)
                    else:
                        ew = src
                else:
                    # Fresh MID: use MID-specific suppressed suffix
                    ew = random_eva_word(onset_weights_mid, suffix_mid_sup, rng)
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

    lf_am_rate  = sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf else 0
    mid_am_rate = sum(1 for w in mid if w.endswith('am'))/n_mid if n_mid else 0
    am_lf_enr   = lf_am_rate  / am_r if am_r else 0
    am_mid_enr  = mid_am_rate / am_r if am_r else 0

    edy_rate   = sum(1 for w in aw if w.endswith('edy'))/n
    word_len   = sum(len(w) for w in aw)/n
    qok_r  = oc_all.get('qok', 0)/n
    ch_r   = oc_all.get('ch', 0)/n
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    global_am_pct = am_r * 100
    lf_am_pct     = lf_am_rate * 100
    mid_am_pct    = mid_am_rate * 100
    ll_am_pct     = ll_am * 100

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch,
                _global_am=global_am_pct, _lf_am=lf_am_pct,
                _mid_am=mid_am_pct, _ll_am=ll_am_pct)

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

# ─── Setup ────────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus...")
vms_b_lines = parse_vms_corpus()
vms = compute_vms_distributions(vms_b_lines)
print(f"  VMS B: {len(vms_b_lines)} lines, {vms['n']} words")

d_global    = vms['onset_global'].get('d', 0)
d_ll_target = vms['d_ll_target']
onset_ll_vms = dict(vms['onset_ll'])

vms_ll_d_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0
d_boost_new = compute_d_boost_fixed(d_global, d_ll_target, vms_ll_d_enr, P_BLIND)

ll_onsets    = build_ll_onsets_fixed(onset_ll_vms, d_boost_new)
onset_lf_vms = dict(vms['onset_lf'])
suffix_global = dict(vms['suffix_global'])
onset_weights_mid = dict(vms['onset_mid'])

# VMS reference for am_lf_enr
lf_words_vms = [l[0] for l in vms_b_lines if l]
vms_lf_am_rate = sum(1 for w in lf_words_vms if w.endswith('am')) / len(lf_words_vms)
vms_am_lf_enr  = vms_lf_am_rate / vms['am_r']

print(f"\n  VMS am rates:")
print(f"    Global am = {vms['am_r']*100:.2f}%")
print(f"    LF am rate = {vms_lf_am_rate*100:.3f}%  → am_lf_enr = {vms_am_lf_enr:.3f}")
print(f"    am_ll target = {vms['am_ll_target']:.3f}")
print(f"  Global suffix -am weight = {suffix_global.get('am',0)*100:.2f}%")
print(f"  d_boost = {d_boost_new*100:.2f}%")
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
    'am_lf_enr':   vms_am_lf_enr,
    'am_mid_enr':  0.195,
    'edy_rate':    sum(vms['suffix_global'].get(s,0) for s in ['edy','eedy']),
    'word_len_mean': 5.400,
    'qok_ch':      1.267,
}

EXP231_REF = {
    'am_ll': 6.203, 'd_ll': 1.420, 'y_lf': 3.493, 'ss_mean': 1.354, 'adj_rate': 0.010,
    'qok_lf': 0.771, 'd_lf': 2.265, 's_lf': 4.851, 'ch_ll': 0.858, 'ok_ll': 0.988,
    'qok_ll': 0.593, 'ss_d': 1.505, 'ss_y': 1.858, 'am_lf_enr': 0.407, 'am_mid_enr': 0.281,
    'edy_rate': 0.187, 'word_len_mean': 6.628, 'qok_ch': 1.189,
}

PASS_TOL = 0.20
METRIC_LABELS = [
    ('am_ll', 'CALIBRATED'), ('d_ll', 'CALIBRATED'), ('y_lf', 'VMS-DIRECT'),
    ('ss_mean', 'CALIBRATED (cp/mp)'), ('adj_rate', 'TARGET METRIC'),
    ('qok_lf', 'VMS-DIRECT'), ('d_lf', 'VMS-DIRECT'), ('s_lf', 'VMS-DIRECT'),
    ('ch_ll', 'VMS-DIRECT'), ('ok_ll', 'VMS-DIRECT'), ('qok_ll', 'TARGET METRIC'),
    ('ss_d', 'uncalibrated'), ('ss_y', 'uncalibrated'), ('am_lf_enr', 'uncalibrated'),
    ('am_mid_enr', 'uncalibrated'), ('edy_rate', 'TARGET METRIC'),
    ('word_len_mean', 'uncalibrated'), ('qok_ch', 'TARGET METRIC'),
]

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

# ─── Differential Suppression Sweep ──────────────────────────────────────────

R_LF_VALUES  = [0.25, 0.33, 0.40]
R_MID_VALUES = [0.60, 0.70, 0.80]
SWEEP_GRID   = [(r_lf, r_mid) for r_lf in R_LF_VALUES for r_mid in R_MID_VALUES]

print(f"{'='*100}")
print(f"DIFFERENTIAL SUPPRESSION SWEEP: r_lf ∈ {R_LF_VALUES}, r_mid ∈ {R_MID_VALUES}")
print(f"N={N_SWEEP} per (r_lf, r_mid) combination = {len(SWEEP_GRID)} combinations")
print(f"{'='*100}")
print(f"  {'r_lf':>5} {'r_mid':>5} {'am_lf_enr':>10} {'%VMS':>7} {'P?':>3} {'am_mid_enr':>11} {'%VMS':>7} {'P?':>3} {'am_ll':>7} {'%VMS':>7} {'P?':>3} {'ss_mean':>8} {'P?':>3}")

sweep_results = {}
for r_lf, r_mid in SWEEP_GRID:
    suffix_lf_sup  = make_suppressed_suffix(suffix_global, r_lf)
    suffix_mid_sup = make_suppressed_suffix(suffix_global, r_mid)
    metrics = []
    for i in range(N_SWEEP):
        seed_val = SEED + 10000 + int(r_lf*1000)*100 + int(r_mid*1000) + i
        rng = random.Random(seed_val)
        lines = run_sim(latin, onset_weights_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf_vms, onset_ll_vms, CP, MP, P_QOKCH, P_STUTTER, rng)
        m = compute_metrics(lines, vms)
        if m: metrics.append(m)
    sweep_results[(r_lf, r_mid)] = metrics
    if not metrics: continue

    m_alf  = sum(x['am_lf_enr']  for x in metrics)/len(metrics)
    m_amid = sum(x['am_mid_enr'] for x in metrics)/len(metrics)
    m_all  = sum(x['am_ll']      for x in metrics)/len(metrics)
    m_ss   = sum(x['ss_mean']    for x in metrics)/len(metrics)
    valf   = VMS_REF['am_lf_enr'];  vamid = VMS_REF['am_mid_enr']
    vall   = VMS_REF['am_ll'];      vss   = VMS_REF['ss_mean']

    p_alf  = 'P' if abs(m_alf -valf )/abs(valf ) <= PASS_TOL else 'F'
    p_amid = 'P' if abs(m_amid-vamid)/abs(vamid) <= PASS_TOL else 'F'
    p_all  = 'P' if abs(m_all -vall )/abs(vall ) <= PASS_TOL else 'F'
    p_ss   = 'P' if abs(m_ss  -vss  )/abs(vss  ) <= PASS_TOL else 'F'

    print(f"  {r_lf:>5.2f} {r_mid:>5.2f} {m_alf:>10.3f} {m_alf/valf*100:>6.1f}% {p_alf:>3}  {m_amid:>10.3f} {m_amid/vamid*100:>6.1f}% {p_amid:>3}  {m_all:>7.3f} {m_all/vall*100:>6.1f}% {p_all:>3}  {m_ss:>8.3f} {p_ss:>3}")

# ─── Select best (r_lf, r_mid) ───────────────────────────────────────────────

def score_combo(combo):
    metrics = sweep_results.get(combo, [])
    if not metrics: return float('inf'), float('inf')
    m_alf  = sum(x['am_lf_enr']  for x in metrics)/len(metrics)
    m_amid = sum(x['am_mid_enr'] for x in metrics)/len(metrics)
    m_all  = sum(x['am_ll']      for x in metrics)/len(metrics)
    valf   = VMS_REF['am_lf_enr']
    vamid  = VMS_REF['am_mid_enr']
    vall   = VMS_REF['am_ll']

    # Check both -am metrics are in pass zones and am_ll doesn't fail
    alf_pass  = abs(m_alf  - valf ) / abs(valf ) <= PASS_TOL
    amid_pass = abs(m_amid - vamid) / abs(vamid) <= PASS_TOL
    all_pass  = abs(m_all  - vall ) / abs(vall ) <= PASS_TOL

    # Primary score: combined normalized distance from VMS targets
    combined_dist = (m_alf/valf - 1)**2 + (m_amid/vamid - 1)**2

    if alf_pass and amid_pass and all_pass:
        return 0, combined_dist  # tier 0: all three pass
    elif alf_pass and amid_pass:
        return 1, combined_dist  # tier 1: both am metrics pass (am_ll might fail)
    elif alf_pass or amid_pass:
        return 2, combined_dist  # tier 2: one of two passes
    else:
        return 3, combined_dist  # tier 3: neither passes

scored = [(score_combo(combo), combo) for combo in SWEEP_GRID]
scored.sort(key=lambda x: (x[0][0], x[0][1]))
best_combo = scored[0][1]
best_tier  = scored[0][0][0]

print()
print(f"  Best combo: r_lf={best_combo[0]}, r_mid={best_combo[1]}")
tier_labels = {0: 'both am metrics PASS + am_ll PASS', 1: 'both am metrics PASS', 2: 'one am metric passes', 3: 'neither am metric passes'}
print(f"  Selection tier: {best_tier} ({tier_labels.get(best_tier, '?')})")

# ─── Full Run ─────────────────────────────────────────────────────────────────

r_lf_best, r_mid_best = best_combo
suffix_lf_best  = make_suppressed_suffix(suffix_global, r_lf_best)
suffix_mid_best = make_suppressed_suffix(suffix_global, r_mid_best)

print()
print(f"{'='*105}")
print(f"FULL RUN: N={N_FULL} at r_lf={r_lf_best}, r_mid={r_mid_best}")
print(f"{'='*105}")
print(f"  LF suppressed suffix -am weight:  {suffix_lf_best.get('am',0)*100:.3f}%  (global = {suffix_global.get('am',0)*100:.2f}%)")
print(f"  MID suppressed suffix -am weight: {suffix_mid_best.get('am',0)*100:.3f}%  (global = {suffix_global.get('am',0)*100:.2f}%)")

full_metrics = []
for i in range(N_FULL):
    rng = random.Random(SEED + i)
    lines = run_sim(latin, onset_weights_mid, suffix_global, suffix_lf_best, suffix_mid_best,
                    ll_onsets, onset_lf_vms, onset_ll_vms, CP, MP, P_QOKCH, P_STUTTER, rng)
    m = compute_metrics(lines, vms)
    if m: full_metrics.append(m)

print(f"  Completed {len(full_metrics)} simulations.")
print()

pass_count = 0; total = 0
print(f"  {'Metric':<16} {'VMS':>8} {'E233':>8} {'%':>7} {'P?':<4}  E231    delta")
print(f"  {'-'*80}")
for key, cat in METRIC_LABELS:
    vms_val = VMS_REF.get(key)
    if vms_val is None: continue
    sim_mean, ci_lo, ci_hi = agg(full_metrics, key)
    pct = sim_mean/vms_val*100 if abs(vms_val)>1e-6 else float('inf')
    pass_f = abs(sim_mean-vms_val)/abs(vms_val) <= PASS_TOL if abs(vms_val)>1e-6 else abs(sim_mean)<0.002
    status = 'P' if pass_f else 'F'
    e231 = EXP231_REF.get(key, float('nan'))
    delta = sim_mean - e231
    print(f"  {key:<16} {vms_val:>8.3f} {sim_mean:>8.3f} {pct:>6.1f}% {status}    {e231:>7.3f}  {delta:>+7.3f}  [{cat}]")
    total += 1
    if pass_f: pass_count += 1

print()
print(f"  Pass count:  E233={pass_count}/{total}  |  E231 (baseline)=15/18")
print()

# Diagnostic: actual am rates by position
g_am  = sum(x['_global_am'] for x in full_metrics)/len(full_metrics)
lf_am = sum(x['_lf_am']     for x in full_metrics)/len(full_metrics)
mid_am= sum(x['_mid_am']    for x in full_metrics)/len(full_metrics)
ll_am = sum(x['_ll_am']     for x in full_metrics)/len(full_metrics)

print(f"  -am rate diagnostics (r_lf={r_lf_best}, r_mid={r_mid_best}):")
print(f"    Global am = {g_am:.2f}% (VMS global = {vms['am_r']*100:.2f}%)")
print(f"    LF am     = {lf_am:.3f}% (VMS LF ≈ {vms_lf_am_rate*100:.3f}%)")
print(f"    MID am    = {mid_am:.3f}%")
print(f"    LL am     = {ll_am:.2f}%")
print(f"    Derived am_lf_enr  = {lf_am/g_am:.3f}  (VMS = {VMS_REF['am_lf_enr']:.3f})")
print(f"    Derived am_mid_enr = {mid_am/g_am:.3f}  (VMS = {VMS_REF['am_mid_enr']:.3f})")
print()

# ss_mean safety check
ss_m, _, _ = agg(full_metrics, 'ss_mean')
ss_upper = 1.164 * 1.20
print(f"  ss_mean safety check: {ss_m:.3f} (upper bound = {ss_upper:.3f}, margin = {ss_upper-ss_m:.3f})")
print()

print(f"  Key comparisons (exp_231 vs exp_233):")
for k in ['am_lf_enr', 'am_mid_enr', 'am_ll', 'ss_mean', 'adj_rate', 'edy_rate', 'ss_d']:
    vv = VMS_REF[k]
    m233, _, _ = agg(full_metrics, k)
    m231 = EXP231_REF[k]
    p233 = 'P' if abs(m233-vv)/abs(vv) <= PASS_TOL else 'F'
    p231 = 'P' if abs(m231-vv)/abs(vv) <= PASS_TOL else 'F'
    print(f"    {k:<16}: VMS={vv:.4f}  E231={m231:.4f}[{p231}]  E233={m233:.4f}[{p233}]  delta={m233-m231:+.4f}")

print()
print("Done.")
