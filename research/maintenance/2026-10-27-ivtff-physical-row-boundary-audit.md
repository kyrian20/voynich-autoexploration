# Auditoría IVTFF: delimitadores físicos que falsifican folios — 2026-10-27

**Tipo:** reparación acotada de integridad, sin EXP nuevo ni interpretación semántica.
**Base inspeccionada:** `master` `8e82003c5eb0be81756cca39ab402825d19e52f6`.
**Estado inicial:** propuesta en rama; no declarar cierre hasta verificar CI de PR y de `master` después de integrar.

## Defecto concreto y demostración falsable

`scripts/audit_ivtff_page_locus_ids.py::audit_text` recorría `text.splitlines()`. Python divide también por VT (U+000B), FF (U+000C), FS/GS/RS (U+001C–U+001E), NEL (U+0085), LS (U+2028) y PS (U+2029), además de CR/LF. Un archivo con solo dos saltos LF podía aparentar cuatro líneas IVTFF. En particular, la cadena física `# comment\u2028<f2r> <! $L=B>` podía convertir parte de un comentario en una cabecera de folio y hacer que una línea posterior de `f2r` pareciera correctamente atribuida. La implementación previa aceptaba este fixture sintético sin diagnosticar la separación anómala.

Esto es un **defecto del auditor**, no una demostración de que ZL3b, ZL3a o IT2a contengan esos caracteres. Ya existía una protección similar en el adaptador léxico `scripts/ivtff_rows.py`; aquí se corrige el **auditor estructural independiente**, sin repetir aquel cambio ni tocar el lector histórico congelado.

## Reparación

- `scripts/audit_ivtff_page_locus_ids.py`: delimitar registros físicos solo por CR, LF o CRLF; rechazar explícitamente los ocho separadores adicionales reconocidos por `splitlines()`. Conservar el número real de línea, código Unicode y un máximo de 50 ejemplos diagnósticos, pero contabilizar todos. Si una línea está contaminada, no reconocer su cabecera ni conservar el folio activo.
- `tests/test_ivtff_physical_row_boundaries.py`: ocho variantes de cabecera falsificada dentro de comentario, cabecera contaminada, tres convenciones válidas de salto de línea, límite de previsualización diagnóstica y comentario Unicode no separador.
- `.github/workflows/voynich-check.yml`: ejecutar la nueva regresión junto a la auditoría IVTFF estructural existente.

## Reproducción, controles y conservación

Comandos desde la raíz (Python 3.12):

```sh
python -m unittest discover -s tests -p 'test_ivtff_physical_row_boundaries.py' -v
python tests/test_ivtff_page_locus_ids.py
python scripts/audit_ivtff_page_locus_ids.py
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

Los fixtures son deterministas: **semilla no aplicable**. El criterio previo es que todos los separadores no físicos sean rechazados, que CR/LF/CRLF y comentarios ordinarios permanezcan válidos, y que el inventario real continúe pasando. Los hashes de fuentes y el resultado de CI deben verificarse en la ejecución concreta; **no se han modificado** las transcripciones, manifiestos, corpus de referencia, salidas históricas, particiones reservadas ni compromisos públicos.

## Límites y siguiente paso

La reparación no valida todas las reglas de IVTFF, no certifica los análisis históricos ni demuestra significado de ninguna palabra. La procedencia de corpus, adjudicación independiente de alternativas/ligaduras y PR científicas en borrador siguen abiertas. Revisar el diff y la CI exacta de la PR; si es satisfactoria, fusionar y verificar el nuevo `master` y sus artefactos. No ejecutar experimentos científicos bloqueados por contradicciones pendientes.
