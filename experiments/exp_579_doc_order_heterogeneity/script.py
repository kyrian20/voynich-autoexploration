"""
exp_579: Document-Order Heterogeneity in B-Dialect — Characterization and Driver Analysis

exp_576 found that B-dialect VMS has systematic document-order heterogeneity:
First half: am_ll=5.825, y_lf=2.745; Second half: am_ll=7.147, y_lf=3.889.
Random splits show no shift — the gradient is document-order-specific.

This experiment:
1. Characterizes the shift at folio-quartile granularity across key metrics
2. Tests Candidate A: scribal-hand transitions
3. Tests Candidate B: section composition
4. Reports which driver (if any) explains the document-order gradient
"""
from pathlib import Path as _RepositoryPath

import os, re, math
from collections import Counter, defaultdict

DATA_PATH = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt'))

def folio_sort_key(fname):
    """Convert folio name to numeric sort key preserving document order."""
    m = re.match(r'f(\d+)(r|v|r1|r2|v1|v2)?', fname)
    if not m:
        if fname == 'fRos': return (999, 0)
        return (9999, 0)
    num = int(m.group(1))
    side = m.group(2) or 'r'
    side_val = {'r':0, 'r1':0, 'r2':1, 'v':2, 'v1':2, 'v2':3}.get(side, 0)
    return (num, side_val)

# ── PARSING ───────────────────────────────────────────────────────────────────

ONSET_ORDER = [
    ('qok','qok'), ('qot','qot'), ('qo','qo'), ('cth','cth'),
    ('ch','ch'),   ('sh','sh'),   ('ok','ok'),  ('ot','ot'),
    ('ol','ol'),   ('d','d'),     ('s','s'),    ('y','y'),
    ('k','k'),     ('t','t'),     ('l','l'),    ('r','r'),
    ('p','p'),     ('f','f'),     ('o','o'),
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix):
            return label
    return 'other'

def clean_word(w):
    w = re.sub(r'[*@&~=+$#{}?!\[\]<>%-]', '', w)
    return w.strip()

def parse_transcription(path):
    """Parse ZL3b file. Returns list of dicts, one per line, sorted by folio number."""
    with open(path) as f:
        content = f.read()

    lines = content.split('\n')
    current_folio = None
    current_lang = None
    current_hand = None
    current_quire = None
    records = []

    for line in lines:
        # Folio header
        hdr = re.match(r'<(f[^.>]+)>\s+<!\s*([^>]+)>', line)
        if hdr:
            folio_name = hdr.group(1)
            meta_str = hdr.group(2)
            meta = {}
            for kv in re.findall(r'\$(\w+)=(\w+)', meta_str):
                meta[kv[0]] = kv[1]
            current_folio = folio_name
            current_lang = meta.get('L', '?')
            current_hand = meta.get('H', '?')
            current_quire = meta.get('Q', '?')
            continue

        # Text line
        if current_folio is None:
            continue
        tline = re.match(r'<([^.>]+\.\d+)[,;][^>]*>\s+(.*)', line)
        if not tline:
            continue
        line_id = tline.group(1)
        text_raw = tline.group(2)

        # Strip non-text
        text = re.sub(r'<%>', '', text_raw)
        text = re.sub(r'<[^>]*>', '', text)
        text = re.sub(r'[*@&~=+$#{}?!<>%]', '', text)

        words = []
        for tok in re.split(r'[\s.,;]+', text):
            tok = tok.strip()
            if not tok:
                continue
            # Handle alternates [a:b] → take first
            tok = re.sub(r'\[([^:]*):([^\]]*)\]', r'\1', tok)
            tok = re.sub(r'\{[^}]*\}', '', tok)
            tok = tok.strip('-').strip()
            if tok and re.match(r'^[a-z]+$', tok):
                words.append(tok)

        if not words:
            continue

        records.append({
            'folio': current_folio,
            'lang': current_lang,
            'hand': current_hand,
            'quire': current_quire,
            'words': words,
        })

    # Sort by folio sort key
    records.sort(key=lambda r: folio_sort_key(r['folio']))
    return records

