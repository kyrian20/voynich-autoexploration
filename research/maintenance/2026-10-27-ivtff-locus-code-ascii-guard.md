# Reparación acotada: códigos de locus IVTFF no imprimibles o no ASCII — 2026-10-27

**Estado:** propuesta de reparación; las pruebas y CI definitivas deben comprobarse en la PR antes de declararla cerrada.

## Defecto y reproducción mínima

El auditor estructural `scripts/audit_ivtff_page_locus_ids.py` aceptaba `(?P<code>[^;>]{3})` y un transcriptor opcional `[^;>]`. Por ello, un registro sintético `<f1r.2,   >`, `<f1r.2,éP0>` o `<f1r.2,@P0;é>` coincidía con el patrón y se contabilizaba como locus estructural. Esto no demuestra corrupción de ninguna transcripción original: es un fallo reproducible del contrato de aceptación ante entradas adversariales.

**Corrección:** restringir exclusivamente esos campos a caracteres ASCII imprimibles, excluyendo los delimitadores `;`, `<` y `>`. No imponer un vocabulario de códigos basado únicamente en los datos observados; la comprobación no pretende validar todas las reglas IVTFF.

## Regresión y controles

- `python tests/test_ivtff_page_locus_ids.py`: nueve mutaciones sintéticas adversariales de código/transcriptor (cinco y cuatro) deben contarse como `malformed_record`, nunca como registros válidos.
- Controles positivos para `@P0`, `+P0`, `&Lz`, `/L0`, `!Lf`, `=P0`, `~Lt` y transcriptor ASCII `;A`.
- El mismo test audita sin reescribir las tres transcripciones ZL3b, ZL3a e IT2a; `python scripts/audit_ivtff_page_locus_ids.py` debe conservar los censos y no detectar errores estructurales.
- La CI canónica `.github/workflows/voynich-check.yml` ya ejecuta ambos comandos. No se añade un workflow ni un publicador duplicado.
- Comprobar el run de la PR y el de `master` después de una eventual fusión; un resultado de CI anterior no basta.

## Integridad y alcance científico

No se asigna EXP nuevo, no se reejecutan experimentos lingüísticos ni se modifica el parser histórico congelado de EXP-173. Los archivos originales y resultados negativos quedan intactos. El cambio protege un **censo de identificadores**, no establece la validez semántica de los códigos, la adjudicación independiente completa de IVTFF, la independencia de los folios reservados ni una traducción. Las contradicciones y bloqueos científicos existentes permanecen abiertos.

**Archivos propuestos:** `scripts/audit_ivtff_page_locus_ids.py`, `tests/test_ivtff_page_locus_ids.py` y esta nota. Evidencia de CI, SHA de integración y cierre: pendiente de verificar en GitHub.
