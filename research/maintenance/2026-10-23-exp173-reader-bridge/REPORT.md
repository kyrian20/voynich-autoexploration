# Puente de lectores de EXP-173 — 23-10-2026

Estado: **REPRODUCED** para los cálculos descriptivos, fixtures y snapshots de este paquete. Sensibilidad exploratoria; no validación de EXP-173 completo, de sus valores p ni de una hipótesis lingüística. Base: `29677e387d9c44983a28d61baad2f14e55a42c8e`.

## Qué aporta

Se reconstruye exactamente la población del lector histórico para ZL3b, ZL3a e IT2a, y después se compara con la capa léxica sin pérdida ya existente. Esta es una **proyección candidata explícita**, no certificación completa de IVTFF. Las etiquetas se mantienen en `$L=B`; se incluyen todos los locus que empiezan por P, reproduciendo el alcance histórico, no solo P0.

Se examinan las ocho combinaciones completas de comas split/join, alternativas primary/exclude_word y ligaduras expand/opaque. Se mantienen los códigos opacos e ilegibles en palabras completas. El análisis de -am/inicio y es literal y depende de esas decisiones. No se extraen fragmentos ASCII para mejorar resultados.

Para cada línea se calcula la esperanza k/n bajo intercambio uniforme de sus tokens. Se suman las esperanzas y se informa el cociente observado/esperado. La comparación principal usa los mismos registros no vacíos bajo los nueve lectores (histórico y ocho candidatos). Es un cambio de estimando respecto al cociente contra tasa agrupada de EXP-173.

## Resultados sobre registros comunes

| Edición | Líneas comunes | -am histórico, O/E | -am candidato por defecto, O/E | Rango de ocho candidatos | y histórico, O/E | y candidato por defecto, O/E | Rango de ocho candidatos |
|---|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | 2.466 | 7,17732 | 7,69434 | 7,16876–7,69434 | 3,22747 | 3,16018 | 3,04757–3,16566 |
| ZL3a | 2.466 | 7,17732 | 7,69434 | 7,16876–7,69434 | 3,22747 | 3,16018 | 3,04609–3,16566 |
| IT2a | 2.464 | 7,51664 | 7,56014 | 7,56014–7,56014 | 3,26642 | 3,19132 | 3,19132–3,19132 |

Los dos excesos descriptivos mantienen su signo en todas las vistas examinadas. Las ediciones son transcripciones relacionadas del mismo manuscrito; no son tres muestras independientes. La coincidencia completa de algunas cifras ZL3a/ZL3b refleja esa relación, no una replicación independiente.

Por defecto se usa split/primary/expand, fijado antes de ejecutar. En ZL3b, -am pasa de O=331, E=46,11748 a O=376, E=48,86706. Para y, O=355 permanece igual, pero E pasa de 109,99327 a 112,33548. Ningún resultado confirma significado, lengua o mecanismo de producción.

## Diferencias localizadas

- ZL3b y ZL3a: 2.467 registros B/P brutos. El lector histórico deja vacío `f85r2.6`; las vistas candidatas recuperan el token anotado. Su contenido no aporta -am ni inicio y, de modo que incorporarlo no cambia estas esperanzas ni observados, aunque sí cobertura y tasa agrupada. No se adjudica aquí si ese locus debe formar parte de un futuro análisis exclusivamente lingüístico.
- IT2a: 2.466 registros B/P brutos; dos vacíos históricos (`f84v.42`, `f84v.46`). La intersección conserva 2.464. Se publican también las poblaciones propias de cada lector.
- En ZL3b/ZL3a la vista por defecto recupera **45 finales -am** sin perder ninguno: 34 de las filas ganadas tenían el marcador de párrafo `<$>` unido al último token histórico. Otras diferencias incluyen alternativas, comentarios y delimitación de palabras; no se atribuyen todas a una sola causa.
- En IT2a se recuperan **36 finales -am**: las 36 filas tenían `<$>` en el último token histórico.
- El recuento neto de y en ZL3b/ZL3a oculta 16 ganancias y 16 pérdidas de posición inicial; IT2a tiene seis ganancias y ocho pérdidas. Por ejemplo, en `f43r.1` el histórico descarta `<%>tarodaiin` y coloca `ytedy` en primera posición. La proyección conserva `tarodaiin` como primera palabra. La igualdad neta no implica igualdad de filas ni de lectura.

