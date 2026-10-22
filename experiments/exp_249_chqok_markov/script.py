"""
exp_249: H454 — p_chqok Architecture Extension: Full 19-Metric Battery Test

Question: Does adding p_chqok parameter to draw_from_buffer (when prev_onset='ch',
with prob p_chqok, seek qok-onset word from buffer) pass the 19-metric battery?

exp_248 sweep results (N=10):
  p_chqok=0.10: ch→qok E2=1.194 (VMS=1.147), qok→ch E2=1.196 (VMS=1.234, improved from 1.162),
                qok→qok E2=1.191 (VMS=1.169, improved from 1.335)
  p_chqok=0.05: ch→qok E2=1.073 (slightly below VMS)
  VMS: ch→qok=1.147, qok→ch=1.234

Plan: Sweep p_chqok ∈ {0.05, 0.08, 0.10, 0.12} at N=5, check 19/19 PASS.
      Run best at N=30 (same threshold as exp_236: 19/19 to be confirmed).
      Also compute ch→qok MID-only E2 and qok→ch→qok 2nd_order for verification.

Base architecture: exp_236 (19/19 B-dialect PASS confirmed).
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SWEEP  = 5
N_FULL   = 30
TARGET_LINES = 2447
WINDOW   = 20
SEED     = 249000

# Fixed exp_236 architecture parameters
P_BLIND  = 0.115; P_LF = 1.0; CP = 0.55; MP = 0.90; P_QOKCH = 0.12; P_STUTTER = 0.006
R_LF = 0.12; R_MID = 0.25

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
            if folio_dialect.get(fb, 'unknown') != 'B': continue
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
    n = len(all_words); n_mid = len(mid_words)
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
            if w.endswith(suf): suf_ctr[suf] += 1; matched = True; break
        if not matched: suf_ctr['other'] += 1
    suffix_global = {suf: cnt/n for suf, cnt in suf_ctr.items()}
    am_r  = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words)
    d_r   = oc_all.get('d', 0) / n
    ll_d  = oc_ll.get('d', 0) / len(ll_words)
    return {
        'onset_global': onset_global, 'onset_lf': onset_lf,
        'onset_ll': onset_ll, 'onset_mid': onset_mid,
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
        if suf == 'am': suppressed[suf] = new_am
        else: suppressed[suf] = w + (w / non_am_total) * delta if non_am_total > 0 else w
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
        connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
        return onset + connector + suffix
    return onset + suffix

def random_eva_word(onset_weights, suffix_weights, rng):
    onset  = rng.choices(list(onset_weights.keys()),  weights=list(onset_weights.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_ll_blind_fixed(onset_weights_mid, suffix_global, ll_onsets, onset_ll_vms, p_blind, rng):
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return onset + 'am'
    onset  = rng.choices(list(onset_ll_vms.keys()), weights=list(onset_ll_vms.values()))[0]
    suffix = rng.choices(list(suffix_global.keys()), weights=list(suffix_global.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_lf_vms(onset_weights, suffix_lf, onset_lf_vms, p_lf, rng):
    if rng.random() < p_lf:
        onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
        suffix = rng.choices(list(suffix_lf.keys()), weights=list(suffix_lf.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_weights, suffix_lf, rng)

def timm_modify_edy_preserving_fresh_fallback(word, onset_weights, suffix_mid, rng):
    if not word: return word
    onset_len = get_onset_len(word); edy_len = get_edy_suffix_len(word)
    mod_start = onset_len; mod_end = len(word) - edy_len
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
            return word[:mod_start] + rng.choice(EVA_CHARS) + word[mod_start+1:]
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + word[pos+1:]

def draw_from_buffer(buf, prev_onset, p_qokch, p_chqok, rng):
    """Draw from buffer with optional qok→ch and ch→qok Markov biases."""
    buf_list = list(buf)
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words: return rng.choice(ch_words)
    if prev_onset == 'ch' and p_chqok > 0 and rng.random() < p_chqok:
        qok_words = [w for w in buf_list if get_onset(w) == 'qok']
        if qok_words: return rng.choice(qok_words)
    return rng.choice(buf_list)

def run_sim(latin_words, onset_weights_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms, p_blind, p_chqok, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
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
                                           onset_ll_vms, p_blind, rng)
            else:
                if prev_word is not None and P_STUTTER > 0 and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_from_buffer(buf, prev_onset, P_QOKCH, p_chqok, rng)
                    if rng.random() < MP:
                        ew = timm_modify_edy_preserving_fresh_fallback(
                            src, onset_weights_mid, suffix_mid_sup, rng)
                    else:
                        ew = src
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def compute_metrics(lines, vms):
    aw  = [w for l in lines for w in l]; n = len(aw)
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

    qok_lf = enr('qok', oc_lf, n_lf, oc_all, n); d_lf = enr('d', oc_lf, n_lf, oc_all, n)
    s_lf   = enr('s',   oc_lf, n_lf, oc_all, n); ch_ll = enr('ch', oc_ll, n_ll, oc_all, n)
    ok_ll  = enr('ok',  oc_ll, n_ll, oc_all, n); qok_ll = enr('qok', oc_ll, n_ll, oc_all, n)
    ss_d   = ss('d'); ss_y = ss('y')

    lf_am_rate  = sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf else 0
    mid_am_rate = sum(1 for w in mid if w.endswith('am'))/n_mid if n_mid else 0
    am_lf_enr   = lf_am_rate  / am_r if am_r else 0
    am_mid_enr  = mid_am_rate / am_r if am_r else 0

    edy_rate = sum(1 for w in aw if w.endswith('edy'))/n
    word_len = sum(len(w) for w in aw)/n
    qok_r = oc_all.get('qok', 0)/n; ch_r = oc_all.get('ch', 0)/n
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    # Extra: MID-only ch→qok E2 and qok→qok E2
    oc_mid = Counter(get_onset(w) for w in mid)
    n_m = len(mid)
    mid_bg = Counter()
    mid_bg_n = 0
    for line in lines:
        nn = len(line)
        if nn < 4: continue
        for i in range(1, nn-2):
            mid_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1
            mid_bg_n += 1
    def E2_mid(x, y):
        pxy = mid_bg.get((x,y),0)/mid_bg_n if mid_bg_n>0 else 0
        px = oc_mid.get(x,0)/n_m if n_m>0 else 0
        py = oc_mid.get(y,0)/n_m if n_m>0 else 0
        return pxy/(px*py) if px*py>0 else 0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch, global_am_rate=am_r,
                _ch_qok_mid=E2_mid('ch','qok'),
                _qok_qok_mid=E2_mid('qok','qok'),
                _qok_ch_mid=E2_mid('qok','ch'))

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

def agg_mean(metrics_list, key):
    vals = [x[key] for x in metrics_list]
    return sum(vals)/len(vals) if vals else 0

# ─── VMS Reference ────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus...")
vms_b_lines = parse_vms_corpus()
vms = compute_vms_distributions(vms_b_lines)
print(f"  VMS B: {len(vms_b_lines)} lines, {vms['n']} words")

d_global    = vms['onset_global'].get('d', 0)
d_ll_target = vms['d_ll_target']
onset_ll_vms = dict(vms['onset_ll'])
vms_ll_d_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0
d_boost_new = compute_d_boost_fixed(d_global, d_ll_target, vms_ll_d_enr, P_BLIND)
ll_onsets     = build_ll_onsets_fixed(onset_ll_vms, d_boost_new)
onset_lf_vms  = dict(vms['onset_lf'])
suffix_global  = dict(vms['suffix_global'])
onset_weights_mid = dict(vms['onset_mid'])

lf_words_vms = [l[0] for l in vms_b_lines if l]
vms_lf_am_rate = sum(1 for w in lf_words_vms if w.endswith('am')) / len(lf_words_vms)
vms_am_lf_enr  = vms_lf_am_rate / vms['am_r']

suffix_lf_sup  = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)

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
    'global_am_rate': vms['am_r'],
}
PASS_TOL = 0.20
BATTERY_KEYS = ['am_ll','d_ll','y_lf','ss_mean','adj_rate','qok_lf','d_lf','s_lf',
                'ch_ll','ok_ll','qok_ll','ss_d','ss_y','am_lf_enr','am_mid_enr',
                'edy_rate','word_len_mean','qok_ch','global_am_rate']

def count_passes(metrics, vms_ref):
    passes = 0
    for k in BATTERY_KEYS:
        v = metrics.get(k, 0); t = vms_ref.get(k, 0)
        if t > 0 and abs(v/t - 1) <= PASS_TOL: passes += 1
    return passes

def print_battery(metrics, vms_ref, label=''):
    passes = 0
    print(f"\n  {'Metric':<18} {'VMS':>8} {'Sim':>8} {'%VMS':>7} {'PASS':>5}")
    print(f"  {'-'*50}")
    for k in BATTERY_KEYS:
        v = metrics.get(k, 0); t = vms_ref.get(k, 0)
        pct = 100*v/t if t>0 else 0
        ok = 'PASS' if t>0 and abs(v/t-1)<=PASS_TOL else 'FAIL'
        if ok=='PASS': passes+=1
        flag = '*' if ok=='FAIL' else ''
        print(f"  {k:<18} {t:>8.4f} {v:>8.4f} {pct:>7.1f}% {ok:>5}{flag}")
    print(f"\n  TOTAL: {passes}/{len(BATTERY_KEYS)} PASS")
    if label: print(f"  Label: {label}")
    return passes

print(f"\nVMS B-dialect reference computed.")

# ─── Latin corpus ─────────────────────────────────────────────────────────────

print("Loading Latin corpus...")
latin_words = load_latin(LATIN_CORPUS)
print(f"  {len(latin_words)} Latin words")

# ─── Sweep at N=5 ─────────────────────────────────────────────────────────────

SWEEP_VALUES = [0.00, 0.05, 0.08, 0.10, 0.12]
print(f"\n{'='*70}")
print(f"SWEEP p_chqok ∈ {SWEEP_VALUES}, N={N_SWEEP} trials each")
print(f"{'='*70}")
print(f"\n  {'p_chqok':>8}  {'Pass/19':>7}  {'qok_ch%':>8}  {'ch→qok_m':>10}  {'qok→ch_m':>10}  {'qok→qok_m':>11}")
print(f"  {'---':>8}  {'---':>7}  {'---':>8}  {'---':>10}  {'---':>10}  {'---':>11}")

sweep_results = []
for p_chqok in SWEEP_VALUES:
    all_metrics = []
    for trial in range(N_SWEEP):
        rng = random.Random(SEED + trial * 100 + int(p_chqok * 1000))
        lines = run_sim(latin_words, onset_weights_mid, suffix_global,
                        suffix_lf_sup, suffix_mid_sup, ll_onsets,
                        onset_lf_vms, onset_ll_vms, P_BLIND, p_chqok, rng)
        m = compute_metrics(lines, vms)
        if m: all_metrics.append(m)

    avg_metrics = {k: agg_mean(all_metrics, k) for k in all_metrics[0]} if all_metrics else {}
    passes = count_passes(avg_metrics, VMS_REF)
    qok_ch_pct = 100 * avg_metrics.get('qok_ch', 0) / VMS_REF['qok_ch'] if VMS_REF['qok_ch'] > 0 else 0
    ch_qok_mid = avg_metrics.get('_ch_qok_mid', 0)
    qok_ch_mid = avg_metrics.get('_qok_ch_mid', 0)
    qok_qok_mid = avg_metrics.get('_qok_qok_mid', 0)
    print(f"  {p_chqok:>8.2f}  {passes:>5}/{len(BATTERY_KEYS)}  {qok_ch_pct:>7.1f}%  "
          f"{ch_qok_mid:>10.3f}  {qok_ch_mid:>10.3f}  {qok_qok_mid:>11.3f}")
    sweep_results.append((p_chqok, passes, avg_metrics))

# VMS MID reference
all_mid_vms = [w for l in vms_b_lines for w in l[1:-1] if len(l) > 2]
n_mid_vms = len(all_mid_vms)
mid_bg_vms = Counter()
mid_bg_n_vms = 0
for line in vms_b_lines:
    nn = len(line)
    if nn < 4: continue
    for i in range(1, nn-2):
        mid_bg_vms[(get_onset(line[i]), get_onset(line[i+1]))] += 1
        mid_bg_n_vms += 1
oc_mid_vms = Counter(get_onset(w) for w in all_mid_vms)
def E2_vms_mid(x, y):
    pxy = mid_bg_vms.get((x,y),0)/mid_bg_n_vms if mid_bg_n_vms>0 else 0
    px = oc_mid_vms.get(x,0)/n_mid_vms if n_mid_vms>0 else 0
    py = oc_mid_vms.get(y,0)/n_mid_vms if n_mid_vms>0 else 0
    return pxy/(px*py) if px*py>0 else 0
print(f"\n  VMS MID reference: ch→qok={E2_vms_mid('ch','qok'):.3f}, "
      f"qok→ch={E2_vms_mid('qok','ch'):.3f}, qok→qok={E2_vms_mid('qok','qok'):.3f}")

# ─── Best value at N=30 ───────────────────────────────────────────────────────

# Choose best: highest pass count, then closest qok_ch to VMS
best_sweep = max(sweep_results, key=lambda x: (x[1], -abs(x[2].get('qok_ch',0)/VMS_REF['qok_ch']-1)))
best_p = best_sweep[0]
print(f"\n{'='*70}")
print(f"BEST p_chqok = {best_p} (N={N_SWEEP} sweep). Running N={N_FULL}...")
print(f"{'='*70}")

all_metrics_full = []
for trial in range(N_FULL):
    rng = random.Random(SEED + trial * 100 + int(best_p * 1000))
    lines = run_sim(latin_words, onset_weights_mid, suffix_global,
                    suffix_lf_sup, suffix_mid_sup, ll_onsets,
                    onset_lf_vms, onset_ll_vms, P_BLIND, best_p, rng)
    m = compute_metrics(lines, vms)
    if m: all_metrics_full.append(m)
    if (trial + 1) % 10 == 0:
        print(f"  Trial {trial+1}/{N_FULL} done")

avg_full = {k: agg_mean(all_metrics_full, k) for k in all_metrics_full[0]} if all_metrics_full else {}
passes_full = print_battery(avg_full, VMS_REF, f"p_chqok={best_p}, N={N_FULL}")

# Also check baseline (p_chqok=0) at N=30 for comparison
print(f"\n{'='*70}")
print(f"BASELINE p_chqok=0.00 (exp_236 architecture) at N={N_FULL} for comparison...")
print(f"{'='*70}")

all_metrics_base = []
for trial in range(N_FULL):
    rng = random.Random(SEED + trial * 100)
    lines = run_sim(latin_words, onset_weights_mid, suffix_global,
                    suffix_lf_sup, suffix_mid_sup, ll_onsets,
                    onset_lf_vms, onset_ll_vms, P_BLIND, 0.00, rng)
    m = compute_metrics(lines, vms)
    if m: all_metrics_base.append(m)

avg_base = {k: agg_mean(all_metrics_base, k) for k in all_metrics_base[0]} if all_metrics_base else {}
passes_base = print_battery(avg_base, VMS_REF, "baseline p_chqok=0.00, N=30")

print(f"\n{'='*70}")
print(f"SUMMARY")
print(f"{'='*70}")
print(f"  Baseline (p_chqok=0.00):  {passes_base}/{len(BATTERY_KEYS)} PASS")
print(f"  Best p_chqok={best_p:4.2f}:       {passes_full}/{len(BATTERY_KEYS)} PASS")
print(f"  ch→qok MID E2:  baseline={avg_base.get('_ch_qok_mid',0):.3f}, "
      f"best={avg_full.get('_ch_qok_mid',0):.3f}, VMS={E2_vms_mid('ch','qok'):.3f}")
print(f"  qok→ch MID E2:  baseline={avg_base.get('_qok_ch_mid',0):.3f}, "
      f"best={avg_full.get('_qok_ch_mid',0):.3f}, VMS={E2_vms_mid('qok','ch'):.3f}")
print(f"  qok→qok MID E2: baseline={avg_base.get('_qok_qok_mid',0):.3f}, "
      f"best={avg_full.get('_qok_qok_mid',0):.3f}, VMS={E2_vms_mid('qok','qok'):.3f}")

if passes_full >= passes_base:
    print(f"\n  VERDICT: p_chqok={best_p} PASSES battery without regression.")
else:
    print(f"\n  VERDICT: p_chqok={best_p} REGRESSES battery ({passes_full} vs {passes_base}).")

print("\nDone.")
