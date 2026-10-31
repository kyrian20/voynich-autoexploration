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

- En el checkpoint inicial quedaban 23 grupos por revisar. Las pasadas posteriores completan el triage semántico de los 34 IDs compartidos; esto no sustituye el cotejo binario de archivos ni la trazabilidad de cada resultado.
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


## Cierre del triage semántico de los 34 IDs compartidos — 2026-10-22

La revisión de los casos restantes añade estos seis IDs al registro de diferencias de tema/método:

| ID | Tema Biblioteca | Tema GitHub | Clasificación / acción segura |
|---|---|---|---|
| EXP-589 | Entropía de etiquetas / informe de entropía léxica | Posición inicial de `daiin` con nulo de permutación por línea | Preguntas distintas; no transferir resultados |
| EXP-594 | Sensibilidad a incertidumbre y multiplicidad | Marcadores explícitos de inicio de párrafo IVTFF (además existe una segunda carpeta GH-EXP-594 de inicio de párrafo) | No asumir identidad por número; revisar cada carpeta por separado |
| EXP-596 | Nulo de longitud exacta | Controles posicionales de `daiin` y auditoría pareada ZL3a/ZL3b en dos carpetas distintas | Preguntas distintas; mantener las dos rutas GH separadas |
| EXP-597 | Adyacencia de prefijos/sufijos | Contexto del token siguiente tras formas iniciales y, en otra carpeta, controles de frecuencia de `daiin` | Preguntas distintas; no fusionar carpetas ni resultados |
| EXP-622 | Control zodiacal del orden de palabras | Interacción de especificidad contextual ch/sh (contraste siguiente frente a anterior) | Preguntas distintas; no usar como replicación de orden de palabras |
| EXP-624 | Auditoría de metadatos y control posicional con artefactos separados | Nota de discrepancia de parser y gate de predicción Currier A/B | Preguntas distintas; no asociar por número |

Con estas seis incorporaciones y las 28 diferencias documentadas antes, **los 34 grupos con ID compartido han sido revisados semánticamente y los 34 tienen una discrepancia de pregunta, método o alcance**. Este resultado significa que el número EXP no es una clave de unión fiable entre Biblioteca y GitHub. No significa que todos los experimentos sean erróneos ni que se haya demostrado que sus archivos son distintos byte a byte.

**Pendiente por separado:** comparación SHA-256 de contenido para los pares candidatos; comprobar las asociaciones exactas entre scripts, JSON e informes; ejecutar las reproducciones que aún no se han ejecutado (en especial las dos pruebas piloto de orden de palabras LIB-EXP-623); y revisar los siete IDs de carpetas duplicadas internamente en GitHub. Ningún original se ha renombrado, fusionado, borrado o sobrescrito y no se ha asignado un ID nuevo.


## LIB-EXP-623 reproduction closure — 2026-10-22

The two Library word-order pilot scripts were executed in the isolated GitHub Actions workflow against the exact recorded source transcription blobs. Run: [39729111827](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39729111827); workflow commit `40e636cd7815f0b2de5d10d5ea6b7a47f1ad645d`. Both analysis steps and artifact upload succeeded.

