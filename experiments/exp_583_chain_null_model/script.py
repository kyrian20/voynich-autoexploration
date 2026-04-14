#!/usr/bin/env python3
"""
exp_583: A-Herbal Paragraph Chain Null-Model Test

Tests whether the A herbal_a cross-line chain (d→qot→ch→o→sh, CONF/dir)
survives null-model shuffling. Two controls:
1. Section-shuffled: shuffle line order within each folio (destroys paragraph sequence)
2. Onset-shuffled: permute all LF onset labels (destroys sequential structure)

For each control (N=200 shuffles), exhaustively search for length-5 directed
chains where each edge E≥1.5×. Report percentile rank of real chain vs controls.

A herbal_a definition: folios n≤56, P-locus (per exp_511 methodology).
"""

import re, random
from collections import defaultdict, Counter
from math import log

CORPUS = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"
N_SHUFFLES = 200
CHAIN_THRESHOLD = 1.5  # "directional" E-value threshold for chain search
SEED = 583000

ONSET_PRIORITY = [
    'qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol',
    'sch','skh','sph','d','s','y','k','t','l','r','p','f','o','e','a','n','m'
]

def get_onset(word):
    for o in ONSET_PRIORITY:
        if word.startswith(o):
            return o
    return word[0] if word else None

def folio_num(folio):
    m = re.search(r'f(\d+)', folio)
    return int(m.group(1)) if m else None

def parse_corpus_by_folio():
    """Return dict: folio_n -> list of word-lists (lines), preserving order."""
    folio_lines = defaultdict(list)
    pat = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    with open(CORPUS, encoding='utf-8') as f:
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

def build_cl_bigrams_from_folio_dict(folio_dict):
    """Build CL pairs from per-folio line lists."""
    cl_pairs = []
    for n in sorted(folio_dict):
        lines = folio_dict[n]
        lf_onsets = [get_onset(ln[-1]) for ln in lines if ln]
        for i in range(len(lf_onsets) - 1):
            if lf_onsets[i] and lf_onsets[i+1]:
                cl_pairs.append((lf_onsets[i], lf_onsets[i+1]))
    return cl_pairs

def compute_enrichments(cl_pairs, search_classes):
    """
    Compute N×N enrichment matrix for search_classes.
    E(A→B) = obs(A→B) / (base_A * base_B * N_pairs)
    """
    if not cl_pairs:
        return {}
    # LF baseline from all CL pair senders
    all_lf = [a for a, b in cl_pairs] + [cl_pairs[-1][1]]
    lf_counts = Counter(a for a, b in cl_pairs)
    lf_total = len(cl_pairs)  # N_pairs
    lf_base = {o: c / lf_total for o, c in lf_counts.items()}

    pair_counts = Counter(cl_pairs)
    N_pairs = len(cl_pairs)

    enr = {}
    for a in search_classes:
        for b in search_classes:
            base_a = lf_base.get(a, 0)
            base_b = lf_base.get(b, 0)
            if base_a == 0 or base_b == 0:
                enr[(a, b)] = 0.0
                continue
            expected = base_a * base_b * N_pairs
            obs = pair_counts.get((a, b), 0)
            enr[(a, b)] = obs / expected if expected > 0 else 0.0
    return enr

def search_chains(enr, search_classes, chain_len=5, threshold=1.5):
    """
    Search for all directed chains of length chain_len where each edge E>=threshold.
    A chain of length 5 has 5 nodes and 4 edges.
    Returns list of (chain_tuple, joint_strength) sorted by strength descending.
    joint_strength = product of edge E-values.
    """
    n_edges = chain_len - 1
    sc = search_classes

    def recurse(path, joint_e):
        if len(path) == chain_len:
            return [(tuple(path), joint_e)]
        results = []
        last = path[-1]
        for b in sc:
            e = enr.get((last, b), 0.0)
            if e >= threshold:
                results.extend(recurse(path + [b], joint_e * e))
        return results

    all_chains = []
    for start in sc:
        all_chains.extend(recurse([start], 1.0))

    all_chains.sort(key=lambda x: -x[1])
    return all_chains

def joint_strength_of_chain(enr, chain):
    """Compute joint strength (product of E-values) for a specific chain."""
    js = 1.0
    for i in range(len(chain) - 1):
        e = enr.get((chain[i], chain[i+1]), 0.0)
        js *= e
    return js

