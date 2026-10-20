# Experiment 624 — character entropy under within-word order permutations

**Status:** preregistration / implementation plan; no results claimed yet.  
**Date:** 2026-10-20  
**Primary corpus:** Zandbergen–Landini ZL3b EVA IVTFF. **Replication corpus:** IT2a, treated as an alternate transcription, not an independent manuscript sample.

## Question
Does the original character order within EVA tokens carry more character-level sequential information than a null that preserves each token's character inventory and length but destroys its internal order?

## Preregistered design
1. Parse IVTFF text lines only; preserve line/folio/locus and Currier metadata. Exclude headers, comments, locator markup, non-Voynich annotations, and unresolved alternative/uncertain readings using a documented deterministic policy.
2. Restrict the primary analysis to body text and report P0 separately from other loci. Publish token and character counts plus exclusion counts before testing.
3. Primary statistic: pooled within-token conditional character bigram entropy (equivalently, empirical conditional entropy H(C[t+1] | C[t])) computed across eligible tokens, with token boundaries never crossed.
4. Generate 10,000 deterministic-seed null corpora by independently permuting characters within each token; preserve token length and character multiset exactly. Do not permute across tokens or lines.
5. Compare observed statistic with the null distribution using a two-sided plus-one Monte Carlo p-value and standardized effect (observed minus null mean / null SD). Report the null quantiles and random seed.
6. Robustness: (a) tokens length >= 3; (b) P0 only; (c) Currier A and B separately where labels are available; (d) remove tokens containing uncertain/alternative transcription markup; (e) report token-weighted and equal-token-weighted summaries.
7. Replicate the identical parser and statistic on IT2a, clearly labelling it transcriptional robustness rather than independent replication.

## Interpretation and falsification
- Lower observed conditional entropy than the within-token permutation null indicates local character-order structure beyond each token's character inventory and length. It does **not** establish language, phonetics, meaning, or decipherment.
- If the observed statistic falls inside the central 95% null interval, record the primary test as not distinguishable from this null.
- Any parser disagreement, undocumented filtering, or null that fails to preserve token lengths/multisets invalidates the run.
- Do not select a different entropy statistic after seeing the result. Exploratory alternatives must be labelled as such and tested in a later preregistered experiment.

## Deliverables
Save the executable script, machine-readable JSON (including hashes of input files, configuration, seed, counts, observed statistic and null summary), and a Spanish report under `experiments/exp_624_character_order_entropy/`. The run must be reproducible from checked-in transcription files without an API key.

## Relation to prior work
The preceding word-order bigram experiment did not generalize on held-out folios. This test asks a distinct question about **within-token character order**, so it must not be described as a replication or reversal of that negative result.
