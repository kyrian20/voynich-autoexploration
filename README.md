# Investigación computacional del Manuscrito Voynich

**Dirección de investigación — 25-10-2026:** [estrategia de desciframiento y contribución verificable](research/DECIPHERMENT_AND_RECOGNITION_STRATEGY_2026-10-25.md). Priorizar pruebas que distingan explicaciones y una aportación reproducible para revisión externa. El [piloto visual](research/protocols/semantic-anchor-study.md) permanece **BLOCKED** y deja de ser el eje exclusivo: no continuar máscaras sin revisión y anotadores independientes disponibles. No hay traducción validada ni garantía de reconocimiento. Esta decisión no desactiva automatizaciones.

Repositorio de trabajo: `kyrian20/voynich-autoexploration` (rama `master`).

**Auditoría de word-pair replication — 01-11-2026:** [reimplementación parcial de la métrica de Zhang y Sheng](research/maintenance/2026-11-01-zs-wordpair-audit/REPORT.md); preprocesamiento parcialmente alineado (P/C/R, 225 páginas comunes y glifos EVA); la cifra sigue sin reproducirse porque la fórmula de propensión y algunos detalles de inclusión no están publicados. Código y resultados por semilla adjuntos.

**Sensibilidad de posición final de `daiin` a códigos opacos — 30-10-2026:** [comparación acotada de la vista ASCII de EXP-590 con una política que conserva `@NNN;` sin descifrar](research/maintenance/2026-10-30-exp590-opaque-token-positional-sensitivity.md). El recuento final depende de la política; no reejecuta permutaciones ni rehabilita resultados históricos. Comprobar CI exacta antes de reutilizar las cifras.

**Contacto de códigos high-ASCII con letras ASCII — 30-10-2026:** [auditoría acotada de fragmentación potencial en EXP-590](research/maintenance/2026-10-30-exp590-high-ascii-adjacency.md). Separa códigos dentro/fuera de ligaduras y conserva los originales; no recalcula ni rehabilita métricas históricas. Verificar CI del commit exacto antes de reutilizar recuentos.

**Conciliación IVTFF de registros sin tokens ASCII — 30-10-2026:** [diferencia comprobable entre códigos high-ASCII y lecturas ilegibles en ZL3b/ZL3a/IT2a](research/maintenance/2026-10-30-ivtff-high-ascii-unreadable-record-reconciliation.md). Es una reparación de cobertura descriptiva; no rehabilita EXP-590 ni aporta traducción. Consultar la CI de la PR antes de afirmar reproducción remota.

**Auditoría retrospectiva — 24-10-2026:** [inventario de errores conocidos, PR pendientes y verificaciones no concluidas](research/maintenance/2026-10-24-retrospective-audit-status.md). No equivale a ejecutar ni certificar todo el historial. Las propuestas semánticas recientes son protocolos, no traducciones validadas.

**Estado de revisión — 23-10-2026:** no hay validación global del historial ni traducción validada. Las comprobaciones operativas y reproducciones tienen alcance específico. Consulta el [alcance de reparación](research/maintenance/2026-10-23-repair-scope.md), la [revisión de esta base](research/maintenance/2026-10-23-history-status-review.md) y los informes fechados enlazados abajo antes de reutilizar resultados. Los borradores de PR son propuestas; no forman parte de master mientras no se integren.

**Correcciones de EXP-001/267/288 — 23-10-2026:** [adjudicación de tablas, etiquetas e inferencias](research/maintenance/2026-10-22-claim-link-adjudication/REPORT.md) y [alcance de entropía inicial](research/maintenance/2026-10-23-exp001-claim-scope/REPORT.md), con snapshots comprobados y controles explícitos en CI. Las erratas CORRECTION.md junto a los originales indican qué afirmaciones no deben reutilizarse.

**Corrección de EXP-170 — 23-10-2026:** [auditoría de los 400 vectores conservados](research/maintenance/2026-10-22-exp170-audit/REPORT.md) y [tabla corregida](research/maintenance/2026-10-22-exp170-audit/TABLE.md). Corrige 50 componentes numéricos, dos clasificaciones, recuentos y la confusión máximo/media. Los originales se conservan congelados; no se han reproducido las simulaciones ni se validan sus etiquetas de idioma.

**Incremento BPE frente a carácter — 23-10-2026:** [comparación con objetivo idéntico y control de bordes/longitud](research/analysis/2026-10-23-subword-increment/REPORT.md). No se respalda incremento del contexto BPE en las cuatro vistas Voynich; sí se observa en César/Dante. La señal previa también se recupera con un contexto de un carácter. Control estricto de movilidad escasa; no prueba ausencia de lenguaje ni discrimina teorías.

