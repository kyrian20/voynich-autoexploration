"""
exp_252: H451 — Section-Level Onset Grammar Variation

Question: Do sh→qok and qok→ch MID-only enrichments differ systematically
across VMS sections (herbal vs cosmo vs astro vs bio vs pharma)? Also
compute ot→ot section distribution (H447/H448 partial) and qok→qok, y→y.

Design:
1. Parse VMS B-dialect corpus with section classification
2. For each section × key onset pair, compute MID-only E2 enrichment
3. Also compute HHI-style measures for ot→ot pairs (lexical vs grammar)
4. Compare section-level grammar intensity to corpus-level grammar

Section classification: Use folio-number ranges (approximate):
- Herbal: f1–f57 (plant illustrations)
- Astro: f57v–f73 (zodiac/astro)
- Bio/balneo: f75–f84 (biological/bathing)
- Cosmo: f85–f86 (cosmological)
- Pharma/recipe: f87–f102 (pharmaceutical)
- Stars: f103–f117 (astronomical)
Note: Currier B folio ranges overlap; use folio number as proxy.
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
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

def folio_base(folio): return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def folio_to_num(fb):
    """Convert folio base like 'f23' to integer 23."""
    m = re.match(r'[fF]?(\d+)', fb)
    return int(m.group(1)) if m else 0

def classify_section(fb):
    """Classify folio base into VMS section."""
    n = folio_to_num(fb)
    if n == 0: return 'unknown'
    if 1 <= n <= 57: return 'herbal'
    if 58 <= n <= 73: return 'astro'
    if 75 <= n <= 84: return 'bio'
    if 85 <= n <= 86: return 'cosmo'
    if 87 <= n <= 102: return 'pharma'
    if 103 <= n <= 117: return 'stars'
    return 'other'

# ─── Parse corpus ──────────────────────────────────────────────────────────────

print("Parsing VMS corpus for dialect and section classification...")

# Step 1: determine dialect per folio
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

# Step 2: collect B-dialect paragraph lines with section labels
section_lines = defaultdict(list)  # section -> list of word lists

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
            section = classify_section(fb)
            section_lines[section].append(words)

# Also collect all B-dialect lines together for full-corpus reference
all_b_lines = [wl for sec_lines in section_lines.values() for wl in sec_lines]

print(f"B-dialect sections:")
for sec in sorted(section_lines.keys()):
    n_lines = len(section_lines[sec])
    n_words = sum(len(l) for l in section_lines[sec])
    mid_words = sum(len(l)-2 for l in section_lines[sec] if len(l) > 2)
    print(f"  {sec:12s}: {n_lines:4d} lines, {n_words:5d} words, {mid_words:4d} MID words")

# ─── Compute E2 (MID-only) for pairs of interest ──────────────────────────────

KEY_PAIRS = [
    ('sh', 'qok'),    # H451 primary
    ('qok', 'ch'),    # H451 primary
    ('qok', 'qok'),   # self-succession
    ('ot', 'ot'),     # H447/H448 target
    ('y', 'y'),       # A-dialect cross-reference
    ('ch', 'qok'),    # return coupling
    ('sh', 'sh'),     # self-succession (depleted in VMS)
]

def compute_section_E2(lines, pairs):
    """Compute MID-only bigram E2 for specified pairs."""
    all_words = [w for l in lines for w in l]
    mid_words = [w for l in lines for w in l[1:-1] if len(l) > 2]
    n = len(all_words); n_mid = max(1, len(mid_words))
    oc_mid = Counter(get_onset(w) for w in mid_words)

    mid_bg = Counter()
    mid_bg_n = 0
    for line in lines:
        nn = len(line)
        if nn < 4: continue
        for i in range(1, nn-2):
            mid_bg[(get_onset(line[i]), get_onset(line[i+1]))] += 1
            mid_bg_n += 1

    results = {}
    for (x, y) in pairs:
        n_xy = mid_bg.get((x, y), 0)
        px = oc_mid.get(x, 0) / n_mid
        py = oc_mid.get(y, 0) / n_mid
        pxy = n_xy / mid_bg_n if mid_bg_n > 0 else 0
        e2 = pxy / (px * py) if px * py > 0 else float('nan')
        results[(x, y)] = {'E2': e2, 'N': n_xy, 'px': px, 'py': py, 'n_mid_bg': mid_bg_n}
    return results

print(f"\n{'='*70}")
print(f"MID-ONLY BIGRAM E2 BY SECTION (B-dialect)")
print(f"{'='*70}")

sections_order = ['herbal', 'astro', 'bio', 'cosmo', 'pharma', 'stars', 'other']

# Print header
header = f"  {'Pair':<12}"
for sec in sections_order:
    if sec in section_lines:
        header += f"  {sec[:7]:>7}"
header += f"  {'TOTAL':>7}"
print(header)
print(f"  {'-'*12}" + f"  {'-'*7}" * (sum(1 for s in sections_order if s in section_lines) + 1))

full_results = compute_section_E2(all_b_lines, KEY_PAIRS)

section_results = {}
for sec in sections_order:
    if sec in section_lines and len(section_lines[sec]) >= 10:
        section_results[sec] = compute_section_E2(section_lines[sec], KEY_PAIRS)

for (x, y) in KEY_PAIRS:
    row = f"  {x}→{y:<9}"
    for sec in sections_order:
        if sec in section_results:
            r = section_results[sec].get((x, y), {})
            e2 = r.get('E2', float('nan'))
            n = r.get('N', 0)
            if e2 != e2:  # nan
                row += f"  {'n/a':>7}"
            else:
                row += f"  {e2:>5.3f}({n:3d})"
    r_full = full_results.get((x, y), {})
    e2_full = r_full.get('E2', float('nan'))
    n_full = r_full.get('N', 0)
    row += f"  {e2_full:>5.3f}({n_full:3d})"
    print(row)

# ─── ot→ot pair-level analysis (H448) ─────────────────────────────────────────

print(f"\n{'='*70}")
print(f"ot→ot PAIR-LEVEL LEXICAL ANALYSIS (H448) — B-dialect full corpus")
print(f"{'='*70}")

ot_pairs = Counter()
for line in all_b_lines:
    nn = len(line)
    if nn < 4: continue
    for i in range(1, nn-2):
        if get_onset(line[i]) == 'ot' and get_onset(line[i+1]) == 'ot':
            ot_pairs[(line[i], line[i+1])] += 1

total_ot_ot = sum(ot_pairs.values())
unique_ot_ot = len(ot_pairs)
print(f"  Total ot→ot MID bigrams: {total_ot_ot}")
print(f"  Unique pairs: {unique_ot_ot}")

if total_ot_ot > 0:
    # HHI
    hhi = sum((c/total_ot_ot)**2 for c in ot_pairs.values())
    null_hhi = 1/unique_ot_ot if unique_ot_ot > 0 else 1
    print(f"  HHI: {hhi:.4f} (null={null_hhi:.4f}, ratio={hhi/null_hhi:.2f}×)")

    # Top pairs
    top_pairs = ot_pairs.most_common(10)
    print(f"\n  Top 10 ot→ot pairs:")
    cumulative = 0
    for (w1, w2), cnt in top_pairs:
        cumulative += cnt
        print(f"    {w1:15s} → {w2:15s}: {cnt:4d} ({100*cnt/total_ot_ot:.1f}%, cum={100*cumulative/total_ot_ot:.1f}%)")

    # Enrichment after top-10 removal
    top10_count = sum(c for _, c in top_pairs)
    residual_n = total_ot_ot - top10_count
    print(f"\n  After removing top-10 pairs: {residual_n}/{total_ot_ot} bigrams remain ({100*residual_n/total_ot_ot:.1f}%)")

    # Compare HHI to sh→qok and qok→ch for context
    print(f"\n  Reference HHI/null ratios from prior experiments:")
    print(f"    sh→qok (exp_244): 1.29× (near-random → GRAMMATICAL)")
    print(f"    qok→ch (exp_248): 1.39× (near-random → GRAMMATICAL)")
    print(f"    ot→ot:           {hhi/null_hhi:.2f}× {'→ GRAMMATICAL' if hhi/null_hhi < 2.0 else '→ LEXICAL'}")

# ─── sh→qok pair analysis (comparison) ─────────────────────────────────────────

print(f"\n{'='*70}")
print(f"sh→qok SECTION DISTRIBUTION DETAIL (H451)")
print(f"{'='*70}")

for sec in sections_order:
    if sec not in section_results: continue
    r = section_results[sec].get(('sh', 'qok'), {})
    n_lines = len(section_lines.get(sec, []))
    e2 = r.get('E2', float('nan'))
    n = r.get('N', 0)
    if e2 == e2 and n > 0:
        print(f"  {sec:12s}: E2={e2:.3f}, N={n:3d}, lines={n_lines}")
    elif n_lines > 0:
        print(f"  {sec:12s}: E2=n/a, N={n}, lines={n_lines}")

r_full = full_results.get(('sh', 'qok'), {})
print(f"  {'TOTAL':12s}: E2={r_full.get('E2', 0):.3f}, N={r_full.get('N', 0):3d}")

print(f"\n{'='*70}")
print(f"qok→ch SECTION DISTRIBUTION DETAIL (H451)")
print(f"{'='*70}")

for sec in sections_order:
    if sec not in section_results: continue
    r = section_results[sec].get(('qok', 'ch'), {})
    n_lines = len(section_lines.get(sec, []))
    e2 = r.get('E2', float('nan'))
    n = r.get('N', 0)
    if e2 == e2 and n > 0:
        print(f"  {sec:12s}: E2={e2:.3f}, N={n:3d}, lines={n_lines}")
    elif n_lines > 0:
        print(f"  {sec:12s}: E2=n/a, N={n}, lines={n_lines}")

r_full = full_results.get(('qok', 'ch'), {})
print(f"  {'TOTAL':12s}: E2={r_full.get('E2', 0):.3f}, N={r_full.get('N', 0):3d}")

# ─── ot→ot section distribution ─────────────────────────────────────────────

print(f"\n{'='*70}")
print(f"ot→ot SECTION DISTRIBUTION (H447/H448)")
print(f"{'='*70}")

for sec in sections_order:
    if sec not in section_results: continue
    r = section_results[sec].get(('ot', 'ot'), {})
    n_lines = len(section_lines.get(sec, []))
    e2 = r.get('E2', float('nan'))
    n = r.get('N', 0)
    if e2 == e2 and n > 0:
        print(f"  {sec:12s}: E2={e2:.3f}, N={n:3d}, lines={n_lines}")
    elif n_lines > 0:
        print(f"  {sec:12s}: E2=n/a (N=0), lines={n_lines}")

r_full = full_results.get(('ot', 'ot'), {})
print(f"  {'TOTAL':12s}: E2={r_full.get('E2', 0):.3f}, N={r_full.get('N', 0):3d}")

# ─── Summary table ────────────────────────────────────────────────────────────

print(f"\n{'='*70}")
print(f"SUMMARY — Grammar intensity ranking by section (sh→qok + qok→ch E2)")
print(f"{'='*70}")
print(f"  {'Section':12s}  {'sh→qok E2':>10}  {'N_sh_qok':>10}  {'qok→ch E2':>10}  {'N_qok_ch':>10}  {'lines':>6}")
for sec in sections_order:
    if sec not in section_results: continue
    r_sh = section_results[sec].get(('sh', 'qok'), {})
    r_qc = section_results[sec].get(('qok', 'ch'), {})
    e2_sh = r_sh.get('E2', float('nan'))
    e2_qc = r_qc.get('E2', float('nan'))
    n_sh = r_sh.get('N', 0)
    n_qc = r_qc.get('N', 0)
    n_lines = len(section_lines.get(sec, []))
    sh_str = f"{e2_sh:.3f}" if e2_sh == e2_sh else "  n/a"
    qc_str = f"{e2_qc:.3f}" if e2_qc == e2_qc else "  n/a"
    print(f"  {sec:12s}  {sh_str:>10}  {n_sh:>10}  {qc_str:>10}  {n_qc:>10}  {n_lines:>6}")
r_sh = full_results.get(('sh', 'qok'), {})
r_qc = full_results.get(('qok', 'ch'), {})
print(f"  {'TOTAL':12s}  {r_sh.get('E2', 0):>10.3f}  {r_sh.get('N', 0):>10}  {r_qc.get('E2', 0):>10.3f}  {r_qc.get('N', 0):>10}  {len(all_b_lines):>6}")

print(f"\nDone.")
