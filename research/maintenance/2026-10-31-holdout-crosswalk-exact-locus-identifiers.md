# Holdout crosswalk: comparación de identificadores completos de locus

**Fecha:** 2026-10-31. **Tipo:** corrección operativa acotada, no EXP. **Base:** `master` `60ea23a42884fcd508cc0283f1ebd8e014c05c85` (PR #185 integrada). **Estado al redactar:** PROPUESTA; las pruebas y la CI de esta nueva rama aún no se han ejecutado/verificado. No certifica una traducción.

## Defecto y prueba adversarial

La PR #185 corrigió la omisión de paneles y de filas mediante la comparación de conjuntos de páginas y **cantidades** de cabeceras/registros entre dos lectores IVTFF. Queda una condición no cubierta: dos lectores pueden reconocer las mismas páginas, el mismo número de cabeceras y el mismo número de loci, pero discrepar en el identificador de un locus. Por ejemplo, sustituir en la salida del lector estricto `f67r1.2,@P0` por `f67r1.3,@P0` mantiene intactos el folio, la página, los recuentos y la asignación del holdout. El control de #185 lo aceptaría; la nueva regresión debe rechazarlo.

Es una **inyección sintética sobre el resultado de un lector**, no un error encontrado en ZL3b/IT2a. No se manipula el texto ni se consulta el contenido léxico de los folios reservados.

## Reparación y alcance

- `audit_ivtff_page_locus_ids.audit_text(..., include_locus_ids=True)`: inventario opcional ordenado de etiquetas completas de locus. Por defecto, el informe histórico no cambia.
- `audit_holdout_locus_coverage.inspect_source(..., include_locus_ids=True)`: inventario independiente, también optativo, preservando la salida histórica.
- `audit_holdout_page_crosswalk.crosswalk`: igualdad exacta de las etiquetas de locus de ambos lectores, además de la concordancia de páginas y recuentos ya implantada.
- `test_holdout_page_crosswalk.py`: regresión de sustitución de ID con páginas y recuentos constantes, y control de invariancia de informes por defecto.

Las listas se ordenan conservando multiplicidad; no se colapsan a un conjunto. No se modifica el esquema JSON congelado del crosswalk, los corpus, el manifiesto v2, la sal, las semillas, los resultados históricos, las afirmaciones comprometidas ni las particiones train/dev/test.

## Criterios de aceptación previos a la ejecución

1. Pasar `python -m unittest discover -s tests -p 'test_holdout_page_crosswalk.py' -v` y su versión `python -O`.
2. Pasar la CI completa del commit exacto de la PR; comprobar los pasos pertinentes en logs.
3. El crosswalk de las fuentes congeladas debe continuar siendo idéntico byte a byte a `research/maintenance/2026-10-25-holdout-page-crosswalk/results.json` (comparación `cmp` de CI), y su JSON/archivo SHA-256 deben existir en el artefacto publicado.
4. No integrar antes de verificar head, `master` concurrente y artefactos; tras integrar, verificar CI posterior.

**Unidad:** etiquetas estructurales IVTFF, no palabras ni significados. **Semilla:** no aplica, controles deterministas. **Limitaciones:** concordancia de dos lectores sobre etiquetas no certifica semántica IVTFF completa ni independencia de transcripciones; los folios test han tenido exposición histórica. No se ejecutan nuevas pruebas predictivas hasta resolver contradicciones pendientes.

**Contexto de partida verificado:** PR #185 integrada en `60ea23a42884fcd508cc0283f1ebd8e014c05c85`; CI head de #185 `41158352262` satisfactoria, con 7/7 regresiones de crosswalk en Python normal y optimizado y crosswalk SHA-256 `074f38352d1dbff8c1713cc68f150c132ddbdcce6aad20a883fd2ecaa5d08477`. CI push posterior `41159039523` seguía en curso en la última revisión antes de abrir esta rama. No convertir ese estado parcial en cierre.

**Pendientes independientes:** EXP-170 sin entradas históricas exactas, adjudicación IVTFF completa, conciliación de artefactos y límites del predictor a distancias de PR #7. Evaluación general: 2026-11-22, sin garantía de descifrado.
