# Revisión visual de relaciones y regiones — seis páginas
25-10-2026. Inspección del coordinador expuesto a EVA e hipótesis previas; no anotación independiente.
[Fuentes recuperadas con dimensiones y SHA256](region-source-receipt.json). f2r/f41v/f65r coinciden por hash con las fuentes ya archivadas.
Se inspeccionaron las seis imágenes completas en el visor, sin modificar píxeles. No se aprobó ningún recorte ni se emitió una identificación botánica.

| Página / locus | Observación visual | Relación provisional | Decisión de región |
|---|---|---|---|
| f2r.14 | Dibujo vegetal ramificado; escritura de párrafos alrededor y breve escritura a derecha de una hoja | Proximidad al dibujo principal; no prueba nombre ni qué parte refiere | Objeto completo como candidato; texto entre flores/ramas impide una máscara rectangular global sin pérdida. Requiere segmentación |
| f41v.1 | Dibujo vegetal principal con raíces y hojas; breve texto sobre el comienzo del bloque inferior izquierdo | Cercano a un objeto principal, pero también al párrafo | Preservar dibujo entero; separar rótulo y párrafos sin cortar raíces. No se aprueba máscara |
| f65r.1 | Dibujo vegetal principal; texto breve separado en parte inferior izquierda | Un conjunto vegetal visible cercano; no asignación léxica ni división semántica de palabras | Revisar plan geométrico existente y mantener objeto completo. No duplicar hojas/raíces como referentes |
| f81v.28 | Texto corto a izquierda de un conjunto verde con figuras, cerca de borde/inlet; conducto conectado | Referente no único: borde, conjunto, conducto o figuras. Código Lt no resuelve la imagen | Región de contexto debe incluir borde izquierdo, conexión y conjunto; no recortar una figura arbitraria |
| f77r, 10 localizadores candidatos | Figuras y dispositivos conectados arriba y al lado de bloques de texto | Múltiples referentes próximos; sin alineación individual de IDs | Necesita adjudicación por localizador; página completa solo sirve al coordinador |
| f77v, 8 localizadores candidatos | Figuras, recipientes y conductos conectados; texto intercalado | Relaciones ambiguas entre figura y dispositivo | Mantener contexto de conexiones; no copiar categoría de página a cada fila |

## Alcance de lo verificado
La relación es espacial provisional, no interpretación del texto. En f2r/f41v/f65r se reconoció ubicación aproximada del texto compatible con los registros revisados; no se validó glifo a glifo, alternativa de lectura ni taxón.
En f77r/f77v se inspeccionó disposición general; no se completó alineación de los 18 localizadores. Se mantienen bloqueados individualmente.
Las imágenes completas contienen márgenes y posibles páginas vecinas: el paquete futuro debe limitarse al objeto y retirar ese contenido también; una etiqueta de canvas de una sola página no garantiza un JPEG sin contenido vecino.

## Registro de objetos compartidos
Para preparar adjudicación, el dibujo vegetal completo de cada una de f2r/f41v/f65r debe tratarse como un grupo visual por página, sin contar partes como muestras independientes por defecto.
No se establece todavía identificador definitivo de objeto en la cola: falta revisión independiente.
Para f77r/f77v/f81v no se decide aún si dispositivo y figura forman una unidad o varias. Conservar conexiones en contexto y resolver antes de modelar.
Ningún subtipo IVTFF se añade como categoría visual de entrenamiento.

## Resultado y límite operativo
Se ha completado inspección general de seis páginas y se ha localizado el problema de segmentación y relación en cada caso. No se completó validación de máscaras ni adjudicación independiente.
No es responsable marcar estos ejemplos READY: aprobarlos exigiría comprobar cada recorte y máscara a resolución original y revisión independiente, además de dos anotadores disponibles para la etapa siguiente. Esta sesión no tiene participantes independientes identificados.
La preparación informática no resuelve ese requisito. No generar más modelos o tandas mientras falten datos aptos.

## Autoauditoría
Selección: páginas del piloto ya fijado, con fuentes primarias exactas; no seleccionadas por taxón esperado. Conocimiento previo de candidatos declarado.
Destrucción de rasgos: no se modificaron imágenes; se documenta que máscaras amplias pueden destruir rasgos o conexiones.
Extrapolación: observaciones limitadas a vistas completas, sin certificación paleográfica ni independencia.
Negativos: ambigüedad no implica ausencia de significado. Ninguna traducción ni prueba estadística.
Controles: dimensiones decodificadas coinciden en seis fuentes; hashes de los tres originales previos coinciden. No suite global ni CI nueva certificada.
