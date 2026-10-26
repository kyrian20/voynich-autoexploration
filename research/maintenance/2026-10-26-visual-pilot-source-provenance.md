# Control de procedencia del piloto visual — 26-10-2026

**Tipo:** reparación operativa de integridad; sin EXP nuevo ni inferencia lingüística. **Estado inicial:** propuesta pendiente de CI del commit final.

## Defecto y alcance

`scripts/select_visual_pilot_v2.py` validaba particiones y localizadores de hojas de entrenamiento, pero no cotejaba el inventario recibido con las ediciones y hashes del manifiesto v2. Un inventario alterado podía producir una selección aparentemente normal aunque una fila de desarrollo/prueba declarase otra procedencia, o aunque la fuente declarada ya no coincidiera con la congelada. La herramienta tampoco comprobaba duplicados de ocurrencia/locus al seleccionar el piloto. Esto es una vulnerabilidad de **integridad de entrada**, no evidencia de corrupción real del archivo histórico.

## Reparación propuesta

1. `build` comprueba que las ediciones del inventario sean únicas, que sus rutas y SHA-256 coincidan con `manifest['corpora']`, y que **todas** las filas (no solo entrenamiento) correspondan a su edición y SHA-256. Rechaza ocurrencias repetidas y loci duplicados dentro de una edición.
2. La ejecución CLI lee los bytes de las transcripciones locales y compara SHA-256 con las declaraciones del inventario. No sustituye las transcripciones ni modifica el manifiesto.
3. Las regresiones cubren fuente ausente/sustituida, fila de prueba con hash falso, duplicados y alteración de bytes. La prueba de archivo existente debe mantener exactamente la selección archivada sin reescribirla.

## Entradas congeladas

- `research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json`, blob Git `84f59008a190df7481c4e81a5c84c3916d79a59d`.
- ZL3b `data/transcriptions/eva_zl3b.txt`: SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a `data/transcriptions/eva_it2a.txt`: SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Archivo congelado `research/decipherment/2026-10-25-visual-annotation/pilot-selection-v2.json`, blob Git `7ef9a3d8db62845558731bf44b84d0a2cc113450`.

## Verificación exigida

```sh
python -m unittest discover -s tests -p 'test_visual_annotation_queue.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
python scripts/select_visual_pilot_v2.py --out /tmp/pilot-selection-v2-replay.json
```

La CI canónica ya reproduce y coteja el paquete visual; verificar su run exacto y el resultado de la prueba de archivo. Si falla, no fusionar ni reescribir el JSON histórico. Esta reparación no requiere semillas (comparaciones deterministas).

## Límites

Los hashes comprueban identidad de bytes locales y coherencia declarativa; no autentican por sí mismos la procedencia editorial original, ni la alineación entre etiqueta e imagen. Las 1.172 tareas y las máscaras siguen bloqueadas para anotación semántica. Los folios reservados fueron expuestos históricamente, de modo que no existe una prueba semántica ciega nueva. No se cambian corpus, manifiestos, archivos originales, resultados negativos, `state/committed_claims.md` ni decisiones científicas. Conformidad IVTFF completa, reconciliación de corpus históricos y artefactos de Biblioteca siguen abiertos.
