# EXP-607 — corrección de alcance del holdout físico (28-10-2026)

**Estado para la afirmación de generalización a hojas físicas enteramente no vistas: INVALID_FOR_CLAIM.**

El script histórico [script.py](script.py) aplica SHA-256 y módulo 5 al identificador de **cara** (por ejemplo, f5r o f5v), no a la hoja física (f5). En consecuencia, las dos caras de una misma hoja pueden quedar en grupos diferentes. El informe original [result.md](result.md) y los resultados [results.json](results.json) se conservan sin modificaciones, incluidas las ganancias positivas y el control barajado.

La reconstrucción de elegibilidad y particiones, sin entrenar ni puntuar tokens, identifica 28 hojas físicas compartidas en ZL3b y 27 en IT2a. La evidencia, sus hashes, los límites de inferencia y las pruebas se encuentran en [la adjudicación de EXP-607](../../research/maintenance/2026-10-28-exp607-physical-leaf-leakage.md). Esta corrección no cuantifica cuánto afecta la contaminación a las puntuaciones históricas ni niega que pueda existir estructura local.

No utilizar el resultado histórico como confirmación independiente sobre hojas físicas reservadas. Las comparaciones de sensibilidad posteriores que reutilizan el mismo reparto tampoco convierten ese conjunto en un holdout físico. Una nueva evaluación requiere una partición agrupada por hoja, reglas fijadas antes de observar las nuevas hojas y controles adversariales. No reescribir los resultados históricos ni reutilizar sus folios test como material ciego.
