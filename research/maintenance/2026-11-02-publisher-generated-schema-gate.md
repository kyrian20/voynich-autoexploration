# Publicador: contrato mínimo de identidad y esquema de artefactos concurrentes

**Fecha:** 2026-11-02. **Base:** `b2c0a485034f16a61beaf41086f991c154b86a26`.
**Tipo:** reparación operativa de integridad, sin EXP nuevo y sin nueva inferencia científica.

## Defecto y prueba falsable

La reparación de la PR #251 rechazaba blobs vacíos, JSON sintácticamente
inválido, claves duplicadas y números no finitos, pero aún aceptaba
`{}` o `{"value":2}` como resultado de EXP-590, EXP-593, EXP-622 o EXP-623
si el nombre del archivo y el modo Git coincidían. Esos objetos no contienen
identidad del experimento, procedencia del corpus ni medidas que permitan
interpretar el resultado. El publicador podía por ello rebasar sobre un
artefacto concurrente incompleto tratándolo como una adición inocua.

**Criterio previo a la verificación:** rechazar el JSON vacío, identidad
equivocada, fuente/hash de corpus equivocados, limitaciones ausentes,
conteos negativos o booleanos, resultados de variantes incompletos y
probabilidades fuera de [0,1]. Aceptar los cuatro JSON reales ya
publicados y conservar el rechazo de blobs inválidos de la PR #251.

## Corrección

`scripts/check_publisher_source_drift.py` aplica un contrato **mínimo
específico** para cada uno de los cuatro generadores, únicamente a los
nuevos JSON permitidos en un rebase. Verifica el ID y tipo del experimento,
la transcripción y SHA-256 fijados, las limitaciones y campos estructurales
básicos. Para EXP-590 comprueba recuentos y parámetros/permutación;
para EXP-593 comprueba la correspondencia entre variantes, observaciones
y pruebas; para EXP-622/623 comprueba recuentos, excedencias, probabilidad,
interacción e interpretación. No altera los generadores ni los JSON
congelados y conserva el examen del blob del commit candidato, no el
árbol de trabajo.

Las pruebas sintéticas de `tests/test_publisher_source_drift.py`
incluyen rechazos adversariales y un control positivo con los cuatro
JSON publicados bajo `research/experiments/`. El control positivo
depende deliberadamente de los artefactos reales versionados, no de
inventar un esquema complaciente.

## Comprobación

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

Las ejecuciones remotas y el commit exacto deben verificarse en Actions
antes de declarar que las regresiones pasan; este documento no es por sí
solo un certificado de CI.

## Límites y conservación

Es una barrera contra artefactos estructuralmente ajenos a los cuatro
generadores, **no** una reproducción de sus cálculos, un validador
estadístico completo ni una prueba de que sus p-valores sean correctos.
No comprueba todos los invariantes internos ni que los outputs correspondan
a la ejecución histórica; el hash de fuente es un contrato de corpus, no
un recibo de ejecución. No demuestra que un objeto vacío se publicase
realmente en master. Los corpus, salidas históricas, semillas, particiones
reservadas y resultados negativos permanecen intactos.

Siguen bloqueados la procedencia histórica de EXP-170, la adjudicación
IVTFF integral y la conciliación general de artefactos. No se ejecutan
ciclos científicos prohibidos ni se asignan significados a tokens.
