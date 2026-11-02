# IVTFF — rechazo del folio físico cero (02-11-2026)

**Tipo:** corrección de integridad; sin EXP nuevo ni experimento científico. **Base:** `master` `94763db8da61b9046004c4d399e8ca0dd9a6892d` (PR #246 integrada; comprobación de Actions `41426956956` satisfactoria). **Estado de esta reparación:** pendiente de verificación CI del commit de PR y de integración. **Alcance:** auditoría estructural de folios/loci y auditoría estricta de metadatos; los lectores históricos no se modifican.

## Defecto concreto y criterio falsable

En `scripts/audit_ivtff_page_locus_ids.py`, tanto `PAGE_RE` como `LOCUS_RE` admitían `[0-9]+` sin exigir que el número de folio fuera positivo. Por inspección, un corpus sintético con `<f0r>` y `<f0r.1,@P0>` podía contarse como folio y registro válidos; `physical_page_identity("f0r")` producía una identidad con número cero. En `scripts/audit_ivtff_metadata_strict.py`, `physical_page_key` aceptaba el mismo cero y el recorrido no validaba la identidad de una cabecera sin `$L`.

**Criterio definido antes de CI:** `f0r`, `f00v` y `f000r2` deben rechazarse como cabeceras; si aparecen como límites dañados, la página anterior deja de estar activa. Los loci con esos prefijos deben contarse como registros malformados, no observaciones válidas. El auditor estricto debe rechazar esas cabeceras incluso sin `$L`. El alias positivo `f0001r` debe seguir aceptándose, y las auditorías de los corpus originales deben conservar su resultado anterior.

## Reparación propuesta

- `scripts/audit_ivtff_page_locus_ids.py`: patrón de folio numérico con al menos un dígito no cero, usado para páginas y loci; defensa adicional en la función de identidad física.
- `scripts/audit_ivtff_metadata_strict.py`: rechazo explícito del número físico cero y validación de identidad de cada cabecera reconocida, antes de evaluar si declara Currier.
- `tests/test_ivtff_page_locus_ids.py`: tres mutaciones de cabecera, tres de locus y control de alias positivo, además de las regresiones existentes sobre los corpus.
- `tests/test_ivtff_metadata_strict.py`: tres cabeceras sin `$L` pero con número de folio cero, que deben fallar.

**Comandos de verificación en CI:** `python tests/test_ivtff_page_locus_ids.py`, `python tests/test_ivtff_metadata_strict.py`, `python -O tests/test_ivtff_metadata_strict.py`, `python scripts/audit_ivtff_page_locus_ids.py`, `python scripts/audit_ivtff_metadata_strict.py`. El workflow `Voynich Check` contiene estos pasos. Los tests con `assert` del auditor estructural se ejecutan sin `-O`.

## Preservación, interpretación y limitaciones

No se cambian las transcripciones, las particiones de folios reservados, los resultados negativos ni los históricos congelados, semillas, scripts experimentales o `state/committed_claims.md`. Las pruebas nuevas son **mutaciones sintéticas**; no se afirma que el defecto se haya manifestado en ZL3b/ZL3a/IT2a ni se certifica conformidad completa IVTFF. La corrección no rehabilita experimentos con problemas de identidad de corpus, no reproduce EXP-170 ni permite traducción alguna. EXP-170 permanece BLOCKED para reproducción exacta por falta de entradas externas verificadas. La contradicción C001 y la conciliación general de artefactos siguen abiertas. No se inicia ningún ciclo científico prohibido.

**Cierre requerido:** confirmar los pasos y logs de la PR, fusionar solo si están correctos y comprobar `master` y su CI posterior; actualizar esta nota o dejar una constancia enlazada de las evidencias. Evaluación científica final prevista el 22-11-2026, sin promesa de descifrado.
