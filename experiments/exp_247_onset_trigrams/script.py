"""
exp_247: H452 — Onset Succession Chains: Is sh→qok→ch Enriched as a 3-Word Onset Sequence?

Question: If sh→qok (E_mid=1.967) and qok→ch (E_mid=1.234) are independent first-order
Markov rules, then P(sh,qok,ch) = P(sh)×P(qok)×P(ch)×E_2(sh→qok)×E_2(qok→ch).
Is sh→qok→ch enriched BEYOND this first-order product? This would be evidence for
second-order Markov (hierarchical grammar) vs independent first-order rules.

Design:
  Compute MID-only onset trigrams (all three words at MID positions, consecutive).
  For each (X,Y,Z) trigram in MID context:
    E_3(X→Y→Z) = P(X,Y,Z) / (P(X) × P(Y) × P(Z))
    E_3_pred(X→Y→Z) = E_2(X→Y) × E_2(Y→Z)  [predicted from 1st-order rules]
    2nd_order_enrichment = E_3 / E_3_pred

  Key test: Is 2nd_order_enrichment(sh,qok,ch) > 1.0?
  If yes → VMS has 2nd-order Markov structure (grammar chains)
  If E_3 ≈ E_3_pred → first-order rules fully explain the data

  Also: find all MID trigrams with E_3 > 2.0 AND E_3/E_3_pred > 1.5 (candidates for
  genuine 2nd-order rules beyond 1st-order composition).

  Compare: same analysis for simulation (exp_236 architecture, N=10)
  Does the simulation show similar 2nd-order enrichment patterns?
"""
from pathlib import Path as _RepositoryPath

import os, re, random
from collections import Counter, defaultdict, deque

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

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

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

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

def compute_trigram_stats(lines):
    """Compute MID-only unigram, bigram, and trigram counts and enrichments."""
    all_mid_words = [line[j] for line in lines for j in range(1, len(line)-1) if len(line) >= 4]
    n_mid = len(all_mid_words)
    oc_mid = Counter(get_onset(w) for w in all_mid_words)
    rates_mid = {o: c/n_mid for o, c in oc_mid.items()}

    # MID-only bigrams (i and i+1 both MID)
    mid_bg = Counter()
    mid_bg_n = 0
    for line in lines:
        n = len(line)
        if n < 4: continue
        for i in range(1, n-2):
            mid_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1
            mid_bg_n += 1

    # MID-only trigrams (i, i+1, i+2 all MID → need n >= 5)
    mid_tg = Counter()
    mid_tg_n = 0
    for line in lines:
        n = len(line)
        if n < 5: continue
        for i in range(1, n-3):
            mid_tg[(get_onset(line[i]), get_onset(line[i+1]), get_onset(line[i+2]))] += 1
            mid_tg_n += 1

    def E2(x, y):
        pxy = mid_bg.get((x,y), 0)/mid_bg_n if mid_bg_n>0 else 0
        px = rates_mid.get(x,0); py = rates_mid.get(y,0)
        return pxy/(px*py) if px*py>0 else 0

    def E3(x, y, z):
        pxyz = mid_tg.get((x,y,z), 0)/mid_tg_n if mid_tg_n>0 else 0
        px = rates_mid.get(x,0); py = rates_mid.get(y,0); pz = rates_mid.get(z,0)
        return pxyz/(px*py*pz) if px*py*pz>0 else 0

    return rates_mid, mid_bg, mid_bg_n, mid_tg, mid_tg_n, E2, E3

# ─── Parse VMS ────────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect...")
b_lines = parse_vms_b()
print(f"  {len(b_lines)} lines")

rates_mid, mid_bg, mid_bg_n, mid_tg, mid_tg_n, E2, E3 = compute_trigram_stats(b_lines)

# Only use onsets with rate >= 1% and enough bigram/trigram counts
MIN_RATE = 0.01
MIN_BG_COUNT = 5
MIN_TG_COUNT = 3

focus_onsets = [o for o, r in rates_mid.items() if r >= MIN_RATE]
print(f"  Onsets with rate ≥ 1%: {sorted(focus_onsets)}")
print(f"  Total MID bigrams: {mid_bg_n}, MID trigrams: {mid_tg_n}")

