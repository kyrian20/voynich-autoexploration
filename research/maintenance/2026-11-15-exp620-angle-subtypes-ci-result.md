# EXP-620 — censo de subtipos angulares, CI exacta (2026-11-15)

## Procedencia y ejecución

- Rama de propuesta: `audit/exp620-legacy-ligature-differential-20261114`; commit ejecutado: `7284d5f7e342e24ffb8a044a29a56192b977f51e`.
- GitHub Actions: https://github.com/kyrian20/voynich-autoexploration/actions/runs/43655772602 ; job `132633827766`, conclusión `success`.
- Artefacto: https://github.com/kyrian20/voynich-autoexploration/actions/runs/43655772602/artifacts/14138180774 ; contiene `exp620-angle-subtypes.json` y `exp620-angle-subtypes.sha256`, retención configurada de 90 días.
- Digest SHA-256 del ZIP comunicado por el log de Actions: `92e9cdb131da85ad4483c5da7f26a725f71525a3657dc03cd47b9103c426d57f`. No se ha verificado independientemente el ZIP descomprimido.
- Comando: `python -m py_compile research/maintenance/exp620_angle_record_subtypes.py && python research/maintenance/exp620_angle_record_subtypes.py | tee exp620-angle-subtypes.json`; seguido de `python -m json.tool` y `sha256sum` en CI. No hay semilla aleatoria.

## Resultado observado en stdout de CI

| Entrada congelada | SHA-256 | Registros angulares excluidos | other_f_prefixed_tag | Otros subtipos |
|---|---|---:|---:|---:|
| `data/transcriptions/eva_zl3b.txt` | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | 1231 | 1231 | 0 |
| `data/transcriptions/eva_it2a.txt` | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | 1066 | 1066 | 0 |

Todos los 2297 registros angulares excluidos quedan en la categoría léxica residual `other_f_prefixed_tag`; no se ha encontrado ningún `bare_folio_tag`, `numbered_folio_locus_other_shape`, `folio_locus_non_numeric`, `bang_tag` u `other_tag` en ese conjunto. Esto **no** implica que los 2297 sean inválidos IVTFF, ni que deban procesarse como texto, ni que contengan eventos `ch/sh`.

## Alcance y próximo bloqueo

La clasificación residual es demasiado amplia para adjudicar elegibilidad. El siguiente trabajo no debe repetir el censo: inspeccionar las etiquetas literales y su sintaxis IVTFF, por ejemplo en las líneas físicas ZL3b 2815/2823 y IT2a 1767/1768, y contrastar con la especificación antes de cambiar lectores o afirmaciones históricas. Los números son posiciones físicas de ejemplo, no identificadores de folio. No se alteraron entradas, analizadores ni resultados congelados. Esta prueba es descriptiva y no una traducción.
