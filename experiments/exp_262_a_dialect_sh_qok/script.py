"""
exp_262: H461 — A-Dialect sh→qok Markov Sweep

Question: Does A-dialect's smaller sh→qok gap (Δ=-0.769 vs B-dialect Δ=-1.01) allow a
viable p_sh_qok mechanism in the 12-mechanism A-dialect architecture?

Background:
- A-dialect sh→qok MID E2 gap = Δ=-0.769 (exp_255)
- B-dialect: slope 2.25 E/unit p; max E_global ≈ 1.41 at p=0.20; target 1.905 (gap 1.01)
  → architecturally insufficient at any p without battery regression (exp_243)
- A-dialect gap is 24% smaller (0.769 vs 1.01); might be partially closeable
- B-dialect battery regression: ss_d at p_sh_qok=0.05 at N=30 (18/19)
- NOTE: A-dialect ss_d target differs from B-dialect; different regression risk

Design:
- Base: A-dialect 12-mechanism architecture (exp_258: exp_239 + p_y_y=0.10 + p_o_o=0.10 + filter_other)
- Add p_sh_qok to draw_buf: when prev_onset='sh', seek qok-onset word from buffer
- Sweep p_sh_qok ∈ {0.00, 0.05, 0.10, 0.15, 0.20} at N=5
- Run best value at N=30 (19/19 at N=5, or smallest gap if all regress)
- Monitor: 19-metric battery + sh→qok MID E2 + sh_rate_mid (verify sh distribution)

A-dialect parameters (finalized, exp_258):
  P_BLIND=0.0505, D_BOOST=0.2430, R_LF=0.266, R_MID=0.87, P_STUTTER=0.002
  MU_LEN=5.64, SIGMA_LEN=2.5, CP=0.55, MP=0.90, P_QOKCH=0.12, P_LF=1.0
  P_Y_Y=0.10, P_O_O=0.10
  filter_other applied to all onset distributions
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SWEEP = 5; N_FULL = 30; WINDOW = 20; SEED = 262000

# A-dialect parameters — finalized 12-mechanism architecture
P_BLIND = 0.0505; D_BOOST = 0.2430; R_LF = 0.266; R_MID = 0.87
P_STUTTER = 0.002; MU_LEN = 5.64; SIGMA_LEN = 2.5
CP = 0.55; MP = 0.90; P_QOKCH = 0.12; P_LF = 1.0
P_Y_Y = 0.10; P_O_O = 0.10; P_CHQOK = 0.00

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

def parse_vms_a():
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
    a_lines = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            if folio_dialect.get(fb, 'unknown') != 'A': continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: a_lines.append(words)
    return a_lines

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

def draw_buf(buf, prev_onset, p_sh_qok, rng):
    bl = list(buf)
    if not bl: return None
    if prev_onset == 'qok' and P_QOKCH > 0 and rng.random() < P_QOKCH:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'ch' and P_CHQOK > 0 and rng.random() < P_CHQOK:
        qw = [w for w in bl if get_onset(w) == 'qok']
        if qw: return rng.choice(qw)
    if prev_onset == 'y' and P_Y_Y > 0 and rng.random() < P_Y_Y:
        yw = [w for w in bl if get_onset(w) == 'y']
        if yw: return rng.choice(yw)
    if prev_onset == 'o' and P_O_O > 0 and rng.random() < P_O_O:
        ow = [w for w in bl if get_onset(w) == 'o']
        if ow: return rng.choice(ow)
    if prev_onset == 'sh' and p_sh_qok > 0 and rng.random() < p_sh_qok:
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
            ll_onsets, onset_lf, onset_ll, p_blind, target_lines, p_sh_qok, rng):
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
                    src = draw_buf(buf, prev_onset, p_sh_qok, rng)
                    if src is None: src = random_eva_word(onset_mid, suffix_mid_sup, rng)
                    ew = timm_modify(src, onset_mid, suffix_mid_sup, rng) if rng.random() < MP else src
                else: ew = random_eva_word(onset_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n_words
    return lines[:target_lines]

def compute_metrics(lines, vms_ref):
    aw = [w for l in lines for w in l]; n = len(aw)
    lf = [l[0] for l in lines if l]; ll = [l[-1] for l in lines if len(l)>1]
    mid = [w for l in lines for w in l[1:-1] if len(l)>2]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf  = Counter(get_onset(w) for w in lf)
    oc_ll  = Counter(get_onset(w) for w in ll)
    n_lf, n_ll, n_mid = len(lf), len(ll), len(mid)

    def enr(o, ctr_s, ns):
        s = ctr_s.get(o,0)/ns if ns>0 else 0
        g = oc_all.get(o,0)/n if n>0 else 0
        return s/g if g>0 else 0

    am_r  = sum(1 for w in aw if w.endswith('am'))/n
    ll_am = sum(1 for w in ll if w.endswith('am'))/n_ll if n_ll>0 else 0
    am_ll = ll_am/am_r if am_r>0 else 0
    d_ll  = enr('d', oc_ll, n_ll)
    y_lf  = enr('y', oc_lf, n_lf)
    tb = n-1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o,0)/n
        return bg.get((o,o),0)/(tb*b*b) if b>0 else 1.0
    ss_mean = (ss('qok')+ss('ok')+ss('ch'))/3
    adj = sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)
    qok_lf=enr('qok',oc_lf,n_lf); d_lf=enr('d',oc_lf,n_lf); s_lf=enr('s',oc_lf,n_lf)
    ch_ll=enr('ch',oc_ll,n_ll); ok_ll=enr('ok',oc_ll,n_ll); qok_ll=enr('qok',oc_ll,n_ll)
    ss_d=ss('d'); ss_y=ss('y')
    lf_am=sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf>0 else 0
    mid_am=sum(1 for w in mid if w.endswith('am'))/n_mid if n_mid>0 else 0
    am_lf_enr=lf_am/am_r if am_r>0 else 0
    am_mid_enr=mid_am/am_r if am_r>0 else 0
    edy_rate=sum(1 for w in aw if w.endswith('edy'))/n
    word_len=sum(len(w) for w in aw)/n
    qok_r=oc_all.get('qok',0)/n; ch_r=oc_all.get('ch',0)/n
    qok_ch=bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    # sh→qok MID E2
    oc_mid=Counter(get_onset(w) for w in mid); n_m=max(1,len(mid))
    mid_bg=Counter(); mid_bg_n=0
    for line in lines:
        nn=len(line)
        if nn<4: continue
        for i in range(1,nn-2):
            mid_bg[(get_onset(line[i]),get_onset(line[i+1]))]+=1; mid_bg_n+=1
    def E2_mid(x,y):
        px=oc_mid.get(x,0)/n_m; py=oc_mid.get(y,0)/n_m
        pxy=mid_bg.get((x,y),0)/mid_bg_n if mid_bg_n>0 else 0
        return pxy/(px*py) if px*py>0 else float('nan')

    sh_qok_mid = E2_mid('sh','qok')
    sh_rate_mid = oc_mid.get('sh',0)/n_m

    return dict(am_ll=am_ll,d_ll=d_ll,y_lf=y_lf,ss_mean=ss_mean,adj_rate=adj,
                qok_lf=qok_lf,d_lf=d_lf,s_lf=s_lf,ch_ll=ch_ll,ok_ll=ok_ll,
                qok_ll=qok_ll,ss_d=ss_d,ss_y=ss_y,am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr,edy_rate=edy_rate,word_len_mean=word_len,
                qok_ch=qok_ch,global_am_rate=am_r,
                _sh_qok_mid=sh_qok_mid, _sh_rate_mid=sh_rate_mid)

BATTERY_KEYS = ['am_ll','d_ll','y_lf','ss_mean','adj_rate','qok_lf','d_lf','s_lf',
                'ch_ll','ok_ll','qok_ll','ss_d','ss_y','am_lf_enr','am_mid_enr',
                'edy_rate','word_len_mean','qok_ch','global_am_rate']
PASS_TOL = 0.20

# ─── Main ──────────────────────────────────────────────────────────────────────

print("Parsing VMS A-dialect corpus...")
a_lines = parse_vms_a()
print(f"  A-dialect: {len(a_lines)} lines")

all_words_a = [w for l in a_lines for w in l]
mid_words_a = [w for l in a_lines for w in l[1:-1] if len(l)>2]

# VMS sh→qok MID E2 reference
oc_mid_a = Counter(get_onset(w) for w in mid_words_a); n_mid_a = max(1, len(mid_words_a))
mid_bg_a = Counter(); mid_bg_n_a = 0
for line in a_lines:
    nn = len(line)
    if nn<4: continue
    for i in range(1, nn-2):
        mid_bg_a[(get_onset(line[i]), get_onset(line[i+1]))]+=1; mid_bg_n_a+=1
sh_rate_vms = oc_mid_a.get('sh',0)/n_mid_a
qok_rate_vms = oc_mid_a.get('qok',0)/n_mid_a
sh_qok_e2_vms = (mid_bg_a.get(('sh','qok'),0)/mid_bg_n_a) / (sh_rate_vms*qok_rate_vms) \
                if sh_rate_vms>0 and qok_rate_vms>0 else float('nan')
print(f"  VMS A-dialect: sh→qok E_mid = {sh_qok_e2_vms:.3f}")
print(f"    sh MID rate: {sh_rate_vms:.4f}, qok MID rate: {qok_rate_vms:.4f}")
print(f"    sh→qok count: {mid_bg_a.get(('sh','qok'),0)}, total MID bigrams: {mid_bg_n_a}")

# Build VMS reference metrics for battery
oc_all_a = Counter(get_onset(w) for w in all_words_a)
oc_lf_a  = Counter(get_onset(l[0]) for l in a_lines if l)
oc_ll_a  = Counter(get_onset(l[-1]) for l in a_lines if len(l)>1)
lf_words_a = [l[0] for l in a_lines if l]
ll_words_a = [l[-1] for l in a_lines if len(l)>1]
n_a = len(all_words_a)
am_r_a = sum(1 for w in all_words_a if w.endswith('am'))/n_a
lf_am_a = sum(1 for w in lf_words_a if w.endswith('am'))/len(lf_words_a)
ll_am_a = sum(1 for w in ll_words_a if w.endswith('am'))/len(ll_words_a)

def enr_a(o, ctr_s, ns):
    return (ctr_s.get(o,0)/ns) / (oc_all_a.get(o,0)/n_a) if ns>0 and oc_all_a.get(o,0)>0 else 0

tb_a = n_a-1
bg_a = Counter((get_onset(all_words_a[i]), get_onset(all_words_a[i+1])) for i in range(tb_a))
def ss_a(o):
    b = oc_all_a.get(o,0)/n_a
    return bg_a.get((o,o),0)/(tb_a*b*b) if b>0 else 1.0
qok_r_a = oc_all_a.get('qok',0)/n_a; ch_r_a = oc_all_a.get('ch',0)/n_a
VMS_REF = {
    'am_ll':       ll_am_a/am_r_a,
    'd_ll':        enr_a('d', oc_ll_a, len(ll_words_a)),
    'y_lf':        enr_a('y', oc_lf_a, len(lf_words_a)),
    'ss_mean':     (ss_a('qok')+ss_a('ok')+ss_a('ch'))/3,
    'adj_rate':    sum(1 for i in range(tb_a) if all_words_a[i]==all_words_a[i+1])/max(1,tb_a),
    'qok_lf':      enr_a('qok', oc_lf_a, len(lf_words_a)),
    'd_lf':        enr_a('d', oc_lf_a, len(lf_words_a)),
    's_lf':        enr_a('s', oc_lf_a, len(lf_words_a)),
    'ch_ll':       enr_a('ch', oc_ll_a, len(ll_words_a)),
    'ok_ll':       enr_a('ok', oc_ll_a, len(ll_words_a)),
    'qok_ll':      enr_a('qok', oc_ll_a, len(ll_words_a)),
    'ss_d':        ss_a('d'), 'ss_y': ss_a('y'),
    'am_lf_enr':   lf_am_a/am_r_a,
    'am_mid_enr':  sum(1 for w in mid_words_a if w.endswith('am'))/max(1,len(mid_words_a)) / am_r_a,
    'edy_rate':    sum(1 for w in all_words_a if w.endswith('edy'))/n_a,
    'word_len_mean': sum(len(w) for w in all_words_a)/n_a,
    'qok_ch':      bg_a.get(('qok','ch'),0)/(tb_a*qok_r_a*ch_r_a) if qok_r_a and ch_r_a else 0,
    'global_am_rate': am_r_a,
}
print(f"\n  VMS REF am_ll={VMS_REF['am_ll']:.3f}, ss_d={VMS_REF['ss_d']:.3f}, ss_mean={VMS_REF['ss_mean']:.3f}")

# Build onset distributions WITH filter_other fix
suffix_global = build_suffix(all_words_a)
onset_mid  = filter_other(build_onset_dist(mid_words_a))
onset_lf   = filter_other(build_onset_dist(lf_words_a))
onset_ll   = filter_other(build_onset_dist(ll_words_a))
ll_onsets  = build_ll_onsets(onset_ll, D_BOOST)
suffix_lf_sup  = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
target_lines = len(a_lines)

print(f"  Post-fix onset_mid['sh'] = {onset_mid.get('sh',0):.4f} (VMS MID sh = {sh_rate_vms:.4f})")
print(f"  Post-fix onset_mid['qok'] = {onset_mid.get('qok',0):.4f} (VMS MID qok = {qok_rate_vms:.4f})")

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)

# ─── Sweep ─────────────────────────────────────────────────────────────────────

SWEEP_VALUES = [0.00, 0.05, 0.10, 0.15, 0.20]
print(f"\n{'='*70}")
print(f"SWEEP p_sh_qok ∈ {SWEEP_VALUES}, N={N_SWEEP} each")
print(f"{'='*70}")
print(f"\n  {'p_sh_qok':>8}  {'Pass/19':>7}  {'sh→qok':>8}  {'VMS':>7}  {'Delta':>7}  {'ss_d%':>7}")
print(f"  {'-'*8}  {'-'*7}  {'-'*8}  {'-'*7}  {'-'*7}  {'-'*7}")

sweep_results = []
for p_sh_qok in SWEEP_VALUES:
    all_metrics = []
    for trial in range(N_SWEEP):
        rng = random.Random(SEED + trial*100 + int(p_sh_qok*1000))
        lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, p_sh_qok, rng)
        all_metrics.append(compute_metrics(lines, VMS_REF))
    avg = {k: sum(x[k] for x in all_metrics)/N_SWEEP for k in all_metrics[0]}
    passes = sum(1 for k in BATTERY_KEYS if VMS_REF.get(k,0)>0 and abs(avg.get(k,0)/VMS_REF[k]-1)<=PASS_TOL)
    sh_qok = avg.get('_sh_qok_mid', float('nan'))
    delta = sh_qok - sh_qok_e2_vms if sh_qok == sh_qok else float('nan')
    ss_d_pct = 100*avg.get('ss_d',0)/VMS_REF['ss_d'] if VMS_REF['ss_d']>0 else 0
    print(f"  {p_sh_qok:>8.2f}  {passes:>5}/{len(BATTERY_KEYS)}  {sh_qok:>8.3f}  {sh_qok_e2_vms:>7.3f}  {delta:>+7.3f}  {ss_d_pct:>7.1f}%")
    sweep_results.append((p_sh_qok, passes, avg))

# ─── Best at N=30 ─────────────────────────────────────────────────────────────

# Strategy: prefer 19/19, then smallest |sh→qok delta|
# If none 19/19, use p=0.00 baseline to confirm architecture
best = max(sweep_results, key=lambda x: (x[1], -abs(x[2].get('_sh_qok_mid',0)-sh_qok_e2_vms)))
best_p = best[0]
print(f"\nBest p_sh_qok = {best_p} ({best[1]}/19 at N={N_SWEEP}). Running N={N_FULL}...")

all_metrics_full = []
for trial in range(N_FULL):
    rng = random.Random(SEED + trial*100 + int(best_p*1000))
    lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, best_p, rng)
    all_metrics_full.append(compute_metrics(lines, VMS_REF))
    if (trial+1) % 10 == 0: print(f"  Trial {trial+1}/{N_FULL} done")

avg_full = {k: sum(x[k] for x in all_metrics_full)/N_FULL for k in all_metrics_full[0]}

print(f"\n{'='*70}")
print(f"FULL BATTERY: p_sh_qok={best_p}, N={N_FULL}")
print(f"{'='*70}")
print(f"\n  {'Metric':<18} {'VMS':>8} {'Sim':>8} {'%VMS':>7} {'PASS':>5}")
print(f"  {'-'*50}")
passes_full = 0
for k in BATTERY_KEYS:
    v = avg_full.get(k,0); t = VMS_REF.get(k,0)
    pct = 100*v/t if t>0 else 0
    ok = 'PASS' if t>0 and abs(v/t-1)<=PASS_TOL else 'FAIL'
    if ok=='PASS': passes_full+=1
    flag = ' *' if ok=='FAIL' else ''
    print(f"  {k:<18} {t:>8.4f} {v:>8.4f} {pct:>7.1f}% {ok:>5}{flag}")
print(f"\n  TOTAL: {passes_full}/{len(BATTERY_KEYS)} PASS")

# Non-battery structural check
print(f"\n{'='*70}")
print(f"NON-BATTERY STRUCTURAL CHECK")
print(f"{'='*70}")
sh_qok_full = avg_full.get('_sh_qok_mid', float('nan'))
print(f"  sh→qok MID E2: Sim={sh_qok_full:.3f}, VMS={sh_qok_e2_vms:.3f}, Δ={sh_qok_full-sh_qok_e2_vms:+.3f}")
print(f"  Sim sh MID rate: {avg_full.get('_sh_rate_mid',0):.4f} (VMS: {sh_rate_vms:.4f})")
print(f"  Baseline (p_sh_qok=0.00) sh→qok: {sweep_results[0][2].get('_sh_qok_mid',float('nan')):.3f}")

# Also show slope estimate
if len(SWEEP_VALUES) > 1:
    print(f"\n  Slope analysis (sh→qok E2 vs p_sh_qok):")
    for p_val, n_pass, avg_sv in sweep_results:
        shq = avg_sv.get('_sh_qok_mid', float('nan'))
        print(f"    p={p_val:.2f}: sh→qok={shq:.3f} ({n_pass}/19)")

print(f"\nDone.")
