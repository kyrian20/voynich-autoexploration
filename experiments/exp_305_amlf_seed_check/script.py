"""
exp_305: am_lf_enr Seed Sensitivity in 17-Mechanism clamp_sparse Architecture (H507)

exp_304 clamp_sparse gave am_lf_enr=125.3% with SEED=304000.
This experiment tests whether the failure is seed-dependent.
If majority of seeds give am_lf_enr < 120%, architecture is effectively 19/19.

Also tests R_LF=0.10 (reduced) to see if am_lf_enr can be pulled below ceiling.
"""

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_PER_SEED = 10
TARGET_LINES = 2411
WINDOW   = 20

P_BLIND   = 0.115; P_LF    = 1.0;   CP       = 0.55; MP       = 0.90
P_QOKCH   = 0.12;  P_CHQOK = 0.12;  P_STUTTER = 0.006
R_MID   = 0.20;  MU_LEN   = 8.4;  SIGMA_LEN = 3.0
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
VMS_REF = {
    'am_ll': 6.5498, 'd_ll': 1.3625, 'y_lf': 3.1837, 'ss_mean': 1.1640,
    'adj_rate': 0.0090, 'qok_lf': 0.7450, 'd_lf': 2.1178, 's_lf': 4.4422,
    'ch_ll': 0.9653, 'ok_ll': 1.0028, 'qok_ll': 0.6121, 'ss_d': 1.5850,
    'ss_y': 1.9550, 'am_lf_enr': 0.1225, 'am_mid_enr': 0.1954,
    'edy_rate': 0.1940, 'word_len_mean': 5.4000, 'qok_ch': 1.2670,
    'global_am_rate': 0.0203,
}
BATTERY_19 = list(VMS_REF.keys())
PASS_TOL = 0.20

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
    return 'B' if total > 0 and (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

def parse_vms_b():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r') as f:
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
    with open(DATA_PATH, 'r') as f:
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
        if (edy_len := get_edy_suffix_len(w)):
            midfix = w[onset_len:len(w)-edy_len]
            if len(midfix) >= 1: midfix = midfix[:-1]
        else:
            midfix = w[onset_len:len(w)-suf_len]
        midfix_cnt[midfix] += 1
    total = sum(midfix_cnt.values())
    if total == 0: return {}, 0.0
    p = sum(v for k,v in midfix_cnt.items() if k!='') / total
    ne = {mf: v for mf, v in midfix_cnt.items() if mf != ''}
    nt = sum(ne.values())
    return ({mf: v/nt for mf, v in ne.items()} if nt else {}), p

def compute_vms_distributions(b_lines):
    all_words = [w for l in b_lines for w in l]
    lf_words  = [l[0] for l in b_lines if l]
    ll_words  = [l[-1] for l in b_lines if len(l) > 1]
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words)
    def build_onset(words):
        cnt = Counter(get_onset(w) for w in words); cnt.pop('other', None)
        t = sum(cnt.values()); return {k: v/t for k,v in cnt.items()} if t else {}
    def build_suffix(words):
        cnt = Counter(get_suffix(w) for w in words); t = sum(cnt.values())
        return {k: v/t for k,v in cnt.items()} if t else {}
    onset_global = build_onset(all_words); onset_lf = build_onset(lf_words)
    onset_ll = build_onset(ll_words); onset_mid = build_onset(mid_words)
    suffix_global = build_suffix(all_words)
    mid_nemed, _ = build_midfix_dist(mid_words)
    lf_nemed, _  = build_midfix_dist(lf_words)
    ll_nemed, _  = build_midfix_dist(ll_words)
    am_r  = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words)
    d_r   = Counter(get_onset(w) for w in all_words).get('d', 0) / n
    ll_d  = Counter(get_onset(w) for w in ll_words).get('d', 0) / len(ll_words)
    return dict(onset_global=onset_global, onset_lf=onset_lf, onset_ll=onset_ll,
                onset_mid=onset_mid, suffix_global=suffix_global,
                mid_nemed=mid_nemed, lf_nemed=lf_nemed, ll_nemed=ll_nemed,
                am_r=am_r, am_ll_target=ll_am/am_r if am_r else 0,
                d_r=d_r, d_ll_target=ll_d/d_r if d_r else 0,
                n=n, mid_words=mid_words)

def make_suppressed_suffix(sg, r_am):
    aw = sg.get('am', 0); naw = aw*r_am; delta = aw-naw; non_am = 1.0-aw
    return {s: (naw if s=='am' else w+(w/non_am)*delta if non_am>0 else w) for s,w in sg.items()}
def apply_suffix_length_bias(sw, word_idx, beta):
    if beta == 0.0 or word_idx < IDX_THRESH: return sw
    nw = {s: w*math.exp(-beta*max(0,len(s)-SHORT_THRESH)) if s!='other' else w for s,w in sw.items()}
    t = sum(nw.values()); return {s: v/t for s,v in nw.items()} if t > 0 else sw
