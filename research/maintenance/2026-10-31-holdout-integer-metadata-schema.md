# Holdout v2 — alias numéricos no enteros en metadatos congelados

**Fecha:** 2026-10-31. **Tipo:** reparación acotada de esquema e integridad; no EXP ni ensayo semántico. **Base de rama:** `master` `8c2094f816ad8597f2d6aca76aec8c3a070f35b6`. **Estado científico:** holdout prospectivo, previamente expuesto; no validación ciega.

## Defecto concreto y prueba falsable

El auditor `scripts/audit_holdout_locus_coverage.py::audit` exigía valores iguales a los recuentos y versión esperados, pero no su tipo JSON. En Python, `2.0 == 2` y `102.0 == 102`; por ello una copia del manifiesto con `schema_version: 2.0`, `corpora.eva_zl3b.txt.leaf_count: 102.0`, `counts.train: 68.0` o `eligible_count: 102.0` superaba las comparaciones de igualdad. La forma numérica del esquema congelado no estaba protegida. Es un defecto de validación de **metadatos**, no una alteración de folios ni una prueba de corrupción histórica.

**Criterio de aceptación:** los campos citados deben ser exactamente enteros Python (`type(x) is int`), lo que rechaza también `bool`. Los listados `source_only_leaves` deben ser listas de enteros exactos. El manifiesto v2 original y los corpus congelados deben seguir pasando, sin cambiar la salida del crosswalk.

## Corrección y regresión

Se añaden comprobaciones de tipo antes de la comparación de versión, recuentos por corpus, recuentos por partición, total elegible y listas de hojas exclusivas. La regresión en `tests/test_holdout_manifest_contract.py` cambia **solo metadatos sintéticos en memoria** en cuatro subcasos (2.0, 102.0, 68.0 y 102.0) y exige `ValueError`; el control positivo original ya existe. Esos cuatro casos habrían pasado las igualdades antiguas; el test los detecta después del arreglo.

La CI ya ejecuta este fichero de pruebas en Python normal y optimizado; no se modifica el workflow. Comandos de aceptación:

```sh
python -m unittest discover -s tests -p 'test_holdout_manifest_contract.py' -v
python -O -m unittest discover -s tests -p 'test_holdout_manifest_contract.py' -v
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python scripts/audit_holdout_locus_coverage.py --out holdout-locus-coverage.json
python scripts/audit_holdout_page_crosswalk.py --out holdout-page-crosswalk.json
cmp research/maintenance/2026-10-25-holdout-page-crosswalk/results.json holdout-page-crosswalk.json
```

**La evidencia de ejecución depende de la CI del SHA de la PR y de la CI posterior de `master`.** No declarar estas pruebas superadas antes de inspeccionar los runs y sus logs.

## Identidades y límites

Fuentes originales congeladas: ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. Manifiesto v2 blob Git `84f59008a190df7481c4e81a5c84c3916d79a59d`; asignación original 68/16/18 de 102 hojas físicas, sal `VOYNICH-FUTURE-RULES-2026-10-23-v1`. No se alteran fuentes, manifiesto, sal, semillas, resultados, hallazgos, claims humanos ni particiones. No se leen tokens de prueba para escoger reglas. Semilla nueva: no aplica. La nueva regresión es determinista y no genera datos científicos.

**Pendientes no resueltos:** EXP-170 requiere bytes y commit originales de Naibbe, corpus italiano y recibos individuales; la conformidad IVTFF no está adjudicada completamente; la conciliación Biblioteca/GitHub y las PR científicas #7 y #138 siguen abiertas. Esta corrección no aporta significado lingüístico ni traducción. Evaluación prevista: 2026-11-22, sin promesa de desciframiento.
