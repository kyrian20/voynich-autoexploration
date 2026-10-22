"""
exp_585: Non-Voynich Architecture Specificity Test — Corrected Replication

Corrects exp_584's simulation bug: vocabulary collapse caused spurious same-word
succession (VMS positive control got 7/17 applicable instead of ~17/17). Root cause:
pick_word(onset, suffix) returns actual VMS word strings; many combos have only one
unique type, so the copy-buffer "modify" path often returned the same word as the source,
inflating adj_rate, ss_mean, ss_d, ss_y.

FIX: Use exp_575's abstract-token simulation (timm_modify + make_word_sim). These
generate synthetic VMS-style words where onset class is preserved by the modification
operation but the word STRING is new (character-level perturbation). This matches the
methodology that achieved 19/19 in exp_314/exp_575.

DESIGN: Identical to exp_584 except simulation methodology.
  Corpus 1 (LATIN):  Cicero De Officiis, character-mapped onset/suffix
  Corpus 2 (SYNTH):  Inter-shuffle (exp_575: 12/17 known — used as denominator)
  Corpus 3 (ITAL):   Dante Divina Commedia, character-mapped onset/suffix

PRE-REGISTERED THRESHOLDS (state/preregistration_transliteration_and_specificity_thresholds.md):
  Strong:  R >= 1.3
  Partial: R >= 1.0 (one regime)
  Weak:    R < 1.0
"""
from pathlib import Path as _RepositoryPath

import os, re, random, json, math
from collections import Counter, deque, defaultdict
from itertools import product

