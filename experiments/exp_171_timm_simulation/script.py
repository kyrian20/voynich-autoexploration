#!/usr/bin/env python3
"""
exp_171: Timm/Schinner self-citation null simulation.
Implements the Timm & Schinner (2020) self-citation text generation algorithm
and tests whether it reproduces robust VMS positional/morphological findings.

Algorithm: At each step, copy a word from a recent window (self-citation) or
introduce a new seed word, with optional character-level modification.
This reproduces Zipf's laws, entropy, and long-range correlations — but should
NOT reproduce positional grammar (it has no concept of line positions).

Seeds from real VMS B-dialect high-frequency vocabulary.
100 simulations with VMS-length-matched line breaking.
"""
import os, sys, re, random, json, math
from collections import Counter, defaultdict

VMS_CORPUS = os.path.expanduser('~/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt')
OUT_DIR = os.path.expanduser('~/voynich-cryptanalyst/experiments/exp_171_timm_simulation/data')

# ── Timm self-citation algorithm parameters ───────────────────────────────────
WINDOW_SIZE   = 50     # look back this many words for self-citation
COPY_PROB     = 0.85   # prob of copying from window vs. using seed
MODIFY_PROB   = 0.25   # prob of character-modifying a copied word
TARGET_TOKENS = 20000  # tokens per simulated corpus
N_SIMS        = 100

# EVA alphabet for character substitutions
EVA_CHARS = list('acdeehikklnoqrsty')
EVA_CHARS = list(set(EVA_CHARS))  # deduplicate

# ── Shared onset classifier (same as exp_170) ─────────────────────────────────
def get_onset(word):
    w = word.lower()
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'):  return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('che') or w.startswith('chi'): return 'ch_e'
    if w.startswith('ch'):  return 'ch'
    if w.startswith('sh'):  return 'sh'
    if w.startswith('ok'):  return 'ok'
    if w.startswith('ot'):  return 'ot'
    if w.startswith('ol'):  return 'ol'
    if w.startswith('d'):   return 'd'
    if w.startswith('s'):   return 's'
    if w.startswith('y'):   return 'y'
    if w.startswith('k'):   return 'k'
    if w.startswith('t'):   return 't'
    if w.startswith('l'):   return 'l'
    if w.startswith('r'):   return 'r'
    return 'other'

def has_edy(word):
    return 'edy' in word or 'eedy' in word

# ── VMS corpus parser ─────────────────────────────────────────────────────────
def parse_vms(path):
    folio_words = defaultdict(list)
    raw_lines = []
    folio_para_lines = defaultdict(list)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            parts = line.split(None, 1)
            if len(parts) < 2: continue
            locus_raw, text = parts
            lparts = locus_raw.split(',')
            if len(lparts) < 2: continue
            folio_base = lparts[0].split('.')[0].lstrip('<')
            m = re.match(r'f(\d+)', folio_base)
            if not m: continue
            fnum = int(m.group(1))
            lt = lparts[1].rstrip('>').lstrip('@+*=~&')
            if not lt.startswith('P'): continue
            words = [w for w in text.split('.') if w and re.match(r'[a-z]', w) and not w.startswith('<')]
            if not words: continue
            folio_words[fnum].extend(words)
            raw_lines.append((fnum, words))
            is_para_start = lt == 'P0'
            folio_para_lines[fnum].append((is_para_start, words))
    return folio_words, raw_lines, folio_para_lines

