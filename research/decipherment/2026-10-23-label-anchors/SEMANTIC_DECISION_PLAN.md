# Plan de decisión para etiquetas EVA: avanzar sin traducir por parecidos

Fecha: 2026-10-23. Estado: **DISEÑO PREVIO**, sin resultados semánticos nuevos. Complementa PROTOCOL.md y EXTERNAL_AI_EVIDENCE.md; no crea EXP ni cambia hipótesis confirmadas.

## Punto de partida comprobado

EXP-580 reprodujo sus seis recuentos históricos en Voynich Check #711; el inventario de 547 tipos aún requiere validación de exportación y, sobre todo, auditoría independiente del parser IVTFF. El recuento no prueba que esos tipos sean nombres propios, plantas o estrellas. La partición v2 por hoja física no es un conjunto históricamente virgen: las páginas ya se han examinado en investigaciones anteriores.

## Selección de datos sin fuga

1. Congelar SHA del corpus, script, inventario y manifiesto v2 antes de elegir palabras.
2. Generar tabla por ocurrencia con folio, locus, edición, variante y categoría visual con fuente externa; marcar referencias ambiguas como INELIGIBLE. **No inferir categoría visual a partir de la forma EVA.**
3. Revisar en detalle la prueba externa Simone F-20 y sus errores conocidos. Si nuestro contraste es equivalente al ya realizado, registrar NO-NOVELTY y no ejecutarlo.
4. Trabajar primero con train; usar development una sola vez para fijar umbrales y conservar test sin inspección de los resultados de la hipótesis. Como el test tiene exposición histórica, declarar «holdout prospectivo operacional», nunca validación ciega absoluta.

## Controles mínimos y predicciones

- **Hipótesis nula:** las formas EVA no aportan información sobre referentes visuales más allá de sección, folio, longitud, frecuencia, posición y segmentación.
- **Baselines:** categoría mayoritaria por sección; barajado de etiquetas dentro de sección y hoja, cuando exista variación; longitud/frecuencia/posición; similitud ortográfica a nombres externos (para revelar coincidencias espurias).
- **Controles positivos:** correspondencias sintéticas insertadas en copias separadas y etiquetadas, nunca en los datos Voynich originales. Si el método no las detecta, declarar BLOCKED.
- **Unidad estadística:** hoja física; las etiquetas de una misma hoja son dependientes. Intervalos mediante remuestreo por hoja y permutaciones estratificadas; corregir multiplicidad de hipótesis.
- **Prueba de falsación:** si no mejora todos los baselines en test, si depende de un solo folio, si las imágenes no tienen identificación independiente o si desaparece con un lector alternativo, registrar NEGATIVE/INCONCLUSIVE, nunca «traducción».

## Puertas para pasar a traducción

**G0:** inventario reproducible y metadatos auditados; **G1:** referentes externos suficientes con trazabilidad; **G2:** predicción preregistrada con ventaja reproducible fuera de muestra; **G3:** varias correspondencias estables que permitan predecir ocurrencias nuevas; **G4:** frases con análisis gramatical, coherencia semántica y replicación independiente. Solo G3 permitiría hablar de *candidatos léxicos*; G4 sería evidencia inicial de traducción. Las cifras y umbrales cuantitativos concretos permanecen los de PROTOCOL.md, sin relajarlos retrospectivamente.

## Resultados a conservar

- Inventario y hashes, tabla de exclusiones, identificaciones visuales y sus fuentes.
- Versiones de modelos y semillas; pruebas negativas, comparadores y tamaño del efecto por hoja.
- Informe separado de HECHOS, OBSERVACIONES, HIPÓTESIS y ESPECULACIONES; registrar NO-GO cuando corresponda.

**No se ha probado una palabra traducida en este documento.**
