"""
exp_303: Finite Vocabulary Pool for Sparse-Midfix Onset Classes (H505)

H505: Restricting the qok/ok/ot/qot MID vocabulary to a finite lexicon of N canonical
types (drawn from VMS B-dialect MID frequency) will reduce CP90 over-production from
17× toward 1× while maintaining 19/19 PASS.

Approach: "Vocabulary clamping" — after generating a MID word by any path (copy,
modified, cipher), if its onset is in SPARSE_ONSETS = {qok, ok, ot, qot}, replace it
with a draw from a pre-built finite lexicon (weighted by empirical VMS frequency).
Clamp is applied before inserting into the buffer, so the buffer only contains
lexicon words for sparse-onset classes.

This prevents vocabulary explosion from modification and cipher paths while
preserving all positional, suffix, and onset grammar structure.

Conditions tested:
  N=None  — baseline (no clamping) — should reproduce exp_302 ratios
  N=50    — qok lexicon 50 types; proportionally scaled: ok=107, ot=140, qot=78
  N=100   — qok lexicon 100 types; ok=213, ot=280 (but capped at total types)
  N=32    — exactly VMS CP90 target for qok; ok=45 (67/32×32=67), ot=56
  N_qok=32_all — clamp ALL onset classes to their VMS CP90 target size

Architecture: exp_301/302 (R_MID=0.20, beta=0.30, 16 mechanisms).
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_FULL   = 20
TARGET_LINES = 2411
WINDOW   = 20
SEED     = 303000

P_BLIND   = 0.115; P_LF    = 1.0;   CP       = 0.55; MP       = 0.90
P_QOKCH   = 0.12;  P_CHQOK = 0.12;  P_STUTTER = 0.006
R_LF      = 0.12;  R_MID   = 0.20;  MU_LEN   = 8.4;  SIGMA_LEN = 3.0
P_MF      = 0.20; P_LF_MF = 0.50; P_LL_MF = 0.00
GAMMA     = 0.30; ALPHA    = 0.20;  BETA     = 0.30
IDX_THRESH = 2;   SHORT_THRESH = 2

L_BASE  = 5.40; L_SLOPE = -0.053
SHORT_ONSETS = {'d', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'o'}
EVA_CHARS = list('acdehiklmnoqrsty')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']

# Sparse-midfix onset classes where VMS has concentrated paradigms
SPARSE_ONSETS = {'qok', 'ok', 'ot', 'qot'}

# VMS target closed paradigm sizes (from exp_302/F304)
VMS_CP90 = {
    'qok': (32, 150),   # (n90 types for 90%, total_mid_types)
    'ok':  (67, 151),
    'ot':  (83, 156),
    'sh':  (145, 275),
    'ch':  (284, 467),
    'qot': (46, 88),
    'd':   (149, 150),
}

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
    if w.endswith('edy'):  return 3
    return 0
def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

def parse_vms_b():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
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
            folio = m.group(1).lstrip('+*=&~'); fb = folio_base(folio)
            if folio_dialect.get(fb, 'unknown') != 'B': continue
            lc = m.group(3).lstrip('+*=/~&')
            if not lc.lstrip('@').startswith('P'): continue
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
        edy_len = get_edy_suffix_len(w)
        if edy_len:
            mid_end = len(w) - edy_len
            midfix = w[onset_len:mid_end]
            if len(midfix) >= 1: midfix = midfix[:-1]
        else:
            midfix = w[onset_len:len(w)-suf_len]
        midfix_cnt[midfix] += 1
    total = sum(midfix_cnt.values())
    if total == 0: return {}, 0.0
    p_ne = sum(v for k, v in midfix_cnt.items() if k != '') / total
    ne = {mf: v for mf, v in midfix_cnt.items() if mf != ''}
    nt = sum(ne.values())
    return ({mf: v/nt for mf, v in ne.items()} if nt else {}), p_ne

def compute_vms_distributions(b_lines):
    all_words = [w for l in b_lines for w in l]
    lf_words  = [l[0]  for l in b_lines if l]
    ll_words  = [l[-1] for l in b_lines if len(l) > 1]
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words)
    def build_onset(words):
        cnt = Counter(get_onset(w) for w in words); cnt.pop('other', None)
        total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}
    def build_suffix(words):
        cnt = Counter(get_suffix(w) for w in words); total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}
    onset_global = build_onset(all_words); onset_lf = build_onset(lf_words)
    onset_ll = build_onset(ll_words); onset_mid = build_onset(mid_words)
    suffix_global = build_suffix(all_words)
    suffix_lf = build_suffix(lf_words); suffix_mid = build_suffix(mid_words)
    mid_nemed, mid_p = build_midfix_dist(mid_words)
    lf_nemed,  lf_p  = build_midfix_dist(lf_words)
    ll_nemed,  ll_p  = build_midfix_dist(ll_words)
    am_r  = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words)
    d_r   = Counter(get_onset(w) for w in all_words).get('d', 0) / n
    ll_d  = Counter(get_onset(w) for w in ll_words).get('d', 0) / len(ll_words)
    edy_r = sum(1 for w in all_words if w.endswith('edy') or w.endswith('eedy')) / n
    return {
        'onset_global': onset_global, 'onset_lf': onset_lf,
        'onset_ll': onset_ll, 'onset_mid': onset_mid,
        'suffix_global': suffix_global, 'suffix_lf': suffix_lf, 'suffix_mid': suffix_mid,
        'mid_nemed': mid_nemed, 'mid_p': mid_p,
        'lf_nemed': lf_nemed, 'lf_p': lf_p,
        'll_nemed': ll_nemed, 'll_p': ll_p,
        'am_r': am_r, 'am_ll_target': ll_am/am_r if am_r else 0,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words), 'n_mid': len(mid_words),
        'edy_r': edy_r,
        'mid_words': mid_words,
    }

def build_per_onset_lexicons(mid_words, clamp_n_map):
    """Build per-onset frequency-weighted lexicons from VMS MID words.
    clamp_n_map: dict of onset -> N (max lexicon size). None = no limit.
    Returns: dict of onset -> list of words (with repetitions for weighted sampling)
    """
    lexicons = {}
    per_onset_counts = defaultdict(Counter)
    for w in mid_words:
        onset = get_onset(w)
        if onset in clamp_n_map:
            per_onset_counts[onset][w] += 1
    for onset, n_max in clamp_n_map.items():
        counts = per_onset_counts[onset]
        if not counts:
            lexicons[onset] = []
            continue
        if n_max is None:
            # No limit — use all types
            top_types = list(counts.keys())
        else:
            # Top-N types by frequency
            top_types = [w for w, _ in counts.most_common(n_max)]
        # Build weighted list for sampling (proportional to frequency within lexicon)
        lex_list = []
        for w in top_types:
            lex_list.extend([w] * counts[w])
        lexicons[onset] = lex_list
    return lexicons

def compute_d_boost(d_global, d_ll_target, d_ll_non_blind_enr, p_blind):
    return d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind_enr) / p_blind

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    remaining = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o != 'd'}
    base_total = sum(base.values())
    norm = {o: v/base_total * remaining for o, v in base.items()} if base_total else {}
    norm['d'] = d_boost_weight; return norm

def weighted_choice(rng, dist):
    r = rng.random(); cum = 0.0
    for k, v in dist.items():
        cum += v
        if r < cum: return k
    return list(dist.keys())[-1]

def sample_midfix(rng, non_empty_dist, p_non_empty):
    if non_empty_dist and rng.random() < p_non_empty:
        return weighted_choice(rng, non_empty_dist)
    return ''

def make_word_sim(onset, suffix, rng, non_empty_midfix_dist, p_midfix_present):
    if suffix == 'other': return onset + suffix
    midfix = sample_midfix(rng, non_empty_midfix_dist, p_midfix_present)
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
        return onset + midfix + connector + suffix
    return onset + midfix + suffix

def make_suppressed_suffix(suffix_global, r_am):
    am_w = suffix_global.get('am', 0); new_am = am_w * r_am
    delta = am_w - new_am; non_am = 1.0 - am_w
    return {suf: (new_am if suf=='am' else w + (w/non_am)*delta if non_am>0 else w)
            for suf, w in suffix_global.items()}

def apply_suffix_length_bias(suffix_weights, word_idx, beta):
    if beta == 0.0 or word_idx < IDX_THRESH:
        return suffix_weights
    new_w = {}
    for suf, w in suffix_weights.items():
        suf_len = len(suf) if suf != 'other' else 5
        penalty = max(0, suf_len - SHORT_THRESH)
        new_w[suf] = w * math.exp(-beta * penalty)
    total = sum(new_w.values())
    return {s: v/total for s, v in new_w.items()} if total > 0 else suffix_weights

def random_eva_word_onset_biased(onset_weights, suffix_weights, rng, non_empty_midfix_dist,
                                  p_midfix_present, word_idx, alpha, beta):
    if alpha == 0.0:
        norm = onset_weights
    else:
        new_weights = {o: w*(1+alpha*word_idx) if o in SHORT_ONSETS else w
                       for o, w in onset_weights.items()}
        total = sum(new_weights.values())
        norm = {o: w/total for o, w in new_weights.items()}
    onset = weighted_choice(rng, norm)
    biased_suf = apply_suffix_length_bias(suffix_weights, word_idx, beta)
    suffix = weighted_choice(rng, biased_suf)
    return make_word_sim(onset, suffix, rng, non_empty_midfix_dist, p_midfix_present)

def cipher_ll(onset_ll_vms, ll_onsets, suffix_global, p_blind, rng, ll_nemed):
    if rng.random() < p_blind:
        onset = weighted_choice(rng, ll_onsets)
        return onset + 'am'
    onset  = weighted_choice(rng, onset_ll_vms)
    suffix = weighted_choice(rng, suffix_global)
    return make_word_sim(onset, suffix, rng, ll_nemed, P_LL_MF)

def cipher_lf(onset_mid, onset_lf_vms, suffix_lf, p_lf, rng, lf_nemed):
    if rng.random() < p_lf:
        onset  = weighted_choice(rng, onset_lf_vms)
        suffix = weighted_choice(rng, suffix_lf)
        return make_word_sim(onset, suffix, rng, lf_nemed, P_LF_MF)
    return random_eva_word_onset_biased(onset_mid, suffix_lf, rng, {}, 0.0, 0, 0.0, 0.0)

def timm_modify(word, onset_mid, suffix_mid, rng):
    if not word: return word
    onset_len = get_onset_len(word); edy_len = get_edy_suffix_len(word)
    mod_start = onset_len; mod_end = len(word) - edy_len
    if mod_start >= mod_end:
        return random_eva_word_onset_biased(onset_mid, suffix_mid, rng, {}, 0.0, 0, 0.0, 0.0)
    op = rng.choice(['replace', 'insert', 'delete'])
    if op == 'replace':
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(mod_start, mod_end)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:
        if mod_end - mod_start <= 1:
            return word[:mod_start] + rng.choice(EVA_CHARS) + word[mod_start+1:]
        pos = rng.randint(mod_start, mod_end - 1)
        return word[:pos] + word[pos+1:]

def clamp_to_lexicon(word, lexicons, rng):
    """If word's onset has a lexicon, clamp it to the lexicon (draw by frequency weight)."""
    onset = get_onset(word)
    if onset not in lexicons or not lexicons[onset]:
        return word
    return rng.choice(lexicons[onset])

