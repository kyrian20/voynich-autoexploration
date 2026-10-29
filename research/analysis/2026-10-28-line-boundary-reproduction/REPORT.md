# Réplica independiente: predicción de límites de línea en el Manuscrito Voynich

**Fecha de ejecución:** 28 de octubre de 2026  
**Estado:** reimplementación independiente ejecutada y repetida de forma determinista; coincidencia aproximada con el artículo, no reproducción bit a bit.  
**Repositorio base consultado:** `kyrian20/voynich-autoexploration`, `master` en `9134d8c872f35602912512b33d27b8e9cc8bff67`.  
**Identificadores de experimento:** ninguno asignado; la numeración del proyecto permanece congelada.

> **Errata de normalización de categorías no vistas — 29-10-2026 (corrección de código; sin nueva réplica científica):** el clasificador categórico Naive Bayes aplicaba suavizado `alpha` con denominador `n_clase + alpha * V`, siendo `V` el número de categorías observadas en entrenamiento, pero asignaba también probabilidad positiva `alpha / (n_clase + alpha * V)` a valores no vistos. Esto producía masa total superior a 1 sobre las categorías observadas más una categoría no vista. Ejemplo con tres observaciones de una clase, una sola categoría observada y `alpha=0.5`: masa observada 1 y masa no vista 1/7, total 8/7. Se reserva ahora una categoría OOV explícita con denominador `n_clase + alpha * (V+1)` tanto para categorías vistas como no vistas. En una regresión sintética con tres negativos, un positivo, dos características constantes y dos valores OOV en evaluación, el posterior positivo pasa de 0,7 (código anterior) a 12/19 ≈ 0,631579. La prueba del prior binario se aísla con cero características para no confundir el prior con la verosimilitud suavizada. **Todas las probabilidades y métricas del `results.json` histórico siguen congeladas y `INVALID_FOR_CLAIM` como estimaciones de este clasificador con soporte categórico normalizado**. No se ha ejecutado de nuevo el análisis sobre ZL3b/IT2a ni usado hojas prospectivas reservadas. La elección de un único cubo OOV es una política de modelado explícita, no una afirmación lingüística; deben evaluarse otras políticas y la adjudicación IVTFF antes de extraer conclusiones.
>

> **Errata de continuidad en lectura primaria — 29-10-2026 (reparación de código, sin nueva réplica):** el parser eliminaba `?` antes de construir candidatos en el modo `primary`. Una línea `alpha.?.beta` se convertía en `[alpha,beta]` y producía un par adyacente falso; `ab?cd` se dividía en dos palabras ficticias. Ahora un token con `?` se conserva como barrera `None` en la construcción de candidatos de ambas políticas; `tokens(..., preserve_gaps=False)` sigue omitiendo unidades inciertas en la interfaz de salida. Las regresiones sintéticas comprueban la barrera intralínea, el caso de interrogación incrustada y la ausencia de un salto de línea falso cuando la última unidad es incierta. Esta corrección **no acredita** cuántos casos reales están afectados ni recalcula `results.json`; sus métricas `primary` quedan **INVALID_FOR_CLAIM específicamente como evaluación que respeta barreras de grafemas desconocidos**, hasta una nueva ejecución verificada. El original se conserva y la adjudicación completa IVTFF continúa pendiente.
>

> **Errata de integridad — 29-10-2026, revisión de PR #138:** el modo
> `drop_uncertain_word` eliminaba las marcas `[primaria:alternativa]` antes
> de comprobar incertidumbre, por lo que retenía palabras afectadas por
> corchetes. Prueba falsable: `tokens("ab[cd:ef]gh", "drop_uncertain_word")`
> devolvía `["abcdgh"]` en lugar de `[]`. El código se ha corregido y se
> añaden regresiones para las dos modalidades; **el `results.json` original
> permanece congelado**. Sus métricas `drop_uncertain_word` quedan
> **INVALID_FOR_CLAIM** como evidencia de exclusión efectiva de corchetes
> hasta una nueva ejecución completa y contrastada con el mismo corpus/hash.
> Las métricas `primary` no se recalculan ni reciben validación científica
> adicional por esta corrección. Sigue pendiente la adjudicación IVTFF
> completa y la reconstrucción de las diferencias de conteo con el artículo.

