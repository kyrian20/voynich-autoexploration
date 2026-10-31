# Integridad del comparador genérico de snapshots JSON — 31-10-2026

**Clase:** reparación operativa de un defecto concreto, sin EXP nuevo ni prueba semántica. **Base comprobada antes de la rama:** `master` `e1d4297fdec1668cbfb92f9cdd546666d871a61c`. **Estado de aceptación inicial:** PENDIENTE de ejecutar y verificar CI exacta; este documento no afirma éxito de ejecución.

## Defecto y alcance

`scripts/check_audit_snapshot.py` se usa para comparar salidas regeneradas contra snapshots científicos congelados. Su lectura con `json.load` sin `object_pairs_hook` descartaba silenciosamente claves repetidas, conservando el último valor. Un archivo sintético `{"n":1,"n":1}` se interpretaba como `{"n":1}` y superaba una comparación contra `{"n":1}`. También podía ocurrir en objetos anidados, en el archivo esperado **o** en el regenerado. Esto impide tratar una coincidencia como garantía de integridad del JSON de entrada. No se ha demostrado que los snapshots históricos contengan tales claves.

## Reparación falsable

- Se introduce `load_snapshot` con `object_pairs_hook=reject_duplicate_keys` para ambos lados; toda repetición, incluso de valor idéntico, debe producir `ValueError`.
- `parse_constant=reject_nonstandard_constant` rechaza explícitamente `NaN`, `Infinity` y `-Infinity` en la lectura; el comparador ya exigía floats finitos, pero ahora el contrato de JSON es inequívoco desde el parser.
- La función `compare` y sus tolerancias numéricas **no cambian**. Se conservan las estructuras, los enteros exactos y los floats finitos con tolerancia 1e-12.
- `tests/test_audit_snapshot_json_integrity.py` aporta siete casos sintéticos: duplicados en ambos lados, duplicado anidado en lista, constantes no estándar, coincidencia positiva y rechazo de tipos distintos. Se incorporan a `.github/workflows/voynich-check.yml` con Python normal y optimizado.

## Criterios de aceptación

1. `python -m unittest discover -s tests -p 'test_audit_snapshot_json_integrity.py' -v` y la misma orden con `python -O`, ambas sin fallos.
2. El paso nuevo y los comparadores existentes de `Voynich Check` deben pasar en el **SHA exacto** de la rama, con logs revisados; no basta un estado general antiguo.
3. Revisar el estado de `master`, las PR concurrentes y la base antes de fusionar. Tras una eventual fusión, comprobar la CI push del SHA resultante.
4. Ningún snapshot original, corpus, manifiesto de holdout, resultado histórico, semilla, hash fijado o afirmación comprometida se modifica.

## Limitaciones y siguientes asuntos

El fallo está demostrado por el comportamiento del parser estándar y los casos sintéticos; no implica que una cifra científica histórica sea errónea. La CI del comparador comprueba **igualdad de salida**, no independencia de lectores, corrección de algoritmos ni autenticidad de inputs externos. EXP-170 continúa bloqueado para reproducción histórica por falta de identidad exacta de recursos Naibbe/italianos; siguen pendientes la adjudicación IVTFF, los artefactos y la revisión de PR #7 y #138. No se asignan significados EVA ni se ejecuta ningún experimento en folios reservados. Evaluación global prevista para 22-11-2026, sin promesa de descifrado.
