# EXP-601 — Errata sobre unidad de bootstrap y leave-one-out (2026-10-28)

**Estado: INVALID_FOR_CLAIM**, limitado a describir el intervalo bootstrap y el leave-one-out históricos como pruebas de robustez por **hoja física completa**.

El programa original agrupa por el identificador de **cara o panel** de la transcripción, no por hoja física numerada. El resultado congelado incluye 81 unidades de remuestreo correspondientes a 40 hojas numeradas; algunas hojas aportan cuatro paneles. No se recalculó el intervalo por hoja física. Conservar sin cambios `script.py`, `results.json`, `result.md` y `README.md` como fuentes históricas, pero no reutilizar su redacción de «folio-clustered» como si garantizara conglomerados físicos completos.

**No retirado:** recuento descriptivo de inicios de `daiin`, expectativa bajo inventario de línea y p histórico del nulo de posición uniforme dentro de línea, cada uno con sus limitaciones originales. **No demostrado:** si un intervalo nuevo por hojas físicas completas excluye 1.

[Auditor, hashes, identidades, regresiones y límites](../../research/maintenance/2026-10-28-exp601-physical-leaf-bootstrap-scope.md).
