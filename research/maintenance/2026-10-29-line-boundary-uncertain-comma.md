# Reparación de límites de línea: la coma IVTFF no es un espacio cierto

**Fecha:** 29-10-2026. **Estado inicial:** parche propuesto, CI e integración por comprobar. No se asigna EXP. Trabajo sobre la rama de PR #138 `codex/line-boundary-leaf-replication-20261028`, SHA de partida `187dd2889c2db01c328bf00938f4dbf04137dc14`; `master` en `1bce529f2dd4f572f05489443c7a4579e9c0894f`. PR abiertas comprobadas: #5, #7, #13, #66, #82 y #138. La PR #138 es un borrador; esta reparación no se integra en `master`.

## Defecto y criterio antes de la CI

El predictor `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py` aplicaba `re.split(r"[.\\s,]+", body)`. Así, `alpha,beta` producía dos palabras inequívocas y un candidato negativo (sin salto de línea), y `alpha,beta` seguido de `gamma` podía generar un candidato positivo `beta→gamma`. **Pero la coma es un espacio de palabra incierto**, no una separación segura, según IVTFF 2.0.2, §6.7. Esta distinción ya figura en `research/ivtff_tokenization_policy_2026-10-20.md`. El código anterior era una política de separación posible, pero el análisis no la distinguía de un límite cierto; **no está justificado tratar sus fragmentos como palabras observadas sin incertidumbre**.

**Regla conservadora:** una coma y los dos fragmentos adyacentes quedan en una sola unidad no adjudicada (`None`) para la construcción de candidatos; no se inventa ni unión ni división. Un punto y los marcadores `<->`/`<~>` siguen siendo separadores ciertos. La opción explícita `uncertain_space_policy="split"` conserva el comportamiento previo para un contrafactual condicional, **no** para reconstruir el `results.json` histórico. Ambas políticas de lectura (`primary` y `drop_uncertain_word`) emplean la cuarentena por defecto. Los posibles espacios de formato alrededor de la coma tampoco habilitan palabras ficticias.

**Criterios falsables predefinidos:** (1) `alpha,beta` no produce dos palabras ciertas ni un salto entre filas; (2) `alpha.beta,gamma.delta.epsilon` conserva únicamente la pareja cierta `delta→epsilon`; (3) puntos, dibujos y comentarios conservan su comportamiento; (4) `split` reproduce la política de coma previa; (5) en fuentes congeladas el número de candidatos no aumenta al poner barreras; (6) IT2a, sin comas P, debe permanecer sin diferencias.

## Fuentes y auditoría acotada

Se consultaron las transcripciones versionadas **sin modificarlas**, y se inspeccionaron los cuerpos de los loci P, excluyendo identificadores y comentarios libres. El censo de entrada antes de CI halló:

| Fuente | SHA-256 exigido | Filas P con coma | Comas en filas P |
|---|---|---:|---:|
| ZL3b | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | 1.700 | 2.463 |
| IT2a | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | 0 | 0 |

La regresión Python verifica estos hashes y censos antes de comparar `parse(..., uncertain_space_policy="split")` con `parse(..., uncertain_space_policy="quarantine")`. El contrafactual conserva el resto de las reparaciones anteriores; **no** es una repetición histórica de los resultados originales ni una evaluación predictiva. Los conteos de candidatos retirados deberán extraerse de los logs CI, no inventarse a partir de las 2.463 comas.

Comandos de regresión (Python 3.12, sin dependencias nuevas):

```sh
python -m unittest discover -s tests -p 'test_line_boundary_uncertain_comma.py' -v
python -O -m unittest discover -s tests -p 'test_line_boundary_uncertain_comma.py' -v
```

La CI debe ejecutar estas pruebas junto a las regresiones previas. La comprobación del SHA del commit y de la ejecución posterior a una integración es independiente.

## Integridad y autoauditoría

- **Sin calibración al objetivo:** la distinción procede de la norma IVTFF, no de AUC, log-loss, una palabra o una hipótesis lingüística. La elección de cuarentena es conservadora y explícita.
- **Sesgo posible por exclusión:** la cuarentena descarta parejas auténticas además de las inciertas; el delta mide cobertura de candidatos, no exactitud del modelo ni superioridad de una teoría.
- **Alcance acotado:** no se reentrena, no se calculan métricas ni se accede a los folios reservados. La sensibilidad `split` no valida los valores anteriores, afectados también por otros defectos.
- **Resultado negativo preservado:** IT2a sin comas es un control de ausencia de cambio, no una réplica independiente del manuscrito.
- **Sin sobrescrituras:** `results.json`, corpus, hashes, semillas, manifiestos reservados, logs históricos y `state/committed_claims.md` quedan intactos. Las métricas antiguas permanecen `INVALID_FOR_CLAIM` como estimaciones del lector corregido.
- **Bloqueos:** sigue pendiente la adjudicación IVTFF completa, la reconstrucción exacta de EXP-170 y la conciliación de artefactos. No se inicia un ciclo científico prohibido por contradicciones abiertas.

**Referencia normativa:** René Zandbergen, *IVTFF – Intermediate Voynich MS Transliteration File Format*, issue 2.0.2 (08/07/2025), §6.7: https://www.voynich.nu/software/ivtt/IVTFF_format.pdf.

**Siguiente paso:** verificar CI y los conteos reales de candidatos; si pasa, integrar únicamente en la rama de PR #138 con control de cabeza y verificar CI posterior. No declarar limpieza global ni traducción.
