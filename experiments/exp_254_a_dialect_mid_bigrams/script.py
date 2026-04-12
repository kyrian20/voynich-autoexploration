"""
exp_254: H450 — A-Dialect MID-Only Bigram Tracking

Question: Does the A-dialect architecture (exp_239+p_y_y=0.10) over/under-produce
self-succession bigrams in MID context, similar to B-dialect (exp_246)?

Key questions:
1. A-dialect ot→ot: VMS E_mid=? vs Sim E_mid=? (under-produced like B-dialect?)
2. A-dialect y→y: is it over-produced in MID (p_y_y=0.10 was calibrated to global ss_y)?
3. A-dialect sh→qok: E_mid=1.741 (N=55) from exp_242 — does sim reproduce?
4. A-dialect qok→qok: VMS=1.750, baseline sim=1.727 (from exp_251 — already confirmed correct)
5. Other onset self-successions: o→o (A: VMS 2.801), ok→ok (A: VMS 1.959), qot→qot (A: VMS 3.030)

Design:
- Run exp_239 A-dialect architecture (p_y_y=0.10, all other params fixed) at N=15
- Compute both global bigrams and MID-only bigrams
- Compare to VMS A-dialect corpus

Exp_239 parameters (A-dialect):
  p_blind=0.0505, d_boost=24.30%, r_lf=0.266, r_mid=0.87, p_stutter=0.002
  mu_len=5.64, cp=0.55, mp=0.90, p_qokch=0.12, p_y_y=0.10, p_chqok=0.00, p_lf=1.0
"""

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIM = 15; WINDOW = 20; SEED = 254000

# Fixed A-dialect parameters
P_BLIND = 0.0505; D_BOOST = 0.2430; R_LF = 0.266; R_MID = 0.87
P_STUTTER = 0.002; MU_LEN = 5.64; SIGMA_LEN = 2.5
CP = 0.55; MP = 0.90; P_QOKCH = 0.12; P_LF = 1.0; P_Y_Y = 0.10; P_CHQOK = 0.00

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

def parse_vms_a_dialect():
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

def analyze_bigrams(lines, label=''):
    all_words = [w for l in lines for w in l]
    mid_words = [w for l in lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words); n_mid = max(1, len(mid_words))
    oc_all = Counter(get_onset(w) for w in all_words)
    oc_mid = Counter(get_onset(w) for w in mid_words)

    # Global bigrams
    tb = n - 1
    bg_global = Counter((get_onset(all_words[i]), get_onset(all_words[i+1])) for i in range(tb))

    # MID-only bigrams
    mid_bg = Counter(); mid_bg_n = 0
    for line in lines:
        nn = len(line)
        if nn < 4: continue
        for i in range(1, nn-2):
            mid_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1; mid_bg_n += 1

    def E2_global(x, y):
        px = oc_all.get(x, 0) / n; py = oc_all.get(y, 0) / n
        pxy = bg_global.get((x, y), 0) / tb if tb > 0 else 0
        return pxy / (px * py) if px * py > 0 else float('nan')

    def E2_mid(x, y):
        px = oc_mid.get(x, 0) / n_mid; py = oc_mid.get(y, 0) / n_mid
        pxy = mid_bg.get((x, y), 0) / mid_bg_n if mid_bg_n > 0 else 0
        return pxy / (px * py) if px * py > 0 else float('nan')

    return {
        'label': label, 'n': n, 'n_mid': n_mid, 'mid_bg_n': mid_bg_n,
        'oc_all': oc_all, 'oc_mid': oc_mid,
        'E2_global': E2_global, 'E2_mid': E2_mid,
        'mid_bg': mid_bg,
    }

KEY_PAIRS = [
    ('qok', 'qok'), ('y', 'y'), ('ot', 'ot'), ('ok', 'ok'),
    ('d', 'd'), ('o', 'o'), ('qot', 'qot'), ('ol', 'ol'),
    ('ch', 'ch'), ('sh', 'sh'), ('sh', 'qok'), ('qok', 'ch'),
    ('ch', 'qok'), ('y', 'qok'), ('d', 'qok'),
]

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

def draw_buf(buf, prev_onset, rng):
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
    return rng.choice(bl)

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

# ─── Main ──────────────────────────────────────────────────────────────────────

print("Parsing VMS A-dialect corpus...")
a_lines = parse_vms_a_dialect()
print(f"  A-dialect: {len(a_lines)} lines")

# VMS A-dialect bigram analysis
vms_analysis = analyze_bigrams(a_lines, 'VMS_A')

# Compute VMS suffix distribution for sim setup
all_words = [w for l in a_lines for w in l]
n = len(all_words)
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']
suf_ctr = Counter()
for w in all_words:
    matched = False
    for suf in SUFFIX_PATTERNS:
        if w.endswith(suf): suf_ctr[suf] += 1; matched = True; break
    if not matched: suf_ctr['other'] += 1
suffix_global = {suf: cnt/n for suf, cnt in suf_ctr.items()}
onset_mid = {o: cnt/max(1, sum(1 for l in a_lines for w in l[1:-1] if len(l)>2))
             for o, cnt in Counter(get_onset(w) for l in a_lines for w in l[1:-1] if len(l)>2).items()}