def main():
    rng = random.Random(SEED)

    print("="*70)
    print("exp_583: A-Herbal Paragraph Chain Null-Model Test")
    print("="*70)

    # ── Parse corpus ──────────────────────────────────────────────────────────
    print("\nParsing corpus...")
    folio_lines = parse_corpus_by_folio()

    # A herbal_a: folios n <= 56 (per exp_511 methodology)
    a_herbal_folio_dict = {n: lines for n, lines in folio_lines.items() if n <= 56}
    a_herbal_all = [ln for lines in a_herbal_folio_dict.values() for ln in lines]
    print(f"A herbal_a: {len(a_herbal_all)} lines across {len(a_herbal_folio_dict)} folios")

    # ── Real corpus: CL pairs and chain ──────────────────────────────────────
    real_cl_pairs = build_cl_bigrams_from_folio_dict(a_herbal_folio_dict)
    print(f"Real CL pairs (within-folio): {len(real_cl_pairs)}")

    # LF onset class distribution
    lf_counts = Counter(a for a, b in real_cl_pairs)
    lf_total = sum(lf_counts.values())
    print(f"\nTop LF onset classes (sender in CL pairs):")
    for onset, cnt in sorted(lf_counts.items(), key=lambda x: -x[1])[:12]:
        print(f"  {onset}: {cnt} ({cnt/lf_total:.1%})")

    # Define search classes: onset classes with ≥5 occurrences as LF
    search_classes = [o for o, cnt in lf_counts.items() if cnt >= 5]
    search_classes.sort(key=lambda o: -lf_counts[o])
    print(f"\nSearch space: {len(search_classes)} onset classes: {search_classes}")

    # Compute real enrichment matrix
    real_enr = compute_enrichments(real_cl_pairs, search_classes)

    # ── Step 2: Confirm chain edge values ────────────────────────────────────
    TARGET_CHAIN = ('d', 'qot', 'ch', 'o', 'sh')
    print(f"\n{'='*70}")
    print(f"TARGET CHAIN: {' → '.join(TARGET_CHAIN)}")
    print(f"{'='*70}")
    print(f"\nEdge-by-edge E-values on real A herbal_a corpus:")
    print(f"{'Edge':<20} {'obs':>6} {'exp':>8} {'E':>8} {'N cond':>8} {'status'}")
    print("-"*58)
    pair_counts_real = Counter(real_cl_pairs)
    lf_base_real = {o: c / lf_total for o, c in lf_counts.items()}
    N_pairs_real = len(real_cl_pairs)
    real_js = 1.0
    for i in range(len(TARGET_CHAIN) - 1):
        a, b = TARGET_CHAIN[i], TARGET_CHAIN[i+1]
        obs = pair_counts_real.get((a, b), 0)
        base_a = lf_base_real.get(a, 0)
        base_b = lf_base_real.get(b, 0)
        exp = base_a * base_b * N_pairs_real
        e = obs / exp if exp > 0 else 0.0
        real_js *= e
        n_cond = lf_counts.get(a, 0)
        status = 'CONF' if obs >= 10 and e >= 1.5 else ('dir' if (obs >= 5 and e >= 1.5) or (obs >= 3 and e >= 2.0) else 'sub')
        print(f"{a} → {b:<14} {obs:>6} {exp:>8.2f} {e:>8.3f}× {n_cond:>8} {status}")
    print(f"\nReal chain joint strength: {real_js:.4f}")

    # ── Also search for the best chains in real corpus ────────────────────────
    real_chains = search_chains(real_enr, search_classes, chain_len=5, threshold=CHAIN_THRESHOLD)
    print(f"\nTop 10 length-5 chains (E≥{CHAIN_THRESHOLD}× each edge) in REAL A herbal_a:")
    if real_chains:
        for i, (chain, js) in enumerate(real_chains[:10]):
            mark = " <-- TARGET" if chain == TARGET_CHAIN else ""
            edge_es = [f"{real_enr.get((chain[j], chain[j+1]), 0):.2f}×" for j in range(4)]
            print(f"  {i+1}. {' → '.join(chain):<40} JS={js:.4f}  edges=[{', '.join(edge_es)}]{mark}")
    else:
        print("  No qualifying chains found in real corpus!")

    real_best_js = real_chains[0][1] if real_chains else 0.0
    target_rank_in_real = next((i+1 for i, (c, _) in enumerate(real_chains) if c == TARGET_CHAIN), None)
    print(f"\nReal corpus: {len(real_chains)} qualifying chains")
    print(f"Target chain rank in real corpus: {target_rank_in_real}")

    # ── NULL MODEL 1: Section-shuffled ─────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"NULL MODEL 1: Section-shuffled (N={N_SHUFFLES})")
    print(f"Method: shuffle line order within each folio independently")
    print(f"{'='*70}")

    sec_shuffle_stats = []
    sec_target_found = 0  # how many shuffles contain the specific target chain

    for shuffle_idx in range(N_SHUFFLES):
        if shuffle_idx % 50 == 0:
            print(f"  Shuffle {shuffle_idx}/{N_SHUFFLES}...")
        # Shuffle lines within each folio
        shuffled_folio_dict = {}
        for n, lines in a_herbal_folio_dict.items():
            shuffled = list(lines)
            rng.shuffle(shuffled)
            shuffled_folio_dict[n] = shuffled
        # Rebuild CL pairs
        shuf_cl_pairs = build_cl_bigrams_from_folio_dict(shuffled_folio_dict)
        # Compute enrichments
        shuf_enr = compute_enrichments(shuf_cl_pairs, search_classes)
        # Search chains
        shuf_chains = search_chains(shuf_enr, search_classes, chain_len=5, threshold=CHAIN_THRESHOLD)
        best_js = shuf_chains[0][1] if shuf_chains else 0.0
        n_chains = len(shuf_chains)
        target_js = joint_strength_of_chain(shuf_enr, TARGET_CHAIN)
        target_found = any(c == TARGET_CHAIN for c, _ in shuf_chains)
        if target_found:
            sec_target_found += 1
        sec_shuffle_stats.append({
            'best_js': best_js,
            'n_chains': n_chains,
            'target_js': target_js,
            'target_found': target_found,
        })

    # Analyze section-shuffled results
    sec_best_js_list = [s['best_js'] for s in sec_shuffle_stats]
    sec_n_chains_list = [s['n_chains'] for s in sec_shuffle_stats]
    sec_target_js_list = [s['target_js'] for s in sec_shuffle_stats]

    sec_best_js_sorted = sorted(sec_best_js_list)
    sec_real_best_pctile = sum(1 for v in sec_best_js_list if v >= real_best_js) / N_SHUFFLES
    sec_real_target_pctile = sum(1 for v in sec_target_js_list if v >= real_js) / N_SHUFFLES

    print(f"\n--- Section-shuffled results ---")
    print(f"N shuffles: {N_SHUFFLES}")
    print(f"n_chains per shuffle: mean={sum(sec_n_chains_list)/N_SHUFFLES:.1f}, "
          f"median={sorted(sec_n_chains_list)[N_SHUFFLES//2]}, "
          f"p95={sorted(sec_n_chains_list)[int(0.95*N_SHUFFLES)]}")
    print(f"Best chain JS per shuffle: mean={sum(sec_best_js_list)/N_SHUFFLES:.4f}, "
          f"p50={sec_best_js_sorted[N_SHUFFLES//2]:.4f}, "
          f"p95={sec_best_js_sorted[int(0.95*N_SHUFFLES)]:.4f}, "
          f"max={max(sec_best_js_list):.4f}")
    print(f"Real corpus best chain JS: {real_best_js:.4f}")
    print(f"Fraction of shuffles with best_JS >= real: {sec_real_best_pctile:.4f} "
          f"(percentile rank: {(1-sec_real_best_pctile)*100:.1f}%)")
    print(f"Target chain JS per shuffle: mean={sum(sec_target_js_list)/N_SHUFFLES:.4f}")
    print(f"Real target chain JS: {real_js:.4f}")
    print(f"Fraction of shuffles with target_JS >= real: {sec_real_target_pctile:.4f} "
          f"(percentile rank: {(1-sec_real_target_pctile)*100:.1f}%)")
    print(f"Shuffles containing exact target chain: {sec_target_found}/{N_SHUFFLES}")

    # ── NULL MODEL 2: Onset-shuffled ───────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"NULL MODEL 2: Onset-shuffled (N={N_SHUFFLES})")
    print(f"Method: permute all LF onset labels while preserving folio/line structure")
    print(f"{'='*70}")

    # Extract all LF onsets in order
    all_lf_onsets_by_folio = []
    folio_order = sorted(a_herbal_folio_dict.keys())
    line_lf_index = []  # (folio_n, line_i) → index in flat list
    flat_lf_onsets = []
    for n in folio_order:
        for i, ln in enumerate(a_herbal_folio_dict[n]):
            onset = get_onset(ln[-1]) if ln else None
            line_lf_index.append((n, i))
            flat_lf_onsets.append(onset)

    onset_shuffle_stats = []
    onset_target_found = 0

    for shuffle_idx in range(N_SHUFFLES):
        if shuffle_idx % 50 == 0:
            print(f"  Shuffle {shuffle_idx}/{N_SHUFFLES}...")
        # Permute LF onsets
        shuffled_onsets = list(flat_lf_onsets)
        rng.shuffle(shuffled_onsets)
        # Rebuild CL pairs from shuffled LF onsets
        # Map back to folio structure
        folio_lf_sequences = defaultdict(list)
        for idx, (n, i) in enumerate(line_lf_index):
            folio_lf_sequences[n].append(shuffled_onsets[idx])
        # Build CL pairs
        shuf_cl_pairs = []
        for n in folio_order:
            lf_seq = folio_lf_sequences[n]
            for i in range(len(lf_seq) - 1):
                if lf_seq[i] and lf_seq[i+1]:
                    shuf_cl_pairs.append((lf_seq[i], lf_seq[i+1]))
        # Compute enrichments
        shuf_enr = compute_enrichments(shuf_cl_pairs, search_classes)
        # Search chains
        shuf_chains = search_chains(shuf_enr, search_classes, chain_len=5, threshold=CHAIN_THRESHOLD)
        best_js = shuf_chains[0][1] if shuf_chains else 0.0
        n_chains = len(shuf_chains)
        target_js = joint_strength_of_chain(shuf_enr, TARGET_CHAIN)
        target_found = any(c == TARGET_CHAIN for c, _ in shuf_chains)
        if target_found:
            onset_target_found += 1
        onset_shuffle_stats.append({
            'best_js': best_js,
            'n_chains': n_chains,
            'target_js': target_js,
            'target_found': target_found,
        })

    # Analyze onset-shuffled results
    onset_best_js_list = [s['best_js'] for s in onset_shuffle_stats]
    onset_n_chains_list = [s['n_chains'] for s in onset_shuffle_stats]
    onset_target_js_list = [s['target_js'] for s in onset_shuffle_stats]

    onset_best_js_sorted = sorted(onset_best_js_list)
    onset_real_best_pctile = sum(1 for v in onset_best_js_list if v >= real_best_js) / N_SHUFFLES
    onset_real_target_pctile = sum(1 for v in onset_target_js_list if v >= real_js) / N_SHUFFLES

    print(f"\n--- Onset-shuffled results ---")
    print(f"n_chains per shuffle: mean={sum(onset_n_chains_list)/N_SHUFFLES:.1f}, "
          f"median={sorted(onset_n_chains_list)[N_SHUFFLES//2]}, "
          f"p95={sorted(onset_n_chains_list)[int(0.95*N_SHUFFLES)]}")
    print(f"Best chain JS per shuffle: mean={sum(onset_best_js_list)/N_SHUFFLES:.4f}, "
          f"p50={onset_best_js_sorted[N_SHUFFLES//2]:.4f}, "
          f"p95={onset_best_js_sorted[int(0.95*N_SHUFFLES)]:.4f}, "
          f"max={max(onset_best_js_list):.4f}")
    print(f"Real corpus best chain JS: {real_best_js:.4f}")
    print(f"Fraction of shuffles with best_JS >= real: {onset_real_best_pctile:.4f} "
          f"(percentile rank: {(1-onset_real_best_pctile)*100:.1f}%)")
    print(f"Target chain JS per shuffle: mean={sum(onset_target_js_list)/N_SHUFFLES:.4f}")
    print(f"Real target chain JS: {real_js:.4f}")
    print(f"Fraction of shuffles with target_JS >= real: {onset_real_target_pctile:.4f} "
          f"(percentile rank: {(1-onset_real_target_pctile)*100:.1f}%)")
    print(f"Shuffles containing exact target chain: {onset_target_found}/{N_SHUFFLES}")

    # ── Save CSV ───────────────────────────────────────────────────────────────
    import csv, os
    out_dir = '/Users/asash/voynich-cryptanalyst/state'
    csv_path = os.path.join(out_dir, 'chain_null_model_controls.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['shuffle_type', 'shuffle_idx', 'n_chains', 'best_js', 'target_js', 'target_found'])
        for i, s in enumerate(sec_shuffle_stats):
            writer.writerow(['section', i, s['n_chains'], f"{s['best_js']:.6f}",
                           f"{s['target_js']:.6f}", int(s['target_found'])])
        for i, s in enumerate(onset_shuffle_stats):
            writer.writerow(['onset', i, s['n_chains'], f"{s['best_js']:.6f}",
                           f"{s['target_js']:.6f}", int(s['target_found'])])
    print(f"\nControl data saved to: {csv_path}")

    # ── Save report ─────────────────────────────────────────────────────────────
    report_path = os.path.join(out_dir, 'chain_null_model_report.md')
    with open(report_path, 'w') as f:
        f.write("# Chain Null-Model Report — exp_583\n\n")
        f.write(f"**Generated:** 2026-04-12  \n")
        f.write(f"**Target chain:** d → qot → ch → o → sh  \n")
        f.write(f"**N shuffles per control:** {N_SHUFFLES}  \n")
        f.write(f"**Chain threshold:** E≥{CHAIN_THRESHOLD}× per edge  \n\n")

        f.write("## Real A herbal_a Chain\n\n")
        f.write(f"| Edge | obs | exp | E | N_cond | Status |\n")
        f.write(f"|------|-----|-----|---|--------|--------|\n")
        pair_counts_real = Counter(real_cl_pairs)
        for i in range(len(TARGET_CHAIN) - 1):
            a, b = TARGET_CHAIN[i], TARGET_CHAIN[i+1]
            obs = pair_counts_real.get((a, b), 0)
            base_a = lf_base_real.get(a, 0)
            base_b = lf_base_real.get(b, 0)
            exp_val = base_a * base_b * N_pairs_real
            e = obs / exp_val if exp_val > 0 else 0.0
            n_cond = lf_counts.get(a, 0)
            status = 'CONF' if obs >= 10 and e >= 1.5 else ('dir' if (obs >= 5 and e >= 1.5) or (obs >= 3 and e >= 2.0) else 'sub')
            f.write(f"| {a} → {b} | {obs} | {exp_val:.2f} | {e:.3f}× | {n_cond} | {status} |\n")
        f.write(f"\n**Real chain joint strength:** {real_js:.4f}\n\n")
        f.write(f"**Real corpus best chain JS (over all {len(real_chains)} qualifying chains):** {real_best_js:.4f}\n\n")

        f.write("## Top 10 Qualifying Chains in Real Corpus\n\n")
        f.write(f"| Rank | Chain | Joint Strength | Notes |\n")
        f.write(f"|------|-------|---------------|-------|\n")
        for i, (chain, js) in enumerate(real_chains[:10]):
            mark = "TARGET" if chain == TARGET_CHAIN else ""
            f.write(f"| {i+1} | {' → '.join(chain)} | {js:.4f} | {mark} |\n")
        f.write("\n")

        f.write("## Section-Shuffled Control\n\n")
        f.write(f"| Metric | Value |\n|--------|-------|\n")
        f.write(f"| N shuffles | {N_SHUFFLES} |\n")
        f.write(f"| Mean qualifying chains | {sum(sec_n_chains_list)/N_SHUFFLES:.1f} |\n")
        f.write(f"| p50 best_JS | {sec_best_js_sorted[N_SHUFFLES//2]:.4f} |\n")
        f.write(f"| p95 best_JS | {sec_best_js_sorted[int(0.95*N_SHUFFLES)]:.4f} |\n")
        f.write(f"| Max best_JS | {max(sec_best_js_list):.4f} |\n")
        f.write(f"| Real best_JS | {real_best_js:.4f} |\n")
        f.write(f"| Fraction best_JS ≥ real | {sec_real_best_pctile:.4f} |\n")
        f.write(f"| **Best_JS percentile rank** | **{(1-sec_real_best_pctile)*100:.1f}%** |\n")
        f.write(f"| Real target_JS | {real_js:.4f} |\n")
        f.write(f"| Fraction target_JS ≥ real | {sec_real_target_pctile:.4f} |\n")
        f.write(f"| **Target_JS percentile rank** | **{(1-sec_real_target_pctile)*100:.1f}%** |\n")
        f.write(f"| Shuffles with exact target chain | {sec_target_found}/{N_SHUFFLES} |\n\n")

        f.write("## Onset-Shuffled Control\n\n")
        f.write(f"| Metric | Value |\n|--------|-------|\n")
        f.write(f"| N shuffles | {N_SHUFFLES} |\n")
        f.write(f"| Mean qualifying chains | {sum(onset_n_chains_list)/N_SHUFFLES:.1f} |\n")
        f.write(f"| p50 best_JS | {onset_best_js_sorted[N_SHUFFLES//2]:.4f} |\n")
        f.write(f"| p95 best_JS | {onset_best_js_sorted[int(0.95*N_SHUFFLES)]:.4f} |\n")
        f.write(f"| Max best_JS | {max(onset_best_js_list):.4f} |\n")
        f.write(f"| Real best_JS | {real_best_js:.4f} |\n")
        f.write(f"| Fraction best_JS ≥ real | {onset_real_best_pctile:.4f} |\n")
        f.write(f"| **Best_JS percentile rank** | **{(1-onset_real_best_pctile)*100:.1f}%** |\n")
        f.write(f"| Real target_JS | {real_js:.4f} |\n")
        f.write(f"| Fraction target_JS ≥ real | {onset_real_target_pctile:.4f} |\n")
        f.write(f"| **Target_JS percentile rank** | **{(1-onset_real_target_pctile)*100:.1f}%** |\n")
        f.write(f"| Shuffles with exact target chain | {onset_target_found}/{N_SHUFFLES} |\n\n")

        f.write("## Falsifiability Statement\n\n")
        f.write("The finding would be falsified if the real chain falls in the body of either control distribution "
                "(i.e., if many shuffle iterations produce equally strong or stronger chains by chance). "
                "Concretely: if >5% of shuffles produce a best_JS ≥ real_best_JS, the finding is not robust "
                "against that shuffle type.\n\n")
        f.write(f"Section-shuffled: {sec_real_best_pctile*100:.1f}% of shuffles exceed real best_JS "
                f"→ {'FAILS robustness' if sec_real_best_pctile > 0.05 else 'ROBUST at 5% level'}\n\n")
        f.write(f"Onset-shuffled: {onset_real_best_pctile*100:.1f}% of shuffles exceed real best_JS "
                f"→ {'FAILS robustness' if onset_real_best_pctile > 0.05 else 'ROBUST at 5% level'}\n\n")

    print(f"Report saved to: {report_path}")

    # ── Final summary ───────────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")
    print(f"Real chain: d → qot → ch → o → sh, JS={real_js:.4f}")
    print(f"Real best chain JS: {real_best_js:.4f}")
    print(f"\nSection-shuffled (N={N_SHUFFLES}):")
    print(f"  Best-JS percentile rank: {(1-sec_real_best_pctile)*100:.1f}%")
    print(f"  Target-JS percentile rank: {(1-sec_real_target_pctile)*100:.1f}%")
    print(f"  Exact target chain found in: {sec_target_found}/{N_SHUFFLES} shuffles")
    print(f"\nOnset-shuffled (N={N_SHUFFLES}):")
    print(f"  Best-JS percentile rank: {(1-onset_real_best_pctile)*100:.1f}%")
    print(f"  Target-JS percentile rank: {(1-onset_real_target_pctile)*100:.1f}%")
    print(f"  Exact target chain found in: {onset_target_found}/{N_SHUFFLES} shuffles")

    # Assess robustness
    sec_robust = sec_real_best_pctile <= 0.05
    onset_robust = onset_real_best_pctile <= 0.05
    sec_top1 = sec_real_best_pctile <= 0.01
    onset_top1 = onset_real_best_pctile <= 0.01

    print(f"\nRobustness assessment (using best_JS as comparison metric):")
    print(f"  Section-shuffled: {'ROBUST (top 5%)' if sec_robust else 'NOT ROBUST'}, {'top 1%' if sec_top1 else 'not top 1%'}")
    print(f"  Onset-shuffled:   {'ROBUST (top 5%)' if onset_robust else 'NOT ROBUST'}, {'top 1%' if onset_top1 else 'not top 1%'}")

if __name__ == '__main__':
    main()
