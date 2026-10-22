# Revisión de posibles anclas de lectura — 22 octubre 2026

## Resultado concreto

Se localizaron los tres candidatos en imágenes completas de Yale y se ejecutaron concordancias exactas de nueve términos en dos transcripciones. **Ninguno de los tres candidatos se admite todavía como texto plano conocido.** Esta decisión describe la evidencia obtenida aquí; no demuestra que los textos no sean nombres ni descarta que puedan interpretarse en el futuro.

El avance es una delimitación de dónde buscar y qué no debe confundirse: en f2r, el rótulo lateral y el inicio del párrafo son textos distintos; las propuestas publicadas deben vincularse al lugar exacto que analizan. No se asignaron sonidos ni significados nuevos.

## Imágenes originales y observaciones

Se recuperó el manifiesto IIIF de Yale 2002046 y se seleccionaron canvases por sus etiquetas exactas, sin usar posiciones en la lista. Se descargaron e inspeccionaron las tres imágenes completas. Las observaciones siguientes son inspección visual asistida, no peritaje paleográfico ni identificación botánica independiente.

| Folio | Image ID Yale | Dimensiones | Observación de ubicación |
|---|---:|---:|---|
| f2r | 1006078 | 2691 × 3770 | Texto breve en el margen derecho, junto a una hoja, separado de los dos bloques principales. |
| f41v | 1006155 | 2882 × 3769 | Texto breve por encima del bloque inferior izquierdo. |
| f65r | 1006190 | 2793 × 3707 | Cadena breve a la izquierda del tallo, en una página ocupada principalmente por el dibujo. |

[Recibo de imágenes](decipherment/2026-10-22-anchor-review/image-sources.json): URL de cada imagen y canvas, dimensiones, bytes, SHA-256 de la imagen completa y del manifiesto recibido. El proveedor se registra como Yale University Library. No se reproduce aquí una identificación de especie a partir del parecido visual.

