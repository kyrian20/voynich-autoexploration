# Registro de numeracion de experimentos

Actualizado: 2026-10-20.

## Regla
Los identificadores EXP son unicos. Las fases, los experimentos y las ejecuciones de Actions son series distintas. Un reintento no crea un EXP nuevo. No borrar resultados antiguos: registrar conflictos y conservar los artefactos.

## Conflictos conocidos
- EXP-590: los archivos creados el 20-10-2026 pueden colisionar con numeracion previa; no asumir que sean el EXP-590 historico.
- EXP-591: existe un experimento previo de analisis held-out folio (commit e00b3f8) y un script posterior de variantes creado el mismo dia. El script de variantes no puede usar el identificador 591.
- EXP-592: existe un analisis max-T previo (commits 70db96a y a74cff7).
- EXP-593: script de variantes reasignado: scripts/exp593_daiin_variants.py. Aun debe verificarse contra el indice historico completo.

## Siguiente accion
Recuperar el archivo maestro historico y enumerar todos los scripts, informes y JSON EXP-* antes de asignar nuevos numeros. El ultimo identificador libre no esta confirmado todavia.
