# Preflight ASCII del lector histórico de readiness — 26-10-2026

**Tipo:** reparación operativa acotada, sin EXP nuevo, sin prueba semántica.
**Base:** `master` 06292cf69a4bd3b65dbda16102b2add153625591.
**Incidencia previa:** [guard de 26-10](2026-10-26-derived-ivtff-ascii-row-guard.md), apartado «Fallo de integración». No repetir el intento fallido de modificar el lector congelado.

## Defecto y reproducción sintética

El patrón `ROW` de `scripts/audit_research_readiness.py` usa `\\d`, que en Python acepta decimales Unicode. Un identificador sintético como `<f68r3.١٢,@Ls>` puede ser interpretado por ese lector como si fuera ASCII. El intento previo de editarlo directamente cambió una dependencia SHA-256 congelada del puente EXP-173 y produjo un fallo de snapshot; **no se modifica ni se reetiqueta esa reproducción histórica**.

Esta reparación añade `scripts/audit_readiness_ascii_guard.py` como comprobación previa en CI. Detecta decimales Unicode en los prefijos candidatos de filas IVTFF de las tres transcripciones y termina con error antes de ejecutar el lector histórico. Registra SHA-256 y bytes de cada fuente, además del número de prefijos comprobados, en `readiness-ascii-preflight.json` (artefacto de Actions). Un archivo ausente también detiene el proceso. El lector antiguo, los datos, sus salidas y hashes históricos quedan intactos.

## Controles y parámetros

`python -m unittest discover -s tests -p 'test_readiness_ascii_guard.py' -v` y `python scripts/audit_readiness_ascii_guard.py > readiness-ascii-preflight.json`.

Cinco pruebas deterministas: aceptación de panel y Rosettes ASCII; rechazo de cuatro posiciones con dígitos árabe-índicos; metadatos no relacionados; ausencia de fuente; y fuente sintética adulterada con verificación de inventario. Sin semillas, aleatoriedad ni comparación múltiple. El fixture sintético no sustituye ninguna entrada histórica.

**Validación local previa a publicación:** Python 3.13.5, cinco pruebas superadas y `compileall` correcto sobre los dos archivos nuevos. **CI Python 3.12 y corpus reales: pendiente hasta que se ejecute el SHA de la rama.** No se ha repetido EXP-173 localmente ni certificado la auditoría global.

## Limitaciones y criterio de cierre

El guard solo detecta numerales Unicode en prefijos de filas que siguen la forma IVTFF candidata. No adjudica identificadores arbitrariamente dañados, tokenización, ligaduras, alternativas, folios reservados, ni la validez del corpus. `audit_research_readiness.py` sigue siendo inseguro para entradas no verificadas cuando se invoca **fuera** de la CI protegida; cualquier reutilización externa debe llamar antes al guard o implementar un lector versionado y una reproducción nueva separada.

Para cerrar la **puerta CI**, verificar ejecución de PR en SHA exacto, inspeccionar artefacto de fuentes y hashes, fusionar sin conflicto y comprobar la CI del `master` posterior. El defecto del lector congelado **no** se declara reparado in situ. No hay traducción validada.
