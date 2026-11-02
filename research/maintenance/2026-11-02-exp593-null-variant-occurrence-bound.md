# EXP-593 — cota de momentos nulos por ocurrencias de variante (2026-11-02)

**Tipo:** corrección operativa del guardia de publicación concurrente, **no** nuevo experimento científico ni reproducción de permutaciones.

## Defecto acotado

En `scripts/check_publisher_source_drift.py`, la rama EXP-593 validaba los momentos de la distribución nula de apariciones al inicio de línea usando solo `doc["lines"]` (4.188). Para cada variante `v`, en cualquier permutación que conserve sus tokens, el número de inicios es `X_v <= min(n_lines, occurrences_v)`. La desigualdad necesaria de varianza `Var(X_v) <= E[X_v] * (M_v - E[X_v])` debe usar ese mismo `M_v`, no el total de líneas. Un JSON con estadísticos z autoconsistentes podía eludir el control anterior.

**Reparación:** usar `maximum = min(doc["lines"], row["occurrences"])` para la media y cota de varianza de cada variante. La corrección afecta únicamente a la exención de resultados nuevos en el guardia de deriva de fuentes; no altera cálculos ni archivos archivados.

## Pruebas adversariales y control positivo

Entrada sintética basada en el esquema del JSON congelado de EXP-593, variante `daiiin` con 19 ocurrencias, 2 inicios observados y 4.188 líneas:

- **Media imposible:** `null_mean_initial=20`, `null_sd_initial=1`, `observed_standardized_statistic=-18`. El control anterior de líneas admitía media y varianza; la cota por 19 ocurrencias debe rechazarlo.
- **Varianza imposible:** `null_mean_initial=10`, `null_sd_initial=20`, `observed_standardized_statistic=-0.4`. La varianza 400 supera la cota `10*(19-10)=90`, pero no la cota incorrecta `10*(4188-10)=41780`.
- **Control positivo congelado:** `research/experiments/2026-11-02-exp593-corrected-L-metadata.json` conserva `daiiin`: media 2.9036, desviación 1.5181261607653036, estadístico −0.5952074493891111. Cumple la nueva cota. Las variantes `daiin` y `dain` también quedan por debajo de sus ocurrencias archivadas (726 y 198).

Las dos regresiones nuevas ejercitan `assert_no_source_drift` sobre commits sintéticos de Git, no solo la fórmula aislada. Pruebas a ejecutar en CI: `python -m unittest discover -s tests -p test_publisher_source_drift.py -v`, y la suite canónica completa según `.github/workflows/voynich-check.yml`. Un cálculo independiente de las dos desigualdades se efectuó con Python 3 en el entorno de trabajo antes del cambio; **no** equivale a ejecutar la suite del repositorio.

## Procedencia y preservación

- Fuente original inmóvil: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- Parámetros archivados EXP-593: 5.000 permutaciones, semilla `20261021`; no se ejecutaron ni recalcularon aquí.
- Base revisada de `master`: `0eb980d446b1099ac4815f5ebdeb353b2582836d`. Scripts y regresiones modificados en rama dedicada; ninguna transcripción, salida histórica, partición reservada o compromiso científico fue editado.
- Control anterior y regresiones: `tests/test_publisher_source_drift.py`. Las dos nuevas entradas se identifican por `test_exp593_rare_variant_null_mean_cannot_exceed_occurrences` y `test_exp593_rare_variant_null_sd_respects_occurrence_bound`.
- Logs de CI, hash del commit definitivo y veredicto de fusión: comprobar en la PR asociada; no se afirma éxito de CI antes de su finalización.

## Alcance y pendientes

El filtro demuestra **consistencia aritmética necesaria**, no identidad de los sorteos, calibración de p-valores, reproducibilidad de los 5.000 barajados ni validez semántica. No hay traducción. Sigue bloqueada la reproducción histórica exacta de EXP-170 por procedencia externa; continúan la adjudicación IVTFF y conciliación de artefactos. No se inició un ciclo científico prohibido ni se asignó nuevo EXP. La fecha objetivo de evaluación sigue siendo 2026-11-22 sin garantía de descifrado.
