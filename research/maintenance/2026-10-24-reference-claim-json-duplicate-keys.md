# Rechazo de claves JSON duplicadas en la adjudicación histórica (24-10-2026)

**Tipo:** corrección de integridad de metadatos, sin EXP nuevo. **Estado inicial:** propuesta en rama; no declarar cierre hasta CI remota y, si se integra, CI posterior de `master`.

## Defecto y reproducción mínima

El arreglo anterior de la PR #25 impedía duplicados entre filas de `readers['cases']` y `identities['excluded_from_new_language_baselines']`, pero el lector `json.loads` seguía aceptando claves repetidas **dentro del mismo objeto JSON**, conservando solo el último valor. Por ejemplo:

```python
import json
json.loads('{"source_commit":"wrong","source_commit":"aa9ec5399e7a5cdf8d1b2890fa657f1358825b41","cases":[]}')
# {'source_commit': 'aa9ec5399e7a5cdf8d1b2890fa657f1358825b41', 'cases': []}
```

Esta demostración se ejecutó localmente en Python en esta intervención. La pérdida de un miembro duplicado impediría auditar la contradicción original. **No se afirma que los snapshots reales tengan tales duplicados**; es un fallo de aceptación de entrada malformada. La PR #25 sigue siendo válida para el defecto distinto de filas duplicadas.

## Corrección y regresiones

- `scripts/audit_reference_claim_links.py`: `load_json_strict` con `object_pairs_hook` rechaza claves JSON repetidas en cualquier nivel. Se aplica a las dos entradas de la adjudicación (lectores e identidades) y al snapshot pasado a `--check`.
- `tests/test_reference_claim_links.py`: tres regresiones: clave `source_commit` contradictoria en la raíz, clave `path` contradictoria en un objeto anidado y snapshot con clave `schema_version` duplicada; el último caso también comprueba JSON válido.
- Las pruebas sintéticas usan `TemporaryDirectory` y se detienen antes de abrir corpus históricos. No se modifica `research/maintenance/2026-10-22-remaining-readers/results.json`, `research/CORPUS_IDENTITY_REVIEW.json`, el snapshot de adjudicación, los scripts históricos ni los corpus.
- No hay aleatoriedad, parámetros de muestreo ni semilla: prueba determinista de rechazo de entrada.

## Alcance y verificación exigida

Base exacta: `master` `054b0cf1835d4a4dcc20e354060c2f50931bc266` (PR #24 integrada). Antes del cambio se revisaron PR abiertas #5, #6, #7 y #13 y no se modificó ninguna de sus ramas. El run posterior a #24 `40080649556` estaba `in_progress` al inicio de esta intervención, por lo que no se ha usado como CI verde.

Ejecutar en Python 3.12:

```sh
python tests/test_reference_claim_links.py
python scripts/audit_reference_claim_links.py --check research/maintenance/2026-10-22-claim-link-adjudication/results.json
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La CI existente `.github/workflows/voynich-check.yml` contiene los controles de referencia y operativos; comprobar el resultado real por SHA de head. No sustituir una entrada histórica y llamarla reproducción. Este cambio no reejecuta simulaciones, no valida los idiomas de los corpus, no certifica IVTFF y no produce traducción.

## Criterio de cierre

1. Tres nuevas regresiones aprobadas, snapshot de adjudicación idéntico bajo JSON válido y controles existentes aprobados en el head exacto de la PR.
2. Comprobar concurrencia y compatibilidad con el `master` vigente antes de integrar.
3. Tras integrar, confirmar CI de `master` sobre el commit de fusión.
4. Si falla cualquier etapa, conservar el fallo y dejar la PR sin fusionar.
