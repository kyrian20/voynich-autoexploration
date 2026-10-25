# IVTFF — cabeceras con sangría y espacios internos (25-10-2026)

**Tipo:** corrección de integridad del auditor, sin EXP nuevo ni inferencia lingüística.
**Base de trabajo:** `d8af1ee3a953efdaaf1fbf5ed5aa9b5c64851b3b` (master, consultado antes de crear la rama).
**Estado inicial:** propuesta en rama, pendiente de CI y revisión antes de integración.

## Defecto y prueba adversarial

La comprobación de cabeceras con sangría en `scripts/audit_ivtff_page_locus_ids.py` comparaba el texto situado entre `<` y `>` sin quitar los espacios internos. Un límite de página sintético como ` <f2r > <! $L=B>` o ` < f2r> <! $L=B>` no se reconocía ni como válido ni como defectuoso: se ignoraba, dejando activo el folio anterior. Un locus posterior `<f1r.2,@P0>` podía seguir contándose como si el límite no hubiera existido. Es un defecto del **auditor**, no prueba de corrupción en las transcripciones originales.

## Reparación y regresión

Solo en la **rama diagnóstica para líneas con sangría**, la identificación de candidatas elimina espacios ASCII o tabuladores dentro de los corchetes angulares antes de comparar con el patrón amplio. El identificador registrado sigue siendo el texto bruto, no se acepta ni repara ninguna cabecera inválida y se invalida `active_page`. `PAGE_RE` y `LOCUS_RE` permanecen intactos.

`tests/test_ivtff_page_locus_ids.py` incorpora tres casos sintéticos (espacio final, espacio inicial y panel incorrecto con espacio final), todos con un registro posterior que debe disparar `page_mismatch_count`. Un control negativo ` <unrelated >` verifica que no se clasifican metadatos ajenos. El test también comprueba las tres fuentes reales sin modificarlas.

**Comando de CI:** `python tests/test_ivtff_page_locus_ids.py` dentro de `Voynich Check`.

## Procedencia y límites

No se han modificado corpus, hashes de fuentes, resultados originales, scripts de experimentos, parámetros, semillas, manifiestos reservados, ni `committed_claims.md`. No se ha ejecutado ningún ciclo científico. El cambio solo detecta una familia adicional de errores sintéticos; no certifica conformidad IVTFF completa ni validez de traducción. Se requiere CI del commit exacto y posterior a la integración antes de cerrar la incidencia.
