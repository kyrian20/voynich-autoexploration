"""
exp_244: Q004 — sh→qok Enrichment: Lexical Co-Clustering vs Grammatical Rule?

Question: Is the VMS B-dialect sh→qok bigram enrichment (E_mid=1.967, N=339 MID pairs)
driven by a few specific (sh-word, qok-word) pairs appearing as near-fixed collocations,
or is it a grammatical rule spread across the full sh and qok vocabulary?

If lexical co-clustering: a few specific pairs account for most of the 339 instances →
  the enrichment is a vocabulary-level constraint, not onset-level grammar.
If grammatical rule: instances are distributed across many distinct (sh-word, qok-word) pairs
  proportional to their individual frequencies.

Design:
  1. Extract all MID-only consecutive (sh-onset word, qok-onset word) pairs from B-dialect corpus
  2. Count frequency of each unique word pair
  3. Compute Herfindahl-Hirschman Index (concentration) and cumulative coverage by top-N pairs
  4. Compare: is sh-word distribution before qok-words different from sh-word global distribution?
     (Kolmogorov-Smirnov test or chi-square)
  5. Compare: is qok-word distribution after sh-words different from qok-word global distribution?
  6. Check cross-section consistency: does the enrichment appear in both herbal and cosmo B?
  7. Same analysis for qok→ch (known Markov rule) as comparison baseline

Expected outcomes:
  A) Lexical co-clustering: Top-5 sh/qok word pairs account for >50% of instances;
     HHI of pair distribution >> null expectation; specific words drive enrichment
  B) Grammatical rule: Pairs distributed proportionally; HHI ≈ null; enrichment persists
     when specific word pairs are excluded
"""

import os, re, math
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
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

def classify_section(folio_raw):
    """Rough section classification by folio number."""
    fb = folio_base(folio_raw.lstrip('+*=&~'))
    digits = re.findall(r'\d+', fb)
    if not digits: return 'unknown'
    n = int(digits[0])
    # Rough section boundaries (approximate)
    if n <= 66: return 'herbal'
    if n <= 84: return 'astro'
    if n <= 102: return 'bio'
    if n <= 116: return 'cosmo'
    return 'pharma'

def parse_vms_b_with_folio():
    """Parse B-dialect lines, retaining folio info for section analysis."""
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

    b_lines_with_folio = []
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
            if words:
                section = classify_section(folio_raw)
                b_lines_with_folio.append((words, fb, section))
    return b_lines_with_folio

def extract_bigram_pairs(lines_with_folio, onset_A, onset_B, mid_only=True):
    """
    Extract all consecutive (word_A, word_B) pairs where onset_A → onset_B.
    If mid_only: both words must be in MID positions (not LF=0, not LL=n-1).
    """
    pairs = []
    for (line, fb, section) in lines_with_folio:
        n = len(line)
        if mid_only:
            if n < 4: continue
            for i in range(1, n - 2):
                if get_onset(line[i]) == onset_A and get_onset(line[i+1]) == onset_B:
                    pairs.append((line[i], line[i+1], fb, section))
        else:
            for i in range(n - 1):
                if get_onset(line[i]) == onset_A and get_onset(line[i+1]) == onset_B:
                    pairs.append((line[i], line[i+1], fb, section))
    return pairs

