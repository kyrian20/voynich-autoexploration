# Zhang–Sheng: no omitir loci malformados ni duplicar identidades físicas

**Fecha:** 2026-11-01. **Clase:** reparación acotada de integridad de lectores; sin EXP nuevo ni inferencia semántica.
**Base inspeccionada:** `master` `e1001c12545524be42b90bbee0f413a53e85af62` (CI posterior #41334802914 satisfactoria).
**Estado inicial de esta reparación:** pendiente de verificar CI de la PR y `master` posterior; no se declara cerrada por el mero commit.

## Incidencia y criterio falsable

La auditoría parcial de pares Zhang–Sheng contenía dos lectores con cobertura asimétrica de registros. El lector EVA aceptaba un locus sintácticamente arbitrario mientras comenzara por la cabecera de página vigente, y podía contabilizar dos veces el mismo locus numérico con ceros iniciales. El lector ASCII histórico además omitía silenciosamente un locus malformado o huérfano porque el regex de línea no coincidía o porque no existía página activa. Un registro sin cierre `>` también podía ignorarse. En todos estos casos el universo de líneas, el conteo de pares o la partición por páginas podría cambiar sin error visible.

**Criterio adversarial:** ambos lectores deben rechazar loci huérfanos, malformados, con número cero, de otra página, sin cierre y alias duplicados de la misma combinación (número de línea, etiqueta de localización). La validación debe ocurrir **antes** de filtrar categorías P/C/R, para que una categoría excluida no oculte la corrupción. Dos etiquetas diferentes del mismo número de línea son registros distintos y deben seguir siendo aceptadas.

## Cambio de código y regresiones

`research/maintenance/2026-11-01-zs-wordpair-audit/wordpair_audit.py` incorpora `checked_text_locus()` compartida y rechazo de filas que parecen etiquetas `<f...` pero no cierran correctamente. Ambos lectores emplean la misma validación de identidad; no se modifica la proyección de tokens, el algoritmo de permutación, el ajuste estadístico ni el formato de salida.

`tests/test_zs_wordpair_source_lock.py` añade tres regresiones: duplicados por ceros iniciales incluso en categoría excluida; cinco corrupciones estructurales por ambos lectores; y control positivo de etiquetas distintas en la misma línea numérica.

Antes de la reparación, una inspección de las fuentes originales en `master` contó 227 cabeceras de página y 5.385 registros de locus en ZL3b, y 225 cabeceras y 5.215 loci en IT2a; no se detectaron loci malformados, huérfanos ni alias duplicados bajo la gramática de este lector. Este censo es **una comprobación de estructura acotada**, no certificación IVTFF integral. Los tests existentes deben verificar que las cabeceras originales se conservan y que las dos filas numéricas preseleccionadas del archivo congelado siguen reproduciéndose.

## Comprobación obligatoria

```sh
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
python scripts/check_corpus_integrity.py
```

La CI canónica `Voynich Check` ya invoca los tests específicos en modo normal y optimizado, además de la reproducción de **2/54** filas congeladas, y archiva el log con SHA-256. Comprobar ejecución y artefactos de esta PR y después el SHA de `master`; no atribuir a esta reparación una reproducción de las otras 52 filas.

## Conservación y límites

Fuentes originales congeladas: ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`, IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. No se editan corpus, `results.json`, parámetros (20 barajados; semillas 20261101–20261103; 150/300/600 tipos), controles negativos, manifiestos reservados ni `state/committed_claims.md`.

El defecto se prueba con entradas sintéticas; **no se afirma corrupción de las transcripciones originales**. El artículo Zhang–Sheng continúa sin réplica exacta, la adjudicación IVTFF completa sigue abierta, y EXP-170 permanece `BLOCKED` para reproducción histórica por falta de recibos de entradas externas de abril. No se ejecuta un ciclo científico nuevo ni se atribuyen significados. Próximo paso tras CI: continuar la conciliación de procedencia EXP-170/artefactos. Evaluación general: 22-11-2026, sin promesa de descifrado.
