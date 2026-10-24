# IVTFF: rechazo de asignaciones Currier malformadas — 24-10-2026

**Tipo:** reparación de una puerta de validación; no EXP nuevo. **Base:** `master` `085648c2f2c92f9a1f45e3f4a0863e5a6134b6b7`. **Estado inicial:** propuesto, sujeto a CI y revisión.

## Defecto y reproducción acotada

`scripts/audit_ivtff_metadata_strict.py` llamaba a `legacy.parse_currier_language(metadata)` y, cuando esta devolvía `None`, omitía la cabecera. El lector heredado devuelve `None` tanto cuando **no hay** campo `$L` (válido: clase no especificada) como cuando **sí hay** un campo inválido, p. ej. `$L=C` o `$L=`. Además acepta dos asignaciones idénticas `$L=A $L=A` sin diagnóstico. Reproducción aislada anterior al parche: `$L=C -> None`, `$L= -> None`, `$L=A $L=A -> 'A'`, `$Q=A -> None`. No se afirma que esas cadenas estén presentes en las transcripciones originales.

La tabla 6 de IVTFF 2.0.2 limita `$L` (idioma de Currier) a `A` o `B`; `$Q` es quire y no sustituye `$L`. Fuente normativa: https://www.voynich.nu/software/ivtt/IVTFF_format.pdf, §6.3, tabla 6.

## Reparación

Se añade `strict_currier_language` **solo** al auditor estricto. Distingue ausencia legítima de `$L` de presencia inválida; exige una única asignación `$L=A` o `$L=B` y coteja el resultado con el lector heredado. Ante valores no permitidos, campos vacíos, duplicados o concatenaciones malformadas, falla con página y número de línea. Se conserva `scripts/audit_ivtff_metadata.py` sin modificaciones porque su hash forma parte de snapshots archivados de EXP-173.

Las regresiones sintéticas cubren cuatro formas inválidas, una segunda cabecera inválida tras una asignación válida y la ausencia legítima de `$L` con `$Q=A` y `$I=B`. Permanecen las pruebas anteriores de cabeceras repetidas A/B consistentes y contradictorias.

## Verificación exigida

```sh
python tests/test_ivtff_metadata_strict.py
python scripts/audit_ivtff_metadata_strict.py
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

La CI canónica ejecuta los dos primeros comandos y los contratos operativos. Un resultado verde acredita únicamente las rutas cubiertas por esos controles, no conformidad completa IVTFF.

## Integridad y límites

No se han modificado corpus, transcripciones, scripts históricos, resultados congelados, compromisos científicos, parámetros, semillas ni métricas. Los fixtures son deterministas (sin RNG). La corrección no adjudica las restantes reglas de IVTFF, no reproduce EXP-173 y no autoriza predicción confirmatoria por Currier A/B. No se atribuyen significados a palabras del manuscrito ni se declara traducción.
