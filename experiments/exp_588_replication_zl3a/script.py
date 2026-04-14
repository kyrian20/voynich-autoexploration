#!/usr/bin/env python3
"""
exp_588: Transliteration Replication — Session R3 (ZL3a, tiebreaker)

ZL3a is an earlier version of the ZL EVA transliteration (version 3a, 2023-02-04).
It differs from ZL3b (version 3b, 2025-05-13) primarily in uncertainty annotations,
some corrected readings, and line-break positions. Same alphabet and classifiers.

R3 is triggered because R1 (EVA-basic) RETAINED and R2 (v101) FAILED for F4.
ZL3a serves as tiebreaker: if ZL3a RETAINS F4, the overall verdict is RETAINED (2/3).

This session runs all 5 findings for completeness, using the same methodology as
exp_586 (EVA-basic) but with the ZL3a file instead of ZL3b.

Plan reference: transliteration_replication_plan.md §7.4, §8.2 (R3_ZL3a_conditional).
"""

import sys, os, re, random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / 'state'))

from voynich_constraints import (
    load_vms_corpus, tokenize, get_onset, get_suffix,
    positional_enrichment, bigram_enrichment,
    iter_all_words, iter_slot_words,
)

ZL3A_PATH = str(ROOT / 'data' / 'transcriptions' / 'zl3a.txt')
ZL3B_PATH = str(ROOT / 'data' / 'transcriptions' / 'eva_zl3b.txt')
SEED = 588000

ALL_ONSET_CLASSES = [
    'qok', 'qot', 'qo', 'cth', 'sch', 'ckh', 'cph',
    'ch', 'sh', 'ok', 'ot', 'ol',
    'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'a', 'o',
]

CONF_E  = 1.5
CONF_N  = 20
A_HERBAL_MAX_FOLIO = 56

# ZL3b F1 classifications (from exp_586 baseline)
ZL3B_F1_CLASSES = {
    'qok': 'mid', 'qot': 'mid', 'qo': 'mid',
    'cth': 'rare', 'sch': 'rare', 'ckh': 'rare', 'cph': 'rare',
    'ch': 'mid', 'sh': 'mid',
    'ok': 'mid', 'ot': 'mid', 'ol': 'mid',
    'd': 'opener', 's': 'opener', 'y': 'opener', 'k': 'mid', 't': 'opener',
    'l': 'terminal', 'r': 'terminal', 'p': 'opener', 'f': 'rare',
    'a': 'terminal', 'o': 'terminal',
}

def sep(char='─', width=70): print(char * width)

# ── F1: Positional architecture ──────────────────────────────────────────────

def classify_positional_architecture(corpus):
    result = {}
    for cls in ALL_ONSET_CLASSES:
        e_lf, obs_lf, _ = positional_enrichment(corpus, cls, 'LF')
        e_ll, obs_ll, _ = positional_enrichment(corpus, cls, 'LL')
        if obs_lf < CONF_N and obs_ll < CONF_N:
            result[cls] = 'rare'
            continue
        lf_conf = (e_lf == e_lf) and (e_lf >= CONF_E) and (obs_lf >= CONF_N)
        ll_conf = (e_ll == e_ll) and (e_ll >= CONF_E) and (obs_ll >= CONF_N)
        if lf_conf and not ll_conf:   cat = 'opener'
        elif ll_conf and not lf_conf: cat = 'terminal'
        elif lf_conf and ll_conf:     cat = 'opener' if e_lf >= e_ll else 'terminal'
        else:                         cat = 'mid'
        result[cls] = cat
    return result

# ── F2: Terminal sets ─────────────────────────────────────────────────────────

def get_conf_terminals(corpus):
    result = {}
    for cls in ALL_ONSET_CLASSES:
        e, obs, _ = positional_enrichment(corpus, cls, 'LL')
        if (e == e) and (e >= CONF_E) and (obs >= CONF_N):
            result[cls] = (round(e, 3), obs)
    return result

# ── F3: Bigram invariants ─────────────────────────────────────────────────────