def compute_d_boost(d_g, d_ll_t, d_ll_nb, pb):
    return d_g * (d_ll_t - (1-pb) * d_ll_nb) / pb
def build_ll_onsets(oll, d_boost):
    rem = 1.0-d_boost; base = {o:v for o,v in oll.items() if o!='d'}; bt = sum(base.values())
    norm = {o: v/bt*rem for o,v in base.items()} if bt else {}; norm['d'] = d_boost; return norm
def weighted_choice(rng, dist):
    r=rng.random(); cum=0.0
    for k,v in dist.items():
        cum+=v
        if r<cum: return k
    return list(dist.keys())[-1]
def sample_midfix(rng, ned, pne):
    return weighted_choice(rng, ned) if ned and rng.random()<pne else ''
def make_word_sim(onset, suffix, rng, ned, pne):
    if suffix=='other': return onset+suffix
    mf = sample_midfix(rng, ned, pne)
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset+mf+rng.choice(['a','ai','o','oi','e','ei'])+suffix
    return onset+mf+suffix
def random_eva_word_onset_biased(ow, sw, rng, ned, pne, wi, alpha, beta):
    if alpha==0.0: norm=ow
    else:
        nw = {o: w*(1+alpha*wi) if o in SHORT_ONSETS else w for o,w in ow.items()}
        t = sum(nw.values()); norm = {o: w/t for o,w in nw.items()}
    onset = weighted_choice(rng, norm)
    biased = apply_suffix_length_bias(sw, wi, beta)
    suffix = weighted_choice(rng, biased)
    return make_word_sim(onset, suffix, rng, ned, pne)
def cipher_ll(oll, ll_on, sg, pb, rng, lln):
    if rng.random()<pb:
        return weighted_choice(rng, ll_on)+'am'
    return make_word_sim(weighted_choice(rng, oll), weighted_choice(rng, sg), rng, lln, P_LL_MF)
def cipher_lf(om, olf, slf, plf, rng, lfn):
    if rng.random()<plf:
        return make_word_sim(weighted_choice(rng, olf), weighted_choice(rng, slf), rng, lfn, P_LF_MF)
    return random_eva_word_onset_biased(om, slf, rng, {}, 0.0, 0, 0.0, 0.0)
def timm_modify(word, om, sm, rng):
    if not word: return word
    ol = get_onset_len(word); el = get_edy_suffix_len(word)
    ms = ol; me = len(word)-el
    if ms >= me:
        return random_eva_word_onset_biased(om, sm, rng, {}, 0.0, 0, 0.0, 0.0)
    op = rng.choice(['replace','insert','delete'])
    if op=='replace':
        p = rng.randint(ms, me-1); return word[:p]+rng.choice(EVA_CHARS)+word[p+1:]
    elif op=='insert':
        p = rng.randint(ms, me); return word[:p]+rng.choice(EVA_CHARS)+word[p:]
    else:
        if me-ms<=1: return word[:ms]+rng.choice(EVA_CHARS)+word[ms+1:]
        p = rng.randint(ms, me-1); return word[:p]+word[p+1:]
def clamp_to_lexicon(word, lexicons, rng):
    onset = get_onset(word)
    if onset in lexicons and lexicons[onset]: return rng.choice(lexicons[onset])
    return word
def draw_buf_lb(buf, po, pqch, pcqk, rng, wi, gamma):
    bl = list(buf)
    if not bl: return None
    pref = None
    if po=='qok' and pqch>0 and rng.random()<pqch:
        cw=[w for w in bl if get_onset(w)=='ch']
        if cw: pref=cw
    elif po=='ch' and pcqk>0 and rng.random()<pcqk:
        qw=[w for w in bl if get_onset(w)=='qok']
        if qw: pref=qw
    cands = pref if pref else bl
    if gamma==0.0: return rng.choice(cands)
    Lt = L_BASE+L_SLOPE*wi
    wts = [math.exp(-gamma*(len(w)-Lt)**2) for w in cands]
    t = sum(wts)
    if t==0: return rng.choice(cands)
    r = rng.random()*t; cum=0.0
    for w,wt in zip(cands, wts):
        cum+=wt
        if r<cum: return w
    return cands[-1]

def build_lexicons(mid_words):
    counts = defaultdict(Counter)
    for w in mid_words:
        onset = get_onset(w)
        if onset in {'qok','ok','ot','qot'}: counts[onset][w] += 1
    lex = {}
    for onset, cnt in counts.items():
        lex_list = []
        for w, c in cnt.items(): lex_list.extend([w]*c)
        lex[onset] = lex_list
    return lex

