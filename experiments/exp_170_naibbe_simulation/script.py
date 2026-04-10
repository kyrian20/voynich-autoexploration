#!/usr/bin/env python3
"""
exp_170: Naibbe homophonic cipher null simulation.
Tests whether robust VMS positional/morphological findings emerge from
a Greshko/Naibbe tarot-deck cipher applied to Latin or Italian plaintext.
Primary comparison: B-dialect VMS values vs Naibbe simulated corpora.

Run: 100 simulations × 2 plaintext sources × 2 line-break protocols = 400 runs.
"""
import os, sys, re, random, json, math
from collections import Counter, defaultdict

# ── Path setup ───────────────────────────────────────────────────────────────
REPO_DIR = os.path.expanduser('~/voynich-cryptanalyst/data/derived/naibbe-cipher')
VMS_CORPUS = os.path.expanduser('~/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt')
ITALIAN_CORPUS = os.path.expanduser(
    '~/voynich-cryptanalyst/data/derived/naibbe-cipher/input/examples/divina_commedia.txt')
LATIN_CORPUS = os.path.expanduser(
    '~/voynich-cryptanalyst/data/reference_corpora/latin/vulgate.txt')
OUT_DIR = os.path.expanduser(
    '~/voynich-cryptanalyst/experiments/exp_170_naibbe_simulation/data')

N_SIMS = 100
TARGET_TOKENS = 20000   # tokens per simulated corpus

# ── Import Naibbe cipher ──────────────────────────────────────────────────────
os.chdir(REPO_DIR)
sys.path.insert(0, REPO_DIR)
from naibbe_v2 import encrypt_naibbe, naibbe_tables, placeholder_to_glyph, clean_line

# ── Helper: onset class ───────────────────────────────────────────────────────
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

def is_gallows(word):
    """Gallows characters: k, t, f, p in EVA (plain or extended)"""
    onset = get_onset(word)
    return onset in ('k', 't') or word.startswith('f') or word.startswith('p')

def ends_am(word):
    return word.endswith('am') or word.endswith('ain') # -am and -ain are the main ones
    # Per F087: specifically -am
    # return word.endswith('am')

def has_edy(word):
    return 'edy' in word or 'eedy' in word

# ── VMS corpus parser ─────────────────────────────────────────────────────────
def parse_vms(path):
    """Parse VMS corpus. Returns: folio_words, raw_lines (folio_num, words list per line)."""
    folio_words = defaultdict(list)
    raw_lines = []
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
    return folio_words, raw_lines

