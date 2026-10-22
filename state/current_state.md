# Current State — Voynich Cryptanalyst

**Last updated:** 2026-10-22 (operational follow-up; scientific blockers remain)



## Latest session update — 2026-10-19 (experiments 612–620)

- exp_612: descriptive ch/sh next-character vowel-rate comparison in IVTFF $Q=T, matched by folio × exact token length × digraph position; result documented in `experiments/exp_612_ch_sh_currier_stratification/`.
- exp_613–615: folio-cluster bootstrap, within-cell conditional permutation, and vowel-inventory sensitivity saved with standalone Node scripts in `experiments/exp_613_615_ch_sh_inference_sensitivity/`. Corrected parser excludes terminal ch/sh occurrences lacking a following character. ZL3b: ch 83.63%, sh 89.15%, pooled difference +5.52 percentage points; IT2a: ch 83.03%, sh 88.91%, difference +5.88 points. Folio-bootstrap 95% CIs for equal-weight mean differences are above zero in both sources; conditional permutation has zero exceedances in 20,000 draws (plus-one p=0.00005, Monte Carlo floor).
- exp_617: high-support cells requiring at least 3 or 5 occurrences of each digraph retain a positive pooled contrast in both transcriptions; report/script in `experiments/exp_617_ch_sh_high_support/`.
- exp_618: distinct word-type weighting still gives a positive contrast in both sources; report/script in `experiments/exp_618_ch_sh_word_type_sensitivity/`.
- exp_620 parser audit is PARTIAL only: a terminal-digraph counting inconsistency was found and corrected in 613–617, but an independent parser and full IVTFF edge-case audit remain outstanding. See `experiments/exp_620_parser_audit/partial_audit.md`.
- Open work: exp_616 section/folio-group holdout; exp_619 preregistered negative-control/multiple-testing audit; finish exp_620 independent parser audit; exp_621 synthesis. These are not marked complete.
- Interpretation: these are conditional distributional observations, not semantic decoding, phonetic proof, or evidence of translation. ZL3b and IT2a are alternative transcriptions of the same manuscript, not independent manuscript samples.



## Latest session addendum — 2026-10-19 (experiments 612–621)

Experiments 612–615 and 617–618 are saved; 616 and 619–621 are partial. The ch/sh next-character vowel contrast remains positive in the matched IVTFF $Q=T subset, including bootstrap, conditional permutation, narrower vowel inventory, high-support cells, and unique-word-type weighting. However, exp619's preceding-character control has a contrast of similar or larger magnitude (+7.41 pp ZL3b, +8.16 pp IT2a), with folio-bootstrap intervals including zero. This is a meaningful warning that broad token-template/local-context effects may account for the apparent next-character contrast. Do not claim the effect is specific to following characters or supports decipherment.

The terminal-digraph parser inconsistency in follow-up scripts was corrected; the corrected ZL3b counts match exp612. Exp620 remains partial pending a genuinely independent parser and full IVTFF edge-case tests. Exp616 used heuristic numeric folio blocks, not verified manuscript sections. Exp619 is one exploratory adjacent-context control, not a complete multiple-testing audit. Interim synthesis: experiments/exp_621_interim_ch_sh_decision_report/result.md. Remaining work: authoritative section holdout, preregistered control family/multiple-testing review, independent parser, then final closure.


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

The corrected parser covers 5,385 aligned line IDs, with zero duplicates and zero skipped identifiers; ZL3a has four additional IDs. Of aligned rows, 5,327 (98.92%) have identical trimmed raw body-payload strings and 5,336 (99.09%) have identical cleaned token sequences; 49 rows (0.91%) differ at token level. All matched rows have the same normalized locus and Currier label under this parser, and paragraph-marker flags match. This confirms the two files are closely related alternative transcriptions, **not independent samples**. Four ZL3a-only keys: `f1r.29`, `f1r.30`, `f1r.31`, `f89v2.26`.

## exp_601 — paired primary-statistic sensitivity (implementation present; results pending verification)
Files: `experiments/exp_601_primary_statistic_paired_sensitivity/script.py`, `README.md`; workflow: `.github/workflows/voynich-paired-sensitivity.yml`. The run must be inspected and its JSON/report committed before its findings are promoted to the synthesis.

## Next work: exp_601 primary-statistic paired sensitivity
Measure the effect of the exact ZL3a/ZL3b token differences on the primary Currier-B/P0 `daiin` first-position statistic. Report per-version total target count, observed first count, line-inventory expectation, enrichment, and paired aligned-line changes. Also include the exp_596 control tokens, so version-level robustness is measured rather than assumed. This is a sensitivity analysis, not an independent-sample significance test.

