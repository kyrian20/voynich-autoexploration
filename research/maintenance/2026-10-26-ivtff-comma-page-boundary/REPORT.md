# IVTFF: cabecera de folio dañada por coma — 26-10-2026

**Tipo:** reparación de integridad de la auditoría estructural; no se crea EXP ni se formula hipótesis lingüística.
**Base exacta:** `master` `ac63ceca9472ddf4f9227a8e8db48a43084faed5`.
**Archivos de implementación:** `scripts/audit_ivtff_page_locus_ids.py`, `tests/test_ivtff_page_locus_ids.py`.

## Defecto y alcance

El auditor distinguía cabeceras de página por ausencia de coma en el identificador. Una cabecera física dañada como `<f2r,> <! $L=B>` caía por ello en la rama de **registro malformado**, sin invalidar `active_page`. Tras una cabecera válida `<f1r>`, el siguiente registro `<f1r.2,@P0>` podía aparecer sin discrepancia de página pese a existir una cabecera dañada intermedia. El problema afecta a la **detección de errores en entradas sintéticas o dañadas**, no demuestra que ocurra en las transcripciones congeladas.

## Corrección y regresión

Antes de decidir entre cabecera y locus, se inspecciona el prefijo anterior a la primera coma. Si ese prefijo es un candidato a folio físico (`f2r`, `fRos`, `f86v4`, o incluso una grafía decimal Unicode inválida), se registra `malformed_header_count` y se pone `active_page = None`. **Nunca** se acepta el identificador corrupto como página válida. Los loci normales incluyen el separador `.` y no coinciden con este prefijo.

La prueba determinista incorpora cuatro cabeceras dañadas (folio normal, Rosettes, desplegable y cifras Unicode), y exige un error de cabecera más un `page_mismatch` posterior. Un control con un locus malformado por coma extra exige error de registro, sin cambiar la página activa.

## Comprobación prevista y conservación

- `python tests/test_ivtff_page_locus_ids.py`
- `python scripts/audit_ivtff_page_locus_ids.py` sobre las tres transcripciones originales, sin escribirlas.
- Auditoría de identidad de corpus y resto de `Voynich Check` en la PR; comprobar run, SHA, jobs y conclusión, y repetir la comprobación en `master` si se integra.

**Estado inicial:** la ejecución remota de esta rama aún no está acreditada en este informe. No atribuir éxito a CI hasta consultar la ejecución exacta. No se modifican corpus, hashes históricos, resultados negativos, manifiestos de folios reservados, parámetros de experimentos ni `state/committed_claims.md`. Sin semilla aleatoria; todas las pruebas añadidas son cadenas sintéticas. Esta corrección no certifica la conformidad completa IVTFF ni constituye desciframiento.

## Siguiente incidencia

Continuar con discrepancias de tokenización y procedencia de lectores históricos, pero solo tras cotejar el registro y las ramas/PR activas. No repetir EXP antiguos con entradas sustitutas.
