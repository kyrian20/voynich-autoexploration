# Proyección IVTFF de múltiples filas físicas — 25-10-2026

**Estado:** corrección operativa propuesta en PR #43; no es un EXP ni una traducción. El criterio de cierre exige CI verde de la revisión final.

## Defecto y solución aditiva

El auxiliar histórico `scripts/ivtff_lossless.py` expone `tokens(payloads)` para una sola fila o una cadena completa de continuaciones. Al suministrar dos filas físicas ordinarias (`ab.cd` y `ef.gh`), su comprobación de continuidad rechaza la segunda. Concatenarlas manualmente, en cambio, introduciría falsas palabras entre filas. La colección de filas independientes no estaba soportada.

Se incorpora `scripts/ivtff_rows.py::tokens_rows` como adaptador **nuevo**: proyecta cada fila independiente por separado y concatena únicamente cadenas explícitas de `/` final + `/` inicial. Rechaza continuaciones huérfanas, conserva las políticas analíticas del lexer y no modifica las fuentes. El llamante sigue siendo responsable de suministrar filas en el orden y ámbito de locus correctos.

`tests/test_ivtff_lossless.py`, ya ejecutado por `Voynich Check`, cubre filas independientes, cadenas de dos y tres filas, cadenas separadas, mezclas, filas vacías, alternativas/comas, políticas inválidas y continuaciones mal emparejadas.

## Revisión adversarial y fallo histórico de la primera propuesta

La primera revisión de esta PR modificó directamente `scripts/ivtff_lossless.py`. La CI [40160328721](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40160328721) falló en el control de snapshot de EXP-173 **antes** de ejecutar las pruebas léxicas: `Snapshot mismatch: results.json`. La razón es que el resultado congelado incluye el SHA-256 del código de lexer. La segunda revisión introdujo un comparador que permitía solo una transición de hash; [40160510519](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40160510519) confirmó que los campos científicos del puente EXP-173 y `changed-rows.json.gz` coincidían, pero falló después en `Paragraph strata snapshot mismatch`, otro consumidor con hashes congelados.

Para no degradar la trazabilidad histórica ni encadenar excepciones de procedencia, **se ha revertido por completo el cambio al lexer y al puente EXP-173** en la revisión final. Se retiró también el overlay transitorio. La solución definitiva es el adaptador independiente; el lexer y los comparadores históricos quedan byte a byte idénticos a `master`. Los fallos de CI anteriores se conservan en GitHub como evidencia del intento descartado.

## Alcance y limitaciones

Esta reparación proporciona una API para secuencias de filas físicas; no acredita conformidad integral con IVTFF 2.0.2 ni reemplaza los lectores históricos. No altera corpus, particiones, semillas, snapshots, resultados negativos ni compromisos científicos. Las entradas sintéticas no utilizan aleatoriedad. No se declara validación en folios reservados ni se asignan significados a EVA. Una nueva ejecución de CI sobre el commit final debe verificar que no hay deriva de snapshots y que pasan las regresiones nuevas.
