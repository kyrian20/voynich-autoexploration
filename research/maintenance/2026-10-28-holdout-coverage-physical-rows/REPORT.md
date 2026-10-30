# Auditoría acotada — límites físicos en el censo independiente de holdout

**Fecha:** 2026-10-28. **Tipo:** corrección de integridad de metadatos, no experimento científico. **Estado:** pendiente de CI y revisión de PR hasta que se verifiquen los runs.

## Defecto y reproducción mínima

El generador del manifiesto v2 `scripts/prepare_prospective_leaf_holdout_v2.py` ya usa `checked_physical_lines` (PR #121), pero `scripts/audit_holdout_locus_coverage.py::inspect_source` todavía usaba `str.splitlines()`. Esta última función interpretaba VT, FF, U+001C–U+001E, U+0085, U+2028 y U+2029 como separadores de filas, aunque no son CR/LF/CRLF físicos del archivo IVTFF.

Entrada sintética adversarial: cabecera válida `<f1r>`, locus válido, después una **misma fila física** con `# comment` seguido de U+2028 y `<f2r>`, y finalmente `<f2r.1,@P0>`. Antes de la reparación, `splitlines()` podía convertir `<f2r>` en una cabecera independiente y contar una hoja inexistente. No se atribuye esta secuencia a los corpus reales.

## Reparación

- `scripts/audit_holdout_locus_coverage.py`: reutiliza el iterador estricto de filas físicas, tanto como script directo como importación de paquete; rechaza separadores no físicos con `ValueError`, sin normalizarlos.
- `tests/test_holdout_locus_coverage.py`: regresión con los ocho separadores reales y control positivo para CR, LF y CRLF.
- No se modifica el generador v1 histórico, el manifiesto v2 congelado, los corpus, la asignación de folios ni ningún resultado de EXP.
- No se utiliza texto reservado para seleccionar reglas; las pruebas son sintéticas. Sin aleatoriedad ni semilla.

## Verificación y alcance

**Comandos de verificación previstos en la CI existente:**

```sh
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python scripts/audit_holdout_locus_coverage.py --out holdout-locus-coverage.json
python -m unittest discover -s tests -p 'test_holdout_page_crosswalk.py' -v
python scripts/audit_holdout_page_crosswalk.py --out holdout-page-crosswalk.json
cmp research/maintenance/2026-10-25-holdout-page-crosswalk/results.json holdout-page-crosswalk.json
```

La ejecución sobre fuentes reales está condicionada a los hashes exactos del manifiesto y a la comparación de la instantánea del crosswalk. Hasta verificar la CI no se afirma que el resultado sea idéntico ni que toda la conformidad IVTFF esté resuelta.

## Bloqueos no modificados

La adjudicación integral IVTFF, los identificadores históricos ambiguos, las entradas exactas de EXP-170 y la conciliación de artefactos permanecen abiertos. Esta reparación cierra únicamente la aceptación de separadores no físicos en el lector independiente de cobertura. No aporta semántica, hipótesis confirmada ni traducción.
