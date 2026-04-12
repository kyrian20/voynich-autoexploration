"""
exp_224: H408 — Parameter-Count Control

Motivation:
  exp_211 achieves all 5 primary VMS metrics within 3% using 4 calibrated parameters
  (p_blind, d_am, p_lf_blind, cp/mp) in the Mode B architecture (blind LL + VMS LF dist
  + onset-preserving Timm char mod copy buffer).

  Mode B (exp_221) achieves 11/18 pass on the full 18-metric battery, and exp_223
  confirms this is a stable corpus-level property.

  H408 asks: Is the 11/18 result about the SPECIFIC ARCHITECTURE, or is it achievable
  by ANY 3-parameter position-aware model with a copy buffer?

  Test: Replace the specific architectural choices with QUALITATIVELY DIFFERENT ones
  while keeping the same parameter count:

  ALTERNATIVE ARCHITECTURE A — Random LL suffix (no -am bias):
    - LL mapping: p_rand fraction of LL words drawn from RANDOM EVA onset + RANDOM suffix
      (no -am preference); remaining fraction = standard random word
    - LF mapping: p_lf fraction drawn from VMS LF onset distribution (VMS-direct, same as Mode B)
    - MID: onset-preserving copy buffer (same as Mode B)
    - Parameters: p_rand ∈ {0.10, 0.20, 0.30}, cp ∈ {0.40, 0.55, 0.70}, mp=0.90
    - Expected: am_ll will NOT be reproduced (random LL suffix produces am_ll≈1.0)
    - This tests the architectural necessity of the blind -am rule

  ALTERNATIVE ARCHITECTURE B — Uniform suffix LL mapping (p_am, p_edy, p_other):
    - LL mapping: draw LL suffix from {am: p_am, edy: p_edy, other: 1-p_am-p_edy}
    - Can tuned to reproduce am_ll by setting p_am appropriately
    - Parameters: p_am ∈ {0.10, 0.15, 0.20}, p_edy ∈ {0, 0.05, 0.10}, cp=0.55
    - This tests whether a DIFFERENT mechanism for am_ll enrichment also works

  ALTERNATIVE ARCHITECTURE C — Uniform LF (no VMS LF distribution):
    - LF mapping: p_lf fraction drawn from uniform over all onset classes (no VMS-direct)
    - LL mapping: same as Mode B (blind -am)
    - Parameters: p_lf ∈ {0.10, 0.20, 0.30}, cp=0.55, mp=0.90
    - This tests the architectural necessity of the VMS LF onset calibration
    - Expected: y_lf, d_lf, s_lf, qok_lf will fail (no positional onset structure at LF)

  Mode B (exp_221 best): 11/18 pass. If ANY alternative architecture also achieves 11/18,
  then the result is about parameter count, not architecture-specific choices.
  If alternatives fail on the specific metrics they bypass: architecture MATTERS.

Report: for each alternative architecture, report pass count on 18-metric battery
and specifically whether the bypassed architectural feature leads to expected failures.
"""

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIMS       = 20
TARGET_LINES = 2447
WINDOW       = 20
SEED         = 224000
P_LF    = 1.0

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
        'onset_global': onset_global, 'onset_lf': onset_lf, 'onset_ll': onset_ll, 'onset_mid': onset_mid,
        'suffix_global': suffix_global,
        'am_r': am_r, 'am_ll_target': ll_am/am_r,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words),
        'vms_b_lines': b_lines,
    }

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    remaining_weight = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o not in ('d', 'qok')}
    base_total = sum(base.values())
    normalized = {o: v/base_total * remaining_weight for o, v in base.items()} if base_total > 0 else {}
    normalized['d'] = d_boost_weight
    return normalized

def make_word_sim(onset, suffix, rng):
    connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
    return onset + connector + suffix

