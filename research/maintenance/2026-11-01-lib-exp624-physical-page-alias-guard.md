# LIB-EXP-624 — alias de página física en las asignaciones corregidas

**Fecha:** 2026-11-01. **Tipo:** reparación de integridad, sin experimento lingüístico. **Base de trabajo:** `master` `86771faa95764fc3ca382c79d51ce794a16150d4`. **Estado científico:** `BLOCKED` para puntuación confirmatoria. **No se asigna EXP nuevo.**

## Incidencia concreta y criterio de aceptación

Los scripts derivados `prepare_library_exp624_leaf_grouped_splits.py` y `prepare_library_exp624_joint_strata.py` verificaban la unicidad de los identificadores crudos, pero no rechazaban dos identificadores diferentes que denotan **la misma página física**. Por ejemplo `f1r`/`f01r` y `f2r1`/`f002R1` se consideraban páginas distintas, aunque ambas variantes comparten número físico, cara y panel. El reparto por hoja impide que crucen train/test, pero la población y el peso de una página pueden duplicarse. Esta es una debilidad comprobable con entradas adversariales, no evidencia de duplicados en las transcripciones originales.

**Criterio previo:** ambas APIs deben rechazar duplicados físicos, incluidos ceros iniciales y diferencias de mayúsculas; los paneles distintos deben permanecer diferentes; el resultado sobre los corpus congelados debe conservar su población y semillas, y la CI no debe reejecutar modelos científicos.

## Corrección

- `physical_page_id()` convierte únicamente la identidad física en tupla `(hoja_entera, lado_minúscula, panel_entero_o_None)` después de validar sintaxis ASCII. No reescribe ni normaliza las transcripciones.
- `grouped_splits()` rechaza una segunda aparición de la misma tupla, además del rechazo existente de IDs crudos repetidos.
- `derive_joint_strata()` aplica la misma guardia al ser invocada directamente, incluso si se elude el generador agrupado.
- Se añaden regresiones adversariales en `tests/test_library_exp624_leaf_grouped_splits.py` y `tests/test_library_exp624_joint_strata.py`. Las pruebas congeladas ya existentes deben confirmar ausencia de regresiones.

## Procedencia y ejecución

Fuente ZL3b: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.

Fuente IT2a: `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

La implementación mantiene el generador LCG de 32 bits y Fisher–Yates, semilla inicial 624010, incremento 7919, ocho repeticiones globales, y la división de 70/30 por hoja. La serie A/B separada anterior usa 625010 y seis repeticiones y **no se rehabilita** para combinación entre estratos. El archivo histórico de la Biblioteca y sus resultados no se ejecutan ni modifican.

Pruebas esperadas en la CI existente, sin nuevas ejecuciones científicas: `python -m unittest tests.test_library_exp624_leaf_grouped_splits tests.test_library_exp624_joint_strata` y el modo optimizado equivalente con `python -O -m unittest`; verificar los pasos exactos y los artefactos del run antes de declarar éxito. Registro de partida: [CI de master 41280046922](https://github.com/kyrian20/voynich-autoexploration/actions/runs/41280046922), job `check` completado con 120 pasos y 30 artefactos listados, **sin auditoría individual de sus ZIP**.

## Alcance y límites

Se corrige una **guardia preventiva** de población, no un fallo observado en las fuentes originales. No se recuperan entradas externas de EXP-170, no se adjudica IVTFF y no se revalidan las 28 particiones históricas contaminadas de LIB-EXP-624. Las dos ediciones del mismo manuscrito no son réplicas independientes; la selección histórica sigue siendo permisiva y los folios ya han sido inspeccionados. No hay puntuación predictiva, prueba semántica ni traducción.

**Evidencia de integración:** consultar la PR asociada, sus logs CI y el commit posterior a integración. Si CI no termina, la reparación permanece sin cierre; no sustituir esta sección por afirmaciones anticipadas.
