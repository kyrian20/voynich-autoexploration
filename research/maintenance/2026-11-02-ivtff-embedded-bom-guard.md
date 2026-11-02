# IVTFF — firma UTF-8 incrustada y pérdida silenciosa de folio (02-11-2026)

**Tipo:** reparación de integridad del auditor estructural; **sin EXP nuevo ni ciclo científico**. Base examinada: `master` `4cb5be47ade2c2e757d2a0f23752ecaa823d8e34`, CI push `41435305424` (completed/success). Se comprobaron las diez PR abiertas; las #2, #8 y #10 ya están fusionadas. No se modifican sus correcciones.

## Defecto y criterio falsable (fijado antes de ejecutar CI)

`scripts/audit_ivtff_page_locus_ids.py` separaba filas por CR/LF y solo reconocía una cabecera estructural que empezase en columna cero con `<`. Un carácter U+FEFF incrustado antes de `<f2r>` impedía reconocer la transición y no se contabilizaba como anomalía; el folio anterior seguía activo y un locus posterior suyo podía pasar sin aviso. El mismo carácter dentro de una etiqueta de locus, de su texto o de un comentario no estaba explícitamente censado.

**Criterio de aceptación:** un U+FEFF en cualquier fila ya decodificada debe contabilizarse con línea exacta en `unexpected_bom_count`, excluir esa fila de cabeceras/registros y anular el folio activo; un registro posterior debe registrar `page_mismatch_count`. La firma UTF-8 genuina al comienzo del archivo sigue permitida cuando el lector la retira mediante `utf-8-sig`; el API `audit_text` no retira firmas implícitamente.

## Cambios propuestos y comprobación

- `scripts/audit_ivtff_page_locus_ids.py`: rechazo temprano de filas con U+FEFF, diagnóstico aditivo `unexpected_bom_rows`/`unexpected_bom_count` y puerta de error estructural.
- `tests/test_ivtff_page_locus_ids.py`: cabecera contaminada, locus, cuerpo de palabra, comentario, firma inicial normalizada y entrada API sin normalizar. Mutaciones exclusivamente sintéticas.
- Comprobar en GitHub Actions `python tests/test_ivtff_page_locus_ids.py` y `python scripts/audit_ivtff_page_locus_ids.py` contra los tres corpus congelados. Comprobar SHA del commit y CI de PR; si se integra, comprobar CI push del nuevo `master`. **No declarar cierre antes de ver ambas ejecuciones.**

## Conservación y límites

Se preservan sin cambios los corpus originales, transcripciones ZL3a/ZL3b/IT2a, resultados positivos y negativos, scripts históricos, semillas, hashes archivados, particiones de folios reservados y `state/committed_claims.md`. El nuevo contador amplía el JSON diagnóstico del auditor (no es una reproducción de estadísticas históricas). La regresión sintética prueba un fallo de la lógica anterior, **no** que el corpus original contenga U+FEFF incrustado. Esta corrección no acredita conformidad IVTFF completa, identidad histórica de EXP-170, conciliación global de artefactos, semántica ni traducción.

**Pendientes:** entradas externas originales de EXP-170 y hashes de procedencia (reproducción exacta BLOCKED); contradicciones históricas C001 pendientes de adjudicación humana; auditoría IVTFF integral; reconciliación de artefactos y PR científicas #7/#138. No se ejecutan ciclos científicos prohibidos. Evaluación global el 22-11-2026 sin prometer descifrado.
