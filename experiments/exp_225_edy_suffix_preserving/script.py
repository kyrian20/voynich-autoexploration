"""
exp_225: H425 — edy-Suffix-Preserving Modification

Motivation:
  exp_221 (Mode B, cp=0.55, mp=0.90) achieves 11/18 PASS — program best.
  One of the 7 remaining failures is edy_rate=0.140 (72.4% of VMS 0.194).

  Root cause (diagnosed in exp_222/F222): Timm copy buffer modification erodes
  'edy' endings. When an edy-suffix word in the buffer is modified in its suffix
  region, the 'edy' characters can be replaced, inserted into, or deleted from,
  producing a non-edy word. This is the SAME failure mode as onset erosion
  (which was fixed by onset-preserving modification in exp_219, yielding +4 passes).

  Fix: additionally protect the 'edy'/'eedy' suffix from modification. The
  modifiable region becomes [onset_len : len(word) - edy_suffix_len]. If this
  region is empty (onset + edy suffix covers the whole word), return word unchanged.

  This is a SINGLE CONTROLLED CHANGE from exp_221. All other architecture
  parameters are identical: Mode B (VMS MID onset for MID, onset-preserving,
  p_blind=0.30, p_lf=1.0, d_boost calibrated, cp=0.55, mp=0.90).

  Question: Does edy-suffix preservation fix edy_rate without regressing any of
  the 11 currently passing metrics?

  Expected outcome:
  - edy_rate: 0.140 → ~0.194 (PASS). Mechanism: edy-ending buffer words always
    output edy-ending modified copies; fresh words draw from global suffix
    distribution (edy ≈ 19.4%); combined output edy_rate ≈ VMS 19.4%.
  - All 11 currently passing metrics maintained (modification-region narrowing
    does not affect onset structure, LF/LL rules, or ss_mean if onset still preserved).
  - word_len_mean: may slightly increase (edy-region blocking prevents some deletions
    from edy words) or decrease (can't insert into edy region). Monitor for change.
  - am_lf_enr / am_mid_enr / qok_ll / qok_ch: expect unchanged (no mechanism path).
  - adj_rate: may be slightly affected if edy-blocked words are returned unchanged
    more often (unmodified copy → higher adj_rate risk). Monitor.

  If edy_rate PASSES → 12/18 PASS — new program best.
  If edy_rate PARTIALLY IMPROVES → documents ceiling without full edy preservation.
  If edy_rate UNCHANGED → mechanism diagnosis is wrong (not Timm erosion).
"""

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIMS_FULL  = 30
TARGET_LINES = 2447
WINDOW       = 20
SEED         = 225000
P_BLIND = 0.30
P_LF    = 1.0
CP      = 0.55
MP      = 0.90

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
    """Return the length of the edy-type suffix to protect (0 if none)."""
    if w.endswith('eedy'): return 4
    if w.endswith('edy'):  return 3
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

def timm_modify_onset_and_edy_preserving(word, rng):
    """
    Onset-preserving AND edy-suffix-preserving Timm modification.
    Modifiable region: [onset_len : len(word) - edy_suffix_len]
    If region is empty, return word unchanged (cannot modify without eroding onset or edy).
    """
    if not word: return word
    onset_len = get_onset_len(word)
    edy_len   = get_edy_suffix_len(word)
    mod_start = onset_len
    mod_end   = len(word) - edy_len   # exclusive upper bound on modifiable region
    if mod_start >= mod_end:
        # No modifiable positions — return unchanged
        return word
    op = rng.choice(['replace', 'insert', 'delete'])
    if op == 'replace':
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(mod_start, mod_end)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:  # delete
        if mod_end - mod_start <= 1:
            # Only one modifiable char — replace instead of delete to avoid pathological shortening
            pos = mod_start
            return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
        pos = rng.randint(mod_start, mod_end - 1)
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
                    if rng.random() < mp:
                        ew = timm_modify_onset_and_edy_preserving(rng.choice(list(buf)), rng)
                    else:
                        ew = rng.choice(list(buf))
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

# ─── Main ─────────────────────────────────────────────────────────────────────

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
onset_weights_mid = dict(vms['onset_mid'])

print(f"  p_blind={P_BLIND}, d_boost={d_boost*100:.2f}%, p_lf={P_LF}")
print(f"  onset_weights = VMS MID onset distribution")
print(f"  cp={CP}, mp={MP}")
print()

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

# edy preservation diagnostic
n_edy_check = min(1000, len(vms_b_lines)*10)
all_vms = [w for l in vms_b_lines for w in l][:n_edy_check]
edy_words = [w for w in all_vms if w.endswith('edy') or w.endswith('eedy')]
no_middle = [w for w in edy_words if get_edy_suffix_len(w) + get_onset_len(w) >= len(w)]
print(f"Edy-preservation diagnostic:")
print(f"  Sample edy words: {len(edy_words)} (from first {min(n_edy_check,len(all_vms))} VMS words)")
print(f"  Edy words with NO modifiable middle region: {len(no_middle)} ({100*len(no_middle)/max(1,len(edy_words)):.1f}%)")
print(f"  Example no-middle: {no_middle[:8]}")
mid_examples = [w for w in edy_words if get_edy_suffix_len(w) + get_onset_len(w) < len(w)]
print(f"  Example with middle: {mid_examples[:8]}")
print()

