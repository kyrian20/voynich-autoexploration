# Duplicación, identidad de corpus y continuidad científica — 22-10-2026

Estado: auditoría ejecutada y repetida byte a byte sobre el commit fuente `2da0b63617a3d6dc29b47b99a731a8c9692e9aaa`. Sin EXP nuevo, borrados ni renumeración.

## Qué se comprobó

- 1.534 archivos del commit, obtenidos de `git archive HEAD`, con SHA-256, tamaño y ruta. El número no incluye directorios: no comparar con antiguos recuentos de rutas totales.
- Cinco grupos de archivos no vacíos idénticos. Incluyen salidas antiguas y copias de archivo EXP-590/593 y del parser EXP-602. Igualdad por bytes no cambia su estatus científico ni autoriza contarlas como replicaciones.
- Un archivo vacío: `data/reference_corpora/latin/cicero_caesar_latin.txt`. Marcado `BLOCKED_EMPTY_DO_NOT_USE` en el manifiesto de entradas. No hay referencias a ese nombre en scripts Python versionados según búsqueda literal de esta revisión. No se rellena con otro texto sin procedencia.
- 14 corpus TXT congelados por hash y tamaño. La nueva guardia de CI rechaza modificaciones, altas y bajas sin revisión del manifiesto. La excepción vacía explícita preserva el archivo histórico y no lo habilita como baseline.
- EXP-607: dos transcripciones × dos lectores × dos alcances (mixed/P0), con partición por folio existente. Cero líneas completas de evaluación presentes en entrenamiento en las ocho comparaciones. Test mixed=597 registros; P0=581 por vista. No se excluye ninguna fila y las puntuaciones permanecen idénticas.

## Decisión

La coincidencia de líneas completas entre particiones no explica la ventaja del modelo en el universo ensayado porque no se encontró ninguna. No se descartan solapamientos parciales, parentesco entre páginas, selección previa del modelo ni dependencia de tokenización. Se conservan todos los archivos duplicados con sus rutas: no se fusionan informes por nombre o número EXP.

La reproducción exige el commit fuente para el inventario, además de los scripts nuevos: después de incorporarlos, HEAD tendrá legítimamente un inventario distinto. Para reproducir el inventario antiguo se debe usar un checkout del commit fuente y ejecutar una copia de este auditor. Los resultados EXP-607 solo dependen de sus inputs/lectores versionados.

## Autoauditoría

Selección del objetivo: auditoría motivada por fallos históricos; no confirmación lingüística. Implementación: la eliminación propuesta de líneas exactas no elimina ninguna en esta muestra; no se modifican originales. Extrapolación: igualdad por bytes y contaminación por líneas completas, sin equivalencia semántica ni certificación integral. Negativos: cero coincidencias no prueba independencia. Control: se esperaba caída de la ventaja si dependía de líneas completas compartidas; se observaron cero exclusiones y las ocho puntuaciones idénticas. No se interpreta ese hecho como desciframiento.

## Reproducción y límites

`python tests/test_duplicate_leakage.py`; `python tests/test_corpus_integrity.py`; `python scripts/check_corpus_integrity.py`; `python scripts/audit_duplicate_leakage.py`.

Dos pruebas de exclusión adversarial y dos de integridad pasan; se rechazan mutación de un byte, ausencia, alta y vacío no autorizado en fixtures temporales. Pruebas operativas y seis regresiones EXP-607 pasan. El inventario y el análisis se ejecutaron dos veces con igualdad exacta de JSON una vez fijada la lectura desde Git.

Pendientes: cotejo completo Biblioteca/GitHub, procedencia y licencia de todos los corpus, conformidad IVTFF independiente y evaluación científica de históricos. No se declara el proyecto entero limpio.
