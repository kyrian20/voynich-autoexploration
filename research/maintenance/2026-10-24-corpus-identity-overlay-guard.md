# Puerta de identidad de corpus históricos — 24-10-2026

**Tipo:** corrección de integridad y trazabilidad, sin EXP nuevo. **Base revisada:** `master` `3ade29294582f42ad0d8a5d4e28a58c21b886b26`. **Estado:** parche en rama; CI remota pendiente de verificación antes de considerar la incidencia cerrada.

## Defecto y alcance

`scripts/check_corpus_integrity.py` ya congelaba bytes, tamaños y rutas de corpus. Sin embargo, el fichero de exclusiones `research/CORPUS_IDENTITY_REVIEW.json` no tenía una puerta propia en el workflow principal. Una modificación de su etiqueta de idioma, tipo de incidencia, evidencia o eliminación de una fila podía pasar los controles de integridad de bytes, aunque esos bytes fueran idénticos. Esto debilita la exclusión de controles incorrectamente identificados.

Se añaden `scripts/audit_corpus_identity_overlay.py`, `tests/test_corpus_identity_overlay.py` y un paso en `.github/workflows/voynich-check.yml`. No se modifica la identidad histórica archivada ni se sustituyen corpus.

## Criterios y pruebas

El auditor exige que las seis exclusiones históricas sigan presentes con la misma clase de incidencia, que sus tamaños y SHA-256 coincidan con el manifiesto congelado y con los bytes leídos, y que las pruebas documentales consignadas existan en el corpus correspondiente. Las cabeceras declaradas se buscan en las primeras 120 líneas; las otras citas, como subcadenas literales del texto. Rechaza cambios de la condición `PENDING_SCOPE_AUDIT_NOT_AUTOMATICALLY_RETRACTED`, filas duplicadas, rutas ajenas, enlaces simbólicos y pérdida de cuarentena del corpus vacío.

Las diez regresiones sintéticas (semilla: no aplica) incluyen caso positivo, hash alterado, fila duplicada, cabecera y cita inventadas, cambio de estado histórico, ruta ajena, corpus vacío, symlink, exclusión eliminada y cambio de clasificación. Ejecutadas localmente sobre fixtures temporales con Python 3.13: **10/10 aprobadas**. No se declara con ello que se hayan ejecutado sobre los corpus originales; el paso remoto del workflow lo comprobará.

Comandos de verificación en el repositorio:

```sh
python -m unittest discover -s tests -p 'test_corpus_identity_overlay.py' -v
python scripts/audit_corpus_identity_overlay.py
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

## Límites y siguiente acción

Esta puerta valida **consistencia documental**, no identifica idiomas de forma independiente, no determina la proporción de latín/inglés en Cicerón, no demuestra que los resultados antiguos usaran esos bytes, ni reproduce experimentos. Los seis corpus conservan sus hashes y estado previo. La clasificación de los demás corpus, las entradas históricas exactas de Naibbe, la adjudicación IVTFF completa y la conciliación de resultados siguen pendientes.

Tras verificar la CI de la PR y, si se integra, una ejecución **push** nueva de `master`, continuar la trazabilidad de las afirmaciones históricas afectadas sin reinterpretar resultados congelados ni ejecutar experimentos prohibidos por contradicciones.
