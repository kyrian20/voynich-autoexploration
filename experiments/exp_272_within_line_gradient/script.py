"""
exp_272: H481 — VMS B-Dialect Within-Line Word Length Gradient

From exp_271 result: VMS B-dialect shows word length gradient within lines.
Words at high word-index positions within long lines are shorter than words at
low word-index positions. The simulation stays flat (~5.4-5.6 chars across all
word indices) because all MID words are drawn from the same position-agnostic buffer.

This gradient (shorter words deeper in long lines) is the architectural cause of
the B-dialect Menzerath magnitude gap (sim r=-0.055 vs VMS r=-0.206).

Analysis:
1. Mean word length by word_index, stratified by line_length bucket (VMS vs sim)
2. Gradient coefficient: regression of word_index on word_length within long lines (linlen>=8)
3. A vs B dialect comparison (does A show weaker gradient, explaining why A matches sim?)
4. Word index as fraction of line length (normalized position) — is gradient universal?
5. Onset composition by word index — do shorter onsets dominate at high word-index?
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_RUNS = 10; SEED = 272000

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

def pearson_r(xs, ys):
    n = len(xs)
    if n < 2: return 0.0
    mx = sum(xs)/n; my = sum(ys)/n
    num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    dx = math.sqrt(sum((x-mx)**2 for x in xs))
    dy = math.sqrt(sum((y-my)**2 for y in ys))
    return num/(dx*dy) if dx*dy > 0 else 0.0

def linreg_slope(xs, ys):
    """Slope of linear regression of ys on xs."""
    n = len(xs)
    if n < 2: return 0.0
    mx = sum(xs)/n; my = sum(ys)/n
    num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    den = sum((x-mx)**2 for x in xs)
    return num/den if den > 0 else 0.0

def analyze_gradient(lines, label=''):
    """
    Section 1: mean word length by word index (absolute), stratified by linlen bucket.
    Section 2: mean word length by normalized position (word_index / line_length).
    Section 3: gradient coefficient within long lines (linlen >= 8).
    Section 4: onset composition by word index quintile.
    """
    # Build (linlen, word_idx, word_len) tuples
    records = []
    for line in lines:
        L = len(line)
        for i, w in enumerate(line):
            records.append((L, i, len(w), get_onset_label(w)))

    # Section 1: by linlen bucket and word_index
    print(f"\n--- {label}: Word Length by Word Index and Line Length Bucket ---")
    buckets = [(2,4,'2-4'), (5,7,'5-7'), (8,10,'8-10'), (11,20,'11+')]
    for blo, bhi, bname in buckets:
        # Collect by word index
        by_idx = defaultdict(list)
        for L, i, wlen, onset in records:
            if blo <= L <= bhi:
                by_idx[i].append(wlen)
        max_idx = max(by_idx.keys()) if by_idx else 0
        idx_list = sorted(by_idx.keys())
        if not idx_list:
            print(f"  Linlen {bname}: no data")
            continue
        n_total = sum(len(v) for v in by_idx.values())
        print(f"  Linlen {bname} (N_words={n_total}):")
        row = []
        for i in idx_list[:12]:  # cap at first 12 positions
            vals = by_idx[i]
            row.append(f"idx{i}={sum(vals)/len(vals):.2f}(n={len(vals)})")
        print("    " + "  ".join(row))

    # Section 2: Normalized position analysis
    print(f"\n--- {label}: Word Length by Normalized Position (Quintile) ---")
    # Group into 5 quintiles of fractional position i/(L-1)
    norm_bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    norm_bin_names = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
    norm_by_bin = [[] for _ in range(5)]
    for L, i, wlen, onset in records:
        if L < 3: continue  # need at least 3 words for normalized position to be meaningful
        frac = i / (L - 1)
        for b in range(5):
            if frac <= norm_bins[b+1]:
                norm_by_bin[b].append(wlen)
                break
    print("  " + "  ".join(f"{name}: {sum(v)/len(v):.3f}(n={len(v)})" if v else f"{name}: --"
                           for name, v in zip(norm_bin_names, norm_by_bin)))

    # Section 3: gradient coefficient in long lines (linlen >= 8)
    print(f"\n--- {label}: Gradient Coefficient in Long Lines (linlen >= 8) ---")
    long_xs = [i for L, i, wlen, onset in records if L >= 8]
    long_ys = [wlen for L, i, wlen, onset in records if L >= 8]
    if long_xs:
        slope = linreg_slope(long_xs, long_ys)
        r = pearson_r(long_xs, long_ys)
        mean_len = sum(long_ys)/len(long_ys)
        n = len(long_xs)
        print(f"  N={n}  mean_len={mean_len:.3f}  slope(chars/word)={slope:.4f}  r={r:.4f}")
        print(f"  Interpretation: word length changes {slope:.3f} chars per word-index step")
        print(f"  Over 10 words: total gradient = {slope*10:.3f} chars")
    else:
        print("  No long lines found")

    # Also: strictly MID words in long lines (exclude LF and LL)
    mid_xs = [i for L, i, wlen, onset in records if L >= 8 and 0 < i < L-1]
    mid_ys = [wlen for L, i, wlen, onset in records if L >= 8 and 0 < i < L-1]
    if mid_xs:
        slope = linreg_slope(mid_xs, mid_ys)
        r = pearson_r(mid_xs, mid_ys)
        mean_len = sum(mid_ys)/len(mid_ys)
        print(f"  MID only: N={len(mid_xs)}  mean={mean_len:.3f}  slope={slope:.4f}  r={r:.4f}")

    # Section 4: onset composition by word index in long lines
    print(f"\n--- {label}: Onset Composition by Word Index in Long Lines (linlen>=8, MID only) ---")
    onset_by_idx = defaultdict(Counter)
    for L, i, wlen, onset in records:
        if L >= 8 and 0 < i < L-1:
            onset_by_idx[i][onset] += 1
    for i in sorted(onset_by_idx.keys())[:10]:
        ctr = onset_by_idx[i]
        total = sum(ctr.values())
        # Show top 3 onsets and 'other' fraction
        top = ctr.most_common(3)
        top_str = ", ".join(f"{o}:{cnt/total:.2f}" for o, cnt in top)
        other_frac = ctr.get('other', 0) / total
        short_onsets = sum(ctr.get(o, 0) for o in ('d','s','y','k','t','l','r','p','f','o')) / total
        print(f"  idx{i:2d} (n={total:4d}): top3=[{top_str}]  short_onset={short_onsets:.3f}  other={other_frac:.3f}")

    return {
        'norm_means': [sum(v)/len(v) if v else None for v in norm_by_bin],
        'gradient_slope': linreg_slope(long_xs, long_ys) if long_xs else None,
        'gradient_r': pearson_r(long_xs, long_ys) if long_xs else None,
    }

# ---- Simulation (using exp_270 position-agnostic midfix architecture) ----

def build_onset_dist(words):
    n = max(1, len(words))
    return {o: cnt/n for o, cnt in Counter(get_onset_label(w) for w in words).items()}

def build_suffix_dist(words):
    suf_ctr = Counter(get_suffix(w) for w in words)
    total = max(1, len(words))
    return {s: cnt/total for s, cnt in suf_ctr.items()}

def build_midfix_dist(words):
    """Build position-agnostic midfix dist from recognized non-edy, non-other suffix words."""
    midfixes = []
    for w in words:
        suf = get_suffix(w)
        if suf in ('edy', 'eedy', 'other'): continue
        _, onset_len = get_onset(w)
        mf = w[onset_len:-len(suf)]
        midfixes.append(mf)
    if not midfixes:
        return [''], 1.0
    empty_frac = sum(1 for m in midfixes if not m) / len(midfixes)
    non_empty = [m for m in midfixes if m]
    return (non_empty if non_empty else ['']), empty_frac

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

def cipher_lf(onset_lf, suffix_lf_dist, p_lf, midfix_lf, midfix_lf_empty_frac, rng):
    if rng.random() < p_lf:
        o = rng.choices(list(onset_lf.keys()), weights=list(onset_lf.values()))[0]
        s = rng.choices(list(suffix_lf_dist.keys()), weights=list(suffix_lf_dist.values()))[0]
        if s in ('edy', 'eedy'): return make_word_sim(o, s, rng)
        if s == 'other': return make_word_sim(o, s, rng)
        mf = '' if rng.random() < midfix_lf_empty_frac else rng.choice(midfix_lf)
        return make_word_sim_with_midfix(o, mf, s)
    o = rng.choices(list(onset_lf.keys()), weights=list(onset_lf.values()))[0]
    s = rng.choices(list(suffix_lf_dist.keys()), weights=list(suffix_lf_dist.values()))[0]
    return make_word_sim(o, s, rng)

def cipher_ll(onset_mid, suffix_ll_dist, ll_onsets, onset_ll, p_blind,
              midfix_ll, midfix_ll_empty_frac, rng):
    if rng.random() < p_blind:
        o = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return o + 'am'
    o = rng.choices(list(onset_ll.keys()), weights=list(onset_ll.values()))[0]
    s = rng.choices(list(suffix_ll_dist.keys()), weights=list(suffix_ll_dist.values()))[0]
    if s in ('edy', 'eedy'): return make_word_sim(o, s, rng)
    if s == 'other': return make_word_sim(o, s, rng)
    mf = '' if rng.random() < midfix_ll_empty_frac else rng.choice(midfix_ll)
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

def run_sim(latin_words, onset_mid, suffix_mid_sup,
            onset_lf, suffix_lf_dist, midfix_lf, midfix_lf_ef,
            onset_ll, suffix_ll_dist, ll_onsets, midfix_ll, midfix_ll_ef,
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
                ew = cipher_lf(onset_lf, suffix_lf_dist, params['p_lf'],
                               midfix_lf, midfix_lf_ef, rng)
            elif i == len(chunk)-1:
                ew = cipher_ll(onset_mid, suffix_ll_dist, ll_onsets, onset_ll,
                               params['p_blind'], midfix_ll, midfix_ll_ef, rng)
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

def main():
    print("Loading Latin corpus...")
    latin_words = load_latin(LATIN_CORPUS)

    results = {}

    for dialect_label, params in [('A', A_PARAMS), ('B', B_PARAMS)]:
        print(f"\n{'='*70}")
        print(f"DIALECT {dialect_label} — VMS CORPUS ANALYSIS")
        print(f"{'='*70}")

        vms_lines = parse_vms(dialect_label)
        all_words = [w for l in vms_lines for w in l]
        mid_words = [w for l in vms_lines for w in l[1:-1] if len(l) > 2]
        lf_words  = [l[0] for l in vms_lines if l]
        ll_words  = [l[-1] for l in vms_lines if len(l) > 1]

        print(f"VMS lines: {len(vms_lines)}, words: {len(all_words)}")
        print(f"LF words: {len(lf_words)}, MID words: {len(mid_words)}, LL words: {len(ll_words)}")

        vms_result = analyze_gradient(vms_lines, label=f'VMS-{dialect_label}')

        # Run simulation
        onset_mid = filter_other(build_onset_dist(mid_words))
        onset_lf  = filter_other(build_onset_dist(lf_words))
        onset_ll  = filter_other(build_onset_dist(ll_words))

        suffix_global = build_suffix_dist(all_words)
        suffix_lf_dist = build_suffix_dist(lf_words)
        suffix_ll_dist = build_suffix_dist(ll_words)
        suffix_mid_sup = make_suppressed_suffix(suffix_global, params.get('r_mid', 0.25))

        midfix_lf, midfix_lf_ef = build_midfix_dist(lf_words)
        midfix_ll, midfix_ll_ef = build_midfix_dist(ll_words)

        d_boost_w = params.get('d_boost', 0.0)
        ll_onsets = build_ll_onsets(onset_ll, d_boost_w) if d_boost_w > 0 else onset_ll.copy()

        print(f"\n{'='*70}")
        print(f"DIALECT {dialect_label} — SIMULATION (N_runs={N_RUNS} combined)")
        print(f"{'='*70}")

        # Aggregate simulation lines across runs for gradient analysis
        rng = random.Random(SEED)
        all_sim_lines = []
        for run in range(N_RUNS):
            sim_lines = run_sim(
                latin_words, onset_mid, suffix_mid_sup,
                onset_lf, suffix_lf_dist, midfix_lf, midfix_lf_ef,
                onset_ll, suffix_ll_dist, ll_onsets, midfix_ll, midfix_ll_ef,
                params, len(vms_lines), rng
            )
            all_sim_lines.extend(sim_lines)

        sim_result = analyze_gradient(all_sim_lines, label=f'SIM-{dialect_label}')

        # Section 5: Gradient comparison summary
        print(f"\n--- GRADIENT COMPARISON SUMMARY: {dialect_label}-dialect ---")
        print(f"  VMS gradient slope (long lines): {vms_result['gradient_slope']:.4f} chars/word-idx")
        print(f"  Sim gradient slope (long lines): {sim_result['gradient_slope']:.4f} chars/word-idx")
        print(f"  Gap: {vms_result['gradient_slope'] - sim_result['gradient_slope']:.4f}")
        print(f"  VMS gradient r: {vms_result['gradient_r']:.4f}")
        print(f"  Sim gradient r: {sim_result['gradient_r']:.4f}")
        print(f"  VMS normalized quintile means: {[f'{v:.3f}' if v else '--' for v in vms_result['norm_means']]}")
        print(f"  Sim normalized quintile means: {[f'{v:.3f}' if v else '--' for v in sim_result['norm_means']]}")

        results[dialect_label] = {'vms': vms_result, 'sim': sim_result}

    # Cross-dialect comparison
    print(f"\n{'='*70}")
    print("CROSS-DIALECT GRADIENT SUMMARY")
    print(f"{'='*70}")
    for d in ['A', 'B']:
        vms_slope = results[d]['vms']['gradient_slope']
        sim_slope = results[d]['sim']['gradient_slope']
        print(f"  {d}: VMS slope={vms_slope:.4f}  Sim slope={sim_slope:.4f}  Gap={vms_slope - sim_slope:.4f}")
    print()
    print("If B shows steeper (more negative) VMS gradient than A, and sim shows near-zero")
    print("slope for both, this confirms within-line gradient is the B-dialect Menzerath gap.")

if __name__ == '__main__':
    main()
