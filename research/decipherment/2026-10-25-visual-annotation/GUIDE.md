# Guía de anotación visual independiente — 25-10-2026

Estado: PROPOSED para el procedimiento de anotación; cola generada de manera reproducible. No se han producido anotaciones ni identificaciones nuevas.

## Paquetes y alcance

`annotator-queue.json.gz` contiene 1.172 tareas con IDs opacos, sin EVA ni folios. `coordinator-map.json.gz` relaciona cada tarea con los registros de transcripción y la procedencia visual archivada. Se agrupa por identificador de locus, no por objeto demostrado: una fila puede contener varias etiquetas y un objeto puede estar relacionado con varias filas. Las dos ediciones no son dos observaciones visuales independientes.

El coordinador debe adjudicar región y relación etiqueta/objeto antes de una evaluación. La columna `shared_illustration_group` debe agrupar objetos compartidos para evitar duplicación y fuga entre particiones. Si la relación no es determinable, registrar la incertidumbre y mantener la tarea bloqueada. No identificar la planta para decidir qué región seleccionar.

Las 1.172 tareas están bloqueadas; ninguna tiene aún recorte enmascarado ni revisor de máscara. Tres folios tienen enlaces archivados a imágenes completas, que no se entregan automáticamente al anotador. La cola sin texto es preparación para un cegamiento, no prueba de que haya ocurrido. Los IDs son hashes deterministas de localizadores, no un secreto criptográfico; no se protege frente a quien busque el mapa público o el corpus.

## Preparación por el coordinador

1. Recuperar la imagen desde su fuente primaria y comprobar su hash. Registrar licencia, procedencia, dimensiones y fecha. Los hashes archivados no sustituyen esta comprobación para una imagen nueva.
2. Delimitar región con coordenadas x/y/ancho/alto en píxeles de la imagen fuente y documentar su relación con el locus. Conservar original, máscara y recorte en archivos separados; nunca alterar fuentes.
3. Ocultar todos los glifos, transcripciones, leyendas, nombres propuestos, folio y metadatos de archivo que revelen hipótesis previas. Conservar la ilustración relevante. Registrar si el enmascarado oculta también rasgos visuales necesarios.
4. Un revisor comprueba que no queda texto legible y que el recorte permite anotación. Si los glifos se superponen al dibujo, conservar el bloqueo o marcarlo no evaluable; no reconstruir visualmente zonas ocultas.
5. Congelar hash de la imagen enmascarada y versión de guía. Solo entonces establecer status READY, annotation_ready true, masked_image_path, masked_image_sha256 y mask_reviewed_by. Este cambio necesita evidencia de revisión; no basta rellenar campos.
6. Entregar al anotador únicamente el paquete enmascarado y la guía. No entregar el mapa del coordinador ni el inventario EVA. El coordinador debe conservar una copia separada del paquete efectivamente entregado.

## Primera ronda independiente

Dos anotadores distintos trabajan por separado sin ver EVA, hipótesis anteriores ni respuestas del otro. Registrar formación relevante y exposición previa; alguien que ya conoce esos candidatos no se declara ciego para ellos. Esta sesión ha visto EVA y no se presenta como anotador independiente de los loci examinados.

La primera decisión es una categoría amplia: plant_or_plant_part, human_or_body, animal, astronomical_or_geometric, vessel_or_object, mixed, no_identifiable_referent o uncertain. Describir rasgos observables en notas. `uncertain` y `no_identifiable_referent` se conservan como respuestas, sin forzar nombre.

Registrar confianza low/medium/high con justificación descriptiva. No equivale a probabilidad calibrada. Un nombre específico es opcional y necesita fuente primaria o edición crítica independiente, cita precisa y argumento visual. Una URL por sí sola no acredita identidad, ni se admiten catálogos derivados de propuestas de traducción del Voynich como verdad de referencia.

Cada fila sigue annotation-template.json: task_id, annotator_id, round, category, confidence, image_sha256, timestamp ISO 8601, saw_eva, saw_prior_hypotheses, external_referent, external_source y notes. No copiar el ejemplo como observación real. El validador comprueba estructura y algunas puertas; no comprueba honestidad, independencia efectiva ni calidad botánica de una fuente.

## Desacuerdos y evaluación

Conservar las dos respuestas iniciales inmutables. Registrar discrepancias y adjudicación posterior por separado, sin sustituirlas por un consenso retrospectivo. Medir cobertura de respuestas y matriz de confusión, acuerdo bruto y una medida corregida por azar, con incertidumbre agrupada por hoja física. Informar categorías raras y efecto de prevalencia; no elegir la medida que dé mejor acuerdo después de verlo.

No se fijan aquí umbrales arbitrarios de fiabilidad ni potencia: deben congelarse en el protocolo de objetivo antes de entrenar. La categoría visual y la recuperación de nombres son objetivos distintos. Una categoría acordada no valida un nombre y un nombre propuesto no valida una correspondencia fonética. No usar regiones del mismo objeto, caras de la misma hoja ni ediciones alternativas en particiones diferentes.

## Reproducción y verificación

```sh
python scripts/prepare_visual_annotation_queue.py --out-dir research/decipherment/2026-10-25-visual-annotation
python -m unittest discover -s tests -p test_visual_annotation_queue.py -v
```

El script utiliza el archivo inventory.json.gz integrado por PR #47. Los archivos gzip se generan sin fecha variable; SHA256.json fija ambos paquetes. Las pruebas incluyen emparejamiento de ediciones sin filtrar EVA al paquete del anotador y rechazo de imágenes no preparadas, hashes discordantes, exposición declarada y nombres sin fuente.

Se han recuperado e inspeccionado las tres imágenes archivadas; fresh-image-receipt.json documenta identidad por SHA256 y region-proposals.json conserva coordenadas provisionales para f65r. No se han generado ni aprobado máscaras, anotado referentes, medido acuerdo, entrenado modelos ni evaluado un holdout. El siguiente paso material es revisar las regiones y preparar máscaras sin destruir detalles, con registro de exposición de quienes participen.
