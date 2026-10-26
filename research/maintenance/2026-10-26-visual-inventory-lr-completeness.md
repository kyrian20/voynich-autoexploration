# Censo de completitud L/R del inventario visual — 26-10-2026

**Estado inicial: PROPOSED; no declarar cierre hasta CI verificada.** Reparación de integridad, no nuevo EXP ni experimento de traducción.

## Incidencia falsable

PR #73 vinculó las 2.196 filas **presentes** en el inventario a líneas físicas de las transcripciones, pero no probó que **todas** las líneas L/R elegibles estuvieran presentes. La eliminación de una fila sin alterar los bytes de las fuentes podía superar esa auditoría de vinculación. Criterio de aceptación fijado antes de ejecutar: censo independiente de líneas L/R idéntico al conjunto de líneas archivadas por edición, sin filas extra, sin líneas indecidibles y con `selected_rows` coincidente.

## Implementación y controles

- `scripts/audit_visual_inventory_completeness.py`: reescanea cada línea física de ZL3b e IT2a usando una expresión independiente del constructor, clasifica registros con marcador de locus L/R y compara conjuntos de números de línea, además de invocar primero la auditoría exacta de PR #73.
- Rechaza ausencias, inclusiones ajenas a L/R, recuentos declarados falsos y líneas no interpretables en lugar de descartarlas silenciosamente.
- `tests/test_visual_inventory_completeness.py`: seis regresiones sintéticas, incluido un ejemplo en que la auditoría previa de vinculación acepta una selección incompleta. Se conservan casos negativos como pruebas.
- `.github/workflows/voynich-check.yml`: ejecuta regresiones y censo sobre las fuentes reales y publica JSON y SHA-256 en un artefacto de CI.

Comando reproducible desde la raíz del repositorio:

```sh
python -m unittest discover -s tests -p 'test_visual_inventory_completeness.py' -v
python scripts/audit_visual_inventory_completeness.py --out visual-inventory-completeness.json
sha256sum visual-inventory-completeness.json > visual-inventory-completeness.sha256
```

El informe JSON conserva hashes de los dos corpus, del inventario gzip y del manifiesto; no hay parámetros estocásticos ni semilla. No se alteran transcripciones, inventario, manifiestos, resultados históricos ni compromisos científicos.

## Límites y decisión

El censo verifica completitud **solo bajo la gramática explícita de selección L/R del constructor**, no conformidad integral con IVTFF. Las ediciones alternativas no son muestras independientes. No certifica que un locus represente un objeto ilustrado, que exista anotación ciega o que haya una traducción. Se comprueban metadatos de todas las particiones sin analizar resultados reservados.

La CI posterior a la integración en `master` debe verificarse por separado. Si aparecen líneas indecidibles o diferencias, registrar BLOCKED con los números de línea; no regenerar el inventario histórico bajo otra fuente y llamarlo reproducción.
