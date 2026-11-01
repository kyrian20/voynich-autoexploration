# Corrección de alcance: mitades por páginas frente a hojas físicas

**Fecha:** 2026-11-01. **Clase:** defecto comprobado de independencia física en la reimplementación parcial Zhang–Sheng; no experimento nuevo, sin traducción.
**Base de la auditoría:** `master` `9875c0d209c688e30b648bab037689463b731d39`.
**Fuentes originales congeladas:** ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

## Incidencia falsable y población

El cálculo archivado de 54 filas (`results.json`) separa **páginas IVTFF** en bloques alternos de 10, no hojas físicas. En los 225 encabezados comunes de cada transcripción (se excluyen `f116v` y `fRos` como en `main()`), los paneles de cuatro hojas físicas aparecen en **ambas** mitades. La enumeración independiente de cabeceras, en orden de fuente y con índices de base cero, arroja el mismo resultado en ZL3b e IT2a:

| Hoja | Mitad 1 (índice impar de bloque) | Mitad 0 (índice par de bloque) |
| --- | --- | --- |
| `f67` | `f67r1` (118), `f67r2` (119) | `f67v2` (120), `f67v1` (121) |
| `f72` | `f72r1` (136), `f72r2` (137), `f72r3` (138), `f72v3` (139) | `f72v2` (140), `f72v1` (141) |
| `f90` | `f90r1` (178), `f90r2` (179) | `f90v2` (180), `f90v1` (181) |
| `f102` | `f102r1` (198), `f102r2` (199) | `f102v2` (200), `f102v1` (201) |

**Criterio de falsación:** `audit_page_half_leakage()` debe detectar exactamente esas cuatro hojas en ambas fuentes; `require_disjoint_physical_leaves()` debe rechazar el split histórico antes de una evaluación que exija hojas físicamente independientes, sin rechazar paneles de una misma hoja que estén en la misma mitad. Los tests también cubren alias numéricos, hojas inválidas y parámetros de bloque incorrectos.

## Reparación y alcance

`wordpair_audit.py` añade el diagnóstico de pertenencia a hoja física y una puerta explícita `require_leaf_independence=True` que **falla antes del cálculo** cuando una hoja aparece en ambas mitades. La ruta histórica por defecto permanece disponible exclusivamente para reproducir y auditar el archivo congelado; cada resultado en memoria incluye `split_diagnostics` y advierte de que no es una partición independiente por hoja. `flatten_run_records()` conserva exactamente el contrato plano archivado.

**Adjudicación:** las correlaciones numéricas del archivo original se **conservan** como descripciones de mitades de páginas del mismo manuscrito. **No son válidas para la afirmación específica de evaluación con hojas físicas independientes.** No se sustituyen por una nueva partición ni se reinterpretan como puntuaciones de folios reservados. El método descrito por Zhang–Sheng también usa bloques de páginas; esta incidencia no demuestra un error de su artículo, sino una limitación concreta de nuestra reimplementación para extrapolaciones de independencia física.

## Evidencia y reproducción

```sh
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
python scripts/check_corpus_integrity.py
```

No se han modificado las fuentes, `results.json` (54 filas), las 20 permutaciones/semillas 20261101–20261103, los resultados negativos, los manifiestos reservados ni `state/committed_claims.md`. La prueba numérica acotada sigue cubriendo solo **2/54** filas. Los resultados de esta corrección requieren verificar CI de la PR y del commit de `master` antes de declarar cierre.

## Próximo paso y limitaciones

Para cualquier evaluación independiente por hoja, definir **antes de ejecutar** una partición por identidad física completa, validarla contra los manifiestos reservados y no comparar sus métricas con el archivo histórico como si usara el mismo universo. La conciliación IVTFF integral, EXP-170 y la reproducción exacta del artículo continúan pendientes. No se ejecutan ciclos científicos prohibidos por contradicciones pendientes. Evaluación general: **22-11-2026**, sin garantía de descifrado.