## exp_601 — paired primary-statistic sensitivity (completed)
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39260083190  
Report: `experiments/exp_601_primary_statistic_paired_sensitivity/result.md`; JSON: `results.json`.

The 2,325 matched eligible B/P0 lines contain 10 lines with cleaned-token differences between ZL3a/ZL3b. Two rows differ in their literal first token, but none changes first-position status for the six predeclared tokens. For `daiin`, total count is 295/296, first count 88/88, expectation 31.279/31.384 and enrichment 2.813×/2.804× (ZL3b/ZL3a). The other five controls' first-position counts are unchanged. The successful Actions artifact was recovered and the output committed manually after a concurrency race in the auto-commit step. This is paired version sensitivity, not independent replication.

## Next work: independent parser/provenance audit
Cross-check IVTFF header, identifier, locus, locator, Currier label, paragraph markers and token cleanup against the official specification in a separately implemented extractor before developing new lexical hypotheses.

## exp_602 — independent parser audit (implementation added; run/results to verify)
Files: `experiments/exp_602_independent_ivtff_parser_audit/script.py`, `README.md`; workflow: `.github/workflows/voynich-independent-parser-audit.yml`.

Two differently implemented extraction/tokenization paths are compared on ZL3a and ZL3b. The audit checks line keys, folio/Currier state, raw and normalized locus, body text, token sequences, paragraph marker flags, and the six primary/control token statistics. It is an implementation-consistency check, not proof that either parser is authoritative. Do not claim parser agreement until the new run's JSON has been verified.

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


## Exp_602 completed — held-out folio prediction (2026-10-19)
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39260149768
Output: `experiments/exp_602_heldout_predictive_test/results.json`
- Deterministic folio-hash split: 1,797 training lines from 60 folios; 528 held-out lines from 21 folios. No folio crosses the split.
- Primary `daiin`: train-only global line-initial probability = 0.03450. On held-out folios, model mean log loss 0.19917 vs per-line inventory baseline 0.11786; gain (baseline minus model) = -0.08131, folio-cluster 95% interval [-0.11174, -0.05641]. Brier score likewise worse for the global model.
- Predeclared controls `dain` and `saiin` show the same direction: global-rate model performs worse than the per-line inventory baseline.
- This is a real negative result for the claim that one global line-initial rate predicts held-out starts better than the conditional inventory baseline. The baseline has access to each test line's token inventory and is an oracle-style conditional null, not a deployable predictor, so the comparison is intentionally stringent and does not disprove the observed positional enrichment.
- Next step: do not tune this split. Compare predeclared, train-only section/folio-grouped probabilities against a baseline available without target-line token inventory; retain the present result as a failed primary predictive criterion, not as a positive finding.


## exp_603 — predicción estratificada fuera de muestra
Workflow: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39260612200
Reporte: `experiments/exp_603_stratified_heldout_prediction/result.md`; datos: `results.json`.

Se reutilizó el criterio determinista de separación por hash de folio de exp_602, ahora con filas P0 de Currier A y B (ZL3b; al menos dos tokens limpios): entrenamiento 2.928 líneas/148 folios y test 919 líneas/47 folios. Comparación fijada antes de evaluar: probabilidad global estimada solo en train frente a tasa Beta(1,1) suavizada por estratos Currier A/B × longitud fija (2–4, 5–7, 8+ tokens). Los folios del test no se usan para ajustar tasas.

- `daiin`: log loss global 0,168849; estratificado 0,171576; ganancia global−estratificado −0,002727, IC bootstrap por folio 95% [−0,005202, −0,000135]. El modelo estratificado empeora modestamente en test.
- Control `dain`: ganancia +0,000173, IC [−0,001160, +0,001890]; inconcluso.
- Control `saiin`: ganancia +0,000914, IC [−0,001515, +0,003611]; inconcluso.
- El Brier no mejora para ninguno de los tres objetivos.

**Conclusión:** añadir dialecto Currier y bandas de longitud no aporta predicción fuera de muestra demostrable para el inicio de `daiin`; el intervalo agrupado es enteramente negativo. Esto no contradice el enriquecimiento posicional exp_601: la descripción estadística y la capacidad predictiva son preguntas diferentes. No cambiar split ni bins para perseguir un resultado positivo. Siguiente paso útil: auditar sensibilidad a la definición de filas/etiquetas en un análisis de robustez previamente delimitado, o cerrar esta rama predictiva y pasar a evidencia externa independiente; no inferir semántica.


## exp_604 — replicación posicional en IT2a
Workflow completado correctamente: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39261252303
Reporte: `experiments/exp_604_independent_transcription_replication/result.md`; resultados: `results.json`; script: `script.py`.

