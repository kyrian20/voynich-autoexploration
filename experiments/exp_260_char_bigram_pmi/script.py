"""
exp_260: H463 — Character Bigram PMI Analysis

Question: Which consecutive character pairs within VMS words have highest PMI
(pointwise mutual information)? Do they correspond to known onset/suffix templates?

PMI(c_i, c_{i+1}) = log2(P(c_i, c_{i+1}) / (P(c_i) * P(c_{i+1})))

Analysis:
1. Compute PMI for all within-word character bigrams: VMS A, VMS B, Latin
2. Rank by PMI descending
3. Compare A vs B top-PMI bigrams (dialect-specific suffix/onset templates)
4. Also: compute NEGATIVE PMI (depleted bigrams — avoidances)
5. Mutual information as sum: I(C_i; C_{i+1}) = sum P(x,y) * PMI(x,y)

Uses same corpus parsing as exp_259.
"""

import os, re, math
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')

EVA_CHARS = set('acdehiklmnoqrsty')

# ── corpus parsing (same as exp_259) ─────────────────────────────────────────

def clean_token(tok):
    tok = re.sub(r'<[^>]*>', '', tok)
    tok = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', tok)
    tok = re.sub(r'\{([^}]*)\}', r'\1', tok)
    tok = re.sub(r'[!?,*\-=@#$%^&|~]', '', tok)
    tok = tok.strip()
    if not tok: return None
    if not all(c in EVA_CHARS for c in tok): return None
    return tok

def get_dialect(folio_tag):
    base = re.sub(r'[a-z]', '', folio_tag)
    try:
        fnum = int(base)
    except:
        return 'U'
    for lo, hi in [(75, 86), (103, 117)]:
        if lo <= fnum <= hi: return 'B'
    for lo, hi in [(1, 57), (87, 102)]:
        if lo <= fnum <= hi: return 'A'
    return 'U'

def parse_vms(path):
    words_a, words_b = [], []
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'^<f(\S+?)\.(\d+),([^>]+)>\s*(.*)', line)
            if not m: continue
            folio_tag, rest = m.group(1), m.group(4)
            dialect = get_dialect(folio_tag)
            for tok in rest.split('.'):
                ctok = clean_token(tok)
                if ctok and len(ctok) >= 2:
                    if dialect == 'A': words_a.append(ctok)
                    elif dialect == 'B': words_b.append(ctok)
    return words_a, words_b

def parse_latin(path):
    words = []
    with open(path) as f:
        for line in f:
            for tok in re.findall(r'[a-zA-Z]+', line):
                if len(tok) >= 2:
                    words.append(tok.lower())
    return words

# ── PMI computation ───────────────────────────────────────────────────────────

def compute_pmi(words, char_filter=None, min_count=10):
    """
    Compute PMI for all within-word character bigrams.
    char_filter: set of valid chars (None = all)
    min_count: minimum bigram count to include in output
    Returns: (pmi_dict, unigram_counts, bigram_counts, total_bigrams)
    """
    uni = Counter()  # character counts
    bi  = Counter()  # bigram (prev, cur) counts

    for w in words:
        chars = list(w)
        for i, c in enumerate(chars):
            if char_filter and c not in char_filter: continue
            uni[c] += 1
            if i > 0:
                prev = chars[i-1]
                if char_filter and prev not in char_filter: continue
                bi[(prev, c)] += 1

    total_uni = sum(uni.values())
    total_bi  = sum(bi.values())

    pmi = {}
    for (x, y), cnt in bi.items():
        if cnt < min_count: continue
        p_xy = cnt / total_bi
        p_x  = uni[x] / total_uni
        p_y  = uni[y] / total_uni
        if p_x > 0 and p_y > 0:
            pmi[(x, y)] = math.log2(p_xy / (p_x * p_y))

    # Also compute mutual information
    mi = sum((bi[(x,y)]/total_bi) * pmi[(x,y)]
             for (x,y) in pmi)

    return pmi, uni, bi, total_bi, mi

def print_pmi_table(pmi_dict, bi_counts, total_bi, n=25, label=""):
    ranked = sorted(pmi_dict.items(), key=lambda kv: kv[1], reverse=True)
    print(f"\n  Top {n} enriched bigrams ({label}):")
    print(f"  {'Bigram':>8}  {'PMI':>6}  {'Count':>7}  {'P(xy)':>8}  {'Meaning'}")
    for (x, y), pmi in ranked[:n]:
        cnt = bi_counts[(x, y)]
        p_xy = cnt / total_bi
        print(f"  {x+y:>8}  {pmi:>6.3f}  {cnt:>7d}  {p_xy:>8.5f}  {interpret_bigram(x, y)}")

    print(f"\n  Bottom {n} depleted bigrams ({label}):")
    print(f"  {'Bigram':>8}  {'PMI':>6}  {'Count':>7}")
    for (x, y), pmi in ranked[-n:]:
        cnt = bi_counts[(x, y)]
        print(f"  {x+y:>8}  {pmi:>6.3f}  {cnt:>7d}")