def draw_buf_length_biased(buf, prev_onset, p_qokch, p_chqok, rng, word_idx, gamma):
    buf_list = list(buf)
    if not buf_list: return None
    preferred = None
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words: preferred = ch_words
    elif prev_onset == 'ch' and p_chqok > 0 and rng.random() < p_chqok:
        qok_words = [w for w in buf_list if get_onset(w) == 'qok']
        if qok_words: preferred = qok_words
    candidates = preferred if preferred else buf_list
    if gamma == 0.0: return rng.choice(candidates)
    L_target = L_BASE + L_SLOPE * word_idx
    weights = [math.exp(-gamma * (len(w) - L_target)**2) for w in candidates]
    total = sum(weights)
    if total == 0: return rng.choice(candidates)
    r = rng.random() * total; cum = 0.0
    for w, wt in zip(candidates, weights):
        cum += wt
        if r < cum: return w
    return candidates[-1]

def run_sim_clamped(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf_vms, onset_ll_vms,
                    mid_nemed, lf_nemed, ll_nemed, rng, lexicons):
    """Run simulation with vocabulary clamping for sparse-midfix onset classes.
    lexicons: dict of onset -> list of words (for clamping), or empty dict (no clamping).
    """
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    mid_words = []
    while len(lines) < TARGET_LINES and pos < len(w) - 2:
        n = max(2, min(20, round(rng.gauss(MU_LEN, SIGMA_LEN))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []; word_idx = 0
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf(onset_mid, onset_lf_vms, suffix_lf_sup, P_LF, rng, lf_nemed)
            elif i == len(chunk) - 1:
                ew = cipher_ll(onset_ll_vms, ll_onsets, suffix_global, P_BLIND, rng, ll_nemed)
            else:
                if prev_word is not None and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf_length_biased(buf, prev_onset, P_QOKCH, P_CHQOK,
                                                 rng, word_idx, GAMMA)
                    if src is None: src = rng.choice(list(buf))
                    if rng.random() < MP:
                        ew = timm_modify(src, onset_mid, suffix_mid_sup, rng)
                        # Clamp modified word to lexicon if applicable
                        if lexicons:
                            ew = clamp_to_lexicon(ew, lexicons, rng)
                    else:
                        ew = src  # copy — already clamped in buffer
                else:
                    ew = random_eva_word_onset_biased(onset_mid, suffix_mid_sup, rng,
                                                      mid_nemed, P_MF, word_idx, ALPHA, BETA)
                    # Clamp cipher word to lexicon if applicable
                    if lexicons:
                        ew = clamp_to_lexicon(ew, lexicons, rng)
                buf.append(ew); word_idx += 1
                mid_words.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES], mid_words

def closed_paradigm_size(words, onset, target=0.90):
    onset_words = [w for w in words if get_onset(w) == onset]
    if len(onset_words) < 10: return 0, 0, 0
    counts = Counter(onset_words)
    total = len(onset_words)
    n_types = len(counts)
    cumsum = 0; n90 = 0
    for w, c in counts.most_common():
        cumsum += c; n90 += 1
        if cumsum / total >= target: break
    return n90, n_types, n90/n_types if n_types else 0

def compute_battery_metrics(lines):
    """Compute key battery metrics for pass/fail check."""
    all_words = [w for l in lines for w in l]
    lf_words  = [l[0]  for l in lines if l]
    ll_words  = [l[-1] for l in lines if len(l) > 1]
    mid_words = [w for l in lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words)
    if n == 0: return {}

    # edy_rate
    edy_r = sum(1 for w in all_words if w.endswith('edy') or w.endswith('eedy')) / n

    # am_mid_enr
    am_all = sum(1 for w in all_words if w.endswith('am')) / n
    am_mid = sum(1 for w in mid_words if w.endswith('am')) / len(mid_words) if mid_words else 0
    am_mid_enr = (am_mid / am_all) if am_all else 0

    # y_lf: fraction of LF words with y-onset
    y_lf = sum(1 for w in lf_words if w.startswith('y')) / len(lf_words) if lf_words else 0

    # am_ll: ll_am / global_am
    am_ll_raw = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words) if ll_words else 0
    am_ll = (am_ll_raw / am_all) if am_all else 0

    # d_ll: ll_d / global_d
    d_all = sum(1 for w in all_words if get_onset(w) == 'd') / n
    d_ll  = sum(1 for w in ll_words  if get_onset(w) == 'd') / len(ll_words) if ll_words else 0
    d_ll_enr = (d_ll / d_all) if d_all else 0

    # qok_ch: fraction of ch-onset words that are in MID (ch_mid/ch_all)
    ch_all = sum(1 for w in all_words if get_onset(w) == 'ch')
    ch_mid = sum(1 for w in mid_words if get_onset(w) == 'ch')
    qok_ch = ch_mid / ch_all if ch_all else 0

    # word lengths
    lf_wl  = sum(len(w) for w in lf_words)  / len(lf_words)  if lf_words else 0
    mid_wl = sum(len(w) for w in mid_words) / len(mid_words) if mid_words else 0
    ll_wl  = sum(len(w) for w in ll_words)  / len(ll_words)  if ll_words else 0

    return {
        'edy_r': edy_r, 'am_mid_enr': am_mid_enr,
        'y_lf': y_lf, 'am_ll': am_ll, 'd_ll': d_ll_enr, 'qok_ch': qok_ch,
        'lf_wl': lf_wl, 'mid_wl': mid_wl, 'll_wl': ll_wl,
        'n_words': n, 'n_mid': len(mid_words),
    }

