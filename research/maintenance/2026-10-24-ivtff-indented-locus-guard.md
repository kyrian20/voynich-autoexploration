# IVTFF: rechazo de filas y cabeceras con sangría — 24-10-2026

**Clase:** reparación operativa acotada, sin EXP nuevo. **Base de `master` inspeccionada:** `1c8b7a582179dcd9d9077867b8ec44a4c48c3493`. **Estado:** pendiente de CI y revisión de PR; no es conformidad IVTFF global.

## Defecto comprobable y criterio de cierre

La auditoría `scripts/audit_ivtff_page_locus_ids.py` solo analizaba filas que comenzaran exactamente por `<`. Un locus con un espacio o tabulación delante, por ejemplo ` <f1r.2,@P0> chedy`, se ignoraba sin sumar `malformed_record_count`; si había una cabecera y otro locus correctos, `structural_errors` podía devolver una lista vacía. Una cabecera indentada ` <f2r>` también se ignoraba, manteniendo activa una página anterior. El defecto se deduce de la rama de descarte de entradas no etiquetadas en la base fijada.

**Criterio previo a la verificación:** rechazar explícitamente los prefijos de locus reconocibles con sangría, sin normalizarlos ni incorporarlos como datos válidos; detectar cabeceras reconocibles indentadas, invalidar el estado de página y rechazar el locus siguiente hasta recibir cabecera correcta. Seguir ignorando metadatos libres sin aspecto de locus.

## Cambios propuestos

- `scripts/audit_ivtff_page_locus_ids.py`: inspección no destructiva de prefijos con espacios/tabulaciones antes de descartar líneas no estructurales; incremento de contadores existentes, conservando la línea cruda como evidencia (hasta 180 caracteres).
- `tests/test_ivtff_page_locus_ids.py`: fixture de un registro válido y tres filas dañadas, fixture de cabecera indentada y locus posterior, además de las regresiones previas y comprobación de las tres transcripciones congeladas.
- Sin cambio en `data/`, los lectores de producción, los resultados históricos, `state/committed_claims.md` ni la numeración de EXP. No se han asignado significados ni se han calculado estadísticas lingüísticas.

## Comprobaciones requeridas

```sh
python tests/test_ivtff_page_locus_ids.py
python scripts/audit_ivtff_page_locus_ids.py
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La CI `Voynich Check` de la rama debe ejecutar estos controles y conservar el SHA exacto. No se considera cerrada la reparación hasta verificar el resultado. El último CI verde de `master` anterior a esta rama no prueba este cambio.

## Limitaciones

Se reconocen únicamente los prefijos de página/locus previstos por las expresiones existentes; un identificador completamente ilegible o un tipo de línea no reconocido puede seguir escapando a esta guardia. La auditoría no certifica todas las reglas IVTFF 2.0.2, alternativas, ligaduras o codificaciones extendidas. Las fuentes ZL3b, ZL3a e IT2a son ediciones del mismo manuscrito. Continúan pendientes las identidades históricas de corpus y las contradicciones científicas; no se reabre el ciclo confirmatorio.
