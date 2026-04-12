"""
exp_578: Q007 Copy-Buffer Amplification Diagnosis

exp_577 found: VMS sh/ch/d adj_rate ≈ random expectation from their CP90 sizes.
exp_304 found: clamping vocabulary raises adj_rate from 0.009 to 0.0114 (126.3% of VMS).

This experiment directly tests the copy-buffer amplification hypothesis:
When vocabulary is clamped (sh/ch/d reduced to VMS CP90), does the copy-buffer
generate MORE per-onset identical pairs than VMS has from its natural CP90?

If copy-buffer amplification is real:
- Baseline simulation (large vocab): per-onset adj_rate << VMS (more diversity)
- Clamped simulation (VMS vocab): per-onset adj_rate >> VMS (buffer collision)
- VMS: per-onset adj_rate ≈ 1/CP90 (random-pool baseline)

The pattern should be: baseline << VMS << clamped for sh/ch/d.
This would confirm the constraint is a simulation artifact, not a VMS property.

METHOD: Run N=5 trials of:
  1. Baseline architecture (exp_314 params, no lexicon clamping)
  2. clamp_sparse_only (qok/ok/ot/qot clamped, sh/ch/d free)
  3. clamp_all_7 (all 7 classes clamped to VMS lexicon)
  4. clamp_sh_ch_d_only (ONLY sh/ch/d clamped, sparse classes free)

For each condition, measure:
  - Global adj_rate
  - Per-onset adj_rate for each major onset class
  - Total unique MID word types

Compare to VMS measurements from exp_577.
"""

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
SEED = 578000

# Architecture params (exp_314)
P_SHORT=0.060; P_LONG=0.180; THRESH_SHORT=5; THRESH_LONG=10; MEAN_N=8.4
P_LF=1.0; CP=0.55; MP=0.90; P_CHQOK=0.12; P_QOKCH=0.12; P_STUTTER=0.006
MU_LEN=8.4; SIGMA_LEN=3.0; P_MF=0.20; P_LF_MF=0.50; P_LL_MF=0.00
GAMMA=0.30; ALPHA=0.20; BETA_BASE=0.50; BETA_SCALE=1.8; P_BLIND=0.115
R_LF=0.12; R_MID=0.20
IDX_THRESH=2; SHORT_THRESH=2; TARGET_LINES=2411; WINDOW=20
MAX_RETRY=10; N_TRIALS=5
LL_BASE=8; LL_SLOPE=0.30; LL_N_REF=5; LL_MIN_CAP=3
L_BASE=5.40; L_SLOPE=-0.053
SHORT_ONSETS={'d','s','y','k','t','l','r','p','f','o'}
EVA_CHARS=list('acdehiklmnoqrsty')
ONSET_ORDER=[
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o'),
]
SUFFIX_PATTERNS=['eedy','edy','aiin','ain','am','ey','ol','or','al','ar','dy']
SPARSE_ONSETS={'qok','ok','ot','qot'}

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
def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total >= 0.05 else 'A'
def weighted_choice(rng, dist):
    r = rng.random(); cum = 0.0
    for k,v in dist.items():
        cum += v
        if r < cum: return k
    return list(dist.keys())[-1]

def parse_vms_b_lines():
    folio_word_stats = defaultdict(lambda: {'total':0,'edy':0,'eedy':0})
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
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            if folio_dialect.get(fb, 'unknown') != 'B': continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
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
        if (edy_len := get_edy_suffix_len(w)):
            mid_end = len(w)-edy_len; midfix = w[onset_len:mid_end]
            if len(midfix) >= 1: midfix = midfix[:-1]
        else:
            midfix = w[onset_len:len(w)-suf_len]
        midfix_cnt[midfix] += 1
    total = sum(midfix_cnt.values())
    if total == 0: return {}, 0.0
    p_non_empty = sum(v for k,v in midfix_cnt.items() if k != '')/total
    non_empty_raw = {mf:v for mf,v in midfix_cnt.items() if mf != ''}
    non_empty_total = sum(non_empty_raw.values())
    return {mf:v/non_empty_total for mf,v in non_empty_raw.items()} if non_empty_total else {}, p_non_empty