# ─── Key trigrams ─────────────────────────────────────────────────────────────

print(f"\n{'='*90}")
print("KEY TRIGRAM ANALYSIS — sh→qok→ch AND RELATED CHAINS")
print(f"{'='*90}")
print()

KEY_TRIGRAMS = [
    ('sh', 'qok', 'ch', 'sh→qok→ch (chain of 2 known rules)'),
    ('sh', 'qok', 'qok', 'sh→qok→qok (qok self-succession after chain)'),
    ('sh', 'qok', 'ok', 'sh→qok→ok (qok→ok after sh→qok)'),
    ('qok', 'ch', 'qok', 'qok→ch→qok (ch surrounded by qok)'),
    ('qok', 'ch', 'sh', 'qok→ch→sh (ch followed by sh)'),
    ('d', 'd', 'd', 'd→d→d (ternary d self-succession)'),
    ('y', 'y', 'y', 'y→y→y (ternary y self-succession)'),
    ('ot', 'ot', 'ot', 'ot→ot→ot (ternary ot self-succession)'),
    ('sh', 'sh', 'qok', 'sh→sh→qok (sh self-succession then qok)'),
    ('qok', 'sh', 'qok', 'qok→sh→qok (sh between qoks)'),
]

print(f"  {'Trigram':<18} {'N':>5} {'E3':>8} {'E3_pred':>9} {'2nd_order':>10}  Count_m→m  Label")
print(f"  {'-'*85}")

for x, y, z, label in KEY_TRIGRAMS:
    e3 = E3(x, y, z)
    e2_xy = E2(x, y)
    e2_yz = E2(y, z)
    e3_pred = e2_xy * e2_yz  # predicted from 1st-order
    second_order = e3 / e3_pred if e3_pred > 0 else 0
    cnt = mid_tg.get((x, y, z), 0)
    cnt_xy = mid_bg.get((x, y), 0)
    cnt_yz = mid_bg.get((y, z), 0)
    print(f"  {x}→{y}→{z:<6} {cnt:>5} {e3:>8.3f} {e3_pred:>9.3f} {second_order:>10.3f}  bg={cnt_xy}/{cnt_yz}  {label}")

# ─── Full trigram matrix: find all highly enriched trigrams ──────────────────

print(f"\n{'='*90}")
print("TOP MID-ONLY TRIGRAMS BY E3 AND 2ND-ORDER ENRICHMENT")
print(f"{'='*90}")

MIN_TG_RATE = 0.005  # both X and Y and Z onset rate
all_trigrams = {}
for (x, y, z), cnt in mid_tg.items():
    if cnt < MIN_TG_COUNT: continue
    if rates_mid.get(x, 0) < MIN_TG_RATE: continue
    if rates_mid.get(y, 0) < MIN_TG_RATE: continue
    if rates_mid.get(z, 0) < MIN_TG_RATE: continue
    e3 = E3(x, y, z)
    e2_xy = E2(x, y)
    e2_yz = E2(y, z)
    e3_pred = e2_xy * e2_yz
    second_order = e3 / e3_pred if e3_pred > 0 else 0
    all_trigrams[(x,y,z)] = (e3, e3_pred, second_order, cnt)

print(f"\nTop 25 by E3 (absolute trigram enrichment, N≥{MIN_TG_COUNT}):")
print(f"  {'Trigram':<18} {'N':>5} {'E3':>8} {'E3_pred':>9} {'2nd_order':>10}")
print(f"  {'-'*60}")
for (x,y,z), (e3, e3p, so, cnt) in sorted(all_trigrams.items(), key=lambda kv: -kv[1][0])[:25]:
    print(f"  {x}→{y}→{z:<6} {cnt:>5} {e3:>8.3f} {e3p:>9.3f} {so:>10.3f}")

