"""
exp_301: H504 — R_MID Calibration to Stabilize am_mid_enr Below 120%

exp_299 revealed that am_mid_enr = 0.1954 (VMS) is stochastically at the ±20% boundary.
Current sim: ~0.232-0.237 = 118-121%. The metric flips pass/fail depending on seed.

R_MID=0.25 sets MID am-rate = 25% of global am-rate. Since VMS am_mid_enr ~0.20,
and VMS global_am_rate=0.0203, the VMS MID am-rate = 0.0203 * 0.20 = 0.00406.
We want sim am_mid_enr < 1.20 * 0.1954 = 0.2345, so MID am-rate / global_am_rate < 0.2345.
At R_MID=0.25, the actual MID am-rate depends on suffix composition.

Sweep R_MID ∈ {0.10, 0.15, 0.18, 0.20, 0.22, 0.25} — all other exp_287 params fixed.
Use multiple seeds (N=30 each) to check stochastic stability.

Architecture: exp_287 16-mechanism baseline (beta=0.30).
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_FULL   = 30
TARGET_LINES = 2411
WINDOW   = 20
SEED     = 301000

# 16-mechanism B-dialect parameters (exp_287)
P_BLIND   = 0.115; P_LF    = 1.0;   CP       = 0.55; MP       = 0.90
P_QOKCH   = 0.12;  P_CHQOK = 0.12;  P_STUTTER = 0.006
R_LF      = 0.12;  MU_LEN   = 8.4;  SIGMA_LEN = 3.0
P_MF      = 0.20; P_LF_MF = 0.50; P_LL_MF = 0.00
GAMMA     = 0.30; ALPHA    = 0.20;  BETA     = 0.30
IDX_THRESH = 2;   SHORT_THRESH = 2

L_BASE  = 5.40; L_SLOPE = -0.053
SHORT_ONSETS = {'d', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'o'}
EVA_CHARS = list('acdehiklmnoqrsty')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'
def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0
def get_suffix(w):
    for s in SUFFIX_PATTERNS:
        if w.endswith(s): return s
    return 'other'
def get_edy_suffix_len(w):
    if w.endswith('eedy'): return 4
    if w.endswith('edy'):  return 3
    return 0
def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

def parse_vms_b():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio = m.group(1).lstrip('+*=&~'); fb = folio_base(folio)
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
            folio = m.group(1).lstrip('+*=&~'); fb = folio_base(folio)
            if folio_dialect.get(fb, 'unknown') != 'B': continue
            lc = m.group(3).lstrip('+*=/~&')
            if not lc.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: b_lines.append(words)
    return b_lines

def build_midfix_dist(words):
    midfix_cnt = Counter()
    for w in words:
        onset = get_onset(w); suf = get_suffix(w)
        if onset == 'other' or suf == 'other': continue
        onset_len = get_onset_len(w); suf_len = len(suf)
        edy_len = get_edy_suffix_len(w)
        if edy_len:
            mid_end = len(w) - edy_len
            midfix = w[onset_len:mid_end]
            if len(midfix) >= 1: midfix = midfix[:-1]
        else:
            midfix = w[onset_len:len(w)-suf_len]
        midfix_cnt[midfix] += 1
    total = sum(midfix_cnt.values())
    if total == 0: return {}, 0.0
    p_ne = sum(v for k, v in midfix_cnt.items() if k != '') / total
    ne = {mf: v for mf, v in midfix_cnt.items() if mf != ''}
    nt = sum(ne.values())
    return ({mf: v/nt for mf, v in ne.items()} if nt else {}), p_ne

def compute_vms_distributions(b_lines):
    all_words = [w for l in b_lines for w in l]
    lf_words  = [l[0]  for l in b_lines if l]
    ll_words  = [l[-1] for l in b_lines if len(l) > 1]
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words); n_mid = len(mid_words)
    def build_onset(words):
        cnt = Counter(get_onset(w) for w in words); cnt.pop('other', None)
        total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}
    def build_suffix(words):
        cnt = Counter(get_suffix(w) for w in words); total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}
    onset_global = build_onset(all_words); onset_lf = build_onset(lf_words)
    onset_ll = build_onset(ll_words); onset_mid = build_onset(mid_words)
    suffix_global = build_suffix(all_words)
    mid_nemed, mid_p = build_midfix_dist(mid_words)
    lf_nemed,  lf_p  = build_midfix_dist(lf_words)
    ll_nemed,  ll_p  = build_midfix_dist(ll_words)
    am_r  = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words)
    d_r   = Counter(get_onset(w) for w in all_words).get('d', 0) / n
    ll_d  = Counter(get_onset(w) for w in ll_words).get('d', 0) / len(ll_words)
    lf_am_rate = sum(1 for w in lf_words if w.endswith('am')) / len(lf_words)
    mid_am_rate = sum(1 for w in mid_words if w.endswith('am')) / n_mid if n_mid else 0
    return {
        'onset_global': onset_global, 'onset_lf': onset_lf,
        'onset_ll': onset_ll, 'onset_mid': onset_mid,
        'suffix_global': suffix_global,
        'mid_nemed': mid_nemed, 'mid_p': mid_p,
        'lf_nemed': lf_nemed, 'lf_p': lf_p,
        'll_nemed': ll_nemed, 'll_p': ll_p,
        'am_r': am_r, 'am_ll_target': ll_am/am_r if am_r else 0,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'am_lf_enr': lf_am_rate/am_r if am_r else 0,
        'am_mid_enr': mid_am_rate/am_r if am_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words), 'n_mid': n_mid,
    }

def compute_d_boost(d_global, d_ll_target, d_ll_non_blind_enr, p_blind):
    return d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind_enr) / p_blind

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    remaining = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o != 'd'}
    base_total = sum(base.values())
    norm = {o: v/base_total * remaining for o, v in base.items()} if base_total else {}
    norm['d'] = d_boost_weight; return norm

def weighted_choice(rng, dist):
    r = rng.random(); cum = 0.0
    for k, v in dist.items():
        cum += v
        if r < cum: return k
    return list(dist.keys())[-1]

def sample_midfix(rng, non_empty_dist, p_non_empty):
    if non_empty_dist and rng.random() < p_non_empty:
        return weighted_choice(rng, non_empty_dist)
    return ''

def make_word_sim(onset, suffix, rng, non_empty_midfix_dist, p_midfix_present):
    if suffix == 'other': return onset + suffix
    midfix = sample_midfix(rng, non_empty_midfix_dist, p_midfix_present)
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
        return onset + midfix + connector + suffix
    return onset + midfix + suffix

def make_suppressed_suffix(suffix_global, r_am):
    am_w = suffix_global.get('am', 0); new_am = am_w * r_am
    delta = am_w - new_am; non_am = 1.0 - am_w
    return {suf: (new_am if suf=='am' else w + (w/non_am)*delta if non_am>0 else w)
            for suf, w in suffix_global.items()}

def apply_suffix_length_bias(suffix_weights, word_idx, beta):
    if beta == 0.0 or word_idx < IDX_THRESH:
        return suffix_weights
    new_w = {}
    for suf, w in suffix_weights.items():
        suf_len = len(suf) if suf != 'other' else 5
        penalty = max(0, suf_len - SHORT_THRESH)
        new_w[suf] = w * math.exp(-beta * penalty)
    total = sum(new_w.values())
    return {s: v/total for s, v in new_w.items()} if total > 0 else suffix_weights

def random_eva_word_onset_biased(onset_weights, suffix_weights, rng, non_empty_midfix_dist,
                                  p_midfix_present, word_idx, alpha, beta):
    if alpha == 0.0:
        norm = onset_weights
    else:
        new_weights = {o: w*(1+alpha*word_idx) if o in SHORT_ONSETS else w
                       for o, w in onset_weights.items()}
        total = sum(new_weights.values())
        norm = {o: w/total for o, w in new_weights.items()}
    onset = weighted_choice(rng, norm)
    biased_suf = apply_suffix_length_bias(suffix_weights, word_idx, beta)
    suffix = weighted_choice(rng, biased_suf)
    return make_word_sim(onset, suffix, rng, non_empty_midfix_dist, p_midfix_present)

def cipher_ll(onset_ll_vms, ll_onsets, suffix_global, p_blind, rng, ll_nemed):
    if rng.random() < p_blind:
        onset = weighted_choice(rng, ll_onsets)
        return onset + 'am'
    onset  = weighted_choice(rng, onset_ll_vms)
    suffix = weighted_choice(rng, suffix_global)
    return make_word_sim(onset, suffix, rng, ll_nemed, P_LL_MF)

def cipher_lf(onset_mid, onset_lf_vms, suffix_lf, p_lf, rng, lf_nemed):
    if rng.random() < p_lf:
        onset  = weighted_choice(rng, onset_lf_vms)
        suffix = weighted_choice(rng, suffix_lf)
        return make_word_sim(onset, suffix, rng, lf_nemed, P_LF_MF)
    return random_eva_word_onset_biased(onset_mid, suffix_lf, rng, {}, 0.0, 0, 0.0, 0.0)

def timm_modify(word, onset_mid, suffix_mid, rng):
    if not word: return word
    onset_len = get_onset_len(word); edy_len = get_edy_suffix_len(word)
    mod_start = onset_len; mod_end = len(word) - edy_len
    if mod_start >= mod_end:
        return random_eva_word_onset_biased(onset_mid, suffix_mid, rng, {}, 0.0, 0, 0.0, 0.0)
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

def draw_buf_length_biased(buf, prev_onset, p_qokch, p_chqok, rng, word_idx, gamma):
    buf_list = list(buf)
    if not buf_list: return None
    preferred = None
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words: preferred = ch_words
    elif prev_onset == 'ch' and p_chqok > 0 and rng.random() < p_chqok:
        qok_words = [w for w in buf_list if get_onset(w) == 'qok']
        if qok_words: preferred = qok_words
    candidates = preferred if preferred else buf_list
    if gamma == 0.0: return rng.choice(candidates)
    L_target = L_BASE + L_SLOPE * word_idx
    weights = [math.exp(-gamma * (len(w) - L_target)**2) for w in candidates]
    total = sum(weights)
    if total == 0: return rng.choice(candidates)
    r = rng.random() * total; cum = 0.0
    for w, wt in zip(candidates, weights):
        cum += wt
        if r < cum: return w
    return candidates[-1]

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms,
            mid_nemed, lf_nemed, ll_nemed, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    while len(lines) < TARGET_LINES and pos < len(w) - 2:
        n = max(2, min(20, round(rng.gauss(MU_LEN, SIGMA_LEN))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []; word_idx = 0
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf(onset_mid, onset_lf_vms, suffix_lf_sup, P_LF, rng, lf_nemed)
            elif i == len(chunk) - 1:
                ew = cipher_ll(onset_ll_vms, ll_onsets, suffix_global, P_BLIND, rng, ll_nemed)
            else:
                if prev_word is not None and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf_length_biased(buf, prev_onset, P_QOKCH, P_CHQOK,
                                                 rng, word_idx, GAMMA)
                    if src is None: src = rng.choice(list(buf))
                    if rng.random() < MP:
                        ew = timm_modify(src, onset_mid, suffix_mid_sup, rng)
                    else:
                        ew = src
                else:
                    ew = random_eva_word_onset_biased(onset_mid, suffix_mid_sup, rng,
                                                      mid_nemed, P_MF, word_idx, ALPHA, BETA)
                buf.append(ew); word_idx += 1
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def compute_metrics(lines):
    aw  = [w for l in lines for w in l]; n = len(aw)
    if n < 100: return None
    lf  = [l[0]  for l in lines if l]
    ll  = [l[-1] for l in lines if len(l) > 1]
    mid = [w for l in lines for w in l[1:-1] if len(l) > 2]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf  = Counter(get_onset(w) for w in lf)
    oc_ll  = Counter(get_onset(w) for w in ll)
    n_lf, n_ll, n_mid = len(lf), len(ll), len(mid)
    def enr(onset, ctr_slot, n_slot):
        s = ctr_slot.get(onset, 0)/n_slot if n_slot else 0
        g = oc_all.get(onset, 0)/n if n else 0
        return s/g if g > 0 else 0
    am_r   = sum(1 for w in aw if w.endswith('am')) / n
    ll_am  = sum(1 for w in ll if w.endswith('am')) / n_ll if n_ll else 0
    am_ll  = ll_am / am_r if am_r else 0
    d_ll   = enr('d', oc_ll, n_ll); y_lf = enr('y', oc_lf, n_lf)
    tb = n-1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o, 0)/n
        return bg.get((o,o),0)/(tb*b*b) if b > 0 and tb > 0 else 1.0
    ss_mean = (ss('qok')+ss('ok')+ss('ch'))/3
    adj = sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)
    qok_lf = enr('qok', oc_lf, n_lf); d_lf  = enr('d',  oc_lf, n_lf)
    s_lf   = enr('s',   oc_lf, n_lf); ch_ll = enr('ch', oc_ll, n_ll)
    ok_ll  = enr('ok',  oc_ll, n_ll); qok_ll = enr('qok', oc_ll, n_ll)
    ss_d = ss('d'); ss_y = ss('y')
    lf_am_rate  = sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf else 0
    mid_am_rate = sum(1 for w in mid if w.endswith('am'))/n_mid if n_mid else 0
    am_lf_enr   = lf_am_rate  / am_r if am_r else 0
    am_mid_enr  = mid_am_rate / am_r if am_r else 0
    edy_rate = sum(1 for w in aw if w.endswith('edy') or w.endswith('eedy'))/n
    word_len = sum(len(w) for w in aw)/n
    qok_r = oc_all.get('qok', 0)/n; ch_r = oc_all.get('ch', 0)/n
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r and tb > 0 else 0
    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch, global_am_rate=am_r)

BATTERY_19 = ['am_ll', 'd_ll', 'y_lf', 'ss_mean', 'adj_rate', 'qok_lf', 'd_lf', 's_lf',
              'ch_ll', 'ok_ll', 'qok_ll', 'ss_d', 'ss_y', 'am_lf_enr', 'am_mid_enr',
              'edy_rate', 'word_len_mean', 'qok_ch', 'global_am_rate']
PASS_TOL = 0.20
VMS_REF = {
    'am_ll': 6.5498, 'd_ll': 1.3625, 'y_lf': 3.1837, 'ss_mean': 1.1640,
    'adj_rate': 0.0090, 'qok_lf': 0.7450, 'd_lf': 2.1178, 's_lf': 4.4422,
    'ch_ll': 0.9653, 'ok_ll': 1.0028, 'qok_ll': 0.6121, 'ss_d': 1.5850,
    'ss_y': 1.9550, 'am_lf_enr': 0.1225, 'am_mid_enr': 0.1954,
    'edy_rate': 0.1940, 'word_len_mean': 5.4000, 'qok_ch': 1.2670,
    'global_am_rate': 0.0203,
}
def passes(sim_val, vms_val, tol=PASS_TOL):
    if vms_val == 0: return True
    r = sim_val / vms_val
    return (1 - tol) <= r <= (1 + tol)
def agg(metrics_list, key):
    vals = [x[key] for x in metrics_list if key in x]
    return sum(vals) / len(vals) if vals else 0
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

print("exp_301: H504 — R_MID Calibration to Stabilize am_mid_enr")
print("=" * 65)

print("Parsing VMS B-dialect corpus...")
b_lines = parse_vms_b()
vms = compute_vms_distributions(b_lines)
print(f"  VMS B: {len(b_lines)} lines, {vms['n']} words")
print(f"  VMS am_mid_enr = {vms['am_mid_enr']:.4f}")
print(f"  VMS global_am_rate = {vms['am_r']:.4f}")
print(f"  VMS MID am-rate = {vms['am_r'] * vms['am_mid_enr']:.5f}")

print("\nLoading Latin corpus...")
latin_words = load_latin(LATIN_CORPUS)
print(f"  {len(latin_words)} Latin words loaded.")

suffix_global = vms['suffix_global']
suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
onset_lf_vms = vms['onset_lf']; onset_ll_vms = vms['onset_ll']; onset_mid = vms['onset_mid']
d_global = vms['onset_global'].get('d', 0)
d_ll_non_blind_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0
d_boost_weight = compute_d_boost(d_global, vms['d_ll_target'], d_ll_non_blind_enr, P_BLIND)
d_boost_weight = max(0.0, min(d_boost_weight, 1.0))
ll_onsets = build_ll_onsets(onset_ll_vms, d_boost_weight)
mid_nemed = vms['mid_nemed']; lf_nemed = vms['lf_nemed']; ll_nemed = vms['ll_nemed']

print(f"\n  Target: am_mid_enr < {1.20 * VMS_REF['am_mid_enr']:.4f} (120% of VMS {VMS_REF['am_mid_enr']})")

print(f"\n{'='*65}")
print(f"SWEEP: R_MID ∈ {{0.10, 0.15, 0.18, 0.20, 0.22, 0.25}} (N={N_FULL})")
print('='*65)
print(f"  {'R_MID':>6}  {'PASS':>6}  {'am_mid_enr':>10}  {'am_lf_enr':>9}  {'am_ll':>6}  {'adj':>7}  {'ss_mean':>7}")
print(f"  {'VMS':>6}         {'0.1954':>10}  {'0.1225':>9}  {'6.550':>6}  {'0.009':>7}  {'1.164':>7}")
print(f"  {'-'*75}")

best_r_mid = 0.25; best_pass = -1
for r_mid in [0.10, 0.15, 0.18, 0.20, 0.22, 0.25]:
    suffix_mid_sup = make_suppressed_suffix(suffix_global, r_mid)
    metrics_list = []
    for trial in range(N_FULL):
        rng = random.Random(SEED + trial * 1000 + int(r_mid * 10000))
        lines = run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf_vms, onset_ll_vms,
                        mid_nemed, lf_nemed, ll_nemed, rng)
        m = compute_metrics(lines)
        if m: metrics_list.append(m)
    if not metrics_list: continue
    pass_count = sum(1 for key in BATTERY_19 if passes(agg(metrics_list, key), VMS_REF[key]))
    ame = agg(metrics_list, 'am_mid_enr')
    alf = agg(metrics_list, 'am_lf_enr')
    amll = agg(metrics_list, 'am_ll')
    adj = agg(metrics_list, 'adj_rate')
    ssm = agg(metrics_list, 'ss_mean')
    pct = ame / VMS_REF['am_mid_enr'] * 100
    print(f"  {r_mid:>6.2f}  {pass_count:>4}/19  {ame:>10.4f} ({pct:.0f}%)  "
          f"{alf:>9.4f}  {amll:>6.3f}  {adj:>7.5f}  {ssm:>7.4f}")
    if pass_count > best_pass:
        best_pass = pass_count; best_r_mid = r_mid

print(f"\n  BEST (most 19/19 metrics): R_MID={best_r_mid}")

# Full battery for best R_MID
print(f"\n{'='*65}")
print(f"FULL BATTERY: R_MID={best_r_mid}, N={N_FULL}")
print('='*65)
suffix_mid_sup = make_suppressed_suffix(suffix_global, best_r_mid)
metrics_list = []
for trial in range(N_FULL):
    rng = random.Random(SEED + trial * 1000 + int(best_r_mid * 10000))
    lines = run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf_vms, onset_ll_vms,
                    mid_nemed, lf_nemed, ll_nemed, rng)
    m = compute_metrics(lines)
    if m: metrics_list.append(m)

print(f"\n  19-Metric Battery (R_MID={best_r_mid}, N={N_FULL}):")
print(f"  {'Metric':<20}  {'VMS':>8}  {'Sim':>8}  {'%VMS':>6}  Status")
print(f"  {'-'*55}")
pass_count = 0
for key in BATTERY_19:
    vval = VMS_REF[key]; sval = agg(metrics_list, key)
    ok = passes(sval, vval)
    if ok: pass_count += 1
    pct = sval/vval*100 if vval else 0
    print(f"  {key:<20}  {vval:>8.4f}  {sval:>8.4f}  {pct:>5.1f}%  {'PASS' if ok else 'FAIL'}")
print(f"\n  TOTAL PASS: {pass_count}/19")
print("\nDone.")
