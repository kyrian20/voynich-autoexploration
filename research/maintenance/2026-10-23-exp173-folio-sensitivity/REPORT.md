# EXP-173 / C005–C006: sensibilidad por folio físico — 23-10-2026

**Estado:** diagnóstico retrospectivo y descriptivo; no es un EXP nuevo, una reproducción íntegra de EXP-173, una inferencia confirmatoria ni una traducción. Base canónica verificada antes de escribir: `c70a0ba5a97276edce09d7bfe7b8dc88514a2881`. Se conserva sin cambios el experimento histórico, las afirmaciones comprometidas y los corpus.

## Fuente primaria, población y unidades

Fuente: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` (Zandbergen–Landini IVTFF ZL3b, 13-05-2025). El lector histórico EXP-173 tiene Git blob `3fb1eeb92c301d3caf841499571f5e1a8b590bcc`; el crosswalk ya integrado tiene blob `db27baa834a898b2e1b6a78e94a3b8d6d98cff43`. Se aplican sus reglas históricas de selección P y tokens separados por puntos, pero el grupo B se obtiene **solo** del metadato explícito `$L=B`, sin imputar etiquetas ausentes. Es un subconjunto legado, no un lector IVTFF exhaustivo.

La selección consta de **2466 líneas, 20652 palabras, 40 folios físicos y 82 loci de página**. Para evitar seudorreplicación, recto, verso y paneles del mismo folio `fNN` se agrupan en un solo conglomerado. Los detalles de los 40 folios se conservan en `results.json`.

## Dos contrastes descriptivos con control de orden

| Métrica | Observado | Esperanza de orden aleatorio dentro de cada línea | Cociente observado/esperado | Enriquecimiento F3/F6 heredado |
| --- | ---: | ---: | ---: | ---: |
| `-am` al final de línea (F3) | 331 | 46.117476967 | 7.17732239 | 6.827646135 |
| `y-` al comienzo de línea (F6) | 355 | 109.993273393 | 3.22747009 | 3.493557029 |

La esperanza es **exacta bajo el nulo condicional** de permutar uniformemente los tokens de *cada línea* conservando sus palabras, longitudes y pertenencia a folio: suma de `n_tokens_con_rasgo/n_tokens_línea`. No se ejecutó Monte Carlo ni se calculó valor p. La esperanza condicionada no equivale a la tasa global usada como denominador de F3/F6. El resultado muestra un desajuste descriptivo con la intercambiabilidad posicional, **no** identifica si su origen es lengua, cifrado, plantilla o una convención de transcripción.

## Sensibilidad a conglomerados

| Métrica | Folios con exceso positivo/negativo | Rango al eliminar un folio | SE jackknife por folio | Intervalo normal 95 % aproximado |
| --- | --- | --- | ---: | --- |
| F3 | 39/1 | 6.725693657–6.899439691 | 0.21482014 | 6.406598661–7.248693609 |
| F6 | 39/1 | 3.372728746–3.836282102 | 0.425459106 | 2.65965718–4.327456878 |

El jackknife elimina un **folio físico** por vez y vuelve a calcular el cociente con denominadores nuevos. Su intervalo es aproximación normal descriptiva (40 conglomerados, distribución posiblemente heterogénea); **no** es el valor p histórico, ni prueba de independencia entre folios, ni corrección por búsqueda retrospectiva de métricas. La amplitud del intervalo no valida C005/C006 como afirmaciones inferenciales. Los folios `f26` (F3) y `f57` (F6) son los únicos con exceso negativo frente a la esperanza condicional; no se excluyen.

## Falsabilidad, límites y siguiente decisión

Bajo intercambiabilidad dentro de línea, los valores esperados condicionales son 46,117477 y 109,993273. Los observados 331 y 355 son distintos. El test es retrospectivo y no discrimina entre lenguaje natural, cifrado posicional o generador con reglas de posición. Un análisis confirmatorio posterior debe congelar **antes de observar** su población IVTFF completa, hipótesis rivales, nulo con permutaciones por folio, estadístico, umbrales y multiplicidad; comparar también corpus naturales correctamente identificados y controles generativos no ajustados al objetivo. No se reutiliza un corpus inglés como latín.

**Límites:** parser P legado; ambigüedad de ligaduras y codificaciones extendidas; etiquetas `$L` por página; sesgo de selección retrospectiva de F3/F6; dependencia entre folios no verificada; CI general distinta de ejecutar específicamente este auditor. Se mantienen originales, negativos y numeración sin cambios. C005 y C006 requieren adjudicación humana antes de modificar compromisos.

## Reproducción y auditoría

```sh
python tests/test_exp173_folio_sensitivity.py
python scripts/audit_exp173_folio_sensitivity.py --check research/maintenance/2026-10-23-exp173-folio-sensitivity/results.json
```

El código valida SHA-256 del corpus, blobs Git del lector histórico y del crosswalk, la población de 4.118 líneas y los conteos B antes de comparar el snapshot completo. Sin semillas ni paquetes externos. Se han superado **ocho pruebas unitarias locales con fixtures**; los agregados del corpus se calcularon independientemente contra el archivo remoto, pero la reproducción Python sobre checkout completo debe confirmarse explícitamente. No se toca el workflow compartido porque la PR #2 trabaja en él.

### Autoauditoría según `skills/audit_experiment.md`

1. **Target-awareness:** selección retrospectiva de dos métricas históricas; no se calibraron los valores del control para obtener una coincidencia con el manuscrito. Interpretación solo exploratoria.
2. **Feature-destroying:** la permutación dentro de línea destruye intencionalmente el orden que se contrasta, conservando longitud y vocabulario de cada línea. No es una simulación justa de un cifrado con gramática posicional; no se rechaza esa clase.
3. **Extrapolación:** las cifras se limitan a las 2.466 líneas P legadas con `$L=B` y a 40 folios físicos, no a todo el manuscrito ni a cualquier mecanismo.
4. **Negativos:** un desajuste del nulo de intercambiabilidad no implica semántica, lengua natural ni desciframiento.
5. **Control:** esperamos 46,117477 finales `-am` y 109,993273 comienzos `y-` bajo permutación uniforme porque cada token tiene probabilidad `1/longitud` de ocupar el borde. Los observados son 331 y 355, respectivamente. La discrepancia es precisamente la señal de orden posicional; no es una comparación inesperada ni una evidencia de significado. No se estima aquí la cola nula ni se asigna p.