> **Revisión adicional de integridad — 29-10-2026 (sin nueva ejecución de métricas):** el filtro corregido todavía eliminaba palabras inciertas antes de construir pares y, por tanto, podía crear adyacencias artificiales entre vecinos que no eran contiguos en el original, o incluso un salto entre líneas a través de una línea compuesta solo por palabras inciertas. El constructor conserva ahora barreras `None` en el modo de exclusión y omite candidatos que las cruzan. La API pública `tokens(..., "drop_uncertain_word")` conserva su salida sin barreras; el parser usa `preserve_gaps=True` exclusivamente para construir candidatos. También se ha corregido la ruta de entrada: las transcripciones versionadas están en `data/transcriptions/`, no junto al script. El ejecutable verifica SHA-256 fijados antes de analizar y crea su archivo nuevo en modo exclusivo, rechazando sobrescrituras y enlaces simbólicos. **No se ha reejecutado el experimento completo ni reemplazado `results.json`. Todas las cifras archivadas de `drop_uncertain_word` siguen `INVALID_FOR_CLAIM` para la sensibilidad declarada**; el estado de `primary` no cambia. Estas correcciones se comprueban mediante regresiones de comportamiento y CI, no mediante una reproducción numérica del estudio. La conformidad IVTFF integral sigue pendiente.

> **Contrato de filas físicas — 29-10-2026 (corrección de código sin recalcular métricas):**
> el lector de esta réplica empleaba `str.splitlines()`, que interpreta
> separadores de control como filas nuevas; un byte Latin-1 U+0085 dentro
> de una línea podía crear un locus aparente `<f2r.P.1,P0>` que no existía
> como registro físico. El parser usa ahora el lector compartido
> `scripts/ivtff_physical_rows.py`, que solo acepta CR, LF y CRLF y rechaza
> los demás separadores. Se añadieron pruebas de inyección de loci falsos y
> de los tres finales de línea válidos. La entrada versionada sigue protegida
> por SHA-256; **no hay evidencia de que el defecto afectara a los corpus
> congelados, y no se han regenerado las puntuaciones archivadas**.
> Esta corrección no resuelve la conformidad IVTFF ni habilita por sí sola
> ninguna afirmación de descifrado.

> **Errata de métrica AP — 29-10-2026 (sin regenerar resultados):**
> `ap(y,s)` ordenaba candidatos por puntuación y sumaba precisión por
> cada positivo. Cuando varias observaciones tenían la misma probabilidad,
> el orden original de las filas decidía arbitrariamente el AP: con
> `s=[0.5,0.5]`, `y=[1,0]` producía 1.0 y `y=[0,1]` producía 0.5,
> pese a ser la misma predicción y las mismas etiquetas. El código ahora
> agrupa todos los empates como un único umbral de puntuación y calcula el
> AP no interpolado por grupos; las regresiones comprueban invariancia ante
> permutación, empates parciales y casos sin empates. **Los AP de
> `results.json` quedan `INVALID_FOR_CLAIM` para una métrica AP
> invariante a empates hasta repetir y cotejar la ejecución corregida.**
> Esta errata no cambia el cálculo de AUC, ganancia de log-loss o Brier,
> ni demuestra que sus valores archivados sean válidos. No se ha
> reejecutado el estudio completo, ni se han modificado corpus,
> `results.json`, particiones, parámetros o semillas. La limitación
> IVTFF y las erratas de `drop_uncertain_word` continúan vigentes.

