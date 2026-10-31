# Holdout v2 — cabeceras físicas duplicadas en el auditor independiente

**Fecha:** 2026-10-31. **Base comprobada:** `master` `1da1bd9558a7c49db37ef565f0f7ddbc4bbec8d4`.
**Tipo:** corrección de integridad estructural, **no** experimento científico ni validación semántica.

## Defecto y alcance

`scripts/audit_holdout_locus_coverage.py::inspect_source` almacenaba los nombres de páginas en un conjunto, pero no rechazaba una segunda cabecera física con el mismo identificador. La segunda cabecera aumentaba `numeric_page_header_count` o `named_page_header_count`, mientras `numeric_leaves` y las particiones permanecían intactas. En un corpus sintético rehasheado junto con su manifiesto, el auditor independiente podía aceptar la fuente aunque tuviera una cabecera repetida. Esto no demuestra corrupción del corpus original: los SHA-256 congelados se siguen verificando y otro lector IVTFF ya disponía de una prueba de cabeceras únicas.

## Reparación

Se rechaza una segunda cabecera física con el mismo identificador de página, incluyendo paneles desplegables y `fRos`, indicando la línea. Se reemplaza la antigua prueba que aceptaba cabeceras repetidas por regresiones adversariales de tres clases y se añade una regresión de auditoría completa con SHA-256 sintético recalculado. Se conserva el control positivo existente de las ediciones ZL3b e IT2a.

## Comandos de verificación

```sh
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python -O -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python scripts/audit_holdout_locus_coverage.py
python scripts/audit_holdout_page_crosswalk.py
```

Verificar por separado el resultado de Voynich Check del **head de la PR** y, si se integra, del **SHA posterior de master**. Este informe no presupone su éxito. Los corpus, manifiestos, semillas, particiones, transcripciones, resultados históricos y afirmaciones comprometidas permanecen sin editar.

**Límites:** auditoría de identificadores y cobertura, no conformidad IVTFF completa. El holdout prospectivo no es históricamente ciego; EXP-170 permanece bloqueado para reproducción exacta y no se ha producido traducción. Evaluación global prevista para 2026-11-22, sin garantía de descifrado.
