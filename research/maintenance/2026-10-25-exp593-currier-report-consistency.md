# EXP-593 — conciliación de tablas Currier JSON/Markdown (25-10-2026)

**Alcance:** reparación de integridad del archivador, sin nuevo EXP ni simulación. Estado de la reparación y evidencias de CI: consultar la solicitud de integración de esta rama.

## Defecto reproducible

En la versión de `master` `735a519fc4e820817b478638354839793a20d452`, `archive_result_complete` comprueba la procedencia, los agregados `observed` y la fila-resumen del informe, pero **no** comprueba que las filas por clase Currier del informe Markdown coincidan con `observed[word].by_currier` en JSON. Un cambio sintético de la clave de clase `A` a `B`, sin modificar recuentos agregados, podía ser aceptado como un archivo existente y activar `skipped_existing` sin advertir la contradicción entre artefactos.

## Reparación acotada

- `scripts/exp593_daiin_variants.py`: para cada variante se exige una sección Currier única y una coincidencia exacta del multiconjunto de filas de clase, recuentos, inicios y finales con el JSON. Se rechazan filas ausentes, repetidas o inesperadas. Se conserva la comprobación previa de la tabla-resumen.
- `tests/test_exp593_archive_guard.py`: el informe sintético de prueba ahora contiene las tablas por clase, y se añaden tres regresiones: clase distinta con agregados idénticos, fila ausente y fila duplicada.
- La comprobación de compatibilidad con los dos archivos históricos fechados el 21-10-2026 sigue siendo obligatoria; no se regeneran ni editan esos archivos.

## Reproducción y límites

Comando específico: `python -m unittest discover -s tests -p 'test_exp593_archive_guard.py' -v`. La CI canónica `Voynich Check` ejecuta esa prueba y los demás controles. Los fixtures son deterministas y no usan semilla; el EXP-593 histórico mantiene semilla `20261021`, 5.000 permutaciones y fuente SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.

Esto detecta **inconsistencias estructurales entre los dos archivos**, no recalcula las permutaciones, no autentica la fuente ni certifica la interpretación estadística. La comprobación de igualdad de filas tampoco constituye una traducción ni resuelve la conformidad IVTFF. Se mantienen los resultados negativos y los originales congelados. La CI de la rama y de un eventual commit de integración deben comprobarse por separado.