> **Errata de prior Naive Bayes — 29-10-2026 (parche de código; no ejecución científica):**
> `pred()` calculaba el término de prior de cada clase con
> `(n_clase + 2*alpha)/(n_total + 2*alpha)`, aunque el modelo descrito
> emplea un prior binario simétrico Dirichlet(`alpha`, `alpha`).
> La forma correcta es `(n_clase + alpha)/(n_total + 2*alpha)`.
> Con tres candidatos negativos y uno positivo, rasgos categóricos
> idénticos y `alpha=0.5`, el programa anterior predecía 1/3 para
> la clase positiva; el prior correcto predice 0,3. Es una discrepancia
> demostrable sin consultar el manuscrito. Se ha reparado el código y
> añadido una regresión con cuatro casos, incluidas clases desequilibradas
> y una clase ausente. **No se han recalculado los valores de
> `results.json`**: las métricas archivadas son `INVALID_FOR_CLAIM`
> específicamente como estimaciones del clasificador con prior binario
> Dirichlet(`alpha`, `alpha`) hasta ejecutar y auditar la versión
> corregida. El predictor anterior sigue siendo una función determinista
> cuya salida histórica se conserva; este defecto no demuestra que toda
> predictibilidad desaparezca, ni valida traducción o semántica.
> La corrección puede cambiar probabilidades, ganancia logarítmica,
> Brier, AP y métricas AUC agrupadas entre hojas. Las limitaciones de
> tokenización, selección de pares, empates AP y adjudicación IVTFF
> permanecen abiertas. Las fuentes originales, semillas, folios reservados
> y artefactos históricos no se han modificado.

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

En el corte cada quinta página, el modelo completo obtiene para ZL3b AUC **0,8443** y ganancia **0,1147** bits/hueco. Para IT2a obtiene AUC **0,8469** y ganancia **0,1189**. La ejecución archivada informó AUC **0,8438** (ZL3b) y **0,8463** (IT2a) bajo la etiqueta `drop_uncertain_word`, pero el filtro no excluía palabras con corchetes. **Estas dos cifras se conservan solo como historia y no sostienen una conclusión de sensibilidad a la incertidumbre**; debe reejecutarse el análisis corregido antes de interpretarlas.

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

El script y el JSON de resultados se incluyen junto a este informe. Para una nueva ejecución desde la raíz del repositorio, use `python research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py`. El script lee las transcripciones versionadas en `data/transcriptions/`, verifica sus SHA-256 y crea `line_boundary_results.json` exclusivamente si no existe. Si ya existe, se detiene sin sobrescribir; archive cada salida nueva con su hash y log por separado. No confunda esa salida nueva con el `results.json` histórico congelado.

## Referencias