def interpret_bigram(x, y):
    """Quick human-readable label for known EVA bigrams."""
    bigram = x + y
    known = {
        'qo': 'qo- onset prefix',
        'ch': 'ch onset/gallows',
        'sh': 'sh onset/gallows',
        'ct': 'cth onset (part)',
        'th': 'cth onset (part)',
        'ai': 'aiin suffix (part)',
        'ii': 'aiin suffix (part)',
        'in': 'aiin suffix (part)',
        'ck': 'ckh onset (part)',
        'kh': 'ckh onset (part)',
        'dy': '-edy suffix end',
        'ed': '-edy suffix start',
        'ee': '-eedy/-eey pattern',
        'ey': '-eey suffix',
        'ol': '-ol suffix',
        'or': '-or suffix',
        'oa': 'o+a combination',
        'ok': 'ok onset',
        'ot': 'ot onset',
    }
    return known.get(bigram, '')

# ── dialect comparison ────────────────────────────────────────────────────────

def top_dialect_diff(pmi_a, pmi_b, n=15):
    """Find bigrams where A and B PMI differ most."""
    all_bigrams = set(pmi_a.keys()) | set(pmi_b.keys())
    diffs = []
    for bg in all_bigrams:
        pa = pmi_a.get(bg, float('nan'))
        pb = pmi_b.get(bg, float('nan'))
        if math.isnan(pa) or math.isnan(pb): continue
        diffs.append((bg, pa, pb, pa - pb))
    diffs.sort(key=lambda x: abs(x[3]), reverse=True)
    print(f"\n  Top A vs B PMI differences (A PMI - B PMI):")
    print(f"  {'Bigram':>8}  {'PMI_A':>7}  {'PMI_B':>7}  {'Δ':>7}  {'Meaning'}")
    for (x,y), pa, pb, delta in diffs[:n]:
        print(f"  {x+y:>8}  {pa:>7.3f}  {pb:>7.3f}  {delta:>+7.3f}  {interpret_bigram(x, y)}")

# ── position-stratified PMI (first-half vs second-half of word) ───────────────

def pmi_by_word_half(words, char_filter=None, min_count=5):
    """Separate PMI for bigrams in first half vs second half of words."""
    bi_first = Counter()  # bigrams in positions 0..floor(len/2)-1
    bi_last  = Counter()  # bigrams in positions floor(len/2)..end
    uni_first = Counter()
    uni_last  = Counter()

    for w in words:
        chars = list(w)
        L = len(chars)
        mid = L // 2
        for i, c in enumerate(chars):
            if char_filter and c not in char_filter: continue
            if i < mid:
                uni_first[c] += 1
                if i > 0 and (not char_filter or chars[i-1] in char_filter):
                    bi_first[(chars[i-1], c)] += 1
            else:
                uni_last[c] += 1
                if i > 0 and i == mid and (not char_filter or chars[i-1] in char_filter):
                    pass  # skip cross-boundary
                elif i > max(1, mid) and (not char_filter or chars[i-1] in char_filter):
                    bi_last[(chars[i-1], c)] += 1

    def compute_local_pmi(bi, uni, min_cnt):
        total_bi  = sum(bi.values())
        total_uni = sum(uni.values())
        if total_bi == 0: return {}
        result = {}
        for (x, y), cnt in bi.items():
            if cnt < min_cnt: continue
            p_xy = cnt / total_bi
            p_x  = uni[x] / total_uni
            p_y  = uni[y] / total_uni
            if p_x > 0 and p_y > 0:
                result[(x,y)] = math.log2(p_xy / (p_x * p_y))
        return result

    pmi_f = compute_local_pmi(bi_first, uni_first, min_count)
    pmi_l = compute_local_pmi(bi_last, uni_last, min_count)
    return pmi_f, pmi_l

# ── main ──────────────────────────────────────────────────────────────────────

print("Parsing VMS corpus...")
words_a, words_b = parse_vms(DATA_PATH)
print(f"  A-dialect: {len(words_a)} tokens  B-dialect: {len(words_b)} tokens")

print("Parsing Latin corpus...")
words_lat = parse_latin(LATIN_CORPUS)
print(f"  Latin: {len(words_lat)} tokens")

