# Sensibilidad de candidatos a eliminar literalmente `?` (30-10-2026)

**Estado:** auditoría de integridad acotada, sin EXP nuevo. **No es una reconstrucción histórica**, no ejecuta el predictor, no usa folios reservados ni rehabilita métricas `INVALID_FOR_CLAIM`. Base de trabajo: cabeza verificada de PR #138 `5c436dfd78f8663001436952cbb95454641f25b9`; `master` observado en `342b4dd0eaf36e4b2ee94cc2628378b0ae47320b`.

## Pregunta falsable y regla fijada antes de CI

El censo anterior de 90/67 filas P con interrogación seleccionada no demuestra cuántos pares candidatos dependen de conservar esas barreras. Pregunta: **¿cómo cambia la población de candidatos, positivos entre filas y negativos dentro de línea, si se suprimen los caracteres literales `?` en los mismos cuerpos fuente, manteniendo el resto del lector corregido?**

Se calculan dos brazos para ZL3b e IT2a y ambas políticas `primary`/`drop_uncertain_word`: (1) lector corregido sin cambios y (2) contrafactual `body.replace("?", "")` sobre las **mismas filas físicas P**, antes de aplicar `tokens(..., preserve_gaps=True)`. Se conservan exactamente los identificadores, ordinales, loci no-P interpuestos, pertenencia a página y reglas actuales de tokenización. El conteo `(negativos, positivos)` procede del mismo constructor `candidates()`. Se registra la diferencia firmada `contrafactual - corregido` por clase y fuente. **No se fija un tamaño de efecto esperado**: las diferencias, incluso cero o negativas, se archivarán como observaciones, no se reajustará el protocolo para obtener un resultado deseado.

**Control sintético:** `alpha.?` seguido por `beta` con ordinal consecutivo no debe generar positivo con la barrera, pero sí un positivo al borrar el signo. `[ch:?]` no debe alterar la población primaria porque el interrogante está en la alternativa no seleccionada. Se exige conservar hashes de ambas fuentes, páginas, filas, ordinales y loci entre los dos brazos; no se cambia `results.json`.

## Entradas, ejecución y reproducibilidad

- ZL3b: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: `data/transcriptions/eva_it2a.txt`, SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- Script/fixture reproducible: `tests/test_line_boundary_question_mark_scope.py`; lector: `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py`.
- Comandos: `python -m unittest discover -s tests -p 'test_line_boundary_question_mark_scope.py' -v` y `python -O -m unittest discover -s tests -p 'test_line_boundary_question_mark_scope.py' -v`. Python 3.12 en CI. Semilla: no aplica; no hay muestreo ni entrenamiento.
- La CI de PR ejecuta ambos modos y archiva logs con SHA-256 en el artefacto `line-boundary-question-scope-<run_id>`. El registro numérico se obtiene de líneas `QUESTION_CANDIDATES` del job correspondiente. **No afirmar resultados hasta consultar la CI real.**

## Interpretación y limitaciones

La supresión literal de `?` es una sensibilidad artificial **con el lector actual**: no es el comportamiento íntegro de ninguna versión histórica, ni atribuye toda diferencia a una sola corrección pasada. Otros signos IVTFF, anotaciones, políticas de alternativas, comas inciertas y barreras de párrafo pueden interactuar con la supresión. Los dos testigos son transcripciones alternativas del mismo manuscrito, no réplicas independientes. Una variación de candidatos no implica cambio en AUC, AP, log-loss, idioma, significado ni validez científica. Los resultados históricos del predictor permanecen `INVALID_FOR_CLAIM` hasta reconstrucción completa y adjudicación IVTFF.

## Autoauditoría (cinco comprobaciones)

- **Target-awareness:** se estudia el signo literal `?` porque ya era una barrera de integridad documentada; no se seleccionan umbrales ni candidatos por rendimiento predictivo.
- **Feature-destroying:** borrar `?` puede fusionar unidades o promover pares inciertos; precisamente se cuantifica esta sensibilidad y **no** se presenta como prueba justa de un mecanismo lingüístico.
- **Extrapolación:** solo dos corpus congelados, dos políticas y este contrafactual; no se generaliza a otros transcriptores ni al manuscrito físico.
- **Resultado negativo:** un delta cero no prueba que el lector sea correcto; un delta distinto de cero tampoco demuestra mejora predictiva.
- **Control:** se espera cero positivo con `alpha.?`→`beta` y uno al borrar `?`; el caso de alternativa no seleccionada debe ser invariante. La observación efectiva y el estado CI se consignarán tras ejecución.

**Siguiente paso:** comprobar resultados y logs de CI; si pasan, integrar exclusivamente en la rama de PR #138, comprobar CI posterior y archivar conteos exactos. No ejecutar ciclos científicos mientras persistan las contradicciones y adjudicaciones pendientes.
