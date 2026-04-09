"""
Experiment: exp_021_f57v_f66r_overlap
Hypothesis: H023
Goal: Test whether the character overlap between f57v's 17-token repeating
sequence and f66r column 2 exceeds random expectation, and characterize
the @glyph overlap (@169, @172) in context.
"""

import re
import json
import math
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parents[2]
CORPUS = BASE / 'data/transcriptions/eva_zl3b.txt'


def ivtff_tokenize(text):
    """Tokenize IVTFF text on dots, respecting brackets."""
    tokens = []
    current = []
    depth = 0
    for ch in text:
        if ch == '[':
            depth += 1
            current.append(ch)
        elif ch == ']':
            depth -= 1
            current.append(ch)
        elif ch == '.' and depth == 0:
            tok = ''.join(current).strip()
            if tok:
                tokens.append(tok)
            current = []
        else:
            current.append(ch)
    last = ''.join(current).strip()
    if last:
        tokens.append(last)
    return tokens


def extract_folio_lines(path, folio_str):
    """Extract all lines from a folio."""
    lines = []
    in_folio = False
    with open(path, encoding='latin-1') as f:
        for raw_line in f:
            stripped = raw_line.strip()
            if re.match(rf'^<{re.escape(folio_str)}>', stripped):
                in_folio = True
                continue
            if in_folio:
                if re.match(r'^<f\d+', stripped) and f'<{folio_str}.' not in stripped:
                    break
                if stripped:
                    lines.append(stripped)
    return lines


def token_to_chars(tok):
    """Extract constituent characters from an IVTFF token.
    Handles: plain chars, [a:b] uncertainty brackets, @NNN; special glyphs.
    Returns the primary character representation."""
    tok = tok.strip()
    # @NNN; or @NNN;X compound
    if tok.startswith('@'):
        return [tok]  # treat whole @glyph token as atomic
    # [a:b] uncertainty bracket — take first alternative
    if tok.startswith('['):
        inner = tok[1:-1]
        return [inner.split(':')[0]]
    # Plain chars or compound (e.g., 'sh', 'air')
    return [tok]


def hypergeometric_pvalue(N, K, n, k):
    """P(X >= k) for Hypergeometric(N, K, n).
    N = population size (25 EVA chars)
    K = successes in population (f57v char set size)
    n = draws (f66r col2 char set size)
    k = observed successes (overlap size)
    """
    # P(X >= k) = sum_{i=k}^{min(K,n)} P(X=i)
    prob = 0.0
    for i in range(k, min(K, n) + 1):
        # C(K, i) * C(N-K, n-i) / C(N, n)
        try:
            p = (math.comb(K, i) * math.comb(N - K, n - i)) / math.comb(N, n)
            prob += p
        except ValueError:
            pass
    return prob


