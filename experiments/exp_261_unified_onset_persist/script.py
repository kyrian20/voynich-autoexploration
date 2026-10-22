"""
exp_261: H462 — Unified Onset Persistence Rule

Question: Can a single p_persist parameter (applied to all onset classes with
MID rate < threshold) replace separate p_y_y=0.10 and p_o_o=0.10 in A-dialect,
while maintaining 19/19 PASS and reproducing both y→y and o→o MID E2?

Architecture base: exact copy of exp_258 with draw_buf variants.

Test conditions (N=5 each):
a. Baseline (p_y_y=0.10, p_o_o=0.10) — reference from exp_258
b. Unified p_persist=0.10, threshold=0.08 (y ~5.2%, o ~5.1% → both below; ok ~6.4%, qok ~6.4% → above)
c. Unified p_persist=0.10, threshold=0.06 (y and o below; ok, qok above)
d. Unified p_persist=0.10, threshold=0.055 (y and o below; ok and qok above; safest)

Best condition runs at N=30.
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SWEEP = 5; N_FULL = 30; WINDOW = 20; SEED = 261000

# A-dialect parameters (exp_239 + p_y_y=0.10)
P_BLIND = 0.0505; D_BOOST = 0.2430; R_LF = 0.266; R_MID = 0.87
P_STUTTER = 0.002; MU_LEN = 5.64; SIGMA_LEN = 2.5
CP = 0.55; MP = 0.90; P_QOKCH = 0.12; P_LF = 1.0; P_CHQOK = 0.00

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
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'
def filter_other(dist):
    filtered = {k: v for k, v in dist.items() if k != 'other'}
    total = sum(filtered.values())
    return {k: v/total for k, v in filtered.items()} if total > 0 else filtered

def parse_vms_a():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); fb = folio_base(folio_raw.lstrip('+*=&~'))
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1
    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}
    a_lines = []
    with open(DATA_PATH, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            fb = folio_base(folio_raw.lstrip('+*=&~'))
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
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf): suf_ctr[suf] += 1; break
        else: suf_ctr['other'] += 1
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
    # A-dialect: d takes absolute probability mass = D_BOOST (24.3%)
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

# ── draw_buf variants ─────────────────────────────────────────────────────────

def draw_buf_separate(buf, prev_onset, p_y_y, p_o_o, rng):
    """Separate p_y_y and p_o_o (current exp_258 architecture)."""
    bl = list(buf)
    if not bl: return None
    if prev_onset == 'qok' and P_QOKCH > 0 and rng.random() < P_QOKCH:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'ch' and P_CHQOK > 0 and rng.random() < P_CHQOK:
        qw = [w for w in bl if get_onset(w) == 'qok']
        if qw: return rng.choice(qw)
    if prev_onset == 'y' and p_y_y > 0 and rng.random() < p_y_y:
        yw = [w for w in bl if get_onset(w) == 'y']
        if yw: return rng.choice(yw)
    if prev_onset == 'o' and p_o_o > 0 and rng.random() < p_o_o:
        ow = [w for w in bl if get_onset(w) == 'o']
        if ow: return rng.choice(ow)
    return rng.choice(bl)

def draw_buf_unified(buf, prev_onset, onset_mid_rates, p_persist, threshold, rng):
    """Unified: apply persist rule to any onset with MID rate < threshold."""
    bl = list(buf)
    if not bl: return None
    if prev_onset == 'qok' and P_QOKCH > 0 and rng.random() < P_QOKCH:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'ch' and P_CHQOK > 0 and rng.random() < P_CHQOK:
        qw = [w for w in bl if get_onset(w) == 'qok']
        if qw: return rng.choice(qw)
    if (prev_onset and p_persist > 0
            and onset_mid_rates.get(prev_onset, 1.0) < threshold
            and rng.random() < p_persist):
        pw = [w for w in bl if get_onset(w) == prev_onset]
        if pw: return rng.choice(pw)
    return rng.choice(bl)

# ── simulation ────────────────────────────────────────────────────────────────

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf, onset_ll, p_blind, target_lines,
            draw_buf_fn, rng):
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
                    src = draw_buf_fn(buf, prev_onset, rng)
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
    # MID bigrams
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
    return dict(am_ll=am_ll,d_ll=d_ll,y_lf=y_lf,ss_mean=ss_mean,adj_rate=adj,
                qok_lf=qok_lf,d_lf=d_lf,s_lf=s_lf,ch_ll=ch_ll,ok_ll=ok_ll,
                qok_ll=qok_ll,ss_d=ss_d,ss_y=ss_y,am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr,edy_rate=edy_rate,word_len_mean=word_len,
                qok_ch=qok_ch,global_am_rate=am_r,
                _y_y=E2_mid('y','y'), _o_o=E2_mid('o','o'),
                _s_s=E2_mid('s','s'), _l_l=E2_mid('l','l'))

BATTERY_KEYS = ['am_ll','d_ll','y_lf','ss_mean','adj_rate','qok_lf','d_lf','s_lf',
                'ch_ll','ok_ll','qok_ll','ss_d','ss_y','am_lf_enr','am_mid_enr',
                'edy_rate','word_len_mean','qok_ch','global_am_rate']
PASS_TOL = 0.20

# ── Setup ─────────────────────────────────────────────────────────────────────

print("Parsing VMS A-dialect corpus...")
a_lines = parse_vms_a()
print(f"  A-dialect: {len(a_lines)} lines")
all_words_a = [w for l in a_lines for w in l]
mid_words_a = [w for l in a_lines for w in l[1:-1] if len(l)>2]
lf_words_a  = [l[0] for l in a_lines if l]
ll_words_a  = [l[-1] for l in a_lines if len(l)>1]
n_a = len(all_words_a)

# Compute onset MID rates (for threshold comparison)
onset_mid_rates = filter_other(build_onset_dist(mid_words_a))
print("\nOnset MID rates (sorted ascending):")
for onset, rate in sorted(onset_mid_rates.items(), key=lambda kv: kv[1]):
    print(f"  {onset:>6}: {rate:.4f}")

# VMS bigram reference
oc_mid_a = Counter(get_onset(w) for w in mid_words_a); n_mid_a = max(1, len(mid_words_a))
mid_bg_a = Counter(); mid_bg_n_a = 0
for line in a_lines:
    nn = len(line)
    if nn<4: continue
    for i in range(1, nn-2):
        mid_bg_a[(get_onset(line[i]), get_onset(line[i+1]))]+=1; mid_bg_n_a+=1
def E2_vms(x, y):
    px = oc_mid_a.get(x,0)/n_mid_a; py = oc_mid_a.get(y,0)/n_mid_a
    pxy = mid_bg_a.get((x,y),0)/mid_bg_n_a if mid_bg_n_a>0 else 0
    return pxy/(px*py) if px*py>0 else float('nan')
y_y_vms = E2_vms('y','y'); o_o_vms = E2_vms('o','o')
s_s_vms = E2_vms('s','s'); l_l_vms = E2_vms('l','l')
print(f"\nVMS MID E2: y→y={y_y_vms:.3f}  o→o={o_o_vms:.3f}  s→s={s_s_vms:.3f}  l→l={l_l_vms:.3f}")

# VMS battery reference
oc_all_a = Counter(get_onset(w) for w in all_words_a)
oc_lf_a  = Counter(get_onset(l[0]) for l in a_lines if l)
oc_ll_a  = Counter(get_onset(l[-1]) for l in a_lines if len(l)>1)
am_r_a = sum(1 for w in all_words_a if w.endswith('am'))/n_a
tb_a = n_a-1; bg_a = Counter((get_onset(all_words_a[i]), get_onset(all_words_a[i+1])) for i in range(tb_a))
def ss_a(o):
    b = oc_all_a.get(o,0)/n_a
    return bg_a.get((o,o),0)/(tb_a*b*b) if b>0 else 1.0
def enr_a(o, ctr_s, ns):
    return (ctr_s.get(o,0)/ns) / (oc_all_a.get(o,0)/n_a) if ns>0 and oc_all_a.get(o,0)>0 else 0
qok_r_a = oc_all_a.get('qok',0)/n_a; ch_r_a = oc_all_a.get('ch',0)/n_a
lf_am_a = sum(1 for w in lf_words_a if w.endswith('am'))/len(lf_words_a)
ll_am_a = sum(1 for w in ll_words_a if w.endswith('am'))/len(ll_words_a)
VMS_REF = {
    'am_ll': ll_am_a/am_r_a, 'd_ll': enr_a('d', oc_ll_a, len(ll_words_a)),
    'y_lf': enr_a('y', oc_lf_a, len(lf_words_a)), 'ss_mean': (ss_a('qok')+ss_a('ok')+ss_a('ch'))/3,
    'adj_rate': sum(1 for i in range(tb_a) if all_words_a[i]==all_words_a[i+1])/max(1,tb_a),
    'qok_lf': enr_a('qok', oc_lf_a, len(lf_words_a)), 'd_lf': enr_a('d', oc_lf_a, len(lf_words_a)),
    's_lf': enr_a('s', oc_lf_a, len(lf_words_a)), 'ch_ll': enr_a('ch', oc_ll_a, len(ll_words_a)),
    'ok_ll': enr_a('ok', oc_ll_a, len(ll_words_a)), 'qok_ll': enr_a('qok', oc_ll_a, len(ll_words_a)),
    'ss_d': ss_a('d'), 'ss_y': ss_a('y'),
    'am_lf_enr': lf_am_a/am_r_a,
    'am_mid_enr': sum(1 for w in mid_words_a if w.endswith('am'))/max(1,len(mid_words_a)) / am_r_a,
    'edy_rate': sum(1 for w in all_words_a if w.endswith('edy'))/n_a,
    'word_len_mean': sum(len(w) for w in all_words_a)/n_a,
    'qok_ch': bg_a.get(('qok','ch'),0)/(tb_a*qok_r_a*ch_r_a) if qok_r_a and ch_r_a else 0,
    'global_am_rate': am_r_a,
}
print(f"VMS REF am_ll={VMS_REF['am_ll']:.3f}, y_lf={VMS_REF['y_lf']:.3f}")

# Build distributions
onset_mid  = filter_other(build_onset_dist(mid_words_a))
onset_lf   = filter_other(build_onset_dist(lf_words_a))
onset_ll   = filter_other(build_onset_dist(ll_words_a))
suffix_global  = build_suffix(all_words_a)
ll_onsets      = build_ll_onsets(onset_ll, D_BOOST)
suffix_lf_sup  = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
target_lines   = len(a_lines)

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)

# Show which onsets fall below each threshold
print("\nOnsets below threshold (would get persist rule):")
for thresh in [0.055, 0.06, 0.07, 0.08]:
    below = [o for o, r in sorted(onset_mid_rates.items(), key=lambda kv: kv[1]) if r < thresh]
    print(f"  thr={thresh}: {below}")

# ── Test Conditions ────────────────────────────────────────────────────────────

# Define draw_buf functions as closures for each condition
cond_draw_bufs = [
    ('Separate p_y_y=0.10 p_o_o=0.10',
     lambda buf, po, rng: draw_buf_separate(buf, po, 0.10, 0.10, rng)),
    ('Unified p=0.10 thr=0.055',
     lambda buf, po, rng, m=onset_mid_rates: draw_buf_unified(buf, po, m, 0.10, 0.055, rng)),
    ('Unified p=0.10 thr=0.060',
     lambda buf, po, rng, m=onset_mid_rates: draw_buf_unified(buf, po, m, 0.10, 0.060, rng)),
    ('Unified p=0.10 thr=0.070',
     lambda buf, po, rng, m=onset_mid_rates: draw_buf_unified(buf, po, m, 0.10, 0.070, rng)),
]

print(f"\n{'='*80}")
print(f"SWEEP: N={N_SWEEP} each condition")
print(f"{'='*80}")
print(f"{'Condition':<40}  {'Pass':>5}  {'y→y':>7}  {'o→o':>7}  {'s→s':>7}  {'l→l':>7}")
print(f"{'VMS reference':.<40}  {'':>5}  {y_y_vms:>7.3f}  {o_o_vms:>7.3f}  {s_s_vms:>7.3f}  {l_l_vms:>7.3f}")
print('-' * 80)

cond_results = []
for cond_name, draw_fn in cond_draw_bufs:
    all_metrics = []
    for trial in range(N_SWEEP):
        rng = random.Random(SEED + trial * 100 + hash(cond_name) % 10000)
        lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, draw_fn, rng)
        all_metrics.append(compute_metrics(lines, VMS_REF))
    avg = {k: sum(x[k] for x in all_metrics)/N_SWEEP for k in all_metrics[0]}
    passes = sum(1 for k in BATTERY_KEYS
                 if VMS_REF.get(k,0)>0 and abs(avg.get(k,0)/VMS_REF[k]-1)<=PASS_TOL)
    y_y_s = avg.get('_y_y', float('nan'))
    o_o_s = avg.get('_o_o', float('nan'))
    s_s_s = avg.get('_s_s', float('nan'))
    l_l_s = avg.get('_l_l', float('nan'))
    print(f"{cond_name:<40}  {passes:>3}/{len(BATTERY_KEYS)}  {y_y_s:>7.3f}  {o_o_s:>7.3f}  {s_s_s:>7.3f}  {l_l_s:>7.3f}")
    cond_results.append((cond_name, passes, avg, draw_fn))

# ── Full battery for the best unified condition ────────────────────────────────

# Pick best unified condition (highest passes among unified)
unified_results = [(n, p, a, fn) for n, p, a, fn in cond_results if 'Unified' in n]
best = max(unified_results, key=lambda x: (x[1], -abs(x[2].get('_y_y',0)-y_y_vms)-abs(x[2].get('_o_o',0)-o_o_vms)))
best_name, best_passes, _, best_fn = best

print(f"\nBest unified condition: '{best_name}' ({best_passes}/19 at N={N_SWEEP})")
print(f"Running N={N_FULL} full battery...")

all_metrics_full = []
for trial in range(N_FULL):
    if trial % 10 == 9: print(f"  Trial {trial+1}/{N_FULL} done")
    rng = random.Random(SEED + 5000 + trial * 100 + hash(best_name) % 10000)
    lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, best_fn, rng)
    all_metrics_full.append(compute_metrics(lines, VMS_REF))

avg_full = {k: sum(x[k] for x in all_metrics_full)/N_FULL for k in all_metrics_full[0]}
passes_full = sum(1 for k in BATTERY_KEYS
                  if VMS_REF.get(k,0)>0 and abs(avg_full.get(k,0)/VMS_REF[k]-1)<=PASS_TOL)

print(f"\n{'='*80}")
print(f"FULL BATTERY N={N_FULL}: {best_name}")
print(f"{'='*80}")
print(f"\n  {'Metric':<20}  {'VMS':>8}  {'Sim':>8}  {'%VMS':>7}  PASS")
print('  ' + '-'*50)
for k in BATTERY_KEYS:
    vms = VMS_REF.get(k, float('nan'))
    sim = avg_full.get(k, float('nan'))
    if math.isnan(vms) or math.isnan(sim) or vms == 0: continue
    pct = sim/vms*100
    passed = abs(pct/100 - 1) <= PASS_TOL
    print(f"  {k:<20}  {vms:>8.4f}  {sim:>8.4f}  {pct:>6.1f}%  {'PASS' if passed else 'FAIL'}")
print(f"\n  TOTAL: {passes_full}/{len(BATTERY_KEYS)} PASS")

print(f"\nStructural checks:")
print(f"  y→y MID E2: Sim={avg_full['_y_y']:.3f}, VMS={y_y_vms:.3f}, Δ={avg_full['_y_y']-y_y_vms:+.3f}")
print(f"  o→o MID E2: Sim={avg_full['_o_o']:.3f}, VMS={o_o_vms:.3f}, Δ={avg_full['_o_o']-o_o_vms:+.3f}")
print(f"  s→s MID E2: Sim={avg_full['_s_s']:.3f}, VMS={s_s_vms:.3f}, Δ={avg_full['_s_s']-s_s_vms:+.3f}")
print(f"  l→l MID E2: Sim={avg_full['_l_l']:.3f}, VMS={l_l_vms:.3f}, Δ={avg_full['_l_l']-l_l_vms:+.3f}")

# Also run the 'separate' condition at N=30 for comparison
print(f"\n{'='*80}")
print("REFERENCE: Separate p_y_y=0.10 p_o_o=0.10, N={N_FULL}")
print(f"{'='*80}")
sep_fn = cond_draw_bufs[0][1]
all_sep = []
for trial in range(N_FULL):
    if trial % 10 == 9: print(f"  Trial {trial+1}/{N_FULL} done")
    rng = random.Random(SEED + 8000 + trial * 100)
    lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, sep_fn, rng)
    all_sep.append(compute_metrics(lines, VMS_REF))
avg_sep = {k: sum(x[k] for x in all_sep)/N_FULL for k in all_sep[0]}
passes_sep = sum(1 for k in BATTERY_KEYS
                 if VMS_REF.get(k,0)>0 and abs(avg_sep.get(k,0)/VMS_REF[k]-1)<=PASS_TOL)
print(f"  Separate p_y_y=0.10 p_o_o=0.10: {passes_sep}/{len(BATTERY_KEYS)} PASS")
print(f"  y→y={avg_sep['_y_y']:.3f}  o→o={avg_sep['_o_o']:.3f}  s→s={avg_sep['_s_s']:.3f}  l→l={avg_sep['_l_l']:.3f}")

print("\nDone.")
