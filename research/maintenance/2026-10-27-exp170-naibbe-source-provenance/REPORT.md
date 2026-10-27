# Recuperación de procedencia de Naibbe para EXP-170 — 27-10-2026

**Estado: fuentes públicas localizadas; reproducción histórica todavía BLOQUEADA.** Esta comprobación documental no es un EXP ni valida las salidas archivadas. No se ejecutó el cifrador y no se modifican corpus, manifiestos, semillas, particiones, resultados históricos ni `state/committed_claims.md`.

## Hallazgos comprobados

1. El [repositorio oficial de Michael Greshko](https://github.com/greshko/naibbe-cipher) conserva `naibbe_v2.py` y el input `input/examples/divina_commedia.txt`. El segundo ocupa exactamente la ruta relativa que espera `experiments/exp_170_naibbe_simulation/script.py`; esa ruta no existe en el checkout actual de este proyecto.
2. La copia vendorizada `experiments/common_battery_2026_10_22/vendor/naibbe_v2.py` coincide línea por línea con el archivo de la rama pública `main`. Ambos archivos comparten el Git blob SHA-1 `b566ad82e4b6ff0782ecdddebf77718dac44f292`. Esto identifica la copia actual, pero no acredita qué commit había en el checkout local de EXP-170.
3. El historial público de `naibbe_v2.py` comienza en el commit `b17f1cefdd3be2e1ec3428dd9344da61b7e57677` (16-09-2025). En esa versión `USE_78_CARD_DECK` tenía valor predeterminado `False`; el commit `cd24d1d819b71bc690e0d26bb3736b9cbfe2e7a1`, del mismo día, lo cambió a `True`. La copia actual conserva el valor `True`. El informe de EXP-170 declara una baraja de 78 cartas, pero no registra el SHA del checkout ni permite inferir con certeza qué versión/configuración generó cada salida.
4. El input público `divina_commedia.txt` existe en el upstream (Git blob SHA-1 `2f57181cca66ab61d8719e35778d6b06688ee8be`). El proyecto no conserva actualmente una copia en la ruta esperada ni un SHA-256 histórico que permita demostrar identidad byte a byte con la entrada usada en 2026.
5. El artículo revisado por pares de Greshko remite sus materiales suplementarios y datasets a [Zenodo 16415087](https://doi.org/10.5281/zenodo.16415087) y el código Python al repositorio anterior. Su publicación es *Cryptologia* (2025), DOI [10.1080/01611194.2025.2566408](https://doi.org/10.1080/01611194.2025.2566408).

## Consecuencia para EXP-170

La fuente y el texto italiano ya no están perdidos en términos de disponibilidad pública. Sin embargo, su recuperación no basta para reproducir el experimento histórico: faltan el commit exacto de Naibbe, los hashes de las entradas exactas y el estado de las semillas/salidas por réplica. El informe previo documenta además que el JSON archivado solo contiene métricas y no tokens cifrados, denominadores ni semillas por registro. Por tanto, EXP-170 sigue **BLOQUEADO para reproducción histórica exacta**.

La copia vendorizada se identifica como igual al upstream público actual, no como «la dependencia histórica recuperada». Una ejecución futura con los recursos actuales deberá etiquetarse como reconstrucción moderna salvo que se establezca la identidad histórica. No se sustituye la dependencia de Naibbe por otra implementación.

## Próximos pasos seguros

- Buscar en artefactos y registros históricos una referencia al commit del upstream y a los hashes de los dos corpus de entrada.
- Si no existe esa evidencia, preparar una reconstrucción separada y claramente etiquetada, congelando commit, archivos, SHA-256, versión de Python, parámetros, semillas y comandos antes de ejecutarla.
- Mantener toda nueva salida en una ruta nueva; nunca sobrescribir `experiments/exp_170_naibbe_simulation/data/simulation_results.json` ni reinterpretar como reproducción los vectores ya auditados.

## Alcance de esta comprobación

Se inspeccionaron `SOUL.md`, `CLAUDE.md`, la norma de integridad, el código e informe de EXP-170, el informe de auditoría previo y el upstream oficial. No se ejecutaron pruebas, simulaciones ni CI local. No se cambió ningún artefacto experimental. La conformidad IVTFF independiente y la conciliación global de artefactos siguen pendientes.