def compute_vms_dists(b_lines):
    all_words = [w for l in b_lines for w in l]
    lf_words = [l[0] for l in b_lines if l]
    ll_words = [l[-1] for l in b_lines if len(l) > 1]
    mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
    def build_onset(words):
        cnt = Counter(get_onset(w) for w in words); cnt.pop('other', None)
        total = sum(cnt.values())
        return {k:v/total for k,v in cnt.items()} if total else {}
    def build_suffix(words):
        cnt = Counter(get_suffix(w) for w in words); total = sum(cnt.values())
        return {k:v/total for k,v in cnt.items()} if total else {}
    onset_lf = build_onset(lf_words); onset_ll = build_onset(ll_words)
    onset_mid = build_onset(mid_words); suffix_global = build_suffix(all_words)
    mid_nemed, mid_p = build_midfix_dist(mid_words)
    lf_nemed, lf_p = build_midfix_dist(lf_words)
    ll_nemed, ll_p = build_midfix_dist(ll_words)
    d_global = Counter(get_onset(w) for w in all_words).get('d',0)/len(all_words)
    ll_d = Counter(get_onset(w) for w in ll_words).get('d',0)/len(ll_words)
    d_ll_target = ll_d/d_global if d_global else 0
    d_ll_non_blind_enr = onset_ll.get('d',0)/d_global if d_global else 0
    d_boost = d_global*(d_ll_target-(1-P_BLIND)*d_ll_non_blind_enr)/P_BLIND
    d_boost = max(0.0, min(d_boost, 1.0))
    remaining = 1.0 - d_boost
    base = {o:v for o,v in onset_ll.items() if o != 'd'}
    base_total = sum(base.values())
    ll_onsets = {o:v/base_total*remaining for o,v in base.items()} if base_total else {}
    ll_onsets['d'] = d_boost
    return {'onset_lf':onset_lf, 'onset_ll':onset_ll, 'onset_mid':onset_mid,
            'suffix_global':suffix_global, 'mid_nemed':mid_nemed, 'lf_nemed':lf_nemed,
            'll_nemed':ll_nemed, 'll_onsets':ll_onsets, 'mid_words':mid_words, 'd_boost':d_boost}

def make_suppressed_suffix(sg, r_am):
    am_w = sg.get('am',0); new_am = am_w*r_am; delta = am_w-new_am; non_am = 1.0-am_w
    return {suf:(new_am if suf == 'am' else w+(w/non_am)*delta if non_am > 0 else w)
            for suf,w in sg.items()}

def make_word_sim(onset, suffix, rng, nemed, p_mf):
    midfix = ''
    if nemed and rng.random() < p_mf: midfix = weighted_choice(rng, nemed)
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset + midfix + rng.choice(['a','ai','o','oi','e','ei']) + suffix
    return onset + midfix + suffix

def apply_suffix_length_bias(suf_w, word_idx, beta):
    if beta == 0.0 or word_idx < IDX_THRESH: return suf_w
    new_w = {}
    for suf,w in suf_w.items():
        suf_len = len(suf) if suf != 'other' else 5
        penalty = max(0, suf_len-SHORT_THRESH)
        new_w[suf] = w*math.exp(-beta*penalty)
    total = sum(new_w.values())
    return {s:v/total for s,v in new_w.items()} if total > 0 else suf_w

def timm_modify(word, onset_mid, suffix_mid, rng):
    if not word: return word
    onset_len = get_onset_len(word); edy_len = get_edy_suffix_len(word)
    mod_start = onset_len; mod_end = len(word)-edy_len
    if mod_start >= mod_end:
        return make_word_sim(weighted_choice(rng,onset_mid), weighted_choice(rng,suffix_mid), rng, {}, 0.0)
    op = rng.choice(['replace','insert','delete'])
    if op == 'replace':
        pos = rng.randint(mod_start, mod_end-1)
        return word[:pos]+rng.choice(EVA_CHARS)+word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(mod_start, mod_end)
        return word[:pos]+rng.choice(EVA_CHARS)+word[pos:]
    else:
        if mod_end-mod_start <= 1:
            return word[:mod_start]+rng.choice(EVA_CHARS)+word[mod_start+1:]
        pos = rng.randint(mod_start, mod_end-1)
        return word[:pos]+word[pos+1:]

