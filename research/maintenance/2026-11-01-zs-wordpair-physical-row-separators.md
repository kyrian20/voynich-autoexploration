# Zhang–Sheng: rechazar separadores no físicos antes de leer páginas IVTFF

**Fecha:** 2026-11-01. **Tipo:** reparación acotada de lector / integridad de fuente; sin EXP nuevo.
**Base inspeccionada:** `master` `171b258c22b8289fcbb7fafaf1f392ad7aab6044`.
**Estado:** propuesta de reparación; las pruebas CI de la PR y de `master` deben verificarse antes de cerrar.

## Incidencia y criterio adversarial

Ambos lectores en `research/maintenance/2026-11-01-zs-wordpair-audit/wordpair_audit.py` usaban `str.splitlines()`. Python considera U+2028, U+0085, VT, FF y otros controles como saltos de línea, aunque el auditor estructural independiente `scripts/audit_ivtff_page_locus_ids.py` define como límites físicos IVTFF únicamente CR, LF y CRLF. Un comentario como `# comment\u2028<f2r> $L=B` podía crear un encabezado `f2r` aparente. Esto es un fallo del lector frente a entradas adversariales, **no** evidencia de alteración de las transcripciones congeladas.

La reparación introduce `physical_ivtff_rows()`: normaliza exclusivamente CRLF/CR a LF, rechaza ocho separadores no físicos antes de procesar cualquier etiqueta en la fila y conserva el orden y el texto original de las filas restantes. Los dos lectores, EVA lossless y proyección ASCII histórica, utilizan la misma barrera.

## Pruebas de regresión y ejecución

Archivo: `tests/test_zs_wordpair_source_lock.py`. Se añaden:
- Rechazo de cada uno de `\\v, \\f, \\x1c, \\x1d, \\x1e, \\x85, \\u2028, \\u2029` por ambos lectores cuando ocultan una falsa cabecera detrás de un comentario.
- Aceptación de CR, LF y CRLF físicos por ambos lectores.

Comandos para verificar desde la raíz:

```bash
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
```

La CI existente ejecuta estas pruebas y reproduce únicamente **dos** de las 54 filas numéricas congeladas. No se reclasifican las otras 52 filas como reproducidas ni se interpreta esta reparación como reproducción de Zhang–Sheng.

## Conservación, límites y siguiente paso

No se modifican `data/transcriptions/`, `results.json`, semillas (20261101–20261103), parámetros (20 barajados; 150/300/600 tipos), manifiestos prospectivos, experimentos históricos ni `state/committed_claims.md`. Fuentes fijadas: ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

Este control no certifica la conformidad IVTFF completa. Las entradas originales pasan otras auditorías estructurales, pero el presente cambio no incluye una comparación byte a byte de los 54 resultados. Si la CI falla, registrar la causa y mantener la PR abierta; si pasa, verificar el `master` posterior a la integración antes de declarar cierre.

**Pendientes externos:** EXP-170 bloqueado por entradas Naibbe históricas no acreditadas; conciliación de artefactos GitHub/Biblioteca y adjudicación IVTFF completa. No se han ejecutado pruebas semánticas ni se asignan traducciones.
