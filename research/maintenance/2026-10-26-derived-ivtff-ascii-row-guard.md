# Guard de dígitos ASCII en inventario astronómico IVTFF — 26-10-2026

**Alcance:** una corrección de lectura estructural, sin EXP nuevo ni inferencia semántica. Base: `6bd304c333400c41beadf4c79bc5ed5fd04cd015` (`master`).

## Defecto demostrado

`research/decipherment/2026-10-26-astronomical-anchor/run.py` aceptaba `\\d` en su patrón `ROW`, que en Python incluye decimales Unicode. Así, el inventario de candidatos podía tratar una fila sintética como `<f68r3.١٢,@Ls> doary` como si su identificador fuese válido, aunque el auditor estricto IVTFF ya exige `[0-9]`. No hay evidencia de que los corpus congelados contengan estos identificadores.

**Corrección:** el patrón del inventario astronómico exige `[0-9]` y el lector rechaza explícitamente un numeral decimal Unicode en el prefijo `<f…>` para evitar omisiones silenciosas. El control positivo ASCII permanece en las pruebas existentes. Se añadieron tres fixtures negativos en `test_run.py` (folio numérico, número de locus y locus `fRos`). La CI existente ejecuta esas pruebas en Python normal y `-O`, reproduce dos veces el inventario y compara los resultados.

## Fallo de integración detectado y preservación del historial

La primera versión de la propuesta también modificaba `scripts/audit_research_readiness.py`. El run [40252066138](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40252066138) falló **antes** de ejecutar los tests nuevos: `scripts/audit_exp173_reader_bridge.py --check` devolvió `Snapshot mismatch: results.json`. La causa comprobable es que ese snapshot congelado incluye el SHA-256 de `audit_research_readiness.py` en `dependencies_sha256`; al cambiar la dependencia, ya no podía llamarse reproducción exacta.

**Decisión:** se restauró `audit_research_readiness.py` byte a byte desde el commit base. Se retiró la prueba general y el paso CI añadido, dejando la reparación **solo** en el inventario astronómico y su suite ya existente. No se alteran los snapshots ni se relaja el comprobador EXP-173. La aceptación Unicode de `audit_research_readiness.py` queda como incidencia separada **BLOCKED** hasta versionar y reproducir explícitamente el puente EXP-173 bajo la nueva dependencia, sin sustituir su archivo histórico.

## Preservación y criterio de cierre

Se conservan transcripciones, manifiestos, lexer congelado, resultados negativos, `inventory.json`, `inventory-v2.json`, logs y checksums anteriores. El script astronómico cambia de SHA-256: sus nuevos artefactos incluyen un hash distinto y no se presentan como reproducciones byte a byte de los artefactos históricos. No hay semillas ni parámetros estocásticos para los fixtures.

**Pendiente de cierre:** CI verde de la rama corregida, revisión del diff, integración y CI del SHA posterior de `master`. Este control no certifica conformidad IVTFF completa ni descifra `doaro`/`doary`.