# VMS reference values for battery
VMS_BATTERY = {
    'edy_r':     (0.126, 0.20),   # target, ±frac
    'am_mid_enr': (1.0, 0.20),    # normalised to 1.0
    'y_lf':      (None, None),    # not checked here
    'am_ll':     (6.55, 0.20),    # ll_am/global_am
    'd_ll':      (2.60, 0.20),    # ll_d/global_d
    'qok_ch':    (0.877, 0.20),   # ch fraction at MID (pass ≥0.70)
    'lf_wl':     (5.732, 0.20),
    'mid_wl':    (5.184, 0.20),
    'll_wl':     (5.015, 0.20),
}

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

# Clamp conditions to test
# Each entry: (label, clamp_n_map_func)
# clamp_n_map_func takes (vms_mid_words) and returns the n_map dict or None (baseline)
CLAMP_CONDITIONS = [
    ('baseline_N=None',  lambda mid: None),
    ('clamp_N_qok=32',   lambda mid: {'qok': 32,  'ok': 67,  'ot': 83,  'qot': 46}),
    ('clamp_N_qok=50',   lambda mid: {'qok': 50,  'ok': 107, 'ot': 130, 'qot': 72}),
    ('clamp_N_qok=100',  lambda mid: {'qok': 100, 'ok': 150, 'ot': 156, 'qot': 88}),  # capped at total types
    ('clamp_ALL_CP90',   lambda mid: {'qok': 32, 'ok': 67, 'ot': 83, 'qot': 46,
                                       'sh': 145, 'ch': 284, 'd': 149}),
]

