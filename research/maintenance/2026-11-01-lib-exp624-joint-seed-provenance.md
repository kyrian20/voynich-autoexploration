# LIB-EXP-624 — verificar procedencia RNG de las asignaciones conjuntas

**Fecha:** 2026-11-01. **Tipo:** reparación de integridad de la API derivada, sin ejecución de modelos ni experimento lingüístico. **Base de rama:** `master` `9011d4215d644ead15168fed6d8ba74b3386e4b5`. **Estado científico:** `BLOCKED` para puntuación confirmatoria. No se asigna EXP nuevo.

## Incidencia y criterio de aceptación

La API pública `derive_joint_strata(pages, global_rows)` comprobaba que las páginas se particionaran sin duplicados, que no hubiera fuga entre hojas físicas y que las listas de hojas concordaran con las páginas. **No comprobaba que las hojas asignadas fueran las producidas por la semilla declarada**. Un llamante podía permutar hojas completas entre entrenamiento y evaluación, actualizar los campos de hojas y recuentos, mantener todos los invariantes de independencia y obtener un informe que atribuía la asignación adulterada a la semilla original.

Criterio previo: rechazar una asignación sintética sin fuga pero incompatible con su semilla; rechazar semillas no enteras (incluidos booleanos); aceptar asignaciones generadas por el LCG/Fisher–Yates existente y conservar las salidas congeladas de CI. No introducir experimentos científicos nuevos.

## Reparación

- `scripts/prepare_library_exp624_joint_strata.py`: tras los controles de población y fuga, valida el tipo exacto de `seed` y regenera **una** asignación canónica mediante `grouped.grouped_splits(pages, seed, 1)`; compara conjuntos de páginas de entrenamiento y prueba. No altera el generador ni los datos.
- `tests/test_library_exp624_joint_strata.py`: regresión adversarial que intercambia dos hojas físicas completas manteniendo población, estratos, recuentos, conjuntos disjuntos y `seed` original; regresión para semillas cadena, booleano, decimal y nula. Control positivo con asignación real.

El defecto está demostrado por inspección del camino anterior de `derive_joint_strata`; **no se afirma que los JSON congelados contengan asignaciones adulteradas**.

## Entradas, parámetros y preservación

- ZL3b `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Semillas globales `624010 + 7919*i` para `i=0..7`, LCG de 32 bits, Fisher–Yates, corte 70/30 por número de hojas; `625010 + 7919*i` para `i=0..5` sigue siendo la serie separada histórica no apta para combinar estratos.
- No se modifica la política de selección histórica permisiva, las fuentes originales, el archivo de la Biblioteca, el manifiesto prospectivo, los resultados negativos ni `state/committed_claims.md`. Las pruebas sintéticas no usan aleatoriedad nueva.

## Pruebas y evidencia exigida

Comandos previstos en la CI canónica:

```sh
python -m unittest discover -s tests -p 'test_library_exp624_joint_strata.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp624_joint_strata.py' -v
python scripts/prepare_library_exp624_joint_strata.py --out library-exp624-joint-strata.json
sha256sum library-exp624-joint-strata.json > library-exp624-joint-strata.sha256
```

Antes de cerrar: verificar run de PR, SHA de la rama, pasos específicos, run posterior de `master`, y comparar el JSON y hash del artefacto previo y posterior. Un artefacto publicado sin inspección interna no prueba igualdad. La CI general no equivale a validación científica.

## Limitaciones

Esta reparación impide atribuir una partición externa arbitraria a una semilla que no la generó; no recupera una evaluación prospectiva ciega ni rehabilita las 28 particiones históricas con contaminación física. La concordancia IVTFF completa y la procedencia exacta de EXP-170 continúan bloqueadas. No se ejecutó ningún modelo ni se infiere semántica o traducción. Evaluación global: 22-11-2026, sin promesa de descifrado.