Zenil, H. & Uthamacumaran, A. (2026). *Reconstruction of Geometric and Structural Aspects of Undeciphered Messages by Information-theoretic Methods*. arXiv:2610.08861. [Artículo y métodos](https://arxiv.org/abs/2610.08861).

Transcripciones en el manifiesto del repositorio: [ZL3b e IT2a, `kyrian20/voynich-autoexploration`](https://github.com/kyrian20/voynich-autoexploration/tree/master/data/transcriptions). Los SHA-256 anteriores identifican los bytes realmente analizados.



## Corrección de integridad — 29-10-2026: filas P vacías y adyacencias inventadas

**Ámbito:** rama de la PR #138, sin EXP nuevo. La reparación se propone por separado y requiere CI y revisión antes de integrarse. Los corpus, el `results.json` histórico, los manifiestos reservados y las semillas no se modifican.

**Defecto falsable:** el parser descartaba filas físicas de cuerpo con cero tokens (por ejemplo `<f1r.P.2,P0> ???`) antes de construir los pares. Con `<f1r.P.1,P0> alpha`, una fila P vacía y `<f1r.P.3,P0> beta`, el constructor anterior producía un candidato positivo artificial `alpha → beta`, aunque no son líneas consecutivas. Además, una fila `<f1r.P.2,P0>` sin payload se descartaba por el requisito de espacio posterior a la etiqueta. No se ha demostrado todavía cuántos casos de este tipo existen en los corpus congelados.

**Reparación:** conservar filas P sin tokens como barreras de continuidad; impedir candidatos que toquen esas filas y no permitir conexiones entre sus vecinas. Las páginas compuestas únicamente por filas vacías continúan excluidas del conjunto de páginas de calibración, evitando desplazar el corte histórico cada quinta página. La expresión regular reconoce explícitamente loci P con payload vacío y sigue rechazando texto pegado a la etiqueta sin separador. La nueva suite sintética comprueba filas vacías por signos, filas sin payload, páginas enteramente vacías y manejo directo de barreras, sin datos del manuscrito ni aleatoriedad.

**Estado científico:** corrección de un defecto lógico, no nueva ejecución del modelo. Las puntuaciones históricas de `results.json` siguen congeladas y no pueden reutilizarse para afirmar que se aplicó el contrato corregido de continuidad. Tampoco se ha demostrado un cambio numérico en la población real. Los demás bloqueos (adjudicación IVTFF, continuidad entre tipos de locus, lectura de ligaduras, incertidumbre, suavizado y AP históricos) permanecen abiertos. Una ejecución posterior deberá guardar resultados nuevos, hashes, parámetros y logs, sin sustituir la reproducción histórica.

## Errata de selección — 29-10-2026: páginas con solo centinelas de incertidumbre

**Defecto lógico y alcance:** en la sensibilidad `drop_uncertain_word`, una página que solo contuviera una palabra incierta se representaba como `[None]`. El filtro final `any(row["words"] for row in ls)` consideraba esa lista no vacía, aunque no hubiera ninguna palabra utilizable. La página entraba indebidamente en la lista ordenada para la calibración de «cada quinta página», con posibilidad de desplazar la selección de prueba. Las filas de incertidumbre **dentro de páginas pobladas** deben seguir conservándose como barreras de continuidad.

**Corrección:** exigir al menos una palabra distinta de `None` para incluir una página; no eliminar las filas barrera de páginas válidas. Una regresión con páginas sintéticas `f1r`–`f4r` verifica ambas políticas: la página `f2r` con `[cd:ef]` se conserva en la lectura primaria y se excluye en la sensibilidad; `f3r` con `?` queda excluida en ambas. El cambio no asigna un EXP, no modifica corpus ni el `results.json` congelado y no consume folios prospectivos reservados.

**Limitación:** esta prueba sintética demuestra un defecto y su reparación, no demuestra que existan páginas de este tipo en las transcripciones congeladas ni cuantifica un cambio real de métricas. Los resultados históricos de `drop_uncertain_word` siguen `INVALID_FOR_CLAIM` para la política corregida hasta ejecutar y archivar una nueva réplica verificable. La adjudicación IVTFF completa y las otras erratas de la PR continúan pendientes.


## Errata de continuidad — 29-10-2026: ligaduras IVTFF como falsas separaciones

**Defecto concreto (reproducción sintética y ejemplo presente en ZL3b):** el tokenizador de esta réplica reemplazaba el contenido `{...}` por un espacio y después extraía secuencias alfabéticas. Así, `dlo{ct}o` se transformaba en dos palabras ficticias `["dlo","o"]`, creando un candidato negativo dentro de una sola unidad gráfica. El texto congelado ZL3b contiene esa forma en `f1r.19`; también contiene `{c'y}` en `f1r.7`. La norma IVTFF 2.0.2, §6.6, identifica las llaves como ligaduras, **no como separadores de palabras**. Este defecto es independiente de los errores previos de corchetes, interrogaciones, prior y OOV.

**Corrección conservadora:** en la ruta de construcción de candidatos, cualquier palabra con `{` o `}` pasa a ser un centinela `None`, en ambas políticas. Se rechazan también marcadores mal cerrados. Se conservan las palabras seguras vecinas, pero nunca se conectan a través de la ligadura ni se inventan dos palabras a partir de ella. Esta decisión es un **fail-closed provisional**, no una interpretación completa de ligaduras: el contrato IVTFF recomienda conservar una capa bruta y una vista de expansión de grafemas antes de cualquier análisis confirmatorio. No se asigna valor lingüístico a las ligaduras.

**Pruebas nuevas:** tres regresiones en `tests/test_line_boundary_uncertainty_contract.py` para (1) ligaduras dentro de palabra y aisladas, (2) no creación de pares ni saltos falsos en filas P sintéticas, (3) llaves mal cerradas. Comando: `python -m unittest discover -s tests -p 'test_line_boundary_uncertainty_contract.py'` y repetición con `python -O`. El resultado de CI se debe registrar tras su ejecución; esta errata por sí sola no demuestra que haya pasado.

**Estado de evidencia:** los `results.json` históricos permanecen inmutables; las métricas previas de la política `primary` son `INVALID_FOR_CLAIM` como estimación que respeta ligaduras. No se han recalculado conteos, AUC, AP, Brier ni ganancias, ni se han consumido folios prospectivos reservados. El ejemplo real prueba presencia de la clase de entrada, **no cuantifica** el impacto estadístico. Siguen pendientes la adjudicación integral IVTFF, la expansión no destructiva de ligaduras y la reconstrucción exacta de las entradas del artículo.
