# EXP-601 — bloqueo de identidad de páginas/paneles en auditoría retrospectiva

**Fecha:** 2026-10-28. **Tipo:** reparación acotada de integridad del auditor derivado de PR #134. **Estado:** propuesta hasta comprobar CI y revisión; no es un nuevo experimento ni una reproducción del bootstrap.

## Defecto demostrado antes del parche

`scripts/audit_exp601_physical_leaf_cluster_scope.py` exigía 81 unidades, 40 hojas numeradas, 36 con ambas caras y el histograma `{"1":3,"2":35,"4":2}`, pero **no fijaba la identidad exacta de las 81 etiquetas**. Una sustitución sintética de `f103r` por `f103r1` conserva los cuatro resúmenes y, sin embargo, cambia la etiqueta archivada. El antiguo guardia aceptaba ese caso al llamar `adjudicate` con un diccionario manipulado. La ruta normal `audit()` ya comprueba el hash del JSON congelado; el defecto estaba en el contrato de adjudicación aislado y su prueba, no en una modificación observada de los originales.

## Reparación y evidencia

Se añade `FROZEN_PAGE_IDS_SHA256=03817ab591c91407bb9502f7ae2cf33fc946fc2b43c1cb4228e41ff7bc5d5795`, calculado sobre la lista de 81 IDs en el **orden del archivo histórico** mediante `json.dumps(ids, ensure_ascii=True, separators=(",", ":")).encode("ascii")`. Se rechazan tanto sustituciones con resúmenes idénticos como reordenaciones. El hash se incluye en el JSON derivado del auditor para que pueda cotejarse; por ello **el artefacto derivado cambia deliberadamente**, aunque los 81 IDs y recuentos no cambian. La comprobación de SHA-1 Git del script/resultados históricos y SHA-256 del corpus permanece obligatoria.

Pruebas sintéticas: sustitución `f103r -> f103r1` conservando agregados, permutación de dos IDs, rechazo de una hoja distinta y aceptación del archivo congelado. Ejecutar:

```sh
python -m unittest discover -s tests -p 'test_exp601_physical_leaf_cluster_scope.py' -v
python -O -m unittest discover -s tests -p 'test_exp601_physical_leaf_cluster_scope.py' -v
python scripts/audit_exp601_physical_leaf_cluster_scope.py --out exp601-physical-leaf-scope.json
sha256sum exp601-physical-leaf-scope.json
```

La CI ya contiene estos comandos y publica JSON + hash; no se añade otro workflow. Conservar corpus, programas y resultados congelados. El estado científico de EXP-601 sigue **INVALID_FOR_CLAIM** solo para intervalos supuestamente agrupados por hoja física. La corrección **no** recalcula el bootstrap, no valida el parser IVTFF ni asigna significado a `daiin`.

**Límites:** SHA-256 identifica el orden de etiquetas archivadas, no demuestra procedencia independiente ni validez codicológica. El agrupamiento por número de hoja es una aproximación, no una reconstrucción de bifolios. Evaluación general prevista: 2026-11-22, sin prometer descifrado.
