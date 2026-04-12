"""
exp_243: H446 — sh→qok B-Dialect Markov Rule

Question: Does adding p_sh_qok parameter to draw_buf (when prev_onset='sh', with
probability p_sh_qok search buffer for qok-onset word) reproduce the confirmed
within-MID sh→qok enrichment (exp_242: E_mid=1.967, N=339) without regressing
the 19-metric battery (currently 19/19 PASS in exp_236)?

Design:
  Base architecture: exp_236 B-dialect frozen (19/19 PASS)
    p_blind=0.115, r_lf=0.12, r_mid=0.25, p_stutter=0.006
    cp=0.55, mp=0.90, p_qokch=0.12, p_lf=1.0, mu_len=8.4

  Addition: p_sh_qok ∈ {0.00, 0.05, 0.10, 0.15, 0.20} sweep at N=5 each
    At each value: report 19-metric PASS count + sh→qok enrichment (diagnostic)
    Best value: closest to E(sh→qok) = 1.967 (VMS MID-only) while maintaining 19/19

  Additional diagnostic: compute global sh→qok enrichment (E_global target ~2.109)
  and MID-only approximation (using consecutive non-LF/non-LL pairs in the simulation).

  Expected result: p_sh_qok ≈ 0.10-0.15 should raise sh→qok enrichment from ~0.97
  (current exp_236 baseline) toward ~2.0 without affecting 19-metric battery
  (sh→qok is not in the 19-metric battery; indirect effects via onset composition small).
"""

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SWEEP  = 5
N_FULL   = 30
TARGET_LINES = 2447
WINDOW   = 20
SEED     = 243000

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
            if w.endswith(suf):
                suf_ctr[suf] += 1; matched = True; break
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
    """edy-conditional connector (exp_234 architecture)."""
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

def draw_from_buffer(buf, prev_onset, p_qokch, p_sh_qok, rng):
    """
    Draw from buffer with Markov onset-succession rules:
    - qok→ch: if prev_onset='qok', with prob p_qokch seek ch-onset word
    - sh→qok:  if prev_onset='sh',  with prob p_sh_qok seek qok-onset word (NEW)
    Falls back to random buffer draw if no matching word found.
    """
    buf_list = list(buf)
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words: return rng.choice(ch_words)
    if prev_onset == 'sh' and p_sh_qok > 0 and rng.random() < p_sh_qok:
        qok_words = [w for w in buf_list if get_onset(w) == 'qok']
        if qok_words: return rng.choice(qok_words)
    return rng.choice(buf_list)

def run_sim(latin_words, onset_weights_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms, p_sh_qok, rng):
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
                ew = cipher_lf_vms(onset_weights_mid, suffix_lf_sup, onset_lf_vms, P_LF, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_blind_fixed(onset_weights_mid, suffix_global, ll_onsets,
                                           onset_ll_vms, P_BLIND, rng)
            else:
                if prev_word is not None and P_STUTTER > 0 and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_from_buffer(buf, prev_onset, P_QOKCH, p_sh_qok, rng)
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

def compute_sh_qok_enrichment(lines):
    """Compute global sh→qok bigram enrichment E(sh→qok)."""
    all_words = [w for l in lines for w in l]
    n = len(all_words)
    oc = Counter(get_onset(w) for w in all_words)
    tb = n - 1
    bg = Counter((get_onset(all_words[i]), get_onset(all_words[i+1])) for i in range(tb))
    sh_r = oc.get('sh', 0) / n
    qok_r = oc.get('qok', 0) / n
    sh_qok_obs = bg.get(('sh', 'qok'), 0) / tb if tb > 0 else 0
    E = sh_qok_obs / (sh_r * qok_r) if sh_r * qok_r > 0 else 0
    return E

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

    # Diagnostic: sh→qok enrichment
    sh_r = oc_all.get('sh', 0)/n
    sh_qok_e = bg.get(('sh','qok'),0)/(tb*sh_r*qok_r) if sh_r*qok_r>0 else 0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch,
                global_am_rate=am_r,
                sh_qok_e=sh_qok_e)   # diagnostic only — NOT in 19-metric battery

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
    return mean

