# IVTFF: pérdida de separador antes del comentario de cabecera — 2026-10-27

**Estado:** reparación técnica acotada; la validación depende de CI del commit y del estado posterior de master. No es un experimento lingüístico.

## Defecto reproducible y criterio previo

En `scripts/audit_ivtff_page_locus_ids.py`, el detector de cabeceras sin delimitador inicial reconocía `f2r <! $L=B>`, pero no `f2r<! $L=B>`: exigía al menos un espacio antes de `<!`. Esa línea quedaba descartada y el folio anterior permanecía activo. La siguiente fila del folio anterior podía contarse como si nada hubiera ocurrido.

Criterio de regresión: cuatro cabeceras dañadas (`f2r`, `fRos`, `f86v4`, un dígito Unicode, incluyendo sangría y comentario truncado) deben producir una cabecera malformada, una discrepancia de página, cero registros malformados y conservar exactamente dos registros. Dos controles de texto no estructural deben seguir sin errores.

## Cambio y reproducibilidad

- Cambiar exclusivamente `\\s+<!` por `\\s*<!` en el detector **diagnóstico** `MISSING_OPEN_PAGE_WITH_METADATA_RE`; la gramática de aceptación `PAGE_RE` no cambia.
- Añadir fixtures en `tests/test_ivtff_page_locus_ids.py`, ya invocados por la CI existente.
- Ejecutar `python tests/test_ivtff_page_locus_ids.py` y `python scripts/audit_ivtff_page_locus_ids.py`; ejecutar el workflow `Voynich Check` completo.
- Base: `51f541ec817570bf55a1733428264939e819bc69`. Blobs originales: auditor `cbaf1bc8cdddf9a492b8a129a0731a635fa32b78`, pruebas `a135f3abcf2b2c9d6c5ff62904f9d3b484afe0b4`.
- Transcripción ZL3b original (SHA-256 histórico declarado, a verificar en CI): `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.

No se alteran corpus, experimentos archivados, seeds, divisiones reservadas, salidas negativas ni `state/committed_claims.md`. La prueba es determinista y sintética: no hay semilla aleatoria ni afirmación de que el defecto exista en las transcripciones originales.

## Limitaciones

La corrección detecta una forma adicional de cabecera rota; no certifica IVTFF completo, no adjudica corpus históricos, no resuelve PR científicas abiertas ni valida traducción. No reabrir experimentos confirmatorios por este cambio aislado.
