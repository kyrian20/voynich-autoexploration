# Guard de procedencia de cuatro lectores históricos — 2026-10-27

**Estado al abrir PR:** reparación propuesta, verificación de CI pendiente. **No es un EXP nuevo ni una reproducción histórica completa.**

## Defecto concreto

En `scripts/audit_remaining_reference_loaders.py::compute`, el archivo `research/CORPUS_IDENTITY_REVIEW.json` se leía con `json.loads` permisivo y se indexaba mediante `{r['path']: r ...}`. Una entrada duplicada para el mismo corpus sobrescribía silenciosamente la anterior; una clave JSON duplicada también podía pasar inadvertida. Además, este consumidor cotejaba los SHA-256 de solo dos archivos contra el propio overlay, sin verificar directamente que la adjudicación coincidiera con el manifiesto congelado ni con las decisiones históricas. Una copia de bytes correcta no valida por sí sola el idioma o la obra asignados.

Esto es una vulnerabilidad de **aceptación de metadatos de procedencia** en la ejecución directa de este auditor. No prueba que los archivos reales hayan sido alterados. Los controles separados de CI ya auditan el overlay; esta corrección evita que el consumidor dependa de su orden de ejecución.

## Reparación

Añadir `load_verified_reference_metadata(root)` al mismo auditor y llamarlo **antes** de extraer los lectores históricos. Ambos JSON se cargan con rechazo de claves duplicadas (`unique_keys`). Se reutiliza `scripts/audit_corpus_identity_overlay.py::audit`, que contrasta las seis exclusiones históricas, rutas únicas, manifiesto congelado, hashes y tamaños, bytes, evidencias y adjudicaciones de obra/idioma. Ante cualquier discrepancia se detiene sin ejecutar lectores ni producir un recibo de reproducción. No se introducen nuevos criterios de clasificación de idiomas ni se modifican decisiones congeladas.

## Regresiones propuestas

Cinco casos sintéticos en `tests/test_remaining_reference_loaders.py`: overlay íntegro, ruta duplicada con idioma contradictorio, sustitución plausible del tipo de error de Vulgata, hash alterado en manifiesto y miembros JSON duplicados. Los corpus sintéticos se generan en directorios temporales; ninguna entrada real se modifica. Sin semillas aleatorias.

El workflow canónico ya ejecuta `python tests/test_remaining_reference_loaders.py` y `python scripts/audit_remaining_reference_loaders.py --check research/maintenance/2026-10-22-remaining-readers/results.json`. También ejecuta los auditores de corpus por separado. Debe comprobarse el resultado CI del **SHA final de la PR** y posteriormente el de `master`. El snapshot de 2026-10-22 se conserva exactamente.

## Procedencia, límites y autoauditoría

Base `master` comprobada antes de crear rama: `6827ba6f123ba7fa8dfe9e9f525fdec9382b1a0e`. Corpus implicados: `data/reference_corpora/latin/cicero_de_officiis_latin.txt` (SHA-256 archivado `3a33a076d3dda42673ec7ab0331ae7e58fc150e7e92751c0adf6d1db7297b670`) y `data/reference_corpora/latin/vulgate.txt` (SHA-256 archivado `d63b1b81824e259b1cf92ba8a6e5cbbf783e2a83214cf2c3db2ecd1459165bfe`). Los hashes son **del registro previo**, no recálculos realizados en esta sesión. Fuente de resultados congelados: `research/maintenance/2026-10-22-remaining-readers/results.json`.

**Target-awareness:** ninguna selección nueva de palabras o métrica Voynich. **Feature-destroying implementation:** se mantienen intactos los lectores AST, filtros y el defecto histórico de coordenadas EXP-001; la corrección solo añade una puerta previa. **Extrapolación:** protege un consumidor y sus dos entradas efectivas, no toda la procedencia histórica. **Resultado negativo:** los ataques sintéticos rechazados no demuestran contaminación real. **Control:** overlay y manifiesto sintéticos coherentes deben pasar; cada alteración declarada debe fallar. Las pruebas y CI son pendientes hasta ejecución verificable.

La selección histórica de cuatro lectores no certifica qué bytes usaron las ejecuciones originales, ni convierte Cicero bilingüe o Douay-Rheims inglesa en controles latinos monolingües. No hay adjudicación IVTFF completa, inferencia semántica ni traducción. No tocar `state/committed_claims.md`, resultados negativos, particiones reservadas, corpus, scripts experimentales ni numeración EXP.

## Criterio de cierre

Confirmar cinco regresiones nuevas, las seis anteriores, comparación completa del snapshot histórico, CI en PR y CI de `master` posteriores a la fusión; documentar enlaces y hashes reales en la conversación de la PR. Si alguna falla, dejar sin fusionar y conservar el fallo.
