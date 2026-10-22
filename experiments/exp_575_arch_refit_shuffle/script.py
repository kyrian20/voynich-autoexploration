"""
exp_575: Architecture Refit to Shuffled Targets — Real Negative Control

exp_574 tested whether the FIXED exp_314 parameters can match shuffled corpora against
VMS_REF as the target. Result: 10/19 on both shuffled conditions.

This experiment asks a harder question: if we run a FRESH GRID SEARCH optimizing
parameters to match EACH CORPUS'S OWN METRICS as the target, how many metrics can
the architecture achieve on:
  1. Real B-dialect (positive control — expected ~19/19)
  2. Within-line shuffled VMS B-dialect (intra-shuffle)
  3. Word-to-line shuffled VMS B-dialect (inter-shuffle)

This is the true negative control. If the architecture achieves near-19/19 on
shuffled corpora when the shuffled corpus's own metrics are the target, then:
  → 6 free parameters are enough to fit any corpus structure
  → The real-VMS 19/19 is primarily about parameter flexibility, not VMS specificity

If the architecture CANNOT achieve near-19/19 even when calibrated to shuffled targets,
then there exist structural properties of VMS that the architecture captures specifically,
and some target metrics are fundamentally unreachable by this architecture regardless
of parameter choice.

Key prediction from structural analysis:
  - Inter-shuffle ss_y ≈ 0.5585 (target range [0.447, 0.670])
  - Copy-buffer always generates ss_y >> 1.0 (≈1.6–2.0) regardless of parameters
  - Therefore: inter-shuffle CANNOT achieve 19/19 — structural impossibility on ss_y
  - Intra-shuffle ss_y ≈ 1.63 (target range [1.30, 1.96]) — architecture CAN achieve this

Grid: beta_scale[4] x p_blind[4] x r_lf[4] x r_mid[4] x p_qokch[4] = 1024 combos
Fast pass (N=3) → top candidates → confirm pass (N=10).
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

# ── FIXED ARCHITECTURAL CONSTANTS (never searched) ───────────────────────────
P_SHORT=0.060; P_LONG=0.180; THRESH_SHORT=5; THRESH_LONG=10; MEAN_N=8.4
P_LF=1.0; CP=0.55; MP=0.90; P_CHQOK=0.12; P_STUTTER=0.006
MU_LEN=8.4; SIGMA_LEN=3.0; P_MF=0.20; P_LF_MF=0.50; P_LL_MF=0.00
GAMMA=0.30; ALPHA=0.20; BETA_BASE=0.50
IDX_THRESH=2; SHORT_THRESH=2; TARGET_LINES=2411; WINDOW=20; SEED=574000
MAX_RETRY=10
LL_BASE=8; LL_SLOPE=0.30; LL_N_REF=5; LL_MIN_CAP=3
L_BASE=5.40; L_SLOPE=-0.053
SHORT_ONSETS={'d','s','y','k','t','l','r','p','f','o'}
EVA_CHARS=list('acdehiklmnoqrsty')
ONSET_ORDER=[
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o'),
]
SUFFIX_PATTERNS=['eedy','edy','aiin','ain','am','ey','ol','or','al','ar','dy']
SPARSE_ONSETS={'qok','ok','ot','qot'}
BATTERY_19=['am_ll','d_ll','y_lf','ss_mean','adj_rate','qok_lf','d_lf','s_lf',
            'ch_ll','ok_ll','qok_ll','ss_d','ss_y','am_lf_enr','am_mid_enr',
            'edy_rate','word_len_mean','qok_ch','global_am_rate']
PASS_TOL=0.20
# Real VMS B-dialect reference (for information only in this experiment)
VMS_REF_REAL={'am_ll':6.5498,'d_ll':1.3625,'y_lf':3.1837,'ss_mean':1.1640,
              'adj_rate':0.0090,'qok_lf':0.7450,'d_lf':2.1178,'s_lf':4.4422,
              'ch_ll':0.9653,'ok_ll':1.0028,'qok_ll':0.6121,'ss_d':1.5850,
              'ss_y':1.9550,'am_lf_enr':0.1225,'am_mid_enr':0.1954,
              'edy_rate':0.1940,'word_len_mean':5.4000,'qok_ch':1.2670,
              'global_am_rate':0.0203}

# ── GRID SEARCH PARAMETERS ───────────────────────────────────────────────────
GRID = {
    'beta_scale': [0.8, 1.2, 1.8, 2.5],
    'p_blind':    [0.0, 0.05, 0.115, 0.18],
    'r_lf':       [0.05, 0.12, 0.50, 1.0],
    'r_mid':      [0.10, 0.20, 0.50, 1.0],
    'p_qokch':    [0.05, 0.12, 0.20, 0.30],
}
N_FAST = 3    # trials per grid point (fast pass)
N_CONFIRM = 10  # trials for best combo confirmation

# ── HELPER FUNCTIONS ─────────────────────────────────────────────────────────

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
    if w.endswith('edy'): return 3
    return 0
def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total >= 0.05 else 'A'
def weighted_choice(rng, dist):
    r = rng.random(); cum = 0.0
    for k,v in dist.items():
        cum += v
        if r < cum: return k
    return list(dist.keys())[-1]

def parse_vms_b_lines():
    folio_word_stats = defaultdict(lambda: {'total':0,'edy':0,'eedy':0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
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

def build_midfix_dist(words):
    midfix_cnt = Counter()
    for w in words:
        onset = get_onset(w); suf = get_suffix(w)
        if onset == 'other' or suf == 'other': continue
        onset_len = get_onset_len(w); suf_len = len(suf)
        if (edy_len := get_edy_suffix_len(w)):
            mid_end = len(w)-edy_len; midfix = w[onset_len:mid_end]
            if len(midfix) >= 1: midfix = midfix[:-1]
        else:
            midfix = w[onset_len:len(w)-suf_len]
        midfix_cnt[midfix] += 1
    total = sum(midfix_cnt.values())
    if total == 0: return {}, 0.0
    p_non_empty = sum(v for k,v in midfix_cnt.items() if k != '')/total
    non_empty_raw = {mf:v for mf,v in midfix_cnt.items() if mf != ''}
    non_empty_total = sum(non_empty_raw.values())
    return {mf:v/non_empty_total for mf,v in non_empty_raw.items()} if non_empty_total else {}, p_non_empty

def compute_vms_dists(b_lines, p_blind):
    """Compute corpus distributions. d_boost depends on p_blind."""
    all_words = [w for l in b_lines for w in l]
    lf_words = [l[0] for l in b_lines if l]
    ll_words = [l[-1] for l in b_lines if len(l) > 1]
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
    def build_onset(words):
        cnt = Counter(get_onset(w) for w in words); cnt.pop('other', None)
        total = sum(cnt.values())
        return {k:v/total for k,v in cnt.items()} if total else {}
    def build_suffix(words):
        cnt = Counter(get_suffix(w) for w in words); total = sum(cnt.values())
        return {k:v/total for k,v in cnt.items()} if total else {}
    onset_lf = build_onset(lf_words); onset_ll = build_onset(ll_words)
    onset_mid = build_onset(mid_words); suffix_global = build_suffix(all_words)
    mid_nemed, mid_p = build_midfix_dist(mid_words)
    lf_nemed, lf_p = build_midfix_dist(lf_words)
    ll_nemed, ll_p = build_midfix_dist(ll_words)
    d_global = Counter(get_onset(w) for w in all_words).get('d',0)/len(all_words)
    ll_d = Counter(get_onset(w) for w in ll_words).get('d',0)/len(ll_words)
    d_ll_target = ll_d/d_global if d_global else 0
    d_ll_non_blind_enr = onset_ll.get('d',0)/d_global if d_global else 0
    if p_blind > 0:
        d_boost = d_global*(d_ll_target-(1-p_blind)*d_ll_non_blind_enr)/p_blind
        d_boost = max(0.0, min(d_boost, 1.0))
    else:
        d_boost = 0.0
    remaining = 1.0 - d_boost
    base = {o:v for o,v in onset_ll.items() if o != 'd'}
    base_total = sum(base.values())
    ll_onsets = {o:v/base_total*remaining for o,v in base.items()} if base_total else {}
    ll_onsets['d'] = d_boost
    return {'onset_lf':onset_lf, 'onset_ll':onset_ll, 'onset_mid':onset_mid,
            'suffix_global':suffix_global, 'mid_nemed':mid_nemed, 'lf_nemed':lf_nemed,
            'll_nemed':ll_nemed, 'll_onsets':ll_onsets, 'mid_words':mid_words, 'd_boost':d_boost}

def make_suppressed_suffix(sg, r_am):
    am_w = sg.get('am',0); new_am = am_w*r_am; delta = am_w-new_am; non_am = 1.0-am_w
    return {suf:(new_am if suf == 'am' else w+(w/non_am)*delta if non_am > 0 else w)
            for suf,w in sg.items()}

def make_word_sim(onset, suffix, rng, nemed, p_mf):
    midfix = ''
    if nemed and rng.random() < p_mf: midfix = weighted_choice(rng, nemed)
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset + midfix + rng.choice(['a','ai','o','oi','e','ei']) + suffix
    return onset + midfix + suffix

def apply_suffix_length_bias(suf_w, word_idx, beta):
    if beta == 0.0 or word_idx < IDX_THRESH: return suf_w
    new_w = {}
    for suf,w in suf_w.items():
        suf_len = len(suf) if suf != 'other' else 5
        penalty = max(0, suf_len-SHORT_THRESH)
        new_w[suf] = w*math.exp(-beta*penalty)
    total = sum(new_w.values())
    return {s:v/total for s,v in new_w.items()} if total > 0 else suf_w

def timm_modify(word, onset_mid, suffix_mid, rng):
    if not word: return word
    onset_len = get_onset_len(word); edy_len = get_edy_suffix_len(word)
    mod_start = onset_len; mod_end = len(word)-edy_len
    if mod_start >= mod_end:
        return make_word_sim(weighted_choice(rng,onset_mid), weighted_choice(rng,suffix_mid), rng, {}, 0.0)
    op = rng.choice(['replace','insert','delete'])
    if op == 'replace':
        pos = rng.randint(mod_start, mod_end-1)
        return word[:pos]+rng.choice(EVA_CHARS)+word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(mod_start, mod_end)
        return word[:pos]+rng.choice(EVA_CHARS)+word[pos:]
    else:
        if mod_end-mod_start <= 1:
            return word[:mod_start]+rng.choice(EVA_CHARS)+word[mod_start+1:]
        pos = rng.randint(mod_start, mod_end-1)
        return word[:pos]+word[pos+1:]

def clamp_to_lexicon(word, lexicons, rng):
    onset = get_onset(word)
    if onset in lexicons and lexicons[onset]: return rng.choice(lexicons[onset])
    return word

def build_full_vms_lexicons(mid_words, onset_classes):
    lexicons = {}; per_onset_counts = defaultdict(Counter)
    for w in mid_words:
        onset = get_onset(w)
        if onset in onset_classes: per_onset_counts[onset][w] += 1
    for onset in onset_classes:
        counts = per_onset_counts[onset]; lex_list = []
        for w,c in counts.items(): lex_list.extend([w]*c)
        lexicons[onset] = lex_list
    return lexicons

def get_p_blind_n(n, p_blind_base):
    """Scale p_blind by line length, same as exp_314 logic."""
    if n <= THRESH_SHORT: return P_SHORT * (p_blind_base / 0.115) if p_blind_base > 0 else 0.0
    if n >= THRESH_LONG: return P_LONG * (p_blind_base / 0.115) if p_blind_base > 0 else 0.0
    frac = (n-THRESH_SHORT)/(THRESH_LONG-THRESH_SHORT)
    base = P_SHORT + frac*(P_LONG-P_SHORT)
    return base * (p_blind_base / 0.115) if p_blind_base > 0 else 0.0

def get_max_ll_len(n):
    return max(LL_MIN_CAP, round(LL_BASE-LL_SLOPE*max(0, n-LL_N_REF)))

def draw_buf(buf, prev_onset, rng, word_idx, p_qokch):
    buf_list = list(buf)
    if not buf_list: return None
    preferred = None
    if prev_onset == 'qok' and rng.random() < p_qokch:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words: preferred = ch_words
    elif prev_onset == 'ch' and rng.random() < P_CHQOK:
        qok_words = [w for w in buf_list if get_onset(w) == 'qok']
        if qok_words: preferred = qok_words
    candidates = preferred if preferred else buf_list
    if GAMMA == 0.0: return rng.choice(candidates)
    L_target = L_BASE+L_SLOPE*word_idx
    weights = [math.exp(-GAMMA*(len(w)-L_target)**2) for w in candidates]
    total = sum(weights)
    if total == 0: return rng.choice(candidates)
    r = rng.random()*total; cum = 0.0
    for w,wt in zip(candidates, weights):
        cum += wt
        if r < cum: return w
    return candidates[-1]

def generate_ll_word(rng, vms_d, suffix_global, max_ll):
    candidates = []
    for _ in range(MAX_RETRY+1):
        onset = weighted_choice(rng, vms_d['onset_ll'])
        suf = weighted_choice(rng, suffix_global)
        ew = make_word_sim(onset, suf, rng, vms_d['ll_nemed'], P_LL_MF)
        if len(ew) <= max_ll: return ew
        candidates.append(ew)
    return min(candidates, key=len)

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

def run_sim(latin_words, vms_d, rng, n_trials, params):
    """Run 21-mechanism simulation with given distributions and parameters."""
    beta_scale = params['beta_scale']
    p_blind_base = params['p_blind']
    r_lf = params['r_lf']
    r_mid = params['r_mid']
    p_qokch = params['p_qokch']

    suffix_global = vms_d['suffix_global']
    suffix_lf_sup = make_suppressed_suffix(suffix_global, r_lf)
    suffix_mid_sup = make_suppressed_suffix(suffix_global, r_mid)
    lexicons = build_full_vms_lexicons(vms_d['mid_words'], SPARSE_ONSETS)
    all_lines = []
    for _ in range(n_trials):
        w = list(latin_words); rng.shuffle(w)
        lines = []; buf = deque(maxlen=WINDOW); pos = 0
        prev_onset = None; prev_word = None
        while len(lines) < TARGET_LINES and pos < len(w)-2:
            n = max(2, min(20, round(rng.gauss(MU_LEN, SIGMA_LEN))))
            chunk = w[pos:pos+n]
            if len(chunk) < 2: pos += len(chunk); continue
            line = []; word_idx = 0
            p_blind_n = get_p_blind_n(n, p_blind_base)
            max_ll = get_max_ll_len(n)
            beta_eff = BETA_BASE*beta_scale*(n/MEAN_N)
            for i, word in enumerate(chunk):
                if i == 0:
                    if rng.random() < P_LF:
                        onset = weighted_choice(rng, vms_d['onset_lf'])
                        suf = weighted_choice(rng, suffix_lf_sup)
                        ew = make_word_sim(onset, suf, rng, vms_d['lf_nemed'], P_LF_MF)
                    else:
                        onset = weighted_choice(rng, vms_d['onset_mid'])
                        suf = weighted_choice(rng, suffix_lf_sup)
                        ew = make_word_sim(onset, suf, rng, {}, 0.0)
                elif i == len(chunk)-1:
                    if rng.random() < p_blind_n:
                        onset = weighted_choice(rng, vms_d['ll_onsets'])
                        ew = onset+'am'
                    else:
                        ew = generate_ll_word(rng, vms_d, vms_d['suffix_global'], max_ll)
                else:
                    if prev_word is not None and rng.random() < P_STUTTER:
                        ew = prev_word
                    elif buf and rng.random() < CP:
                        src = draw_buf(buf, prev_onset, rng, word_idx, p_qokch)
                        if src is None: src = rng.choice(list(buf))
                        if rng.random() < MP:
                            ew = timm_modify(src, vms_d['onset_mid'], suffix_mid_sup, rng)
                            ew = clamp_to_lexicon(ew, lexicons, rng)
                        else:
                            ew = src
                    else:
                        new_ow = {o:v*(1+ALPHA*word_idx) if o in SHORT_ONSETS else v
                                  for o,v in vms_d['onset_mid'].items()}
                        tot = sum(new_ow.values())
                        norm = {o:v/tot for o,v in new_ow.items()} if tot else vms_d['onset_mid']
                        onset = weighted_choice(rng, norm)
                        biased_suf = apply_suffix_length_bias(suffix_mid_sup, word_idx, beta_eff)
                        suf = weighted_choice(rng, biased_suf)
                        ew = make_word_sim(onset, suf, rng, vms_d['mid_nemed'], P_MF)
                        ew = clamp_to_lexicon(ew, lexicons, rng)
                    buf.append(ew); word_idx += 1
                prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
            lines.append(line); pos += n
        all_lines.extend(lines[:TARGET_LINES])
    return all_lines

def compute_metrics(all_lines, n_trials):
    trial_size = TARGET_LINES; trial_metrics = []
    for t in range(n_trials):
        lines = all_lines[t*trial_size:(t+1)*trial_size]
        aw = [w for l in lines for w in l]; n_aw = len(aw)
        if n_aw < 100: continue
        lf = [l[0] for l in lines if l]
        ll = [l[-1] for l in lines if len(l) > 1]
        mid = [w for l in lines for w in l[1:-1] if len(l) > 2]
        oc_all = Counter(get_onset(w) for w in aw)
        oc_lf = Counter(get_onset(w) for w in lf)
        oc_ll = Counter(get_onset(w) for w in ll)
        n_lf = len(lf); n_ll = len(ll); n_mid = len(mid)
        def enr(onset, ctr, ns):
            s = ctr.get(onset,0)/ns if ns else 0
            g = oc_all.get(onset,0)/n_aw if n_aw else 0
            return s/g if g > 0 else 0
        am_r = sum(1 for w in aw if w.endswith('am'))/n_aw
        ll_am = sum(1 for w in ll if w.endswith('am'))/n_ll if n_ll else 0
        am_ll = ll_am/am_r if am_r else 0
        d_ll = enr('d', oc_ll, n_ll); y_lf = enr('y', oc_lf, n_lf)
        tb = n_aw-1
        bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
        def ss(o):
            b = oc_all.get(o,0)/n_aw
            return bg.get((o,o),0)/(tb*b*b) if b > 0 and tb > 0 else 1.0
        ss_mean = (ss('qok')+ss('ok')+ss('ch'))/3
        adj = sum(1 for i in range(tb) if aw[i] == aw[i+1])/max(1,tb)
        qok_lf = enr('qok', oc_lf, n_lf); d_lf = enr('d', oc_lf, n_lf)
        s_lf = enr('s', oc_lf, n_lf); ch_ll = enr('ch', oc_ll, n_ll)
        ok_ll = enr('ok', oc_ll, n_ll); qok_ll = enr('qok', oc_ll, n_ll)
        ss_d = ss('d'); ss_y = ss('y')
        lf_am_rate = sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf else 0
        mid_am_rate = sum(1 for w in mid if w.endswith('am'))/n_mid if n_mid else 0
        am_lf_enr = lf_am_rate/am_r if am_r else 0
        am_mid_enr = mid_am_rate/am_r if am_r else 0
        edy_rate = sum(1 for w in aw if w.endswith('edy') or w.endswith('eedy'))/n_aw
        word_len = sum(len(w) for w in aw)/n_aw
        qok_r = oc_all.get('qok',0)/n_aw; ch_r = oc_all.get('ch',0)/n_aw
        qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r and tb > 0 else 0
        metrics = {'am_ll':am_ll,'d_ll':d_ll,'y_lf':y_lf,'ss_mean':ss_mean,'adj_rate':adj,
                   'qok_lf':qok_lf,'d_lf':d_lf,'s_lf':s_lf,'ch_ll':ch_ll,'ok_ll':ok_ll,
                   'qok_ll':qok_ll,'ss_d':ss_d,'ss_y':ss_y,'am_lf_enr':am_lf_enr,
                   'am_mid_enr':am_mid_enr,'edy_rate':edy_rate,'word_len_mean':word_len,
                   'qok_ch':qok_ch,'global_am_rate':am_r}
        trial_metrics.append(metrics)
    return trial_metrics

def compute_corpus_metrics(lines):
    """Compute the 19 VMS metrics for a given corpus."""
    aw = [w for l in lines for w in l]; n_aw = len(aw)
    lf = [l[0] for l in lines if l]
    ll = [l[-1] for l in lines if len(l) > 1]
    mid = [w for l in lines for w in l[1:-1] if len(l) > 2]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf = Counter(get_onset(w) for w in lf)
    oc_ll = Counter(get_onset(w) for w in ll)
    n_lf = len(lf); n_ll = len(ll); n_mid = len(mid)
    def enr(onset, ctr, ns):
        s = ctr.get(onset,0)/ns if ns else 0
        g = oc_all.get(onset,0)/n_aw if n_aw else 0
        return s/g if g > 0 else 0
    am_r = sum(1 for w in aw if w.endswith('am'))/n_aw
    ll_am = sum(1 for w in ll if w.endswith('am'))/n_ll if n_ll else 0
    am_ll = ll_am/am_r if am_r else 0
    d_ll = enr('d', oc_ll, n_ll); y_lf = enr('y', oc_lf, n_lf)
    tb = n_aw-1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o,0)/n_aw
        return bg.get((o,o),0)/(tb*b*b) if b > 0 and tb > 0 else 1.0
    ss_mean = (ss('qok')+ss('ok')+ss('ch'))/3
    adj = sum(1 for i in range(tb) if aw[i] == aw[i+1])/max(1,tb)
    qok_lf = enr('qok', oc_lf, n_lf); d_lf = enr('d', oc_lf, n_lf)
    s_lf = enr('s', oc_lf, n_lf); ch_ll = enr('ch', oc_ll, n_ll)
    ok_ll = enr('ok', oc_ll, n_ll); qok_ll = enr('qok', oc_ll, n_ll)
    ss_d = ss('d'); ss_y = ss('y')
    lf_am_rate = sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf else 0
    mid_am_rate = sum(1 for w in mid if w.endswith('am'))/n_mid if n_mid else 0
    am_lf_enr = lf_am_rate/am_r if am_r else 0
    am_mid_enr = mid_am_rate/am_r if am_r else 0
    edy_rate = sum(1 for w in aw if w.endswith('edy') or w.endswith('eedy'))/n_aw
    word_len = sum(len(w) for w in aw)/n_aw
    qok_r = oc_all.get('qok',0)/n_aw; ch_r = oc_all.get('ch',0)/n_aw
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r and tb > 0 else 0
    return {'am_ll':am_ll,'d_ll':d_ll,'y_lf':y_lf,'ss_mean':ss_mean,'adj_rate':adj,
            'qok_lf':qok_lf,'d_lf':d_lf,'s_lf':s_lf,'ch_ll':ch_ll,'ok_ll':ok_ll,
            'qok_ll':qok_ll,'ss_d':ss_d,'ss_y':ss_y,'am_lf_enr':am_lf_enr,
            'am_mid_enr':am_mid_enr,'edy_rate':edy_rate,'word_len_mean':word_len,
            'qok_ch':qok_ch,'global_am_rate':am_r}

def count_pass_local(tms, local_ref):
    """Count passes against a LOCAL reference (the corpus's own metrics)."""
    def agg(k): return sum(m[k] for m in tms)/len(tms) if tms else 0
    passes = 0
    for k in BATTERY_19:
        v = agg(k); ref = local_ref[k]
        if ref > 0 and ref*(1-PASS_TOL) <= v <= ref*(1+PASS_TOL):
            passes += 1
        elif ref == 0 and v == 0:
            passes += 1
    return passes

def agg_metrics(tms):
    if not tms: return {}
    return {k: sum(m[k] for m in tms)/len(tms) for k in BATTERY_19}

def run_grid_search(latin_words, b_lines, local_ref, condition_label):
    """Grid search for best parameters matching local_ref."""
    print(f"\n{'='*70}")
    print(f"GRID SEARCH: {condition_label}")
    print(f"Local targets (this corpus's own metrics):")
    for k in BATTERY_19:
        print(f"  {k:<18} {local_ref[k]:.4f}")
    print(f"\nRunning {len(GRID['beta_scale'])*len(GRID['p_blind'])*len(GRID['r_lf'])*len(GRID['r_mid'])*len(GRID['p_qokch'])} grid points (N={N_FAST} each)...")

    best_pass = -1
    best_params = None
    best_tms = None
    grid_results = []

    total_combos = (len(GRID['beta_scale']) * len(GRID['p_blind']) *
                    len(GRID['r_lf']) * len(GRID['r_mid']) * len(GRID['p_qokch']))
    done = 0

    for beta_scale in GRID['beta_scale']:
        for p_blind in GRID['p_blind']:
            # Recompute vms_d with this p_blind (d_boost changes)
            vms_d = compute_vms_dists(b_lines, p_blind)
            for r_lf in GRID['r_lf']:
                for r_mid in GRID['r_mid']:
                    for p_qokch in GRID['p_qokch']:
                        params = {'beta_scale':beta_scale, 'p_blind':p_blind,
                                  'r_lf':r_lf, 'r_mid':r_mid, 'p_qokch':p_qokch}
                        rng = random.Random(SEED+200+done)
                        all_lines = run_sim(latin_words, vms_d, rng, N_FAST, params)
                        tms = compute_metrics(all_lines, N_FAST)
                        n_pass = count_pass_local(tms, local_ref)
                        grid_results.append((n_pass, params, tms))
                        if n_pass > best_pass:
                            best_pass = n_pass
                            best_params = params
                            best_tms = tms
                        done += 1
                        if done % 100 == 0:
                            print(f"  {done}/{total_combos} done, current best: {best_pass}/19")

    print(f"\nGrid search complete. Best: {best_pass}/19")
    print(f"Best params: {best_params}")

    # Show distribution of pass counts
    from collections import Counter as C2
    dist = C2(r[0] for r in grid_results)
    print(f"\nPass count distribution:")
    for cnt in sorted(dist.keys(), reverse=True)[:10]:
        print(f"  {cnt}/19: {dist[cnt]} combos")

    # Show top-5 candidates
    top5 = sorted(grid_results, key=lambda x: x[0], reverse=True)[:5]
    print(f"\nTop 5 parameter combinations:")
    for rank, (n_pass, params, tms) in enumerate(top5, 1):
        print(f"  #{rank}: {n_pass}/19 — {params}")

    # Confirm best with N=10
    print(f"\nConfirming best parameters at N={N_CONFIRM}...")
    vms_d_best = compute_vms_dists(b_lines, best_params['p_blind'])
    rng_confirm = random.Random(SEED+300)
    all_lines_confirm = run_sim(latin_words, vms_d_best, rng_confirm, N_CONFIRM, best_params)
    tms_confirm = compute_metrics(all_lines_confirm, N_CONFIRM)
    n_pass_confirm = count_pass_local(tms_confirm, local_ref)
    print(f"Confirmed: {n_pass_confirm}/19 PASS (N={N_CONFIRM})")

    # Detailed battery report vs local_ref
    print(f"\nDetailed battery ({condition_label}, best params, N={N_CONFIRM}):")
    print(f"{'Metric':<18} {'LocalRef':>9} {'SimVal':>9} {'%Ref':>7} {'Status':>6} {'VMS_Real':>9}")
    print("-"*70)
    agg = agg_metrics(tms_confirm)
    for k in BATTERY_19:
        ref = local_ref[k]; sim = agg[k]; vms_real = VMS_REF_REAL[k]
        pct = sim/ref*100 if ref > 0 else 0
        ok = ref*(1-PASS_TOL) <= sim <= ref*(1+PASS_TOL) if ref > 0 else (sim == 0)
        status = 'PASS' if ok else 'FAIL'
        print(f"{k:<18} {ref:>9.4f} {sim:>9.4f} {pct:>6.1f}% {status:>6} {vms_real:>9.4f}")

    # Which metrics fail?
    fail_list = []
    for k in BATTERY_19:
        ref = local_ref[k]; sim = agg[k]
        ok = ref*(1-PASS_TOL) <= sim <= ref*(1+PASS_TOL) if ref > 0 else (sim == 0)
        if not ok: fail_list.append((k, ref, sim))
    if fail_list:
        print(f"\nFailing metrics ({len(fail_list)} total):")
        for k, ref, sim in fail_list:
            direction = 'OVER' if sim > ref else 'UNDER'
            print(f"  {k}: target={ref:.4f}, sim={sim:.4f} ({direction})")
    else:
        print(f"\nAll 19 metrics PASS!")

    return n_pass_confirm, best_params, tms_confirm, local_ref

# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("exp_575: Architecture Refit to Shuffled Targets")
    print("="*70)
    print("Loading data...")
    b_lines_real = parse_vms_b_lines()
    print(f"B-dialect: {len(b_lines_real)} lines, {sum(len(l) for l in b_lines_real)} words")
    latin_words = load_latin(LATIN_CORPUS)
    print(f"Latin: {len(latin_words)} words")

    # Create shuffled corpora (identical seeds to exp_574 for reproducibility)
    rng_shuf1 = random.Random(SEED+1)
    b_lines_intra = [list(l) for l in b_lines_real]
    for l in b_lines_intra: rng_shuf1.shuffle(l)

    rng_shuf2 = random.Random(SEED+2)
    all_words_pool = [w for l in b_lines_real for w in l]
    rng_shuf2.shuffle(all_words_pool)
    line_lengths = [len(l) for l in b_lines_real]
    b_lines_inter = []; pos = 0
    for ln in line_lengths:
        b_lines_inter.append(all_words_pool[pos:pos+ln]); pos += ln

    # Compute local reference metrics for each corpus
    cm_real = compute_corpus_metrics(b_lines_real)
    cm_intra = compute_corpus_metrics(b_lines_intra)
    cm_inter = compute_corpus_metrics(b_lines_inter)

    print("\nCorpus metrics summary (to confirm correct shuffling):")
    print(f"{'Metric':<18} {'Real VMS':>10} {'Intra':>10} {'Inter':>10}")
    print("-"*50)
    for k in BATTERY_19:
        print(f"{k:<18} {cm_real[k]:>10.4f} {cm_intra[k]:>10.4f} {cm_inter[k]:>10.4f}")

    # Run grid search for each condition
    conditions = [
        ("Real B-dialect (POSITIVE CTRL)", b_lines_real, cm_real),
        ("Intra-shuffle (within-line)", b_lines_intra, cm_intra),
        ("Inter-shuffle (word-to-line)", b_lines_inter, cm_inter),
    ]

    results = []
    for label, b_lines, local_ref in conditions:
        n_pass, params, tms, ref = run_grid_search(latin_words, b_lines, local_ref, label)
        results.append((label, n_pass, params, tms, ref))

    # ── DECISIVE SUMMARY ─────────────────────────────────────────────────────
    print("\n\n" + "="*70)
    print("DECISIVE SUMMARY: Can the architecture fit shuffled targets?")
    print("="*70)
    print(f"{'Condition':<40} {'Pass':>4}  {'Interpretation'}")
    print("-"*70)
    for label, n_pass, params, tms, ref in results:
        if n_pass >= 17:
            interp = "NEAR-PERFECT FIT — architecture is too flexible"
        elif n_pass >= 14:
            interp = "HIGH FIT — possible over-parameterization"
        elif n_pass >= 10:
            interp = "PARTIAL FIT — some structural incompatibility"
        else:
            interp = "POOR FIT — strong structural specificity"
        print(f"{label:<40} {n_pass:>4}  {interp}")

    # Report on the decisive question
    real_pass = results[0][1]
    intra_pass = results[1][1]
    inter_pass = results[2][1]
    print(f"\n{'DECISIVE QUESTION ANSWER':}")
    print(f"Real VMS (best case): {real_pass}/19")
    print(f"Intra-shuffle (best fit to shuffled): {intra_pass}/19")
    print(f"Inter-shuffle (best fit to shuffled): {inter_pass}/19")
    print()
    if intra_pass >= 17 or inter_pass >= 17:
        print("CONCLUSION: Architecture DOES achieve near-19/19 on shuffled targets.")
        print("The 6 free parameters are sufficient to fit arbitrary corpus structure.")
        print("The real-VMS 19/19 is primarily about parameter flexibility.")
        print("This WEAKENS the architectural specificity claim.")
    elif intra_pass >= 14 or inter_pass >= 14:
        print("CONCLUSION: Architecture achieves HIGH but not perfect fit on shuffled.")
        print("Moderate over-parameterization possible. Structural incompatibilities exist.")
        print("The 19/19 on real VMS is partly but not solely parameter flexibility.")
    else:
        print("CONCLUSION: Architecture CANNOT achieve near-19/19 on shuffled targets.")
        print("Hard structural impossibilities prevent the architecture from fitting")
        print("arbitrary corpus metrics regardless of parameter choice.")
        print("The real-VMS 19/19 reflects genuine structural specificity.")

    # Identify structurally impossible metrics (fail in all shuffled conditions)
    agg_intra = agg_metrics(results[1][3])
    agg_inter = agg_metrics(results[2][3])
    ref_intra = results[1][4]
    ref_inter = results[2][4]
    structurally_impossible = []
    for k in BATTERY_19:
        ri = ref_intra[k]; si = agg_intra[k]
        ro = ref_inter[k]; so = agg_inter[k]
        fail_intra = not (ri*(1-PASS_TOL) <= si <= ri*(1+PASS_TOL)) if ri > 0 else False
        fail_inter = not (ro*(1-PASS_TOL) <= so <= ro*(1+PASS_TOL)) if ro > 0 else False
        if fail_intra and fail_inter:
            structurally_impossible.append((k, ri, si, ro, so))
    if structurally_impossible:
        print(f"\nMetrics failing in BOTH shuffled conditions (structural impossibilities):")
        for k, ri, si, ro, so in structurally_impossible:
            print(f"  {k}: intra_target={ri:.4f}, sim={si:.4f} | inter_target={ro:.4f}, sim={so:.4f}")
    else:
        print(f"\nNo metrics fail in both shuffled conditions (full flexibility)")

if __name__ == '__main__':
    main()
