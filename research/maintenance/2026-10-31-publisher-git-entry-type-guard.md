# Publicador: rechazar entradas Git no regulares en nuevas salidas permitidas

**Fecha:** 2026-10-31. **Base inspeccionada:** `master` `0c4d078edfeb717a7987cadfb633aebc7dd52a7b` (publicación programada posterior a la CI verde del commit anterior). **Tipo:** reparación operativa acotada, sin EXP ni nueva afirmación científica.

## Problema verificable

El guard `scripts/check_publisher_source_drift.py` de las reparaciones del 30-10-2026 compara ascendencia, rutas y estados de cambios concurrentes, pero su excepción para adiciones `A` con nombre de resultado programado no inspeccionaba el tipo de objeto Git. Una adición con nombre permitido podía ser un **enlace simbólico** (modo Git `120000`) o un ejecutable (modo `100755`) y ser tratada como una salida de datos ordinaria. La coincidencia de nombre no prueba que el archivo sea un blob regular. No se ha observado tal objeto en las cuatro nuevas salidas del publicador; el defecto se demuestra por inyección de un objeto Git sintético.

## Criterio y cambio

Una adición concurrente se exime únicamente si: (1) la ruta coincide exactamente con una de las familias cerradas de resultados programados; (2) Git confirma que el objeto en el commit candidato es `100644 blob`; (3) el objeto corresponde a esa ruta exacta. El comando `git ls-tree -z <candidate> -- <path>` conserva los límites de nombres de archivo y no sigue symlinks. Cualquier modo no regular se registra como cambio bloqueante. Un fallo de Git o una entrada de árbol ambigua produce excepción, no aceptación.

No se altera la política de que cualquier modificación/borrado de un archivo existente bloquee la publicación. No se habilitan nombres adicionales. Las pruebas nuevas crean repositorios Git temporales y comprueban rechazo de un enlace `120000` y un archivo ejecutable `100755`, conservando la prueba positiva de adición regular `100644`.

## Reproducción y límites

Comandos previstos en la CI canónica:

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python scripts/audit_repository_operations.py
```

No se ha ejecutado cifrado, transcripción, predicción ni análisis de folios reservados. Semillas: no aplican (fixtures deterministas). Corpus, resultados históricos, hashes congelados, compromisos y scripts científicos: sin cambios. La CI de la rama y cualquier integración se deben comprobar por ID y SHA antes de declararlas satisfactorias.

**Límite importante:** este guard solo autentica **modo/tipo de Git y ruta** durante un rebase; no valida bytes, semántica, calidad de resultados ni prueba que el commit publicado tenga CI propia. El publicador con `GITHUB_TOKEN` no dispara una nueva CI `push` por sí solo. Las PR #7 y #138 requieren revisión científica; EXP-170 sigue bloqueado por procedencia exacta, y IVTFF y la conciliación de artefactos siguen abiertos. El objetivo de evaluación sigue siendo 22-11-2026, sin prometer descifrado.

## Autoauditoría

Sin calibración a métricas del manuscrito, sin transformación de características lingüísticas y sin extrapolación a teorías de cifrado. Control positivo esperado: nueva salida `100644` aceptada; controles adversariales esperados: `120000` y `100755` rechazados. No se deriva ninguna afirmación semántica ni científica de estos controles operativos.
