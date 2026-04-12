"""
exp_267: H471 — Word Length by Line Position and Onset Class

Question: Does word length vary systematically by line position (LF/MID/LL)?
Does onset class predict word length? Does position within line (word index) correlate with length?

Menzerath's Law: In natural language, longer sentences contain shorter words.
Prediction under copy-buffer model: word length mostly determined by onset+suffix template;
position-dependent length variation should be small.

Metrics:
1. Mean word length by LF/MID/LL for A and B dialect
2. Word length by onset class (which onsets produce long vs short words?)
3. Word length by position within line (word index 0, 1, 2, ...)
4. Word length distribution shape (histogram)
5. Correlation: longer lines → shorter words? (Menzerath test)
"""

import os, re, math
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')

EVA_CHARS = set('acdehiklmnoqrsty')
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

EVA_CHARS_s = set('acdehiklmnoqrsty')

def clean_token(tok):
    tok = re.sub(r'<[^>]+>', '', tok)
    tok = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', tok)
    tok = re.sub(r'\{([^}]*)\}', r'\1', tok)
    tok = re.sub(r'[!?,*\-=@#$%^&|~]', '', tok)
    tok = tok.strip()
    if not tok: return None
    if not all(c in EVA_CHARS_s for c in tok): return None
    return tok

def parse_vms():
    """Return lines of (dialect, [(word, onset, lpos, line_idx, n_words)])."""
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

    records = []  # (dialect, word, onset, lpos, line_pos_idx, line_length)
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>\s*(.*)', line)
            if not m: continue
            folio_raw, lnum_s, ltype, rest = m.group(1), m.group(2), m.group(3), m.group(4)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            lc_stripped = ltype.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            dialect = folio_dialect.get(fb, 'U')
            if dialect not in ('A', 'B'): continue
            raw_tokens = rest.split('.')
            clean = [t for tok in raw_tokens for t in [clean_token(tok)] if t and len(t) >= 2]
            n = len(clean)
            if n == 0: continue
            for idx, word in enumerate(clean):
                if n == 1:   lpos = 'LL'
                elif idx == 0: lpos = 'LF'
                elif idx == n-1: lpos = 'LL'
                else:          lpos = 'MID'
                records.append((dialect, word, get_onset(word), lpos, idx, n))
    return records

# ── Main ─────────────────────────────────────────────────────────────────────

print("Parsing VMS corpus...")
records = parse_vms()
print(f"  Total word records: {len(records)}")

# ── 1. Mean word length by position ──────────────────────────────────────────

