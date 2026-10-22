# Fuentes externas primarias y uso concreto

Consultadas el 22-10-2026. Esta revisión dirigida complementa la revisión profesional previa; no cuenta fuentes ya conocidas como descubrimientos nuevos.

## Reddy y Knight (2011)

*What We Know About The Voynich Manuscript*, ACL LaTeCH, pp. 78–86. [PDF primario](https://aclanthology.org/W11-1511.pdf), §5. Distingue predictibilidad de identidades de tokens y de caracteres de borde. Usamos esa distinción para formular controles propios. Su transcripción Currier y su evaluación no son nuestro corpus EVA ni EXP-607; sus cifras no se trasplantan a nuestros resultados.

## Emma May Smith y Marco Ponzi (2019; preprint de julio de 2018)

*Glyph combinations across word breaks in the Voynich manuscript*, DOI [10.1080/01611194.2019.1596998](https://doi.org/10.1080/01611194.2019.1596998). [Preprint alojado por la autora](https://agnosticvoynich.wordpress.com/wp-content/uploads/2019/06/glyph-combinations-across-word-breaks-in-the-voynich-manuscript-preprint.pdf). Analiza dependencia entre signos finales e iniciales y explicita decisiones de segmentación. Inspira conservar bordes en vez de destruirlos en todos los nulos. Nuestro primer/último carácter EVA es un proxy más simple que su inventario de signos; no afirmamos replicar su tabla.

## Rozanova y Temerev (2026)

*A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space*, [arXiv:2608.17096v1](https://arxiv.org/html/2608.17096v1), preprint, 17-08-2026. Propone contrastar unidades observadas con interpretaciones lingüísticas; distingue información de identidad y borde, y declara controles y código. Incorporamos la pregunta metodológica, sin convertir sus conclusiones en consenso ni traducción. La revisión de código siguiente limita qué parte hemos reproducido.

## Archivo computacional del preprint

[Repositorio fijado](https://github.com/lrozanova/voynich-units/tree/66f8adaadc120f93e8a4c906685ba66a9d3ab847). Se inspeccionaron README, DATA_SOURCES y el driver de sintaxis antes de ejecutarlo; se conservaron hashes y salida. Se reprodujo exactamente un driver antiguo, con 25 barajados. En el árbol fijado de 298 entradas no aparecen los nombres `reproduce_headlines.py`, `reproduce_edge_order.py` o `reproduce_scale_transition.py` citados por el preprint. Hay scripts relacionados anteriores; no concluimos que sean equivalentes ni que los anexos arXiv carezcan de esos archivos. El README reconoce reconstrucción de algunos cálculos y documentación incompleta de una calibración. Por eso no afirmamos reproducción íntegra del artículo.

La auditoría propia encontró y verificó un defecto de retirada de pies en el cargador Gutenberg. Los prefijos realmente analizados permanecen iguales al corregirlo. Se registra el defecto sin atribuirle un cambio que no produce en esta comparación.

## Montemurro y Zanette (2013)

*Keywords and Co-Occurrence Patterns…*, [PLOS ONE, DOI 10.1371/journal.pone.0066344](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0066344). Investiga distribución y coocurrencia a escalas largas y una ordenación por secciones. Sus redes estadísticas no proporcionan por sí mismas equivalencias de texto plano ni validan nuestra pareja local. Se mantiene separada esa escala de la adyacencia dentro de registro.

## Límite de acceso

Se localizó *The challenge of analyzing a dynamic text* de Torsten Timm, DOI 10.1080/01611194.2026.2693462, pero el acceso directo al editor devolvió 403. No se declara lectura integral ni se incorporan sus conclusiones como verificadas. No se usaron noticias o foros como evidencia de un desciframiento.
