"""
exp_257: H460 — B-Dialect 19-Metric Battery Verification With Fixed 'Other' Onset Distributions

Question: Does the 12-mechanism B-dialect baseline (exp_249 architecture, p_chqok=p_qokch=0.12,
NO p_ot_ot) pass 19/19 battery metrics after applying the 'other' onset fix?

Background: The 'other' onset fix (filter 'other' from onset_mid, onset_lf, onset_ll, renormalize)
changes all onset rates by ~6.4% (renormalization factor). While battery metrics based on enrichment
ratios should be preserved, we need to verify that no metric regresses due to the distribution change.

Design:
- Apply filter_other to all onset distributions
- Run 12-mechanism B-dialect architecture (exp_249: p_qokch=0.12, p_chqok=0.12) at N=30
- Report full 19-metric battery
- Also report ot→ot MID E2 as a non-battery structural check (should match exp_256: Δ=-0.161)
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_FULL = 30; WINDOW = 20; SEED = 257000

# exp_249 12-mechanism B-dialect parameters (NO p_ot_ot)
P_BLIND = 0.115; P_LF = 1.0; CP = 0.55; MP = 0.90
P_QOKCH = 0.12; P_CHQOK = 0.12; P_STUTTER = 0.006
R_LF = 0.12; R_MID = 0.25; MU_LEN = 8.4; SIGMA_LEN = 3.0

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
def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def filter_other(dist):
    filtered = {k: v for k, v in dist.items() if k != 'other'}
    total = sum(filtered.values())
    return {k: v/total for k, v in filtered.items()} if total > 0 else filtered

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

SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']

def build_suffix(words):
    n = len(words); suf_ctr = Counter()
    for w in words:
        matched = False
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf): suf_ctr[suf] += 1; matched = True; break
        if not matched: suf_ctr['other'] += 1
    return {suf: cnt/n for suf, cnt in suf_ctr.items()}

def build_onset_dist(words):
    n = max(1, len(words))
    return {o: cnt/n for o, cnt in Counter(get_onset(w) for w in words).items()}

def make_suppressed_suffix(suffix_global, r_am):
    am_w = suffix_global.get('am', 0.0); new_am = am_w * r_am; delta = am_w - new_am
    non_am = 1.0 - am_w
    return {s: (new_am if s=='am' else w + w/non_am*delta) for s, w in suffix_global.items()} \
           if non_am > 0 else dict(suffix_global)

def build_ll_onsets(onset_ll, d_boost_weight):
    rem = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll.items() if o != 'd'}
    bt = sum(base.values())
    norm = {o: v/bt*rem for o, v in base.items()} if bt > 0 else {}
    norm['d'] = d_boost_weight; return norm

def compute_d_boost(d_global, d_ll_target, d_ll_non_blind_enr, p_blind):
    """d_ll_non_blind_enr = onset_ll['d'] / d_global (enrichment ratio, not raw rate)."""
    return d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind_enr) / p_blind

def make_word_sim(onset, suffix, rng):
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset + rng.choice(['a','ai','o','oi','e','ei']) + suffix
    return onset + suffix

def random_eva_word(onset_w, suffix_w, rng):
    o = rng.choices(list(onset_w.keys()), weights=list(onset_w.values()))[0]
    s = rng.choices(list(suffix_w.keys()), weights=list(suffix_w.values()))[0]
    return make_word_sim(o, s, rng)

def cipher_ll(onset_w, suffix_g, ll_onsets, onset_ll, p_blind, rng):
    if rng.random() < p_blind:
        o = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return o + 'am'
    o = rng.choices(list(onset_ll.keys()), weights=list(onset_ll.values()))[0]
    s = rng.choices(list(suffix_g.keys()), weights=list(suffix_g.values()))[0]
    return make_word_sim(o, s, rng)

def cipher_lf(onset_w, suffix_lf, onset_lf, p_lf, rng):
    if rng.random() < p_lf:
        o = rng.choices(list(onset_lf.keys()), weights=list(onset_lf.values()))[0]
        s = rng.choices(list(suffix_lf.keys()), weights=list(suffix_lf.values()))[0]
        return make_word_sim(o, s, rng)
    return random_eva_word(onset_w, suffix_lf, rng)

def timm_modify(word, onset_w, suffix_mid, rng):
    if not word: return word
    ol = get_onset_len(word); el = get_edy_suffix_len(word)
    ms = ol; me = len(word) - el
    if ms >= me: return random_eva_word(onset_w, suffix_mid, rng)
    op = rng.choice(['replace','insert','delete'])
    if op == 'replace':
        pos = rng.randint(ms, me-1); return word[:pos]+rng.choice(EVA_CHARS)+word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(ms, me); return word[:pos]+rng.choice(EVA_CHARS)+word[pos:]
    else:
        if me-ms<=1: return word[:ms]+rng.choice(EVA_CHARS)+word[ms+1:]
        pos = rng.randint(ms, me-1); return word[:pos]+word[pos+1:]

def draw_buf(buf, prev_onset, rng):
    bl = list(buf)
    if not bl: return None
    if prev_onset == 'qok' and P_QOKCH > 0 and rng.random() < P_QOKCH:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'ch' and P_CHQOK > 0 and rng.random() < P_CHQOK:
        qw = [w for w in bl if get_onset(w) == 'qok']
        if qw: return rng.choice(qw)
    return rng.choice(bl)

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

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf, onset_ll, p_blind, target_lines, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    while len(lines) < target_lines and pos < len(w)-2:
        n_words = max(2, min(20, round(rng.gauss(MU_LEN, SIGMA_LEN))))
        chunk = w[pos:pos+n_words]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0: ew = cipher_lf(onset_mid, suffix_lf_sup, onset_lf, P_LF, rng)
            elif i == len(chunk)-1: ew = cipher_ll(onset_mid, suffix_global, ll_onsets, onset_ll, p_blind, rng)
            else:
                if prev_word is not None and P_STUTTER > 0 and rng.random() < P_STUTTER: ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf(buf, prev_onset, rng)
                    if src is None: src = random_eva_word(onset_mid, suffix_mid_sup, rng)
                    ew = timm_modify(src, onset_mid, suffix_mid_sup, rng) if rng.random() < MP else src
                else: ew = random_eva_word(onset_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n_words
    return lines[:target_lines]

def compute_metrics_full(lines, vms_ref):
    aw = [w for l in lines for w in l]; n = len(aw)
    lf = [l[0] for l in lines if l]; ll = [l[-1] for l in lines if len(l)>1]
    mid = [w for l in lines for w in l[1:-1] if len(l)>2]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf  = Counter(get_onset(w) for w in lf)
    oc_ll  = Counter(get_onset(w) for w in ll)
    n_lf, n_ll, n_mid = len(lf), len(ll), len(mid)

    def enr(o, ctr_s, ns, ctr_a, na):
        s = ctr_s.get(o,0)/ns if ns>0 else 0
        g = ctr_a.get(o,0)/na if na>0 else 0
        return s/g if g>0 else 0

    am_r  = sum(1 for w in aw if w.endswith('am'))/n
    ll_am = sum(1 for w in ll if w.endswith('am'))/n_ll if n_ll>0 else 0
    am_ll = ll_am/am_r if am_r>0 else 0
    d_ll  = enr('d', oc_ll, n_ll, oc_all, n)
    y_lf  = enr('y', oc_lf, n_lf, oc_all, n)

    tb = n-1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o,0)/n
        return bg.get((o,o),0)/(tb*b*b) if b>0 else 1.0
    ss_mean = (ss('qok')+ss('ok')+ss('ch'))/3
    adj = sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)

    qok_lf = enr('qok', oc_lf, n_lf, oc_all, n); d_lf  = enr('d', oc_lf, n_lf, oc_all, n)
    s_lf   = enr('s', oc_lf, n_lf, oc_all, n);   ch_ll = enr('ch', oc_ll, n_ll, oc_all, n)
    ok_ll  = enr('ok', oc_ll, n_ll, oc_all, n);   qok_ll = enr('qok', oc_ll, n_ll, oc_all, n)
    ss_d = ss('d'); ss_y = ss('y')

    lf_am  = sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf>0 else 0
    mid_am = sum(1 for w in mid if w.endswith('am'))/n_mid if n_mid>0 else 0
    am_lf_enr  = lf_am/am_r if am_r>0 else 0
    am_mid_enr = mid_am/am_r if am_r>0 else 0
    edy_rate   = sum(1 for w in aw if w.endswith('edy'))/n
    word_len   = sum(len(w) for w in aw)/n
    qok_r = oc_all.get('qok',0)/n; ch_r = oc_all.get('ch',0)/n
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    # ot→ot MID E2 (non-battery structural check)
    oc_mid = Counter(get_onset(w) for w in mid); n_m = max(1, len(mid))
    mid_bg = Counter(); mid_bg_n = 0
    for line in lines:
        nn = len(line)
        if nn < 4: continue
        for i in range(1, nn-2):
            mid_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1; mid_bg_n += 1
    def E2_mid(x, y):
        px = oc_mid.get(x,0)/n_m; py = oc_mid.get(y,0)/n_m
        pxy = mid_bg.get((x,y),0)/mid_bg_n if mid_bg_n>0 else 0
        return pxy/(px*py) if px*py>0 else float('nan')

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch, global_am_rate=am_r,
                _ot_ot_mid=E2_mid('ot','ot'),
                _ot_mid_rate=oc_mid.get('ot',0)/n_m)

BATTERY_KEYS = ['am_ll','d_ll','y_lf','ss_mean','adj_rate','qok_lf','d_lf','s_lf',
                'ch_ll','ok_ll','qok_ll','ss_d','ss_y','am_lf_enr','am_mid_enr',
                'edy_rate','word_len_mean','qok_ch','global_am_rate']
PASS_TOL = 0.20

def print_battery(avg, vms_ref):
    passes = 0
    print(f"\n  {'Metric':<18} {'VMS':>8} {'Sim':>8} {'%VMS':>7} {'PASS':>5}")
    print(f"  {'-'*50}")
    for k in BATTERY_KEYS:
        v = avg.get(k, 0); t = vms_ref.get(k, 0)
        pct = 100*v/t if t>0 else 0
        ok = 'PASS' if t>0 and abs(v/t-1)<=PASS_TOL else 'FAIL'
        if ok=='PASS': passes+=1
        flag = '*' if ok=='FAIL' else ''
        print(f"  {k:<18} {t:>8.4f} {v:>8.4f} {pct:>7.1f}% {ok:>5}{flag}")
    print(f"\n  TOTAL: {passes}/{len(BATTERY_KEYS)} PASS")
    return passes

# ─── Main ──────────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus...")
b_lines = parse_vms_b()
print(f"  B-dialect: {len(b_lines)} lines")

# Build VMS reference metrics
all_words_b = [w for l in b_lines for w in l]
lf_words_b  = [l[0] for l in b_lines if l]
ll_words_b  = [l[-1] for l in b_lines if len(l)>1]
mid_words_b = [w for l in b_lines for w in l[1:-1] if len(l)>2]
n_b = len(all_words_b)

oc_all_b = Counter(get_onset(w) for w in all_words_b)
oc_lf_b  = Counter(get_onset(w) for w in lf_words_b)
oc_ll_b  = Counter(get_onset(w) for w in ll_words_b)

am_r_b = sum(1 for w in all_words_b if w.endswith('am'))/n_b
ll_am_b = sum(1 for w in ll_words_b if w.endswith('am'))/len(ll_words_b)
lf_am_b = sum(1 for w in lf_words_b if w.endswith('am'))/len(lf_words_b)

def enr_b(o, ctr_s, ns):
    return (ctr_s.get(o,0)/ns) / (oc_all_b.get(o,0)/n_b) if ns>0 and oc_all_b.get(o,0)>0 else 0

VMS_REF = {
    'am_ll': ll_am_b/am_r_b,
    'd_ll': enr_b('d', oc_ll_b, len(ll_words_b)),
    'y_lf': enr_b('y', oc_lf_b, len(lf_words_b)),
    'ss_mean': 1.164,
    'adj_rate': 0.009,
    'qok_lf': enr_b('qok', oc_lf_b, len(lf_words_b)),
    'd_lf': enr_b('d', oc_lf_b, len(lf_words_b)),
    's_lf': enr_b('s', oc_lf_b, len(lf_words_b)),
    'ch_ll': enr_b('ch', oc_ll_b, len(ll_words_b)),
    'ok_ll': enr_b('ok', oc_ll_b, len(ll_words_b)),
    'qok_ll': enr_b('qok', oc_ll_b, len(ll_words_b)),
    'ss_d': 1.291, 'ss_y': 1.955,
    'am_lf_enr': lf_am_b/am_r_b,
    'am_mid_enr': 0.195,
    'edy_rate': sum(1 for w in all_words_b if w.endswith('edy'))/n_b,
    'word_len_mean': 5.400,
    'qok_ch': 1.267,
    'global_am_rate': am_r_b,
}

# VMS ot→ot MID for comparison
oc_mid_b = Counter(get_onset(w) for w in mid_words_b)
mid_bg_b = Counter(); mid_bg_n_b = 0
for line in b_lines:
    nn = len(line)
    if nn < 4: continue
    for i in range(1, nn-2):
        mid_bg_b[(get_onset(line[i]), get_onset(line[i+1]))] += 1; mid_bg_n_b += 1
vms_ot_rate = oc_mid_b.get('ot',0)/max(1,len(mid_words_b))
vms_ot_ot = mid_bg_b.get(('ot','ot'),0)/mid_bg_n_b / (vms_ot_rate**2) if vms_ot_rate>0 else 0
print(f"  VMS ot→ot E_mid = {vms_ot_ot:.3f} (VMS ot rate = {vms_ot_rate:.4f})")

# Build onset distributions WITH fix
suffix_global = build_suffix(all_words_b)
onset_mid_raw = build_onset_dist(mid_words_b)
onset_mid = filter_other(onset_mid_raw)  # FIX
onset_lf_raw = build_onset_dist(lf_words_b)
onset_lf = filter_other(onset_lf_raw)
onset_ll_raw = build_onset_dist(ll_words_b)
onset_ll = filter_other(onset_ll_raw)

d_global = oc_all_b.get('d',0)/n_b
d_ll_rate = oc_ll_b.get('d',0)/len(ll_words_b)
d_ll_target = d_ll_rate/d_global if d_global>0 else 1.0
# Must pass enrichment ratio (onset_ll['d']/d_global), not raw rate — matches exp_249 formula
d_ll_non_blind_enr = onset_ll.get('d',0) / d_global if d_global>0 else 0
d_boost = compute_d_boost(d_global, d_ll_target, d_ll_non_blind_enr, P_BLIND)
ll_onsets = build_ll_onsets(onset_ll, d_boost)
suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
target_lines = len(b_lines)

print(f"  Post-fix onset_mid sum = {sum(onset_mid.values()):.4f}")
print(f"  Post-fix onset_mid['ot'] = {onset_mid.get('ot',0):.4f} (VMS MID = {vms_ot_rate:.4f})")

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)

print(f"\nRunning N={N_FULL} simulations (12-mechanism B-dialect, fixed distributions)...")
all_metrics = []
for trial in range(N_FULL):
    rng = random.Random(SEED + trial*100)
    lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, rng)
    m = compute_metrics_full(lines, VMS_REF)
    all_metrics.append(m)
    if (trial+1) % 10 == 0: print(f"  Trial {trial+1}/{N_FULL} done")

avg = {k: sum(x[k] for x in all_metrics)/N_FULL for k in all_metrics[0]}

print(f"\n{'='*70}")
print(f"19-METRIC BATTERY: 12-MECHANISM B-DIALECT WITH 'OTHER' ONSET FIX, N={N_FULL}")
print(f"{'='*70}")
passes = print_battery(avg, VMS_REF)

print(f"\n{'='*70}")
print(f"NON-BATTERY STRUCTURAL CHECK")
print(f"{'='*70}")
print(f"  ot→ot MID E2: Sim={avg['_ot_ot_mid']:.3f}, VMS={vms_ot_ot:.3f}, Δ={avg['_ot_ot_mid']-vms_ot_ot:+.3f}")
print(f"  Sim ot MID rate: {avg['_ot_mid_rate']:.4f} (VMS: {vms_ot_rate:.4f})")
print(f"\nDone.")
