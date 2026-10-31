# Salidas de auditorías de holdout: creación exclusiva, sin sobrescritura

**Fecha:** 2026-10-31. **Tipo:** corrección operativa acotada; ningún EXP nuevo. **Base:** `master` `7fc2449bb39976eff11f9de7170a09e1439d56af`. **Estado:** propuesta en rama; requiere CI del commit final, inspección de registros y verificación posterior a integración antes de declararse cerrada.

## Defecto comprobable en el código anterior

`scripts/audit_holdout_locus_coverage.py --out RUTA` y `scripts/audit_holdout_page_crosswalk.py --out RUTA` usaban `Path.write_text()`, que trunca una ruta ya existente. Un segundo análisis, una ruta equivocada o un enlace simbólico podían sobrescribir evidencia del control de folios. El generador del manifiesto v2 ya había recibido protección de salida en la PR #136; **estos dos auditores seguían utilizando escrituras destructivas**. No se ha observado una sobrescritura real del archivo histórico.

Se cambia únicamente el modo de apertura a `Path.open("x", encoding="utf-8", newline="\\n")` para ambos auditores. Si la ruta existe (también como enlace simbólico), Python lanza `FileExistsError` antes de truncar. La serialización, los cálculos, los datos, la sal de partición y la selección de folios no cambian. La ruta de comparación `research/maintenance/2026-10-25-holdout-page-crosswalk/results.json` sigue congelada.

## Regresión y aceptación

`tests/test_holdout_page_crosswalk.py::PageCrosswalkTests.test_both_audit_clis_refuse_existing_outputs_and_symlinks` llama a **ambos** `main()` reales sobre dos fuentes IVTFF sintéticas, con hashes y manifiesto v2 consistentes (folio `f67r` asignado a entrenamiento). Para cada auditor exige: primera creación con JSON no vacío y terminador LF; segunda invocación a la misma ruta lanza `FileExistsError` y conserva bytes idénticos; intento sobre enlace simbólico lanza `FileExistsError` y deja intacto el destino y el enlace. No usa ni lee tokens de folios de test para seleccionar reglas.

Criterio de cierre fijado antes de ejecutar: pasar el test nuevo y las suites existentes de cobertura/crosswalk; producir en CI el mismo JSON de crosswalk que el snapshot histórico; terminar la CI de PR y, si se integra, la CI push del nuevo `master`. Un run pendiente o cancelado no satisface el criterio.

Comandos (Python 3.12, desde raíz):

```sh
python -m unittest discover -s tests -p 'test_holdout_page_crosswalk.py' -v
python -O -m unittest discover -s tests -p 'test_holdout_page_crosswalk.py' -v
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python scripts/audit_holdout_locus_coverage.py --out /tmp/holdout-coverage-NUEVO.json
python scripts/audit_holdout_page_crosswalk.py --out /tmp/holdout-crosswalk-NUEVO.json
cmp research/maintenance/2026-10-25-holdout-page-crosswalk/results.json /tmp/holdout-crosswalk-NUEVO.json
```

La CI existente ejecuta ambas suites, ambos auditores y el `cmp` sobre salidas nuevas en el checkout. No se añade otra ejecución científica ni un workflow duplicado. Semilla: no aplicable. Los corpus congelados y el manifiesto v2 conservan sus SHA-256 de `research/CORPUS_INPUT_MANIFEST.json`; no se modifican.

## Alcance científico y autoauditoría

Este cambio previene la destrucción accidental de artefactos por los dos auditores; **no** acredita independencia histórica de los folios, validez semántica, conformidad IVTFF integral ni reproducción de EXP-170. No cambia los resultados negativos ni las afirmaciones comprometidas. La prueba es sintética y operacional; no se infieren significados. Se mantiene bloqueado cualquier ciclo científico que dependa de contradicciones o procedencia no resueltas.

Pendientes: adjudicación IVTFF, recuperación de entradas históricas exactas de EXP-170, conciliación de artefactos y revisión de las PR científicas en borrador. Evaluación general: 22-11-2026, sin promesa de descifrado.
