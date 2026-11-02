# EXP-593 — rechazo de claves JSON duplicadas (2026-11-02)

**Estado de esta intervención:** corrección de integridad de archivo, no EXP nuevo ni reproducción numérica.

## Incidencia y evidencia estática

En `scripts/exp593_daiin_variants.py`, `archive_status()` utilizaba
`json.loads(...)` sin `object_pairs_hook`. Python conserva silenciosamente
la última aparición de una clave repetida. Por tanto, un JSON archivado con
`"experiment"` duplicado o con un campo `"occurrences"` duplicado dentro de
`observed` podía superar la comprobación de consistencia como si hubiera una
sola interpretación de sus datos. No se ha demostrado que ningún archivo
histórico real contenga este defecto.

## Reparación y pruebas falsables

Se incorpora `_unique_json_pairs()` para rechazar duplicados a **cualquier
profundidad**, antes de examinar los campos de procedencia y estadísticas.
La lectura captura `ValueError` y falla cerrada; no reescribe el archivo.

`tests/test_exp593_archive_guard.py` incluye dos casos sintéticos:
duplicación idéntica de `experiment` en el nivel superior y duplicación
contradictoria de `occurrences` dentro de `observed.daiin`.
El resultado esperado de ambos es `RuntimeError` con diagnóstico de
lectura ambigua; con el lector antiguo se aceptarían como un solo valor.
El test preexistente sobre el archivo congelado de 2026-10-21 debe continuar
pasando. Se exige ejecución tanto normal como `python -O`.

Comandos reproducibles desde la raíz:

```bash
python -m unittest discover -s tests -p 'test_exp593_archive_guard.py' -v
python -O -m unittest discover -s tests -p 'test_exp593_archive_guard.py' -v
```

## Preservación y límites

No se modifican los corpus EVA, los resultados archivados de EXP-593,
las semillas (20261021), el número de permutaciones (5000), el código
estadístico ni los folios reservados. No se ejecutan simulaciones.
Esta intervención solo protege la interpretación de los archivos al
comprobar si se puede omitir una reproducción; no demuestra que las cifras
históricas sean correctas, ni resuelve la adjudicación IVTFF, las entradas
externas de EXP-170, ni la conciliación global de artefactos.

**CI y fusión:** verificar en la PR y en el run posterior de `master`;
no considerar el informe una certificación por sí mismo.

**Siguiente paso:** continuar la adjudicación de entradas históricas de
EXP-170 con hashes y procedencia verificables, sin reconstrucciones
sustitutivas presentadas como reproducción original.
