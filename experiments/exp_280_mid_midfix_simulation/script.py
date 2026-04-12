"""
exp_280: H484 — Midfix Sampling for MID Words

Question: Does adding midfix sampling to MID word generation expand vocabulary
toward VMS levels while maintaining the 19-metric battery?

Background:
- exp_279 (F279): 62-71% of VMS MID words have midfixes; simulation generates only
  194-223 unique types vs VMS 2036-2929 (10-15× gap). Root cause: no midfix in MID.
- exp_270 (F270): midfix added to LF/LL — same framework should work for MID words.
- VMS MID midfix distribution (from exp_279 analysis):
  B-dialect: empty midfix 53.2%, non-empty 46.8%; mean non-empty = 2.14 chars; mean all = 1.00 char
  A-dialect: empty midfix 47.8%, non-empty 52.2%; mean non-empty = 2.28 chars; mean all = 1.19 char
  Top midfixes (B): 'e' (9%), 'ch' (5.5%), 'k' (3.7%), 'ed' (1.9%), 'd' (1.6%), 'pch' (1.5%)...

Design:
- Part 1: Measure vocabulary expansion as a function of midfix sampling rate
  Sweep midfix presence probability p_mf ∈ {0.0, 0.2, 0.3, 0.4, 0.5} for B-dialect
  Report: unique types, TTR, word_len_mean, edy_rate
- Part 2: At the best p_mf (word_len_mean within target ±20%), run full 19-metric battery
  The key calibration challenge: adding midfix increases word_len_mean → may require
  recalibrating (lower suffix lengths or offset mu_len)
- Part 3: Compare to VMS vocabulary: does the vocabulary size approach VMS levels?

Implementation:
- Build midfix distribution from VMS MID words (recognized suffix only)
- For each simulated MID word: sample onset + suffix (existing) + midfix (new)
- Midfix applied with probability p_mf; sampled from empirical distribution
- Word structure: onset + midfix + suffix (or onset + midfix + connector + suffix for edy)
"""

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIM    = 5     # runs per p_mf value
N_FULL   = 30    # for best p_mf
TARGET_LINES = 2411  # B-dialect line count
WINDOW   = 20
SEED     = 280000

# B-dialect 12-mechanism parameters (frozen at exp_257 values)
P_BLIND   = 0.115; P_LF    = 1.0;   CP       = 0.55; MP       = 0.90
P_QOKCH   = 0.12;  P_CHQOK = 0.12;  P_STUTTER = 0.006
R_LF      = 0.12;  R_MID   = 0.25;  MU_LEN   = 8.4;  SIGMA_LEN = 3.0

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

    # Build MID midfix distribution (recognized suffix only)
    midfixes = []
    for w in mid_words:
        onset = get_onset(w); suf = get_suffix(w)
        if onset == 'other' or suf == 'other': continue
        onset_len = get_onset_len(w); suf_len = len(suf)
        midfix = w[onset_len:len(w)-suf_len] if onset_len + suf_len <= len(w) else ''
        midfixes.append(midfix)
    midfix_cnt = Counter(midfixes)
    total_mf = sum(midfix_cnt.values())
    midfix_dist = {mf: cnt/total_mf for mf, cnt in midfix_cnt.items()} if total_mf else {}
    # Separate empty and non-empty
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
        'midfix_dist': midfix_dist, 'non_empty_midfix_dist': non_empty_dist,
        'p_empty_midfix': p_empty_midfix,
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
    """Sample a midfix string. With prob p_non_empty, sample from non-empty distribution; else return ''."""
    if rng.random() < p_non_empty:
        return weighted_choice(rng, non_empty_dist)
    return ''

def make_word_sim(onset, suffix, rng, non_empty_midfix_dist, p_midfix_present):
    """Generate a simulated word with optional midfix."""
    if suffix == 'other':
        # For 'other' suffix — use simple 5-char placeholder as before, no midfix
        return onset + suffix
    midfix = sample_midfix(rng, non_empty_midfix_dist, p_midfix_present)
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        # edy/eedy suffix uses connector logic (which is like a midfix itself)
        connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
        return onset + midfix + connector + suffix
    return onset + midfix + suffix

def random_eva_word(onset_weights, suffix_weights, rng, non_empty_midfix_dist, p_midfix_present):
    onset  = weighted_choice(rng, onset_weights)
    suffix = weighted_choice(rng, suffix_weights)
    return make_word_sim(onset, suffix, rng, non_empty_midfix_dist, p_midfix_present)

def cipher_ll(onset_ll_vms, ll_onsets, suffix_global, p_blind, rng):
    if rng.random() < p_blind:
        onset = weighted_choice(rng, ll_onsets)
        return onset + 'am'
    onset  = weighted_choice(rng, onset_ll_vms)
    suffix = weighted_choice(rng, suffix_global)
    return make_word_sim(onset, suffix, rng, {}, 0.0)  # no midfix for LF/LL

