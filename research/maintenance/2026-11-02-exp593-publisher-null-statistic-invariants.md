# EXP-593 — puerta de integridad de momentos nulos, estadístico z y max-T

**Fecha:** 2026-11-02. **Base fijada:** `4eb94ea9af674d4ab29072cc7fcfd1f7c8e2a9c0` (master posterior a PR #256). **Tipo:** reparación operativa de aceptación de resultados concurrentes; no es un experimento nuevo, ni una reproducción científica.

## Defecto y criterio falsable

`scripts/check_publisher_source_drift.py` aceptaba JSON nuevos de EXP-593 con medias/desviaciones nulas no finitas o imposibles, estadísticos estandarizados incongruentes, p-valores incompatibles con la rejilla discreta de 5.000 permutaciones, o p ajustado max-T inferior al p empírico. El generador `scripts/exp593_daiin_variants.py` calcula `z=(observed-null_mean)/null_sd` (z=0 si sd=0), los dos p con corrección `(exceedances+1)/(permutations+1)`, y max-T como máximo de los z nulos de las variantes predefinidas.

**Criterio previo:** ocho mutaciones sintéticas deterministas de un JSON archivado deben rechazarse mediante `assert_no_source_drift` leyendo el blob del commit candidato. Los cuatro JSON archivados de EXP-590, 593, 622 y 623 deben continuar siendo aceptados. No se alteran entradas, resultados históricos ni el generador.

## Código y regresiones

- `scripts/check_publisher_source_drift.py`: comprueba media nula entre 0 y líneas, desviación no negativa y la cota de varianza de una variable acotada `sd² <= mean*(lines-mean)`; números finitos sin booleanos; z observado consistente (tolerancia absoluta `1e-10`); p de cola en la rejilla `k/(permutations+1)` con `k >= 1` (tolerancia `1e-8` tras multiplicar); y p max-T >= p empírico.
- `tests/test_publisher_source_drift.py`: ocho regresiones para desviación negativa, media fuera de rango, desviación imposible, z alterado, z booleano, p empírico fuera de rejilla, p max-T fuera de rejilla y p ajustado menor que p bruto.
- No se han ejecutado permutaciones nuevas; los fixtures no usan aleatoriedad.

## Referencia congelada

Control positivo: `research/experiments/2026-11-02-exp593-corrected-L-metadata.json`, blob Git `84ccf9b64b1f5a3c84ac0ce0138e54f30b71c162`. Fuente ZL3b `data/transcriptions/eva_zl3b.txt`, SHA-256 declarado `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`. Semilla `20261021`; 5.000 permutaciones; 4.188 líneas, 32.732 tokens. Estos recuentos pertenecen a la cobertura histórica restringida de EXP-593 y **no** a la población más amplia de EXP-590.

## Verificación necesaria

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

**Este documento no certifica que se hayan ejecutado las pruebas.** La aceptación depende de la CI de la PR sobre el SHA exacto, seguida de una CI posterior a la fusión en master. Conservar los logs y el enlace a cada ejecución.

## Límites

Estas son relaciones aritméticas necesarias, no suficientes. No verifican los vectores de permutación originales, la adecuación del nulo, la selección retrospectiva de variantes, la tokenización IVTFF ni el significado del texto. No se corrigen ni rehabilitan resultados históricos; no se declara traducción. EXP-170 sigue BLOCKED para reproducción exacta por ausencia de evidencia independiente de sus entradas externas. Persisten adjudicación IVTFF y conciliación de artefactos. No se han tocado corpus, archivos congelados, semillas, particiones reservadas ni `state/committed_claims.md`.
