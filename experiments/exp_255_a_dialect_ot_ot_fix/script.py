"""
exp_255: H457 — Fix 'other' Onset Bug and Re-Measure A-Dialect ot→ot MID Bigram

Bug: In exp_254, 'other' (6.48% of A-dialect MID words) was used as a literal onset
string in make_word_sim, producing words beginning with 'o-t-h-e-r', which get_onset
classifies as 'ot'. Sim MID ot=10.63% vs VMS=4.44% — 2.4× inflated. ot→ot invalid.

Fix: Filter 'other' from onset_mid, onset_lf, onset_ll before passing to simulation.
Renormalize. This means 'other'-onset VMS words are excluded from the onset distribution
used by the sim — they represent ~6.5% of MID words that are unusual forms (cph, ckh,
a-starting, etc.) and cannot be faithfully reproduced by the onset+suffix template.

Also: verify sim ot rate now matches VMS (~4.44% MID).
Also: measure o→o correctly (already valid in exp_254 but confirm).
Also: add B-dialect check — does B-dialect onset_mid also have 'other' contamination?
"""

import os, re, random
from collections import Counter, deque, defaultdict

REPO_DIR     = os.path.expanduser('~/voynich-cryptanalyst')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH    = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

N_SIM = 15; WINDOW = 20; SEED = 255000

# Fixed A-dialect parameters (exp_239 + p_y_y=0.10)
P_BLIND = 0.0505; D_BOOST = 0.2430; R_LF = 0.266; R_MID = 0.87
P_STUTTER = 0.002; MU_LEN = 5.64; SIGMA_LEN = 2.5
CP = 0.55; MP = 0.90; P_QOKCH = 0.12; P_LF = 1.0; P_Y_Y = 0.10; P_CHQOK = 0.00

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
def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def filter_other(dist):
    """Remove 'other' key from onset distribution and renormalize."""
    filtered = {k: v for k, v in dist.items() if k != 'other'}
    total = sum(filtered.values())
    if total > 0:
        return {k: v/total for k, v in filtered.items()}
    return filtered

def parse_vms(target_dialect='A'):
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
    lines_out = []
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
            if words: lines_out.append(words)
    return lines_out

def analyze_bigrams(lines, label=''):
    all_words = [w for l in lines for w in l]
    mid_words = [w for l in lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words); n_mid = max(1, len(mid_words))
    oc_all = Counter(get_onset(w) for w in all_words)
    oc_mid = Counter(get_onset(w) for w in mid_words)
    tb = n - 1
    bg_global = Counter((get_onset(all_words[i]), get_onset(all_words[i+1])) for i in range(tb))
    mid_bg = Counter(); mid_bg_n = 0
    for line in lines:
        nn = len(line)
        if nn < 4: continue
        for i in range(1, nn-2):
            mid_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1; mid_bg_n += 1
    def E2_mid(x, y):
        px = oc_mid.get(x, 0) / n_mid; py = oc_mid.get(y, 0) / n_mid
        pxy = mid_bg.get((x, y), 0) / mid_bg_n if mid_bg_n > 0 else 0
        return pxy / (px * py) if px * py > 0 else float('nan')
    return {'label': label, 'n': n, 'n_mid': n_mid, 'oc_all': oc_all, 'oc_mid': oc_mid,
            'E2_mid': E2_mid, 'mid_bg': mid_bg}

SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']

def build_suffix(words):
    n = len(words); suf_ctr = Counter()
    for w in words:
        matched = False
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf): suf_ctr[suf] += 1; matched = True; break
        if not matched: suf_ctr['other'] += 1
    return {suf: cnt/n for suf, cnt in suf_ctr.items()}

def build_onset_dist(words):
    n = max(1, len(words))
    return {o: cnt/n for o, cnt in Counter(get_onset(w) for w in words).items()}

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

def cipher_ll(onset_w, suffix_g, ll_onsets, onset_ll, p_blind, rng):
    if rng.random() < p_blind:
        o = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
        return o + 'am'
    o = rng.choices(list(onset_ll.keys()), weights=list(onset_ll.values()))[0]
    s = rng.choices(list(suffix_g.keys()), weights=list(suffix_g.values()))[0]
    return make_word_sim(o, s, rng)