def random_eva_word(onset_weights, suffix_weights, rng):
    onset  = rng.choices(list(onset_weights.keys()),  weights=list(onset_weights.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
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

# ─── Architecture variants ────────────────────────────────────────────────────

# MODE B (baseline): p_blind=0.30, VMS LF onset, VMS MID onset, onset-preserving Timm
def run_mode_b(latin_words, onset_weights_mid, suffix_weights, ll_onsets, onset_lf_vms,
               cp, mp, p_blind, rng):
    """exp_221 Mode B architecture."""
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
                suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
                ew = make_word_sim(onset, suffix, rng)
            elif i == len(chunk)-1:
                if rng.random() < p_blind:
                    onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
                    ew = make_word_sim(onset, 'am', rng)
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_weights, rng)
            else:
                if buf and rng.random() < cp:
                    ew = timm_modify_onset_preserving(rng.choice(list(buf)), rng) if rng.random() < mp else rng.choice(list(buf))
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_weights, rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

# ALT A: No -am LL bias — LL words drawn entirely from uniform random (no positional rule)
def run_alt_a(latin_words, onset_weights_mid, suffix_weights, onset_lf_vms,
              cp, mp, rng):
    """Alternative A: VMS LF onset, but NO special LL rule (all LL = random)."""
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
                suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
                ew = make_word_sim(onset, suffix, rng)
            elif i == len(chunk)-1:
                # NO special LL rule — just random
                ew = random_eva_word(onset_weights_mid, suffix_weights, rng)
            else:
                if buf and rng.random() < cp:
                    ew = timm_modify_onset_preserving(rng.choice(list(buf)), rng) if rng.random() < mp else rng.choice(list(buf))
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_weights, rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

# ALT B: Uniform suffix LL (p_am, 0, 1-p_am = other) — different am_ll mechanism
def run_alt_b(latin_words, onset_weights_mid, suffix_weights, onset_lf_vms,
              cp, mp, p_am, rng):
    """Alternative B: VMS LF onset, LL draws from suffix={am:p_am, other:1-p_am} (no onset boost)."""
    ll_suffix_probs = {'am': p_am, 'other': 1.0-p_am}
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
                suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
                ew = make_word_sim(onset, suffix, rng)
            elif i == len(chunk)-1:
                # LL: random onset from global, suffix biased toward am
                suf = rng.choices(list(ll_suffix_probs.keys()), weights=list(ll_suffix_probs.values()))[0]
                if suf == 'other':
                    suf = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
                onset = rng.choices(list(onset_weights_mid.keys()), weights=list(onset_weights_mid.values()))[0]
                ew = make_word_sim(onset, suf, rng)
            else:
                if buf and rng.random() < cp:
                    ew = timm_modify_onset_preserving(rng.choice(list(buf)), rng) if rng.random() < mp else rng.choice(list(buf))
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_weights, rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

# ALT C: Uniform LF (no VMS LF distribution) — LL uses Mode B blind -am
def run_alt_c(latin_words, onset_weights_mid, suffix_weights, ll_onsets,
              cp, mp, p_blind, p_lf_unif, rng):
    """Alternative C: NO VMS LF onset preference (uniform LF), Mode B LL."""
    # LF gets all onset classes with equal probability (uniform_onset)
    uniform_onset = {o: 1.0/len(ONSET_ORDER) for _, o in ONSET_ORDER}
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                if rng.random() < p_lf_unif:
                    # Uniform LF onset — no VMS structure
                    onset = rng.choice([o for _, o in ONSET_ORDER])
                    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
                    ew = make_word_sim(onset, suffix, rng)
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_weights, rng)
            elif i == len(chunk)-1:
                if rng.random() < p_blind:
                    onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
                    ew = make_word_sim(onset, 'am', rng)
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_weights, rng)
            else:
                if buf and rng.random() < cp:
                    ew = timm_modify_onset_preserving(rng.choice(list(buf)), rng) if rng.random() < mp else rng.choice(list(buf))
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_weights, rng)
                buf.append(ew)
            line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

