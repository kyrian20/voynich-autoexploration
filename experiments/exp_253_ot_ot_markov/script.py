"""
exp_253: H447 — ot→ot Self-Succession Markov Rule

Question: Does adding p_ot_ot (when prev_onset='ot', seek ot-onset word from buffer)
fix the B-dialect ot→ot MID E2 gap (sim=1.410 vs VMS=1.887) without regressing
the 19-metric battery?

Context:
- ot→ot is GRAMMATICAL (H448, exp_252): HHI/null=1.23× — dispersed vocabulary
- ot→ot sim gap Δ=0.477 (from 1.410 to 1.887 target)
- Compare: qok→ch Δ=0.27 → succeeded (p_qokch=0.12)
- Compare: sh→qok Δ=1.01 → failed (max achievable ~1.41)
- ot→ot Δ=0.477 is between these two: potentially achievable

Design:
1. Baseline: confirm sim ot→ot MID E2 at N=5 using exp_236 (B-dialect) architecture
   including both p_qokch=0.12 and p_chqok=0.12
2. Sweep p_ot_ot ∈ {0.05, 0.10, 0.15, 0.20} at N=5
3. If any value gives ≥18/19 and improves ot→ot toward VMS: run best at N=30
4. Report whether p_ot_ot is a viable fourth Markov rule

Exp_236+exp_249 parameters (FIXED, B-dialect):
  p_blind=0.115, d_boost=9.13%, r_lf=0.12, r_mid=0.25, p_stutter=0.006
  mu_len=8.4, cp=0.55, mp=0.90, p_qokch=0.12, p_chqok=0.12, p_lf=1.0
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SWEEP = 5; N_FULL = 30; WINDOW = 20; SEED = 253000; PASS_TOL = 0.20

# Fixed B-dialect parameters (exp_236 + p_chqok=0.12 from exp_249)
P_BLIND = 0.115; D_BOOST = 0.0913; R_LF = 0.12; R_MID = 0.25
P_STUTTER = 0.006; MU_LEN = 8.4; SIGMA_LEN = 2.5
CP = 0.55; MP = 0.90; P_QOKCH = 0.12; P_CHQOK = 0.12; P_LF = 1.0

EVA_CHARS = list('acdehiklmnoqrsty')
ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]
BATTERY_KEYS = ['am_ll','d_ll','y_lf','ss_mean','adj_rate','qok_lf','d_lf','s_lf',
                'ch_ll','ok_ll','qok_ll','ss_d','ss_y','am_lf_enr','am_mid_enr',
                'edy_rate','word_len_mean','qok_ch','global_am_rate']

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

def parse_vms_b_dialect():
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

def compute_vms_targets(lines):
    all_words = [w for l in lines for w in l]
    lf_words  = [l[0]  for l in lines if l]
    ll_words  = [l[-1] for l in lines if len(l) > 1]
    mid_words = [w for l in lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words); n_mid = max(1, len(mid_words))
    oc_all = Counter(get_onset(w) for w in all_words)
    oc_lf  = Counter(get_onset(w) for w in lf_words)
    oc_ll  = Counter(get_onset(w) for w in ll_words)
    oc_mid = Counter(get_onset(w) for w in mid_words)
    SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']
    suf_ctr = Counter()
    for w in all_words:
        matched = False
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf): suf_ctr[suf] += 1; matched = True; break
        if not matched: suf_ctr['other'] += 1
    suffix_global = {suf: cnt/n for suf, cnt in suf_ctr.items()}
    am_r = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am_r = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words)
    lf_am_r = sum(1 for w in lf_words if w.endswith('am')) / len(lf_words)
    mid_am_r = sum(1 for w in mid_words if w.endswith('am')) / n_mid
    def enr(o, cs, ns, ca, na):
        s=cs.get(o,0)/ns if ns else 0; g=ca.get(o,0)/na if na else 0; return s/g if g>0 else 0
    tb = n - 1
    bg = Counter((get_onset(all_words[i]), get_onset(all_words[i+1])) for i in range(tb))
    def ss(o): b=oc_all.get(o,0)/n; return bg.get((o,o),0)/(tb*b*b) if b>0 else 1.0

    # MID-only bigrams
    mid_bg = Counter(); mid_bg_n = 0
    for line in lines:
        nn = len(line)
        if nn < 4: continue
        for i in range(1, nn-2):
            mid_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1; mid_bg_n += 1
    def E2_mid(x, y):
        pxy = mid_bg.get((x,y),0)/mid_bg_n if mid_bg_n>0 else 0
        px = oc_mid.get(x,0)/n_mid; py = oc_mid.get(y,0)/n_mid
        return pxy/(px*py) if px*py>0 else 0

    return {
        'onset_global': {o: cnt/n for o, cnt in oc_all.items()},
        'onset_lf': {o: cnt/len(lf_words) for o, cnt in oc_lf.items()},
        'onset_ll': {o: cnt/len(ll_words) for o, cnt in oc_ll.items()},
        'onset_mid': {o: cnt/n_mid for o, cnt in oc_mid.items()},
        'suffix_global': suffix_global, 'n_lines': len(lines), 'n': n,
        'am_r': am_r, 'll_am_rate': ll_am_r, 'lf_am_rate': lf_am_r, 'mid_am_rate': mid_am_r,
        'am_ll': ll_am_r / am_r if am_r else 0,
        'd_ll': enr('d', oc_ll, len(ll_words), oc_all, n),
        'y_lf': enr('y', oc_lf, len(lf_words), oc_all, n),
        'ss_mean': (ss('qok')+ss('ok')+ss('ch'))/3,
        'adj_rate': sum(1 for i in range(tb) if all_words[i]==all_words[i+1])/max(1,tb),
        'qok_lf': enr('qok', oc_lf, len(lf_words), oc_all, n),
        'd_lf': enr('d', oc_lf, len(lf_words), oc_all, n),
        's_lf': enr('s', oc_lf, len(lf_words), oc_all, n),
        'ch_ll': enr('ch', oc_ll, len(ll_words), oc_all, n),
        'ok_ll': enr('ok', oc_ll, len(ll_words), oc_all, n),
        'qok_ll': enr('qok', oc_ll, len(ll_words), oc_all, n),
        'ss_d': ss('d'), 'ss_y': ss('y'),
        'am_lf_enr': lf_am_r / am_r if am_r else 0,
        'am_mid_enr': mid_am_r / am_r if am_r else 0,
        'edy_rate': sum(1 for w in all_words if w.endswith('edy'))/n,
        'word_len_mean': sum(len(w) for w in all_words)/n,
        'qok_ch': bg.get(('qok','ch'),0)/(tb*(oc_all.get('qok',0)/n)*(oc_all.get('ch',0)/n))
                  if oc_all.get('qok',0) and oc_all.get('ch',0) else 0,
        'global_am_rate': am_r,
        '_ot_ot_mid': E2_mid('ot','ot'),
        '_sh_qok_mid': E2_mid('sh','qok'),
        '_qok_ch_mid': E2_mid('qok','ch'),
        '_ch_qok_mid': E2_mid('ch','qok'),
        'n_mid_bigrams': mid_bg_n,
    }

def make_suppressed_suffix(suffix_global, r_am):
    am_w = suffix_global.get('am', 0.0); new_am = am_w * r_am; delta = am_w - new_am
    non_am = 1.0 - am_w
    return {s: (new_am if s=='am' else w + w/non_am*delta) for s, w in suffix_global.items()} \
           if non_am > 0 else dict(suffix_global)

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    rem = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o != 'd'}
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

def draw_buf(buf, prev_onset, p_qokch, p_chqok, p_ot_ot, rng):
    bl = list(buf)
    if not bl: return None
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'ch' and p_chqok > 0 and rng.random() < p_chqok:
        qw = [w for w in bl if get_onset(w) == 'qok']
        if qw: return rng.choice(qw)
    if prev_onset == 'ot' and p_ot_ot > 0 and rng.random() < p_ot_ot:
        ow = [w for w in bl if get_onset(w) == 'ot']
        if ow: return rng.choice(ow)
    return rng.choice(bl)

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf, onset_ll, p_blind, target_lines, p_ot_ot, rng):
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
                    src = draw_buf(buf, prev_onset, P_QOKCH, P_CHQOK, p_ot_ot, rng)
                    if src is None: src = random_eva_word(onset_mid, suffix_mid_sup, rng)
                    ew = timm_modify(src, onset_mid, suffix_mid_sup, rng) if rng.random() < MP else src
                else: ew = random_eva_word(onset_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n_words
    return lines[:target_lines]

def compute_metrics(lines):
    aw = [w for l in lines for w in l]; n = len(aw)
    if n < 100: return None
    lf = [l[0] for l in lines if l]; ll = [l[-1] for l in lines if len(l)>1]
    mid = [w for l in lines for w in l[1:-1] if len(l)>2]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf = Counter(get_onset(w) for w in lf); oc_ll = Counter(get_onset(w) for w in ll)
    oc_mid = Counter(get_onset(w) for w in mid)
    n_lf=len(lf); n_ll=len(ll); n_mid=max(1,len(mid))
    def enr(o,cs,ns,ca,na): s=cs.get(o,0)/ns if ns else 0; g=ca.get(o,0)/na if na else 0; return s/g if g>0 else 0
    am_r = sum(1 for w in aw if w.endswith('am'))/n
    ll_am = sum(1 for w in ll if w.endswith('am'))/n_ll if n_ll else 0
    lf_am = sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf else 0
    mid_am = sum(1 for w in mid if w.endswith('am'))/n_mid if n_mid else 0
    tb = n-1
    bg = Counter((get_onset(aw[i]),get_onset(aw[i+1])) for i in range(tb))
    def ss(o): b=oc_all.get(o,0)/n; return bg.get((o,o),0)/(tb*b*b) if b>0 else 1.0
    ss_mean=(ss('qok')+ss('ok')+ss('ch'))/3
    adj=sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)
    qok_r=oc_all.get('qok',0)/n; ch_r=oc_all.get('ch',0)/n
    qok_ch=bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0
    mid_bg=Counter(); mid_bg_n=0
    for line in lines:
        nn=len(line)
        if nn<4: continue
        for i in range(1,nn-2): mid_bg[(get_onset(line[i]),get_onset(line[i+1]))]+=1; mid_bg_n+=1
    def E2m(x,y):
        pxy=mid_bg.get((x,y),0)/mid_bg_n if mid_bg_n>0 else 0
        px=oc_mid.get(x,0)/n_mid; py=oc_mid.get(y,0)/n_mid
        return pxy/(px*py) if px*py>0 else 0
    return dict(am_ll=ll_am/am_r if am_r else 0, d_ll=enr('d',oc_ll,n_ll,oc_all,n),
                y_lf=enr('y',oc_lf,n_lf,oc_all,n), ss_mean=ss_mean, adj_rate=adj,
                qok_lf=enr('qok',oc_lf,n_lf,oc_all,n), d_lf=enr('d',oc_lf,n_lf,oc_all,n),
                s_lf=enr('s',oc_lf,n_lf,oc_all,n), ch_ll=enr('ch',oc_ll,n_ll,oc_all,n),
                ok_ll=enr('ok',oc_ll,n_ll,oc_all,n), qok_ll=enr('qok',oc_ll,n_ll,oc_all,n),
                ss_d=ss('d'), ss_y=ss('y'), am_lf_enr=lf_am/am_r if am_r else 0,
                am_mid_enr=mid_am/am_r if am_r else 0,
                edy_rate=sum(1 for w in aw if w.endswith('edy'))/n,
                word_len_mean=sum(len(w) for w in aw)/n, qok_ch=qok_ch, global_am_rate=am_r,
                _ot_ot_mid=E2m('ot','ot'), _sh_qok_mid=E2m('sh','qok'),
                _qok_ch_mid=E2m('qok','ch'), _ch_qok_mid=E2m('ch','qok'))

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

def count_passes(m, ref):
    return sum(1 for k in BATTERY_KEYS if ref.get(k,0)>0 and abs(m.get(k,0)/ref[k]-1)<=PASS_TOL)

def agg(lst, k): return sum(x[k] for x in lst)/len(lst) if lst else 0

# ─── Main ──────────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus...")
b_lines = parse_vms_b_dialect()
vms = compute_vms_targets(b_lines)
print(f"  B-dialect: {len(b_lines)} lines, {vms['n']} words")
print(f"\n  VMS B-dialect MID bigram diagnostics:")
print(f"    ot→ot MID E2:  {vms['_ot_ot_mid']:.3f} (N_mid_bg={vms['n_mid_bigrams']})")
print(f"    sh→qok MID E2: {vms['_sh_qok_mid']:.3f}")
print(f"    qok→ch MID E2: {vms['_qok_ch_mid']:.3f}")
print(f"    ch→qok MID E2: {vms['_ch_qok_mid']:.3f}")
print(f"  Context: sh→qok Δ=1.01 (failed in exp_243); ch→qok Δ=0.16 (succeeded, p=0.12)")
print(f"  ot→ot Δ={vms['_ot_ot_mid']-1.410:.3f} from sim baseline 1.410")

d_global = vms['onset_global'].get('d', 0)
d_ll_target = vms['d_ll']
onset_ll_vms = dict(vms['onset_ll'])
vms_ll_d_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0
ll_onsets = build_ll_onsets(onset_ll_vms, D_BOOST)
onset_lf = dict(vms['onset_lf']); onset_ll = dict(vms['onset_ll'])
suffix_global = dict(vms['suffix_global']); onset_mid = dict(vms['onset_mid'])
suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
target_lines = len(b_lines)
VMS_REF = {k: vms[k] for k in BATTERY_KEYS if k in vms}

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words")

# ─── Baseline ─────────────────────────────────────────────────────────────────

print(f"\n{'='*65}")
print(f"BASELINE N={N_SWEEP} at p_ot_ot=0.00 (exp_249 architecture)")
print(f"{'='*65}")
base_m = []
for trial in range(N_SWEEP):
    rng = random.Random(SEED + trial*100)
    lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, 0.00, rng)
    m = compute_metrics(lines)
    if m: base_m.append(m)
avg_base = {k: agg(base_m, k) for k in base_m[0]} if base_m else {}
passes_base = count_passes(avg_base, VMS_REF)
print(f"  Baseline: {passes_base}/{len(BATTERY_KEYS)} PASS")
print(f"  Baseline ot→ot_mid: {avg_base.get('_ot_ot_mid',0):.3f} (VMS={vms['_ot_ot_mid']:.3f})")
print(f"  Baseline sh→qok_mid: {avg_base.get('_sh_qok_mid',0):.3f}")
print(f"  Baseline qok→ch_mid: {avg_base.get('_qok_ch_mid',0):.3f}")
print(f"  Baseline ch→qok_mid: {avg_base.get('_ch_qok_mid',0):.3f}")

# ─── Sweep ────────────────────────────────────────────────────────────────────

SWEEP = [0.05, 0.10, 0.15, 0.20]
print(f"\n{'='*65}")
print(f"SWEEP p_ot_ot ∈ {SWEEP}, N={N_SWEEP}")
print(f"{'='*65}")
print(f"\n  {'p_ot_ot':>8}  {'Pass/19':>7}  {'ot→ot_m':>9}  {'sh→qok_m':>10}  {'qok→ch_m':>10}  {'ss_mean':>8}")
print(f"  {'---':>8}  {'---':>7}  {'---':>9}  {'---':>10}  {'---':>10}  {'---':>8}")

sweep_results = []
for p_ot_ot in SWEEP:
    all_m = []
    for trial in range(N_SWEEP):
        rng = random.Random(SEED + trial*100 + int(p_ot_ot*1000))
        lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, p_ot_ot, rng)
        m = compute_metrics(lines)
        if m: all_m.append(m)
    avg = {k: agg(all_m, k) for k in all_m[0]} if all_m else {}
    passes = count_passes(avg, VMS_REF)
    print(f"  {p_ot_ot:>8.2f}  {passes:>5}/{len(BATTERY_KEYS)}  "
          f"{avg.get('_ot_ot_mid',0):>9.3f}  {avg.get('_sh_qok_mid',0):>10.3f}  "
          f"{avg.get('_qok_ch_mid',0):>10.3f}  {avg.get('ss_mean',0):>8.3f}")
    sweep_results.append((p_ot_ot, passes, avg))

# ─── Best by passes, then closest ot→ot to VMS ────────────────────────────────

vms_ot_ot = vms['_ot_ot_mid']
best = max(sweep_results, key=lambda x: (x[1], -abs(x[2].get('_ot_ot_mid',0)/vms_ot_ot-1)))
best_p = best[0]
print(f"\n  → Best: p_ot_ot={best_p} ({best[1]}/{len(BATTERY_KEYS)} PASS)")
print(f"    VMS ot→ot_mid={vms_ot_ot:.3f}, Sim={best[2].get('_ot_ot_mid',0):.3f}")

# ─── Full N=30 at best value ──────────────────────────────────────────────────

print(f"\n{'='*65}")
print(f"FULL N={N_FULL} at p_ot_ot={best_p}")
print(f"{'='*65}")

all_m_full = []
for trial in range(N_FULL):
    rng = random.Random(SEED + trial*100 + int(best_p*1000))
    lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, best_p, rng)
    m = compute_metrics(lines)
    if m: all_m_full.append(m)
    if (trial+1)%10==0: print(f"  Trial {trial+1}/{N_FULL} done")

avg_full = {k: agg(all_m_full, k) for k in all_m_full[0]} if all_m_full else {}
passes_full = 0
print(f"\n  {'Metric':<18} {'VMS':>8} {'Sim':>8} {'%VMS':>7} {'PASS':>5}")
print(f"  {'-'*48}")
for k in BATTERY_KEYS:
    v=avg_full.get(k,0); t=VMS_REF.get(k,0)
    pct=100*v/t if t>0 else 0; ok='PASS' if t>0 and abs(v/t-1)<=PASS_TOL else 'FAIL'
    if ok=='PASS': passes_full+=1
    print(f"  {k:<18} {t:>8.4f} {v:>8.4f} {pct:>7.1f}% {ok:>5}{'*' if ok=='FAIL' else ''}")

print(f"\n  TOTAL: {passes_full}/{len(BATTERY_KEYS)} PASS  (p_ot_ot={best_p}, N={N_FULL})")
print(f"\n  MID bigrams:")
print(f"    ot→ot:  Sim={avg_full.get('_ot_ot_mid',0):.3f}, VMS={vms['_ot_ot_mid']:.3f}")
print(f"    sh→qok: Sim={avg_full.get('_sh_qok_mid',0):.3f}, VMS={vms['_sh_qok_mid']:.3f}")
print(f"    qok→ch: Sim={avg_full.get('_qok_ch_mid',0):.3f}, VMS={vms['_qok_ch_mid']:.3f}")
print(f"    ch→qok: Sim={avg_full.get('_ch_qok_mid',0):.3f}, VMS={vms['_ch_qok_mid']:.3f}")

# ─── Summary ──────────────────────────────────────────────────────────────────

print(f"\n{'='*65}")
print(f"SUMMARY")
print(f"{'='*65}")
print(f"  VMS B-dialect ot→ot MID E2: {vms_ot_ot:.3f}")
print(f"  Baseline sim ot→ot_mid: {avg_base.get('_ot_ot_mid',0):.3f}  (N={N_SWEEP})")
print(f"  Best p_ot_ot={best_p}: {avg_full.get('_ot_ot_mid',0):.3f}  (N={N_FULL})")
print(f"  Baseline: {passes_base}/{len(BATTERY_KEYS)} PASS (N={N_SWEEP})")
print(f"  p_ot_ot={best_p}: {passes_full}/{len(BATTERY_KEYS)} PASS (N={N_FULL})")
gap_before = abs(avg_base.get('_ot_ot_mid',0) - vms_ot_ot)
gap_after = abs(avg_full.get('_ot_ot_mid',0) - vms_ot_ot)
print(f"  ot→ot gap: before={gap_before:.3f}, after={gap_after:.3f}")
if passes_full >= 19 and gap_after < gap_before:
    print(f"  H447: CONFIRMED — p_ot_ot={best_p} improves ot→ot without regression")
elif passes_full < 19:
    print(f"  H447: NEGATIVE — p_ot_ot={best_p} causes battery regression")
else:
    print(f"  H447: MIXED — p_ot_ot={best_p} passes battery but gap not improved")
print("\nDone.")