# ── Compute metrics on a list of lines (list of word-lists) ──────────────────
def compute_metrics(lines, para_starts=None):
    """
    Compute the key discriminating metrics.
    lines: list of word-lists (each element is one line's words)
    para_starts: set of line indices that are paragraph starts (for F101 metric)
    Returns: dict of metric_name -> value
    """
    if not lines:
        return {}

    all_words = [w for line in lines for w in line]
    n_total = len(all_words)
    if n_total == 0:
        return {}

    # ── Slot classification ───────────────────────────────────────────────────
    lf_words = [line[0] for line in lines if line]
    ll_words = [line[-1] for line in lines if line]
    mid_words = [w for line in lines for i, w in enumerate(line)
                 if i > 0 and i < len(line)-1]

    # ── Baseline rates ────────────────────────────────────────────────────────
    onset_counts = Counter(get_onset(w) for w in all_words)
    n_lf = len(lf_words)
    n_ll = len(ll_words)

    metrics = {}

    # M1: edy rate (dialect marker)
    metrics['edy_rate'] = sum(1 for w in all_words if has_edy(w)) / n_total

    # M2: l-onset rate
    l_total = onset_counts.get('l', 0)
    metrics['l_onset_rate'] = l_total / n_total

    # M3: -am line-final enrichment
    am_overall = sum(1 for w in all_words if w.endswith('am')) / n_total
    am_at_ll   = sum(1 for w in ll_words if w.endswith('am')) / n_ll if n_ll > 0 else 0
    metrics['am_ll_enrichment'] = (am_at_ll / am_overall) if am_overall > 0 else 0

    # M4: daiin→cth bigram enrichment
    daiin_bigrams = 0
    daiin_cth = 0
    for line in lines:
        for i in range(len(line)-1):
            if line[i] == 'daiin':
                daiin_bigrams += 1
                if get_onset(line[i+1]) == 'cth':
                    daiin_cth += 1
    cth_rate = onset_counts.get('cth', 0) / n_total
    if daiin_bigrams > 0 and cth_rate > 0:
        daiin_cth_obs = daiin_cth / daiin_bigrams
        metrics['daiin_cth_enrichment'] = daiin_cth_obs / cth_rate
    else:
        metrics['daiin_cth_enrichment'] = 0

    # M5: k-onset (gallows) paragraph-start enrichment
    if para_starts and n_lf > 0:
        ps_words = [lines[i][0] for i in para_starts if i < len(lines) and lines[i]]
        n_ps = len(ps_words)
        k_at_ps = sum(1 for w in ps_words if get_onset(w) == 'k') / n_ps if n_ps > 0 else 0
        k_rate = onset_counts.get('k', 0) / n_total
        metrics['k_para_start_enrichment'] = (k_at_ps / k_rate) if k_rate > 0 else 0
    else:
        metrics['k_para_start_enrichment'] = None

    # M6: y-onset LF enrichment
    y_at_lf = sum(1 for w in lf_words if get_onset(w) == 'y') / n_lf if n_lf > 0 else 0
    y_rate = onset_counts.get('y', 0) / n_total
    metrics['y_lf_enrichment'] = (y_at_lf / y_rate) if y_rate > 0 else 0

    # M7: cth-onset LF enrichment (should be ~0 in A, near-baseline in B)
    cth_at_lf = sum(1 for w in lf_words if get_onset(w) == 'cth') / n_lf if n_lf > 0 else 0
    metrics['cth_lf_enrichment'] = (cth_at_lf / cth_rate) if cth_rate > 0 else 0

    # M8: qok→ch bigram enrichment (key B-dialect sequential grammar)
    qok_bigrams = 0
    qok_ch = 0
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

    # M9: onset self-succession rates (qok→qok, ok→ok, d→d, ch→ch)
    for cls in ['qok', 'ok', 'd', 'ch', 'qo', 'sh']:
        bigrams = 0
        self_succ = 0
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

    # M10: -edy / -ol ratio (B-side suffix paradigm: B favors -edy, A favors -ol)
    edy_count = sum(1 for w in all_words if 'edy' in w)
    ol_count  = sum(1 for w in all_words if w.endswith('ol'))
    metrics['edy_ol_ratio'] = edy_count / ol_count if ol_count > 0 else float('inf')

    # M11: d-onset LL enrichment (A-dialect d-words close lines)
    d_at_ll = sum(1 for w in ll_words if get_onset(w) == 'd') / n_ll if n_ll > 0 else 0
    d_rate = onset_counts.get('d', 0) / n_total
    metrics['d_ll_enrichment'] = (d_at_ll / d_rate) if d_rate > 0 else 0

    # M12: sh LF enrichment (B-dialect sh opens lines, from F159)
    sh_at_lf = sum(1 for w in lf_words if get_onset(w) == 'sh') / n_lf if n_lf > 0 else 0
    sh_rate = onset_counts.get('sh', 0) / n_total
    metrics['sh_lf_enrichment'] = (sh_at_lf / sh_rate) if sh_rate > 0 else 0

    # M13: qok LF rate (qok should NOT open lines in B-dialect — LF depleted)
    qok_at_lf = sum(1 for w in lf_words if get_onset(w) == 'qok') / n_lf if n_lf > 0 else 0
    qok_rate = onset_counts.get('qok', 0) / n_total
    metrics['qok_lf_enrichment'] = (qok_at_lf / qok_rate) if qok_rate > 0 else 0

    return metrics

