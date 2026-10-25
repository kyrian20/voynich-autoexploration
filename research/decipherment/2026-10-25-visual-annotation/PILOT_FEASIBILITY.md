# Viabilidad del piloto visual — selección inicial

25-10-2026. Estado: **BLOCKED**. Comprobación ejecutada sobre inventario archivado; sin entrenamiento, anotación ni consulta de resultados semánticos.

## Regla aplicada
Primeras 12 hojas de train del manifiesto v2 en orden numérico: 1, 2, 6, 7, 8, 10, 13, 14, 16, 17, 18, 19.
Se interpreta «ordenar por identificador de hoja» como orden numérico de hoja física. No se filtra antes por existencia de rótulos, palabra EVA o imagen deseada. Se mantiene esta selección; no se rellenan huecos con hojas posteriores.

Fuentes:
- research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json; blob Git 84f59008a190df7481c4e81a5c84c3916d79a59d.
- research/decipherment/2026-10-25-label-inventory/inventory.json.gz; blob Git 0a71e0d12ede5b5efe9386456230007df283a354.
- SHA256 de los bytes gzip: cc4f79d106e21d9e690a6f1e38436761f5770808713c3fef3aaa51ad0f680ce4.

## Resultado calculado
| Hoja | Registros de edición | Localizadores distintos | Registros con fuente visual archivada |
|---|---:|---:|---:|
| 1 | 0 | 0 | 0 |
| 2 | 2 | 2 | 2 |
| 6 | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 |
| 8 | 0 | 0 | 0 |
| 10 | 0 | 0 | 0 |
| 13 | 0 | 0 | 0 |
| 14 | 0 | 0 | 0 |
| 16 | 0 | 0 | 0 |
| 17 | 1 | 1 | 0 |
| 18 | 0 | 0 | 0 |
| 19 | 0 | 0 | 0 |

Solo f2r y f17r están representados. Los tres registros/localizadores no acreditan tres objetos, categorías distintas, cobertura completa de ambas ediciones ni regiones adjudicadas. Las dos fuentes archivadas de hoja 2 son referencias por registro, no necesariamente dos imágenes distintas.
Cero registros en este inventario no demuestra ausencia de rótulos en el original.
No se han recuperado imágenes nuevas ni aprobado máscaras. No hay anotadores independientes identificados en esta sesión.

## Método reproducible
Descomprimir el gzip con gzip.decompress; leer records. Para cada hoja seleccionada, aceptar folio con re.fullmatch(r'f(\\d+)[rv]\\d*', folio), comparar el grupo numérico y contar filas, valores distintos de id y image_source_archived no vacío.
Los conteos se ejecutaron localmente con Python sobre los bytes del blob, sin usar tokens, categorías o nombres esperados para seleccionar. No se reprodujo el lector desde transcripciones; se audita cobertura del inventario, no conformidad IVTFF ni completitud paleográfica.
La regla de selección puede verificarse con sorted(manifest['partitions']['train'])[:12].

## Decisión
La selección inicial no proporciona cobertura suficiente para el piloto de hasta 12 hojas previsto y no permite medir fiabilidad o diversidad. Se pausa esta selección; no entrenar ni ampliar automáticamente.
Esto no refuta que rótulos y dibujos puedan estar relacionados. Revela un defecto de diseño de muestreo: seleccionar hojas del manuscrito completo no garantiza unidades elegibles del estudio de rótulos.
Una futura enmienda podría definir primero el universo de hojas de entrenamiento con rótulos auditados y después seleccionar determinísticamente, pero sería un cambio de diseño explícito, no ejecución exitosa de este piloto. No se ha aplicado en esta comprobación.
La falta de dos anotadores independientes y máscaras revisadas sigue bloqueando cualquier estudio posterior, incluso si se enmienda el muestreo.

## Autoauditoría y límites
- Selección fijada antes de conteos; sin reemplazos posteriores.
- No se alteraron corpus, lectores ni inventario; análisis exclusivamente de metadatos.
- No es prueba de hipótesis semántica ni estimación de potencia.
- Se conservan resultados desfavorables y se distingue falta de datos de resultado negativo.
- Cambio documental y cálculo acotado; no suite global ni CI certificada.
