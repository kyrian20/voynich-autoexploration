# Current State — Voynich Cryptanalyst

**Last updated:** 2026-10-19 (exp_589–exp_600 completed; exp_600 source-key parser corrected and results recorded)

## Canonical status and source of truth
Read the synthesis at `research/synthesis/2026-10-19-daiin-position-synthesis.md`. It separates robust distribution observations, annotation-sensitive outcomes, non-significant comparisons, and the exp_598 method failure.

The pre-existing project checkpoint remains exp_588, summarized in `state/transliteration_replication_final_summary.md`; it has not been independently rerun in this session. The reported 21-mechanism generator score of 19/19 is compatibility with a defined metrics battery, not proof of the manuscript's generative mechanism or a decipherment.

## API / automation
The separate LLM agent workflow returned HTTP 429 because no OpenAI API funds were available, as reported by the maintainer. It was not retried. Corpus experiments run as standard Python in GitHub Actions without OpenAI API credit. Generated results use 90-day artifacts and are also committed to the repo where possible.

## Main positional observations: exp_589–exp_599
- exp_589: whole-body `daiin` is ~1.51× expected at line start in ZL3a/ZL3b; Currier B ~2.75×, Currier A ~0.88×.
- exp_590: Currier-B effect is positive across five coarse folio-number ranges (1.62×–4.10×, Holm-adjusted under the chosen null). These ranges are heuristic proxies, not authoritative codicological section labels.
- exp_591: in Currier-B P0, 89 initial `daiin` vs 31.53 expected (2.823×); P0 carries the dominant signal.
- exp_592: leave-one-folio-out across 88 represented folios leaves B/P0 enrichment between 2.651× and 2.939×; no single folio explains it.
- exp_593: B/P0 `+` locator rows show 89 vs 30.634 expected (~2.91×). IVTFF `@`, `+`, `*` are layout/locator codes, not paragraph-open markers.
- exp_594–595: explicit `<%>` paragraph-start annotation is associated with an initial-token deficit in Currier A; B rows without an explicit start marker show ~3× enrichment. The direction replicates across ZL3a/ZL3b, but absence of `<%>` is not definitive continuation.
- exp_596: the effect is not unique to `daiin`. In B/P0 `dain` is ~3.17× and `saiin` ~5.02× initial; `aiin`/`chedy` are depleted.
- exp_597: successor-token distributions after `daiin`, `dain`, and `saiin` were not statistically distinguishable (Holm-adjusted p=1.0).
- exp_598: explicitly **uninformative due to sparsity**; the rare-pair collapse merged 97.1%–100% of joint contexts into one bucket.
- exp_599: marginal next-token and second-successor distributions were not significantly different after adjustment; nonsignificance does not prove equivalence.

## exp_600 — ZL3a/ZL3b concordance audit
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39259781970  
Report: `experiments/exp_600_transcription_concordance/result.md`; JSON: `results.json`.

The corrected parser covers 5,385 aligned line IDs, with zero duplicates and zero skipped identifiers; ZL3a has four additional IDs. Of aligned rows, 5,327 (98.92%) have byte-level-equivalent IVTFF payloads and 5,336 (99.09%) have identical cleaned token sequences; 49 rows (0.91%) differ at token level. All matched rows have the same normalized locus and Currier label under this parser, and paragraph-marker flags match. This confirms the two files are closely related alternative transcriptions, **not independent samples**. Four ZL3a-only keys: `f1r.29`, `f1r.30`, `f1r.31`, `f89v2.26`.

## Next work: exp_601 primary-statistic paired sensitivity
Measure the effect of the exact ZL3a/ZL3b token differences on the primary Currier-B/P0 `daiin` first-position statistic. Report per-version total target count, observed first count, line-inventory expectation, enrichment, and paired aligned-line changes. Also include the exp_596 control tokens, so version-level robustness is measured rather than assumed. This is a sensitivity analysis, not an independent-sample significance test.

## Research integrity
- Keep observations, hypotheses, null results, and method failures separate.
- Each experiment should include exact filter/token rules, source hashes, JSON output, a report, and workflow URL.
- The 19/19 mechanism fit and positional effects do not constitute a decipherment.
- Never infer the meaning of `daiin` from position or local context alone.


## Exp_600 transcription concordance — completed
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39259522070
Machine-readable output: `experiments/exp_600_transcription_concordance/results.json`
- Exact folio.line alignment found 5,225 shared keys; ZL3a has four additional keys and ZL3b none unmatched. No duplicate keys.
- Clean token sequences match on 5,188 aligned lines and differ on 37; 46 raw payloads differ. Within the aligned lines, Currier labels match and normalized loci match.
- These versions are highly similar alternate transcriptions, not independent replications. Invalid-identifier flags largely concern special folio labels such as fRos and must be interpreted as format-specific cases, not silently dropped.
- This concordance output is a separate experiment from the lightweight IVTFF structural audit also numbered exp_600; paths distinguish them.

## Exp_601 completed — folio-clustered confirmation
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39259869279
Report: `experiments/exp_601_folio_clustered_confirmation/result.md`
- Frozen primary endpoint: Currier B, P0, at least 2 cleaned tokens, first token exactly `daiin`; ZL3b source SHA-256 recorded in results.
- 2,325 eligible lines across 81 folios; 88 observed initial hits vs line-inventory expectation 31.2792; enrichment 2.8134×.
- 20,000 folio-cluster bootstrap replicates give percentile 95% interval 2.1156–3.5932×, wholly above 1.
- 20,000 conditional within-line randomizations give one-sided p=0.00005; this tests uniform positional exchangeability conditional on each line's inventory and length, a distinct question from the cluster bootstrap.
- Leave-one-folio-out enrichment range 2.6404–2.9306×. The preregistered robustness rule is met for this operational parser/filter.
- Conclusion remains narrow: a robust positional excess under this test, not a semantic/grammatical inference or decipherment.

## Next high-value experiment
Do not add more hand-selected lexical variants. Build a held-out predictive test: freeze train/test folios before analysis, train a minimal positional model on training folios, evaluate predictive log-loss/calibration on untouched folios, and compare with line-inventory-preserving baselines plus negative-control tokens. Report all predeclared outcomes and do not use held-out results to tune the model.
