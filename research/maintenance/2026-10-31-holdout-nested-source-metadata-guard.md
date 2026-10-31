# Holdout físico: puerta de esquema para metadatos anidados de corpus

**Fecha:** 2026-10-31. **Tipo:** corrección de integridad operativa, sin EXP nuevo ni ensayo lingüístico. **Base examinada:** `master` `ad21fa5819783b6f9cc5085fdff16949510759a7`. **Estado científico:** partición propuesta, no validación semántica ni históricamente ciega.

## Defecto y aceptación falsable

`scripts/audit_holdout_locus_coverage.py::audit` exigía un conjunto exacto de claves **en el nivel superior** del manifiesto y verificaba `path`, `sha256` y `leaf_count` en cada corpus. Sin embargo, aceptaba claves adicionales dentro de `corpora.<edición>`. Una copia sintética del manifiesto podía introducir `corpora.eva_zl3b.txt.semantic_validation=true` y seguir superando la auditoría sin alterar hashes, recuentos ni asignación de folios. La aceptación de ese campo desconocido no acreditaba una validación científica; sí constituía un defecto de la puerta de integridad del manifiesto congelado.

**Criterio fijado antes de CI:** cada registro de corpus debe ser un objeto con exactamente `path`, `sha256` y `leaf_count`. Rechazar campo extra, ausencia de `sha256` o registro que no sea un objeto, mediante `ValueError`. El manifiesto original debe seguir aprobando, con **102 hojas compartidas** (68 entrenamiento, 16 desarrollo, 18 prueba). La salida JSON de cobertura y el crosswalk congelado no deben cambiar.

## Código, regresiones y reproducción

- `scripts/audit_holdout_locus_coverage.py`: valida el esquema anidado antes de leer atributos de procedencia.
- `tests/test_holdout_manifest_contract.py`: tres casos sintéticos adversariales, además del control positivo existente.
- `.github/workflows/voynich-check.yml`: ejecuta el contrato también con Python optimizado `-O`.

Comandos de aceptación (Python 3.12):

```sh
python -m unittest discover -s tests -p 'test_holdout_manifest_contract.py' -v
python -O -m unittest discover -s tests -p 'test_holdout_manifest_contract.py' -v
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python scripts/audit_holdout_locus_coverage.py --out /tmp/holdout-coverage-guard-new.json
python scripts/audit_holdout_page_crosswalk.py --out /tmp/holdout-crosswalk-guard-new.json
cmp research/maintenance/2026-10-25-holdout-page-crosswalk/results.json /tmp/holdout-crosswalk-guard-new.json
```

La CI canónica también ejecuta las auditorías generales y publica artefactos. **No atribuir éxito a estas comprobaciones hasta consultar el run exacto y sus logs**; el informe documenta criterios y cambios, no resultados anticipados. El fallo de la versión previa se deriva de la ausencia de una comparación de claves anidadas y de los casos sintéticos especificados; no se ha demostrado adulteración de los datos originales.

## Identidades y límites

Manifiesto congelado: `research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json` (Git blob `84f59008a190df7481c4e81a5c84c3916d79a59d`). ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. Sal de partición `VOYNICH-FUTURE-RULES-2026-10-23-v1`; no se genera ni cambia ninguna semilla.

No se leen tokens reservados para seleccionar hipótesis; las transcripciones son dos ediciones del mismo manuscrito. Ninguna hoja se vuelve históricamente ciega: la advertencia de exposición previa sigue vigente. No se ejecutan simulaciones Naibbe ni ciclos científicos bloqueados. Los corpus, manifiestos, resultados negativos, archivos históricos, semillas, compromisos humanos y `state/committed_claims.md` permanecen sin modificación.

**Pendientes separados:** procedencia exacta de EXP-170, conformidad completa IVTFF, conciliación intersuperficies de artefactos y evaluación semántica independiente. Fecha objetivo de evaluación: 22-11-2026, sin promesa de descifrado.
