# Auditoría de vinculación de registros del inventario visual — 26-10-2026

**Estado: PROPOSED / pendiente de verificación CI en esta rama.** Mantenimiento de integridad, no experimento semántico ni nuevo EXP.

## Incidencia delimitada

La selección v2 verificaba los hashes de las transcripciones, las ediciones declaradas y la concordancia superficial entre folio y localizador, pero no demostraba que cada registro archivado apuntase a la **línea física exacta** de su transcripción. Un registro alterado con hash de corpus correcto podía conservar una atribución de línea falsa.

## Reparación propuesta

El auditor `scripts/audit_visual_inventory_source_rows.py` verifica, para **todos** los registros archivados y no solo entrenamiento, el archivo de edición y su SHA-256, el número entero positivo de línea, `occurrence_id`, `raw_line`, `raw_line_sha256`, el identificador de folio/locus, el subtipo editorial y `raw_body` frente a la línea fuente. Detecta duplicación de línea física. Lee las fuentes exactamente con la convención archivada del constructor (`utf-8-sig`, `splitlines()`).

Comando CI:
```sh
python -m unittest discover -s tests -p 'test_visual_inventory_source_rows.py' -v
python scripts/audit_visual_inventory_source_rows.py --out visual-inventory-source-rows.json
sha256sum visual-inventory-source-rows.json > visual-inventory-source-rows.sha256
```

El workflow guarda el JSON y su SHA-256 como artefactos de la ejecución. Las pruebas sintéticas introducen falsificaciones de línea, cuerpo, identificador, hash, duplicado, tipo de número y fuente alterada. El resultado real queda pendiente hasta observar CI y sus logs.

## Invariantes y limitaciones

- No se modifica ningún corpus, inventario histórico, partición, resultado negativo o `state/committed_claims.md`.
- No se reinterpreta ningún registro IVTFF ni se reproducen resultados históricos; la vinculación es contra la selección ya archivada de registros L/R.
- Esta comprobación **no prueba completitud de la selección**, conformidad IVTFF independiente, correspondencia imagen/objeto, independencia de anotadores ni significado de palabras.
- No se examinan resultados de folios reservados ni se modifica su asignación. La comprobación de procedencia incluye sus metadatos archivados sin consumir resultados.
- No hay semilla ni aleatoriedad: comprobación determinista de identidad de bytes y campos.
- Si el archivo archivado y el original discrepan, no sustituir entradas; registrar bloqueo y recuperar procedencia exacta.

## Alcance de cierre

Solo se cerrará la incidencia tras CI satisfactoria del commit de la PR, comprobación del JSON/artefacto y, si se fusiona, CI del nuevo `master`. Esta nota inicial no certifica dichos resultados.
