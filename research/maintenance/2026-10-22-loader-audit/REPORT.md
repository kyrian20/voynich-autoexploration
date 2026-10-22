# Auditoría de lectores históricos de Cicero — 22 de octubre de 2026

Estado: diagnóstico de entradas; no reproducción de simulaciones ni validación de conclusiones históricas. Fuente congelada: commit `1e49032d698713dd29672fd6fbbf2107cac80cd8`.

## Qué se comprobó

Se censaron los 100 scripts de `experiments/` con una referencia literal a `cicero_de_officiis_latin.txt`. Se aislaron sus funciones lectoras mediante AST: no se importaron módulos históricos ni se ejecutaron sus simulaciones, escrituras o búsquedas de parámetros. Se ejecutaron los lectores sobre el archivo bilingüe congelado y se contrastó su selección con una reconstrucción independiente. El JSON conserva hashes del corpus, scripts, AST y secuencias seleccionadas, así como líneas de evidencia y listas exactas de palabras del filtro.

Las siete menciones anteriores a la variable `english_stopwords` eran una búsqueda literal de ese nombre; **no significaban que solo siete scripts filtrasen el inglés**. Muchos emplean `ENGLISH_SW` o `ENGLISH_STOPWORDS`.

## Selecciones reproducidas

96 lectores coinciden con su reconstrucción; quedan cuatro casos sin resolver. Estos grupos cuentan scripts, no ejecuciones independientes.

| Scripts | Tokens seleccionados | Selección |
|---:|---:|---|
| 14 | 34,977 | Filtro de párrafos; variante histórica |
| 78 | 35,090 | Filtro de párrafos; variante histórica |
| 1 | 112,081 | Sin filtro de idioma |
| 1 | 107,590 | Sin filtro de idioma |
| 1 | 32,711 | Filtro de párrafos; variante histórica |
| 1 | 32,765 | Filtro de párrafos; variante histórica |

## Hallazgos y alcance

Los filtros de párrafos conservan material ajeno al texto principal: encabezados, bibliografía e índices. Ejemplos verificables: `CONTENTS` (línea 42), `CORRECTIONS:` (14259) y entradas de índice. En los lectores de EXP584/585 sobrevive la entrada inglesa `Slaves, duty toward, I, 41; III, 89.` (13955). Su existencia demuestra contaminación residual; no cuantifica el porcentaje total de inglés o de latín perdido.

EXP259 y EXP260 usan `parse_latin` sin separación de idiomas: tokenizan el archivo entero, incluida la traducción inglesa. Los conteos comparativos allí denominados «Latin» no pueden interpretarse como una muestra monolingüe latina sin una nueva reproducción sobre una selección adjudicada. No se ha recalculado su efecto sobre las métricas o conclusiones.

Los lectores que segmentan en bloques aleatorios de 8–15 tokens tampoco recuperan oraciones o cláusulas del original. La semilla de este diagnóstico sirve para hacer reproducibles esos bloques; no reproduce el estado aleatorio de una ejecución histórica. El diagnóstico compara además el conjunto ordenado de tokens antes de segmentarlos.

Los cuatro casos sin lector aislado se revisaron estáticamente: EXP266 y EXP577 declaran la ruta, pero el AST no contiene ninguna lectura de esa variable; EXP267 y EXP288 leen el archivo en línea sin separar idiomas. Así, hay cuatro consumidores sin separación de idiomas identificados en fuente (259, 260, 267 y 288), de los cuales dos lectores se ejecutaron de forma aislada. No se han analizado accesos dinámicos o transitivos.

Las otras tres referencias del inventario se revisaron estáticamente: EXP001 pasa Vulgata al tokenizador genérico; EXP170 la pasa al lector de líneas; EXP031 declara una ruta antigua distinta (`latin_vulgate.txt`) sin ninguna lectura AST de la variable `LATIN`. Ninguna de estas tres simulaciones se ejecutó en este diagnóstico. El inventario inicial buscaba nombres de archivo, por lo que el caso EXP031 no prueba uso del archivo canónico. Una referencia a un archivo nunca se equipara automáticamente a una ejecución ni a un resultado inválido.

No se cambian corpus, experimentos, resultados ni compromisos históricos. La exclusión de Cicero de nuevas bases monolingües sigue vigente. No procede sustituirlo silenciosamente por otro texto: cambiarían edición, género, tamaño, vocabulario y filtros.

## Reproducción

Desde cualquier directorio, con Python 3.12:

```sh
python /ruta/al/repositorio/tests/test_historical_latin_loaders.py
python /ruta/al/repositorio/scripts/audit_historical_latin_loaders.py --check /ruta/al/repositorio/research/maintenance/2026-10-22-loader-audit/results.json
```

Para generar otro diagnóstico se usa `--out /ruta/nueva/results.json`. El modo `--check` no escribe resultados y exige igualdad de la estructura completa. La CI ejecuta ambos comandos. El inventario anterior de referencias conserva su alcance histórico y excluye explícitamente este nuevo diagnóstico; no se cuentan sus declaraciones de entrada como un experimento adicional.

## Autoauditoría

1. **Conocimiento del objetivo:** se reutilizan los filtros originales sin ajustarlos a métricas del Voynich. No se evalúa ningún modelo de descifrado.
2. **Destrucción de rasgos:** los filtros pueden aceptar encabezados y rechazar latín que comparte palabras con el inglés. Las pruebas adversariales exhiben ambos riesgos; no estiman su prevalencia real. La tokenización ASCII puede alterar palabras con diacríticos.
3. **Extrapolación:** el censo cubre referencias literales en `experiments/`, no dependencias transitivas ni todo uso histórico del corpus.
4. **Resultados negativos:** no se infiere ausencia de lenguaje, semántica o posibilidad de descifrado.
5. **Controles:** las pruebas verifican que el cuerpo del módulo no se ejecuta, que pasan encabezados ingleses, que un párrafo inglés común se rechaza, que homógrafos latinos pueden activar el filtro y que el lector sin filtro conserva ambos idiomas. La reconstrucción se detiene ante cualquier discrepancia; una diferencia inicial entre expresiones regulares con y sin límites de palabra se corrigió antes de archivar la salida final.

## Trabajo pendiente

Reproducir los dos consumidores en línea y los dos lectores activos de Vulgata; adjudicar segmentos del Cicero bilingüe con offsets de origen; relacionar cada ejecución y afirmación con su entrada efectiva; repetir solo las comparaciones que dependan de esas entradas, conservando el resultado original. La auditoría no autoriza todavía nuevas inferencias lingüísticas con esos controles.
