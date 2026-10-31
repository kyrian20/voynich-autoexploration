# Revisión externa: pruebas calibradas y morfología estructural — 31-10-2026

**Estado:** revisión de literatura y alcance; no es reproducción independiente ni resultado del manuscrito.
**EXP:** no asignado. No se ejecutó un análisis nuevo ni se modificaron corpus, resultados históricos, particiones o estado científico.

## 1. Zhang y Sheng — pruebas calibradas de cifrado frente a generación

**Fuente primaria:** Xin Zhang y Victor S. Sheng, “Does the Voynich Manuscript Mean Anything? Calibrated Tests Find Little Trace of Language”, arXiv:2610.34499v1, enviado el 25-10-2026.  
https://arxiv.org/abs/2610.34499

### Qué informan los autores

El preprint compara programas de copia y familias de cifrado usando el mismo presupuesto de búsqueda, evalúa estadísticas no usadas durante el ajuste y calibra los descifradores con textos de control. Para la huella lingüística sin descifrado usa 28 textos en 16 lenguas y mide, entre otros aspectos, la repetición de pares de palabras en líneas. También prueba mensajes plantados y variantes de códigos por palabra.

Los autores informan que:

- El modelo de copia de Timm predice las estadísticas retenidas mejor que los cifrados de una sola clave evaluados; ciertos modelos con segunda clave y uno que cifra clases de palabras quedan igual de cerca.
- La asociación de pares de palabras entre líneas en el Voynich es aproximadamente la mitad de la observada en el control lingüístico más débil de su conjunto.
- Sus descifradores no obtienen texto legible bajo las familias de cifrado probadas, condicionando cada decisión a que los controles pertinentes sí sean legibles.
- No excluyen un nomenclátor de segunda clave en 9 de las 16 lenguas ensayadas. Para igualar algunas medidas necesita una tasa alta de errores de copia.
- La dependencia entre el último glifo de una palabra y el primero de la siguiente explica gran parte de la señal del descifrador de letras. Ninguno de los programas probados reproduce conjuntamente esa dependencia y los espacios observados.

Estos son **resultados reportados por los autores**, no réplicas nuestras. El propio trabajo concluye que ningún programa ensayado pasa todos sus controles conjuntos; no decide por ello entre todas las explicaciones posibles.

### Límites expresos y reproducibilidad

La sección de límites del preprint restringe sus conclusiones a los programas, códigos, idiomas y transformaciones probados. No cubre, entre otros, claves variables de otras formas, transposiciones adicionales o textos transformados antes del cifrado. Los autores señalan que parte de las reglas de copia se deriva del propio manuscrito, mientras los cifrados no reciben la misma información específica; ambos descifradores usan modelos de bigramas. También reconocen que ZL3b e IT2a comparten convenciones de separación y de glifos que afectan las medidas de frontera, por lo que no son dos manuscritos ni dos réplicas independientes. La prueba de mensajes cortos tiene baja potencia para esquemas con homófonos o huecos.

En las fuentes consultadas para esta nota no localicé un repositorio de código o un paquete de reproducción asociado al preprint. El registro de arXiv proporciona el preprint (v1, 153 kB); esto **no demuestra que el código no exista**. No se contactó a los autores.

### Relación con nuestro trabajo

El resultado de frontera es relevante para los análisis locales de orden y de posición del proyecto, pero no es el mismo estimando que el predictor de identidad, las auditorías de tokens o los patrones de inicio/final ya registrados. En particular, una dependencia entre bordes de palabras puede surgir de convenciones de transliteración o de acoplamiento gráfico; por sí sola no identifica unidades lingüísticas ni significado.

Los resultados propios de orden residual ya describen ganancias pequeñas e inciertas de identidad en las vistas Voynich y ganancias mayores en controles de César y Dante ([informe integrado](analysis/2026-10-22-residual-order/REPORT.md)). Esa coincidencia conceptual no reproduce la medida del nuevo artículo ni confirma su explicación causal.

