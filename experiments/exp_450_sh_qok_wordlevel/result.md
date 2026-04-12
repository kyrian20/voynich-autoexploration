# exp_450: sh→qok Bigram Word-Level Analysis (H522)

**Hypothesis (H522, archived):** The sh→qok enrichment in B MID (E=1.97×, F372) is driven by she-body sh-words ('she-' prefix), not by specific word-type pairs. The qok successor is class-uniform. F372 claims: "sh→qok = 'she-' body sh subclass → qok-class uniform successor."

**Note:** H522 was previously RESOLVED → F372 (exp_370). This experiment provides a high-N confirmation with subtype breakdown and cross-dialectal extension.

---

## Results

### B-dialect (confirmed at N=263, E=1.96×)

| she-body sh-word | N(sh→qok) | N(sh→any) | qok_rate | E vs baseline |
|------------------|-----------|-----------|----------|---------------|
| shedy | 76 | 186 | 0.409 | 2.62× |
| shey | 33 | 93 | 0.355 | 2.27× |
| sheedy | 16 | 41 | 0.390 | 2.50× |
| sheey | 15 | 54 | 0.278 | 1.78× |
| sheckhy | 10 | 23 | 0.435 | 2.79× |
| sheol | 11 | 34 | 0.324 | 2.07× |
| shecthy | 5 | 10 | 0.500 | 3.21× |
| **shol** | 4 | 24 | **0.167** | **1.07×** ← baseline |
| **shcthy** | 2 | 22 | **0.105** | **0.67×** ← depleted |

**Body-class split confirmed**: she-body sh-words E=1.78–3.21×; non-she-body words (shol, shcthy, shy) at or below baseline.

P(qok successor | MID baseline) = 0.156. Top-3 sh-words (shedy/shey/sheedy) account for 47.5% of sh→qok pairs — but this is proportional to their frequency (shedy=26% of sh-tokens). No specific sh-word has disproportionately elevated qok rate.

**Uniqueness: 62.4% unique (sh, qok) pairs (164/263)** — not fully class-level (vs >80% threshold), reflecting large N in B. No pair exceeds 5% (shedy→qokedy=13/263=4.9%).

### B-dialect qok successor distribution (after sh)

Top qok-words: qokeedy=36(13.7%), qokain=35(13.3%), qokedy=34(12.9%), qokaiin=31(11.8%), qokeey=29(11.0%). Each elevated E=1.8–2.5× after sh. **qok successor is distributed across multiple types — no single qok word dominates (no E>3× at high N).** This confirms the "qok-class uniform successor" claim.

### A-dialect (N=43, E=1.81×)

| sh-word | N(sh→qok) | N(sh→any) | qok_rate | E vs baseline |
|---------|-----------|-----------|----------|---------------|
| sheody | 3 | 9 | 0.333 | 4.27× |
| sheey | 4 | 14 | 0.286 | 3.66× |
| sheol | 4 | 16 | 0.250 | 3.20× |
| shey | 4 | 19 | 0.211 | 2.69× |
| **shol** | 5 | 34 | **0.147** | **1.88×** (borderline) |
| **sho** | 1 | 33 | **0.036** | **0.46×** ← depleted |

**A-dialect: 97.7% unique pairs (42/43)** — fully class-level. No specific (sh, qok) pair repeated. She-body A-words (sheody/sheey/sheol/shey) E=2.7–4.3×; shol borderline (N=5); sho depleted (N=1).

A qok successors: 10 distinct qok-word types among 43 pairs — distributed, not word-specific.

---

## Interpretation

**F372 CONFIRMED at high N with detailed subtype breakdown.**

1. **Body-class rule confirmed (B N=263):** she-body sh-words (shedy/shey/sheedy/sheey/sheol/sheckhy) uniformly elevated E=1.78–3.21×. Non-she-body words (shol E=1.07×, shcthy E=0.67×) at or below baseline. The she-body distinction (presence of 'e' as first body character after 'sh') is the governing rule, not word-specific identity.

2. **qok successor is class-level (both dialects):** Top 5 qok successors in B all E=1.8–2.5×, spread across 10+ types. No single qok-word pair accounts for >5% of sh→qok transitions. The qok side of the rule is uniform — any qok-class word can fill the successor slot.

3. **Apparent word concentration is frequency-driven:** shedy accounts for 29% of B sh→qok pairs, but shedy is also 26% of sh-tokens in MID. Its qok rate (40.9%) matches other she-body words. The top-3 concentration (47.5%) is proportional to the she-body words' collective frequency, not to any special word-pair grammar.

4. **A-dialect: fully class-level (97.7% unique pairs).** With N=43, A sh→qok has no repeated pairs. The she-body pattern holds (sheody/sheey/sheol/shey all elevated), but A's most common sh-word is shol (o-body), which is near-baseline. This is consistent with F372: A sh→qok enrichment is weaker (E=1.81× vs B=1.96×) partly because A's sh-vocabulary is more o-body weighted.

5. **H522 archived entry cleaned up:** The original H522 was resolved by exp_370/F372. The H522_archived entry in hypothesis_backlog.md is a legacy duplicate that should be removed.

---

## Self-Audit

**Target-awareness**: No target-aware elements. Analysis is descriptive word-level decomposition of a corpus pattern.

**Feature-destroying implementation**: No issues. MID bigrams computed from continuation lines 1:-1, positions [1:lw-1] — standard MID extraction.

**Extrapolation**: All claims within observed N. E-values computed from observed/expected ratios. N<10 cases (shcthy/shol in B) treated as directional where appropriate.

**Negative-result scope**: N/A — positive confirmatory result. shol (non-she-body) showing E=1.07× is a within-experiment null that supports the she-body specificity, not a stand-alone negative finding.

**Control behavior**: No external control corpus. Baseline = empirical MID qok rate (B=0.156, A=0.078). No surprises — baseline calculated from same corpus, unrelated to the sh-qok hypothesis.

---

## Conclusion

H522 (archived) CONFIRMED at N=263 (B) and N=43 (A): F372 is correct. The sh→qok enrichment is a **body-class rule**: she-body sh-words (sh-e-[body]) have qok succession rate E=1.78–3.21× above baseline; non-she-body sh-words (shol, shcthy) are at or below baseline. The qok successor is uniformly distributed across qok-word types (class-level). No specific (sh-word, qok-word) pair dominates. A-dialect is fully class-level (97.7% unique pairs); B-dialect is 62.4% unique (frequency-driven concentration, not grammar-specific). **No new finding ID** — confirmatory of F372. H522_archived entry should be removed from hypothesis backlog.