# ── Metric computation (same as exp_170) ─────────────────────────────────────
def compute_metrics(lines, para_starts=None):
    if not lines: return {}
    all_words = [w for line in lines for w in line]
    n_total = len(all_words)
    if n_total == 0: return {}

    lf_words = [line[0] for line in lines if line]
    ll_words  = [line[-1] for line in lines if line]
    n_lf = len(lf_words)
    n_ll = len(ll_words)

    onset_counts = Counter(get_onset(w) for w in all_words)

    metrics = {}
    metrics['edy_rate']      = sum(1 for w in all_words if has_edy(w)) / n_total
    metrics['l_onset_rate']  = onset_counts.get('l', 0) / n_total

    am_overall = sum(1 for w in all_words if w.endswith('am')) / n_total
    am_at_ll   = sum(1 for w in ll_words  if w.endswith('am')) / n_ll if n_ll > 0 else 0
    metrics['am_ll_enrichment'] = (am_at_ll / am_overall) if am_overall > 0 else 0

    daiin_bigrams, daiin_cth = 0, 0
    for line in lines:
        for i in range(len(line)-1):
            if line[i] == 'daiin':
                daiin_bigrams += 1
                if get_onset(line[i+1]) == 'cth':
                    daiin_cth += 1
    cth_rate = onset_counts.get('cth', 0) / n_total
    if daiin_bigrams > 0 and cth_rate > 0:
        metrics['daiin_cth_enrichment'] = (daiin_cth / daiin_bigrams) / cth_rate
    else:
        metrics['daiin_cth_enrichment'] = 0

    y_at_lf = sum(1 for w in lf_words if get_onset(w) == 'y') / n_lf if n_lf > 0 else 0
    y_rate   = onset_counts.get('y', 0) / n_total
    metrics['y_lf_enrichment'] = (y_at_lf / y_rate) if y_rate > 0 else 0

    cth_at_lf = sum(1 for w in lf_words if get_onset(w) == 'cth') / n_lf if n_lf > 0 else 0
    metrics['cth_lf_enrichment'] = (cth_at_lf / cth_rate) if cth_rate > 0 else 0

    qok_bigrams, qok_ch = 0, 0
    for line in lines:
        for i in range(len(line)-1):
            if get_onset(line[i]) == 'qok':
                qok_bigrams += 1
                if get_onset(line[i+1]) in ('ch', 'ch_e'):
                    qok_ch += 1
    ch_rate = (onset_counts.get('ch', 0) + onset_counts.get('ch_e', 0)) / n_total
    if qok_bigrams > 0 and ch_rate > 0:
        metrics['qok_ch_enrichment'] = (qok_ch / qok_bigrams) / ch_rate
    else:
        metrics['qok_ch_enrichment'] = 0

    for cls in ['qok', 'ok', 'd', 'ch', 'qo', 'sh']:
        bigrams, self_succ = 0, 0
        cls_rate = onset_counts.get(cls, 0) / n_total
        for line in lines:
            for i in range(len(line)-1):
                if get_onset(line[i]) == cls:
                    bigrams += 1
                    if get_onset(line[i+1]) == cls:
                        self_succ += 1
        if bigrams > 0 and cls_rate > 0:
            metrics[f'{cls}_self_succ'] = (self_succ / bigrams) / cls_rate
        else:
            metrics[f'{cls}_self_succ'] = 0

    edy_count = sum(1 for w in all_words if 'edy' in w)
    ol_count  = sum(1 for w in all_words if w.endswith('ol'))
    metrics['edy_ol_ratio'] = edy_count / ol_count if ol_count > 0 else float('inf')

    d_at_ll  = sum(1 for w in ll_words if get_onset(w) == 'd') / n_ll if n_ll > 0 else 0
    d_rate   = onset_counts.get('d', 0) / n_total
    metrics['d_ll_enrichment'] = (d_at_ll / d_rate) if d_rate > 0 else 0

    sh_at_lf = sum(1 for w in lf_words if get_onset(w) == 'sh') / n_lf if n_lf > 0 else 0
    sh_rate  = onset_counts.get('sh', 0) / n_total
    metrics['sh_lf_enrichment'] = (sh_at_lf / sh_rate) if sh_rate > 0 else 0

    qok_at_lf = sum(1 for w in lf_words if get_onset(w) == 'qok') / n_lf if n_lf > 0 else 0
    qok_rate  = onset_counts.get('qok', 0) / n_total
    metrics['qok_lf_enrichment'] = (qok_at_lf / qok_rate) if qok_rate > 0 else 0

    # Extra Timm-relevant metrics
    # Word type-token ratio (Timm self-citation produces low TTR due to repetition)
    types = len(set(all_words))
    metrics['type_token_ratio'] = types / n_total

    # Mean word length (should match VMS if seeds match)
    metrics['mean_word_length'] = sum(len(w) for w in all_words) / n_total

    # Repetition rate: fraction of adjacent identical words
    identical_adj = sum(1 for line in lines for i in range(len(line)-1) if line[i] == line[i+1])
    total_adj = sum(len(line)-1 for line in lines if len(line) > 1)
    metrics['identical_adj_rate'] = identical_adj / total_adj if total_adj > 0 else 0

    return metrics