# ── Parse VMS and compute B-dialect baseline ──────────────────────────────────
print("Parsing VMS corpus...")
folio_words, raw_lines = parse_vms(VMS_CORPUS)

# Assign dialects by folio
folio_edy_rate = {}
folio_dialect = {}
for fn, wds in folio_words.items():
    if len(wds) < 10: continue
    rate = sum(1 for w in wds if has_edy(w)) / len(wds)
    folio_edy_rate[fn] = rate
    folio_dialect[fn] = 'B' if rate >= 0.05 else 'A'

# Paragraph structure in VMS: VMS uses P0 for paragraph starts, P1+ for continuation
# We need to identify paragraph starts by parsing loci with line type P0
# Re-parse to get paragraph structure
folio_para_lines = defaultdict(list)  # folio -> list of (is_para_start, words)
with open(VMS_CORPUS) as f:
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
        is_para_start = lt == 'P0' or lt.startswith('P0')
        folio_para_lines[fnum].append((is_para_start, words))

# Separate A and B dialect lines
a_lines = [(fn, wds) for fn, wds in raw_lines if folio_dialect.get(fn) == 'A']
b_lines = [(fn, wds) for fn, wds in raw_lines if folio_dialect.get(fn) == 'B']

a_word_lists = [wds for _, wds in a_lines]
b_word_lists = [wds for _, wds in b_lines]

# B-dialect paragraph starts
b_para_lines = []
for fn, para_data in folio_para_lines.items():
    if folio_dialect.get(fn) == 'B':
        b_para_lines.extend(para_data)

b_para_word_lists = [wds for _, wds in b_para_lines]
b_para_starts = {i for i, (is_ps, _) in enumerate(b_para_lines) if is_ps}

print(f"VMS: A-dialect lines={len(a_word_lists)}, B-dialect lines={len(b_word_lists)}")
print(f"B-dialect para structure: {len(b_para_lines)} lines, {len(b_para_starts)} para-starts")

print("\nComputing VMS B-dialect metrics...")
vms_b_metrics = compute_metrics(b_para_word_lists if b_para_word_lists else b_word_lists,
                                  para_starts=b_para_starts)
print("VMS A-dialect metrics (for comparison)...")
vms_a_metrics = compute_metrics(a_word_lists)

print("\n=== VMS B-dialect baseline metrics ===")
for k, v in sorted(vms_b_metrics.items()):
    a_v = vms_a_metrics.get(k)
    a_str = f" (A={a_v:.3f})" if a_v is not None else ""
    print(f"  {k}: {v:.4f}{a_str}" if v is not None else f"  {k}: None")

# ── Load plaintext corpora ────────────────────────────────────────────────────
def load_plaintext(path, max_lines=None):
    """Load plaintext lines, filtering blanks and non-alpha-heavy lines."""
    lines = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            # Skip lines that are mostly numbers/roman numerals
            alpha = sum(1 for c in line if c.isalpha())
            if alpha < 3: continue
            lines.append(line)
            if max_lines and len(lines) >= max_lines:
                break
    return lines

print("\nLoading plaintext corpora...")
italian_lines = load_plaintext(ITALIAN_CORPUS)
latin_lines = load_plaintext(LATIN_CORPUS)
print(f"Italian: {len(italian_lines)} lines")
print(f"Latin: {len(latin_lines)} lines")

# ── Plaintext → paragraph structure (Protocol A) ─────────────────────────────
# Group Italian lines into canto-based paragraphs: new paragraph when we see 'Canto'
def group_italian_paragraphs(lines):
    """Returns list of (lines_in_paragraph, is_new_para_at_start)."""
    paragraphs = []  # each element: list of text lines
    current = []
    for line in lines:
        if re.match(r'[Cc]anto\s+[IVXLCDM]+', line) and current:
            paragraphs.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        paragraphs.append(current)
    return paragraphs

