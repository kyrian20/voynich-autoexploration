# LIB-EXP-624 — impedir alias de semillas en la asignación por hoja

**Fecha:** 2026-11-01. **Clase:** reparación operativa acotada de reproducibilidad; no experimento de descifrado. **Base:** `master` `76a66eddf214f97889eb04803d5c7b1491974128`. **Estado científico:** `BLOCKED` para puntuación confirmatoria. Sin nuevo ID EXP.

## Incidencia y criterio previo

`scripts/prepare_library_exp624_leaf_grouped_splits.py::grouped_splits` registraba `seed_base + 7919*i` sin validar tipo, rango ni desbordamiento. El LCG histórico reduce internamente `seed & 0xffffffff`; por ello las semillas `624010` y `624010 + 2**32` generan exactamente la misma permutación y podían emitirse con recibos que aparentaban semillas distintas. La API de derivación conjunta ya rechazaba alias, pero el generador de origen no. Este defecto de contrato se detectó en el código, no en los ocho recibos canónicos.

**Criterio falsable antes de CI:** aceptar las series originales `624010 + 7919*i` (8) y `625010 + 7919*i` (6), rechazar semillas de tipo no entero (incluido `bool`), fuera de `[0, 2**32)`, repeticiones de tipo no entero o vacías, y series cuyo último elemento alcance `2**32`; conservar byte a byte los JSON de los corpus congelados.

## Corrección y regresión

- `scripts/prepare_library_exp624_leaf_grouped_splits.py`: valida `seed_base` y `repetitions` con tipo exacto `int`, el rango de la primera semilla y el último valor de la serie, antes de construir asignaciones. No cambia el LCG ni el barajado Fisher–Yates.
- `tests/test_library_exp624_leaf_grouped_splits.py`: caso adversarial de alias módulo `2**32`, semillas y repeticiones mal tipadas, límites negativos y superiores, desbordamiento del último elemento y control positivo en `2**32-1`. Permanecen las regresiones de independencia física, identidades de página y los corpus congelados.

## Fuentes y parámetros conservados

- ZL3b: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Biblioteca LIB-EXP-624: script histórico SHA-256 `1f00846ab8e91cefd07bc2dcd26ad12cf8a7c4bc7b2478d480afec391a13f3a9`, resultados `d6e1b7490e563c96367ff10ab56feb5487d6b2775a885494f249c89f87bd4bab`, informe `7de18cce59ea21598af7958a7ded3e05b03e305e8a6cc84c0740917b807447c4`.
- Serie global: `seed_base=624010`, paso `7919`, 8 repeticiones; A/B: `625010`, paso `7919`, 6 repeticiones. Corte 70/30 por hoja física. No se reentrena modelo ni se modifica ningún corpus, partición prospectiva o resultado histórico.

## Reproducción y criterio de cierre

```sh
python -m unittest discover -s tests -p 'test_library_exp624_leaf_grouped_splits.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp624_leaf_grouped_splits.py' -v
python scripts/prepare_library_exp624_leaf_grouped_splits.py --out library-exp624-grouped-allocation.json
sha256sum library-exp624-grouped-allocation.json
```

**Evidencia pendiente al redactar:** confirmar CI del commit de la PR, su ejecución específica y artefactos; comparar el JSON resultante con el de `master` previo a esta corrección. No inferir igualdad por tamaños ni afirmar éxito antes de descargar y comprobar bytes. Tras la integración, comprobar CI de `master` actual, no de una PR histórica.

## Autoauditoría y límites

- **Target-awareness:** no se calibra ningún parámetro con métricas Voynich; se valida el dominio del LCG.
- **Feature-destroying:** no se transforman tokens, páginas ni orden canónico; la corrección afecta solo a entradas no canónicas.
- **Extrapolación:** se protege este generador, no todos los scripts históricos que utilicen RNG.
- **Resultado negativo:** el rechazo adversarial no demuestra que los archivos históricos estén alterados.
- **Control:** el LCG original produce exactamente la misma permutación con semillas separadas por `2**32`; la regresión debe rechazar la segunda y aceptar las semillas canónicas.

Continúan bloqueadas las puntuaciones de LIB-EXP-624 para independencia por hoja histórica, la adjudicación IVTFF integral, la procedencia exacta de EXP-170 y la conciliación global. Sin traducción validada. Fecha de evaluación: **22-11-2026**, sin promesa de descifrado.
