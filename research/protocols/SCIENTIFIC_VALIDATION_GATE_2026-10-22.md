# Puerta científica de integración — 22 octubre 2026

Estado: protocolo propuesto, sin nuevos resultados ni traducción.

## Base comprobada
- Rama master: dfb660e38523732ec9e00a3959eba33f2139481c.
- Voynich Check: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39847415625 (success).
- El registro `research/EXPERIMENT_PATH_REGISTRY.json` distingue rutas únicas de alias numéricos repetidos.
- `research/INTENSIVE_REVIEW_2026-10-22.md` documenta reparación de rutas, capa IVTFF sin pérdida y limitaciones de reproducción.
- `research/next_decisive_test_plan_2026-10-22.md` declara que el predictor de `daiin` ya evaluado no superó su regla primaria: no repetirlo disfrazado ni declarar desciframiento.

## Tareas de Codex y revisión humana (en orden)
1. Leer `SOUL.md`, `CLAUDE.md`, `state/working_position.md` y `state/committed_claims.md` antes de planear cambios.
2. Auditar la batería común incorporada en PR #3: declarar exactamente qué outputs proceden de ejecución real, cuáles son reconstruidos y cuáles carecen de material bruto histórico. Comparar checksums, fuentes, parámetros y versiones. No alterar outputs históricos.
3. Diseñar previamente una prueba discriminativa nueva frente a tres mecanismos: Naibbe con texto claro conocido, autocitación y un predictor entrenable; controles comparables con misma transcripción, tokenizador, filtrado, presupuesto y splits disjuntos por folio. Prohibido elegir parámetros mirando el conjunto reservado. Criterio primario e IC agrupado por folio predeclarados; documentar controles negativos.
4. Contrastar literatura: Michael Greshko, Cryptologia 2025 DOI 10.1080/01611194.2025.2566408; Christophe Parisel arXiv:2604.25979v2; Timm & Schinner, Cryptologia DOI 10.1080/01611194.2019.1596999; estudios Cryptologia DOI 10.1080/01611194.2026.2697318 y 10.1080/01611194.2026.2693462. Diferenciar DOI/preprint/revisión por pares, texto completo vs resumen y afirmaciones aún no reproducidas. No priorizar fuentes de la dark web sin procedencia contrastable.
5. Antes de cualquier modificación de código, registrar hipótesis refutable, hashes de entrada, métricas, baselines, semilla, entorno, reglas de aceptación y qué resultado la falsaría. No volver a usar un alias EXP ambiguo.
6. Publicar código y documentación en rama separada como PR borrador, no fusionar automáticamente ni modificar `state/committed_claims.md`; conservar hallazgos negativos, artefactos, trazas y errores. No activar APIs de pago ni exponer secretos.

## Criterios de finalización
- Ingeniería verde no equivale a inferencia validada.
- No afirmar que se descifró texto sin traducción consistente, reproducible y contrastada por evidencia externa.
- Marcar `BLOCKED_MISSING_INPUT` cuando proceda.
- No repetir EXP-607 ni EXP-602 sin justificación y diseño nuevo.