# ── SECTION ASSIGNMENT ────────────────────────────────────────────────────────

def folio_to_num(folio_name):
    """Extract numeric folio number."""
    m = re.match(r'f(\d+)', folio_name)
    if m:
        return int(m.group(1))
    return 9999

def assign_section(folio_name):
    """Assign B-dialect folio to manuscript section."""
    fn = folio_to_num(folio_name)
    if folio_name == 'fRos':
        return 'B_astro'   # rose/cosmological foldout
    # B-dialect folios:
    # f26-f66: herbal/botanical (Quires D-H)
    # f75-f84: bio/balneological (Quire M)
    # f85-f95: stars/astronomical (Quires N, Q)
    # f103-f116: text/recipes/pharma (Quire T)
    if 26 <= fn <= 72:
        return 'B_herbal'
    elif 73 <= fn <= 84:
        return 'B_bio'
    elif 85 <= fn <= 102:
        return 'B_astro'
    elif 103 <= fn <= 116:
        return 'B_pharma'
    return 'other'

# ── METRIC COMPUTATION ────────────────────────────────────────────────────────

SUFFIX_PATTERNS = ['eedy', 'edy', 'aiin', 'ain', 'am', 'ey', 'ol', 'or', 'al', 'ar', 'dy']

def get_suffix(w):
    for s in SUFFIX_PATTERNS:
        if w.endswith(s):
            return s
    return 'other'

