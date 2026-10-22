# Análisis descriptivo por folio de la posición de daiin

- Fecha: 2026-10-22
- Fuente: `data/transcriptions/eva_zl3b.txt`
- SHA-256 de la fuente: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- Líneas con tokens: 5.376
- Folios con texto parseado: 227
- Método: token exacto daiin; se informa tanto el número de ocurrencias como el de líneas que contienen al menos una ocurrencia. La clase Currier procede exclusivamente de IVTFF `$L`.

## Resultados por clase

| Clase | Folios | Folios con daiin | Líneas parseadas | Ocurrencias exactas | Líneas con daiin | Líneas con daiin que empiezan por daiin | Líneas con daiin que terminan por daiin | Proporción de líneas con daiin que empiezan por daiin |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 114 | 109 | 1.815 | 502 | 423 | 60 | 104 | 0,1418 |
| B | 83 | 77 | 2.806 | 314 | 283 | 91 | 27 | 0,3216 |
| unknown | 30 | 20 | 755 | 37 | 34 | 10 | 3 | 0,2941 |

## Comparación con remuestreo por folio

La tasa de cada folio es:

[
r_f = rac{	ext{líneas con daiin que empiezan por daiin}}{	ext{líneas que contienen daiin}}
]

Se calcula la media no ponderada de estas tasas entre folios de A y B que contienen al menos una línea con daiin. Se remuestrean folios completos dentro de cada clase; no se tratan líneas del mismo folio como observaciones independientes.

- Diferencia de medias A − B: **−0,179871**
- Intervalo percentil del 95 %: **[−0,271083; −0,090770]**
- Folios incluidos: A = 109; B = 77
- Réplicas bootstrap: 20.000
- Semilla: 20261022

En esta definición descriptiva, las líneas que contienen daiin comienzan con daiin con menor frecuencia en A que en B. La diferencia no es una traducción, no establece función gramatical y no identifica por sí sola la causa del patrón.

## Interpretación y límites

- El análisis sigue siendo exploratorio; daiin fue seleccionado tras trabajo previo y el intervalo no corrige esa selección histórica.
- La tokenización simplificada elimina etiquetas IVTFF, spans entre llaves y spans entre corchetes. La sensibilidad a convenciones IVTFF debe seguir documentándose.
- ZL3a, ZL3b e IT2a son transcripciones alternativas del mismo manuscrito, no muestras independientes.
- El bootstrap describe incertidumbre entre folios bajo este procedimiento; no valida una hipótesis de desciframiento.
- Este seguimiento no recibe un nuevo ID EXP y no sobrescribe el resultado base de EXP-590.

## Reproducción

Script: [`scripts/exp590_folio_cluster_sensitivity.py`](../../scripts/exp590_folio_cluster_sensitivity.py)  
Prueba de regresión: [`tests/test_exp590_folio_cluster_sensitivity.py`](../../tests/test_exp590_folio_cluster_sensitivity.py)  
El workflow de GitHub Actions ejecuta la prueba y genera un artefacto JSON/Markdown fechado para inspección.

## Control adicional incorporado después del primer análisis

Se añadió al script una referencia de aleatorización condicionada a cada línea: conserva el multiconjunto de tokens de la línea y supone que todas las posiciones son intercambiables. Para una línea con (k) tokens y (m) apariciones exactas de daiin, la probabilidad nula de que la primera posición sea daiin es (m/k); su varianza para el indicador inicial es ((m/k)(1-m/k)). Se suman estas expectativas y varianzas por clase Currier.

Este control no es un modelo realista del lenguaje ni una prueba de desciframiento: solo mide cuánto se aparta la posición inicial observada de un baseline que ignora el orden de los tokens dentro de cada línea. El script y la prueba de regresión se han ampliado para calcularlo. Los valores numéricos generados por esta versión se deben tomar del artefacto de GitHub Actions correspondiente al commit actualizado, no de la tabla anterior de este informe.

