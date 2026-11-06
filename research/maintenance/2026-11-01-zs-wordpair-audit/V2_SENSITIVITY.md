# Sensibilidad de la auditoría de pares de palabras con la regla literal v2

**Fecha:** 2026-11-06  
**Estado:** recálculo acotado completado; no es una reproducción del artículo ni una prueba sobre significado.

## Pregunta

¿Cuánto cambia la reimplementación parcial del 1 de noviembre al sustituir solo su filtro de casi-copias Levenshtein ≤1 por la regla descrita en Zhang y Sheng v2: excluir un par de tipos distintos si al borrar exactamente un glifo EVA de cada palabra se obtiene la misma forma?

## Método y entradas

Se reutilizaron las dos transcripciones, sus hashes SHA-256 y Git del informe anterior, las 225 páginas comunes, categorías P/C/R, exclusiones f116v y fRos, tres vistas de tokenización, tamaños de vocabulario 150/300/600, las mismas tres semillas y 20 barajados por semilla. Se calcularon las 54 combinaciones completas. El script de auditoría de noviembre y su JSON histórico no se modificaron; el cambio se aplica en un runner separado mediante la función aislada `near_copy_v2.py`.

Se conserva la misma fórmula OLS aditiva de propensión, el mismo desempate, el mismo nulo de barajado y las mismas particiones de páginas del cálculo anterior. Las particiones alternas de bloques de diez páginas comparten hojas físicas; por ello sus mitades no constituyen validación independiente por hoja. El artículo no publica la fórmula exacta de propensión ni todos los detalles de inclusión y aleatorización.

## Resultado principal — vocabulario de 300 tipos, vista EVA «split»

| Transcripción | Pares admisibles: v2 / Levenshtein | Correlación residual v2, media (rango de 3 semillas) | Levenshtein, media (rango) |
|---|---:|---:|---:|
| ZL3b | 43.930 / 43.781 | 0,0344 (0,0341–0,0351) | 0,0340 (0,0335–0,0344) |
| IT2a | 43.937 / 43.781 | 0,0462 (0,0433–0,0488) | 0,0460 (0,0429–0,0487) |

En la rejilla completa, la regla v2 admite entre 108 y 173 pares adicionales, según transcripción, vista y tamaño del vocabulario. El cambio de correlación es pequeño en el punto principal; el recálculo no resuelve la discrepancia con los valores comunicados por el artículo.

## Interpretación

El filtro literal v2 queda implementado y aplicado a las entradas fijadas. Con el resto del procedimiento congelado, cambiar solo este filtro no altera sustancialmente las correlaciones de 300 tipos en la vista principal. Esto acota la sensibilidad de nuestra operacionalización, pero **no reproduce la cifra publicada**: siguen sin conocerse la corrección exacta por propensión, reglas completas de selección de líneas y detalles del nulo. ZL3b e IT2a son transcripciones alternativas de un mismo manuscrito, no réplicas independientes.

No se infiere si el Voynich es lenguaje, cifrado o generador, y no se obtiene ninguna lectura semántica. No se asigna ID EXP ni se modifica una afirmación comprometida.

## Reproducción

Desde la raíz del repositorio:

```bash
python research/maintenance/2026-11-01-zs-wordpair-audit/run_v2_sensitivity.py > /tmp/zs-v2-sensitivity.json
```

El resultado completo de 54 ejecuciones está en [`v2_sensitivity_results.json`](v2_sensitivity_results.json). El script comprueba las mismas cerraduras SHA-256/Git mediante el lector de la auditoría histórica. La regla v2 se prueba también en CI dentro de la PR #265, pero la CI del componente no acredita por sí sola estos cálculos sobre el corpus.