def build_vms_lexicons(mid_words, onset_classes):
    """Build per-onset VMS lexicons with frequency weights."""
    lexicons = {}
    for onset_class in onset_classes:
        wds = [w for w in mid_words if get_onset(w) == onset_class]
        lexicons[onset_class] = wds  # Keep duplicates for frequency-weighted sampling
    return lexicons

def clamp_to_lexicon(word, lexicons, rng):
    onset = get_onset(word)
    if onset in lexicons and lexicons[onset]:
        return rng.choice(lexicons[onset])
    return word

def get_p_blind_n(n):
    if n <= THRESH_SHORT: return P_SHORT*(P_BLIND/0.115)
    if n >= THRESH_LONG: return P_LONG*(P_BLIND/0.115)
    frac = (n-THRESH_SHORT)/(THRESH_LONG-THRESH_SHORT)
    base = P_SHORT+frac*(P_LONG-P_SHORT)
    return base*(P_BLIND/0.115)

def get_max_ll_len(n):
    return max(LL_MIN_CAP, round(LL_BASE-LL_SLOPE*max(0, n-LL_N_REF)))

def draw_buf(buf, prev_onset, rng, word_idx):
    buf_list = list(buf)
    if not buf_list: return None
    preferred = None
    if prev_onset == 'qok' and rng.random() < P_QOKCH:
        ch_words = [w for w in buf_list if get_onset(w) == 'ch']
        if ch_words: preferred = ch_words
    elif prev_onset == 'ch' and rng.random() < P_CHQOK:
        qok_words = [w for w in buf_list if get_onset(w) == 'qok']
        if qok_words: preferred = qok_words
    candidates = preferred if preferred else buf_list
    if GAMMA == 0.0: return rng.choice(candidates)
    L_target = L_BASE+L_SLOPE*word_idx
    weights = [math.exp(-GAMMA*(len(w)-L_target)**2) for w in candidates]
    total = sum(weights)
    if total == 0: return rng.choice(candidates)
    r = rng.random()*total; cum = 0.0
    for w,wt in zip(candidates, weights):
        cum += wt
        if r < cum: return w
    return candidates[-1]

def generate_ll_word(rng, vms_d, max_ll):
    candidates = []
    for _ in range(MAX_RETRY+1):
        onset = weighted_choice(rng, vms_d['onset_ll'])
        suf = weighted_choice(rng, vms_d['suffix_global'])
        ew = make_word_sim(onset, suf, rng, vms_d['ll_nemed'], P_LL_MF)
        if len(ew) <= max_ll: return ew
        candidates.append(ew)
    return min(candidates, key=len)

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

