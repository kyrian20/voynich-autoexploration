"""
exp_222: H423 — VMS Positional Suffix Distributions (LF/MID/LL)

Motivation:
  exp_221 (Mode B, cp=0.55, mp=0.90) achieves 11/18 pass — program best.
  Three remaining failures are suffix-distribution artifacts:
    am_lf_enr  = 0.380 (310.3% VMS 0.122) — LF uses global suffix → LF am ≈ global am
    am_mid_enr = 0.277 (142.2% VMS 0.195) — MID uses global suffix → MID am inflated by copy
    edy_rate   = 0.140 (72.4% VMS 0.194)  — VMS B global suffix edy rate should calibrate...
                                              but Timm mod erodes edy on copy buffer words

  Fix analogous to H421 MID onset fix: use VMS positional suffix distributions.
    - LF words: onset from VMS LF onset dist (p_lf=1.0) + suffix from VMS LF suffix dist
    - MID fresh words: onset from VMS MID onset dist + suffix from VMS MID suffix dist
    - MID copy buffer words (non-modified): suffix already from prior generation
    - MID Timm-modified words: modification in suffix region only (unchanged)
    - LL non-blind fraction: suffix from VMS LL suffix dist (instead of global)
    - LL blind fraction (p_blind=0.30): still forced suffix = 'am' (architecture requirement)

  Note on am_lf_enr mechanism:
    Currently global am rate is elevated (~5.5%) because p_blind=0.30 of LL words are always -am.
    LF am rate = suffix_global['am'] ≈ VMS global am rate ≈ 2%.
    am_lf_enr = 2%/5.5% ≈ 0.36 (sim) vs VMS 0.122.
    With positional suffix: LF am rate = VMS LF am rate ≈ 0.25% (very low).
    Global am rate shifts (LF contributes less am) but LL still dominates global am elevation.
    Expected: am_lf_enr = VMS_LF_am / (new_global_am) → closer to VMS 0.122.

  Hold all other parameters fixed: cp=0.55, mp=0.90, p_blind=0.30, p_lf=1.0.

Architecture: Mode B + onset-preserving Timm + VMS POSITIONAL SUFFIX DISTRIBUTIONS
  - onset_weights (MID)  = VMS MID onset distribution
  - suffix_lf            = VMS LF suffix distribution
  - suffix_mid           = VMS MID suffix distribution
  - suffix_ll            = VMS LL suffix distribution (for non-blind LL fraction)
  - suffix_all           = VMS global suffix distribution (used only for diagnostics)
  - Onset-preserving Timm modification (suffix region only)
  - p_blind=0.30, d_boost=14.79%, p_lf=1.0
  - cp=0.55, mp=0.90

N=30 simulations.
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIMS      = 30
TARGET_LINES = 2447
WINDOW       = 20
SEED         = 222000
P_BLIND = 0.30
P_LF    = 1.0
CP      = 0.55
MP      = 0.90

EVA_CHARS = list('acdehiklmnoqrsty')

SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']

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

def compute_suffix_dist(words):
    """Compute suffix distribution for a list of words."""
    n = len(words)
    if n == 0: return {suf: 1/len(SUFFIX_PATTERNS+['other']) for suf in SUFFIX_PATTERNS+['other']}
    ctr = Counter()
    for w in words:
        matched = False
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf):
                ctr[suf] += 1; matched = True; break
        if not matched: ctr['other'] += 1
    return {suf: ctr.get(suf, 0)/n for suf in SUFFIX_PATTERNS+['other']}

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

    suffix_global = compute_suffix_dist(all_words)
    suffix_lf     = compute_suffix_dist(lf_words)
    suffix_mid    = compute_suffix_dist(mid_words)
    suffix_ll     = compute_suffix_dist(ll_words)

    am_r  = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words)
    d_r   = oc_all.get('d', 0) / n
    ll_d  = oc_ll.get('d', 0) / len(ll_words)

    print(f"\n  VMS B positional suffix distributions (am rate at each position):")
    print(f"    Global am = {suffix_global.get('am', 0)*100:.2f}%")
    print(f"    LF am     = {suffix_lf.get('am', 0)*100:.2f}%")
    print(f"    MID am    = {suffix_mid.get('am', 0)*100:.2f}%")
    print(f"    LL am     = {suffix_ll.get('am', 0)*100:.2f}%")
    print(f"  VMS B positional suffix distributions (edy rate at each position):")
    print(f"    Global edy = {(suffix_global.get('edy', 0)+suffix_global.get('eedy', 0))*100:.2f}%")
    print(f"    LF edy     = {(suffix_lf.get('edy', 0)+suffix_lf.get('eedy', 0))*100:.2f}%")
    print(f"    MID edy    = {(suffix_mid.get('edy', 0)+suffix_mid.get('eedy', 0))*100:.2f}%")
    print(f"    LL edy     = {(suffix_ll.get('edy', 0)+suffix_ll.get('eedy', 0))*100:.2f}%")

    return {
        'onset_global': onset_global,
        'onset_lf': onset_lf,
        'onset_ll': onset_ll,
        'onset_mid': onset_mid,
        'suffix_global': suffix_global,
        'suffix_lf': suffix_lf,
        'suffix_mid': suffix_mid,
        'suffix_ll': suffix_ll,
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

def cipher_ll_blind(onset_weights, suffix_weights_ll, ll_onsets, p_blind, rng):
    """LL generation: p_blind fraction → ll_onsets + forced -am; rest → onset_weights + VMS LL suffix."""
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return make_word_sim(onset, 'am', rng)
    return random_eva_word(onset_weights, suffix_weights_ll, rng)

def cipher_lf_vms(onset_lf_vms, suffix_weights_lf, p_lf, rng):
    """LF generation: always VMS LF onset dist + VMS LF suffix dist (p_lf=1.0)."""
    onset  = rng.choices(list(onset_lf_vms.keys()),  weights=list(onset_lf_vms.values()))[0]
    suffix = rng.choices(list(suffix_weights_lf.keys()), weights=list(suffix_weights_lf.values()))[0]
    return make_word_sim(onset, suffix, rng)

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

def run_sim(latin_words, onset_weights_mid, suffix_weights_mid, suffix_weights_ll,
            onset_lf_vms, suffix_weights_lf, ll_onsets, cp, mp, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                # LF: VMS LF onset + VMS LF suffix
                ew = cipher_lf_vms(onset_lf_vms, suffix_weights_lf, P_LF, rng)
            elif i == len(chunk)-1:
                # LL: p_blind fraction → forced -am; rest → VMS LL suffix
                ew = cipher_ll_blind(onset_weights_mid, suffix_weights_ll, ll_onsets, P_BLIND, rng)
            else:
                # MID: copy buffer or fresh random (VMS MID onset + VMS MID suffix)
                if buf and rng.random() < cp:
                    ew = timm_modify_onset_preserving(rng.choice(list(buf)), rng) if rng.random() < mp else rng.choice(list(buf))
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_weights_mid, rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def compute_metrics(lines):
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

# Positional onset and suffix distributions
onset_weights_mid = dict(vms['onset_mid'])    # VMS MID onset
suffix_weights_lf  = dict(vms['suffix_lf'])   # VMS LF suffix (NEW)
suffix_weights_mid = dict(vms['suffix_mid'])   # VMS MID suffix (NEW)
suffix_weights_ll  = dict(vms['suffix_ll'])    # VMS LL suffix (NEW)
suffix_weights_all = dict(vms['suffix_global'])  # global (for reference/exp_221 comparison)

print(f"\n  p_blind={P_BLIND}, d_boost={d_boost*100:.2f}%, p_lf={P_LF}")
print(f"  cp={CP}, mp={MP}")
print(f"  Architecture: VMS positional onset (MID) + VMS positional suffix (LF/MID/LL)")
print(f"  vs exp_221: adds positional suffix distributions for all 3 positions")
print()

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

# VMS reference values (same as exp_221)
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
    ('ss_d', 'uncalibrated'), ('ss_y', 'uncalibrated'), ('am_lf_enr', 'VMS-DIRECT suffix'),
    ('am_mid_enr', 'VMS-DIRECT suffix'), ('edy_rate', 'VMS-DIRECT suffix'),
    ('word_len_mean', 'uncalibrated'), ('qok_ch', 'uncalibrated'),
]

# exp_221 reference (for comparison)
EXP221_REF = {
    'am_ll': 6.258, 'd_ll': 1.222, 'y_lf': 3.440, 'ss_mean': 1.341, 'adj_rate': 0.003,
    'qok_lf': 0.756, 'd_lf': 2.253, 's_lf': 5.138, 'ch_ll': 1.066, 'ok_ll': 1.043,
    'qok_ll': 0.750, 'ss_d': 1.452, 'ss_y': 1.673, 'am_lf_enr': 0.380, 'am_mid_enr': 0.277,
    'edy_rate': 0.140, 'word_len_mean': 6.592, 'qok_ch': 0.987,
}

print("=" * 100)
print(f"exp_222: Mode B + VMS POSITIONAL SUFFIX (LF/MID/LL), cp={CP}, mp={MP}, N={N_SIMS}")
print(f"VMS am_ll={VMS_REF['am_ll']:.3f}, am_lf_enr={VMS_REF['am_lf_enr']:.3f}, am_mid_enr=0.195")
print("=" * 100)

all_metrics = []
for i in range(N_SIMS):
    rng = random.Random(SEED + i)
    lines = run_sim(latin, onset_weights_mid, suffix_weights_mid, suffix_weights_ll,
                    onset_lf_vms, suffix_weights_lf, ll_onsets, CP, MP, rng)
    m = compute_metrics(lines)
    if m: all_metrics.append(m)

print(f"  Completed {len(all_metrics)} simulations.")
print()

def agg(key):
    vals = sorted(x[key] for x in all_metrics)
    mean = sum(vals)/len(vals)
    ci_lo = vals[max(0, int(.05*len(vals)))]
    ci_hi = vals[min(len(vals)-1, int(.95*len(vals)))]
    return mean, ci_lo, ci_hi

PASS_TOL = 0.20
pass_count = 0; total = 0

print(f"  {'Metric':<16} {'VMS':>8} {'E222':>8} {'%VMS':>7} {'Status':<6}  vs E221  [Category]")
print(f"  {'-'*90}")
for key, cat in METRIC_LABELS:
    vms_val = VMS_REF.get(key)
    if vms_val is None: continue
    sim_mean, ci_lo, ci_hi = agg(key)
    pct = sim_mean/vms_val*100 if abs(vms_val)>1e-6 else float('inf')
    pass_f = abs(sim_mean-vms_val)/abs(vms_val) <= PASS_TOL if abs(vms_val)>1e-6 else abs(sim_mean)<0.002
    status = 'PASS' if pass_f else 'FAIL'
    e221_val = EXP221_REF.get(key)
    e221_note = f"was {e221_val:.3f}" if e221_val else ""
    print(f"  {key:<16} {vms_val:>8.3f} {sim_mean:>8.3f} {pct:>6.1f}%  [{status}]  {e221_note}  [{cat}]")
    total += 1
    if pass_f: pass_count += 1

print()
print(f"  Pass count: {pass_count}/{total} (exp_221 Mode B: 11/18)")
print(f"  Config: p_blind={P_BLIND}, d_boost={d_boost*100:.2f}%, p_lf={P_LF}")
print(f"          onset_weights=VMS MID, suffix_weights=VMS POSITIONAL, onset-preserving mod")
print(f"          cp={CP}, mp={MP}")
print()
print("=" * 100)
print("ARCHITECTURE EVOLUTION")
print("=" * 100)
print(f"  exp_218 (VMS calibrated dists, all-char Timm):                        4/17 pass")
print(f"  exp_219 (onset-preserving modification):                               8/18 pass")
print(f"  exp_220 (Mode B, cp=0.6, VMS MID onset for MID):                      9/18 pass")
print(f"  exp_221 (Mode B, cp=0.55, fine-tuned):                               11/18 pass")
print(f"  exp_222 (Mode B + VMS positional suffix LF/MID/LL, cp=0.55):         {pass_count}/{total} pass")
