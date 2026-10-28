# Réplica independiente: predicción de límites de línea en el Manuscrito Voynich

**Fecha de ejecución:** 28 de octubre de 2026  
**Estado:** reimplementación independiente ejecutada y repetida de forma determinista; coincidencia aproximada con el artículo, no reproducción bit a bit.  
**Repositorio base consultado:** `kyrian20/voynich-autoexploration`, `master` en `9134d8c872f35602912512b33d27b8e9cc8bff67`.  
**Identificadores de experimento:** ninguno asignado; la numeración del proyecto permanece congelada.

## Resumen

Reimplementé el clasificador publicado por Zenil y Uthamacumaran para estimar si una separación entre dos palabras es un límite de línea. Luego repetí la evaluación reteniendo una hoja física completa cada vez, agrupando juntas sus caras recto/verso y paneles. Excluí del entrenamiento las líneas textualmente idénticas a las líneas de evaluación; en los datos normalizados no encontré duplicados que activaran esa exclusión.

Con la transcripción ZL3b, la partición por páginas reproduce de cerca el resultado publicado: AUC **0,844** y ganancia de código **0,115 bits por hueco**, frente a **0,843** y **0,114** en el artículo. El número de huecos difiere en 39 (6.229 frente a 6.190), aunque ambos tienen 719 límites de línea.

En validación leave-one-physical-leaf-out, el modelo completo conserva rendimiento: AUC micro agrupada **0,854** (ZL3b) y **0,856** (IT2a); la media macro por hoja es **0,835** y **0,838**, respectivamente. La ganancia de código media por pliegue es **0,111** y **0,115 bits por hueco**. Los resultados son estables entre dos transcripciones EVA, pero esas transcripciones describen el mismo manuscrito y no constituyen dos manuscritos independientes.

El hallazgo permite afirmar que la forma local de las palabras contiene información para predecir la disposición de los saltos de línea. No identifica por sí solo idioma, mecanismo de producción, significado ni descifrado.

## Pregunta y método

**Pregunta:** ¿Los rasgos superficiales de las palabras contiguas permiten predecir si el hueco entre ellas coincide con un salto de línea en una página no usada para entrenar?

El artículo codifica cada palabra con una tupla categórica: sus dos primeros caracteres, sus dos últimos y su longitud limitada a 12. Un clasificador Naive Bayes categórico estima por separado la probabilidad de los rasgos de la palabra izquierda y derecha, con suavizado aditivo α = 0,5. La puntuación se convierte en probabilidades y se compara con una predicción constante basada en la prevalencia de límites en el entrenamiento. Medí AUC y ganancia de código en bits por candidato (pérdida logarítmica del baseline menos pérdida del modelo).

La unidad de independencia de la evaluación nueva es la **hoja física numerada**. Para cada hoja, todas sus páginas, paneles y ambas caras quedan fuera del entrenamiento. Se generan predicciones para cada uno de los 99 grupos compartidos por ZL3b e IT2a. Los intervalos del 95 % remuestrean las 99 hojas 1.999 veces; se mantiene fija cada predicción fuera de pliegue. Además del modelo publicado, comparé los rasgos iniciales, finales y longitud por separado. El modelo “seis rasgos separados” incorpora los tres rasgos de las dos palabras como seis variables categóricas independientes; es una extensión exploratoria, no el modelo original.

## Datos y preparación

| Fuente | SHA-256 | Páginas con texto | Hojas físicas numeradas | Líneas con tokens | Unidades extraídas |
|---|---|---:|---:|---:|---:|
| ZL3b | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | 207 | 99 | 4.130 | 35.318 |
| IT2a | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | 206 | 99 | 4.118 | 34.510 |

Se retuvo la primera lectura de alternativas entre corchetes, se quitaron etiquetas IVTFF/comentarios y se formaron unidades de palabras a partir de los separadores EVA. La sensibilidad secundaria descartó unidades afectadas por marcas de incertidumbre.

ZL3b contiene 206 páginas numeradas con texto y el pliego desplegable `fRos` (11 líneas); esto da las 207 páginas del conteo del artículo. `fRos` no tiene un número de hoja física comparable y se excluyó del análisis por hoja. Las dos transcripciones tienen las mismas 99 hojas numeradas con texto.

**Discrepancias de reconstrucción:** la extracción primaria arroja 35.318 unidades ZL3b frente a 34.963 informadas por el artículo. En el corte cada quinta página, obtengo 6.229 candidatos frente a 6.190. Los 719 límites positivos coinciden exactamente. No apareció ninguna línea normalizada idéntica compartida entre entrenamiento y prueba en ese corte, así que el embargo por duplicados no cambió el conjunto. Estas diferencias impiden etiquetar el resultado como reproducción exacta y apuntan a convenciones de tokenización/selección que el artículo no permite reconstruir completamente.

