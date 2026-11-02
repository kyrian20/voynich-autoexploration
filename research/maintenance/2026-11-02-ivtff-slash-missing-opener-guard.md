# IVTFF — slash y apertura de etiqueta perdidas simultáneamente (02-11-2026)

**Clase:** reparación de integridad estructural, sin EXP nuevo. **Base comprobada:** `master` `7dcea2c167a341368e19609a990d5a40160e6ff5` (PR #245 ya integrada). **Estado de la revisión:** pendiente de CI del head exacto y, si procede, de integración. **Estado científico:** no cambia; EXP-170 permanece BLOCKED para reproducción histórica exacta.

## Incidencia reproducible por inspección del flujo

`scripts/audit_ivtff_page_locus_ids.py::audit_text` detectaba `/<f2r>` y `/<f1r.2,@P0>`, pero al recibir `/f2r>` o `/f1r.X,@P0>` (barra de continuación y apertura `<` perdidas a la vez) entraba en la rama de continuación, incrementaba `continuation_lines` y omitía la estructura. En el caso de una página, `active_page` permanecía en `f1r` y un registro posterior de `f1r` parecía válido. El defecto se deduce del orden anterior de las condiciones; **son mutaciones sintéticas**, no filas observadas en los corpus.

**Criterio falsable antes de CI:** una barra seguida de una cabecera sin `<` pero con `>` o metadatos `<!` debe producir `malformed_header_count=1`, anular la página activa y causar el desacuerdo esperado en la fila posterior; una barra seguida de un locus sin `<` y con `>` debe producir `malformed_record_count=1`. Las continuaciones de prosa no estructural deben seguir aceptándose.

## Cambio y controles

- Se reutilizan los detectores diagnósticos de página y locus ya existentes, exclusivamente después de la rama de barra y únicamente si no hay apertura `<`. No se amplía `PAGE_RE` ni `LOCUS_RE`.
- Se exige terminador explícito de etiqueta o metadatos adyacentes para detectar cabecera; para locus se exige `>` y prefijo de folio/locus. No se confunde `/f2r commentary` ni `/f1r.notes, ordinary prose` con etiquetas.
- Regresiones: cuatro cabeceras dañadas (incluidos Rosettes, panel y metadatos), tres loci dañados (ordinal válido y malformado) y cuatro continuaciones benignas. Se mantienen las pruebas anteriores de barras, indentación y corpus reales.

**Verificación exigida:** `python tests/test_ivtff_page_locus_ids.py`, `python scripts/audit_ivtff_page_locus_ids.py`, `python scripts/check_corpus_integrity.py`, `python scripts/audit_repository_operations.py` y `Voynich Check` de la PR y del `master` posterior si se integra. Los comandos no se declaran ejecutados hasta comprobar sus logs. La suite con `assert` se ejecuta con Python normal, no como prueba sustantiva bajo `-O`.

## Preservación y limitaciones

No se modifica ninguna transcripción, manifiesto de folios reservados, script o resultado histórico, semilla, parámetro, hash congelado, salida negativa ni `state/committed_claims.md`. No hay aleatoriedad ni simulaciones nuevas. La reparación detecta corrupción sintética que antes podía omitirse; **no demuestra** que existiera en ZL3b, ZL3a o IT2a, ni certifica la conformidad IVTFF integral. No se ejecutan ciclos científicos bloqueados. Persisten la procedencia no acreditada de EXP-170, la conciliación global de artefactos y la revisión científica de las PR #7/#138. Evaluación final prevista para el 22-11-2026, sin promesa de descifrado.