**Dependencia entre subunidades — 23-10-2026:** [predictor BPE con puerta natural y controles](research/analysis/2026-10-23-subword-boundary/REPORT.md). La puerta se supera en César y Dante; las cuatro vistas Voynich también muestran ganancia superior a sus 16 controles de entrenamiento barajado. Resultado exploratorio de orden, sin significado asignado ni discriminación de teorías; intento sintético fallido y reparación conservados.

**Límite de soporte del predictor — 23-10-2026:** [descomposición exacta de contextos](research/maintenance/2026-10-23-identity-support/REPORT.md). Solo 7,29–8,27 % de las tripletas Voynich permiten una corrección de identidad no trivial con las tablas entrenadas; César 0,42 % y Dante 2,95 %. Diagnóstico del instrumento, sin conclusión lingüística ni cambio de pesos.

**Memoria de dos tokens y reparación de sesgo — 23-10-2026:** [predictor calibrado, intento fallido conservado y controles](research/analysis/2026-10-23-two-token-residual/REPORT.md). Se corrigió una ganancia artificial de suavizado antes del análisis real. La identidad adicional se desactiva en las cuatro vistas Voynich y ofrece señal primaria incierta en los dos controles naturales: no discrimina teorías ni traduce. [Alcance de la revisión de errores](research/maintenance/2026-10-23-repair-scope.md).

**Verificación CI corregida y control alternativo — 23-10-2026:** [evidencia de ejecuciones push satisfactorias](research/CI_VERIFICATION.md) y [control de contexto por folio](research/maintenance/2026-10-23-folio-context-control/REPORT.md). La alternativa permite variar 196 de 325 predecesores de cierres -am en ZL3b, conservando inventario de folio y plantillas de línea, pero relajando el inventario de cada línea. Es otro nulo; no se presenta como prueba semántica.

**Soporte del control de contexto — 23-10-2026:** [oportunidades exactas de intercambio del predecesor final](research/maintenance/2026-10-23-predecessor-opportunities/REPORT.md). Al conservar extremos de línea, inventario, bordes y longitud, solo 16 de 325 cierres -am ZL3b permiten cambiar su predecesor en la vista por defecto. Diagnóstico de soporte, sin contraste semántico ni cálculo de potencia.

**Contribuciones léxicas de -am — 23-10-2026:** [descomposición exacta y exclusión de una forma cada vez](research/maintenance/2026-10-23-am-lexical-contributions/REPORT.md). En las mismas líneas B/P0 sin marcador explícito, el exceso final persiste tras dejar de contar cualquiera de las formas -am, bajo las ocho políticas de lectura. Sensibilidad descriptiva, sin asignación semántica.

**Separación de párrafos — 23-10-2026:** [estratos por P0/otros P y marcador explícito de fin](research/maintenance/2026-10-23-paragraph-strata/REPORT.md). En ZL3b, el exceso -am/final persiste en las 1.883 líneas P0 sin marcador bajo las ocho vistas y las 40 retiradas de folio. Ausencia de marcador no se equipara automáticamente con interior de párrafo. Resultado descriptivo, sin significado asignado.

**Avance del 23-10-2026:** [puente de lectores para los patrones -am/final e y/inicial](research/maintenance/2026-10-23-exp173-reader-bridge/REPORT.md): tres transcripciones, ocho políticas completas, poblaciones comunes y sensibilidad al retirar cada folio. Los dos excesos descriptivos persisten dentro de esta rejilla; se documentan las diferencias de extremos y las limitaciones IVTFF. No hay traducción ni nueva significación estadística. Incluye reproducción en CI de las cuatro auditorías acotadas de EXP-173.

La [batería común lenguaje/cifrado/generación](experiments/common_battery_2026_10_22/result.md) conserva EXP-170 y publica protocolo y resultados nuevos; los tokens archivados siguen pendientes de autorización y recuperación (véase PUBLICACION.md del experimento). Su primaria no discrimina barajados; no valida una teoría del manuscrito.

## Estado operativo actual — 22 octubre 2026

**Cuatro lectores restantes reproducidos:** [selección efectiva de EXP-267/288/001/170 y defecto de coordenadas de EXP-001](research/maintenance/2026-10-22-remaining-readers/REPORT.md). Coincidencia de secuencias, hashes y seis controles en CI; las entradas bilingües o inglesas siguen excluidas como bases monolingües latinas. No valida los experimentos completos.

