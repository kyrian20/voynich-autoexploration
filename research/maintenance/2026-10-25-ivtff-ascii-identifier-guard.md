# Auditoría de identificadores IVTFF: numerales no ASCII — 25-10-2026

**Tipo:** corrección de validación estructural, sin EXP nuevo ni ejecución científica.
**Base comprobada:** `980c2e39886d42019d9b1352242f1323f2026ed3` (`master`).
**Estado:** propuesta de reparación; verificar la CI de la PR y, si se fusiona, la CI posterior antes de cerrarla.

## Defecto concreto y alcance

`scripts/audit_ivtff_page_locus_ids.py` empleaba `\\d` de Python en las expresiones estrictas `PAGE_RE` y `LOCUS_RE`. En Python 3, `\\d` admite dígitos decimales Unicode, no solo los dígitos ASCII `0–9` usados por los identificadores IVTFF. Por ello, el auditor aceptaba sintéticamente `<f١r>` y `<f١r.1,@P0>` como página y registro normales; también `<f1r.٢,@P0>`. La conversión `int()` no impedía la aceptación. Esto era un defecto de validación, no evidencia de corrupción en las transcripciones actuales.

La corrección restringe **solo las expresiones de aceptación** de página y locus a `[0-9]`. Las expresiones de diagnóstico de una etiqueta con `<` perdido siguen siendo deliberadamente más amplias para poder detectar, en vez de ignorar, una línea rota con dígitos Unicode.

## Controles de regresión

`tests/test_ivtff_page_locus_ids.py` incluye ahora cuatro casos sintéticos:

1. Página y registro con numeral árabe-índico U+0661: rechazo de ambos.
2. Número de línea con U+0662: rechazo del registro.
3. Cabecera Unicode entre dos registros: se marca cabecera inválida y se invalida la página activa; no se asigna el segundo registro silenciosamente.
4. Cabecera Unicode sin `<`: sigue siendo visible como error gracias al detector amplio.

Las pruebas positivas preexistentes cubren páginas ASCII y paneles, incluido `f86v4` y `fRos`.

**Comando de regresión:** `python tests/test_ivtff_page_locus_ids.py`. Se ejecuta en `Voynich Check`; el resultado definitivo debe tomarse del run asociado a la PR. Los fixtures no usan aleatoriedad, semilla ni corpus externo para estos cuatro casos. El test completo también audita las tres transcripciones originales sin modificarlas.

## Preservación y límites

No se han cambiado corpus, manifiestos, resultados negativos, numeraciones EXP, `state/committed_claims.md`, lectores históricos ni políticas de tokenización. Esta reparación **no** prueba conformidad IVTFF completa, ni adjudica ligaduras/alternativas, ni autentica imágenes o folios, ni valida ninguna traducción. No se ha repetido ninguna simulación estadística.

**Siguiente paso:** comprobar CI en la PR, revisar diff y trabajo concurrente; integrar solo si supera controles, verificar el commit de `master` y la CI posterior.