# ─── Main ────────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus...")
vms_b_lines = parse_vms_corpus()
vms = compute_vms_distributions(vms_b_lines)
print(f"  VMS B: {len(vms_b_lines)} lines, {vms['n']} words")

d_global = vms['onset_global'].get('d', 0)
d_ll_target = vms['d_ll_target']
P_BLIND = 0.30
d_boost = d_global * (d_ll_target - (1-P_BLIND)) / P_BLIND
ll_onsets = build_ll_onsets(vms['onset_ll'], d_boost)
onset_lf_vms = dict(vms['onset_lf'])
onset_weights_mid = dict(vms['onset_mid'])
suffix_weights = dict(vms['suffix_global'])

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

print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

METRIC_ORDER = [
    'am_ll', 'd_ll', 'y_lf', 'ss_mean', 'adj_rate',
    'qok_lf', 'd_lf', 's_lf', 'ch_ll', 'ok_ll', 'qok_ll',
    'ss_d', 'ss_y', 'am_lf_enr', 'am_mid_enr', 'edy_rate', 'word_len_mean', 'qok_ch'
]

def run_and_score(sim_func, name, N=N_SIMS):
    all_metrics = []
    for i in range(N):
        m = compute_metrics(sim_func(i), vms)
        if m: all_metrics.append(m)
    pass_count = 0; results = {}
    for key in METRIC_ORDER:
        vms_val = VMS_REF.get(key, 0)
        sim_mean = sum(x[key] for x in all_metrics)/len(all_metrics) if all_metrics else 0
        pct = sim_mean/vms_val*100 if abs(vms_val)>1e-6 else float('inf')
        pass_f = abs(sim_mean-vms_val)/abs(vms_val) <= 0.20 if abs(vms_val)>1e-6 else abs(sim_mean)<0.002
        results[key] = (vms_val, sim_mean, pct, pass_f)
        if pass_f: pass_count += 1
    return results, pass_count

# Mode B (baseline)
print("=" * 90)
print(f"MODE B (baseline, cp=0.55, mp=0.90, p_blind=0.30): N={N_SIMS}")
print("=" * 90)
def mode_b_sim(i): return run_mode_b(latin, onset_weights_mid, suffix_weights, ll_onsets,
                                      onset_lf_vms, 0.55, 0.90, P_BLIND, random.Random(SEED+i))
res_b, pc_b = run_and_score(mode_b_sim, "Mode B")
print(f"  Mode B pass count: {pc_b}/18")

# Alt A: No LL rule
print("\nALT A: No LL positional rule (all LL = random word)")
def alt_a_sim(i): return run_alt_a(latin, onset_weights_mid, suffix_weights, onset_lf_vms,
                                    0.55, 0.90, random.Random(SEED+1000+i))
res_a, pc_a = run_and_score(alt_a_sim, "Alt A")
print(f"  Alt A pass count: {pc_a}/18")

# Alt B: Uniform suffix LL with p_am
# Find best p_am from sweep first
print("\nALT B SWEEP: Uniform suffix LL with p_am parameter")
best_b_count = 0; best_p_am = 0
for p_am in [0.05, 0.10, 0.13, 0.15, 0.18, 0.20, 0.25]:
    sims = []
    for i in range(10):
        rng = random.Random(SEED+2000+i+int(p_am*100))
        lines = run_alt_b(latin, onset_weights_mid, suffix_weights, onset_lf_vms, 0.55, 0.90, p_am, rng)
        m = compute_metrics(lines, vms)
        if m: sims.append(m)
    if sims:
        am_ll_mean = sum(x['am_ll'] for x in sims)/len(sims)
        pct = am_ll_mean/VMS_REF['am_ll']*100
        print(f"  p_am={p_am:.2f}: am_ll={am_ll_mean:.3f} ({pct:.1f}%VMS)")
        # Count passes
        passes = sum(1 for key in METRIC_ORDER
                     if abs(sum(x[key] for x in sims)/len(sims) - VMS_REF.get(key,0))/max(abs(VMS_REF.get(key,0)),1e-6) <= 0.20)
        if passes > best_b_count:
            best_b_count = passes; best_p_am = p_am

