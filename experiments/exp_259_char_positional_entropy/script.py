"""
exp_259: H449 — Positional Entropy of EVA Characters Within Words

Question: Does Shannon entropy h(c_i) vary by character position i within VMS words?
Does the entropy profile differ between A- and B-dialect, and between VMS and Latin?

Hypotheses:
- Natural language: low-high-low entropy profile (onset constrained, midfix free, suffix constrained)
- If VMS is a hoax: near-uniform profile (no structural constraint at boundaries)
- Copy-buffer/glossographic: profile should reflect onset/suffix template structure

Analysis:
1. h(c_i): entropy of character at position i (marginally, over all words of length > i)
2. h(c_i | c_{i-1}): conditional entropy at position i given previous character
3. Separate A-dialect, B-dialect, and Latin comparison
4. Also compute: fraction of mass at positions 0..4 (onset zone) and last 3 (suffix zone)

Character set: EVA ASCII characters (a c d e h i k l m n o q r s t y)
Words filtered: all VMS words (labels excluded); minimum frequency ≥ 2 to reduce noise
"""
from pathlib import Path as _RepositoryPath

import os, re, math
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')

EVA_CHARS = set('acdehiklmnoqrsty')

# ── corpus parsing ────────────────────────────────────────────────────────────

def clean_token(tok):
    """Strip transcription special markers and return clean EVA string (or None)."""
    # Remove inline annotations: <%>, <$>, <!...>, <*>
    tok = re.sub(r'<[^>]*>', '', tok)
    # Uncertain readings [x:y] → take x
    tok = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', tok)
    # Partially legible {abc} → abc
    tok = re.sub(r'\{([^}]*)\}', r'\1', tok)
    # Remove wildcards and punctuation used in transcription
    tok = re.sub(r'[!?,*\-=@#$%^&|~]', '', tok)
    tok = tok.strip()
    if not tok: return None
    # Must consist only of valid EVA chars
    if not all(c in EVA_CHARS for c in tok): return None
    return tok

def parse_vms(path):
    """Return list of (folio, ltype, dialect, position_in_line, word)."""
    records = []
    cur_folio = None
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'): continue
            # folio header: <f1r> or <f1r> <! ...>
            m = re.match(r'^<(f\S+?)>', line)
            if m and ',' not in m.group(1):
                cur_folio = m.group(1)  # e.g. 'f1r'
                continue
            # data line: <f1r.1,@P0>   words.separated.by.dots
            m = re.match(r'^<f(\S+?)\.(\d+),([^>]+)>\s*(.*)', line)
            if not m: continue
            folio_tag, lnum_s, ltype, rest = m.group(1), m.group(2), m.group(3), m.group(4)
            cur_folio = 'f' + folio_tag
            # Split on '.' to get word tokens
            raw_tokens = rest.split('.')
            # Collect clean tokens
            clean = []
            for tok in raw_tokens:
                ctok = clean_token(tok)
                if ctok and len(ctok) >= 2:  # minimum word length 2
                    clean.append(ctok)
            n = len(clean)
            if n == 0: continue
            dialect = get_dialect(folio_tag, ltype)
            for idx, tok in enumerate(clean):
                if n == 1:
                    pos = 'LL'
                elif idx == 0:
                    pos = 'LF'
                elif idx == n - 1:
                    pos = 'LL'
                else:
                    pos = 'MID'
                records.append((cur_folio, ltype, dialect, pos, tok))
    return records

def get_dialect(folio, ltype):
    """Return 'A' or 'B' dialect based on folio assignment from F037."""
    if folio is None: return 'U'
    base = re.sub(r'[rv]$', '', folio)
    try:
        fnum = int(re.sub(r'[a-z]', '', base))
    except:
        return 'U'
    # B-dialect: f75-f86 (cosmo), f103-f116 (stars), f1-f57 partial
    # Use established folio-dialect assignment from F037:
    # A: 1-57, 87-102; B: 58-74 (pharma disputed), 75-86, 103-117
    # Simplified: use B for known B sections
    b_ranges = [(75, 86), (103, 117)]
    a_ranges = [(1, 57), (87, 102)]
    for lo, hi in b_ranges:
        if lo <= fnum <= hi: return 'B'
    for lo, hi in a_ranges:
        if lo <= fnum <= hi: return 'A'
    # bio section (f105-f116 disputed) — treat as B
    return 'U'

