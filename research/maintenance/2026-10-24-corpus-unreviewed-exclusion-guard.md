# Auditoría de exclusiones: rechazar séptima entrada no adjudicada — 24-10-2026

**Tipo:** reparación de integridad de procedencia, sin EXP nuevo ni experimento de descifrado.  
**Base fijada:** `master` `143be8cd4665b0d042729d7cf06679c5f7abef29`.  
**Estado:** cambio propuesto; su integración requiere CI del commit de la PR y posterior verificación de `master`.

## Defecto acotado

El auditor `scripts/audit_corpus_identity_overlay.py` exigía que las seis rutas históricas `EXPECTED_ISSUES` siguieran presentes y con su adjudicación, pero **no rechazaba una exclusión adicional** si su ruta ya figuraba en el manifiesto congelado. Una séptima fila con hash, tamaño, evidencia textual, etiqueta de problema y lengua internamente coherentes podía pasar todas las comprobaciones. Esto permitiría añadir silenciosamente una exclusión a las bases lingüísticas sin revisión de procedencia ni decisión científica.

El defecto se deduce del recorrido anterior: tras comprobar que la ruta estaba en `frozen`, el auditor solo fijaba `issue` y `adjudicated_work` **si** `name in EXPECTED_ISSUES`/`EXPECTED_WORKS`. No se ha identificado tal séptima fila en el overlay real; el problema es una puerta insuficiente, no una alteración histórica observada.

## Reparación y regresión

La auditoría rechaza con `Unreviewed corpus exclusion` toda fila adicional presente en el manifiesto pero ausente del conjunto explícitamente adjudicado. Las seis rutas ya aprobadas siguen siendo obligatorias. Una futura exclusión legítima requiere revisar evidencia y actualizar deliberadamente el mapa de adjudicaciones y sus pruebas, no copiar una etiqueta válida.

La regresión `test_unreviewed_manifest_backed_exclusion_is_rejected` añade una séptima ruta sintética `latin/virgil_aeneid_latin.txt`, con bytes no vacíos, cabecera inglesa, hash SHA-256 calculado, tamaño coincidente, entrada de manifiesto y una etiqueta `WRONG_LANGUAGE_FOR_LATIN` que ya era válida. **La etiqueta es deliberadamente sintética; no adjudica ni caracteriza la obra real de Virgilio.** El resultado exigido es rechazo por falta de revisión, incluso cuando las demás comprobaciones pasan.

**Aleatoriedad:** ninguna; semilla no aplicable. **Entradas:** solo fixture temporal en la regresión; corpus originales inmutables. **Parámetros:** mapa `EXPECTED_ISSUES` y overlay congelado de seis filas. **Criterio de aceptación:** regresión rechaza la séptima fila; suite existente y auditor sobre los seis corpus reales terminan con código 0.

## Comprobaciones y archivo

```sh
python -m unittest discover -s tests -p 'test_corpus_identity_overlay.py' -v
python scripts/audit_corpus_identity_overlay.py
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

`.github/workflows/voynich-check.yml` ya invoca tanto el módulo de regresiones como el auditor real; no es necesario añadir un workflow o disparar ciclos redundantes. Verificar la ejecución exacta de la PR y el run posterior de `master` antes de afirmar integración completa.

Los hashes de los seis corpus y sus tamaños permanecen en `research/CORPUS_INPUT_MANIFEST.json`, las adjudicaciones en `research/CORPUS_IDENTITY_REVIEW.json`; ambos se conservan sin cambios. La PR y sus runs conservan commits, logs y resultados de regresión. No se modifica `state/committed_claims.md`, ninguna transcripción, experimento o resultado histórico.

## Límites científicos

El control fija la **lista de exclusiones documentadas**; no verifica por sí mismo las identidades de todas las obras, la pureza lingüística, la exactitud de los corpus históricos usados por cada EXP ni la validez de una comparación Voynich/latín. No se ha realizado prueba semántica, evaluación de folios reservados ni traducción. Los bloqueos IVTFF, EXP-170 y revisión de PR #7 continúan abiertos.
