"""
exp_241: H442 — Onset Bigram Structure: Completeness Analysis

Question: Are qok→ch (B, p_qokch=0.12) and y→y (A, p_y_y=0.10) the only
onset-succession bigram pairs with significant enrichment in VMS? Or does
the current architecture miss additional succession rules?

Design:
  (1) Compute full onset-onset bigram enrichment matrix for A and B dialects.
      Enrichment: E(X→Y) = P(X,Y) / (P(X) × P(Y)) — deviation from independence.
      Filter: pairs where P(X) > 1%, P(Y) > 1%, and abs(E-1) > 0.20 (±20% deviation).
  (2) For each significantly elevated pair: is it captured by the current model?
      Run exp_239/236 architecture, measure same bigram enrichments in simulation.
  (3) Classify: CAPTURED (sim within ±20% of VMS), MISSED (sim outside ±20%),
      OVERCAPTURED (sim exceeds VMS by >20%).
  (4) Assess: does the model need additional Markov rules beyond qok→ch and y→y?

The ss_mean metric (qok+ok+ch self-succession average) and ss_d, ss_y are already
in the 19-metric battery. This experiment maps the full bigram space to verify
no elevated pairs are systematically missed.

Expected: The copy buffer naturally generates moderate self-succession via word
propagation; qok→ch and y→y are the only pairs that need explicit Markov rules;
all other elevated pairs are either already within ±20% of VMS or are minor cross-onset
effects within the buffer's natural dynamics.
"""

import os, re, random
from collections import Counter, defaultdict
from itertools import product

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')

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

def compute_bigram_enrichments(dialect_lines, min_rate=0.01, enrichment_threshold=0.20):
    """Compute onset bigram enrichment matrix, returning significant pairs."""
    all_words = [w for l in dialect_lines for w in l]
    n = len(all_words)
    tb = n - 1

    oc = Counter(get_onset(w) for w in all_words)
    bg = Counter((get_onset(all_words[i]), get_onset(all_words[i+1])) for i in range(tb))

    rates = {o: cnt/n for o, cnt in oc.items()}
    significant = {o for o, r in rates.items() if r >= min_rate}

    enrichments = {}
    for x in significant:
        for y in significant:
            px = rates[x]; py = rates[y]
            pxy = bg.get((x,y), 0) / tb
            e = pxy / (px * py) if px * py > 0 else 1.0
            enrichments[(x, y)] = {'e': e, 'px': px, 'py': py, 'pxy': pxy,
                                    'count': bg.get((x,y), 0)}

    return enrichments, rates

def print_bigram_matrix(name, enrichments, rates, threshold=0.20):
    """Print significantly elevated/depleted onset bigram pairs."""
    print(f"\n{name} — significant bigram pairs (|E - 1| > {threshold*100:.0f}%):")
    print(f"  {'X→Y':<14} {'E(X→Y)':>9} {'%dev':>7} {'P(X)':>7} {'P(Y)':>7} {'count':>6}  dir")
    print(f"  {'-'*65}")

    sig_pairs = [(k, v) for k, v in enrichments.items()
                 if abs(v['e'] - 1) > threshold]
    sig_pairs.sort(key=lambda x: abs(x[1]['e'] - 1), reverse=True)

    self_pairs = [(k, v) for k, v in sig_pairs if k[0] == k[1]]
    cross_pairs = [(k, v) for k, v in sig_pairs if k[0] != k[1]]

    print(f"\n  [SELF-SUCCESSION PAIRS]")
    for (x, y), v in self_pairs:
        dev = (v['e'] - 1) * 100
        direction = 'ENRICH' if v['e'] > 1 else 'DEPLETE'
        print(f"  {x}→{y:<10} {v['e']:>9.3f} {dev:>+6.1f}% {v['px']*100:>6.1f}% {v['py']*100:>6.1f}% {v['count']:>6}  {direction}")

    print(f"\n  [CROSS-ONSET PAIRS — top 20]")
    for (x, y), v in cross_pairs[:20]:
        dev = (v['e'] - 1) * 100
        direction = 'ENRICH' if v['e'] > 1 else 'DEPLETE'
        print(f"  {x}→{y:<10} {v['e']:>9.3f} {dev:>+6.1f}% {v['px']*100:>6.1f}% {v['py']*100:>6.1f}% {v['count']:>6}  {direction}")

    return self_pairs, cross_pairs