def parse_latin(path):
    """Return list of Latin words (lowercase, letters only)."""
    words = []
    with open(path) as f:
        for line in f:
            for tok in re.findall(r'[a-zA-Z]+', line):
                words.append(tok.lower())
    return words

# ── entropy computations ─────────────────────────────────────────────────────

def entropy(counter):
    total = sum(counter.values())
    if total == 0: return 0.0
    return -sum((v/total) * math.log2(v/total) for v in counter.values() if v > 0)

def positional_entropy(words, max_pos=12):
    """
    Compute:
    - h_i: entropy of character at position i (marginal)
    - h_cond_i: conditional entropy H(c_i | c_{i-1})
    - n_i: number of words contributing to position i
    Returns: list of (i, h_i, n_i, h_cond_i)
    """
    pos_counters = defaultdict(Counter)  # position → char counts
    bigram_counters = defaultdict(Counter)  # (i-1, i) → (prev_char, cur_char) counts
    cond_prev = defaultdict(Counter)  # position → prev_char counts

    for w in words:
        chars = list(w)
        L = len(chars)
        for i, c in enumerate(chars):
            if i >= max_pos: break
            if c not in EVA_CHARS: continue
            pos_counters[i][c] += 1
            if i > 0:
                prev = chars[i-1]
                if prev in EVA_CHARS:
                    bigram_counters[i][(prev, c)] += 1
                    cond_prev[i][prev] += 1

    results = []
    for i in range(max_pos):
        cnt = pos_counters[i]
        h_i = entropy(cnt)
        n_i = sum(cnt.values())
        # conditional entropy H(c_i | c_{i-1})
        if i > 0 and bigram_counters[i]:
            # H(X,Y) - H(X)  where X=c_{i-1}, Y=c_i
            joint = bigram_counters[i]
            H_joint = entropy(joint)
            H_prev  = entropy(cond_prev[i])
            h_cond = H_joint - H_prev
        else:
            h_cond = float('nan')
        results.append((i, h_i, n_i, h_cond))
    return results

def positional_entropy_latin(words, max_pos=12):
    """Same computation for Latin words (ASCII letters)."""
    pos_counters = defaultdict(Counter)
    bigram_counters = defaultdict(Counter)
    cond_prev = defaultdict(Counter)
    for w in words:
        chars = list(w)
        for i, c in enumerate(chars):
            if i >= max_pos: break
            pos_counters[i][c] += 1
            if i > 0:
                prev = chars[i-1]
                bigram_counters[i][(prev, c)] += 1
                cond_prev[i][prev] += 1
    results = []
    for i in range(max_pos):
        cnt = pos_counters[i]
        h_i = entropy(cnt)
        n_i = sum(cnt.values())
        if i > 0 and bigram_counters[i]:
            H_joint = entropy(bigram_counters[i])
            H_prev  = entropy(cond_prev[i])
            h_cond = H_joint - H_prev
        else:
            h_cond = float('nan')
        results.append((i, h_i, n_i, h_cond))
    return results

def char_distribution(words, pos):
    """Return sorted char distribution at position pos."""
    cnt = Counter()
    for w in words:
        if len(w) > pos:
            c = w[pos]
            if c in EVA_CHARS:
                cnt[c] += 1
    total = sum(cnt.values())
    return [(c, v, v/total) for c, v in cnt.most_common(8)]

# ── position-specific analysis ────────────────────────────────────────────────

def suffix_entropy(words, from_end_positions=(1, 2, 3)):
    """Entropy of last-k characters (k from from_end_positions)."""
    results = {}
    for k in from_end_positions:
        cnt = Counter()
        for w in words:
            if len(w) >= k:
                c = w[-k]
                if c in EVA_CHARS:
                    cnt[c] += 1
        results[k] = (entropy(cnt), sum(cnt.values()))
    return results

