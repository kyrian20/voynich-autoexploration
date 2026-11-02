# EXP-593 — invariantes de recuentos y partición Currier en el publicador

**Fecha:** 2026-11-02. **Base inicial:** `cecb7df1a413e8cab897fd8908672adf1d3f3de2` (`master` posterior a PR #253).
**Clase:** reparación operativa de integridad de artefactos; **no** es un EXP nuevo ni una reproducción de permutaciones.

## Incidencia concreta y criterio de cierre

El guardia de publicación concurrente `scripts/check_publisher_source_drift.py` (tras PR #253) exigía recuentos enteros no negativos para EXP-593, pero podía conceder una excepción de deriva de fuentes a un nuevo JSON con `occurrences > tokens`, `line_initial > lines`, una clase Currier ausente, subtotales incompatibles o `initial_fraction` contradictoria. El archivador EXP-593 ya contiene comprobaciones de coherencia relacionadas; el control de publicación no las aplicaba. No hay evidencia de que un JSON publicado real contenga esos defectos.

**Criterio falsable:** al intentar eximir un nuevo blob generado del rechazo de deriva, cualquiera de las siete mutaciones sintéticas debe producir `RuntimeError` con causa específica; los cuatro JSON originales publicados deben continuar aceptándose. La validación examina el blob del commit candidato, no el árbol de trabajo.

## Cambios

- `scripts/check_publisher_source_drift.py`: límites de apariciones/inicios/finales por tokens y líneas; partición exhaustiva A/B/unknown con enteros no negativos; límites por subgrupo; sumas exactas de ocurrencias/inicios/finales; coherencia de `initial_fraction` con tolerancia absoluta `1e-12` y sin booleanos.
- `tests/test_publisher_source_drift.py`: siete regresiones adversariales: apariciones > tokens, inicios > líneas, clase unknown ausente, subtotales que no suman, inicios de A > ocurrencias de A, booleano en subgrupo y fracción inicial incompatible. El control positivo existente utiliza los cuatro JSON archivados.

## Datos y conservación

Control positivo EXP-593: `research/experiments/2026-11-02-exp593-corrected-L-metadata.json`. Fuente declarada ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; semilla `20261021`; 5.000 permutaciones; 4.188 líneas y 32.732 tokens; variantes `daiin`, `dain`, `daiiin`. Particiones conservadas: daiin 726=440+278+8, dain 198=92+106+0, daiiin 19=11+8+0. No se recalculan estos resultados ni se afirma que los p-valores sean independientes del tokenizador.

No se modifican los corpus, los JSON/Markdown históricos, las semillas, los vectores de EXP-170, los manifiestos held-out ni `state/committed_claims.md`. Las siete entradas son mutaciones deterministas de fixtures, sin semilla nueva. El SHA Git de los archivos modificados y la CI exacta deben consultarse en la PR.

## Comprobaciones obligatorias

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

**Evidencia:** el resultado de estos comandos solo podrá declararse aprobado tras comprobar la ejecución de GitHub Actions para el SHA exacto de esta rama y, si se integra, el SHA posterior de `master`. Esta nota por sí sola no certifica que hayan pasado.

## Límites y siguiente acción

Es una puerta mínima de integridad, no una reproducción de EXP-593 ni validación estadística, IVTFF o semántica. No resuelve los inputs externos históricos de EXP-170, la adjudicación completa de corpus ni las contradicciones de compromisos. No se ejecuta un nuevo ciclo científico. Tras verificar CI, continuar con la recuperación verificable de entradas de EXP-170 y conciliación de artefactos; no sustituir originales faltantes por candidatos modernos.
