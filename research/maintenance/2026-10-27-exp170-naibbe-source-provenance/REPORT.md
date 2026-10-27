# Recuperación de procedencia de Naibbe para EXP-170 — 27-10-2026

**Estado: fuentes públicas localizadas; reproducción histórica todavía BLOQUEADA.** Esta comprobación documental no es un EXP ni valida las salidas archivadas. No se ejecutó el cifrador y no se modifican corpus, manifiestos, semillas, particiones, resultados históricos ni `state/committed_claims.md`.

## Hallazgos comprobados

1. El [repositorio oficial de Michael Greshko](https://github.com/greshko/naibbe-cipher) conserva `naibbe_v2.py` y el input `input/examples/divina_commedia.txt`. Este texto ocupa exactamente la ruta relativa que espera `experiments/exp_170_naibbe_simulation/script.py`; esa ruta no existe en el checkout actual de este proyecto.
2. La copia vendorizada `experiments/common_battery_2026_10_22/vendor/naibbe_v2.py` coincide línea por línea con el archivo de la rama pública `main`. Ambos archivos comparten el Git blob SHA-1 `b566ad82e4b6ff0782ecdddebf77718dac44f292`. Esto identifica la copia actual, pero no acredita qué commit había en el checkout local de EXP-170.
3. El historial público del archivo empieza con `b17f1cefdd3be2e1ec3428dd9344da61b7e57677` (16-09-2025). Allí `USE_78_CARD_DECK` tenía valor predeterminado `False`; el commit `cd24d1d819b71bc690e0d26bb3736b9cbfe2e7a1`, del mismo día, lo cambió a `True`. **En EXP-170 ambos protocolos llaman explícitamente a `encrypt_naibbe(..., use_78=True)`**, así que esa diferencia de valor predeterminado queda anulada por el script. La comparación de esos snapshots solo mostró además cambios en comentarios de licencia/cita. Sigue sin estar fijado el commit exacto que se usó históricamente.
4. El input italiano público existe en el upstream (Git blob SHA-1 `2f57181cca66ab61d8719e35778d6b06688ee8be`), pero no está en la ruta del proyecto ni tiene un SHA-256 histórico registrado. El input del otro protocolo, `data/reference_corpora/latin/vulgate.txt`, sí está fijado por el manifiesto actual (5.650.501 bytes; SHA-256 `d63b1b81824e259b1cf92ba8a6e5cbbf783e2a83214cf2c3db2ecd1459165bfe`). La auditoría previa advierte que el archivo identificado como “Latin” corresponde a inglés Douay-Rheims; por tanto, el hash congela bytes, no valida la identidad lingüística ni acredita por sí solo qué bytes leyó la ejecución histórica.
5. El script fija una fórmula determinista de semillas por réplica y protocolo; no es correcto decir que las semillas sean desconocidas. Sin embargo, el JSON archivado solo conserva métricas, no los tokens cifrados ni un recibo por réplica que vincule semilla, éxito/fallo e inputs. El [informe de auditoría de EXP-170](../2026-10-22-exp170-audit/REPORT.md) detalla estos límites y los errores corregidos de la tabla histórica.
6. El artículo revisado por pares de Greshko remite los materiales suplementarios y datasets a [Zenodo 16415087](https://doi.org/10.5281/zenodo.16415087) y el código Python al repositorio anterior. Publicado en *Cryptologia* (2025), DOI [10.1080/01611194.2025.2566408](https://doi.org/10.1080/01611194.2025.2566408).

## Consecuencia para EXP-170

La fuente y el texto italiano ya no están perdidos en términos de disponibilidad pública. Su recuperación no demuestra identidad byte a byte con los recursos históricos ni permite vincular los vectores archivados a cada semilla y ejecución. La copia vendorizada se identifica como igual al upstream público actual, no como «la dependencia histórica recuperada». Por tanto, EXP-170 sigue **BLOQUEADO para reproducción histórica exacta**.

Una ejecución con los recursos actuales deberá etiquetarse como reconstrucción moderna salvo que se establezca la identidad histórica. No se sustituye la dependencia de Naibbe por otra implementación.

## Próximos pasos seguros

- Buscar en artefactos y registros históricos el commit de Naibbe, el input italiano exacto y cualquier log por réplica.
- Si no existe esa evidencia, preparar una reconstrucción separada y claramente etiquetada, congelando commit, archivos, SHA-256, versión de Python, parámetros, semillas y comandos antes de ejecutarla.
- Mantener toda nueva salida en una ruta nueva; nunca sobrescribir `experiments/exp_170_naibbe_simulation/data/simulation_results.json` ni reinterpretar como reproducción los vectores ya auditados.

## Alcance de esta comprobación

Se inspeccionaron `SOUL.md`, `CLAUDE.md`, la norma de integridad, el código e informe de EXP-170, el informe de auditoría previo, el manifiesto de corpus y el upstream oficial. No se ejecutaron pruebas, simulaciones ni CI local. No se cambió ningún artefacto experimental. La conformidad IVTFF independiente y la conciliación global de artefactos siguen pendientes.
