# Registro de colisiones y alias de artefactos

Fecha de auditoría: 20-10-2026  
Estado: inventario parcial; no equivale a una auditoría completa de los más de 2.000 paths de GitHub ni de todos los ficheros de la Biblioteca.

## Reglas

- Los nombres históricos se conservan por trazabilidad.
- No fusionar artefactos por compartir EXP ID o similitud de nombre.
- Los alias técnicos se añaden en este registro; el renombrado físico solo se hará después de localizar referencias y comparar hashes.
- Un resultado se marca inválido solo para las afirmaciones afectadas por su defecto; no se borra.

## Conflictos confirmados

| Nombre histórico | Ubicación | Contenido/alcance | Acción segura |
|---|---|---|---|
| EXP-623 | GitHub: informe de interacción ch/sh | Sensibilidad de una interacción contextual entre transcripciones ZL3b/IT2a; interacción no significativa, cambia de signo | Conservar como GH-EXP-623; no usar para afirmaciones de orden de palabras |
| EXP-623 control de orden, variante A | Biblioteca: Informe_Voynich_exp623_Control_orden_palabras_2026-10-19.md | Bigramas en folios reservados, control que baraja todas las palabras dentro del locus; el orden real no supera al control en la métrica reportada | Alias de inventario LIB-ORDER-2026-10-19-A; no renumerar hasta comparar el script y el JSON |
| EXP-623 control de orden, variante B | Biblioteca: Informe_Voynich_exp623_control_orden_2026-10-19.md | Modelo de bigramas en folios reservados; control que permuta palabras interiores y mantiene extremos; informa ventaja predictiva frente a ese nulo, con limitaciones exploratorias | Alias de inventario LIB-ORDER-2026-10-19-B; no fusionar con A ni con GitHub |
| EXP-590 | GitHub: scripts/exp590_daiin_position.py y resultados JSON/MD del 20-10-2026 | El script original usaba $Q para clase Currier; el script se corrigió para usar $L. Resultados antiguos por clase siguen pendientes de regeneración/verificación | Alias GH-EXP-590-OLD-Q; conservar el output histórico y marcar las tablas por clase como INVALID_FOR_CLAIM hasta repetición |
| EXP-593 | GitHub: scripts/exp593_daiin_variants.py y JSON/MD | Se corrigió extracción de clase a $L; el registro advierte que hay conflictos históricos de numeración y que debe verificarse la ejecución CI | Mantener ID con advertencia; no reasignar hasta revisar el índice histórico completo |

## Colisiones de numeración entre GitHub y Biblioteca

Los IDs `EXP-NNN` **no son globalmente únicos entre las dos superficies**. La Biblioteca contiene una serie histórica centrada en análisis zodiacales (aprox. EXP-590–624), mientras que GitHub reutiliza parte de esa numeración para otros experimentos. Hasta que se haga el cotejo completo, referirse a cada elemento con prefijo `GH-` o `LIB-` y un alias descriptivo. No renombrar ni borrar los originales.

| ID | GitHub (GH) | Biblioteca (LIB) | Estado |
|---|---|---|---|
| EXP-590 | Posición de `daiin` y metadatos Currier | Auditoría de modelos externos | Colisión confirmada |
| EXP-593 | Variantes/posición de `daiin` | Denominadores zodiacales y reconciliación zodiacal | Colisión confirmada |
| EXP-600 | Conformidad del parser IVTFF; concordancia de transcripciones | Comparación zodiacal ZL3b–IT2a | Colisión confirmada |
| EXP-601 | Confirmación agrupada por folio; sensibilidad pareada | Comparación de 299 etiquetas RF1b/ZL3b/IT2a | Colisión confirmada |
| EXP-602 | Predicción held-out; auditoría independiente de parser | Heterogeneidad de inicios por signo | Colisión confirmada |
| EXP-622 | Interacción contextual ch/sh | Control de orden zodiacal | Colisión confirmada |
| EXP-623 | Replicación ch/sh en IT2a | Dos análisis distintos de orden de palabras (extremos de locus / permutación de palabras interiores) | Colisión confirmada |
| EXP-624 | Gate de discrepancia de parser y bloqueo de predicción A/B | Auditoría de metadatos y control posicional, con scripts/resultados separados | Colisión confirmada |

