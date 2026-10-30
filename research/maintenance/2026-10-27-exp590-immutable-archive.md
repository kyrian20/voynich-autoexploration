# EXP-590 — guardia de archivo inmutable (27-10-2026)

**Tipo:** corrección operativa acotada, sin nuevo experimento ni asignación de ID. **Estado:** pendiente de CI en la PR hasta comprobar su ejecución.

## Defecto y alcance

En `scripts/exp590_daiin_position.py`, las salidas fechadas `research/experiments/YYYY-MM-DD-exp590-corrected-L-metadata.{json,md}` se escribían mediante `Path.write_text`, que **sobrescribe** una pareja existente. La ejecución programada y la CI pueden coincidir el mismo día; el resultado previo podía reemplazarse sin conservar evidencia del cambio. La herramienta EXP-593 ya dispone de una protección similar, que no se duplica.

La reparación EXP-590 comprueba antes de las 5.000 permutaciones si existe una pareja completa con la misma fecha, hash del corpus, parámetros y resúmenes internos. Si es consistente, emite `skipped_existing`, sin reejecutar la simulación ni modificar los archivos. Si la pareja está incompleta, tiene claves JSON duplicadas, destino simbólico, metadatos diferentes, conteos incompatibles o informe truncado, **falla sin sobrescribir** y exige adjudicación humana. Los archivos nuevos se abren con modo exclusivo `x`. Un fallo entre la creación de ambos deja una pareja parcial bloqueada: no se repara ni sustituye automáticamente.

El guardia comprueba integridad **estructural y consistencia interna**, no la reproducción independiente de los valores estadísticos. Los archivos de 27-10-2026 son **históricos**, no se modifican. La cobertura ampliada de EXP-590 sigue siendo distinta de la restringida de EXP-593; no deben compararse como muestras idénticas.

## Entrada, parámetros y límites

- Corpus: `data/transcriptions/eva_zl3b.txt`; SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- Experimento preexistente EXP-590; semilla `20261020`, `N_PERM=5000`; token exacto `daiin`.
- Archivo histórico de referencia: `research/experiments/2026-10-27-exp590-corrected-L-metadata.json` y `.md` (sin mutaciones).
- No se ha ejecutado un nuevo contraste científico en esta reparación; no hay nuevas conclusiones sobre el Voynich, ni traducción validada.
- La validación IVTFF independiente y la procedencia de corpus históricos siguen pendientes. Una CI verde no equivale a certificar todos los experimentos.

## Pruebas y aceptación

Regresiones en `tests/test_exp590_archive_guard.py`: pareja histórica válida, destino nuevo, pareja parcial, hash discordante, JSON duplicado, reasignación Currier, informe truncado, semilla distinta, conteos imposibles, prohibición de sobrescritura y enlace simbólico. La CI canónica ejecuta explícitamente las regresiones antes de invocar EXP-590. Criterio de cierre: regresiones satisfactorias, comprobación de artefactos de la PR y CI de `master` tras fusionar. **No considerar cerrado sin estos enlaces y resultados.**

## Concurrencia y limitaciones

La PR se crea desde `master` `c959732e51e10a65acb9f74da13747fd11f3e91c`. Cinco PR científicas permanecían abiertas (#5, #7, #13, #66 y #82) al preparar el cambio; no se modifican. La ejecución programada `40474457056` generó los cuatro archivos EXP-590/593 del día en `c959732`; su estado satisfactorio no equivale a una CI de `master` para ese commit. La última CI push verificada antes de la reparación corresponde a `61e7017` (`40472029512`).

Si el contenido histórico existente estuviera adulterado pero sus cifras mantuvieran consistencia interna, esta guardia podría aceptarlo. La prueba de reproducción desde el corpus y el cotejo de hashes de artefactos siguen siendo controles separados.