Con el protocolo fijado (Currier B, P0 exacto, al menos dos tokens limpios, `daiin` literal como primer token), la transcripción IT2a contiene 2.324 líneas elegibles en 81 folios. Se observan 84 inicios `daiin`, frente a 32,282 esperados según el inventario de cada línea: enriquecimiento 2,602×; bootstrap agrupado por folio 95% [1,935×, 3,345×]; permutación condicional 20.000 veces, p unilateral con corrección +1 = 0,000050. El análisis leave-one-folio-out queda entre 2,427× y 2,708×.

**Conclusión:** el patrón posicional se reproduce en IT2a con el mismo criterio estrecho, así que no depende únicamente de ZL3b. Límite: IT2a es otra transcripción/versionado, no un testigo manuscrito independiente; puede compartir convenciones editoriales. No implica significado de `daiin` ni descifrado.


## exp_606 — lexical boundary audit around known foliation gaps (completed)
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39267834416
Report: `experiments/exp_606_gap_boundary_lexical_audit/result.md`; JSON: `experiments/exp_606_gap_boundary_lexical_audit/results.json`.

Compared six predeclared transitions around known foliation gaps against adjacent surviving pages with the same Currier label, using simple cleaned-token Jensen–Shannon divergence and vocabulary overlap. Five transitions were measurable in each transcription; f90v→f93r was unavailable. Mean divergence at the five measured gap edges was 0.770 bits (ZL3b) and 0.765 (IT2a), versus 0.718 and 0.728 for 165 same-label adjacent controls. This is only a weak descriptive elevation, driven partly by f58v→f65r, whose right side yields just three tokens in this simple parser; two edges also cross Currier labels. One gap edge had lower divergence than 97% of controls. The result is mixed, sensitive to text volume and section boundaries, and **does not support a claim of additional missing pages**. Token cleanup is not a validated EVA parser; the experiment is exploratory, with no inferential p-value. Physical image/codicological verification is needed for any claim about missing leaves.

## Next research direction
Avoid further repetition of the same `daiin` positional statistic and avoid treating text discontinuity as evidence of lost pages. Prioritize a higher-value linguistic test: evaluate whether the manuscript's token sequences exhibit stable local transition structure beyond frequency and Currier class, with predeclared train/test splits by folio and negative controls. Report failures as well as positive results.


## Latest verified addendum — EXP-622/623 (2026-10-22)

The committed outputs for EXP-622 and EXP-623 were inspected directly:
- **EXP-622 (ZL3b):** 5,162 ch/sh occurrences with both adjacent characters; 472 matched strata across 144 folios. Mean matched-stratum sh−ch vowel contrast was +4.38 percentage points after the digraph and +3.85 points before it. The difference-in-differences was only +0.53 points; two-sided within-stratum permutation p=0.82342 (10,000 draws).
- **EXP-623 (IT2a):** 5,374 occurrences; 485 matched strata across 149 folios. The contrast was +4.50 points after and +5.41 points before; interaction −0.91 points, p=0.69003 (10,000 draws).
- **Decision:** the data do not show that the ch/sh vowel contrast is specifically stronger after the digraph than before it. This weakens the outcome-specific/phonetic interpretation; it does not erase the descriptive contrast, but neither experiment establishes sound values, meaning, language identity, or decipherment. IT2a and ZL3b are alternative transcriptions of one manuscript, not independent manuscript samples.
- **Provenance correction:** the EXP-623 script and generated report/JSON previously contained copy-paste wording incorrectly saying the analysis used ZL3b. The source path and SHA-256 were already IT2a; wording has now been corrected in all three files without changing the statistics.
- **Still open:** independent parser/IVTFF edge-case audit; section-level holdout using defensible codicological boundaries; and a complete predeclared multiple-testing/control-family review. Do not mark the ch/sh line closed or start another lexical variant scan before those checks.


## Workflow integrity correction — 2026-10-22

Two workflows that commit generated results to `master` used separate GitHub Actions concurrency groups (`voynich-independent-parser-audit` and `voynich-paired-sensitivity`). Because concurrency only serializes runs sharing the same group, those settings did not serialize them with the other master-writing workflows despite comments implying coordination. Both have been changed to the shared `voynich-master-writes` group with `cancel-in-progress: false`. This reduces avoidable non-fast-forward races; it does not guarantee every future push will succeed, so run logs still need verification.

## Integrity follow-up — 2026-10-22

