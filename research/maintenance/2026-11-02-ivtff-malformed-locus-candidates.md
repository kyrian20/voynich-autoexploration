# Auditoría de pérdida silenciosa de loci IVTFF malformados (2026-11-02)

**Tipo:** corrección operativa acotada, sin EXP nuevo. **Base inicial:** `master` `9c39dcc10c04597255b742c98d1d0e5dc940a51b`. **Estado:** pendiente de CI y revisión de integración.

## Defecto y prueba previa

En `scripts/audit_ivtff_page_locus_ids.py`, `MISSING_OPEN_LOCUS_RE` solo reconocía números de locus con `\d+` seguidos de coma. Una fila de aspecto estructural con el delimitador `<` perdido y un ordinal dañado, por ejemplo `f1r.X,@P0> chedy`, no coincidía y se descartaba como texto ordinario sin incrementar `malformed_record_count`. La misma omisión ocurría con ` <f1r.X,@P0> chedy` y `/<f1r.X,@P0> chedy` porque los detectores de etiquetas estructurales estaban restringidos a ordinals numéricos. El control anterior `re.match(r'^f(?:\d+[rv][1-6]?|Ros)\.\d+,', 'f1r.X,@P0> chedy')` devuelve `None`. Esta es una prueba de una omisión lógica sobre datos sintéticos, **no evidencia de corrupción de los corpus**.

## Reparación falsable

- Añadir un detector diagnóstico de prefijo de locus, que admita números malformados únicamente para clasificarlos como error. No se amplía la gramática de loci válidos (`LOCUS_RE`).
- Para la ruta sin `<`, exigir también un `>` antes del espacio, de modo que `f1r.notes, commentary not a record` no se clasifique como registro.
- Mantener las tres rutas independientes: sin apertura, con indentación y tras barra de continuación. En todas, una entrada estructural malformada debe incrementar `malformed_record_count` y hacer que `structural_errors` no sea vacío.
- Añadir 4 casos sin apertura, 3 indentados, 3 tras barra y 1 control de prosa (11 comprobaciones), sin modificar los archivos originales ni resultados históricos.

## Criterios y límites

Comprobar `python tests/test_ivtff_page_locus_ids.py`, `python scripts/audit_ivtff_page_locus_ids.py`, el workflow `Voynich Check` de la PR y, si se integra, el del nuevo `master`. La prueba sintética no demuestra que existan estas formas en ZL3b, ZL3a o IT2a. El lector sigue siendo una auditoría estructural, no una certificación completa IVTFF; los corpus originales, particiones reservadas, seeds y resultados negativos permanecen congelados. No se ejecuta ningún experimento científico ni se reclama significado de palabras.

**Pendientes ajenos a este defecto:** EXP-170 bloqueado para reproducción histórica exacta por procedencia no acreditada de entradas externas, conciliación IVTFF integral, referencias de corpus históricas y artefactos, PR científicas #7/#138. No se levanta el bloqueo de ciclos científicos. Fecha de evaluación global: 22-11-2026, sin promesa de desciframiento.