# ─── Setup ────────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus...")
vms_b_lines = parse_vms_corpus()
vms = compute_vms_distributions(vms_b_lines)
print(f"  VMS B: {len(vms_b_lines)} lines, {vms['n']} words")

# VMS sh→qok enrichment (global)
all_vms = [w for l in vms_b_lines for w in l]
n_vms = len(all_vms)
oc_vms = Counter(get_onset(w) for w in all_vms)
tb_vms = n_vms - 1
bg_vms = Counter((get_onset(all_vms[i]), get_onset(all_vms[i+1])) for i in range(tb_vms))
sh_r_vms = oc_vms.get('sh', 0) / n_vms
qok_r_vms = oc_vms.get('qok', 0) / n_vms
vms_sh_qok_global = bg_vms.get(('sh','qok'), 0) / (tb_vms * sh_r_vms * qok_r_vms) if sh_r_vms*qok_r_vms>0 else 0
print(f"  VMS B sh→qok E_global = {vms_sh_qok_global:.3f}  (exp_242: E_mid=1.967, target)")

d_global    = vms['onset_global'].get('d', 0)
d_ll_target = vms['d_ll_target']
onset_ll_vms = dict(vms['onset_ll'])
vms_ll_d_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0

d_boost = compute_d_boost_fixed(d_global, d_ll_target, vms_ll_d_enr, P_BLIND)
ll_onsets    = build_ll_onsets_fixed(onset_ll_vms, d_boost)
onset_lf_vms = dict(vms['onset_lf'])
suffix_global = dict(vms['suffix_global'])
onset_weights_mid = dict(vms['onset_mid'])

suffix_lf_sup  = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)

lf_words_vms = [l[0] for l in vms_b_lines if l]
vms_lf_am_rate = sum(1 for w in lf_words_vms if w.endswith('am')) / len(lf_words_vms)
vms_am_lf_enr  = vms_lf_am_rate / vms['am_r']

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
BATTERY_19 = [
    'am_ll', 'd_ll', 'y_lf', 'ss_mean', 'adj_rate',
    'qok_lf', 'd_lf', 's_lf', 'ch_ll', 'ok_ll',
    'qok_ll', 'ss_d', 'ss_y', 'am_lf_enr',
    'am_mid_enr', 'edy_rate', 'word_len_mean', 'qok_ch',
    'global_am_rate',
]

def passes(sim_val, vms_val, tol=PASS_TOL):
    if vms_val == 0: return True
    r = sim_val / vms_val
    return (1 - tol) <= r <= (1 + tol)

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")

# ─── Sweep ────────────────────────────────────────────────────────────────────

P_SH_QOK_VALUES = [0.00, 0.05, 0.10, 0.15, 0.20]

print(f"\n{'='*80}")
print("SWEEP: p_sh_qok — N=5 each")
print(f"{'='*80}")
print(f"  {'p_sh_qok':>10}  {'PASS/19':>8}  {'sh→qok_E':>10}  {'qok_ch':>8}  {'ss_mean':>8}  {'ss_y':>8}")
print(f"  {'-'*60}")

sweep_results = {}

for p_sh_qok in P_SH_QOK_VALUES:
    rng = random.Random(SEED + int(p_sh_qok * 1000))
    results = []
    for trial in range(N_SWEEP):
        rng_t = random.Random(SEED + int(p_sh_qok * 1000) + trial * 100)
        lines = run_sim(latin, onset_weights_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf_vms, onset_ll_vms, p_sh_qok, rng_t)
        m = compute_metrics(lines, vms)
        if m: results.append(m)

    if not results: continue
    mean_m = {k: agg(results, k) for k in results[0]}
    pass_count = sum(1 for metric in BATTERY_19 if passes(mean_m[metric], VMS_REF[metric]))
    sh_qok_e = mean_m['sh_qok_e']
    sweep_results[p_sh_qok] = (pass_count, mean_m)
    print(f"  {p_sh_qok:>10.2f}  {pass_count:>5}/19  {sh_qok_e:>10.3f}  "
          f"{mean_m['qok_ch']:>8.3f}  {mean_m['ss_mean']:>8.3f}  {mean_m['ss_y']:>8.3f}")

# ─── Select best ──────────────────────────────────────────────────────────────