Los IDs intermedios de la serie `LIB-EXP-591` a `LIB-EXP-621` también deben tratarse como posibles colisiones de namespace hasta cotejar sus títulos con los experimentos GitHub correspondientes. La tabla anterior enumera los conflictos que ya se han confirmado por título/alcance, no pretende ser una reconciliación completa de toda la serie.

## Colisiones de ID dentro de carpetas GitHub

El inventario de árbol identificó estas colisiones adicionales. Los alias de abajo son **alias de registro solamente**; las rutas originales no se han renombrado y no deben fusionarse.

| ID histórico | Alias técnico A — ruta original | Alias técnico B — ruta original |
|---|---|---|
| EXP-177 | `GH-EXP-177-POSITION-SENSITIVE-CIPHER` — `experiments/exp_177_position_sensitive_cipher/` | `GH-EXP-177-VERIFY` — `experiments/exp_177_verify/` |
| EXP-594 | `GH-EXP-594-EXPLICIT-PARAGRAPH-MARKERS` — `experiments/exp_594_daiin_explicit_paragraph_markers/` | `GH-EXP-594-PARAGRAPH-START` — `experiments/exp_594_daiin_paragraph_start/` |
| EXP-596 | `GH-EXP-596-DAIIN-POSITION-CONTROLS` — `experiments/exp_596_daiin_position_controls/` | `GH-EXP-596-ZL3A-ZL3B-LINE-AUDIT` — `experiments/exp_596_zl3a_zl3b_line_level_audit/` |
| EXP-597 | `GH-EXP-597-DAIIN-FREQUENCY-CONTROLS` — `experiments/exp_597_daiin_frequency_control_words/` | `GH-EXP-597-INITIAL-NEXT-TOKEN-CONTEXT` — `experiments/exp_597_initial_form_next_token_context/` |
| EXP-600 | `GH-EXP-600-IVTFF-PARSER-CONFORMANCE` — `experiments/exp_600_ivtff_parser_conformance/` | `GH-EXP-600-TRANSCRIPTION-CONCORDANCE` — `experiments/exp_600_transcription_concordance/` |
| EXP-601 | `GH-EXP-601-FOLIO-CLUSTERED-CONFIRMATION` — `experiments/exp_601_folio_clustered_confirmation/` | `GH-EXP-601-PAIRED-SENSITIVITY` — `experiments/exp_601_primary_statistic_paired_sensitivity/` |
| EXP-602 | `GH-EXP-602-HELDOUT-PREDICTIVE-TEST` — `experiments/exp_602_heldout_predictive_test/` | `GH-EXP-602-INDEPENDENT-PARSER-AUDIT` — `experiments/exp_602_independent_ivtff_parser_audit/` |

La colisión EXP-623 con los dos informes de orden de palabras de la Biblioteca se documenta en la tabla anterior de este registro; no se añade una tercera ruta física ni se renumera ningún original.

## Parser y corpus

- La auditoría de protocolo v1 registró 1.466 desacuerdos de listas de tokens para ZL3b y 1.472 para ZL3a. Los recuentos posteriores fueron 792/805 (v2), 36/37 (v3/v4) y 3/3 (v5). El protocolo v7 informa **cero desacuerdos de campos o listas de tokens** para ZL3b (5.385 registros) y ZL3a (5.389 registros), tras fijar el tratamiento de comentarios, alternativas embebidas, anotaciones internas y alternativas primarias vacías. Todos los JSON de versiones se conservan por separado; v1 está archivado en `experiments/exp_602_independent_ivtff_parser_audit/archive/results_pre_terminator_fix_2026-10-20.json` y v6 y v7 están preservados en `experiments/exp_602_independent_ivtff_parser_audit/results_v6.json` y `experiments/exp_602_independent_ivtff_parser_audit/results_v7.json` (versión actual). Esto acredita acuerdo entre las dos implementaciones bajo la política actual, no certificación completa de IVTFF 2.0.2.
- Los conteos anteriores deben conservarse como evidencia histórica de discrepancia, no como una medida de que un parser concreto sea correcto.
- ZL3a, ZL3b e IT2a son transcripciones alternativas del mismo manuscrito y no deben contarse como réplicas independientes.

