"""
exp_277: H466 — B-Dialect Fine-Grained p_sh_qok Sweep

Question: Is there a small p_sh_qok value (0.01–0.04) that provides partial sh→qok
closure for B-dialect without regressing ss_d or other battery metrics?

Background:
- exp_243: B-dialect p_sh_qok sweep {0.00, 0.05, 0.10, 0.15, 0.20}
  - p=0.05 only 19/19 at N=5; at N=30: ss_d=120.6% FAIL
  - A-dialect succeeded at p=0.10 because A ss_d target (1.274) < B ss_d target (1.585)
  - B-dialect has less headroom; threshold is likely p=0.02-0.03
  - At slope 2.25 E/unit p (exp_243), p=0.03 → Δsh_qok ≈ +0.068 (small but measurable)
- Architecture update since exp_243:
  - exp_249: p_chqok=0.12 added (bidirectional qok↔ch coupling)
  - exp_257: filter_other applied to all onset distributions
  - These changes may shift baseline ss_d slightly

Design:
- Parameters frozen at exp_257 values + p_chqok=0.12
- Sweep p_sh_qok ∈ {0.00, 0.01, 0.02, 0.03, 0.04} at N=10
- Monitor: full 19-metric battery (especially ss_d) + sh→qok E2 (diagnostic)
- PASS threshold: 19/19; ss_d within ±20% of VMS 1.585 (B-dialect target)
- If any value passes without regression, accept as 13th B-dialect mechanism
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SWEEP  = 10
N_FULL   = 30
TARGET_LINES = 2411  # B-dialect line count
WINDOW   = 20
SEED     = 277000

# B-dialect 12-mechanism parameters (frozen at exp_257 values)
P_BLIND   = 0.115; P_LF    = 1.0;   CP       = 0.55; MP       = 0.90
P_QOKCH   = 0.12;  P_CHQOK = 0.12;  P_STUTTER = 0.006
R_LF      = 0.12;  R_MID   = 0.25;  MU_LEN   = 8.4;  SIGMA_LEN = 3.0

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

    def build_onset(words, filter_other=True):
        cnt = Counter(get_onset(w) for w in words)
        if filter_other: cnt.pop('other', None)
        total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}

    def build_suffix(words):
        cnt = Counter()
        for w in words:
            matched = False
            for suf in SUFFIX_PATTERNS:
                if w.endswith(suf): cnt[suf] += 1; matched = True; break
            if not matched: cnt['other'] += 1
        total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}

    onset_global = build_onset(all_words)
    onset_lf     = build_onset(lf_words)
    onset_ll     = build_onset(ll_words)
    onset_mid    = build_onset(mid_words)
    suffix_global = build_suffix(all_words)

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
        'am_r': am_r, 'am_ll_target': ll_am/am_r if am_r else 0,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'am_lf_enr': lf_am_rate/am_r if am_r else 0,
        'am_mid_enr': mid_am_rate/am_r if am_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words), 'n_mid': n_mid,
    }

def make_suppressed_suffix(suffix_global, r_am):
    am_w = suffix_global.get('am', 0)
    new_am = am_w * r_am
    delta = am_w - new_am
    non_am = 1.0 - am_w
    out = {}
    for suf, w in suffix_global.items():
        if suf == 'am': out[suf] = new_am
        else: out[suf] = w + (w / non_am) * delta if non_am > 0 else w
    return out

def compute_d_boost(d_global, d_ll_target, d_ll_non_blind_enr, p_blind):
    return d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind_enr) / p_blind

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    remaining = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o != 'd'}
    base_total = sum(base.values())
    norm = {o: v/base_total * remaining for o, v in base.items()} if base_total else {}
    norm['d'] = d_boost_weight
    return norm

def make_word_sim(onset, suffix, rng):
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
        return onset + connector + suffix
    return onset + suffix

def random_eva_word(onset_weights, suffix_weights, rng):
    onset  = rng.choices(list(onset_weights.keys()),  weights=list(onset_weights.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_ll(onset_ll_vms, ll_onsets, suffix_global, p_blind, rng):
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return onset + 'am'
    onset  = rng.choices(list(onset_ll_vms.keys()), weights=list(onset_ll_vms.values()))[0]
    suffix = rng.choices(list(suffix_global.keys()), weights=list(suffix_global.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_lf(onset_mid, onset_lf_vms, suffix_lf, p_lf, rng):
    if rng.random() < p_lf:
        onset  = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
        suffix = rng.choices(list(suffix_lf.keys()),    weights=list(suffix_lf.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_mid, suffix_lf, rng)

def timm_modify(word, onset_mid, suffix_mid, rng):
    if not word: return word
    onset_len = get_onset_len(word); edy_len = get_edy_suffix_len(word)
    mod_start = onset_len; mod_end = len(word) - edy_len
    if mod_start >= mod_end:
        return random_eva_word(onset_mid, suffix_mid, rng)
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

def draw_buf(buf, prev_onset, p_qokch, p_chqok, p_sh_qok, rng):
    buf_list = list(buf)
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words: return rng.choice(ch_words)
    elif prev_onset == 'ch' and p_chqok > 0 and rng.random() < p_chqok:
        qok_words = [w for w in buf_list if get_onset(w) == 'qok']
        if qok_words: return rng.choice(qok_words)
    elif prev_onset == 'sh' and p_sh_qok > 0 and rng.random() < p_sh_qok:
        qok_words = [w for w in buf_list if get_onset(w) == 'qok']
        if qok_words: return rng.choice(qok_words)
    return rng.choice(buf_list)

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms, p_sh_qok, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    while len(lines) < TARGET_LINES and pos < len(w) - 2:
        n = max(2, min(20, round(rng.gauss(MU_LEN, SIGMA_LEN))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf(onset_mid, onset_lf_vms, suffix_lf_sup, P_LF, rng)
            elif i == len(chunk) - 1:
                ew = cipher_ll(onset_ll_vms, ll_onsets, suffix_global, P_BLIND, rng)
            else:
                if prev_word is not None and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf(buf, prev_onset, P_QOKCH, P_CHQOK, p_sh_qok, rng)
                    ew = timm_modify(src, onset_mid, suffix_mid_sup, rng) if rng.random() < MP else src
                else:
                    ew = random_eva_word(onset_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def compute_metrics(lines, VMS_REF):
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
    d_ll   = enr('d', oc_ll, n_ll)
    y_lf   = enr('y', oc_lf, n_lf)

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
    ss_d   = ss('d');                  ss_y   = ss('y')

    lf_am_rate  = sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf else 0
    mid_am_rate = sum(1 for w in mid if w.endswith('am'))/n_mid if n_mid else 0
    am_lf_enr   = lf_am_rate  / am_r if am_r else 0
    am_mid_enr  = mid_am_rate / am_r if am_r else 0

    edy_rate = sum(1 for w in aw if w.endswith('edy') or w.endswith('eedy'))/n
    word_len = sum(len(w) for w in aw)/n
    qok_r = oc_all.get('qok', 0)/n; ch_r = oc_all.get('ch', 0)/n
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r and tb > 0 else 0
    global_am_rate = am_r

    # Diagnostics (not in battery)
    sh_r = oc_all.get('sh', 0)/n
    sh_qok_e = bg.get(('sh','qok'),0)/(tb*sh_r*qok_r) if sh_r*qok_r > 0 and tb > 0 else 0
    ch_qok_e = bg.get(('ch','qok'),0)/(tb*ch_r*qok_r) if ch_r*qok_r > 0 and tb > 0 else 0
    qok_ch_e = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r*ch_r > 0 and tb > 0 else 0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch, global_am_rate=global_am_rate,
                # Diagnostics:
                sh_qok_e=sh_qok_e, ch_qok_e=ch_qok_e, qok_ch_e=qok_ch_e)

BATTERY_19 = [
    'am_ll', 'd_ll', 'y_lf', 'ss_mean', 'adj_rate',
    'qok_lf', 'd_lf', 's_lf', 'ch_ll', 'ok_ll',
    'qok_ll', 'ss_d', 'ss_y', 'am_lf_enr',
    'am_mid_enr', 'edy_rate', 'word_len_mean', 'qok_ch',
    'global_am_rate',
]
PASS_TOL = 0.20

def passes(sim_val, vms_val, tol=PASS_TOL):
    if vms_val == 0: return True
    r = sim_val / vms_val
    return (1 - tol) <= r <= (1 + tol)

def agg(metrics_list, key):
    vals = sorted(x[key] for x in metrics_list)
    return sum(vals) / len(vals)

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

# ─── Setup ────────────────────────────────────────────────────────────────────

print("exp_277: H466 — B-Dialect Fine-Grained p_sh_qok Sweep (p=0.01-0.04)")
print("=" * 70)

print("Parsing VMS B-dialect corpus...")
b_lines = parse_vms_b()
vms = compute_vms_distributions(b_lines)
print(f"  VMS B: {len(b_lines)} lines, {vms['n']} words")

# VMS sh→qok enrichment (global)
all_vms = [w for l in b_lines for w in l]
n_vms = len(all_vms); tb_vms = n_vms - 1
bg_vms = Counter((get_onset(all_vms[i]), get_onset(all_vms[i+1])) for i in range(tb_vms))
oc_vms = Counter(get_onset(w) for w in all_vms)
sh_r_vms  = oc_vms.get('sh', 0) / n_vms
qok_r_vms = oc_vms.get('qok', 0) / n_vms
vms_sh_qok = bg_vms.get(('sh','qok'), 0) / (tb_vms * sh_r_vms * qok_r_vms) if sh_r_vms*qok_r_vms>0 else 0
print(f"  VMS B sh→qok E_global = {vms_sh_qok:.3f}  (target for partial closure)")

d_global = vms['onset_global'].get('d', 0)
d_ll_non_blind_enr = vms['onset_ll'].get('d', 0) / d_global if d_global else 0
d_boost = compute_d_boost(d_global, vms['d_ll_target'], d_ll_non_blind_enr, P_BLIND)
ll_onsets   = build_ll_onsets(vms['onset_ll'], d_boost)
onset_ll_vms = dict(vms['onset_ll'])
onset_lf_vms = dict(vms['onset_lf'])
onset_mid    = dict(vms['onset_mid'])
suffix_global = dict(vms['suffix_global'])

suffix_lf_sup  = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)

VMS_REF = {
    'am_ll':         vms['am_ll_target'],
    'd_ll':          vms['d_ll_target'],
    'y_lf':          vms['onset_lf'].get('y',0) / vms['onset_global'].get('y',0.001),
    'ss_mean':       1.164,
    'adj_rate':      0.009,
    'qok_lf':        vms['onset_lf'].get('qok',0) / vms['onset_global'].get('qok',0.001),
    'd_lf':          vms['onset_lf'].get('d',0) / vms['onset_global'].get('d',0.001),
    's_lf':          vms['onset_lf'].get('s',0) / vms['onset_global'].get('s',0.001),
    'ch_ll':         vms['onset_ll'].get('ch',0) / vms['onset_global'].get('ch',0.001),
    'ok_ll':         vms['onset_ll'].get('ok',0) / vms['onset_global'].get('ok',0.001),
    'qok_ll':        vms['onset_ll'].get('qok',0) / vms['onset_global'].get('qok',0.001),
    'ss_d':          1.585,
    'ss_y':          1.955,
    'am_lf_enr':     vms['am_lf_enr'],
    'am_mid_enr':    vms['am_mid_enr'],
    'edy_rate':      sum(vms['suffix_global'].get(s,0) for s in ['edy','eedy']),
    'word_len_mean': 5.400,
    'qok_ch':        1.267,
    'global_am_rate': vms['am_r'],
}

print(f"\n  VMS reference targets:")
print(f"    am_ll={VMS_REF['am_ll']:.3f}, d_ll={VMS_REF['d_ll']:.3f}, "
      f"ss_d={VMS_REF['ss_d']:.3f}, ss_y={VMS_REF['ss_y']:.3f}")
print(f"    qok_ch={VMS_REF['qok_ch']:.3f}")

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")

# ─── Sweep ────────────────────────────────────────────────────────────────────

P_SH_QOK_VALUES = [0.00, 0.01, 0.02, 0.03, 0.04]

print(f"\n{'='*75}")
print("SWEEP: p_sh_qok ∈ {0.00, 0.01, 0.02, 0.03, 0.04} — N=10 each")
print(f"{'='*75}")
print(f"  {'p_sh_qok':>10}  {'PASS/19':>8}  {'sh→qok_E':>10}  "
      f"{'ss_d %VMS':>10}  {'ss_y %VMS':>10}  {'qok_ch %VMS':>12}")
print(f"  {'-'*65}")

sweep_results = {}

for p_sh_qok in P_SH_QOK_VALUES:
    results = []
    for trial in range(N_SWEEP):
        rng_t = random.Random(SEED + int(p_sh_qok * 1000) + trial * 100)
        lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf_vms, onset_ll_vms, p_sh_qok, rng_t)
        m = compute_metrics(lines, VMS_REF)
        if m: results.append(m)

    if not results: continue
    mean_m = {k: agg(results, k) for k in results[0]}
    pass_count = sum(1 for metric in BATTERY_19 if passes(mean_m[metric], VMS_REF[metric]))
    sweep_results[p_sh_qok] = (pass_count, mean_m)

    ss_d_pct = mean_m['ss_d'] / VMS_REF['ss_d'] * 100
    ss_y_pct = mean_m['ss_y'] / VMS_REF['ss_y'] * 100
    qok_ch_pct = mean_m['qok_ch'] / VMS_REF['qok_ch'] * 100

    print(f"  {p_sh_qok:>10.2f}  {pass_count:>5}/19  {mean_m['sh_qok_e']:>10.3f}  "
          f"{ss_d_pct:>9.1f}%  {ss_y_pct:>9.1f}%  {qok_ch_pct:>11.1f}%")

# ─── Full Run at best viable p ─────────────────────────────────────────────────

print(f"\n{'='*75}")
print("FULL RUN at best viable p_sh_qok (19/19 required), N=30")
print(f"{'='*75}")

best_p = None; best_e_gap = float('inf')
for p, (pc, mm) in sweep_results.items():
    if pc < 19: continue
    e_gap = abs(vms_sh_qok - mm['sh_qok_e'])
    if e_gap < best_e_gap: best_e_gap = e_gap; best_p = p

if best_p is None:
    print("  No value achieved 19/19. Running p=0.00 baseline for reference.")
    best_p = 0.00
else:
    print(f"  Best viable p_sh_qok = {best_p:.2f}")

full_results = []
for trial in range(N_FULL):
    rng_t = random.Random(SEED + 90000 + trial * 100)
    lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf_vms, onset_ll_vms, best_p, rng_t)
    m = compute_metrics(lines, VMS_REF)
    if m: full_results.append(m)

mean_full = {k: agg(full_results, k) for k in full_results[0]}
pass_full  = sum(1 for metric in BATTERY_19 if passes(mean_full[metric], VMS_REF[metric]))

print(f"\n  19-Metric Battery (p_sh_qok={best_p:.2f}, N={N_FULL}):")
print(f"  {'Metric':<16} {'VMS':>8} {'Sim':>8} {'%VMS':>8}  Status")
print(f"  {'-'*55}")
for metric in BATTERY_19:
    vref = VMS_REF[metric]; sval = mean_full[metric]
    pct  = sval / vref * 100 if vref else 0
    ok   = passes(sval, vref)
    if ok: pass_full += 0  # already counted
    flag = 'PASS' if ok else 'FAIL'
    print(f"  {metric:<16} {vref:>8.4f} {sval:>8.4f} {pct:>8.1f}%  {flag}")

print(f"\n  TOTAL PASS: {pass_full}/19")
print(f"  sh→qok E_global: Sim={mean_full['sh_qok_e']:.3f}, VMS={vms_sh_qok:.3f}, "
      f"Δ={mean_full['sh_qok_e']-vms_sh_qok:+.3f}")
print(f"  ch→qok E_global: Sim={mean_full['ch_qok_e']:.3f}")
print(f"  qok→ch E_global: Sim={mean_full['qok_ch_e']:.3f}")

print("\nDone.")
