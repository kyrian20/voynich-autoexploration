# Reparación de la solicitud Gemini: metadatos IVTFF y folios reservados — 2026-10-25

**Tipo:** incidencia metodológica y de integración, sin EXP nuevo. **Estado de la propuesta:** pendiente de CI e integración (consultar PR y ejecución concreta). Ningún experimento ni petición nueva a Gemini forma parte de esta reparación.

## Problema comprobado

El prompt v1 `research/protocols/2026-10-24-gemini-ch-sh-review-prompt.md` indicaba `$Q=T` sin definir el significado del metadato, y pedía una partición holdout sin obligar a reutilizar el manifiesto existente. La revisión externa anterior interpretó `$Q` incorrectamente como calidad y propuso una partición no conciliada con los folios reservados. El error del revisor no demuestra que el parser local clasifique mal las líneas: se trata de un riesgo concreto de contaminación metodológica al reutilizar la propuesta.

## Corrección acotada

- Se preserva el prompt v1 sin alteraciones para que su hash siga identificando la revisión histórica.
- Se crea `research/protocols/2026-10-25-gemini-ch-sh-review-prompt-v2.md`: define `$Q` = quire, `$L` = clase Currier, `$I` = ilustración; exige manifiesto train/development/test y hashes antes de fijar el diseño; prohíbe nuevos splits y obliga a `needs_data` si faltan insumos.
- `scripts/request_gemini_review.py` utiliza v2 en futuras ejecuciones manuales. El recibo ya incorpora SHA-256 del prompt y de la respuesta.
- `.github/workflows/gemini-methodological-review.yml` cambia el sparse checkout y su verificación al nuevo prompt, manteniendo permisos `contents: read` y exclusión de corpus.
- `tests/test_gemini_review_request.py` comprueba los metadatos, el requisito de folios reservados, la permanencia de v1 y la concordancia entre ruta del script y checkout del workflow.

## Reproducción, límites y criterios de cierre

Comando de pruebas: `python -m unittest discover -s tests -p 'test_gemini_review_request.py' -v`. Verificar además `Voynich Check` en la PR y tras cualquier integración. Las pruebas son deterministas, no tienen semilla ni consumen API.

No se modifican corpus, scripts científicos, EXP, simulaciones, informes negativos ni artefactos históricos. Esta reparación **no revalida retrospectivamente** la respuesta de Gemini anterior ni convierte su propuesta en evidencia. El control de esquema sigue siendo sintáctico, no una revisión científica. Una nueva revisión solo se ejecutará mediante autorización manual, con recibo de versión v2 y adjudicación humana antes de aceptar hipótesis.

**Próximo paso científico condicionado:** confirmar metadatos y correspondencia de folios contra el IVTFF original y la partición ya registrada, y solo después considerar un contraste falsable fuera de los folios de entrenamiento. No hay traducción validada.
