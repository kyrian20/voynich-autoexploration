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

## Resultados observados y congelación de regresión

**Primera CI verificada:** [Voynich Check #41018119008](https://github.com/kyrian20/voynich-autoexploration/actions/runs/41018119008), cabeza `df96376d0ab1409225f11330da02d09d7ff50fba`, `success`, job `123938966359`. Los cuatro tests de este archivo pasaron en Python normal y `-O`; se inspeccionaron ambas secciones de logs `QUESTION_CANDIDATES`, que coinciden. Artefacto `line-boundary-question-scope-41018119008` (ID 12961035904, 1.804 bytes según log), con logs y archivo de SHA-256. Se comprobó publicación del ZIP, **no** se extrajo ni auditó su contenido individualmente.

| Fuente | Política | Corregido negativos | Corregido positivos | Borrando `?` negativos | Borrando `?` positivos | Δ negativos | Δ positivos |
|---|---|---:|---:|---:|---:|---:|---:|
| ZL3b | primary | 24.270 | 2.554 | 24.400 | 2.576 | **+130** | **+22** |
| ZL3b | drop_uncertain_word | 23.534 | 2.417 | 23.598 | 2.427 | **+64** | **+10** |
| IT2a | primary | 30.244 | 3.291 | 30.368 | 3.307 | **+124** | **+16** |
| IT2a | drop_uncertain_word | 30.244 | 3.291 | 30.368 | 3.307 | **+124** | **+16** |

**Interpretación limitada:** eliminar literalmente interrogantes con el lector actual añade entre 74 y 152 pares candidatos por fuente/política (sumando las dos clases). Es una diferencia de **población de candidatos**, no una variación de puntuaciones, ni una reproducción del predictor histórico. En IT2a ambas políticas coinciden para este contraste; no se infiere independencia de las fuentes. El efecto está condicionado por el resto de barreras y filtros ya corregidos.

Tras inspeccionar esta primera CI, los ocho recuentos por fuente/política se fijaron **a posteriori como snapshots de regresión** en `EXPECTED_CANDIDATE_TOTALS`, sin presentarlos como expectativas predeclaradas ni como evidencia estadística independiente. La segunda CI del commit con estos snapshots debe verificarse por separado antes de integrar.

## Interpretación y limitaciones

La supresión literal de `?` es una sensibilidad artificial **con el lector actual**: no es el comportamiento íntegro de ninguna versión histórica, ni atribuye toda diferencia a una sola corrección pasada. Otros signos IVTFF, anotaciones, políticas de alternativas, comas inciertas y barreras de párrafo pueden interactuar con la supresión. Los dos testigos son transcripciones alternativas del mismo manuscrito, no réplicas independientes. Una variación de candidatos no implica cambio en AUC, AP, log-loss, idioma, significado ni validez científica. Los resultados históricos del predictor permanecen `INVALID_FOR_CLAIM` hasta reconstrucción completa y adjudicación IVTFF.

## Autoauditoría (cinco comprobaciones)

- **Target-awareness:** se estudia el signo literal `?` porque ya era una barrera de integridad documentada; no se seleccionan umbrales ni candidatos por rendimiento predictivo.
- **Feature-destroying:** borrar `?` puede fusionar unidades o promover pares inciertos; precisamente se cuantifica esta sensibilidad y **no** se presenta como prueba justa de un mecanismo lingüístico.
- **Extrapolación:** solo dos corpus congelados, dos políticas y este contrafactual; no se generaliza a otros transcriptores ni al manuscrito físico.
- **Resultado negativo:** un delta cero no prueba que el lector sea correcto; un delta distinto de cero tampoco demuestra mejora predictiva.
- **Control:** se espera cero positivo con `alpha.?`→`beta` y uno al borrar `?`; el caso de alternativa no seleccionada debe ser invariante. La observación efectiva y el estado CI se consignarán tras ejecución.

**Siguiente paso:** comprobar resultados y logs de CI; si pasan, integrar exclusivamente en la rama de PR #138, comprobar CI posterior y archivar conteos exactos. No ejecutar ciclos científicos mientras persistan las contradicciones y adjudicaciones pendientes.
