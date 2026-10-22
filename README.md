# Investigación computacional del Manuscrito Voynich

Repositorio de trabajo: `kyrian20/voynich-autoexploration` (rama `master`).

## Estado operativo actual — 22 octubre 2026

La arquitectura de publicación se ha reparado: **un único publicador y 31 workflows lectores**, con artefactos y guardias de CI. [Estado, pruebas y límites actuales](research/OPERATIONAL_STATUS.md). [Registro inequívoco de las 624 carpetas](research/EXPERIMENT_PATH_REGISTRY.json). La validación científica y la conformidad completa IVTFF siguen pendientes.

## Estado histórico — 20 octubre 2026

**Prioridad actual: estabilizar el corpus y la trazabilidad antes de añadir nuevas tandas de experimentos.** El árbol contiene más de 2.000 rutas y aproximadamente 1.900 archivos bajo `experiments/`; hay resultados útiles, experimentos históricos y algunos conflictos de numeración. No interpretar el número máximo de EXP como número de conclusiones válidas.

## Índice de navegación

- [`SOUL.md`](SOUL.md): objetivo, principios y ciclo de investigación.
- [`CLAUDE.md`](CLAUDE.md): instrucciones operativas y documentos de estado.
- [`research/EXPERIMENT_REGISTER.md`](research/EXPERIMENT_REGISTER.md): registro de numeración y conflictos conocidos. Consultar antes de asignar cualquier ID nuevo.
- [`research/ORDER_AND_STABILIZATION_STATUS_2026-10-21.md`](research/ORDER_AND_STABILIZATION_STATUS_2026-10-21.md): estado operativo actual, bloqueos y orden obligatorio antes de reanudar experimentos.
- [`research/WORKFLOW_CONCURRENCY_AUDIT_2026-10-21.md`](research/WORKFLOW_CONCURRENCY_AUDIT_2026-10-21.md): evidencia de runs 39491327187/39490460729 y riesgos de escrituras concurrentes.
- [`research/repository_inventory_audit_2026-10-20.md`](research/repository_inventory_audit_2026-10-20.md): inventario estructural de 2.085 rutas, colisiones de ID y workflows; no equivale a auditoría científica completa.
- [`research/RESEARCH_INTEGRITY_STANDARD.md`](research/RESEARCH_INTEGRITY_STANDARD.md): norma obligatoria de estados, trazabilidad, controles y publicación.
- [`research/ARTIFACT_COLLISION_REGISTER.md`](research/ARTIFACT_COLLISION_REGISTER.md): colisiones confirmadas entre IDs de GitHub y la Biblioteca, con alias sin borrar originales.
- [`research/experiments/2026-10-20-exp590-erratum.md`](research/experiments/2026-10-20-exp590-erratum.md): errata formal para los resultados EXP-590 afectados por el uso histórico de `$Q`.
- [`state/canonical_methodology.md`](state/canonical_methodology.md): metodología histórica canónica. Puede reflejar convenciones antiguas; contrastar con auditorías recientes.
- [`state/current_state.md`](state/current_state.md): estado operativo histórico, consultar antes de cambiar decisiones.
- [`state/working_position.md`](state/working_position.md): síntesis de hipótesis y discriminación teórica.
- [`state/hypothesis_backlog.md`](state/hypothesis_backlog.md): hipótesis pendientes.
- [`state/findings.md`](state/findings.md): hechos/conclusiones acumuladas; revisar ID y evidencia antes de añadir.
- [`state/failed_approaches.md`](state/failed_approaches.md): enfoques fallidos o no respaldados.
- [`state/open_questions.md`](state/open_questions.md): cuestiones sin resolver.
- [`state/iteration_log.md`](state/iteration_log.md): registro cronológico.
- [`research/external_research_scan_2026-10-20.md`](research/external_research_scan_2026-10-20.md): exploración externa reciente.
- [`research/exp_625_external_methods_integration_plan.md`](research/exp_625_external_methods_integration_plan.md): cómo convertir métodos externos en pruebas nuestras.
- [`research/exp_624_parser_disagreement_and_prediction_gate.md`](research/exp_624_parser_disagreement_and_prediction_gate.md): bloqueo actual de tokenización y etiquetas Currier.
- [`research/ivtff_tokenization_policy_2026-10-20.md`](research/ivtff_tokenization_policy_2026-10-20.md): reglas del formato oficial y fixtures exigidos antes de reabrir la predicción A/B.
- [`research/exp_622_external_context_and_next_tests.md`](research/exp_622_external_context_and_next_tests.md): contexto externo y siguientes pruebas.
- [`research/EXTERNAL_RESEARCH_REVIEW.md`](research/EXTERNAL_RESEARCH_REVIEW.md) y [`research/EXTERNAL_KNOWLEDGE_LOG_2026-10-20.md`](research/EXTERNAL_KNOWLEDGE_LOG_2026-10-20.md): comparación y registro de literatura externa.

## Estructura

