# Guardia del reparto congelado antes del piloto visual — 27-10-2026

**Tipo:** corrección operativa de integridad y prevención de fuga de folios; sin EXP nuevo, sin análisis de palabras ni validación semántica. **Estado:** propuesta en rama; no declarar cerrada hasta CI de PR y verificación posterior a fusión.

## Defecto identificable y riesgo

`scripts/select_visual_pilot_v2.py` leía el manifiesto v2 con `json.loads` y su función `build` comprobaba recuentos, solapamientos e identidad declarada de fuentes, pero **no recalculaba la asignación individual por SHA-256 y sal histórica congelada**. Un manifiesto manipulado que intercambiase una hoja de `train` por otra de `test`, conservando los tamaños y los hashes de transcripción, superaba esas comprobaciones de recuento. La selección de un piloto visual podía así usar una hoja reservada como entrenamiento. No se ha demostrado que el manifiesto archivado esté manipulado: se trata de una vulnerabilidad de aceptación reproducible mediante un caso sintético.

La auditoría `scripts/audit_holdout_locus_coverage.py` ya corregida en trabajos anteriores (PR #87 y #90) **sí** comprueba el reparto individual, la sal, el contrato científico y los hashes reales. No se duplica su algoritmo.

## Corrección acotada

La entrada de línea de comandos del piloto ahora llama a `load_verified_frozen_manifest`, que lee el JSON con la protección existente contra claves duplicadas, obtiene los bytes de ambas transcripciones originales y ejecuta `audit_frozen_holdout` **antes** de seleccionar hojas. Si cualquier asignación, contrato, hash o cobertura no coincide, aborta sin generar selección. Se preserva la función `build` para fixtures sintéticos sin manifiesto congelado: invocarla aisladamente **no sustituye** esta guardia de entrada.

La CI ejecuta `tests/test_visual_pilot_frozen_manifest.py` antes de regenerar y comparar el piloto archivado. Las cuatro pruebas verifican: manifiesto original válido; intercambio de hojas train/test manteniendo recuentos; claves JSON duplicadas; y hash de fuente falsificado. Las pruebas solo escriben manifiestos temporales.

## Datos y reproducción

- Base inicial de rama: `4286c4846e1a0f3dbd64313a7d793c62bde01d3e` (`master`).
- Manifiesto congelado: `research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json`; Git blob `84f59008a190df7481c4e81a5c84c3916d79a59d`.
- ZL3b SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Reparto original: 68 entrenamiento, 16 desarrollo, 18 prueba; 102 hojas físicas compartidas.
- Ejecución determinista: sin semilla aleatoria, sin optimización ni inspección de resultados de test.

Comandos a comprobar en CI:
```sh
python -m unittest discover -s tests -p 'test_visual_pilot_frozen_manifest.py' -v
python -m unittest discover -s tests -p 'test_visual_annotation_queue.py' -v
python scripts/select_visual_pilot_v2.py --out /tmp/pilot-selection-v2.json
cmp research/decipherment/2026-10-25-visual-annotation/pilot-selection-v2.json /tmp/pilot-selection-v2.json
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

## Límites y siguiente decisión

Esta guardia protege **la entrada del CLI del piloto visual**, no todas las llamadas directas a `build`, ni todos los consumidores del manifiesto. El holdout no es históricamente ciego: sus folios fueron examinados antes. El control solo prueba integridad de particiones y procedencia de bytes; no adjudica IVTFF completo, no aporta anotaciones visuales independientes ni significados EVA. Las transcripciones, particiones, resultados históricos, scripts originales de otros experimentos y `state/committed_claims.md` no se modifican.

Tras verificar CI y la comparación exacta del piloto, comprobar concurrencia y `master` antes de fusionar; después verificar CI de `master`. Continuar con conformidad IVTFF independiente y procedencia histórica, sin activar el experimento semántico bloqueado.
