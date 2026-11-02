# Auditoría acotada: interrogaciones IVTFF en el predictor de límites (30-10-2026)

**Tipo:** censo de procedencia y regresión de código, **no** EXP nuevo ni reejecución del predictor. **Estado de integración:** propuesta dependiente de PR #138; CI remota y fusión se documentan en su PR, no se presuponen aquí.

## Incidencia y criterio de aceptación

La reparación anterior que conserva `?` como barrera de continuidad no cuantificaba su presencia en las filas P reales. Una comparación de las transcripciones sin distinguir interrogaciones en comentarios y alternativas no seleccionadas podía exagerar el alcance del defecto.

Criterio **fijado antes de ejecutar CI**: los bytes SHA-256 de ambas fuentes deben coincidir con los originales; el censo de filas P y de signos `?` fuera de comentarios debe coincidir exactamente con la tabla; el censo de la lectura primaria debe descartar las alternativas no seleccionadas; cada fila que conserve un `?` seleccionado debe proyectar al menos una barrera `None`, también bajo `python -O`. Un fixture `[ch:?]` debe conservar `ch` en primaria, pero bloquearse al excluir palabras inciertas.

| Fuente | SHA-256 | Filas P | Filas con `?` bruto fuera de comentario | Signos brutos | Filas con `?` en lectura primaria | Signos en primaria |
|---|---|---:|---:|---:|---:|---:|
| ZL3b | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | 4.130 | 155 | 201 | 90 | 132 |
| IT2a | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | 4.118 | 67 | 129 | 67 | 129 |

Los recuentos se obtuvieron de una inspección independiente de las fuentes versionadas antes de fijarlos como expectativas. La prueba vuelve a contar las filas físicas mediante `checked_physical_lines`, comprueba las identidades SHA-256 y usa la selección de alternativas declarada por el lector. **Una fila que contenga `?` no equivale a un candidato estadístico retirado.** El censo no mide cuánto cambian AUC, AP, log-loss ni el número total de candidatos. Los signos en alternativas no elegidas pueden ser irrelevantes en primaria, pero no para la política que excluye toda la palabra incierta.

## Reproducción y controles

```bash
python -m unittest discover -s tests -p 'test_line_boundary_question_mark_scope.py' -v
python -O -m unittest discover -s tests -p 'test_line_boundary_question_mark_scope.py' -v
```

Código: `tests/test_line_boundary_question_mark_scope.py`; dependencia de lectura: `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py` en la rama de PR #138. Parámetros: `primary`, `drop_uncertain_word`, `preserve_gaps=True`. Semilla: no aplica (censo determinista). Control adversarial: `safe.[ch:?].clean` no debe crear un signo seleccionado en primaria; `safe.[?:ch].clean` sí debe preservar barrera. Los tests de barreras de candidatos ya existentes permanecen obligatorios.

## Límites y decisiones

La presencia de interrogaciones es una **observación estructural de la transcripción**, no una traducción. La tabla no atribuye a `?` todas las barreras de una fila: pueden coexistir comas inciertas, ligaduras, códigos high-ASCII o marcas de párrafo. No se compara contra la versión original congelada del predictor ni se reconstruye una salida histórica exacta. No se consumen folios reservados, no se ajusta modelo, no se cambian corpus, semillas, `results.json` ni afirmaciones comprometidas.

**Siguiente paso:** una vez integrada y verificada la regresión, priorizar las adjudicaciones IVTFF restantes y, solo cuando la puerta de integridad lo permita, realizar una reconstrucción separada y preregistrada de la población de candidatos y métricas. Hasta entonces, las cifras históricas de PR #138 siguen `INVALID_FOR_CLAIM` para el código corregido.