- Removed duplicate `cancel-in-progress: false` keys from `.github/workflows/voynich-independent-parser-audit.yml` and `.github/workflows/voynich-paired-sensitivity.yml`; both retain the shared `voynich-master-writes` concurrency group.
- Hardened `experiments/exp_602_independent_ivtff_parser_audit/script.py`: the audit now stops if either required transcription file is missing, if the expected ZL3b/ZL3a coverage is incomplete, or if either parser returns zero records for a transcription. This prevents a partial/empty run from being written as if it were a complete audit.
- These are guardrail changes, not a new scientific result. Existing exp_602 result values have not been represented as newly rerun.
- CI verification remains pending: the available repository status/run lookup returned no status entries or workflow runs for the relevant commits, so this session cannot claim that GitHub Actions passed. Confirm the run in the Actions UI before treating the updated script as execution-verified.


## Workflow write-safety audit — 2026-10-22 (follow-up)

- Re-audited all 30 workflows with write capability in `.github/workflows/`. Each now has its own non-cancelling concurrency group (named for that workflow) and a bounded five-attempt rebase/push retry loop; the read-only `voynich-check.yml` remains outside these writer groups. This is deliberately per-workflow rather than one global group: GitHub keeps only one pending run per concurrency group, so a single shared group can cancel other workflows' pending runs.
- During the initial shared-group change, several pending workflow runs were cancelled by GitHub concurrency semantics. That design was corrected by restoring separate per-workflow groups. Those cancellations are not counted as successful validations; reruns/checks must be assessed by their own run IDs and conclusions.
- GitHub Actions runs triggered by these commits are still in progress/queued at the time of this note. Several `Voynich Check` runs and workflow-specific checks have already completed successfully, but the latest commit's check and every affected writer workflow have not all reached a final state. Do not claim the entire workflow suite is green until the run list is rechecked.
- No new EXP ID was allocated and no scientific result was intentionally changed by these workflow edits. The IVTFF conformance/prediction gate, ID collisions, and GitHub-versus-Library hash reconciliation remain separate research blockers.


## Auditoría de estabilización — 2026-10-22 (verificación directa)

- HEAD de `master` consultado: `3baca1a468c57ef3b2fe663e7860738153eb923a`. El run `39721778175` de `Voynich Check` para ese HEAD terminó `success`; varios workflows específicos recientes también terminaron en éxito. Esto no certifica toda la suite histórica ni reproduce todos los experimentos.
- Se inspeccionaron los 31 workflows YAML: 30 escritores tienen grupos de concurrencia individuales, `cancel-in-progress: false` y bucle de cinco intentos para rebase/push; `voynich-check.yml` es de solo lectura. Los grupos individuales evitan cancelaciones globales de pendientes, pero no serializan dos workflows diferentes. El reintento mitiga conflictos, no es una garantía formal. Se requiere una solución arquitectónica futura: un escritor central o publicación de artefactos sin push directo de cada workflow.
- El árbol completo de GitHub (2.119 rutas, no truncado) confirma 624 carpetas top-level bajo `experiments/`, 617 IDs distintos y siete colisiones: EXP-177, 594, 596, 597, 600, 601 y 602. Véase `research/stabilization_audit_2026-10-22.md` y `research/EXPERIMENT_REGISTER.md`.
- No se renumeraron ni borraron carpetas; no se creó un EXP nuevo ni se recalcularon resultados científicos en esta auditoría.
- La lista consultada de la Biblioteca devolvió como máximo 200 elementos y no permite afirmar que se haya cotejado todo su contenido. El cotejo de hashes GitHub/Biblioteca sigue pendiente, al igual que la adjudicación IVTFF independiente y la revisión de cada resultado histórico relevante.
- Siguiente orden obligatorio: (1) reconciliar IDs y referencias, (2) inventariar y comparar hashes de ambos repositorios, (3) completar fixtures IVTFF y verificar resultados críticos con logs, (4) elegir un único experimento confirmatorio preregistrado y pasar `skills/audit_experiment.md` antes de actualizar estado científico.


## Operational follow-up — 2026-10-22 (repository inspection)

- Re-read the concurrency audit, experiment register, Voynich Check workflow, and writer workflows for EXP-603 through EXP-611 plus the corpus-experiments workflow.
- The inspected EXP-605–611 and corpus-experiments workflows now contain per-workflow concurrency groups and bounded rebase/push retry loops. This reduces the chance that transient cross-workflow push races permanently lose result publication, but does not globally serialize different workflows; it is not proof that every workflow or every recent run is healthy.
- Corrected misleading concurrency comments in `.github/workflows/voynich-exp603.yml` and `.github/workflows/voynich-exp604.yml`: their groups serialize only executions of the same workflow, while cross-workflow races rely on bounded retries.
- This session inspected workflow source, not live run conclusions. Do not mark CI globally closed without verifying the relevant latest run IDs, commit SHAs, and failed/cancelled jobs.
- Scientific and archival gates remain unchanged: no new EXP IDs; reconcile the experiment register and Library/GitHub artifacts; complete independent IVTFF conformance fixtures; preserve historical outputs; and do not interpret distributional results as decipherment.