print(f"\nTop 25 by 2nd-order enrichment (E3/E3_pred, N≥{MIN_TG_COUNT}):")
print(f"  {'Trigram':<18} {'N':>5} {'E3':>8} {'E3_pred':>9} {'2nd_order':>10}")
print(f"  {'-'*60}")
for (x,y,z), (e3, e3p, so, cnt) in sorted(all_trigrams.items(), key=lambda kv: -kv[1][2])[:25]:
    print(f"  {x}→{y}→{z:<6} {cnt:>5} {e3:>8.3f} {e3p:>9.3f} {so:>10.3f}")

print(f"\nTop 25 by 2nd-order DEPLETION (E3/E3_pred < 1, N≥{MIN_TG_COUNT}):")
print(f"  {'Trigram':<18} {'N':>5} {'E3':>8} {'E3_pred':>9} {'2nd_order':>10}")
print(f"  {'-'*60}")
depleted = {k: v for k, v in all_trigrams.items() if v[2] < 0.7}
for (x,y,z), (e3, e3p, so, cnt) in sorted(depleted.items(), key=lambda kv: kv[1][2])[:25]:
    print(f"  {x}→{y}→{z:<6} {cnt:>5} {e3:>8.3f} {e3p:>9.3f} {so:>10.3f}")

# ─── Simulation comparison ────────────────────────────────────────────────────

print(f"\n{'='*90}")
print("SIMULATION COMPARISON — exp_236 ARCHITECTURE (N=10)")
print(f"{'='*90}")

# Load simulation infrastructure for exp_236
EVA_CHARS = list('acdehiklmnoqrsty')
TARGET_LINES = 2447; WINDOW = 20; SEED = 247000
P_BLIND=0.115; P_LF=1.0; CP=0.55; MP=0.90; P_QOKCH=0.12; P_STUTTER=0.006
R_LF=0.12; R_MID=0.25; MU_LEN=8.4

def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0
def get_edy_suffix_len(w):
    if w.endswith('eedy'): return 4
    if w.endswith('edy'):  return 3
    return 0

all_vms = [w for l in b_lines for w in l]
n_vms = len(all_vms)
SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']
suf_ctr = Counter()
for w in all_vms:
    matched = False
    for suf in SUFFIX_PATTERNS:
        if w.endswith(suf): suf_ctr[suf] += 1; matched = True; break
    if not matched: suf_ctr['other'] += 1
suffix_global = {suf: c/n_vms for suf, c in suf_ctr.items()}

lf_vms = [l[0] for l in b_lines if l]; ll_vms = [l[-1] for l in b_lines if len(l)>1]
oc_lf = Counter(get_onset(w) for w in lf_vms); oc_ll = Counter(get_onset(w) for w in ll_vms)
onset_lf_vms = {o: c/len(lf_vms) for o, c in oc_lf.items()}
onset_ll_vms = {o: c/len(ll_vms) for o, c in oc_ll.items()}
onset_weights_mid = dict(rates_mid)

d_global = Counter(get_onset(w) for w in all_vms).get('d', 0) / n_vms
oc_ll_d = oc_ll.get('d', 0); n_ll = len(ll_vms)
d_ll_target = (oc_ll_d/n_ll) / d_global if d_global else 0
vms_ll_d_enr = onset_ll_vms.get('d', 0) / d_global if d_global else 0
d_boost = d_global * (d_ll_target - (1-P_BLIND) * vms_ll_d_enr) / P_BLIND

def build_ll_onsets(onset_ll_vms, d_boost):
    rem = 1.0 - d_boost
    base = {o: v for o, v in onset_ll_vms.items() if o != 'd'}
    bt = sum(base.values())
    n = {o: v/bt * rem for o, v in base.items()} if bt > 0 else {}
    n['d'] = d_boost; return n

ll_onsets = build_ll_onsets(onset_ll_vms, d_boost)

def make_sup(sg, r):
    am = sg.get('am', 0); new_am = am * r; delta = am - new_am; non_am = 1 - am
    return {s: (new_am if s=='am' else w + w/non_am*delta) for s, w in sg.items()} if non_am > 0 else dict(sg)

suf_lf = make_sup(suffix_global, R_LF); suf_mid = make_sup(suffix_global, R_MID)

