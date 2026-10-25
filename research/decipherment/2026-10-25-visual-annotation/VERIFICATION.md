# Verificación del paquete visual — 25-10-2026

Alcance: preparación reproducible, no anotación semántica. Inventario de entrada integrado en PR #47, cabeza 364ec298cd928f0ad1d6f6e51a03698adbb455ed; CI de esa cabeza aprobada: https://github.com/kyrian20/voynich-autoexploration/actions/runs/40175871776. Fusión realizada: 6c0b23566616cd00bc92d71e60f258446152f8d8. La CI citada corresponde a la cabeza anterior a la fusión, no certifica por sí sola el merge.

Verificación local: Python 3.12.14, checkout base 412fd7cc2f830f1e9f4a298154d163af95cbc79a con los archivos de inventario de PR #47 y este paquete visual. Suite de 254 tests OK, skipped=1 (archivo crudo de batería histórica ausente). Tres tests nuevos: separación del paquete sin EVA, emparejamiento de ediciones y puertas de recepción de anotaciones. Auditoría de operaciones exit 0; identidad de 14 corpus exit 0 y cuarentena de Cicero conservada. Dos reproducciones de cada paquete gzip coinciden byte a byte. Estas comprobaciones locales no certifican un master concurrente posterior ni sustituyen la CI de la nueva propuesta.

Salida: 1.172 tareas/2.196 registros de fuente; cero tareas listas, cero anotaciones y cero referentes nuevos. Cada localizador requiere adjudicar relación con objeto, región y grupo de ilustración compartida. El JSON de plantilla es un ejemplo vacío y deliberadamente no pasa como anotación real.

Revisión de integridad: no se ha filtrado por nombre deseado; la cola conserva todos los localizadores del inventario. Agrupar por locus no prueba equivalencia de objeto entre transcripciones. No hay contraste de hipótesis, simulación ni conclusión negativa sobre significado. Los marcadores especiales y la identificación visual siguen pendientes. El validador comprueba campos y exposición declarada, no independencia efectiva ni revisión de máscara real.

No se han descargado o procesado imágenes ni ejecutado la CI completa local. Los siguientes pasos son materiales: regiones de imagen, máscara revisada y anotadores con exposición documentada; no entrenar un modelo sobre referentes nulos.