## Inventario estructural actualizado

La auditoría de árbol del 20-10-2026 cuenta 2.085 rutas, 624 carpetas `experiments/exp_NNN_*`, 617 IDs únicos, siete grupos de colisión de IDs de carpeta y 31 workflows. El informe [repository inventory audit](repository_inventory_audit_2026-10-20.md) detalla los grupos y evita etiquetar automáticamente como defectuosas las carpetas históricas sin script o salida convencional.

## Próxima auditoría de colisiones

1. Enumerar todos los archivos cuyo nombre contenga EXP, exp, fase, vNNN o checksum en GitHub y Biblioteca.
2. Extraer el ID del contenido, no solo del nombre.
3. Calcular SHA-256 de cada script, JSON, informe y fuente.
4. Agrupar coincidencias exactas y detectar pares con mismo ID pero distinta pregunta, script o resultado.
5. Resolver cada grupo con un alias estable, una relación de sustitución y referencias cruzadas.
6. No borrar ni sobrescribir artefactos históricos durante el proceso.


## Actualización de inventario top-level — 2026-10-22

La auditoría recursiva de GitHub confirma las colisiones de carpeta EXP-177, EXP-594, EXP-596, EXP-597, EXP-600, EXP-601 y EXP-602. La lista de pares de carpetas y las limitaciones del método están en [stabilization_audit_2026-10-22.md](stabilization_audit_2026-10-22.md). No se renombró ni eliminó ningún artefacto. Esta auditoría solo recorrió GitHub; la Biblioteca no está completamente reconciliada y sus IDs no deben asumirse globalmente únicos.


## Cross-surface evidence check — 2026-10-22

A direct read of the two Library reports confirms that the EXP-623 label masks two different order-model analyses with different null constructions and different reported outcomes:

- `LIB-ORDER-2026-10-19-A` — `Informe_Voynich_exp623_Control_orden_palabras_2026-10-19.md`: permutes all words within each locus; its own table reports that the real order loses to the permuted control (17/20 ZL3b and 20/20 IT2a partitions favor the permutation).
- `LIB-ORDER-2026-10-19-B` — `Informe_Voynich_exp623_control_orden_2026-10-19.md`: permutes only interior words while preserving the first and last word; its own table reports a positive real-order advantage under that different null.
- `GH-EXP-623` is instead the IT2a ch/sh context-specificity interaction test. It is neither Library order experiment. Do not compare the numeric outputs as if they were replications of one hypothesis, and do not copy either Library result into the GitHub EXP-623 slot.
- The two Library reports alone are insufficient to reproduce either result. The associated scripts and JSON outputs must be paired to their exact report, checked for corpus/parser hashes, and rerun before either is marked reproduced. This check did not calculate content hashes, modify Library files, or rename anything.

This remains a partial cross-surface check. The Library listing for `/Investigación Voynich/` is paginated and the returned first page is not a complete inventory; full reconciliation still requires paging every item and comparing materialized content hashes with GitHub blobs.


## Scoped hash and cross-surface identity checkpoint — 2026-10-22

Raw Library bytes for the priority set were materialized and SHA-256 hashed. Values and sizes are in [library_artifact_sha256_manifest_2026-10-22.md](library_artifact_sha256_manifest_2026-10-22.md). This is a scoped content manifest, not a full pairwise hash comparison with GitHub.

Additional same-number/different-question cases are now confirmed by directly reading both sides:

- `LIB-EXP-590-EXTERNAL-MODELS` — `Voynich_Informe_exp590_Auditoria_Modelos_Externos_2026-10-18.md` is an audit of external models. GitHub `experiments/exp_590_daiin_section_stratification/` instead tests `daiin` initial-position enrichment across coarse folio-number ranges. These are different research questions and must not be treated as matching EXP-590 artifacts.
- `LIB-EXP-593-ZODIAC-DENOMINATORS` — `Voynich_Informe_exp593_Denominadores_Zodiacales_2026-10-18.md` and its Library JSON/script concern zodiac denominators/reconciliation. GitHub `experiments/exp_593_daiin_line_metadata_contrast/` instead compares initial `daiin` across IVTFF locator categories. Separately, GitHub's dated `research/experiments/2026-10-22-exp593-corrected-L-metadata.*` is a corrected-`L)-metadata analysis of `daiin) variants, also not the Library zodiac report.
- These are alias/ID namespace collisions, not proof that any one artifact is false. Preserve all originals and use descriptive stable aliases in cross-surface records.

