# Incidencia: claves JSON duplicadas en la carga del manifiesto holdout v2

Fecha: 27-10-2026. Estado de esta propuesta: **corrección publicada en rama; verificación CI pendiente**. Sin EXP nuevo y sin experimento lingüístico.

## Defecto verificable y alcance

Antes de este cambio, tanto `scripts/audit_holdout_locus_coverage.py::main` como `scripts/audit_holdout_page_crosswalk.py::main` leían el manifiesto mediante `json.loads` sin `object_pairs_hook`. Python conserva silenciosamente la última de dos claves repetidas. Por ejemplo, `{"salt":"wrong","salt":"correct"}` se interpreta como una sola asignación; el miembro anterior desaparece de la representación usada por los auditores. Lo mismo puede ocurrir en `partitions.train`, `counts.test` o en un hash de `corpora`. Una auditoría de procedencia no debe aceptar una entrada JSON ambigua, incluso cuando el valor final satisface las invariantes.

**No hay evidencia de que el manifiesto congelado actual contenga claves duplicadas.** La CI ya compara su regeneración byte a byte: esta reparación es una defensa adicional en los dos consumidores del manifiesto, no una denuncia de manipulación histórica. El patrón de fallo de JSON duplicado ya se había reparado en otro lector (`research/maintenance/2026-10-24-reference-claim-json-duplicate-keys.md`); esta incidencia se limita a los dos lectores del holdout, que seguían utilizando `json.loads` permisivo.

## Corrección y regresión

Se añade `load_manifest(path)` en el auditor de cobertura, con `object_pairs_hook` que rechaza la primera clave repetida en cualquier profundidad; el auditor de correspondencias entre páginas utiliza el mismo lector. El workflow `Voynich Check` ejecuta ahora explícitamente la nueva regresión en su paso de auditoría de cobertura, además de los controles existentes. Se mantiene `audit(source_bytes, manifest)` para pruebas de diccionarios ya construidos: no puede detectar claves JSON que un llamador haya descartado previamente. Los consumidores CLI son la superficie protegida.

La nueva prueba `tests/test_holdout_manifest_json_integrity.py` contiene cuatro entradas sintéticas adversariales (sal repetida, grupo train repetido, SHA anidado repetido y clave idéntica repetida) y un control positivo del manifiesto v2 congelado (102 hojas, sal histórica). Sin aleatoriedad: **semilla no aplicable**. No se alteran las asignaciones de train/desarrollo/test ni se leen sus tokens para seleccionar reglas.

## Procedencia y verificación

Base exacta: `master` `c3a16c21b675848fac1ac96ada874d91ad73227d`. La CI de esa base: [40425106965](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40425106965), `success` (comprobada antes de abrir la rama). PR abiertas observadas antes del cambio: #5, #7, #13, #66 y #82; no se modifican.

Comandos exigidos en la CI de la propuesta (la suite global no está incluida en este workflow y no debe darse por ejecutada):

```sh
python -m unittest discover -s tests -p 'test_holdout_manifest_json_integrity.py' -v
python scripts/audit_holdout_locus_coverage.py --out /tmp/holdout-locus-coverage.json
python scripts/audit_holdout_page_crosswalk.py --out /tmp/holdout-page-crosswalk.json
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

Las transcripciones congeladas mantienen sus SHA-256 **publicados** en `research/CORPUS_INPUT_MANIFEST.json`: ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` e IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. Esos hashes son referencias archivadas, no nuevos cálculos locales en este bloque. Los scripts y pruebas se conservan en commits Git; la CI deberá aportar los logs, SHA exacto y artefactos antes de cerrar la incidencia.

## Limitaciones y siguiente paso

El rechazo de claves duplicadas es integridad de metadatos, no conformidad completa IVTFF, independencia histórica de los folios ni validación semántica. No se modifican corpus originales, manifiestos v1/v2, resultados negativos, scripts históricos ni `state/committed_claims.md`. Tampoco se ejecuta un ciclo científico mientras persistan bloqueos de adjudicación. Si la CI pasa, revisar diff y concurrencia, fusionar solo tras verificar el head, y comprobar la CI posterior de `master`. Si falla, conservar el fallo y reparar su causa concreta. Después, priorizar la adjudicación IVTFF y la procedencia de comparadores antes de pruebas confirmatorias.
