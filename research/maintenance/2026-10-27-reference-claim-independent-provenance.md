# Puerta independiente de procedencia en auditoría de afirmaciones históricas — 27-10-2026

**Estado al preparar la PR: corrección propuesta, pruebas remotas y fusión pendientes.** No constituye reproducción histórica ni experimento científico nuevo.

## Incidencia concreta y falsable

`scripts/audit_reference_claim_links.py::audit` comparaba la identidad de los corpus de EXP-001/170/267/288 entre el snapshot de lectores y `research/CORPUS_IDENTITY_REVIEW.json`, pero no validaba por sí mismo el manifiesto congelado `research/CORPUS_INPUT_MANIFEST.json` ni la adjudicación histórica de obra/idioma. Dos metadatos alterados de manera coordinada podían coincidir y superar esta comprobación directa mientras se atribuía un corpus a una obra equivocada. El paso separado de identidad de corpus de CI ya detectaba parte de estas situaciones; esta reparación elimina la dependencia de que otro programa se haya ejecutado antes. No hay evidencia de alteración real en los archivos originales.

## Reparación limitada

Se reutiliza la auditoría ya probada `scripts/audit_corpus_identity_overlay.py::audit` dentro del auditor de afirmaciones. Se lee el manifiesto mediante JSON estricto y se verifica la adjudicación independiente de las seis exclusiones, bytes, SHA-256, identidad de obra/idioma, evidencias y cuarentena. El control se ejecuta antes de leer los scripts y corpus de los cuatro casos para emitir resultados. Se conservan los chequeos existentes de claves JSON duplicadas y de identidades duplicadas para que no cambie su diagnóstico. No se inventan etiquetas de idioma, no se modifica el corpus, el manifiesto ni los resultados históricos.

## Pruebas falsables y controles

`python tests/test_reference_claim_links.py` añade cuatro pruebas: (1) seis identidades originales coherentes pasan; (2) etiqueta de obra inventada para `vulgate.txt` se rechaza pese a conservar bytes; (3) SHA-256 adulterado en manifiesto se rechaza; (4) exclusión histórica retirada se rechaza. La auditoría original y el snapshot se deben comprobar con `python scripts/audit_reference_claim_links.py --check research/maintenance/2026-10-22-claim-link-adjudication/results.json`. El workflow `Voynich Check` ya ejecuta ambos comandos; no se duplica CI.

## Proveniencia, límites y prevención de errores

Base de rama: `33130f6d571a1eb0439802d04ccf7b1def5da30e`, master posterior a PR #107. Archivo de referencia congelado `data/reference_corpora/latin/vulgate.txt`: SHA-256 registrado `d63b1b81824e259b1cf92ba8a6e5cbbf783e2a83214cf2c3db2ecd1459165bfe`; `cicero_de_officiis_latin.txt`: `3a33a076d3dda42673ec7ab0331ae7e58fc150e7e92751c0adf6d1db7297b670`. Son hashes del manifiesto previo, **no recálculos locales**. La prueba positiva remota debe confirmar la lectura de los bytes reales. No se alteran transcripciones IVTFF, particiones reservadas, semillas, vectores EXP-170 ni resultados negativos.

**Autocrítica metodológica:** no se prueba ninguna hipótesis de lenguaje ni se eligen parámetros con información del manuscrito; la modificación solo rechaza adjudicaciones no verificadas. La reproducción de lectores no certifica que esos bytes fueran los usados históricamente. EXP-170 sigue sin dependencia Naibbe original acreditada y no se reejecuta. Los archivos etiquetados como latinos pero ingleses/bilingües siguen excluidos de afirmaciones monolingües. Una CI verde de esta PR no equivale a limpieza global ni traducción validada.

## Cierre exigido

Inspeccionar CI del SHA final de la PR, snapshot, pruebas y CI del SHA de master tras integración. Registrar fallos y sus reparaciones sin sobrescribir fuentes. Si no hay evidencia de éxito, dejar la PR sin fusionar y conservar este estado.
