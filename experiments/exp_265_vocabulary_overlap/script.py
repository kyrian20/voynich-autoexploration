"""
exp_265: H467 — Word Vocabulary Overlap Between LF, MID, and LL Positions

Question: How much of the MID vocabulary is shared with LF/LL pools?
Does MID have lower type-token ratio (TTR) than LF/LL (consistent with copy buffer recycling)?

Key metrics:
1. Type-token ratio (TTR) for each position stratum (lower = more repetition)
2. Vocabulary overlap: |MID_types ∩ LF_types| / |MID_types| (what fraction of MID words also appear at LF)
3. Null baseline: expected overlap under random sampling (hypergeometric null)
4. Most frequent words by position pool

Expected under copy-buffer glossographic model:
- MID TTR << LF TTR (buffer recycles; MID has more word repetition)
- MID vocabulary heavily overlaps LF/LL (words copied from shared pool)
- Most frequent MID words appear frequently in LF/LL too
"""
from pathlib import Path as _RepositoryPath

import os, re, math
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
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
    """Return list of (dialect, lpos, word)."""
    records = []
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'^<f(\S+?)\.(\d+),([^>]+)>\s*(.*)', line)
            if not m: continue
            folio_tag, lnum_s, ltype, rest = m.group(1), m.group(2), m.group(3), m.group(4)
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
                if n == 1:   lpos = 'LL'
                elif idx == 0: lpos = 'LF'
                elif idx == n-1: lpos = 'LL'
                else:          lpos = 'MID'
                records.append((dialect, lpos, tok))
    return records

def hypergeometric_expected_overlap(n_mid_types, n_lf_types, n_total_types):
    """
    Expected overlap |MID_types ∩ LF_types| under null hypothesis that both
    LF and MID draw their types uniformly from the total vocabulary.
    E[overlap] = n_mid_types * (n_lf_types / n_total_types) approximately.
    More precisely: 1 - C(n_total - n_lf, n_mid) / C(n_total, n_mid)
    but that's computationally heavy. Use approximation.
    """
    # Probability any given MID type also appears in LF (under random assignment)
    # P(type t in LF) ≈ 1 - (1 - 1/n_total)^n_lf_tokens ≈ n_lf_types / n_total_types (type level approx)
    p_lf = n_lf_types / n_total_types
    return n_mid_types * p_lf

def ttr(words):
    """Type-token ratio."""
    types = set(words)
    return len(types) / len(words) if words else 0

def hapax_rate(words):
    """Fraction of tokens that are hapax legomena (appear exactly once)."""
    cnt = Counter(words)
    hapax = sum(1 for w, c in cnt.items() if c == 1)
    return hapax / len(words) if words else 0

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

print("\nCorpus sizes:")
for (d, lp), words in strata.items():
    cnt = Counter(words)
    print(f"  {d}-{lp:3s}: {len(words):6d} tokens, {len(cnt):5d} types, TTR={ttr(words):.4f}")

# ── Type-Token Ratio Analysis ─────────────────────────────────────────────────

print(f"\n{'='*70}")
print("TYPE-TOKEN RATIO (TTR) AND HAPAX RATE BY POSITION")
print(f"{'='*70}")
print(f"  {'Stratum':>10}  {'Tokens':>8}  {'Types':>7}  {'TTR':>7}  {'Hapax%':>8}  {'Freq_top1':>10}")
for dialect in ('A', 'B'):
    for lpos in ('LF', 'MID', 'LL'):
        words = strata[(dialect, lpos)]
        cnt = Counter(words)
        t = ttr(words)
        h = hapax_rate(words)
        top1 = cnt.most_common(1)[0] if cnt else ('?', 0)
        print(f"  {dialect}-{lpos:3s}       {len(words):8d}  {len(cnt):7d}  {t:7.4f}  {100*h:8.2f}%  "
              f"{top1[0]}({top1[1]})")

# ── Vocabulary Overlap Analysis ───────────────────────────────────────────────

print(f"\n{'='*70}")
print("VOCABULARY OVERLAP: MID TYPE-SET ∩ LF/LL TYPE-SETS")
print(f"{'='*70}")