onset_lf = {o: cnt/max(1, len(a_lines))
            for o, cnt in Counter(get_onset(l[0]) for l in a_lines if l).items()}
onset_ll = {o: cnt/max(1, len([l for l in a_lines if len(l)>1]))
            for o, cnt in Counter(get_onset(l[-1]) for l in a_lines if len(l)>1).items()}
ll_onsets = build_ll_onsets(onset_ll, D_BOOST)
suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
target_lines = len(a_lines)

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)

# Run N=15 simulations
print(f"\nRunning {N_SIM} simulations...")
sim_all_lines = []
for trial in range(N_SIM):
    rng = random.Random(SEED + trial*100)
    lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, rng)
    sim_all_lines.extend(lines)
    if (trial+1) % 5 == 0: print(f"  Trial {trial+1}/{N_SIM} done")

sim_analysis = analyze_bigrams(sim_all_lines, 'Sim_A')

# ─── Print comparison ──────────────────────────────────────────────────────────

print(f"\n{'='*75}")
print(f"A-DIALECT BIGRAM COMPARISON: VMS vs Sim (N={N_SIM})")
print(f"{'='*75}")
print(f"\n  {'Pair':<12}  {'VMS_global':>12}  {'Sim_global':>12}  {'VMS_mid':>10}  {'Sim_mid':>10}  {'N_vms_m':>8}  {'N_sim_m':>8}")
print(f"  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*10}  {'-'*10}  {'-'*8}  {'-'*8}")

for (x, y) in KEY_PAIRS:
    vg = vms_analysis['E2_global'](x, y)
    sg_ = sim_analysis['E2_global'](x, y)
    vm_ = vms_analysis['E2_mid'](x, y)
    sm_ = sim_analysis['E2_mid'](x, y)
    nvm = vms_analysis['mid_bg'].get((x, y), 0)
    nsm = sim_analysis['mid_bg'].get((x, y), 0)

    def fmt(v): return f"{v:8.3f}" if v == v else "     nan"
    status = ''
    if vm_ == vm_ and sm_ == sm_:
        delta = sm_ - vm_
        if abs(delta) > 0.3: status = f" ({'SIM>VMS' if delta>0 else 'SIM<VMS'}:{delta:+.2f})"
    print(f"  {x}→{y:<9}  {fmt(vg)}    {fmt(sg_)}    {fmt(vm_)}  {fmt(sm_)}  {nvm:>8}  {nsm:>8}{status}")

# ─── Onset rates comparison ────────────────────────────────────────────────────

print(f"\n{'='*75}")
print(f"ONSET RATES COMPARISON (global and MID)")
print(f"{'='*75}")
print(f"\n  {'Onset':<8}  {'VMS_global':>10}  {'VMS_mid':>10}  {'Sim_global':>10}  {'Sim_mid':>10}")
for onset in ['qok','ch','sh','ot','y','d','ok','o','qot','ol']:
    vg_ = vms_analysis['oc_all'].get(onset,0) / vms_analysis['n']
    vm_ = vms_analysis['oc_mid'].get(onset,0) / vms_analysis['n_mid']
    sg_ = sim_analysis['oc_all'].get(onset,0) / sim_analysis['n']
    sm_ = sim_analysis['oc_mid'].get(onset,0) / sim_analysis['n_mid']
    print(f"  {onset:<8}  {vg_:>10.4f}  {vm_:>10.4f}  {sg_:>10.4f}  {sm_:>10.4f}")

# ─── Key findings summary ──────────────────────────────────────────────────────

print(f"\n{'='*75}")
print(f"KEY FINDINGS SUMMARY")
print(f"{'='*75}")
pairs_of_interest = [
    ('qok','qok','A-dialect self-succession (B=1.169, confirmed correct in exp_251)'),
    ('y','y','y→y (p_y_y=0.10 calibrated to global ss_y)'),
    ('ot','ot','ot→ot (B-dialect gap: VMS=1.887, sim=1.41 — is A-dialect similar?)'),
    ('ok','ok','ok→ok (B: VMS=1.322)'),
    ('d','d','d→d (B: VMS=1.540)'),
    ('o','o','o→o (A: VMS=2.801 from exp_242 — high enrichment)'),
    ('sh','qok','sh→qok (A: E_mid=1.741 from exp_242, N=55)'),
    ('qok','ch','qok→ch (A: E_mid=0.985 from exp_250 — near random)'),
]
for (x, y, note) in pairs_of_interest:
    vm_ = vms_analysis['E2_mid'](x, y)
    sm_ = sim_analysis['E2_mid'](x, y)
    nvm = vms_analysis['mid_bg'].get((x, y), 0)
    if vm_ == vm_ and sm_ == sm_:
        delta = sm_ - vm_
        direction = 'SIM>VMS' if delta > 0.1 else ('SIM<VMS' if delta < -0.1 else 'MATCH')
        print(f"  {x}→{y}: VMS={vm_:.3f}(N={nvm}), Sim={sm_:.3f}, Δ={delta:+.3f} [{direction}]")
        print(f"     Note: {note}")
    else:
        print(f"  {x}→{y}: VMS=nan or Sim=nan (insufficient data)")

print(f"\nDone.")
