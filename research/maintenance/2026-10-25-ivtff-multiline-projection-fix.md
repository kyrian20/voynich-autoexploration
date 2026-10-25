# Corrección de proyección IVTFF: filas independientes y continuaciones — 25-10-2026

**Estado:** propuesta de reparación operativa, pendiente de CI específica y revisión. No es un EXP ni una traducción.

## Defecto reproducible

En `scripts/ivtff_lossless.py`, la validación anterior de `tokens(payloads)` exigía que toda fila posterior a la primera empezara por `/` y que toda fila anterior a la última terminara en `/`. Por tanto, dos filas ordinarias consecutivas, como `ab.cd` y `ef.gh`, lanzaban `ValueError('Incomplete or unpaired continuation chain')` aunque no existiera continuación. Una implementación que omitiera la validación y simplemente visitara ambas filas también podría concatenar palabras entre líneas. Esto impide utilizar correctamente la proyección sobre colecciones de filas físicas.

## Cambio y criterio

El validador exige ahora emparejamiento **local** entre `/` final de una fila y `/` inicial de la siguiente. Las filas ordinarias son independientes y fuerzan un límite de palabra, mientras que las filas unidas por continuaciones preservan la concatenación. No se cambia la lexicación de cada fila, las transcripciones, los hashes originales, las políticas de alternativas/ligaduras ni los tokenizadores históricos.

La regresión ejecutada por `Voynich Check` (`python tests/test_ivtff_lossless.py`) cubre dos filas ordinarias, una cadena de continuación completa, dos cadenas separadas, mezcla de filas normales y continuadas, fila vacía y cuatro cadenas mal emparejadas que deben rechazarse.

## Alcance científico y limitaciones

Se trata de una reparación de la **proyección léxica auxiliar**. No demuestra conformidad completa con IVTFF 2.0.2, no reinterpreta experimentos archivados y no permite reabrir automáticamente los clasificadores Currier ni la evaluación de folios reservados. La validez de los corpus, etiquetas y reglas de separación sigue requiriendo las adjudicaciones pendientes.

No se atribuye ninguna semántica a las cadenas EVA. El cambio no utiliza semillas ni controles estocásticos; es una prueba determinista con entradas sintéticas. Los resultados de CI y el SHA de integración deben comprobarse antes de marcar esta incidencia como cerrada.
