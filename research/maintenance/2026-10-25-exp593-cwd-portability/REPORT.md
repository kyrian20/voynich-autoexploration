# EXP-593: ruta de trabajo ajena al repositorio — reparación acotada (25-10-2026)

**Clase:** incidencia operativa, no experimento nuevo. **Estado al abrir la PR:** pendiente de CI remota. No modifica resultados científicos ni adjudica IVTFF.

## Defecto reproducible por inspección

En el commit base `0b7e23387d6291dced96085502c0a9af1ec23b92`, `scripts/exp593_daiin_variants.py` (blob Git `28f07feebb5af707f528f376a2671e4543d35308`) define `SOURCE = Path("data/transcriptions/eva_zl3b.txt")` y `OUT = Path("research/experiments")`. Ambas rutas dependen del directorio de trabajo del proceso. Desde otro directorio `parse()` intenta abrir un archivo inexistente y `main()` podría escribir resultados en un destino ajeno al repositorio.

El mismo script añade la raíz del checkout a `sys.path`, pero eso **no** cambia la resolución de `Path` relativo. Este defecto afecta la portabilidad, no demuestra un error en los valores publicados previamente desde la raíz.

## Corrección y regresión

- Anclar `SOURCE` y `OUT` a `ROOT = Path(__file__).resolve().parents[1]`.
- Mantener el campo JSON `source` relativo al repositorio mediante `SOURCE.relative_to(ROOT)`; no introducir rutas absolutas de máquina en la procedencia publicada.
- Añadir `tests/test_exp593_cwd_portability.py`, que importa el script real desde un directorio temporal ajeno al checkout, invoca **solo** `parse()`, comprueba SHA-256 del corpus y la cobertura histórica, y verifica las rutas de entrada/salida.
- Ejecutar esa prueba en `.github/workflows/voynich-check.yml`. No añadir otra ejecución de las 5.000 permutaciones a la CI ni duplicar los experimentos históricos.

## Identidad y parámetros conservados

- Corpus: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- Universo **histórico restringido** de EXP-593: 4.188 líneas con tokens y 32.732 tokens; no sustituir por el universo más amplio de EXP-590.
- Variantes, semilla y permutaciones del script: `("daiin", "dain", "daiiin")`, `20261021`, `5000`.
- Originales `research/experiments/2026-10-25-exp593-corrected-L-metadata.{json,md}`: **sin modificar**. Tampoco se cambia el lector, la transcripción, el registro EXP ni las particiones por folio.

## Criterio de cierre y límites

Cerrar la incidencia solo si la regresión ejecutada desde cwd ajeno y la CI completa de la cabeza de la PR terminan satisfactoriamente; verificar también el commit exacto. No confundir ese cierre operativo con reproducción de las permutaciones históricas, conformidad completa IVTFF, validez inferencial o traducción. Si se fusiona, verificar aparte la CI posterior de master.

**Autoauditoría:** no se modifica selección de datos, nulo, estadística, semilla ni umbral; no se ensaya una hipótesis lingüística. El control adversarial es la ejecución desde cwd sin `data/`, que debe encontrar el corpus únicamente a través de `ROOT`. La prueba no pretende inferir semántica ni revalidar afirmaciones previas.