# ── main ──────────────────────────────────────────────────────────────────────

print("Parsing VMS corpus...")
records = parse_vms(DATA_PATH)
print(f"  Total word tokens: {len(records)}")

words_a = [r[4] for r in records if r[2] == 'A']
words_b = [r[4] for r in records if r[2] == 'B']
print(f"  A-dialect: {len(words_a)} tokens  B-dialect: {len(words_b)} tokens")

# Validate: print sample words
print(f"\n  Sample A words: {words_a[:10]}")
print(f"  Sample B words: {words_b[:10]}")

# Word length distribution
def word_lengths(words):
    cnt = Counter(len(w) for w in words)
    total = sum(cnt.values())
    return [(l, cnt[l], cnt[l]/total) for l in sorted(cnt) if cnt[l] >= 10]

print("\nWord length distribution (A-dialect):")
for l, n, f in word_lengths(words_a)[:12]:
    bar = '#' * int(f * 60)
    print(f"  len={l:2d}: n={n:5d}  {bar}")

print("\nWord length distribution (B-dialect):")
for l, n, f in word_lengths(words_b)[:12]:
    bar = '#' * int(f * 60)
    print(f"  len={l:2d}: n={n:5d}  {bar}")

# ── positional entropy tables ─────────────────────────────────────────────────

MAX_POS = 12

ent_a = positional_entropy(words_a, MAX_POS)
ent_b = positional_entropy(words_b, MAX_POS)

print("\nLoading Latin corpus...")
latin_words = parse_latin(LATIN_CORPUS)
print(f"  Latin: {len(latin_words)} word tokens")
ent_lat = positional_entropy_latin(latin_words, MAX_POS)

print(f"\n{'='*80}")
print("MARGINAL ENTROPY h(c_i) BY POSITION")
print(f"{'='*80}")
print(f"{'Pos':>4}  {'A-VMS':>7}  {'N_A':>7}  {'B-VMS':>7}  {'N_B':>7}  {'Latin':>7}  {'N_Lat':>7}")
print('-' * 55)
for i in range(MAX_POS):
    ha = ent_a[i][1] if i < len(ent_a) else float('nan')
    na = ent_a[i][2] if i < len(ent_a) else 0
    hb = ent_b[i][1] if i < len(ent_b) else float('nan')
    nb = ent_b[i][2] if i < len(ent_b) else 0
    hl = ent_lat[i][1] if i < len(ent_lat) else float('nan')
    nl = ent_lat[i][2] if i < len(ent_lat) else 0
    if na < 100 and nb < 100 and nl < 100: continue
    print(f"  {i:2d}  {ha:7.4f}  {na:7d}  {hb:7.4f}  {nb:7d}  {hl:7.4f}  {nl:7d}")

print(f"\n{'='*80}")
print("CONDITIONAL ENTROPY h(c_i | c_{i-1}) BY POSITION")
print(f"{'='*80}")
print(f"{'Pos':>4}  {'A-VMS':>7}  {'B-VMS':>7}  {'Latin':>7}")
print('-' * 35)
for i in range(1, MAX_POS):
    hca = ent_a[i][3] if i < len(ent_a) else float('nan')
    hcb = ent_b[i][3] if i < len(ent_b) else float('nan')
    hcl = ent_lat[i][3] if i < len(ent_lat) else float('nan')
    na = ent_a[i][2] if i < len(ent_a) else 0
    if na < 100: continue
    print(f"  {i:2d}  {hca:7.4f}  {hcb:7.4f}  {hcl:7.4f}")

# ── character distributions at key positions ──────────────────────────────────

print(f"\n{'='*80}")
print("CHARACTER DISTRIBUTION AT KEY POSITIONS")
print(f"{'='*80}")