def group_latin_paragraphs(lines):
    """Group Vulgate lines by chapter (numeric lines start chapters)."""
    paragraphs = []
    current = []
    for line in lines:
        if re.match(r'^\d+:\d+', line) and current:
            paragraphs.append(current)
            current = [line]
        elif re.match(r'^[A-Z]{2,}', line) and current:  # Book headers
            paragraphs.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        paragraphs.append(current)
    return paragraphs

italian_paras = group_italian_paragraphs(italian_lines)
latin_paras = group_latin_paragraphs(latin_lines)
print(f"Italian paragraphs: {len(italian_paras)}")
print(f"Latin paragraphs: {len(latin_paras)}")

# ── VMS line length distribution ─────────────────────────────────────────────
vms_b_line_lengths = [len(wds) for wds in b_word_lists if len(wds) >= 2]
mean_ll = sum(vms_b_line_lengths) / len(vms_b_line_lengths)
# Distribution for Protocol B sampling
ll_counts = Counter(vms_b_line_lengths)
ll_choices = list(range(2, 20))
ll_weights = [ll_counts.get(n, 0) for n in ll_choices]
ll_total = sum(ll_weights)
ll_probs = [w/ll_total for w in ll_weights]
print(f"\nVMS B-dialect line-length distribution: mean={mean_ll:.1f}")
print(f"  Lengths 3-14: {[(n, ll_counts[n]) for n in range(3, 15)]}")

# ── Encrypt a plaintext corpus → list of token lists (lines) ─────────────────
def encrypt_corpus_protocol_a(plaintext_paras, seed, target_tokens):
    """
    Protocol A: preserve sentence/paragraph structure.
    Returns (lines, para_start_indices).
    """
    random.seed(seed)
    lines = []       # list of token-lists
    para_starts = set()
    total = 0
    for para_idx, para_lines in enumerate(plaintext_paras):
        if total >= target_tokens: break
        para_start_line = len(lines)
        for text_line in para_lines:
            if total >= target_tokens: break
            cleaned = clean_line(text_line)
            if not cleaned: continue
            try:
                tokens = encrypt_naibbe(cleaned, naibbe_tables, placeholder_to_glyph, use_78=True)
            except Exception:
                continue
            if tokens:
                lines.append(tokens)
                total += len(tokens)
        if lines and len(lines) > para_start_line:
            para_starts.add(para_start_line)
    return lines, para_starts

def encrypt_corpus_protocol_b(plaintext_paras, seed, target_tokens):
    """
    Protocol B: break ciphertext at VMS-matching token counts.
    Returns (lines, para_start_indices).
    """
    random.seed(seed)
    # First, generate a continuous token stream from the plaintext
    all_tokens = []
    for para_lines in plaintext_paras:
        for text_line in para_lines:
            cleaned = clean_line(text_line)
            if not cleaned: continue
            try:
                tokens = encrypt_naibbe(cleaned, naibbe_tables, placeholder_to_glyph, use_78=True)
                all_tokens.extend(tokens)
            except Exception:
                continue
            if len(all_tokens) >= target_tokens * 2:
                break
        if len(all_tokens) >= target_tokens * 2:
            break

    # Break into lines matching VMS line-length distribution
    lines = []
    para_starts = set()
    PARA_SIZE = 10  # lines per paragraph (approximate VMS para size)
    pos = 0
    while pos < len(all_tokens) and len([w for l in lines for w in l]) < target_tokens:
        line_len = random.choices(ll_choices, weights=ll_probs)[0]
        chunk = all_tokens[pos:pos+line_len]
        if not chunk: break
        pos += line_len
        lines.append(chunk)
        # Mark paragraph starts
        if len(lines) % PARA_SIZE == 1:
            para_starts.add(len(lines) - 1)
    return lines, para_starts