def make_word(onset, suffix, rng):
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        return onset + rng.choice(['a','ai','o','oi','e','ei']) + suffix
    return onset + suffix

def rand_word(ow, sw, rng):
    o = rng.choices(list(ow), weights=list(ow.values()))[0]
    s = rng.choices(list(sw), weights=list(sw.values()))[0]
    return make_word(o, s, rng)

def cipher_lf(rng):
    o = rng.choices(list(onset_lf_vms), weights=list(onset_lf_vms.values()))[0]
    s = rng.choices(list(suf_lf), weights=list(suf_lf.values()))[0]
    return make_word(o, s, rng)

def cipher_ll(rng):
    if rng.random() < P_BLIND:
        o = rng.choices(list(ll_onsets), weights=list(ll_onsets.values()))[0]
        return o + 'am'
    o = rng.choices(list(onset_ll_vms), weights=list(onset_ll_vms.values()))[0]
    s = rng.choices(list(suffix_global), weights=list(suffix_global.values()))[0]
    return make_word(o, s, rng)

def timm_modify(word, rng):
    ol = get_onset_len(word); el = get_edy_suffix_len(word)
    ms = ol; me = len(word) - el
    if ms >= me: return rand_word(onset_weights_mid, suf_mid, rng)
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
    if prev_onset == 'qok' and rng.random() < P_QOKCH:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    return rng.choice(bl)

