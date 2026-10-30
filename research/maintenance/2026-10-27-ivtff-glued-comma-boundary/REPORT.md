# Auditor IVTFF: cabecera con coma y sufijo pegado — 27-10-2026

**Estado inicial:** corrección de código propuesta; la CI de la PR y la de una eventual fusión deben comprobarse por SHA. No se crea EXP ni se ejecuta una hipótesis de desciframiento.

## Defecto concreto, relación con correcciones anteriores

En `scripts/audit_ivtff_page_locus_ids.py::audit_text`, el guardia para un sufijo pegado tras `>` se ejecutaba **antes** del detector de cabeceras dañadas por coma. Así, tras `<f1r>`, una línea `<f2r,>garbage` se clasificaba como **registro malformado** y conservaba `active_page=f1r`. El locus posterior `<f1r.2,@P0>` se aceptaba sin discrepancia de folio. La combinación de ambas corrupciones no estaba cubierta por los fixtures de la reparación de comas (26-10) ni por los de límites de etiquetas (27-10). No se infiere que haya sucedido en los corpus históricos.

**Criterio de regresión:** `<f2r,>garbage`, `<fRos,><! $L=B>`, `<f86v4 ,>garbage` y `<f٢r,>garbage` deben registrar una cabecera malformada, invalidar la página activa y detectar un `page_mismatch` en el locus antiguo siguiente; no deben sumar un registro malformado. Los registros genuinos con sufijo pegado deben seguir siendo rechazados como registros. Las cabeceras bien formadas deben permanecer aceptadas.

## Reparación

Se antepone el detector de cabecera con coma al detector de sufijo pegado. No se modifica la gramática aceptada, ni se normaliza ninguna cabecera corrupta. Se añaden cuatro fixtures deterministas al archivo `tests/test_ivtff_page_locus_ids.py`, que la CI canónica ejecuta directamente. La intervención se limita a estos dos archivos y a este informe.

## Procedencia y reproducción

- Base fija: `master` `0de7b0aefcb97abf4b5b6a40d861757b4b8d1c61`.
- Corpus originales congelados (no modificados): ZL3b `data/transcriptions/eva_zl3b.txt`, SHA-256 archivado `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; IT2a `data/transcriptions/eva_it2a.txt`, SHA-256 archivado `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`. Estos hashes se citan del manifiesto existente; no son recálculos de esta sesión.
- Fuente de evidencia del defecto: inspección del orden de las dos ramas condicionales en el código del SHA base y fixture sintético adversarial. No se atribuye una ejecución local de Python.
- Comandos para CI: `python tests/test_ivtff_page_locus_ids.py`, `python scripts/audit_ivtff_page_locus_ids.py`, `python -m unittest discover -s tests -v`, `python scripts/check_corpus_integrity.py`, `python scripts/audit_repository_operations.py`.
- Parámetros: cuatro entradas sintéticas explícitas; semilla no aplicable. Unidad: fila estructural y folio activo. No se consulta ni puntúa el contenido de hojas de prueba.
- Verificación: registrar el run, SHA, conclusión, pasos y artefactos de la PR; si se integra, comprobar CI de `master` por separado.

## Límites y siguiente incidencia

Esta reparación fortalece el **auditor estructural**, no los lectores científicos históricos. No certifica conformidad integral IVTFF ni reconciliación de artefactos de Biblioteca; no modifica manifiestos, resultados negativos, corpus, EXP ni `state/committed_claims.md`. La antigua cifra de 1.466/1.472 discrepancias corresponde al protocolo v1 de EXP-602; el v7 registra cero discrepancias bajo su propia política, pero no demuestra conformidad normativa. Próximo paso: contrastar los fixtures pendientes de IVTFF contra la especificación y adjudicar lectores/corpus históricos sin reinterpretar el holdout como ciego.
