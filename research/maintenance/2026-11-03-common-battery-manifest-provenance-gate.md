# Batería común run-03 — integridad del manifiesto y alcance del recibo (2026-11-03)

**Tipo:** reparación operativa y de procedencia. **No** nuevo EXP, ejecución científica, recuperación de datos bloqueados ni traducción.

## Defecto reproducible antes de la reparación

`scripts/verify_common_battery_reconstruction.py` aceptaba cualquier manifiesto JSON no vacío aportado por el llamador y devolvía `EXACT_HISTORICAL_HASH_MATCH`. Por ejemplo, un manifiesto sintético con una sola entrada arbitraria y un archivo con hash coincidente recibía el mismo estado que los cuatro archivos históricos run-03. También aceptaba enlaces simbólicos a archivos externos cuyos bytes coincidiesen con el hash; un manifiesto con claves duplicadas se interpretaba silenciosamente con la última clave. Ninguna de estas situaciones prueba la identidad de la ejecución histórica.

## Cambio acotado

- Fijar el SHA-256 del manifiesto **original** `experiments/common_battery_2026_10_22/data/run-03/SHA256.json`: `f5e8d316e7e0712ef9cfbc20be158eef5159aca9daf4bfc4f254b96ebc95bf8b` (348 bytes, salto de línea final). La ruta canónica solo puede emitir `EXACT_HISTORICAL_HASH_MATCH` si coincide el manifiesto y están presentes sus cuatro nombres históricos.
- Los manifiestos de pruebas proporcionados explícitamente pueden comprobar bytes, pero emiten el estado diferenciado `SUPPLIED_MANIFEST_HASH_MATCH` y `historical_manifest_pinned=false`.
- Rechazar claves JSON duplicadas, manifiestos vacíos o de tipo incorrecto, SHA-256 no canónicos, rutas con separadores y archivos o componentes de ruta enlazados simbólicamente. Mantener `FileNotFoundError` para archivos ausentes.
- Añadir ocho regresiones al archivo `tests/test_common_battery.py`; el contrato anterior de manifiesto sintético se ajusta al estado honesto. La CI canónica ya ejecuta este archivo tras reconstruir run-03 con Python 3.12.14 y dependencias fijadas.

## Evidencia y pruebas

- Demostración sintética previa en Python 3: un manifiesto de un solo archivo y un archivo simbólico ambos producían `EXACT_HISTORICAL_HASH_MATCH` con el código antiguo. No implica que el archivo histórico real estuviese alterado.
- Prototipo aislado de la reparación: siete pruebas locales superadas en modo normal y con `python -O`, compilación Python correcta; no equivale a ejecutar toda la suite de este repositorio.
- **Verificación de GitHub:** consultar la CI de la PR y la ejecución de `master` posterior a la fusión antes de declarar el cierre. Este documento no anticipa sus resultados.

## Preservación, límites y siguientes pasos

Se mantienen sin modificar los cuatro hashes de salida archivados, el manifiesto original, las fuentes, el script científico congelado, semillas, parámetros, logs históricos, corpus y particiones reservadas. Los archivos de datos crudos no autorizados siguen ausentes del repositorio público; la CI puede reconstruirlos temporalmente, pero el hash coincidente no demuestra por sí solo que se recuperaran los bytes del entorno histórico original. La verificación de hashes tampoco acredita que el programa se haya ejecutado: exige un recibo independiente de ejecución para esa afirmación.

Persisten el bloqueo de procedencia de entradas externas de EXP-170, la conformidad IVTFF integral y la conciliación general de artefactos. No se asignan nuevos significados ni se desbloquean experimentos prohibidos por contradicciones. Próximo paso: verificar el run exacto de CI de esta rama, revisar conflictos y decidir fusión solo con evidencia; después, verificar el nuevo `master`.
