# LIB-EXP-624 — guardia de clase Currier por página entre ediciones

**Fecha:** 2026-11-01. **Tipo:** reparación de integridad; no experimento de descifrado. **Base:** `master` `aae15e276138fef1b3be476eed14fb75d187dafd`. **Estado científico:** `BLOCKED` para puntuaciones confirmatorias. No se asigna EXP.

## Incidencia y criterio de aceptación previo

`prepare_library_exp624_leaf_grouped_splits.build()` exigía 203 páginas elegibles en cada edición, 114 A / 81 B, igualdad de IDs y de hojas train/test, **pero no igualdad de la clase `$L` de cada página**. Dos páginas podían intercambiar A/B en una edición manteniendo idénticos los totales y las hojas asignadas. Esto habría permitido derivar estratos desde ZL3b y atribuirlos implícitamente también a IT2a sin verificar su concordancia página a página.

**Criterio:** rechazar un intercambio adversarial A/B de dos páginas de IT2a aunque se mantengan los hashes de los bytes congelados, los 203 IDs y los totales 114/81; aceptar los dos corpus originales; conservar las salidas y semillas originales y no ejecutar ningún clasificador.

## Corrección

- `scripts/prepare_library_exp624_leaf_grouped_splits.py`: conserva en memoria el mapa `id -> lang` de cada proyección del lector histórico y exige identidad exacta ZL3b/IT2a después de comprobar la identidad de IDs. No normaliza ni escribe corpus; el mapa es transitorio y no altera el JSON público.
- `tests/test_library_exp624_leaf_grouped_splits.py`: nueva regresión con `unittest.mock.patch.object` sobre el lector de IT2a. Intercambia dos etiquetas A/B **solo en memoria**; los bytes de las dos fuentes y sus hashes permanecen intactos. Los recuentos globales son iguales, pero la guardia debe rechazar la diferencia por página. La prueba existente sobre ambos corpus originales sirve de control positivo.

## Fuentes y reproducibilidad

- ZL3b `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Scripts originales y resultados históricos LIB-EXP-624 permanecen congelados; consultar `research/maintenance/2026-11-01-lib-exp624-joint-strata-leaf-gate.md` para sus hashes.
- Asignación derivada sin cambios: LCG 32 bits, Fisher–Yates, `seed_base=624010`, incremento `7919`, 8 repeticiones, corte 70/30 por hoja; A/B separados `seed_base=625010`, 6 repeticiones. Ninguna aleatoriedad en la nueva regresión.

Comandos de prueba desde la raíz con Python 3.12:

```sh
python -m unittest tests.test_library_exp624_leaf_grouped_splits -v
python -O -m unittest tests.test_library_exp624_leaf_grouped_splits -v
python -m unittest tests.test_library_exp624_joint_strata -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

## Evidencia y límites

Una comprobación de lectura independiente de ambas fuentes originales con la selección permisiva histórica encontró 203 IDs elegibles y clases A=114, B=81, sin clasificar=8 en cada edición; **cero diferencias de clase por ID**. Esto no es una adjudicación IVTFF ni una verificación del lector estricto. La regresión sintética demuestra una guardia que faltaba, **no** un error de clasificación observado en los originales.

La CI de la PR y la posterior a integración deben verificarse por SHA y artefactos antes de declarar cierre. No se alteran corpus, particiones prospectivas, resultados negativos, puntuaciones históricas, registros de compromisos ni etiquetas de idioma. Las 28 particiones históricas contaminadas siguen `INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY`. EXP-170, conformidad IVTFF completa y conciliación de artefactos continúan pendientes. La fecha del 22-11-2026 es evaluación, no promesa de descifrado.