# Best: maximize sh→qok enrichment toward VMS target (1.967 MID; 2.109 global)
# while maintaining ≥19/19 PASS
# Target E_global ≈ 2.109
VMS_SH_QOK_TARGET = vms_sh_qok_global  # use actual VMS global value

best_p = 0.00
best_dist = float('inf')
for p, (pc, mm) in sweep_results.items():
    if pc < 19: continue  # must maintain 19/19
    dist = abs(mm['sh_qok_e'] - VMS_SH_QOK_TARGET)
    if dist < best_dist:
        best_dist = dist; best_p = p

# If no 19/19 found, pick best pass count
if best_dist == float('inf'):
    best_p = max(sweep_results.keys(), key=lambda p: (sweep_results[p][0], -abs(sweep_results[p][1]['sh_qok_e'] - VMS_SH_QOK_TARGET)))

print(f"\n  Best p_sh_qok = {best_p:.2f} (closest to VMS sh→qok E={VMS_SH_QOK_TARGET:.3f} while maintaining 19/19)")

# ─── Full Run ─────────────────────────────────────────────────────────────────

print(f"\n{'='*80}")
print(f"FULL RUN: p_sh_qok = {best_p:.2f}, N={N_FULL}")
print(f"{'='*80}")

full_results = []
for trial in range(N_FULL):
    rng_t = random.Random(SEED + 50000 + trial * 100)
    lines = run_sim(latin, onset_weights_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf_vms, onset_ll_vms, best_p, rng_t)
    m = compute_metrics(lines, vms)
    if m: full_results.append(m)

mean_full = {k: agg(full_results, k) for k in full_results[0]}

print(f"\n  19-Metric Battery (p_sh_qok={best_p:.2f}, N={N_FULL}):")
print(f"  {'Metric':<16} {'VMS':>8} {'Sim':>8} {'%VMS':>8}  Status")
print(f"  {'-'*55}")

pass_total = 0
for metric in BATTERY_19:
    vref = VMS_REF[metric]
    sval = mean_full[metric]
    pct  = sval / vref * 100 if vref else 0
    ok   = passes(sval, vref)
    if ok: pass_total += 1
    flag = 'PASS' if ok else 'FAIL'
    print(f"  {metric:<16} {vref:>8.4f} {sval:>8.4f} {pct:>8.1f}%  {flag}")

print(f"\n  TOTAL: {pass_total}/19 PASS")
print(f"\n  DIAGNOSTIC — sh→qok enrichment:")
print(f"    VMS E_global = {vms_sh_qok_global:.3f}  (exp_242 E_mid=1.967)")
print(f"    Sim E_global = {mean_full['sh_qok_e']:.3f}")
print(f"    Change from baseline (p_sh_qok=0.00):")
baseline_e = sweep_results.get(0.00, (0, {'sh_qok_e': 0}))[1].get('sh_qok_e', 0)
print(f"      Baseline sh→qok E = {baseline_e:.3f}")
print(f"      With p_sh_qok={best_p:.2f}: sh→qok E = {mean_full['sh_qok_e']:.3f}")
print(f"      Delta = {mean_full['sh_qok_e'] - baseline_e:+.3f}")

# ─── Also run baseline (p=0.00) at N=30 for comparison ────────────────────────

if best_p != 0.00:
    print(f"\n{'='*80}")
    print(f"COMPARISON: p_sh_qok = 0.00 (baseline), N={N_FULL}")
    print(f"{'='*80}")
    base_full_results = []
    for trial in range(N_FULL):
        rng_t = random.Random(SEED + 60000 + trial * 100)
        lines = run_sim(latin, onset_weights_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf_vms, onset_ll_vms, 0.00, rng_t)
        m = compute_metrics(lines, vms)
        if m: base_full_results.append(m)
    mean_base = {k: agg(base_full_results, k) for k in base_full_results[0]}
    base_pass = sum(1 for metric in BATTERY_19 if passes(mean_base[metric], VMS_REF[metric]))
    print(f"  Baseline: {base_pass}/19 PASS, sh→qok E = {mean_base['sh_qok_e']:.3f}")
    print(f"  With p_sh_qok={best_p:.2f}: {pass_total}/19 PASS, sh→qok E = {mean_full['sh_qok_e']:.3f}")

print("\nDone.")
