# EXP-590 — cota de soporte de los momentos nulos y conciliación JSON/Markdown

**Fecha:** 2026-11-02. **Base fija:** `ebbefd861ae82e1f1feb761b5c054dc57b605c56` (master después de PR #257). **Estado:** reparación operativa propuesta; no reproducción de permutaciones ni experimento nuevo.

## Incidencia, alcance y criterio previo

Dos validadores de EXP-590 aceptaban momentos nulos matemáticamente imposibles. El guardia de publicación `scripts/check_publisher_source_drift.py` exigía media <= número de líneas y desviación no negativa, pero no limitaba la media por el número de ocurrencias de `daiin` ni la varianza por el soporte. `archive_status` en `scripts/exp590_daiin_position.py` no imponía estas cotas y, además, cotejaba el p del JSON con el informe Markdown pero **no** la media/desviación nulas impresas. Un JSON alterado podía superar el control de archivo si los demás campos permanecían intactos.

En cada permutación de EXP-590, `X` cuenta líneas que empiezan por el token exacto `daiin`. Como cada línea solo tiene una primera posición y no se crean tokens, necesariamente `0 <= X <= M = min(n_líneas, n_ocurrencias)`. Por la cota de varianza de una variable acotada, `Var(X) <= E[X] * (M - E[X])`. La implementación de referencia usa desviación poblacional sobre 5.000 permutaciones, por lo que la desigualdad es aplicable sin reconstruir esas permutaciones.

**Criterio falsable previo a CI:** dos JSON sintéticos (media superior al número de tokens objetivo; desviación que viola la cota) deben ser rechazados por el publicador al leer el blob del commit candidato. Cuatro mutaciones equivalentes o de discordancia con Markdown deben ser rechazadas por `archive_status`. Los cuatro JSON positivos de los generadores 590/593/622/623 y el par congelado del 27-10-2026 deben seguir aceptándose. Las pruebas son deterministas y no usan semilla ni datos nuevos.

## Modificaciones propuestas

- `scripts/check_publisher_source_drift.py`: acotar media y varianza por `M=min(lines,target_occurrences)` y conservar el rechazo de NaN/Inf, booleanos, excedencias y p incompatibles.
- `scripts/exp590_daiin_position.py`: aplicar las mismas condiciones en la validación de archivo existente; exigir que la media y desviación impresas (3 decimales) coincidan con los valores del JSON, igual que se exige para el p y los recuentos.
- `tests/test_publisher_source_drift.py`: dos regresiones adversariales nuevas con comparación de commits Git.
- `tests/test_exp590_archive_guard.py`: cuatro regresiones de soporte, varianza y desacuerdo JSON/Markdown sobre una copia temporal del archivo congelado.

## Procedencia, parámetros y preservación

Control positivo actual: `research/experiments/2026-11-02-exp590-corrected-L-metadata.json` (blob Git `b542a123e3a7a146b93564a7078a5dfefef992a7`). Fuente inmutable `data/transcriptions/eva_zl3b.txt`, SHA-256 archivado `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`. Semilla 20261020, 5.000 permutaciones, 5.376 líneas, 39.594 tokens, 853 `daiin`, media nula 109.1214, desviación 9.314948311182407; el par del 27-10-2026 es el fixture congelado para `archive_status`. No se modifican resultados, corpus, particiones reservadas, parámetros ni semillas. No se vuelve a ejecutar la simulación.

## Comprobaciones exigidas y evidencia

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -m unittest discover -s tests -p 'test_exp590_archive_guard.py' -v
python -O -m unittest discover -s tests -p 'test_exp590_archive_guard.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La CI `voynich-check.yml` ejecuta los tests del publicador y la suite general; debe comprobarse su ejecución en el SHA de la PR y, tras integrar, en el SHA de master. **Este informe no certifica por sí mismo que las pruebas hayan pasado.** Se deben enlazar los runs y comprobar los artefactos antes de cerrar.

## Limitaciones y estado científico

Son relaciones necesarias de coherencia, **no** una reproducción de los 5.000 vectores nulos ni una validación del procedimiento de permutación. El cotejo Markdown utiliza el redondeo a tres decimales del generador; no detecta modificaciones menores que esa precisión y no es una prueba criptográfica de identidad de contenido. No hay evidencia de que el archivo histórico real presente el defecto sintético. Se conserva el original; no se rehabilita ninguna afirmación estadística ni se propone significado para `daiin`. EXP-170 continúa BLOCKED para reproducción exacta por entradas externas no acreditadas; siguen pendientes la adjudicación IVTFF y la conciliación general de artefactos. No se ejecutan ciclos científicos bloqueados.