BIGRAM_INVARIANTS = [
    ('y',   'y',   'elevated'),
    ('sh',  'qok', 'elevated'),
    ('ok',  'ok',  'elevated'),
    ('qok', 's',   'elevated'),
    ('sh',  'ch',  'depleted'),
]

def compute_bigram_invariants(a_corp, b_corp):
    results = {}
    for (sender, receiver, direction) in BIGRAM_INVARIANTS:
        ae, ao, _ = bigram_enrichment(a_corp, sender, receiver)
        be, bo, _ = bigram_enrichment(b_corp, sender, receiver)
        if direction == 'elevated':
            a_ok = (ae == ae) and ae > 1.0
            b_ok = (be == be) and be > 1.0
        else:
            a_ok = (ae == ae) and ae < 1.0
            b_ok = (be == be) and be < 1.0
        results[f'{sender}→{receiver}'] = {
            'direction': direction,
            'A_E': round(ae, 3) if ae == ae else float('nan'),
            'B_E': round(be, 3) if be == be else float('nan'),
            'A_ok': a_ok, 'B_ok': b_ok,
            'replicated': a_ok and b_ok,
        }
    return results

# ── F4: A-herbal paragraph chain ─────────────────────────────────────────────

TARGET_CHAIN = ['d', 'qot', 'ch', 'o', 'sh']

def load_a_herbal_folio_lines(path, max_folio=A_HERBAL_MAX_FOLIO):
    """Load A-dialect herbal folio lines for CL chain analysis."""
    raw = defaultdict(list)
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            parts = line.split(None, 1)
            if len(parts) < 2: continue
            locus_raw, text = parts
            lparts = locus_raw.split(',')
            if len(lparts) < 2: continue
            folio_base = lparts[0].split('.')[0].lstrip('<')
            m = re.match(r'f(\d+)', folio_base)
            if not m: continue
            fnum = int(m.group(1))
            if fnum > max_folio: continue
            lt = lparts[1].rstrip('>').lstrip('@+*=~&')
            if not lt.startswith('P'): continue
            words = tokenize(text)
            if words: raw[fnum].append(words)

    out = {}
    for fnum, lines in raw.items():
        all_words = [w for wl in lines for w in wl]
        if len(all_words) < 10: continue
        edy_rate = sum(1 for w in all_words if 'edy' in w or 'eedy' in w) / len(all_words)
        if edy_rate < 0.05:
            out[fnum] = lines
    return out

def build_ll_ll_pairs(folio_lines):
    pairs = []
    for fnum in sorted(folio_lines):
        lines = folio_lines[fnum]
        ll_onsets = [get_onset(l[-1]) for l in lines if l]
        for i in range(len(ll_onsets) - 1):
            pairs.append((ll_onsets[i], ll_onsets[i+1]))
    return pairs

def chain_strength(pairs, chain):
    if not pairs: return 0.0
    total = len(pairs)
    lf_base = Counter(a for a,b in pairs)
    pc = Counter(pairs)
    js = 1.0
    for i in range(len(chain) - 1):
        a, b = chain[i], chain[i+1]
        fa = lf_base.get(a, 0) / total
        fb = lf_base.get(b, 0) / total
        if fa == 0 or fb == 0: return 0.0
        obs = pc.get((a, b), 0)
        js *= obs / (fa * fb * total)
    return js

def run_section_shuffle(folio_lines, target_chain, n=200, seed=SEED):
    rng = random.Random(seed)
    real_pairs = build_ll_ll_pairs(folio_lines)
    real_js = chain_strength(real_pairs, target_chain)
    null = []
    for _ in range(n):
        shuf = {fnum: list(lines) for fnum, lines in folio_lines.items()}
        for fnum in shuf: rng.shuffle(shuf[fnum])
        null.append(chain_strength(build_ll_ll_pairs(shuf), target_chain))
    pct = sum(1 for v in null if real_js > v) / n * 100
    return real_js, pct

