# IVTFF — alias de cabecera física por ceros iniciales (2026-11-01)

**Base inspeccionada:** `master` `a3e93280adb1f923c6850528d87a612cd1358f88`. **Clase:** reparación de integridad de dos censos independientes; **no** experimento lingüístico. **Estado:** propuesta sometida a CI por SHA, sin validación científica de transcripciones ni traducción.

## Defecto reproducible y alcance

Las expresiones de ambos censos admitían `f01r` y `f1r` como nombres de página. La detección de duplicados se basaba en cadenas literales, por lo que un mismo folio físico podía figurar dos veces con números decimales escritos de forma distinta. El censo estricto no contabilizaba un duplicado, y el auditor independiente conservaba ambas cabeceras, aunque las dos pertenecían a la misma hoja física. Los hashes actualizados de una fuente sintética no bastan para detectar esa ambigüedad. Los casos incluyen paneles `f86v4`/`f086v4`; `f86v4` y `f86v5` siguen siendo páginas distintas.

## Reparación

Se añade una clave lógica de página `(hoja_numérica, lado, panel)` en cada lector, sin compartir su implementación ni reescribir las etiquetas originales. `fRos` conserva identidad propia. El lector estricto usa esta clave para detectar duplicados y contar páginas lógicas distintas; el auditor de cobertura la usa para rechazar la segunda cabecera, conservando los IDs crudos para el crosswalk. No se normaliza el texto, no se fusionan registros, no se cambia la partición ni se descodifican tokens.

## Regresiones y reproducción exigida

Se añaden casos de `f1r/f01r`, `f86v4/f086v4` y `f86v5/f0086v5`, un control que conserva paneles distintos y un caso con fuente sintética y manifiesto rehasheados. Comandos en Python 3.12:

```sh
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python -O -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python tests/test_ivtff_page_locus_ids.py
python scripts/audit_ivtff_page_locus_ids.py
python scripts/audit_holdout_locus_coverage.py --help
python scripts/check_corpus_integrity.py
```

Los dos últimos comandos no certifican por sí solos IVTFF completo. Comprobar además Voynich Check para el SHA exacto de la PR y tras una eventual fusión; verificar jobs, artefactos y recuentos congelados. No se declaran aquí ejecuciones no observadas.

## Limitaciones

El defecto se demuestra con entradas adversariales sintéticas. No se afirma que existan alias decimales en las fuentes originales; una CI correcta sobre los corpus congelados sería evidencia de que no se alteran los recuentos admitidos, no de que el parser sea plenamente conforme a IVTFF. Los corpus, hashes, manifiestos, scripts históricos, semillas, particiones y resultados negativos quedan intactos. EXP-170 sigue **BLOCKED** para reproducción histórica exacta; siguen pendientes adjudicación IVTFF integral, conciliación de artefactos y revisión científica de PR #7/#138. No se actualiza `state/committed_claims.md`.
