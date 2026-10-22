"""
exp_576: Architecture Parameter Stability — Corpus Split Cross-Validation

The 21-mechanism architecture (exp_314) was calibrated on the full B-dialect corpus.
This experiment tests whether the 6 calibrated parameters are STABLE PROPERTIES of
B-dialect (same values emerge regardless of which portion of the corpus you use) or
CORPUS-FIT ARTIFACTS (values drift substantially across different corpus splits).

DESIGN: Three independent split schemes, each 50/50:
1. ODD/EVEN folio split — interleaved folios, geographically distributed
2. FIRST/SECOND half split — folios in document order, tests section consistency
3. RANDOM 50/50 split — no systematic bias (SEED=576000)

For each split:
- Run independent grid search on EACH HALF against that half's own VMS metrics
- Compare best parameters found on each half
- Test cross-validation: fit on half-A, evaluate on half-B (and vice versa)
- Parameter stability metric: absolute difference in best parameter values

INTERPRETATION:
- Stable parameters: same best values emerge from both halves independently
  → The parameters are structural properties of B-dialect, not corpus-size artifacts
  → Cross-validation should maintain high pass count (≥ 16/19)
- Unstable parameters: best values differ substantially between halves
  → The calibration is corpus-specific
  → Cross-validation degrades significantly (< 14/19)

Grid: beta_scale[4] x p_blind[4] x r_lf[4] x r_mid[4] x p_qokch[4] = 1024 combos
N=3 (fast), N=10 (confirm best). Cross-validation at N=10.
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

# ── FIXED ARCHITECTURAL CONSTANTS ────────────────────────────────────────────
P_SHORT=0.060; P_LONG=0.180; THRESH_SHORT=5; THRESH_LONG=10; MEAN_N=8.4
P_LF=1.0; CP=0.55; MP=0.90; P_CHQOK=0.12; P_STUTTER=0.006
MU_LEN=8.4; SIGMA_LEN=3.0; P_MF=0.20; P_LF_MF=0.50; P_LL_MF=0.00
GAMMA=0.30; ALPHA=0.20; BETA_BASE=0.50
IDX_THRESH=2; SHORT_THRESH=2; TARGET_LINES=1200; WINDOW=20; SEED=576000
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
# Full-corpus VMS_REF (from exp_314/exp_575)
VMS_REF_FULL={'am_ll':6.5498,'d_ll':1.3625,'y_lf':3.1837,'ss_mean':1.1640,
              'adj_rate':0.0090,'qok_lf':0.7450,'d_lf':2.1178,'s_lf':4.4422,
              'ch_ll':0.9653,'ok_ll':1.0028,'qok_ll':0.6121,'ss_d':1.5850,
              'ss_y':1.9550,'am_lf_enr':0.1225,'am_mid_enr':0.1954,
              'edy_rate':0.1940,'word_len_mean':5.4000,'qok_ch':1.2670,
              'global_am_rate':0.0203}
# Exp_314 reference parameters
EXP314_PARAMS = {'beta_scale':1.8, 'p_blind':0.115, 'r_lf':0.12, 'r_mid':0.20, 'p_qokch':0.12}

# ── GRID ─────────────────────────────────────────────────────────────────────
GRID = {
    'beta_scale': [0.8, 1.2, 1.8, 2.5],
    'p_blind':    [0.0, 0.05, 0.115, 0.18],
    'r_lf':       [0.05, 0.12, 0.50, 1.0],
    'r_mid':      [0.10, 0.20, 0.50, 1.0],
    'p_qokch':    [0.05, 0.12, 0.20, 0.30],
}
N_FAST = 3
N_CONFIRM = 10

# ── HELPERS ──────────────────────────────────────────────────────────────────

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

def parse_vms_b_lines_with_folios():
    """Parse B-dialect VMS lines, returning (lines, folio_labels) for splitting."""
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
    b_lines = []; folio_labels = []
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
            if words:
                b_lines.append(words)
                folio_labels.append(fb)
    return b_lines, folio_labels

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
    ll_d = Counter(get_onset(w) for w in ll_words).get('d',0)/len(ll_words) if ll_words else 0
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
    if p_blind_base == 0: return 0.0
    if n <= THRESH_SHORT: return P_SHORT * (p_blind_base / 0.115)
    if n >= THRESH_LONG: return P_LONG * (p_blind_base / 0.115)
    frac = (n-THRESH_SHORT)/(THRESH_LONG-THRESH_SHORT)
    base = P_SHORT + frac*(P_LONG-P_SHORT)
    return base * (p_blind_base / 0.115)

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

def run_sim(latin_words, vms_d, rng, n_trials, params, target_lines=None):
    if target_lines is None: target_lines = TARGET_LINES
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
        while len(lines) < target_lines and pos < len(w)-2:
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
        all_lines.extend(lines[:target_lines])
    return all_lines

def compute_metrics(all_lines, n_trials, target_lines=None):
    if target_lines is None: target_lines = TARGET_LINES
    trial_size = target_lines; trial_metrics = []
    for t in range(n_trials):
        lines = all_lines[t*trial_size:(t+1)*trial_size]
        aw = [w for l in lines for w in l]; n_aw = len(aw)
        if n_aw < 50: continue
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
    aw = [w for l in lines for w in l]; n_aw = len(aw)
    if n_aw < 50: return {k: 0.0 for k in BATTERY_19}
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

def agg_metrics(tms):
    if not tms: return {}
    return {k: sum(m[k] for m in tms)/len(tms) for k in BATTERY_19}

def count_pass_local(tms, local_ref):
    def agg(k): return sum(m[k] for m in tms)/len(tms) if tms else 0
    passes = 0
    for k in BATTERY_19:
        v = agg(k); ref = local_ref[k]
        if ref > 0 and ref*(1-PASS_TOL) <= v <= ref*(1+PASS_TOL):
            passes += 1
        elif ref == 0 and v < 0.001:
            passes += 1
    return passes

def grid_search(latin_words, b_lines, local_ref, label, seed_offset, n_fast=N_FAST):
    """Run grid search and return best params + pass count."""
    best_pass = -1; best_params = None; done = 0
    total_combos = 4**5
    for beta_scale in GRID['beta_scale']:
        for p_blind in GRID['p_blind']:
            vms_d = compute_vms_dists(b_lines, p_blind)
            for r_lf in GRID['r_lf']:
                for r_mid in GRID['r_mid']:
                    for p_qokch in GRID['p_qokch']:
                        params = {'beta_scale':beta_scale, 'p_blind':p_blind,
                                  'r_lf':r_lf, 'r_mid':r_mid, 'p_qokch':p_qokch}
                        rng = random.Random(seed_offset + done)
                        all_lines = run_sim(latin_words, vms_d, rng, n_fast, params, TARGET_LINES)
                        tms = compute_metrics(all_lines, n_fast, TARGET_LINES)
                        n_pass = count_pass_local(tms, local_ref)
                        if n_pass > best_pass:
                            best_pass = n_pass; best_params = params
                        done += 1
                        if done % 200 == 0:
                            print(f"  [{label}] {done}/{total_combos} done, best: {best_pass}/19")
    # Confirm at N=10
    vms_d_best = compute_vms_dists(b_lines, best_params['p_blind'])
    rng_c = random.Random(seed_offset + 9999)
    all_lines_c = run_sim(latin_words, vms_d_best, rng_c, N_CONFIRM, best_params, TARGET_LINES)
    tms_c = compute_metrics(all_lines_c, N_CONFIRM, TARGET_LINES)
    n_pass_c = count_pass_local(tms_c, local_ref)
    print(f"  [{label}] Best: {n_pass_c}/19 at {best_params}")
    return best_params, n_pass_c, tms_c

def cross_validate(latin_words, b_lines_train, local_ref_test, best_params, label, seed_offset):
    """Evaluate best_params from training half on test half's metrics."""
    vms_d = compute_vms_dists(b_lines_train, best_params['p_blind'])
    rng = random.Random(seed_offset)
    all_lines = run_sim(latin_words, vms_d, rng, N_CONFIRM, best_params, TARGET_LINES)
    tms = compute_metrics(all_lines, N_CONFIRM, TARGET_LINES)
    n_pass = count_pass_local(tms, local_ref_test)
    print(f"  [{label}] Cross-val: {n_pass}/19 (trained on A half, evaluated on B half's metrics)")
    return n_pass, tms