print("exp_303: Finite Vocabulary Pool for Sparse-Midfix Onset Classes (H505)")
print("=" * 70)

print("\nParsing VMS B-dialect corpus...")
b_lines = parse_vms_b()
vms_dist = compute_vms_distributions(b_lines)
vms_mid = vms_dist['mid_words']
print(f"  VMS B: {len(b_lines)} lines, {vms_dist['n']} words, {len(vms_mid)} MID words")

print("\nLoading Latin corpus...")
latin_words = load_latin(LATIN_CORPUS)
print(f"  {len(latin_words)} Latin words loaded.")

# Print VMS reference CP90 sizes
print("\nVMS Per-Onset Closed Paradigm (MID words):")
print(f"  {'Onset':6s}  {'N':6s}  {'Types':6s}  {'CP90':6s}  {'CP90%':6s}")
for onset in ['qok', 'ok', 'ot', 'qot', 'sh', 'ch', 'd']:
    n90, n_types, frac = closed_paradigm_size(vms_mid, onset)
    print(f"  {onset:6s}  {sum(1 for w in vms_mid if get_onset(w)==onset):6d}  {n_types:6d}  {n90:6d}  {frac*100:5.1f}%")

suffix_global = vms_dist['suffix_global']
suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
onset_lf_vms = vms_dist['onset_lf']; onset_ll_vms = vms_dist['onset_ll']
onset_mid = vms_dist['onset_mid']
d_global = vms_dist['onset_global'].get('d', 0)
d_ll_non_blind_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0
d_boost_weight = compute_d_boost(d_global, vms_dist['d_ll_target'], d_ll_non_blind_enr, P_BLIND)
ll_onsets = build_ll_onsets(onset_ll_vms, d_boost_weight)

