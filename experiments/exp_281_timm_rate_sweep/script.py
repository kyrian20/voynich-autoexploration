"""
exp_281: H485 — Timm Modification Rate Sweep

Question: Does reducing the Timm modification rate MP (currently 0.90) bring
simulation MID vocabulary closer to VMS levels (2929 types) while maintaining 19/19?

Background:
- exp_280 (F280): Full simulation at p_mf=0.20 generates 6458 unique MID types
  (TTR=0.419) vs VMS 2929 (TTR=0.211) — 2.2× over VMS. Even at p_mf=0.00,
  the full simulation generates 5255 types (1.8× VMS).
- Root cause: Timm modification at MP=0.90 (replace/insert/delete one char
  from 16-char EVA alphabet) generates a combinatorial explosion of unique
  word forms from buffer words.
- MP=0.90 was originally calibrated to satisfy bigram succession metrics
  (qok↔ch, qok→qok). Reducing MP may affect those metrics.

Design:
- Part 1: Sweep MP ∈ {0.50, 0.60, 0.70, 0.80, 0.90} at N=10 each (p_mf=0.20)
  Report: PASS/19, mid_types, mid_TTR, word_len_mean, qok_ch (key bigram)
- Part 2: At best MP, run N=30 full battery
- Key calibration question: which bigram metrics degrade when MP is reduced?
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SWEEP  = 10    # runs per MP value in sweep
N_FULL   = 30    # for best MP
TARGET_LINES = 2411  # B-dialect line count
WINDOW   = 20
SEED     = 281000

# B-dialect 12-mechanism parameters (frozen at exp_257 values)
P_BLIND   = 0.115; P_LF    = 1.0;   CP       = 0.55
P_QOKCH   = 0.12;  P_CHQOK = 0.12;  P_STUTTER = 0.006
R_LF      = 0.12;  R_MID   = 0.25;  MU_LEN   = 8.4;  SIGMA_LEN = 3.0
P_MF      = 0.20   # best midfix rate from exp_280

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
    """Parse B-dialect lines from ZL3b transcription using edy/eedy dialect classifier."""
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
    lf_words  = [l[0]      for l in b_lines if l]
    ll_words  = [l[-1]     for l in b_lines if len(l) > 1]
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words); n_mid = len(mid_words)

    def dist(words, filter_other=False):
        cnt = Counter(get_onset(w) for w in words)
        if filter_other: cnt.pop('other', None)
        total = sum(cnt.values())
        return {k: v/total for k, v in cnt.items()} if total else {}

    onset_global = dist(all_words)
    onset_lf     = dist(lf_words, filter_other=True)
    onset_ll     = dist(ll_words)
    onset_mid    = dist(mid_words, filter_other=True)

    suffix_cnt = Counter(get_suffix(w) for w in all_words)
    suffix_total = sum(suffix_cnt.values())
    suffix_global = {s: c/suffix_total for s, c in suffix_cnt.items()}

    # Midfix distribution (from MID words with recognized suffix)
    midfix_cnt = Counter()
    for w in mid_words:
        onset = get_onset(w); suf = get_suffix(w)
        if onset == 'other' or suf == 'other': continue
        onset_len = get_onset_len(w); suf_len = len(suf)
        if edy_len := get_edy_suffix_len(w):
            # midfix = word[onset_len : len(w)-edy_len - connector_len]
            # connector is 1-2 chars before edy/eedy
            mid_end = len(w) - edy_len
            # conservative: don't extract midfix from edy words (connector ambiguous)
            midfix = w[onset_len:mid_end]
            # strip likely connector (1 char min)
            if len(midfix) >= 1:
                midfix = midfix[:-1]  # remove connector char
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

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms, non_empty_midfix_dist,
            p_midfix_present, mp, rng):
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
                    if rng.random() < mp:
                        ew = timm_modify(src, onset_mid, suffix_mid_sup, rng)
                    else:
                        ew = src
                else:
                    ew = random_eva_word(onset_mid, suffix_mid_sup, rng,
                                        non_empty_midfix_dist, p_midfix_present)
                buf.append(ew)
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

VMS_REF = {
    'am_ll': 6.5498, 'd_ll': 1.3625, 'y_lf': 3.1837, 'ss_mean': 1.1640,
    'adj_rate': 0.0090, 'qok_lf': 0.7450, 'd_lf': 2.1178, 's_lf': 4.4422,
    'ch_ll': 0.9653, 'ok_ll': 1.0028, 'qok_ll': 0.6121, 'ss_d': 1.5850,
    'ss_y': 1.9550, 'am_lf_enr': 0.1225, 'am_mid_enr': 0.1954,
    'edy_rate': 0.1940, 'word_len_mean': 5.4000, 'qok_ch': 1.2670,
    'global_am_rate': 0.0203,
}

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

print("exp_281: H485 — Timm Modification Rate Sweep")
print("=" * 65)

print("Parsing VMS B-dialect corpus...")
b_lines = parse_vms_b()
vms = compute_vms_distributions(b_lines)
print(f"  VMS B: {len(b_lines)} lines, {vms['n']} words, {vms['n_mid']} MID words")
print(f"  VMS MID unique types: {len(set(w for l in b_lines for w in l[1:-1] if len(l)>2))}, "
      f"TTR={len(set(w for l in b_lines for w in l[1:-1] if len(l)>2))/vms['n_mid']:.3f}")

print("\nLoading Latin corpus...")
latin_words = load_latin(LATIN_CORPUS)
print(f"  {len(latin_words)} Latin words loaded.")

# Build derived distributions
suffix_global = vms['suffix_global']
suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)

onset_lf_vms = vms['onset_lf']
onset_ll_vms = vms['onset_ll']
onset_mid    = vms['onset_mid']

d_global = vms['onset_global'].get('d', 0)
d_ll_non_blind_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0
d_boost_weight = compute_d_boost(d_global, vms['d_ll_target'], d_ll_non_blind_enr, P_BLIND)
d_boost_weight = max(0.0, min(d_boost_weight, 1.0))
ll_onsets = build_ll_onsets(onset_ll_vms, d_boost_weight)

non_empty_midfix_dist = vms['non_empty_midfix_dist']

print(f"\n{'='*70}")
print(f"SWEEP: MP ∈ {{0.50, 0.60, 0.70, 0.80, 0.90}} — N={N_SWEEP} each (p_mf={P_MF})")
print(f"{'='*70}")
print(f"  {'MP':>6}  {'PASS/19':>8}  {'word_len':>9}  {'mid_types':>10}  {'mid_TTR':>8}  {'qok_ch':>8}  {'ss_mean':>8}")
print(f"  {'-'*70}")

best_mp = 0.90
best_pass = 0
mp_results = {}

for mp in [0.50, 0.60, 0.70, 0.80, 0.90]:
    rng = random.Random(SEED + int(mp*100))
    metrics_list = []
    for run in range(N_SWEEP):
        rng2 = random.Random(SEED + int(mp*100) + run*1000)
        lines = run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets, onset_lf_vms, onset_ll_vms, non_empty_midfix_dist,
                        P_MF, mp, rng2)
        m = compute_metrics(lines)
        if m: metrics_list.append(m)

    if not metrics_list: continue

    pass_count = sum(
        1 for metric in BATTERY_19
        if passes(agg(metrics_list, metric), VMS_REF[metric])
    )
    wl   = agg(metrics_list, 'word_len_mean')
    mt   = agg(metrics_list, 'mid_types')
    ttr  = agg(metrics_list, 'mid_ttr')
    qch  = agg(metrics_list, 'qok_ch')
    ss   = agg(metrics_list, 'ss_mean')
    mp_results[mp] = {'pass': pass_count, 'word_len': wl, 'mid_types': mt,
                      'ttr': ttr, 'qok_ch': qch, 'ss_mean': ss}
    print(f"  {mp:>6.2f}  {pass_count:>5}/19  {wl:>9.3f}  {mt:>10.0f}  {ttr:>8.3f}  {qch:>8.4f}  {ss:>8.4f}")
    if pass_count >= best_pass:
        best_pass = pass_count
        best_mp = mp

# Find best MP that maximizes PASS while minimizing mid_types (closest to VMS 2929)
# PASS must be 19/19; among those, pick minimum mid_types
viable_mps = [(mp, res) for mp, res in mp_results.items() if res['pass'] == 19]
if viable_mps:
    # Among 19/19, pick lowest mid_types (closest to VMS 2929)
    viable_mps.sort(key=lambda x: x[1]['mid_types'])
    best_mp = viable_mps[0][0]
    print(f"\n  Best viable MP = {best_mp} ({mp_results[best_mp]['pass']}/19 PASS, "
          f"mid_types={mp_results[best_mp]['mid_types']:.0f}, closest to VMS 2929)")
else:
    # No 19/19 — pick highest pass count
    viable_mps = sorted(mp_results.items(), key=lambda x: -x[1]['pass'])
    best_mp = viable_mps[0][0]
    print(f"\n  No 19/19 found. Best MP = {best_mp} ({mp_results[best_mp]['pass']}/19)")

print(f"\n{'='*70}")
print(f"FULL RUN: MP = {best_mp}, N={N_FULL}")
print(f"{'='*70}")

full_metrics = []
for run in range(N_FULL):
    rng = random.Random(SEED + 999000 + run*1000)
    lines = run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf_vms, onset_ll_vms, non_empty_midfix_dist,
                    P_MF, best_mp, rng)
    m = compute_metrics(lines)
    if m: full_metrics.append(m)

print(f"\n  19-Metric Battery (MP={best_mp}, N={N_FULL}):")
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
print(f"  MID vocab: types={agg(full_metrics,'mid_types'):.0f} (VMS 2929), "
      f"TTR={agg(full_metrics,'mid_ttr'):.3f} (VMS 0.211)")
print(f"  qok_ch (key metric): {agg(full_metrics,'qok_ch'):.4f} (VMS {VMS_REF['qok_ch']:.4f})")
print(f"  ss_mean: {agg(full_metrics,'ss_mean'):.4f} (VMS {VMS_REF['ss_mean']:.4f})")
print(f"\nDone.")
