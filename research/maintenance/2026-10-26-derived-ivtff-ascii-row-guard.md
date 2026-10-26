# Rechazo de dígitos Unicode en dos lectores IVTFF derivados — 26-10-2026

**Alcance:** mantenimiento de validación de identificadores, sin EXP nuevo ni prueba semántica. Base congelada de la rama: `6bd304c333400c41beadf4c79bc5ed5fd04cd015` (`master`). No reescribir los inventarios anteriores ni sus hashes.

## Defecto y criterio

`scripts/audit_research_readiness.py` y `research/decipherment/2026-10-26-astronomical-anchor/run.py` conservaban `\\d` en el patrón de aceptación `ROW`, a diferencia del auditor estructural reparado en PR #58. En Python, `\\d` reconoce dígitos decimales Unicode. Por tanto, una línea sintética como `<f68r3.١١,@Ls> doary` podía entrar como registro válido, mientras el auditor estricto rechazaba el identificador. Este es un defecto de contrato entre lectores; no se ha encontrado tal entrada en los corpus originales fijados por hash.

**Corrección:** los dos patrones aceptan exclusivamente `[0-9]`. Si aparece un numeral decimal Unicode en el prefijo de un tag `<f…>`, ambos lectores fallan explícitamente en vez de descartar silenciosamente la fila. No se amplía el universo de registros ni se interpreta el texto.

## Regresiones y verificación requerida

`tests/test_ivtff_ascii_row_readers.py` comprueba las dos rutas con entradas sintéticas: página numérica con dígitos árabe-índicos, número de locus con esos dígitos y locus nombrado `fRos` con número no ASCII. Control positivo: `f68r3.11` y `fRos.1` siguen siendo aceptados. La CI ejecuta este archivo antes del inventario de preservación de información y conserva sus auditorías habituales.

Comando: `python -m unittest discover -s tests -p 'test_ivtff_ascii_row_readers.py' -v`. No hay aleatoriedad, parámetros ajustados, ni semilla. **Pendiente:** revisar CI de la PR, después de integrar comprobar CI del nuevo SHA de `master`. Una suite omitida no cuenta como prueba superada.

## Preservación y limitaciones

No se cambian corpus, particiones de hojas, lector léxico congelado, resultados negativos ni inventarios astronómicos `inventory.json`/`inventory-v2.json`. El script astronómico cambia de hash; sus salidas futuras incluirán el hash nuevo y no se deben hacer pasar por reproducciones byte a byte de las salidas archivadas con el script anterior. El inventario histórico v2 conserva su valor documental para las fuentes congeladas; no constituye una validación independiente de la conformidad IVTFF. La identidad semántica de `doaro`/`doary` continúa **BLOCKED**.

El cambio solo prueba un fallo de validación sintético. Quedan por resolver ligaduras, alternativas, procedencia de corpus y auditoría científica global. No se adjudica ninguna traducción.
