# Adjudicación de afirmaciones frente a salidas de referencia — 22-10-2026

**Estado:** revisión documental acotada; no EXP nuevo, simulación repetida ni validación global. Base canónica: b31492596c3e9a0c3f322c0ece62fa13a84d739d, sucesora inmediata de 19994b57027ce45e455c62eee745385c4c320838. Los cuatro lectores ya estaban reproducidos (CI 39820885646: success). La PR #2 audita EXP-170 y modifica el workflow principal; no se pisan sus archivos.

## Fuentes primarias y trazabilidad

Los lectores, SHA-256 y unidades están en [el snapshot congelado](../2026-10-22-remaining-readers/results.json) y el [manifiesto de identidad](../../CORPUS_IDENTITY_REVIEW.json). EXP-267 selecciona 105.892 tokens, EXP-288 87.754 registros de onset, ambos del Cicero **bilingüe latín+inglés**. EXP-001 selecciona 991.553 tokens y EXP-170 97.164 líneas de Douay-Rheims **inglés**. No sumar unidades diferentes ni atribuir retrospectivamente bytes a ejecuciones antiguas.

Fuentes de afirmaciones: [EXP-267/result.md](../../../experiments/exp_267_word_length_position/result.md), blob Git 92c47d101d35543dabce569f877cbf98176db246, y [EXP-288/result.md](../../../experiments/exp_288_stolfi_onset_decomp/result.md), blob Git c2c5711acf98c8779c179088275a4218699d3caf. Los scripts y corpus se comprueban por SHA-256 contra el snapshot. EXP-001 ya figura en [Q001](../../../state/open_questions.md); EXP-170/C001 ya está adjudicado [por separado](../2026-10-22-c001-adjudication/REPORT.md) y la PR #2 amplía su auditoría.

## Matriz afirmación → resultado → adjudicación

| Referencia | Afirmación histórica | Evidencia y decisión |
|---|---|---|
| EXP-267, §5 | Comparación con «Latin» (media 4,966; pico 2–3 caracteres). | El lector usa el Cicero bilingüe sin separar idiomas y conserva paratextos. **INVALID_FOR_CLAIM** como referencia latina monolingüe; cifras históricas intactas. |
| EXP-267, §2 | «En ambos dialectos MID tiene las palabras más cortas». | Tabla original: B MID=5,456, B LL=5,275. En B **LL es menor**; contradicción documental confirmada. En A MID=5,268 es menor que LF=5,526 y LL=5,706. |
| EXP-267, §3 | «Index 0 = line-final word (LF)». | El script fija índice 0 como **LF=line-first**, último índice como LL. La cabecera es incorrecta; el propio texto posterior usa la convención correcta. |
| EXP-288, control | «Latin Cicero Control». | Selección de 87.754 registros del bilingüe, además con descomposición distinta de EVA. **INVALID_FOR_CLAIM** como control latino monolingüe comparable; no se invalidan por ello las tablas internas del VMS. |
| EXP-288, interpretación | El rango de entropías por onset de 0,678/0,789 bits reduce incertidumbre sobre sufijo en ~0,7 bits. | **Inferencia matemática inválida**: rango de entropías condicionales no es información mutua. Contraejemplo exacto: dos onsets equiprobables determinan sufijos distintos; rango=0 bits, MI=1 bit. La MI real de EXP-288 no está calculada. |
| EXP-001 / EXP-170 | Controles «Vulgate/Latin». | Identidad inglesa ya documentada; EXP-170 excluido aquí por PR #2. |

Estas decisiones se refieren a **afirmaciones específicas**, no a la validez total de EXP-267/288, al efecto causal de la mezcla de idiomas ni a significados del manuscrito. No se modifican resultados históricos, committed_claims, findings ni la numeración.

## Código, pruebas y límites

Auditor: [scripts/audit_reference_claim_links.py](../../../scripts/audit_reference_claim_links.py); snapshot: [results.json](results.json); [cuatro pruebas puras](../../../tests/test_reference_claim_links.py). Comandos:

    python tests/test_reference_claim_links.py
    python scripts/audit_reference_claim_links.py --check research/maintenance/2026-10-22-claim-link-adjudication/results.json

El auditor compara hashes SHA-256 de cuatro scripts y dos corpus, identidad, blobs Git de los informes y la tabla histórica. Falla ante cambios y no importa experimentos ni reejecuta simulaciones. El snapshot contiene valores archivados y un control lógico exacto, no resultados experimentales nuevos. Cuatro pruebas puras se ejecutaron localmente con éxito; **la auditoría integral sobre checkout de GitHub sigue pendiente de ejecución**. El workflow principal está en modificación concurrente por PR #2, por lo que no se edita ahora; la CI existente comprobará sintaxis Python, no necesariamente este snapshot.

## Prueba falsable siguiente — no ejecutada

Preinscribir si el onset aporta información predictiva de sufijos **más allá de longitud de palabra y sección**. Congelar corpus/transcripción, SHA-256, lector IVTFF, lista de sufijos y división por folios. Comparar log-verosimilitud fuera de muestra de un baseline longitud+sección frente al mismo modelo añadiendo onset; control negativo de onset permutado dentro de estratos de longitud+sección y control positivo sintético con dependencia conocida. Informar ganancias por folio, intervalos, multiplicidad y fallos; si la ganancia no supera el nulo predefinido, no hay evidencia de dependencia adicional bajo ese protocolo. Si lo supera, no demuestra por sí sola lengua natural frente a cifrado o plantilla. No asignar EXP sin comprobar el registro y estudios previos.

## Autoauditoría según skills/audit_experiment.md

**Target-awareness:** selección retrospectiva de afirmaciones, no confirmación. **Destrucción de rasgos:** no se modifica tokenización ni manuscrito. **Extrapolación:** solo dos informes y sus lectores. **Alcance negativo:** interpretaciones particulares, no ausencia de lengua o traducción. **Controles:** rango=0 y MI=1 en el contraejemplo matemático; lectores heredados del bloque reproducido, no ejecutados de nuevo aquí.

**Sin sustituciones de corpus, borrados, nueva numeración EXP ni desciframiento declarado.**
