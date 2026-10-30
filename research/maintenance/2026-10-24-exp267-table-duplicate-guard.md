# EXP-267: rechazo de filas duplicadas en la adjudicación de tablas — 24-10-2026

**Estado:** corrección propuesta; no experimento científico nuevo. Base congelada de esta rama: `9deb7af112dbf24585997630e400f8353f240b7b`. No modificar ni sustituir resultados históricos.

## Incidencia reproducible

`scripts/audit_reference_claim_links.py::parse_position_table` extraía seis celdas (Currier A/B × LF/MID/LL) del informe histórico de EXP-267. La implementación anterior construía primero un diccionario y comprobaba que contuviera seis claves. Si el informe añadía una séptima fila para una clave ya existente, el diccionario sobrescribía silenciosamente la primera. La auditoría podía aceptar un valor contradictorio y atribuirlo al informe congelado.

Fixture sintético de seis filas distintas más una séptima `B/LL`:
- duplicado idéntico: el código anterior aceptaba las siete filas;
- duplicado contradictorio: el código anterior aceptaba y retenía el último valor (por ejemplo, `999.0`);
- código propuesto: rechaza ambos antes de producir adjudicación;
- seis filas distintas: conserva la tabla original sin cambios.

La prueba de reproducción previa se hizo **solo sobre la función aislada**, sin importar ni ejecutar scripts históricos. No se atribuye a los archivos originales la presencia de duplicados: el defecto es un riesgo de lectura y validación, no una alteración observada del corpus.

## Reparación y controles

- `scripts/audit_reference_claim_links.py`: exige **exactamente una** fila reconocida por cada celda A/B × LF/MID/LL antes de convertir a diccionario.
- `tests/test_reference_claim_links.py`: dos nuevas regresiones sintéticas, para duplicado idéntico y contradictorio; se conserva el control existente de tabla válida y el rechazo de tabla incompleta.
- La CI canónica ya ejecuta `python tests/test_reference_claim_links.py` y `python scripts/audit_reference_claim_links.py --check research/maintenance/2026-10-22-claim-link-adjudication/results.json`. El snapshot debe permanecer idéntico.

**Evidencia local acotada:** ejecución aislada de las versiones anterior y propuesta con fixtures: seis filas válidas coinciden; ambos duplicados son aceptados por la versión anterior y rechazados por la nueva. Esta comprobación no equivale a ejecutar la suite completa del repositorio. La CI de la PR y la reproducción del snapshot deben comprobarse por SHA y ejecución antes de declarar integración.

## Integridad y límites

No se modifican `experiments/`, `data/`, `state/committed_claims.md`, `research/maintenance/2026-10-22-claim-link-adjudication/results.json` ni las decisiones históricas. El informe EXP-267 permanece identificado por blob Git `92c47d101d35543dabce569f877cbf98176db246`; EXP-288 por `c2c5711acf98c8779c179088275a4218699d3caf`. No hay semillas ni datos nuevos: los fixtures son deterministas y no usan aleatoriedad.

La reparación verifica unicidad de las filas **que coinciden con el patrón histórico**, no valida todas las formas posibles de tablas Markdown ni las conclusiones científicas de EXP-267. La fuente de control «latino» sigue siendo el Cicero bilingüe; las afirmaciones monolingües permanecen `INVALID_FOR_CLAIM`. La adjudicación IVTFF, el archivo histórico y la reconciliación de artefactos continúan pendientes.

## Criterio de cierre

1. Las dos regresiones nuevas y las anteriores pasan en CI.
2. La auditoría completa conserva el snapshot exacto de adjudicación, sin escribir sobre el original.
3. La PR se integra solo después de comprobar su ejecución y compatibilidad con el `master` actual; se comprueba de nuevo la CI del commit fusionado.

**Interpretación:** corrección de un control de integridad documental, no nueva evidencia de estructura lingüística, hipótesis semántica ni traducción del manuscrito.