def cipher_lf(onset_w, suffix_lf, onset_lf, p_lf, rng):
    if rng.random() < p_lf:
        o = rng.choices(list(onset_lf.keys()), weights=list(onset_lf.values()))[0]
        s = rng.choices(list(suffix_lf.keys()), weights=list(suffix_lf.values()))[0]
        return make_word_sim(o, s, rng)
    return random_eva_word(onset_w, suffix_lf, rng)

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
        if me-ms<=1: return word[:ms]+rng.choice(EVA_CHARS)+word[ms+1:]
        pos = rng.randint(ms, me-1); return word[:pos]+word[pos+1:]

def draw_buf(buf, prev_onset, rng):
    bl = list(buf)
    if not bl: return None
    if prev_onset == 'qok' and P_QOKCH > 0 and rng.random() < P_QOKCH:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'ch' and P_CHQOK > 0 and rng.random() < P_CHQOK:
        qw = [w for w in bl if get_onset(w) == 'qok']
        if qw: return rng.choice(qw)
    if prev_onset == 'y' and P_Y_Y > 0 and rng.random() < P_Y_Y:
        yw = [w for w in bl if get_onset(w) == 'y']
        if yw: return rng.choice(yw)
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

def run_sim(latin_words, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
            ll_onsets, onset_lf, onset_ll, p_blind, target_lines, rng):
    w = list(latin_words); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=WINDOW), 0
    prev_onset = None; prev_word = None
    while len(lines) < target_lines and pos < len(w)-2:
        n_words = max(2, min(20, round(rng.gauss(MU_LEN, SIGMA_LEN))))
        chunk = w[pos:pos+n_words]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0: ew = cipher_lf(onset_mid, suffix_lf_sup, onset_lf, P_LF, rng)
            elif i == len(chunk)-1: ew = cipher_ll(onset_mid, suffix_global, ll_onsets, onset_ll, p_blind, rng)
            else:
                if prev_word is not None and P_STUTTER > 0 and rng.random() < P_STUTTER: ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf(buf, prev_onset, rng)
                    if src is None: src = random_eva_word(onset_mid, suffix_mid_sup, rng)
                    ew = timm_modify(src, onset_mid, suffix_mid_sup, rng) if rng.random() < MP else src
                else: ew = random_eva_word(onset_mid, suffix_mid_sup, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n_words
    return lines[:target_lines]

# ─── Main ──────────────────────────────────────────────────────────────────────

print("Parsing VMS A-dialect corpus...")
a_lines = parse_vms('A')
print(f"  A-dialect: {len(a_lines)} lines")

# Check 'other' onset rates BEFORE fix
all_words_a = [w for l in a_lines for w in l]
mid_words_a = [w for l in a_lines for w in l[1:-1] if len(l)>2]
other_mid_rate = Counter(get_onset(w) for w in mid_words_a).get('other', 0) / max(1, len(mid_words_a))
print(f"\n  Pre-fix: A-dialect MID 'other' onset rate = {other_mid_rate:.4f} ({other_mid_rate*100:.2f}%)")

# Check B-dialect for same issue
print("\nChecking B-dialect onset_mid for 'other' contamination...")
b_lines = parse_vms('B')
mid_words_b = [w for l in b_lines for w in l[1:-1] if len(l)>2]
other_mid_rate_b = Counter(get_onset(w) for w in mid_words_b).get('other', 0) / max(1, len(mid_words_b))
print(f"  B-dialect MID 'other' onset rate = {other_mid_rate_b:.4f} ({other_mid_rate_b*100:.2f}%)")

# Build distributions WITH 'other' filtered (the fix)
suffix_global = build_suffix(all_words_a)
onset_mid_raw = build_onset_dist(mid_words_a)
onset_mid = filter_other(onset_mid_raw)  # THE FIX
onset_lf_raw = build_onset_dist([l[0] for l in a_lines if l])
onset_lf = filter_other(onset_lf_raw)
onset_ll_raw = build_onset_dist([l[-1] for l in a_lines if len(l)>1])
onset_ll = filter_other(onset_ll_raw)
ll_onsets = build_ll_onsets(onset_ll, D_BOOST)
suffix_lf_sup = make_suppressed_suffix(suffix_global, R_LF)
suffix_mid_sup = make_suppressed_suffix(suffix_global, R_MID)
target_lines = len(a_lines)

print(f"\nPost-fix onset_mid['ot'] = {onset_mid.get('ot', 0):.4f} (VMS MID ot = {Counter(get_onset(w) for w in mid_words_a).get('ot',0)/len(mid_words_a):.4f})")
print(f"Post-fix onset_mid['o']  = {onset_mid.get('o', 0):.4f}")
print(f"Post-fix onset_mid sum   = {sum(onset_mid.values()):.4f}")

# VMS bigram analysis
vms_analysis = analyze_bigrams(a_lines, 'VMS_A')

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)

