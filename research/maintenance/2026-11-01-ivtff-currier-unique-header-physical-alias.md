# Auditor de cabeceras Currier — identidad física con ceros iniciales

**Fecha:** 2026-11-01. **Base de partida:** `master` `2bb0399110f4b0d266bad76faeb6d3e904fb9304`. **Estado:** reparación de integridad operativa, no experimento científico. **Sin nueva asignación EXP.**

## Defecto específico y reproducción mínima

`scripts/audit_ivtff_unique_page_headers.py` es el guardia aditivo independiente del censo de metadatos Currier. A diferencia de los dos auditores reparados en PR #211, almacenaba la cabecera **cruda** como clave de unicidad. Por ello, `<f1r>` y `<f01r>` eran dos claves distintas pese a representar el mismo recto físico; el mismo defecto afectaba a `<f67r1>`/`<f067r1>` y `<f86v4>`/`<f086v4>`. La reproducción estática del algoritmo anterior con esas dos primeras líneas acepta dos páginas (no lanza error). Es un defecto de este guardia independiente, **no** evidencia de duplicación en ZL3b.

El extractor histórico `HEADER` utiliza `\\d`, que admite dígitos Unicode; una cabecera como `<f١r>` podía pasar la extracción y el censo de unicidad sin comprobar que el número fuese ASCII. Se rechaza explícitamente al convertir la identidad.

## Reparación

- `scripts/audit_ivtff_unique_page_headers.py`: conserva el extractor `HEADER` histórico y sus fuentes, pero compara la identidad `(número entero, cara, panel)` de páginas numéricas; Rosettes tiene identidad propia. Rechaza dígitos no ASCII. No altera los textos originales.
- `tests/test_ivtff_unique_page_headers.py`: tres pruebas nuevas: alias con ceros en páginas y paneles; no confundir caras/paneles realmente diferentes; rechazo de dígitos Unicode.
- `.github/workflows/voynich-check.yml`: ejecutar ese módulo de pruebas también con `python -O`, además de modo normal y del censo original.

**Comandos de comprobación:**
```sh
python -m unittest discover -s tests -p 'test_ivtff_unique_page_headers.py' -v
python -O -m unittest discover -s tests -p 'test_ivtff_unique_page_headers.py' -v
python scripts/audit_ivtff_unique_page_headers.py
```

**Criterios de cierre:** PR CI `success` en el head exacto; las nuevas pruebas visibles como `ok` en logs; censo original de ZL3b `folio_headers=227` y `distinct_folio_ids=227`; integración solo tras revisar concurrencia y `master`, seguida de CI de `master` satisfactoria. Hasta entonces, reparación **propuesta**, no cerrada.

## Alcance y límites

El guardia solo comprueba unicidad de cabeceras reconocidas por el patrón histórico: no acredita conformidad IVTFF completa, ni tokenización, ni clases Currier correctas, ni traducción. El problema se ha demostrado en datos sintéticos; no hay prueba de que afecte a los corpus originales. No se tocan transcripciones, manifiestos congelados, particiones, scripts históricos, semillas, resultados positivos/negativos ni `state/committed_claims.md`. EXP-170 continúa `BLOCKED` para reproducción histórica exacta; PR #7 y #138 permanecen en revisión. Los cambios de PR #212/#213 se integraron en la rama de PR #138 y no deben confundirse con `master`.

**Siguiente paso:** verificar CI y el censo original de este guardia; después continuar con procedencia de EXP-170 o discrepancias IVTFF de impacto científico, sin ejecutar ciclos científicos bloqueados. Evaluación final prevista para 2026-11-22, sin promesa de descifrado.
