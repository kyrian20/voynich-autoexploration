"""
exp_219: H419 — Onset-Preserving Copy Mechanism

Motivation:
  exp_217 and exp_218 together established that Timm character modifications
  (replace/insert/delete a random character) erode multi-character onset prefixes
  from MID copy-buffer words. This is the UNIVERSAL failure mode for all positional
  enrichment metrics:
  - MID ch/ok/qok rates drop below calibration (Timm erodes ch/ok/qok prefixes)
  - LF/LL positions (which bypass the buffer) appear enriched vs Timm-depleted global
  - Result: wrong-direction or exaggerated positional enrichments

  Diagnosis from F218: "Fixing requires onset-preserving Timm modifications (e.g.,
  modify only suffix positions, never onset positions)."

Fix applied vs exp_218:
  SINGLE CHANGE: timm_modify() now restricts character modifications to the SUFFIX
  region only (characters from onset_len onwards). The onset prefix is NEVER modified.
  All other parameters identical to exp_218 best config:
  - p_blind=0.33 (for direct comparison)
  - p_lf=1.0 (VMS LF distribution for all LF words)
  - cp=0.76, mp=0.9
  - VMS B-calibrated onset, suffix, LF, LL distributions

Expected effects:
  1. ch/ok/qok MID rates restored to VMS calibration → ch_ll/ok_ll/qok_ll approach neutral
  2. qok_lf: MID qok no longer depleted → qok_lf should flip toward VMS depletion (0.778×)
  3. y_lf: MID y rate preserved → enrichment ratio may change (separate issue from erosion)
  4. ss_mean: onset preservation means modified copies ALWAYS have same onset as source
     → ss_mean likely higher than exp_218

CONTROLLED COMPARISON: p_blind held at 0.33 (exp_218 best) to isolate the single-variable
change. A brief sweep also checks whether p_blind needs re-calibration after this change.

Self-audit note: This change CANNOT be feature-destroying for onset self-succession (ss_mean)
because preserving the onset is strictly better for onset self-succession than eroding it.
If ss_mean decreases, that would indicate a bug.
"""

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIMS       = 30
TARGET_LINES = 2447
WINDOW       = 20
CP, MP       = 0.76, 0.9
SEED         = 219000

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

def get_onset_len(w):
    """Return length of the onset prefix of word w."""
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0

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
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words)

    oc_all = Counter(get_onset(w) for w in all_words)
    oc_lf  = Counter(get_onset(w) for w in lf_words)
    oc_ll  = Counter(get_onset(w) for w in ll_words)
    oc_mid = Counter(get_onset(w) for w in mid_words)

    onset_global = {o: cnt/n for o, cnt in oc_all.items()}
    onset_lf     = {o: cnt/len(lf_words) for o, cnt in oc_lf.items()}
    onset_ll     = {o: cnt/len(ll_words) for o, cnt in oc_ll.items()}
    onset_mid    = {o: cnt/len(mid_words) for o, cnt in oc_mid.items()}

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
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words), 'n_mid': len(mid_words),
    }

# ─── Simulation ─────────────────────────────────────────────────────────────

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    """Build LL_ONSETS: VMS LL distribution, d boosted, qok excluded."""
    remaining_weight = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o not in ('d', 'qok')}
    base_total = sum(base.values())
    if base_total > 0:
        normalized = {o: v/base_total * remaining_weight for o, v in base.items()}
    else:
        normalized = {}
    normalized['d'] = d_boost_weight
    return normalized  # qok = 0

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
    """LF override using VMS B LF onset distribution."""
    if rng.random() < p_lf:
        onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
        suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_weights, suffix_weights, rng)

