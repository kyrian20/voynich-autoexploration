"""
exp_221: H422 — Fine-Sweep cp=0.40-0.55 in Mode B

Motivation:
  exp_220 (Mode B: onset-preserving + VMS MID onset for MID, p_blind=0.30) achieves
  9/18 pass at cp=0.60, mp=0.90 but ss_mean=1.403 (120.6% of VMS corpus 1.164 = FAIL).

  The sweep shows cp=0.40-0.50 should give ss_mean≈1.18-1.29 (within ±20% of 1.164)
  while Mode B maintains y_lf≈3.35-3.55 (PASS) across all tested combos.

  Question: At cp=0.40-0.55, which combination achieves:
  (a) ss_mean within ±20% of VMS corpus 1.164 (i.e., ss_mean ≤ 1.397)
  (b) am_ll within ±20% of VMS 6.550 (i.e., am_ll ≥ 5.24)
  (c) adj_rate ≤ 0.009
  (d) y_lf within ±20% of VMS 3.324 (i.e., y_lf ≥ 2.66)

  Fine sweep: cp ∈ {0.40, 0.45, 0.50, 0.55} × mp ∈ {0.60, 0.70, 0.80, 0.90} = 16 combos.
  N=15 sims per combo (preliminary). Full N=30 at best viable.

Architecture: identical to exp_220 Mode B
  - onset_weights = VMS MID onset distribution (H421 fix)
  - Onset-preserving Timm modification
  - p_blind=0.30, p_lf=1.0 (VMS LF dist)
  - All VMS B-calibrated distributions
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIMS_SWEEP = 15
N_SIMS_FULL  = 30
TARGET_LINES = 2447
WINDOW       = 20
SEED         = 221000
P_BLIND = 0.30
P_LF    = 1.0

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
            dialect = folio_dialect.get(fb, 'unknown')
            if dialect != 'B': continue
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
    n = len(all_words)
    n_mid = len(mid_words)

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
        'onset_global': onset_global,
        'onset_lf': onset_lf,
        'onset_ll': onset_ll,
        'onset_mid': onset_mid,
        'suffix_global': suffix_global,
        'am_r': am_r, 'am_ll_target': ll_am/am_r,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words),
    }

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    remaining_weight = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o not in ('d', 'qok')}
    base_total = sum(base.values())
    if base_total > 0:
        normalized = {o: v/base_total * remaining_weight for o, v in base.items()}
    else:
        normalized = {}
    normalized['d'] = d_boost_weight
    return normalized

def make_word_sim(onset, suffix, rng):
    connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
    return onset + connector + suffix

def random_eva_word(onset_weights, suffix_weights, rng):
    onset  = rng.choices(list(onset_weights.keys()),  weights=list(onset_weights.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_ll_blind(onset_weights, suffix_weights, ll_onsets, p_blind, rng):
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return make_word_sim(onset, 'am', rng)
    return random_eva_word(onset_weights, suffix_weights, rng)

def cipher_lf_vms(onset_weights, suffix_weights, onset_lf_vms, p_lf, rng):
    if rng.random() < p_lf:
        onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
        suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_weights, suffix_weights, rng)

def timm_modify_onset_preserving(word, rng):
    if not word: return word
    onset_len = get_onset_len(word)
    suffix_start = onset_len
    if suffix_start >= len(word): return word
    op = rng.choice(['replace', 'insert', 'delete'])
    if op == 'replace':
        pos = rng.randint(suffix_start, len(word) - 1)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(suffix_start, len(word))
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:
        if len(word) <= suffix_start + 1:
            if suffix_start < len(word):
                return word[:suffix_start] + rng.choice(EVA_CHARS) + word[suffix_start+1:]
            return word
        pos = rng.randint(suffix_start, len(word) - 1)
        return word[:pos] + word[pos+1:]

def run_sim(latin_words, onset_weights, suffix_weights, ll_onsets, onset_lf_vms, cp, mp, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf_vms(onset_weights, suffix_weights, onset_lf_vms, P_LF, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_blind(onset_weights, suffix_weights, ll_onsets, P_BLIND, rng)
            else:
                if buf and rng.random() < cp:
                    ew = timm_modify_onset_preserving(rng.choice(list(buf)), rng) if rng.random() < mp else rng.choice(list(buf))
                else:
                    ew = random_eva_word(onset_weights, suffix_weights, rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def compute_metrics(lines, vms):
    aw  = [w for l in lines for w in l]
    n   = len(aw)
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

    qok_lf = enr('qok', oc_lf, n_lf, oc_all, n)
    d_lf   = enr('d',   oc_lf, n_lf, oc_all, n)
    s_lf   = enr('s',   oc_lf, n_lf, oc_all, n)
    ch_ll  = enr('ch',  oc_ll, n_ll, oc_all, n)
    ok_ll  = enr('ok',  oc_ll, n_ll, oc_all, n)
    qok_ll = enr('qok', oc_ll, n_ll, oc_all, n)
    ss_d   = ss('d');  ss_y = ss('y')
    am_lf_enr  = (sum(1 for w in lf if w.endswith('am'))/n_lf) / am_r if am_r else 0
    am_mid_enr = (sum(1 for w in mid if w.endswith('am'))/n_mid / am_r) if (n_mid and am_r) else 0
    edy_rate   = sum(1 for w in aw if w.endswith('edy'))/n
    word_len   = sum(len(w) for w in aw)/n
    qok_r  = oc_all.get('qok', 0)/n
    ch_r   = oc_all.get('ch', 0)/n
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch)

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

# ─── Main ────────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus...")
vms_b_lines = parse_vms_corpus()
vms = compute_vms_distributions(vms_b_lines)

print(f"  VMS B: {len(vms_b_lines)} lines, {vms['n']} words")

d_global    = vms['onset_global'].get('d', 0)
d_ll_target = vms['d_ll_target']
d_boost     = d_global * (d_ll_target - (1-P_BLIND)) / P_BLIND
ll_onsets   = build_ll_onsets(vms['onset_ll'], d_boost)
onset_lf_vms = dict(vms['onset_lf'])
suffix_weights = dict(vms['suffix_global'])

# Mode B: VMS MID onset for MID
onset_weights_mid = dict(vms['onset_mid'])

print(f"  p_blind={P_BLIND}, d_boost={d_boost*100:.2f}%, p_lf={P_LF}")
print(f"  onset_weights = VMS MID onset distribution")
print()

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

VMS_AM  = vms['am_ll_target']   # 6.550
VMS_SS  = 1.164                  # corpus ss_mean
VMS_ADJ = 0.009
VMS_YLF = vms['onset_lf'].get('y',0) / vms['onset_global'].get('y',0.001)  # 3.324

# Fine sweep
CP_VALUES = [0.40, 0.45, 0.50, 0.55]
MP_VALUES = [0.60, 0.70, 0.80, 0.90]

print("=" * 95)
print(f"FINE SWEEP: Mode B (VMS MID onset for MID, onset-preserving), p_blind={P_BLIND}")
print(f"VMS targets: am_ll={VMS_AM:.3f}, ss_mean={VMS_SS:.3f} (corpus), adj≤{VMS_ADJ}, y_lf={VMS_YLF:.3f}")
print("=" * 95)
print(f"{'cp':>4} {'mp':>4}  {'am_ll':>8} {'d_ll':>7} {'y_lf':>7} {'ss_mean':>8} {'adj':>7}  {'all4?'}")
print("-" * 95)

viable_all4 = []
viable_ss_adj = []
for cp in CP_VALUES:
    for mp in MP_VALUES:
        sims = []
        for i in range(N_SIMS_SWEEP):
            rng = random.Random(SEED + i + int(cp*1000) + int(mp*100))
            lines = run_sim(latin, onset_weights_mid, suffix_weights, ll_onsets, onset_lf_vms, cp, mp, rng)
            m = compute_metrics(lines, vms)
            if m: sims.append(m)
        if not sims: continue
        means = {k: sum(x[k] for x in sims)/len(sims) for k in sims[0]}
        ss = means['ss_mean']; adj = means['adj_rate']
        am = means['am_ll']; ylf = means['y_lf']
        ss_ok   = abs(ss-VMS_SS)/VMS_SS <= 0.20
        adj_ok  = adj <= VMS_ADJ
        am_ok   = abs(am-VMS_AM)/VMS_AM <= 0.20
        ylf_ok  = abs(ylf-VMS_YLF)/VMS_YLF <= 0.20
        all4    = ss_ok and adj_ok and am_ok and ylf_ok
        flag = '  *** ALL4 ***' if all4 else ('  ss+adj' if ss_ok and adj_ok else '')
        print(f"  {cp:.2f} {mp:.2f}  {am:>8.3f} {means['d_ll']:>7.3f} {ylf:>7.3f} {ss:>8.3f} {adj:>7.4f}  {flag}")
        if all4: viable_all4.append({'cp': cp, 'mp': mp, 'means': means})
        if ss_ok and adj_ok: viable_ss_adj.append({'cp': cp, 'mp': mp, 'means': means})

print()
print(f"Combinations with all 4 criteria (ss ±20%, adj≤{VMS_ADJ}, am ±20%, y_lf ±20%): {len(viable_all4)}")
print(f"Combinations with ss+adj only: {len(viable_ss_adj)}")
print()

# Best combo: maximize am_ll among all-4-viable, or closest-to-VMS-am among ss_adj_viable
best = None
if viable_all4:
    best = min(viable_all4, key=lambda x: abs(x['means']['am_ll'] - VMS_AM))
    print(f"Best all-4-viable: cp={best['cp']}, mp={best['mp']}")
elif viable_ss_adj:
    best = min(viable_ss_adj, key=lambda x: abs(x['means']['am_ll'] - VMS_AM))
    print(f"Best ss+adj viable (am may be borderline): cp={best['cp']}, mp={best['mp']}")
else:
    # Use lowest ss in sweep
    all_results = [(cp, mp) for cp in CP_VALUES for mp in MP_VALUES]
    print("No fully viable combo found. Selecting lowest-ss combination for full run.")
    best = {'cp': 0.40, 'mp': 0.90}

# Full run at best combination
best_cp = best['cp']; best_mp = best['mp']
print(f"\n{'='*95}")
print(f"FULL RUN (Mode B, cp={best_cp}, mp={best_mp}): N={N_SIMS_FULL}")
print(f"{'='*95}")

all_metrics = []
for i in range(N_SIMS_FULL):
    rng = random.Random(SEED + 5000 + i)
    lines = run_sim(latin, onset_weights_mid, suffix_weights, ll_onsets, onset_lf_vms, best_cp, best_mp, rng)
    m = compute_metrics(lines, vms)
    if m: all_metrics.append(m)

print(f"  Completed {len(all_metrics)} simulations.")
print()

def agg(key):
    vals = sorted(x[key] for x in all_metrics)
    mean = sum(vals)/len(vals)
    ci_lo = vals[max(0, int(.05*len(vals)))]
    ci_hi = vals[min(len(vals)-1, int(.95*len(vals)))]
    return mean, ci_lo, ci_hi

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
    'am_lf_enr':   (sum(1 for w in [l[0] for l in vms_b_lines if l] if w.endswith('am'))
                    / len([l[0] for l in vms_b_lines if l])) / vms['am_r'],
    'am_mid_enr':  0.195,
    'edy_rate':    sum(vms['suffix_global'].get(s,0) for s in ['edy','eedy']),
    'word_len_mean': 5.400,
    'qok_ch':      1.267,
}

METRIC_LABELS = [
    ('am_ll', 'CALIBRATED'), ('d_ll', 'CALIBRATED'), ('y_lf', 'VMS-DIRECT'),
    ('ss_mean', 'CALIBRATED (cp/mp)'), ('adj_rate', 'CALIBRATED (cp/mp)'),
    ('qok_lf', 'VMS-DIRECT'), ('d_lf', 'VMS-DIRECT'), ('s_lf', 'VMS-DIRECT'),
    ('ch_ll', 'VMS-DIRECT'), ('ok_ll', 'VMS-DIRECT'), ('qok_ll', 'partial'),
    ('ss_d', 'uncalibrated'), ('ss_y', 'uncalibrated'), ('am_lf_enr', 'uncalibrated'),
    ('am_mid_enr', 'uncalibrated'), ('edy_rate', 'VMS-DIRECT suffix'),
    ('word_len_mean', 'uncalibrated'), ('qok_ch', 'uncalibrated'),
]

# Compare to exp_220 Mode B cp=0.6 result
EXP220_REF = {
    'am_ll': 6.292, 'd_ll': 1.242, 'y_lf': 3.453, 'ss_mean': 1.403, 'adj_rate': 0.003,
    'qok_lf': 0.753, 'd_lf': 2.281, 's_lf': 5.030, 'ch_ll': 1.061, 'ok_ll': 1.054,
    'qok_ll': 0.742, 'ss_d': 1.568, 'ss_y': 1.748, 'am_lf_enr': 0.418, 'am_mid_enr': 0.264,
    'edy_rate': 0.132, 'word_len_mean': 6.593, 'qok_ch': 0.966,
}

PASS_TOL = 0.20
pass_count = 0; total = 0

print(f"  {'Metric':<16} {'VMS':>8} {'E221':>8} {'%VMS':>7} {'Status':<6}  vs E220(cp=0.6)")
print(f"  {'-'*80}")
for key, cat in METRIC_LABELS:
    vms_val = VMS_REF.get(key)
    if vms_val is None: continue
    sim_mean, ci_lo, ci_hi = agg(key)
    pct = sim_mean/vms_val*100 if abs(vms_val)>1e-6 else float('inf')
    pass_f = abs(sim_mean-vms_val)/abs(vms_val) <= PASS_TOL if abs(vms_val)>1e-6 else abs(sim_mean)<0.002
    status = 'PASS' if pass_f else 'FAIL'
    e220_val = EXP220_REF.get(key)
    e220_note = f"was {e220_val:.3f}" if e220_val else ""
    print(f"  {key:<16} {vms_val:>8.3f} {sim_mean:>8.3f} {pct:>6.1f}%  [{status}]  {e220_note}  [{cat}]")
    total += 1
    if pass_f: pass_count += 1

print()
print(f"  Pass count: {pass_count}/{total} (exp_220 Mode B: 9/18)")
print(f"  Config: p_blind={P_BLIND}, d_boost={d_boost*100:.2f}%, p_lf={P_LF}")
print(f"          onset_weights=VMS MID, onset-preserving mod, cp={best_cp}, mp={best_mp}")

# Also print summary vs all prior experiments
print()
print("=" * 95)
print("COMPARISON ACROSS ARCHITECTURE EVOLUTION")
print("=" * 95)
print(f"  exp_218 (VMS calibrated dists, all-char Timm):            4/17 pass")
print(f"  exp_219 (onset-preserving, VMS global onset for MID):     8/18 pass")
print(f"  exp_220 (Mode B, cp=0.6, VMS MID onset for MID):         9/18 pass")
print(f"  exp_221 (Mode B, cp={best_cp}, VMS MID onset for MID):   {pass_count}/{total} pass")