# ── Parse VMS ─────────────────────────────────────────────────────────────────
print("Parsing VMS corpus...")
folio_words, raw_lines, folio_para_lines = parse_vms(VMS_CORPUS)

folio_edy_rate = {}
folio_dialect  = {}
for fn, wds in folio_words.items():
    if len(wds) < 10: continue
    rate = sum(1 for w in wds if has_edy(w)) / len(wds)
    folio_edy_rate[fn] = rate
    folio_dialect[fn]  = 'B' if rate >= 0.05 else 'A'

a_lines = [(fn, wds) for fn, wds in raw_lines if folio_dialect.get(fn) == 'A']
b_lines = [(fn, wds) for fn, wds in raw_lines if folio_dialect.get(fn) == 'B']
b_word_lists = [wds for _, wds in b_lines]
a_word_lists = [wds for _, wds in a_lines]

b_para_lines = []
for fn, para_data in folio_para_lines.items():
    if folio_dialect.get(fn) == 'B':
        b_para_lines.extend(para_data)
b_para_word_lists = [wds for _, wds in b_para_lines]
b_para_starts = {i for i, (is_ps, _) in enumerate(b_para_lines) if is_ps}

print(f"VMS: A={len(a_word_lists)} lines, B={len(b_word_lists)} lines")

# ── Compute VMS baseline metrics ──────────────────────────────────────────────
print("Computing VMS B-dialect metrics...")
vms_b_metrics = compute_metrics(b_para_word_lists if b_para_word_lists else b_word_lists,
                                  para_starts=b_para_starts)
vms_a_metrics = compute_metrics(a_word_lists)

print("\n=== VMS B-dialect baseline ===")
for k, v in sorted(vms_b_metrics.items()):
    av = vms_a_metrics.get(k)
    print(f"  {k}: {v:.4f}" + (f" (A={av:.4f})" if av is not None else ""))

# ── Build seed vocabulary from B-dialect ──────────────────────────────────────
all_b_words = [w for wds in b_word_lists for w in wds]
b_word_freq = Counter(all_b_words)

# Top 200 words as seed pool, weighted by frequency
top_200 = b_word_freq.most_common(200)
seed_words  = [w for w, _ in top_200]
seed_weights = [c for _, c in top_200]
total_seed_w = sum(seed_weights)
seed_probs = [w/total_seed_w for w in seed_weights]

print(f"\nSeed vocabulary: {len(seed_words)} words (top B-dialect by frequency)")
print(f"  Top 10: {seed_words[:10]}")

# ── VMS line-length distribution for Protocol B ────────────────────────────────
vms_b_line_lengths = [len(wds) for wds in b_word_lists if len(wds) >= 2]
ll_counts = Counter(vms_b_line_lengths)
ll_choices = list(range(2, 20))
ll_weights_prob = [ll_counts.get(n, 0) for n in ll_choices]
ll_total = sum(ll_weights_prob)
ll_probs_norm = [w/ll_total for w in ll_weights_prob]

# ── Timm self-citation character modification ──────────────────────────────────
def modify_word(word):
    """
    Apply a small character modification to a word to simulate
    the Timm 'copy with modification' mechanism.
    Operations (pick one at random):
    - Replace a character with another EVA character
    - Delete a character (if len > 3)
    - Insert a character
    """
    if len(word) < 2:
        return word
    op = random.randint(0, 2)
    w = list(word)
    if op == 0:  # replace
        pos = random.randint(0, len(w)-1)
        w[pos] = random.choice(EVA_CHARS)
    elif op == 1 and len(w) > 3:  # delete
        pos = random.randint(0, len(w)-1)
        del w[pos]
    else:  # insert
        pos = random.randint(0, len(w))
        w.insert(pos, random.choice(EVA_CHARS))
    return ''.join(w)