print(f"  Best Alt B: p_am={best_p_am}, {best_b_count}/18 passes (from sweep N=10)")

# Full run at best p_am
print(f"\nALT B FULL: p_am={best_p_am}, N={N_SIMS}")
def alt_b_sim(i): return run_alt_b(latin, onset_weights_mid, suffix_weights, onset_lf_vms,
                                    0.55, 0.90, best_p_am, random.Random(SEED+2000+i))
res_balt, pc_balt = run_and_score(alt_b_sim, "Alt B")
print(f"  Alt B pass count: {pc_balt}/18")

# Alt C: No VMS LF distribution
print("\nALT C: No VMS LF onset distribution (uniform LF onset), Mode B LL")
def alt_c_sim(i): return run_alt_c(latin, onset_weights_mid, suffix_weights, ll_onsets,
                                    0.55, 0.90, P_BLIND, 0.30, random.Random(SEED+3000+i))
res_c, pc_c = run_and_score(alt_c_sim, "Alt C")
print(f"  Alt C pass count: {pc_c}/18")

# Print comparison table
print()
print("=" * 110)
print("COMPARISON: MODE B vs ALTERNATIVE ARCHITECTURES")
print("=" * 110)
print(f"  {'Metric':<16} {'VMS':>7}  "
      f"{'ModeB':>7} {'%':>6} {'P?':>2}  |  "
      f"{'AltA':>7} {'%':>6} {'P?':>2}  |  "
      f"{'AltB':>7} {'%':>6} {'P?':>2}  |  "
      f"{'AltC':>7} {'%':>6} {'P?':>2}")
print(f"  {'-'*105}")

for key in METRIC_ORDER:
    vms_val = VMS_REF.get(key, 0)
    def fmt(results, k):
        vv, sv, pct, pf = results.get(k, (0,0,0,False))
        return sv, pct, 'P' if pf else 'F'
    sb, pb, pfb = fmt(res_b, key)
    sa, pa, pfa = fmt(res_a, key)
    sbalt, pbalt, pfbalt = fmt(res_balt, key)
    sc, pc_val, pfc = fmt(res_c, key)
    print(f"  {key:<16} {vms_val:>7.3f}  "
          f"{sb:>7.3f} {pb:>5.1f}% {pfb:>2}  |  "
          f"{sa:>7.3f} {pa:>5.1f}% {pfa:>2}  |  "
          f"{sbalt:>7.3f} {pbalt:>5.1f}% {pfbalt:>2}  |  "
          f"{sc:>7.3f} {pc_val:>5.1f}% {pfc:>2}")

print()
print(f"  Pass count:  Mode B={pc_b}/18  |  Alt A (no LL rule)={pc_a}/18  |  "
      f"Alt B (uniform suffix LL, p_am={best_p_am})={pc_balt}/18  |  Alt C (uniform LF)={pc_c}/18")
print()
print("=" * 110)
print("ARCHITECTURAL NECESSITY SUMMARY")
print("=" * 110)
print(f"  Mode B specific features:")
print(f"    (1) Blind -am rule at LL (p_blind=0.30): needed for am_ll enrichment")
print(f"    (2) VMS LF onset distribution at LF (p_lf=1.0): needed for y_lf/d_lf/s_lf/qok_lf")
print(f"    (3) VMS MID onset distribution for MID: needed for y_lf/s_lf calibration")
print(f"    (4) Onset-preserving Timm modification: needed for ch_ll/ok_ll/qok_lf direction")
print()
print(f"  Alt A removes (1): tests whether VMS LF dist + copy buffer alone gives 11/18")
print(f"  Alt B replaces (1) with uniform suffix: tests whether -am IS the LL rule or just any suffix bias")
print(f"  Alt C removes (2): tests whether VMS LF onset structure is necessary")