# ── Run simulations ───────────────────────────────────────────────────────────
print("\n" + "="*60)
print("RUNNING SIMULATIONS")
print("="*60)

results = {}  # (corpus, protocol) -> list of metric dicts

for corpus_name, corpus_paras in [('italian', italian_paras), ('latin', latin_paras)]:
    for protocol in ['A', 'B']:
        key = (corpus_name, protocol)
        print(f"\n--- {corpus_name.upper()}, Protocol {protocol} ({N_SIMS} runs) ---")
        run_metrics = []
        for sim_idx in range(N_SIMS):
            seed = sim_idx * 1000 + (0 if corpus_name == 'italian' else 500) + (0 if protocol == 'A' else 250)
            try:
                if protocol == 'A':
                    lines, para_starts = encrypt_corpus_protocol_a(corpus_paras, seed, TARGET_TOKENS)
                else:
                    lines, para_starts = encrypt_corpus_protocol_b(corpus_paras, seed, TARGET_TOKENS)
                if not lines:
                    continue
                m = compute_metrics(lines, para_starts=para_starts)
                run_metrics.append(m)
            except Exception as e:
                print(f"  Sim {sim_idx} failed: {e}")
            if (sim_idx+1) % 25 == 0:
                print(f"  Completed {sim_idx+1}/{N_SIMS} sims")
        results[key] = run_metrics
        print(f"  Done: {len(run_metrics)} successful runs")

# ── Save raw simulation data ──────────────────────────────────────────────────
os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(OUT_DIR, 'simulation_results.json'), 'w') as f:
    json.dump({f"{k[0]}_{k[1]}": v for k, v in results.items()}, f, indent=2)
print(f"\nSaved simulation data to {OUT_DIR}/simulation_results.json")

# ── Analysis: compare VMS vs simulated distributions ─────────────────────────
def summarize_distribution(values):
    values = [v for v in values if v is not None]
    if not values:
        return {'mean': None, 'std': None, 'p5': None, 'p95': None, 'n': 0}
    values_sorted = sorted(values)
    n = len(values)
    mean = sum(values) / n
    var = sum((v - mean)**2 for v in values) / n
    std = math.sqrt(var)
    p5 = values_sorted[max(0, int(0.05*n))]
    p95 = values_sorted[min(n-1, int(0.95*n))]
    return {'mean': mean, 'std': std, 'p5': p5, 'p95': p95, 'n': n}

def inside_interval(vms_val, summary):
    if summary['p5'] is None or vms_val is None:
        return 'N/A'
    if summary['p5'] <= vms_val <= summary['p95']:
        return 'INSIDE'
    elif vms_val < summary['p5']:
        return 'BELOW'
    else:
        return 'ABOVE'

print("\n" + "="*60)
print("COMPARISON: VMS B-DIALECT vs NAIBBE SIMULATIONS")
print("="*60)

metric_labels = {
    'edy_rate': 'edy rate (B-dialect marker)',
    'l_onset_rate': 'l-onset rate (F131)',
    'am_ll_enrichment': '-am LL enrichment (F087)',
    'daiin_cth_enrichment': 'daiin→cth enrichment (F125)',
    'k_para_start_enrichment': 'k@para-start enrichment (F101)',
    'y_lf_enrichment': 'y-onset LF enrichment (F098)',
    'cth_lf_enrichment': 'cth LF enrichment (expect low in A, ~1.0 in B)',
    'qok_ch_enrichment': 'qok→ch enrichment (B sequential grammar)',
    'qok_self_succ': 'qok self-succession enrichment',
    'ok_self_succ': 'ok self-succession enrichment',
    'd_self_succ': 'd self-succession enrichment (expect ~1)',
    'ch_self_succ': 'ch self-succession enrichment',
    'edy_ol_ratio': '-edy/-ol ratio (B-suffix paradigm)',
    'd_ll_enrichment': 'd-onset LL enrichment (A closing particle)',
    'sh_lf_enrichment': 'sh LF enrichment (B opener)',
    'qok_lf_enrichment': 'qok LF enrichment (should be depleted in B)',
}

