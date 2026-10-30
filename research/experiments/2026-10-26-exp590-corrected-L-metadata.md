# EXP-590 — Posición inicial de daiin

- Fecha UTC: 2026-10-26
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

**Precaución inferencial:** el valor p no corrige la selección histórica de daiin entre otras palabras ni otros análisis de esta transcripción. Es un contraste exploratorio bajo el nulo elegido, no una prueba confirmatoria independiente.

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

## Cobertura histórica y actual

| Métrica | Patrón restringido histórico | Patrón actual |
|---|---:|---:|
| Líneas con tokens | 4188 | 5376 |
| Tokens | 32732 | 39594 |
| daiin exactos | 726 | 853 |
| Inicios daiin | 133 | 161 |

Las columnas usan distinta cobertura de identificadores; no describen idéntica población. El filtro ASCII no decodifica los códigos de caracteres extendidos @…;. Se conserva la transcripción bruta. Véase la auditoría operativa para el cotejo exacto de registros excluidos.
