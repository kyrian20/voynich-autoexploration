# IVTFF: detectar cabeceras de página sin delimitador inicial — 24-10-2026

**Tipo:** reparación estructural acotada; sin EXP nuevo. **Base inspeccionada:** `master` `9d5fd5defb3669755380652bc540c6844847a475`. **Estado:** parche propuesto en rama; CI y revisión remotas requeridas antes de afirmar integración.

## Defecto y criterio de aceptación

`scripts/audit_ivtff_page_locus_ids.py::audit_text` comprobaba los registros sin `<` inicial, pero no las **cabeceras** sin `<`. Una línea `f2r> <! $L=B>` no empieza por `<` ni coincide con `MISSING_OPEN_LOCUS_RE`; por tanto se omitía como texto ajeno. Si era la última línea, la auditoría podía devolver cero anomalías aun perdiendo una cabecera. Si seguían registros, el estado de página anterior permanecía activo, lo que confundía la causa del error. Es una deducción directa de las ramas de control del código de base; no se afirma haber observado este defecto en los tres corpus originales.

**Criterio falsable:** el fixture con `f2r> <! $L=B>` y ` fRos> <! $L=A>` debe registrar exactamente dos cabeceras malformadas, invalidar la página activa y producir dos discordancias en los registros siguientes. Una cabecera dañada final `f86v4> <! $L=B>` debe fallar aun sin registros posteriores. Texto ordinario `f2r>not-a-header` no debe clasificarse como cabecera.

## Reparación propuesta

- `scripts/audit_ivtff_page_locus_ids.py`: expresión regular acotada a nombres de página ya reconocidos, con `>` y separador posterior plausible; registrar `missing opening <` y poner `active_page = None`.
- `tests/test_ivtff_page_locus_ids.py`: tres controles sintéticos (dos cabeceras con registros, cabecera terminal y texto libre negativo). El fixture existente sigue comprobando los tres corpus originales sin modificarlos.
- No se cambian lectores de tokens, transcripciones, políticas de ligaduras, resultados históricos ni afirmaciones semánticas.

## Verificación requerida y límites

La CI canónica ejecuta `python tests/test_ivtff_page_locus_ids.py` y `python scripts/audit_ivtff_page_locus_ids.py`, además de controles operativos y de corpus. Comprobar URL, SHA, estado final y, si se integra, una ejecución **push** nueva sobre `master`; un check de la PR no sustituye esa ejecución.

Sin muestreo, aleatoriedad ni semillas; el fixture es determinista. Los SHA-256 de los corpus originales se imprimen en el JSON del auditor, sin modificar bytes. El arreglo detecta **un patrón** de cabecera rota; no es una implementación completa de IVTFF 2.0.2 y no resuelve la adjudicación de tokenización, procedencia de corpus latinos, ni la conciliación histórica. No se han ejecutado ciclos científicos ni asignado significado a vocablos.
