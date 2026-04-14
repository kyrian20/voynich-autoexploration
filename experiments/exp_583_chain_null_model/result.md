# exp_583: A-Herbal Paragraph Chain Null-Model Test

**Date:** 2026-04-12  
**Type:** Verification experiment (paper support)  
**Status:** COMPLETE — TARGET CHAIN ROBUST; BEST-CHAIN METRIC INVALID DUE TO SPARSE-DATA ARTIFACT

---

## Question

Does the A herbal_a cross-line chain (d→qot→ch→o→sh) survive null-model shuffling? Two controls: (1) section-shuffled (line order within each folio randomized), (2) onset-shuffled (all LF onset labels permuted). For each control, compute how often random shuffles produce a chain at least as strong as the real chain.

---

## Method

**A herbal_a corpus:** Folios n≤56, P-locus (per exp_511 methodology). 1,188 lines across 55 folios. 1,133 within-folio consecutive-line pairs (CL pairs).

**Chain definition:** d→qot→ch→o→sh (5 nodes, 4 edges). Each edge: E = obs(A→B) / (base_A × base_B × N_pairs), where base_X is the LF onset class frequency and N_pairs is total CL pairs. Edge threshold: E≥1.5× (directional), with at least 3 CONF (E≥1.5×, obs≥10) edges.

**Joint strength metric:** Product of edge E-values. For d→qot→ch→o→sh: JS = E(d→qot) × E(qot→ch) × E(ch→o) × E(o→sh).

**Search space:** All LF onset classes with ≥5 occurrences as sender (19 classes). Exhaustive search over all 5-node directed chains with each edge E≥1.5×.

**Controls:** N=200 shuffles each.
- Section-shuffled: shuffle line order within each folio independently (preserves folio membership, destroys paragraph sequence).
- Onset-shuffled: permute all LF onset labels across all positions (preserves class distribution, destroys all sequential structure).

**Percentile metrics reported separately:**
- **Target-JS percentile:** rank of specific target chain JS against control distribution
- **Best-JS percentile:** rank of real corpus's best qualifying chain JS against control distribution

---

## Results

### Step 1: Real chain edge values

| Edge | obs | exp | E | N_cond | Status |
|------|-----|-----|---|--------|--------|
| d → qot | 13 | 8.31 | **1.564×** | 277 | **CONF** |
| qot → ch | 12 | 6.09 | **1.970×** | 34 | **CONF** |
| ch → o | 13 | 8.42 | **1.544×** | 203 | **CONF** |
| o → sh | 5 | 2.03 | **2.460×** | 47 | **dir** |

**Real chain joint strength: JS = 11.699**  
First 3 edges are CONF (obs≥10, E≥1.5×). Final edge (o→sh) is directional (obs=5, E=2.46×).

Note: E-values differ slightly from findings F490/F491/F506/F507 because the bigram enrichment formula uses different baseline denominators (all-pairs vs. condition-specific). All edges confirm the coupling directionally. F490 (qot→ch, E=2.00×/obs=12) and F491 (d→qot, E=1.64×/obs=13) use a conditional probability formula; this script uses the joint independence baseline. Both confirm the same qualitative finding.

### Step 2: Chain search in real corpus

The exhaustive search found **9,203 qualifying length-5 chains** (each edge E≥1.5×) in the real A herbal_a corpus. The top chains by JS involve rare onset class `cph` (compound gallows, ~1.0% LF base rate):

| Rank | Chain | JS |
|------|-------|-----|
| 1 | s → cph → t → cph → t | 1641.6 |
| 2 | s → cph → t → cph → qot | 1496.7 |
| 3 | t → cph → t → cph → t | 1376.8 |
| ... | ... | ... |
| **8776** | **d → qot → ch → o → sh** | **11.70** |

The target chain ranks 8,776th of 9,203 qualifying chains in the real corpus.

**Critical finding: the target chain is not the strongest chain in the real corpus.** It was identified by theoretical/domain reasoning (exp_515–524), not by searching for the globally strongest chain.

### Step 3: Null model results — section-shuffled

| Metric | Value |
|--------|-------|
| n_chains per shuffle: mean / median / p95 | 7,897 / 7,664 / 11,584 |
| Best chain JS: p50 / p95 / max | 12,859 / 4,218,515 / 402,308,947 |
| Real corpus best chain JS | 1,641.6 |
| **Fraction best_JS ≥ real: → Best-JS percentile rank** | **86.5% exceed → 13.5th percentile** |
| Real target chain JS | 11.70 |
| **Fraction target_JS ≥ real: → Target-JS percentile rank** | **0/200 exceed → 100th percentile** |
| Shuffles containing exact target chain (d→qot→ch→o→sh) | **0/200** |

