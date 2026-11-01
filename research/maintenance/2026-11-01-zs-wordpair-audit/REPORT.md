# Auditoría de reproducibilidad parcial: word-pair replication

**Fecha:** 2026-11-01  
**Estado:** reimplementación parcial; no reproduce de forma exacta el resultado publicado.  
**Alcance:** una métrica descriptiva del artículo de Zhang y Sheng, no un experimento de desciframiento.

## Afirmación revisada

La sección 5.1 informa una correlación de replicación de pares de palabras de **0,071 para ZL** y **0,053 para IT**. El apéndice E informa **0,069–0,070** para ZL al variar el vocabulario de 300 tipos a 150 o 600. El texto describe el conteo de pares que aparecen en la misma línea, 20 barajados dentro de cada página con extremos de línea fijos, dos mitades hechas con bloques alternos de diez páginas, una corrección por la tendencia general de cada palabra y una correlación de Spearman.

## Entradas fijadas

Se descargaron los archivos actuales del repositorio y se verificó que el SHA Git del contenido coincide con el objeto de GitHub. Los SHA-256 son:

| Archivo | SHA Git | SHA-256 |
|---|---|---|
| `eva_zl3b.txt` | `2a4533ab9bdfa85db9bad602d590978953055df1` | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` |
| `eva_it2a.txt` | `4d6d3f2537b1f507a257529b49c94af7d6e03446` | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` |

ZL3b e IT2a son transcripciones alternativas del mismo manuscrito; no son muestras independientes.

## Reglas de esta reconstrucción

El script usa el lector IVTFF del repositorio para una vista sin pérdida y, como sensibilidad, reproduce la proyección ASCII usada por el análisis histórico EXP-590. En cada vista:

- Selecciona los 150, 300 o 600 tipos más frecuentes, con desempate alfabético.
- Deja fuera pares de tipos iguales o a distancia Levenshtein de un glifo. La frase del artículo “one glyph apart” no define formalmente esta regla; aquí se interpreta como distancia de edición 1.
- Estima el recuento esperado con 20 barajados por página, permutando los tokens interiores de las líneas y dejando fijos el primero y el último.
- Divide las páginas en bloques alternos de diez. Usa semillas 20261101, 20261102 y 20261103.
- Estandariza el exceso como `(observado − esperado) / sqrt(esperado + 0.5)`.
- Define “quitar la tendencia general de cada palabra” como un ajuste OLS aditivo `z(i,j) = efecto(i) + efecto(j) + residuo`, calculado por separado en cada mitad y solo sobre pares admisibles. Esta fórmula es una decisión explícita de la reimplementación; el artículo no publica la fórmula ni el código.

El paquete JSON adjunto conserva los resultados por semilla, vista, tamaño de vocabulario y transcripción.

## Resultado

Con la proyección ASCII histórica sobre todas las filas no vacías:

| Transcripción | 150 tipos | 300 tipos | 600 tipos |
|---|---:|---:|---:|---:|
| ZL3b | 0,0327 (0,0277–0,0363) | 0,0378 (0,0371–0,0392) | 0,0862 (0,0844–0,0883) |
| IT2a | 0,0303 (0,0267–0,0354) | 0,0447 (0,0418–0,0476) | 0,0927 (0,0893–0,0958) |

La tabla da la media de tres semillas y, entre paréntesis, su mínimo y máximo. Con la vista P de párrafos y las 225 páginas comunes, la media para 300 tipos es **0,0418** en ZL3b y **0,0503** en IT2a. El intervalo de las tres semillas es 0,0401–0,0442 y 0,0493–0,0509, respectivamente.

La cifra de IT2a en P queda cerca de 0,053, pero esa proximidad no basta para llamarla reproducción: el resultado de ZL3b no coincide y la población de entrada tampoco coincide con la descrita en el artículo.

## Por qué la réplica exacta queda bloqueada

La proyección ASCII de todas las filas produce 5.376 líneas y 39.594 tokens para ZL3b; la vista de párrafos P en las 225 páginas comunes produce 4.119 líneas y 35.517 tokens. Para IT2a, esas cantidades son 5.207/37.945 y 4.118/34.510. La tabla 8 del artículo describe un canal de 4.355 posiciones de inicio/final de línea y 37.554 palabras. Ninguna de las poblaciones reconstruidas coincide con esas cantidades.

Además, el preprint no fija la regla de ajuste por propensión de palabra, la interpretación operacional de “a un glifo de distancia”, el filtro de etiquetas IVTFF ni la semilla de los barajados. El apéndice F dice que el código y las reglas se publicarían con la versión publicada; a la fecha de esta auditoría no estaban disponibles en el preprint consultado.

Por ello, la diferencia numérica no demuestra un error del artículo ni una propiedad lingüística del manuscrito. Muestra que el texto metodológico disponible no basta para identificar una réplica única. No se ejecutaron los controles de 28 textos del artículo y no se derivan conclusiones sobre la presencia o ausencia de significado.

## Reproducción

Desde la raíz del repositorio, con Python y NumPy instalados:

```bash
python3 research/maintenance/2026-11-01-zs-wordpair-audit/wordpair_audit.py > /tmp/wordpair-audit.json
```

La auditoría no recibe un número EXP nuevo y no modifica transcripciones ni resultados archivados. Se mantiene como nota de reproducibilidad metodológica.

## Fuente externa

Xin Zhang y Victor S. Sheng, *Does the Voynich Manuscript Mean Anything? Calibrated Tests Find Little Trace of Language*, arXiv:2610.34499v1, secciones 5.1 y apéndices E–F: https://arxiv.org/abs/2610.34499
