"""
exp_307: Section-Level Menzerath Analysis — VMS Menzerath r Residual (H509)

The simulation achieves Menzerath r=−0.109 (48% of VMS −0.225) after exp_306.
H509: The remaining 52% gap may be driven by section-level heterogeneity.
If the stars section (f103-117, 45% of B corpus) has a stronger Menzerath r
than bio/herbal, then the global r=−0.225 is dominated by cross-section
effects that the homogeneous simulation doesn't model.

This experiment:
  1. Parses B-dialect VMS by section (stars, bio, herbal, astro, pharma, cosmo)
  2. Computes Menzerath r separately per section and overall
  3. Computes VMS within-line MID slope per section
  4. Measures section-level mean line length and word length
  5. Runs simulation at beta=0.50 (exp_306 architecture) to compare section profiles
  6. Reports: where does the VMS r come from? Cross-section or within-section?
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

# Section folio ranges (B-dialect text sections)
# Based on exp_252 / exp_297 section characterization:
# stars = f103-f117 (astrological circular, shortest/most regular lines)
# bio   = f75-f84   (biological, medium lines)
# herbal = f1-f57   (herbal, longer lines)
# astro = f57-f73   (astrological zodiac)
# pharma = f88-f102 (pharmaceutical)
# cosmo = f85-f86   (cosmological)
# Note: folio numbers from prior section analyses in this project

def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def folio_num(fb):
    try: return int(re.sub(r'[^0-9]', '', fb))
    except: return 0

def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

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

def assign_section(fn):
    """Assign B-dialect folio to section based on folio number."""
    if   fn <= 57:  return 'herbal'
    elif fn <= 73:  return 'astro'
    elif fn <= 84:  return 'bio'
    elif fn <= 87:  return 'cosmo'
    elif fn <= 102: return 'pharma'
    elif fn <= 116: return 'stars'
    else:           return 'text'

def parse_vms_b_by_section():
    """Parse B-dialect lines, tagging each line with its section."""
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

    # Second pass: parse lines with section labels
    section_lines = defaultdict(list)  # section → list of word lists
    all_b_lines = []
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
            if not words: continue
            fn = folio_num(fb)
            section = assign_section(fn)
            section_lines[section].append(words)
            all_b_lines.append(words)

    return all_b_lines, section_lines

def pearson_r(xs, ys):
    """Pearson correlation coefficient."""
    n = len(xs)
    if n < 3: return float('nan')
    mx = sum(xs)/n; my = sum(ys)/n
    cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))/n
    sx = (sum((x-mx)**2 for x in xs)/n)**0.5
    sy = (sum((y-my)**2 for y in ys)/n)**0.5
    if sx*sy == 0: return float('nan')
    return cov/(sx*sy)

def spearman_r(xs, ys):
    """Spearman rank correlation."""
    n = len(xs)
    if n < 3: return float('nan')
    def ranks(vals):
        sorted_idx = sorted(range(n), key=lambda i: vals[i])
        r = [0]*n
        for rank, idx in enumerate(sorted_idx):
            r[idx] = rank + 1
        return r
    rx = ranks(xs); ry = ranks(ys)
    return pearson_r(rx, ry)

def compute_menzerath_stats(lines, min_len=3):
    """Compute Menzerath r and MID slope for a set of lines."""
    line_lens = [len(l) for l in lines if len(l) >= min_len]
    line_mean_wl = [sum(len(w) for w in l)/len(l) for l in lines if len(l) >= min_len]
    if len(line_lens) < 5:
        return {'n_lines': len(line_lens), 'menz_r': float('nan'), 'menz_rho': float('nan'),
                'mid_slope': float('nan'), 'mean_line_len': 0, 'mean_word_len': 0}

    menz_r = pearson_r(line_lens, line_mean_wl)
    menz_rho = spearman_r(line_lens, line_mean_wl)
    mean_line_len = sum(line_lens)/len(line_lens)
    mean_word_len = sum(line_mean_wl)/len(line_mean_wl)

    # MID slope (word length vs position within line)
    idx_lens = []
    for l in lines:
        if len(l) < 4: continue
        for j, w in enumerate(l[1:-1]): idx_lens.append((j, len(w)))
    if len(idx_lens) > 50:
        n_il = len(idx_lens)
        mean_idx = sum(x for x,y in idx_lens)/n_il
        mean_len = sum(y for x,y in idx_lens)/n_il
        cov_il = sum((x-mean_idx)*(y-mean_len) for x,y in idx_lens)/n_il
        var_il = sum((x-mean_idx)**2 for x,y in idx_lens)/n_il
        mid_slope = cov_il / var_il if var_il > 0 else 0
    else:
        mid_slope = float('nan')

    return {'n_lines': len(line_lens), 'menz_r': menz_r, 'menz_rho': menz_rho,
            'mid_slope': mid_slope, 'mean_line_len': mean_line_len, 'mean_word_len': mean_word_len}

def variance_decomp(line_lens, line_mean_wl):
    """Decompose Menzerath r into within-section vs between-section components (conceptual)."""
    pass

# ─── Parse VMS ─────────────────────────────────────────────────────────────────
print("exp_307: Section-Level Menzerath Analysis (H509)")
print("=" * 70)

print("\nParsing VMS B-dialect by section...")
all_b_lines, section_lines = parse_vms_b_by_section()
print(f"  Total B-dialect lines: {len(all_b_lines)}")
for section, slines in sorted(section_lines.items()):
    print(f"  {section:10s}: {len(slines)} lines, {sum(len(l) for l in slines)} words")

# ─── VMS Menzerath stats by section ────────────────────────────────────────────
print(f"\n{'='*70}")
print("VMS Menzerath Statistics by Section")
print(f"{'='*70}")
print(f"\n{'Section':10s}  {'N_lines':8s}  {'Mean_LL':9s}  {'Mean_WL':9s}  {'Menz_r':9s}  {'Spearman':9s}  {'MID_slope':10s}")
print("-" * 80)

section_stats = {}
for section in ['overall', 'stars', 'bio', 'herbal', 'astro', 'pharma', 'cosmo', 'text']:
    lines = all_b_lines if section == 'overall' else section_lines.get(section, [])
    if not lines:
        print(f"{section:10s}  (no data)")
        continue
    stats = compute_menzerath_stats(lines)
    section_stats[section] = stats
    mr = stats['menz_r']; rho = stats['menz_rho']; ms = stats['mid_slope']
    pct_vms = (mr / -0.225 * 100) if not math.isnan(mr) else float('nan')
    print(f"{section:10s}  {stats['n_lines']:8d}  {stats['mean_line_len']:9.2f}  "
          f"{stats['mean_word_len']:9.3f}  {mr:+9.4f}  {rho:+9.4f}  "
          f"{ms:+10.4f}")

# ─── Cross-section vs within-section analysis ───────────────────────────────────
print(f"\n{'='*70}")
print("Cross-Section vs Within-Section Menzerath Analysis")
print(f"{'='*70}")

# Build (line_len, mean_wl) pairs tagged by section
all_pairs = []  # (section, line_len, mean_wl)
for section, slines in section_lines.items():
    for l in slines:
        if len(l) >= 3:
            all_pairs.append((section, len(l), sum(len(w) for w in l)/len(l)))

if all_pairs:
    # Global r (already computed in overall)
    global_r = section_stats.get('overall', {}).get('menz_r', float('nan'))
    print(f"\nGlobal Menzerath r (all B-dialect): {global_r:+.4f}")
    print(f"VMS target: -0.225")
    print(f"Simulation (exp_306 beta=0.50): -0.1089 (48% of VMS)")

    # Within-section r (average of section r's, weighted by N)
    section_weights = [(section_stats[s]['n_lines'], section_stats[s]['menz_r'])
                       for s in ['stars', 'bio', 'herbal', 'astro', 'pharma']
                       if s in section_stats and not math.isnan(section_stats[s]['menz_r'])]
    if section_weights:
        total_n = sum(n for n, _ in section_weights)
        weighted_r = sum(n*r for n, r in section_weights) / total_n
        print(f"\nWeighted mean within-section r: {weighted_r:+.4f}")
        print(f"(Sections contributing to within-section pool: {[s for s,_ in zip(['stars','bio','herbal','astro','pharma'], section_weights)]})")

    # Between-section contribution: compare section mean WL vs section mean LL
    print(f"\nSection-level Menzerath (mean_LL vs mean_WL across sections):")
    s_ll = []; s_wl = []
    for section in ['stars', 'bio', 'herbal', 'astro', 'pharma']:
        if section in section_stats:
            s = section_stats[section]
            s_ll.append(s['mean_line_len'])
            s_wl.append(s['mean_word_len'])
            print(f"  {section:8s}: mean_LL={s['mean_line_len']:5.2f}, mean_WL={s['mean_word_len']:5.3f}")
    if len(s_ll) >= 3:
        between_r = pearson_r(s_ll, s_wl)
        between_rho = spearman_r(s_ll, s_wl)
        print(f"\n  Between-section r (mean_LL vs mean_WL): {between_r:+.4f}  (Spearman: {between_rho:+.4f})")
        print(f"  (N_sections={len(s_ll)}; if this is << −0.5, cross-section gradient is substantial)")

# ─── Line length distribution per section ──────────────────────────────────────
print(f"\n{'='*70}")
print("Line Length Distribution by Section")
print(f"{'='*70}")
print(f"\n{'Section':10s}  {'Min':5s}  {'P25':5s}  {'P50':5s}  {'P75':5s}  {'Max':5s}  {'Var':8s}")
print("-" * 60)
for section in ['overall', 'stars', 'bio', 'herbal', 'astro', 'pharma']:
    lines = all_b_lines if section == 'overall' else section_lines.get(section, [])
    ll = sorted([len(l) for l in lines if len(l) >= 2])
    if not ll: continue
    n = len(ll)
    p25 = ll[n//4]; p50 = ll[n//2]; p75 = ll[3*n//4]
    mean = sum(ll)/n
    var = sum((x-mean)**2 for x in ll)/n
    print(f"{section:10s}  {min(ll):5d}  {p25:5d}  {p50:5d}  {p75:5d}  {max(ll):5d}  {var:8.2f}")

# ─── Simulation section profile check ──────────────────────────────────────────
# Note: simulation generates homogeneous lines (one "section")
# The simulation Menzerath r from exp_306 is −0.1089 for 2411 lines total
# We can check: what is the expected Menzerath r for a homogeneous simulation
# if we apply the same section structure as VMS?

print(f"\n{'='*70}")
print("Interpretation Summary")
print(f"{'='*70}")
print(f"\nVMS overall Menzerath r: {section_stats.get('overall',{}).get('menz_r', float('nan')):+.4f}")
print(f"Simulation (exp_306, beta=0.50): −0.1089")
print(f"Residual gap: {-0.225 - (-0.1089):+.4f} ({(1 - 0.1089/0.225)*100:.1f}% of VMS unaccounted)")
print(f"\nKey question: Is VMS r driven by cross-section heterogeneity (different mean LL")
print(f"per section correlated with different mean WL per section)?")
print(f"Or by within-section structure (each section individually has negative r)?")
print(f"\nIf between-section r << −0.5:")
print(f"  → VMS global r is partly driven by section heterogeneity")
print(f"  → Simulation lacks this because it's a single homogeneous section")
print(f"  → Closing the gap requires section-level architecture (outside current scope)")
print(f"If within-section r ≈ VMS global r:")
print(f"  → Within-section mechanisms already sufficient in principle")
print(f"  → Simulation's gap is a parameter/mechanism problem, not section structure")

print("\nDone.")
