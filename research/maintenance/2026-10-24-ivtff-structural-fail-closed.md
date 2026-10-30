# Auditoría IVTFF: fallo explícito ante anomalías estructurales — 24-10-2026

**Clase:** corrección operativa sin nuevo EXP. **Base inspeccionada:** `92b90babe8dbe9f51c2bfb8808c4490eeb7a5f9b` (master). **Estado:** propuesta de reparación, pendiente de CI del commit de la rama.

## Defecto reproducible en código previo

`scripts/audit_ivtff_page_locus_ids.py` ya registraba `malformed_header_count`, `malformed_record_count`, `page_mismatch_count` y `locus_number_out_of_range_count`, pero `main()` solo devolvía error cuando había tags de registro duplicados. Una transcripción con identificador de página discordante o locus fuera de rango producía un informe con anomalías y salida del proceso 0, de modo que el paso de GitHub Actions podía aparecer en verde. Un archivo vacío tampoco tenía una barrera específica en este auditor (aunque otros controles de corpus pudieran bloquearlo).

## Cambio propuesto

Añadir `structural_errors(report)` como predicado explícito para las cinco categorías ya contabilizadas, además de ausencia de cabeceras o registros. Mantener sin cambios el JSON, el lector, las reglas de IVTFF, las fuentes y los resultados archivados. El proceso sigue imprimiendo el informe completo, pero termina con código no cero si hay anomalías.

Ampliar `tests/test_ivtff_page_locus_ids.py` con casos sintéticos deterministas: registro válido; cabecera malformada; locus malformado; página discordante; número 161 fuera del límite operativo 1–160; registro duplicado; entrada vacía; y control de las tres transcripciones originales. No hay aleatoriedad ni semillas; el límite 160 sigue siendo una comprobación de corpus, no una regla universal del formato.

## Alcance y límites

El registro `research/EXPERIMENT_REGISTER.md` documenta que ZL3b/ZL3a/IT2a tenían cero anomalías en estas categorías bajo la auditoría previa. La corrección no convierte la coincidencia de parsers en conformidad IVTFF, ni adjudica alternativas, ligaduras, codificaciones extendidas o identidades históricas. No se crean EXP, ni se editan corpus, hashes históricos, resultados negativos o afirmaciones comprometidas. No se ejecutan ciclos científicos bloqueados.

**Verificación necesaria:** `python tests/test_ivtff_page_locus_ids.py`, `python scripts/audit_ivtff_page_locus_ids.py`, `python -m unittest discover -s tests -v`, auditoría operativa e integridad de corpus; después confirmar `Voynich Check` sobre el SHA exacto de la PR. Un CI anterior de master no valida este cambio.