def run_sim(latin_words, vms_d, rng, n_trials, lexicons=None):
    """Run simulation with optional vocabulary clamping."""
    suffix_global = vms_d['suffix_global']
    suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
    suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
    all_lines = []
    for _ in range(n_trials):
        w = list(latin_words); rng.shuffle(w)
        lines = []; buf = deque(maxlen=WINDOW); pos = 0
        prev_onset = None; prev_word = None
        while len(lines) < TARGET_LINES and pos < len(w)-2:
            n = max(2, min(20, round(rng.gauss(MU_LEN, SIGMA_LEN))))
            chunk = w[pos:pos+n]
            if len(chunk) < 2: pos += len(chunk); continue
            line = []; word_idx = 0
            p_blind_n = get_p_blind_n(n)
            max_ll = get_max_ll_len(n)
            beta_eff = BETA_BASE*BETA_SCALE*(n/MEAN_N)
            for i, word in enumerate(chunk):
                if i == 0:
                    if rng.random() < P_LF:
                        onset = weighted_choice(rng, vms_d['onset_lf'])
                        suf = weighted_choice(rng, suffix_lf_sup)
                        ew = make_word_sim(onset, suf, rng, vms_d['lf_nemed'], P_LF_MF)
                    else:
                        onset = weighted_choice(rng, vms_d['onset_mid'])
                        suf = weighted_choice(rng, suffix_lf_sup)
                        ew = make_word_sim(onset, suf, rng, {}, 0.0)
                elif i == len(chunk)-1:
                    if rng.random() < p_blind_n:
                        onset = weighted_choice(rng, vms_d['ll_onsets'])
                        ew = onset+'am'
                    else:
                        ew = generate_ll_word(rng, vms_d, max_ll)
                else:
                    if prev_word is not None and rng.random() < P_STUTTER:
                        ew = prev_word
                    elif buf and rng.random() < CP:
                        src = draw_buf(buf, prev_onset, rng, word_idx)
                        if src is None: src = rng.choice(list(buf))
                        if rng.random() < MP:
                            ew = timm_modify(src, vms_d['onset_mid'], suffix_mid_sup, rng)
                            # Apply lexicon clamping if provided
                            if lexicons: ew = clamp_to_lexicon(ew, lexicons, rng)
                        else:
                            ew = src
                            # Apply lexicon clamping to copies too
                            if lexicons: ew = clamp_to_lexicon(ew, lexicons, rng)
                    else:
                        new_ow = {o:v*(1+ALPHA*word_idx) if o in SHORT_ONSETS else v
                                  for o,v in vms_d['onset_mid'].items()}
                        tot = sum(new_ow.values())
                        norm = {o:v/tot for o,v in new_ow.items()} if tot else vms_d['onset_mid']
                        onset = weighted_choice(rng, norm)
                        biased_suf = apply_suffix_length_bias(suffix_mid_sup, word_idx, beta_eff)
                        suf = weighted_choice(rng, biased_suf)
                        ew = make_word_sim(onset, suf, rng, vms_d['mid_nemed'], P_MF)
                        if lexicons: ew = clamp_to_lexicon(ew, lexicons, rng)
                    buf.append(ew); word_idx += 1
                prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
            lines.append(line); pos += n
        all_lines.extend(lines[:TARGET_LINES])
    return all_lines

def compute_adjrate_decomposition(all_lines, label):
    """Compute per-onset adj_rate and vocabulary stats."""
    all_words = [w for l in all_lines for w in l]
    n_words = len(all_words)
    if n_words < 100: return None

    global_adj = sum(1 for i in range(n_words-1) if all_words[i] == all_words[i+1]) / (n_words-1)

    onset_adj = Counter(); onset_tokens = Counter()
    for i in range(n_words-1):
        w1 = all_words[i]; w2 = all_words[i+1]
        o1 = get_onset(w1); onset_tokens[o1] += 1
        if w1 == w2: onset_adj[o1] += 1

    # Per-onset vocab
    onset_vocab = {}; onset_cp90 = {}
    for onset_class in ['qok','ok','ot','qot','sh','ch','d','y','s','t']:
        wds = [w for w in all_words if get_onset(w) == onset_class]
        cnt = Counter(wds); n_types = len(cnt)
        sorted_c = sorted(cnt.values(), reverse=True)
        cumsum = 0; cp90 = 0; target = sum(sorted_c) * 0.90
        for c in sorted_c:
            cumsum += c; cp90 += 1
            if cumsum >= target: break
        onset_vocab[onset_class] = n_types
        onset_cp90[onset_class] = cp90

    # Also measure MID unique types total
    mid_words = [w for l in all_lines for w in l[1:-1] if len(l) > 2]
    mid_unique = len(set(mid_words))

    return {
        'label': label,
        'global_adj': global_adj,
        'onset_adj': dict(onset_adj),
        'onset_tokens': dict(onset_tokens),
        'onset_vocab': onset_vocab,
        'onset_cp90': onset_cp90,
        'mid_unique': mid_unique,
        'n_words': n_words,
    }