## Live GitHub Actions spot-check — 2026-10-22

- Queried the live Actions run list and inspected job summaries for three targeted writer/check runs. Voynich Check run [39727077696](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727077696) completed successfully on commit `8f7840f565be138a0a6abd83a159e3d4b34c0d53`; exp604 run [39727063490](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727063490) completed successfully on `49929c6aed05dc64980b4c66964638ec2107d22e`; exp603 run [39727059573](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727059573) completed successfully on `ed2b4087529012f5ccc6161110bc4056739e3e37`.
- Inspected older run [39490460729](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39490460729): analysis steps completed, but artifact publication failed at `git push` because `master` advanced between rebase and push (remote ref lock mismatch). This is a real concurrency race, not a scientific-test failure. Later run [39569620268](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39569620268) succeeded, but reported no changed experiment outputs to commit; it does not retroactively change the older run's conclusion.
- Scope limitation: this is a targeted spot-check, not a full audit of all 812 listed Actions runs or all 31 workflows. Do not claim global CI is fully green. Continue checking the latest run for each writer workflow and classify any cancelled/failed run before closing the operational gate.


## Latest-workflow status sweep — 2026-10-22

- Queried the live Actions API and grouped the newest run in the returned page by workflow name. It contained 31 distinct workflows (the read-only check plus 30 writer workflows); **all 31 newest observed runs had conclusion `success`**, including Voynich Check run [39727180525](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727180525) on current HEAD `937cade89758d2981f7b14f01c3a6fd4b97c0016`. The latest observed writer runs for EXP-603 and EXP-604 also succeeded.
- This is a point-in-time latest-per-workflow sweep, not a claim that every historical run succeeded. Older cancelled runs remain cancellations, and the earlier push-race failure remains in the history. Recent successful runs show the current pipelines can complete, but they do not prove that all archived experiment outputs are scientifically valid or that every generated artifact is reconciled.
- Operational conclusion: the immediate Actions gate is green for the newest observed run of each of the 31 workflows. Keep the archival/scientific gates closed: do not assign new EXP IDs, merge or delete collisions, or claim decipherment until the GitHub/Library register and parser-conformance work are reconciled.


## Follow-up verification after state/register commits — 2026-10-22

- The Actions run triggered by the status-sweep commit, [39727256177](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727256177), completed with conclusion `success` on commit `8df3c9715e536082555eee459303b22116bdde38`.
- A fresh recursive Git tree query (not truncated) again found 624 experiment folders, 617 distinct numeric folder IDs, and the same seven collision groups: 177, 594, 596, 597, 600, 601, 602. No folders were renamed or deleted.
- The Library cross-surface spot-check read both distinct EXP-623 order reports and recorded their different null models/outcomes in [ARTIFACT_COLLISION_REGISTER.md](../research/ARTIFACT_COLLISION_REGISTER.md). It remains partial: the Library listing is paginated, and no full SHA-256 pairing or bulk content reconciliation has yet been completed.
- The collision-register update itself triggers a new Voynich Check run; verify that run before claiming the very latest commit is green. All newest observed runs for the 31 workflows were successful before this final register update; the post-update check is pending at the time this note was written.


## Library inventory pagination completed — 2026-10-22

- Completed all six pages for `/Investigación Voynich/`: 501 listed items, no listing warnings, and no exact duplicate filenames in this folder snapshot. A filename inventory found 176 names matching the broad EXP/fase/checkpoint/master-document pattern; this is a name-based inventory only, not semantic classification or checksum reconciliation.
- The listing confirms a sequence of large master-document exports `v39`–`v58`, alongside the checkpoint and the two distinct Library EXP-623 order-analysis reports. These are historical artifacts and have not been deleted or overwritten.
- The GitHub tree query returned 2,120 tree entries (1,449 blobs; recursive response not truncated), while the earlier inventory's 2,085 count refers to paths under its own counting method. Do not compare these raw counts as if they were the same unit; directories/tree entries and blob/path counts differ.
- Full GitHub/Library reconciliation is still **not complete**: metadata listing does not expose content SHA-256 for every item, and names/sizes/modified times are not proof of byte identity. Next safe stage is a scoped hash manifest for high-priority scripts/results (starting with EXP-590/593 and the two Library EXP-623 analyses), then expand systematically without modifying originals.


## Inventory artifact and verification — 2026-10-22

