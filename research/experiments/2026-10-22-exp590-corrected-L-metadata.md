# EXP-590 — Posición inicial de daiin

- Fecha UTC: 2026-10-22
- Fuente: data/transcriptions/eva_zl3b.txt
- SHA-256 de la transcripción: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc
- Líneas EVA parseadas: 5,376
- Tokens parseados: 39,594
- Ocurrencias exactas de daiin: 853
- Ocurrencias en primera posición de línea: 161
- Ocurrencias en última posición de línea: 134
- Fracción de ocurrencias en primera posición: 0.1887
- Fracción de ocurrencias en última posición: 0.1571

## Contraste de permutación

- Permutaciones: 5,000
- Semilla fija: 20261020
- Media nula de líneas que empiezan por daiin: 109.121
- Desviación típica nula: 9.315
- p empírico unilateral con corrección +1: 0.000200

La hipótesis nula permuta el orden de los tokens dentro de cada línea, conservando su multiconjunto exacto. El contraste evalúa si daiin aparece al principio de línea más de lo esperable bajo ese modelo; no prueba significado lingüístico. No se han explorado múltiples palabras en este experimento, pero cualquier búsqueda posterior deberá corregir comparaciones múltiples.


**Precaución inferencial:** el valor p es empírico para este contraste concreto, con 5.000 permutaciones. No corrige una posible selección previa de `daiin` entre otras palabras o patrones en la historia de la investigación ni otros análisis de la misma transcripción. Por tanto, debe interpretarse como evidencia exploratoria de posición bajo este modelo nulo, no como una prueba confirmatoria independiente.

## Distribución por clase de Currier

| Clase | Ocurrencias exactas | Líneas iniciales | Líneas finales | Líneas parseadas |
|---|---:|---:|---:|---:|
| A | 502 | 60 | 104 | 1815 |
| B | 314 | 91 | 27 | 2806 |
| unknown | 37 | 10 | 3 | 755 |

## Limitaciones y reproducibilidad

- Solo se cuenta el token exacto daiin; no se mezclan variantes como dain.
- La tokenización elimina etiquetas IVTFF y material entre llaves/corchetes; los resultados dependen de esa decisión.
- La clasificación Currier se lee de cabeceras de folio cuando está disponible; los casos sin clasificación quedan como unknown.
- Esto es una línea base exploratoria reproducible, no una traducción ni una afirmación de desciframiento.
- Datos completos y hash de entrada están en el JSON de este experimento.

## Impacto de la corrección de cobertura

| Métrica | Parser histórico | Parser corregido | Cambio absoluto | Cambio relativo aprox. |
|---|---:|---:|---:|---:|
| Líneas con tokens | 4.188 | 5.376 | +1.188 | +28,4 % |
| Tokens | 32.732 | 39.594 | +6.862 | +21,0 % |
| Ocurrencias exactas de `daiin` | 726 | 853 | +127 | +17,5 % |
| Líneas con `daiin` inicial | 133 | 161 | +28 | +21,1 % |

Las dos columnas proceden de ejecuciones con distinta cobertura de identificadores de página. Los valores históricos se conservan para trazabilidad, pero no deben compararse como si describieran idéntica población. La diferencia no demuestra una propiedad lingüística nueva por sí sola; obliga a basar análisis futuros en la población corregida y a registrar siempre la versión del parser.
