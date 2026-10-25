# Recuperación documental del comparador Met 19.68.1

26-10-2026 (Madrid). Nota bibliográfica exploratoria; no experimento semántico, no EXP nuevo. Base consultada: b0d84dab43ea57e305b5909de0d5b96d618aa25e.

## Cambio de conocimiento

REPORT.md y sources.json conservan correctamente el estado de la consulta anterior: el comparador no se había recuperado. En esta continuación sí se recuperó la ficha oficial vigente:

https://www.metmuseum.org/art/collection/search/447071

Se comprobó la coincidencia explícita entre Object Number 19.68.1 y el registro 447071. La ficha identifica un folio del Mu'nis al-ahrar de Jajarmi, fechado 741 AH/1340–41 CE y realizado en Isfahán. Su descripción principal presenta la luna entrando en las casas zodiacales y menciona Géminis, Cáncer y Leo. Se parafrasea el catálogo, no se traduce ninguna inscripción de la imagen.

La búsqueda de 19.68.1 también devuelve copias en Wikimedia Commons que remiten a este registro. Sirvieron como pista de localización; la adjudicación del número de inventario procede de la ficha oficial, no de esas copias.

## Resultado y límite

Se resuelve el acceso al registro bibliográfico. No se resuelve todavía qué imagen/detalle corresponde a la figura de Tauro de Bax, ni la lectura de su inscripción. La ficha ofrece varias imágenes: no debe confundirse la descripción principal con una enumeración exhaustiva de todas sus caras o detalles. Que el texto principal mencione otros signos tampoco refuta la figura de Bax.

Se solicitaron enlaces oficiales de imágenes del registro. El servicio devolvió bloques de imagen para las rutas 906007, 856389, 884116 y 856391, y error para 906017 y 856390. No se conserva una copia local ni un hash de sus bytes y no se afirma una adjudicación visual o paleográfica de esos bloques. Direcciones reproducibles:

- https://collectionapi.metmuseum.org/api/collection/v1/iiif/447071/906007/main-image
- https://collectionapi.metmuseum.org/api/collection/v1/iiif/447071/906017/main-image
- https://collectionapi.metmuseum.org/api/collection/v1/iiif/447071/856389/main-image
- https://collectionapi.metmuseum.org/api/collection/v1/iiif/447071/884116/main-image
- https://collectionapi.metmuseum.org/api/collection/v1/iiif/447071/856390/main-image
- https://collectionapi.metmuseum.org/api/collection/v1/iiif/447071/856391/main-image

Los identificadores son rutas consultadas, no equivalencias con figuras concretas. No inferir ausencia de una imagen por un fallo del servicio.

## Decisión y siguiente contraste

La admisión de f68r3 como ancla permanece BLOCKED. Recuperar un paralelo histórico no identifica automáticamente el dibujo Voynich ni su idioma. Para avanzar: cotejar la figura 6 de Bax con la imagen exacta del Met; fijar cara/detalle y procedencia; obtener una lectura atribuible de la inscripción; después evaluar qué rasgos distinguen Tauro, Pléyades y alternativas sin utilizar una clave elegida para producir esos nombres. La semejanza de motivos por sí sola no establece dependencia documental.

## Autoauditoría según skills/audit_experiment.md

- Conciencia del objetivo: búsqueda dirigida a una referencia ya conocida de Bax; resultado exploratorio, sin selección ciega ni puntuación de semejanza.
- Destrucción de características: no se normaliza ni transforma texto o imagen. La extracción del catálogo no sustituye inspección de las imágenes.
- Extrapolación: solo se confirma identidad y acceso al registro; no relación genealógica entre manuscritos, lengua, sonido o significado Voynich.
- Alcance negativo: los errores de imágenes son fallos de recuperación, no evidencia contra la propuesta astronómica.
- Controles: contraste exacto del número 19.68.1 en la fuente oficial. No se diseñó ni ejecutó un nulo estadístico o una evaluación semántica.

## Verificación y omisiones

Lectura de la ficha oficial y cotejo explícito de identificadores ejecutados en esta sesión. No se ejecutan scripts, pruebas unitarias o CI por esta consulta documental; no se declara validación técnica del repositorio. No se modifican corpus, resultados originales, manifiestos, committed_claims ni estados científicos. No hubo nueva llamada a Gemini ni revisión externa independiente. Se conserva la consulta previa como historial y se añade esta nota, sin sobrescribirla.