for dialect in ('A', 'B'):
    words_lf  = strata[(dialect,'LF')]
    words_mid = strata[(dialect,'MID')]
    words_ll  = strata[(dialect,'LL')]

    types_lf  = set(words_lf)
    types_mid = set(words_mid)
    types_ll  = set(words_ll)
    all_types = types_lf | types_mid | types_ll

    overlap_mid_lf = types_mid & types_lf
    overlap_mid_ll = types_mid & types_ll
    overlap_all    = types_lf & types_mid & types_ll

    n_total = len(all_types)
    null_overlap_lf = hypergeometric_expected_overlap(len(types_mid), len(types_lf), n_total)
    null_overlap_ll = hypergeometric_expected_overlap(len(types_mid), len(types_ll), n_total)

    print(f"\n--- {dialect}-dialect ---")
    print(f"  Total vocabulary (LF∪MID∪LL): {n_total} types")
    print(f"  LF types: {len(types_lf)},  MID types: {len(types_mid)},  LL types: {len(types_ll)}")
    print(f"")
    print(f"  MID ∩ LF: {len(overlap_mid_lf)} types = {100*len(overlap_mid_lf)/len(types_mid):.1f}% of MID vocabulary")
    print(f"    Null expected: {null_overlap_lf:.0f} types = {100*null_overlap_lf/len(types_mid):.1f}%")
    print(f"    Observed/Expected ratio: {len(overlap_mid_lf)/null_overlap_lf:.2f}×")
    print(f"")
    print(f"  MID ∩ LL: {len(overlap_mid_ll)} types = {100*len(overlap_mid_ll)/len(types_mid):.1f}% of MID vocabulary")
    print(f"    Null expected: {null_overlap_ll:.0f} types = {100*null_overlap_ll/len(types_mid):.1f}%")
    print(f"    Observed/Expected ratio: {len(overlap_mid_ll)/null_overlap_ll:.2f}×")
    print(f"")
    print(f"  LF ∩ MID ∩ LL: {len(overlap_all)} types = {100*len(overlap_all)/len(types_mid):.1f}% of MID vocabulary")
    print(f"  MID-exclusive (not in LF or LL): {len(types_mid - types_lf - types_ll)} types = "
          f"{100*len(types_mid - types_lf - types_ll)/len(types_mid):.1f}% of MID vocabulary")

# ── Token-level overlap (reuse rate) ─────────────────────────────────────────

print(f"\n{'='*70}")
print("TOKEN-LEVEL REUSE: WHAT FRACTION OF MID TOKENS ARE LF/LL WORD TYPES?")
print(f"{'='*70}")

for dialect in ('A', 'B'):
    words_lf  = strata[(dialect,'LF')]
    words_mid = strata[(dialect,'MID')]
    words_ll  = strata[(dialect,'LL')]

    types_lf = set(words_lf)
    types_ll = set(words_ll)

    n_mid = len(words_mid)
    mid_in_lf_types = sum(1 for w in words_mid if w in types_lf)
    mid_in_ll_types = sum(1 for w in words_mid if w in types_ll)
    mid_in_lf_or_ll = sum(1 for w in words_mid if w in types_lf or w in types_ll)

    print(f"\n--- {dialect}-dialect ---")
    print(f"  MID tokens using LF word types: {mid_in_lf_types}/{n_mid} = {100*mid_in_lf_types/n_mid:.1f}%")
    print(f"  MID tokens using LL word types: {mid_in_ll_types}/{n_mid} = {100*mid_in_ll_types/n_mid:.1f}%")
    print(f"  MID tokens using LF OR LL word types: {mid_in_lf_or_ll}/{n_mid} = {100*mid_in_lf_or_ll/n_mid:.1f}%")

# ── Top words by stratum ──────────────────────────────────────────────────────

print(f"\n{'='*70}")
print("TOP 10 WORDS BY STRATUM")
print(f"{'='*70}")
for dialect in ('A', 'B'):
    print(f"\n--- {dialect}-dialect ---")
    for lpos in ('LF', 'MID', 'LL'):
        words = strata[(dialect, lpos)]
        cnt = Counter(words)
        top10 = cnt.most_common(10)
        top_str = "  ".join(f"{w}({c})" for w, c in top10)
        print(f"  {lpos:3s}: {top_str}")

# ── Zipf slope analysis ───────────────────────────────────────────────────────

print(f"\n{'='*70}")
print("ZIPF ANALYSIS: LOG-RANK vs LOG-FREQUENCY")
print(f"{'='*70}")

def zipf_slope(words, top_n=50):
    """Estimate Zipf slope from log-rank regression on top_n types."""
    cnt = Counter(words)
    freqs = sorted(cnt.values(), reverse=True)[:top_n]
    if len(freqs) < 5: return float('nan')
    log_ranks = [math.log(i+1) for i in range(len(freqs))]
    log_freqs = [math.log(f) for f in freqs]
    n = len(log_ranks)
    sx = sum(log_ranks); sy = sum(log_freqs)
    sxy = sum(log_ranks[i]*log_freqs[i] for i in range(n))
    sx2 = sum(lr**2 for lr in log_ranks)
    slope = (n*sxy - sx*sy) / (n*sx2 - sx**2) if n*sx2 != sx**2 else float('nan')
    return slope

for dialect in ('A', 'B'):
    print(f"\n--- {dialect}-dialect Zipf slopes (top-50 types) ---")
    for lpos in ('LF', 'MID', 'LL'):
        words = strata[(dialect, lpos)]
        slope = zipf_slope(words)
        cnt = Counter(words)
        top1_pct = 100*cnt.most_common(1)[0][1]/len(words) if words else 0
        top5_pct = 100*sum(c for _,c in cnt.most_common(5))/len(words) if words else 0
        print(f"  {lpos:3s}: Zipf slope = {slope:.3f}  (top-1 = {top1_pct:.1f}%, top-5 = {top5_pct:.1f}%)")

print(f"\nDone.")
