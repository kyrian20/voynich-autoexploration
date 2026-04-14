#!/usr/bin/env python3
"""
exp_586: Transliteration Replication — Session R1 (EVA-basic)

Replicates five pre-registered findings under EVA-basic tokenization.
EVA-basic uses the same ZL3b corpus file but with a stricter tokenizer
that accepts only pure EVA-alphabet tokens (drops uncertainty markers
and non-EVA characters).

Pre-registered findings (preregistration_transliteration_and_specificity_thresholds.md):
  F1: Three-layer positional architecture (openers/mid/terminals)
      Retained if ≥75% onset-class category agreement with ZL3b (≥15/20)
  F2: Terminal-layer dialect inversion (A={d,cth}; B={r,l,ol,o,a}; zero overlap)
      Retained if zero overlap holds; d=A-terminal; ≥1 of {r,l,ol,o,a}=B-terminal
  F3: Bigram matrix cross-dialect invariants (y→y, sh→qok, ok→ok, qok→s elevated;
      sh→ch depleted)
      Retained if ≥4/5 invariants replicate directionally in both dialects
  F4: A-herbal paragraph chain d→qot→ch→o→sh
      Retained if chain exceeds 95th percentile of both null distributions (N=200)
      CL bigrams = (LL-onset[i], LL-onset[i+1]) per exp_583 methodology
  F5: Systematic -edy suffix transformation (A:-ol/-or/-ey; B:-edy/-eedy)
      Retained if ≥75% of onset classes show directional B-suffix increase

Implementation notes:
  - F2 uses CONF threshold (E>=1.5, n>=20) to define terminal sets, not top-N
  - F3 uses directional threshold (E>1.0 elevated, E<1.0 depleted) in both dialects
  - F4 uses (LL[i]->LL[i+1]) CL pairs per exp_583, not (LL[i]->LF[i+1])
  - F5 requires b_b_rate >= 3*a_b_rate AND b_b_rate >= 0.05 (directional 3× increase)

Plan references: transliteration_replication_plan.md §7.2, §8.4
"""

import sys, os, re, random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / 'state'))

from voynich_constraints import (
    load_vms_corpus, tokenize, tokenize_eva_basic,
    get_onset, get_suffix, positional_enrichment,
    suffix_positional_enrichment, bigram_enrichment,
    iter_all_words, iter_slot_words,
)

CORPUS_PATH = str(ROOT / 'data' / 'transcriptions' / 'eva_zl3b.txt')
SEED = 586000

ALL_ONSET_CLASSES = [
    'qok', 'qot', 'qo', 'cth', 'sch', 'ckh', 'cph',
    'ch', 'sh', 'ok', 'ot', 'ol',
    'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'a', 'o',
]

# Thresholds
CONF_E    = 1.5   # CONF enrichment for positional architecture
CONF_N    = 20    # Min obs for CONF positional classification
MIN_N_TERMINAL = 20  # Min obs to qualify as terminal

# A-herbal folio range (per exp_511/583 methodology)
A_HERBAL_MAX_FOLIO = 56

def sep(char='─', width=70):
    print(char * width)

# ── F1: Positional architecture ─────────────────────────────────────────────

def classify_positional_architecture(corpus):
    """Classify each onset class as opener / terminal / mid / rare."""
    classifications = {}
    details = {}
    for cls in ALL_ONSET_CLASSES:
        e_lf, obs_lf, n_lf = positional_enrichment(corpus, cls, 'LF')
        e_ll, obs_ll, n_ll = positional_enrichment(corpus, cls, 'LL')
        if obs_lf < CONF_N and obs_ll < CONF_N:
            classifications[cls] = 'rare'
            details[cls] = (e_lf, obs_lf, e_ll, obs_ll, 'rare')
            continue
        lf_conf = (e_lf == e_lf) and (e_lf >= CONF_E) and (obs_lf >= CONF_N)
        ll_conf = (e_ll == e_ll) and (e_ll >= CONF_E) and (obs_ll >= CONF_N)
        if lf_conf and not ll_conf:
            cat = 'opener'
        elif ll_conf and not lf_conf:
            cat = 'terminal'
        elif lf_conf and ll_conf:
            cat = 'opener' if e_lf >= e_ll else 'terminal'
        else:
            cat = 'mid'
        classifications[cls] = cat
        details[cls] = (e_lf, obs_lf, e_ll, obs_ll, cat)
    return classifications, details

