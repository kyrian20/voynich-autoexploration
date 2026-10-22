"""
exp_282: H483 — Word-Index-Conditioned MID Generation

Question: Can conditioning MID word selection on position within line (word_index)
produce the B-dialect within-line word length gradient and improve Menzerath magnitude?

Background:
- exp_272 (F272): VMS B-dialect MID slope=-0.053 chars/word-idx (Sim=-0.001; 58× gap)
  Onset composition gradient: short-onset fraction increases 20.8%→32.7% at idx1→idx10
  A-dialect MID slope=+0.016 (no gradient) — no fix needed for A
  B-dialect Menzerath r=-0.206 vs sim=-0.055 (magnitude gap)
- exp_270 (F270): midfix LF/LL mechanism improved Menzerath direction but not magnitude
- Architecture reason for flat sim: position-agnostic buffer cannot produce word-index-
  dependent word lengths by construction (draws uniformly from buffer regardless of position)

Approach:
Two mechanisms to test in combination:
  A) Buffer draw preference: when drawing from buffer at word_index i, prefer shorter words.
     Implemented as soft preference: P(accept word w at index i) ∝ exp(-gamma * (len(w) - L_target(i)) ^ 2)
     where L_target(i) = L_base - slope * i (calibrated to VMS B-dialect slope=-0.053)
     gamma controls strength of preference.
  B) Onset preference: at high word_index, prefer short-onset classes (d/s/y/k/t).
     Implemented as onset distribution reweighting: multiply short-onset weights by (1 + alpha * i),
     normalize. alpha controls strength.

The two mechanisms are complementary:
  A affects buffer draws (CP=0.55 of MID words)
  B affects fresh word generation (45% of MID words, after stutter check)

Design:
- Part 1: Sweep gamma ∈ {0.00, 0.05, 0.10, 0.20, 0.30} at N=10 each (alpha=0)
  Measure: within-line MID slope, Menzerath r, 19-metric PASS
- Part 2: At best gamma, sweep alpha ∈ {0.00, 0.05, 0.10, 0.15} at N=10
  Measure: same
- Part 3: Full run (N=30) at best combination

Calibration:
- L_base = 5.40 (VMS B-dialect MID mean word length)
- L_slope = -0.053 chars/word-idx (VMS B MID slope from F272)
- Short-onset classes: d, s, y, k, t, l, r, p, f, o (single/short char onsets)
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict
import math

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SWEEP  = 10
N_FULL   = 30
TARGET_LINES = 2411
WINDOW   = 20
SEED     = 282000

# B-dialect 12-mechanism parameters (frozen at exp_257 + exp_281 p_mf=0.20)
P_BLIND   = 0.115; P_LF    = 1.0;   CP       = 0.55; MP       = 0.90
P_QOKCH   = 0.12;  P_CHQOK = 0.12;  P_STUTTER = 0.006
R_LF      = 0.12;  R_MID   = 0.25;  MU_LEN   = 8.4;  SIGMA_LEN = 3.0
P_MF      = 0.20   # best midfix rate from exp_280

# Within-line gradient calibration
L_BASE  = 5.40    # VMS B MID mean word length
L_SLOPE = -0.053  # VMS B MID slope (chars/word-idx) from F272

# Short-onset classes (single or 2-char, typically shorter words)
SHORT_ONSETS = {'d', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'o'}

EVA_CHARS = list('acdehiklmnoqrsty')

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']

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
            if folio_dialect.get(fb, 'unknown') != 'B': continue
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
    n = len(all_words); n_mid = len(mid_words)

    def build_onset(words):
        cnt = Counter(get_onset(w) for w in words)
        cnt.pop('other', None)
        total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}

    def build_suffix(words):
        cnt = Counter(get_suffix(w) for w in words)
        total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}

    onset_global = build_onset(all_words)
    onset_lf     = build_onset(lf_words)
    onset_ll     = build_onset(ll_words)
    onset_mid    = build_onset(mid_words)
    suffix_global = build_suffix(all_words)

    # Midfix distribution
    midfix_cnt = Counter()
    for w in mid_words:
        onset = get_onset(w); suf = get_suffix(w)
        if onset == 'other' or suf == 'other': continue
        onset_len = get_onset_len(w); suf_len = len(suf)
        if edy_len := get_edy_suffix_len(w):
            mid_end = len(w) - edy_len
            midfix = w[onset_len:mid_end]
            if len(midfix) >= 1: midfix = midfix[:-1]
        else:
            midfix = w[onset_len:len(w)-suf_len]
        midfix_cnt[midfix] += 1

    total_mf = sum(midfix_cnt.values())
    midfix_dist = {mf: cnt/total_mf for mf, cnt in midfix_cnt.items()} if total_mf else {}
    p_empty_midfix = midfix_dist.get('', 0)
    non_empty_dist_raw = {mf: v for mf, v in midfix_dist.items() if mf != ''}
    non_empty_total = sum(non_empty_dist_raw.values())
    non_empty_dist = {mf: v/non_empty_total for mf, v in non_empty_dist_raw.items()} if non_empty_total else {}

    am_r  = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words)
    d_r   = Counter(get_onset(w) for w in all_words).get('d', 0) / n
    ll_d  = Counter(get_onset(w) for w in ll_words).get('d', 0) / len(ll_words)
    lf_am_rate = sum(1 for w in lf_words if w.endswith('am')) / len(lf_words)
    mid_am_rate = sum(1 for w in mid_words if w.endswith('am')) / n_mid if n_mid else 0

    return {
        'onset_global': onset_global, 'onset_lf': onset_lf,
        'onset_ll': onset_ll, 'onset_mid': onset_mid,
        'suffix_global': suffix_global,
        'non_empty_midfix_dist': non_empty_dist,
        'am_r': am_r, 'am_ll_target': ll_am/am_r if am_r else 0,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'am_lf_enr': lf_am_rate/am_r if am_r else 0,
        'am_mid_enr': mid_am_rate/am_r if am_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words), 'n_mid': n_mid,
    }

def make_suppressed_suffix(suffix_global, r_am):
    am_w = suffix_global.get('am', 0); new_am = am_w * r_am
    delta = am_w - new_am; non_am = 1.0 - am_w
    return {suf: (new_am if suf=='am' else w + (w/non_am)*delta if non_am>0 else w) for suf, w in suffix_global.items()}

def compute_d_boost(d_global, d_ll_target, d_ll_non_blind_enr, p_blind):
    return d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind_enr) / p_blind

def build_ll_onsets(onset_ll_vms, d_boost_weight):
    remaining = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o != 'd'}
    base_total = sum(base.values())
    norm = {o: v/base_total * remaining for o, v in base.items()} if base_total else {}
    norm['d'] = d_boost_weight
    return norm

def weighted_choice(rng, dist):
    r = rng.random(); cum = 0.0
    for k, v in dist.items():
        cum += v
        if r < cum: return k
    return list(dist.keys())[-1]

def sample_midfix(rng, non_empty_dist, p_non_empty):
    if rng.random() < p_non_empty:
        return weighted_choice(rng, non_empty_dist)
    return ''

def make_word_sim(onset, suffix, rng, non_empty_midfix_dist, p_midfix_present):
    if suffix == 'other':
        return onset + suffix
    midfix = sample_midfix(rng, non_empty_midfix_dist, p_midfix_present)
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
        return onset + midfix + connector + suffix
    return onset + midfix + suffix

def random_eva_word(onset_weights, suffix_weights, rng, non_empty_midfix_dist, p_midfix_present):
    onset  = weighted_choice(rng, onset_weights)
    suffix = weighted_choice(rng, suffix_weights)
    return make_word_sim(onset, suffix, rng, non_empty_midfix_dist, p_midfix_present)

def random_eva_word_onset_biased(onset_weights, suffix_weights, rng, non_empty_midfix_dist,
                                  p_midfix_present, word_idx, alpha):
    """Generate a fresh word with onset bias toward shorter onsets at high word_index."""
    if alpha == 0.0:
        return random_eva_word(onset_weights, suffix_weights, rng, non_empty_midfix_dist, p_midfix_present)
    # Reweight: multiply short-onset weights by (1 + alpha * word_idx)
    new_weights = {}
    for o, w in onset_weights.items():
        if o in SHORT_ONSETS:
            new_weights[o] = w * (1 + alpha * word_idx)
        else:
            new_weights[o] = w
    total = sum(new_weights.values())
    norm_weights = {o: w/total for o, w in new_weights.items()}
    onset  = weighted_choice(rng, norm_weights)
    suffix = weighted_choice(rng, suffix_weights)
    return make_word_sim(onset, suffix, rng, non_empty_midfix_dist, p_midfix_present)

def cipher_ll(onset_ll_vms, ll_onsets, suffix_global, p_blind, rng):
    if rng.random() < p_blind:
        onset = weighted_choice(rng, ll_onsets)
        return onset + 'am'
    onset  = weighted_choice(rng, onset_ll_vms)
    suffix = weighted_choice(rng, suffix_global)
    return make_word_sim(onset, suffix, rng, {}, 0.0)

def cipher_lf(onset_mid, onset_lf_vms, suffix_lf, p_lf, rng):
    if rng.random() < p_lf:
        onset  = weighted_choice(rng, onset_lf_vms)
        suffix = weighted_choice(rng, suffix_lf)
        return make_word_sim(onset, suffix, rng, {}, 0.0)
    return random_eva_word(onset_mid, suffix_lf, rng, {}, 0.0)

def timm_modify(word, onset_mid, suffix_mid, rng):
    if not word: return word
    onset_len = get_onset_len(word); edy_len = get_edy_suffix_len(word)
    mod_start = onset_len; mod_end = len(word) - edy_len
    if mod_start >= mod_end:
        return random_eva_word(onset_mid, suffix_mid, rng, {}, 0.0)
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

def draw_buf(buf, prev_onset, p_qokch, p_chqok, rng):
    buf_list = list(buf)
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words: return rng.choice(ch_words)
    elif prev_onset == 'ch' and p_chqok > 0 and rng.random() < p_chqok:
        qok_words = [w for w in buf_list if get_onset(w) == 'qok']
        if qok_words: return rng.choice(qok_words)
    return rng.choice(buf_list)

def draw_buf_length_biased(buf, prev_onset, p_qokch, p_chqok, rng, word_idx, gamma):
    """Draw from buffer, preferring words whose length matches L_target(word_idx)."""
    buf_list = list(buf)
    if not buf_list: return None

    # First apply onset bias (qok→ch, ch→qok) — filter to preferred onset if applicable
    preferred = None
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words: preferred = ch_words
    elif prev_onset == 'ch' and p_chqok > 0 and rng.random() < p_chqok:
        qok_words = [w for w in buf_list if get_onset(w) == 'qok']
        if qok_words: preferred = qok_words

    candidates = preferred if preferred else buf_list

    if gamma == 0.0:
        return rng.choice(candidates)

    # Length-biased draw
    L_target = L_BASE + L_SLOPE * word_idx  # L_SLOPE is negative, so higher idx → shorter
    weights = []
    for w in candidates:
        diff = len(w) - L_target
        weights.append(math.exp(-gamma * diff * diff))
    total = sum(weights)
    if total == 0:
        return rng.choice(candidates)
    r = rng.random() * total
    cum = 0.0
    for w, wt in zip(candidates, weights):
        cum += wt
        if r < cum: return w
    return candidates[-1]

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms, non_empty_midfix_dist,
            gamma, alpha, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    while len(lines) < TARGET_LINES and pos < len(w) - 2:
        n = max(2, min(20, round(rng.gauss(MU_LEN, SIGMA_LEN))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        word_idx = 0  # 0-indexed within MID words only (not counting LF/LL)
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf(onset_mid, onset_lf_vms, suffix_lf_sup, P_LF, rng)
            elif i == len(chunk) - 1:
                ew = cipher_ll(onset_ll_vms, ll_onsets, suffix_global, P_BLIND, rng)
            else:
                if prev_word is not None and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf_length_biased(buf, prev_onset, P_QOKCH, P_CHQOK,
                                                 rng, word_idx, gamma)
                    if src is None:
                        src = rng.choice(list(buf))
                    if rng.random() < MP:
                        ew = timm_modify(src, onset_mid, suffix_mid_sup, rng)
                    else:
                        ew = src
                else:
                    ew = random_eva_word_onset_biased(onset_mid, suffix_mid_sup, rng,
                                                      non_empty_midfix_dist, P_MF,
                                                      word_idx, alpha)
                buf.append(ew)
                word_idx += 1
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def compute_metrics(lines):
    aw  = [w for l in lines for w in l]; n = len(aw)
    if n < 100: return None
    lf  = [l[0]  for l in lines if l]
    ll  = [l[-1] for l in lines if len(l) > 1]
    mid = [w for l in lines for w in l[1:-1] if len(l) > 2]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf  = Counter(get_onset(w) for w in lf)
    oc_ll  = Counter(get_onset(w) for w in ll)
    n_lf, n_ll, n_mid = len(lf), len(ll), len(mid)

    def enr(onset, ctr_slot, n_slot):
        s = ctr_slot.get(onset, 0)/n_slot if n_slot else 0
        g = oc_all.get(onset, 0)/n if n else 0
        return s/g if g > 0 else 0

    am_r   = sum(1 for w in aw if w.endswith('am')) / n
    ll_am  = sum(1 for w in ll if w.endswith('am')) / n_ll if n_ll else 0
    am_ll  = ll_am / am_r if am_r else 0
    d_ll   = enr('d', oc_ll, n_ll)
    y_lf   = enr('y', oc_lf, n_lf)

    tb = n-1
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    def ss(o):
        b = oc_all.get(o, 0)/n
        return bg.get((o,o),0)/(tb*b*b) if b > 0 and tb > 0 else 1.0
    ss_mean = (ss('qok')+ss('ok')+ss('ch'))/3
    adj = sum(1 for i in range(tb) if aw[i]==aw[i+1])/max(1,tb)

    qok_lf = enr('qok', oc_lf, n_lf); d_lf  = enr('d',  oc_lf, n_lf)
    s_lf   = enr('s',   oc_lf, n_lf); ch_ll = enr('ch', oc_ll, n_ll)
    ok_ll  = enr('ok',  oc_ll, n_ll); qok_ll = enr('qok', oc_ll, n_ll)
    ss_d = ss('d'); ss_y = ss('y')

    lf_am_rate  = sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf else 0
    mid_am_rate = sum(1 for w in mid if w.endswith('am'))/n_mid if n_mid else 0
    am_lf_enr   = lf_am_rate  / am_r if am_r else 0
    am_mid_enr  = mid_am_rate / am_r if am_r else 0

    edy_rate = sum(1 for w in aw if w.endswith('edy') or w.endswith('eedy'))/n
    word_len = sum(len(w) for w in aw)/n
    qok_r = oc_all.get('qok', 0)/n; ch_r = oc_all.get('ch', 0)/n
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r and tb > 0 else 0

    # Menzerath and within-line slope diagnostics
    # Menzerath: correlation between line length (n_words) and mean word length
    line_lens = [len(l) for l in lines if len(l) >= 3]
    line_mean_wl = [sum(len(w) for w in l)/len(l) for l in lines if len(l) >= 3]
    if len(line_lens) > 10:
        mn_ll = sum(line_lens)/len(line_lens); mn_wl = sum(line_mean_wl)/len(line_mean_wl)
        cov = sum((x-mn_ll)*(y-mn_wl) for x,y in zip(line_lens, line_mean_wl))/len(line_lens)
        var_ll = sum((x-mn_ll)**2 for x in line_lens)/len(line_lens)
        menz_r = cov / (var_ll**0.5 * (sum((y-mn_wl)**2 for y in line_mean_wl)/len(line_mean_wl))**0.5) if var_ll > 0 else 0
    else:
        menz_r = 0.0

    # Within-line MID slope: for MID words, regress len(word) on word_index
    idx_lens = []
    for l in lines:
        if len(l) < 4: continue  # need at least 2 MID words
        for j, w in enumerate(l[1:-1]):
            idx_lens.append((j, len(w)))
    if len(idx_lens) > 100:
        n_il = len(idx_lens)
        mean_idx = sum(x for x,y in idx_lens)/n_il
        mean_len = sum(y for x,y in idx_lens)/n_il
        cov_il = sum((x-mean_idx)*(y-mean_len) for x,y in idx_lens)/n_il
        var_il = sum((x-mean_idx)**2 for x,y in idx_lens)/n_il
        mid_slope = cov_il / var_il if var_il > 0 else 0
    else:
        mid_slope = 0.0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch, global_am_rate=am_r,
                menz_r=menz_r, mid_slope=mid_slope)

BATTERY_19 = [
    'am_ll', 'd_ll', 'y_lf', 'ss_mean', 'adj_rate',
    'qok_lf', 'd_lf', 's_lf', 'ch_ll', 'ok_ll',
    'qok_ll', 'ss_d', 'ss_y', 'am_lf_enr',
    'am_mid_enr', 'edy_rate', 'word_len_mean', 'qok_ch',
    'global_am_rate',
]
PASS_TOL = 0.20

VMS_REF = {
    'am_ll': 6.5498, 'd_ll': 1.3625, 'y_lf': 3.1837, 'ss_mean': 1.1640,
    'adj_rate': 0.0090, 'qok_lf': 0.7450, 'd_lf': 2.1178, 's_lf': 4.4422,
    'ch_ll': 0.9653, 'ok_ll': 1.0028, 'qok_ll': 0.6121, 'ss_d': 1.5850,
    'ss_y': 1.9550, 'am_lf_enr': 0.1225, 'am_mid_enr': 0.1954,
    'edy_rate': 0.1940, 'word_len_mean': 5.4000, 'qok_ch': 1.2670,
    'global_am_rate': 0.0203,
    # Diagnostic targets
    'menz_r': -0.206, 'mid_slope': -0.053,
}

def passes(sim_val, vms_val, tol=PASS_TOL):
    if vms_val == 0: return True
    r = sim_val / vms_val
    return (1 - tol) <= r <= (1 + tol)

def agg(metrics_list, key):
    vals = [x[key] for x in metrics_list if key in x]
    return sum(vals) / len(vals) if vals else 0

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

# ─── Setup ────────────────────────────────────────────────────────────────────

print("exp_282: H483 — Word-Index-Conditioned MID Generation")
print("=" * 65)

print("Parsing VMS B-dialect corpus...")
b_lines = parse_vms_b()
vms = compute_vms_distributions(b_lines)
print(f"  VMS B: {len(b_lines)} lines, {vms['n']} words, {vms['n_mid']} MID words")

# Measure VMS baseline Menzerath and slope
bl_metrics = compute_metrics(b_lines)
print(f"  VMS Menzerath r = {bl_metrics['menz_r']:.4f} (target: -0.206)")
print(f"  VMS MID slope = {bl_metrics['mid_slope']:.4f} (target: -0.053)")

print("\nLoading Latin corpus...")
latin_words = load_latin(LATIN_CORPUS)
print(f"  {len(latin_words)} Latin words loaded.")

# Build derived distributions
suffix_global = vms['suffix_global']
suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
onset_lf_vms = vms['onset_lf']; onset_ll_vms = vms['onset_ll']; onset_mid = vms['onset_mid']
d_global = vms['onset_global'].get('d', 0)
d_ll_non_blind_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0
d_boost_weight = compute_d_boost(d_global, vms['d_ll_target'], d_ll_non_blind_enr, P_BLIND)
d_boost_weight = max(0.0, min(d_boost_weight, 1.0))
ll_onsets = build_ll_onsets(onset_ll_vms, d_boost_weight)
non_empty_midfix_dist = vms['non_empty_midfix_dist']

# ─── Part 1: Gamma sweep (alpha=0) ─────────────────────────────────────────

print(f"\n{'='*70}")
print(f"PART 1: Gamma sweep (alpha=0) — N={N_SWEEP} each")
print(f"{'='*70}")
print(f"  {'gamma':>7}  {'PASS/19':>8}  {'menz_r':>8}  {'mid_slope':>10}  {'word_len':>9}")
print(f"  {'-'*52}")

best_gamma = 0.0; best_menz_r = 999
gamma_results = {}

for gamma in [0.00, 0.05, 0.10, 0.20, 0.30]:
    metrics_list = []
    for run in range(N_SWEEP):
        rng = random.Random(SEED + int(gamma*100) + run*1000)
        lines = run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf_vms, onset_ll_vms, non_empty_midfix_dist,
                        gamma, 0.0, rng)
        m = compute_metrics(lines)
        if m: metrics_list.append(m)

    if not metrics_list: continue

    pass_count = sum(
        1 for metric in BATTERY_19
        if passes(agg(metrics_list, metric), VMS_REF[metric])
    )
    mr = agg(metrics_list, 'menz_r')
    ms = agg(metrics_list, 'mid_slope')
    wl = agg(metrics_list, 'word_len_mean')
    gamma_results[gamma] = {'pass': pass_count, 'menz_r': mr, 'mid_slope': ms, 'word_len': wl}
    print(f"  {gamma:>7.2f}  {pass_count:>5}/19  {mr:>8.4f}  {ms:>10.4f}  {wl:>9.3f}")
    if pass_count == 19 and abs(mr - VMS_REF['menz_r']) < abs(best_menz_r - VMS_REF['menz_r']):
        best_gamma = gamma; best_menz_r = mr

viable_gammas = [(g, r) for g, r in gamma_results.items() if r['pass'] == 19]
if viable_gammas:
    # Among 19/19, pick closest menz_r to VMS -0.206
    viable_gammas.sort(key=lambda x: abs(x[1]['menz_r'] - VMS_REF['menz_r']))
    best_gamma = viable_gammas[0][0]
    print(f"\n  Best gamma (19/19, closest menz_r) = {best_gamma}")
else:
    best_gamma = max(gamma_results.keys(), key=lambda g: gamma_results[g]['pass'])
    print(f"\n  No 19/19. Best gamma by pass count = {best_gamma}")

# ─── Part 2: Alpha sweep (at best_gamma) ───────────────────────────────────

print(f"\n{'='*70}")
print(f"PART 2: Alpha sweep (gamma={best_gamma}) — N={N_SWEEP} each")
print(f"{'='*70}")
print(f"  {'alpha':>7}  {'PASS/19':>8}  {'menz_r':>8}  {'mid_slope':>10}  {'word_len':>9}")
print(f"  {'-'*52}")

best_alpha = 0.0; best_menz_r2 = gamma_results.get(best_gamma, {}).get('menz_r', 999)
alpha_results = {}

for alpha in [0.00, 0.05, 0.10, 0.15, 0.20]:
    metrics_list = []
    for run in range(N_SWEEP):
        rng = random.Random(SEED + 500000 + int(alpha*100) + run*1000)
        lines = run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf_vms, onset_ll_vms, non_empty_midfix_dist,
                        best_gamma, alpha, rng)
        m = compute_metrics(lines)
        if m: metrics_list.append(m)

    if not metrics_list: continue

    pass_count = sum(
        1 for metric in BATTERY_19
        if passes(agg(metrics_list, metric), VMS_REF[metric])
    )
    mr = agg(metrics_list, 'menz_r')
    ms = agg(metrics_list, 'mid_slope')
    wl = agg(metrics_list, 'word_len_mean')
    alpha_results[alpha] = {'pass': pass_count, 'menz_r': mr, 'mid_slope': ms, 'word_len': wl}
    print(f"  {alpha:>7.2f}  {pass_count:>5}/19  {mr:>8.4f}  {ms:>10.4f}  {wl:>9.3f}")
    if pass_count == 19 and abs(mr - VMS_REF['menz_r']) < abs(best_menz_r2 - VMS_REF['menz_r']):
        best_alpha = alpha; best_menz_r2 = mr

viable_alphas = [(a, r) for a, r in alpha_results.items() if r['pass'] == 19]
if viable_alphas:
    viable_alphas.sort(key=lambda x: abs(x[1]['menz_r'] - VMS_REF['menz_r']))
    best_alpha = viable_alphas[0][0]
    print(f"\n  Best alpha (19/19, closest menz_r) = {best_alpha}")
else:
    best_alpha = max(alpha_results.keys(), key=lambda a: alpha_results[a]['pass'])
    print(f"\n  No 19/19. Best alpha by pass count = {best_alpha}")

# ─── Part 3: Full run ────────────────────────────────────────────────────────

print(f"\n{'='*70}")
print(f"FULL RUN: gamma={best_gamma}, alpha={best_alpha}, N={N_FULL}")
print(f"{'='*70}")

full_metrics = []
for run in range(N_FULL):
    rng = random.Random(SEED + 999000 + run*1000)
    lines = run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf_vms, onset_ll_vms, non_empty_midfix_dist,
                    best_gamma, best_alpha, rng)
    m = compute_metrics(lines)
    if m: full_metrics.append(m)

print(f"\n  19-Metric Battery (gamma={best_gamma}, alpha={best_alpha}, N={N_FULL}):")
print(f"  {'Metric':<20} {'VMS':>8} {'Sim':>8} {'%VMS':>7}  Status")
print(f"  {'-'*55}")
total_pass = 0
for metric in BATTERY_19:
    vms_val = VMS_REF[metric]
    sim_val = agg(full_metrics, metric)
    pct = 100 * sim_val / vms_val if vms_val else 0
    status = 'PASS' if passes(sim_val, vms_val) else 'FAIL'
    if status == 'PASS': total_pass += 1
    print(f"  {metric:<20} {vms_val:>8.4f} {sim_val:>8.4f} {pct:>6.1f}%  {status}")

print(f"\n  TOTAL PASS: {total_pass}/19")

# Diagnostic metrics
menz_r_full = agg(full_metrics, 'menz_r')
slope_full  = agg(full_metrics, 'mid_slope')
print(f"\n  DIAGNOSTIC (not in battery):")
print(f"  Menzerath r: sim={menz_r_full:.4f}, VMS={VMS_REF['menz_r']:.4f}, "
      f"ratio={menz_r_full/VMS_REF['menz_r']:.3f}")
print(f"  MID slope:   sim={slope_full:.4f}, VMS={VMS_REF['mid_slope']:.4f}, "
      f"ratio={slope_full/VMS_REF['mid_slope']:.3f}")

print(f"\nDone.")
