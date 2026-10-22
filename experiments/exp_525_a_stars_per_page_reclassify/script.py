"""
exp_525: A stars per-page reclassification (H_new_EN)

Current methodology: groups all lines from a folio number (e.g., f57r + f57v = n=57).
When one side is B-dialect and other is A-dialect, combined edy > 5% → excluded from A stars.

This experiment: classify each page name separately (f57r, f57v, f58r, f58v...)
Determines: how many A-dialect pages are recovered in 57-72 range; does A stars expand?
Also: reproduce F503 (o-LF→y@pos1 dir in A stars) and F446 (t-LF elevation) with per-page classification.
Also: explore t-LF within-line grammar in A stars (H_new_EJ).
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSET_PRIORITY = [
    'qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph',
    'd','s','y','k','t','l','r','p','f','o','e','a','n','m'
]

def get_onset(word):
    for onset in ONSET_PRIORITY:
        if word.startswith(onset):
            return onset
    return 'other'

def folio_num(folio):
    m = re.search(r'f(\d+)', folio)
    return int(m.group(1)) if m else None

def is_b_dialect_page(page_lines):
    """Determine if a specific page is B-dialect based on that page's words only."""
    words = [w for ln in page_lines for w in ln]
    if not words:
        return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

def parse_corpus_per_page(path):
    """Parse corpus, keeping pages separate (key = page name like 'f57r')."""
    page_lines = defaultdict(list)  # page_name → [words_list, ...]
    pat = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    for m in pat.finditer(raw):
        folio_raw, _, locus_raw, text = m.groups()
        folio = folio_raw.lstrip('+*=&~')
        lc = locus_raw.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        words = [w for w in re.split(r'[-.\s]', text)
                 if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        n = folio_num(folio)
        if n is None:
            continue
        page_lines[folio].append({'n': n, 'words': words})
    return page_lines

# Also parse with original methodology for comparison
def parse_corpus_by_folio_num(path):
    folio_lines = defaultdict(list)
    pat = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    for m in pat.finditer(raw):
        folio_raw, _, locus_raw, text = m.groups()
        folio = folio_raw.lstrip('+*=&~')
        lc = locus_raw.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        words = [w for w in re.split(r'[-.\s]', text)
                 if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        n = folio_num(folio)
        if n is None:
            continue
        folio_lines[n].append(words)
    return folio_lines

def flag(obs, E):
    if obs >= 10 and E >= 1.5:
        return 'CONF'
    elif obs >= 5 and E >= 2.0:
        return 'dir'
    elif obs >= 3 and E >= 2.5:
        return '(dir)'
    elif E >= 1.0:
        return f'{E:.2f}×'
    else:
        return f'DEPL {E:.2f}×'

print("="*70)
print("PART 1: PER-PAGE vs FOLIO-NUMBER COMPARISON")
print("="*70)

# Original methodology (folio-number grouping)
folio_lines_orig = parse_corpus_by_folio_num(CORPUS)

def is_b_dialect_folio(lines):
    words = [w for ln in lines for w in ln]
    if not words:
        return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

orig_a_stars = {n: ls for n, ls in folio_lines_orig.items()
                if 57 <= n <= 72 and not is_b_dialect_folio(ls)}
orig_a_stars_lines = [ln for ls in orig_a_stars.values() for ln in ls]
print(f"\nOriginal (folio-number grouping) A stars: {len(orig_a_stars)} folios, {len(orig_a_stars_lines)} lines")
for n in sorted(orig_a_stars.keys()):
    lines = orig_a_stars[n]
    words = [w for ln in lines for w in ln]
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    print(f"  n={n}: {len(lines)} lines, edy_rate={edy/len(words):.3f}" if words else f"  n={n}: {len(lines)} lines, no words")

# Per-page methodology
page_lines = parse_corpus_per_page(CORPUS)
print(f"\nPer-page methodology:")
print(f"Total distinct pages in corpus: {len(page_lines)}")

# Classify each page
per_page_a_stars = {}  # page_name → [line_records]
per_page_b_57_72 = {}
per_page_excluded = {}  # pages in 57-72 excluded as B-dialect by folio-num but would be A by page

for page, records in page_lines.items():
    n = records[0]['n'] if records else None
    if n is None:
        continue
    if not (57 <= n <= 72):
        continue
    page_words_lines = [r['words'] for r in records]
    b = is_b_dialect_page(page_words_lines)
    if not b:
        per_page_a_stars[page] = [r['words'] for r in records]
    else:
        per_page_b_57_72[page] = [r['words'] for r in records]

print(f"\nPer-page A stars (57-72, not B-dialect): {len(per_page_a_stars)} pages")
for page in sorted(per_page_a_stars.keys()):
    lines = per_page_a_stars[page]
    words = [w for ln in lines for w in ln]
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    n = folio_num(page)
    in_orig = n in orig_a_stars
    print(f"  {page}: {len(lines)} lines, edy_rate={edy/len(words):.3f} {'[IN ORIG]' if in_orig else '[NEW - recovered]'}" if words else f"  {page}: no words")

per_page_a_stars_lines = [ln for ls in per_page_a_stars.values() for ln in ls]
print(f"\nTotal per-page A stars lines: {len(per_page_a_stars_lines)} (vs {len(orig_a_stars_lines)} original)")

print(f"\nPer-page B-dialect pages in 57-72 range: {sorted(per_page_b_57_72.keys())}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: t-LF in per-page A stars
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 2: t-LF IN PER-PAGE A STARS (H_new_EJ)")
print("="*70)

a_stars_pp_lines = per_page_a_stars_lines
print(f"\nPer-page A stars: {len(a_stars_pp_lines)} lines")

def lf_distribution(lines, label):
    lf_counts = Counter(get_onset(ln[-1]) for ln in lines)
    total = len(lines)
    print(f"\n{label} LF distribution (top 12):")
    for cls, cnt in lf_counts.most_common(12):
        print(f"  {cls}: {cnt} ({100*cnt/total:.1f}%)")
    return lf_counts

lf_dist = lf_distribution(a_stars_pp_lines, "Per-page A stars")

# Compute baselines for per-page A stars
def compute_baselines_from_lines(lines):
    pos1_counts = Counter()
    pos2_counts = Counter()
    pen_counts = Counter()
    for ln in lines:
        if len(ln) >= 2:
            pos1_counts[get_onset(ln[0])] += 1
        if len(ln) >= 3:
            pos2_counts[get_onset(ln[1])] += 1
            pen_counts[get_onset(ln[-2])] += 1
    return {
        'pos1': (pos1_counts, sum(pos1_counts.values())),
        'pos2': (pos2_counts, sum(pos2_counts.values())),
        'pen': (pen_counts, sum(pen_counts.values())),
    }

pp_baselines = compute_baselines_from_lines(a_stars_pp_lines)

def positional_profile_lines(lines, lf_class, baselines, section_label):
    lf_lines = [ln for ln in lines if get_onset(ln[-1]) == lf_class]
    print(f"\n  {section_label} {lf_class}-LF (N_lines={len(lf_lines)}):")
    for pos_name, pos_idx, min_len in [('pos1', 0, 2), ('pos2', 1, 3), ('pen', -2, 3)]:
        elig = [ln for ln in lf_lines if len(ln) >= min_len]
        counts = Counter(get_onset(ln[pos_idx]) for ln in elig)
        base_counts, base_total = baselines[pos_name]
        N_elig = len(elig)
        print(f"\n    {pos_name} (N_elig={N_elig}):")
        if N_elig == 0:
            print("      (no eligible lines)")
            continue
        chain = {'d','qot','ch','o','sh','ok','ot','y','cth','s','k','t',lf_class}
        rows = []
        for cls, obs in counts.most_common(10):
            exp = (base_counts.get(cls, 0) / base_total) * N_elig
            E = obs / exp if exp > 0 else 0.0
            rows.append((cls, obs, exp, E))
        shown = {cls for cls, _, _, _ in rows}
        for cls in chain - shown:
            obs = counts.get(cls, 0)
            exp = (base_counts.get(cls, 0) / base_total) * N_elig
            E = obs / exp if exp > 0 else 0.0
            rows.append((cls, obs, exp, E))
        rows.sort(key=lambda x: -x[3])
        print(f"    {'cls':8} {'obs':>5} {'exp':>6} {'E':>7}  flag")
        seen = set()
        for cls, obs, exp, E in rows:
            if cls in seen: continue
            seen.add(cls)
            print(f"    {cls:8} {obs:>5} {exp:>6.1f} {E:>7.2f}x  {flag(obs, E)}")

# t-LF positional grammar in per-page A stars
positional_profile_lines(a_stars_pp_lines, 't', pp_baselines, 'Per-page A stars')

# Also check o-LF (for F503 reproduction)
print("\n--- o-LF (F503 verification) ---")
positional_profile_lines(a_stars_pp_lines, 'o', pp_baselines, 'Per-page A stars')

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: F446 reproduction — t-LF elevation in A stars
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 3: F446 t-LF ELEVATION REPRODUCTION")
print("="*70)

# F446: A stars t-LF elevation (E=2.12×/N=15) vs A herbal_a baseline
# Compute A herbal_a t-LF rate from original folio-number methodology
orig_a_ha = {n: ls for n, ls in folio_lines_orig.items()
             if n <= 56 and not is_b_dialect_folio(ls)}
a_ha_lines_orig = [ln for ls in orig_a_ha.values() for ln in ls]
a_ha_lf = Counter(get_onset(ln[-1]) for ln in a_ha_lines_orig)
a_ha_t_rate = a_ha_lf.get('t', 0) / len(a_ha_lines_orig)

a_st_pp_lf = Counter(get_onset(ln[-1]) for ln in a_stars_pp_lines)
a_st_pp_t_rate = a_st_pp_lf.get('t', 0) / len(a_stars_pp_lines) if a_stars_pp_lines else 0
a_st_pp_t_count = a_st_pp_lf.get('t', 0)

print(f"\nA herbal_a t-LF rate: {a_ha_lf.get('t',0)}/{len(a_ha_lines_orig)} = {a_ha_t_rate:.3f}")
print(f"Per-page A stars t-LF count: {a_st_pp_t_count}/{len(a_stars_pp_lines)} = {a_st_pp_t_rate:.3f}")
E_t = a_st_pp_t_rate / a_ha_t_rate if a_ha_t_rate > 0 else 0
print(f"Elevation E = {E_t:.2f}× (F446 claimed E=2.12×/N=15)")

# Also compare orig A stars t-LF
orig_a_st_lines = orig_a_stars_lines
orig_a_st_lf = Counter(get_onset(ln[-1]) for ln in orig_a_st_lines)
orig_t_rate = orig_a_st_lf.get('t', 0) / len(orig_a_st_lines) if orig_a_st_lines else 0
print(f"\nOriginal folio-num A stars t-LF count: {orig_a_st_lf.get('t',0)}/{len(orig_a_st_lines)} = {orig_t_rate:.3f}")
print(f"Original E = {orig_t_rate/a_ha_t_rate:.2f}×")

# ─────────────────────────────────────────────────────────────────────────────
# PART 4: Compare per-page and folio-number A stars LF distributions
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 4: LF DISTRIBUTION COMPARISON (folio-num vs per-page)")
print("="*70)

print(f"\n{'LF class':12} {'folio-num':>10} {'per-page':>10} {'E change':>10}")
classes = sorted(set(list(orig_a_st_lf.keys()) + list(a_st_pp_lf.keys())))
for cls in sorted(classes, key=lambda c: -a_st_pp_lf.get(c, 0)):
    orig_n = orig_a_st_lf.get(cls, 0)
    pp_n = a_st_pp_lf.get(cls, 0)
    orig_pct = 100*orig_n/len(orig_a_st_lines) if orig_a_st_lines else 0
    pp_pct = 100*pp_n/len(a_stars_pp_lines) if a_stars_pp_lines else 0
    change = f"{pp_pct-orig_pct:+.1f}pp"
    print(f"  {cls:10} {orig_n:>4}({orig_pct:.1f}%) {pp_n:>4}({pp_pct:.1f}%) {change:>10}")
