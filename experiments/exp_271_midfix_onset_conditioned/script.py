"""
exp_271: H480 — Onset-Conditioned Midfix Sampling

Problem from exp_270: position-agnostic midfix over-corrects B-LL by +0.55 chars.
Root cause: B-LL -am/-dy words (d/ol/ot onset, short) get midfixes from long ch/sh-onset
words' distribution — these don't have midfixes in VMS but get them in simulation.

Fix: build ONSET-CONDITIONED midfix distributions for LF and LL.
  For each onset class, separately compute midfix empty_frac and non-empty list.
  When generating a word: sample onset → look up onset-conditioned midfix → apply.

Expected: d-onset B-LL words get empty midfixes (correct); ch/sh-onset get longer ones.
B-LL mean word length should move closer to VMS 5.015.
B-dialect Menzerath r should improve toward -0.206.
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_RUNS = 30; SEED = 271000

A_PARAMS = dict(
    p_blind=0.0505, d_boost=0.2430, r_lf=0.266, r_mid=0.87,
    p_stutter=0.002, mu_len=5.64, sigma_len=2.5,
    cp=0.55, mp=0.90, p_qokch=0.12, p_chqok=0.00, p_lf=1.0,
    p_y_y=0.10, p_o_o=0.10, p_sh_qok=0.10, window=20,
)
B_PARAMS = dict(
    p_blind=0.115, r_lf=0.12, r_mid=0.25,
    p_stutter=0.006, mu_len=8.4, sigma_len=3.0,
    cp=0.55, mp=0.90, p_qokch=0.12, p_chqok=0.12, p_lf=1.0,
    p_y_y=0.00, p_o_o=0.00, p_sh_qok=0.00, window=20,
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
        if w.startswith(prefix): return label, len(prefix)
    return 'other', 0

def get_onset_label(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0

def get_suffix(w):
    for suf in SUFFIX_PATTERNS:
        if w.endswith(suf): return suf
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

def filter_other(dist):
    filtered = {k: v for k, v in dist.items() if k != 'other'}
    total = sum(filtered.values())
    return {k: v/total for k, v in filtered.items()} if total > 0 else filtered

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
    return {o: cnt/n for o, cnt in Counter(get_onset_label(w) for w in words).items()}

def build_suffix_dist(words):
    suf_ctr = Counter(get_suffix(w) for w in words)
    total = max(1, len(words))
    return {s: cnt/total for s, cnt in suf_ctr.items()}

def build_onset_conditioned_midfix(words):
    """
    Build onset-conditioned midfix distributions from words with recognized
    non-edy, non-other suffixes.

    Returns dict: onset_label → {'empty_frac': float, 'non_empty': list_of_midfixes}
    If insufficient data for an onset (N<5 recognized-suffix words), falls back to
    'global' entry which is the pooled distribution across all onsets.
    """
    per_onset = defaultdict(list)  # onset → list of midfixes (including empty strings)

    for w in words:
        suf = get_suffix(w)
        if suf in ('edy', 'eedy', 'other'): continue
        label, onset_len = get_onset(w)
        mf = w[onset_len:-len(suf)]
        per_onset[label].append(mf)

    result = {}
    all_midfixes = []
    for label, mfs in per_onset.items():
        all_midfixes.extend(mfs)
        empty_frac = sum(1 for m in mfs if not m) / len(mfs) if mfs else 1.0
        non_empty = [m for m in mfs if m]
        result[label] = {
            'empty_frac': empty_frac,
            'non_empty': non_empty if non_empty else [''],
            'n': len(mfs)
        }

    # Global fallback
    if all_midfixes:
        empty_frac = sum(1 for m in all_midfixes if not m) / len(all_midfixes)
        non_empty = [m for m in all_midfixes if m]
        result['__global__'] = {
            'empty_frac': empty_frac,
            'non_empty': non_empty if non_empty else [''],
            'n': len(all_midfixes)
        }
    else:
        result['__global__'] = {'empty_frac': 1.0, 'non_empty': [''], 'n': 0}

    return result

def sample_midfix(onset_label, midfix_dist, rng, min_n=5):
    """Sample midfix conditioned on onset. Falls back to global if onset has insufficient data."""
    if onset_label in midfix_dist and midfix_dist[onset_label]['n'] >= min_n:
        entry = midfix_dist[onset_label]
    else:
        entry = midfix_dist.get('__global__', {'empty_frac': 1.0, 'non_empty': ['']})

    if rng.random() < entry['empty_frac']:
        return ''
    return rng.choice(entry['non_empty'])

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

def make_word_sim_with_midfix(onset, midfix, suffix):
    return onset + midfix + suffix

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

def random_eva_word(onset_w, suffix_w, rng):
    o = rng.choices(list(onset_w.keys()), weights=list(onset_w.values()))[0]
    s = rng.choices(list(suffix_w.keys()), weights=list(suffix_w.values()))[0]
    return make_word_sim(o, s, rng)

def cipher_lf_conditioned(onset_lf, suffix_lf_dist, p_lf, midfix_lf_cond, rng):
    """LF word generation with onset-conditioned midfix."""
    if rng.random() < p_lf:
        o = rng.choices(list(onset_lf.keys()), weights=list(onset_lf.values()))[0]
        s = rng.choices(list(suffix_lf_dist.keys()), weights=list(suffix_lf_dist.values()))[0]
        if s in ('edy', 'eedy'): return make_word_sim(o, s, rng)
        if s == 'other': return make_word_sim(o, s, rng)
        mf = sample_midfix(o, midfix_lf_cond, rng)
        return make_word_sim_with_midfix(o, mf, s)
    o = rng.choices(list(onset_lf.keys()), weights=list(onset_lf.values()))[0]
    s = rng.choices(list(suffix_lf_dist.keys()), weights=list(suffix_lf_dist.values()))[0]
    return make_word_sim(o, s, rng)

def cipher_ll_conditioned(onset_mid, suffix_ll_dist, ll_onsets, onset_ll, p_blind,
                          midfix_ll_cond, rng):
    """LL word generation with onset-conditioned midfix."""
    if rng.random() < p_blind:
        o = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return o + 'am'
    o = rng.choices(list(onset_ll.keys()), weights=list(onset_ll.values()))[0]
    s = rng.choices(list(suffix_ll_dist.keys()), weights=list(suffix_ll_dist.values()))[0]
    if s in ('edy', 'eedy'): return make_word_sim(o, s, rng)
    if s == 'other': return make_word_sim(o, s, rng)
    mf = sample_midfix(o, midfix_ll_cond, rng)
    return make_word_sim_with_midfix(o, mf, s)

def draw_buf(buf, prev_onset, p_qokch, p_chqok, p_y_y, p_o_o, p_sh_qok, rng):
    bl = list(buf)
    if not bl: return None
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        cw = [w for w in bl if get_onset_label(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'ch' and p_chqok > 0 and rng.random() < p_chqok:
        qw = [w for w in bl if get_onset_label(w) == 'qok']
        if qw: return rng.choice(qw)
    if prev_onset == 'y' and p_y_y > 0 and rng.random() < p_y_y:
        yw = [w for w in bl if get_onset_label(w) == 'y']
        if yw: return rng.choice(yw)
    if prev_onset == 'o' and p_o_o > 0 and rng.random() < p_o_o:
        ow = [w for w in bl if get_onset_label(w) == 'o']
        if ow: return rng.choice(ow)
    if prev_onset == 'sh' and p_sh_qok > 0 and rng.random() < p_sh_qok:
        qw = [w for w in bl if get_onset_label(w) == 'qok']
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

def pearson_r(xs, ys):
    n = len(xs)
    if n < 2: return 0.0
    mx = sum(xs)/n; my = sum(ys)/n
    num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    dx = math.sqrt(sum((x-mx)**2 for x in xs))
    dy = math.sqrt(sum((y-my)**2 for y in ys))
    return num/(dx*dy) if dx*dy > 0 else 0.0

def menzerath_r(lines):
    xs, ys = [], []
    for line in lines:
        if len(line) < 2: continue
        xs.append(len(line)); ys.append(sum(len(w) for w in line)/len(line))
    return pearson_r(xs, ys)

def position_mean_len(lines):
    def m(lst): return sum(lst)/len(lst) if lst else 0.0
    return (m([len(l[0]) for l in lines if l]),
            m([len(w) for l in lines for w in l[1:-1] if len(l) > 2]),
            m([len(l[-1]) for l in lines if len(l) > 1]))

def run_sim(latin_words, onset_mid, suffix_mid_sup,
            onset_lf, suffix_lf_dist, midfix_lf_cond,
            onset_ll, suffix_ll_dist, ll_onsets, midfix_ll_cond,
            params, target_lines, rng):
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
                ew = cipher_lf_conditioned(onset_lf, suffix_lf_dist, params['p_lf'],
                                           midfix_lf_cond, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll_conditioned(onset_mid, suffix_ll_dist, ll_onsets, onset_ll,
                                           params['p_blind'], midfix_ll_cond, rng)
            else:
                if prev_word is not None and params['p_stutter'] > 0 and rng.random() < params['p_stutter']:
                    ew = prev_word
                elif buf and rng.random() < params['cp']:
                    src = draw_buf(buf, prev_onset,
                                   params['p_qokch'], params['p_chqok'],
                                   params['p_y_y'], params['p_o_o'], params['p_sh_qok'], rng)
                    if src is None: src = random_eva_word(onset_mid, suffix_mid_sup, rng)
                    ew = timm_modify(src, onset_mid, suffix_mid_sup, rng) if rng.random() < params['mp'] else src
                else:
                    ew = random_eva_word(onset_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset_label(ew); prev_word = ew
            line.append(ew)
        lines.append(line); pos += n_words
    return lines[:target_lines]

def print_onset_midfix_summary(midfix_cond, pos_name):
    print(f"  {pos_name} onset-conditioned midfix:")
    for o, entry in sorted(midfix_cond.items(), key=lambda x: -x[1]['n']):
        if o == '__global__': continue
        if entry['n'] < 3: continue
        non_empty_rate = 1.0 - entry['empty_frac']
        mean_ne_len = sum(len(m) for m in entry['non_empty'])/len(entry['non_empty']) if entry['non_empty'] else 0
        expected_add = non_empty_rate * mean_ne_len
        print(f"    {o:>5}: n={entry['n']:>4}  non_empty={non_empty_rate:.3f}  "
              f"mean_ne_len={mean_ne_len:.2f}  expected_add={expected_add:.3f}")

def main():
    print("Loading Latin corpus...")
    latin_words = load_latin(LATIN_CORPUS)

    for dialect_label, params in [('A', A_PARAMS), ('B', B_PARAMS)]:
        print(f"\n{'='*70}")
        print(f"DIALECT: {dialect_label}")
        print(f"{'='*70}")

        vms_lines = parse_vms(dialect_label)
        all_words = [w for l in vms_lines for w in l]
        mid_words = [w for l in vms_lines for w in l[1:-1] if len(l) > 2]
        lf_words  = [l[0] for l in vms_lines if l]
        ll_words  = [l[-1] for l in vms_lines if len(l) > 1]

        onset_mid = filter_other(build_onset_dist(mid_words))
        onset_lf  = filter_other(build_onset_dist(lf_words))
        onset_ll  = filter_other(build_onset_dist(ll_words))

        suffix_global = build_suffix_dist(all_words)
        suffix_lf_dist = build_suffix_dist(lf_words)
        suffix_ll_dist = build_suffix_dist(ll_words)
        suffix_mid_sup = make_suppressed_suffix(suffix_global, params.get('r_mid', 0.25))

        midfix_lf_cond = build_onset_conditioned_midfix(lf_words)
        midfix_ll_cond = build_onset_conditioned_midfix(ll_words)

        d_boost_w = params.get('d_boost', 0.0)
        ll_onsets = build_ll_onsets(onset_ll, d_boost_w) if d_boost_w > 0 else onset_ll.copy()

        vms_r = menzerath_r(vms_lines)
        vms_lf, vms_mid, vms_ll = position_mean_len(vms_lines)

        print(f"\nVMS: r={vms_r:.4f}  LF={vms_lf:.3f}  MID={vms_mid:.3f}  LL={vms_ll:.3f}")
        print_onset_midfix_summary(midfix_lf_cond, 'LF')
        print_onset_midfix_summary(midfix_ll_cond, 'LL')

        sim_rs = []; sim_lf_means = []; sim_mid_means = []; sim_ll_means = []
        rng = random.Random(SEED)
        for run in range(N_RUNS):
            sim_lines = run_sim(
                latin_words, onset_mid, suffix_mid_sup,
                onset_lf, suffix_lf_dist, midfix_lf_cond,
                onset_ll, suffix_ll_dist, ll_onsets, midfix_ll_cond,
                params, len(vms_lines), rng
            )
            sim_rs.append(menzerath_r(sim_lines))
            lf_m, mid_m, ll_m = position_mean_len(sim_lines)
            sim_lf_means.append(lf_m); sim_mid_means.append(mid_m); sim_ll_means.append(ll_m)

        def mean(lst): return sum(lst)/len(lst) if lst else 0.0
        def sd(lst): m=mean(lst); return math.sqrt(sum((x-m)**2 for x in lst)/len(lst)) if lst else 0.0

        sim_r_mean = mean(sim_rs); sim_r_sd = sd(sim_rs)
        sim_lf = mean(sim_lf_means); sim_mid = mean(sim_mid_means); sim_ll = mean(sim_ll_means)
        n_neg = sum(1 for r in sim_rs if r < 0)

        print(f"\nSIM (N={N_RUNS}): r={sim_r_mean:.4f}±{sim_r_sd:.4f}  ({n_neg}/{N_RUNS} neg)")
        print(f"  Position: LF={sim_lf:.3f}  MID={sim_mid:.3f}  LL={sim_ll:.3f}")
        print(f"  Δ vs VMS:  r={vms_r-sim_r_mean:.4f}  LF={vms_lf-sim_lf:.3f}  MID={vms_mid-sim_mid:.3f}  LL={vms_ll-sim_ll:.3f}")
        print(f"\nComparison:")
        exp268 = {'A': (0.078, 4.708, 4.775), 'B': (0.097, 4.857, 4.947)}[dialect_label]
        exp270 = {'A': (-0.189, 5.839, 5.933), 'B': (-0.052, 5.867, 5.561)}[dialect_label]
        print(f"  exp_268 (no midfix):          r={exp268[0]:+.3f}  LF={exp268[1]:.3f}  LL={exp268[2]:.3f}")
        print(f"  exp_270 (position midfix):    r={exp270[0]:+.3f}  LF={exp270[1]:.3f}  LL={exp270[2]:.3f}")
        print(f"  exp_271 (onset-cond midfix):  r={sim_r_mean:+.3f}  LF={sim_lf:.3f}  LL={sim_ll:.3f}")
        print(f"  VMS target:                   r={vms_r:+.3f}  LF={vms_lf:.3f}  LL={vms_ll:.3f}")

        # Global word_len_mean
        vms_gl = sum(len(w) for l in vms_lines for w in l)/max(1,sum(len(l) for l in vms_lines))
        rng2 = random.Random(SEED)
        one_sim = run_sim(
            latin_words, onset_mid, suffix_mid_sup,
            onset_lf, suffix_lf_dist, midfix_lf_cond,
            onset_ll, suffix_ll_dist, ll_onsets, midfix_ll_cond,
            params, len(vms_lines), rng2
        )
        sim_gl = sum(len(w) for l in one_sim for w in l)/max(1,sum(len(l) for l in one_sim))
        pct = sim_gl/vms_gl*100
        print(f"\nGlobal word_len_mean: VMS={vms_gl:.3f}  SIM={sim_gl:.3f}  ({pct:.1f}% — {'PASS' if 80<=pct<=120 else 'FAIL'})")

    print("\nDone.")

if __name__ == '__main__':
    main()
