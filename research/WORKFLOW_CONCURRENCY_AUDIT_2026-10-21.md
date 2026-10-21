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