## Resultados principales

| Modelo | ZL3b: AUC fuera de hoja (micro) | AUC macro por hoja [IC 95 %] | Ganancia bits/hueco [IC 95 %] | IT2a: AUC micro | IT2a: ganancia bits/hueco |
|---|---:|---:|---:|---:|---:|
| Baseline de prevalencia | 0,500 | — | 0 | 0,500 | 0 |
| Solo inicio de ambas palabras | 0,841 | 0,819 [0,805–0,833] | 0,116 [0,102–0,129] | 0,843 | 0,117 |
| Solo final de ambas palabras | 0,759 | 0,763 [0,751–0,775] | 0,082 [0,073–0,091] | 0,768 | 0,087 |
| Solo longitud de ambas palabras | 0,616 | 0,612 [0,598–0,628] | 0,012 [0,009–0,016] | 0,625 | 0,015 |
| **Tupla completa (modelo del artículo)** | **0,854** | **0,835 [0,823–0,846]** | **0,111 [0,098–0,123]** | **0,856** | **0,115** |
| Seis rasgos separados (exploratorio) | 0,889 | 0,874 [0,863–0,885] | 0,163 [0,147–0,177] | 0,894 | 0,167 |

El resultado “micro” calcula AUC sobre todas las predicciones fuera de hoja concatenadas. El AUC macro promedia las AUC de los pliegues, dando el mismo peso a cada hoja; los intervalos de la tabla usan ese estimando macro. La ganancia e intervalo se calculan como promedio de ganancias por pliegue frente a la prevalencia de entrenamiento de ese pliegue. Los resultados completos por modelo y sensibilidad están en `results.json`.

En el corte cada quinta página, el modelo completo obtiene para ZL3b AUC **0,8443** y ganancia **0,1147** bits/hueco. Para IT2a obtiene AUC **0,8469** y ganancia **0,1189**. Al descartar unidades con incertidumbre, el AUC del modelo completo por página es **0,8438** en ZL3b y **0,8463** en IT2a; las conclusiones descriptivas no cambian de forma sustancial.

## Interpretación

La predicción persiste al retener hojas completas y se replica de forma aproximada en una transcripción EVA alternativa. La señal proviene en buena parte de rasgos iniciales; la longitud sola aporta poco. Separar los tres componentes de la tupla eleva la puntuación, pero esa variante no fue el modelo registrado en el artículo y se trata como exploratoria.

Esto es evidencia de **asociación estructural local**: los rasgos EVA próximos a un hueco ayudan a distinguir candidatos con y sin salto de línea. El experimento no separa idioma de hábitos del escriba, regularidades de maquetación, convenciones de transcripción u otros mecanismos. Tampoco constituye evidencia de traducción ni de que las tuplas tengan valor fonético.

## Auditoría, límites y reproducibilidad

- No se optimizaron parámetros con las etiquetas de prueba; α = 0,5 y los rasgos se fijaron siguiendo la descripción del artículo.
- El corte por hoja es una validación cruzada retrospectiva; no vuelve ciega la investigación previa. No consumí el manifiesto prospectivo reservado del proyecto.
- El artículo informa que sus scripts y revisiones exactas son necesarios para una reproducción exacta; no deposita allí los scripts de análisis. Por ello, este trabajo reconstruye el método descrito de forma independiente.
- El intervalo de hoja mantiene fijas las predicciones fuera de pliegue y no incorpora incertidumbre del corpus, del parser, ni variación por reentrenar cada bootstrap.
- El experimento solo incluye líneas del cuerpo identificadas por loci P; los límites se crean entre palabras adyacentes dentro de una página. No se genera un candidato que cruce a otra página o a otra hoja.
- ZL3b e IT2a no son observaciones independientes: comparten el objeto histórico y su segmentación general.
- No se asigna un nuevo ID EXP ni se modifica el registro de afirmaciones del proyecto.

El script y el JSON de resultados se incluyen junto a este informe. Para repetir desde una copia del repositorio, coloque las transcripciones en el mismo directorio con los nombres `eva_zl3b.txt` y `eva_it2a.txt`, y ejecute `python line_boundary_replication.py`.

## Referencias

Zenil, H. & Uthamacumaran, A. (2026). *Reconstruction of Geometric and Structural Aspects of Undeciphered Messages by Information-theoretic Methods*. arXiv:2610.08861. [Artículo y métodos](https://arxiv.org/abs/2610.08861).

Transcripciones en el manifiesto del repositorio: [ZL3b e IT2a, `kyrian20/voynich-autoexploration`](https://github.com/kyrian20/voynich-autoexploration/tree/master/data/transcriptions). Los SHA-256 anteriores identifican los bytes realmente analizados.