# ── F2: Terminal dialect inversion ─────────────────────────────────────────

def get_conf_terminals(corpus, dialect_label, min_e=CONF_E, min_obs=MIN_N_TERMINAL):
    """Return onset classes with CONF LL enrichment (E>=min_e, obs>=min_obs)."""
    terminals = {}
    for cls in ALL_ONSET_CLASSES:
        e, obs, n = positional_enrichment(corpus, cls, 'LL')
        if (e == e) and (e >= min_e) and (obs >= min_obs):
            terminals[cls] = (round(e, 3), obs)
    return terminals

# ── F3: Bigram invariants ─────────────────────────────────────────────────

# CONF threshold = directional: elevated=E>1.0, depleted=E<1.0 in BOTH dialects.
# qok→s was found as A-specific elevated under old tokenizer; under canonical
# tokenizer qok→s (A=0.827) is not elevated in A → expected to fail.
BIGRAM_INVARIANTS = [
    ('y',   'y',   'elevated'),
    ('sh',  'qok', 'elevated'),
    ('ok',  'ok',  'elevated'),
    ('qok', 's',   'elevated'),
    ('sh',  'ch',  'depleted'),
]

def compute_bigram_invariants(a_corpus, b_corpus):
    results = {}
    for (sender, receiver, direction) in BIGRAM_INVARIANTS:
        ae, ao, an = bigram_enrichment(a_corpus, sender, receiver)
        be, bo, bn = bigram_enrichment(b_corpus, sender, receiver)
        if direction == 'elevated':
            a_ok = (ae == ae) and ae > 1.0
            b_ok = (be == be) and be > 1.0
        else:  # depleted
            a_ok = (ae == ae) and ae < 1.0
            b_ok = (be == be) and be < 1.0
        replicated = a_ok and b_ok
        results[f'{sender}→{receiver}'] = {
            'direction': direction,
            'A_E': round(ae, 3) if ae == ae else float('nan'),
            'B_E': round(be, 3) if be == be else float('nan'),
            'A_obs': ao, 'B_obs': bo,
            'A_ok': a_ok, 'B_ok': b_ok,
            'replicated': replicated,
        }
    return results

# ── F4: A-herbal paragraph chain ─────────────────────────────────────────