# ─── Simulation for bigram comparison ─────────────────────────────────────────

from collections import deque

# Exp_236 B-dialect params
B_PARAMS = dict(
    p_blind=0.115, d_boost=0.0913, r_lf=0.12, r_mid=0.25,
    p_stutter=0.006, mu_len=8.4, p_y_y=0.00, p_qokch=0.12,
    cp=0.55, mp=0.90, p_lf=1.0
)
# Exp_239 A-dialect params
A_PARAMS = dict(
    p_blind=0.0505, d_boost=0.2430, r_lf=0.266, r_mid=0.87,
    p_stutter=0.002, mu_len=5.64, p_y_y=0.10, p_qokch=0.12,
    cp=0.55, mp=0.90, p_lf=1.0
)

EVA_CHARS = list('acdehiklmnoqrsty')

def get_onset_len(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return len(prefix)
    return 0

def get_edy_suffix_len(w):
    if w.endswith('eedy'): return 4
    if w.endswith('edy'):  return 3
    return 0

def make_word_sim(onset, suffix, rng):
    if suffix.endswith('edy') or suffix.endswith('eedy'):
        connector = rng.choice(['a', 'ai', 'o', 'oi', 'e', 'ei'])
        return onset + connector + suffix
    return onset + suffix

def make_suppressed_suffix(sg, r_am):
    am_w = sg.get('am', 0.0)
    new_am = am_w * r_am
    delta = am_w - new_am
    non_am_total = 1.0 - am_w
    s = {}
    for k, w in sg.items():
        if k == 'am': s[k] = new_am
        else: s[k] = w + (w / non_am_total) * delta if non_am_total > 0 else w
    return s

def build_ll_onsets(onset_ll, d_boost):
    rem = 1.0 - d_boost
    base = {o: v for o, v in onset_ll.items() if o != 'd'}
    bt = sum(base.values())
    norm = {o: v/bt * rem for o, v in base.items()} if bt > 0 else {}
    norm['d'] = d_boost
    return norm

def random_eva_word(ow, sw, rng):
    o = rng.choices(list(ow.keys()), weights=list(ow.values()))[0]
    s = rng.choices(list(sw.keys()), weights=list(sw.values()))[0]
    return make_word_sim(o, s, rng)

def timm_modify(word, ow, sm, rng):
    if not word: return word
    ol = get_onset_len(word); el = get_edy_suffix_len(word)
    ms = ol; me = len(word) - el
    if ms >= me: return random_eva_word(ow, sm, rng)
    op = rng.choice(['replace', 'insert', 'delete'])
    if op == 'replace':
        pos = rng.randint(ms, me - 1)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos+1:]
    elif op == 'insert':
        pos = rng.randint(ms, me)
        return word[:pos] + rng.choice(EVA_CHARS) + word[pos:]
    else:
        if me - ms <= 1: return word[:ms] + rng.choice(EVA_CHARS) + word[ms+1:]
        pos = rng.randint(ms, me - 1)
        return word[:pos] + word[pos+1:]

def draw_buf(buf, prev_onset, p_qokch, p_y_y, rng):
    bl = list(buf)
    if prev_onset == 'qok' and p_qokch > 0 and rng.random() < p_qokch:
        cw = [w for w in bl if get_onset(w) == 'ch']
        if cw: return rng.choice(cw)
    if prev_onset == 'y' and p_y_y > 0 and rng.random() < p_y_y:
        yw = [w for w in bl if get_onset(w) == 'y']
        if yw: return rng.choice(yw)
    return rng.choice(bl)

