"""
exp_268: H473 — Menzerath's Law in Simulation
Does the copy-buffer simulation reproduce VMS Menzerath's Law (r < 0) without parameter tuning?

Prediction: LF/LL words are longer than MID words on average; as line length increases,
proportion of MID words increases, pulling mean word length down → r(line_length, mean_word_len) < 0.

VMS targets (from exp_267):
  A-dialect: r = -0.249, N_lines = 1687
  B-dialect: r = -0.293, N_lines = 2391
  A position means: LF=5.526, MID=5.268, LL=5.706
  B position means: LF=5.821, MID=5.456, LL=5.275
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_RUNS = 30; SEED = 268000

# ─── A-dialect 13-mechanism parameters (finalized, exp_262/264) ───
A = dict(
    p_blind=0.0505, d_boost=0.2430, r_lf=0.266, r_mid=0.87,
    p_stutter=0.002, mu_len=5.64, sigma_len=2.5,
    cp=0.55, mp=0.90, p_qokch=0.12, p_chqok=0.00, p_lf=1.0,
    p_y_y=0.10, p_o_o=0.10, p_sh_qok=0.10,
    window=20,
)

# ─── B-dialect 12-mechanism parameters (finalized, exp_257/249) ───
B = dict(
    p_blind=0.115, r_lf=0.12, r_mid=0.25,
    p_stutter=0.006, mu_len=8.4, sigma_len=3.0,
    cp=0.55, mp=0.90, p_qokch=0.12, p_chqok=0.12, p_lf=1.0,
    p_y_y=0.00, p_o_o=0.00, p_sh_qok=0.00,
    window=20,
)

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

def get_edy_suffix_len(w):
    if w.endswith('eedy'): return 4
    if w.endswith('edy'):  return 3
    return 0

def filter_other(dist):
    filtered = {k: v for k, v in dist.items() if k != 'other'}
    total = sum(filtered.values())
    return {k: v/total for k, v in filtered.items()} if total > 0 else filtered

def folio_base(folio): return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_vms(target_dialect):
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
    vms_lines = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            if folio_dialect.get(fb, 'unknown') != target_dialect: continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: vms_lines.append(words)
    return vms_lines

def build_onset_dist(words):
    n = max(1, len(words))
    return {o: cnt/n for o, cnt in Counter(get_onset(w) for w in words).items()}

def build_suffix(words):
    n = len(words); suf_ctr = Counter()
    for w in words:
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf): suf_ctr[suf] += 1; break
        else: suf_ctr['other'] += 1
    return {suf: cnt/n for suf, cnt in suf_ctr.items()}

def make_suppressed_suffix(suffix_global, r_am):
    am_w = suffix_global.get('am', 0.0); new_am = am_w * r_am; delta = am_w - new_am
    non_am = 1.0 - am_w
    return {s: (new_am if s=='am' else w + w/non_am*delta) for s, w in suffix_global.items()} \
           if non_am > 0 else dict(suffix_global)

def build_ll_onsets(onset_ll, d_boost_weight):
    rem = 1.0 - d_boost_weight
    base = {o: v for o, v in onset_ll.items() if o != 'd'}
    bt = sum(base.values())
    norm = {o: v/bt*rem for o, v in base.items()} if bt > 0 else {}
    norm['d'] = d_boost_weight; return norm

def make_word_sim(onset, suffix, rng):
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset + rng.choice(['a','ai','o','oi','e','ei']) + suffix
    return onset + suffix

def random_eva_word(onset_w, suffix_w, rng):
    o = rng.choices(list(onset_w.keys()), weights=list(onset_w.values()))[0]
    s = rng.choices(list(suffix_w.keys()), weights=list(suffix_w.values()))[0]
    return make_word_sim(o, s, rng)

def cipher_ll(onset_mid, suffix_global, ll_onsets, onset_ll, p_blind, rng):
    if rng.random() < p_blind:
        o = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return o + 'am'
    o = rng.choices(list(onset_ll.keys()), weights=list(onset_ll.values()))[0]
    s = rng.choices(list(suffix_global.keys()), weights=list(suffix_global.values()))[0]
    return make_word_sim(o, s, rng)

def cipher_lf(onset_mid, suffix_lf, onset_lf, p_lf, rng):
    if rng.random() < p_lf:
        o = rng.choices(list(onset_lf.keys()), weights=list(onset_lf.values()))[0]
        s = rng.choices(list(suffix_lf.keys()), weights=list(suffix_lf.values()))[0]
        return make_word_sim(o, s, rng)
    return random_eva_word(onset_mid, suffix_lf, rng)

def timm_modify(word, onset_w, suffix_mid, rng):
    if not word: return word
    ol = get_onset_len(word); el = get_edy_suffix_len(word)
    ms = ol; me = len(word) - el
    if ms >= me: return random_eva_word(onset_w, suffix_mid, rng)
    op = rng.choice(['replace','insert','delete'])
    if op == 'replace':
        pos = rng.randint(ms, me-1); return word[:pos]+rng.choice(EVA_CHARS)+word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(ms, me); return word[:pos]+rng.choice(EVA_CHARS)+word[pos:]
    else:
        if me-ms <= 1: return word[:ms]+rng.choice(EVA_CHARS)+word[ms+1:]
        pos = rng.randint(ms, me-1); return word[:pos]+word[pos+1:]

def draw_buf(buf, prev_onset, p_qokch, p_chqok, p_y_y, p_o_o, p_sh_qok, rng):
    bl = list(buf)
    if not bl: return None
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'ch' and p_chqok > 0 and rng.random() < p_chqok:
        qw = [w for w in bl if get_onset(w) == 'qok']
        if qw: return rng.choice(qw)
    if prev_onset == 'y' and p_y_y > 0 and rng.random() < p_y_y:
        yw = [w for w in bl if get_onset(w) == 'y']
        if yw: return rng.choice(yw)
    if prev_onset == 'o' and p_o_o > 0 and rng.random() < p_o_o:
        ow = [w for w in bl if get_onset(w) == 'o']
        if ow: return rng.choice(ow)
    if prev_onset == 'sh' and p_sh_qok > 0 and rng.random() < p_sh_qok:
        qw = [w for w in bl if get_onset(w) == 'qok']
        if qw: return rng.choice(qw)
    return rng.choice(bl)

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

def run_sim_lines(latin_words, onset_mid, suffix_global, suffix_lf, suffix_mid,
                  ll_onsets, onset_lf, onset_ll, params, target_lines, rng):
    """Run simulation and return list of lines (each line = list of EVA words)."""
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=params['window']), 0
    prev_onset = None; prev_word = None
    while len(lines) < target_lines and pos < len(w) - 2:
        n_words = max(2, min(20, round(rng.gauss(params['mu_len'], params['sigma_len']))))
        chunk = w[pos:pos+n_words]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                ew = cipher_lf(onset_mid, suffix_lf, onset_lf, params['p_lf'], rng)
            elif i == len(chunk)-1:
                ew = cipher_ll(onset_mid, suffix_global, ll_onsets, onset_ll,
                               params['p_blind'], rng)
            else:
                if prev_word is not None and params['p_stutter'] > 0 and rng.random() < params['p_stutter']:
                    ew = prev_word
                elif buf and rng.random() < params['cp']:
                    src = draw_buf(buf, prev_onset,
                                   params['p_qokch'], params['p_chqok'],
                                   params['p_y_y'], params['p_o_o'], params['p_sh_qok'], rng)
                    if src is None: src = random_eva_word(onset_mid, suffix_mid, rng)
                    ew = timm_modify(src, onset_mid, suffix_mid, rng) if rng.random() < params['mp'] else src
                else:
                    ew = random_eva_word(onset_mid, suffix_mid, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew
            line.append(ew)
        lines.append(line)
        pos += n_words
    return lines[:target_lines]

def pearson_r(xs, ys):
    n = len(xs)
    if n < 2: return 0.0
    mx = sum(xs)/n; my = sum(ys)/n
    num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    dx = math.sqrt(sum((x-mx)**2 for x in xs))
    dy = math.sqrt(sum((y-my)**2 for y in ys))
    return num/(dx*dy) if dx*dy > 0 else 0.0

def menzerath_r(lines):
    """Compute Pearson r(line_length_words, mean_word_len_chars)."""
    xs, ys = [], []
    for line in lines:
        if len(line) < 2: continue
        xs.append(len(line))
        ys.append(sum(len(w) for w in line) / len(line))
    return pearson_r(xs, ys), len(xs)

def position_mean_len(lines):
    """Return (lf_mean, mid_mean, ll_mean) for a list of lines."""
    lf_lens = [len(l[0]) for l in lines if l]
    mid_lens = [len(w) for l in lines for w in l[1:-1] if len(l) > 2]
    ll_lens = [len(l[-1]) for l in lines if len(l) > 1]
    def mean(lst): return sum(lst)/len(lst) if lst else 0.0
    return mean(lf_lens), mean(mid_lens), mean(ll_lens)

def compute_d_boost(d_global, d_ll_target, d_ll_enr_target, p_blind):
    """Compute d_boost weight for LL onset distribution."""
    # A-dialect: d_boost=24.30% is the target d-onset LL weight
    # Return it directly (pre-computed from dialect calibration)
    return d_ll_target

def prepare_dialect(vms_lines, params):
    """Build all distributions needed for simulation from VMS lines."""
    all_words = [w for l in vms_lines for w in l]
    mid_words = [w for l in vms_lines for w in l[1:-1] if len(l) > 2]
    lf_words  = [l[0] for l in vms_lines if l]
    ll_words  = [l[-1] for l in vms_lines if len(l) > 1]

    onset_mid = filter_other(build_onset_dist(mid_words))
    onset_lf  = filter_other(build_onset_dist(lf_words))
    onset_ll  = filter_other(build_onset_dist(ll_words))
    suffix_global = build_suffix(all_words)
    suffix_lf     = build_suffix(lf_words) if lf_words else suffix_global
    suffix_mid    = build_suffix(mid_words) if mid_words else suffix_global

    # Suppressed suffixes (r_am controls -am in MID/LF)
    suffix_lf_sup  = make_suppressed_suffix(suffix_global, params.get('r_lf', 0.12))
    suffix_mid_sup = make_suppressed_suffix(suffix_global, params.get('r_mid', 0.25))

    # LL onset distribution with d_boost
    d_boost_w = params.get('d_boost', 0.0)
    if d_boost_w > 0:
        ll_onsets = build_ll_onsets(onset_ll, d_boost_w)
    else:
        ll_onsets = onset_ll.copy()

    return onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup, ll_onsets, onset_lf, onset_ll

def run_dialect(dialect_label, vms_lines, params, latin_words):
    """Run N_RUNS simulations, collect Menzerath r and position means."""
    onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup, ll_onsets, onset_lf, onset_ll = \
        prepare_dialect(vms_lines, params)
    target_lines = len(vms_lines)

    # VMS Menzerath
    vms_r, vms_n = menzerath_r(vms_lines)
    vms_lf, vms_mid, vms_ll = position_mean_len(vms_lines)

    print(f"\n{'='*68}")
    print(f"DIALECT: {dialect_label}")
    print(f"{'='*68}")
    print(f"VMS Menzerath r = {vms_r:.4f}  (N_lines={vms_n})")
    print(f"VMS position means: LF={vms_lf:.3f}  MID={vms_mid:.3f}  LL={vms_ll:.3f}")
    print()

    sim_rs = []
    sim_lf_means, sim_mid_means, sim_ll_means = [], [], []

    rng = random.Random(SEED)
    for run in range(N_RUNS):
        sim_lines = run_sim_lines(
            latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf, onset_ll, params, target_lines, rng
        )
        r, _ = menzerath_r(sim_lines)
        sim_rs.append(r)
        lf_m, mid_m, ll_m = position_mean_len(sim_lines)
        sim_lf_means.append(lf_m)
        sim_mid_means.append(mid_m)
        sim_ll_means.append(ll_m)

    def mean(lst): return sum(lst)/len(lst) if lst else 0.0
    def stdev(lst):
        m = mean(lst); return math.sqrt(sum((x-m)**2 for x in lst)/len(lst)) if lst else 0.0

    sim_r_mean = mean(sim_rs); sim_r_sd = stdev(sim_rs)
    sim_lf = mean(sim_lf_means); sim_mid = mean(sim_mid_means); sim_ll = mean(sim_ll_means)
    n_negative = sum(1 for r in sim_rs if r < 0)

    print(f"SIM Menzerath r = {sim_r_mean:.4f} ± {sim_r_sd:.4f}  ({n_negative}/{N_RUNS} runs negative)")
    print(f"SIM position means: LF={sim_lf:.3f}  MID={sim_mid:.3f}  LL={sim_ll:.3f}")
    print()
    print(f"Δr = VMS - SIM_mean = {vms_r - sim_r_mean:.4f}")
    print(f"Δ_LF_mean  = {vms_lf - sim_lf:.3f}")
    print(f"Δ_MID_mean = {vms_mid - sim_mid:.3f}")
    print(f"Δ_LL_mean  = {vms_ll - sim_ll:.3f}")

    # Distribution of sim r values
    print(f"\nSim r distribution: min={min(sim_rs):.4f}  max={max(sim_rs):.4f}")
    r_neg = sum(1 for r in sim_rs if r < -0.10)
    print(f"  Runs with r < -0.10: {r_neg}/{N_RUNS}")

    # Per-bucket comparison: VMS vs SIM
    print(f"\nLine-length bucket mean word length (VMS vs SIM):")
    vms_buckets = defaultdict(list)
    for line in vms_lines:
        if len(line) >= 2:
            vms_buckets[len(line)].append(sum(len(w) for w in line)/len(line))
    rng2 = random.Random(SEED)
    one_sim = run_sim_lines(
        latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
        ll_onsets, onset_lf, onset_ll, params, target_lines, rng2
    )
    sim_buckets = defaultdict(list)
    for line in one_sim:
        if len(line) >= 2:
            sim_buckets[len(line)].append(sum(len(w) for w in line)/len(line))
    buckets = sorted(set(list(vms_buckets.keys()) + list(sim_buckets.keys())))
    print(f"  {'LinLen':>6}  {'VMS_N':>6}  {'VMS_mean':>8}  {'SIM_N':>6}  {'SIM_mean':>8}")
    for b in buckets:
        if b > 14: break
        vm = vms_buckets.get(b, []); sm = sim_buckets.get(b, [])
        vm_m = sum(vm)/len(vm) if vm else 0
        sm_m = sum(sm)/len(sm) if sm else 0
        print(f"  {b:>6}  {len(vm):>6}  {vm_m:>8.3f}  {len(sm):>6}  {sm_m:>8.3f}")

    return sim_r_mean, sim_r_sd, n_negative

def main():
    print("Parsing VMS corpus...")
    a_lines = parse_vms('A')
    b_lines = parse_vms('B')
    print(f"  A-dialect: {len(a_lines)} lines")
    print(f"  B-dialect: {len(b_lines)} lines")

    print("\nLoading Latin corpus...")
    latin_words = load_latin(LATIN_CORPUS)
    print(f"  Latin: {len(latin_words)} words")

    run_dialect('A-dialect', a_lines, A, latin_words)
    run_dialect('B-dialect', b_lines, B, latin_words)

    print("\n\n" + "="*68)
    print("SUMMARY")
    print("="*68)
    print("VMS targets (exp_267): A r=-0.249, B r=-0.293")
    print("Prediction: r < 0 in both dialects (Menzerath emerges from buffer dynamics)")
    print("See above for simulation results.")

if __name__ == '__main__':
    main()
