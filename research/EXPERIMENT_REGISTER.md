# Registro de numeracion de experimentos

Actualizado: 2026-10-20.

## Regla
Los identificadores EXP son unicos. Las fases, los experimentos y las ejecuciones de Actions son series distintas. Un reintento no crea un EXP nuevo. No borrar resultados antiguos: registrar conflictos y conservar los artefactos.

## Conflictos conocidos
- EXP-590: los archivos creados el 20-10-2026 pueden colisionar con numeracion previa; no asumir que sean el EXP-590 historico.
- EXP-591: existe un experimento previo de analisis held-out folio (commit e00b3f8) y un script posterior de variantes creado el mismo dia. El script de variantes no puede usar el identificador 591.
- EXP-592: existe un analisis max-T previo (commits 70db96a y a74cff7).
- EXP-593: script canonico scripts/exp593_daiin_variants.py; ejecucion completada y resultados guardados en research/experiments/2026-10-20-exp593.md y .json. Fuente SHA-256: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc. El identificador aun debe cotejarse con el indice historico completo.

## Resultado validado de EXP-593
- 4.188 lineas parseadas y 32.732 tokens.
- 5.000 permutaciones con semilla 20261021.
- `daiin`: 726 ocurrencias, 133 inicios de linea; p empirico y ajustado reportado 0,000200.
- `dain`: 198 ocurrencias; p ajustado 1,000.
- `daiiin`: 19 ocurrencias; p ajustado 1,000.
- Advertencia: 607 de las 726 ocurrencias de `daiin` quedaron con clase Currier desconocida. No interpretar la comparacion A/B como concluyente. El nulo permuta tokens dentro de cada linea y la señal posicional no demuestra traduccion.

## Siguiente accion
Recuperar el archivo maestro historico y enumerar todos los scripts, informes y JSON EXP-* antes de asignar nuevos numeros. El ultimo identificador libre no esta confirmado todavia.