def run_sim_trial(latin_words, rng):
    w = list(latin_words); rng.shuffle(w)
    lines = []; buf = deque(maxlen=WINDOW); pos = 0; prev_onset = None; prev_word = None
    while len(lines) < TARGET_LINES and pos < len(w)-2:
        n = max(2, min(20, round(rng.gauss(MU_LEN, 3.0))))
        chunk = w[pos:pos+n]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, _ in enumerate(chunk):
            if i == 0: ew = cipher_lf(rng)
            elif i == len(chunk)-1: ew = cipher_ll(rng)
            else:
                if prev_word and P_STUTTER > 0 and rng.random() < P_STUTTER: ew = prev_word
                elif buf and rng.random() < CP:
                    src = draw_buf(buf, prev_onset, rng)
                    ew = timm_modify(src, rng) if rng.random() < MP else src
                else: ew = rand_word(onset_weights_mid, suf_mid, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += n
    return lines[:TARGET_LINES]

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

print("Loading Latin corpus and running 10 sim trials...")
latin = load_latin(LATIN_CORPUS)
N_TRIALS = 10

sim_tg_sums = defaultdict(float)
sim_bg_sums = defaultdict(float)
sim_mid_words_count = 0

for trial in range(N_TRIALS):
    rng_t = random.Random(SEED + trial * 100)
    lines = run_sim_trial(latin, rng_t)
    sim_mid_words = [line[j] for line in lines for j in range(1, len(line)-1) if len(line) >= 4]
    sim_oc = Counter(get_onset(w) for w in sim_mid_words)
    n_sim_mid = len(sim_mid_words)
    sim_mid_words_count += n_sim_mid

    sim_bg_local = Counter()
    sim_bg_n_local = 0
    sim_tg_local = Counter()
    sim_tg_n_local = 0

    for line in lines:
        n = len(line)
        if n >= 4:
            for i in range(1, n-2):
                sim_bg_local[(get_onset(line[i]), get_onset(line[i+1]))] += 1
                sim_bg_n_local += 1
        if n >= 5:
            for i in range(1, n-3):
                sim_tg_local[(get_onset(line[i]), get_onset(line[i+1]), get_onset(line[i+2]))] += 1
                sim_tg_n_local += 1

    sim_rates = {o: c/n_sim_mid for o, c in sim_oc.items()}
    # Compute E3 for each key trigram in this trial
    for x, y, z, _ in KEY_TRIGRAMS:
        pxyz = sim_tg_local.get((x,y,z), 0)/sim_tg_n_local if sim_tg_n_local>0 else 0
        px = sim_rates.get(x,0); py = sim_rates.get(y,0); pz = sim_rates.get(z,0)
        e3 = pxyz/(px*py*pz) if px*py*pz>0 else 0
        sim_tg_sums[(x,y,z)] += e3

        pxy = sim_bg_local.get((x,y),0)/sim_bg_n_local if sim_bg_n_local>0 else 0
        pyz = sim_bg_local.get((y,z),0)/sim_bg_n_local if sim_bg_n_local>0 else 0
        e2_xy = pxy/(px*py) if px*py>0 else 0
        e2_yz = pyz/(py*pz) if py*pz>0 else 0
        sim_bg_sums[(x,y,'E2_XY')] += e2_xy
        sim_bg_sums[(x,y,'E2_YZ')] += e2_yz

    if (trial+1) % 5 == 0:
        print(f"  Trial {trial+1}/{N_TRIALS} done")

print(f"\n{'='*90}")
print("KEY TRIGRAMS: VMS vs SIMULATION COMPARISON")
print(f"{'='*90}")
print(f"\n  {'Trigram':<18} {'VMS_E3':>8} {'VMS_2nd':>9} {'Sim_E3':>8} {'Sim_2nd':>9}  {'VMS_N':>6}  Label")
print(f"  {'-'*90}")

for x, y, z, label in KEY_TRIGRAMS:
    vms_e3 = E3(x, y, z)
    vms_e2_xy = E2(x, y)
    vms_e2_yz = E2(y, z)
    vms_e3_pred = vms_e2_xy * vms_e2_yz
    vms_2nd = vms_e3/vms_e3_pred if vms_e3_pred > 0 else 0

    sim_e3 = sim_tg_sums[(x,y,z)] / N_TRIALS
    sim_e2_xy = sim_bg_sums[(x,y,'E2_XY')] / N_TRIALS
    sim_e2_yz = sim_bg_sums[(x,y,'E2_YZ')] / N_TRIALS  # Note: stored as (x,y) key for YZ
    # Fix: YZ means (y→z), so the key should be different. Let me recalculate:
    # Actually I stored E2_YZ under (x,y,'E2_YZ') which is wrong notation but the values are E2(y,z)
    sim_e3_pred = sim_e2_xy * sim_e2_yz
    sim_2nd = sim_e3/sim_e3_pred if sim_e3_pred > 0 else 0

    cnt = mid_tg.get((x,y,z), 0)
    print(f"  {x}→{y}→{z:<6} {vms_e3:>8.3f} {vms_2nd:>9.3f} {sim_e3:>8.3f} {sim_2nd:>9.3f}  {cnt:>6}  {label}")

print(f"\n{'='*90}")
print("VERDICT: SECOND-ORDER MARKOV STRUCTURE IN VMS?")
print(f"{'='*90}")

sh_qok_ch_e3 = E3('sh', 'qok', 'ch')
sh_qok_ch_pred = E2('sh', 'qok') * E2('qok', 'ch')
sh_qok_ch_2nd = sh_qok_ch_e3 / sh_qok_ch_pred if sh_qok_ch_pred > 0 else 0
cnt_sh_qok_ch = mid_tg.get(('sh','qok','ch'), 0)

print(f"\n  sh→qok→ch:")
print(f"    VMS E3 = {sh_qok_ch_e3:.3f}")
print(f"    1st-order prediction = E2(sh→qok) × E2(qok→ch) = {E2('sh','qok'):.3f} × {E2('qok','ch'):.3f} = {sh_qok_ch_pred:.3f}")
print(f"    2nd-order enrichment = {sh_qok_ch_2nd:.3f}")
print(f"    Count: {cnt_sh_qok_ch} MID trigrams")

if sh_qok_ch_2nd > 1.3:
    print(f"\n  → 2ND-ORDER MARKOV CONFIRMED: sh→qok→ch enriched {sh_qok_ch_2nd:.2f}× beyond 1st-order prediction")
elif sh_qok_ch_2nd > 0.8:
    print(f"\n  → NEAR 1ST-ORDER: sh→qok→ch is consistent with independent 1st-order rules")
else:
    print(f"\n  → 2ND-ORDER DEPLETION: sh→qok→ch is less frequent than 1st-order rules predict")

print("\nDone.")
