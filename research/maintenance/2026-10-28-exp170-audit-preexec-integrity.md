# EXP-170 — bloqueo de entradas congeladas antes de ejecutar AST histórico (28-10-2026)

**Tipo:** reparación operativa acotada, sin EXP nuevo ni reproducción de las 400 simulaciones. **Estado inicial:** propuesta pendiente de CI e integración. La reproducción histórica exacta sigue **BLOCKED** por la procedencia no acreditada de Naibbe y de las entradas de las ejecuciones originales.

## Defecto y evidencia

`scripts/audit_exp170_archive.py` extraía funciones del script histórico mediante AST y ejecutaba parte de su código para reconstruir el baseline. Hasta esta reparación, calculaba los SHA-256 de script, corpus, vectores e informe **al final** de `audit()`, sin exigir que coincidieran con la identidad congelada **antes** de compilar/ejecutar el bloque AST. `--check` comparaba el snapshot solo después de ejecutar ese bloque. Una alteración accidental del script o de los datos podía, por tanto, influir en la evaluación antes de que el resultado se comparase con el snapshot; un AST alterado podría incluso introducir efectos secundarios. No hay evidencia de alteraciones en los originales.

## Corrección

- `scripts/audit_exp170_archive.py`: referencia independiente `FROZEN_INPUT_SHA256` con cuatro hashes procedentes del snapshot auditado del 22-10-2026; `verify_frozen_inputs()` rechaza archivos ausentes, enlaces simbólicos o discrepancias de bytes **antes de `historical_namespace`**. No se regeneran estos hashes a partir de los inputs sometidos a prueba.
- `tests/test_exp170_archive.py`: prueba positiva de las cuatro identidades y su concordancia con el snapshot, cuatro alteraciones adversariales temporales, y enlace simbólico; se comprueba mediante mock que ninguna variante alterada alcanza la evaluación AST. Los originales se copian a un directorio temporal, nunca se modifican.
- La CI canónica ya ejecuta `python tests/test_exp170_archive.py`, `python -O tests/test_exp170_archive.py` y el cotejo `--check` en ambos modos. No se crea un workflow redundante.

## Identidades congeladas (SHA-256)

- `experiments/exp_170_naibbe_simulation/script.py`: `8fe0f7d153211b320b34ca8543dac1ba029e629c4413c203fb2df0031063721c`.
- `experiments/exp_170_naibbe_simulation/result.md`: `740e9997559a43529391ba29e339bbf955722aa0a1b8302efb451cb66706f354`.
- `experiments/exp_170_naibbe_simulation/data/simulation_results.json`: `c71f7161eb69c6cefa7b7fb6a72c000b6647137200166f331ca920042159e874`.
- `data/transcriptions/eva_zl3b.txt`: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.

Los hashes son los ya publicados en `research/maintenance/2026-10-22-exp170-audit/results.json`; se conservan script histórico, resultados, corpus, parámetros y semillas sin modificación. El estado de los vectores es una **recomputación de estadísticas archivadas**, no una reproducción del cifrador ni una traducción.

## Pruebas de aceptación y límites

```bash
python tests/test_exp170_archive.py
python -O tests/test_exp170_archive.py
python scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json
python -O scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json
python -m unittest discover -s tests -v
```

Requiere CI de PR en el SHA exacto y CI posterior en `master` antes de declarar cierre. La referencia fija solo la identidad de **cuatro archivos de esta auditoría**; no valida la autenticidad histórica, la identificación lingüística del texto etiquetado Latin, la versión Naibbe usada, ni los 624 experimentos. Tampoco protege una ejecución **directa** del script histórico, que sigue pudiendo escribir `simulation_results.json`; esa es una incidencia separada y exige aislamiento sin alterar el script congelado. La adjudicación IVTFF, las PR científicas abiertas y la conciliación de artefactos siguen pendientes.

## Procedencia y concurrencia

Base `master`: `f062d285a1e0caf15c943618038c4d4b775512bf`, CI push `40599239821` (success). Cinco PR científicas abiertas al inicio: #5, #7, #13, #66, #82. Ninguna se modifica. El bloque no ejecuta cifrado, no cambia compromisos científicos ni toca folios reservados. Siguiente paso: verificar CI, fusionar solo si pasa y comprobar de nuevo `master`; después abordar la escritura directa del simulador en un entorno aislado.
