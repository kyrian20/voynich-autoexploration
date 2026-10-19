# exp_589 — Result: daiin line-position audit

**Execution date:** 2026-10-19  
**Status:** executed successfully in GitHub Actions; exploratory finding, pending independent review  
**Workflow run:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256111019  
**Artifact:** `exp-589-daiin-position-audit` (JSON output also committed as `results.json`)

## Question
Is EVA `daiin` over-represented as the first token of body-text lines after conditioning on each line's own token composition and length, and does the direction replicate in ZL3a and across Currier A/B?

## Method
- Corpus files: checked-in Zandbergen–Landini IVTFF EVA ZL3b and ZL3a.
- Parser: body records whose locus begins with `P` after optional `+`, `*`, or `@`; only ASCII-letter tokens are retained after conservative markup cleanup. See `script.py` for exact rules.
- 2,000 Monte Carlo replicates per subset; each line chooses a uniformly random token position. This is statistically equivalent for the first-position count to randomly shuffling each line, while preserving its token composition and length.
- Fixed seeds; target `daiin` is the single primary positional hypothesis. The minimum resolvable one-sided Monte Carlo p-value with 2,000 replicates and +1 correction is 1/2001 ≈ 0.0005.
- The reported p-value is conditional on this parser and null model. The test is not a decipherment.

## Results

| Transcription / subset | `daiin` body tokens | Observed first | Expected first | Enrichment | Monte Carlo p (one-sided) |
|---|---:|---:|---:|---:|---:|
| ZL3b, all body | 807 | 158 | 104.44 | 1.513× | 0.0005 (resolution floor) |
| ZL3b, Currier A | 490 in eligible lines | 61 | 69.33 | 0.880× | 0.8951 |
| ZL3b, Currier B | 317 in eligible lines | 97 | 35.11 | 2.763× | 0.0005 (resolution floor) |
| ZL3a, all body | 808 | 158 | 104.58 | 1.511× | 0.0005 (resolution floor) |
| ZL3a, Currier A | 490 in eligible lines | 61 | 69.37 | 0.879× | 0.8891 |
| ZL3a, Currier B | 318 in eligible lines | 97 | 35.21 | 2.755× | 0.0005 (resolution floor) |

The two transcriptions produce the same directional pattern: a line-initial excess in Currier B, no such excess in Currier A, where the first-position count is below its conditional expectation. ZL3b and ZL3a counts closely agree, making this pattern robust to this transcription-version change.

For descriptive context, observed last-position counts were 127 overall, including 101 in A and 26 in B. Under the same within-line exchangeability expectation, the corresponding expected counts equal the expected-first values for each subset. This suggests a possible A-side final-position enrichment, but this is secondary/descriptive and has not been separately tested in the registered primary test.

## Interpretation and limitations
1. **Supported, narrowly:** under this operational tokenizer and within-line exchangeability null, `daiin` is strongly enriched at line start in the B-dialect corpus and that result replicates between ZL3b and ZL3a.
2. **Not supported:** the same initial-position claim for Currier A. Aggregate-only reporting would hide this dialect split.
3. The 0.0005 values are not exact p-values; they are the resolution floor of 2,000 Monte Carlo replicates. A larger simulation would sharpen the bound, but is not needed to see the directional split in this first pass.
4. The null assumes token positions are exchangeable within each line. It preserves per-line length and word inventory but does not condition on section, paragraph role, folio, or position-dependent transcription uncertainty. A follow-up should stratify by section and line/locus subtype.
5. This is evidence about placement only. It does **not** tell us what `daiin` means, whether it is a grammatical particle, or whether the manuscript has been deciphered.

## Provenance
- ZL3b file bytes: 411,671; SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- ZL3a file bytes: 411,710; SHA-256: `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2`.
- Machine-readable results: `results.json`.
- Relevant public context: https://voynich.world/explore/manuscript?word=daiin ; https://www.voynich.nu/data/ZL3b-n.txt ; https://arxiv.org/abs/2604.25979

## Next preregistered test
Repeat the same analysis stratified by manuscript section and paragraph/line locus, keeping Currier A/B results separate. Report all strata (including null results); check whether the B initial excess remains when the Recipes section and folio-openers/closers are not allowed to dominate. Do not select strata after seeing their outcomes without labelling that analysis exploratory.