def cipher_lf(onset_mid, onset_lf_vms, suffix_lf, p_lf, rng):
    if rng.random() < p_lf:
        onset  = weighted_choice(rng, onset_lf_vms)
        suffix = weighted_choice(rng, suffix_lf)
        return make_word_sim(onset, suffix, rng, {}, 0.0)  # no midfix for LF
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

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms, non_empty_midfix_dist, p_midfix_present, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    while len(lines) < TARGET_LINES and pos < len(w) - 2:
        n = max(2, min(20, round(rng.gauss(MU_LEN, SIGMA_LEN))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf(onset_mid, onset_lf_vms, suffix_lf_sup, P_LF, rng)
            elif i == len(chunk) - 1:
                ew = cipher_ll(onset_ll_vms, ll_onsets, suffix_global, P_BLIND, rng)
            else:
                if prev_word is not None and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf(buf, prev_onset, P_QOKCH, P_CHQOK, rng)
                    if rng.random() < MP:
                        ew = timm_modify(src, onset_mid, suffix_mid_sup, rng)
                    else:
                        ew = src
                else:
                    ew = random_eva_word(onset_mid, suffix_mid_sup, rng, non_empty_midfix_dist, p_midfix_present)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

def compute_metrics(lines, VMS_REF):
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

    # Vocabulary metrics (diagnostics)
    mid_types = len(set(mid))
    mid_ttr = mid_types / n_mid if n_mid else 0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch, global_am_rate=am_r,
                mid_types=mid_types, mid_ttr=mid_ttr)

BATTERY_19 = [
    'am_ll', 'd_ll', 'y_lf', 'ss_mean', 'adj_rate',
    'qok_lf', 'd_lf', 's_lf', 'ch_ll', 'ok_ll',
    'qok_ll', 'ss_d', 'ss_y', 'am_lf_enr',
    'am_mid_enr', 'edy_rate', 'word_len_mean', 'qok_ch',
    'global_am_rate',
]
PASS_TOL = 0.20

def passes(sim_val, vms_val, tol=PASS_TOL):
    if vms_val == 0: return True
    r = sim_val / vms_val
    return (1 - tol) <= r <= (1 + tol)

def agg(metrics_list, key):
    vals = [x[key] for x in metrics_list]
    return sum(vals) / len(vals)

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

print("exp_280: H484 — Midfix Sampling for MID Words")
print("=" * 65)

print("Parsing VMS B-dialect corpus...")
b_lines = parse_vms_b()
vms = compute_vms_distributions(b_lines)
print(f"  VMS B: {len(b_lines)} lines, {vms['n']} words, {vms['n_mid']} MID words")

mid_vms = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
print(f"  VMS MID unique types: {len(set(mid_vms))}, TTR={len(set(mid_vms))/len(mid_vms):.3f}")
print(f"  VMS MID midfix: p_empty={vms['p_empty_midfix']:.3f}, p_non_empty={1-vms['p_empty_midfix']:.3f}")
print(f"  Non-empty midfix count: {len(vms['non_empty_midfix_dist'])}")
top10_mf = sorted(vms['non_empty_midfix_dist'].items(), key=lambda x: -x[1])[:10]
print(f"  Top-10 non-empty midfixes: {[(repr(m), f'{p:.3f}') for m, p in top10_mf]}")

d_global = vms['onset_global'].get('d', 0)
d_ll_non_blind_enr = vms['onset_ll'].get('d', 0) / d_global if d_global else 0
d_boost = compute_d_boost(d_global, vms['d_ll_target'], d_ll_non_blind_enr, P_BLIND)
ll_onsets   = build_ll_onsets(vms['onset_ll'], d_boost)
onset_ll_vms = dict(vms['onset_ll'])
onset_lf_vms = dict(vms['onset_lf'])
onset_mid    = dict(vms['onset_mid'])
suffix_global = dict(vms['suffix_global'])
suffix_lf_sup  = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
non_empty_midfix_dist = dict(vms['non_empty_midfix_dist'])

VMS_REF = {
    'am_ll':         vms['am_ll_target'],
    'd_ll':          vms['d_ll_target'],
    'y_lf':          vms['onset_lf'].get('y',0) / vms['onset_global'].get('y',0.001),
    'ss_mean':       1.164,
    'adj_rate':      0.009,
    'qok_lf':        vms['onset_lf'].get('qok',0) / vms['onset_global'].get('qok',0.001),
    'd_lf':          vms['onset_lf'].get('d',0) / vms['onset_global'].get('d',0.001),
    's_lf':          vms['onset_lf'].get('s',0) / vms['onset_global'].get('s',0.001),
    'ch_ll':         vms['onset_ll'].get('ch',0) / vms['onset_global'].get('ch',0.001),
    'ok_ll':         vms['onset_ll'].get('ok',0) / vms['onset_global'].get('ok',0.001),
    'qok_ll':        vms['onset_ll'].get('qok',0) / vms['onset_global'].get('qok',0.001),
    'ss_d':          1.585,
    'ss_y':          1.955,
    'am_lf_enr':     vms['am_lf_enr'],
    'am_mid_enr':    vms['am_mid_enr'],
    'edy_rate':      sum(vms['suffix_global'].get(s,0) for s in ['edy','eedy']),
    'word_len_mean': 5.400,
    'qok_ch':        1.267,
    'global_am_rate': vms['am_r'],
}

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")

# ─── Sweep: midfix presence probability ───────────────────────────────────────

P_MIDFIX_VALUES = [0.00, 0.10, 0.20, 0.30, 0.40]
# p_midfix_present = probability that a MID word (non-edy non-other suffix) gets a non-empty midfix

print(f"\n{'='*70}")
print("SWEEP: p_midfix_present ∈ {0.00, 0.10, 0.20, 0.30, 0.40} — N=5 each")
print(f"{'='*70}")
print(f"  {'p_mf':>6}  {'PASS/19':>8}  {'word_len':>10}  {'mid_types':>10}  {'mid_TTR':>8}  {'word_len %VMS':>13}")
print(f"  {'-'*60}")

sweep_results = {}
for p_mf in P_MIDFIX_VALUES:
    results = []
    for trial in range(N_SIM):
        rng_t = random.Random(SEED + int(p_mf * 1000) + trial * 100)
        lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf_vms, onset_ll_vms, non_empty_midfix_dist, p_mf, rng_t)
        m = compute_metrics(lines, VMS_REF)
        if m: results.append(m)

    if not results: continue
    mean_m = {k: agg(results, k) for k in results[0]}
    pass_count = sum(1 for metric in BATTERY_19 if passes(mean_m[metric], VMS_REF[metric]))
    sweep_results[p_mf] = (pass_count, mean_m)
    wl_pct = mean_m['word_len_mean'] / VMS_REF['word_len_mean'] * 100
    print(f"  {p_mf:>6.2f}  {pass_count:>5}/19  {mean_m['word_len_mean']:>10.3f}  "
          f"{int(mean_m['mid_types']):>10}  {mean_m['mid_ttr']:>8.3f}  {wl_pct:>12.1f}%")

