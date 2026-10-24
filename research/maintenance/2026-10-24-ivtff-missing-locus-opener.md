# Guardia contra pérdida silenciosa de locus sin apertura «<» — 24-10-2026

**Tipo:** reparación operativa acotada; no se asigna EXP. **Base fijada:** `2f8d82a221d6a95aab5b935a587b44bcf18cd7b1` (master). **Estado inicial:** propuesta sometida a CI, no cierre científico.

## Defecto y falsación

En `scripts/audit_ivtff_page_locus_ids.py`, `audit_text` ignoraba cualquier línea no vacía que no empezara por `<` (salvo comentarios y continuaciones). Un locus cuya apertura se hubiera perdido, por ejemplo `f1r.2,@P0> chedy`, no se contaba ni se denunciaba. Si el archivo también contenía registros válidos, `structural_errors` podía devolver una lista vacía pese a la pérdida de una fila.

**Criterio de reparación, fijado antes de CI:** una línea que empiece con un prefijo de locus reconocible `fNNr/v[panel].<número>,` o `fRos.<número>,` sin `<` debe figurar como registro malformado y causar fallo del auditor. El resto de metadatos libres sin etiqueta no debe convertirse artificialmente en locus.

## Cambio propuesto

- `scripts/audit_ivtff_page_locus_ids.py`: detección conservadora `MISSING_OPEN_LOCUS_RE` antes del descarte de líneas no etiquetadas; aprovecha el contador `malformed_record_count` y el predicado `structural_errors` ya existentes. No se modifica el análisis de los tags válidos.
- `tests/test_ivtff_page_locus_ids.py`: fixture determinista con un registro válido, dos registros dañados (`f1r` y `fRos`), y control de metadatos no etiquetados. La prueba exige exactamente dos errores y el rechazo correspondiente.
- **Sin semillas ni azar**; no se modifican transcripciones, scripts de tokenización, artefactos históricos, resultados negativos ni afirmaciones científicas.

## Comprobaciones exigidas para cerrar

1. `python tests/test_ivtff_page_locus_ids.py` (incluye control de las tres fuentes originales y cotejo de duplicados).
2. `python scripts/audit_ivtff_page_locus_ids.py` sobre las tres transcripciones originales.
3. `python -m unittest discover -s tests -v`, `python scripts/audit_repository_operations.py` y `python scripts/check_corpus_integrity.py`.
4. `Voynich Check` del SHA de la rama y, si se integra, del SHA nuevo de master.

**Limitaciones:** la expresión solo cubre filas sin `<` que conservan un prefijo reconocible y no constituye un parser IVTFF completo. El acuerdo de lectores no prueba conformidad de ligaduras, alternativas ni semántica. Ningún resultado lingüístico ni traducción se deriva de esta reparación. Las discrepancias de corpus históricos y la adjudicación normativa siguen abiertas.