# Main loop over clamp conditions
print("\n" + "=" * 70)
print("Per-Onset CP90 Ratios Under Vocabulary Clamping")
print("=" * 70)

onsets_to_check = ['qok', 'ok', 'ot', 'qot', 'sh', 'ch', 'd']
vms_n90 = {}
for onset in onsets_to_check:
    n90, n_types, _ = closed_paradigm_size(vms_mid, onset)
    vms_n90[onset] = (n90, n_types)

results_table = []

for cond_label, clamp_n_func in CLAMP_CONDITIONS:
    print(f"\n--- Condition: {cond_label} ---")
    n_map = clamp_n_func(vms_mid)

    # Build lexicons
    if n_map:
        lexicons = build_per_onset_lexicons(vms_mid, n_map)
        for onset, lex in lexicons.items():
            n_types_in_lex = len(set(lex))
            print(f"  Lexicon: {onset} → {n_types_in_lex} types, {len(lex)} weighted tokens")
    else:
        lexicons = {}

    # Run N_FULL trials
    rng = random.Random(SEED)
    all_mid_words = []
    all_sim_lines = []
    for trial in range(N_FULL):
        lines, mid_words = run_sim_clamped(
            latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms,
            vms_dist['mid_nemed'], vms_dist['lf_nemed'], vms_dist['ll_nemed'],
            rng, lexicons)
        all_mid_words.extend(mid_words)
        all_sim_lines.extend(lines)

    # Aggregate over all trials for CP90
    print(f"\n  Per-Onset CP90 (aggregated {N_FULL} trials):")
    print(f"  {'Onset':6s}  {'N/trial':8s}  {'Types/trial':11s}  {'CP90':6s}  {'CP90%':6s}  VMS_CP90  Ratio")

    cond_ratios = {'label': cond_label}
    for onset in onsets_to_check:
        n90, n_types, frac = closed_paradigm_size(all_mid_words, onset)
        total_onset = sum(1 for w in all_mid_words if get_onset(w) == onset)
        types_per_trial = n_types * 1.0  # across all trials combined
        n_per_trial = total_onset / N_FULL
        # Estimate per-trial types by scaling
        vms_n90_this, vms_ntypes = vms_n90.get(onset, (1, 1))
        ratio = n90 / vms_n90_this if vms_n90_this > 0 else float('nan')
        print(f"  {onset:6s}  {n_per_trial:8.0f}  {types_per_trial:11.0f}  {n90:6d}  {frac*100:5.1f}%  {vms_n90_this:8d}  {ratio:5.2f}×")
        cond_ratios[onset] = ratio

    # Total MID vocabulary
    total_types = len(set(all_mid_words))
    per_trial_types = total_types  # approximate
    print(f"\n  Total MID unique types ({N_FULL} trials combined): {total_types}")
    print(f"  VMS MID unique types: {len(set(vms_mid))}")
    cond_ratios['total_types'] = total_types

    # Battery metrics (sampled from last 5 trials)
    # Re-run 5 trials for battery to get per-trial estimates
    rng2 = random.Random(SEED + 5000)
    battery_accum = defaultdict(list)
    for trial in range(5):
        lines, _ = run_sim_clamped(
            latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms,
            vms_dist['mid_nemed'], vms_dist['lf_nemed'], vms_dist['ll_nemed'],
            rng2, lexicons)
        m = compute_battery_metrics(lines)
        for k, v in m.items():
            battery_accum[k].append(v)

    print(f"\n  Key battery metrics (mean over 5 trials):")
    print(f"  edy_r: {sum(battery_accum['edy_r'])/5:.4f}  (VMS~0.126, need ≥0.101)")
    print(f"  am_mid_enr: {sum(battery_accum['am_mid_enr'])/5:.4f}  (VMS~1.00, need 0.80-1.20)")
    print(f"  am_ll: {sum(battery_accum['am_ll'])/5:.3f}  (VMS=6.55, need 5.24-7.86)")
    print(f"  d_ll: {sum(battery_accum['d_ll'])/5:.3f}  (VMS~2.60, need 2.08-3.12)")
    print(f"  lf_wl: {sum(battery_accum['lf_wl'])/5:.3f}, mid_wl: {sum(battery_accum['mid_wl'])/5:.3f}, ll_wl: {sum(battery_accum['ll_wl'])/5:.3f}")
    edy_mean = sum(battery_accum['edy_r'])/5
    am_mid_mean = sum(battery_accum['am_mid_enr'])/5
    am_ll_mean = sum(battery_accum['am_ll'])/5
    edy_ok = 0.101 <= edy_mean <= 0.151
    am_mid_ok = 0.80 <= am_mid_mean <= 1.20
    am_ll_ok = 5.24 <= am_ll_mean <= 7.86
    print(f"  PASS checks: edy_r={'PASS' if edy_ok else 'FAIL'}, "
          f"am_mid_enr={'PASS' if am_mid_ok else 'FAIL'}, "
          f"am_ll={'PASS' if am_ll_ok else 'FAIL'}")

    results_table.append(cond_ratios)

# Summary comparison table
print("\n" + "=" * 70)
print("SUMMARY: CP90 Ratios vs Condition")
print("=" * 70)
print(f"  {'Condition':25s}  {'qok':6s}  {'ok':6s}  {'ot':6s}  {'qot':6s}  {'sh':6s}  {'ch':6s}  {'d':6s}")
for r in results_table:
    label = r['label'][:25]
    row = "  " + f"{label:25s}"
    for onset in ['qok', 'ok', 'ot', 'qot', 'sh', 'ch', 'd']:
        val = r.get(onset, float('nan'))
        row += f"  {val:5.2f}×"
    print(row)

print("\nDone.")