print(f"\n{'Metric':<35} {'VMS-B':>8} {'Ital-A mean':>11} {'Ital-A 95CI':>18} {'Lat-A mean':>10} {'Lat-A 95CI':>18} {'Ital-B mean':>11} {'Lat-B mean':>10}")
print("-"*140)

comparison_table = {}

for metric_key, label in metric_labels.items():
    vms_val = vms_b_metrics.get(metric_key)
    row = {'vms_b': vms_val, 'label': label}

    col_parts = []
    for corpus_name in ['italian', 'latin']:
        for protocol in ['A', 'B']:
            key = (corpus_name, protocol)
            if key not in results: continue
            vals = [m.get(metric_key) for m in results[key] if m.get(metric_key) is not None]
            summary = summarize_distribution(vals)
            row[f'{corpus_name}_{protocol}'] = summary
            inside = inside_interval(vms_val, summary)
            col_parts.append((corpus_name, protocol, summary, inside))

    comparison_table[metric_key] = row

    # Print concise row
    vms_str = f"{vms_val:.3f}" if vms_val is not None else "None"
    parts_str = []
    for cn, prot, summ, inside in col_parts:
        if summ['mean'] is not None:
            ci_str = f"[{summ['p5']:.3f},{summ['p95']:.3f}]"
            parts_str.append(f"{summ['mean']:>8.3f} {ci_str:>18} {inside:>8}")
        else:
            parts_str.append(" "*37)

    print(f"{label[:35]:<35} {vms_str:>8} {'  '.join(parts_str)}")

# ── Summary: INSIDE/BELOW/ABOVE counts per corpus/protocol ───────────────────
print("\n\n=== SUMMARY: VMS-B vs NAIBBE (INSIDE 95% CI?) ===")
print(f"{'Metric':<38} {'Ital-A':>8} {'Ital-B':>8} {'Lat-A':>8} {'Lat-B':>8}")
print("-"*75)
for metric_key, label in metric_labels.items():
    row = comparison_table.get(metric_key, {})
    results_by_combo = {}
    for cn in ['italian', 'latin']:
        for prot in ['A', 'B']:
            summ = row.get(f'{cn}_{prot}', {})
            vms_val = row.get('vms_b')
            results_by_combo[(cn, prot)] = inside_interval(vms_val, summ)

    print(f"{label[:38]:<38} "
          f"{results_by_combo.get(('italian','A'),'N/A'):>8} "
          f"{results_by_combo.get(('italian','B'),'N/A'):>8} "
          f"{results_by_combo.get(('latin','A'),'N/A'):>8} "
          f"{results_by_combo.get(('latin','B'),'N/A'):>8}")

# ── Bidirectional: what patterns does Naibbe produce that VMS lacks? ──────────
print("\n\n=== BIDIRECTIONAL CHECK: PATTERNS IN NAIBBE BUT NOT VMS-B ===")
print("(metrics where VMS-B value is OUTSIDE the Naibbe CI, indicating Naibbe artifacts)")
for metric_key, label in metric_labels.items():
    row = comparison_table.get(metric_key, {})
    vms_val = row.get('vms_b')
    for cn in ['italian', 'latin']:
        for prot in ['A', 'B']:
            summ = row.get(f'{cn}_{prot}', {})
            status = inside_interval(vms_val, summ)
            if status in ('BELOW', 'ABOVE') and summ.get('mean') is not None:
                direction = "VMS < Naibbe" if status == 'BELOW' else "VMS > Naibbe"
                print(f"  [{cn}-{prot}] {label}: {direction} "
                      f"(VMS={vms_val:.3f}, Naibbe={summ['mean']:.3f} CI=[{summ['p5']:.3f},{summ['p95']:.3f}])")

print("\n\nDone.")