# ── Timm self-citation generator ──────────────────────────────────────────────
def generate_timm_corpus(seed, target_tokens):
    """
    Generate a token stream using the Timm self-citation mechanism.
    At each step:
    - With prob COPY_PROB: copy a word from the recent window
      (uniform random from last WINDOW_SIZE tokens)
    - With prob 1-COPY_PROB: draw from seed vocabulary (frequency-weighted)
    - With prob MODIFY_PROB: apply character modification to the selected word
    Returns flat list of tokens.
    """
    random.seed(seed)
    tokens = []
    # Bootstrap with some seed words
    for _ in range(min(WINDOW_SIZE, 20)):
        w = random.choices(seed_words, weights=seed_probs)[0]
        tokens.append(w)

    while len(tokens) < target_tokens:
        if random.random() < COPY_PROB and len(tokens) >= WINDOW_SIZE:
            # Copy from window
            start = max(0, len(tokens) - WINDOW_SIZE)
            source = random.choice(tokens[start:])
        else:
            # Draw from seed vocabulary
            source = random.choices(seed_words, weights=seed_probs)[0]

        # Optionally modify
        if random.random() < MODIFY_PROB:
            source = modify_word(source)

        tokens.append(source)

    return tokens[:target_tokens]

def tokens_to_lines(tokens):
    """Break a flat token list into lines using VMS B-dialect line-length distribution."""
    lines = []
    para_starts = set()
    PARA_SIZE = 10  # lines per paragraph
    pos = 0
    while pos < len(tokens):
        line_len = random.choices(ll_choices, weights=ll_probs_norm)[0]
        chunk = tokens[pos:pos+line_len]
        if not chunk: break
        lines.append(chunk)
        pos += line_len
        if len(lines) % PARA_SIZE == 1:
            para_starts.add(len(lines) - 1)
    return lines, para_starts

# ── Run simulations ───────────────────────────────────────────────────────────
print(f"\nRunning {N_SIMS} Timm simulations...")
timm_results = []
for sim_idx in range(N_SIMS):
    seed = sim_idx * 1337
    tokens = generate_timm_corpus(seed, TARGET_TOKENS)
    # Re-seed for line breaking to keep it independent
    random.seed(seed + 99999)
    lines, para_starts = tokens_to_lines(tokens)
    m = compute_metrics(lines, para_starts=para_starts)
    timm_results.append(m)
    if (sim_idx+1) % 25 == 0:
        print(f"  Completed {sim_idx+1}/{N_SIMS}")

print(f"Done: {len(timm_results)} successful runs")

# ── Load Naibbe results for comparison ────────────────────────────────────────
naibbe_path = os.path.expanduser(
    '~/voynich-cryptanalyst/experiments/exp_170_naibbe_simulation/data/simulation_results.json')
try:
    with open(naibbe_path) as f:
        naibbe_raw = json.load(f)
    naibbe_results = naibbe_raw.get('latin_B', [])  # Latin Protocol B as reference
    print(f"Loaded {len(naibbe_results)} Naibbe (Latin-B) runs for comparison")
except Exception as e:
    naibbe_results = []
    print(f"Could not load Naibbe results: {e}")

# ── Analysis ──────────────────────────────────────────────────────────────────
def summarize(values):
    values = [v for v in values if v is not None and not math.isinf(v)]
    if not values:
        return {'mean': None, 'std': None, 'p5': None, 'p95': None, 'n': 0}
    vs = sorted(values)
    n = len(vs)
    mean = sum(vs) / n
    std = math.sqrt(sum((v-mean)**2 for v in vs) / n)
    return {'mean': mean, 'std': std, 'p5': vs[max(0,int(.05*n))], 'p95': vs[min(n-1,int(.95*n))], 'n': n}

def status(vms_val, summ):
    if summ['p5'] is None or vms_val is None:
        return 'N/A'
    if summ['p5'] <= vms_val <= summ['p95']:
        return 'INSIDE'
    return 'BELOW' if vms_val < summ['p5'] else 'ABOVE'

