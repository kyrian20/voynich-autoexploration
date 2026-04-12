"""
exp_263: H464 — Position-Stratified Character Entropy (LF/MID/LL)

Question: Does separating words by line position (LF/MID/LL) reveal stronger onset
constraint at LF and suffix constraint at LL than pooled analysis (exp_259)?

Expected:
- LF words: lower pos-0 entropy (y/s/t-onset dominance → restricted first character)
- LL words: lower last-1-char entropy (LL suffix grammar → -am/-aiin terminal patterns)
- MID words: intermediate entropy profile

Analysis:
1. Compute h(c_i) and h(c_i | c_{i-1}) separately for LF, MID, LL word pools
2. Compare pos-0 entropy across pools (onset constraint signal)
3. Compare last-k char entropy across pools (suffix constraint signal)
4. Separate A and B dialect for each pool
"""

import os, re, math
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

EVA_CHARS = set('acdehiklmnoqrsty')

def clean_token(tok):
    tok = re.sub(r'<[^>]*>', '', tok)
    tok = re.sub(r'\[([^:]+):[^\]]+\]', r'\1', tok)
    tok = re.sub(r'\{([^}]*)\}', r'\1', tok)
    tok = re.sub(r'[!?,*\-=@#$%^&|~]', '', tok)
    tok = tok.strip()
    if not tok: return None
    if not all(c in EVA_CHARS for c in tok): return None
    return tok

def get_dialect(folio):
    if folio is None: return 'U'
    base = re.sub(r'[rv]$', '', folio)
    try:
        fnum = int(re.sub(r'[a-z]', '', base))
    except:
        return 'U'
    b_ranges = [(75, 86), (103, 117)]
    a_ranges = [(1, 57), (87, 102)]
    for lo, hi in b_ranges:
        if lo <= fnum <= hi: return 'B'
    for lo, hi in a_ranges:
        if lo <= fnum <= hi: return 'A'
    return 'U'

def parse_vms(path):
    """Return list of (dialect, line_pos, word)."""
    records = []
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'^<f(\S+?)\.(\d+),([^>]+)>\s*(.*)', line)
            if not m: continue
            folio_tag, lnum_s, ltype, rest = m.group(1), m.group(2), m.group(3), m.group(4)
            # Filter: only paragraph lines (ltype starts with @P or P after stripping +*=/~&)
            lc_stripped = ltype.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            raw_tokens = rest.split('.')
            clean = []
            for tok in raw_tokens:
                ctok = clean_token(tok)
                if ctok and len(ctok) >= 2:
                    clean.append(ctok)
            n = len(clean)
            if n == 0: continue
            dialect = get_dialect(folio_tag)
            for idx, tok in enumerate(clean):
                if n == 1:
                    lpos = 'LL'
                elif idx == 0:
                    lpos = 'LF'
                elif idx == n - 1:
                    lpos = 'LL'
                else:
                    lpos = 'MID'
                records.append((dialect, lpos, tok))
    return records

def entropy(counter):
    total = sum(counter.values())
    if total == 0: return 0.0
    return -sum((v/total) * math.log2(v/total) for v in counter.values() if v > 0)

def positional_entropy(words, max_pos=12):
    pos_counters = defaultdict(Counter)
    bigram_counters = defaultdict(Counter)
    cond_prev = defaultdict(Counter)
    for w in words:
        chars = list(w)
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
        if i > 0 and bigram_counters[i]:
            H_joint = entropy(bigram_counters[i])
            H_prev  = entropy(cond_prev[i])
            h_cond = H_joint - H_prev
        else:
            h_cond = float('nan')
        results.append((i, h_i, n_i, h_cond))
    return results

def suffix_entropy(words):
    """Entropy of last-k characters for k in {1,2,3,4}."""
    results = {}
    for k in (1, 2, 3, 4):
        cnt = Counter()
        for w in words:
            if len(w) >= k:
                c = w[-k]
                if c in EVA_CHARS:
                    cnt[c] += 1
        results[k] = (entropy(cnt), sum(cnt.values()))
    return results

def char_dist_pos(words, pos, top_n=6):
    cnt = Counter()
    for w in words:
        if len(w) > pos and w[pos] in EVA_CHARS:
            cnt[w[pos]] += 1
    total = sum(cnt.values())
    return [(c, v/total) for c, v in cnt.most_common(top_n)] if total > 0 else []

# ── Main ─────────────────────────────────────────────────────────────────────

print("Parsing VMS corpus...")
records = parse_vms(DATA_PATH)
print(f"  Total records: {len(records)}")

# Stratify by dialect and line position
strata = {('A','LF'):[], ('A','MID'):[], ('A','LL'):[],
          ('B','LF'):[], ('B','MID'):[], ('B','LL'):[]}
for dialect, lpos, word in records:
    key = (dialect, lpos)
    if key in strata:
        strata[key].append(word)

print("\nCorpus sizes by stratum:")
for (d, lp), words in strata.items():
    print(f"  {d}-{lp:3s}: {len(words):6d} words")

MAX_POS = 10

# ── Positional entropy for each stratum ──────────────────────────────────────

print(f"\n{'='*80}")
print("MARGINAL ENTROPY h(c_i) BY POSITION — STRATIFIED BY LINE POSITION")
print(f"{'='*80}")

