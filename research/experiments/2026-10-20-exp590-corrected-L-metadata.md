# EXP-590 — Posición inicial de daiin

- Fecha UTC: 2026-10-20
- Fuente: data/transcriptions/eva_zl3b.txt
- SHA-256 de la transcripción: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc
- Líneas EVA parseadas: 4,188
- Tokens parseados: 32,732
- Ocurrencias exactas de daiin: 726
- Ocurrencias en primera posición de línea: 133
- Ocurrencias en última posición de línea: 118
- Fracción de ocurrencias en primera posición: 0.1832
- Fracción de ocurrencias en última posición: 0.1625

## Contraste de permutación

- Permutaciones: 5,000
- Semilla fija: 20261020
- Media nula de líneas que empiezan por daiin: 94.628
- Desviación típica nula: 8.625
- p empírico unilateral con corrección +1: 0.000200

La hipótesis nula permuta el orden de los tokens dentro de cada línea, conservando su multiconjunto exacto. El contraste evalúa si daiin aparece al principio de línea más de lo esperable bajo ese modelo; no prueba significado lingüístico. No se han explorado múltiples palabras en este experimento, pero cualquier búsqueda posterior deberá corregir comparaciones múltiples.

## Distribución por clase de Currier

| Clase | Ocurrencias exactas | Líneas iniciales | Líneas finales | Líneas parseadas |
|---|---:|---:|---:|---:|
| A | 440 | 50 | 97 | 1567 |
| B | 278 | 80 | 21 | 2418 |
| unknown | 8 | 3 | 0 | 203 |

## Limitaciones y reproducibilidad

- Solo se cuenta el token exacto daiin; no se mezclan variantes como dain.
- La tokenización elimina etiquetas IVTFF y material entre llaves/corchetes; los resultados dependen de esa decisión.
- La clasificación Currier se lee de cabeceras de folio cuando está disponible; los casos sin clasificación quedan como unknown.
- Esto es una línea base exploratoria reproducible, no una traducción ni una afirmación de desciframiento.
- Datos completos y hash de entrada están en el JSON de este experimento.
