# f41v: comparación histórica y viabilidad de una lectura candidata

Fecha: 22 octubre 2026. Estado: revisión exploratoria, sin recuperación de texto plano.

## Decisión del bloque

No utilizar f41v como nombre conocido para calibrar una clave. Se mantiene como propuesta externa pendiente de identificación y de reglas explícitas.

Se completaron dos tareas concretas: recuperar e inspeccionar un comparador histórico nombrado de Egerton MS 747 y ejecutar un subconjunto formalizado de correspondencias aproximadas sobre nueve candidatos. El ensayo no produjo una lectura completa y única. Esa conclusión es condicional al subconjunto y sus decisiones informáticas; no es una refutación de todos los sistemas de escritura ni de la propuesta completa del autor.

## Comparador histórico recuperado

La [ficha de British Library](https://searcharchives.bl.uk/catalog/032-001983805) enlaza el manifiesto de Egerton MS 747. Se seleccionó por etiqueta exacta **f.27v**, evitando confundirla con f.127v. Se descargó e inspeccionó la imagen completa, de 3992 × 5835 píxeles.

La página muestra dos plantas, con sus entradas textuales: la de la izquierda lleva un comienzo legible como Coliandru..., y la de la derecha, Cerfolliu.... Estas lecturas breves sirven como localizadores de las entradas; no son una transcripción diplomática completa ni una nueva identificación taxonómica de ambos dibujos.

La [imagen original](https://bl.digirati.io/images/ark:/81055/vdc_100058663074.0x00003e/full/full/0/default.jpg) es un comparador de la tradición de herbarios, no una traducción del Voynich ni prueba de que ambos manuscritos compartan autor, lugar o modelo.

[Recibo](decipherment/2026-10-22-f41v-feasibility/comparator-sources.json): canvas, dimensiones, URL, SHA-256 del manifiesto y de los bytes de imagen recibidos. Las dos plantas de la página se mantienen como referencia; no se eligió un recorte favorable de una sola.

## Comparación morfológica: qué indica y qué no

Fuentes botánicas modernas:
- [Kew, Coriandrum sativum, descripción de Flora Zambesiaca](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:840760-1/general-information).
- [Royal Botanic Garden Edinburgh, Flora of Bhutan, Mark F. Watson](https://websites.rbge.org.uk/URC/bhutanumbels/Coriandrum.htm).

Estas floras describen hojas basales relativamente anchas y hojas superiores mucho más finamente divididas, inflorescencias en umbelas compuestas y flores blancas o rosadas. Kew también describe una raíz principal delgada.

Las siguientes observaciones de los dibujos son nuestras, no diagnósticos de un botánico y no se realizaron a ciegas:

| Rasgo | Egerton, planta de la entrada izquierda | Voynich f41v | Alcance |
|---|---|---|---|
| Raíz representada | Trazos finos bajo un tallo largo | Dos grandes engrosamientos oscuros | Diferencia visible; la estilización impide traducirla directamente en especie. |
| Hojas | Varias hojas anchas y lobuladas incluso en zonas altas | Hojas grandes con lóbulos marcados en varios niveles | La transición de hojas propia de la planta viva no queda claramente documentada en ninguno de los dos dibujos. |
| Estructura floral | Grupos ramificados de pequeñas formas circulares | Numerosas formas azules agrupadas en la parte alta | La semejanza general no permite identificar una especie. |
| Color de las flores | Verde, como buena parte de la planta | Azul | La diferencia de pigmento no se usa como criterio decisivo. |

**Corrección metodológica importante:** confrontar solo el Voynich con una planta viva habría dado demasiado peso a rasgos que el propio comparador histórico simplifica. Por ello, esta comparación no certifica ni refuta Coriandrum en f41v. Tampoco permite distinguirlo con seguridad de otras plantas ilustradas con hojas e inflorescencias parecidas.

No se calculan porcentajes de parecido ni confianza botánica: no hay muestra de referencia etiquetada, evaluación ciega ni criterio de identificación validado para hacerlo.

## Ensayo de correspondencias aproximadas

Fuente: [Bax, manuscrito de trabajo de 2014](https://stephenbax.net/wp-content/uploads/2014/01/Voynich-a-provisional-partial-decoding-BAX.pdf), apéndice 1, pp. 56–57. Se consultó la extracción web de las tablas. La descarga directa local devolvió 403: no se completó la inspección local renderizada del PDF y no se afirma haberla realizado.

El [protocolo](decipherment/2026-10-22-f41v-feasibility/PROTOCOL.md) declara un subconjunto de trece claves y conserva sonidos alternativos y condiciones no resueltas. La segmentación por coincidencia más larga es una decisión informática nuestra. No implementa la duración de vocales repetidas ni todos los elementos de la propuesta del autor.

No se agregaron valores para signos ausentes con el fin de encajar nombres. No se consultó un diccionario para seleccionar sonidos.

| Forma evaluada | Caracteres sin valor en este subconjunto | Otras dificultades conservadas |
|---|---|---|
| ytoail | i, l, t | Alternativas de sonido |
| keeredal | l | Alternativas, vocal tras r no especificada, duración de ee pendiente |
| keerodal | l | Alternativas, vocal tras r no especificada, duración de ee pendiente |
| otaim | i, t | Alternativas y condición de m no resuelta |
| dam | Ninguno | Alternativas y condición de m no resuelta |
| alam | l | Alternativas y condición de m no resuelta |
| otaimdam | i, t | Alternativas y condiciones de m no resueltas |
| kydainy | Ninguno | Alternativas de sonido |
| kydain | Ninguno | Alternativas de sonido |

La diferencia e/o de f41v produce propuestas distintas y se conserva. **Cubrir todos los signos tampoco valida una palabra**: dam y los dos inicios de párrafo siguen teniendo alternativas y carecen de significado demostrado.

La [salida completa](decipherment/2026-10-22-f41v-feasibility/rule-results.json) contiene reglas, posiciones de cada unidad, sonidos propuestos, huecos y límites. Todos los campos de texto plano permanecen vacíos. No se generan cadenas presentadas como traducciones.

## Qué cambia en la investigación

- f41v no sirve todavía como dato conocido para aprender ni para validar una clave.
- Una futura propuesta debe especificar el valor del signo pendiente, sus alternativas de transcripción y las reglas contextuales sin ajustarlas palabra por palabra.
- La comparación botánica debe incluir dibujos históricos nombrados y rivales de aspecto parecido; la comparación exclusiva con fotografías modernas es insuficiente.
- Se mantiene la búsqueda de correspondencias documentales, pero no se repetirá otra tanda de ajustes a este mismo nombre sin evidencia externa nueva.
- Una próxima evaluación semántica necesitará referentes establecidos por una vía independiente de la clave. La cobertura fonética de este ensayo no cumple ese requisito.

No se promueven nuevos significados al estado de hallazgos y no se reemplazan resultados históricos. Este bloque no asigna un nuevo EXP ID.

## Autoauditoría

**Conciencia del objetivo:** candidatos y propuesta externa ya eran conocidos. La lista de nueve formas y el subconjunto de reglas se fijaron antes de ejecutar este ensayo. La comparación visual no es ciega; no se presenta como validación independiente.

**Implementación que destruye características:** el subconjunto omite elementos del autor, incluida la duración vocálica, y adopta una segmentación concreta. Por tanto, su incapacidad para producir una lectura única no refuta la propuesta completa. Los signos desconocidos se preservan, sin borrarlos para mejorar el resultado.

**Extrapolación:** los resultados solo describen este subconjunto y estas nueve formas. No excluyen correspondencias fonéticas adicionales ni otros mecanismos de escritura.

**Alcance negativo:** f41v no se admite como texto conocido con la evidencia actual. No se concluye que el dibujo no sea coriandro ni que ningún rótulo del manuscrito pueda interpretarse.

**Controles:** el comparador histórico limita el uso de rasgos de la planta viva como criterio de rechazo. No hay un test estadístico ni distribución nula; no se inventan valores esperados o p-valores. Cinco pruebas verifican conservación de unidades, grupos sin solapamientos, alternativas e/o, ausencia de promoción semántica y selección exacta del folio histórico.

Esta autoauditoría no sustituye una revisión botánica y paleográfica independiente.

## Reproducción

- python tests/test_partial_sound_rule_feasibility.py
- python scripts/audit_partial_sound_rule_feasibility.py
- python scripts/fetch_egerton_comparator.py --cache-dir /tmp/egerton-comparator

La descarga requiere red. La selección del canvas se comprobó contra el manifiesto recibido. CI ejecuta las pruebas y reproduce el JSON de reglas sin red; no descarga imágenes ni el PDF.