def run_sim(latin, onset_mid, suffix_global, suffix_lf, suffix_mid,
            ll_onsets, onset_lf, onset_ll, params, target_lines, rng):
    p = params
    w = list(latin); rng.shuffle(w)
    lines, buf, pos = [], deque(maxlen=20), 0
    prev_onset = None; prev_word = None
    while len(lines) < target_lines and pos < len(w) - 2:
        nw = max(2, min(20, round(rng.gauss(p['mu_len'], 2.5))))
        chunk = w[pos:pos+nw]
        if len(chunk) < 2: pos += len(chunk); continue
        line = []
        for i, word in enumerate(chunk):
            if i == 0:
                if rng.random() < p['p_lf']:
                    o = rng.choices(list(onset_lf.keys()), weights=list(onset_lf.values()))[0]
                    s = rng.choices(list(suffix_lf.keys()), weights=list(suffix_lf.values()))[0]
                    ew = make_word_sim(o, s, rng)
                else:
                    ew = random_eva_word(onset_mid, suffix_lf, rng)
            elif i == len(chunk) - 1:
                if rng.random() < p['p_blind']:
                    o = rng.choices(list(ll_onsets.keys()), weights=list(ll_onsets.values()))[0]
                    ew = o + 'am'
                else:
                    o = rng.choices(list(onset_ll.keys()), weights=list(onset_ll.values()))[0]
                    s = rng.choices(list(suffix_global.keys()), weights=list(suffix_global.values()))[0]
                    ew = make_word_sim(o, s, rng)
            else:
                if prev_word is not None and p['p_stutter'] > 0 and rng.random() < p['p_stutter']:
                    ew = prev_word
                elif buf and rng.random() < p['cp']:
                    src = draw_buf(buf, prev_onset, p['p_qokch'], p['p_y_y'], rng)
                    if rng.random() < p['mp']:
                        ew = timm_modify(src, onset_mid, suffix_mid, rng)
                    else:
                        ew = src
                else:
                    ew = random_eva_word(onset_mid, suffix_mid, rng)
                buf.append(ew)
            prev_onset = get_onset(ew); prev_word = ew; line.append(ew)
        lines.append(line); pos += nw
    return lines[:target_lines]

def compute_bigrams_from_lines(lines, min_rate=0.01):
    aw = [w for l in lines for w in l]; n = len(aw); tb = n - 1
    oc = Counter(get_onset(w) for w in aw)
    bg = Counter((get_onset(aw[i]), get_onset(aw[i+1])) for i in range(tb))
    rates = {o: cnt/n for o, cnt in oc.items()}
    sig = {o for o, r in rates.items() if r >= min_rate}
    enr = {}
    for x in sig:
        for y in sig:
            px = rates[x]; py = rates[y]; pxy = bg.get((x,y),0)/tb
            enr[(x,y)] = pxy/(px*py) if px*py > 0 else 1.0
    return enr, rates

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

def compute_vms_distr(lines, SUFFIX_PATTERNS=None):
    if SUFFIX_PATTERNS is None:
        SUFFIX_PATTERNS = ['eedy','edy','aiin','ain','am','ey','ol','or','al','ar','dy']
    aw = [w for l in lines for w in l]; n = len(aw)
    n_mid = max(1, sum(len(l)-2 for l in lines if len(l)>2))
    oc_all = Counter(get_onset(w) for w in aw)
    oc_lf  = Counter(get_onset(l[0]) for l in lines if l)
    oc_ll  = Counter(get_onset(l[-1]) for l in lines if len(l)>1)
    suf_ctr = Counter()
    for w in aw:
        for suf in SUFFIX_PATTERNS:
            if w.endswith(suf): suf_ctr[suf] += 1; break
        else: suf_ctr['other'] += 1
    return {
        'onset_global': {o: c/n for o,c in oc_all.items()},
        'onset_lf':  {o: c/sum(oc_lf.values()) for o,c in oc_lf.items()},
        'onset_ll':  {o: c/sum(oc_ll.values()) for o,c in oc_ll.items()},
        'onset_mid': {},  # not needed here
        'suffix_global': {s: c/n for s,c in suf_ctr.items()},
        'n_lines': len(lines),
    }

