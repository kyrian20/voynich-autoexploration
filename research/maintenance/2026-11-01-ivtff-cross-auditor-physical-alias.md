# IVTFF — identidad física de folio en dos auditores pendientes

**Fecha:** 2026-11-01. **Base comprobada antes de abrir la rama:** \`master\` \`fe06a9d8c309c3ca54a88bf4c2b702fd8fcb132a\`. **Clase:** reparación acotada de integridad de identificadores, no experimento nuevo. **Estado:** pendiente de verificar CI exacta de la PR y, si se integra, del nuevo \`master\`.

## Defecto concreto y falsación

Tras las correcciones de duplicados en otros auditores (#210, #211 y #214), quedaban dos comparaciones por **cadena literal**:

1. \`scripts/audit_ivtff_metadata_strict.py::validate\` indexaba las etiquetas Currier por \`page\` literal. Por tanto, \`<f1r> <! $L=A>\` seguido de \`<f01r> <! $L=B>\` no activaba su guardia de contradicción, aunque ambas cabeceras identifican la misma página física. La misma omisión existía en paneles como \`f86v4/f086v4\`.
2. \`scripts/audit_ivtff_page_locus_ids.py::audit_text\` construía la clave de duplicado de locus con la página literal. \`<f1r.1,@P0>\` y \`<f01r.01,@P0>\` no se contabilizaban como duplicados de locus aunque coincidieran en folio físico, línea numérica, localizador y transcriptor.

**Criterio previo a CI:** los dos casos adversariales deben rechazarse o diagnosticarse explícitamente, mientras que \`f86v4\` y \`f86v5\`, y dos localizadores diferentes, deben seguir siendo distintos. La prueba de contradicción usa \`$L\`, nunca \`$Q\`. La prueba de locus mantiene por separado el aviso existente de discrepancia de grafía de página.

## Corrección implementada

- El auditor estricto Currier compara una tupla \`(número entero, lado, panel)\` para folios numéricos y una clave propia para \`fRos\`. Rechaza cifras no ASCII en la identidad física; preserva las cadenas originales en los errores. El censo de folios con \`$L\` pasa a contar identidades físicas.
- El auditor de loci reutiliza su función ya existente \`physical_page_identity\` al construir la clave de duplicado. No se cambia la extracción, los identificadores originales, el alcance de \`page_mismatch\` ni los umbrales de línea.
- Las regresiones prueban conflicto A/B bajo alias, alias consistente, paneles distintos, cifras Unicode, duplicados de locus con doble cero inicial y no duplicados con otro código de localizador.

Las pruebas adversariales son **sintéticas**; no demuestran que los corpus congelados contengan tales alias. El auditor de cabeceras únicas ya rechaza páginas repetidas: esta reparación cierra dos diagnósticos independientes que antes podían ser engañosamente negativos. No se afirma que se haya levantado una barrera científica nueva ni que exista traducción.

## Comandos y evidencia pendiente

Desde la raíz, con Python 3.12:

\`\`\`sh
python tests/test_ivtff_metadata_strict.py
python tests/test_ivtff_page_locus_ids.py
python scripts/audit_ivtff_metadata_strict.py
python scripts/audit_ivtff_page_locus_ids.py
python scripts/check_corpus_integrity.py
python scripts/audit_repository_operations.py
\`\`\`

La CI canónica \`.github/workflows/voynich-check.yml\` ya ejecuta ambos archivos de regresión y ambos auditores. Verificar estado, pasos y artefactos para el SHA exacto de PR; no considerar aprobado este cambio por el éxito de un run previo. Si se integra, volver a comprobar el SHA y el run de \`master\`.

## Conservación, bloqueos y siguiente paso

Se mantienen sin modificación las transcripciones ZL3b/ZL3a/IT2a, corpus originales, scripts y resultados históricos, semillas, hashes congelados, particiones de entrenamiento/folios reservados, resultados negativos y \`state/committed_claims.md\`. Sin parámetros estocásticos ni asignación de EXP. Esta reparación no adjudica la conformidad IVTFF completa (alternativas, ligaduras, separadores, códigos extendidos); EXP-170 continúa **BLOCKED** para reproducción histórica exacta por ausencia de recibos que vinculen sus entradas externas con la ejecución original. Siguen abiertas la conciliación global de artefactos y la revisión científica de las PR #7/#138.

**Siguiente paso prioritario:** cotejar recibos históricos originales de EXP-170 o, si no existen, conservar el bloqueo sin sustituir entradas por reconstrucciones modernas. Evaluación general: 2026-11-22, sin promesa de descifrado.
