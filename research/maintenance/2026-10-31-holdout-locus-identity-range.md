# Holdout v2 — unicidad y rango de identificadores de registro

**Fecha:** 2026-10-31. **Base inspeccionada:** `master` `a3050f242662429ad94a9bbb3b111787d61ff1f1`.
**Tipo:** reparación de cobertura estructural, sin experimento científico.

## Defecto reproducible

`scripts/audit_holdout_locus_coverage.py::inspect_source` aceptaba dos registros físicos con el mismo identificador completo (por ejemplo, `<f1r.1,@P0>` repetido) y números de registro fuera del intervalo 1..160 (por ejemplo, `<f1r.0,@P0>` y `<f1r.999,@P0>`). La expresión regular original solo exigía entre uno y tres dígitos y no conservaba el conjunto de IDs vistos. Esto podía inflar el recuento de registros del auditor independiente con una fuente sintética rehasheada, sin cambiar las hojas elegibles ni las particiones. El lector estricto `scripts/audit_ivtff_page_locus_ids.py` ya rechaza ambas anomalías; esta reparación cierra la divergencia de validación cuando se usa el auditor de cobertura de forma independiente.

## Reparación y regresiones

Se guarda un conjunto de identificadores de locus ya observados y se rechazan duplicados con número de línea. Se comprueba que el índice numérico esté entre 1 y 160, incluidos los extremos. Tres nuevas pruebas cubren: duplicados de página normal, panel y Rosettes; índices 0, 161 y 999 y control positivo 160; y fuente sintética con SHA-256 actualizado en su manifiesto que no puede ocultar el duplicado.

**No se alteran** corpus, hashes congelados, manifiestos, sal, particiones, datos reservados, semillas, resultados históricos, scripts de experimentos ni `state/committed_claims.md`. El bloqueo EXP-170, la adjudicación IVTFF completa y la conciliación de artefactos persisten. No se atribuye semántica a ninguna secuencia.

## Verificación exigida

```sh
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python -O -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python scripts/audit_holdout_locus_coverage.py
python scripts/audit_ivtff_page_locus_ids.py
```

Verificar los logs de CI del SHA exacto de la rama y, si se integra, del nuevo `master`. Este informe no presupone resultados de ejecución. La reparación no convierte el holdout prospectivo en históricamente ciego ni valida traducción. Evaluación final: 2026-11-22.