print(f"\n{'='*70}")
print("1. MEAN WORD LENGTH BY LINE POSITION AND DIALECT")
print(f"{'='*70}")
print(f"  {'Dialect':>8}  {'Position':>8}  {'N':>8}  {'Mean_len':>10}  {'Std':>7}  {'Median':>8}")
print(f"  {'-'*55}")
for dialect in ('A', 'B'):
    for lpos in ('LF', 'MID', 'LL'):
        ws = [r[1] for r in records if r[0]==dialect and r[3]==lpos]
        if not ws: continue
        lengths = [len(w) for w in ws]
        n = len(lengths)
        mean = sum(lengths)/n
        std = (sum((l-mean)**2 for l in lengths)/n)**0.5
        lengths_s = sorted(lengths)
        median = lengths_s[n//2]
        print(f"  {dialect:>8}  {lpos:>8}  {n:>8}  {mean:>10.3f}  {std:>7.3f}  {median:>8}")

# ── 2. Word length by onset class ─────────────────────────────────────────────

print(f"\n{'='*70}")
print("2. MEAN WORD LENGTH BY ONSET CLASS (ALL POSITIONS POOLED)")
print(f"{'='*70}")
print(f"  {'Onset':>8}  {'N_A':>6}  {'Len_A':>7}  {'N_B':>6}  {'Len_B':>7}")
print(f"  {'-'*40}")
onset_lengths_a = defaultdict(list)
onset_lengths_b = defaultdict(list)
for dialect, word, onset, lpos, idx, n in records:
    if dialect == 'A': onset_lengths_a[onset].append(len(word))
    elif dialect == 'B': onset_lengths_b[onset].append(len(word))
# Sort by A-dialect mean length
onsets_sorted = sorted(onset_lengths_a.keys(),
                       key=lambda o: sum(onset_lengths_a[o])/len(onset_lengths_a[o]) if onset_lengths_a[o] else 0)
for onset in onsets_sorted:
    la = onset_lengths_a[onset]; lb = onset_lengths_b.get(onset, [])
    na = len(la); nb = len(lb)
    if na < 10: continue
    mla = sum(la)/na; mlb = sum(lb)/nb if nb > 0 else float('nan')
    print(f"  {onset:>8}  {na:>6}  {mla:>7.3f}  {nb:>6}  {mlb:>7.3f}")

# ── 3. Word length by position within line (word index) ──────────────────────

print(f"\n{'='*70}")
print("3. MEAN WORD LENGTH BY WORD INDEX IN LINE (0=LF, ...)")
print(f"{'='*70}")
print(f"  {'Index':>6}  {'N_A':>6}  {'Len_A':>7}  {'N_B':>6}  {'Len_B':>7}")
print(f"  {'-'*40}")
idx_lengths_a = defaultdict(list)
idx_lengths_b = defaultdict(list)
for dialect, word, onset, lpos, idx, n in records:
    if dialect == 'A': idx_lengths_a[idx].append(len(word))
    elif dialect == 'B': idx_lengths_b[idx].append(len(word))
for idx in range(10):
    la = idx_lengths_a[idx]; lb = idx_lengths_b.get(idx, [])
    na = len(la); nb = len(lb)
    if na < 100: continue
    mla = sum(la)/na; mlb = sum(lb)/nb if nb > 0 else float('nan')
    lb_s = f'{mlb:7.3f}' if mlb==mlb else '    n/a'
    print(f"  {idx:>6}  {na:>6}  {mla:>7.3f}  {nb:>6}  {lb_s}")

# ── 4. Word length distribution (histogram) ──────────────────────────────────

print(f"\n{'='*70}")
print("4. WORD LENGTH DISTRIBUTION (HISTOGRAM)")
print(f"{'='*70}")
len_a = [len(r[1]) for r in records if r[0]=='A']
len_b = [len(r[1]) for r in records if r[0]=='B']
cnt_a = Counter(len_a); cnt_b = Counter(len_b)
print(f"  A-dialect: mean={sum(len_a)/len(len_a):.3f}, N={len(len_a)}")
print(f"  B-dialect: mean={sum(len_b)/len(len_b):.3f}, N={len(len_b)}")
print(f"\n  {'Length':>8}  {'N_A':>7}  {'%_A':>7}  {'N_B':>7}  {'%_B':>7}")
for l in range(2, 16):
    na = cnt_a.get(l, 0); nb = cnt_b.get(l, 0)
    pct_a = 100*na/len(len_a); pct_b = 100*nb/len(len_b)
    bar_a = '#'*int(pct_a*2); bar_b = '#'*int(pct_b*2)
    print(f"  {l:>8}  {na:>7}  {pct_a:>7.2f}% {bar_a}")

# ── 5. Menzerath test: line length vs mean word length ────────────────────────

print(f"\n{'='*70}")
print("5. MENZERATH TEST: DOES LINE LENGTH PREDICT WORD LENGTH?")
print(f"{'='*70}")
# Compute mean word length per line
line_stats_a = []  # (line_length, mean_word_length)
line_stats_b = []
by_line = defaultdict(lambda: {'n': 0, 'total_len': 0})

# Reconstruct lines
folio_word_stats2 = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
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
            folio_word_stats2[fb]['total'] += 1
            if w.endswith('eedy'): folio_word_stats2[fb]['eedy'] += 1
            elif w.endswith('edy'): folio_word_stats2[fb]['edy'] += 1
folio_dialect2 = {fb: classify_dialect(stats) for fb, stats in folio_word_stats2.items()}

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for raw in f:
        line = raw.strip()
        if not line or line.startswith('#'): continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>\s*(.*)', line)
        if not m: continue
        folio_raw, lnum_s, ltype, rest = m.group(1), m.group(2), m.group(3), m.group(4)
        folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
        lc_stripped = ltype.lstrip('+*=/~&')
        if not lc_stripped.lstrip('@').startswith('P'): continue
        dialect = folio_dialect2.get(fb, 'U')
        if dialect not in ('A', 'B'): continue
        raw_tokens = rest.split('.')
        clean = [t for tok in raw_tokens for t in [clean_token(tok)] if t and len(t) >= 2]
        n = len(clean)
        if n < 2: continue
        mean_len = sum(len(w) for w in clean) / n
        if dialect == 'A': line_stats_a.append((n, mean_len))
        else: line_stats_b.append((n, mean_len))

def pearson_r(xs, ys):
    n = len(xs)
    if n < 3: return float('nan')
    mx = sum(xs)/n; my = sum(ys)/n
    num = sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
    den_x = sum((x-mx)**2 for x in xs)**0.5
    den_y = sum((y-my)**2 for y in ys)**0.5
    return num/(den_x*den_y) if den_x*den_y > 0 else float('nan')

r_a = pearson_r([s[0] for s in line_stats_a], [s[1] for s in line_stats_a])
r_b = pearson_r([s[0] for s in line_stats_b], [s[1] for s in line_stats_b])
print(f"\n  A-dialect: r(line_length, mean_word_length) = {r_a:.4f} (N={len(line_stats_a)} lines)")
print(f"  B-dialect: r(line_length, mean_word_length) = {r_b:.4f} (N={len(line_stats_b)} lines)")
print(f"\n  Menzerath's Law prediction: negative correlation (r < 0)")
print(f"  A: {'CONSISTENT' if r_a < -0.1 else 'INCONSISTENT'} with Menzerath's Law (r={r_a:.3f})")
print(f"  B: {'CONSISTENT' if r_b < -0.1 else 'INCONSISTENT'} with Menzerath's Law (r={r_b:.3f})")

# Mean word length by line length bucket
print(f"\n  Mean word length by line length bucket:")
print(f"  {'LinLen':>8}  {'N_A':>6}  {'MeanLen_A':>10}  {'N_B':>6}  {'MeanLen_B':>10}")
from collections import defaultdict
bucket_a = defaultdict(list); bucket_b = defaultdict(list)
for (ll, ml) in line_stats_a: bucket_a[ll].append(ml)
for (ll, ml) in line_stats_b: bucket_b[ll].append(ml)
for ll in sorted(set(bucket_a) | set(bucket_b)):
    if ll < 2 or ll > 15: continue
    la = bucket_a[ll]; lb = bucket_b[ll]
    na = len(la); nb = len(lb)
    if na < 5 and nb < 5: continue
    mla = sum(la)/na if na > 0 else float('nan')
    mlb = sum(lb)/nb if nb > 0 else float('nan')
    mla_s = f'{mla:10.3f}' if mla==mla else '         n/a'
    mlb_s = f'{mlb:10.3f}' if mlb==mlb else '         n/a'
    print(f"  {ll:>8}  {na:>6}  {mla_s}  {nb:>6}  {mlb_s}")

# ── 6. Latin comparison ───────────────────────────────────────────────────────

print(f"\n{'='*70}")
print("6. LATIN COMPARISON: WORD LENGTH DISTRIBUTION")
print(f"{'='*70}")
with open(LATIN_CORPUS, encoding='utf-8', errors='replace') as f:
    latin_text = f.read()
latin_words = re.findall(r'\b[a-zA-Z]{2,}\b', latin_text)
latin_lens = [len(w) for w in latin_words]
cnt_lat = Counter(latin_lens)
print(f"  Latin: mean={sum(latin_lens)/len(latin_lens):.3f}, N={len(latin_lens)}")
print(f"\n  {'Length':>8}  {'VMS_A%':>8}  {'VMS_B%':>8}  {'Latin%':>8}")
for l in range(2, 14):
    pa = 100*cnt_a.get(l,0)/len(len_a); pb = 100*cnt_b.get(l,0)/len(len_b)
    pl = 100*cnt_lat.get(l,0)/len(latin_lens)
    print(f"  {l:>8}  {pa:>8.2f}  {pb:>8.2f}  {pl:>8.2f}")

print(f"\nDone.")