def run_onset_shuffle(folio_lines, target_chain, n=200, seed=SEED+1):
    rng = random.Random(seed)
    real_pairs = build_ll_ll_pairs(folio_lines)
    real_js = chain_strength(real_pairs, target_chain)
    null = []
    for _ in range(n):
        all_onsets = [a for a,b in real_pairs] + ([real_pairs[-1][1]] if real_pairs else [])
        perm = list(all_onsets); rng.shuffle(perm)
        shuf = [(perm[i], perm[i+1]) for i in range(len(real_pairs))]
        null.append(chain_strength(shuf, target_chain))
    pct = sum(1 for v in null if real_js > v) / n * 100
    return real_js, pct

# ── F5: Suffix transformation ─────────────────────────────────────────────────

B_SUFFIXES = {'edy', 'eedy'}
A_SUFFIXES = {'ol', 'or', 'ey'}
B_SUFFIX_FOLD_THRESHOLD = 3.0
B_SUFFIX_ABS_THRESHOLD  = 0.05
MIN_TOKENS_FOR_SUFFIX   = 20

def suffix_transformation_analysis(a_corp, b_corp):
    def suf_rate(corpus, cls, suf_set):
        words = [w for _, ws in corpus for w in ws if get_onset(w) == cls]
        if not words: return 0.0, 0
        hits = sum(1 for w in words if any(w.endswith(s) for s in suf_set))
        return hits / len(words), len(words)

    results = {}
    for cls in ALL_ONSET_CLASSES:
        a_b, n_a = suf_rate(a_corp, cls, B_SUFFIXES)
        b_b, n_b = suf_rate(b_corp, cls, B_SUFFIXES)
        a_a, _   = suf_rate(a_corp, cls, A_SUFFIXES)
        b_a, _   = suf_rate(b_corp, cls, A_SUFFIXES)
        if n_a < MIN_TOKENS_FOR_SUFFIX or n_b < MIN_TOKENS_FOR_SUFFIX:
            results[cls] = None; continue
        fold = (b_b / a_b) if a_b > 0 else float('inf')
        shows = (b_b >= B_SUFFIX_ABS_THRESHOLD) and ((a_b == 0) or (fold >= B_SUFFIX_FOLD_THRESHOLD))
        results[cls] = {
            'shows_transform': shows,
            'a_bsuf': round(a_b, 4), 'b_bsuf': round(b_b, 4),
            'fold': round(fold, 1) if a_b > 0 else '∞', 'n_a': n_a, 'n_b': n_b,
        }
    return results

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    sep('═')
    print("exp_588: Transliteration Replication — Session R3 (ZL3a tiebreaker)")
    sep('═')
    print("  Tiebreaker triggered: R1 (EVA-basic) RETAINED F4; R2 (v101) FAILED F4")
    print("  ZL3a result determines overall F4 classification (need 2/3 to RETAIN)")

    # ── Load corpora ──────────────────────────────────────────────────────────
    print("\n[1] Loading ZL3a and ZL3b corpora...")
    zl3b_b = load_vms_corpus(ZL3B_PATH, dialect='B')
    zl3b_a = load_vms_corpus(ZL3B_PATH, dialect='A')
    zl3a_b = load_vms_corpus(ZL3A_PATH, dialect='B')
    zl3a_a = load_vms_corpus(ZL3A_PATH, dialect='A')

    n_3b_b = sum(len(w) for _,w in zl3b_b)
    n_3b_a = sum(len(w) for _,w in zl3b_a)
    n_3a_b = sum(len(w) for _,w in zl3a_b)
    n_3a_a = sum(len(w) for _,w in zl3a_a)
    db = abs(n_3b_b - n_3a_b) / n_3b_b * 100
    da = abs(n_3b_a - n_3a_a) / n_3b_a * 100
    print(f"  ZL3b B: {n_3b_b:,} tokens; ZL3a B: {n_3a_b:,} tokens (delta={db:.2f}%)")
    print(f"  ZL3b A: {n_3b_a:,} tokens; ZL3a A: {n_3a_a:,} tokens (delta={da:.2f}%)")

    # ── F1: Positional architecture ───────────────────────────────────────────
    sep()
    print("\n[F1] Three-layer positional architecture")
    zl3a_cls = classify_positional_architecture(zl3a_b)
    print(f"  {'Class':<8} {'ZL3b':<12} {'ZL3a':<12} Match")
    print(f"  {'-'*8} {'-'*12} {'-'*12} -----")
    matches = 0; total_charted = 0
    for cls in ALL_ONSET_CLASSES:
        z_cat = ZL3B_F1_CLASSES[cls]; a_cat = zl3a_cls[cls]
        if z_cat == 'rare' and a_cat == 'rare':
            print(f"  {cls:<8} {z_cat:<12} {a_cat:<12} — (rare)"); continue
        total_charted += 1
        m = (z_cat == a_cat)
        if m: matches += 1
        print(f"  {cls:<8} {z_cat:<12} {a_cat:<12} {'YES' if m else 'NO'}")
    agr = 100.0 * matches / total_charted if total_charted else 0
    print(f"\n  Agreement: {matches}/{total_charted} = {agr:.1f}%")
    f1_status = 'RETAINED' if agr >= 75.0 and matches >= 15 else ('WEAKENED' if agr >= 50.0 else 'FAILED')
    print(f"  Result: {f1_status}")

    # ── F2: Terminal inversion ────────────────────────────────────────────────
    sep()
    print("\n[F2] Terminal-layer dialect inversion")
    a_terms = get_conf_terminals(zl3a_a)
    b_terms = get_conf_terminals(zl3a_b)
    print("\n  A-dialect CONF terminals:")
    for cls,(e,obs) in sorted(a_terms.items(), key=lambda x:-x[1][0]):
        print(f"    {cls:<8} E={e:.3f} (n={obs})")
    if not a_terms: print("    (none)")
    print("  B-dialect CONF terminals:")
    for cls,(e,obs) in sorted(b_terms.items(), key=lambda x:-x[1][0]):
        print(f"    {cls:<8} E={e:.3f} (n={obs})")
    if not b_terms: print("    (none)")
    a_set = set(a_terms.keys()); b_set = set(b_terms.keys())
    overlap = a_set & b_set
    d_in_a = 'd' in a_set
    b_member = len({'r','l','ol','o','a'} & b_set) > 0
    print(f"\n  Overlap: {overlap if overlap else '∅ (zero overlap)'}")
    print(f"  d ∈ A-terminals: {d_in_a}")
    b_canonical = {'r','l','ol','o','a'}
    print(f"  B-canonical ∩ B-terminals: {b_canonical & b_set}")
    f2_retained = (len(overlap) == 0) and d_in_a and b_member
    f2_status = 'RETAINED' if f2_retained else 'FAILED'
    print(f"  Result: {f2_status}")

    # ── F3: Bigram invariants ─────────────────────────────────────────────────
    sep()
    print("\n[F3] Bigram matrix cross-dialect invariants")
    brs = compute_bigram_invariants(zl3a_a, zl3a_b)
    print(f"  {'Pair':<12} {'Direction':<10} {'A_E':<8} {'B_E':<8} Rep")
    n_rep = 0
    for key, r in brs.items():
        a_e = f"{r['A_E']:.3f}{'✓' if r['A_ok'] else '✗'}"
        b_e = f"{r['B_E']:.3f}{'✓' if r['B_ok'] else '✗'}"
        if r['replicated']: n_rep += 1
        print(f"  {key:<12} {r['direction']:<10} {a_e:<8} {b_e:<8} {'YES' if r['replicated'] else 'NO'}")
    print(f"\n  Replicated: {n_rep}/{len(brs)}")
    f3_status = 'RETAINED' if n_rep >= 4 else ('WEAKENED' if n_rep >= 3 else 'FAILED')
    print(f"  Result: {f3_status}")

    # ── F4: A-herbal paragraph chain ─────────────────────────────────────────
    sep()
    print("\n[F4] A-herbal paragraph chain d→qot→ch→o→sh  ← TIEBREAKER")
    herbal = load_a_herbal_folio_lines(ZL3A_PATH)
    all_pairs = build_ll_ll_pairs(herbal)
    print(f"  Loaded: {len(herbal)} A-herbal folios, {len(all_pairs)} CL pairs")

    real_js_sec, pct_sec = run_section_shuffle(herbal, TARGET_CHAIN)
    real_js_ons, pct_ons = run_onset_shuffle(herbal, TARGET_CHAIN)

    print(f"  Section-shuffled: JS={real_js_sec:.4f} at {pct_sec:.1f}th percentile")
    print(f"  Onset-shuffled:   JS={real_js_ons:.4f} at {pct_ons:.1f}th percentile")

    # Per-edge
    pc = Counter(all_pairs); total = len(all_pairs)
    lf_base = Counter(a for a,b in all_pairs)
    print("  Per-edge enrichments:")
    for i in range(len(TARGET_CHAIN)-1):
        a,b = TARGET_CHAIN[i], TARGET_CHAIN[i+1]
        fa = lf_base.get(a,0)/total if total else 0
        fb = lf_base.get(b,0)/total if total else 0
        obs = pc.get((a,b),0)
        e = obs/(fa*fb*total) if fa>0 and fb>0 and total>0 else 0.0
        print(f"    {a}→{b}: E={e:.3f} (obs={obs})")

    f4_retained = (pct_sec > 95.0) and (pct_ons > 95.0)
    f4_status = 'RETAINED' if f4_retained else ('WEAKENED' if pct_sec > 90.0 and pct_ons > 90.0 else 'FAILED')
    print(f"  Pre-reg threshold: >95th pct both controls. Result: {f4_status}")

    # Overall F4 verdict across R1+R2+R3
    print("\n  Overall F4 verdict (R1=EVA-basic RETAINED, R2=v101 FAILED, R3=ZL3a):")
    retained_count = 1 + (1 if f4_retained else 0)  # R1 always retained
    v101_pct_sec = 77.0; v101_pct_ons = 86.5  # from exp_587
    if f4_retained:
        print(f"  R1=RETAINED, R2=FAILED, R3={f4_status} → 2/3 RETAINED → F4 OVERALL: RETAINED")
    elif pct_sec > 90.0 and pct_ons > 90.0:
        print(f"  R1=RETAINED, R2=FAILED, R3=WEAKENED → WEAKENED overall")
    else:
        print(f"  R1=RETAINED, R2=FAILED, R3=FAILED → R2+R3 both below 90th → F4 OVERALL: FAILED")

    # ── F5: Suffix transformation ─────────────────────────────────────────────
    sep()
    print("\n[F5] Systematic -edy suffix transformation")
    f5_results = suffix_transformation_analysis(zl3a_a, zl3a_b)
    n_trans = 0; n_tested = 0
    print(f"  {'Class':<8} {'A:Bsuf':<10} {'B:Bsuf':<10} {'fold':<8} Transforms")
    for cls in ALL_ONSET_CLASSES:
        r = f5_results[cls]
        if r is None: print(f"  {cls:<8} — (insuff)"); continue
        n_tested += 1
        t = 'YES' if r['shows_transform'] else 'NO'
        if r['shows_transform']: n_trans += 1
        print(f"  {cls:<8} {r['a_bsuf']:<10.3f} {r['b_bsuf']:<10.3f} {str(r['fold'])+'×':<8} {t}")
    pct_t = 100.0 * n_trans / n_tested if n_tested else 0
    print(f"\n  Transforms: {n_trans}/{n_tested} = {pct_t:.1f}%")
    f5_status = 'RETAINED' if pct_t >= 75.0 else ('WEAKENED' if pct_t >= 50.0 else 'FAILED')
    print(f"  Result: {f5_status}")

    # ── Summary ───────────────────────────────────────────────────────────────
    sep('═')
    print("\n[SUMMARY] ZL3a Replication Results (R3 tiebreaker)")
    sep('═')
    for name, st in [
        ('F1 Positional architecture', f1_status),
        ('F2 Terminal inversion',       f2_status),
        ('F3 Bigram invariants',        f3_status),
        ('F4 A-herbal chain',           f4_status),
        ('F5 Suffix transformation',    f5_status),
    ]:
        print(f"  {name:<30} {st}")

    all_ret = all(s == 'RETAINED' for s in [f1_status, f2_status, f3_status, f4_status, f5_status])
    print(f"\n  R3 gate: {'ALL_RETAINED' if all_ret else 'PARTIAL'}")

if __name__ == '__main__':
    main()
