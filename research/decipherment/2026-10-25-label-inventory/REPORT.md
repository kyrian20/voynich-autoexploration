# Inventario de etiquetas por registro físico — 25-10-2026

Estado: **REPRODUCED**, exclusivamente para la generación determinista de este inventario con el lector existente. Evaluación semántica **BLOCKED**. No es un nuevo EXP, una anotación visual ni una validación independiente de IVTFF.

## Alcance y resultados

Base del código y fuentes: commit 412fd7cc2f830f1e9f4a298154d163af95cbc79a. Se selecciona cada registro cuyo código de locus empieza por L o R después del marcador de registro, sin seleccionar por grafía EVA o identidad botánica deseada. Se incluyen identificadores no numéricos. No se equipara esta selección con las 1.087 filas del lector histórico EXP-580: es una definición nueva y explícita.

| Edición | Registros seleccionados | Otros registros conservados en exclusiones | IDs seleccionados ausentes respecto a la unión |
| --- | ---: | ---: | ---: |
| ZL3b | 1.171 | 4.214 | 1 |
| IT2a | 1.025 | 4.190 | 147 |

Total: 2.196 registros de fuente, 1.172 identificadores distintos en la unión, cero líneas no clasificadas y cero errores de proyección en las ocho vistas. Las ediciones son lecturas del mismo manuscrito: no son muestras independientes. Las ausencias se registran sin completar ni imputar texto.

Dos registros con marcadores especiales se conservan y señalan para adjudicación: ZL3b fRos.110 `/L0` e IT2a f89v2.26 `!Lf`. Este inventario no certifica la interpretación de esos marcadores. Las continuaciones del cuerpo no se unen entre registros; de existir una cadena incompleta, quedaría un error explícito por vista.

Cada registro contiene edición, hash completo de fuente, línea física, línea literal y hash, folio, locus, metadatos de cabecera, cuerpo crudo y diagnósticos. Ocho proyecciones cruzan espacios inciertos split/join, alternativas primary/exclude_word y ligaduras expand/opaque. Los índices de las listas de tokens solo tienen sentido dentro de su vista; no se afirma alineamiento de tokens entre vistas o ediciones. Las lecturas alternativas siguen conservadas en el cuerpo crudo, no se enumeran todas sus combinaciones.

En f65r se conservan `otaim/dam/alam` y `otaimdam/alam`; en f41v se conserva `[e:o]`. En IT2a se documenta la ausencia de la etiqueta f2r.14. No se adjudican mediante nombres propuestos.

## Referentes visuales

Se enlaza la procedencia visual archivada existente para seis registros de los tres folios f2r/f41v/f65r. El enlace corresponde al folio completo, no a una región de imagen identificada. No se han vuelto a descargar ni inspeccionar imágenes. El hash del manifiesto archivado figura en inventory.json.

**Cero registros elegibles para evaluación semántica:** categoría visual, referente externo y fuente de anotación independiente permanecen nulos. Todos conservan el motivo de exclusión; un enlace a Yale no es identificación botánica ni una traducción. No se inventan referentes para rellenar campos.

## Reproducción y pruebas

Python 3.12.14. Desde la raíz:

```sh
python scripts/build_label_occurrence_inventory.py --out research/decipherment/2026-10-25-label-inventory/inventory.json
python -m unittest discover -s tests -p test_label_occurrence_inventory.py -v
python -m unittest discover -s tests -v
```

Cinco pruebas específicas aprobadas: selección amplia con marcadores especiales e IDs no numéricos, espacios inciertos y procedencia de línea, errores visibles, duplicados/desacuerdo de cabecera, y cobertura de fuentes reales. Suite completa: 251 pruebas, OK, una omitida por ausencia del archivo crudo de la batería histórica. Una segunda generación coincide byte a byte mediante cmp. SHA256.json fija script, tests, JSON descomprimido y archivo gzip. El paquete publica inventory.json.gz (gzip con mtime=0); para inspeccionarlo: `gzip -dc inventory.json.gz`. El comando anterior reconstruye el JSON sin comprimir. No se ejecutó la batería CI completa ni el código propuesto en PR #13.

## Autoauditoría (skills/audit_experiment.md)

- Conciencia del objetivo: selección declarada por metadatos L/R, sin ajuste a palabras o significados. Las tres imágenes enlazadas proceden de candidatos exploratorios previos; no constituyen una muestra visual independiente.
- Destrucción de rasgos: el cuerpo literal se conserva; las proyecciones pueden excluir palabras ambiguas, por lo que no sustituyen al original ni a una transcripción paleográfica.
- Extrapolación: los recuentos describen estas dos fuentes y esta selección. No certifican todas las etiquetas reales del manuscrito ni conformidad plena IVTFF.
- Negativos: cero referentes verificados significa falta de anotación independiente en este paquete; no significa ausencia de significado.
- Controles: no se realiza contraste inferencial. Las pruebas con fixtures comprueban conservación de incertidumbre y visibilidad de errores; la regeneración comprueba determinismo, no independencia del lector.

## Próxima acción

Crear una guía de anotación de imágenes sin mostrar EVA al anotador, delimitar las regiones de etiquetas y registrar categoría, incertidumbre, identificador de anotador y fuente externa. Someter primero los dos marcadores especiales a adjudicación documental. Solo después medir acuerdo entre anotadores y decidir si hay suficientes hojas con referentes fiables para congelar uno de los protocolos predictivos. No entrenar con los campos nulos ni declarar un holdout históricamente ciego.
