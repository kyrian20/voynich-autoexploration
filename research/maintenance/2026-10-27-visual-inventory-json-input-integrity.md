# Integridad de JSON de inventario y manifiesto en lectores visuales — 27-10-2026

**Estado al proponer:** corrección operativa en rama; CI y verificación posterior a integración pendientes. **No es un EXP** y no constituye una prueba semántica. Base de `master`: `397d389532bb2a92ba53e87a22abdd189d0164c1`; su CI push [40478140501](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40478140501) figuraba `success` antes de abrir esta rama.

## Defecto delimitado y control adversarial

El manifiesto v2 ya tenía un lector estricto con detección de claves JSON repetidas y un contrato congelado, usado por el piloto y la cola visual. **El inventario `inventory.json.gz` no tenía el equivalente**: `select_visual_pilot_v2.py`, `audit_label_partition_coverage.py`, `audit_visual_inventory_source_rows.py`, `audit_visual_inventory_completeness.py` y `audit_visual_inventory_projections.py` llamaban a `json.loads(gzip.decompress(...))`. Python acepta silenciosamente `{"folio":"f2r","folio":"f99r"}` y conserva la última clave. El hash del archivo recibido podía registrarse sin advertir esta ambigüedad. No se ha demostrado que el inventario histórico tenga claves repetidas: es una vía de aceptación sintética.

Además, las entradas CLI de los tres auditores de líneas, completitud y proyecciones leían el manifiesto mediante `json.loads` simple, sin exigir el contrato científico ni recalcular las asignaciones individuales de las hojas reservadas. Sus funciones `audit()` / `replay()` aceptan manifiestos sintéticos deliberadamente para las pruebas unitarias; **no** se presentan como guardias de entrada autónomas.

## Reparación

- `scripts/select_visual_pilot_v2.py` incorpora `load_unique_inventory(archive_bytes)`: descomprime exactamente los bytes archivados y rechaza claves duplicadas **a cualquier profundidad**, incluidas vistas y metadatos, antes de construir un informe. El piloto lo utiliza.
- Los otros cuatro consumidores citados usan ese lector compartido, sin alterar los datos archivados ni el algoritmo de selección.
- Los tres auditores CLI usan también `load_verified_frozen_manifest`, ya existente, que comprueba claves únicas, sal, particiones, contrato de uso y hashes de transcripciones. No se crea una segunda implementación del reparto.
- `tests/test_visual_inventory_json_integrity.py` cubre JSON normal y archivo histórico, duplicados de raíz y anidados, rechazo por cobertura/cola/piloto, y rechazo del manifiesto duplicado o con intercambio train/test por los auditores.
- La CI ejecuta explícitamente estas pruebas antes de las auditorías del inventario.

**Aceptación exigida:** regresiones nuevas y pruebas existentes satisfactorias, reproducción de los informes y paquetes históricos sin cambios, CI de la PR verde y, si se fusiona, CI del nuevo `master` verificada con SHA y artefactos. Si la entrada histórica falla, **no** se reescribe ni se sustituye para forzar concordancia.

## Reproducción y límites

```sh
python -m unittest discover -s tests -p 'test_visual_inventory_json_integrity.py' -v
python -m unittest discover -s tests -p 'test_visual_inventory_source_rows.py' -v
python -m unittest discover -s tests -p 'test_visual_inventory_completeness.py' -v
python -m unittest discover -s tests -p 'test_visual_inventory_projections.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

Entradas congeladas: `data/transcriptions/eva_zl3b.txt` (SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`), `data/transcriptions/eva_it2a.txt` (`7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`), `research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json` y `research/decipherment/2026-10-25-label-inventory/inventory.json.gz`. Los hashes de corpus citados proceden de los registros archivados y deben comprobarse en CI; no se afirma haberlos recalculado localmente en esta sesión.

No hay semilla ni selección de reglas: las mutaciones son fixtures sintéticos. No se ejecuta ninguna hipótesis de traducción, no se leen resultados semánticos de test y no se modifica `state/committed_claims.md`. El holdout tiene exposición histórica previa. El acuerdo de lectores y la integridad JSON no prueban conformidad IVTFF independiente, imagen-etiqueta, idioma ni significado.

**Pendiente tras este bloque:** adjudicación IVTFF independiente y procedencia de corpus históricos, revisión de PR #5/#7/#13/#66/#82; no activar experimentos confirmatorios bloqueados.