def compute_metrics(lines_data):
    """
    Compute all metrics for a list of line records.
    Each record has 'words' (list of word strings).

    Returns a dict of metric_name -> value.
    """
    # We need positional info: for each line, identify LF (last word), LL (second-to-last), pos0 (first)
    # and onset of each word

    total_words = 0
    total_lines = 0

    # Positional counts
    am_at_ll = 0; total_ll = 0
    am_at_lf = 0; am_at_mid = 0
    d_at_ll = 0
    y_at_lf = 0
    qok_at_lf = 0
    s_at_lf = 0

    # Onset frequency counts
    onset_counts = Counter()

    # Self-succession (for ok, ch, qok, overall)
    prev_onset = None
    ss_total = 0; ss_same = 0
    ss_ok_total = 0; ss_ok_same = 0
    ss_ch_total = 0; ss_ch_same = 0
    ss_qok_total = 0; ss_qok_same = 0

    # adj_rate
    prev_word = None
    adj_pairs = 0; total_pairs = 0

    # Word/line length
    word_lens = []
    line_lens = []

    # Suffix (edy)
    edy_count = 0

    for rec in lines_data:
        words = rec['words']
        if not words:
            continue
        n = len(words)
        total_lines += 1
        total_words += n
        line_lens.append(n)

        for i, w in enumerate(words):
            onset = get_onset(w)
            word_lens.append(len(w))
            onset_counts[onset] += 1

            # Position flags — matches battery convention in exp_576:
            #   LF = Line First = index 0 (first word)
            #   LL = Line Last  = index n-1 (last word)
            #   mid = words at index 1..n-2 (between first and last)
            is_lf = (i == 0)               # Line First
            is_ll = (i == n - 1)           # Line Last
            is_mid = (not is_lf and not is_ll)

            # am (word ends with 'am') — enriched at LL in VMS
            if w.endswith('am'):
                if is_ll:   am_at_ll += 1
                elif is_lf: am_at_lf += 1
                else:       am_at_mid += 1

            if is_ll:
                total_ll += 1
                if onset == 'd': d_at_ll += 1

            if is_lf:
                if onset == 'y':   y_at_lf += 1
                if onset == 'qok': qok_at_lf += 1
                if onset == 's':   s_at_lf += 1

            # Self-succession
            if prev_onset is not None:
                ss_total += 1
                if onset == prev_onset:
                    ss_same += 1
                if prev_onset == 'ok':
                    ss_ok_total += 1
                    if onset == 'ok': ss_ok_same += 1
                if prev_onset == 'ch':
                    ss_ch_total += 1
                    if onset == 'ch': ss_ch_same += 1
                if prev_onset == 'qok':
                    ss_qok_total += 1
                    if onset == 'qok': ss_qok_same += 1

            prev_onset = onset

            # adj_rate
            if prev_word is not None:
                total_pairs += 1
                if w == prev_word:
                    adj_pairs += 1
            prev_word = w

            # edy
            suf = get_suffix(w)
            if suf in ('edy', 'eedy'):
                edy_count += 1

    if total_words == 0:
        return None

    # Compute rates
    am_ll_rate = am_at_ll / total_ll if total_ll > 0 else 0
    am_lf_rate = am_at_lf / total_lines if total_lines > 0 else 0
    am_mid_rate = am_at_mid / (total_words - 2*total_lines) if total_words > 2*total_lines else 0

    # am_lf_enr: enrichment of am at LF vs MID
    am_lf_enr = am_lf_rate / am_mid_rate if am_mid_rate > 0 else 0
    am_mid_enr = am_mid_rate  # raw rate

    y_lf_rate = y_at_lf / total_lines if total_lines > 0 else 0
    qok_lf_rate = qok_at_lf / total_lines if total_lines > 0 else 0
    s_lf_rate = s_at_lf / total_lines if total_lines > 0 else 0
    d_ll_rate = d_at_ll / total_ll if total_ll > 0 else 0

    ss_mean = ss_same / ss_total if ss_total > 0 else 0
    ss_ok = ss_ok_same / ss_ok_total if ss_ok_total > 0 else 0
    ss_ch = ss_ch_same / ss_ch_total if ss_ch_total > 0 else 0
    ss_qok = ss_qok_same / ss_qok_total if ss_qok_total > 0 else 0

    adj_rate = adj_pairs / total_pairs if total_pairs > 0 else 0

    mean_line = sum(line_lens) / len(line_lens) if line_lens else 0
    mean_word = sum(word_lens) / len(word_lens) if word_lens else 0
    edy_rate = edy_count / total_words

    # Onset frequencies
    onset_freqs = {o: onset_counts[o] / total_words for o, _ in ONSET_ORDER}

    return {
        'am_ll': am_ll_rate,
        'y_lf': y_lf_rate,
        'd_ll': d_ll_rate,
        'qok_lf': qok_lf_rate,
        's_lf': s_lf_rate,
        'ss_mean': ss_mean,
        'ss_ok': ss_ok,
        'ss_ch': ss_ch,
        'ss_qok': ss_qok,
        'adj_rate': adj_rate,
        'mean_line': mean_line,
        'mean_word': mean_word,
        'edy_rate': edy_rate,
        'qok_rate': onset_freqs.get('qok', 0),
        'ch_rate': onset_freqs.get('ch', 0),
        'sh_rate': onset_freqs.get('sh', 0),
        'd_rate': onset_freqs.get('d', 0),
        'y_rate': onset_freqs.get('y', 0),
        'ok_rate': onset_freqs.get('ok', 0),
        'l_rate': onset_freqs.get('l', 0),
        'n_lines': total_lines,
        'n_words': total_words,
    }

# ── MAIN ──────────────────────────────────────────────────────────────────────

print("exp_579: Document-Order Heterogeneity — B-Dialect Characterization")
print("=" * 70)

records = parse_transcription(DATA_PATH)
print(f"Total records parsed: {len(records)}")

# Filter B-dialect
b_records = [r for r in records if r['lang'] == 'B']
print(f"B-dialect line records: {len(b_records)}")

# Assign sections
for r in b_records:
    r['section'] = assign_section(r['folio'])

# Show folio distribution
folio_set = sorted(set(r['folio'] for r in b_records), key=folio_sort_key)

print(f"\nB-dialect folios in document order ({len(folio_set)} folios):")
# Show section + hand per folio
folio_info = {}
for r in b_records:
    folio_info[r['folio']] = (r['hand'], r['section'])