def concentration_analysis(pairs, label):
    """Analyze lexical concentration of word pairs."""
    pair_counter = Counter((w1, w2) for (w1, w2, fb, s) in pairs)
    w1_counter   = Counter(w1 for (w1, w2, fb, s) in pairs)
    w2_counter   = Counter(w2 for (w1, w2, fb, s) in pairs)
    folio_counter = Counter(fb for (w1, w2, fb, s) in pairs)
    section_counter = Counter(s for (w1, w2, fb, s) in pairs)

    n_total = len(pairs)
    n_unique_pairs = len(pair_counter)
    n_unique_w1 = len(w1_counter)
    n_unique_w2 = len(w2_counter)

    # HHI of word pairs (sum of squared shares)
    hhi = sum((c/n_total)**2 for c in pair_counter.values()) if n_total > 0 else 0

    # Null HHI: if pairs are uniformly random over (unique_w1 × unique_w2) combinations
    # weighted by marginal distributions, expected HHI ≈ (Σ p_i^2)(Σ q_j^2)
    if n_total > 0 and w1_counter and w2_counter:
        hhi_null = sum((c/n_total)**2 for c in w1_counter.values()) * \
                   sum((c/n_total)**2 for c in w2_counter.values())
    else:
        hhi_null = 0

    print(f"\n{label}:")
    print(f"  Total MID pairs: {n_total}")
    print(f"  Unique word pairs: {n_unique_pairs} ({n_unique_w1} distinct {label.split('→')[0]} words × "
          f"{n_unique_w2} distinct {label.split('→')[1]} words)")
    print(f"  HHI of pair distribution: {hhi:.4f}  (null expectation: {hhi_null:.4f})")
    hhi_ratio = hhi/hhi_null if hhi_null > 0 else 0
    print(f"  HHI / null = {hhi_ratio:.2f}× {'(concentrated)' if hhi_ratio > 2 else '(near-random)'}")

    # Cumulative coverage by top-N pairs
    sorted_pairs = sorted(pair_counter.items(), key=lambda x: -x[1])
    print(f"\n  Top 20 specific word pairs (of {n_unique_pairs} unique):")
    print(f"  {'Rank':<5} {'sh-word':<16} {'qok-word':<16} {'Count':>6} {'%Total':>8}  {'Cum%':>8}")
    cumulative = 0
    for rank, ((w1, w2), cnt) in enumerate(sorted_pairs[:20], 1):
        pct = cnt / n_total * 100 if n_total > 0 else 0
        cumulative += pct
        print(f"  {rank:<5} {w1:<16} {w2:<16} {cnt:>6} {pct:>8.1f}%  {cumulative:>8.1f}%")

    # Coverage by top-N
    top_n_coverage = []
    cumsum = 0
    for rank, ((w1, w2), cnt) in enumerate(sorted_pairs, 1):
        cumsum += cnt / n_total * 100 if n_total > 0 else 0
        if rank in [1, 3, 5, 10, 20, 50]:
            top_n_coverage.append((rank, cumsum))
    print(f"\n  Cumulative coverage by top-N pairs:")
    for rank, pct in top_n_coverage:
        print(f"    Top {rank:3d} pairs: {pct:.1f}%")

    # Section distribution
    print(f"\n  Section distribution of pairs:")
    for s, cnt in sorted(section_counter.items(), key=lambda x: -x[1]):
        print(f"    {s:<12}: {cnt:>4} ({cnt/n_total*100:.1f}%)")

    # Folio distribution (top-10)
    print(f"\n  Top-10 folios by pair count:")
    for fb, cnt in sorted(folio_counter.items(), key=lambda x: -x[1])[:10]:
        print(f"    f{fb:<8}: {cnt:>4}")

    return pair_counter, w1_counter, w2_counter

def enrichment_without_top_pairs(lines_with_folio, onset_A, onset_B, exclusion_set, label):
    """
    Compute onset-level enrichment E(A→B) after removing the top-K specific word pairs.
    If enrichment is reduced by >50%, top pairs drive the effect.
    """
    # All MID pairs (both filtered and unfiltered)
    all_words_mid = []
    bg_full = Counter()
    bg_excl = Counter()

    for (line, fb, section) in lines_with_folio:
        n = len(line)
        if n < 4: continue
        for i in range(1, n - 2):
            w1, w2 = line[i], line[i+1]
            o1, o2 = get_onset(w1), get_onset(w2)
            bg_full[(o1, o2)] += 1
            if (w1, w2) not in exclusion_set:
                bg_excl[(o1, o2)] += 1

    # Unigram rates from all MID words
    all_mid_words = [line[j] for (line, fb, section) in lines_with_folio
                     for j in range(1, len(line)-1) if len(line) >= 4]
    n_mid = len(all_mid_words)
    oc_mid = Counter(get_onset(w) for w in all_mid_words)
    rates = {o: c/n_mid for o, c in oc_mid.items()} if n_mid > 0 else {}

    def compute_E(bg, label_str):
        n_total = sum(bg.values())
        pxy = bg.get((onset_A, onset_B), 0) / n_total if n_total > 0 else 0
        px = rates.get(onset_A, 0); py = rates.get(onset_B, 0)
        E = pxy / (px * py) if px * py > 0 else 0
        cnt = bg.get((onset_A, onset_B), 0)
        print(f"  {label_str}: E={E:.3f}, count={cnt}, total_pairs={n_total}")
        return E

    print(f"\n{label} — Enrichment after excluding top-K word pairs:")
    E_full = compute_E(bg_full, "Full (no exclusion)")
    E_excl = compute_E(bg_excl, f"After excluding top-{len(exclusion_set)} pairs")
    if E_full > 0:
        reduction = (E_full - E_excl) / E_full * 100
        print(f"  Enrichment reduction: {reduction:.1f}%  {'(lexically driven)' if reduction > 50 else '(spread across vocabulary)'}")
    return E_full, E_excl

# ─── Run analysis ─────────────────────────────────────────────────────────────

print("Parsing VMS B-dialect corpus...")
b_lines_with_folio = parse_vms_b_with_folio()
print(f"  B-dialect: {len(b_lines_with_folio)} lines")

print(f"\n{'='*80}")
print("LEXICAL CO-CLUSTERING ANALYSIS — sh→qok vs qok→ch (MID-ONLY PAIRS)")
print(f"{'='*80}")

# Main analysis: sh→qok
sh_qok_pairs = extract_bigram_pairs(b_lines_with_folio, 'sh', 'qok', mid_only=True)
sh_qok_counter, sh_ctr, qok_after_sh_ctr = concentration_analysis(sh_qok_pairs, "sh→qok (MID-only)")