The Library listing has now been fully paged (501 items across six pages, no listing warnings). The remaining gap is not listing completeness but content-level mapping: verify exact script/JSON/report relationships, compare candidate GitHub and Library bytes, and trace each result to corpus/parser hashes. No original was edited, no EXP folder was renamed, and no new ID was allocated.


## EXP-623 method-pairing clarification — 2026-10-22

The scoped manifest now records a content-level method association for the two Library reports:
- `LIB-ORDER-2026-10-19-A` pairs by method with `exp623_resultados_2026-10-19.json` and `exp623_shuffle_holdout.py` (all-token within-locus shuffle; 20 splits × 50 shuffles).
- `LIB-ORDER-2026-10-19-B` pairs by method with `exp623_order_null_summary.json` and `exp623_order_null.py` (interior-only shuffle preserving endpoints; 10 splits × 39 nulls).

This resolves the intended report/JSON/script mapping at the protocol level, but **does not verify that either Python script generated the recorded pilot output**: both reports describe exploratory JavaScript pilot results, and their Python implementations were not run in GitHub Actions. Reproduction requires executing the exact scripts against the recorded transcription versions and comparing outputs. Keep both analyses exploratory and separate from GH-EXP-623.


## Priority cross-surface EXP namespace triage — 2026-10-22

A fresh inventory compared all 501 Library entries with the current 2,122-entry GitHub tree. **34 EXP-number groups occur on both surfaces.** This is a candidate set for semantic/provenance review, not 34 proven byte-level duplicates. The Library listing is complete; content-level pairing is not.

### Additional question-level mismatches confirmed from Library titles and GitHub experiment protocols

| ID | Library artifact topic | GitHub experiment topic | Status / safe action |
|---|---|---|---|
| EXP-591 | Sensitivity to line length | Exact IVTFF body-locus subtype stratification | Different question; keep separate |
| EXP-592 | Zodiac-label replication | Leave-one-folio-out influence audit for `daiin` | Different question; keep separate |
| EXP-595 | Re-grouping signs | Replication of explicit paragraph-marker findings in ZL3a | Different question; keep separate |
| EXP-598 | Inter-transcriber audit (`Lz`) | Two-token successor context after line-initial forms | Different question; keep separate |
| EXP-599 | Zodiac beginnings audit | Marginal successor distributions at offsets +1/+2 | Different question; keep separate |
| EXP-600 | Zodiac comparison ZL3b/IT2a | GitHub has two separate IDs under this number: IVTFF parser conformance and transcription concordance | Namespace collision already present inside GitHub; do not assign Library files by number |
| EXP-601 | Comparison of 299 RF1b/ZL3b/IT2a labels | Folio-clustered confirmation and paired positional-statistic sensitivity | Different question; keep separate |
| EXP-602 | Sign-based positional heterogeneity | Held-out predictive test and independent IVTFF parser audit | Different question; keep separate |

Together with the previously confirmed EXP-590, EXP-593 and EXP-623 cross-surface mismatches, these give **11 question-level mismatches identified so far**. For these cases, shared numeric labels must not be treated as identity. This does not mean any report is false; it means the number alone is not a reliable join key.

### Remaining triage

- The full overlap set contains 34 IDs; 23 other overlapping groups still need title/protocol review before classification.
- Seven duplicated GitHub experiment-folder IDs remain historical collisions: 177, 594, 596, 597, 600, 601 and 602.
- The selected SHA-256 manifest covers ten Library files only. Full file-by-file content hashing and GitHub counterpart pairing remains outstanding.
- No file has been renamed, merged, deleted, or overwritten. No new EXP ID has been allocated.


## Segunda pasada de triage semántico — 2026-10-22

