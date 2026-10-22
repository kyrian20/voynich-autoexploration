"""
exp_234: H434 — edy-Conditional Connector

Motivation:
  exp_233 achieves 17/18 PASS with 1 remaining failure:
  - word_len_mean = 6.627 (122.7% FAIL; VMS = 5.400, pass zone [4.320, 6.480])

  Root cause: the generation model uses onset + connector + suffix for ALL words.
  The connector (['a','ai','o','oi','e','ei'], avg 1.5 chars) adds ~1.2 chars beyond
  what VMS words average.

  exp_227 showed that removing the connector entirely (onset+suffix only) FIXES
  word_len (6.637→5.118, 94.8% PASS) but BREAKS edy_rate (96.4%→63.4% FAIL).
  Root cause of exp_227 failure: without a connector, words like onset+'edy' have
  mod_start >= mod_end → no modifiable middle region → timm_modify triggers fresh
  fallback for ALL edy words → edy_rate collapses.

  Key insight: the connector is ONLY needed to create the modifiable middle region
  for edy-suffix words (the Timm modification erases edy endings if it modifies the
  suffix, so we protect edy by restricting modification to the connector region).
  NON-edy words do NOT need the connector: their suffix can be modified directly
  (the modification doesn't destroy anything structurally required).

  Fix (this experiment):
  Make connector presence conditional on the suffix:
    - If suffix ∈ {'edy', 'eedy'}: use connector (onset + connector + edy suffix)
      → preserves modifiable middle region for edy words
    - Otherwise: NO connector (onset + suffix directly)
      → shorter words for ~80% of vocabulary

  Analytical prediction:
    P(edy/eedy) ≈ 0.194 (current edy_rate)
    For edy words: same length as current (onset + connector + edy)
    For non-edy words: remove connector (save ~1.5 chars)
    Expected word_len = 6.627 - (1 - 0.194) × 1.5 = 6.627 - 1.209 = 5.418
    → PASS [4.320, 6.480] ← within pass zone

  All other parameters identical to exp_233:
  cp=0.55, mp=0.90, p_blind=0.30, p_lf=1.0, p_qokch=0.12, p_stutter=0.009,
  d_boost=9.13%, VMS LL onset for non-blind LL, r_lf=0.25, r_mid=0.60.

  Question: Does edy-conditional connector (connector only for edy words) fix
  word_len_mean (122.7%→PASS) without regressing any of the 17 currently passing
  metrics from exp_233?
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_FULL   = 30
TARGET_LINES = 2447
WINDOW   = 20
SEED     = 234000

P_BLIND   = 0.30
P_LF      = 1.0
CP        = 0.55
MP        = 0.90
P_QOKCH   = 0.12
P_STUTTER = 0.009
R_LF      = 0.25   # from exp_233
R_MID     = 0.60   # from exp_233

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

# KEY CHANGE: connector is conditional on suffix type
def make_word_sim(onset, suffix, rng):
    """
    Generate a simulated EVA word.
    If suffix is edy/eedy: include connector (preserves modifiable middle region).
    Otherwise: no connector (onset + suffix directly, shorter words).
    """
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
        return onset + connector + suffix
    else:
        return onset + suffix

def random_eva_word(onset_weights, suffix_weights, rng):
    onset  = rng.choices(list(onset_weights.keys()),  weights=list(onset_weights.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_ll_blind_fixed(onset_weights_mid, suffix_global, ll_onsets, onset_ll_vms, p_blind, rng):
    """LL generator — uses GLOBAL suffix for non-blind LL."""
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        # Blind LL: always -am suffix (no connector needed — just onset + 'am')
        return onset + 'am'
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
    """Modification: onset-preserving, edy-suffix-preserving, fresh-fallback."""
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
                ew = cipher_lf_vms(onset_weights_mid, suffix_lf_sup, onset_lf_vms, P_LF, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_blind_fixed(onset_weights_mid, suffix_global, ll_onsets,
                                           onset_ll_vms, P_BLIND, rng)
            else:
                if prev_word is not None and p_stutter > 0 and rng.random() < p_stutter:
                    ew = prev_word
                elif buf and rng.random() < cp:
                    src = draw_from_buffer(buf, prev_onset, p_qokch, rng)
                    if rng.random() < mp:
                        ew = timm_modify_edy_preserving_fresh_fallback(
                            src, onset_weights_mid, suffix_mid_sup, rng)
                    else:
                        ew = src
                else:
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

lf_words_vms = [l[0] for l in vms_b_lines if l]
vms_lf_am_rate = sum(1 for w in lf_words_vms if w.endswith('am')) / len(lf_words_vms)
vms_am_lf_enr  = vms_lf_am_rate / vms['am_r']

suffix_lf_sup  = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)

print(f"\n  VMS am rates:")
print(f"    Global am = {vms['am_r']*100:.2f}%")
print(f"    LF am rate = {vms_lf_am_rate*100:.3f}%  → am_lf_enr = {vms_am_lf_enr:.3f}")
print(f"    am_ll target = {vms['am_ll_target']:.3f}")
print(f"  d_boost = {d_boost_new*100:.2f}%")
print(f"  r_lf = {R_LF}, r_mid = {R_MID}")
print(f"  KEY CHANGE: connector used only for edy/eedy suffix words")
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

EXP233_REF = {
    'am_ll': 7.023, 'd_ll': 1.404, 'y_lf': 3.466, 'ss_mean': 1.368, 'adj_rate': 0.010,
    'qok_lf': 0.787, 'd_lf': 2.273, 's_lf': 4.918, 'ch_ll': 0.862, 'ok_ll': 0.987,
    'qok_ll': 0.616, 'ss_d': 1.522, 'ss_y': 1.919, 'am_lf_enr': 0.115, 'am_mid_enr': 0.198,
    'edy_rate': 0.189, 'word_len_mean': 6.627, 'qok_ch': 1.194,
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

# Predict expected word_len from edy_rate diagnostic
print("  Analytical prediction for word_len_mean:")
print(f"    exp_233 word_len = 6.627")
print(f"    exp_233 edy_rate ≈ 0.189 (fraction of words with connector)")
print(f"    connector removal saves ~1.5 chars for (1-0.189) = 81.1% of words")
print(f"    expected reduction = 0.811 × 1.5 = {0.811 * 1.5:.3f} chars")
print(f"    predicted word_len = 6.627 - {0.811*1.5:.3f} = {6.627 - 0.811*1.5:.3f}")
print()

# ─── Full Run ─────────────────────────────────────────────────────────────────

print(f"{'='*105}")
print(f"FULL RUN: N={N_FULL} — edy-conditional connector")
print(f"{'='*105}")

full_metrics = []
for i in range(N_FULL):
    rng = random.Random(SEED + i)
    lines = run_sim(latin, onset_weights_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf_vms, onset_ll_vms, CP, MP, P_QOKCH, P_STUTTER, rng)
    m = compute_metrics(lines, vms)
    if m: full_metrics.append(m)

print(f"  Completed {len(full_metrics)} simulations.")
print()

pass_count = 0; total = 0
print(f"  {'Metric':<16} {'VMS':>8} {'E234':>8} {'%':>7} {'P?':<4}  E233    delta")
print(f"  {'-'*80}")
for key, cat in METRIC_LABELS:
    vms_val = VMS_REF.get(key)
    if vms_val is None: continue
    sim_mean, ci_lo, ci_hi = agg(full_metrics, key)
    pct = sim_mean/vms_val*100 if abs(vms_val)>1e-6 else float('inf')
    pass_f = abs(sim_mean-vms_val)/abs(vms_val) <= PASS_TOL if abs(vms_val)>1e-6 else abs(sim_mean)<0.002
    status = 'P' if pass_f else 'F'
    e233 = EXP233_REF.get(key, float('nan'))
    delta = sim_mean - e233
    print(f"  {key:<16} {vms_val:>8.3f} {sim_mean:>8.3f} {pct:>6.1f}% {status}    {e233:>7.3f}  {delta:>+7.3f}  [{cat}]")
    total += 1
    if pass_f: pass_count += 1

print()
print(f"  Pass count:  E234={pass_count}/{total}  |  E233 (baseline)=17/18")
print()

# Diagnostics
g_am  = sum(x['_global_am'] for x in full_metrics)/len(full_metrics)
lf_am = sum(x['_lf_am']     for x in full_metrics)/len(full_metrics)
mid_am= sum(x['_mid_am']    for x in full_metrics)/len(full_metrics)
ll_am_d = sum(x['_ll_am']   for x in full_metrics)/len(full_metrics)

print(f"  -am rate diagnostics:")
print(f"    Global am = {g_am:.2f}% (VMS global = {vms['am_r']*100:.2f}%)")
print(f"    LF am     = {lf_am:.3f}% (VMS LF ≈ {vms_lf_am_rate*100:.3f}%)")
print(f"    MID am    = {mid_am:.3f}%")
print(f"    LL am     = {ll_am_d:.2f}%")
print(f"    Derived am_lf_enr  = {lf_am/g_am:.3f}  (VMS = {VMS_REF['am_lf_enr']:.3f})")
print(f"    Derived am_mid_enr = {mid_am/g_am:.3f}  (VMS = {VMS_REF['am_mid_enr']:.3f})")
print()

ss_m, _, _ = agg(full_metrics, 'ss_mean')
ss_upper = 1.164 * 1.20
print(f"  ss_mean safety check: {ss_m:.3f} (upper bound = {ss_upper:.3f}, margin = {ss_upper-ss_m:.3f})")
print()

wl_m, _, _ = agg(full_metrics, 'word_len_mean')
print(f"  word_len_mean: {wl_m:.3f} (VMS = 5.400, pass zone [4.320, 6.480])")
print(f"  edy_rate: {sum(x['edy_rate'] for x in full_metrics)/len(full_metrics):.3f} (VMS = {VMS_REF['edy_rate']:.3f})")
print()

print(f"  Key comparisons (exp_233 vs exp_234):")
for k in ['word_len_mean', 'edy_rate', 'am_lf_enr', 'am_mid_enr', 'am_ll', 'ss_mean', 'ss_d', 'adj_rate']:
    vv = VMS_REF[k]
    m234, _, _ = agg(full_metrics, k)
    m233 = EXP233_REF[k]
    p234 = 'P' if abs(m234-vv)/abs(vv) <= PASS_TOL else 'F'
    p233 = 'P' if abs(m233-vv)/abs(vv) <= PASS_TOL else 'F'
    print(f"    {k:<16}: VMS={vv:.4f}  E233={m233:.4f}[{p233}]  E234={m234:.4f}[{p234}]  delta={m234-m233:+.4f}")

print()
print("Done.")