print(f"\nRunning {N_SIM} simulations (with 'other' onset fix)...")
sim_all_lines = []
for trial in range(N_SIM):
    rng = random.Random(SEED + trial*100)
    lines = run_sim(latin, onset_mid, suffix_global, suffix_lf_sup, suffix_mid_sup,
                    ll_onsets, onset_lf, onset_ll, P_BLIND, target_lines, rng)
    sim_all_lines.extend(lines)
    if (trial+1) % 5 == 0: print(f"  Trial {trial+1}/{N_SIM} done")

sim_analysis = analyze_bigrams(sim_all_lines, 'Sim_A_fixed')

# ─── Print comparison ──────────────────────────────────────────────────────────

print(f"\n{'='*75}")
print(f"A-DIALECT MID BIGRAMS COMPARISON (WITH 'OTHER' ONSET FIX)")
print(f"{'='*75}")
print(f"\n  {'Pair':<12}  {'VMS_mid':>10}  {'Sim_mid':>10}  {'Delta':>8}  {'N_vms':>7}  {'N_sim':>7}")
print(f"  {'-'*12}  {'-'*10}  {'-'*10}  {'-'*8}  {'-'*7}  {'-'*7}")

KEY_PAIRS = [
    ('ot', 'ot'), ('o', 'o'), ('qok', 'qok'), ('y', 'y'),
    ('ok', 'ok'), ('d', 'd'), ('sh', 'qok'), ('qok', 'ch'),
    ('ol', 'ol'), ('ch', 'qok'), ('qot', 'qot'),
]

for (x, y) in KEY_PAIRS:
    vm_ = vms_analysis['E2_mid'](x, y)
    sm_ = sim_analysis['E2_mid'](x, y)
    nvm = vms_analysis['mid_bg'].get((x, y), 0)
    nsm = sim_analysis['mid_bg'].get((x, y), 0)
    def fmt(v): return f"{v:8.3f}" if v == v else "     nan"
    delta_str = ''
    if vm_ == vm_ and sm_ == sm_:
        delta = sm_ - vm_
        delta_str = f"{delta:+8.3f}"
        flag = ''
        if abs(delta) > 0.3: flag = f" ({'SIM>VMS' if delta>0 else 'SIM<VMS'})"
        print(f"  {x}→{y:<9}  {fmt(vm_)}  {fmt(sm_)}  {delta_str}  {nvm:>7}  {nsm:>7}{flag}")
    else:
        print(f"  {x}→{y:<9}  {fmt(vm_)}  {fmt(sm_)}     ---  {nvm:>7}  {nsm:>7}")

# ─── Onset rates ───────────────────────────────────────────────────────────────

print(f"\n{'='*75}")
print(f"ONSET RATE VERIFICATION (MID)")
print(f"{'='*75}")
print(f"\n  {'Onset':<8}  {'VMS_mid':>10}  {'Sim_mid':>10}  {'Match?':>8}")
for onset in ['qok','ch','sh','ot','y','d','ok','o','qot','ol']:
    vm_ = vms_analysis['oc_mid'].get(onset,0) / vms_analysis['n_mid']
    sm_ = sim_analysis['oc_mid'].get(onset,0) / sim_analysis['n_mid']
    ratio = sm_/vm_ if vm_ > 0 else float('inf')
    ok_flag = 'OK' if 0.85 <= ratio <= 1.15 else f'OFF {ratio:.2f}x'
    print(f"  {onset:<8}  {vm_:>10.4f}  {sm_:>10.4f}  {ok_flag:>8}")

print(f"\nDone.")
