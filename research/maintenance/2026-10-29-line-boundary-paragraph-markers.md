# Corrección acotada: marcadores IVTFF de párrafo y candidatos de límites de línea

Fecha: 2026-10-29. Rama base: `codex/line-boundary-leaf-replication-20261028`, commit `d930ef6ca20dc19eb7d337d6ccfc2fae72061082`. No se asigna EXP nuevo.

## Defecto y regla comprobable

El lector de la réplica de límites de línea reemplazaba todas las etiquetas `<...>` por espacios. Los marcadores IVTFF `<%>` (inicio de párrafo) y `<$>` (fin de párrafo) son delimitadores estructurales (IVTFF 2.0.2, §6.7–6.9), no separadores ordinarios entre palabras. La interpretación anterior permitía un candidato positivo artificial entre `<f1r.P.1,P0> alpha<$>` y `<f1r.P.2,P0> beta`, y también uno negativo entre `alpha<%>beta` dentro de una fila.

Política conservadora propuesta: preservar un `None` como barrera en la lista de palabras para cada marcador explícito de párrafo. Esto no reconstruye los párrafos visuales ni adjudica la continuidad entre loci. Los comentarios libres `<!...>` se retiran antes de interpretar marcadores para no confundir texto editorial con etiquetas.

## Regresiones y alcance

El test `tests/test_line_boundary_paragraph_markers.py` verifica con fixtures sintéticas el bloqueo de candidatos falsos entre filas y dentro de la fila, y que espacios ordinarios, interrupciones de dibujo y comentarios libres mantienen su contrato anterior. Comprueba además SHA-256 de ZL3b e IT2a **antes** de una auditoría diferencial de candidatos. El contrafactual de alcance sustituye solo `<%>` y `<$>` por espacios, reproduciendo exactamente la política anterior para esas etiquetas en las filas afectadas; no sustituye corpus, no es una reproducción del estudio histórico ni estima nuevas AUC.

Comandos de regresión:
```sh
python -m unittest discover -s tests -p 'test_line_boundary_paragraph_markers.py' -v
python -O -m unittest discover -s tests -p 'test_line_boundary_paragraph_markers.py' -v
```
La CI de la rama debe comprobar estas pruebas y las regresiones existentes; no atribuirles estado verde antes de inspeccionar la ejecución. Las cifras exactas de filas afectadas y candidatos retirados deben extraerse de logs del run comprobado, no suponerse.

## Integridad y limitaciones

- `results.json` histórico, corpus, semillas y particiones reservadas se mantienen intactos. Las métricas históricas siguen `INVALID_FOR_CLAIM` como evaluación del lector corregido.
- La política de barrera es una decisión metodológica conservadora; no demuestra que todas las líneas físicamente adyacentes sean separadas por párrafos, ni una traducción.
- La inspección de marcadores no sustituye la adjudicación IVTFF completa, la conciliación de EXP-170 ni la auditoría global de artefactos.
- No se ejecuta el predictor ni se abre un conjunto prospectivo de hojas reservadas.
- Auditoría de los cinco riesgos de `skills/audit_experiment.md`: sin ajuste a una métrica Voynich, no se infiere señal científica; las barreras eliminan candidatos por diseño y pueden reducir cobertura; el alcance se limita a la construcción de pares; los resultados negativos se preservan; el control sintético sin marcadores debe permanecer inalterado.

Siguiente paso: inspeccionar logs y diferencias reales, comprobar compatibilidad con otras reparaciones concurrentes y solo integrar si CI y pruebas relevantes son satisfactorias.
