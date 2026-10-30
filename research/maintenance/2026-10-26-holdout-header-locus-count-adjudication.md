# Corrección de recuentos de cabeceras y loci en la cobertura del holdout — 26-10-2026

**Tipo:** incidencia de integridad descriptiva, sin EXP nuevo. **Estado de este informe:** corrección propuesta; cierre condicionado a CI y artefacto del commit exacto. No se ejecuta una prueba de desciframiento.

## Defecto comprobado sobre las fuentes congeladas

`scripts/audit_holdout_locus_coverage.py::inspect_source` incrementaba `numeric_record_count` para **cada etiqueta** `<f…>`, incluidas las cabeceras de página sin locus. De igual forma, `named_locus_records` y `named_locus_record_count` contaban `<fRos>` como si fuera un registro de texto. Esto no alteraba la partición física de hojas, pero confundía los denominadores de cobertura y podía inducir a reutilizar un número de etiquetas como número de loci.

Comprobación de solo lectura de los dos archivos originales de `master` `5c83aeb25bc2ba8cf536c3545bf98863c9e33198`, distinguiendo etiquetas de página (sin punto ni coma en el identificador) y etiquetas de locus:

| Fuente | SHA-256 esperado del manifiesto v2 | Etiquetas numéricas | Cabeceras numéricas | Loci numéricos | Etiquetas nombradas | Cabeceras nombradas | Loci nombrados |
|---|---|---:|---:|---:|---:|---:|---:|
| `eva_zl3b.txt` | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | 5451 | 226 | 5225 | 161 | 1 | 160 |
| `eva_it2a.txt` | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | 5440 | 225 | 5215 | 0 | 0 | 0 |

La auditoría anterior de cobertura informó `Ros=161` como *loci*; la descomposición correcta es una cabecera de página `fRos` y 160 registros de locus. Se conserva el artefacto histórico del run [40242799406](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40242799406); no debe usarse su antiguo campo `named_locus_record_count` como denominador de texto.

## Reparación

El lector conserva la extracción de hojas y la validación de hashes/manifiesto, pero ahora publica `numeric_tag_count`, `numeric_page_header_count`, `numeric_locus_record_count`, `named_tag_count`, `named_page_headers`, `named_page_header_count`, `named_locus_records` y `named_locus_record_count`. Se elimina el antiguo nombre ambiguo `numeric_record_count`. Se mantiene `named_locus_records` con su significado literal corregido (solo loci). Las pruebas incluyen cabeceras, registros, un encabezado repetido y la separación de Rosettes; la CI genera un nuevo JSON de cobertura sin sobrescribir el anterior.

**Regla de regresión:** para cada edición, el total de etiquetas numéricas debe ser la suma de cabeceras y loci numéricos; lo mismo para etiquetas nombradas. El test de las tres hojas sintéticas debe distinguir 3 cabeceras de 3 loci, y la cabecera repetida no puede incrementar los loci.

## Reproducción y puerta de cierre

```sh
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python scripts/audit_holdout_locus_coverage.py --out holdout-locus-coverage.json
```

La CI `Voynich Check` ejecuta ambos comandos y conserva `holdout-locus-coverage-<run_id>`. No declarar la reparación cerrada hasta comprobar la ejecución del commit exacto y el artefacto. Los recuentos son deterministas; no hay semilla ni selección de parámetros. El origen es el manifiesto v2 congelado y sus SHA-256; el lector sigue siendo una auditoría de cobertura, no un parser IVTFF completo.

## Limitaciones

No se cambian corpus, scripts históricos, manifiestos v1/v2, resultados negativos ni `committed_claims`. Los 102 folios elegibles y sus grupos 68/16/18 no se modifican. Los folios de prueba ya habían sido expuestos históricamente; este trabajo no evalúa hipótesis lingüísticas, ni proporciona anclas semánticas o traducción. Persisten la conformidad IVTFF independiente, la procedencia de comparadores históricos y la reconciliación de artefactos de la Biblioteca.