Se conservan los textos brutos y todas las proyecciones distintas de cada fila cambiada en `changed-rows.json.gz`; no es necesario modificar transcripciones originales. Hay 1.903 filas con cambios de tokens en ZL3b, 1.903 en ZL3a y 1.097 en IT2a. Son diferencias de proyección, no igual cantidad de errores independientes ni de cambios del rasgo analizado.

## Sensibilidad al retirar un folio completo

En ZL3b, sobre la intersección, se retira por turno cada uno de los 40 folios numéricos, con todas sus caras y paneles conjuntamente. Se comparan histórico y candidata por defecto en las mismas filas restantes:

| Rasgo | Rango histórico O/E | Rango candidato O/E | Rango candidato menos histórico |
|---|---:|---:|---:|
| -am/final | 7,03758–7,28971 | 7,55362–7,79772 | +0,46673 a +0,57193 |
| y/inicial | 3,12065–3,51175 | 3,04783–3,40792 | −0,10382 a −0,04772 |

Ninguna de esas retiradas elimina los dos excesos en esta población. Los rangos **no son intervalos de confianza**, ni una prueba sobre todos los folios posibles. Tampoco se controlan aquí composición por sección, mano o cierre de párrafo. El control por línea conserva exactamente inventario y longitud de cada línea, pero no identifica la causa de la posición observada.

## Reproducción y comprobaciones

Python 3.12.14, sin dependencias nuevas. Protocolo escrito antes de ejecutar, con selección retrospectiva declarada. `results.json` contiene hashes SHA-256 de las tres transcripciones y de seis dependencias de lectura, las nueve vistas completas y las 40 retiradas pareadas. `checksums.json` fija los artefactos del paquete. El archivo comprimido conserva los registros con diferencias; se verifica su contenido JSON descomprimido, sin exigir una versión concreta de compresor.

```sh
python tests/test_exp173_reader_bridge.py
python scripts/audit_exp173_reader_bridge.py --check research/maintenance/2026-10-23-exp173-reader-bridge
```

Las ocho pruebas del puente pasaron. Cubren marcadores de párrafo, exclusión de alternativas, comas, ligaduras opacas, ilegibles, líneas vacías, retirada conjunta de caras y rechazo de payload irresuelto. Los snapshots completos de resultados y filas cambiadas se regeneraron y cotejaron. Los dos bloques previos se exigen como controles antes del cálculo. La CI se amplía para ejecutar las cuatro auditorías de EXP-173 (23 pruebas y sus snapshots); el éxito de la nueva ejecución se debe verificar por separado.

La CI del commit base sí está verificada: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39906558763 . Ese éxito precede a este paquete y no se atribuye a él.

## Autoauditoría — skills/audit_experiment.md

**Target-awareness:** los rasgos fueron seleccionados históricamente. La rejilla y la vista por defecto se fijan antes de esta ejecución; no se calibran para aumentar el resultado. Las cifras son sensibilidad retrospectiva, no confirmación preinscrita.

**Implementación:** excluir alternativas puede borrar palabras y desplazar extremos; las ligaduras opacas pueden ocultar coincidencias literales. Se publica toda la rejilla y sus filas comunes, sin interpretar esas pérdidas como ausencia de un fenómeno manuscrito. La proyección conserva código opaco, no lo descifra. El lector histórico pierde anotaciones y primeros tokens marcados: se preserva para reconstrucción y no se declara correcto por reproducirlo.

**Extrapolación:** el resultado se limita a B/P, tres ediciones relacionadas y ocho políticas. No establece conformidad IVTFF completa ni validez global de inferencias anteriores.

**Alcance negativo:** ninguna familia de lenguas, cifrados o generadores queda descartada. C005/C006 y sus valores p no se modifican; los cocientes aquí tienen denominador distinto.

**Controles:** se espera reconstrucción idéntica del histórico en cada fuente y coincidencia con los snapshots anteriores; ambas se observan. En la fixture `y.xam<$>` se espera O(-am final)=0 bajo el histórico literal y 1 al interpretar el marcador; se observa 0/1. La recuperación de extremos no es una señal semántica: responde al tratamiento explícito de anotaciones.

Siguiente paso: separar P0 de otros locus y extremos de párrafo en un protocolo fijado, manteniendo las mismas vistas y registros identificados. Después se podrá definir un contraste por folio/sección con incertidumbre adecuada. La adjudicación IVTFF y la identificación semántica siguen abiertas.