def timm_modify_onset_preserving(word, rng):
    """
    KEY CHANGE vs exp_218: Restrict modifications to SUFFIX region only.
    The onset prefix (characters 0..onset_len-1) is NEVER modified.
    This prevents Timm erosion of onset prefixes in the MID copy buffer.
    """
    if not word: return word
    onset_len = get_onset_len(word)
    suffix_start = onset_len  # first modifiable position

    if suffix_start >= len(word):
        # Word consists entirely of the onset (very short word like 'd', 'o')
        # Cannot modify without eroding onset; return unchanged
        return word

    op = rng.choice(['replace', 'insert', 'delete'])

    if op == 'replace':
        pos = rng.randint(suffix_start, len(word) - 1)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(suffix_start, len(word))
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:  # delete
        if len(word) <= suffix_start + 1:
            # Only one suffix character; deleting would leave only the onset
            # Do a replace instead to ensure something changes
            pos = suffix_start
            return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:] if len(word) > suffix_start else word
        pos = rng.randint(suffix_start, len(word) - 1)
        return word[:pos] + word[pos+1:]

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
                    ew = timm_modify_onset_preserving(rng.choice(list(buf)), rng) if rng.random() < MP else rng.choice(list(buf))
                else:
                    ew = random_eva_word(onset_weights, suffix_weights, rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

# ─── Metric computation ──────────────────────────────────────────────────────

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

    def rate(onset, ctr, n_pos): return ctr.get(onset, 0)/n_pos if n_pos else 0
    def enr(onset, ctr_slot, n_slot, ctr_all, n_all):
        slot_r = rate(onset, ctr_slot, n_slot)
        glob_r = rate(onset, ctr_all, n_all)
        return slot_r/glob_r if glob_r>0 else 0

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

    # Uncalibrated metrics
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

    # Diagnostic: actual MID onset rates (to verify onset preservation)
    oc_mid = Counter(get_onset(w) for w in mid)
    n_mid_total = len(mid)
    ch_mid_r   = oc_mid.get('ch',  0)/n_mid_total if n_mid_total else 0
    qok_mid_r  = oc_mid.get('qok', 0)/n_mid_total if n_mid_total else 0
    ok_mid_r   = oc_mid.get('ok',  0)/n_mid_total if n_mid_total else 0
    y_mid_r    = oc_mid.get('y',   0)/n_mid_total if n_mid_total else 0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch, am_r=am_r,
                ch_mid_r=ch_mid_r, qok_mid_r=qok_mid_r, ok_mid_r=ok_mid_r, y_mid_r=y_mid_r)

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

print("=== VMS B onset distributions: global / MID / LF / LL ===")
print(f"  {'onset':<8} {'global':>8} {'MID':>8} {'LF':>8} {'LL':>8}  {'LF enr':>8} {'LL enr':>8}")
for o in ['ch', 'qok', 'ok', 'sh', 'd', 'y', 's', 'p', 'qo', 'cth', 'ot']:
    g = vms['onset_global'].get(o, 0)
    m = vms['onset_mid'].get(o, 0)
    lf= vms['onset_lf'].get(o, 0)
    ll= vms['onset_ll'].get(o, 0)
    lf_enr = lf/g if g else 0
    ll_enr = ll/g if g else 0
    print(f"  {o:<8} {g*100:>7.2f}% {m*100:>7.2f}% {lf*100:>7.2f}% {ll*100:>7.2f}%  {lf_enr:>7.3f}×  {ll_enr:>7.3f}×")

print(f"\nKey: VMS MID y = {vms['onset_mid'].get('y',0)*100:.2f}% vs global y = {vms['onset_global'].get('y',0)*100:.2f}%")
print(f"     VMS MID ch = {vms['onset_mid'].get('ch',0)*100:.2f}% vs global ch = {vms['onset_global'].get('ch',0)*100:.2f}%")
print()

d_global   = vms['onset_global'].get('d', 0)
d_ll_target = vms['d_ll_target']

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

# Use VMS distributions (same as exp_218)
onset_weights  = dict(vms['onset_global'])
suffix_weights = dict(vms['suffix_global'])
onset_lf_vms   = dict(vms['onset_lf'])
P_LF = 1.0

# Quick sweep to check if p_blind needs recalibration after onset-preserving change
print("=== p_blind sweep (N=10 per config) — checking recalibration need ===")
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
        ch_mid_mean = sum(x['ch_mid_r'] for x in sims)/len(sims)
        qok_mid_mean = sum(x['qok_mid_r'] for x in sims)/len(sims)
        print(f"  p_blind={pb:.2f}: am_ll={am_ll_mean:.3f}({am_ll_mean/vms['am_ll_target']*100:.1f}%) "
              f"d_ll={d_ll_mean:.3f} y_lf={y_lf_mean:.3f} ss={ss_mean_:.3f} adj={adj_mean:.4f}  "
              f"[ch_mid={ch_mid_mean*100:.1f}% qok_mid={qok_mid_mean*100:.1f}%]")
        sweep_results[pb] = {'am_ll': am_ll_mean, 'd_ll': d_ll_mean, 'd_boost': d_boost, 'ss_mean': ss_mean_}

