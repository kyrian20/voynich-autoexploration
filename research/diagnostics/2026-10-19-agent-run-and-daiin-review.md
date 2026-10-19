# Revisión de ejecución y siguiente prueba Voynich — 2026-10-19

## Estado operativo verificado

- El conector de GitHub pudo crear un archivo en `master`; commit de diagnóstico: https://github.com/kyrian20/voynich-autoexploration/commit/cf7e585d4fe74b8d45db7a8ee2bb0ca0bebed0d4
- El workflow `Voynich Autonomous Research` está programado con cron `0 8 * * *` (08:00 UTC) y permite ejecución manual.
- La ejecución programada del 2026-10-19 (run 39223666822) falló en el paso `Run bounded research agent`; los registros muestran `HTTP Error 429: Too Many Requests`. El paso de commit se omitió, por lo que no se generó informe. Un 429 puede significar límite de tasa o cuota/billing de la API; el log por sí solo no distingue cuál.
- El workflow actual envía una petición a OpenAI API y requiere el secreto `OPENAI_API_KEY`. El plan ChatGPT y el saldo/crédito de API son independientes. No se ha lanzado una nueva ejecución para evitar consumo adicional.

Ejecución: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39223666822

## Evidencia pública revisada: EVA `daiin` y posición

1. El explorador de concordancias de voynich.world informa 820 apariciones de `daiin` en 205 folios en su transcripción de consenso; identifica el fichero de datos y su SHA-256 en la página de fuentes:
   - https://voynich.world/explore/manuscript?word=daiin
   - https://voynich.world/explore/sources
2. Un análisis posicional anterior describe afinidad de `daiin` por el inicio de línea y señala también apariciones finales; clasifica `dai`, `daiin`, `dair`, `sai`, `saiin`, `sar` y `sol` entre las formas con afinidad inicial:
   - https://voynichattacks.wordpress.com/2022/12/26/word-positions-on-the-folios/
   - https://voynichattacks.wordpress.com/2022/12/30/word-positions-on-the-folios-part-deux/
3. El preprint de Christophe Parisel describe una mezcla Beta-Binomial aplicada a razones de sustitución de pares de caracteres en 185 folios; reporta selección de dos grupos por BIC y 89% de acierto en etiquetas Currier retenidas, y propone además un interruptor de dos estados asociado a vocales tras ch/sh:
   - https://arxiv.org/abs/2604.25979

## Interpretación prudente

La afinidad posicional de `daiin` es una observación replicable y útil, pero no prueba por sí sola que sea una palabra funcional, un marcador gramatical o un elemento de significado conocido. Las cifras de sitios distintos no deben combinarse como si fueran el mismo corpus: las transcripciones, criterios de inclusión y normalizaciones pueden diferir. El resultado de Parisel es un preprint y una clasificación estadística no equivale a descifrar el texto.

## Siguiente experimento reproducible propuesto

**Pregunta:** ¿La afinidad de `daiin` por el inicio de línea permanece después de controlar por sección, longitud de línea y distribución de frecuencias?

1. Fijar una sola transcripción versionada (preferiblemente Zandbergen–Landini EVA/IVTFF 3b) y guardar su URL, fecha y SHA-256.
2. Parsear líneas y tokens sin unir líneas ni párrafos; excluir explícitamente líneas ilegibles/etiquetas y registrar las reglas.
3. Para cada tipo con frecuencia suficiente, calcular: frecuencia total; proporción en posición 1; proporción en última posición; distribución de posición fraccional (i/(n-1)); sección y folio.
4. Comparar `daiin` con controles de frecuencia similar y con `aiin`, `chedy`, `dain`; estratificar o permutar dentro de sección y longitud de línea para evitar que una sección o las líneas cortas expliquen el efecto.
5. Usar permutación por línea (no por token independiente) para preservar la longitud y composición de cada línea; informar efecto, intervalo de confianza, valor p corregido por pruebas múltiples y resultados por sección.
6. Replicar en una transcripción independiente (por ejemplo ZL3a frente a ZL3b). Declarar fallo si la dirección del efecto no se conserva o depende de una sola sección.
7. Publicar código, entradas exactas, hash y salida tabular antes de interpretar semánticamente el resultado.

**Estado:** propuesta de experimento; no ejecutado en esta revisión. No se presenta como resultado experimental nuevo.