# ─── Determine best viable p_mf ─────────────────────────────────────────────

# Best: 19/19 PASS + word_len_mean within ±20% of VMS + maximum mid_types
best_p = 0.00; best_types = 0
for p, (pc, mm) in sweep_results.items():
    if pc < 19: continue
    if not passes(mm['word_len_mean'], VMS_REF['word_len_mean']): continue
    if mm['mid_types'] > best_types:
        best_types = mm['mid_types']; best_p = p

print(f"\n  Best viable p_mf = {best_p:.2f} (19/19 PASS + word_len within ±20%, max mid_types={best_types:.0f})")

# ─── Full Run at best p_mf ─────────────────────────────────────────────────

print(f"\n{'='*70}")
print(f"FULL RUN: p_mf = {best_p:.2f}, N={N_FULL}")
print(f"{'='*70}")

full_results = []
for trial in range(N_FULL):
    rng_t = random.Random(SEED + 90000 + trial * 100)
    lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf_vms, onset_ll_vms, non_empty_midfix_dist, best_p, rng_t)
    m = compute_metrics(lines, VMS_REF)
    if m: full_results.append(m)

mean_full = {k: agg(full_results, k) for k in full_results[0]}
pass_full  = sum(1 for metric in BATTERY_19 if passes(mean_full[metric], VMS_REF[metric]))

print(f"\n  19-Metric Battery (p_mf={best_p:.2f}, N={N_FULL}):")
print(f"  {'Metric':<16} {'VMS':>8} {'Sim':>8} {'%VMS':>8}  Status")
print(f"  {'-'*55}")
for metric in BATTERY_19:
    vref = VMS_REF[metric]; sval = mean_full[metric]
    pct  = sval / vref * 100 if vref else 0
    ok   = passes(sval, vref)
    flag = 'PASS' if ok else 'FAIL'
    print(f"  {metric:<16} {vref:>8.4f} {sval:>8.4f} {pct:>8.1f}%  {flag}")

print(f"\n  TOTAL PASS: {pass_full}/19")
print(f"  MID vocab: types={mean_full['mid_types']:.0f} (VMS {len(set(mid_vms))}), "
      f"TTR={mean_full['mid_ttr']:.3f} (VMS {len(set(mid_vms))/len(mid_vms):.3f})")

print("\nDone.")
