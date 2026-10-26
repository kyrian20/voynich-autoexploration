# Corrección de cobertura y estado del inventario astronómico

26-10-2026, Madrid. Mantenimiento acotado; sin EXP nuevo ni traducción.

## Defecto reproducido

En la base b0d84dab43ea57e305b5909de0d5b96d618aa25e, ROW acepta páginas numéricas y fRos, siempre con número de locus. El contador único numeric_records y la descripción Numerical-locus inducían a llamar numéricos a los 5.385 registros ZL3b. El desglose real es 5.225 numéricos + 160 fRos. IT2a conserva 5.215 + 0. Los encabezados de página no se contaban: este defecto es distinto al corregido en PR64.

Además, el CLI se autocalificaba REPRODUCED al escribir cualquier archivo, antes de contrastarlo. Ahora declara GENERATED; la reproducción se acredita mediante comparación y recibo separados. La comprobación del locus objetivo usaba assert; ahora se rechaza con ValueError también bajo Python -O.

## Reparación y compatibilidad

run.py publica schema_version=2, parsed_records, numeric_records y named_records. En schema2 numeric_records solo cuenta loci en páginas numéricas; el significado del campo histórico no debe trasladarse entre versiones. El protocolo y el informe aclaran este alcance sin alterar el patrón aceptado o las políticas de lectura.

inventory.json, VERIFICATION.json, logs y resultados originales permanecen intactos. Sus hashes del código/informe son históricos y se verifican contra el commit original, no contra la versión corregida. inventory-v2.json y VERIFICATION-v2.json son artefactos nuevos.

## Comprobaciones ejecutadas

- Antes del cambio: cinco pruebas existentes pasaban; dos regresiones nuevas detectaron el campo ausente y el tipo incorrecto de rechazo del locus.
- Después: ocho pruebas específicas pasan tanto en Python normal como con -O, incluida comparación completa de coincidencias, contextos, posiciones y fuentes con inventory.json original.
- Dos ejecuciones con Python3.12.14 producen el mismo JSON v2 byte a byte.
- ZL3b: total5385 = numéricos5225 + nombrados160; IT2a:5215 =5215 +0.
- Coincidencias intactas en ambas políticas: doaro1/1, doary0/0, dary23/24 según edición. No se ha adjudicado ninguna lectura o significado.
- Suite de tests/ después del cambio:304 ejecutadas,303 aprobadas y1 omitida por archivo histórico no disponible. Los mensajes FAILED de transporte dentro de esa salida pertenecen a simulaciones previstas; el resultado unittest es OK.
- Auditoría operativa e identidad de14 corpus sin errores, con el corpus previamente en cuarentena conservado como tal. No certifican procedencia, licencia o conformidad IVTFF completa.
- Se añade a Voynich Check la batería específica, reproducción doble y artefacto astronomical-anchor-v2-<run_id>. La configuración no demuestra todavía CI verde del nuevo commit: comprobar su run exacto antes de fusionar.

## Autoauditoría según skills/audit_experiment.md

Conciencia del objetivo: corrección de un contador sobre corpus ya conocido; no selección de una hipótesis lingüística. Destrucción de rasgos: no cambia lexer, tokenización, fuentes o selección. Extrapolación: solo cobertura/estado de este inventario. Alcance negativo: no refuta Tauro ni otras interpretaciones; la admisión semántica sigue BLOCKED. Controles: se esperaba igualdad de todas las coincidencias archivadas y de la suma de categorías; ambas pasan. No hay p-valores ni muestra independiente.

## Pendiente

Verificar CI remota de la rama y eventual integración. No se reproduce el conjunto de624 experimentos históricos ni se declara limpieza global. La revisión documental ampliada existente en ../2026-10-26-documentary-context/REPORT.md ya había recuperado el comparador Met; no volver a contabilizar su localización como hallazgo nuevo.