# ─── Main analysis ─────────────────────────────────────────────────────────────

print("Parsing VMS corpora...")
lines_by_dialect = parse_vms_both_dialects()
print(f"  B-dialect: {len(lines_by_dialect['B'])} lines")
print(f"  A-dialect: {len(lines_by_dialect['A'])} lines")

print("\n" + "="*80)
print("PART 1: VMS ONSET BIGRAM ENRICHMENT MATRIX")
print("="*80)

# Compute for both dialects
enr_B, rates_B = compute_bigram_enrichments(lines_by_dialect['B'])
enr_A, rates_A = compute_bigram_enrichments(lines_by_dialect['A'])

self_B, cross_B = print_bigram_matrix("B-DIALECT VMS", enr_B, rates_B, threshold=0.20)
self_A, cross_A = print_bigram_matrix("A-DIALECT VMS", enr_A, rates_A, threshold=0.20)

print("\n" + "="*80)
print("PART 2: KNOWN MARKOV RULES VS VMS")
print("="*80)
print("\nChecking known Markov rule enrichments in VMS:")
for pair_label, pair, dialect, enr in [
    ("qok→ch (B)", ('qok','ch'), 'B', enr_B),
    ("y→y (A)", ('y','y'), 'A', enr_A),
]:
    v = enr.get(pair, {'e': 0, 'count': 0})
    print(f"  {pair_label}: VMS E={v['e']:.3f} ({(v['e']-1)*100:+.1f}%, count={v['count']})")

# ─── Part 3: Run simulations and compare bigrams ───────────────────────────────

print("\n" + "="*80)
print("PART 3: SIMULATION BIGRAM ENRICHMENTS (N=10 each)")
print("="*80)

N_SIM = 10
SEED  = 241000

print("\nLoading Latin corpus...")
latin = load_latin(LATIN_CORPUS)
print(f"  {len(latin)} words")

# B-dialect simulation
print("\nRunning B-dialect simulation (exp_236 params)...")
vb = compute_vms_distr(lines_by_dialect['B'])
sg_B = vb['suffix_global']
suffix_lf_B = make_suppressed_suffix(sg_B, B_PARAMS['r_lf'])
suffix_mid_B = make_suppressed_suffix(sg_B, B_PARAMS['r_mid'])
ll_onsets_B = build_ll_onsets(vb['onset_ll'], B_PARAMS['d_boost'])
lines_B_sim = []
for i in range(N_SIM):
    rng = random.Random(SEED + i)
    ls = run_sim(latin, vb['onset_global'], sg_B, suffix_lf_B, suffix_mid_B,
                 ll_onsets_B, vb['onset_lf'], vb['onset_ll'], B_PARAMS,
                 vb['n_lines'], rng)
    lines_B_sim.extend(ls)
enr_B_sim, rates_B_sim = compute_bigrams_from_lines(lines_B_sim)
print(f"  Done. {sum(len(l) for l in lines_B_sim)} words generated.")

# A-dialect simulation
print("\nRunning A-dialect simulation (exp_239 params)...")
va = compute_vms_distr(lines_by_dialect['A'])
sg_A = va['suffix_global']
suffix_lf_A = make_suppressed_suffix(sg_A, A_PARAMS['r_lf'])
suffix_mid_A = make_suppressed_suffix(sg_A, A_PARAMS['r_mid'])
ll_onsets_A = build_ll_onsets(va['onset_ll'], A_PARAMS['d_boost'])
lines_A_sim = []
for i in range(N_SIM):
    rng = random.Random(SEED + 100000 + i)
    ls = run_sim(latin, va['onset_global'], sg_A, suffix_lf_A, suffix_mid_A,
                 ll_onsets_A, va['onset_lf'], va['onset_ll'], A_PARAMS,
                 va['n_lines'], rng)
    lines_A_sim.extend(ls)
