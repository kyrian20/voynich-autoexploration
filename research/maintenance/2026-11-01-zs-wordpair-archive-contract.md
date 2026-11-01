# Zhang–Sheng: reparar el contrato de salida y reproducir un subconjunto congelado

**Fecha:** 2026-11-01. **Clase:** defecto de reproducibilidad del paquete de auditoría, sin nuevo EXP ni inferencia científica. **Base inspeccionada:** `master` `1fd2750ee1f51f89cb074f0c511e1a8e32ccc2a6`. **Estado:** reparación propuesta; verificar CI y fusión antes de marcar cierre.

## Incidencia reproducible por inspección del código y del archivo

`research/maintenance/2026-11-01-zs-wordpair-audit/results.json` contiene exactamente 54 registros bajo la clave `run_records` (2 transcripciones × 3 vistas × 3 tamaños de vocabulario × 3 semillas). Sin embargo, la función `main()` de `wordpair_audit.py` en la base imprimía una clave `results` con un objeto anidado. Por ello, el comando de reproducción publicado en el informe original **no producía un artefacto con el mismo contrato JSON que el archivo archivado**. La CI de la base solo probaba el bloqueo de fuentes; **no recalculaba ni una fila** de las correlaciones del archivo.

La inspección estática demuestra la incompatibilidad del contrato, **no** demuestra que los 54 valores numéricos estén equivocados. El resultado archivado y su informe permanecen congelados.

## Reparación acotada y criterio falsable

1. `wordpair_audit.py` incorpora `flatten_run_records()` y ahora emite la estructura `status/sources/run_records` del archivo congelado. No cambia el cálculo de métricas, la selección, el lector, las semillas ni los controles.
2. `tests/test_zs_wordpair_archive_contract.py` comprueba la estructura de los 54 registros, combinaciones únicas, campos, finitud y recibos de fuente; prueba la conversión de un registro a su esquema archivado.
3. El test **recalcula dos filas fijadas antes de mirar su resultado**, una de ZL3b y otra de IT2a: vista `split`, 150 tipos, semilla `20261101`, 20 barajados, páginas comunes y categorías P/C/R. Compara todos los enteros y etiquetas exactamente y las tres correlaciones con tolerancia absoluta de 1e-9.
4. La CI instala NumPy `2.2.6`, ejecuta el test y archiva el log y su SHA-256. Un desajuste en cualquiera de las dos filas **hace fallar** la PR; no se ajusta el archivo congelado para pasar.

**Fuentes fijadas (SHA-256):**
- ZL3b: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

**Reproducción acotada:**
```bash
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -k test_archive_grid_and_source_receipts -v
```

## Límites de cierre

- El test reproduce **solo 2 de 54 filas** y comprueba el contrato/estructura de las 54; no constituye una reproducción completa del archivo.
- La salida del comando completo pasa a ser estructuralmente compatible con el archivo; no se afirma identidad byte a byte de la salida completa sin ejecutar y comparar los 54 cálculos.
- Los 52 registros restantes, el valor de correlación publicado por Zhang–Sheng y la fórmula de corrección de propensión del artículo siguen **sin reproducción independiente acreditada**. Los 2 registros tampoco validan el método del preprint: son un control de nuestra propia reimplementación.
- ZL3b e IT2a son lecturas del mismo manuscrito, no muestras independientes. No se ejecutan ciclos de descifrado, ni se atribuyen significados.
- No se modifican corpus, resultados históricos, manifiestos de folios reservados, `state/committed_claims.md`, ni el archivo `results.json`.

**Siguiente paso:** tras comprobar la CI de la PR y del `master` fusionado, decidir si la reproducción completa de las 54 filas merece una ejecución separada con tiempo y memoria registrados, antes de citar el archivo como `REPRODUCED`. Mantener EXP-170 como `BLOCKED` para la reconstrucción histórica exacta hasta recuperar sus entradas acreditadas. Fecha de evaluación: 22-11-2026, sin garantía de descifrado.