def print_split_report(split_name, halves, results, xval_results):
    """Print detailed comparison for a split scheme."""
    half_a_label, half_b_label = halves
    (params_a, pass_a, tms_a), (params_b, pass_b, tms_b) = results
    (xval_ab, tms_ab), (xval_ba, tms_ba) = xval_results
    print(f"\n{'='*70}")
    print(f"SPLIT: {split_name}")
    print(f"{'='*70}")
    print(f"\nBest parameters found independently per half:")
    print(f"{'Parameter':<15} {'Half-A':>10} {'Half-B':>10} {'Exp314':>10} {'|A-B|':>8} {'Stable?':>8}")
    print("-"*65)
    param_keys = list(EXP314_PARAMS.keys())
    for k in param_keys:
        va = params_a[k]; vb = params_b[k]; vref = EXP314_PARAMS[k]
        diff = abs(va - vb)
        stable = 'YES' if diff == 0 else ('near' if diff <= 0.07 else 'NO')
        print(f"{k:<15} {va:>10.4f} {vb:>10.4f} {vref:>10.4f} {diff:>8.4f} {stable:>8}")
    print(f"\nPass counts:")
    print(f"  Half-A (fit + eval on A): {pass_a}/19")
    print(f"  Half-B (fit + eval on B): {pass_b}/19")
    print(f"  Cross-val A→B (A params, B metrics): {xval_ab}/19")
    print(f"  Cross-val B→A (B params, A metrics): {xval_ba}/19")
    print(f"\nCross-validation degradation: {max(pass_a,pass_b)} → {min(xval_ab,xval_ba)} (worst case)")

