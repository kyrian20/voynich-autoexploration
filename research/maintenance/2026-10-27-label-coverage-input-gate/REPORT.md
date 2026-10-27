# Reparación acotada: entradas congeladas de la cobertura de etiquetas

Fecha: 2026-10-27. Tipo: **integridad operativa**, no EXP ni experimento lingüístico.
Estado al crear la rama: **PROPUESTA; pruebas CI y comparación de archivo pendientes**.
Base inicial: `master` `4fd7f6320ff742da1d9af7b5de0e72323b25f21f` (CI push 40448274481, success).

## Defecto identificable y alcance

`scripts/audit_label_partition_coverage.py::main` cargaba el manifiesto v2 con `json.loads` y comprobaba en `build` únicamente disyunción de hojas, pertenencia de hojas observadas, edición y hashes **declarados**. Un intercambio train/test que mantuviera tamaños y unión podía cambiar las tablas por partición sin que este consumidor comprobara la sal y asignación congeladas. Una fila del inventario podía declarar un hash correcto y alterar el locus o su línea fuente sin que `build` la cotejara con los bytes originales. El consumidor tampoco rechazaba miembros JSON duplicados. Son fallos potenciales de **aceptación de entradas manipuladas**; no se ha demostrado que el informe archivado estuviera manipulado.

Este es un consumidor diferente del piloto visual corregido en PR #93; no se reimplementa el reparto ni se modifica el manifiesto. Se reutilizan los controles existentes y se evita repetir un experimento científico.

## Corrección y criterios de regresión

Se añade `load_verified_coverage_inputs` al auditor de cobertura y se usa antes de `build` en el CLI. Primero exige la lectura estricta del manifiesto y la auditoría independiente de sal, particiones, fuentes y contrato científico (`load_verified_frozen_manifest`). Después exige la auditoría de vinculación de cada fila original y el censo L/R de líneas físicas (`audit_visual_inventory_completeness`). La función `build` conserva su API para fixtures sintéticos: no se presenta como un validador independiente de fuentes cuando se invoca aisladamente.

Criterios previos a CI: (1) reproducir el JSON archivado exactamente; (2) rechazar intercambio train/test con recuentos conservados; (3) rechazar claves duplicadas; (4) rechazar alteración de una línea cruda del inventario; (5) rechazar omisión de una fila L/R. Cinco regresiones nuevas en `tests/test_label_partition_coverage.py`, descubiertas por el workflow canónico. Entradas adversariales solo en memoria. Sin semilla aleatoria: comparaciones deterministas.

## Procedencia y preservación

Archivos de referencia inmutables:
- `data/transcriptions/eva_zl3b.txt`, SHA-256 archivado `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- `data/transcriptions/eva_it2a.txt`, SHA-256 archivado `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- `research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json`.
- `research/decipherment/2026-10-25-label-inventory/inventory.json.gz`.
- `research/decipherment/2026-10-25-label-coverage/coverage.json` y `SHA256.json`.

Los hashes anteriores proceden del registro existente; no se atribuye un recálculo local de corpus a esta sesión. No se tocan corpus, manifiestos, inventario, tablas, resultados negativos, `state/committed_claims.md` ni identificadores EXP. La CI conserva la comparación byte a byte de la cobertura histórica.

## Pruebas exigidas antes de cerrar

```sh
python -m unittest discover -s tests -p 'test_label_partition_coverage.py' -v
python scripts/audit_label_partition_coverage.py --out /tmp/label-coverage.json
cmp research/decipherment/2026-10-25-label-coverage/coverage.json /tmp/label-coverage.json
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

El workflow `.github/workflows/voynich-check.yml` ya invoca las pruebas específicas y compara la salida congelada. No se inicia una ejecución redundante: se espera la CI de la PR. Registrar ID, SHA y conclusión **después** de comprobarlos.

## Autoauditoría y límites

- **Target-awareness:** no se usan resultados semánticos ni se ajustan umbrales al Voynich; solo se reutiliza la sal histórica, que fue definida antes.
- **Feature-destroying implementation:** no hay tokenización ni normalización nueva; las líneas originales y su selección se preservan.
- **Extrapolación:** protege exclusivamente el CLI de cobertura, no todos los consumidores ni todo el historial.
- **Resultado negativo:** una mutación rechazada demuestra comportamiento del guard, no corrupción real de los datos archivados.
- **Control:** se espera que el archivo intacto produzca exactamente el JSON archivado; se espera que cada mutación sintética sea rechazada. Los resultados se consideran **pendientes** hasta la CI.
- No acredita conformidad IVTFF completa, anotación visual independiente, ceguera histórica del holdout, validez de corpus históricos ni traducción.

## Siguiente acción

Revisar diff, CI y artefactos de la PR. Solo integrar si la CI corresponde al último SHA y la base no ha cambiado de manera conflictiva; después verificar la CI de `master`. Continuar con los consumidores restantes y la adjudicación IVTFF/corpus, sin abrir experimentos confirmatorios mientras haya contradicciones pendientes.