if __name__ == "__main__":
    print("Experiment exp_021: f57v↔f66r Character Overlap Test")
    print("Hypothesis: H023")
    print("Date: 2026-04-09\n")

    # --- f57v: 17-token cycle character set ---
    # From exp_019: the cycle at each of 4 repeats
    # Positions: o l [d:j] r v x k m f/p @169;v t r @170 @171 y I/c @172
    # Standard chars (non-@glyph): positions 1-9, 11-12, 15-17

    f57v_cycle_tokens = [
        'o', 'l', 'd',  # pos 1-3 (d used as primary for [d:j])
        'r', 'v', 'x', 'k', 'm',  # pos 4-8
        'f',            # pos 9 (variant f/p — use f as primary)
        '@169;v',       # pos 10 (@glyph compound)
        't', 'r',       # pos 11-12
        '@170', '@171', # pos 13-14 (@glyphs)
        'y',            # pos 15
        'I',            # pos 16 (variant I/c — use I as primary)
        '@172',         # pos 17 (@glyph)
    ]

    # Variants at pos 9 and 16
    f57v_variants = {9: {'f', 'p'}, 16: {'I', 'c'}}

    # Extract standard chars from f57v cycle (non-@glyph)
    f57v_standard = set()
    for tok in f57v_cycle_tokens:
        if not tok.startswith('@'):
            f57v_standard.add(tok)
    # Include variants
    for pos, variants in f57v_variants.items():
        f57v_standard |= variants

    # @glyphs in f57v cycle
    f57v_at_glyphs = set(tok for tok in f57v_cycle_tokens if tok.startswith('@'))

    print(f"=== f57v 17-token cycle ===")
    print(f"All tokens: {f57v_cycle_tokens}")
    print(f"Standard chars (non-@glyph): {sorted(f57v_standard)}")
    print(f"@glyphs: {sorted(f57v_at_glyphs)}")
    print(f"Standard char count: {len(f57v_standard)}")

    # --- f66r: column 2 character set ---
    # From exp_012: sequence y o s sh y d o f @169 x air d sh y f f y o d s f c @172 x t o @195 l r t o x p d
    # 34 entries, 16 unique

    f66r_col2_raw = [
        'y', 'o', 's', 'sh', 'y', 'd', 'o', 'f', '@169', 'x',
        'air', 'd', 'sh', 'y', 'f', 'f', 'y', 'o', 'd', 's',
        'f', 'c', '@172', 'x', 't', 'o', '@195', 'l', 'r', 't',
        'o', 'x', 'p', 'd'
    ]

    f66r_standard = set(tok for tok in f66r_col2_raw if not tok.startswith('@'))
    f66r_at_glyphs = set(tok for tok in f66r_col2_raw if tok.startswith('@'))

    # Separate single chars from compounds in f66r
    f66r_single = set(tok for tok in f66r_standard if len(tok) == 1)
    f66r_compounds = set(tok for tok in f66r_standard if len(tok) > 1)

    print(f"\n=== f66r column 2 ===")
    print(f"All unique tokens: {sorted(set(f66r_col2_raw))}")
    print(f"Standard (all forms): {sorted(f66r_standard)}")
    print(f"  Single chars: {sorted(f66r_single)}")
    print(f"  Compounds: {sorted(f66r_compounds)}")
    print(f"@glyphs: {sorted(f66r_at_glyphs)}")

    # --- Character overlap analysis ---

    # 1. Standard single-char overlap (most informative)
    f57v_single = set(ch for ch in f57v_standard if len(ch) == 1)
    f66r_single_only = f66r_single  # already single chars

    overlap_single = f57v_single & f66r_single_only
    only_f57v = f57v_single - f66r_single_only
    only_f66r = f66r_single_only - f57v_single

    print(f"\n=== Standard Single-Char Overlap ===")
    print(f"f57v single chars ({len(f57v_single)}): {sorted(f57v_single)}")
    print(f"f66r single chars ({len(f66r_single_only)}): {sorted(f66r_single_only)}")
    print(f"Intersection ({len(overlap_single)}): {sorted(overlap_single)}")
    print(f"Only in f57v ({len(only_f57v)}): {sorted(only_f57v)}")
    print(f"Only in f66r ({len(only_f66r)}): {sorted(only_f66r)}")

    # Jaccard similarity
    union = f57v_single | f66r_single_only
    jaccard = len(overlap_single) / len(union) if union else 0
    print(f"Jaccard similarity: {jaccard:.3f}")

    # 2. Hypergeometric test
    # EVA has 25 single chars
    N = 25  # total EVA single chars
    K = len(f57v_single)  # f57v draws K chars
    n = len(f66r_single_only)  # f66r draws n chars
    k_obs = len(overlap_single)  # observed overlap
    expected = K * n / N
    p_value = hypergeometric_pvalue(N, K, n, k_obs)

    print(f"\n=== Hypergeometric Test (single chars) ===")
    print(f"N (EVA total chars) = {N}")
    print(f"K (f57v char set size) = {K}")
    print(f"n (f66r char set size) = {n}")
    print(f"k_obs (observed overlap) = {k_obs}")
    print(f"Expected under H0: {expected:.2f}")
    print(f"Observed: {k_obs}")
    print(f"Excess: {k_obs - expected:.2f}")
    print(f"P(X >= {k_obs}): {p_value:.6f}")

    # 3. @Glyph overlap
    at_overlap = f57v_at_glyphs & f66r_at_glyphs
    # Note: f57v has @169;v (compound) vs f66r has @169 (standalone)
    # Check for partial match
    f57v_at_ids = set()
    for tok in f57v_at_glyphs:
        m = re.match(r'@(\d+)', tok)
        if m:
            f57v_at_ids.add(int(m.group(1)))

    f66r_at_ids = set()
    for tok in f66r_at_glyphs:
        m = re.match(r'@(\d+)', tok)
        if m:
            f66r_at_ids.add(int(m.group(1)))

    at_id_overlap = f57v_at_ids & f66r_at_ids

    print(f"\n=== @Glyph Overlap ===")
    print(f"f57v @glyphs: {sorted(f57v_at_glyphs)} → IDs: {sorted(f57v_at_ids)}")
    print(f"f66r @glyphs: {sorted(f66r_at_glyphs)} → IDs: {sorted(f66r_at_ids)}")
    print(f"Shared @glyph IDs: {sorted(at_id_overlap)}")
    print(f"  @169: in f57v as '@169;v' (compound), in f66r as '@169' (standalone)")
    print(f"  @172: in both as '@172' (standalone)")
    print(f"Only in f57v: {sorted(f57v_at_ids - f66r_at_ids)}")
    print(f"Only in f66r: {sorted(f66r_at_ids - f57v_at_ids)}")

    # 4. ZL3b context of @169 and @172 in f66r
    print(f"\n=== f66r Column 2 @Glyph Positions ===")
    for i, tok in enumerate(f66r_col2_raw):
        if tok.startswith('@'):
            prev = f66r_col2_raw[i-1] if i > 0 else None
            nxt = f66r_col2_raw[i+1] if i < len(f66r_col2_raw)-1 else None
            print(f"  Position {i+1}: {tok} | prev={prev}, next={nxt}")

    # 5. Positional mapping: does f66r col2 order match f57v cycle order?
    print(f"\n=== Positional Correspondence Test ===")
    # Extract positions of shared chars in f57v cycle
    cycle_pos = {}
    for i, tok in enumerate(f57v_cycle_tokens, 1):
        if not tok.startswith('@'):
            cycle_pos[tok] = i
    cycle_pos['p'] = 9   # variant
    cycle_pos['c'] = 16  # variant

    print("Shared chars and their f57v cycle position (in f66r col2 order):")
    f66r_positions = []
    for tok in f66r_col2_raw:
        if tok in cycle_pos:
            f66r_positions.append((tok, cycle_pos[tok]))

    print(f"  f66r col2 order vs f57v positions:")
    for tok, pos in f66r_positions:
        print(f"    f66r entry '{tok}' → f57v cycle pos {pos}")

    # Check if f66r order is correlated with f57v position order (Spearman)
    if len(f66r_positions) >= 4:
        # Spearman rank correlation computed manually
        f66r_ranks = list(range(1, len(f66r_positions) + 1))
        f57v_pos_vals = [pos for _, pos in f66r_positions]
        n_corr = len(f66r_ranks)
        # Rank the f57v positions
        sorted_vals = sorted(f57v_pos_vals)
        f57v_ranks = [sorted_vals.index(v) + 1 for v in f57v_pos_vals]
        # Spearman = 1 - 6*sum(d^2) / (n*(n^2-1))
        d_sq_sum = sum((r1 - r2)**2 for r1, r2 in zip(f66r_ranks, f57v_ranks))
        rho = 1 - 6 * d_sq_sum / (n_corr * (n_corr**2 - 1))
        # Approximate p-value via t distribution
        t_stat = rho * math.sqrt((n_corr - 2) / (1 - rho**2)) if abs(rho) < 1 else float('inf')
        # Two-tailed p approximation using normal approx for large n; for small n use t-table lookup
        # We'll just report rho and t_stat
        p_spear = None  # exact p not computed without scipy
        print(f"\n  Spearman rho (f66r order vs f57v cycle position): {rho:.3f}, t-stat={t_stat:.3f}")
        print(f"  (p-value not computed — scipy unavailable; rho≈0 means no order correlation)")
    else:
        rho, p_spear, t_stat = None, None, None
        print("  Too few shared entries for rank correlation")

    # 6. Summary
    print(f"\n=== Summary ===")
    results = {
        'f57v_single_chars': sorted(f57v_single),
        'f66r_single_chars': sorted(f66r_single_only),
        'overlap_single': sorted(overlap_single),
        'only_f57v': sorted(only_f57v),
        'only_f66r': sorted(only_f66r),
        'jaccard': round(jaccard, 4),
        'hypergeom': {
            'N': N, 'K': K, 'n': n, 'k_obs': k_obs,
            'expected': round(expected, 2),
            'p_value_one_tailed': round(p_value, 6),
        },
        'at_glyph_shared_ids': sorted(at_id_overlap),
        'at_glyph_f57v_only': sorted(f57v_at_ids - f66r_at_ids),
        'at_glyph_f66r_only': sorted(f66r_at_ids - f57v_at_ids),
        'spearman_rho': round(rho, 3) if rho is not None else None,
        'spearman_t_stat': round(t_stat, 3) if 't_stat' in dir() and t_stat is not None else None,
    }
    print(json.dumps(results, indent=2))

    out_path = Path(__file__).parent / 'data.json'
    with open(out_path, 'w') as f:
        import json as j
        j.dump(results, f, indent=2)
    print(f"\nSaved to {out_path}")
    print("Done.")
