# Revisión externa — actualización 2026-10-30

**Alcance:** búsqueda focalizada de publicaciones y preprints recientes ajenos al repositorio. Esta nota importa preguntas y límites metodológicos; no afirma que hayamos reproducido sus resultados. Se revisaron los registros, resúmenes y materiales públicos enlazados; cuando el texto completo o el código no estuvo disponible, se indica.

## Hallazgos con consecuencias para nuestro trabajo

### 1. Modelos rivales calibrados: las estadísticas del texto no identifican por sí solas el mecanismo

**Xin Zhang y Victor S. Sheng, “Does the Voynich Manuscript Mean Anything? Calibrated Tests Find Little Trace of Language” (arXiv:2610.34499, preprint del 25-10-2026).** [Registro/arXiv](https://arxiv.org/abs/2610.34499)

El resumen informa comparaciones con presupuestos de ajuste iguales y estadísticas de evaluación no usadas durante el ajuste. El generador de copia/modificación de Timm–Schinner ajusta mejor que un cifrado de una sola clave; sin embargo, un cifrado con claves que cambian entre A/B y un código de clases de palabras ajustan de forma comparable. Los autores reportan una señal de pares de palabras compartiendo línea más débil en Voynich que en sus textos de control y límites explícitos de recuperación para las familias de cifrado ensayadas. No concluyen que toda codificación con significado sea imposible.

La lectura del texto completo precisa que queda sin excluir un nomenclátor con segunda clave en 9 de las 16 lenguas evaluadas; no es una lectura del manuscrito. Los autores también atribuyen gran parte de la señal del descifrador de letras a la dependencia del último glifo de una palabra con el primero de la siguiente, y dicen que ninguno de sus programas reproduce conjuntamente esa dependencia y los espacios. Es una observación concreta para cotejar con nuestras métricas de bordes, no evidencia de semántica ni una réplica de nuestros análisis.

**Límites y estado de evidencia:** preprint reciente; hallazgos reportados por los autores, no reproducidos aquí. El propio artículo limita la conclusión a programas, códigos, transformaciones e idiomas específicos; los dos descifradores usan modelos de bigramas y los autores reconocen que su modelo de copia recibe reglas derivadas del manuscrito, mientras los cifrados no tienen la misma información específica. ZL3b e IT2a comparten convenciones de transcripción, por lo que no son muestras independientes. En las fuentes consultadas no se identificó un paquete de código enlazado; esto no demuestra que no haya material adicional.

**Consecuencia:** nuestros patrones de orden, posición y dependencia no deben presentarse como discriminantes entre lengua, cifrado y generación sin una prueba de recuperación calibrada y controles de familias rivales. No repetir EXP-590 ni los controles de orden ya archivados: no estiman necesariamente las mismas cantidades. Cuando se elija una reproducción externa, fijar primero métrica, unidad de partición, corpus y criterio de éxito; reproducir el método antes de proponer una variante.

### 2. Proceso dinámico de copia como hipótesis rival

**Torsten Timm, “The challenge of analyzing a dynamic text: why the Voynich manuscript resists conventional interpretation” (Cryptologia, publicado en línea en 2026).** [DOI](https://doi.org/10.1080/01611194.2026.2693462)

El resumen del artículo propone que la evolución gradual del vocabulario, las formas y sus frecuencias encaja con producción por copia y modificación iterativa. Es una explicación rival concreta; no demuestra por sí misma que el texto carezca de contenido, ni la evolución descriptiva identifica necesariamente su causa.

**Consecuencia:** incluir “proceso dinámico de copia/modificación” explícitamente en la matriz de mecanismos, al lado de cifrados estáticos y cifrados con cambio de clave. Contrastar predicciones que separen mecanismos; no inferir ausencia de significado a partir de deriva léxica sola. El artículo completo y sus datos no se reprodujeron en esta revisión.

### 3. Orden físico y particiones de evaluación

**Colin Layfield y Lisa Fagin Davis, “Singulion Structure and the Voynich Manuscript” (Digital Medievalist 19, 2026).** [Artículo](https://doi.org/10.4000/16k0a)

El trabajo propone, a partir de análisis de similitud y comparación con códices conocidos, que el objeto pudo componerse originalmente de bifolios sueltos (“singulions”) y que el orden encuadernado actual no representa necesariamente el orden de lectura original. Es una hipótesis codicológica; no es una lectura del texto. El sitio de la revista impidió consultar el texto completo en esta revisión; el resumen y la referencia bibliográfica sí estuvieron disponibles. El proyecto ya había registrado esta hipótesis en su estrategia y memo de octubre.

**Consecuencia:** mantener intacta la fuente canónica y no reordenar líneas según una señal de similitud. Para futuras pruebas confirmatorias, preservar juntas las dos caras del mismo soporte físico y reportar sensibilidad al orden alternativo únicamente si hay una reconstrucción externa, documentada y congelada antes de medir resultados. El orden propuesto no se ha adjudicado aquí.

### 4. Un modelo híbrido y una prueba negativa de rótulos zodiacales

**Vitaly Averyanov, Voynich Studies, dos preprints con paquete público de replicación:** [“A Workshop Cipher”](https://voynich.site/paper-1-mechanism?lang=en), [“Thirty Names per Sign”](https://voynich.site/paper-2-labels?lang=en), [datos y código](https://voynich.site/data-and-code?lang=en).

El primer preprint propone combinar un cifrado verbose de clase Naibbe con tablas, reutilización serial de lo recién escrito, elección condicionada por el borde gráfico y errores de copia. El segundo propone que los rótulos zodiacales sean siglas cortas asociadas a listas cerradas por signo; describe una batería para rechazar fuentes candidatas de nombres por grado y reporta resultados negativos para varias clases. El sitio enlaza un paquete con scripts, informes, corpus normalizados y registros de afirmaciones. Sus páginas indican que los trabajos son preprints y que se busca revisión/publicación.

**Estado de evidencia:** mecanismo e interpretación son afirmaciones de un proyecto externo, no consenso ni replicación nuestra. El paquete sí es una oportunidad verificable; antes de ejecutarlo hay que fijar versión, licencia, hashes, dependencias y una afirmación pequeña que no duplique nuestros controles. El número de DOI aparece inconsistente entre páginas del propio sitio; por eso esta nota enlaza los registros del proyecto y no fija un DOI hasta resolver la discrepancia.

**Consecuencia:** el híbrido es un adversario útil frente a cualquier inferencia de que la estructura A/B o el encadenamiento de bordes requieran semántica. La hipótesis de siglas obliga a distinguir rótulos de prosa; no autoriza asignar nombres ni sirve como crib para el texto corrido. El paquete no se copia al repositorio, y sus afirmaciones no se elevan de estado hasta auditoría y reproducción.

### 5. Actualización de una propuesta morfológica externa

**Matthew Dominik, “Structural Decipherment Without Lexical Recovery: A Cross-Validated Morphological Analysis of the Voynich Manuscript”, Zenodo v2, 18-10-2026.** [Registro v2](https://zenodo.org/records/23444474)

La versión 2 reporta 39 cuerpos superficiales CORE-0, acoplamientos morfológicos y una red dirigida de 28 nodos replicada entre calibración, holdout y transcripción alternativa. También declara fallidos sus intentos de pasar de estructura a significado léxico. Sus 12.299 de 12.495 posiciones naturalizables (98,4314 %) son una medida condicional de madurez de un benchmark restringido de 1.609 líneas, no precisión de traducción ni cobertura literal del manuscrito. La página de Zenodo inspeccionada lista el PDF; no pude verificar desde ella un paquete ejecutable completo.

**Estado de evidencia:** preprint del autor; resumen y metadatos consultados, paquete no auditado en esta revisión. El repositorio ya tenía una nota sobre v1; v2 actualiza esa referencia, no constituye confirmación independiente.

**Consecuencia:** comparar solo una afirmación superficial pequeña si se identifica una predicción que distinga reglas y no dependa de sus propias etiquetas de rol. No importar la terminología “desciframiento estructural” como si implicara recuperación semántica.

### 6. Cautela sobre la literatura de LSA

Layfield y Davis también publicaron “The Application of Latent Semantic Analysis to the Voynich Manuscript” en *Digital Humanities Quarterly* 20(1), 2026. [DOI](https://doi.org/10.63744/2ezxpskcezq4). El análisis de similitud latente puede informar sobre coherencia de uso/distribución; sin texto legible, no confirma que la semejanza sea semántica.

Existe una nota crítica pública de Torsten Timm que cuestiona cuatro caracterizaciones de fuentes citadas en ese artículo: [Zenodo](https://zenodo.org/records/20429073). Es una crítica de parte interesada y no se adjudicó aquí contra los trabajos citados. Antes de reutilizar afirmaciones historiográficas o de Currier de ese artículo, cotejar cada cita con la fuente primaria. No usar la disputa bibliográfica como razón para aceptar la hipótesis de copia.

## Decisiones incorporadas

1. **No se crea EXP nuevo ni se ejecuta ningún modelo** como consecuencia de esta revisión. Primero siguen vigentes los bloqueos del registro, la política IVTFF, la identidad de los corpus y las reglas de partición física.
2. La matriz de explicaciones debe conservar como rivales explícitos: lengua/código, cifrado de clave fija, cambio de clave o clase de palabra, mecanismo híbrido, y generador/copia dinámica. No asignar probabilidades no calibradas ni declarar una familia descartada por un único ejemplo.
3. Para evaluar un mecanismo, exigir recuperación de contenido conocido en controles y desafíos adversariales; un buen ajuste estadístico o predicción estructural no equivale a descifrado.
4. Una futura réplica externa se seleccionará entre una predicción falsable de Zhang–Sheng, un test pequeño del paquete Averyanov, o una sensibilidad de partición codicológica. Elegir solo tras revisar sus materiales exactos y solapamiento con experimentos existentes; no abrir tres líneas paralelas.
5. No se añadió traducción candidata, referente semántico ni interpretación iconográfica como hecho. No hubo llamada nueva a Gemini ni se enviaron datos del manuscrito a servicios externos.

## Registro de consulta

Búsqueda pública realizada el 2026-10-30. Se priorizaron artículos, preprints con identificador persistente y páginas de datos/código de los autores. Esta selección no es un censo exhaustivo. Resultados atribuidos a sus autores, salvo donde se indique reproducción en este repositorio.
