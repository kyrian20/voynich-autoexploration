# EXP-173: control exacto que conserva cada línea — 23-10-2026

Estado: REPRODUCED para el cálculo descriptivo y snapshot de este paquete; alcance exploratorio. No valida EXP-173 completo, sus valores p ni una interpretación lingüística. Base c70a0ba5a97276edce09d7bfe7b8dc88514a2881. Protocolo escrito antes de ejecutar, selección retrospectiva declarada.

## Resultado

Se conserva el lector histórico y se seleccionan 2.466 líneas con $L=B explícito: 20.652 tokens, 82 páginas, 40 folios numéricos y 16 líneas de un solo token. No se imputa ninguna etiqueta. Bajo permutación uniforme dentro de cada línea, la esperanza exacta del conteo en un extremo es la suma de la proporción del rasgo en cada línea.

| Rasgo | Observado | Esperado agrupado histórico | Esperado por línea | Cociente agrupado | Cociente por línea |
|---|---:|---:|---:|---:|---:|
| Final -am al final de línea | 331 | 48,4794 | 46,1175 | 6,82765 | 7,17732 |
| Inicio y al principio de línea | 355 | 101,6156 | 109,9933 | 3,49356 | 3,22747 |

La diferencia entre ambos denominadores no elimina estos dos patrones en la población histórica seleccionada. Para -am aumenta el cociente; para y lo reduce. Son dos estimandos diferentes: el nuevo cociente no reemplaza ni contradice por sí solo las cifras históricas de C005/C006. No se calcula distribución nula, significación, intervalo de confianza ni mecanismo causal. Conservar cada línea controla su longitud e inventario, pero no establece conformidad IVTFF, independencia de folios, ausencia de selección retrospectiva ni semántica.

## Verificación pendiente cerrada

En el checkout completo se ejecutaron satisfactoriamente las seis pruebas de `test_exp173_currier_crosswalk.py` y el cotejo completo de su `results.json`; también las cinco pruebas de `test_exp173_c005_scope.py` y su cotejo completo. Esto cierra la ejecución local pendiente descrita en esos informes, sin editar los originales. La CI del commit base terminó con éxito: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39879806640 . Esa CI precede al presente paquete.

## Reproducción

Python estándar, sin dependencias externas, semillas ni simulación Monte Carlo. Fuente SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`. El script comprueba la fuente y el contrato histórico antes del cálculo; el hash del lector figura en results.json. Comandos desde la raíz:

```sh
python tests/test_exp173_line_null.py
python scripts/audit_exp173_line_null.py --check research/maintenance/2026-10-23-exp173-line-null/results.json
```

Cuatro pruebas nuevas pasadas, incluido control exhaustivo de 1.440 órdenes conjuntos para cada rasgo. Las esperanzas se conservan como racionales exactos. Los decimales del JSON son aproximaciones. No se modifica ningún resultado antiguo, corpus, workflow o compromiso público.

## Autoauditoría — skills/audit_experiment.md

- Target-awareness: F3/F6 fueron seleccionados por sus resultados históricos; la auditoría es retrospectiva y no confirma una hipótesis preinscrita. Ningún parámetro se ajusta al nuevo resultado.
- Implementación: el lector histórico pierde información IVTFF; la inferencia se restringe expresamente a sus tokens. Barajar destruye orden y vecindad deliberadamente, por lo que no sirve para descartar modelos que dependan de ellos.
- Extrapolación: solo dos rasgos y la selección histórica con $L=B. Sin afirmación sobre lenguaje, significado o todas las transcripciones.
- Alcance negativo: ninguna familia de lenguas o cifrados queda descartada.
- Control: para -am se espera 2/3 y se observa exactamente 2/3 en el promedio de órdenes sintéticos; para y se espera y observa 1/2. La línea unitaria tiene esperanza y observado iguales a uno. No hay discrepancia inesperada.

Siguiente paso: comparar la cobertura y los extremos con el lector canónico sin cambiar simultáneamente las etiquetas. Solo tras adjudicar esas diferencias, fijar un protocolo de incertidumbre por folio. No interpretar estos cocientes como traducción.
