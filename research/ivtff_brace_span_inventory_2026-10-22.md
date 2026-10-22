# Inventario de fragmentos entre llaves en transcripciones IVTFF

Fecha: 2026-10-22  
Repositorio: `kyrian20/voynich-autoexploration`  
Método: recorrido mecánico de las transcripciones de `master`, ignorando líneas editoriales que comienzan por `#`. No se ha cambiado ningún resultado histórico ni la tokenización de producción.

## Resultados

| Transcripción | Fragmentos entre llaves | Contenidos distintos | Fragmentos con letras ASCII | Llaves sin pareja en líneas de transcripción |
|---|---:|---:|---:|---:|
| ZL3b (`data/transcriptions/eva_zl3b.txt`) | 446 | 107 | 446 | 0 |
| ZL3a (`data/transcriptions/zl3a.txt`) | 444 | 107 | 444 | 0 |
| IT2a (`data/transcriptions/eva_it2a.txt`) | 0 | 0 | 0 | 0 |

ZL3b y ZL3a comparten los contenidos más frecuentes: `ikh` (36 en ambas), `ckhh` (28 en ZL3b; 29 en ZL3a), `ch'` (28 en ambas), `cthh` (27 en ambas) e `ith` (25 en ambas). En ambas transcripciones, todos los fragmentos delimitados por llaves contienen letras ASCII y ninguno contiene espacios en blanco ni llaves anidadas.

## Interpretación prudente

1. El comportamiento actual de ambos tokenizadores descarta el contenido de cada fragmento entre llaves. El inventario demuestra que no son casos aislados: aparecen cientos de veces en ZL3a/ZL3b.
2. Este recuento **no** demuestra por sí mismo que el contenido deba convertirse en tokens ordinarios. Las llaves pueden representar una convención de ligadura y debe respetarse la semántica oficial de IVTFF antes de decidir cómo normalizarlas.
3. ZL3a y ZL3b son transcripciones alternativas del mismo manuscrito, no muestras independientes. La diferencia de dos fragmentos no se debe interpretar como evidencia estadística independiente.
4. IT2a no contiene fragmentos entre llaves en este recorrido; por tanto, este mecanismo concreto no explica por sí mismo diferencias en IT2a.
5. Se excluyeron las líneas editoriales que empiezan por `#`. En el primer recorrido global se detectó una llave de cierre suelta dentro de un comentario editorial de ZL3a/ZL3b (“Plant ID: Botriculum … Mondform?}”); no es un error de delimitación en una línea de transcripción. El filtro evita clasificar comentarios editoriales como datos lingüísticos.

## Puerta de validación pendiente

- Consultar y registrar la regla aplicable de IVTFF 2.0.2 para ligaduras entre llaves.
- Añadir fixtures que separen el texto original, la anotación de ligadura y la vista tokenizada, sin destruir la información original.
- Ejecutar un análisis de sensibilidad en una rama o experimento nuevo y versionado, solo después de decidir la interpretación normativa.
- No modificar ni sobrescribir EXP históricos hasta cuantificar exactamente qué estadísticas cambian.

## Reproducibilidad

El script `scripts/audit_ivtff_brace_spans.py` realiza el inventario no destructivo y se ha incorporado al workflow `Voynich Check`. Las pruebas de regresión también verifican que las líneas de comentarios editoriales se excluyan. El resultado de CI debe quedar en estado `success` antes de considerar validada la integración.


## Adjudicación normativa — 2026-10-22

La consulta de la especificación oficial IVTFF 2.0.2, §6.6, tabla 10, confirma que las llaves delimitan una **ligadura de caracteres Voynichese**, no un comentario: https://www.voynich.nu/software/ivtt/IVTFF_format.pdf. El propio documento ofrece ejemplos en §8 como `yka{ckh'h}` y `{y'}`. Por tanto, los 446 spans de ZL3b y los 444 de ZL3a son anotaciones de ligadura según la convención declarada por el formato; no deben interpretarse como texto editorial ni eliminarse sin dejar rastro.

La cuestión aún abierta es analítica: si un experimento requiere caracteres individuales, ¿debe expandir el contenido de la ligadura, tratarla como una unidad indivisible, o comparar ambas vistas? La especificación define la representación, pero no determina qué representación es óptima para todas las preguntas estadísticas. El siguiente paso es un análisis de sensibilidad versionado, conservando el texto bruto y sin reescribir EXP históricos.
