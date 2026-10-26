# Incidencia acotada: auditor de cobertura del holdout acepta etiquetas IVTFF por prefijo

Fecha: 2026-10-26. Estado inicial: **propuesta de corrección, pendiente de CI**. Sin EXP nuevo ni traducción.

## Defecto y criterio falsable

`scripts/audit_holdout_locus_coverage.py` usaba `NUMERIC.match` / `NAMED.match` sobre el comienzo de cada línea. Un encabezado malformado como `<f9r>garbage`, un panel imposible `<f9r7>` o un locus huérfano `<f9r.1,@P0>` podían contarse como cobertura de una hoja física, sin cabecera válida. El problema es distinto del selector v2 ya reparado en las PR #84 y #85: aquí la superficie afectada es el auditor **independiente** de cobertura, que podía avalar una entrada autoconsistente pero malformada.

Criterio previo: rechazar los tres casos anteriores y las etiquetas pegadas; exigir forma completa de cabecera o locus, límite posterior de etiqueta y pertenencia del locus a la página activa. Mantener los recuentos de las dos transcripciones originales y las asignaciones congeladas. No alterar fuentes ni manifiestos.

## Cambio propuesto

El auditor mantiene expresiones locales (sin importar el parser principal) y valida cada etiqueta completa antes de contabilizarla. Un locus sin cabecera o asociado a otra página se rechaza. Se conserva el tratamiento separado de `fRos`, la exclusión de hojas no numéricas y la detección de hojas no positivas. Los tests sintéticos antiguos se ajustan a loci válidos con código de tres caracteres, sin convertir esas entradas sintéticas en evidencia del manuscrito.

Archivos: `scripts/audit_holdout_locus_coverage.py` y `tests/test_holdout_locus_coverage.py`. Ningún corpus, manifiesto, resultado negativo o script histórico se sobrescribe.

## Procedencia y comprobación previa

Base: `master` `d283d59634af26f6c9a1156bf3c65649a0ba6d00`. Fuente ZL3b blob Git `2a4533ab9bdfa85db9bad602d590978953055df1`, SHA-256 archivado `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`. IT2a blob Git `4d6d3f2537b1f507a257529b49c94af7d6e03446`, SHA-256 archivado `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

Lectura de las líneas originales desde GitHub, verificada con un cotejo independiente de etiquetas y página activa antes de escribir: ZL3b 226 cabeceras numéricas, 5225 loci numéricos, 1 cabecera Ros, 160 loci Ros, 102 hojas; IT2a 225 cabeceras numéricas, 5215 loci numéricos, 0 Ros, 102 hojas. **Cero** etiquetas originales rechazadas por el nuevo criterio en ese cotejo. Es una inspección de cobertura, no una reproducción local del script completo.

## Pruebas y reproducción requerida

Determinista; semilla no aplicable. Unidad: etiqueta IVTFF y página física activa. Control positivo: cabeceras y loci sintéticos válidos con paneles y Ros; adversariales: locus huérfano, locus de otra página, sufijo pegado, panel inválido, coma en cabecera y locus incompleto. Las comprobaciones no utilizan folios de prueba para elegir reglas semánticas.

En CI (Python 3.12):

```sh
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python scripts/audit_holdout_locus_coverage.py --out /tmp/holdout-locus-coverage.json
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La comparación de artefactos históricos debe comprobarse si cambia cualquier resultado: **no** reemplazar el manifiesto ni considerar el resultado REPRODUCED sin run y artefacto específicos.

## Límites

Esto corrige aceptación de entradas malformadas en el auditor; no demuestra corrupción de las dos fuentes actuales. La cobertura no certifica IVTFF completo, ni que los folios reservados sean históricamente ciegos. No se prueba una hipótesis lingüística ni se recupera texto plano. El piloto semántico continúa BLOCKED por falta de referente y anotadores independientes. La auditoría histórica de corpus y EXP sigue abierta.
