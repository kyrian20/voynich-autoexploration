# Auditoría de bloqueo: asignación determinista de hojas del holdout v2

Fecha: 2026-10-26. Estado: **CORRECCIÓN PROPUESTA; CI REMOTA PENDIENTE**. No se crea EXP ni se afirma descifrado.

## Defecto concreto

El auditor `scripts/audit_holdout_locus_coverage.py` verificaba SHA-256 de las fuentes, presencia de hojas, recuentos, disyunción y cobertura total, pero **no** comprobaba que cada hoja perteneciera al grupo que le asigna el algoritmo determinista y la sal congelada del manifiesto. Un intercambio de una hoja `train` con una `test` de igual cardinalidad mantiene los recuentos, la unión, los hashes de corpus y la cobertura, y pasaba esa función. Este es un defecto de aceptación del auditor reutilizable, **no** evidencia de alteración del manifiesto histórico. La CI existente ya compara byte a byte el manifiesto regenerado: esa defensa permanece y esta reparación no la duplica como experimento.

## Criterio fijado antes de comprobar CI

Aceptar el manifiesto original v2 sin alterar fuentes ni asignaciones. Rechazar (a) intercambio de hojas entre train y test con idénticos recuentos; (b) sal modificada u omitida; (c) listas de partición no ordenadas. Mantener los controles sintéticos positivos y la verificación de correspondencia entre páginas y loci.

## Corrección y pruebas

Se fija **independientemente del generador** la sal `VOYNICH-FUTURE-RULES-2026-10-23-v1` y se calcula SHA-256 de `salt:leaf`; los primeros ocho bytes big-endian módulo 10000 determinan train <7000, development <8500 y test en el resto. El auditor comprueba cada hoja y exige la sal histórica. Los fixtures sintéticos pasan a usar f1=train, f4=development, f3=test y f67=train; el manifiesto congelado **no cambia**. Dos pruebas nuevas rechazan el intercambio de grupos y la sustitución/eliminación de sal.

Comandos de verificación previstos en CI (Python 3.12):

```sh
python -m unittest discover -s tests -p 'test_holdout_locus_coverage.py' -v
python -m unittest discover -s tests -p 'test_holdout_page_crosswalk.py' -v
python -m unittest discover -s tests -p 'test_committed_holdout_manifest_invariants.py' -v
python scripts/audit_holdout_locus_coverage.py --out holdout-locus-coverage.json
python scripts/audit_holdout_page_crosswalk.py --out holdout-page-crosswalk.json
cmp research/maintenance/2026-10-25-holdout-page-crosswalk/results.json holdout-page-crosswalk.json
```

Los tests y el auditor ya forman parte de `.github/workflows/voynich-check.yml`; no se añade un workflow ni se dispara una ejecución manual redundante. En la preparación local se cotejó con `hashlib.sha256` que f1=74/10000 (train), f3=8568/10000 (test), f4=7166/10000 (development), f67=2800/10000 (train). **Es una comprobación local del algoritmo, no la ejecución de la suite ni una reproducción histórica.**

## Procedencia y límites

Base de trabajo `master` `bcc2cbb4abfee3dead13e7b9dc3e04d2c526d2e8`. Fuente ZL3b `data/transcriptions/eva_zl3b.txt`, SHA-256 publicado `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. Estos hashes proceden del manifiesto congelado, **no de un nuevo recálculo local de ambos archivos**. No se modifican fuentes, manifiestos, scripts históricos ni resultados negativos. No hay semilla aleatoria: el algoritmo es determinista.

Esta corrección protege la identidad de los grupos prospectivos; **no** hace históricamente ciegos los folios, no valida la conformidad IVTFF completa, ni prueba ninguna hipótesis lingüística. No ejecutar experimentos semánticos mientras persistan bloqueos de adjudicación y referentes independientes.

## Seguimiento

Verificar ejecución CI de la PR en su SHA final; si es satisfactoria, integrar con comprobación de base actual y confirmar CI posterior. Si falla, conservar el fallo y corregir solo la causa demostrada.
