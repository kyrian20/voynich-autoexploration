# Auditoría de reproducibilidad parcial: word-pair replication

> **Corrección de alcance (01-11-2026):** las mitades archivadas por bloques de 10 páginas comparten cuatro hojas físicas en ambas transcripciones (f67, f72, f90, f102). Los 54 valores se conservan como estadística descriptiva de mitades de páginas, **no** como validación en hojas físicas independientes. Véase [corrección y regresiones](PHYSICAL_LEAF_SPLIT_CORRECTION.md).

**Fecha:** 2026-11-01  
**Estado:** reimplementación parcial; el valor publicado no queda reproducido.  
**Alcance:** auditoría de una métrica del artículo, no un experimento de desciframiento.

## Corrección de la primera versión

La versión inicial de esta auditoría usó todas las categorías de líneas, comparó palabras por distancia entre caracteres y no conservó la lista completa de páginas vacías al formar bloques. Eso no seguía el preprocesamiento declarado por el artículo. Sus cifras anteriores quedan **RETIRADAS** y no deben citarse. El historial de Git conserva esa versión; los resultados actuales de este informe y del JSON la reemplazan.

## Afirmación y preprocesamiento publicado

Zhang y Sheng informan una correlación de replicación de pares de **0,071 en ZL** y **0,053 en IT**. En la sección 3 dicen que usan el texto corrido y las líneas de círculos/radios, leen espacios dudosos como separadores y aplican las convenciones EVA en las que `ch`, `sh`, `cth`, `ckh`, `cph` y `cfh` son glifos únicos. Informan 37.554 tokens en ZL y 36.736 en IT. La sección 5.1 describe 300 tipos frecuentes, 20 barajados dentro de página con extremos de línea fijos, mitades de bloques alternos de diez páginas, exclusión de pares idénticos o separados por un glifo y una corrección por la tendencia general de cada palabra.

## Entradas fijadas y alcance reconstruido

Se usaron las transcripciones actuales del repositorio; los SHA Git de ambos archivos se verificaron localmente contra los blobs recuperados. ZL3b e IT2a son lecturas alternativas del mismo manuscrito y no muestras independientes.

| Archivo | SHA Git | SHA-256 |
|---|---|---|
| `eva_zl3b.txt` | `2a4533ab9bdfa85db9bad602d590978953055df1` | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` |
| `eva_it2a.txt` | `4d6d3f2537b1f507a257529b49c94af7d6e03446` | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` |

La reconstrucción principal conserva las páginas comunes a ambas transcripciones (225) y los registros IVTFF de texto corrido, círculos y radios (categorías P/C/R). Con espacios dudosos separados, el lector del repositorio obtiene 4.333 líneas y 37.444 tokens en ZL3b, y 4.332 líneas y 36.873 tokens en IT2a. Es una aproximación cercana a los totales publicados, pero quedan diferencias de 110 y 137 tokens y de 22/23 líneas frente a los 4.355 slots de línea de la tabla 8. El filtro exacto de registros de línea no queda publicado.

## Reglas explícitas de esta reimplementación

- Para cada transcripción se usan las 225 páginas comunes, incluso cuando una página no aporta una línea P/C/R.
- Los tokens EVA se separan con el lector lossless; las seis secuencias indicadas arriba cuentan como glifos únicos al comparar formas.
- “A un glifo de distancia” se operacionaliza como distancia Levenshtein de hasta un glifo, contando sustitución, inserción o borrado. El artículo no define el algoritmo de distancia.
- Se comparan los 150, 300 y 600 tipos más frecuentes; los empates se resuelven en orden alfabético EVA.
- Se hacen 20 barajados por página, moviendo los tokens interiores entre líneas y fijando el primer y último token de cada línea. Se usan tres semillas: 20261101, 20261102 y 20261103.
- El exceso se calcula como `(observado − esperado) / sqrt(esperado + 0.5)`.
- “Quitar la tendencia general de cada palabra” se implementa como una regresión OLS aditiva `z(i,j) = efecto(i) + efecto(j) + residuo`, por separado en cada mitad y solo sobre pares admisibles. Esta fórmula es una decisión explícita de la reimplementación; el artículo no publica la fórmula exacta.

El archivo de resultados conserva cada semilla, vista de tokenización, tamaño de vocabulario, recuento de pares admisibles y transcripción.

## Resultado corregido

La vista principal aplica espacios dudosos como separadores y la distancia entre glifos EVA:

| Transcripción | 150 tipos | 300 tipos | 600 tipos |
|---|---:|---:|---:|
| ZL3b | 0,0207 (0,0180–0,0231) | 0,0340 (0,0335–0,0344) | 0,0839 (0,0824–0,0848) |
| IT2a | 0,0272 (0,0260–0,0284) | 0,0460 (0,0429–0,0487) | 0,0952 (0,0944–0,0967) |

Cada celda es la media de tres semillas; el intervalo entre paréntesis es su mínimo y máximo. El artículo informa 0,071/0,053 para el vocabulario de 300 tipos y, para ZL, 0,069/0,070 con 150/600 tipos. La reimplementación no reproduce esas cifras; además, la fuerte variación con el tamaño del vocabulario no coincide con la sensibilidad descrita en el apéndice E.

La política de espacios unidos y la proyección ASCII histórica del repositorio quedan en el JSON como sensibilidades, separadas de la vista EVA principal.

## Interpretación y límite

El preprint no especifica la fórmula que elimina la propensión de cada palabra a compartir líneas, el algoritmo exacto para “un glifo de distancia”, el desempate de tipos o la semilla de barajado. La sección 3 fija mejor el universo de texto y las convenciones EVA de lo que indicaba esta auditoría inicialmente, pero el total de tokens aún no coincide exactamente. El apéndice F anuncia que el código y las reglas de decisión se publicarían con la versión publicada; no estaban incluidos en el preprint v1 consultado el 2026-11-01.

Por tanto, la discrepancia no demuestra un error del artículo ni una propiedad lingüística del manuscrito. Indica que la descripción disponible no identifica una réplica única. No se ejecutaron los 28 controles multilingües del artículo y no se deriva una conclusión sobre presencia o ausencia de significado.

## Reproducción

Desde la raíz del repositorio, con Python y NumPy:

```bash
python3 research/maintenance/2026-11-01-zs-wordpair-audit/wordpair_audit.py > /tmp/wordpair-audit.json
```

No se asigna un ID EXP: el registro de experimentos mantiene conflictos de numeración, y esta entrada es una auditoría metodológica. No se modifican las transcripciones ni resultados archivados.

## Fuente primaria

Xin Zhang y Victor S. Sheng, *Does the Voynich Manuscript Mean Anything? Calibrated Tests Find Little Trace of Language*, arXiv:2610.34499v1, secciones 3 y 5.1, apéndices E–F: https://arxiv.org/abs/2610.34499
