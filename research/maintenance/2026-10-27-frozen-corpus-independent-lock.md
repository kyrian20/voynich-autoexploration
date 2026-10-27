# Bloque de integridad: bloqueo independiente de corpus congelados — 27-10-2026

**Estado al preparar PR: corrección propuesta; pruebas CI e integración pendientes.** No es un EXP nuevo ni un hallazgo lingüístico.

## Defecto concreto

`scripts/check_corpus_integrity.py` comprobaba que los bytes actuales coincidieran con `research/CORPUS_INPUT_MANIFEST.json`, pero no comparaba ese manifiesto contra una referencia independiente. Si alguien cambiaba simultáneamente corpus y manifiesto (hash, tamaño, estado), el auditor podía dar resultado satisfactorio. El guard de adjudicación de la PR #108 comprueba el overlay frente al manifiesto, pero no resuelve esta alteración coordinada del propio manifiesto. No hay evidencia de que haya ocurrido en los originales.

## Reparación limitada

Se fija en `scripts/check_corpus_integrity.py` la identidad revisada de los **14 archivos**: ruta, tamaño, SHA-256 y estado de cuarentena, junto con `source_commit` y versión de esquema. El nuevo `verify_frozen_manifest` exige coincidencia exacta y rechaza cambios coordinados, altas/bajas y eliminación de cuarentena. La CLI canónica ejecuta esta verificación además de la comparación de bytes existente. Para aceptar una actualización legítima es necesaria una revisión explícita y actualización deliberada de los valores fijados; nunca regenerarlos automáticamente a partir del manifiesto sometido a prueba.

Fuente de los valores: `research/CORPUS_INPUT_MANIFEST.json` en `master` `99f860444b97171963aacaa0a458e8ec17f3c49c`, blob Git `29730845e2274435676a2e3ee082d660e161e6a6`. Se trata de hashes **archivados**, no de recálculos locales. CI comprobará los bytes efectivos.

## Regresiones y comandos

Cuatro pruebas nuevas en `tests/test_corpus_integrity.py`: control positivo del manifiesto real, deriva coordinada simulada de bytes/hash/tamaño, reclasificación de archivo vacío y baja, y alta sin revisión con cambio de fuente. Ninguna prueba escribe corpus reales. Ejecutar `python tests/test_corpus_integrity.py`, `python scripts/check_corpus_integrity.py`, `python -m unittest discover -s tests -v` y revisar el workflow `Voynich Check` del SHA final de PR y de master posterior a integración. La CI ya ejecuta las dos primeras órdenes: no añadir otro workflow.

## Alcance y límites

El bloqueo detecta deriva respecto a los valores archivados de octubre, no demuestra la autenticidad histórica, idioma, licencia ni conformidad IVTFF de las fuentes. El manifiesto congelado y los 14 corpus se mantienen intactos; no se cambian EXP-170, sus salidas, semillas, particiones reservadas, etiquetas, pruebas científicas ni `state/committed_claims.md`. Los seis corpus con identidad conflictiva siguen excluidos; EXP-170 continúa BLOQUEADO para reproducción completa por la versión/entradas históricas Naibbe no acreditadas. La integridad de metadatos no es desciframiento.

## Evidencia de cierre requerida

Comprobar pruebas adversariales, CI de la PR, comparación del árbol y CI posterior a fusión; documentar enlaces, commit y fallos. No afirmar limpieza global ni éxito hasta verificar cada ejecución.