# Compare LF vs MID vs LL within each dialect
for dialect in ('A', 'B'):
    words_lf  = strata[(dialect,'LF')]
    words_mid = strata[(dialect,'MID')]
    words_ll  = strata[(dialect,'LL')]

    ent_lf  = positional_entropy(words_lf,  MAX_POS)
    ent_mid = positional_entropy(words_mid, MAX_POS)
    ent_ll  = positional_entropy(words_ll,  MAX_POS)

    print(f"\n--- {dialect}-dialect ---")
    print(f"  {'Pos':>4}  {'h_LF':>7}  {'N_LF':>7}  {'h_MID':>7}  {'N_MID':>7}  {'h_LL':>7}  {'N_LL':>7}")
    print(f"  {'-'*55}")
    for i in range(MAX_POS):
        h_lf  = ent_lf[i][1]  if i < len(ent_lf)  else float('nan')
        n_lf  = ent_lf[i][2]  if i < len(ent_lf)  else 0
        h_mid = ent_mid[i][1] if i < len(ent_mid) else float('nan')
        n_mid = ent_mid[i][2] if i < len(ent_mid) else 0
        h_ll  = ent_ll[i][1]  if i < len(ent_ll)  else float('nan')
        n_ll  = ent_ll[i][2]  if i < len(ent_ll)  else 0
        if n_lf < 30 and n_mid < 30 and n_ll < 30: continue
        h_lf_s  = f'{h_lf:7.4f}' if n_lf >= 30  else '      -'
        h_mid_s = f'{h_mid:7.4f}' if n_mid >= 30 else '      -'
        h_ll_s  = f'{h_ll:7.4f}'  if n_ll >= 30  else '      -'
        print(f"  {i:4d}  {h_lf_s}  {n_lf:7d}  {h_mid_s}  {n_mid:7d}  {h_ll_s}  {n_ll:7d}")

# ── Key structural signals ────────────────────────────────────────────────────

print(f"\n{'='*80}")
print("KEY STRUCTURAL SIGNALS: Pos-0 Onset Constraint and Suffix Zone")
print(f"{'='*80}")

for dialect in ('A', 'B'):
    words_lf  = strata[(dialect,'LF')]
    words_mid = strata[(dialect,'MID')]
    words_ll  = strata[(dialect,'LL')]

    ent_lf  = positional_entropy(words_lf,  MAX_POS)
    ent_mid = positional_entropy(words_mid, MAX_POS)
    ent_ll  = positional_entropy(words_ll,  MAX_POS)

    print(f"\n--- {dialect}-dialect ---")

    # Pos-0 (onset zone)
    h0_lf  = ent_lf[0][1]  if len(ent_lf)  > 0 and ent_lf[0][2] >= 30  else float('nan')
    h0_mid = ent_mid[0][1] if len(ent_mid) > 0 and ent_mid[0][2] >= 30 else float('nan')
    h0_ll  = ent_ll[0][1]  if len(ent_ll)  > 0 and ent_ll[0][2] >= 30  else float('nan')
    print(f"  Pos-0 entropy (onset constraint):")
    print(f"    LF:  {h0_lf:.4f} (N={ent_lf[0][2] if len(ent_lf)>0 else 0})")
    print(f"    MID: {h0_mid:.4f} (N={ent_mid[0][2] if len(ent_mid)>0 else 0})")
    print(f"    LL:  {h0_ll:.4f} (N={ent_ll[0][2] if len(ent_ll)>0 else 0})")

    # Suffix zone (last-k char)
    suf_lf  = suffix_entropy(words_lf)
    suf_mid = suffix_entropy(words_mid)
    suf_ll  = suffix_entropy(words_ll)
    print(f"  Last-1 char entropy (suffix constraint):")
    print(f"    LF:  {suf_lf[1][0]:.4f}  LF last-2: {suf_lf[2][0]:.4f}")
    print(f"    MID: {suf_mid[1][0]:.4f}  MID last-2: {suf_mid[2][0]:.4f}")
    print(f"    LL:  {suf_ll[1][0]:.4f}  LL last-2: {suf_ll[2][0]:.4f}")

# ── Character distributions at pos-0 for each stratum ────────────────────────

print(f"\n{'='*80}")
print("CHAR DISTRIBUTION AT POS-0 (ONSET ZONE) BY LINE POSITION")
print(f"{'='*80}")
for dialect in ('A', 'B'):
    print(f"\n--- {dialect}-dialect pos-0 char distributions ---")
    for lpos in ('LF', 'MID', 'LL'):
        words = strata[(dialect, lpos)]
        dist = char_dist_pos(words, 0, top_n=8)
        dist_str = "  ".join(f"{c}={100*f:.1f}%" for c, f in dist)
        print(f"  {lpos:3s}: {dist_str}")

# ── Last-2 char distributions ────────────────────────────────────────────────

print(f"\n{'='*80}")
print("CHAR DISTRIBUTION AT LAST-1 (SUFFIX TERMINAL) BY LINE POSITION")
print(f"{'='*80}")
for dialect in ('A', 'B'):
    print(f"\n--- {dialect}-dialect last-1 char distributions ---")
    for lpos in ('LF', 'MID', 'LL'):
        words = strata[(dialect, lpos)]
        cnt = Counter()
        for w in words:
            if len(w) >= 1 and w[-1] in EVA_CHARS:
                cnt[w[-1]] += 1
        total = sum(cnt.values())
        dist = [(c, v/total) for c, v in cnt.most_common(6)]
        dist_str = "  ".join(f"{c}={100*f:.1f}%" for c, f in dist)
        print(f"  {lpos:3s}: {dist_str}")

# ── -am terminal frequency by line position ───────────────────────────────────

print(f"\n{'='*80}")
print("-am SUFFIX RATE BY LINE POSITION")
print(f"{'='*80}")
for dialect in ('A', 'B'):
    print(f"\n--- {dialect}-dialect -am rates ---")
    for lpos in ('LF', 'MID', 'LL'):
        words = strata[(dialect, lpos)]
        am_rate = sum(1 for w in words if w.endswith('am')) / max(1, len(words))
        print(f"  {lpos:3s}: {am_rate:.4f} ({100*am_rate:.2f}%)  N={len(words)}")

print(f"\nDone.")