enr_A_sim, rates_A_sim = compute_bigrams_from_lines(lines_A_sim)
print(f"  Done. {sum(len(l) for l in lines_A_sim)} words generated.")

# ─── Part 4: Comparison table ──────────────────────────────────────────────────

print("\n" + "="*80)
print("PART 4: VMS vs SIMULATION — SIGNIFICANT BIGRAM PAIRS")
print("="*80)

def compare_dialect(dialect_name, enr_vms, enr_sim, rates_vms, threshold=0.20):
    print(f"\n  {dialect_name} — pairs with |VMS E - 1| > {threshold*100:.0f}%:")
    print(f"  {'Pair':<14} {'VMS_E':>8} {'%dev_VMS':>9} {'Sim_E':>8} {'%dev_Sim':>9} {'Captured?'}")
    print(f"  {'-'*65}")

    sig = [(k, v) for k, v in enr_vms.items()
           if abs(v['e'] - 1) > threshold and k in enr_sim]
    sig.sort(key=lambda x: abs(x[1]['e'] - 1), reverse=True)

    captured = missed_enrich = missed_deplete = overcaptured = 0
    for (x, y), v in sig:
        vms_e = v['e']
        sim_e = enr_sim.get((x, y), 1.0)
        dev_vms = (vms_e - 1) * 100
        dev_sim = (sim_e - 1) * 100
        # Is the sim within ±20% of VMS E?
        if vms_e > 0:
            ratio = sim_e / vms_e
            if 0.80 <= ratio <= 1.20:
                cap = 'CAPTURED'
                captured += 1
            elif sim_e > vms_e * 1.20:
                cap = 'OVERCAPTURED'
                overcaptured += 1
            else:
                cap = 'MISSED'
                if vms_e > 1: missed_enrich += 1
                else: missed_deplete += 1
        else:
            cap = '?'
        print(f"  {x}→{y:<10} {vms_e:>8.3f} {dev_vms:>+8.1f}% {sim_e:>8.3f} {dev_sim:>+8.1f}% {cap}")

    print(f"\n  Summary: {captured} CAPTURED, {overcaptured} OVERCAPTURED, "
          f"{missed_enrich} MISSED(enrich), {missed_deplete} MISSED(deplete) "
          f"out of {len(sig)} significant VMS pairs")
    return captured, overcaptured, missed_enrich + missed_deplete

cap_B, over_B, miss_B = compare_dialect("B-DIALECT", enr_B, enr_B_sim, rates_B)
cap_A, over_A, miss_A = compare_dialect("A-DIALECT", enr_A, enr_A_sim, rates_A)

print()
print("="*80)
print("SUMMARY")
print("="*80)
print(f"\n  B-dialect: {cap_B} captured / {over_B} overcaptured / {miss_B} missed")
print(f"  A-dialect: {cap_A} captured / {over_A} overcaptured / {miss_A} missed")
print()
print("  Known Markov rules in model:")
print("    B: qok→ch (p_qokch=0.12)")
print("    A: y→y (p_y_y=0.10), qok→ch (p_qokch=0.12, transferred, not active if qok→ch not enriched)")
print()
print("  COMPLETENESS VERDICT:")
if miss_B == 0 and miss_A == 0:
    print("  COMPLETE — no significantly enriched pairs are systematically missed.")
elif miss_B <= 2 and miss_A <= 2:
    print("  MOSTLY COMPLETE — minor gaps exist; assess whether they affect 19-metric battery.")
else:
    print("  INCOMPLETE — additional Markov rules may improve model fidelity.")
print()
print("Done.")
