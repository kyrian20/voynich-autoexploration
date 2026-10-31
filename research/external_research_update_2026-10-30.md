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


### 7. Seguimiento de la medida de pares recurrentes en un generador rival

**Vitaly Averyanov, actualización pública del 27-10-2026 sobre su modelo de cifrado verbose** ([sitio del proyecto](https://voynich.site/?lang=en); [artículo y estado editorial](https://voynich.site/publications?lang=en); [datos y código](https://voynich.site/data-and-code?lang=en)). La nota aplica la medida de Zhang–Sheng: cuánto se repiten en otras líneas del libro los mismos pares de palabras que ya comparten una línea.

Averyanov informa una reimplementación descriptiva con valor 0,078 para el texto manuscrito, frente al 0,071 reportado por Zhang–Sheng para ZL; después comunica otro contraste preregistrado, con valores de 0,082 para el manuscrito, 0,106 para su muestra de texto sin sentido y 0,138 para su modelo (rango 0,112–0,156 en 20 semillas nuevas). El valor 0,078 no coincide exactamente con el 0,071 publicado, y la página no permite adjudicar si la diferencia procede de la población, normalización o implementación. No se deben mezclar las dos series como una reproducción byte a byte.

El autor dice que el exceso del modelo persiste al cambiar el texto fuente, retirar cualquiera de cinco capas del generador y corromper palabras. Si se confirma con el paquete y una medición común, el resultado mostraría que esa estadística puede aparecer por el mecanismo de escritura y no identifica por sí sola contenido lingüístico. No contradice automáticamente el resultado de Zhang–Sheng: compara otro generador, y ambos trabajos reportan condiciones y valores que requieren reconstrucción independiente.

**Estado de evidencia:** resultado publicado por Averyanov en su propio sitio sobre su propio modelo; el sitio informa que el artículo continúa como preprint en revisión. No es una replicación independiente del generador ni una validación externa de la medida. El proyecto anuncia un paquete público de scripts y corpus, pero sus páginas consultadas discrepan sobre tamaño y recuento de archivos (3,0 MB/226 archivos frente a 43,3 MB/208 scripts en la versión v1.2). En esta actualización no se ha descargado, congelado ni auditado un archivo concreto, su licencia, dependencias o hashes.

**Consecuencia:** añadir el generador de Averyanov a la lista de rivales a contrastar y registrar como pendiente la discrepancia 0,071/0,078/0,082. No importar esas cifras a nuestros resultados ni diseñar una nueva métrica sobre la misma muestra sin un protocolo común, tokenización congelada y comparación de semillas retenidas. La medida de recurrencia de pares, por sí sola, no puede tratarse como detector de significado.

### 8. Dependencia entre abridores de líneas: medida nueva y solapamiento local

**Vitaly Averyanov, “Line openers in the Voynich manuscript: lines remember each other, and no generator reproduces it”** ([hallazgo y método](https://voynich.site/en/findings/line-openers/); [modelo y comparación](https://voynich.site/paper-1-mechanism?lang=en)). La página define el abridor como la primera unidad de glifo de la primera palabra de una línea y calcula la información mutua entre abridores de líneas consecutivas dentro de cada página; el nulo baraja los abridores de cada página 10.000 veces. El autor reporta MI = 0,1683 bits frente a 0,0599 en el nulo (z = +23,95), repetición del mismo abridor en 6,88 % de pares frente a 13,54 % esperados, y un resultado similar en la transcripción Takahashi. También reporta que el efecto persiste al retirar las primeras líneas de párrafo y que no aparece con igual fuerza en finales de línea ni en Cato latino repartido en seudolíneas de longitud comparable. Son resultados publicados por el autor en su propio sitio; no los hemos reproducido.

**Cotejo de solapamiento en este repositorio:** los precedentes que pueden confundirse con esta medida —EXP-444, EXP-445 y EXP-447, junto con la familia de análisis cross-line relacionada— miden principalmente el **último abridor de palabra de la línea N → primer abridor de palabra de la línea N+1** (LL→LF), o pares completos de palabras en esa frontera. Por ejemplo, EXP-444/445 examinan bigramas de clases de inicio LL→LF; EXP-447 profundiza en pares de palabras de esa misma frontera. Averyanov mide **primer abridor de palabra de la línea N → primer abridor de palabra de la línea N+1** (LF→LF). La dirección medida y la población de transiciones difieren, así que las tablas LL→LF no reproducen, confirman ni refutan el efecto LF→LF. PR #138, por su parte, predice la posición de un límite de línea; su variable objetivo tampoco es la transición entre abridores, y su documentación marca las métricas históricas como `INVALID_FOR_CLAIM` hasta una regeneración con lectores corregidos. Estas referencias se usan aquí solo para delimitar solapamiento: sus afirmaciones científicas históricas no se rehabilitan.

**Consecuencia y estado:** esta es una pregunta de réplica candidata, no un nuevo EXP ni un resultado nuestro. El registro de numeración sigue sin reconciliarse; la conformidad IVTFF completa y la adjudicación del inventario de glifos también siguen siendo puertas abiertas. No se ha calculado la MI local, no se han reinterpretado los experimentos LL→LF y no se le asigna estado de finding. Si se retoma tras cerrar esas puertas, congelar primero la unidad de glifo y las reglas para líneas/páginas, replicar el nulo permutado dentro de cada página y medir por separado LF→LF, LL→LF y finales de línea; conservar la primera línea de párrafo como sensibilidad; usar una transcripción alternativa como sensibilidad del mismo manuscrito, y añadir un control natural con seudolíneas emparejadas más un control de permutación que preserve los inventarios por página. Reportar MI, tasa de repetición, intervalos por página/folio y sensibilidad a tokens inciertos. El resultado, cualquiera que sea, solo describiría una dependencia local y no demostraría significado, idioma ni descifrado.

## Decisiones incorporadas

1. **No se crea EXP nuevo ni se ejecuta ningún modelo** como consecuencia de esta revisión. Primero siguen vigentes los bloqueos del registro, la política IVTFF, la identidad de los corpus y las reglas de partición física.
2. La matriz de explicaciones debe conservar como rivales explícitos: lengua/código, cifrado de clave fija, cambio de clave o clase de palabra, mecanismo híbrido, y generador/copia dinámica. No asignar probabilidades no calibradas ni declarar una familia descartada por un único ejemplo.
3. Para evaluar un mecanismo, exigir recuperación de contenido conocido en controles y desafíos adversariales; un buen ajuste estadístico o predicción estructural no equivale a descifrado.
4. Una futura réplica externa se seleccionará entre una predicción falsable de Zhang–Sheng, un test pequeño del paquete Averyanov, o una sensibilidad de partición codicológica. Elegir solo tras revisar sus materiales exactos y solapamiento con experimentos existentes; no abrir tres líneas paralelas.
5. No se añadió traducción candidata, referente semántico ni interpretación iconográfica como hecho. No hubo llamada nueva a Gemini ni se enviaron datos del manuscrito a servicios externos.

## Registro de consulta

Búsqueda pública inicial realizada el 2026-10-30; actualización focalizada de fuentes externas realizada el 2026-10-31. Se priorizaron artículos, preprints con identificador persistente y páginas de datos/código de los autores. Esta selección no es un censo exhaustivo. Resultados atribuidos a sus autores, salvo donde se indique reproducción en este repositorio.
