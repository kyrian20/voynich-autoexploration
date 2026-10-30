# IVTFF: cabeceras malformadas con sangría — 25-10-2026

**Tipo:** reparación estructural acotada; no es EXP nuevo ni inferencia lingüística.  
**Base revisada:** `d35db3e51a90cd0add4e15f1ec0e58bcd583bf30`.  
**Estado:** propuesta; CI y eventual integración pendientes de verificación.

## Defecto localizado

En `scripts/audit_ivtff_page_locus_ids.py`, la rama para filas que no empiezan en columna cero solo reconocía cabeceras con sangría si ya satisfacían `PAGE_RE` (identificador válido). Una cabecera con sangría y numeral Unicode (` <f٢r> <! $L=B>`) o panel inválido (` <f2r7> <! $L=B>`) no satisfacía la expresión estricta, se descartaba silenciosamente y **no invalidaba la página activa**. Un registro posterior de la página anterior podía parecer coherente. Es un defecto del auditor, no evidencia de que esas entradas existan en los corpus congelados.

## Corrección y regresiones

Se añade `INDENTED_PAGE_CANDIDATE_RE` solo para **detectar y rechazar** posibles cabeceras dañadas; `PAGE_RE` sigue siendo la única regla de aceptación. Al encontrar la candidata dañada, el auditor registra una cabecera malformada e invalida la página activa. No se normaliza ni recupera texto corrupto.

Se incorporan dos casos sintéticos con cabecera dañada, cada uno seguido de un locus que no debe heredarse silenciosamente, y un control de metadatos ajenos (` <unrelated>`) para evitar falsos positivos. No hay semilla ni permutaciones.

**Comando de prueba:** `python tests/test_ivtff_page_locus_ids.py`. El test existente también comprueba las tres transcripciones presentes sin alterarlas. La ejecución de CI y los logs deberán enlazarse en la PR antes de considerar el defecto cerrado.

## Preservación y limitaciones

Se mantienen sin cambios las transcripciones, las salidas históricas, el manifiesto de folios reservados, los EXP, las afirmaciones comprometidas y los resultados negativos. Esta reparación no autentica páginas físicas, no resuelve ligaduras ni alternativas, no certifica conformidad IVTFF completa y no autoriza experimentos semánticos bloqueados. No se usa texto de folios reservados para seleccionar parámetros.

**Siguiente paso:** ejecutar CI de la rama, comprobar el diff y el trabajo concurrente; integrar solo con evidencias.