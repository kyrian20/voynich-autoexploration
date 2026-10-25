# EXP-593 — Protección de archivos fechados (25-10-2026)

**Tipo:** reparación operativa, sin EXP nuevo ni ensayo científico. **Estado:** propuesta pendiente de CI y revisión de integración.

## Incidencia y riesgo

`scripts/exp593_daiin_variants.py` escribe dos rutas construidas exclusivamente con la fecha UTC mediante `Path.write_text()`. El publicador `.github/workflows/voynich-agent.yml` puede ejecutarse por programación y por push sobre `master`; varias ejecuciones en un mismo día producen las mismas rutas. La escritura previa sustituía los bytes de archivos existentes, incluso si otra ejecución o una revisión humana los había modificado. No hay prueba de que se haya producido una sobrescritura histórica; sí existe el riesgo directo en el código.

Los archivos ya presentes `research/experiments/2026-10-25-exp593-corrected-L-metadata.{json,md}` y `2026-10-21-exp593-corrected-L-metadata.{json,md}` se mantienen intactos. **No son entradas para reproducir una ejecución histórica distinta**.

## Reparación propuesta

1. Antes de las 5.000 permutaciones, calcular fecha UTC, hash SHA-256 de la entrada efectivamente leída y nombres de salida.
2. Si ambos destinos existen, comprobar que son archivos regulares, no enlaces simbólicos, que el JSON declara el experimento, fecha, corpus, hash, semilla, permutaciones y variantes esperados, y que el informe coincide en fecha, hash, semilla y número de permutaciones. Si coincide, registrar `skipped_existing` y **no ejecutar** la simulación; este mensaje no certifica reproducción.
3. Si solo existe uno, o hay un archivo ilegible, un enlace simbólico o metadatos discordantes, fallar sin reemplazar ni reparar automáticamente. Requiere adjudicación explícita.
4. Si ninguno existe, ejecutar el algoritmo sin cambios y crear los dos archivos con modo exclusivo `x`, para impedir sustitución incluso ante carreras posteriores al control. Una interrupción entre ambas escrituras puede dejar un par incompleto: la siguiente ejecución lo rechazará.

La comparación de metadatos no certifica igualdad del contenido estadístico ni conformidad IVTFF. La política de archivo se limita a impedir pérdidas y trabajo redundante; no revalida las conclusiones.

## Procedencia y alcance

- Fuente histórica: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- Selección original: 4.188 líneas, 32.732 tokens; variantes `daiin`, `dain`, `daiiin`.
- Parámetros inalterados: 5.000 permutaciones, semilla `20261021`, nulo de permutación de orden dentro de línea, corrección max-T estandarizada.
- No se cambian corpus, scripts de otros EXP, particiones por folio, resultados históricos ni `state/committed_claims.md`.
- El conjunto de pruebas usa directorios temporales y `runpy`; no repite las permutaciones ni crea resultados científicos.

## Criterio de verificación

Ejecutar `python -m unittest discover -s tests -p 'test_exp593_archive_guard.py' -v` y `test_exp593_cwd_portability.py`; verificar `Voynich Check` de la cabeza de la PR y luego, si se integra, del commit exacto de `master`. Las regresiones cubren archivo nuevo, archivo existente idéntico, par incompleto, procedencia JSON/informe divergente, JSON corrupto, enlace simbólico y creación exclusiva. Mantener la PR sin fusionar si la CI no es satisfactoria.

**Interpretación:** saneamiento de publicación; ningún resultado nuevo de descifrado, ningún significado asignado, ninguna certificación global.