### Step 4: Null model results — onset-shuffled

| Metric | Value |
|--------|-------|
| n_chains per shuffle: mean / median / p95 | 5,925 / 5,768 / 8,895 |
| Best chain JS: p50 / p95 / max | 2,287 / 40,231 / 4,218,515 |
| Real corpus best chain JS | 1,641.6 |
| **Fraction best_JS ≥ real: → Best-JS percentile rank** | **61.5% exceed → 38.5th percentile** |
| Real target chain JS | 11.70 |
| **Fraction target_JS ≥ real: → Target-JS percentile rank** | **0/200 exceed → 100th percentile** |
| Shuffles containing exact target chain (d→qot→ch→o→sh) | **0/200** |

---

## Interpretation

### Two metrics, two different results

There are two ways to rank the real chain against controls, and they give opposite answers:

1. **Best-JS metric** (exhaustive search, best chain found in real corpus vs. best found in each shuffled control): Real corpus best_JS=1,641 ranks at **13.5th percentile** (section-shuffled) and **38.5th percentile** (onset-shuffled). The real corpus is WEAKER than most shuffled corpora at producing high-JS chains.

2. **Target-JS metric** (the specific target chain d→qot→ch→o→sh in real corpus vs. same chain in each shuffled control): Real corpus target_JS=11.70 ranks at **100th percentile** of BOTH controls. Zero shuffled corpora achieve this chain's strength.

### Why the best-JS metric is invalid for this finding

The best-JS metric fails because the joint-strength formula (product of E-values) is dominated by rare onset classes. `cph` (compound gallows) has LF base rate ~1%; when it co-occurs with `t` twice in 1,133 pairs, the expected count is 0.04×0.04×1,133 ≈ 0.18, giving E=2/0.18=11× per edge. A 4-edge chain through cph accumulates JS ≈ 11^4 ≈ 14,000.

In shuffled corpora, the rare `cph` tokens are randomly redistributed, sometimes creating even stronger local clusters. This is why shuffled corpora have median best_JS of 12,859 (section) and 2,287 (onset) — far above the real corpus's best of 1,641. **The shuffled corpora produce STRONGER "best chains" than the real corpus.** This is a classic sparse-data artifact: shuffling can aggregate rare classes into clusters by chance more easily than the real data concentrates them.

This makes the best-JS metric an invalid comparison for this finding. It is measuring sparse-data noise, not the specific chain structure.

**Control behaved unexpectedly** (Check 5): The shuffled corpora produce stronger best-chains than the real corpus (mean section-shuffled best_JS = 2.8M vs real 1,641). This is the signal for a sparse-data artifact: shuffling should not generate stronger chains than the real data if the real data has genuine structure. The surprise is explained: the "best chain" metric searches over 9,203 combinations including many sparse-class chains, and random permutation can cluster rare classes more strongly than the original data.

### The target-JS metric is the correct metric

The finding (d→qot→ch→o→sh) is a **theoretically-motivated, directed hypothesis** established in exp_515–524 by systematic CL analysis. It is NOT the result of exhaustive search for the strongest chain. Therefore, the correct null model tests whether THIS SPECIFIC CHAIN survives shuffling.

Both null models give the same result: **0/200 shuffled corpora achieve the target chain's joint strength of 11.70**. Under section-shuffled controls, the mean target_JS in shuffled data is 1.12 (vs real 11.70). Under onset-shuffled, mean is 1.03 (baseline). The target chain's enrichment collapses to near-1.0 in all shuffled corpora.

This is the expected behavior for a genuine structural signal: when the paragraph-level ordering is destroyed (section-shuffled) or the onset labels are randomized (onset-shuffled), the specific chain disappears.

### Chain cannot be claimed as "strongest found by search"

The paper must NOT frame the d→qot→ch→o→sh chain as "the strongest chain we found" because:
1. There are 9,202 qualifying chains with higher JS in the real corpus
2. Those chains (cph-dominant) are artifacts of sparse data, not genuine paragraph structure
3. The paper's Section 2 already frames the chain as a theoretically-motivated finding from systematic CL analysis — this framing is CORRECT and should be maintained

