# Auditoría de ejecución y concurrencia — 2026-10-21

Estado: **CI funcional en runs identificados; riesgo de concurrencia parcialmente mitigado y aún abierto**.

## Evidencia de GitHub Actions

### Run 39491327187 — éxito
- Job: `research`, job ID `118866025977`.
- Conclusión: `success`.
- Pasos completados: auditoría de metadatos IVTFF, EXP-590, EXP-593, EXP-622, réplica EXP-623 y escritura de resultados.
- Enlace: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39491327187
- El log confirma que se escribieron los artefactos corregidos de EXP-593 y que el push terminó en el segundo intento, después de un rechazo no-fast-forward.
- Para EXP-622 (ZL3b): interacción next-minus-prev = 0.005296; p bilateral = 0.823418 (10.000 permutaciones).
- Para EXP-623 (IT2a): interacción next-minus-prev = -0.009110; p bilateral = 0.690031 (10.000 permutaciones).
- Interpretación: estas dos réplicas no aportan evidencia de una interacción contextual ch/sh bajo los nulos especificados. Son pruebas exploratorias, no resultados de descifrado.

### Run 39490460729 — fallo de escritura
- Job ID `118861932497`.
- Los cuatro análisis finalizaron, pero el paso de commit/push falló con `cannot lock ref 'refs/heads/master'` porque otra escritura movió la referencia entre el rebase y el push.
- Enlace: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39490460729
- El run es anterior a la mitigación con reintentos que aparece en el workflow autónomo actual. No hubo force-push.

## Mitigación observada

`.github/workflows/voynich-agent.yml` actualmente declara:
- `concurrency.group: voynich-research` y `cancel-in-progress: false`, lo que serializa ejecuciones de ese mismo workflow.
- Reintento de rebase/push hasta cinco veces, sin force-push.
- `permissions.contents: write`, necesario para publicar artefactos.

Límite: la concurrencia de GitHub Actions con el mismo grupo no serializa automáticamente todos los demás workflows que escriben en `master`. La existencia de 30 workflows con escritura, según la auditoría estructural previa, mantiene un riesgo entre workflows distintos. No se debe declarar resuelto hasta auditar sus triggers, grupos de concurrencia y pasos de push.

## Decisiones de conservación

- No borrar ni sobrescribir los resultados históricos.
- Los resultados corregidos de EXP-593 quedan como reproducidos por el run citado, pero la inferencia posicional sigue limitada por el modelo nulo y el parser.
- La captura de Voynich Check de 8 segundos muestra checks verdes, pero no identifica un run ID/SHA; se registra como evidencia visual sin asociarla a un commit concreto.
- No asignar nuevos IDs EXP hasta reconciliar el índice histórico y las colisiones.

## Próximos pasos
1. Revisar los restantes workflows con `git push` o escrituras a `master`; buscar especialmente los que carecen de `concurrency` o reintento seguro.
2. Cotejar hashes y referencias de los artefactos EXP-590/593.
3. Completar el inventario GitHub/Biblioteca y clasificar las 62 carpetas de triage.


## Auditoría completa de los 31 workflows — 21-10-2026

Se revisaron los 31 ficheros YAML de `.github/workflows/` en `master`, incluidos triggers, permisos, grupos de concurrencia y comandos de commit/push.

### Resultado cuantitativo

- **31 workflows en total:** 1 workflow de comprobación de solo lectura y **30 workflows que pueden escribir resultados en `master`**.
- **9/30** workflows de escritura no declaran `concurrency`: `voynich-exp603.yml` a `voynich-exp611.yml`. Tampoco implementan rebase/reintento en su paso de push.
- **21/30** sí declaran `concurrency`, pero sus grupos son específicos de cada workflow; por tanto, no se bloquean mutuamente y no evitan carreras entre workflows distintos.
- Solo **9/30** incluyen un bucle explícito de rebase/push con reintentos: `voynich-agent.yml`, `voynich-folio-clustered-confirmation.yml`, `voynich-heldout-prediction.yml`, `voynich-independent-parser-audit.yml`, `voynich-initial-context.yml`, `voynich-marginal-successors.yml`, `voynich-paired-sensitivity.yml`, `voynich-transcription-concordance.yml` y `voynich-two-token-context.yml`.
- **21/30** no incluyen reintento seguro: `voynich-corpus-experiments.yml`, `voynich-exp603.yml`–`voynich-exp611.yml`, `voynich-folio-influence.yml`, `voynich-lexical-controls.yml`, `voynich-line-level-audit.yml`, `voynich-line-metadata-tests.yml`, `voynich-locus-tests.yml`, `voynich-paragraph-marker-audit.yml`, `voynich-paragraph-marker-tests.yml`, `voynich-paragraph-replication.yml`, `voynich-parser-conformance.yml`, `voynich-position-controls.yml` y `voynich-stratified-tests.yml`.
- `voynich-corpus-experiments.yml` marca `continue-on-error: true` en el paso de publicación; eso puede dejar una ejecución global en verde aunque falle la escritura de resultados.

### Conclusión operativa

La causa de riesgo no es solo la falta de `concurrency`: los grupos diferentes permiten que dos workflows distintos escriban simultáneamente. El fallo histórico `cannot lock ref 'refs/heads/master'` es coherente con este diseño. No se hizo force-push ni se borró ningún resultado durante esta auditoría.

**No se declaran los riesgos de concurrencia resueltos.** La siguiente corrección técnica debe estandarizar el mecanismo de escritura en los 30 workflows: rebase sobre la referencia remota, reintento limitado y fallo explícito si se agotan los intentos; conservar los artefactos y no ocultar errores de push. Antes de aplicar cambios masivos, probar la plantilla en un workflow piloto y verificar el run.



## Follow-up correction — 2026-10-22

The earlier recommendation to use one shared concurrency group across all writers was not retained. GitHub Actions allows only one running and one pending run per group; a newer run can replace/cancel an older pending run. The shared-group trial caused several queued writer runs to be cancelled, so it was replaced with **distinct concurrency groups per workflow**. All 30 write-capable workflows were rechecked: each has a workflow-specific concurrency group with `cancel-in-progress: false` and a bounded five-attempt rebase/push retry loop; the read-only `voynich-check.yml` is excluded. This prevents overlapping runs of the same workflow and makes cross-workflow push races retryable, rather than pretending one group can queue every workflow indefinitely.

Verification is not yet closed: multiple `Voynich Check` runs and workflow-specific runs have succeeded, while some runs triggered during the configuration change were cancelled under the temporary shared-group design and others remain queued/in progress. A cancelled run is not a pass. Recheck Actions for the latest master commit and confirm the final conclusion of each relevant run before resuming new experiments. No force-push or historical result deletion was used.