metric_labels = {
    'edy_rate':             'edy rate (B-dialect marker)',
    'l_onset_rate':         'l-onset rate (F131)',
    'am_ll_enrichment':     '-am LL enrichment (F087)',
    'daiin_cth_enrichment': 'daiin→cth enrichment (F125)',
    'y_lf_enrichment':      'y-onset LF enrichment (F098)',
    'cth_lf_enrichment':    'cth LF enrichment (~1.0 expected B)',
    'qok_ch_enrichment':    'qok→ch enrichment (B sequential)',
    'qok_self_succ':        'qok self-succession',
    'ok_self_succ':         'ok self-succession',
    'd_self_succ':          'd self-succession (~1.0 expected)',
    'ch_self_succ':         'ch self-succession',
    'edy_ol_ratio':         '-edy/-ol ratio (suffix paradigm)',
    'd_ll_enrichment':      'd LL enrichment (line-closing)',
    'sh_lf_enrichment':     'sh LF enrichment (B opener)',
    'qok_lf_enrichment':    'qok LF enrichment (depleted in B)',
    'type_token_ratio':     'type-token ratio (Zipf proxy)',
    'mean_word_length':     'mean word length',
    'identical_adj_rate':   'identical adjacent words rate',
}

print("\n" + "="*80)
print("TIMM vs VMS-B COMPARISON")
print("="*80)
print(f"\n{'Metric':<36} {'VMS-B':>7} {'Timm mean':>9} {'Timm 95CI':>18} {'Status':>7} {'Naibbe-LatB mean':>16}")
print("-"*100)

comparison_table = {}
for metric_key, label in metric_labels.items():
    vms_val  = vms_b_metrics.get(metric_key)
    timm_sum = summarize([m.get(metric_key) for m in timm_results])
    timm_st  = status(vms_val, timm_sum)

    naibbe_vals = [m.get(metric_key) for m in naibbe_results if m.get(metric_key) is not None]
    naibbe_mean = sum(naibbe_vals)/len(naibbe_vals) if naibbe_vals else None

    comparison_table[metric_key] = {
        'vms_b': vms_val, 'timm': timm_sum, 'timm_status': timm_st,
        'naibbe_lb_mean': naibbe_mean
    }

    vms_str  = f"{vms_val:.3f}" if vms_val is not None else "None"
    tmean    = f"{timm_sum['mean']:.3f}" if timm_sum['mean'] is not None else "N/A"
    tci      = f"[{timm_sum['p5']:.3f},{timm_sum['p95']:.3f}]" if timm_sum['p5'] is not None else "N/A"
    nb_mean  = f"{naibbe_mean:.3f}" if naibbe_mean is not None else "N/A"
    print(f"{label[:36]:<36} {vms_str:>7} {tmean:>9} {tci:>18} {timm_st:>7} {nb_mean:>16}")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n\n=== SUMMARY: INSIDE/ABOVE/BELOW ===")
inside = [k for k, r in comparison_table.items() if r['timm_status'] == 'INSIDE']
above  = [k for k, r in comparison_table.items() if r['timm_status'] == 'ABOVE']
below  = [k for k, r in comparison_table.items() if r['timm_status'] == 'BELOW']
print(f"INSIDE ({len(inside)}): {[metric_labels[k] for k in inside]}")
print(f"ABOVE  ({len(above)}):  {[metric_labels[k] for k in above]}")
print(f"BELOW  ({len(below)}):  {[metric_labels[k] for k in below]}")

print("\n\n=== WHAT TIMM REPRODUCES vs NAIBBE (side by side) ===")
print(f"{'Metric':<36} {'VMS-B':>7} {'Timm':>7} {'T-stat':>7} {'Naibbe':>7} {'N-stat':>7}")
print("-"*80)
for metric_key, label in metric_labels.items():
    row = comparison_table[metric_key]
    vms = row['vms_b']
    tm = row['timm'].get('mean')
    ts = row['timm_status']
    nb = row['naibbe_lb_mean']

    # Rough Naibbe status from exp_170 (recompute from Latin-B)
    naibbe_summ = summarize([m.get(metric_key) for m in naibbe_results])
    ns = status(vms, naibbe_summ)

    vstr = f"{vms:.3f}" if vms is not None else "N/A"
    tstr = f"{tm:.3f}" if tm is not None else "N/A"
    nstr = f"{nb:.3f}" if nb is not None else "N/A"
    print(f"{label[:36]:<36} {vstr:>7} {tstr:>7} {ts:>7} {nstr:>7} {ns:>7}")

# ── Save data ─────────────────────────────────────────────────────────────────
os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(OUT_DIR, 'timm_results.json'), 'w') as f:
    json.dump(timm_results, f, indent=2)
print(f"\nSaved simulation data to {OUT_DIR}/timm_results.json")
print("Done.")
