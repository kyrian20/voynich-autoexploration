# Verificación del paquete visual — 25-10-2026

Alcance: preparación reproducible, no anotación semántica. Inventario de entrada integrado en PR #47, cabeza 364ec298cd928f0ad1d6f6e51a03698adbb455ed; CI de esa cabeza aprobada: https://github.com/kyrian20/voynich-autoexploration/actions/runs/40175871776. Fusión realizada: 6c0b23566616cd00bc92d71e60f258446152f8d8. La CI citada corresponde a la cabeza anterior a la fusión, no certifica por sí sola el merge.

Verificación local: Python 3.12.14, checkout base 412fd7cc2f830f1e9f4a298154d163af95cbc79a con los archivos de inventario de PR #47 y este paquete visual. Suite de 254 tests OK, skipped=1 (archivo crudo de batería histórica ausente). Tres tests nuevos: separación del paquete sin EVA, emparejamiento de ediciones y puertas de recepción de anotaciones. Auditoría de operaciones exit 0; identidad de 14 corpus exit 0 y cuarentena de Cicero conservada. Dos reproducciones de cada paquete gzip coinciden byte a byte. Estas comprobaciones locales no certifican un master concurrente posterior ni sustituyen la CI de la nueva propuesta.

Salida: 1.172 tareas/2.196 registros de fuente; cero tareas listas, cero anotaciones y cero referentes nuevos. Cada localizador requiere adjudicar relación con objeto, región y grupo de ilustración compartida. El JSON de plantilla es un ejemplo vacío y deliberadamente no pasa como anotación real.

Revisión de integridad: no se ha filtrado por nombre deseado; la cola conserva todos los localizadores del inventario. Agrupar por locus no prueba equivalencia de objeto entre transcripciones. No hay contraste de hipótesis, simulación ni conclusión negativa sobre significado. Los marcadores especiales y la identificación visual siguen pendientes. El validador comprueba campos y exposición declarada, no independencia efectiva ni revisión de máscara real.

En la preparación inicial no se descargaron imágenes; la continuación documentada abajo recupera e inspecciona las tres fuentes. No se ha ejecutado la CI completa local. Los siguientes pasos son materiales: regiones de imagen, máscara revisada y anotadores con exposición documentada; no entrenar un modelo sobre referentes nulos.

## Continuación: inspección de fuentes y viabilidad de máscara

Se ejecutó `python scripts/fetch_decipherment_anchor_images.py --cache-dir /tmp/voynich-yale-images` y se compararon bytes de las tres imágenes con image-sources.json archivado. Los tres SHA256 y el hash del manifiesto coinciden. Se observaron las tres páginas completas, sin atribuir taxón o referente ni resolver la lectura EVA. La inspección fue efectuada por el mismo asistente expuesto a las hipótesis previas; no cuenta como anotación ciega independiente.

Observación para preparar máscaras: en f2r y f41v texto y estructuras dibujadas se intercalan; máscaras rectangulares amplias pueden ocultar rasgos. En f65r se proponen coordenadas gruesas para etiqueta inferior izquierda y foliación superior derecha, junto con un recorte. Son coordenadas iniciales estimadas sobre la vista mostrada, no una delimitación paleográfica calibrada ni una máscara aprobada. Deben revisarse a resolución original, incluida la zona superior del pliegue y marcas residuales. No se ha guardado ningún recorte o imagen modificada.

Se verificaron por código los hashes completos de las tres descargas y que las coordenadas propuestas tienen dimensiones positivas y quedan dentro de la fuente. Esas comprobaciones no prueban ausencia de texto residual ni conservación de todos los detalles. La cola no cambia: cero tareas listas. No se añaden tests nuevos porque no cambió el código; los 254 tests previos no validan la propuesta geométrica.