# Find best p_blind for am_ll
vms_am_ll_target = vms['am_ll_target']
best_pb = min(sweep_results.keys(), key=lambda pb: abs(sweep_results[pb]['am_ll'] - vms_am_ll_target))
print(f"\n  Best p_blind for am_ll: {best_pb}")
print(f"  exp_218 used p_blind=0.33 — comparison config: p_blind=0.33")
print()

# Run at p_blind=0.33 for direct comparison with exp_218
# AND at best_pb if different
configs = [0.33]
if best_pb != 0.33:
    configs.append(best_pb)

for run_pb in configs:
    d_boost = d_global * (d_ll_target - (1-run_pb)) / run_pb
    if d_boost <= 0 or d_boost > 0.5:
        print(f"Skipping p_blind={run_pb} (d_boost infeasible)")
        continue
    ll_onsets_run = build_ll_onsets(vms['onset_ll'], d_boost)

    label = "DIRECT COMPARISON (same p_blind as exp_218)" if run_pb == 0.33 else "BEST p_blind"
    print(f"=== Full run: N={N_SIMS} sims at p_blind={run_pb} [{label}] ===")
    print(f"  d_boost={d_boost*100:.2f}%")
    print()

    all_metrics = []
    for i in range(N_SIMS):
        rng = random.Random(SEED + 1000 + i)
        lines = run_sim(latin, onset_weights, suffix_weights, ll_onsets_run, onset_lf_vms, run_pb, P_LF, rng)
        m = compute_metrics(lines, vms)
        if m: all_metrics.append(m)

    print(f"  Completed {len(all_metrics)} simulations.")

    # Diagnostic: mean MID onset rates
    ch_mid_diag  = sum(x['ch_mid_r']  for x in all_metrics)/len(all_metrics)
    qok_mid_diag = sum(x['qok_mid_r'] for x in all_metrics)/len(all_metrics)
    ok_mid_diag  = sum(x['ok_mid_r']  for x in all_metrics)/len(all_metrics)
    y_mid_diag   = sum(x['y_mid_r']   for x in all_metrics)/len(all_metrics)
    print(f"\n  === DIAGNOSTIC: MID onset rates (vs VMS MID) ===")
    print(f"  ch:  sim MID = {ch_mid_diag*100:.2f}%  VMS MID = {vms['onset_mid'].get('ch',0)*100:.2f}%  VMS global = {vms['onset_global'].get('ch',0)*100:.2f}%")
    print(f"  qok: sim MID = {qok_mid_diag*100:.2f}%  VMS MID = {vms['onset_mid'].get('qok',0)*100:.2f}%  VMS global = {vms['onset_global'].get('qok',0)*100:.2f}%")
    print(f"  ok:  sim MID = {ok_mid_diag*100:.2f}%  VMS MID = {vms['onset_mid'].get('ok',0)*100:.2f}%  VMS global = {vms['onset_global'].get('ok',0)*100:.2f}%")
    print(f"  y:   sim MID = {y_mid_diag*100:.2f}%  VMS MID = {vms['onset_mid'].get('y',0)*100:.2f}%  VMS global = {vms['onset_global'].get('y',0)*100:.2f}%")
    print()

    def agg(key):
        vals = sorted(x[key] for x in all_metrics)
        mean = sum(vals)/len(vals)
        ci_lo = vals[max(0, int(.05*len(vals)))]
        ci_hi = vals[min(len(vals)-1, int(.95*len(vals)))]
        return mean, ci_lo, ci_hi

    # VMS reference values (corpus computed)
    vms_ss_qok = (vms['onset_lf'].get('qok',0)) / (vms['onset_global'].get('qok',0.001))  # qok_lf
    VMS_REF = {
        'am_ll':       vms['am_ll_target'],
        'd_ll':        vms['d_ll_target'],
        'y_lf':        vms['onset_lf'].get('y',0) / vms['onset_global'].get('y',0.001),
        'ss_mean':     1.164,   # VMS B corpus ss_mean (computed)
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

    METRIC_LABELS = {
        'am_ll':       ('am_ll (corpus)',      'CALIBRATED'),
        'd_ll':        ('d-onset LL enr',      'CALIBRATED'),
        'y_lf':        ('y-onset LF enr',      'VMS-DIRECT'),
        'ss_mean':     ('ss_mean (corpus)',    'CALIBRATED (cp/mp)'),
        'adj_rate':    ('exact adj repeat',    'CALIBRATED (cp/mp)'),
        'qok_lf':      ('qok LF enr',          'VMS-DIRECT'),
        'd_lf':        ('d-onset LF enr',      'VMS-DIRECT'),
        's_lf':        ('s-onset LF enr',      'VMS-DIRECT'),
        'ch_ll':       ('ch-onset LL enr',     'VMS-DIRECT'),
        'ok_ll':       ('ok-onset LL enr',     'VMS-DIRECT'),
        'qok_ll':      ('qok-onset LL enr',    'partial'),
        'ss_d':        ('d self-succession',   'uncalibrated'),
        'ss_y':        ('y self-succession',   'uncalibrated'),
        'am_lf_enr':   ('-am at LF enr',       'uncalibrated'),
        'am_mid_enr':  ('-am at MID enr',      'uncalibrated'),
        'edy_rate':    ('edy-suffix rate',     'VMS-DIRECT (suffix)'),
        'word_len_mean': ('mean word length',  'uncalibrated'),
        'qok_ch':      ('qok->ch bigram enr',  'uncalibrated'),
    }

    print("=" * 95)
    print(f"EXPANDED METRIC BATTERY: exp_219 ONSET-PRESERVING COPY  [p_blind={run_pb}]")
    print(f"vs exp_218 (ALL-CHAR TIMM, p_blind=0.33) — KEY COMPARISON")
    print("=" * 95)
    print(f"{'Metric':<16} {'VMS':>8} {'E219':>8} {'%VMS':>7} {'Status':<6}  vs exp_218 (approx)")
    print("-" * 95)

    # exp_218 reference values for comparison
    EXP218_REF = {
        'am_ll': 6.451, 'd_ll': 1.243, 'y_lf': 2.515, 'ss_mean': None, 'adj_rate': 0.004,
        'qok_lf': 1.447, 'd_lf': 2.015, 's_lf': 2.320, 'ch_ll': 1.720, 'ok_ll': 1.512,
        'qok_ll': 1.230, 'ss_d': 1.577, 'ss_y': 1.804, 'am_lf_enr': 0.368, 'am_mid_enr': 0.248,
        'edy_rate': 0.117, 'word_len_mean': 6.502, 'qok_ch': 0.955,
    }

    PASS_TOL = 0.20
    pass_count_all = 0; total_all = 0

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
        e218_val = EXP218_REF.get(key)
        e218_note = f"was {e218_val:.3f}" if e218_val is not None else "N/A"
        delta = f"{'↑' if sim_mean > e218_val else '↓'}{abs(sim_mean - e218_val):.3f}" if e218_val is not None else ""
        print(f"  {key:<16} {vms_val:>8.3f} {sim_mean:>8.3f} {pct:>6.1f}%  [{status}]   {e218_note} {delta}  [{cal_type}]")

        total_all += 1
        if pass_f: pass_count_all += 1

    print()
    print("=" * 95)
    print("SUMMARY")
    print("=" * 95)
    print(f"  exp_219 (onset-preserving): {pass_count_all}/{total_all} pass")
    print(f"  exp_218 (all-char Timm):    4/17 pass  (direct comparison)")
    print()
    print(f"  Configuration: p_blind={run_pb}, d_boost={d_boost*100:.2f}%, p_lf=1.0 (VMS LF dist), cp={CP}, mp={MP}")
    print(f"  Key test: did onset-preserving modification fix Timm erosion failures?")
    print(f"  Expected improvements: ch_ll/ok_ll/qok_ll → neutral; qok_lf → depletion (VMS 0.778×)")
    print()
