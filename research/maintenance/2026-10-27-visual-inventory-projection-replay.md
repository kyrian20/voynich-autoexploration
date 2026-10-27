# Integridad de las ocho proyecciones del inventario de etiquetas — 27-10-2026

**Estado inicial: reparación propuesta, pendiente de CI del commit exacto.**
Tipo: mantenimiento de procedencia; no EXP nuevo, no inferencia semántica.

## Defecto delimitado

El censo L/R y la vinculación de cada registro a su línea física de la transcripción ya estaban cubiertos por `audit_visual_inventory_completeness.py` y `audit_visual_inventory_source_rows.py`. No se duplican esas correcciones.

Quedaba una frontera distinta: las ocho vistas derivadas `split/join × primary/exclude_word × expand/opaque` y los diagnósticos léxicos archivados no eran reconstruidos ni comparados por esos dos auditores. Cambiar `views["split/primary/expand"]["tokens"]` sin tocar la línea fuente ni su hash podía superar sus comprobaciones y dejar una representación textual adulterada disponible para consumidores posteriores. Esto es una **posibilidad reproducible mediante un fixture sintético**, no un hallazgo de adulteración del archivo original.

## Reparación y criterios de aceptación

`scripts/audit_visual_inventory_projections.py` primero ejecuta el censo completo y la vinculación a líneas fuente; después vuelve a proyectar cada `raw_body` con las ocho políticas congeladas usando el lector existente, y compara **tokens, errores, conjunto exacto de políticas y diagnósticos** con el inventario archivado. Rechaza también que un registro sin anotación independiente se marque como apto para evaluación semántica.

Criterio operativo: (a) siete regresiones sintéticas pasan, incluidas vistas alteradas, diagnósticos, error de proyección, falta de vista, fuente falsificada, omisión y promoción semántica; (b) la reproducción sobre el inventario real devuelve sin error el número de registros y ocho vistas por registro; (c) la CI guarda JSON y SHA-256; (d) tras eventual fusión, se verifica la CI del nuevo `master`. Cualquier discrepancia real detiene el cierre: **no modificar la entrada archivada para forzar concordancia**.

Comandos de CI:

```sh
python -m unittest discover -s tests -p 'test_visual_inventory_projections.py' -v
python scripts/audit_visual_inventory_projections.py --out visual-inventory-projections.json
sha256sum visual-inventory-projections.json > visual-inventory-projections.sha256
```

La comprobación es determinista, sin semilla, selección de palabras ni parámetros ajustados. El JSON incluye hashes de inventario comprimido, manifiesto y transcripciones. Las transcripciones, `inventory.json.gz`, manifiesto v2, resultados históricos y `state/committed_claims.md` permanecen congelados.

## Límites científicos y siguiente paso

Reutilizar el mismo lexer que el constructor **solo demuestra reproducción interna** de sus proyecciones, no conformidad independiente IVTFF. Las ediciones son lecturas del mismo manuscrito. La auditoría no examina imágenes ni referentes externos, no ajusta modelos y no convierte el holdout históricamente expuesto en validación ciega. Ninguna palabra EVA recibe significado.

**Pendiente:** inspeccionar CI, logs y artefacto de la PR; revisar concurrencia y `master` antes de fusionar. Tras cerrar la incidencia, priorizar adjudicación IVTFF independiente y anotaciones visuales con procedencia, sin lanzar una búsqueda semántica mientras estén bloqueadas.
