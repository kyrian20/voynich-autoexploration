# Corrección acotada — límites de etiquetas en auditor estructural IVTFF

Fecha: 2026-10-27. Estado inicial: **PROPUESTA, pendiente de CI**. No se asigna EXP nuevo.

## Defecto falsable y alcance

En `scripts/audit_ivtff_page_locus_ids.py`, `audit_text` extraía el texto hasta el primer `>` y validaba la forma interna, **sin comprobar el carácter siguiente**. Por ello `<f2r>garbage` se contabilizaba como cabecera válida y `<f1r.2,@P0>garbage` como locus válido. El auditor independiente de cobertura del holdout ya rechaza sufijos pegados (PR #86), pero el auditor estructural general seguía aceptándolos. No se encontró esta forma en las tres transcripciones originales consultadas: el defecto afecta a la validación de entradas futuras o alteradas, no demuestra corrupción histórica.

**Criterio previo:** rechazar cabeceras y loci cuyo `>` esté seguido inmediatamente por otro carácter que no sea espacio o tabulador; una cabecera dañada invalida el folio activo, y los registros posteriores no pueden heredar la página anterior. Conservar la aceptación de etiquetas correctamente separadas, los recuentos originales y las auditorías independientes.

## Implementación y regresión

Cambios limitados a `scripts/audit_ivtff_page_locus_ids.py` y `tests/test_ivtff_page_locus_ids.py`. La guarda se ejecuta después de extraer la etiqueta, antes de contabilizarla. Se añaden cuatro cabeceras adversariales (incluidas Rosettes, panel y cifra Unicode), dos loci con sufijo pegado y un control positivo con separadores válidos. Las comprobaciones no asignan significado a texto Voynich ni tocan folios reservados. No hay semilla aleatoria.

Pruebas previstas en la CI canónica:

```sh
python tests/test_ivtff_page_locus_ids.py
python scripts/audit_ivtff_page_locus_ids.py
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

## Procedencia

Base `master` `8eff52d5ee8c1f838839b8d2d516f1301e039231`. Fuentes congeladas:
- ZL3b: `data/transcriptions/eva_zl3b.txt`, blob Git `2a4533ab9bdfa85db9bad602d590978953055df1`, SHA-256 publicado `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: `data/transcriptions/eva_it2a.txt`, blob Git `4d6d3f2537b1f507a257529b49c94af7d6e03446`, SHA-256 publicado `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- ZL3a: `data/transcriptions/zl3a.txt`, blob Git `fe09c6a2f7fbc9649eecbe0c97147e00a3a86934`; SHA-256 de contenido no recalculado en esta revisión.

Inspección directa de los textos recuperados de GitHub: **cero** filas que comiencen por `<f` y presenten un sufijo pegado al primer `>` en ZL3b (8.511 líneas), IT2a (5.445 líneas) y ZL3a (8.514 líneas). Es un cotejo de patrón sobre los contenidos recibidos, no una reproducción completa ni certificación IVTFF. Los hashes SHA-256 de las dos fuentes citados arriba proceden del manifiesto congelado; no se han recalculado en este bloque.

## Límites y decisión

Corrección operativa del auditor de etiquetas, no una nueva hipótesis de desciframiento. No modifica corpus, manifiestos, EXP, resultados negativos ni `state/committed_claims.md`. Las transcripciones siguen siendo ediciones del mismo manuscrito. La conformidad completa IVTFF, las adjudicaciones históricas y las pruebas semánticas independientes permanecen pendientes. Si CI falla, conservar fallo y reparar solo la causa demostrada; no fusionar sin verificar el SHA y los artefactos.