def summarize_splits(all_split_results):
    print(f"\n\n{'='*70}")
    print(f"PARAMETER STABILITY SUMMARY")
    print(f"{'='*70}")
    print(f"\nFor each parameter: how often does it match across halves?")
    print(f"{'Parameter':<15}", end='')
    for split_name, _, results, _ in all_split_results:
        print(f" {split_name[:12]:>13}", end='')
    print()
    print("-"*70)
    param_keys = list(EXP314_PARAMS.keys())
    for k in param_keys:
        print(f"{k:<15}", end='')
        for split_name, _, results, _ in all_split_results:
            (params_a, _, _), (params_b, _, _) = results
            diff = abs(params_a[k] - params_b[k])
            stable = 'SAME' if diff == 0 else (f'Δ{diff:.3f}' if diff <= 0.07 else f'DRIFT{diff:.3f}')
            print(f" {stable:>13}", end='')
        print()

    print(f"\nFor each split: cross-validation pass counts")
    print(f"{'Split':<20} {'A-fit':>8} {'B-fit':>8} {'A→B':>8} {'B→A':>8} {'Worst CV':>10}")
    print("-"*60)
    for split_name, _, results, xval_results in all_split_results:
        (params_a, pass_a, _), (params_b, pass_b, _) = results
        (xval_ab, _), (xval_ba, _) = xval_results
        worst_cv = min(xval_ab, xval_ba)
        print(f"{split_name:<20} {pass_a:>8} {pass_b:>8} {xval_ab:>8} {xval_ba:>8} {worst_cv:>10}")

    print(f"\nInterpretation:")
    all_xval = []
    for split_name, _, results, xval_results in all_split_results:
        (xval_ab, _), (xval_ba, _) = xval_results
        all_xval.extend([xval_ab, xval_ba])
    mean_xval = sum(all_xval)/len(all_xval)
    worst_xval = min(all_xval)
    print(f"  Mean cross-validation pass count: {mean_xval:.1f}/19")
    print(f"  Worst cross-validation pass count: {worst_xval}/19")
    if worst_xval >= 16:
        print(f"  CONCLUSION: Parameters are STABLE — high cross-validation performance.")
        print(f"  The 6 parameters are structural properties of B-dialect, not corpus-size artifacts.")
    elif worst_xval >= 13:
        print(f"  CONCLUSION: Parameters are MODERATELY stable — acceptable cross-validation.")
        print(f"  Some parameters may be corpus-sensitive; key parameters stable.")
    else:
        print(f"  CONCLUSION: Parameters are UNSTABLE — poor cross-validation.")
        print(f"  Calibration is corpus-specific, not a stable B-dialect property.")

# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("exp_576: Parameter Stability — Corpus Split Cross-Validation")
    print("="*70)
    print("Loading data...")
    b_lines_all, folio_labels = parse_vms_b_lines_with_folios()
    n_lines = len(b_lines_all)
    print(f"B-dialect: {n_lines} lines, {sum(len(l) for l in b_lines_all)} words")
    latin_words = load_latin(LATIN_CORPUS)
    print(f"Latin: {len(latin_words)} words")

    # ── SPLIT SCHEMES ─────────────────────────────────────────────────────
    # 1. Odd/even folio split
    unique_folios = list(dict.fromkeys(folio_labels))
    odd_folios = set(unique_folios[1::2])
    even_folios = set(unique_folios[0::2])
    b_lines_odd = [l for l, fb in zip(b_lines_all, folio_labels) if fb in odd_folios]
    b_lines_even = [l for l, fb in zip(b_lines_all, folio_labels) if fb in even_folios]

    # 2. First/second half (by document order)
    mid = n_lines // 2
    b_lines_first = b_lines_all[:mid]
    b_lines_second = b_lines_all[mid:]

    # 3. Random 50/50 split
    rng_split = random.Random(SEED)
    indices = list(range(n_lines)); rng_split.shuffle(indices)
    rand_a_idx = set(indices[:n_lines//2])
    b_lines_rand_a = [b_lines_all[i] for i in range(n_lines) if i in rand_a_idx]
    b_lines_rand_b = [b_lines_all[i] for i in range(n_lines) if i not in rand_a_idx]

    print(f"\nSplit sizes:")
    print(f"  Odd folios: {len(b_lines_odd)} lines | Even folios: {len(b_lines_even)} lines")
    print(f"  First half: {len(b_lines_first)} lines | Second half: {len(b_lines_second)} lines")
    print(f"  Random A:   {len(b_lines_rand_a)} lines | Random B:   {len(b_lines_rand_b)} lines")

    # Compute corpus metrics for each half
    cm_odd = compute_corpus_metrics(b_lines_odd)
    cm_even = compute_corpus_metrics(b_lines_even)
    cm_first = compute_corpus_metrics(b_lines_first)
    cm_second = compute_corpus_metrics(b_lines_second)
    cm_rand_a = compute_corpus_metrics(b_lines_rand_a)
    cm_rand_b = compute_corpus_metrics(b_lines_rand_b)

    print(f"\nKey corpus metrics across splits (to verify similarity of halves):")
    print(f"{'Metric':<16} {'Full':>7} {'Odd':>7} {'Even':>7} {'First':>7} {'Second':>7} {'RandA':>7} {'RandB':>7}")
    for k in ['am_ll','y_lf','ss_mean','adj_rate','ss_y','edy_rate']:
        print(f"{k:<16} {VMS_REF_FULL[k]:>7.3f} {cm_odd[k]:>7.3f} {cm_even[k]:>7.3f} "
              f"{cm_first[k]:>7.3f} {cm_second[k]:>7.3f} {cm_rand_a[k]:>7.3f} {cm_rand_b[k]:>7.3f}")

    # ── GRID SEARCHES ────────────────────────────────────────────────────
    all_split_results = []
    splits_config = [
        ("ODD/EVEN", (b_lines_odd, cm_odd, "Odd"), (b_lines_even, cm_even, "Even"), 1000),
        ("FIRST/SECOND", (b_lines_first, cm_first, "First"), (b_lines_second, cm_second, "Second"), 2000),
        ("RANDOM", (b_lines_rand_a, cm_rand_a, "RandA"), (b_lines_rand_b, cm_rand_b, "RandB"), 3000),
    ]

    for split_name, (lines_a, cm_a, label_a), (lines_b, cm_b, label_b), base_seed in splits_config:
        print(f"\n{'─'*70}")
        print(f"RUNNING SPLIT: {split_name}")
        print(f"{'─'*70}")
        print(f"Grid search on {label_a} half (N={N_FAST} fast, N={N_CONFIRM} confirm)...")
        params_a, pass_a, tms_a = grid_search(latin_words, lines_a, cm_a, label_a, base_seed)
        print(f"Grid search on {label_b} half (N={N_FAST} fast, N={N_CONFIRM} confirm)...")
        params_b, pass_b, tms_b = grid_search(latin_words, lines_b, cm_b, label_b, base_seed+500)
        results = (params_a, pass_a, tms_a), (params_b, pass_b, tms_b)

        # Cross-validation: A params on B metrics, B params on A metrics
        print(f"Cross-validating A→B (A params, B's corpus, B's metrics as target)...")
        xval_ab, tms_xval_ab = cross_validate(latin_words, lines_a, cm_b, params_a, f"{label_a}→{label_b}", base_seed+700)
        print(f"Cross-validating B→A (B params, B's corpus, A's metrics as target)...")
        xval_ba, tms_xval_ba = cross_validate(latin_words, lines_b, cm_a, params_b, f"{label_b}→{label_a}", base_seed+800)
        xval_results = (xval_ab, tms_xval_ab), (xval_ba, tms_xval_ba)

        all_split_results.append((split_name, (label_a, label_b), results, xval_results))
        print_split_report(split_name, (label_a, label_b), results, xval_results)

    summarize_splits(all_split_results)

if __name__ == '__main__':
    main()
