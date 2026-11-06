# Contexto externo para la auditoría de pares Zhang–Sheng

**Fecha de consulta:** 2026-11-01  
**Base revisada:** `master` `8dc31bb784223f46ad56df911a9968d4a0716528`  
**Clase:** incorporación de literatura y contraste metodológico; no es experimento ni resultado nuevo del proyecto.

## Qué cambia en el contexto

El preprint de Zhang y Sheng (arXiv:2610.34499v1, enviado el 25-10-2026) informa una puntuación de recurrencia de pares de palabras en líneas de 0,071 para el manuscrito. Su argumento compara el nivel con 28 textos de 16 lenguas y con varios cifrados; el artículo deja claro que el resultado es un indicio estadístico sobre recurrencia de pares, no una lectura del texto.  
Fuente primaria: https://arxiv.org/abs/2610.34499

Una segunda línea de trabajo, publicada en la cronología del proyecto *Voynich Studies*, dice haber reconstruido la métrica y obtenido 0,078 para el manuscrito. El mismo proyecto informa 0,139–0,411 en su propio generador de tablas, incluidos controles con palabras latinas barajadas y letras independientes, y atribuye la recurrencia de pares de su modelo al dialecto de sección. Es una afirmación de los autores de ese proyecto, no una reproducción independiente comprobada aquí ni una publicación revisada por pares.  
Fuente del registro de resultados: https://voynich.site/publications?lang=en

## Relación con nuestra auditoría

Nuestra reimplementación parcial declara otra operacionalización: páginas comunes; registros IVTFF P/C/R; seis secuencias EVA como glifos únicos; distancia Levenshtein de hasta un glifo; y regresión OLS aditiva para quitar la propensión general de cada palabra. En esa especificación, la vista EVA principal de 300 tipos produce 0,0340 en ZL3b y 0,0460 en IT2a. El informe de auditoría ya advierte que la fórmula publicada de corrección no está especificada y que el valor del artículo no queda reproducido.

Como diagnóstico adicional de los 54 registros congelados, para 300 tipos y la vista EVA con espacios dudosos separados, la media de tres semillas en ZL3b es 0,03578 sin residualizar y 0,03401 con el ajuste OLS aditivo (cambio −0,00178); en IT2a es 0,04307 y 0,04602 (cambio +0,00295). Esto indica que **en esta reimplementación concreta** el ajuste OLS apenas mueve el estadístico y, por sí solo, no explica que ZL3b quede lejos del 0,071 publicado. No descarta otra fórmula de residualización, ni localiza la causa de la diferencia: permanecen abiertos el universo exacto de líneas, elegibilidad de pares, parsing y la operacionalización de la distancia de un glifo. Son promedios descriptivos de las semillas archivadas, no una incertidumbre estadística ni una nueva réplica.

Los valores 0,071, 0,078, 0,0340 y 0,0460 **no son todavía comparables como discrepancias de una misma estadística**: difieren las reconstrucciones disponibles y puede cambiar el resultado con la corrección por palabra, el universo de líneas, la partición y la transcripción. ZL3b e IT2a son ediciones del mismo manuscrito, no réplicas independientes. Además, la auditoría física del 01-11-2026 detectó cuatro hojas compartidas entre las dos mitades del archivo por bloques de páginas; ese archivo describe mitades de páginas y no acredita evaluación en hojas independientes.

El resultado externo sobre el generador importa para interpretar, no para decidir el caso: un valor bajo de recurrencia no identifica por sí solo ausencia de lengua, y un valor alto del modelo tampoco demuestra que el manuscrito use ese mecanismo. La estadística necesita controles de generadores y una definición exacta antes de apoyar una conclusión semántica.

## Próximo paso recomendado

Antes de usar esta métrica en una conclusión del proyecto:

1. Recuperar, si se publica, el código o la fórmula completa de Zhang–Sheng y congelar una interpretación literal de cada paso.
2. Construir una tabla de concordancia de la puntuación con datos sintéticos pequeños cuya salida se pueda calcular a mano; después comparar contra la reconstrucción OLS ya archivada, sin ajustar parámetros al valor del Voynich.
3. Solo entonces ejecutar la misma definición en las dos transcripciones y en generadores/corpora de control, declarando qué unidad se mantiene independiente. Mantener aparte cualquier partición por hojas físicas.

No se cambian scripts, los 54 resultados archivados, corpus, afirmaciones comprometidas ni la conclusión de la auditoría. Este memo no valida ninguno de los valores citados.
