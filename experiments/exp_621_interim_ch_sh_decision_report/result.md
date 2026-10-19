# Interim decision report — ch/sh following-character contrast (experiments 612–621)

**Status: provisional synthesis, not a decipherment result.** The sequence has produced a repeatable descriptive contrast, but the adjacent-context control raises a substantial specificity concern. The full block is not closed: section-level holdout, full multiple-testing review, and an independent parser audit remain open.

## Main question
In IVTFF $Q=T, is the character after ch more often in the tested vowel inventory aeiouy than the character after sh, after matching folio, exact token length, and digraph position?

## Evidence so far

| Experiment | Result | Decision status |
|---|---|---|
| 612 — metadata-stratified descriptive analysis | In ZL3b, ch 83.63% vs sh 89.15% (2,340 ch and 1,051 sh observations); IT2a ch 83.03% vs sh 88.91% (2,387 ch and 1,064 sh). | Descriptive contrast reproduced across two transcription files. |
| 613 — folio-cluster bootstrap | Equal-weight mean of per-folio sh−ch differences: ZL3b +7.60 pp, 95% CI +3.79 to +10.88; IT2a +7.49 pp, 95% CI +3.75 to +10.71. | Positive under this cluster-resampling estimand. |
| 614 — within-cell permutation | Two-sided plus-one Monte Carlo p=0.00005 in both sources (0 exceedances in 20,000 draws; simulation floor). | Strong conditional separation under the specified exchangeability null; not a causal or linguistic test. |
| 615 — vowel-inventory sensitivity | With aeiou, pooled sh−ch is +4.39 pp in ZL3b and +5.09 pp in IT2a; conditional permutation p=0.00795 and 0.00310. | Direction survives this variant. |
| 616 — numeric folio-block omission | Pooled contrast stays positive after omitting each heuristic block (103–106, 107–108, 111–113, 114–116). | Exploratory only; these are not verified codicological sections. |
| 617 — high-support cells | Contrast stays positive when cells require at least 3 or 5 occurrences of each digraph. | Sparse cells alone do not explain the pooled direction. |
| 618 — unique word-type weighting | Unique token types per matched cell still give positive pooled differences: +7.35 pp (ZL3b) and +7.08 pp (IT2a); folio-bootstrap intervals are above zero. | Repeated token frequency alone does not explain the contrast, but shared word templates remain possible. |
| 619 — preceding-character control | The preceding-character vowel-rate contrast is +7.41 pp in ZL3b and +8.16 pp in IT2a; folio-bootstrap 95% CIs include zero in both. Conditional permutation p=.0832 and .0183. In the same position>0 subset, following-character differences are +6.26 pp and +4.73 pp. | **Important caution:** the control contrast is not smaller than the primary contrast. A broad template/context effect may explain some or all of the apparent next-character pattern. Do not claim outcome specificity. |
| 620 — parser audit | Terminal digraphs lacking a following character were initially counted as non-vowels in some follow-up code; corrected, scripts/results updated. | Partial only; independent parser and IVTFF edge-case audit still required. |

## What survives, and what does not

**Survives:** a positive ch/sh distributional difference in the chosen matched contexts across two transcription sources, multiple vowel inventories, high-support filters, and type-weighting variants. It also remains positive after omitting each chosen numeric folio block.

**Does not survive as a strong claim:** that the contrast is specifically about the following character. The preceding-character control shows a similarly large or larger difference, with uncertainty depending on the inferential procedure. This points toward shared lexical-template, token-position, or broader local-context structure as a live alternative explanation.

**Not established:** a phonetic value for ch or sh, semantic content, translation, authorial intent, a language identity, or decipherment. ZL3b and IT2a are alternative transcriptions of the same manuscript, not independent manuscripts.

## Required next steps before closing the block

1. Complete a second, independently written parser and compare token/event fixtures against IVTFF markup.
2. Define manuscript section boundaries from a defensible external source before section-level holdout; do not relabel numeric ranges as sections.
3. Freeze a full family of primary/negative-control outcomes and adjust for multiple testing; report all null or adverse controls.
4. Only then decide whether the ch/sh effect merits a new preregistered held-out replication.

## Reproducibility pointers
- exp612: experiments/exp_612_ch_sh_currier_stratification/
- exp613–615: experiments/exp_613_615_ch_sh_inference_sensitivity/
- exp616 partial: experiments/exp_616_folio_block_holdout_sensitivity/
- exp617: experiments/exp_617_ch_sh_high_support/
- exp618: experiments/exp_618_ch_sh_word_type_sensitivity/
- exp619 partial: experiments/exp_619_ch_sh_adjacent_context_control/
- exp620 partial: experiments/exp_620_parser_audit/partial_audit.md
