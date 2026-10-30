# Publicador: comprobar ascendencia del commit antes de rebase (2026-10-30)

**Estado inicial:** reparación propuesta, pendiente de CI de la PR y de verificación de integración. **Tipo:** integridad de procedencia, no EXP nuevo ni prueba lingüística. Base: `master` `ede52be003c453e9d4206cc11bd29431e94963a5`.

## Defecto falsable

`scripts/check_publisher_source_drift.py` compara los árboles del commit que generó los resultados y del `origin/master` actual mediante `git diff --name-status`. Si `master` se reescribe o se apunta a una historia divergente con **idéntico contenido de archivos**, `git diff` está vacío y el guard original permite la publicación. Un árbol idéntico no acredita que el commit de destino descienda del commit de generación. Esto no demuestra que el repositorio haya sufrido un reescrito real; es un fallo del contrato reproducido con Git local.

En una prueba local determinista con un repositorio temporal se crearon dos commits divergentes con árboles idénticos. `git merge-base --is-ancestor <generating> <replacement>` devolvió 1 y la función anterior devolvió `[]` (aceptación incorrecta). El resultado anterior a la reparación queda documentado aquí, no se modifica ningún histórico.

## Reparación y criterio previo

Antes del diff de rutas, ejecutar `git merge-base --is-ancestor baseline candidate`. Solo código de salida 0 permite continuar. Código 1 rechaza destino no descendiente; cualquier otro error Git (por ejemplo ref desconocido) falla cerrado. Se conserva el filtro de adiciones autorizadas de PR #162 y la comparación byte-safe de rutas; no se añaden excepciones para evidencias históricas.

**Aceptación:** un candidato divergente con árboles idénticos y un ancestro anterior deben rechazarse; el mismo commit y un descendiente legítimo con árbol idéntico deben aceptarse; las regresiones existentes sobre cambios de scripts, corpus y evidencia histórica deben seguir pasando.

## Reproducción

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python scripts/audit_repository_operations.py
```

La reproducción local aislada del defecto y la corrección incluyó cuatro pruebas de ascendencia (4/4 en Python normal y 4/4 en `-O`) usando repositorios Git temporales, sin aleatoriedad ni corpus. La CI del checkout real y la suite completa deben verificarse por SHA; no se declaran aprobadas de antemano. El workflow ya utiliza `fetch-depth: 0` y hace fetch antes de ejecutar el guard.

## Integridad y límites

No se modifican transcripciones, fuentes históricas, resultados negativos, scripts científicos, semillas, particiones reservadas, `state/committed_claims.md` ni el algoritmo de predicción. La prueba no consume folios. Este cambio impide un caso de publicación con historia no descendiente; no certifica el contenido de los resultados ni demuestra que se haya producido ese ataque o accidente en master. Tampoco resuelve la adjudicación IVTFF, los inputs históricos de EXP-170, la conciliación con Biblioteca ni la condición `INVALID_FOR_CLAIM` del predictor de PR #138.

**Siguiente paso:** verificar la CI de la PR y la CI del SHA exacto de master si se integra; continuar con la discrepancia IVTFF de impacto sobre candidatos reales antes de nuevos experimentos confirmatorios.
