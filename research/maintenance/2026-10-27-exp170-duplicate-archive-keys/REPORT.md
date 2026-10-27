# EXP-170 — fail closed ante claves JSON y filas de tabla duplicadas (27-10-2026)

**Alcance:** corrección del auditor retrospectivo, no reproducción de las 400 simulaciones históricas ni nuevo experimento. EXP-170 continúa **BLOCKED** para reproducción exacta por la procedencia de la dependencia Naibbe y las entradas históricas; véase [procedencia](../2026-10-27-exp170-naibbe-source-provenance/REPORT.md).

## Defecto concreto

En `scripts/audit_exp170_archive.py`, `json.loads` aceptaba claves repetidas y conservaba silenciosamente la última aparición, incluso dentro de un vector de métricas. De forma análoga, `report_tables` sobrescribía una métrica o un recuento si su fila aparecía dos veces. El lector de recuentos también aceptaba menos columnas de las cuatro condiciones esperadas por usar `zip` sin validar su anchura. En esas situaciones, el auditor podía afirmar una conciliación sobre un documento ambiguo o incompleto.

No hay evidencia en esta revisión de que los archivos originales contengan tales duplicados. El defecto afecta a la **capacidad de detección** de entradas alteradas, no demuestra corrupción de los resultados congelados.

## Reparación acotada

- `parse_archive` usa `object_pairs_hook` para rechazar claves repetidas en cualquier profundidad del JSON, antes de validar los 400 vectores.
- `report_tables` rechaza métricas y filas de recuentos duplicadas, y exige cuatro valores en cada fila de recuentos.
- `tests/test_exp170_archive.py` añade cinco regresiones: duplicado de métrica, duplicado de recuento, recuento truncado, claves JSON duplicadas a dos profundidades y aceptación del JSON histórico sin modificar.
- El resultado del auditor debe seguir coincidiendo exactamente con `research/maintenance/2026-10-22-exp170-audit/results.json`. Esa prueba existente impide cambiar silenciosamente la tabla o el diagnóstico.

## Inmutabilidad y procedencia

No se modifican `experiments/exp_170_naibbe_simulation/script.py`, `result.md`, `data/simulation_results.json`, los corpus ni el snapshot auditado. Sus SHA-256 archivados son, respectivamente:

- Script histórico: `8fe0f7d153211b320b34ca8543dac1ba029e629c4413c203fb2df0031063721c`.
- Informe histórico: `740e9997559a43529391ba29e339bbf955722aa0a1b8302efb451cb66706f354`.
- Vectores históricos: `c71f7161eb69c6cefa7b7fb6a72c000b6647137200166f331ca920042159e874`.
- EVA ZL3b: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.

Estas huellas proceden del snapshot auditado; su conservación en la rama y la ejecución de las regresiones deben confirmarse en CI, sin confundir el mero registro con una nueva verificación criptográfica.

## Comprobaciones de aceptación

```bash
python -m unittest discover -s tests -p 'test_exp170_archive.py' -v
python scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json
python -m unittest discover -s tests -v
```

La ejecución remota y el commit exacto deben quedar enlazados en la PR. No se ejecuta el cifrador ni se regeneran los 400 vectores.

## Límites y siguiente paso

Una validación sintáctica y de unicidad de entradas no acredita que los corpus estén correctamente identificados ni que los vectores procedan de las semillas y dependencias originales. Mantener EXP-170 bloqueado para reproducción histórica y seguir buscando recibos, hashes y versiones originales. No usar este cambio para rehabilitar afirmaciones generales sobre clases de cifrados ni para declarar desciframiento.
