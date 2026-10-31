# Holdout: impedir identificadores de locus no ASCII en el lector de cobertura

**Fecha:** 2026-10-31. **Base inspeccionada:** `master` `c0387506bf72d5df79b690e8a6797e899ff4cb86` (CI push `41195329837`: success). **Clase:** reparación de integridad IVTFF, sin nuevo EXP ni inferencia semántica. **Estado inicial:** pendiente de CI específica y revisión de integración.

## Defecto acotado y evidencia adversarial

El lector independiente `scripts/audit_holdout_locus_coverage.py` aceptaba el código de localización con `[^;>]{3}` y el identificador de transcriptor con `[^;>]`. Por tanto, aceptaba como registros IVTFF estructurales, entre otros, `f67r.1,éP0`, `f67r.1,<P0`, `f67r.1, P0` y `f67r.1,@P0;é`. Una prueba local del patrón antiguo con `re.fullmatch` devolvió `True` en los cuatro casos; el patrón reparado devuelve `False`. Los ejemplos son sintéticos, no alteraciones observadas en las transcripciones congeladas.

El lector estricto `scripts/audit_ivtff_page_locus_ids.py` ya rechazaba estos códigos. La comparación cruzada de lectores en `audit_holdout_page_crosswalk.py` detectaba la discrepancia, pero la auditoría de cobertura ejecutada **por separado** podía certificar un inventario que incluyera registros mal formados. Este es el alcance exacto de la corrección.

## Reparación y criterio falsable

- `scripts/audit_holdout_locus_coverage.py`: restringir código de localización y transcriptor a ASCII imprimible excluyendo delimitadores de etiqueta, mediante `[!-:=?-~]{3}` y `[!-:=?-~]`. No ampliar el parser a afirmaciones de conformidad total.
- `tests/test_holdout_locus_coverage.py`: cuatro casos negativos de identificadores sintéticos y prueba adicional de `audit` que comprueba que el rechazo se mantiene **aunque el hash del corpus sintético coincida** con el manifiesto sintético.
- `.github/workflows/voynich-check.yml`: ejecutar las regresiones de cobertura en Python 3.12 normal y optimizado. Mantener los checks existentes de crosswalk y comparación de snapshot.

**Criterio de aceptación:** ambas modalidades de regresión pasan; el auditor de cobertura y el crosswalk de las fuentes congeladas pasan en la CI de la rama; el snapshot del crosswalk coincide byte a byte con el archivado; los artefactos y logs de la CI exacta se verifican. No integrar ni declarar éxito antes de completar esas comprobaciones. La prueba positiva ya existente conserva los identificadores `@P0`, `+P0` y `@L0`.

## Reproducibilidad y límites

Comandos: `python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v`, `python -O -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v`; CI también ejecuta `scripts/audit_holdout_locus_coverage.py --out holdout-locus-coverage.json` y el crosswalk con `cmp` del snapshot histórico.

Sin aleatoriedad ni semillas; unidad = identificador estructural de locus. No se leen palabras de folios test ni se evalúan hipótesis lingüísticas. Corpus, manifiestos, particiones, resultados históricos, hashes congelados y `state/committed_claims.md` permanecen intactos. Este control de forma **no prueba** independencia de lectores, conformidad IVTFF completa, validez estadística ni descifrado.

**Autoauditoría:** sin calibración contra una métrica Voynich; sin transformación de tokens ni mecanismo lingüístico; los únicos controles son identificadores sintéticos válidos/inválidos; no se extrapola a la totalidad del formato ni se retira una afirmación histórica. Continúan pendientes EXP-170 (identidad exacta de Naibbe/italiano), adjudicación IVTFF completa, conciliación de artefactos y revisión científica de PR #7/#138. Evaluación global: 22-11-2026, sin promesa de traducción.