REPO = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
TRANS = os.path.join(REPO, 'data/transcriptions/eva_zl3b.txt')
CICERO = os.path.join(REPO, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DANTE  = os.path.join(REPO, 'data/reference_corpora/italian/dante_divina_commedia.txt')
OUT_DIR = os.path.join(REPO, 'experiments/exp_585_nonvms_specificity_v2')

SEED_BASE = 585000

# ─── FIXED ARCHITECTURAL CONSTANTS (from exp_314/575) ─────────────────────────
CP = 0.55; MP = 0.90; P_STUTTER = 0.006; GAMMA = 0.30; ALPHA = 0.20
BETA_BASE = 0.50; LL_BASE = 8; LL_SLOPE = 0.30; LL_N_REF = 5; LL_MIN_CAP = 3
P_SHORT = 0.060; P_LONG = 0.180; THRESH_SHORT = 5; THRESH_LONG = 10; MEAN_N = 8.4
MU_LEN = 8.4; SIGMA_LEN = 3.0
P_MF = 0.20; P_LF_MF = 0.50; P_LL_MF = 0.00
P_CHQOK = 0.12; L_BASE = 5.40; L_SLOPE = -0.053
IDX_THRESH = 2; SHORT_THRESH = 2; WINDOW = 20; MAX_RETRY = 10

SHORT_ONSETS = {'d','s','y','k','t','l','r','p','f','o'}
EVA_CHARS = list('acdehiklmnoqrsty')
SPARSE_ONSETS = {'qok','ok','ot','qot'}

# ─── EVA ONSET/SUFFIX CLASSIFICATION ──────────────────────────────────────────
ONSET_ORDER = [
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o'),
]
SUFFIX_PATTERNS = ['eedy','edy','aiin','ain','am','ey','ol','or','al','ar','dy']

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

def folio_base(folio):
    return re.sub(r'[rv]\d*$', '', folio)

# ─── CHARACTER-BASED ONSET/SUFFIX FOR NON-VMS CORPORA ────────────────────────

def get_onset_char(w):
    w = w.lower()
    if not w: return 'other'
    if w[0] == 'q': return 'qok'
    if w[0] == 'd': return 'd'
    if w[0] == 's': return 's'
    if w[0] in ('y', 'i'): return 'y'
    if w[0] in ('c', 'g', 'k'): return 'ch'
    if w[0] == 'o': return 'ok'
    if w[0] == 'l': return 'l'
    if w[0] == 'a': return 'am_on'
    if w[0] == 'r': return 'r'
    return 'other'

def get_suffix_char(w):
    w = w.lower()
    if not w: return 'other'
    if w.endswith('um') or w.endswith('am') or w.endswith('em') or w.endswith('im'):
        return 'am'
    if w.endswith('edy') or w.endswith('odi') or w.endswith('idi'):
        return 'edy'
    if w.endswith('ant') or w.endswith('unt') or w.endswith('ino') or w.endswith('ina'):
        return 'aiin'
    return 'other'

# ─── VMS CORPUS PARSER ────────────────────────────────────────────────────────

def parse_vms_b_lines():
    folio_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(TRANS, 'r', encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw or raw.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', raw)
            if not m: continue
            fb = folio_base(m.group(1).lstrip('+*=&~'))
            text = re.sub(r'<[^>]+>', '', raw)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_stats[fb]['edy'] += 1

    b_folios = {fb for fb, s in folio_stats.items()
                if s['total'] > 0 and (s['edy']+s['eedy'])/s['total'] >= 0.05}

    b_lines = []
    with open(TRANS, 'r', encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw or raw.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', raw)
            if not m: continue
            folio_raw = m.group(1).lstrip('+*=&~')
            fb = folio_base(folio_raw)
            if fb not in b_folios: continue
            locus = m.group(3).lstrip('+*=/~&@')
            if not locus.startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', raw)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words:
                b_lines.append(words)
    return b_lines

# ─── CORPUS EXTRACTION (Latin / Italian) ─────────────────────────────────────

ENGLISH_STOPWORDS = {
    'the','and','of','to','a','in','that','is','was','he','it','for','on',
    'are','as','with','his','they','at','be','this','have','from','or','had',
    'by','not','but','what','all','were','we','when','your','can','said',
    'there','use','an','each','which','she','do','how','their','if','will',
    'up','other','about','out','many','then','them','these','so','some',
    'her','would','make','like','him','into','time','has','look','two','more',
    'no','way','could','my','than','first','been','call','who','oil','sit',
    'now','find','long','down','day','did','get','come','made','may','part',
}

def extract_latin_words(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    paragraphs = re.split(r'\n\s*\n', text)
    latin_words = []
    for para in paragraphs:
        words = re.findall(r'\b[a-zA-Z]+\b', para)
        if len(words) < 5: continue
        english_ratio = sum(1 for w in words if w.lower() in ENGLISH_STOPWORDS) / len(words)
        if english_ratio < 0.08:
            latin_words.extend([w.lower() for w in words if w.isalpha() and len(w) >= 2])
    return latin_words

def extract_italian_words(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    start = re.search(r'\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*', text)
    if start: text = text[start.end():]
    end = re.search(r'\*\*\* END OF THE PROJECT GUTENBERG EBOOK', text)
    if end: text = text[:end.start()]
    words = re.findall(r'\b[a-zA-Z\u00C0-\u024F]+\b', text)
    return [w.lower() for w in words if len(w) >= 2 and not w.isupper()]

def segment_to_lines(words, len_hist, target_n, rng):
    len_list = sorted(len_hist.keys())
    len_counts = [len_hist[l] for l in len_list]
    total = sum(len_counts)
    cum = []
    s = 0
    for c in len_counts:
        s += c
        cum.append(s / total)

    def sample_len():
        r = rng.random()
        for l, c in zip(len_list, cum):
            if r <= c: return l
        return len_list[-1]

    lines = []
    idx = 0; n = len(words)
    if n == 0: return []
    while len(lines) < target_n:
        ll = sample_len()
        if ll < 2: ll = 2
        word_slice = []
        while len(word_slice) < ll:
            remaining = ll - len(word_slice)
            start_idx = idx % n
            end_idx = start_idx + remaining
            if end_idx <= n:
                word_slice.extend(words[start_idx:end_idx])
                idx = end_idx % n
            else:
                word_slice.extend(words[start_idx:])
                idx = 0
        lines.append(word_slice[:ll])
    return lines[:target_n]

# ─── METRIC COMPUTATION ───────────────────────────────────────────────────────

BATTERY_19 = [
    'am_ll','d_ll','y_lf','ss_mean','adj_rate','qok_lf','d_lf','s_lf',
    'ch_ll','ok_ll','qok_ll','ss_d','ss_y','am_lf_enr','am_mid_enr',
    'edy_rate','word_len_mean','qok_ch','global_am_rate'
]
APPLICABLE = [m for m in BATTERY_19 if m not in ('word_len_mean', 'edy_rate')]
N_APPLICABLE = len(APPLICABLE)  # 17
PASS_TOL = 0.20

def check_pass(sv, tv):
    if tv < 1e-6: return sv < 1e-4
    return abs(sv / tv - 1.0) <= PASS_TOL

def compute_metrics(lines, get_onset_fn, get_suffix_fn):
    if not lines:
        return {k: 0.0 for k in BATTERY_19}

    all_onsets_lf = []; all_onsets_ll = []; all_onsets_mid = []
    all_suf_lf = []; all_suf_ll = []; all_suf_mid = []
    all_words_len = 0; all_words_n = 0
    adj_same = 0; adj_total = 0
    pairs_onset = []

    for line in lines:
        n = len(line)
        if n == 0: continue
        onsets = [get_onset_fn(w) for w in line]
        suffs  = [get_suffix_fn(w) for w in line]
        all_words_n += n
        all_words_len += sum(len(w) for w in line)
        all_onsets_lf.append(onsets[0]); all_suf_lf.append(suffs[0])
        if n >= 2: all_onsets_ll.append(onsets[-1]); all_suf_ll.append(suffs[-1])
        if n >= 3: all_onsets_mid.extend(onsets[1:-1]); all_suf_mid.extend(suffs[1:-1])
        for i in range(n - 1):
            pairs_onset.append((onsets[i], onsets[i+1]))
            adj_total += 1
            if line[i] == line[i+1]: adj_same += 1

    N_all = all_words_n; N_lf = len(all_onsets_lf); N_ll = len(all_onsets_ll)
    N_mid = len(all_onsets_mid); N_pairs = len(pairs_onset)

    if N_all == 0:
        return {k: 0.0 for k in BATTERY_19}

    all_onset_cnt = Counter(all_onsets_lf + all_onsets_ll + all_onsets_mid)
    lf_onset_cnt  = Counter(all_onsets_lf)
    ll_onset_cnt  = Counter(all_onsets_ll)
    all_suf_cnt   = Counter(all_suf_lf + all_suf_ll + all_suf_mid)
    lf_suf_cnt    = Counter(all_suf_lf)
    ll_suf_cnt    = Counter(all_suf_ll)
    mid_suf_cnt   = Counter(all_suf_mid)
    pair_cnt      = Counter(pairs_onset)

    def enr_onset(onset, pos_cnt, N_pos):
        base = all_onset_cnt[onset] / N_all if N_all else 0
        pos  = pos_cnt[onset] / N_pos if N_pos else 0
        return pos / base if base > 1e-6 else 0.0

    def enr_suf(suf, pos_cnt, N_pos):
        base = all_suf_cnt[suf] / N_all if N_all else 0
        pos  = pos_cnt[suf] / N_pos if N_pos else 0
        return pos / base if base > 1e-6 else 0.0

    def ss_for(onset):
        base_p = all_onset_cnt[onset] / N_all if N_all else 0
        expected = N_pairs * base_p * base_p
        obs = pair_cnt[(onset, onset)]
        return obs / expected if expected > 1e-6 else 0.0

    def qok_after_ch():
        n_ch = all_onset_cnt.get('ch', 0)
        n_qok_after = pair_cnt.get(('ch', 'qok'), 0)
        base_qok = all_onset_cnt.get('qok', 0) / N_all if N_all else 0
        rate = n_qok_after / n_ch if n_ch else 0
        return rate / base_qok if base_qok > 1e-6 else 0.0

    am_all_cnt = all_suf_cnt.get('am', 0)
    global_am_rate = am_all_cnt / N_all
    am_lf_enr = enr_suf('am', lf_suf_cnt, N_lf)
    am_ll_enr = enr_suf('am', ll_suf_cnt, N_ll)
    am_mid_rate = mid_suf_cnt.get('am', 0) / N_mid if N_mid else 0
    am_mid_enr = am_mid_rate / global_am_rate if global_am_rate > 1e-6 else 0.0

    edy_cnt = all_suf_cnt.get('edy', 0) + all_suf_cnt.get('eedy', 0)
    edy_rate = edy_cnt / N_all
    word_len_mean = all_words_len / N_all
    adj_rate = adj_same / adj_total if adj_total else 0.0

    ss_qok = ss_for('qok'); ss_ok = ss_for('ok'); ss_ch = ss_for('ch')
    ss_mean = (ss_qok + ss_ok + ss_ch) / 3.0
    ss_d = ss_for('d'); ss_y = ss_for('y')

    return {
        'am_ll':         am_ll_enr,
        'd_ll':          enr_onset('d', ll_onset_cnt, N_ll),
        'y_lf':          enr_onset('y', lf_onset_cnt, N_lf),
        'ss_mean':       ss_mean,
        'adj_rate':      adj_rate,
        'qok_lf':        enr_onset('qok', lf_onset_cnt, N_lf),
        'd_lf':          enr_onset('d', lf_onset_cnt, N_lf),
        's_lf':          enr_onset('s', lf_onset_cnt, N_lf),
        'ch_ll':         enr_onset('ch', ll_onset_cnt, N_ll),
        'ok_ll':         enr_onset('ok', ll_onset_cnt, N_ll),
        'qok_ll':        enr_onset('qok', ll_onset_cnt, N_ll),
        'ss_d':          ss_d,
        'ss_y':          ss_y,
        'am_lf_enr':     am_lf_enr,
        'am_mid_enr':    am_mid_enr,
        'edy_rate':      edy_rate,
        'word_len_mean': word_len_mean,
        'qok_ch':        qok_after_ch(),
        'global_am_rate': global_am_rate,
    }

# ─── SIMULATION (exp_575 abstract-token methodology) ──────────────────────────

def weighted_choice(rng, dist):
    r = rng.random(); cum = 0.0
    for k, v in dist.items():
        cum += v
        if r < cum: return k
    return list(dist.keys())[-1]

def make_word_sim(onset, suffix, rng, nemed, p_mf):
    midfix = ''
    if nemed and rng.random() < p_mf:
        midfix = weighted_choice(rng, nemed)
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset + midfix + rng.choice(['a','ai','o','oi','e','ei']) + suffix
    return onset + midfix + suffix

def timm_modify(word, onset_mid, suffix_mid, rng, nemed):
    if not word: return word
    onset_len = get_onset_len(word)
    edy_len = get_edy_suffix_len(word)
    mod_start = onset_len; mod_end = len(word) - edy_len
    if mod_start >= mod_end:
        return make_word_sim(weighted_choice(rng, onset_mid),
                             weighted_choice(rng, suffix_mid), rng, nemed, P_MF)
    op = rng.choice(['replace','insert','delete'])
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

def apply_suffix_length_bias(suf_w, word_idx, beta):
    if beta == 0.0 or word_idx < IDX_THRESH: return suf_w
    new_w = {}
    for suf, w in suf_w.items():
        suf_len = len(suf) if suf != 'other' else 5
        penalty = max(0, suf_len - SHORT_THRESH)
        new_w[suf] = w * math.exp(-beta * penalty)
    total = sum(new_w.values())
    return {s: v/total for s, v in new_w.items()} if total > 0 else suf_w

def build_midfix_dist(words):
    midfix_cnt = Counter()
    for w in words:
        onset = get_onset(w); suf = get_suffix(w)
        if onset == 'other' or suf == 'other': continue
        onset_len = get_onset_len(w); suf_len = len(suf)
        if (edy_len := get_edy_suffix_len(w)):
            mid_end = len(w) - edy_len
            midfix = w[onset_len:mid_end]
            if len(midfix) >= 1: midfix = midfix[:-1]
        else:
            midfix = w[onset_len:len(w)-suf_len]
        midfix_cnt[midfix] += 1
    total = sum(midfix_cnt.values())
    if total == 0: return {}, 0.0
    p_non_empty = sum(v for k, v in midfix_cnt.items() if k != '') / total
    non_empty = {mf: v for mf, v in midfix_cnt.items() if mf != ''}
    ne_total = sum(non_empty.values())
    return ({mf: v/ne_total for mf, v in non_empty.items()} if ne_total else {}), p_non_empty

def build_vms_dists(b_lines, p_blind):
    all_words = [w for l in b_lines for w in l]
    lf_words  = [l[0]  for l in b_lines if l]
    ll_words  = [l[-1] for l in b_lines if len(l) > 1]
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]

    def build_onset(words):
        cnt = Counter(get_onset(w) for w in words); cnt.pop('other', None)
        total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}

    def build_suffix(words):
        cnt = Counter(get_suffix(w) for w in words); total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}

    onset_lf  = build_onset(lf_words)
    onset_ll  = build_onset(ll_words)
    onset_mid = build_onset(mid_words)
    suffix_global = build_suffix(all_words)
    mid_nemed, mid_p = build_midfix_dist(mid_words)
    lf_nemed,  lf_p  = build_midfix_dist(lf_words)
    ll_nemed,  ll_p  = build_midfix_dist(ll_words)

    # d_boost for blind LL mechanism (from exp_575)
    d_global = Counter(get_onset(w) for w in all_words).get('d', 0) / len(all_words)
    ll_d = Counter(get_onset(w) for w in ll_words).get('d', 0) / len(ll_words)
    d_ll_target = ll_d / d_global if d_global else 0
    d_ll_non_blind_enr = onset_ll.get('d', 0) / d_global if d_global else 0
    if p_blind > 0:
        d_boost = d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind_enr) / p_blind
        d_boost = max(0.0, min(d_boost, 1.0))
    else:
        d_boost = 0.0

    remaining = 1.0 - d_boost
    base = {o: v for o, v in onset_ll.items() if o != 'd'}
    base_total = sum(base.values())
    ll_onsets = {o: v/base_total*remaining for o, v in base.items()} if base_total else {}
    ll_onsets['d'] = d_boost

    # Sparse-onset lexicons (for clamping: qok, ok, ot, qot)
    per_onset = defaultdict(Counter)
    for w in mid_words:
        on = get_onset(w)
        if on in SPARSE_ONSETS:
            per_onset[on][w] += 1
    lexicons = {}
    for on in SPARSE_ONSETS:
        lex = []; counts = per_onset[on]
        for w, c in counts.items(): lex.extend([w] * c)
        lexicons[on] = lex

    return {
        'onset_lf': onset_lf, 'onset_ll': onset_ll, 'onset_mid': onset_mid,
        'suffix_global': suffix_global, 'mid_nemed': mid_nemed, 'lf_nemed': lf_nemed,
        'll_nemed': ll_nemed, 'll_onsets': ll_onsets, 'mid_words': mid_words,
        'd_boost': d_boost, 'lexicons': lexicons,
    }

def make_suppressed_suffix(sg, r_am):
    am_w = sg.get('am', 0)
    new_am = am_w * r_am
    delta = am_w - new_am
    non_am = 1.0 - am_w
    return {suf: (new_am if suf == 'am' else w + (w/non_am)*delta if non_am > 0 else w)
            for suf, w in sg.items()}

def get_p_blind_n(n, p_blind_base):
    if n <= THRESH_SHORT: return P_SHORT * (p_blind_base / 0.115) if p_blind_base > 0 else 0.0
    if n >= THRESH_LONG:  return P_LONG  * (p_blind_base / 0.115) if p_blind_base > 0 else 0.0
    frac = (n - THRESH_SHORT) / (THRESH_LONG - THRESH_SHORT)
    base = P_SHORT + frac * (P_LONG - P_SHORT)
    return base * (p_blind_base / 0.115) if p_blind_base > 0 else 0.0

def get_max_ll_len(n):
    return max(LL_MIN_CAP, round(LL_BASE - LL_SLOPE * max(0, n - LL_N_REF)))

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
    L_target = L_BASE + L_SLOPE * word_idx
    weights = [math.exp(-GAMMA * (len(w) - L_target)**2) for w in candidates]
    total = sum(weights)
    if total == 0: return rng.choice(candidates)
    r = rng.random() * total; cum = 0.0
    for w, wt in zip(candidates, weights):
        cum += wt
        if r < cum: return w
    return candidates[-1]

def generate_ll_word(rng, vms_d, suffix_global, max_ll):
    candidates = []
    for _ in range(MAX_RETRY + 1):
        onset = weighted_choice(rng, vms_d['onset_ll'])
        suf   = weighted_choice(rng, suffix_global)
        ew = make_word_sim(onset, suf, rng, vms_d['ll_nemed'], P_LL_MF)
        if len(ew) <= max_ll: return ew
        candidates.append(ew)
    return min(candidates, key=len)

def run_sim(b_lines, vms_d, params, n_lines, rng):
    """Generate n_lines of VMS-style abstract tokens using exp_575 methodology."""
    beta_scale = params['beta_scale']
    p_blind_base = params['p_blind']
    r_lf   = params['r_lf']
    r_mid  = params['r_mid']
    p_qokch = params['p_qokch']

    suffix_global = vms_d['suffix_global']
    suf_lf_sup  = make_suppressed_suffix(suffix_global, r_lf)
    suf_mid_sup = make_suppressed_suffix(suffix_global, r_mid)
    lexicons = vms_d['lexicons']
    mid_nemed = vms_d['mid_nemed']

    # Menzerath beta
    beta_eff_base = BETA_BASE * beta_scale

    len_hist = Counter(len(line) for line in b_lines)
    len_list = sorted(len_hist.keys())
    len_counts_cum = []
    s = 0; total = sum(len_hist.values())
    for l in len_list:
        s += len_hist[l]
        len_counts_cum.append((l, s / total))

    def sample_len():
        r = rng.random()
        for l, c in len_counts_cum:
            if r <= c: return l
        return len_list[-1]

    sim_lines = []
    buf = deque(maxlen=WINDOW)
    prev_onset = None; prev_word = None

    while len(sim_lines) < n_lines:
        n = sample_len()
        if n < 2: n = 2
        p_blind_n = get_p_blind_n(n, p_blind_base)
        max_ll = get_max_ll_len(n)
        beta_eff = beta_eff_base * (n / MEAN_N)

        line = []
        word_idx = 0

        for i in range(n):
            if i == 0:
                # LF: fresh draw from LF distribution
                onset = weighted_choice(rng, vms_d['onset_lf'])
                suf   = weighted_choice(rng, suf_lf_sup)
                ew = make_word_sim(onset, suf, rng, vms_d['lf_nemed'], P_LF_MF)
            elif i == n - 1:
                # LL: blind mechanism or generate_ll_word
                if rng.random() < p_blind_n:
                    onset = weighted_choice(rng, vms_d['ll_onsets'])
                    ew = onset + 'am'
                else:
                    ew = generate_ll_word(rng, vms_d, suffix_global, max_ll)
            else:
                # MID: stutter / copy-buffer / fresh draw
                if prev_word is not None and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf(buf, prev_onset, rng, word_idx, p_qokch)
                    if src is None: src = rng.choice(list(buf))
                    if rng.random() < MP:
                        # Modify: preserve onset class, perturb characters
                        ew = timm_modify(src, vms_d['onset_mid'], suf_mid_sup, rng, mid_nemed)
                        # Clamp to lexicon for sparse onsets
                        on_new = get_onset(ew)
                        if on_new in lexicons and lexicons[on_new]:
                            ew = rng.choice(lexicons[on_new])
                    else:
                        ew = src
                else:
                    # Fresh draw with SHORT_ONSETS bias and Menzerath
                    new_ow = {o: v*(1+ALPHA*word_idx) if o in SHORT_ONSETS else v
                              for o, v in vms_d['onset_mid'].items()}
                    ow_total = sum(new_ow.values())
                    norm_ow = {o: v/ow_total for o, v in new_ow.items()} if ow_total else vms_d['onset_mid']
                    onset = weighted_choice(rng, norm_ow)
                    biased_suf = apply_suffix_length_bias(suf_mid_sup, word_idx, beta_eff)
                    suf = weighted_choice(rng, biased_suf)
                    ew = make_word_sim(onset, suf, rng, mid_nemed, P_MF)
                    on_new = get_onset(ew)
                    if on_new in lexicons and lexicons[on_new]:
                        ew = rng.choice(lexicons[on_new])
                buf.append(ew)
                word_idx += 1

            prev_onset = get_onset(ew)
            prev_word = ew
            line.append(ew)

        sim_lines.append(line)

    return sim_lines[:n_lines]

# ─── GRID SEARCH ──────────────────────────────────────────────────────────────

GRID_PARAMS = {
    'beta_scale': [0.5, 1.0, 1.2, 1.8],
    'p_blind':    [0.0, 0.05, 0.115, 0.18],
    'r_lf':       [0.05, 0.12, 0.30, 1.0],
    'r_mid':      [0.10, 0.20, 0.40, 1.0],
    'p_qokch':    [0.05, 0.12],
}

def run_grid_search(target_metrics, b_lines, applicable_metrics, n_sim, seed,
                    n_per_combo=3, cached_dists=None):
    combos = list(product(
        GRID_PARAMS['beta_scale'], GRID_PARAMS['p_blind'],
        GRID_PARAMS['r_lf'], GRID_PARAMS['r_mid'], GRID_PARAMS['p_qokch']
    ))
    print(f"  Grid: {len(combos)} combos × {n_per_combo} sims = {len(combos)*n_per_combo} runs")

    best_pass = -1; best_params = None; best_sim_metrics = None

    for ci, (bs, pb, rl, rm, pq) in enumerate(combos):
        params = {'beta_scale': bs, 'p_blind': pb, 'r_lf': rl, 'r_mid': rm, 'p_qokch': pq}

        # Build VMS dists for this p_blind (d_boost depends on p_blind)
        if cached_dists and pb in cached_dists:
            vms_d = cached_dists[pb]
        else:
            vms_d = build_vms_dists(b_lines, pb)
            if cached_dists is not None:
                cached_dists[pb] = vms_d

        accum = defaultdict(float)
        for trial in range(n_per_combo):
            rng = random.Random(seed + ci * 100 + trial)
            sim_lines = run_sim(b_lines, vms_d, params, n_sim, rng)
            m = compute_metrics(sim_lines, get_onset, get_suffix)
            for k, v in m.items(): accum[k] += v

        avg = {k: v / n_per_combo for k, v in accum.items()}
        n_pass = sum(1 for met in applicable_metrics
                     if check_pass(avg.get(met, 0), target_metrics.get(met, 0)))

        if n_pass > best_pass:
            best_pass = n_pass; best_params = params.copy(); best_sim_metrics = avg.copy()

        if (ci + 1) % 100 == 0:
            print(f"    ... {ci+1}/{len(combos)} combos done, best so far: {best_pass}")

    return best_pass, best_params, best_sim_metrics

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("exp_585: Non-VMS Specificity Test — Corrected Replication")
    print("  (abstract-token simulation matching exp_575 methodology)")
    print("=" * 65)

    # ── Load VMS B-dialect corpus ─────────────────────────────────────────────
    print("\n[Step 1] Loading VMS B-dialect corpus...")
    b_lines = parse_vms_b_lines()
    print(f"  B-dialect lines: {len(b_lines)}, words: {sum(len(l) for l in b_lines)}")

    n_target = len(b_lines)
    len_hist = Counter(len(line) for line in b_lines)

    # ── VMS target metrics ────────────────────────────────────────────────────
    print("\n[Step 2] Computing VMS B-dialect target metrics...")
    vms_metrics = compute_metrics(b_lines, get_onset, get_suffix)
    key_show = ['am_ll','d_ll','y_lf','ss_mean','adj_rate','edy_rate','word_len_mean','global_am_rate']
    print(f"  {'Metric':<20} {'VMS Value':>12}")
    for k in key_show:
        print(f"  {k:<20} {vms_metrics.get(k, 0):>12.4f}")

    # ── Latin corpus ──────────────────────────────────────────────────────────
    print("\n[Step 3] Extracting Latin corpus (Cicero De Officiis)...")
    lat_words = extract_latin_words(CICERO)
    print(f"  Latin words extracted: {len(lat_words)}")
    rng_lat = random.Random(SEED_BASE + 1)
    lat_lines = segment_to_lines(lat_words, len_hist, n_target, rng_lat)
    print(f"  Latin lines: {len(lat_lines)}, words: {sum(len(l) for l in lat_lines)}")

    print("\n[Step 4] Computing Latin character-mapped target metrics...")
    lat_metrics = compute_metrics(lat_lines, get_onset_char, get_suffix_char)
    print(f"  {'Metric':<20} {'Latin Value':>12}")
    for k in key_show:
        print(f"  {k:<20} {lat_metrics.get(k, 0):>12.4f}")

    # ── Italian corpus ────────────────────────────────────────────────────────
    print("\n[Step 5] Extracting Italian corpus (Dante Divina Commedia)...")
    ita_words = extract_italian_words(DANTE)
    print(f"  Italian words extracted: {len(ita_words)}")
    rng_ita = random.Random(SEED_BASE + 2)
    ita_lines = segment_to_lines(ita_words, len_hist, n_target, rng_ita)
    print(f"  Italian lines: {len(ita_lines)}, words: {sum(len(l) for l in ita_lines)}")

    print("\n[Step 6] Computing Italian character-mapped target metrics...")
    ita_metrics = compute_metrics(ita_lines, get_onset_char, get_suffix_char)
    print(f"  {'Metric':<20} {'Italian Value':>14}")
    for k in key_show:
        print(f"  {k:<20} {ita_metrics.get(k, 0):>14.4f}")

    # ── Cache VMS distributions for each p_blind value ───────────────────────
    print("\n[Building VMS distribution cache for grid search...]")
    dist_cache = {}
    for pb in GRID_PARAMS['p_blind']:
        dist_cache[pb] = build_vms_dists(b_lines, pb)
    print(f"  Cached {len(dist_cache)} p_blind distributions")

    # ── VMS positive control ──────────────────────────────────────────────────
    print("\n[Step 7] VMS positive control — 6-param grid search (verify ~19/19)...")
    vms_best, vms_params, vms_sim = run_grid_search(
        vms_metrics, b_lines, BATTERY_19, n_target,
        seed=SEED_BASE + 10, n_per_combo=3, cached_dists=dict(dist_cache)
    )
    print(f"  VMS positive control: {vms_best}/19 PASS (expected ~19)")
    print(f"  Best params: {vms_params}")

    # ── Latin grid search ─────────────────────────────────────────────────────
    print(f"\n[Step 8] Grid search for Latin corpus ({N_APPLICABLE} applicable metrics)...")
    lat_best, lat_params, lat_sim = run_grid_search(
        lat_metrics, b_lines, APPLICABLE, n_target,
        seed=SEED_BASE + 20, n_per_combo=3, cached_dists=dict(dist_cache)
    )
    print(f"  Latin best: {lat_best}/{N_APPLICABLE} applicable PASS")
    print(f"  Best params: {lat_params}")

    # ── Italian grid search ───────────────────────────────────────────────────
    print(f"\n[Step 9] Grid search for Italian corpus ({N_APPLICABLE} applicable metrics)...")
    ita_best, ita_params, ita_sim = run_grid_search(
        ita_metrics, b_lines, APPLICABLE, n_target,
        seed=SEED_BASE + 30, n_per_combo=3, cached_dists=dict(dist_cache)
    )
    print(f"  Italian best: {ita_best}/{N_APPLICABLE} applicable PASS")
    print(f"  Best params: {ita_params}")

    # ── Specificity ratio ─────────────────────────────────────────────────────
    print("\n[Step 10] Specificity ratio R...")
    INTER_SHUFFLE_APPLICABLE_PASS = 12  # from exp_575 (correct simulation)

    # VMS applicable PASS from positive control
    vms_applicable_from_control = sum(1 for met in APPLICABLE
                                      if check_pass(vms_sim.get(met, 0), vms_metrics.get(met, 0)))
    print(f"\n  VMS positive control applicable: {vms_applicable_from_control}/{N_APPLICABLE}")
    print(f"  Latin applicable PASS:           {lat_best}/{N_APPLICABLE}")
    print(f"  Italian applicable PASS:         {ita_best}/{N_APPLICABLE}")
    print(f"  Inter-shuffle applicable PASS:   {INTER_SHUFFLE_APPLICABLE_PASS}/{N_APPLICABLE} (exp_575)")

    best_non_vms = max(lat_best, INTER_SHUFFLE_APPLICABLE_PASS, ita_best)

    # R using C008-established VMS=17 (pre-registered)
    VMS_APPLICABLE_C008 = N_APPLICABLE  # 17, from exp_314
    R_6param_c008 = VMS_APPLICABLE_C008 / best_non_vms if best_non_vms > 0 else float('inf')

    # R using this experiment's actual VMS positive control
    R_6param_actual = vms_applicable_from_control / best_non_vms if best_non_vms > 0 else float('inf')

    print(f"\n  Best non-VMS:                    {best_non_vms}/{N_APPLICABLE}")
    print(f"  R_6param (C008 VMS=17):          {VMS_APPLICABLE_C008}/{best_non_vms} = {R_6param_c008:.4f}")
    print(f"  R_6param (this exp VMS actual):  {vms_applicable_from_control}/{best_non_vms} = {R_6param_actual:.4f}")

    for lbl, R in [("C008 VMS=17", R_6param_c008), ("actual", R_6param_actual)]:
        if R >= 1.3:
            cls = "STRONG_SPECIFICITY"
        elif R >= 1.0:
            cls = "PARTIAL_SPECIFICITY"
        else:
            cls = "WEAK_OR_ABSENT_SPECIFICITY"
        print(f"  Classification ({lbl}): {cls}")

    # ── Metric comparison table ───────────────────────────────────────────────
    print("\n[METRIC COMPARISON TABLE]")
    print(f"{'Metric':<20} {'VMS':>8} {'Latin':>8} {'Italian':>8} {'App?':>6}")
    print("-" * 55)
    for met in BATTERY_19:
        vv = vms_metrics.get(met, 0)
        lv = lat_metrics.get(met, 0)
        iv = ita_metrics.get(met, 0)
        app = 'YES' if met in APPLICABLE else 'NO'
        print(f"{met:<20} {vv:>8.4f} {lv:>8.4f} {iv:>8.4f} {app:>6}")

    print("\n[VMS SIM vs VMS TARGET — ALL 19]")
    print(f"{'Metric':<20} {'Target':>8} {'Sim':>8} {'PASS?':>6}")
    print("-" * 45)
    for met in BATTERY_19:
        tv = vms_metrics.get(met, 0); sv = vms_sim.get(met, 0) if vms_sim else 0
        ok = 'PASS' if check_pass(sv, tv) else 'FAIL'
        print(f"{met:<20} {tv:>8.4f} {sv:>8.4f} {ok:>6}")

    print("\n[SIM vs LATIN TARGET — APPLICABLE METRICS]")
    print(f"{'Metric':<20} {'Target':>8} {'Sim':>8} {'PASS?':>6}")
    print("-" * 45)
    for met in APPLICABLE:
        tv = lat_metrics.get(met, 0); sv = lat_sim.get(met, 0) if lat_sim else 0
        ok = 'PASS' if check_pass(sv, tv) else 'FAIL'
        print(f"{met:<20} {tv:>8.4f} {sv:>8.4f} {ok:>6}")

    print("\n[SIM vs ITALIAN TARGET — APPLICABLE METRICS]")
    print(f"{'Metric':<20} {'Target':>8} {'Sim':>8} {'PASS?':>6}")
    print("-" * 45)
    for met in APPLICABLE:
        tv = ita_metrics.get(met, 0); sv = ita_sim.get(met, 0) if ita_sim else 0
        ok = 'PASS' if check_pass(sv, tv) else 'FAIL'
        print(f"{met:<20} {tv:>8.4f} {sv:>8.4f} {ok:>6}")

    # ── Save results ──────────────────────────────────────────────────────────
    results = {
        'vms_metrics': vms_metrics, 'latin_metrics': lat_metrics,
        'italian_metrics': ita_metrics,
        'vms_positive_control_pass_all19': vms_best,
        'vms_positive_control_pass_applicable': vms_applicable_from_control,
        'vms_best_params': vms_params, 'vms_best_sim_metrics': vms_sim,
        'latin_best_pass_applicable': lat_best, 'latin_best_params': lat_params,
        'latin_best_sim_metrics': lat_sim,
        'italian_best_pass_applicable': ita_best, 'italian_best_params': ita_params,
        'italian_best_sim_metrics': ita_sim,
        'inter_shuffle_applicable_pass': INTER_SHUFFLE_APPLICABLE_PASS,
        'vms_applicable_c008': VMS_APPLICABLE_C008,
        'n_applicable': N_APPLICABLE,
        'best_non_vms_applicable': best_non_vms,
        'R_6param_c008': R_6param_c008,
        'R_6param_actual': R_6param_actual,
        'applicable_metrics': APPLICABLE, 'battery_19': BATTERY_19,
    }

    out_path = os.path.join(OUT_DIR, 'specificity_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {out_path}")

    print(f"\n{'='*65}")
    print(f"FINAL RESULT:")
    print(f"  VMS positive control: {vms_best}/19 | applicable: {vms_applicable_from_control}/17")
    print(f"  Latin: {lat_best}/17 | Italian: {ita_best}/17 | Inter-shuffle: {INTER_SHUFFLE_APPLICABLE_PASS}/17")
    print(f"  R_6param (C008): {R_6param_c008:.4f} | R_6param (actual): {R_6param_actual:.4f}")
    print(f"{'='*65}")

if __name__ == '__main__':
    main()