MIN_COUNT = 20  # minimum bigram count for PMI inclusion

pmi_a, uni_a, bi_a, tot_a, mi_a = compute_pmi(words_a, EVA_CHARS, MIN_COUNT)
pmi_b, uni_b, bi_b, tot_b, mi_b = compute_pmi(words_b, EVA_CHARS, MIN_COUNT)
pmi_l, uni_l, bi_l, tot_l, mi_l = compute_pmi(words_lat, None, MIN_COUNT)

print(f"\n{'='*80}")
print("MUTUAL INFORMATION SUMMARY")
print(f"{'='*80}")
print(f"  A-dialect: I(c_i; c_{{i+1}}) = {mi_a:.4f} bits  (N_bigrams={tot_a:,})")
print(f"  B-dialect: I(c_i; c_{{i+1}}) = {mi_b:.4f} bits  (N_bigrams={tot_b:,})")
print(f"  Latin:     I(c_i; c_{{i+1}}) = {mi_l:.4f} bits  (N_bigrams={tot_l:,})")
print(f"\n  Reference: H_max(16 EVA) = 4.000 bits, H_max(23 Latin) = 4.524 bits")
print(f"  Interpretation: higher MI = characters more predictable from each other")

print(f"\n{'='*80}")
print("A-DIALECT: TOP PMI CHARACTER BIGRAMS")
print(f"{'='*80}")
print_pmi_table(pmi_a, bi_a, tot_a, n=20, label="VMS A-dialect")

print(f"\n{'='*80}")
print("B-DIALECT: TOP PMI CHARACTER BIGRAMS")
print(f"{'='*80}")
print_pmi_table(pmi_b, bi_b, tot_b, n=20, label="VMS B-dialect")

print(f"\n{'='*80}")
print("LATIN: TOP PMI CHARACTER BIGRAMS")
print(f"{'='*80}")
print_pmi_table(pmi_l, bi_l, tot_l, n=20, label="Latin (Cicero)")

print(f"\n{'='*80}")
print("DIALECT COMPARISON: A vs B PMI DIFFERENCES")
print(f"{'='*80}")
top_dialect_diff(pmi_a, pmi_b, n=20)

# ── word-half analysis ────────────────────────────────────────────────────────

print(f"\n{'='*80}")
print("WORD HALF ANALYSIS: ONSET ZONE vs SUFFIX ZONE PMI")
print(f"{'='*80}")

pmi_af, pmi_al = pmi_by_word_half(words_a, EVA_CHARS, min_count=10)
pmi_bf, pmi_bl = pmi_by_word_half(words_b, EVA_CHARS, min_count=10)

def top_n(pmi_dict, n=12):
    return sorted(pmi_dict.items(), key=lambda kv: kv[1], reverse=True)[:n]

print("\n  A-dialect ONSET ZONE (first half) top bigrams:")
for (x,y), pmi in top_n(pmi_af, 12):
    print(f"    {x+y}: PMI={pmi:.3f}  {interpret_bigram(x,y)}")

print("\n  A-dialect SUFFIX ZONE (second half) top bigrams:")
for (x,y), pmi in top_n(pmi_al, 12):
    print(f"    {x+y}: PMI={pmi:.3f}  {interpret_bigram(x,y)}")

print("\n  B-dialect ONSET ZONE (first half) top bigrams:")
for (x,y), pmi in top_n(pmi_bf, 12):
    print(f"    {x+y}: PMI={pmi:.3f}  {interpret_bigram(x,y)}")

print("\n  B-dialect SUFFIX ZONE (second half) top bigrams:")
for (x,y), pmi in top_n(pmi_bl, 12):
    print(f"    {x+y}: PMI={pmi:.3f}  {interpret_bigram(x,y)}")

# ── character unigram frequency table ────────────────────────────────────────

print(f"\n{'='*80}")
print("CHARACTER FREQUENCY TABLE")
print(f"{'='*80}")
total_a = sum(uni_a.values())
total_b = sum(uni_b.values())
total_l = sum(uni_l.values())
print(f"{'Char':>5}  {'A %':>6}  {'B %':>6}  {'Lat %':>7}")
all_chars = sorted(set(uni_a.keys()) | set(uni_b.keys()))
for c in all_chars:
    pa = uni_a.get(c, 0) / total_a * 100 if total_a > 0 else 0
    pb = uni_b.get(c, 0) / total_b * 100 if total_b > 0 else 0
    pl = uni_l.get(c, 0) / total_l * 100 if total_l > 0 else 0
    print(f"  {c:>4}  {pa:>6.2f}  {pb:>6.2f}  {pl:>7.3f}")

print("\nDone.")
