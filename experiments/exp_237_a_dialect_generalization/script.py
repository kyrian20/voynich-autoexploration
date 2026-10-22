"""
exp_237: H437 — A-Dialect Generalization

Question: Does the Mode B architecture (exp_236, 19/19 B-dialect PASS) generalize to
A-dialect VMS? Which of the 19 metrics transfer, and which require dialect-specific
recalibration?

Design:
  Two conditions:
  (A) Direct transfer: exp_236 B-calibrated params (p_blind=0.115, r_lf=0.12, r_mid=0.25,
      d_boost=9.13%) applied with A-dialect onset/suffix distributions.
      Establishes: which metrics pass without any recalibration.
  (B) Recalibrated transfer: p_blind analytically derived for A-dialect LL_am;
      d_boost analytically recalibrated for A-dialect d_ll; r_lf/r_mid swept.
      Structural params (cp, mp, p_qokch, p_stutter) TRANSFERRED unchanged from B.
      Establishes: which metrics pass with dialect-specific calibration of am/d params only.

A-dialect analytical derivation:
  A global_am ≈ 1.98%; A LL_am_rate ≈ 6.93%
  p_blind_A = (0.0693 - 0.0198) / (1 - 0.0198) ≈ 0.0505

Key question (user directive):
  If the same architecture with different p_blind and p_lf values reproduces A-dialect,
  the mechanism is more general than a B-specific fit.

Structural params transferred: cp=0.55, mp=0.90, p_qokch=0.12, p_stutter=0.006
Corpus: A-dialect VMS (folio-classified, P lines only, same filter as B)
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SWEEP  = 5
N_FULL   = 30
WINDOW   = 20
SEED     = 237000

# Structural params TRANSFERRED from exp_236 B-dialect (not recalibrated)
CP          = 0.55
MP          = 0.90
P_QOKCH     = 0.12
P_STUTTER   = 0.006
P_LF        = 1.0
PASS_TOL    = 0.20

# B-calibrated am params (for direct-transfer condition A)
P_BLIND_B   = 0.115
R_LF_B      = 0.12
R_MID_B     = 0.25

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

def parse_vms_both_dialects():
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
    lines_by_dialect = {'A': [], 'B': []}
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            dialect = folio_dialect.get(fb, 'unknown')
            if dialect not in ('A', 'B'): continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: lines_by_dialect[dialect].append(words)
    return lines_by_dialect

def compute_vms_distributions(dialect_lines):
    all_words = [w for l in dialect_lines for w in l]
    lf_words  = [l[0]  for l in dialect_lines if l]
    ll_words  = [l[-1] for l in dialect_lines if len(l) > 1]
    mid_words = [w for l in dialect_lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words); n_mid = len(mid_words)

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
    ll_am_rate = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words) if ll_words else 0
    lf_am_rate = sum(1 for w in lf_words if w.endswith('am')) / len(lf_words) if lf_words else 0
    mid_am_rate = sum(1 for w in mid_words if w.endswith('am')) / n_mid if n_mid else 0

    d_r   = oc_all.get('d', 0) / n
    ll_d  = oc_ll.get('d', 0) / len(ll_words) if ll_words else 0

    # Bigrams for ss metrics
    tb = n - 1
    bg = Counter((get_onset(all_words[i]), get_onset(all_words[i+1])) for i in range(tb))
    def ss_corpus(o):
        b = oc_all.get(o, 0)/n
        return bg.get((o,o),0)/(tb*b*b) if b>0 else 1.0
    ss_mean_corpus = (ss_corpus('qok')+ss_corpus('ok')+ss_corpus('ch'))/3
    ss_d_corpus    = ss_corpus('d')
    ss_y_corpus    = ss_corpus('y')

    adj_corpus = sum(1 for i in range(tb) if all_words[i]==all_words[i+1])/max(1,tb)

    word_len_corpus = sum(len(w) for w in all_words)/n

    qok_r = oc_all.get('qok', 0)/n; ch_r = oc_all.get('ch', 0)/n
    qok_ch_corpus = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    def enr(onset, ctr_slot, n_slot, ctr_all, n_all):
        s = ctr_slot.get(onset, 0)/n_slot if n_slot else 0
        g = ctr_all.get(onset, 0)/n_all if n_all else 0
        return s/g if g>0 else 0

    edy_rate_corpus = sum(1 for w in all_words if w.endswith('edy'))/n

    return {
        'onset_global': onset_global, 'onset_lf': onset_lf,
        'onset_ll': onset_ll, 'onset_mid': onset_mid,
        'suffix_global': suffix_global,
        'am_r': am_r, 'll_am_rate': ll_am_rate, 'lf_am_rate': lf_am_rate, 'mid_am_rate': mid_am_rate,
        'am_ll_target': ll_am_rate/am_r if am_r else 0,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words), 'n_mid': n_mid,
        'n_lines': len(dialect_lines),
        # VMS-computed metric targets
        'ss_mean_corpus': ss_mean_corpus,
        'ss_d_corpus':    ss_d_corpus,
        'ss_y_corpus':    ss_y_corpus,
        'adj_corpus':     adj_corpus,
        'word_len_corpus': word_len_corpus,
        'qok_ch_corpus':  qok_ch_corpus,
        'edy_rate_corpus': edy_rate_corpus,
        'am_lf_enr_corpus': lf_am_rate/am_r if am_r else 0,
        'am_mid_enr_corpus': mid_am_rate/am_r if am_r else 0,
        # Onset enrichment ratios
        'qok_lf': enr('qok', oc_lf, len(lf_words), oc_all, n),
        'd_lf':   enr('d',   oc_lf, len(lf_words), oc_all, n),
        's_lf':   enr('s',   oc_lf, len(lf_words), oc_all, n),
        'y_lf':   enr('y',   oc_lf, len(lf_words), oc_all, n),
        'ch_ll':  enr('ch',  oc_ll, len(ll_words),  oc_all, n),
        'ok_ll':  enr('ok',  oc_ll, len(ll_words),  oc_all, n),
        'qok_ll': enr('qok', oc_ll, len(ll_words),  oc_all, n),
    }

def make_suppressed_suffix(suffix_global, r_am):
    am_weight = suffix_global.get('am', 0.0)
    new_am = am_weight * r_am
    delta = am_weight - new_am
    non_am_total = 1.0 - am_weight
    suppressed = {}
    for suf, w in suffix_global.items():
        if suf == 'am':
            suppressed[suf] = new_am
        else:
            suppressed[suf] = w + (w / non_am_total) * delta if non_am_total > 0 else w
    return suppressed

def build_ll_onsets_fixed(onset_ll_vms, d_boost_weight):
    remaining_weight = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll_vms.items() if o != 'd'}
    base_total = sum(base.values())
    normalized = {o: v/base_total * remaining_weight for o, v in base.items()} if base_total > 0 else {}
    normalized['d'] = d_boost_weight
    return normalized

def compute_d_boost_fixed(d_global, d_ll_target, d_ll_non_blind, p_blind):
    """d_boost for the blind LL fraction to achieve d_ll_target overall."""
    return d_global * (d_ll_target - (1-p_blind) * d_ll_non_blind) / p_blind

def make_word_sim(onset, suffix, rng):
    """edy-conditional connector (same as exp_236)."""
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
        return onset + connector + suffix
    else:
        return onset + suffix

def random_eva_word(onset_weights, suffix_weights, rng):
    onset  = rng.choices(list(onset_weights.keys()),  weights=list(onset_weights.values()))[0]
    suffix = rng.choices(list(suffix_weights.keys()), weights=list(suffix_weights.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_ll_blind_fixed(onset_weights_mid, suffix_global, ll_onsets, onset_ll_vms, p_blind, rng):
    if rng.random() < p_blind:
        onset = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return onset + 'am'
    onset  = rng.choices(list(onset_ll_vms.keys()), weights=list(onset_ll_vms.values()))[0]
    suffix = rng.choices(list(suffix_global.keys()), weights=list(suffix_global.values()))[0]
    return make_word_sim(onset, suffix, rng)

def cipher_lf_vms(onset_weights, suffix_lf, onset_lf_vms, p_lf, rng):
    if rng.random() < p_lf:
        onset = rng.choices(list(onset_lf_vms.keys()), weights=list(onset_lf_vms.values()))[0]
        suffix = rng.choices(list(suffix_lf.keys()), weights=list(suffix_lf.values()))[0]
        return make_word_sim(onset, suffix, rng)
    return random_eva_word(onset_weights, suffix_lf, rng)

def timm_modify_edy_preserving_fresh_fallback(word, onset_weights, suffix_mid, rng):
    if not word: return word
    onset_len = get_onset_len(word); edy_len = get_edy_suffix_len(word)
    mod_start = onset_len; mod_end = len(word) - edy_len
    if mod_start >= mod_end:
        return random_eva_word(onset_weights, suffix_mid, rng)
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

def draw_from_buffer(buf, prev_onset, p_qokch, rng):
    buf_list = list(buf)
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words: return rng.choice(ch_words)
    return rng.choice(buf_list)

def run_sim(latin_words, onset_weights_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf_vms, onset_ll_vms, p_blind, target_lines, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    while len(lines) < target_lines and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(8.4, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf_vms(onset_weights_mid, suffix_lf_sup, onset_lf_vms, P_LF, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_blind_fixed(onset_weights_mid, suffix_global, ll_onsets,
                                           onset_ll_vms, p_blind, rng)
            else:
                if prev_word is not None and P_STUTTER > 0 and rng.random() < P_STUTTER:
                    ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_from_buffer(buf, prev_onset, P_QOKCH, rng)
                    if rng.random() < MP:
                        ew = timm_modify_edy_preserving_fresh_fallback(
                            src, onset_weights_mid, suffix_mid_sup, rng)
                    else:
                        ew = src
                else:
                    ew = random_eva_word(onset_weights_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n
    return lines[:target_lines]

def compute_metrics(lines):
    aw  = [w for l in lines for w in l]; n = len(aw)
    if n < 100: return None
    lf  = [l[0]  for l in lines if l]
    ll  = [l[-1] for l in lines if len(l) > 1]
    mid = [w for l in lines for w in l[1:-1] if len(l) > 2]
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf  = Counter(get_onset(w) for w in lf)
    oc_ll  = Counter(get_onset(w) for w in ll)
    n_lf, n_ll, n_mid = len(lf), len(ll), max(1,len(mid))

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

    qok_lf = enr('qok', oc_lf, n_lf, oc_all, n); d_lf = enr('d', oc_lf, n_lf, oc_all, n)
    s_lf   = enr('s',   oc_lf, n_lf, oc_all, n); ch_ll = enr('ch', oc_ll, n_ll, oc_all, n)
    ok_ll  = enr('ok',  oc_ll, n_ll, oc_all, n); qok_ll = enr('qok', oc_ll, n_ll, oc_all, n)
    ss_d   = ss('d'); ss_y = ss('y')

    lf_am_rate  = sum(1 for w in lf if w.endswith('am'))/n_lf if n_lf else 0
    mid_am_rate = sum(1 for w in mid if w.endswith('am'))/n_mid
    am_lf_enr   = lf_am_rate  / am_r if am_r else 0
    am_mid_enr  = mid_am_rate / am_r if am_r else 0

    edy_rate = sum(1 for w in aw if w.endswith('edy'))/n
    word_len = sum(len(w) for w in aw)/n

    qok_r = oc_all.get('qok', 0)/n; ch_r = oc_all.get('ch', 0)/n
    qok_ch = bg.get(('qok','ch'),0)/(tb*qok_r*ch_r) if qok_r and ch_r else 0

    return dict(am_ll=am_ll, d_ll=d_ll, y_lf=y_lf, ss_mean=ss_mean, adj_rate=adj,
                qok_lf=qok_lf, d_lf=d_lf, s_lf=s_lf, ch_ll=ch_ll, ok_ll=ok_ll,
                qok_ll=qok_ll, ss_d=ss_d, ss_y=ss_y, am_lf_enr=am_lf_enr,
                am_mid_enr=am_mid_enr, edy_rate=edy_rate, word_len_mean=word_len,
                qok_ch=qok_ch, global_am_rate=am_r,
                _ll_am=ll_am*100, _lf_am=lf_am_rate*100, _mid_am=mid_am_rate*100)

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

def agg_mean(metrics_list, key):
    vals = [x[key] for x in metrics_list]
    return sum(vals)/len(vals)

def pct(sim, ref):
    return sim/ref*100 if ref else 0

def pass_fail(sim, ref, tol=PASS_TOL):
    return 'P' if ref > 0 and abs(sim-ref)/ref <= tol else 'F'

# ─── Parse Corpora ─────────────────────────────────────────────────────────────

print("Parsing VMS corpora (A and B dialect)...")
lines_by_dialect = parse_vms_both_dialects()
print(f"  A-dialect: {len(lines_by_dialect['A'])} lines")
print(f"  B-dialect: {len(lines_by_dialect['B'])} lines")

vms_a = compute_vms_distributions(lines_by_dialect['A'])
vms_b = compute_vms_distributions(lines_by_dialect['B'])

TARGET_LINES_A = vms_a['n_lines']  # match A-dialect line count

print(f"\n  A-dialect words: {vms_a['n']} (in {vms_a['n_lf']} LF + {vms_a['n_ll']} LL + {vms_a['n_mid']} MID)")
print(f"  B-dialect words: {vms_b['n']}")

# ─── A-dialect VMS Targets (all 19 metrics) ────────────────────────────────────

print("\n" + "="*90)
print("A-DIALECT VMS TARGETS (all 19 metrics, computed from corpus)")
print("="*90)
VMS_A = {
    'am_ll':       vms_a['am_ll_target'],
    'd_ll':        vms_a['d_ll_target'],
    'y_lf':        vms_a['y_lf'],
    'ss_mean':     vms_a['ss_mean_corpus'],
    'adj_rate':    vms_a['adj_corpus'],
    'qok_lf':      vms_a['qok_lf'],
    'd_lf':        vms_a['d_lf'],
    's_lf':        vms_a['s_lf'],
    'ch_ll':       vms_a['ch_ll'],
    'ok_ll':       vms_a['ok_ll'],
    'qok_ll':      vms_a['qok_ll'],
    'ss_d':        vms_a['ss_d_corpus'],
    'ss_y':        vms_a['ss_y_corpus'],
    'am_lf_enr':   vms_a['am_lf_enr_corpus'],
    'am_mid_enr':  vms_a['am_mid_enr_corpus'],
    'edy_rate':    vms_a['edy_rate_corpus'],
    'word_len_mean': vms_a['word_len_corpus'],
    'qok_ch':      vms_a['qok_ch_corpus'],
    'global_am_rate': vms_a['am_r'],
}

VMS_B_REF = {  # B-dialect targets from exp_236 for comparison
    'am_ll': 6.5498, 'd_ll': 1.3625, 'y_lf': 3.3237, 'ss_mean': 1.164, 'adj_rate': 0.009,
    'qok_lf': 0.7777, 'd_lf': 2.2109, 's_lf': 4.6376, 'ch_ll': 0.9386, 'ok_ll': 0.9750,
    'qok_ll': 0.5952, 'ss_d': 1.291, 'ss_y': 1.955, 'am_lf_enr': 0.1225, 'am_mid_enr': 0.195,
    'edy_rate': 0.194, 'word_len_mean': 5.400, 'qok_ch': 1.267, 'global_am_rate': 0.0203,
}

METRIC_LABELS = [
    'am_ll', 'd_ll', 'y_lf', 'ss_mean', 'adj_rate',
    'qok_lf', 'd_lf', 's_lf', 'ch_ll', 'ok_ll', 'qok_ll',
    'ss_d', 'ss_y', 'am_lf_enr', 'am_mid_enr',
    'edy_rate', 'word_len_mean', 'qok_ch', 'global_am_rate',
]

print(f"  {'Metric':<18} {'A-target':>10} {'B-target':>10} {'A/B%':>7}")
print(f"  {'-'*50}")
for m in METRIC_LABELS:
    at = VMS_A[m]; bt = VMS_B_REF[m]
    print(f"  {m:<18} {at:>10.4f} {bt:>10.4f} {at/bt*100:>6.1f}%")

# ─── Analytical Parameter Derivation for A-dialect ────────────────────────────

print("\n" + "="*90)
print("A-DIALECT ANALYTICAL PARAMETER DERIVATION")
print("="*90)

a_global_am  = vms_a['am_r']
a_ll_am_rate = vms_a['ll_am_rate']
a_suffix_am  = vms_a['suffix_global'].get('am', 0)

p_blind_A = (a_ll_am_rate - a_suffix_am) / (1 - a_suffix_am) if (1 - a_suffix_am) > 0 else 0
p_blind_A = max(0, min(0.99, p_blind_A))

print(f"\n  A global_am:    {a_global_am*100:.3f}%")
print(f"  A LL_am_rate:   {a_ll_am_rate*100:.3f}%")
print(f"  A suffix['am']: {a_suffix_am*100:.3f}%")
print(f"  Analytical p_blind_A = ({a_ll_am_rate:.4f} - {a_suffix_am:.4f}) / (1 - {a_suffix_am:.4f}) = {p_blind_A:.4f}")
print(f"  (Compare B: p_blind_B = 0.115)")

d_global_A   = vms_a['onset_global'].get('d', 0)
d_ll_target_A = vms_a['d_ll_target']
onset_ll_A    = dict(vms_a['onset_ll'])
d_ll_nonblind_A = onset_ll_A.get('d', 0) / d_global_A if d_global_A else 0

d_boost_A = compute_d_boost_fixed(d_global_A, d_ll_target_A, d_ll_nonblind_A, p_blind_A)
print(f"\n  A d_global:     {d_global_A*100:.2f}%")
print(f"  A d_ll_target:  {d_ll_target_A:.4f}")
print(f"  A d_ll_nonblind:{d_ll_nonblind_A:.4f}")
print(f"  Analytical d_boost_A = {d_boost_A*100:.2f}%")
print(f"  (Compare B: d_boost_B = 9.13%)")

# clamp d_boost if out of range (can happen with A-dialect's high d base rate)
if d_boost_A < 0 or d_boost_A > 0.99:
    print(f"  WARNING: d_boost_A={d_boost_A:.4f} out of range — clamping to A LL d rate (direct)")
    d_boost_A = max(0, min(0.99, d_boost_A))
    # fallback: just use VMS LL d rate directly
    d_boost_A = onset_ll_A.get('d', 0)
    print(f"  Fallback: d_boost_A = VMS_A LL d rate = {d_boost_A:.4f}")

ll_onsets_A   = build_ll_onsets_fixed(onset_ll_A, d_boost_A)
onset_lf_A    = dict(vms_a['onset_lf'])
onset_ll_A_dict = dict(vms_a['onset_ll'])
suffix_A      = dict(vms_a['suffix_global'])
onset_mid_A   = dict(vms_a['onset_mid'])

print(f"\n  Structural params TRANSFERRED (unchanged from exp_236 B-dialect):")
print(f"    cp={CP}, mp={MP}, p_qokch={P_QOKCH}, p_stutter={P_STUTTER}, p_lf={P_LF}")

print()

# ─── Load Latin ─────────────────────────────────────────────────────────────────
print("Loading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} Latin words loaded.")
print()

# ─── CONDITION A: Direct Transfer (B-calibrated am params, A corpus) ───────────

print("="*90)
print(f"CONDITION A — DIRECT TRANSFER: B-calibrated am params (p_blind={P_BLIND_B}, "
      f"r_lf={R_LF_B}, r_mid={R_MID_B}) + A-dialect corpus")
print(f"N={N_FULL} simulations, {TARGET_LINES_A} lines each")
print("="*90)

# B-calibrated d_boost for A-dialect corpus (using B p_blind with A corpus)
d_boost_A_with_Bblind = compute_d_boost_fixed(d_global_A, d_ll_target_A, d_ll_nonblind_A, P_BLIND_B)
if d_boost_A_with_Bblind < 0 or d_boost_A_with_Bblind > 0.99:
    d_boost_A_with_Bblind = onset_ll_A.get('d', 0)
ll_onsets_A_Bblind = build_ll_onsets_fixed(onset_ll_A_dict, d_boost_A_with_Bblind)
suffix_lf_A_B  = make_suppressed_suffix(suffix_A, R_LF_B)
suffix_mid_A_B = make_suppressed_suffix(suffix_A, R_MID_B)

condA_metrics = []
for i in range(N_FULL):
    rng = random.Random(SEED + i)
    lines = run_sim(latin, onset_mid_A, suffix_A, suffix_lf_A_B, suffix_mid_A_B,
                    ll_onsets_A_Bblind, onset_lf_A, onset_ll_A_dict, P_BLIND_B,
                    TARGET_LINES_A, rng)
    m = compute_metrics(lines)
    if m: condA_metrics.append(m)

print(f"\n  Metric             A-target     CondA-sim    %    P?    B-target")
print(f"  {'-'*70}")
condA_passes = 0
for ml in METRIC_LABELS:
    at = VMS_A[ml]; bt = VMS_B_REF[ml]
    sim = agg_mean(condA_metrics, ml)
    pf = pass_fail(sim, at)
    if pf == 'P': condA_passes += 1
    print(f"  {ml:<18} {at:>10.4f} {sim:>10.4f} {pct(sim,at):>6.1f}% {pf:>3}  [{bt:>8.4f}]")

print(f"\n  Condition A PASS: {condA_passes}/19 (no am/d recalibration)")

# ─── CONDITION B: Recalibrated Transfer ─────────────────────────────────────────

print()
print("="*90)
print(f"CONDITION B — RECALIBRATED: p_blind={p_blind_A:.4f}, d_boost={d_boost_A:.4f} "
      f"(A-dialect analytical); r_lf/r_mid sweep + A corpus")
print("="*90)

R_LF_VALUES  = [0.08, 0.10, 0.12, 0.15, 0.18, 0.20]
R_MID_VALUES = [0.15, 0.20, 0.25, 0.30]
SWEEP_GRID   = [(r_lf, r_mid) for r_lf in R_LF_VALUES for r_mid in R_MID_VALUES]

print(f"\nSWEEP: r_lf ∈ {R_LF_VALUES}, r_mid ∈ {R_MID_VALUES}")
print(f"N={N_SWEEP} per combo = {len(SWEEP_GRID)} combos")
print(f"\n  {'r_lf':>5} {'r_mid':>5} {'global_am%':>11} {'%A':>7} {'P?':>3} "
      f"{'am_lf_enr':>10} {'%A':>7} {'P?':>3} {'am_mid_enr':>11} {'%A':>7} {'P?':>3} "
      f"{'am_ll':>7} {'%A':>7} {'P?':>3}")

sweep_results = {}
for r_lf, r_mid in SWEEP_GRID:
    suffix_lf_sup  = make_suppressed_suffix(suffix_A, r_lf)
    suffix_mid_sup = make_suppressed_suffix(suffix_A, r_mid)
    metrics = []
    for i in range(N_SWEEP):
        seed_val = SEED + 10000 + int(r_lf*1000)*100 + int(r_mid*1000) + i
        rng = random.Random(seed_val)
        lines = run_sim(latin, onset_mid_A, suffix_A, suffix_lf_sup, suffix_mid_sup,
                        ll_onsets_A, onset_lf_A, onset_ll_A_dict, p_blind_A,
                        TARGET_LINES_A, rng)
        m = compute_metrics(lines)
        if m: metrics.append(m)
    sweep_results[(r_lf, r_mid)] = metrics
    if not metrics: continue

    m_gam  = agg_mean(metrics, 'global_am_rate')
    m_alf  = agg_mean(metrics, 'am_lf_enr')
    m_amid = agg_mean(metrics, 'am_mid_enr')
    m_all  = agg_mean(metrics, 'am_ll')
    vgam, valf, vamid, vall = (VMS_A['global_am_rate'], VMS_A['am_lf_enr'],
                                VMS_A['am_mid_enr'],    VMS_A['am_ll'])

    p_gam  = pass_fail(m_gam, vgam); p_alf = pass_fail(m_alf, valf)
    p_amid = pass_fail(m_amid, vamid); p_all = pass_fail(m_all, vall)
    print(f"  {r_lf:>5.2f} {r_mid:>5.2f} {m_gam*100:>11.2f}% {m_gam/vgam*100:>6.1f}% {p_gam:>3} "
          f"{m_alf:>10.3f} {m_alf/valf*100:>6.1f}% {p_alf:>3} "
          f"{m_amid:>10.3f} {m_amid/vamid*100:>6.1f}% {p_amid:>3} "
          f"{m_all:>7.3f} {m_all/vall*100:>6.1f}% {p_all:>3}")

# Select best combo
def score_combo(combo):
    metrics = sweep_results.get(combo, [])
    if not metrics: return (9, float('inf'))
    m_gam  = agg_mean(metrics, 'global_am_rate')
    m_alf  = agg_mean(metrics, 'am_lf_enr')
    m_amid = agg_mean(metrics, 'am_mid_enr')
    m_all  = agg_mean(metrics, 'am_ll')
    vgam, valf, vamid, vall = (VMS_A['global_am_rate'], VMS_A['am_lf_enr'],
                                VMS_A['am_mid_enr'],    VMS_A['am_ll'])
    passes = sum([pass_fail(m_gam,vgam)=='P', pass_fail(m_alf,valf)=='P',
                  pass_fail(m_amid,vamid)=='P', pass_fail(m_all,vall)=='P'])
    combined = ((m_gam/vgam-1)**2 + (m_alf/valf-1)**2 + (m_amid/vamid-1)**2
                + (m_all/vall-1)**2) if all(v>0 for v in [vgam,valf,vamid,vall]) else float('inf')
    return (4 - passes, combined)

scored = [(score_combo(c), c) for c in SWEEP_GRID]
scored.sort(key=lambda x: (x[0][0], x[0][1]))
best_combo = scored[0][1]
best_tier  = 4 - scored[0][0][0]
r_lf_best, r_mid_best = best_combo
print(f"\n  Best combo: r_lf={r_lf_best}, r_mid={r_mid_best}  (tier: {best_tier}/4 am-metrics PASS)")

# ─── Full Run: Condition B Best ───────────────────────────────────────────────

suffix_lf_best  = make_suppressed_suffix(suffix_A, r_lf_best)
suffix_mid_best = make_suppressed_suffix(suffix_A, r_mid_best)

print()
print("="*90)
print(f"FULL RUN (Condition B): N={N_FULL}, p_blind={p_blind_A:.4f}, "
      f"r_lf={r_lf_best}, r_mid={r_mid_best}")
print("="*90)

condB_metrics = []
for i in range(N_FULL):
    rng = random.Random(SEED + 100000 + i)
    lines = run_sim(latin, onset_mid_A, suffix_A, suffix_lf_best, suffix_mid_best,
                    ll_onsets_A, onset_lf_A, onset_ll_A_dict, p_blind_A,
                    TARGET_LINES_A, rng)
    m = compute_metrics(lines)
    if m: condB_metrics.append(m)

print(f"\n  {'Metric':<18} {'A-target':>10} {'CondA-sim':>10} {'CondB-sim':>10} "
      f"{'%':>7} {'P?':>3}  {'Transfer?'}")
print(f"  {'-'*90}")

condB_passes = 0
category_counts = {'YES': 0, 'CALIBRATE': 0, 'FAIL': 0}
for ml in METRIC_LABELS:
    at = VMS_A[ml]
    sA = agg_mean(condA_metrics, ml)
    sB = agg_mean(condB_metrics, ml)
    pfA = pass_fail(sA, at)
    pfB = pass_fail(sB, at)
    if pfB == 'P': condB_passes += 1
    # Categorize transfer
    if pfA == 'P' and pfB == 'P':
        cat = 'DIRECT'      # passes without recalibration
    elif pfA == 'F' and pfB == 'P':
        cat = 'CALIBRATE'   # needs calibration but mechanism works
    else:
        cat = 'FAIL'        # fails even after calibration
    if cat != 'FAIL': category_counts['YES' if cat=='DIRECT' else cat] += 1
    else: category_counts['FAIL'] += 1
    condA_pct = pct(sA, at); condB_pct = pct(sB, at)
    print(f"  {ml:<18} {at:>10.4f} {sA:>10.4f} {sB:>10.4f} {condB_pct:>6.1f}% {pfB:>3}  [{cat}]")

print(f"\n  -am diagnostics (Condition B):")
print(f"    p_blind_A    = {p_blind_A:.4f} (B was 0.115)")
print(f"    r_lf_A       = {r_lf_best:.3f} (B was 0.12)")
print(f"    r_mid_A      = {r_mid_best:.3f} (B was 0.25)")
print(f"    Global am    = {agg_mean(condB_metrics,'global_am_rate')*100:.2f}% (A-VMS: {VMS_A['global_am_rate']*100:.2f}%)")
print(f"    LL am rate   = {agg_mean(condB_metrics,'_ll_am'):.2f}% (A-VMS: {vms_a['ll_am_rate']*100:.2f}%)")
print(f"    am_ll        = {agg_mean(condB_metrics,'am_ll'):.3f} (A-VMS: {VMS_A['am_ll']:.3f})")

print()
print("="*90)
print("GENERALIZATION VERDICT")
print("="*90)
print(f"\n  Condition A (direct transfer, NO recalibration):  {condA_passes}/19 PASS")
print(f"  Condition B (recalibrated p_blind/d_boost/r):     {condB_passes}/19 PASS")
print(f"\n  Transfer categories:")
print(f"    DIRECT   (pass with B params, A corpus):  {category_counts['YES']}/19")
print(f"    CALIBRATE(pass after am/d recalibration): {category_counts['CALIBRATE']}/19")
print(f"    FAIL     (fails even after calibration):  {category_counts['FAIL']}/19")

print(f"\n  B-dialect 19/19 (exp_236): all metrics PASS")
print(f"  A-dialect generalization test complete.")
print()
print("Done.")
