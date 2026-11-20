# EXP-590 / EXP-593: reconciliación exacta de poblaciones

Fecha: 2026-11-16  
Estado: **REPRODUCED** (auditoría de cobertura y sensibilidad exploratoria; no es un EXP nuevo).

## Pregunta

¿Las 4.188 líneas de EXP-593 son la misma población que las 5.376 líneas de EXP-590, o existe una diferencia real de cobertura? Se comparan los identificadores físicos de línea, el texto crudo y los tokens parseados. Se conservan intactos los artefactos históricos.

## Fuente y procedimiento

- Fuente: `data/transcriptions/eva_zl3b.txt`
- SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- Script: `scripts/reconcile_exp590_exp593_population.py`
- Ejecución: `python scripts/reconcile_exp590_exp593_population.py --source data/transcriptions/eva_zl3b.txt`

El script aplica las expresiones de identificación de línea de los dos análisis y la misma limpieza/tokenización al registro completo. Luego compara los conjuntos de loci, exige que la población restringida esté contenida en la amplia y comprueba que cada fila compartida conserva idénticos texto crudo y tokens. No interpreta etiquetas de Currier como filtro de inclusión.

## Resultado de la reconciliación

| Población | Líneas con tokens | Tokens | *daiin* | Inicio | Final |
|---|---:|---:|---:|---:|---:|
| EXP-590, patrón amplio | 5.376 | 39.594 | 853 | 161 | 134 |
| EXP-593, patrón restringido | 4.188 | 32.732 | 726 | 133 | 118 |
| Solo patrón amplio | 1.188 | 6.862 | 127 | 28 | 16 |

Los **4.188 loci restringidos son un subconjunto exacto** de los 5.376 loci amplios. En las 4.188 líneas compartidas, el registro crudo y la secuencia tokenizada coinciden. No hay loci duplicados ni líneas exclusivas del patrón restringido. Las 1.188 líneas añadidas por el patrón amplio son **1.028 líneas de subfolios numerados y 160 líneas de `fRos`**. La causa concreta es la expresión regular de EXP-593, que acepta `fNNr/v` pero no sus sufijos numerados ni `fRos`; no es una discrepancia en el corpus ni una corrección de `$L`.

La sensibilidad de población amplia ya documentada en la rama de EXP-593 ampliado queda así respaldada por reconciliación locus a locus. Los informes históricos de EXP-590 y EXP-593 no se reemplazan ni se mezclan como si tuvieran la misma cobertura.

## Prueba exacta de posición bajo el mismo nulo

Además de la conciliación, el script calcula la cola superior exacta de Poisson-binomial. Para cada línea, la probabilidad nula de comenzar por una variante es su frecuencia en esa línea dividida por el número de tokens; las líneas se tratan como independientes bajo el nulo de permutación dentro de línea. Se aplica Holm a las tres variantes seleccionadas previamente.

| Población | Variante | Ocurrencias | Inicios observados | p exacto | p ajustado Holm |
|---|---|---:|---:|---:|---:|
| Amplia | `daiin` | 853 | 161 | 9,87×10⁻⁸ | 2,96×10⁻⁷ |
| Amplia | `dain` | 212 | 49 | 4,57×10⁻⁶ | 9,13×10⁻⁶ |
| Amplia | `daiiin` | 21 | 2 | 0,8589 | 0,8589 |
| Restringida | `daiin` | 726 | 133 | 1,85×10⁻⁵ | 5,55×10⁻⁵ |
| Restringida | `dain` | 198 | 45 | 2,51×10⁻⁵ | 5,55×10⁻⁵ |
| Restringida | `daiiin` | 19 | 2 | 0,8238 | 0,8238 |

Los excesos iniciales de `daiin` y `dain` sobreviven a la corrección por las tres variantes en ambos alcances. `daiiin` no muestra exceso. La diferencia de cobertura cambia los recuentos y los valores p, pero no revierte la dirección de esos dos resultados bajo este nulo.

## Interpretación y límites

La discrepancia se resuelve como una diferencia deliberada/de implementación en alcance del parser: el archivo histórico EXP-593 tenía un patrón más estrecho. La explicación no depende de que la cifra 4.188 sea errónea; es reproducible bajo su patrón original. La prueba exacta mejora la resolución frente a los 5.000 remuestreos archivados, pero la familia de palabras fue seleccionada durante investigación previa. Holm solo cubre estas tres variantes, no esa selección histórica ni todas las consultas anteriores.

El nulo conserva el multiconjunto de tokens de cada línea y destruye el orden; solo responde si el número de inicios supera lo esperado bajo esa permutación. No prueba lenguaje, significado ni desciframiento. ZL3b es una transcripción alternativa del mismo manuscrito y no una muestra independiente. La coincidencia del parser se limita a estas reglas y no certifica conformidad completa con IVTFF.

## Autoauditoría metodológica

1. **Selección consciente del objetivo:** las tres variantes proceden de análisis exploratorios anteriores. Se declara explícitamente y la corrección Holm se limita a esa familia.
2. **Implementación que destruya el rasgo:** el contraste estudia el primer token; el nulo aleatoriza la selección de token dentro de cada línea y conserva las frecuencias por línea. La tokenización puede afectar la inclusión, pero el cotejo locus a locus muestra que ambas vistas usan filas compartidas idénticas.
3. **Extrapolación:** no se generaliza a todas las palabras, modelos ni hipótesis sobre la producción del manuscrito.
4. **Resultado negativo:** la falta de exceso de `daiiin` solo se refiere a esta variante, población y nulo.
5. **Interpretación del control:** bajo el nulo, cada línea aporta una Bernoulli con probabilidad frecuencia/longitud. El resultado compara orden observado con ese nulo; no con una lengua ni con texto aleatorio.

**Conclusión:** la diferencia de 1.188 líneas queda explicada y auditada exactamente; los resultados posicionales para `daiin` y `dain` permanecen bajo esta corrección de cobertura. No hay traducción validada.