def run_sim(latin_words, om, sg, slf, sms, ll_on, olf, oll, mned, lfned, llned, rng, lex):
    w=list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    po=None; pw=None
    while len(lines)<TARGET_LINES and pos<len(w)-2:
        n=max(2,min(20,round(rng.gauss(MU_LEN,SIGMA_LEN))))
        chunk=w[pos:pos+n]
        if len(chunk)<2: pos+=len(chunk); continue
        line=[]; wi=0
        for i, word in enumerate(chunk):
            if i==0: ew=cipher_lf(om, olf, slf, P_LF, rng, lfned)
            elif i==len(chunk)-1: ew=cipher_ll(oll, ll_on, sg, P_BLIND, rng, llned)
            else:
                if pw is not None and rng.random()<P_STUTTER: ew=pw
                elif buf and rng.random()<CP:
                    src=draw_buf_lb(buf, po, P_QOKCH, P_CHQOK, rng, wi, GAMMA)
                    if src is None: src=rng.choice(list(buf))
                    if rng.random()<MP:
                        ew=timm_modify(src, om, sms, rng)
                        if lex: ew=clamp_to_lexicon(ew, lex, rng)
                    else: ew=src
                else:
                    ew=random_eva_word_onset_biased(om, sms, rng, mned, P_MF, wi, ALPHA, BETA)
                    if lex: ew=clamp_to_lexicon(ew, lex, rng)
                buf.append(ew); wi+=1
            po=get_onset(ew); pw=ew; line.append(ew)
        lines.append(line); pos+=n
    return lines[:TARGET_LINES]

def compute_metrics(lines):
    aw=[w for l in lines for w in l]; n=len(aw)
    if n<100: return None
    lf=[l[0] for l in lines if l]
    ll=[l[-1] for l in lines if len(l)>1]
    mid=[w for l in lines for w in l[1:-1] if len(l)>2]
    oc_all=Counter(get_onset(w) for w in aw)
    oc_lf=Counter(get_onset(w) for w in lf)
    oc_ll=Counter(get_onset(w) for w in ll)
    nlf,nll,nmid=len(lf),len(ll),len(mid)
    def enr(onset, cs, ns):
        s=cs.get(onset,0)/ns if ns else 0
        g=oc_all.get(onset,0)/n if n else 0
        return s/g if g>0 else 0
    am_r=sum(1 for w in aw if w.endswith('am'))/n
    ll_am=sum(1 for w in ll if w.endswith('am'))/nll if nll else 0
    am_ll=ll_am/am_r if am_r else 0
    lf_am_rate=sum(1 for w in lf if w.endswith('am'))/nlf if nlf else 0
    mid_am_rate=sum(1 for w in mid if w.endswith('am'))/nmid if nmid else 0
    am_lf_enr=lf_am_rate/am_r if am_r else 0
    am_mid_enr=mid_am_rate/am_r if am_r else 0
    d_ll=enr('d',oc_ll,nll); y_lf=enr('y',oc_lf,nlf)
    tb=n-1
    bg=Counter((get_onset(aw[i]),get_onset(aw[i+1])) for i in range(tb))
    def ss(o): b=oc_all.get(o,0)/n; return bg.get((o,o),0)/(tb*b*b) if b>0 and tb>0 else 1.0
    ss_mean=(ss('qok')+ss('ok')+ss('ch'))/3
    adj=sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)
    qok_lf=enr('qok',oc_lf,nlf); d_lf=enr('d',oc_lf,nlf); s_lf=enr('s',oc_lf,nlf)
    ch_ll=enr('ch',oc_ll,nll); ok_ll=enr('ok',oc_ll,nll); qok_ll=enr('qok',oc_ll,nll)
    ss_d=ss('d'); ss_y=ss('y')
    edy=sum(1 for w in aw if w.endswith('edy') or w.endswith('eedy'))/n
    wl=sum(len(w) for w in aw)/n
    qok_r=oc_all.get('qok',0)/n; ch_r=oc_all.get('ch',0)/n
    qok_ch=bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r and tb>0 else 0
    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy, word_len_mean=wl,
                qok_ch=qok_ch, global_am_rate=am_r)

def passes(sv, vv, tol=PASS_TOL):
    if vv==0: return True
    r=sv/vv; return (1-tol)<=r<=(1+tol)
def agg(ml, key):
    vals=[x[key] for x in ml if key in x]; return sum(vals)/len(vals) if vals else 0

ENGLISH_SW = {'the','and','of','to','a','in','that','is','was','he','it','for','on','are',
              'as','with','his','they','at','be','this','have','from','or','had','by','not',
              'but','what','all','were','we'}
def load_latin(path):
    with open(path, errors='replace') as f: text = f.read()
    words = []
    for p in re.split(r'\n\s*\n', text):
        ws = re.findall(r'\b[a-zA-Z]+\b', p)
        if not ws: continue
        if sum(1 for w in ws if w.lower() in ENGLISH_SW)/len(ws) < 0.08: words.extend(ws)
    return words