**Siguiente paso condicionado:** una vez resueltos los bloqueos de parser y archivo, identificar primero la definición exacta de dependencia entre fronteras que usan Zhang y Sheng y cotejarla con nuestras métricas existentes. Solo diseñar una reproducción si hay código o suficientes detalles, control de lectura por folio y una predicción que diferencie modelos. No asignar EXP hasta reconciliar el registro y cerrar los bloqueos actuales.

## 2. Dominik — análisis morfológico cruzado sin recuperación léxica

**Fuente primaria:** Matthew Dominik, “Structural Decipherment Without Lexical Recovery: A Cross-Validated Morphological Analysis of the Voynich Manuscript”, Zenodo v2.0, publicado el 18-10-2026, DOI [10.5281/zenodo.23444474](https://doi.org/10.5281/zenodo.23444474).

La versión 2 informa una morfología de borde izquierdo, 39 cuerpos CORE-0 transferibles y una red dirigida de 28 nodos replicada en sus particiones de calibración, holdout y transcripción alternativa. Informa además 12.299 de 12.495 posiciones con roles asignables en un benchmark restringido. El autor advierte expresamente que el 98,4314 % es una medida condicional de madurez del benchmark, **no** exactitud de traducción ni recuperación de texto plano. El mismo resumen señala que los intentos de pasar de organización estructural a significado léxico no superaron sus criterios de promoción.

El registro de Zenodo consultado lista el PDF como archivo visible; desde la página inspeccionada no pude verificar un paquete ejecutable de scripts, datos, particiones y resultados. La versión 1 ya aparecía en el escaneo externo del 20-10; esta nota registra que la v2 contiene afirmaciones actualizadas, sin validar su cambio frente a v1.

**Valor para nuestro proyecto:** sus particiones protegidas y su freno explícito a la interpretación semántica son buenas prácticas que merece auditar. Los roles CORE y nuestra morfología observada no se deben equiparar sin una definición operacional común, correspondencias exactas y conteos reconstruidos. No se adopta el porcentaje de benchmark como evidencia de descifrado.

## 3. Decisión de trabajo

1. Incorporar ambos trabajos al mapa bibliográfico como métodos y resultados publicados por sus autores, no como hallazgos propios.
2. Mantener separadas tres preguntas: regularidad de glifos dentro de la palabra, dependencia entre palabras adyacentes y recuperación de contenido lingüístico. Una mejora en una no responde automáticamente las otras.
3. No abrir ahora una nueva prueba: el repositorio sigue en auditoría y la política vigente bloquea nuevos EXP hasta reconciliar el registro, resolver los asuntos IVTFF pertinentes y la trazabilidad de artefactos.
4. Cuando se despejen esos bloqueos, priorizar una comparación estrecha de la dependencia de borde palabra-final → palabra-inicial con el trabajo de Zhang y Sheng, solo si pueden reconstruirse la métrica y los controles. Evaluar por folio, informar la política de transcripción y mantener ZL3b/IT2a como ediciones relacionadas, no muestras independientes.
5. Buscar los materiales ejecutables citados o enlazados por los autores antes de llamar “réplica” a una implementación propia. Si no están disponibles, etiquetar cualquier intento como implementación independiente.

## Fuentes y alcance de la búsqueda

- Zhang y Sheng, arXiv:2610.34499v1: https://arxiv.org/abs/2610.34499
- Dominik, Zenodo v2.0: https://zenodo.org/records/23444474
- Contexto interno: `research/EXTERNAL_RESEARCH_REVIEW.md`, `research/external_research_scan_2026-10-20.md`, `research/analysis/2026-10-22-residual-order/REPORT.md`, `research/RESEARCH_INTEGRITY_STANDARD.md` y `research/ORDER_AND_STABILIZATION_STATUS_2026-10-21.md`.

Se revisaron las páginas primarias y el texto disponible del preprint el 31-10-2026. La búsqueda de código fue acotada; no es una revisión exhaustiva de la web. No se ejecutaron scripts externos, no se recalcularon métricas del manuscrito y no se verificaron independientemente los resultados reportados.