- `data/transcriptions/`: transcripciones EVA ZL3b, IT2a, ZL3a y V101, más documentación. No reemplazar originales sin versionado/checksum.
- `data/reference_corpora/`: textos de comparación en varias lenguas; revisar procedencia, licencia y duplicados antes de utilizarlos.
- `experiments/`: experimentos históricos numerados, normalmente con scripts, resultados y datos. Preservar resultados negativos y no reutilizar IDs.
- `scripts/`: implementaciones ejecutables recientes y auditorías auxiliares.
- `research/experiments/`: resultados recientes de análisis, en Markdown/JSON.
- `research/blocks/` y `research/protocols/`: planes de bloques y protocolos.
- `research/diagnostics/`: diagnósticos de ejecución, permisos y calidad.
- `research/agent-reports/`: informes de ejecuciones automáticas.
- `state/`: memoria de trabajo, metodología, hipótesis, resultados acumulados y archivo histórico.
- `seeds/`: conversaciones y material de arranque; no es una fuente de resultados validados.
- `.github/workflows/`: automatizaciones de Actions.

## Resultados recientes y su estatus

1. **EXP-622 / EXP-623 (`ch/sh`)**: replicación entre transcripciones de una interacción contextual concreta. El efecto no fue significativo y cambió de signo entre transcripciones; no respalda la hipótesis de especificidad contextual probada. Las transcripciones son variantes del mismo manuscrito, no muestras independientes.
2. **EXP-602 (predicción held-out)**: prueba de posición inicial de token en líneas Currier B/P0; no es un clasificador Currier A frente a B.
3. **Auditoría de parser**: el protocolo v1 registró 1.466/1.472 desacuerdos de tokens. Tras corregir el terminador de comentarios, el tratamiento de alternativas y los marcadores dentro de alternativas, el protocolo v7 registra cero desacuerdos entre parsers para ZL3b (5.385 registros) y ZL3a (5.389). Es acuerdo bajo la política de normalización documentada, no certificación completa del formato; la predicción Currier A/B sigue bloqueada hasta completar los fixtures.
4. **EXP-593**: se detectó una asignación incorrecta de clase mediante `$Q` en una versión previa; Currier A/B debe salir de `$L=A/B`. Los resultados antiguos por clase se conservan por trazabilidad y no deben usarse como válidos hasta una repetición verificada.
5. **EXP-589 y otros análisis de `daiin`**: hay resultados de enriquecimiento/posición y controles de nulo; consultar informes y scripts exactos antes de resumirlos como evidencia. La posición estructural no equivale a traducción.

## Orden obligatorio de trabajo

1. Revisar `research/EXPERIMENT_REGISTER.md` y `state/iteration_log.md` antes de crear EXP nuevo.
2. Resolver las reglas de tokenización IVTFF mediante fixtures con salidas esperadas y justificación documental.
3. Validar metadatos `$L=A/B`; no sustituirlos por `$Q` o `$I`.
4. Reproducir los informes recientes desde los scripts y conservar hashes, parámetros, semillas, logs y resultados.
5. Solo después ejecutar un único experimento confirmatorio preinscrito; dividir por folio y comparar con controles adecuados.
6. Al cerrar un experimento, ejecutar la auditoría definida en `skills/`, actualizar registro e índice de estado y conservar resultados negativos.
7. No confundir una ejecución de GitHub Actions, un EXP y una fase histórica: son numeraciones distintas.

## Deuda técnica conocida

- Se eliminó la ruta accidental anidada `.github/workflows/.github/workflows/voynich-check.yml` (el historial Git conserva el archivo). El workflow canónico `.github/workflows/voynich-check.yml` ahora comprueba los archivos de transcripción, la sintaxis de todos los scripts Python y los metadatos Currier `$L`.
- Hay workflows específicos para múltiples EXP, lo que dificulta mantenerlos; evaluar consolidación después de confirmar que sus triggers y artefactos no se pierden.
- Hay conflicto de numeración alrededor de EXP-590/591/592 documentado en el registro. No renumerar silenciosamente los artefactos históricos.
- El workflow de validación parece exigir `README.md`; este archivo restablece ese requisito.
- El workflow de agente y las automatizaciones deben describirse como asistentes de ejecución, no como investigación continua autónoma. Confirmar cada run y su artefacto antes de declarar resultados.

## Regla de evidencia

Cada conclusión debe apuntar a script, corpus/transcripción, hash, unidad de análisis, división de evaluación, baseline, nulo/control, semilla y resultado. Las hipótesis externas se registran como hipótesis hasta que se repliquen independientemente. No se afirma desciframiento sin recuperación semántica verificable.

## Criterio de calidad institucional

El repositorio todavía no se declara completamente limpio: persisten la discrepancia de tokenización, colisiones de IDs entre GitHub y la Biblioteca, y ejecuciones CI cuya confirmación debe comprobarse. La norma de integridad define el orden de cierre. No se borrarán datos históricos ni se publicarán como validados resultados afectados por defectos conocidos.
