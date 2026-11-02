# EXP-590 — cierre acotado de integridad del publicador: tasas y cola de permutación

**Fecha:** 2026-11-02. **Base:** `ff010687936fb9bbbb171d4a747da60a010b41bb` (master posterior a PR #255).
**Clase:** corrección operativa; no reproducción de permutaciones ni nuevo experimento.

## Incidencia reproducible y criterio previo

El guardia `scripts/check_publisher_source_drift.py` comprobaba los recuentos de EXP-590 y el dominio del p, pero aceptaba un JSON añadido concurrentemente en el que las tasas inicial/final no correspondieran a sus numeradores, faltaran las excedencias nulas, estas superasen las réplicas, los momentos nulos fueran negativos o imposibles, o el p publicado no correspondiera a la corrección +1 del generador. El archivador `scripts/exp590_daiin_position.py` ya verifica invariantes relacionadas, pero el publicador eximía estos blobs sin esas comprobaciones. No hay evidencia de que los archivos históricos presentaran el defecto.

**Criterio falsable:** siete mutaciones sintéticas deterministas del JSON original deben ser rechazadas por `assert_no_source_drift` leyendo el blob del commit candidato; los cuatro JSON positivos de EXP-590/593/622/623 deben continuar siendo aceptados. No se permite eximir una alteración de entradas o de evidencia ya existente.

## Código y pruebas

- `scripts/check_publisher_source_drift.py`: validar `initial_rate_per_target_occurrence = line_initial_occurrences/target_occurrences` y su análogo final (con `None` para denominador cero), sin booleanos y tolerancia absoluta `1e-12`; exigir `null_ge_observed` entero no negativo y <= permutaciones; momentos nulos finitos, media entre cero y líneas, desviación no negativa; exigir `empirical_one_sided_p = (null_ge_observed+1)/(permutations+1)`.
- `tests/test_publisher_source_drift.py`: siete regresiones: tasa inicial alterada, tasa final booleana, excedencias ausentes, excedencias > réplicas, desviación negativa, media > líneas y p alterado. Se mantiene control positivo de los cuatro archivos publicados.
- No se cambia `scripts/exp590_daiin_position.py`, no se ejecutan permutaciones ni se recalculan valores históricos.

## Procedencia congelada y resultados de referencia

Control positivo: `research/experiments/2026-11-02-exp590-corrected-L-metadata.json` (Git blob `b542a123e3a7a146b93564a7078a5dfefef992a7`).
Transcripción ZL3b `data/transcriptions/eva_zl3b.txt` (SHA-256 declarado `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`).
Semilla `20261020`; 5.000 réplicas; 39.594 tokens, 5.376 líneas, 853 ocurrencias, 161 inicios y 134 finales; 0 excedencias; p archivado `0.0001999600079984003`. Los siete fixtures no usan aleatoriedad.

## Verificación pendiente de CI

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

Este informe por sí mismo **no certifica ejecución**: revisar la CI del SHA exacto de la PR y después la del SHA integrado de master antes de declarar el cierre.

## Límites

Las validaciones comprueban coherencia aritmética y de dominio, no la autenticidad de las permutaciones ni el nulo estadístico, la conformidad IVTFF, el control de selección retrospectiva, una traducción o la validez de un resultado de descifrado. Se conservan corpus, resultados positivos y negativos, semillas, vectores de EXP-170, folios reservados y `state/committed_claims.md` sin modificación. EXP-170 sigue BLOCKED para reproducción histórica exacta por falta de prueba independiente de sus entradas externas. La adjudicación IVTFF y la conciliación de artefactos siguen abiertas.

**Siguiente paso:** cerrar esta incidencia solo tras CI de PR y master, luego continuar recuperación de procedencia histórica EXP-170 y conciliación de artefactos sin nuevos ciclos científicos.
