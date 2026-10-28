# Integridad de evidencia documental en exclusiones de corpus — 2026-10-28

**Tipo:** reparación de procedencia, no EXP nuevo ni descifrado. **Base:** `master` `c6cdc073e01d9f83b3db2316605e62dd7658b4c1`. **Estado de apertura:** propuesta en rama; CI y revisión pendientes.

## Defecto comprobable en el contrato del auditor

El auditor `scripts/audit_corpus_identity_overlay.py::audit` cotejaba los fragmentos de `header_title`, `header_language` y `evidence` con el texto del corpus, pero no exigía conservar **las pruebas documentales que ya constaban** en `research/CORPUS_IDENTITY_REVIEW.json`. Por ejemplo, sustituir las doce citas archivadas para `latin/vulgate.txt` por una sola cadena real, `Language: English`, mantenía el hash, el tamaño, la clasificación y la existencia de evidencia textual, y podía superar el control. Asimismo, `source_commit` no se cotejaba con ninguna referencia independiente. Se trata de una puerta de integridad insuficiente; **no se ha observado manipulación de los registros reales**.

## Reparación y falsación

Se fijan en el código, de forma independiente del JSON examinado, el identificador de commit documental registrado (`b566b6fa461f3a4e6fd8bb3a1aaa6e71f035f190`) y las listas completas de títulos, idiomas de cabecera y citas ya adjudicadas para las seis exclusiones. `audit` rechaza cambios o supresiones, incluso si el nuevo fragmento también aparece en el corpus. Los controles existentes de presencia textual y SHA-256 siguen vigentes. Una adjudicación futura legítima requerirá revisión explícita y actualización coordinada del bloqueo y de sus regresiones; **no se afirma que ese commit sea el momento de creación del overlay ni que certifique las identidades históricas**.

`tests/test_corpus_identity_overlay.py` ahora construye seis corpus temporales con los fragmentos archivados y añade dos pruebas adversariales: cambio del commit de referencia y debilitamiento de las citas/cabecera de la Vulgata. No se accede a folios reservados ni se ejecutan simulaciones. Semilla no aplicable; entradas sintéticas deterministas. Se conserva la regresión del séptimo corpus no adjudicado. El consumidor histórico `tests/test_remaining_reference_loaders.py` también crea seis corpus sintéticos para validar el mismo auditor; sus fixtures se han alineado con las evidencias fijadas, sin modificar `scripts/audit_remaining_reference_loaders.py` ni el snapshot de lectores.

**Criterio de aceptación (previo a CI):** pasar las 14 pruebas del auditor (12 anteriores + 2 nuevas), las 11 del consumidor de lectores, rechazar las tres mutaciones adversariales nuevas, ejecutar el auditor contra los seis corpus reales y completar `Voynich Check` del SHA final de la PR. Tras fusionar, verificar un nuevo run `push` de `master` y sus artefactos. El workflow existente ya incluye pruebas y auditor, por lo que no se añade otro.

```sh
python -m unittest discover -s tests -p 'test_corpus_identity_overlay.py' -v
python scripts/audit_corpus_identity_overlay.py
python tests/test_remaining_reference_loaders.py
python scripts/audit_remaining_reference_loaders.py --check research/maintenance/2026-10-22-remaining-readers/results.json
python scripts/check_corpus_integrity.py
```

## Archivos y límites

Se cambian exclusivamente `scripts/audit_corpus_identity_overlay.py`, `tests/test_corpus_identity_overlay.py`, `tests/test_remaining_reference_loaders.py` y este informe. Los 14 corpus congelados, `research/CORPUS_INPUT_MANIFEST.json`, `research/CORPUS_IDENTITY_REVIEW.json`, scripts históricos, resultados negativos, semillas, manifiestos de holdout y `state/committed_claims.md` quedan intactos.

El bloqueo conserva **consistencia de evidencia registrada**, no determina de forma independiente idioma, autenticidad, licencia ni calidad de corpus. Las conclusiones históricas afectadas por inglés mal etiquetado o texto bilingüe siguen pendientes de adjudicación; EXP-170 continúa BLOCKED para reproducción exacta y la conformidad IVTFF no está cerrada. No se ha ejecutado experimento semántico ni producido traducción.

## Fallo inicial conservado y corrección de compatibilidad

La primera ejecución de PR, [run 40669578007](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40669578007), **falló** en `Reproducir cuatro lectores de referencia restantes`: 2 errores en 11 pruebas. Los dos fallos provenían de fixtures sintéticos antiguos de `RemainingReaderProvenanceTests`, que no incluían `source_commit` y usaban citas genéricas en lugar de las evidencias ahora fijadas. El propio auditor y sus 14 pruebas sí pasaron en el paso previo de esa ejecución. Se actualizaron los fixtures del consumidor; no se relajó el bloqueo de procedencia ni se tocaron los resultados históricos. La aceptación requiere una **nueva** CI completa en el SHA posterior, no reutilizar el run fallido.
