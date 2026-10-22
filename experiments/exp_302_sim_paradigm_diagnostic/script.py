"""
exp_302: Simulation Per-Onset Closed Paradigm Diagnostic (Q007)

Q007: The simulation over-produces unique MID word types (6,458 vs VMS 2,929, 2.2×).
Phase 6 provides new constraints:
  - VMS qok-onset: 32 types for 90% coverage (18.2% of 176 types)
  - VMS ok-onset: 67 types for 90% coverage (33.8% of 198 types)
  - VMS ot-onset: 83 types for 90% coverage (39.0% of 213 types)
  - VMS sh-onset: 145 types for 90% coverage (43.3% of 335 types)
  - VMS ch-onset: 284 types for 90% coverage (46.8% of 607 types)

This experiment:
1. Measures simulation per-onset closed paradigm sizes at R_MID=0.20
2. Compares sim vs VMS for each onset class
3. Analyzes the DISTRIBUTION of word types in sim vs VMS
4. Identifies the mechanism producing excess types (Timm modification path vs cipher path)

Architecture: exp_301 (R_MID=0.20, 16 mechanisms including beta=0.30).
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_FULL   = 10  # smaller N since this is diagnostic
TARGET_LINES = 2411
WINDOW   = 20
SEED     = 302000

# 16-mechanism B-dialect parameters (exp_301: R_MID updated to 0.20)
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

# VMS target closed paradigm sizes (from exp_295, F296)
VMS_CP90 = {
    'qok': (32, 176),   # (types for 90%, total types)
    'ok':  (67, 198),
    'ot':  (83, 213),
    'sh':  (145, 335),
    'ch':  (284, 607),
    'qot': (46, 117),
    'd':   (149, 281),
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
    mid_nemed, mid_p = build_midfix_dist(mid_words)
    lf_nemed,  lf_p  = build_midfix_dist(lf_words)
    ll_nemed,  ll_p  = build_midfix_dist(ll_words)
    am_r  = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words)
    d_r   = Counter(get_onset(w) for w in all_words).get('d', 0) / n
    ll_d  = Counter(get_onset(w) for w in ll_words).get('d', 0) / len(ll_words)
    return {
        'onset_global': onset_global, 'onset_lf': onset_lf,
        'onset_ll': onset_ll, 'onset_mid': onset_mid,
        'suffix_global': suffix_global,
        'mid_nemed': mid_nemed, 'mid_p': mid_p,
        'lf_nemed': lf_nemed, 'lf_p': lf_p,
        'll_nemed': ll_nemed, 'll_p': ll_p,
        'am_r': am_r, 'am_ll_target': ll_am/am_r if am_r else 0,
        'd_r': d_r, 'd_ll_target': ll_d/d_r if d_r else 0,
        'n': n, 'n_lf': len(lf_words), 'n_ll': len(ll_words), 'n_mid': len(mid_words),
    }

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

def run_sim_tracked(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf_vms, onset_ll_vms,
                    mid_nemed, lf_nemed, ll_nemed, rng):
    """Run simulation, tracking word origin (buffer_copy vs buffer_modified vs cipher_generated)."""
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    # Track MID word origins
    mid_words = []
    mid_origins = []  # 'copy', 'modified', 'cipher', 'stutter'
    while len(lines) < TARGET_LINES and pos < len(w) - 2:
        n = max(2, min(20, round(rng.gauss(MU_LEN, SIGMA_LEN))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []; word_idx = 0
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf(onset_mid, onset_lf_vms, suffix_lf_sup, P_LF, rng, lf_nemed)
                origin = 'lf'
            elif i == len(chunk) - 1:
                ew = cipher_ll(onset_ll_vms, ll_onsets, suffix_global, P_BLIND, rng, ll_nemed)
                origin = 'll'
            else:
                if prev_word is not None and rng.random() < P_STUTTER:
                    ew = prev_word; origin = 'stutter'
                elif buf and rng.random() < CP:
                    src = draw_buf_length_biased(buf, prev_onset, P_QOKCH, P_CHQOK,
                                                 rng, word_idx, GAMMA)
                    if src is None: src = rng.choice(list(buf))
                    if rng.random() < MP:
                        ew = timm_modify(src, onset_mid, suffix_mid_sup, rng)
                        origin = 'modified'
                    else:
                        ew = src; origin = 'copy'
                else:
                    ew = random_eva_word_onset_biased(onset_mid, suffix_mid_sup, rng,
                                                      mid_nemed, P_MF, word_idx, ALPHA, BETA)
                    origin = 'cipher'
                buf.append(ew); word_idx += 1
                mid_words.append(ew); mid_origins.append(origin)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES], mid_words, mid_origins

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

print("exp_302: Simulation Per-Onset Closed Paradigm Diagnostic (Q007)")
print("=" * 65)

print("Parsing VMS B-dialect corpus...")
b_lines = parse_vms_b()
vms_dist = compute_vms_distributions(b_lines)
vms_mid = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
print(f"  VMS B: {len(b_lines)} lines, {vms_dist['n']} words")
print(f"  VMS MID words: {len(vms_mid)}")

print("\nLoading Latin corpus...")
latin_words = load_latin(LATIN_CORPUS)
print(f"  {len(latin_words)} Latin words loaded.")

suffix_global = vms_dist['suffix_global']
suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
onset_lf_vms = vms_dist['onset_lf']; onset_ll_vms = vms_dist['onset_ll']; onset_mid = vms_dist['onset_mid']
d_global = vms_dist['onset_global'].get('d', 0)
d_ll_non_blind_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0
d_boost_weight = compute_d_boost(d_global, vms_dist['d_ll_target'], d_ll_non_blind_enr, P_BLIND)
d_boost_weight = max(0.0, min(d_boost_weight, 1.0))
ll_onsets = build_ll_onsets(onset_ll_vms, d_boost_weight)
mid_nemed = vms_dist['mid_nemed']; lf_nemed = vms_dist['lf_nemed']; ll_nemed = vms_dist['ll_nemed']

# VMS closed paradigm analysis
print(f"\n{'='*65}")
print("VMS Per-Onset Closed Paradigm Sizes (MID words only)")
print('='*65)
print(f"  {'Onset':<5}  {'MID N':>6}  {'Types':>5}  {'CP90':>4}  {'CP90%':>6}")
for onset, (vms_n90, vms_ntypes) in VMS_CP90.items():
    vms_toks = [w for w in vms_mid if get_onset(w) == onset]
    vms_types_actual = len(Counter(vms_toks))
    print(f"  {onset:<5}  {len(vms_toks):>6}  {vms_types_actual:>5}  {vms_n90:>4}  "
          f"{vms_n90/vms_types_actual:.1%}  (target: {vms_n90}/{vms_ntypes}={vms_n90/vms_ntypes:.1%})")

# Run simulations (N=N_FULL) and aggregate MID words
print(f"\n{'='*65}")
print(f"Running {N_FULL} simulation trials (R_MID={R_MID})...")
print('='*65)

all_mid_words = []
all_mid_origins = []
origin_type_counters = {'copy': Counter(), 'modified': Counter(), 'cipher': Counter(), 'stutter': Counter()}

for trial in range(N_FULL):
    rng = random.Random(SEED + trial * 1000)
    _, mid_words, mid_origins = run_sim_tracked(
        latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
        ll_onsets, onset_lf_vms, onset_ll_vms,
        mid_nemed, lf_nemed, ll_nemed, rng)
    all_mid_words.extend(mid_words)
    all_mid_origins.extend(mid_origins)
    for w, o in zip(mid_words, mid_origins):
        origin_type_counters[o][w] += 1

n_mid = len(all_mid_words) // N_FULL  # approximate per-trial count
print(f"  Total MID words collected: {len(all_mid_words)} ({N_FULL} trials)")

# Aggregate per-onset analysis
print(f"\n  Per-Onset Closed Paradigm Analysis (aggregated over {N_FULL} trials):")
print(f"  {'Onset':<5}  {'N/trial':>7}  {'Types/trial':>11}  {'CP90':>4}  {'CP90%':>6}  "
      f"{'VMS N90':>7}  {'VMS%':>5}  {'Ratio':>5}")

for onset, (vms_n90, vms_ntypes) in VMS_CP90.items():
    onset_words = [w for w, _ in zip(all_mid_words, all_mid_origins)
                   if get_onset(w) == onset]
    if not onset_words: continue
    # Average over trials
    trial_n90s = []
    trial_ntypes = []
    for trial in range(N_FULL):
        tw = [w for w, o in zip(all_mid_words[trial*len(all_mid_words)//N_FULL:
                                               (trial+1)*len(all_mid_words)//N_FULL],
                               all_mid_origins[trial*len(all_mid_words)//N_FULL:
                                               (trial+1)*len(all_mid_words)//N_FULL])
              if get_onset(w) == onset]
        if not tw: continue
        n90, nt, _ = closed_paradigm_size(tw, onset)
        trial_n90s.append(n90); trial_ntypes.append(nt)
    if not trial_n90s: continue
    avg_n90 = sum(trial_n90s)/len(trial_n90s)
    avg_nt = sum(trial_ntypes)/len(trial_ntypes)
    avg_frac = avg_n90/avg_nt if avg_nt else 0
    n_per_trial = len(onset_words)/N_FULL
    ratio_n90 = avg_n90/vms_n90 if vms_n90 else 0
    print(f"  {onset:<5}  {n_per_trial:>7.0f}  {avg_nt:>11.0f}  {avg_n90:>4.0f}  "
          f"{avg_frac:>6.1%}  {vms_n90:>7}  {vms_n90/vms_ntypes:>5.1%}  {ratio_n90:>5.2f}×")

# Origin analysis for qok
print(f"\n  ORIGIN ANALYSIS for qok-onset MID words:")
qok_by_origin = {'copy': 0, 'modified': 0, 'cipher': 0, 'stutter': 0}
qok_types_by_origin = {'copy': Counter(), 'modified': Counter(), 'cipher': Counter()}
for w, o in zip(all_mid_words, all_mid_origins):
    if get_onset(w) == 'qok':
        qok_by_origin[o] = qok_by_origin.get(o, 0) + 1
        if o in qok_types_by_origin:
            qok_types_by_origin[o][w] += 1
total_qok = sum(qok_by_origin.values())
for orig, count in sorted(qok_by_origin.items(), key=lambda x: -x[1]):
    types = len(qok_types_by_origin.get(orig, {}))
    pct = count/total_qok*100 if total_qok else 0
    print(f"    {orig:<10}: {count:6d} tokens ({pct:.1f}%), {types:4d} unique types")

# Total MID vocabulary
print(f"\n  TOTAL MID VOCABULARY (all onsets, all {N_FULL} trials aggregated):")
all_types = Counter(all_mid_words)
print(f"    Total MID tokens: {len(all_mid_words)}")
print(f"    Unique MID types: {len(all_types)}")
print(f"    Per-trial estimate: {len(all_types)/N_FULL:.0f} types/trial")
print(f"    VMS MID types: {len(Counter(vms_mid))}")
print(f"    Ratio: {len(all_types)/N_FULL / len(Counter(vms_mid)):.2f}×")

# Hapax rate
hapax_sim = sum(1 for w, c in all_types.items() if c == 1)
hapax_vms = sum(1 for w, c in Counter(vms_mid).items() if c == 1)
print(f"    Sim hapax types: {hapax_sim} ({hapax_sim/len(all_types):.1%})")
print(f"    VMS hapax types: {hapax_vms} ({hapax_vms/len(Counter(vms_mid)):.1%})")

print("\nDone.")
