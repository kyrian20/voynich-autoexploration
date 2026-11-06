# Corrección acotada: fragmentos falsos dentro de llaves IVTFF

**Fecha:** 2026-10-30. **Estado inicial:** FIX PROPOSED / CI PENDING.
**Base exacta:** rama de investigación de PR #138, SHA `dfa3cc0a5082373d292bf3f1a964e5b664baa784`.
**Master inspeccionado:** `1bce529f2dd4f572f05489443c7a4579e9c0894f`.
**PR abiertas antes de actuar:** #5, #7, #13, #66, #82, #138.
**Sin nuevo EXP ni experimento predictivo.**

## Defecto falsable y reparación

El tokenizador conservador rechazaba unidades que contenían `{` o `}`, pero dividía la cadena por puntos, comas o espacios **antes** de consumir un tramo entre llaves. En consecuencia, `alpha.{a.b.c.d}.omega` podía generar `alpha, None, b, c, None, omega`: los tokens interiores `b` y `c` eran ficticios y podían formar un candidato negativo dentro de un único tramo no adjudicado. Lo mismo ocurría con espacios internos; una llave sin cerrar podía dejar palabras interiores como tokens aparentes.

La reparación consume cada tramo `{...}` completo como **una sola barrera de incertidumbre** `?` antes de separar palabras. Si hay llaves anidadas o desbalanceadas, pone en cuarentena toda la fila; no inventa una lectura. Los fragmentos limpios exteriores siguen disponibles, salvo las adyacencias que cruzan la barrera.

**Contrato previo a la CI:** los ejemplos sintéticos con puntos, comas y espacios interiores no deben crear tokens ni candidatos; los casos anidados o incompletos deben fallar de modo conservador; las palabras ordinarias deben conservarse. Cinco regresiones se ejecutarán con Python normal y `-O`. La CI completa debe comprobarse en el SHA exacto antes de considerar la corrección integrada.

## Corpus, alcance y reproducción

Se mantienen inmutables las dos fuentes versionadas:
- ZL3b: SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- IT2a: SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.

**Censo preliminar independiente de contenido recuperado por GitHub (no es aún ejecución de Python/CI):** 4.130 filas P en ZL3b con 394 tramos completos entre llaves y 0 con separadores internos; 4.118 filas P en IT2a, con 0 tramos. En ZL3b existe un tramo con espacios fuera del universo de filas P. La regresión SHA-locked exige estos recuentos; si difieren, debe fallar, no relajarse automáticamente.

Archivos:
- Código: `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py`.
- Regresiones: `tests/test_line_boundary_brace_spans.py`.
- CI: `.github/workflows/voynich-check.yml`.

Comandos de reproducción:
```sh
python -m unittest discover -s tests -p 'test_line_boundary_brace_spans.py' -v
python -O -m unittest discover -s tests -p 'test_line_boundary_brace_spans.py' -v
```
Semilla: no aplica; pruebas deterministas. No se entrena modelo, no se ejecuta bootstrap, no se consumen folios reservados y no se recalculan métricas.

## Autoauditoría y limitaciones

1. **Calibración a la señal:** ninguna; la barrera se define por el alcance de llaves, no por AUC, vocablos o etiquetas de Voynich.
2. **Destrucción de característica:** la cuarentena puede descartar una adyacencia real; es preferible a afirmar una adyacencia no documentada, pero **no** adjudica el valor de los glifos entre llaves.
3. **Extrapolación:** el parche solo cubre tramos entre llaves y sus errores de cierre. No demuestra conformidad IVTFF completa.
4. **Resultado negativo:** si el censo confirmado sigue mostrando cero tramos con separadores internos en filas P congeladas, el impacto medido en esos dos corpus es **cero**, sin inferir nada sobre otros corpus o revisiones.
5. **Controles:** se espera que `alpha.beta` conserve dos palabras y que una barrera `{a.b.c.d}` no produzca palabras interiores; los fixtures comprueban ambas condiciones.

**No modificar** `results.json`, corpus, semillas, particiones reservadas ni afirmaciones comprometidas. Las cifras históricas de la PR #138 permanecen `INVALID_FOR_CLAIM` bajo el lector corregido por defectos anteriores. Esta reparación no es una traducción ni una mejora de predicción demostrada.

**Pendientes independientes:** adjudicación IVTFF, reproducción histórica exacta de EXP-170, conciliación de artefactos, evaluación de PR #7 y nueva ejecución predictiva solo después de resolver las contradicciones metodológicas. No se integra en `master` mediante este parche.