# Comparison: qok→ch (known Markov rule)
print(f"\n{'='*80}")
qok_ch_pairs = extract_bigram_pairs(b_lines_with_folio, 'qok', 'ch', mid_only=True)
qok_ch_counter, qok_ctr, ch_after_qok_ctr = concentration_analysis(qok_ch_pairs, "qok→ch (MID-only, comparison)")

# Also compute global sh→qok for reference
sh_qok_global_pairs = extract_bigram_pairs(b_lines_with_folio, 'sh', 'qok', mid_only=False)
qok_ch_global_pairs = extract_bigram_pairs(b_lines_with_folio, 'qok', 'ch', mid_only=False)
print(f"\n  Global (not MID-only) sh→qok pairs: {len(sh_qok_global_pairs)}")
print(f"  Global (not MID-only) qok→ch pairs: {len(qok_ch_global_pairs)}")
print(f"  MID-only sh→qok pairs: {len(sh_qok_pairs)}")
print(f"  MID-only qok→ch pairs: {len(qok_ch_pairs)}")

# Enrichment excluding top pairs
print(f"\n{'='*80}")
print("ENRICHMENT DECOMPOSITION — EXCLUDING TOP WORD PAIRS")
print(f"{'='*80}")

# Get top-5 sh→qok pairs
top5_sh_qok = set(p for p, _ in sorted(sh_qok_counter.items(), key=lambda x: -x[1])[:5])
top10_sh_qok = set(p for p, _ in sorted(sh_qok_counter.items(), key=lambda x: -x[1])[:10])

enrichment_without_top_pairs(b_lines_with_folio, 'sh', 'qok', top5_sh_qok,
                              "sh→qok, excluding top-5 pairs")
enrichment_without_top_pairs(b_lines_with_folio, 'sh', 'qok', top10_sh_qok,
                              "sh→qok, excluding top-10 pairs")

# Comparison: qok→ch
top5_qok_ch = set(p for p, _ in sorted(qok_ch_counter.items(), key=lambda x: -x[1])[:5])
enrichment_without_top_pairs(b_lines_with_folio, 'qok', 'ch', top5_qok_ch,
                              "qok→ch, excluding top-5 pairs")

# Section consistency: does sh→qok enrichment appear in both herbal and cosmo?
print(f"\n{'='*80}")
print("SECTION-LEVEL sh→qok ENRICHMENT")
print(f"{'='*80}")

for target_section in ['herbal', 'cosmo', 'astro', 'bio', 'pharma']:
    # Filter to target section
    section_lines = [(line, fb, s) for (line, fb, s) in b_lines_with_folio if s == target_section]
    if len(section_lines) < 50: continue

    all_mid_words = [line[j] for (line, fb, s) in section_lines
                     for j in range(1, len(line)-1) if len(line) >= 4]
    if len(all_mid_words) < 100: continue

    oc = Counter(get_onset(w) for w in all_mid_words)
    n_total_pairs = 0
    sh_qok_cnt = 0
    for (line, fb, s) in section_lines:
        n = len(line)
        if n < 4: continue
        for i in range(1, n - 2):
            n_total_pairs += 1
            if get_onset(line[i]) == 'sh' and get_onset(line[i+1]) == 'qok':
                sh_qok_cnt += 1

    n_words = len(all_mid_words)
    sh_r = oc.get('sh', 0) / n_words
    qok_r = oc.get('qok', 0) / n_words
    E = (sh_qok_cnt / n_total_pairs) / (sh_r * qok_r) if sh_r * qok_r > 0 and n_total_pairs > 0 else 0
    print(f"  {target_section:<12}: N_lines={len(section_lines):>4}, MID_pairs={n_total_pairs:>5}, "
          f"sh→qok_cnt={sh_qok_cnt:>4}, E={E:.3f}")

# Summary verdict
print(f"\n{'='*80}")
print("VERDICT: LEXICAL CO-CLUSTERING vs GRAMMATICAL RULE?")
print(f"{'='*80}")
n_total = len(sh_qok_pairs)
sorted_sh_qok = sorted(sh_qok_counter.items(), key=lambda x: -x[1])
top5_coverage = sum(c for (_, c) in sorted_sh_qok[:5]) / n_total * 100 if n_total > 0 else 0
top10_coverage = sum(c for (_, c) in sorted_sh_qok[:10]) / n_total * 100 if n_total > 0 else 0
n_unique = len(sh_qok_counter)

print(f"\n  Total MID sh→qok instances: {n_total}")
print(f"  Unique (sh-word, qok-word) pairs: {n_unique}")
print(f"  Coverage by top-5 pairs: {top5_coverage:.1f}%")
print(f"  Coverage by top-10 pairs: {top10_coverage:.1f}%")

if top5_coverage > 60:
    verdict = "LEXICAL CO-CLUSTERING — Top-5 pairs dominate"
elif top5_coverage > 40:
    verdict = "MIXED — Moderate concentration with lexical contribution"
else:
    verdict = "GRAMMATICAL RULE — Enrichment spread across vocabulary"
print(f"\n  Verdict: {verdict}")

print("\nDone.")
