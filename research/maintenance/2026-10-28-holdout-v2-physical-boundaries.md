# Corrección de integridad del holdout v2 — límites físicos IVTFF (28-10-2026)

**Estado:** reparación propuesta; verificar CI del SHA exacto antes de fusionar. No es un EXP nuevo ni un experimento semántico.

## Incidencia reproducible

El generador de particiones por hoja `scripts/prepare_prospective_leaf_holdout_v2.py` leía cabeceras mediante `str.splitlines()`. Python reconoce como separadores caracteres de control y Unicode que **no son delimitadores físicos CR, LF o CRLF del archivo IVTFF**. Por ejemplo, el texto sintético `<f1r> valid\n<!editor\u2028<f2r> forged\n` produce dos cabeceras aparentes (`f1r` y `f2r`) con el lector anterior, aunque `f2r` no comienza una fila física. Esto podía incorporar una hoja ficticia a las particiones train/development/test y falsear el manifiesto si una fuente cambiaba o estaba dañada.

La reproducción es una **inyección sintética**: no se afirma que el corpus congelado contenga esa secuencia. No se han examinado folios reservados ni ajustado reglas con resultados del conjunto test.

## Reparación

- Sustituir `splitlines()` por `checked_physical_lines` del módulo ya existente `scripts/ivtff_physical_rows.py`: solo CR, LF y CRLF definen filas; los ocho separadores no físicos conocidos provocan `ValueError` con número de fila, sin asignar una hoja.
- Añadir dos regresiones a `tests/test_prospective_leaf_holdout_v2.py`: rechazo de los ocho separadores (incluidos U+2028 y U+2029) y aceptación de CR, LF y CRLF.
- Conservar inalterados `scripts/prepare_prospective_leaf_holdout.py` (v1), `manifest.json` (v1), `manifest-v2.json`, las transcripciones y todos los resultados históricos. El contrato de v2 y la sal de asignación siguen idénticos.

## Validación exigida

1. `python -m unittest discover -s tests -p 'test_prospective_leaf_holdout_v2.py' -v`.
2. `python scripts/prepare_prospective_leaf_holdout_v2.py --out prospective-leaf-holdout-v2.json`.
3. `cmp research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json prospective-leaf-holdout-v2.json`.
4. Comprobar la CI `Voynich Check` de la PR y del commit de `master` posterior a fusión. Los pasos 1–3 ya forman parte del workflow existente; no se crean jobs ni ejecuciones redundantes.

**Límites:** esta reparación solo corrige la identificación de filas físicas en el generador de holdout v2; no certifica conformidad IVTFF completa, independencia histórica de los folios, procedencia de corpus, ausencia de fugas en todos los modelos ni traducción. Los controles históricos y resultados negativos permanecen intactos. EXP-170 sigue bloqueado por entradas externas no verificadas. El 22-11-2026 es fecha de evaluación, no garantía de descifrado.
