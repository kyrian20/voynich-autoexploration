# EXP-259 — Errata enlazada del comparador «Latin Cicero» (24-10-2026)

**Estado de la afirmación concreta: `INVALID_FOR_CLAIM`.** Se conserva íntegro `result.md` y `script.py` como documentos históricos. Esta errata no sustituye sus tablas ni presenta una nueva reproducción del experimento.

## Incidencia comprobada

El lector histórico `parse_latin` del EXP-259 procesa con una expresión regular todas las palabras ASCII del archivo `data/reference_corpora/latin/cicero_de_officiis_latin.txt`, sin separar idiomas. El archivo original congelado contiene **latín e inglés**, y el registro de procedencia lo clasifica `BILINGUAL_REQUIRES_FILTER_AUDIT`. La lectura histórica devuelve **112081** tokens del comparador mixto; ese número **no** es un recuento de tokens exclusivamente latinos.

Por tanto, **no se pueden utilizar** como comparaciones con latín monolingüe la columna `h(Lat)`, las entropías condicionales `h_cond(Lat)`, la «Finding 4», la comparación con latín en «Finding 1»/«Finding 3», el control latino de «Self-Audit» ni el punto 4 de «Conclusion» de `result.md`. La afirmación «aproximadamente un bit más predecibles que el latín» queda **`INVALID_FOR_CLAIM`**. No deben reutilizarse esas cifras como evidencia de una lengua, morfología natural, hipótesis de engaño o traducción.

## Alcance que permanece abierto

Los números internos de Currier A/B **no** quedan automáticamente refutados por la contaminación del comparador, pero tampoco se han reproducido ni validado aquí. La asignación simplificada de folios, la política EVA carácter/glifo, el tamaño de alfabetos y la conformidad IVTFF requieren auditoría separada. La conclusión `H449 CONFIRMED` del informe histórico **no es una validación científica vigente** para las inferencias citadas.

La evidencia, las invariantes SHA-256/Git blob, el lector histórico aislado, el control sintético bilingüe, los límites y el recibo reproducible están en [la adjudicación técnica](../../research/maintenance/2026-10-24-exp259-bilingual-comparator-guard.md). La ejecución de CI invoca `scripts/audit_exp259_latin_claim.py` y las regresiones `tests/test_exp259_latin_claim.py`; el auditor verifica también que esta errata siga presente y no pierda su estado explícito.

**Conservación:** sin cambios a los corpus, al script histórico, a `result.md`, a los resultados negativos ni a `state/committed_claims.md`. Semilla no aplicable a esta comprobación determinista. No se ha aislado un corpus latino monolingüe ni se ha calculado una entropía corregida; **no existe traducción validada**.