for pos_label, pos_idx in [("Position 0 (first char)", 0),
                             ("Position 1", 1),
                             ("Position 2", 2),
                             ("Position 3", 3)]:
    print(f"\n--- {pos_label} ---")
    dist_a = char_distribution(words_a, pos_idx)
    dist_b = char_distribution(words_b, pos_idx)
    print(f"  A-dialect: " + "  ".join(f"{c}={100*f:.1f}%" for c, _, f in dist_a))
    print(f"  B-dialect: " + "  ".join(f"{c}={100*f:.1f}%" for c, _, f in dist_b))

# ── suffix zone analysis ──────────────────────────────────────────────────────

print(f"\n{'='*80}")
print("SUFFIX ZONE ENTROPY (from end)")
print(f"{'='*80}")
suf_a = suffix_entropy(words_a, (1, 2, 3, 4))
suf_b = suffix_entropy(words_b, (1, 2, 3, 4))
print(f"{'k-from-end':>12}  {'h_A':>7}  {'N_A':>7}  {'h_B':>7}  {'N_B':>7}")
for k in (1, 2, 3, 4):
    ha, na = suf_a[k]
    hb, nb = suf_b[k]
    print(f"  last-{k:1d} char  {ha:7.4f}  {na:7d}  {hb:7.4f}  {nb:7d}")

# ── summary: entropy gradient profile ────────────────────────────────────────

print(f"\n{'='*80}")
print("ENTROPY GRADIENT SUMMARY")
print(f"{'='*80}")

def gradient_label(vals):
    """Quick characterization of shape."""
    valid = [(i, h) for i, h in vals if not math.isnan(h) and h > 0]
    if len(valid) < 4: return "insufficient data"
    hs = [h for _, h in valid]
    peak_i = hs.index(max(hs))
    trough_start = hs[0]
    trough_end = hs[-1]
    peak = max(hs)
    if peak_i > 0 and peak_i < len(hs)-1 and trough_start < peak and trough_end < peak:
        return f"U-shape peak at pos {valid[peak_i][0]} (h={peak:.3f}), low at 0 ({trough_start:.3f}) and end ({trough_end:.3f})"
    elif trough_start > trough_end:
        return f"monotone decrease {trough_start:.3f}→{trough_end:.3f}"
    elif trough_start < trough_end:
        return f"monotone increase {trough_start:.3f}→{trough_end:.3f}"
    else:
        return f"flat ~{sum(hs)/len(hs):.3f}"

h_profile_a = [(i, ent_a[i][1]) for i in range(MAX_POS) if ent_a[i][2] >= 100]
h_profile_b = [(i, ent_b[i][1]) for i in range(MAX_POS) if ent_b[i][2] >= 100]
h_profile_l = [(i, ent_lat[i][1]) for i in range(MAX_POS) if ent_lat[i][2] >= 100]

print(f"  A-dialect: {gradient_label(h_profile_a)}")
print(f"  B-dialect: {gradient_label(h_profile_b)}")
print(f"  Latin:     {gradient_label(h_profile_l)}")

# Max entropy (uniform over 16 EVA chars)
print(f"\n  Reference: H_max for 16 EVA chars = {math.log2(16):.4f} bits")
print(f"  Reference: H_max for 23 Latin chars = {math.log2(23):.4f} bits")

# ── dialect comparison at each position ──────────────────────────────────────

print(f"\n{'='*80}")
print("DIALECT COMPARISON: A vs B entropy difference by position")
print(f"{'='*80}")
print(f"{'Pos':>4}  {'h_A':>7}  {'h_B':>7}  {'Δ(A-B)':>8}  {'direction':>15}")
for i in range(MAX_POS):
    ha = ent_a[i][1] if i < len(ent_a) else float('nan')
    hb = ent_b[i][1] if i < len(ent_b) else float('nan')
    na = ent_a[i][2] if i < len(ent_a) else 0
    nb = ent_b[i][2] if i < len(ent_b) else 0
    if na < 100 or nb < 100: continue
    if math.isnan(ha) or math.isnan(hb): continue
    delta = ha - hb
    direction = "A more constrained" if delta < -0.1 else "B more constrained" if delta > 0.1 else "similar"
    print(f"  {i:2d}  {ha:7.4f}  {hb:7.4f}  {delta:+8.4f}  {direction}")

print("\nDone.")
