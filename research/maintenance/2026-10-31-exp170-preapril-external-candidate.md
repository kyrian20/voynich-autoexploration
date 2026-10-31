# EXP-170 — existencia preabril del candidato externo Naibbe (auditoría de procedencia)

**Fecha:** 2026-10-31. **Base de partida:** `master` `4936f8d6da64980db07ff5f7b1f6b6333898946d`. **Clase:** conciliación de procedencia, **sin experimento científico** ni ejecución de Naibbe. **Estado de reproducción histórica exacta:** **BLOCKED**.

## Pregunta concreta

El registro de fuentes citaba el commit externo `719f2f4c4d1eacf95fabf48381cd84fc6cd94279` (19-10-2026), posterior a la incorporación de EXP-170 (10-04-2026). ¿Existían ya los **mismos blobs** de código, tablas e italiano en un commit anterior al experimento? Una respuesta afirmativa elimina solo la objeción de **imposibilidad temporal** de este candidato, pero no acredita qué archivos se utilizaron realmente.

## Evidencia recuperada y comprobada

Se consultó la historia de commits del repositorio público `greshko/naibbe-cipher` hasta el 10-04-2026 y se identificó el commit `d9cab18fafaca29610515753193806652cb019f2` (28-09-2025, 15:00:37 UTC). Se recuperaron **ambos árboles recursivos** mediante GitHub REST; ambos informaron `truncated=false`. Los tres objetos Git siguientes tienen **el mismo blob SHA-1 y tamaño** en el commit de 2025 y en el commit de 2026:

| Ruta externa | Blob SHA-1 (ambos commits) | Bytes |
| --- | --- | ---: |
| `naibbe_v2.py` | `b566ad82e4b6ff0782ecdddebf77718dac44f292` | 11626 |
| `references/naibbe_tables.csv` | `5cd34fb81d80faf3b4d57dbf1719c05ffde25302` | 8913 |
| `input/examples/divina_commedia.txt` | `2f57181cca66ab61d8719e35778d6b06688ee8be` | 1112569 |

Objetos y fechas comprobables:

- [Árbol Git externo del 28-09-2025](https://api.github.com/repos/greshko/naibbe-cipher/git/trees/d9cab18fafaca29610515753193806652cb019f2?recursive=1), SHA del árbol `263896a7b28ce5b7cf501d389cc3ec5908d9e099`.
- [Árbol Git externo del 19-10-2026](https://api.github.com/repos/greshko/naibbe-cipher/git/trees/719f2f4c4d1eacf95fabf48381cd84fc6cd94279?recursive=1), SHA del árbol `be16bb4cdd327769c3c19addee401195cff7a8f2`.
- [Commit externo de 2025](https://github.com/greshko/naibbe-cipher/commit/d9cab18fafaca29610515753193806652cb019f2) y [commit externo de 2026](https://github.com/greshko/naibbe-cipher/commit/719f2f4c4d1eacf95fabf48381cd84fc6cd94279).
- [Commit original EXP-170](https://github.com/kyrian20/voynich-autoexploration/commit/bfa786767d61a2c52bfb7a34a10d8b81ab777230), fechado 10-04-2026 06:19:47 UTC.

La identidad de blob Git demuestra identidad de **contenido** de esos tres archivos entre las dos revisiones externas. No se compararon en este bloque bytes contra un snapshot externo del proceso histórico de abril: ese snapshot no está acreditado.

## Reparación de trazabilidad

El registro `research/external/2026-10-22-professional-sources/registry.json` conserva el commit de octubre y añade `pre_experiment_candidate` con el commit anterior, fechas, árboles, tres identidades de blob, fuentes de evidencia y **`historical_identity_proven: false`**. No se sustituye el commit previamente registrado ni se etiqueta la fuente de 2025 como entrada histórica confirmada.

Se incorpora una regresión offline en `tests/test_exp170_isolated_reconstruction.py` que fija las tres identidades de blob y tamaños, el orden temporal, el commit EXP-170 original y el estado explícito de **candidato no demostrado**. Ejecutar:

```sh
python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python -O -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
```

Esta prueba verifica la **consistencia del registro congelado**, no consulta la API de GitHub. Las consultas independientes a los árboles se hicieron antes de registrar sus valores. La ejecución de CI debe comprobarse por SHA exacto antes de declarar aprobada la regresión.

## Decisión y límites

**Resuelto de forma acotada:** existe un candidato externo **temporalmente disponible antes del 10-04-2026** cuyos tres blobs coinciden exactamente con los del commit externo citado en octubre. **No resuelto:** no existe recibo de la ejecución histórica que pruebe que EXP-170 utilizó esos bytes, ni que el italiano de ese repositorio sea la entrada histórica exacta, ni las dependencias, versiones, semillas efectivas y salidas individuales. La ruta `latin` histórica apunta a inglés y sigue sin convertirse en un control latino. Por tanto, **EXP-170 permanece BLOCKED para reproducción histórica exacta** y sus 400 vectores congelados no se rehabilitan.

No se han modificado corpus, scripts históricos, simulaciones, parámetros, particiones reservadas, hashes originales, resultados negativos ni `state/committed_claims.md`. No se ejecutan nuevos ciclos científicos ante contradicciones pendientes. **Siguiente paso:** buscar recibos originales o archivos externos con hashes verificables que vinculen explícitamente la ejecución de abril con estos tres blobs; sin ello, cualquier ejecución sería reconstrucción moderna no validada. Evaluación global: 22-11-2026, sin promesa de descifrado.
