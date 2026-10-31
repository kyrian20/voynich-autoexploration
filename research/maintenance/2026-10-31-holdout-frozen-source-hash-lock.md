# Bloque acotado — identidad independiente de fuentes del holdout v2

**Fecha:** 2026-10-31. **Clase:** reparación de integridad/procedencia; sin experimento semántico. **Base de trabajo:** `master` `ba2517b42991d954bac6cb127cfc4a0ac643e5c4`. **Estado científico:** holdout propuesto, no validación histórica ciega.

## Defecto verificable

`scripts/audit_holdout_locus_coverage.py::audit` cotejaba el SHA-256 de cada fuente contra el campo `manifest["corpora"][name]["sha256"]`, pero no contra una identidad independiente. Si alguien alteraba una transcripción **y actualizaba también su hash en el manifiesto**, conservando la cobertura de hojas, el auditor podía devolver `COVERAGE_VERIFIED_NOT_IVTFF_OR_SEMANTIC_VALIDATION`. El crosswalk usaba el mismo auditor. La sal y las particiones congeladas protegen la asignación de hojas, **no los bytes de las transcripciones**.

## Reparación y contrato falsable

Se fijan de forma independiente en el auditor los hashes originales del holdout v2:

- `eva_zl3b.txt`: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- `eva_it2a.txt`: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

La API `audit(...)` y `crosswalk(...)` exigen esos hashes por defecto. Solo las pruebas sintéticas pueden optar explícitamente por `enforce_frozen_source_hashes=False`; ese modo **no acredita fuentes congeladas**. El CLI sigue usando siempre el modo estricto.

Regresión adversarial: una fuente sintética original supera la comprobación con hashes independientes fijados; al añadir una fila de comentario y actualizar a la vez el hash del manifiesto, el antiguo control de coherencia sigue aceptándola, mientras que el nuevo bloqueo independiente rechaza `Frozen source SHA-256 mismatch`. Los controles existentes de particiones, cabeceras, crosswalk y exclusividad de salida siguen siendo aplicables. No se recalculan ni cambian las particiones, los corpus, el manifiesto ni los resultados anteriores.

## Comprobación y límites

Comandos de regresión previstos para CI y ejecución local:

```sh
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python -O -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python -m unittest discover -s tests -p 'test_holdout_page_crosswalk.py' -v
python -O -m unittest discover -s tests -p 'test_holdout_page_crosswalk.py' -v
python scripts/audit_holdout_locus_coverage.py
```

**Evidencia de CI:** comprobar el SHA de la PR y la ejecución posterior de `master` antes de declarar éxito. No se afirma en este documento que se hayan ejecutado los comandos.

La reparación prueba identidad de bytes respecto a las dos ediciones congeladas; **no** resuelve la conformidad IVTFF completa, las diferencias de transcripción, la conciliación Biblioteca/GitHub, las entradas históricas de EXP-170 ni la exposición previa de las hojas de prueba. ZL3b e IT2a no son manuscritos independientes. No hay regla semántica ni traducción validada.

**Siguiente acción:** revisar el resultado CI y, si pasa, integrar y verificar CI de `master`; después continuar adjudicación IVTFF o procedencia exacta de EXP-170. Evaluación final prevista: 2026-11-22, sin promesa de desciframiento.