- Saved a metadata-only CSV snapshot of all 501 Library items after traversing all six pages: [library_inventory_metadata_2026-10-22.csv](../research/library_inventory_metadata_2026-10-22.csv). It records paths, names, item kind, byte size, and modified timestamp. It deliberately contains no content hashes and must not be mistaken for a byte-level reconciliation.
- The check on commit `82f93451e1cd87c8ee8ae5b2078994fcf31bd5ff` passed: [run 39727348147](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727348147). The check on the collision-register commit `3aa41afdad6fba839130a07582d8202beea29350` also passed: [run 39727305142](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727305142).
- The CSV inventory commit triggers a new check; do not assume that newest run is green until it completes. Historical artifacts remain untouched.


## Scoped Library content-hash checkpoint — 2026-10-22

- Materialized raw bytes for six EXP-623 Library artifacts (two different order-analysis reports, two scripts, and two JSON files) and four selected EXP-590/593 Library artifacts; calculated SHA-256 hashes and saved the values in [library_artifact_sha256_manifest_2026-10-22.md](../research/library_artifact_sha256_manifest_2026-10-22.md).
- This is the first scoped content-hash checkpoint, not a complete reconciliation. GitHub counterparts have not yet all been proven byte-identical, and the EXP-623 JSON-to-script mapping remains a required provenance check.
- The two Library EXP-623 reports remain distinct null-model analyses. Neither is the GitHub EXP-623 ch/sh-context experiment. Do not merge their results or reuse the EXP number as if these were the same experiment.
- Verified the previously pending Voynich Check run [39727424359](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727424359) for commit `6b72a09891d7be30d5121c2875fdf6dd7fe11881`: conclusion `success`. The new manifest commit creates a newer check that must be verified separately.
- No original Library files were edited, no collision was renumbered, and no new scientific experiment ID was allocated. Remaining blockers: GitHub/Library pairwise reconciliation, EXP-623 script/JSON provenance, and independent IVTFF parser conformance.


## Cross-surface ID collision extension — 2026-10-22