Se revisaron títulos de informes de la Biblioteca y los protocolos/resultados de GitHub para los IDs restantes 603–613 y 616–621. La comparación es semántica por pregunta y método; **no** demuestra igualdad ni falsedad de los datos. Los IDs que no aparecen en esta tabla no se dan por reconciliados.

| ID compartido | Tema Biblioteca | Tema GitHub | Clasificación / acción |
|---|---|---|---|
| EXP-603 | Transiciones de inicios entre etiquetas | Predicción estratificada held-out de daiin usando clase Currier y longitud | Preguntas distintas; mantener alias separados |
| EXP-604 | Tendencia posicional de inicios | Replicación de daiin en IT2a | Preguntas/diseños distintos; mantener separados |
| EXP-605 | Longitud de párrafos Herbal frente a Recetas | Auditoría de secuencia y huecos de foliación en cabeceras | Preguntas distintas; no cruzar resultados |
| EXP-606 | Control por folio | Auditoría léxica en límites alrededor de huecos de foliación | Preguntas distintas; mantener separados |
| EXP-607 | Control de sección Currier B | Predicción del siguiente token en folios reservados | Preguntas distintas; mantener separados |
| EXP-608 | Auditoría del parser | Auditoría descriptiva del carácter posterior a ch/sh | Preguntas distintas; mantener separados |
| EXP-609 | Auditoría de estructura | Prueba pareada por folio de vocal tras ch/sh | Preguntas distintas; mantener separados |
| EXP-610 | Robustez por cara | Auditoría ch/sh estratificada por longitud de palabra | Preguntas distintas; mantener separados |
| EXP-611 | Longitud de líneas | Emparejamiento exacto por longitud y posición de ch/sh | Preguntas distintas; mantener separados |
| EXP-612 | Diversidad de vocabulario | Estratificación descriptiva ch/sh por etiquetas IVTFF | Preguntas distintas; mantener separados |
| EXP-613 | Adyacencia | Sensibilidad inferencial corregida ch/sh (bloque 613–615) | Preguntas distintas; mantener separados |
| EXP-616 | Reutilización de bigramas | Sensibilidad por bloques de folios reservados para ch/sh | Preguntas distintas; mantener separados |
| EXP-617 | Bigramas entre caras | Sensibilidad de celdas emparejadas ch/sh con soporte alto | Preguntas distintas; mantener separados |
| EXP-618 | Validación de caras reservadas | Sensibilidad de tipos léxicos frente a frecuencias de tokens | Preguntas distintas; mantener separados |
| EXP-619 | Sensibilidad al tamaño de muestra | Control de contexto adyacente anterior para contraste ch/sh | Preguntas distintas; mantener separados |
| EXP-620 | Predicción de bigramas / validación predictiva | Auditoría del parser IVTFF | Preguntas distintas; mantener separados |
| EXP-621 | Repetición de particiones | Informe provisional de decisión sobre contraste ch/sh | Preguntas distintas; mantener separados |

### Resultado de esta pasada y límites

- Los 17 números de la tabla son **mismatches semánticos de alta confianza por título y protocolo**, no colisiones de bytes ni veredictos sobre validez científica.
- Para EXP-613, la ruta de GitHub agrupa explícitamente los análisis 613–615 en un solo directorio; no se debe inventar una correspondencia uno-a-uno con cada archivo de Biblioteca.
- GitHub EXP-620 no contiene un result.md en la ruta esperada; su árbol muestra partial_audit.md. Esto se registra como diferencia estructural y no como fallo de resultado sin revisar el workflow.
- Los experimentos GitHub 608–621 forman una secuencia relacionada sobre el contexto de ch/sh, pero los tests de sensibilidad no equivalen a réplicas independientes. La síntesis de EXP-621 declara expresamente pendientes el holdout por sección, la revisión completa de multiplicidad y la auditoría independiente del parser.
- La suma acumulada de mismatches semánticos identificados en el registro pasa de 11 a 28. La revisión de los restantes solapamientos, las comparaciones de hashes de contenido y la trazabilidad exacta script→JSON→informe siguen pendientes.
- No se han renombrado, fusionado, borrado ni sobrescrito archivos históricos; no se ha asignado ningún EXP ID nuevo.