for f in folio_set:
    h, s = folio_info[f]
    print(f"  {f:12s}  hand={h}  section={s}")

# ── STEP 1: QUARTILE ANALYSIS ─────────────────────────────────────────────────

print("\n" + "=" * 70)
print("STEP 1: METRIC PROFILES BY QUARTILE AND HALF")
print("=" * 70)

# Assign each line a document position (0-indexed)
n_total = len(b_records)
for i, r in enumerate(b_records):
    r['doc_pos'] = i

# Quartile boundaries (by line count)
q_size = n_total // 4
quartile_bins = [
    ('Q1 (first 25%)',  0,          q_size),
    ('Q2 (26-50%)',     q_size,     2*q_size),
    ('Q3 (51-75%)',     2*q_size,   3*q_size),
    ('Q4 (last 25%)',   3*q_size,   n_total),
]
half_bins = [
    ('First half',   0,          n_total//2),
    ('Second half',  n_total//2, n_total),
]

# Primary metrics to report
PRIMARY_METRICS = ['am_ll', 'y_lf', 'd_ll', 'qok_lf', 's_lf', 'ss_mean', 'adj_rate',
                   'mean_line', 'mean_word', 'edy_rate']
ONSET_METRICS = ['qok_rate', 'ch_rate', 'sh_rate', 'd_rate', 'y_rate', 'ok_rate', 'l_rate']
SS_METRICS = ['ss_ok', 'ss_ch', 'ss_qok']

ALL_METRICS = PRIMARY_METRICS + ONSET_METRICS + SS_METRICS

# Compute metrics for each bin
def metrics_for_bin(records, start, end):
    return compute_metrics(records[start:end])

bin_metrics = {}
print(f"\nLine distribution: n={n_total}, Q_size≈{q_size}")
for label, start, end in quartile_bins + half_bins:
    m = metrics_for_bin(b_records, start, end)
    bin_metrics[label] = m
    print(f"  {label}: lines={m['n_lines']}, words={m['n_words']}")

# Show primary metrics table
print("\n--- PRIMARY POSITIONAL METRICS ---")
fmt_labels = [label for label, _, _ in quartile_bins + half_bins]
header = f"{'Metric':12s}" + "".join(f"  {l[:16]:>16s}" for l in fmt_labels)
print(header)
for metric in PRIMARY_METRICS:
    row = f"{metric:12s}"
    for label in fmt_labels:
        v = bin_metrics[label][metric]
        row += f"  {v:16.4f}"
    print(row)

# Show onset frequency table
print("\n--- ONSET CLASS FREQUENCIES ---")
print(f"{'Metric':12s}" + "".join(f"  {l[:16]:>16s}" for l in fmt_labels))
for metric in ONSET_METRICS + SS_METRICS:
    row = f"{metric:12s}"
    for label in fmt_labels:
        v = bin_metrics[label][metric]
        row += f"  {v:16.4f}"
    print(row)

# Flag metrics with large quartile range
print("\n--- QUARTILE RANGE ANALYSIS ---")
print("Metric                  Q1       Q2       Q3       Q4    Range  StdErr  Ratio")
for metric in PRIMARY_METRICS + ['qok_rate', 'ch_rate']:
    vals = [bin_metrics[f'Q{i+1} (first 25%)' if i==0 else
                        f'Q{i+1} (26-50%)' if i==1 else
                        f'Q{i+1} (51-75%)' if i==2 else
                        'Q4 (last 25%)'][metric]
            for i in range(4)]
    # Fix: directly iterate
    qvals = []
    for label, _, _ in quartile_bins:
        qvals.append(bin_metrics[label][metric])
    q_range = max(qvals) - min(qvals)
    # Within-quartile standard error approximation: use variation across halves as proxy
    # We'll use half difference / 2 as the SE proxy
    half_vals = [bin_metrics[h][metric] for h, _, _ in half_bins]
    se_approx = abs(half_vals[1] - half_vals[0]) / 2
    ratio = q_range / (se_approx + 1e-9) if se_approx > 0 else 0
    flag = " *LARGE*" if ratio > 1.5 else ""
    print(f"{metric:20s}  {qvals[0]:.4f}  {qvals[1]:.4f}  {qvals[2]:.4f}  {qvals[3]:.4f}  "
          f"{q_range:.4f}  {se_approx:.4f}  {ratio:.2f}{flag}")

# ── STEP 2A: SCRIBAL HAND ANALYSIS ───────────────────────────────────────────

print("\n" + "=" * 70)
print("STEP 2A: CANDIDATE A — SCRIBAL HAND ANALYSIS")
print("=" * 70)

# Group by scribal hand
hand_records = defaultdict(list)
for r in b_records:
    hand_records[r['hand']].append(r)

print("\nB-dialect line counts by scribal hand:")
for hand in sorted(hand_records.keys()):
    n = len(hand_records[hand])
    folios = sorted(set(r['folio'] for r in hand_records[hand]), key=folio_sort_key)
    sections = Counter(r['section'] for r in hand_records[hand])
    print(f"  Hand {hand}: {n} lines, {len(folios)} folios, sections={dict(sections)}")

# Compute metrics per hand
hand_metrics = {}
for hand in sorted(hand_records.keys()):
    m = compute_metrics(hand_records[hand])
    if m:
        hand_metrics[hand] = m

print("\n--- PRIMARY METRICS BY SCRIBAL HAND ---")
h_labels = sorted(hand_metrics.keys())
print(f"{'Metric':12s}" + "".join(f"  {'Hand '+h:>12s}" for h in h_labels))
for metric in PRIMARY_METRICS[:7]:
    row = f"{metric:12s}"
    for h in h_labels:
        v = hand_metrics[h][metric]
        row += f"  {v:12.4f}"
    print(row)

# Compare inter-hand variance vs inter-quartile variance for key metrics
print("\n--- INTER-HAND vs INTER-QUARTILE VARIANCE ---")
print(f"{'Metric':12s}  {'Hand_range':>12s}  {'Qrt_range':>12s}  {'Hand>Qrt?':>12s}")
for metric in ['am_ll', 'y_lf', 'd_ll', 's_lf']:
    h_vals = [hand_metrics[h][metric] for h in h_labels if h in hand_metrics]
    q_vals = [bin_metrics[label][metric] for label, _, _ in quartile_bins]
    h_range = max(h_vals) - min(h_vals) if h_vals else 0
    q_range = max(q_vals) - min(q_vals)
    answer = "YES (scribe>" if h_range > q_range else "NO (section?"
    print(f"{metric:12s}  {h_range:12.4f}  {q_range:12.4f}  {answer}")

# ── STEP 2B: SECTION COMPOSITION ANALYSIS ────────────────────────────────────

print("\n" + "=" * 70)
print("STEP 2B: CANDIDATE B — SECTION COMPOSITION ANALYSIS")
print("=" * 70)

# Per-section metrics
section_records = defaultdict(list)
for r in b_records:
    section_records[r['section']].append(r)

print("\nB-dialect line counts by section:")
for sec in sorted(section_records.keys()):
    n = len(section_records[sec])
    folios = sorted(set(r['folio'] for r in section_records[sec]), key=folio_sort_key)
    hands = Counter(r['hand'] for r in section_records[sec])
    print(f"  {sec}: {n} lines, {len(folios)} folios, hands={dict(hands)}")

section_metrics = {}
for sec in sorted(section_records.keys()):
    m = compute_metrics(section_records[sec])
    if m:
        section_metrics[sec] = m

print("\n--- PRIMARY METRICS BY SECTION ---")
s_labels = sorted(section_metrics.keys())
print(f"{'Metric':12s}" + "".join(f"  {s[:14]:>14s}" for s in s_labels))
for metric in PRIMARY_METRICS[:7]:
    row = f"{metric:12s}"
    for s in s_labels:
        v = section_metrics[s][metric]
        row += f"  {v:14.4f}"
    print(row)

# Section-composition prediction model
# For each quartile, compute the section composition (fraction of lines from each section)
# Then predict quartile mean = sum(section_frac * section_mean) for each metric
print("\n--- SECTION-COMPOSITION PREDICTION MODEL ---")
print("For each quartile: observed vs predicted (from section composition)")
print()

for metric in ['am_ll', 'y_lf', 'd_ll', 's_lf', 'qok_lf']:
    print(f"Metric: {metric}")
    print(f"  {'Bin':20s}  {'Observed':>10s}  {'Predicted':>10s}  {'Residual':>10s}  {'ExplainPct':>12s}")
    for label, start, end in quartile_bins + half_bins:
        bin_recs = b_records[start:end]
        # Section composition in this bin
        bin_sec_counts = Counter(r['section'] for r in bin_recs)
        bin_n = len(bin_recs)
        # Predicted = weighted sum of section means
        predicted = 0.0
        for sec, m in section_metrics.items():
            frac = bin_sec_counts.get(sec, 0) / bin_n
            predicted += frac * m[metric]
        observed = bin_metrics[label][metric]
        residual = observed - predicted
        # How much of the half-shift does section explain?
        # Compare: |predicted_shift| / |observed_shift| over halves
        pct_str = ""
        explain_pct = (1 - abs(residual) / (abs(observed) + 1e-9)) * 100
        print(f"  {label:20s}  {observed:10.4f}  {predicted:10.4f}  {residual:10.4f}  {explain_pct:12.1f}%")

    # Compute how much of first/second half shift is explained by section
    obs_shift = bin_metrics['Second half']['am_ll' if metric == 'am_ll' else metric] - \
                bin_metrics['First half']['am_ll' if metric == 'am_ll' else metric]
    # Fix: re-extract correctly
    obs_first = bin_metrics['First half'][metric]
    obs_second = bin_metrics['Second half'][metric]
    obs_shift = obs_second - obs_first

    # Predicted shift
    def predicted_for_half(half_label, half_start, half_end):
        half_recs = b_records[half_start:half_end]
        bin_sec_c = Counter(r['section'] for r in half_recs)
        n = len(half_recs)
        pred = sum((bin_sec_c.get(s, 0)/n) * section_metrics[s][metric]
                   for s in section_metrics)
        return pred

    pred_first = predicted_for_half('First half', 0, n_total//2)
    pred_second = predicted_for_half('Second half', n_total//2, n_total)
    pred_shift = pred_second - pred_first

    if abs(obs_shift) > 0.001:
        explained = pred_shift / obs_shift * 100
        print(f"  → Half-shift explanation: obs={obs_shift:+.4f}, pred={pred_shift:+.4f}, "
              f"section explains {explained:.1f}% of shift")
    print()

# ── STEP 3: MONOTONICITY AND TREND ───────────────────────────────────────────

print("=" * 70)
print("STEP 3: MONOTONIC TREND ANALYSIS")
print("=" * 70)

print("\nDoes the gradient increase monotonically from Q1→Q4?")
print(f"{'Metric':12s}  {'Q1':>8s}  {'Q2':>8s}  {'Q3':>8s}  {'Q4':>8s}  Monotonic?")
for metric in ['am_ll', 'y_lf', 'd_ll', 's_lf']:
    qvals = [bin_metrics[label][metric] for label, _, _ in quartile_bins]
    mono_up = all(qvals[i] <= qvals[i+1] for i in range(3))
    mono_dn = all(qvals[i] >= qvals[i+1] for i in range(3))
    mono_str = "YES(up)" if mono_up else ("YES(dn)" if mono_dn else "NO")
    print(f"{metric:12s}  {qvals[0]:8.4f}  {qvals[1]:8.4f}  {qvals[2]:8.4f}  {qvals[3]:8.4f}  {mono_str}")

# ── SUMMARY ───────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

# Print half shift for key metrics
print("\nKey metric shifts (First half → Second half):")
for metric in PRIMARY_METRICS[:5]:
    v1 = bin_metrics['First half'][metric]
    v2 = bin_metrics['Second half'][metric]
    shift = v2 - v1
    pct = shift / (v1 + 1e-9) * 100
    print(f"  {metric:12s}: {v1:.4f} → {v2:.4f}  (shift {shift:+.4f}, {pct:+.1f}%)")

print("\nSection composition in each half:")
for half_label, h_start, h_end in half_bins:
    half_recs = b_records[h_start:h_end]
    sec_c = Counter(r['section'] for r in half_recs)
    n = len(half_recs)
    print(f"  {half_label} ({n} lines):",
          {s: f"{100*c/n:.1f}%" for s, c in sorted(sec_c.items())})

print("\nSection composition in each quartile:")
for label, start, end in quartile_bins:
    bin_recs = b_records[start:end]
    sec_c = Counter(r['section'] for r in bin_recs)
    n = len(bin_recs)
    print(f"  {label} ({n} lines):",
          {s: f"{100*c/n:.1f}%" for s, c in sorted(sec_c.items())})

print("\nScribal hand composition in each half:")
for half_label, h_start, h_end in half_bins:
    half_recs = b_records[h_start:h_end]
    hand_c = Counter(r['hand'] for r in half_recs)
    n = len(half_recs)
    print(f"  {half_label} ({n} lines):",
          {f"H{h}": f"{100*c/n:.1f}%" for h, c in sorted(hand_c.items())})

# ── WITHIN-SECTION HAND COMPARISON ───────────────────────────────────────────
# Test whether hand differences persist within the same section
# B_astro has Hand 2 (188), Hand 3 (61), Hand 4 (159) — only section with 3 hands
print("\n" + "=" * 70)
print("WITHIN-SECTION HAND COMPARISON (B_astro only — 3 hands overlap)")
print("=" * 70)

astro_by_hand = defaultdict(list)
for r in b_records:
    if r['section'] == 'B_astro':
        astro_by_hand[r['hand']].append(r)

print("\nB_astro: line counts per hand:", {h: len(recs) for h, recs in sorted(astro_by_hand.items())})
print("\n--- METRICS WITHIN B_ASTRO BY HAND ---")
astro_hand_metrics = {}
for hand, recs in sorted(astro_by_hand.items()):
    m = compute_metrics(recs)
    if m:
        astro_hand_metrics[hand] = m

h_labels_astro = sorted(astro_hand_metrics.keys())
print(f"{'Metric':12s}" + "".join(f"  {'H'+h+' (astro)':>14s}" for h in h_labels_astro))
for metric in ['am_ll', 'y_lf', 'd_ll', 's_lf', 'qok_lf', 'ss_mean', 'adj_rate', 'edy_rate']:
    row = f"{metric:12s}"
    for h in h_labels_astro:
        v = astro_hand_metrics[h][metric]
        row += f"  {v:14.4f}"
    print(row)

# Check if within-astro hand range is large relative to cross-section range
print("\n--- WITHIN-ASTRO HAND RANGE vs CROSS-SECTION RANGE ---")
print(f"{'Metric':12s}  {'Astro_hand_range':>18s}  {'Cross-sec_range':>18s}  {'Hand residual?':>16s}")
for metric in ['am_ll', 'y_lf', 'd_ll', 's_lf']:
    astro_vals = [astro_hand_metrics[h][metric] for h in h_labels_astro if h in astro_hand_metrics]
    astro_range = max(astro_vals) - min(astro_vals) if len(astro_vals) >= 2 else 0
    cross_sec_vals = [section_metrics[s][metric] for s in section_metrics]
    cross_sec_range = max(cross_sec_vals) - min(cross_sec_vals)
    # If within-astro hand range > 30% of cross-section range, hand has independent signal
    ratio = astro_range / (cross_sec_range + 1e-9)
    residual = "YES (hand signal)" if ratio > 0.30 else "no (section primary)"
    print(f"{metric:12s}  {astro_range:18.4f}  {cross_sec_range:18.4f}  {ratio:6.2f}× ({residual})")

# ── ENRICHMENT-FACTOR COMPARISON (matching exp_576 battery metrics) ───────────
print("\n" + "=" * 70)
print("ENRICHMENT FACTOR COMPARISON (matching exp_576 am_ll units)")
print("=" * 70)
print("Note: exp_576 battery uses am_ll = (am_rate_at_LL / overall_am_rate)")
print("      exp_579 primary analysis uses raw rates; this section converts.")

def compute_enrichment_metrics(recs):
    """Compute battery-style enrichment metrics for comparison with exp_576."""
    all_words = [w for r in recs for w in r['words']]
    n_aw = len(all_words)
    if n_aw < 50:
        return None

    # Overall rates
    am_r = sum(1 for w in all_words if w.endswith('am')) / n_aw
    global_qok = sum(1 for w in all_words if get_onset(w) == 'qok') / n_aw
    global_y   = sum(1 for w in all_words if get_onset(w) == 'y') / n_aw
    global_d   = sum(1 for w in all_words if get_onset(w) == 'd') / n_aw
    global_s   = sum(1 for w in all_words if get_onset(w) == 's') / n_aw

    # Per-line positional extraction — LF=first word, LL=last word (battery convention)
    lf_words = []; ll_words = []; mid_words = []
    for r in recs:
        ws = r['words']
        n = len(ws)
        if n >= 1: lf_words.append(ws[0])    # LF = Line First
        if n >= 1: ll_words.append(ws[-1])   # LL = Line Last
        if n >= 3: mid_words.extend(ws[1:-1])

    n_lf = len(lf_words); n_ll = len(ll_words)

    # Enrichments
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / n_ll if n_ll else 0
    am_ll_enr = ll_am / am_r if am_r > 0 else 0

    def enr(onset, pos_words, n_pos):
        g = {'qok': global_qok, 'y': global_y, 'd': global_d, 's': global_s}.get(onset, 0)
        r = sum(1 for w in pos_words if get_onset(w) == onset) / n_pos if n_pos else 0
        return r / g if g > 0 else 0

    y_lf_enr = enr('y', lf_words, n_lf)
    d_ll_enr  = enr('d', ll_words, n_ll)
    qok_lf_enr = enr('qok', lf_words, n_lf)
    s_lf_enr  = enr('s', lf_words, n_lf)

    return {
        'am_ll': am_ll_enr,
        'y_lf': y_lf_enr,
        'd_ll': d_ll_enr,
        'qok_lf': qok_lf_enr,
        's_lf': s_lf_enr,
        'global_am_rate': am_r,
    }

# Compute enrichment metrics for halves and full corpus
enr_bins = [('Full corpus', 0, n_total),
            ('First half', 0, n_total//2),
            ('Second half', n_total//2, n_total)] + \
           [(label, start, end) for label, start, end in quartile_bins]

print(f"\n{'Bin':20s}  {'am_ll_enr':>10s}  {'y_lf_enr':>10s}  {'d_ll_enr':>10s}  "
      f"{'qok_lf_enr':>10s}  {'s_lf_enr':>10s}  {'am_rate':>10s}")
for label, start, end in enr_bins:
    m = compute_enrichment_metrics(b_records[start:end])
    if m:
        print(f"{label:20s}  {m['am_ll']:10.3f}  {m['y_lf']:10.3f}  {m['d_ll']:10.3f}  "
              f"{m['qok_lf']:10.3f}  {m['s_lf']:10.3f}  {m['global_am_rate']:10.4f}")

print(f"\nexp_576 reference (from corpus metrics table):")
print(f"  Full: am_ll=6.550, y_lf=3.184, First: am_ll=5.825, y_lf=2.745, "
      f"Second: am_ll=7.147, y_lf=3.889")