def print_comparison(results_list, vms_ref):
    """Print per-onset adj_rate comparison across conditions."""
    major_classes = ['qok','ok','ot','qot','sh','ch','d']

    print(f"\n{'='*80}")
    print(f"PER-ONSET ADJ_RATE COMPARISON")
    print(f"{'='*80}")
    print(f"{'Metric':<12}", end='')
    for r in results_list:
        print(f"  {r['label'][:15]:>15}", end='')
    print()
    print("-"*80)

    # Global adj_rate
    print(f"{'global_adj':<12}", end='')
    print(f"  {'VMS':>15}", end='')
    for r in results_list:
        print(f"  {r['global_adj']*100:>14.3f}%", end='')
    print(f"\n{'':12}  {'0.933%':>15}", end='')
    print()

    # Per-onset adj_rate
    print(f"\nPer-onset identical pair rate:")
    for onset_class in major_classes:
        vms_adj = vms_ref['onset_adj'].get(onset_class, 0) / max(1, vms_ref['onset_tokens'].get(onset_class, 1))
        print(f"  {onset_class:<10}", end='')
        print(f"  {vms_adj*100:>14.3f}%", end='')
        for r in results_list:
            tok = r['onset_tokens'].get(onset_class, 0)
            adj = r['onset_adj'].get(onset_class, 0)
            rate = adj/tok*100 if tok else 0
            ratio = (adj/tok) / vms_adj if vms_adj > 0 and tok > 0 else 0
            flag = ' ↑' if ratio > 1.5 else (' ↓' if ratio < 0.5 else '  ')
            print(f"  {rate:>13.3f}%{flag}", end='')
        print()

    # Per-onset CP90
    print(f"\nPer-onset CP90 (types covering 90% of tokens):")
    for onset_class in major_classes:
        vms_cp90 = vms_ref['onset_cp90'].get(onset_class, 0)
        print(f"  {onset_class:<10}", end='')
        print(f"  {vms_cp90:>15d}", end='')
        for r in results_list:
            cp90 = r['onset_cp90'].get(onset_class, 0)
            ratio = cp90 / vms_cp90 if vms_cp90 else 0
            flag = ' ↑' if ratio > 1.3 else (' ≈' if abs(ratio-1.0) < 0.3 else ' ↓')
            print(f"  {cp90:>13d}{flag}", end='')
        print()

    # MID unique types
    print(f"\nMID unique word types:")
    vms_mid = vms_ref['mid_unique']
    print(f"  {'mid_unique':<10}  {vms_mid:>15,}", end='')
    for r in results_list:
        ratio = r['mid_unique'] / vms_mid if vms_mid else 0
        print(f"  {r['mid_unique']:>13,}  ({ratio:.2f}×)", end='')
    print()