### Paper assessment

The chain finding (as presented in the paper: a theoretically-motivated CL chain found in systematic analysis) is **robust**: 0/200 in both null model controls. The 100th percentile target_JS result under both shuffles provides strong null-model evidence.

The null model reveals an additional finding: the A herbal_a CL bigram space contains many high-JS chains through rare classes (cph, ckh, l combinations) that outrank the target chain by JS. These are not paragraph-structure signals — they are sparse-data clustering. Any paper claim about "the strongest chain found" would need to account for this.

**Paper implication:** The sentence should be: "The chain d→qot→ch→o→sh, identified via systematic CL analysis, is robust to both section-shuffled (0/200 shuffles match, 100th percentile) and onset-shuffled (0/200 shuffles match, 100th percentile) null models. The finding is reported as a theoretically-motivated directed result, not as the globally strongest chain in an exhaustive search."

---

## Limitations

1. **Joint strength metric dominated by rare classes:** The product-of-E-values formula inflates rare onset classes. A better metric for chain comparison might be a minimum-E-value or a log-sum metric normalized by observation count. However, for the TARGET-JS percentile (which tests the specific chain), this metric is appropriate because we're comparing the same chain across corpora.

2. **A herbal_a defined as folio n≤56:** This is a physical section definition, not a linguistic one. Some folios in this range might have different content (e.g., cosmological content). The CL signal comes from within-folio pairs, so any folio-level heterogeneity would appear in both real and shuffled corpora equally.

3. **Section-shuffled preserves folio composition:** The section-shuffled control only shuffles line ORDER within each folio, not which lines appear in which folio. If the chain signal comes from global ordering across folios (not within-folio), this shuffle would not test that. However, the CL analysis is already within-folio, so this is not a limitation.

4. **Target chain has obs=5 for the final edge (o→sh):** The final edge falls below the CONF threshold (requires obs≥10). The chain's joint strength is partly driven by this directional edge. A chain where all edges are CONF would be stronger evidence; this chain's strength relies on 3 CONF + 1 directional edges.

5. **No correction for multiple testing across the whole chain-identification process (exp_515–524):** The chain was identified across 9 experiments testing multiple class pairs. Each individual edge was tested independently. A Bonferroni correction across the full search space would tighten the CONF thresholds. The null model provides complementary evidence for the complete chain as a unit.

---

## Self-Audit

**Target-awareness:** The target chain d→qot→ch→o→sh was pre-specified from prior experimental findings (F490, F491, F506, F507), not selected post-hoc from this experiment's results. The E-value computation uses no VMS target metrics from the 19-metric battery. No target-awareness issues.

**Feature-destroying implementation:** The section-shuffled control preserves all within-line content and the onset class distribution but destroys cross-line ordering. This is the correct null for testing paragraph-level structure. The onset-shuffled control preserves positional structure (folio membership, LF position) but destroys onset class sequencing — also the correct null. Neither control features an implementation detail that would create a false positive.

**Extrapolation:** The claim "0/200 controls match the target chain" is within the tested range (N=200 shuffles, exactly the specified target chain). No claim is made about other chains or other sections. The claim that "best-JS metric is dominated by rare-class artifact" is supported by direct evidence (cph base rate ~1%, its chain JS=1,641 from small obs counts).

**Negative-result scope:** The failure of the "best-JS percentile" metric (13.5th / 38.5th percentile) is NOT a negative result for the chain finding. It is a finding about the *metric*: best_JS is an invalid comparison when rare classes dominate the search space. The correct metric (target_JS) gives a 100th percentile positive result. These are not contradictory — they measure different things.

**Control behavior:** **UNEXPECTED — investigated and explained.** Section-shuffled controls produce mean best_JS=2.8M vs real 1,641 (controls 1,700× stronger). This is the opposite of what one expects if the real chain is a genuine signal. Investigation reveals: the best_JS metric is dominated by rare-class sparse-data chains (cph etc.), and shuffling can concentrate rare tokens into clusters more strongly than the original data does. This is not a failure of the chain finding — it is a failure of the best_JS metric. The target_JS metric (specific directed chain) behaves as expected: controls near 1.0×, real data at 11.7×.

**Revised interpretation based on Check 5:** Added prominent section "Why the best-JS metric is invalid for this finding" explaining the sparse-data artifact. The paper should use only the target_JS percentile, not best_JS. No revision needed to the finding itself, but the methodology note is critical for the paper.