**Investigación abierta unificada:** [bloque de orden residual integrado con corpus y lector canónicos](research/analysis/2026-10-22-residual-order/README.md), con reproducción conjunta en CI. [Informe](research/analysis/2026-10-22-residual-order/REPORT.md) y [revisión de identidad de corpus](research/CORPUS_IDENTITY_REVIEW.json). Los análisis históricos que dependan de corpus mal identificados siguen pendientes de adjudicación; no se declara validación científica global.

**Contraste científico con fuentes externas:** [controles exactos de posición/bordes y reproducción de un driver publicado](research/decipherment/2026-10-22-constrained-pair/REPORT.md). La pareja daiin→dam no se admite como ancla semántica: al conservar bordes el control espera 7–7,5 de las ocho apariciones, con muy poca variación residual.

**Revisión de precisión:** [validación estricta del manifiesto y distribución exacta del control local](research/maintenance/2026-10-22-precision-review/REPORT.md). Se conservan los cálculos Monte Carlo anteriores como históricos; la selección retrospectiva sigue limitando la inferencia.

**Continuidad auditada:** [identidad de 14 corpus, duplicados por bytes y control de contaminación EXP-607](research/maintenance/2026-10-22-duplicate-control/REPORT.md). [Primer control local de daiin→dam con denominadores](research/decipherment/2026-10-22-daiin-dam-control/REPORT.md): exploratorio, sin significado asignado.

**Lectura candidata de f41v:** [comparador histórico recuperado y ensayo limitado de correspondencias publicadas](research/F41V_READING_FEASIBILITY_2026-10-22.md). El subconjunto implementado no produce una lectura completa y única; la identidad botánica sigue sin establecerse y no se utiliza como clave conocida.

**Anclas contrastadas con imágenes:** [tres lugares verificados en Yale y concordancias de nueve candidatos](research/DECIPHERMENT_ANCHOR_REVIEW_2026-10-22.md). Se distingue el rótulo lateral de f2r del inicio de párrafo usado por Bax; ninguna equivalencia se admite todavía como texto plano conocido.

**Vía de desciframiento iniciada:** [diagnóstico P0 ejecutado y primeras posibles anclas textuales](research/DECIPHERMENT_START_2026-10-22.md). La ventaja del orden real persiste sin etiquetas en el modelo ensayado; no se ha recuperado texto plano ni establecido significados.

**Investigación profesional externa:** [ocho fuentes, conocimiento aplicable y límites de acceso](research/PROFESSIONAL_EXTERNAL_REVIEW_2026-10-22.md), con versiones fijadas de cuatro repositorios de autores. Se incorpora metodología; no se atribuye validación propia a sus conclusiones.

**Sensibilidad ejecutada:** [rejilla de 128 normalizaciones y comparación de EXP-601/607](research/READER_SENSITIVITY_DECISION_2026-10-22.md). El patrón inicial B/P0 y la ventaja del modelo frente a su control conservan el signo bajo los perfiles ensayados; son resultados exploratorios, sin interpretación semántica.

**Revisión intensiva posterior:** [reparaciones, pruebas y límites](research/INTENSIVE_REVIEW_2026-10-22.md): 474 scripts con rutas portables, auditor de 227 cabeceras y capa léxica sin pérdida probada sobre tres transcripciones. EXP-170 sigue bloqueado por inputs externos requeridos; EXP-031 y la parte latina de EXP-436 pasan una ejecución desde otro directorio.

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
- [`state/working_position.md`](state/working_position.md): síntesis histórica archivada; sus etiquetas VALID/RULED OUT y probabilidades no son adjudicaciones actuales. Consultar auditorías posteriores antes de reutilizarlas.
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

El repositorio no se declara completamente validado. El acuerdo de parsers v7 documentado arriba no equivale a conformidad completa IVTFF; quedan casos y adjudicaciones pendientes. Las carpetas históricas ya tienen identificadores inequívocos por ruta, pero faltan reconciliaciones de referencias y artefactos entre GitHub y la Biblioteca. La [guía de verificación CI](research/CI_VERIFICATION.md) explica por qué una consulta filtrada vacía no prueba fallo o ausencia de ejecuciones. Cada commit requiere evidencia propia. No se borran originales ni se consideran válidos resultados afectados por defectos conocidos.

Auditoría del 22-10-2026: [lectores históricos de Cicero, selección efectiva y límites](research/maintenance/2026-10-22-loader-audit/REPORT.md).
