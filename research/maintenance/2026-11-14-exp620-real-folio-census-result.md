# EXP-620 — resultado del censo real de atribución por folio (14-11-2026)

## Pregunta falsable y alcance

¿Hay líneas que los regex de los analizadores congelados EXP-613/617 reconocen pero cuyo folio no coincide con la cabecera activa, en las dos transcripciones fijadas? La prueba **no** valida la gramática IVTFF completa ni recupera ejecuciones históricas. No se sustituyen fuentes ni se modifican resultados congelados.

## Ejecución exacta

- Rama: `audit/exp620-legacy-ligature-differential-20261114`; commit ejecutado: `4e16ea7862cbffa2614d3b7f02c9ceaede9c2bff`.
- Código: `research/maintenance/exp620_real_corpus_folio_census.py` (blob Git `5eac03bfd88d96d4c045b3f2e66ff86ba89ea558`).
- Comando CI: `python -m py_compile research/maintenance/exp620_real_corpus_folio_census.py && python research/maintenance/exp620_real_corpus_folio_census.py | tee exp620-folio-census.json && python -m json.tool exp620-folio-census.json > /dev/null && sha256sum exp620-folio-census.json > exp620-folio-census.sha256`.
- [GitHub Actions #43623884674](https://github.com/kyrian20/voynich-autoexploration/actions/runs/43623884674): conclusión `success`, job `check`; se inspeccionó stdout de la ejecución exacta.
- [Artefacto #14125607123](https://github.com/kyrian20/voynich-autoexploration/actions/runs/43623884674/artifacts/14125607123): `exp620-folio-census.json` y `exp620-folio-census.sha256` (retención 90 días). GitHub registra ZIP SHA-256 `38df8a65319a765542c9be06fc7051f5569acacb7c56726c1524548bb0bc70f3`. No se ha descargado/descomprimido el ZIP ni verificado independientemente el hash interno.
- Sin aleatoriedad ni semillas: censo determinista.

| Entrada fijada | SHA-256 de bytes | Cabeceras | Líneas reconocidas | Coinciden | Discordantes | Sin cabecera | Coinciden con $Q=T | Otras líneas no vacías |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `data/transcriptions/eva_zl3b.txt` | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | 184 | 4197 | 4197 | 0 | 0 | 1085 | 4129 |
| `data/transcriptions/eva_it2a.txt` | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | 183 | 4191 | 4191 | 0 | 0 | 1083 | 1070 |

`q_t_mismatched=0` en ambas entradas; no hay ejemplos de discordancia en el subconjunto reconocido.

## Interpretación y decisión de integridad

**Resultado negativo acotado:** no se observa contaminación por desacuerdo entre cabecera y folio de línea **entre los registros que reconoce el regex congelado**, en estas dos entradas y hashes. La regresión sintética sigue mostrando una vulnerabilidad del parser ante una entrada malformada; el resultado real no demuestra que el fallo afectase a los números históricos. **No retirar ni corregir cifras históricas por este motivo sin otra evidencia.**

**Cobertura insuficiente para cerrar la adjudicación IVTFF:** las 4129 líneas no vacías no reconocidas en ZL3b y 1070 en IT2a no fueron clasificadas por este censo. Pueden incluir comentarios, metadatos y registros de otros tipos; no deben etiquetarse automáticamente como errores. El censo usa expresiones regulares específicas, no un parser normativo. Tampoco compara todas las versiones ni las entradas exactas de cada ejecución histórica. El resultado no valida ninguna traducción ni inferencia semántica.

## Próximo trabajo distinto (sin repetir este censo)

Clasificar los registros no reconocidos por categoría IVTFF y contrastarlos con un lector independiente y la especificación, preservando bytes, líneas físicas, hashes y denominadores; después comprobar si alguna exclusión afecta a eventos `ch/sh` en folios reservados. Requiere adjudicación explícita de las políticas de ligaduras y variantes de transcripción antes de recalcular inferencias. Mantener EXP-620 abierto para esta cobertura; no lanzar experimentos lingüísticos que dependan de afirmaciones contradichas.
