# Nota de literatura externa — estructura de singuliones y orden de los bifolios
Fecha de revisión: 2026-10-21
Estado: LEAD_VERIFIED_AS_PUBLISHED; hipótesis externa no replicada por nuestro proyecto.

## Fuente primaria

Colin Layfield y Lisa Fagin Davis, “Singulion Structure and the Voynich Manuscript”, *Digital Medievalist*, vol. 19 (2026), publicado en línea el 10 de julio de 2026. DOI: https://doi.org/10.4000/16k0a  
Texto completo: https://journals.openedition.org/digitalmedievalist/2331

La fuente primaria propone que el manuscrito pudo producirse originalmente como bifolios individuales apilados (“singuliones”), y no como cuadernos de bifolios anidados en su disposición actual. Combina observaciones codicológicas (por ejemplo, ilustraciones que parecen cruzar el pliegue entre páginas no consecutivas) con Latent Semantic Analysis (LSA) de bloques de texto. Los autores contrastan el comportamiento del Voynich con el *Aberdeen Bestiary* y el *Speculum Humanae Salvationis*.

## Resultados cuantitativos comunicados por los autores

En su tabla de promedios globales, los autores informan:
- Aberdeen Bestiary: similitud media confoliate 0,428; facing 0,398; conjoint 0,207.
- Speculum: confoliate 0,398; facing 0,398; conjoint 0,277.
- Voynich: confoliate 0,383; facing 0,298; conjoint 0,433.

El patrón del Voynich difiere de los dos manuscritos de texto conocido: la similitud entre páginas conjoint supera a la de páginas facing. Los autores interpretan esta diferencia como compatible con un orden actual incorrecto. También ensayan una posible reordenación de bifolios en las secciones balneológica (folios 75–84) y estrellas marginales (folios 103–116).

## Qué no debemos dar por demostrado

- La LSA mide similitud distribucional en este corpus; en un texto no descifrado, la similitud no puede llamarse “semántica” con seguridad.
- Los propios autores describen el análisis como un modelo interno autocontenido: el espacio semántico se entrena con el corpus que luego se compara. No es una prueba de generalización predictiva.
- El artículo usa la transcripción ZL versión 2a, fechada 17-03-2022, mientras nuestros análisis recientes usan ZL3b e IT2a. La versión de transcripción, las reglas de limpieza, stopwords, partición en bloques, dimensiones LSA y estructura codicológica deben igualarse antes de considerar una reproducción.
- El artículo no ofrece una traducción del texto. Una hipótesis sobre el orden físico no establece idioma, significado ni desciframiento.

## Consecuencias para nuestra investigación

1. EXP-605 solo comprueba consistencia de cabeceras y una lista de folios ausentes; no valida el orden de los bifolios.
2. EXP-606 mide distancia léxica alrededor de seis transiciones de foliación en el orden actual. En su versión corregida, solo tres bordes tienen etiquetas Currier no nulas e iguales a ambos lados. Su JSD media (ZL3b 0,6914; IT2a 0,6734) no supera la media de los controles adyacentes de la misma clase (0,7019 y 0,7107). Este resultado pequeño no prueba ni refuta la hipótesis de singuliones: la unidad, la métrica y la pregunta son distintas.
3. Los análisis de posición, adyacencia y predicción por folio deben etiquetarse con la versión del orden físico usado. Si se prueba un reordenamiento, el orden actual debe seguir siendo la condición de referencia inmutable.

## Protocolo propuesto (sin asignar ID EXP nuevo)

No crear un nuevo identificador hasta reconciliar el registro histórico de experimentos y el archivo maestro.

- **Hipótesis falsable:** dentro de las secciones 13 y 20, la secuencia de bifolios sugerida por el procedimiento publicado mejora la similitud entre páginas facing frente al orden actual, y esa mejora supera las mejoras obtenidas con permutaciones aleatorias restringidas.
- **Congelación del método:** documentar corpus y SHA-256; recrear segmentación por página/tipo de texto; registrar reglas de limpieza y stopwords; fijar TF-IDF, dimensión reducida y similitud coseno antes de comparar secuencias.
- **Unidad codicológica:** mantener separadas las relaciones confoliate, conjoint y facing. No tratar páginas de un mismo bifolio como observaciones independientes.
- **Comparación primaria:** orden actual vs secuencia publicada/derivada por autores, por sección, con score global y scores por bifolio; conservar la secuencia original en el registro.
- **Nulo:** permutar el orden de bifolios dentro de cada sección al menos 10.000 veces, sin romper las relaciones físicas confoliate/conjoint; reportar la posición percentil de la secuencia propuesta, tamaño del efecto y estabilidad por transcripción.
- **Controles negativos:** (a) el orden actual; (b) secuencias aleatorias; (c) los manuscritos de texto conocido, si sus transcripciones y colaciones se pueden obtener legalmente y documentar.
- **Replicación:** repetir exactamente el protocolo en ZL3b e IT2a, sin tratarlas como testigos independientes; informar si el resultado depende de una transcripción.
- **Criterio de rechazo:** no apoyar la secuencia propuesta si no supera el nulo restringido, si el efecto desaparece en la segunda transcripción o si la mejora depende de decisiones de limpieza ajustadas después de mirar los resultados.
- **Criterio de éxito limitado:** una mejora reproducible apoyaría la hipótesis estructural de orden, no la traducción ni la identificación de un idioma.

## Fuentes de referencia

- Layfield & Davis, *Digital Medievalist* 19 (2026), DOI: https://doi.org/10.4000/16k0a
- Página del artículo: https://journals.openedition.org/digitalmedievalist/2331
- Christophe Parisel, “A Quantitative Confirmation of the Currier Language Distinction”, arXiv:2604.25979v2 (5 mayo 2026): https://arxiv.org/abs/2604.25979

Esta nota distingue afirmaciones publicadas por terceros de hipótesis aún no replicadas en este repositorio.
