# Guard de etiquetas IVTFF ocultas tras barra con sangría — 2026-10-27

**Estado inicial:** reparación propuesta; no declarar cierre hasta comprobar la CI del head y, si se fusiona, la de `master`. Rama basada en `f38c270bcea9d080ddb8e116d1f97a532a6a2cad`.

## Incidencia concreta y reproducción

El auditor `scripts/audit_ivtff_page_locus_ids.py` ya rechazaba `/<f2r>` y `/<f1r.2,@P0>` (PR #97), pero el mismo contenido precedido por espacio o tabulador (` /<f2r>`, `\t/<f1r.2,@P0>`) no pasaba por el guard de barras: el bucle exigía `raw.startswith("/")`. Después, el guard de filas con sangría solo buscaba un `<` inicial y descartaba la fila. Un límite de página dañado podía desaparecer sin invalidar el folio activo, y un registro podía omitirse sin elevar el contador de errores. La demostración utiliza **mutaciones sintéticas**, no anomalías observadas en los originales.

## Corrección y pruebas falsables

- `scripts/audit_ivtff_page_locus_ids.py`: se inspecciona la barra inicial después de eliminar **solo** espacios ASCII y tabulaciones al comienzo; el diagnóstico conserva la fila original y no convierte etiquetas dañadas en válidas.
- `tests/test_ivtff_page_locus_ids.py`: cinco cabeceras adversariales (página normal, Rosettes, panel, numeral Unicode y cabecera truncada), dos loci con barra y sangría, y dos continuaciones ordinarias con sangría como control positivo.
- Contrato previo al resultado: cada cabecera dañada debe producir `malformed_header_count=1`, `page_mismatch_count=1` y `continuation_lines=0`; cada locus dañado debe producir `malformed_record_count=1`; las continuaciones ordinarias deben seguir contabilizándose como dos y sin errores.
- Comandos de reproducción: `python tests/test_ivtff_page_locus_ids.py` y `python scripts/audit_ivtff_page_locus_ids.py`. Ambos ya figuran en `.github/workflows/voynich-check.yml`, sin nuevos workflows ni reintentos redundantes.
- Comprobar además la suite CI, sus logs y artefactos, y el SHA posterior a fusión. No inferir éxito de este informe.

## Procedencia y conservación

El script anterior tenía Git blob `696b22af5cf4e7bd936b421c2d40810c52089a2a`; la prueba anterior, `c1e0122128ac82aa6a14667d465b6808c3daaa36`. El corpus ZL3b congelado se identifica históricamente por SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` (la CI debe comprobar el archivo real). El cambio no modifica ninguna transcripción, manifiesto, script histórico de EXP-173, semilla, resultado previo, resultado negativo ni `state/committed_claims.md`. La auditoría es determinista, sin parámetros aleatorios ni EXP nuevo. La salida observable es un recuento de anomalías de identificadores.

## Alcance y bloqueos restantes

Este guard **no** acredita conformidad IVTFF completa, identidad de corpus históricos, independencia de folios reservados, resultados semánticos o traducción. No autoriza experimentos confirmatorios mientras las contradicciones de procedencia y la adjudicación IVTFF sigan abiertas. Las PR #5/#7/#13/#66/#82 continúan como propuestas independientes. No interpretar la reparación de un caso sintético como prueba de corrupción en los archivos originales.

## Evidencia de cierre

Pendiente de comprobar: URL de PR, SHA de head, ejecución CI y estado de sus pasos, reproducción sobre las tres fuentes y CI posterior a una eventual fusión. No cambiar esta sección sin verificación real.
