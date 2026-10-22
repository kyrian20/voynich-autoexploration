"""
exp_218: H412+H413 — VMS-Calibrated Onset/Suffix Distributions

Motivation:
  exp_217 identified three systematic failure modes in exp_211's architecture:
  A) LF y-only override: misses d_lf, s_lf, p_lf enrichments
  B) LL_ONSETS architecture: enriches ch/ok/qok at LL; VMS has these near-neutral
  C) ONSET_WEIGHTS: ch=6.4% in simulation vs VMS=15.48%

  All three failures stem from using approximate/incorrect distributions.
  The hypothesis: if we calibrate ALL distributions directly from VMS B corpus,
  how many metrics does the architecture reproduce?

Fixes applied vs exp_211:
  1. ONSET_WEIGHTS: replaced with VMS B global onset distribution (ch=15.48% etc.)
  2. SUFFIX_WEIGHTS: replaced with VMS B suffix distribution
  3. LL_ONSETS: replaced with VMS B LL onset distribution, d boosted to calibrate
     d_ll, qok=0 to allow qok_ll depletion
  4. LF override: replaced y-only with multi-onset VMS B LF distribution
     (d, y, s, p, t enriched at LF; depleted onsets excluded)
  5. p_blind: re-swept to calibrate am_ll

CRITICAL: This is maximally target-aware. Every distribution is derived from VMS
corpus data. The only free sweep parameter is p_blind (for am_ll calibration).
The result demonstrates achievability, not independent prediction.

Architecture:
  - LF: p_lf fraction → VMS B LF onset distribution; (1-p_lf) → global onset
  - LL: p_blind fraction → LL_ONSETS (VMS LL distribution, d adjusted) + -am suffix;
         (1-p_blind) → global onset + random suffix
  - MID: Timm copy buffer as before (cp=0.76, mp=0.9)

Sweep: p_blind ∈ {0.25, 0.30, 0.33, 0.36, 0.40} to find am_ll target
Fixed: p_lf=1.0 (all LF words use VMS LF distribution), cp=0.76, mp=0.9
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIMS       = 30
TARGET_LINES = 2447
WINDOW       = 20
CP, MP       = 0.76, 0.9
SEED         = 218000

EVA_CHARS = list('acdehiklmnoqrsty')

# ─── Onset detection ────────────────────────────────────────────────────────

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

# ─── Parse VMS B-dialect corpus ─────────────────────────────────────────────

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
    """Compute onset and suffix distributions from VMS B corpus."""
    all_words = [w for l in b_lines for w in l]
    lf_words  = [l[0]  for l in b_lines if l]
    ll_words  = [l[-1] for l in b_lines if len(l) > 1]
    n = len(all_words)

    # Global onset distribution
    oc_all = Counter(get_onset(w) for w in all_words)
    oc_lf  = Counter(get_onset(w) for w in lf_words)
    oc_ll  = Counter(get_onset(w) for w in ll_words)

    onset_global = {o: cnt/n for o, cnt in oc_all.items()}
    onset_lf     = {o: cnt/len(lf_words) for o, cnt in oc_lf.items()}
    onset_ll     = {o: cnt/len(ll_words) for o, cnt in oc_ll.items()}

    # Suffix distribution: detect common suffixes
    SUFFIX_PATTERNS = [
        'eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy'
    ]
    suf_ctr = Counter()
    for w in all_words:
        matched = False
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf):
                suf_ctr[suf] += 1; matched = True; break
        if not matched: suf_ctr['other'] += 1

    suffix_global = {suf: cnt/n for suf, cnt in suf_ctr.items()}

    # Also compute: am_r, d_ll for reference
    am_r  = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words)
    d_r   = oc_all.get('d', 0) / n
    ll_d  = oc_ll.get('d', 0) / len(ll_words)

    return {
        'onset_global': onset_global,
        'onset_lf': onset_lf,
        'onset_ll': onset_ll,
        'suffix_global': suffix_global,
        'am_r': am_r, 'am_ll_target': ll_am/am_r,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words),
    }

# ─── Simulation ─────────────────────────────────────────────────────────────

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    """
    Build LL_ONSETS from VMS B LL distribution with modifications:
    - d: boosted to d_boost_weight (to achieve d_ll target)
    - qok: set to 0 (to allow qok_ll depletion at LL)
    - remaining onsets: proportionally from VMS LL distribution (excluding d, qok)
    """
    remaining_weight = 1.0 - d_boost_weight
    # Use VMS LL distribution for all onsets except d and qok
    base = {o: v for o, v in onset_ll_vms.items() if o not in ('d', 'qok')}
    base_total = sum(base.values())
    if base_total > 0:
        normalized = {o: v/base_total * remaining_weight for o, v in base.items()}
    else:
        normalized = {}
    normalized['d'] = d_boost_weight
    # qok = 0 (excluded)
    return normalized

def make_word_sim(onset, suffix, rng):
    """Generate a simulated EVA word: onset + connector + suffix."""
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
    """LF override using VMS B LF onset distribution."""
    if rng.random() < p_lf:
        # Draw onset from VMS LF distribution
        onsets = list(onset_lf_vms.keys())
        weights = list(onset_lf_vms.values())
        onset = rng.choices(onsets, weights=weights)[0]
        suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_weights, suffix_weights, rng)

def timm_modify(word, rng):
    if not word: return word
    op = rng.choice(['replace', 'insert', 'delete'])
    pos = rng.randint(0, max(0, len(word)-1))
    if op == 'replace': return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert': return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else: return word[:pos] + word[pos+1:] if len(word)>1 else word

def run_sim(latin_words, onset_weights, suffix_weights, ll_onsets, onset_lf_vms,
            p_blind, p_lf, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf_vms(onset_weights, suffix_weights, onset_lf_vms, p_lf, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_blind(onset_weights, suffix_weights, ll_onsets, p_blind, rng)
            else:
                if buf and rng.random() < CP:
                    ew = timm_modify(rng.choice(list(buf)), rng) if rng.random() < MP else rng.choice(list(buf))
                else:
                    ew = random_eva_word(onset_weights, suffix_weights, rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

# ─── Metric computation (from exp_217) ──────────────────────────────────────

def compute_metrics(lines, vms_ref):
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

    def rate(onset, ctr, n_pos): return ctr.get(onset, 0)/n_pos if n_pos else 0
    def enr(onset, ctr_slot, n_slot, ctr_all, n_all):
        slot_r = rate(onset, ctr_slot, n_slot)
        glob_r = rate(onset, ctr_all, n_all)
        return slot_r/glob_r if glob_r>0 else 0

    am_r   = sum(1 for w in aw if w.endswith('am')) / n
    ll_am  = sum(1 for w in ll if w.endswith('am')) / n_ll if n_ll else 0
    am_ll  = ll_am / am_r if am_r else 0

    d_r    = oc_all.get('d', 0)/n
    d_ll   = enr('d', oc_ll, n_ll, oc_all, n)

    y_r    = oc_all.get('y', 0)/n
    y_lf   = enr('y', oc_lf, n_lf, oc_all, n)

    tb = n-1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o, 0)/n
        return bg.get((o,o),0)/(tb*b*b) if b>0 else 1.0
    ss_mean = (ss('qok')+ss('ok')+ss('ch'))/3
    adj = sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)

    # Uncalibrated metrics
    qok_r  = oc_all.get('qok', 0)/n
    qok_lf = enr('qok', oc_lf, n_lf, oc_all, n)
    d_lf   = enr('d',   oc_lf, n_lf, oc_all, n)
    s_r    = oc_all.get('s', 0)/n
    s_lf   = enr('s',   oc_lf, n_lf, oc_all, n)
    ch_r   = oc_all.get('ch', 0)/n
    ch_ll  = enr('ch',  oc_ll, n_ll, oc_all, n)
    ok_r   = oc_all.get('ok', 0)/n
    ok_ll  = enr('ok',  oc_ll, n_ll, oc_all, n)
    qok_ll = enr('qok', oc_ll, n_ll, oc_all, n)
    ss_d   = ss('d');  ss_y = ss('y')
    am_lf_enr  = (sum(1 for w in lf if w.endswith('am'))/n_lf) / am_r if am_r else 0
    am_mid_enr = (sum(1 for w in mid if w.endswith('am'))/n_mid / am_r) if (n_mid and am_r) else 0
    edy_rate   = sum(1 for w in aw if w.endswith('edy'))/n
    word_len   = sum(len(w) for w in aw)/n
    qok_ch     = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch, am_r=am_r, d_r=d_r, y_r=y_r, ch_r=ch_r, qok_r=qok_r)

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
print(f"  am_ll_target (corpus): {vms['am_ll_target']:.3f}")
print(f"  d_ll_target (corpus):  {vms['d_ll_target']:.3f}")
print()

# Print VMS distributions being used
print("=== VMS B global onset distribution (top 12) ===")
for o, r in sorted(vms['onset_global'].items(), key=lambda x:-x[1])[:12]:
    print(f"  {o:<8}: {r*100:.2f}%")

print("\n=== VMS B LF onset distribution (top 10) ===")
for o, r in sorted(vms['onset_lf'].items(), key=lambda x:-x[1])[:10]:
    enr = r / vms['onset_global'].get(o, 0.001)
    print(f"  {o:<8}: {r*100:.2f}%  ({enr:.2f}x vs global)")

print("\n=== VMS B LL onset distribution (top 10) ===")
for o, r in sorted(vms['onset_ll'].items(), key=lambda x:-x[1])[:10]:
    enr = r / vms['onset_global'].get(o, 0.001)
    print(f"  {o:<8}: {r*100:.2f}%  ({enr:.2f}x vs global)")

print("\n=== VMS B suffix distribution (top 12) ===")
for suf, r in sorted(vms['suffix_global'].items(), key=lambda x:-x[1])[:12]:
    print(f"  {suf:<8}: {r*100:.2f}%")

# Compute d_boost_weight needed to achieve d_ll_target
# With p_blind=X and d_LL_ONSETS=d_boost:
# d_at_LL = p_blind * d_boost + (1-p_blind) * d_global
# d_ll = d_at_LL / d_global = p_blind*(d_boost/d_global - 1) + 1 = d_ll_target
# → d_boost = d_global * [(d_ll_target - 1 + p_blind) / p_blind + 1 - 1]
# Actually: d_ll_target = p_blind*(d_boost/d_global) + (1-p_blind)
# → d_boost = d_global * (d_ll_target - (1-p_blind)) / p_blind

d_global = vms['onset_global'].get('d', 0)
d_ll_target = vms['d_ll_target']

print("\n=== d_boost_weight needed for d_ll calibration at various p_blind ===")
for pb in [0.25, 0.30, 0.33, 0.36, 0.40]:
    d_boost = d_global * (d_ll_target - (1-pb)) / pb
    print(f"  p_blind={pb:.2f}: d_boost={d_boost*100:.2f}%  (vs VMS LL d={vms['onset_ll'].get('d',0)*100:.2f}%)")

# Load Latin
print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

# Use VMS distributions
onset_weights = dict(vms['onset_global'])
suffix_weights = dict(vms['suffix_global'])
onset_lf_vms = dict(vms['onset_lf'])

# Sweep p_blind to calibrate am_ll
P_LF = 1.0  # Use VMS LF distribution for all LF words

print("=== p_blind sweep (N=10 per config) to calibrate am_ll ===")
sweep_results = {}
for pb in [0.25, 0.30, 0.33, 0.36, 0.40]:
    d_boost = d_global * (d_ll_target - (1-pb)) / pb
    if d_boost <= 0 or d_boost > 0.5:
        print(f"  p_blind={pb:.2f}: d_boost infeasible ({d_boost*100:.1f}%)")
        continue
    ll_onsets = build_ll_onsets(vms['onset_ll'], d_boost)
    sims = []
    for i in range(10):
        rng = random.Random(SEED + i)
        lines = run_sim(latin, onset_weights, suffix_weights, ll_onsets, onset_lf_vms, pb, P_LF, rng)
        m = compute_metrics(lines, vms)
        if m: sims.append(m)
    if sims:
        am_ll_mean = sum(x['am_ll'] for x in sims)/len(sims)
        d_ll_mean  = sum(x['d_ll']  for x in sims)/len(sims)
        y_lf_mean  = sum(x['y_lf']  for x in sims)/len(sims)
        ss_mean_   = sum(x['ss_mean']  for x in sims)/len(sims)
        adj_mean   = sum(x['adj_rate'] for x in sims)/len(sims)
        print(f"  p_blind={pb:.2f}: am_ll={am_ll_mean:.3f}({am_ll_mean/vms['am_ll_target']*100:.1f}%) "
              f"d_ll={d_ll_mean:.3f}({d_ll_mean/d_ll_target*100:.1f}%) "
              f"y_lf={y_lf_mean:.3f}({y_lf_mean/vms['onset_lf'].get('y',0.001)/vms['onset_global'].get('y',0.001)*100:.1f}%)  "
              f"[d_boost={d_boost*100:.1f}%]")
        sweep_results[pb] = {'am_ll': am_ll_mean, 'd_ll': d_ll_mean, 'd_boost': d_boost}

# Find best p_blind for am_ll
vms_am_ll_target = vms['am_ll_target']
best_pb = min(sweep_results.keys(), key=lambda pb: abs(sweep_results[pb]['am_ll'] - vms_am_ll_target))
print(f"\n  Best p_blind for am_ll={vms_am_ll_target:.3f}: {best_pb}")
print()

# Full run at best p_blind
print(f"=== Full run: N={N_SIMS} sims at p_blind={best_pb} ===")
d_boost_best = sweep_results[best_pb]['d_boost']
ll_onsets_best = build_ll_onsets(vms['onset_ll'], d_boost_best)
print(f"  d_boost={d_boost_best*100:.2f}%,  LL_ONSETS (top 8):")
for o, w in sorted(ll_onsets_best.items(), key=lambda x:-x[1])[:8]:
    print(f"    {o:<8}: {w*100:.2f}%")
print()

all_metrics = []
for i in range(N_SIMS):
    rng = random.Random(SEED + 1000 + i)
    lines = run_sim(latin, onset_weights, suffix_weights, ll_onsets_best, onset_lf_vms, best_pb, P_LF, rng)
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

# VMS reference values (corpus computed)
VMS_REF = {
    'am_ll': vms['am_ll_target'],
    'd_ll': vms['d_ll_target'],
    'y_lf': (vms['onset_lf'].get('y',0)) / (vms['onset_global'].get('y',0.001)),
    'ss_mean': None,  # use exp_216 corpus value
    'adj_rate': 0.009,
    'qok_lf': (vms['onset_lf'].get('qok',0)) / (vms['onset_global'].get('qok',0.001)),
    'd_lf': (vms['onset_lf'].get('d',0)) / (vms['onset_global'].get('d',0.001)),
    's_lf': (vms['onset_lf'].get('s',0)) / (vms['onset_global'].get('s',0.001)),
    'ch_ll': (vms['onset_ll'].get('ch',0)) / (vms['onset_global'].get('ch',0.001)),
    'ok_ll': (vms['onset_ll'].get('ok',0)) / (vms['onset_global'].get('ok',0.001)),
    'qok_ll': (vms['onset_ll'].get('qok',0)) / (vms['onset_global'].get('qok',0.001)),
    'ss_d': 1.291, 'ss_y': 1.955,
    'am_lf_enr': (sum(1 for w in [l[0] for l in vms_b_lines if l] if w.endswith('am')) / len([l[0] for l in vms_b_lines if l])) / vms['am_r'],
    'am_mid_enr': 0.195,  # from exp_217
    'edy_rate': sum(vms['suffix_global'].get(s,0) for s in ['edy','eedy']),
    'word_len_mean': 5.400,
    'qok_ch': 1.267,
}

METRIC_LABELS = {
    'am_ll':       ('VMS corpus am_ll',     'CALIBRATED'),
    'd_ll':        ('d-onset LL enr',        'CALIBRATED'),
    'y_lf':        ('y-onset LF enr',        'VMS-DIRECT'),
    'ss_mean':     ('onset self-succession', 'CALIBRATED (cp/mp)'),
    'adj_rate':    ('exact adj repeat',      'CALIBRATED (cp/mp)'),
    'qok_lf':      ('qok LF enr',            'VMS-DIRECT'),
    'd_lf':        ('d-onset LF enr',        'VMS-DIRECT'),
    's_lf':        ('s-onset LF enr',        'VMS-DIRECT'),
    'ch_ll':       ('ch-onset LL enr',       'VMS-DIRECT'),
    'ok_ll':       ('ok-onset LL enr',       'VMS-DIRECT'),
    'qok_ll':      ('qok-onset LL enr',      'partial'),
    'ss_d':        ('d self-succession',     'uncalibrated'),
    'ss_y':        ('y self-succession',     'uncalibrated'),
    'am_lf_enr':   ('-am at LF enr',         'uncalibrated'),
    'am_mid_enr':  ('-am at MID enr',        'uncalibrated'),
    'edy_rate':    ('edy-suffix rate',       'VMS-DIRECT (suffix)'),
    'word_len_mean': ('mean word length',    'uncalibrated'),
    'qok_ch':      ('qok->ch bigram enr',    'uncalibrated'),
}

print("=" * 90)
print("EXPANDED METRIC BATTERY: exp_218 VMS-CALIBRATED ARCHITECTURE vs VMS B-DIALECT")
print("=" * 90)
print(f"{'Metric':<16} {'VMS':>8} {'Sim':>8} {'%VMS':>7} {'CI 5-95':>18} {'Status':<8} {'Note'}")
print("-" * 90)

PASS_TOL = 0.20
pass_counts = {'VMS-DIRECT': 0, 'CALIBRATED': 0, 'partial': 0, 'uncalibrated': 0}
total_counts = {'VMS-DIRECT': 0, 'CALIBRATED': 0, 'partial': 0, 'uncalibrated': 0}
pass_count_all = fail_count_all = 0

for key, (label, cal_type) in METRIC_LABELS.items():
    vms_val = VMS_REF.get(key)
    if vms_val is None: continue
    sim_mean, ci_lo, ci_hi = agg(key)
    if abs(vms_val) < 1e-6:
        pct = float('inf'); pass_f = abs(sim_mean) < 0.002
    else:
        pct = sim_mean/vms_val*100
        pass_f = abs(sim_mean-vms_val)/abs(vms_val) <= PASS_TOL

    status = 'PASS' if pass_f else 'FAIL'
    print(f"  {key:<16} {vms_val:>8.3f} {sim_mean:>8.3f} {pct:>6.1f}%  [{ci_lo:.3f},{ci_hi:.3f}]  [{status}]  {cal_type}")

    cat = cal_type.split(' ')[0]
    if cat in total_counts: total_counts[cat] += 1
    else: total_counts['uncalibrated'] += 1
    if pass_f:
        if cat in pass_counts: pass_counts[cat] += 1
        else: pass_counts['uncalibrated'] += 1
        pass_count_all += 1
    else:
        fail_count_all += 1

print()
print("=" * 90)
print("SUMMARY")
print("=" * 90)
print(f"  Total: {pass_count_all}/{pass_count_all+fail_count_all} pass (within ±20%)")
for cat in ['CALIBRATED', 'VMS-DIRECT', 'partial', 'uncalibrated']:
    t = total_counts.get(cat, 0)
    p = pass_counts.get(cat, 0)
    if t: print(f"  {cat}: {p}/{t}")
print()

print("  Improvement vs exp_217 (expected):")
print("  - qok_lf: was 168% (wrong direction); now ~100% (VMS-DIRECT correction)")
print("  - d_lf/s_lf: was 40%/13%; now ~100% (VMS-DIRECT correction)")
print("  - ch_ll/ok_ll: was 196%/204%; now ~100% (VMS-DIRECT correction)")
print("  - qok_ll: partial correction (qok=0 in LL_ONSETS; residual from global rate)")
print("  - Uncalibrated: word_len, ss_d, ss_y, qok_ch — unchanged by these fixes")
