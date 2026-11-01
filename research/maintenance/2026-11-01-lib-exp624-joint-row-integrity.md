# LIB-EXP-624 — rechazo de recibos conjuntos no canónicos y semillas repetidas

**Fecha:** 2026-11-01. **Clase:** reparación acotada de integridad, no experimento lingüístico. **Base:** `master` `f8096a4f45d79a7176b1921faddd5f800ffdd1e1`. **Estado científico:** `BLOCKED` para puntuaciones confirmatorias; no se asigna EXP nuevo.

## Incidencia y criterio previo

La reparación anterior de `derive_joint_strata(pages, global_rows)` (PR #218) ya exigía disjunción por hoja y coincidencia de los **conjuntos** de páginas con la semilla. Sin embargo, un consumidor externo podía aportar un recibo con recuentos falsos, hojas duplicadas o páginas reordenadas y obtener una derivación aparentemente aceptada. Además, dos filas con la misma semilla se admitían como repeticiones distintas. Como el LCG reduce las semillas módulo `2**32`, `624010` y `624010 + 2**32` producen el mismo flujo y tampoco deben presentarse como semillas independientes.

**Criterio falsable:** aceptar los recibos originales generados por el LCG/Fisher–Yates, rechazar una mutación adversarial de cualquiera de sus campos canónicos aunque la pertenencia train/test sea correcta, rechazar semillas repetidas o fuera del rango entero sin signo de 32 bits, y no modificar el JSON derivado de los corpus congelados.

## Código y pruebas

- `scripts/prepare_library_exp624_joint_strata.py`: verifica tipo y rango de cada semilla, unicidad dentro de `global_rows` y coincidencia **exacta** de `train_leaves`, `test_leaves`, `train_page_ids`, `test_page_ids`, `train_page_count` y `test_page_count` con el recibo regenerado desde la misma semilla. Rechaza recuentos booleanos o no enteros. No cambia el algoritmo generador.
- `tests/test_library_exp624_joint_strata.py`: dos regresiones adversariales con duplicación de hoja, reordenación de páginas, recuentos falsos, booleanos, repetición de semilla y alias módulo `2**32`. Control positivo con el recibo original y prueba preexistente con los dos corpus congelados.
- No se modifica `grouped_splits`, el lector histórico ni el contrato de las ocho semillas canónicas. La API de derivación admite semillas externas **únicas** dentro del rango LCG; no se interpreta una repetición como réplica independiente.

## Fuentes y parámetros inmutables

- ZL3b: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Biblioteca LIB-EXP-624, script histórico SHA-256 `1f00846ab8e91cefd07bc2dcd26ad12cf8a7c4bc7b2478d480afec391a13f3a9`, resultados `d6e1b7490e563c96367ff10ab56feb5487d6b2775a885494f249c89f87bd4bab`, informe `7de18cce59ea21598af7958a7ded3e05b03e305e8a6cc84c0740917b807447c4`.
- LCG 32 bits / Fisher–Yates; `seed_base=624010`, `seed_step=7919`, `repetitions=8`, 70/30 por hoja física. 203 páginas elegibles; 114 A, 81 B, 8 sin clase bajo lector permisivo histórico.

## Reproducción y límites

```sh
python -m unittest discover -s tests -p 'test_library_exp624_joint_strata.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp624_joint_strata.py' -v
python scripts/prepare_library_exp624_joint_strata.py --out library-exp624-joint-strata.json
sha256sum library-exp624-joint-strata.json
```

La CI de la PR y, si se integra, la de `master` deben comprobarse **después** de ejecutar, incluyendo artefactos; no se anticipa aquí su éxito. La salida canónica debería permanecer idéntica porque los ocho recibos válidos no cambian; esto requiere comparación de bytes y SHA-256, no solo tamaños.

**Autoauditoría:** no hay calibración semántica ni manipulación de tokens; el control positivo es la asignación original, los controles adversariales son recibos sintéticos malformados. El resultado negativo esperado es su rechazo; no prueba que los históricos hayan sufrido estas alteraciones. La conformidad IVTFF integral, los resultados históricos con fuga física, la procedencia exacta de EXP-170 y la conciliación global siguen pendientes. No se reejecuta ningún modelo ni se rehabilitan puntuaciones. Los folios reservados permanecen intactos. Evaluación: 22-11-2026, sin promesa de descifrado.
