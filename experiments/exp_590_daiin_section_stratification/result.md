# exp_590 — Results: daiin across folio-number ranges

**Execution date:** 2026-10-19  
**Status:** completed in GitHub Actions; sensitivity analysis  
**Workflow:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256487097  
**Machine-readable output:** `results.json`

## Question
Does the Currier-B line-initial excess found in exp_589 persist across coarse folio-number ranges, or is it confined to one range?

## Results

| Folio-number proxy | Currier | Lines | Observed first | Expected first | Enrichment | Nominal p | Holm-adjusted p |
|---|---|---:|---:|---:|---:|---:|---:|
| f001–f066 | A | 1,166 | 42 | 57.99 | 0.72× | 0.9955 | 0.9955 (secondary A family) |
| f001–f066 | B | 347 | 13 | 8.03 | 1.62× | 0.0485 | 0.0485 (primary B family) |
| f067–f073 | B | 84 | 6 | 1.99 | 3.01× | 0.0045 | 0.0135 |
| f074–f084 | B | 771 | 17 | 9.55 | 1.78× | 0.0175 | 0.0350 |
| f085–f102 | A | 358 | 19 | 11.34 | 1.68× | 0.0155 | 0.0310 (secondary A family) |
| f085–f102 | B | 242 | 13 | 3.49 | 3.72× | 0.0005 | 0.0025 |
| f103–f116 | B | 1,083 | 48 | 11.70 | 4.10× | 0.0005 | 0.0025 |

There are also 11 body lines with unknown folio range in Currier B; they contain one `daiin` token and are reported descriptively only.

### Primary inference: Currier B
All five eligible Currier-B range bins show a positive first-position excess. All five nominal Monte Carlo results remain below 0.05 after Holm adjustment across this five-test primary family. The strength varies from 1.62× in f001–f066 to 4.10× in f103–f116. The two largest effects are in the f085–f102 and f103–f116 bins, but the pattern is not confined to either: the three other bins also have positive effects and adjusted p-values at or below 0.0485.

### Secondary Currier-A pattern
The two populated A bins differ: f001–f066 is below its conditional expectation (0.72×), while f085–f102 is above it (1.68×; separately adjusted p=0.0310). This explains why the aggregate Currier-A result in exp_589 is below expectation. It is not accurate to say that A has one uniform positional pattern across the whole manuscript.

## Limitations
- These are **coarse folio-number ranges**, inherited from an older simplified script, not adjudicated codicological section labels. Folio numbering and manuscript content are more complicated than these bins suggest.
- This is a sensitivity analysis on ZL3b, not an independent transcription replication; only exp_589 compared ZL3b with ZL3a.
- The null preserves each line's token inventory and length, but does not model all dependencies among manuscript positions.
- `p=0.0005` is the Monte Carlo resolution floor for 2,000 replicates, not a precise probability.
- Locus codes in the corpus include P0, P1, Pb, Pc and Pr. This experiment records those types but does not assign a grammatical interpretation to them.
- These results concern position only; they do not establish the meaning of `daiin` or decipher the manuscript.

## Next step
Test exact IVTFF body-locus subtypes (P0/P1/Pb/Pc/Pr) within Currier A/B, and report whether the initial excess survives in the dominant P0 group rather than being an artefact of mixing locus subtypes. Treat very small subtypes as descriptive. Apply a multiple-testing correction within predeclared B and A test families.