Fuentes primarias:
- [Manifiesto Yale](https://collections.library.yale.edu/manifests/2002046).
- [Imagen f2r](https://collections.library.yale.edu/iiif/2/1006078/full/full/0/default.jpg).
- [Imagen f41v](https://collections.library.yale.edu/iiif/2/1006155/full/full/0/default.jpg).
- [Imagen f65r](https://collections.library.yale.edu/iiif/2/1006190/full/full/0/default.jpg).

El catálogo HTML dio errores de acceso, pero el manifiesto y las imágenes se recuperaron mediante peticiones públicas directas. Los hashes identifican los bytes recibidos, no una certificación de autenticidad realizada por nuestro proyecto. Las imágenes no se almacenan en este repositorio; se conservan sus fuentes y recibos para recuperarlas.

## Contraste con propuestas anteriores

### f2r: no trasladar una lectura entre loci

En su manuscrito de trabajo de 2014, Bax vincula una propuesta de Centaurea al **primer término del párrafo**, no al pequeño texto lateral ytoail. Sus argumentos y equivalencias son hipótesis del autor. En nuestros corpus, los inicios pertinentes son kydainy en f2r.1 y kydain en f2r.8. La asociación propuesta no proporciona una traducción de ytoail.

Fuente: [Bax, versión 1, enero 2014](https://stephenbax.net/wp-content/uploads/2014/01/Voynich-a-provisional-partial-decoding-BAX.pdf), pp. 25–32. Su discusión de f41v (pp. 22–25) propone una relación con el nombre del coriandro y la califica como especulativa. Ese nombre no se incorpora como ancla verificada.

### Descripciones históricas de los folios

Las [notas de Stolfi sobre f2r](https://ic.unicamp.br/~stolfi/voynich/Notes/040/html/f2r.htm) ubican el rótulo en el margen derecho. Recogen una identificación botánica tentativa y también discrepancias de hojas y color; no constituyen una etiqueta de especie validada.

Las [notas de f41v](https://ic.unicamp.br/~stolfi/voynich/Notes/040/html/f41v.htm) mencionan el texto breve y su aspecto más desvaído. Esta observación histórica no permite fecharlo ni decidir que pertenezca a otro autor.

Las [notas de f65r](https://ic.unicamp.br/~stolfi/voynich/Notes/040/html/f65r.htm) describen el único texto como un rótulo de tres palabras junto a la planta. No aportan una identidad botánica establecida. Los espejos que reutilizan estas notas no cuentan como testimonios independientes.

## Concordancias ejecutadas

El [protocolo](decipherment/2026-10-22-anchor-review/PROTOCOL.md) fija los nueve términos antes de obtener sus recuentos. La selección de candidatos y la consulta bibliográfica ya habían ocurrido: es un inventario exploratorio, no una validación ciega.

Se examinaron 5.385 registros ZL3b y 5.215 IT2a, incluidas páginas subdivididas. Se conservan alternativas primarias, ligaduras expandidas y dos tratamientos del espacio incierto. No se buscaron substrings: dam no incluye adam ni dame.

| Término exacto | ZL3b separar coma | ZL3b unir coma | IT2a separar coma | IT2a unir coma |
|---|---:|---:|---:|---:|
| ytoail | 1 | 1 | 0 | 0 |
| keeredal | 1 | 1 | 0 | 0 |
| keerodal | 0 | 0 | 1 | 1 |
| otaim | 2 | 1 | 2 | 2 |
| dam | 88 | 74 | 98 | 98 |
| alam | 11 | 6 | 8 | 8 |
| otaimdam | 0 | 1 | 0 | 0 |
| kydainy | 1 | 1 | 1 | 1 |
| kydain | 1 | 1 | 1 | 1 |

Son conteos condicionados a esas vistas, no cifras universales del manuscrito. En particular, la alternativa e/o de ZL3b no se enumeró para cada registro del corpus: la vista primaria produce keeredal y conserva el texto original keer[e:o]dal para revisión. La ausencia de keerodal en esa vista no resuelve la duda paleográfica.

[Salida completa](decipherment/2026-10-22-anchor-review/concordances.json): cada aparición contiene ID, folio, locus, línea de fuente, posición de token, cuerpo original y contexto próximo.

## Qué permiten comprobar las repeticiones

En la vista que separa comas, otaim aparece en f65r.1 y f111v.3 en ambas fuentes. En ZL3b, unir la coma del rótulo crea otaimdam y deja solo la aparición de otaim en f111v.3. Por eso el tratamiento del espacio es parte de la hipótesis de lectura.

Alam aparece en f111v.21, distinto registro de la otra aparición de otaim. Esa coincidencia de folio no repite la cadena otaim dam alam. No se presenta como confirmación de una frase, un nombre compartido o una receta.

Los candidatos exactos de f2r y f41v no ofrecen otras apariciones en las vistas consultadas con las que validar una lectura por transferencia. Ser únicos no los refuta como nombres; simplemente no proporciona esa validación. Dam, por el contrario, tiene muchos contextos: asignarle un significado a partir de f65r exigiría comprobarlo en el resto, conservando todos los casos desfavorables.

## Decisión de admisión

| Candidato | Localización visual | Lectura de signos independiente | Identidad de objeto verificada | Texto plano admitido |
|---|---|---|---|---|
| f2r.14 / ytoail | Sí, ubicación compatible | Pendiente; no se rehízo la transcripción | No | No |
| f41v.1 / keer[e:o]dal | Sí, ubicación compatible | Alternativa e/o abierta | No; propuesta externa de coriandro | No |
| f65r.1 / otaim,dam.alam | Sí, ubicación compatible | Espacio incierto conservado | No | No |

«No admitido» es un estado de evidencia, no una refutación. Ninguna entrada del paquete anterior se convirtió en diccionario. Los originales y sus campos de lectura vacíos se conservan.

## Próxima condición necesaria para intentar una clave

Antes de ajustar equivalencias fonéticas, necesitamos un nombre y una correspondencia con imagen/texto que no dependan de que la clave deseada encaje. Una propuesta externa puede orientar la búsqueda, pero no sirve a la vez como dato de entrenamiento y prueba de que la lectura funciona.

La vía f41v sigue siendo una hipótesis histórica concreta que podría someterse a comparación con herbarios identificados y nombres documentados; con las fuentes consultadas en este bloque no queda resuelta. No se inventará una clave para cubrir ese vacío. Las concordancias ya preparadas permitirán revisar predicciones fuera de la imagen de origen cuando exista una propuesta explícita.

## Autoauditoría

**Conciencia del objetivo:** los nueve términos se eligieron por los candidatos y la bibliografía ya vistos, no como muestra aleatoria ni test ciego. La lista se fijó antes de contar y se informan ceros y ambas políticas de espacio.

**Implementación que destruye características:** el tokenizador conserva los cuerpos originales, pero las vistas son proyecciones y usan alternativas primarias. Sus ausencias son condicionales; no refutan posibles lecturas bajo alternativas no desplegadas. La coma de f65r cambia la unidad de análisis y se muestra explícitamente.

**Extrapolación:** la revisión cubre tres lugares y fuentes concretas; no establece que ninguna planta del manuscrito sea identificable ni que todos sus rótulos sean nombres. No demuestra o excluye una lengua o familia de cifrados.

**Alcance negativo:** no se ha obtenido un ancla admisible en este bloque. Eso no refuta las identificaciones ni las lecturas propuestas por todos los autores; indica que no podemos utilizarlas como texto conocido validado aquí.

**Controles:** no se compara contra una distribución aleatoria ni se calcula significación. Las fixtures comprueban coincidencia exacta frente a substrings, ocurrencias frente a líneas, alternativa primaria, coma, páginas subdivididas, markup inválido y resolución de canvases por etiqueta. Los seis tests pasan y el selector reproduce los tres canvases del manifiesto recibido. No hay p-valores que interpretar.

La revisión humana independiente de transcripción e identificación botánica sigue pendiente. No se modificaron committed_claims.md, findings.md o failed_approaches.md ni se asignó un EXP nuevo.

## Reproducción

- python tests/test_decipherment_anchor_evidence.py
- python scripts/audit_decipherment_anchor_concordances.py
- python scripts/fetch_decipherment_anchor_images.py --cache-dir /tmp/voynich-anchor-images

El último comando requiere red y recupera copias para inspección; comparar los hashes con el recibo para comprobar si los bytes coinciden. Los tests y concordancias se reproducen sin red en CI. El script de descarga no se ejecuta en CI.