- Directly compared the topics of the selected Library reports with current GitHub experiment definitions. Two more same-number mismatches are confirmed: Library EXP-590 is an external-model audit, unlike GitHub EXP-590's coarse folio-range stratification; Library EXP-593 is a zodiac-denominator report, unlike GitHub EXP-593's IVTFF locator-stratified `daiin` analysis and dated corrected-`L)-metadata follow-ups.
- Registered stable descriptive aliases and the distinction in `research/ARTIFACT_COLLISION_REGISTER.md`. The hash manifest provides raw-byte SHA-256 values for the selected Library artifacts; pairwise identity with GitHub files is still unverified, and the EXP-623 report-to-script/JSON mapping remains open.
- The Library list is now fully paginated (501 items, six pages, no warnings). The next gap is content mapping and corpus/parser provenance, not missing pages in that listing.
- No originals changed, no IDs were renumbered, and no new scientific experiment was created. The collision-register commit and this state update each trigger a new Voynich Check; verify the latest run after the final commit before claiming HEAD is green.


## EXP-623 Library pilot provenance clarification — 2026-10-22

- Reviewed the raw JSON and script headers, resolving the intended method pairings: all-token shuffle report ↔ `exp623_resultados_2026-10-19.json` ↔ `exp623_shuffle_holdout.py`; endpoint-preserving interior shuffle report ↔ `exp623_order_null_summary.json` ↔ `exp623_order_null.py`.
- Critical limitation: both reports describe exploratory JavaScript pilot results; the corresponding Python scripts were not run in GitHub Actions. The method pairing is clear from protocol fields, but exact output provenance is not established. Both analyses remain exploratory/unreproduced until the exact scripts are run against the recorded source transcription versions and their outputs compared.
- Recorded this distinction in the SHA-256 manifest and collision register. This does not alter any reported statistics and does not turn either Library report into GitHub EXP-623, which remains the ch/sh interaction test.
- Recent manifest and collision-register commits have successful Voynich Check runs for earlier commits, but the newest commits' checks remain queued/in progress at this checkpoint; verify HEAD's check before claiming current CI green.


## Latest CI close-out — 2026-10-22

- Rechecked the latest Actions runs after the manifest and collision-register updates. Voynich Check runs for the manifest, register, and current state commits all completed successfully: [39727674234](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727674234), [39727710207](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727710207), [39727746074](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727746074), [39727755678](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727755678), [39727764037](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39727764037). Each was observed with conclusion `success`.
- These checks validate the repository's configured checks for those commits; they do not execute the two Library EXP-623 Python pilot scripts, establish complete byte-for-byte Library/GitHub reconciliation, or certify scientific conclusions. The current state commit will trigger another check and must be checked separately.


## EXP-623 source identity verification — 2026-10-22

- Checked the two source transcription blob IDs recorded in the Library pilot JSON against the live `master` Git tree. Both match exactly: ZL3b `2a4533ab9bdfa85db9bad602d590978953055df1` (411,671 bytes), IT2a `4d6d3f2537b1f507a257529b49c94af7d6e03446` (342,104 bytes).
- This closes source-file identity for those pilot metadata records, but not output provenance: the saved Python scripts still need to be executed against those exact source blobs and their fresh JSON outputs compared with the JavaScript pilot results.
- The two analyses have different declared filters (all matching locus records vs P0-only paragraph-body loci), different sample sizes, and different null constructions. Treat them as separate exploratory analyses, not as direct replications. Details are in `research/library_artifact_sha256_manifest_2026-10-22.md`.
- No original results were overwritten and no new experiment ID was allocated. Check the workflow triggered by this state update before claiming the current HEAD has passed CI.


## Cross-surface namespace triage expansion — 2026-10-22

- Recompared the complete 501-item Library inventory with the 2,122-entry GitHub tree. Thirty-four EXP-number groups overlap across surfaces and need semantic/provenance triage; numeric overlap alone is not proof of same artifact.
- Confirmed question-level mismatches now total eleven, including EXP-590, 591, 592, 593, 595, 598, 599, 600, 601, 602 and 623. See `research/ARTIFACT_COLLISION_REGISTER.md` for the comparison and safe handling. The count means topic/protocol mismatch, not invalid science.
- Seven internal GitHub folder-ID collisions (177, 594, 596, 597, 600, 601, 602) remain distinct from the cross-surface mismatches.
- The Library SHA-256 manifest is deliberately scoped to ten files; complete byte-level pairing across all candidate artifacts is still pending. Do not rename or merge anything until exact references, scripts, JSON, and corpus/parser hashes are reconciled.
- No new experiment IDs were assigned. The last verified Voynich Check for an earlier state commit succeeded, but the newest state and collision-register commits have new checks to verify before claiming HEAD is green.


## Segunda pasada de triage semántico — 2026-10-22

- El registro de colisiones se amplió en el commit `049181b656abe8af8d6643606c8ee6844e779f27` con la comparación de EXP-603–613 y EXP-616–621 entre informes de Biblioteca y protocolos/resultados GitHub.
- El registro acumula ahora 28 mismatches semánticos identificados por tema/método. Son diferencias de pregunta y/o diseño, no pruebas de que un resultado sea falso ni de duplicación binaria. La reconciliación de los demás grupos solapados continúa pendiente.
- Se observó una diferencia estructural en GitHub EXP-620: existe `partial_audit.md`, no `result.md` en la ruta esperada. No se clasifica como fallo científico sin revisar el workflow y el artefacto completo.
- La síntesis de GitHub EXP-621 sobre ch/sh mantiene pendientes el holdout por sección, la revisión completa de multiplicidad y la auditoría independiente del parser. Los análisis de sensibilidad correlacionados no deben contarse como réplicas independientes.
- No se renombró, fusionó, borró ni sobrescribió ningún original. No se asignó ningún EXP ID nuevo. El SHA-256 manifest sigue limitado a diez archivos; los emparejamientos binarios y la reproducción exacta de EXP-623 siguen abiertos.
- Tras este commit, comprobar el estado de Actions del HEAD más reciente; no inferir CI verde a partir de ejecuciones anteriores.


## Cierre del triage semántico de IDs compartidos — 2026-10-22

- La última pasada revisó los seis IDs restantes del solapamiento (EXP-589, 594, 596, 597, 622 y 624). El registro documenta ahora discrepancias semánticas de tema/método para los **34 de 34 grupos** con ID compartido entre Biblioteca y GitHub.
- Esto cierra el triage semántico por títulos y protocolos, no la auditoría binaria: aún faltan hashes de contenido comparables para todos los candidatos, emparejamiento script→JSON→informe y reproducción exacta de los pilotos LIB-EXP-623.
- EXP-594, EXP-596 y EXP-597 tienen además más de una carpeta GitHub bajo el mismo número; no fusionar las carpetas. Persisten siete IDs de carpeta duplicados internamente: 177, 594, 596, 597, 600, 601 y 602.
- No se modificaron ni renombraron artefactos experimentales originales; no se asignó ningún ID nuevo. El manifiesto SHA-256 sigue siendo un checkpoint de diez archivos, no una cobertura total.
- El nuevo commit de cierre del registro debe pasar su propio Voynich Check antes de considerar CI del HEAD verde.


## EXP-623 reproducción aislada en curso — 2026-10-22

- Se copiaron a rutas de reproducción separadas los dos scripts de Biblioteca sin modificar los originales: `research/reproduction/exp623_order_null.py` (nulo que preserva extremos) y `research/reproduction/exp623_shuffle_holdout.py` (barajado de todos los tokens dentro del locus).
- Se añadió `.github/workflows/exp623-reproduction.yml`, que comprueba los Git blob IDs de las fuentes ZL3b e IT2a antes de ejecutar ambos análisis y publica los JSON como artefactos de Actions. No sustituye los resultados históricos ni asigna un nuevo EXP ID.
- Ejecución inicial del workflow: [39729111827](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39729111827), iniciada en el commit `40e636cd7815f0b2de5d10d5ea6b7a47f1ad645d`; al redactar esta nota, el paso del primer análisis seguía en curso. No declarar reproducción completa hasta que termine y se comparen los outputs con los JSON piloto.
- El workflow de comprobaciones ordinarias para ese mismo commit es [39729111832](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39729111832), observado completado con éxito. La reproducción científica es un control separado y aún no se considera validada.
- Los scripts compilan en Python 3.12. Esto solo valida sintaxis; no constituye por sí mismo reproducción de resultados.


## LIB-EXP-623 pilot reproduction completed — 2026-10-22

- The isolated Actions reproduction completed successfully: [run 39729111827](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39729111827), workflow commit `40e636cd7815f0b2de5d10d5ea6b7a47f1ad645d`. Both source-blob verification, script compilation, both analysis runs, and artifact upload passed.
- Exact transcription blob identities were verified in the workflow: ZL3b `2a4533ab9bdfa85db9bad602d590978953055df1` (411,671 bytes); IT2a `4d6d3f2537b1f507a257529b49c94af7d6e03446` (342,104 bytes).
- Endpoint-preserving pilot: ZL3b 3,879 loci / 32,959 tokens and IT2a 3,881 / 33,380; the 10-split mean/median/range and categorical outcomes match the saved JS pilot within floating-point rounding. Both transcriptions have 10/10 splits above the null q95 and maximum.
- All-token shuffle pilot: ZL3b 5,376 loci / 39,298 tokens and IT2a 5,207 / 37,945; counts and categorical outcomes match exactly, with mean-loss differences around 10^-15 bits/token. Original sequence loss is lower in 3/20 ZL3b splits and 0/20 IT2a splits; shuffles have lower loss than original in 76.9% and 98.8% of draws.
- These are distinct protocols: one refits the model under an endpoint-preserving interior-shuffle null; the other scores all-token-shuffled test sequences against a model fit to original training sequences. Do not combine their statistics. Neither supports semantic decipherment; the two transcriptions are not independent manuscripts.
- Durable comparison note: `research/reproduction/EXP623_REPRODUCTION_COMPARISON_2026-10-22.md`. Immutable run artifact ID 12404740024 contains both reproduced JSON outputs and their SHA-256 values are recorded in the comparison note.
- This closes the execution-provenance gap for these two Library pilots only. Full Library↔GitHub byte-level reconciliation, seven internal duplicate GitHub folder IDs, and independent IVTFF parser audit remain open. No original Library pilot was overwritten, renamed, merged or deleted; no new EXP ID was assigned.
- Verify the latest Voynich Check for this state update and the collision-register update before claiming the current HEAD has passed CI.


## Estado corregido tras cierre de reproducción EXP-623 — 2026-10-22

Esta sección sustituye cualquier nota anterior que describa la reproducción como «en curso» o pendiente de comparación: la reproducción terminó y el informe comparativo quedó registrado en el commit `c988bfd9c3aaa5316fd4fac6863fa7fdae042320`.

- Comparación documentada: `research/reproduction/EXP623_REPRODUCTION_COMPARISON_2026-10-22.md`.
- Los dos protocolos y los dos JSON de salida se ejecutaron en Actions contra los blobs de transcripción fijados y verificados. Coincidencias de conteos y resultados reproducidos descritas en el informe; no combinar los nulos ni llamar a los cortes repetidos «réplicas independientes».
- El workflow de reproducción terminó en éxito: [39729111827](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39729111827). El control ordinario del HEAD `c988bfd9c3aaa5316fd4fac6863fa7fdae042320` también terminó en éxito: [39730573888](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39730573888). Esto confirma CI para ese HEAD concreto, no garantiza que cada workflow histórico o cada análisis sea científicamente válido.
- Próximos trabajos prioritarios: comparación de bytes/hashes Biblioteca↔GitHub en pares de artefactos; resolución documental de las siete carpetas con IDs duplicados (177, 594, 596, 597, 600, 601, 602); y auditoría independiente del parser IVTFF. No asignar IDs EXP nuevos ni sobrescribir originales antes de terminar la reconciliación.
