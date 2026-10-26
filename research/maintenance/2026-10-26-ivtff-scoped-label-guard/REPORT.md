# IVTFF: guardia de etiquetas de folio en proyecciones acotadas — 2026-10-26

**Tipo:** reparación de integridad de entradas sintéticas; no EXP nuevo ni inferencia lingüística.
**Base exacta:** `master` `a7fcd15b17613fee1e5644fb864a1eb6646f4175`.
**Estado:** propuesto en rama; la CI del SHA de la PR debe comprobarse antes de integrar.

## Defecto y criterio previo

`scripts/ivtff_rows.py::tokens_scoped_rows` agrupa filas contiguas por `(source_id, folio_id)` y permite unir palabras partidas por `/` dentro de ese ámbito. Su validación anterior exigía cadenas no vacías sin espacios exteriores, pero admitía identificadores inventados como `f1r-f1v`, `f1r.1` o `f1r\nf1v`. Así, dos fragmentos `a/` y `/b` etiquetados con un ámbito compuesto podían producir `ab` sin que la función advirtiera que la etiqueta no representa un único folio físico. También admitía caracteres de control/invisibles incrustados en `source_id`.

**Criterio de aceptación fijado antes de la CI:** rechazar etiquetas de folio que no coincidan exactamente con el formato de página ya admitido por el auditor estructural (`f<dígitos ASCII><r|v>[1-6 opcional]` o `fRos`), rechazar identificadores de fuente con caracteres no imprimibles, mantener casos válidos `fRos` y `f86v6`, y conservar las pruebas previas de continuaciones correctas. No reinterpretar datos históricos.

## Cambio acotado

- `scripts/ivtff_rows.py`: comprobación sintáctica de `folio_id` y `source_id.isprintable()` antes de añadir una fila al grupo. Los identificadores de origen siguen siendo etiquetas proporcionadas por quien llama, no pruebas criptográficas de procedencia.
- `tests/test_ivtff_lossless.py`: regresiones con folio compuesto, folio con salto de línea, identificador de locus usado como folio, dígitos Unicode y fuente con salto de línea o carácter invisible; controles positivos `fRos` y `f86v6`.
- Ningún cambio a `scripts/ivtff_lossless.py`, corpus, snapshots, particiones reservadas, resultados negativos o `state/committed_claims.md`.

## Reproducción y evidencia pendiente

Prueba determinista sin semilla aleatoria ni corpus externo:
```sh
python tests/test_ivtff_lossless.py
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

El workflow `Voynich Check` incluye `tests/test_ivtff_lossless.py`; se debe inspeccionar el run `pull_request` del SHA exacto y posteriormente el run `push` de `master` si se fusiona. La CI verde prueba únicamente los controles ejecutados, no la conformidad total IVTFF.

## Limitaciones

No se ha demostrado que alguna entrada real del manuscrito estuviera mal etiquetada, ni que los experimentos históricos llamaran a esta API con identificadores compuestos. La validación de formato no verifica que cada etiqueta corresponda al folio físico correcto, que no haya contaminación de holdout ni que las transcripciones sean independientes. Los desacuerdos de tokenización histórica y las reclamaciones semánticas siguen bloqueados. No se obtiene traducción.
