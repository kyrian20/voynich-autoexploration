# Incidencia: contrato de uso científico del holdout v2 no protegido

Fecha: 2026-10-27. **Tipo:** reparación de integridad de metadatos, sin EXP nuevo ni traducción. **Estado al publicar la rama:** propuesta pendiente de CI; no declarar cierre hasta comprobar la ejecución y, si se fusiona, el push de master.

## Defecto y reproducción conceptual

El auditor `scripts/audit_holdout_locus_coverage.py::audit` validaba SHA-256 de los corpus, sal, hojas, grupos y conteos, pero **no validaba** campos esenciales para interpretar el experimento: `status`, `caveat`, `forbidden`, `unit`, `allocation`, `selection`, `supersedes` y `correction`. Una modificación del manifiesto congelado de `status=PROPOSED_FOR_FUTURE_RULES` a `status=VALIDATED`, o la supresión de la advertencia de que las hojas ya habían sido examinadas, podía atravesar esa auditoría si no se cambiaban las asignaciones. Esto no altera los datos, pero permitiría atribuir indebidamente evidencia semántica o independencia histórica a un split que no las posee.

No hay evidencia de que el manifiesto original contenga tales cambios. Esta incidencia no es la de claves JSON duplicadas ya reparada en PR #90: aquí el JSON es sintácticamente inequívoco, pero el contrato científico podía cambiar silenciosamente.

## Corrección

Se fija `FROZEN_CONTRACT` en el auditor, independiente del archivo JSON y del generador. Se comprueban exactamente los campos declarativos, el conjunto completo de claves y los nombres de grupos en `counts` y de ediciones en `source_only_leaves`. Se mantienen las verificaciones anteriores de sal, asignación por SHA-256, cobertura, hashes de corpus y registros. Los tests sintéticos anteriores se completan con los metadatos correctos, sin relajar la puerta.

Se añaden 11 regresiones en `tests/test_holdout_manifest_contract.py`: un control positivo con las transcripciones congeladas y diez alteraciones adversariales de metadatos. El workflow `Voynich Check` ejecuta explícitamente esas pruebas. Las mutaciones se realizan únicamente en copias en memoria; los corpus, manifiestos v1/v2 y resultados históricos permanecen intactos. No hay aleatoriedad: semilla no aplicable.

## Procedencia y verificación

Base comprobada antes de crear la rama: `master` `c3751e065380e9a2f12e6334299b50241c733d11`. CI push de esa base: [40431010741](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40431010741), `completed/success`. Las PR abiertas entonces eran #5, #7, #13, #66 y #82. La PR #90 ya estaba fusionada. No se modifica ninguna de ellas.

Fuentes históricas publicadas en `research/CORPUS_INPUT_MANIFEST.json`, que el auditor compara con bytes leídos: ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. Estos son **hashes archivados**, no nuevos cálculos independientes en esta sesión.

Verificación esperada en CI, no atribuida a la rama antes de consultar sus logs:

```sh
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python -m unittest discover -s tests -p 'test_holdout_manifest_json_integrity.py' -v
python -m unittest discover -s tests -p 'test_holdout_manifest_contract.py' -v
python scripts/audit_holdout_locus_coverage.py --out holdout-locus-coverage.json
python -m unittest discover -s tests -p 'test_holdout_page_crosswalk.py' -v
python scripts/audit_holdout_page_crosswalk.py --out holdout-page-crosswalk.json
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

## Límites

Esta puerta evita que un manifiesto numéricamente consistente cambie de significado científico. No prueba conformidad IVTFF completa, ausencia histórica de exposición de los folios, reproducibilidad de resultados previos ni traducción. No se ejecuta un ciclo científico por los bloqueos metodológicos y de corpus pendientes. La suite `tests/` no sustituye la revisión de los cientos de experimentos históricos.

## Siguiente acción

Comprobar la CI del SHA exacto de esta rama y sus artefactos. Si falla, conservar el log y reparar el defecto concreto; si pasa, revisar diff y concurrencia, integrar y verificar la nueva CI push de `master`. Después retomar adjudicación IVTFF y trazabilidad de los comparadores históricos, sin reutilizar resultados inválidos para afirmaciones por lengua.