print("exp_305: am_lf_enr Seed Sensitivity — 17-Mechanism clamp_sparse (H507)")
print("=" * 65)

b_lines = parse_vms_b()
vms = compute_vms_distributions(b_lines)
vms_mid = vms['mid_words']
latin_words = load_latin(LATIN_CORPUS)
print(f"VMS B: {len(b_lines)} lines, {vms['n']} words")

sg = vms['suffix_global']
om = vms['onset_mid']; olf = vms['onset_lf']; oll = vms['onset_ll']
d_global = vms['onset_global'].get('d',0)
d_ll_nb = oll.get('d',0)/d_global if d_global else 0
db = max(0.0, min(1.0, compute_d_boost(d_global, vms['d_ll_target'], d_ll_nb, P_BLIND)))
ll_on = build_ll_onsets(oll, db)
mned = vms['mid_nemed']; lfned = vms['lf_nemed']; llned = vms['ll_nemed']

# Build sparse lexicons (clamp_sparse: qok/ok/ot/qot)
lex_sparse = build_lexicons(vms_mid)
for onset, lex in lex_sparse.items():
    print(f"  Lexicon: {onset} → {len(set(lex))} types")

# Test seeds
SEEDS = [100, 200, 500, 1000, 5000, 304000, 287000, 301000, 10000, 50000]
print(f"\n  Seed sensitivity test (N={N_PER_SEED} per seed, clamp_sparse, R_LF=0.12):")
print(f"  {'Seed':8s}  {'Pass':7s}  {'am_lf_enr':10s}  {'%VMS':7s}  {'edy_rate':9s}  {'am_mid_enr':12s}")
print(f"  {'-'*65}")

pass_counts = []; am_lf_vals = []
for seed in SEEDS:
    R_LF = 0.12
    slf = make_suppressed_suffix(sg, R_LF)
    sms = make_suppressed_suffix(sg, R_MID)
    ml = []
    rng = random.Random(seed)
    for trial in range(N_PER_SEED):
        lines = run_sim(latin_words, om, sg, slf, sms, ll_on, olf, oll, mned, lfned, llned, rng, lex_sparse)
        m = compute_metrics(lines)
        if m: ml.append(m)
    pc = sum(1 for metric in BATTERY_19 if passes(agg(ml, metric), VMS_REF[metric]))
    amlf = agg(ml, 'am_lf_enr')
    amm = agg(ml, 'am_mid_enr')
    edy = agg(ml, 'edy_rate')
    pct = amlf/VMS_REF['am_lf_enr']*100
    ok = 'PASS' if passes(amlf, VMS_REF['am_lf_enr']) else 'FAIL'
    print(f"  {seed:8d}  {pc:4d}/19  {amlf:.4f} {ok}  {pct:6.1f}%  {edy:.4f}  {amm:.4f}")
    pass_counts.append(pc); am_lf_vals.append(amlf)

print(f"\n  am_lf_enr summary: mean={sum(am_lf_vals)/len(am_lf_vals):.4f}, "
      f"min={min(am_lf_vals):.4f}, max={max(am_lf_vals):.4f}")
pct_pass = sum(1 for v in am_lf_vals if passes(v, VMS_REF['am_lf_enr']))*100//len(am_lf_vals)
print(f"  am_lf_enr PASS rate: {pct_pass}%")
print(f"  Battery: {sum(pass_counts)} total passes / {len(pass_counts)} seed groups × 19 = {sum(pass_counts)/len(pass_counts):.1f} avg")

# Also test R_LF=0.10 with original seed
print(f"\n  R_LF sensitivity (R_LF=0.10 vs 0.12, SEED=304000, N=10):")
for r_lf in [0.12, 0.10, 0.08]:
    slf = make_suppressed_suffix(sg, r_lf)
    sms = make_suppressed_suffix(sg, R_MID)
    ml = []
    rng = random.Random(304000)
    for trial in range(N_PER_SEED):
        lines = run_sim(latin_words, om, sg, slf, sms, ll_on, olf, oll, mned, lfned, llned, rng, lex_sparse)
        m = compute_metrics(lines)
        if m: ml.append(m)
    pc = sum(1 for metric in BATTERY_19 if passes(agg(ml, metric), VMS_REF[metric]))
    amlf = agg(ml, 'am_lf_enr')
    amll = agg(ml, 'am_ll')
    pct = amlf/VMS_REF['am_lf_enr']*100
    ok = 'PASS' if passes(amlf, VMS_REF['am_lf_enr']) else 'FAIL'
    print(f"  R_LF={r_lf:.2f}: {pc}/19, am_lf_enr={amlf:.4f} ({pct:.1f}%) {ok}, am_ll={amll:.3f}")

print("\nDone.")
