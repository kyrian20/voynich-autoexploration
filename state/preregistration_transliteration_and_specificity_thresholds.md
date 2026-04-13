# Pre-registered Thresholds for v3 Transliteration Replication and Architecture Specificity

**Author**: Asa Shepard
**Date**: [TODAY'S DATE]
**Commit-before**: All experiments described below. This document must be committed to the public voynich-cryptanalyst repository before any of the described experiments are run. The commit hash is the time anchor.

## Purpose

This document pre-specifies the numerical thresholds against which the v3 experiments for the Voynich paper (arxiv preprint, Shepard 2026) will be evaluated. Pre-registration is used to foreclose post-hoc framing flexibility on claims where the paper's contribution is load-bearing.

Thresholds specified here must be reported as pass/fail against the pre-registered criteria in the final paper, regardless of whether those criteria match alternative framings of the results.

## Transliteration replication thresholds

The paper's Section 2 characterization findings are currently reported for EVA ZL3b only. The replication experiment tests whether the characterization survives under v101 (Zattera 2022), EVA-basic, and optionally ZL3a.

### Finding 1: Three-layer positional architecture (openers, mid-classes, terminals)

*Retained if*: In at least 2 of 3 alternative transliterations, the classification of each onset class (opener / mid / terminal) under CONF thresholds agrees with the ZL3b classification for ≥75% of onset classes characterized in ZL3b (i.e., at least 15 of 20 classes receive the same category assignment).

*Weakened if*: Agreement falls between 50% and 75%.

*Failed if*: Agreement falls below 50% in any 2 of 3 alternative transliterations.

### Finding 2: Terminal-layer dialect inversion (A = {d, cth}; B = {r, l, ol, o, a}; zero overlap)

*Retained if*: A-terminal and B-terminal sets share zero classes under at least 2 of 3 alternative transliterations, with d-onset classified as A-terminal and at least one of {r, l, ol, o, a} classified as B-terminal in each of those.

*Weakened if*: Zero-overlap holds in 1 of 3 alternative transliterations, or non-zero overlap of ≤1 class holds in 2 of 3.

*Failed if*: Non-zero overlap of ≥2 classes holds in at least 2 of 3.

### Finding 3: Bigram matrix cross-dialect invariants

*Retained if*: Of the five cross-dialect invariant elevated pairs (y→y, sh→qok, ok→ok, qok→s, plus the sh→ch depletion), at least 4 replicate at CONF threshold in both dialects under at least 2 of 3 alternative transliterations.

*Weakened if*: 2-3 of 5 invariants replicate under at least 2 of 3 alternative transliterations.

*Failed if*: Fewer than 2 of 5 replicate.

### Finding 4: A-herbal paragraph chain d→qot→ch→o→sh

*Retained if*: The directed chain exceeds the 95th percentile of both section-shuffled and onset-shuffled null distributions (200 controls each) under at least 2 of 3 alternative transliterations, with all four edges reaching at least directional enrichment (E ≥ 1.5×).

*Weakened if*: Chain exceeds 95th percentile in 1 of 3 transliterations, or chain exceeds 90th but not 95th percentile in ≥2 transliterations.

*Failed if*: Chain falls below the 90th percentile in any 2 of 3 transliterations.

### Finding 5: Systematic -edy suffix transformation (A: -ol/-or/-ey; B: -edy/-eedy)

*Retained if*: The A→B suffix transformation pattern holds across ≥75% of characterized onset classes under at least 2 of 3 alternative transliterations.

*Weakened if*: 50-75% transformation agreement.

*Failed if*: Below 50% agreement in any 2 of 3 transliterations.

### Required reporting

Results for all five findings must be reported against these thresholds in the paper's Section 2 or a dedicated replication subsection, regardless of outcome. Findings marked "Weakened" must be reported with the weakened framing explicitly. Findings marked "Failed" must be reported as non-replicating and the paper's corresponding claims adjusted.

## Architecture specificity thresholds

The paper's Section 5 reports that a 21-mechanism position-aware copy-buffer hybrid architecture achieves 19/19 on a B-dialect battery and asserts this is specific to Voynich structure. The specificity experiment tests this claim against three structurally-matched non-Voynich corpora (medieval Latin line-segmented to match VMS distribution; Voynich-matched synthetic with random word order; a morphologically-complex non-Latin natural language).

Specificity is measured by the specificity ratio R = (applicable battery PASS count on Voynich after re-optimization) / (best applicable battery PASS count on any non-Voynich corpus after re-optimization).

The ratio is reported separately for the 6-parameter re-optimization and the 21-parameter re-optimization.

### Strong specificity

*R ≥ 1.3 under both 6-parameter and 21-parameter re-optimization.*

Interpretation: The architecture's 19/19 on Voynich is substantively specific to Voynich structure. The paper's Section 5 specificity claim is retained and may be strengthened to cite these results. C008 is strengthened.

### Partial specificity

*R ≥ 1.3 under 6-parameter re-optimization but 1.0 ≤ R < 1.3 under 21-parameter re-optimization, or vice versa.*

Interpretation: The architecture has calibrated-parameter specificity to Voynich but some or all of the structural specificity is due to the fixed mechanism constants. The paper's Section 5 retains the specificity claim with explicit disclosure of the parameterization-regime dependence. C008 is retained with a scope qualification.

### Weak or absent specificity

*R < 1.0 under either regime, i.e., at least one non-Voynich corpus matches or exceeds Voynich battery PASS count after re-optimization.*

Interpretation: The architecture is generic to structurally-matched corpora rather than specific to Voynich. The paper's Section 5 must be further demoted: the 19/19 on Voynich is not evidence about Voynichese structure, only about the architecture's fitting flexibility. C008 is contradicted and must be withdrawn or substantially amended. The paper's central claims are not affected (characterization and discrimination stand) but the architecture section shrinks to the feasibility-only framing.

### Required reporting

The specificity ratio R must be reported in the paper's Section 5 under both parameterization regimes, with explicit pass/fail against the thresholds above. If R falls in the weak-or-absent range, the paper must acknowledge this and adjust Section 5 accordingly; silent reframing is not permitted.

## Repository commitment

This document is committed to the voynich-cryptanalyst repository at commit [hash to be filled in at commit time]. No experiments described above will be run before this commit is public. Experiments run after this commit will report their results against the thresholds specified here.

Deviations from these thresholds in the final paper — including changes to the threshold values, changes to what counts as replication, or introduction of new post-hoc criteria — must be disclosed explicitly in the paper's methods section with a specific note indicating the deviation, why it was made, and what the pre-registered threshold would have yielded.

## Addendum: Canonical Specificity Experiment (2026-04-13)

The architecture-specificity test described above was run in two stages. exp_584 was the original attempt; exp_585 is a corrected replication of the same pre-registered protocol.

exp_584 contained a methodology issue: the simulation drew MID-position tokens from a vocabulary of actual VMS word strings, which caused vocabulary collapse on the copy-buffer modify path and produced spurious same-word repetition, bringing the VMS positive control down to 7/17 applicable instead of the expected 17/17. The specificity ratio reported in exp_584 was derived by substituting the exp_314 / exp_575 VMS value rather than the script's own positive control, which is not what the pre-registration intended.

exp_585 replaces the vocabulary-lookup step with abstract-token synthesis matching the methodology used in exp_575 (character-level perturbation that preserves the onset class while producing fresh synthetic word strings). Under the corrected simulation the VMS positive control recovers to 19/19 (17/17 applicable), and the canonical specificity ratio is R_6param = 17/12 = 1.417, satisfying the pre-registered STRONG_SPECIFICITY threshold (R ≥ 1.3). Cicero Latin reaches 5/17 applicable and Dante Italian reaches 4/17 under matched re-optimization. exp_585 is therefore the canonical run for the specificity section; exp_584 is retained in the repository as a record of the bug and its correction but should not be cited as the canonical result.

This addendum was committed after both experiments completed. The original pre-registration commit timestamp remains the time anchor for the threshold values themselves, which were not modified. Only this addendum — noting which experiment supplies the canonical numbers — has been added; the specificity thresholds in the "Architecture specificity thresholds" section above stand as originally written.