- `research/reproduction/exp623_order_null.py`: endpoint-preserving interior shuffle, 10 folio-stratified splits × 39 nulls. Loci/tokens match pilot metadata (ZL3b 3,879/32,959; IT2a 3,881/33,380); mean deltas and split classifications match within floating-point rounding; all 10/10 splits in both transcriptions are above the null 95th percentile and maximum.
- `research/reproduction/exp623_shuffle_holdout.py`: all-token within-locus shuffle, 20 splits × 50 shuffles. Loci/tokens match (ZL3b 5,376/39,298; IT2a 5,207/37,945); categorical outcomes match exactly. Mean shuffled-minus-original loss differs from pilot by only about 10^-15 bits/token. Original sequence has lower loss in 3/20 ZL3b splits and 0/20 IT2a splits; random shuffles have lower loss in 76.9% and 98.8% of draws, respectively.
- The source blobs verified in the workflow are ZL3b `2a4533ab9bdfa85db9bad602d590978953055df1` and IT2a `4d6d3f2537b1f507a257529b49c94af7d6e03446`.
- Full comparison, interpretation limits, artifact ID and output hashes: [EXP623_REPRODUCTION_COMPARISON_2026-10-22.md](https://github.com/kyrian20/voynich-autoexploration/blob/master/research/reproduction/EXP623_REPRODUCTION_COMPARISON_2026-10-22.md). The Actions artifact is `exp623-reproduction-40e636cd7815f0b2de5d10d5ea6b7a47f1ad645d` (ID 12404740024).

This closes a limited numerical reproduction of these two Library pilot scripts, not exact byte identity of the scripts or the broader binary reconciliation. The two protocols use different null constructions and must remain separate; neither is a decipherment result. Historical Library files were not overwritten or merged. No new EXP ID was assigned.


## Adjudicación del holdout por hoja física de LIB-ORDER-2026-10-19-A/B — 28-10-2026

[Informe y auditor reproducible](maintenance/2026-10-28-lib-exp623-physical-leaf-leakage.md). Los dos scripts históricos de Biblioteca EXP-623 dividían por **identificador de cara** (fNNr/fNNv), no por **hoja física**; los hashes de los seis originales de Biblioteca están verificados. Bajo las semillas originales, la reconstrucción de metadatos encuentra **41–57 hojas compartidas** entre entrenamiento/prueba en A/ZL3b, **38–53** en A/IT2a, y **31–48** en B para ambas transcripciones (semilla 623: **44**). Se conserva el resultado histórico, pero las afirmaciones de evaluación sobre hojas físicas enteramente no vistas quedan **INVALID_FOR_CLAIM**. La auditoría no reproduce los scores de los pilotos ni demuestra cuánto infló el efecto; tampoco constituye una traducción. A y B usan diferentes filtros y controles (B reentrena también el nulo), de modo que no deben combinarse. El EXP-623 de GitHub sigue siendo un trabajo distinto sobre ch/sh.


## Cotejo binario de los scripts piloto LIB-ORDER — 2026-10-31

Se recuperaron de la Biblioteca los dos scripts originales (versión 1) y se contrastaron sus **bytes reales** con los blobs Git de las copias del repositorio. **Corrección de integridad del 01-11-2026:** la afirmación anterior de identidad binaria era falsa por **un byte** en cada par: las copias de GitHub carecen del salto de línea LF final (`0a`) presente en ambos originales de Biblioteca. El código previo al byte final es idéntico; los hashes de los archivos completos **no** coinciden.

| Piloto | Biblioteca: bytes / SHA-256 | GitHub: bytes / SHA-256 | Git blob SHA-1 (Biblioteca → GitHub) |
| --- | --- | --- | --- |
| LIB-ORDER-2026-10-19-B, `exp623_order_null.py` | 11.137 / `ea51e67e6f36b8c651231262cb22ebbb5ef9f98cd31c4673924e33d6a3627010` | 11.136 / `28925cddaa94a8a9236ad67f6f92ae83459561414cea8ba3d5d4febfac90e9c7` | `2264c534cb109d823842d3f8d585574cc8c7d607` → `8b6e250fc1c6eeee72822ba3f20892fcd7ce3110` |
| LIB-ORDER-2026-10-19-A, `exp623_shuffle_holdout.py` | 8.563 / `c4bb8e7fb44632b93979a26bb88c49264c3fb7c4c2d3685a59d72958f902b070` | 8.562 / `0be5b31be711e5f6e9b216f370d786a6a247120f4539f07719dc65e624e0c28b` | `91f301ea65fe634601e6ce704f6542d7c6eff362` → `59093cd0ff017af42c3fc8631690d3ce3919cfbf` |

Comprobación independiente: materialización de ambos originales desde Biblioteca, `sha256sum`, `wc -c`, `git hash-object`; contraste con los blob SHA-1 de GitHub y verificación de que eliminar el último byte `0a` de cada original reproduce **exactamente** el SHA-256 y Git blob SHA-1 de su copia. Regresión offline: `python -m unittest discover -s tests -p 'test_lib_exp623_terminal_lf_provenance.py' -v` (también `python -O`). No requiere descargar la Biblioteca en CI: fija ambos pares de hashes y comprueba la diferencia de LF sobre las copias versionadas. Esta prueba no certifica la ejecución histórica ni recupera los JSON originales.

La ausencia de LF final no cambia la semántica Python del script; **sí impide afirmar identidad binaria**. Se conservan los seis originales de Biblioteca, los scripts GitHub y los resultados archivados sin modificaciones.

La reproducción de GitHub Actions 39729111827 y `research/reproduction/EXP623_REPRODUCTION_COMPARISON_2026-10-22.md` registran que ambos scripts se ejecutaron y que los resultados reproducidos coinciden con los pilotos dentro del redondeo numérico descrito allí. Esta comprobación añade identidad binaria de los scripts; no convierte los dos nulos en el mismo protocolo ni demuestra que sus hipótesis sean equivalentes. Los JSON reproducidos permanecen en el artefacto de Actions y no se afirma aquí igualdad byte por byte de esos JSON con los originales de Biblioteca.

La nota histórica del 22-10 sobre scripts aún no ejecutados se conserva como registro del estado de esa fecha; las secciones posteriores documentan la reproducción. Este cotejo cierra la identidad de código y la reproducción de estos dos pilotos únicamente. La adjudicación de contaminación por hoja física del 28-10 sigue vigente: las métricas de holdout de los pilotos no sustentan generalización a hojas enteramente no vistas. `GH-EXP-623` sigue siendo el análisis distinto de interacción ch/sh. No se renumeró, fusionó ni sobrescribió ningún artefacto y no se asignó un nuevo EXP ID.