VMS_AM  = vms['am_ll_target']
VMS_SS  = 1.164
VMS_ADJ = 0.009
VMS_YLF = vms['onset_lf'].get('y',0) / vms['onset_global'].get('y',0.001)

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

# exp_221 Mode B baseline for comparison
EXP221_REF = {
    'am_ll': 6.258, 'd_ll': 1.247, 'y_lf': 3.389, 'ss_mean': 1.347, 'adj_rate': 0.003,
    'qok_lf': 0.753, 'd_lf': 2.321, 's_lf': 5.142, 'ch_ll': 1.052, 'ok_ll': 1.067,
    'qok_ll': 0.730, 'ss_d': 1.483, 'ss_y': 1.632, 'am_lf_enr': 0.400, 'am_mid_enr': 0.291,
    'edy_rate': 0.140, 'word_len_mean': 6.595, 'qok_ch': 0.963,
}

METRIC_LABELS = [
    ('am_ll', 'CALIBRATED'), ('d_ll', 'CALIBRATED'), ('y_lf', 'VMS-DIRECT'),
    ('ss_mean', 'CALIBRATED (cp/mp)'), ('adj_rate', 'CALIBRATED (cp/mp)'),
    ('qok_lf', 'VMS-DIRECT'), ('d_lf', 'VMS-DIRECT'), ('s_lf', 'VMS-DIRECT'),
    ('ch_ll', 'VMS-DIRECT'), ('ok_ll', 'VMS-DIRECT'), ('qok_ll', 'partial'),
    ('ss_d', 'uncalibrated'), ('ss_y', 'uncalibrated'), ('am_lf_enr', 'uncalibrated'),
    ('am_mid_enr', 'uncalibrated'), ('edy_rate', 'TARGET METRIC'),
    ('word_len_mean', 'uncalibrated'), ('qok_ch', 'uncalibrated'),
]

print(f"{'='*95}")
print(f"FULL RUN: Mode B + edy-suffix-preserving modification")
print(f"Architecture: VMS MID onset (MID), onset-preserving + edy-preserving Timm mod")
print(f"p_blind={P_BLIND}, d_boost={d_boost*100:.2f}%, p_lf={P_LF}, cp={CP}, mp={MP}, N={N_SIMS_FULL}")
print(f"{'='*95}")

all_metrics = []
for i in range(N_SIMS_FULL):
    rng = random.Random(SEED + i)
    lines = run_sim(latin, onset_weights_mid, suffix_weights, ll_onsets, onset_lf_vms, CP, MP, rng)
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

PASS_TOL = 0.20
pass_count = 0; total = 0

print(f"  {'Metric':<16} {'VMS':>8} {'E225':>8} {'%':>7} {'P?':<4}  E221    delta")
print(f"  {'-'*80}")
for key, cat in METRIC_LABELS:
    vms_val = VMS_REF.get(key)
    if vms_val is None: continue
    sim_mean, ci_lo, ci_hi = agg(key)
    pct = sim_mean/vms_val*100 if abs(vms_val)>1e-6 else float('inf')
    pass_f = abs(sim_mean-vms_val)/abs(vms_val) <= PASS_TOL if abs(vms_val)>1e-6 else abs(sim_mean)<0.002
    status = 'P' if pass_f else 'F'
    e221 = EXP221_REF.get(key, float('nan'))
    delta = sim_mean - e221
    print(f"  {key:<16} {vms_val:>8.3f} {sim_mean:>8.3f} {pct:>6.1f}% {status}    {e221:>7.3f}  {delta:>+7.3f}  [{cat}]")
    total += 1
    if pass_f: pass_count += 1

print()
print(f"  Pass count: exp_225 (edy-preserving) = {pass_count}/{total}  |  exp_221 (baseline) = 11/18")
print()
print(f"  Focused edy comparison:")
edy_mean, edy_lo, edy_hi = agg('edy_rate')
print(f"    VMS edy_rate:     {VMS_REF['edy_rate']:.4f} (100.0%)")
print(f"    exp_221 edy_rate: {EXP221_REF['edy_rate']:.4f} ({100*EXP221_REF['edy_rate']/VMS_REF['edy_rate']:.1f}%) FAIL")
print(f"    exp_225 edy_rate: {edy_mean:.4f} ({100*edy_mean/VMS_REF['edy_rate']:.1f}%) {'PASS' if abs(edy_mean-VMS_REF['edy_rate'])/VMS_REF['edy_rate']<=0.20 else 'FAIL'}")
print(f"    Improvement: {100*(edy_mean-EXP221_REF['edy_rate'])/VMS_REF['edy_rate']:+.1f}pp (% of VMS)")
print()
print(f"  Word length impact:")
wl_mean, wl_lo, wl_hi = agg('word_len_mean')
print(f"    exp_221 word_len: {EXP221_REF['word_len_mean']:.3f}")
print(f"    exp_225 word_len: {wl_mean:.3f}  (delta: {wl_mean-EXP221_REF['word_len_mean']:+.3f})")
print(f"    VMS word_len:     {VMS_REF['word_len_mean']:.3f}")
print()
print(f"  adj_rate impact:")
adj_mean, adj_lo, adj_hi = agg('adj_rate')
print(f"    exp_221 adj_rate: {EXP221_REF['adj_rate']:.4f}")
print(f"    exp_225 adj_rate: {adj_mean:.4f}  (delta: {adj_mean-EXP221_REF['adj_rate']:+.4f})")