def load_a_herbal_folio_lines(tokenizer_fn, max_folio=A_HERBAL_MAX_FOLIO):
    """Load A-dialect herbal folio lines for CL chain analysis.

    Returns dict: folio_num -> list_of_word_lists (lines in order).
    Uses folios n <= max_folio, P-locus body lines, folio-level A-dialect filter.
    """
    raw = defaultdict(list)
    with open(CORPUS_PATH, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(None, 1)
            if len(parts) < 2:
                continue
            locus_raw, text = parts
            lparts = locus_raw.split(',')
            if len(lparts) < 2:
                continue
            folio_base = lparts[0].split('.')[0].lstrip('<')
            m = re.match(r'f(\d+)', folio_base)
            if not m:
                continue
            fnum = int(m.group(1))
            if fnum > max_folio:
                continue
            lt = lparts[1].rstrip('>').lstrip('@+*=~&')
            if not lt.startswith('P'):
                continue
            words = tokenizer_fn(text)
            if words:
                raw[fnum].append(words)

    out = {}
    for fnum, lines in raw.items():
        all_words = [w for wl in lines for w in wl]
        if len(all_words) < 10:
            continue
        edy_rate = sum(1 for w in all_words if 'edy' in w or 'eedy' in w) / len(all_words)
        if edy_rate < 0.05:  # A-dialect
            out[fnum] = lines
    return out

def build_ll_ll_pairs(folio_lines):
    """CL bigrams = (LL-onset[i], LL-onset[i+1]) per exp_583 methodology.

    Consecutive last-word onsets within each folio.
    """
    pairs = []
    for fnum in sorted(folio_lines):
        lines = folio_lines[fnum]
        ll_onsets = [get_onset(l[-1]) for l in lines if l]
        for i in range(len(ll_onsets) - 1):
            pairs.append((ll_onsets[i], ll_onsets[i + 1]))
    return pairs

def chain_strength(pairs, chain):
    """Joint enrichment product using exp_583 formula: E = obs / (f_a * f_b * N)."""
    if not pairs:
        return 0.0
    total = len(pairs)
    lf_base = Counter(a for a, b in pairs)
    pair_counts = Counter(pairs)
    js = 1.0
    for i in range(len(chain) - 1):
        a, b = chain[i], chain[i + 1]
        fa = lf_base.get(a, 0) / total
        fb = lf_base.get(b, 0) / total
        if fa == 0 or fb == 0:
            return 0.0
        expected = fa * fb * total
        obs = pair_counts.get((a, b), 0)
        e = obs / expected if expected > 0 else 0.0
        js *= e
    return js

def run_chain_null_model(folio_lines, target_chain, n_shuffles=200, seed=SEED):
    """Test target_chain against section-shuffled null model.

    Shuffles: randomly reorder lines within each folio (destroys paragraph sequence).
    Returns: (real_js, percentile, null_dist)
    """
    rng = random.Random(seed)
    real_pairs = build_ll_ll_pairs(folio_lines)
    real_js = chain_strength(real_pairs, target_chain)

    null_js = []
    for _ in range(n_shuffles):
        shuf = {}
        for fnum, lines in folio_lines.items():
            sl = list(lines)
            rng.shuffle(sl)
            shuf[fnum] = sl
        sp = build_ll_ll_pairs(shuf)
        null_js.append(chain_strength(sp, target_chain))

    pct = sum(1 for v in null_js if real_js > v) / n_shuffles * 100
    return real_js, pct, null_js

def run_onset_shuffle_null(folio_lines, target_chain, n_shuffles=200, seed=SEED+1):
    """Onset-shuffled null model: permute LL-onset labels."""
    rng = random.Random(seed)
    real_pairs = build_ll_ll_pairs(folio_lines)
    real_js = chain_strength(real_pairs, target_chain)

    null_js = []
    for _ in range(n_shuffles):
        all_onsets = [a for a, b in real_pairs] + ([real_pairs[-1][1]] if real_pairs else [])
        perm = list(all_onsets)
        rng.shuffle(perm)
        # Rebuild pairs with permuted onsets
        shuf_pairs = [(perm[i], perm[i+1]) for i in range(len(real_pairs))]
        null_js.append(chain_strength(shuf_pairs, target_chain))

    pct = sum(1 for v in null_js if real_js > v) / n_shuffles * 100
    return real_js, pct, null_js

# ── F5: Suffix transformation ─────────────────────────────────────────────

A_SUFFIXES = {'ol', 'or', 'ey'}
B_SUFFIXES = {'edy', 'eedy'}
MIN_TOKENS_FOR_SUFFIX = 20
# Transform threshold: B-suffix rate at least 3× higher in B-dialect than A-dialect,
# AND absolute B-suffix rate in B >= 5%
B_SUFFIX_FOLD_THRESHOLD = 3.0
B_SUFFIX_ABS_THRESHOLD  = 0.05

def suffix_transformation_analysis(a_corpus, b_corpus):
    """
    For each onset class, check whether B-dialect shows a systematic
    3×-fold increase in B-suffix rate relative to A-dialect, with
    absolute rate >= 5%.

    This is the directional definition of the -edy suffix transformation.
    """
    def suf_rate(corpus, cls, suf_set):
        words = [w for _, ws in corpus for w in ws if get_onset(w) == cls]
        if not words:
            return 0.0, 0
        hits = sum(1 for w in words if any(w.endswith(s) for s in suf_set))
        return hits / len(words), len(words)

    results = {}
    for cls in ALL_ONSET_CLASSES:
        a_bsuf, n_a = suf_rate(a_corpus, cls, B_SUFFIXES)
        b_bsuf, n_b = suf_rate(b_corpus, cls, B_SUFFIXES)
        a_asuf, _   = suf_rate(a_corpus, cls, A_SUFFIXES)
        b_asuf, _   = suf_rate(b_corpus, cls, A_SUFFIXES)

        if n_a < MIN_TOKENS_FOR_SUFFIX or n_b < MIN_TOKENS_FOR_SUFFIX:
            results[cls] = None
            continue

        # Transformation: B-suffix rate dramatically increased in B vs A
        fold = (b_bsuf / a_bsuf) if a_bsuf > 0 else float('inf')
        shows = (b_bsuf >= B_SUFFIX_ABS_THRESHOLD) and (
            (a_bsuf == 0) or (fold >= B_SUFFIX_FOLD_THRESHOLD)
        )
        results[cls] = {
            'shows_transform': shows,
            'a_bsuf': round(a_bsuf, 4), 'b_bsuf': round(b_bsuf, 4),
            'a_asuf': round(a_asuf, 4), 'b_asuf': round(b_asuf, 4),
            'fold': round(fold, 1) if a_bsuf > 0 else '∞',
            'n_a': n_a, 'n_b': n_b,
        }
    return results

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    rng = random.Random(SEED)

    sep('═')
    print("exp_586: Transliteration Replication — Session R1 (EVA-basic)")
    sep('═')

    # ── Load corpora ──────────────────────────────────────────────────────────
    print("\n[0] Loading corpora...")

    zl3b_b = load_vms_corpus(CORPUS_PATH, dialect='B')
    zl3b_a = load_vms_corpus(CORPUS_PATH, dialect='A')
    eva_b  = load_vms_corpus(CORPUS_PATH, dialect='B', tokenizer=tokenize_eva_basic)
    eva_a  = load_vms_corpus(CORPUS_PATH, dialect='A', tokenizer=tokenize_eva_basic)

    n_zl3b_b = sum(len(w) for _, w in zl3b_b)
    n_zl3b_a = sum(len(w) for _, w in zl3b_a)
    n_eva_b  = sum(len(w) for _, w in eva_b)
    n_eva_a  = sum(len(w) for _, w in eva_a)
    delta_b  = 100.0 * (n_zl3b_b - n_eva_b) / n_zl3b_b
    delta_a  = 100.0 * (n_zl3b_a - n_eva_a) / n_zl3b_a

    print(f"  ZL3b  B: {len(zl3b_b)} lines, {n_zl3b_b:,} tokens")
    print(f"  ZL3b  A: {len(zl3b_a)} lines, {n_zl3b_a:,} tokens")
    print(f"  EVA-b B: {len(eva_b)} lines, {n_eva_b:,} tokens  (delta={delta_b:.3f}%)")
    print(f"  EVA-b A: {len(eva_a)} lines, {n_eva_a:,} tokens  (delta={delta_a:.3f}%)")
    if delta_b >= 10.0 or delta_a >= 10.0:
        print("  ABORT: token delta ≥10%")
        return
    print(f"  Token-count delta GATE (<10%): PASS")

    # ── F1: Three-layer positional architecture ───────────────────────────────
    sep()
    print("\n[F1] Three-layer positional architecture")
    print(f"     CONF: E≥{CONF_E}×, obs≥{CONF_N}")

    zl3b_cls, _ = classify_positional_architecture(zl3b_b)
    eva_cls, _  = classify_positional_architecture(eva_b)

    print(f"\n  {'Class':<8} {'ZL3b':<12} {'EVA-basic':<12} Match")
    print(f"  {'-'*8} {'-'*12} {'-'*12} -----")
    matches = 0
    total_charted = 0
    for cls in ALL_ONSET_CLASSES:
        z, e = zl3b_cls[cls], eva_cls[cls]
        if z == 'rare' and e == 'rare':
            print(f"  {cls:<8} {z:<12} {e:<12} — (rare)")
            continue
        total_charted += 1
        m = (z == e)
        if m: matches += 1
        print(f"  {cls:<8} {z:<12} {e:<12} {'YES' if m else 'NO '}")

    agreement_pct = 100.0 * matches / total_charted if total_charted else 0
    print(f"\n  Agreement: {matches}/{total_charted} = {agreement_pct:.1f}%")
    f1_status = ('RETAINED' if agreement_pct >= 75.0 and matches >= 15
                 else ('WEAKENED' if agreement_pct >= 50.0
                       else 'FAILED'))
    print(f"  Pre-reg threshold: ≥75% (≥15/20). Result: {f1_status}")

    # ── F2: Terminal-layer dialect inversion ──────────────────────────────────
    sep()
    print("\n[F2] Terminal-layer dialect inversion")
    print(f"     CONF terminal: E≥{CONF_E}×, obs≥{MIN_N_TERMINAL}")

    # Compute CONF terminal sets under EVA-basic
    eva_a_terms = get_conf_terminals(eva_a, 'A')
    eva_b_terms = get_conf_terminals(eva_b, 'B')

    print("\n  A-dialect CONF terminals (E≥1.5, obs≥20):")
    for cls, (e, obs) in sorted(eva_a_terms.items(), key=lambda x: -x[1][0]):
        print(f"    {cls:<8} E={e:.3f} (n={obs})")

    print("\n  B-dialect CONF terminals (E≥1.5, obs≥20):")
    for cls, (e, obs) in sorted(eva_b_terms.items(), key=lambda x: -x[1][0]):
        print(f"    {cls:<8} E={e:.3f} (n={obs})")

    a_set = set(eva_a_terms.keys())
    b_set = set(eva_b_terms.keys())
    overlap = a_set & b_set
    d_in_a = 'd' in a_set
    b_canonical = {'r', 'l', 'ol', 'o', 'a'}
    b_member = len(b_canonical & b_set) > 0

    print(f"\n  Overlap: {overlap if overlap else '∅ (zero overlap)'}")
    print(f"  d ∈ A-terminals: {d_in_a}")
    print(f"  B-canonical member ∈ B-terminals: {b_member} ({b_canonical & b_set})")

    f2_retained = (len(overlap) == 0) and d_in_a and b_member
    f2_weakened = (not f2_retained) and (len(overlap) <= 1)
    f2_status = ('RETAINED' if f2_retained else ('WEAKENED' if f2_weakened else 'FAILED'))
    print(f"  Pre-reg threshold: zero overlap + d=A-terminal + ≥1 B-canonical in B.")
    print(f"  Result: {f2_status}")

    # ── F3: Bigram matrix cross-dialect invariants ────────────────────────────
    sep()
    print("\n[F3] Bigram matrix cross-dialect invariants")
    print("     Threshold: directional (E>1.0 elevated / E<1.0 depleted) in both dialects")

    bigram_res = compute_bigram_invariants(eva_a, eva_b)
    n_replicated = 0
    for pair_str, r in bigram_res.items():
        ok_a = '✓' if r['A_ok'] else '✗'
        ok_b = '✓' if r['B_ok'] else '✗'
        rep = 'REPLICATED' if r['replicated'] else 'not replicated'
        print(f"  {pair_str:<12} ({r['direction']:<8}) "
              f"A={r['A_E']:.3f}{ok_a}(n={r['A_obs']}) "
              f"B={r['B_E']:.3f}{ok_b}(n={r['B_obs']})  {rep}")
        if r['replicated']:
            n_replicated += 1

    print(f"\n  Replicated: {n_replicated}/5")
    note = ""
    if not bigram_res['qok→s']['replicated']:
        note = " (qok→s A-specific under old tokenizer; A=depleted under canonical)"
    f3_status = ('RETAINED' if n_replicated >= 4 else ('WEAKENED' if n_replicated >= 2 else 'FAILED'))
    print(f"  Pre-reg threshold: ≥4/5. Result: {f3_status}{note}")

    # ── F4: A-herbal paragraph chain ──────────────────────────────────────────
    sep()
    print("\n[F4] A-herbal paragraph chain d→qot→ch→o→sh")
    TARGET_CHAIN = ['d', 'qot', 'ch', 'o', 'sh']
    N_SHUFFLES = 200
    print(f"     CL pairs: (LL[i], LL[i+1]) per exp_583 methodology")
    print(f"     Null model: N={N_SHUFFLES} section-shuffled + {N_SHUFFLES} onset-shuffled")

    print("     Loading A-herbal folio lines (EVA-basic)...")
    a_herbal = load_a_herbal_folio_lines(tokenize_eva_basic)
    pairs_all = build_ll_ll_pairs(a_herbal)
    print(f"     {len(a_herbal)} A-herbal folios, {len(pairs_all)} CL pairs")

    real_js, section_pct, sec_dist = run_chain_null_model(
        a_herbal, TARGET_CHAIN, n_shuffles=N_SHUFFLES, seed=SEED
    )
    _, onset_pct, ons_dist = run_onset_shuffle_null(
        a_herbal, TARGET_CHAIN, n_shuffles=N_SHUFFLES, seed=SEED+1
    )

    print(f"\n  Target chain: {' → '.join(TARGET_CHAIN)}")
    print(f"  Real chain joint-strength: {real_js:.6f}")
    print(f"  Section-shuffled percentile: {section_pct:.1f}th (>95th required)")
    print(f"  Onset-shuffled percentile:   {onset_pct:.1f}th (>95th required)")

    # Per-edge enrichments
    total = len(pairs_all)
    lf_base = Counter(a for a, b in pairs_all)
    pc = Counter(pairs_all)
    print(f"\n  Per-edge enrichments:")
    all_edges_dir = True
    for i in range(len(TARGET_CHAIN) - 1):
        a, b = TARGET_CHAIN[i], TARGET_CHAIN[i+1]
        fa = lf_base.get(a, 0) / total if total > 0 else 0
        fb = lf_base.get(b, 0) / total if total > 0 else 0
        exp_v = fa * fb * total
        obs_v = pc.get((a, b), 0)
        e_v = obs_v / exp_v if exp_v > 0 else 0
        dir_ok = e_v >= 1.5
        if not dir_ok: all_edges_dir = False
        print(f"    {a}→{b}: obs={obs_v}, E={e_v:.3f} {'(dir ✓)' if dir_ok else '(dir ✗)'}")

    f4_both_95 = section_pct >= 95.0 and onset_pct >= 95.0
    f4_both_90 = section_pct >= 90.0 and onset_pct >= 90.0
    if f4_both_95:
        f4_status = 'RETAINED'
    elif f4_both_90:
        f4_status = 'WEAKENED'
    elif section_pct >= 95.0 or onset_pct >= 95.0:
        f4_status = 'WEAKENED'
    else:
        f4_status = 'FAILED'
    print(f"\n  Pre-reg threshold: >95th both controls. Result: {f4_status}")

    # ── F5: Suffix transformation ──────────────────────────────────────────────
    sep()
    print("\n[F5] Systematic -edy suffix transformation")
    print(f"     A-suffixes: {sorted(A_SUFFIXES)}, B-suffixes: {sorted(B_SUFFIXES)}")
    print(f"     Threshold: B-suf rate in B ≥ {B_SUFFIX_FOLD_THRESHOLD}× rate in A "
          f"AND B-suf rate in B ≥ {B_SUFFIX_ABS_THRESHOLD:.0%}")

    suf_res = suffix_transformation_analysis(eva_a, eva_b)
    n_shows, n_eligible = 0, 0

    print(f"\n  {'Class':<6} {'A:Bsuf':<8} {'B:Bsuf':<8} {'fold':<6} {'n_A':<5} {'n_B':<5} Transforms")
    print(f"  {'-'*6} {'-'*8} {'-'*8} {'-'*6} {'-'*5} {'-'*5} {'-'*10}")
    for cls in ALL_ONSET_CLASSES:
        r = suf_res[cls]
        if r is None:
            print(f"  {cls:<6} — (n_A or n_B < {MIN_TOKENS_FOR_SUFFIX})")
            continue
        n_eligible += 1
        if r['shows_transform']:
            n_shows += 1
        print(f"  {cls:<6} {r['a_bsuf']:<8.4f} {r['b_bsuf']:<8.4f} "
              f"{str(r['fold']):<6} {r['n_a']:<5} {r['n_b']:<5} "
              f"{'YES' if r['shows_transform'] else 'no'}")

    pct_transform = 100.0 * n_shows / n_eligible if n_eligible else 0
    print(f"\n  Transforms: {n_shows}/{n_eligible} = {pct_transform:.1f}%")
    f5_status = ('RETAINED' if pct_transform >= 75.0
                 else ('WEAKENED' if pct_transform >= 50.0 else 'FAILED'))
    print(f"  Pre-reg threshold: ≥75%. Result: {f5_status}")

    # ── Summary ───────────────────────────────────────────────────────────────
    sep('═')
    print("\n[SUMMARY] EVA-basic vs ZL3b replication")
    sep('═')
    print(f"\n  Token delta: B={delta_b:.3f}%, A={delta_a:.3f}% (gate: <10% — PASS)")
    print(f"\n  F1 (Positional architecture):   {f1_status}")
    print(f"     Agreement {matches}/{total_charted} = {agreement_pct:.1f}%")
    print(f"\n  F2 (Terminal dialect inversion): {f2_status}")
    print(f"     A-terminals: {sorted(a_set)}")
    print(f"     B-terminals: {sorted(b_set)}")
    print(f"     Overlap: {sorted(overlap) if overlap else '∅'}")
    print(f"\n  F3 (Bigram invariants):          {f3_status}")
    print(f"     {n_replicated}/5 replicated directionally")
    print(f"\n  F4 (A-herbal chain):             {f4_status}")
    print(f"     Section-pct={section_pct:.1f}th, Onset-pct={onset_pct:.1f}th")
    print(f"\n  F5 (Suffix transformation):      {f5_status}")
    print(f"     {n_shows}/{n_eligible} classes transform = {pct_transform:.1f}%")

    statuses = [f1_status, f2_status, f3_status, f4_status, f5_status]
    n_retained = sum(1 for s in statuses if s == 'RETAINED')
    n_weakened = sum(1 for s in statuses if s == 'WEAKENED')
    n_failed   = sum(1 for s in statuses if s == 'FAILED')

    sep()
    print(f"\nR1 GATE: RETAINED={n_retained}/5  WEAKENED={n_weakened}/5  FAILED={n_failed}/5")
    if n_retained == 5:
        gate = "ALL_RETAINED — proceed to R2"
    elif n_failed == 0:
        gate = "PARTIAL_RETENTION — proceed to R2 with notes on weakened findings"
    else:
        gate = "INVESTIGATE — one or more findings failed"
    print(f"Verdict: {gate}")
    print()

    return {
        'delta_b': delta_b, 'delta_a': delta_a,
        'f1': f1_status, 'f1_pct': agreement_pct, 'f1_m': matches, 'f1_tot': total_charted,
        'f2': f2_status, 'f2_a_terms': sorted(a_set), 'f2_b_terms': sorted(b_set),
        'f3': f3_status, 'f3_n': n_replicated,
        'f4': f4_status, 'f4_sec': section_pct, 'f4_ons': onset_pct,
        'f5': f5_status, 'f5_pct': pct_transform, 'f5_n': n_shows, 'f5_tot': n_eligible,
        'gate': gate,
    }

if __name__ == '__main__':
    main()