def main():
    print("exp_578: Q007 Copy-Buffer Amplification Diagnosis")
    print("="*70)
    print("Testing: does copy-buffer amplify adj_rate when vocabulary is clamped?")
    print("Expected pattern: VMS baseline << VMS measured << clamped simulation\n")

    print("Loading data...")
    b_lines = parse_vms_b_lines()
    print(f"B-dialect: {len(b_lines)} lines, {sum(len(l) for l in b_lines)} words")
    latin_words = load_latin(LATIN_CORPUS)
    print(f"Latin: {len(latin_words)} words")

    # Compute VMS distributions and lexicons
    vms_d = compute_vms_dists(b_lines)

    # Build VMS MID lexicons for each onset class
    mid_words = vms_d['mid_words']
    all_onset_classes = {'qok','ok','ot','qot','sh','ch','d','y','s','t','ol','l','r'}
    sparse_classes = {'qok','ok','ot','qot'}
    rich_classes = {'sh','ch','d'}

    lexicons_sparse = build_vms_lexicons(mid_words, sparse_classes)
    lexicons_all7 = build_vms_lexicons(mid_words, sparse_classes | rich_classes)
    lexicons_rich_only = build_vms_lexicons(mid_words, rich_classes)

    # VMS reference (from exp_577 analysis)
    all_vms_words = [w for l in b_lines for w in l]
    n_vms = len(all_vms_words)
    vms_onset_adj = Counter(); vms_onset_tokens = Counter()
    for i in range(n_vms-1):
        w1 = all_vms_words[i]; w2 = all_vms_words[i+1]
        o1 = get_onset(w1); vms_onset_tokens[o1] += 1
        if w1 == w2: vms_onset_adj[o1] += 1
    vms_onset_vocab = {}; vms_onset_cp90 = {}
    for oc in ['qok','ok','ot','qot','sh','ch','d','y','s','t']:
        wds = [w for w in all_vms_words if get_onset(w) == oc]
        cnt = Counter(wds)
        sorted_c = sorted(cnt.values(), reverse=True)
        cumsum = 0; cp90 = 0; target = sum(sorted_c) * 0.90
        for c in sorted_c:
            cumsum += c; cp90 += 1
            if cumsum >= target: break
        vms_onset_vocab[oc] = len(cnt); vms_onset_cp90[oc] = cp90
    vms_mid_words = [w for l in b_lines for w in l[1:-1] if len(l) > 2]
    vms_ref = {'onset_adj': dict(vms_onset_adj), 'onset_tokens': dict(vms_onset_tokens),
               'onset_vocab': vms_onset_vocab, 'onset_cp90': vms_onset_cp90,
               'mid_unique': len(set(vms_mid_words))}

    # Run four simulation conditions
    conditions = [
        ("Baseline", None),
        ("Sparse_clamp", lexicons_sparse),
        ("All7_clamp", lexicons_all7),
        ("Rich_only_clamp", lexicons_rich_only),
    ]

    all_results = []
    for condition_name, lexicons in conditions:
        print(f"\nRunning: {condition_name} (N={N_TRIALS})...")
        rng = random.Random(SEED + len(all_results) * 100)
        all_lines = run_sim(latin_words, vms_d, rng, N_TRIALS, lexicons)
        result = compute_adjrate_decomposition(all_lines, condition_name)
        if result:
            all_results.append(result)
            print(f"  Global adj_rate = {result['global_adj']*100:.3f}%")

    # Print comparison
    print_comparison(all_results, vms_ref)

    # Key diagnostic
    print(f"\n\n{'='*70}")
    print(f"KEY DIAGNOSTIC: Where does clamping increase adj_rate?")
    print(f"{'='*70}")

    if len(all_results) >= 3:
        baseline = all_results[0]
        all7 = all_results[2]
        print(f"\nGlobal adj_rate:")
        print(f"  VMS actual:           0.933%")
        print(f"  Baseline simulation:  {baseline['global_adj']*100:.3f}%")
        print(f"  All7 clamped:         {all7['global_adj']*100:.3f}%")
        print(f"\nPer-onset adj_rate change (Baseline → All7 clamp):")
        print(f"  (VMS adj_rate shown for comparison)")
        print(f"\n{'Onset':<8} {'VMS%':>7} {'Base%':>8} {'All7%':>8} {'Δ%':>7} {'Driver?'}")
        print("-"*55)
        for oc in ['qok','ok','ot','qot','sh','ch','d']:
            vms_tok = vms_onset_tokens.get(oc, 0)
            vms_adj_rate = vms_onset_adj.get(oc, 0) / vms_tok * 100 if vms_tok else 0
            b_tok = baseline['onset_tokens'].get(oc, 0)
            b_adj_rate = baseline['onset_adj'].get(oc, 0) / b_tok * 100 if b_tok else 0
            a7_tok = all7['onset_tokens'].get(oc, 0)
            a7_adj_rate = all7['onset_adj'].get(oc, 0) / a7_tok * 100 if a7_tok else 0
            delta = a7_adj_rate - b_adj_rate
            pct_total = a7_tok / len([w for l in all_lines for w in l]) * 100 if all_lines else 0
            delta_global = delta * pct_total / 100
            driver = 'MAJOR' if delta_global > 0.05 else ('minor' if delta_global > 0.01 else 'negligible')
            print(f"{oc:<8} {vms_adj_rate:>6.3f}% {b_adj_rate:>7.3f}% {a7_adj_rate:>7.3f}% {delta:>+6.3f}% {driver}")

    print(f"\nConclusion:")
    print(f"If the 'MAJOR' drivers are sh/ch/d (the clamped rich-midfix classes),")
    print(f"this confirms: vocabulary clamping of sh/ch/d specifically causes the adj_rate failure.")
    print(f"If drivers are sparse classes (qok/ok/ot/qot), the failure has a different root cause.")

if __name__ == '__main__':
    main()
