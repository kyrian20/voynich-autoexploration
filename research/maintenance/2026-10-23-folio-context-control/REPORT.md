# Control alternativo de contexto por folio — 23-10-2026

Estado: **REPRODUCED**, para soporte del control y snapshot. Diseño retrospectivo después de conocer el control limitado por línea. No se ejecuta todavía una prueba de asociación ni se declara potencia suficiente.

## Resultado y cambio de pregunta

Se ha implementado un control con mayor soporte: intercambiar identidades de tokens interiores entre posiciones de iguales bordes y longitud dentro de un mismo folio físico. Se conservan los extremos de cada línea, la plantilla de bordes/longitudes de sus posiciones y el inventario total del folio. **No se conserva el inventario de cada línea.** Por eso este control es una alternativa con otros supuestos, no una reparación equivalente del nulo anterior.

En la vista por defecto de ZL3b permite cambiar el predecesor de **196 de 325 cierres -am**, frente a los 16 del control por línea. La esperanza del número de predecesores cambiados es **111,22193**, frente a 8. Las líneas variables abarcan 38 folios físicos. Esto ofrece un universo más amplio para diseñar un contraste futuro, pero no demuestra asociación léxica ni explica el significado del cierre.

| Fuente, vista split/primary/expand | Cierres -am | Predecesores variables | Esperanza de cambios | Folios con variación | Otros cierres: variables/total |
|---|---:|---:|---:|---:|---:|
| ZL3b | 325 | 196 | 111,22193 | 38 | 968/1.558 |
| ZL3a | 325 | 196 | 111,22193 | 38 | 967/1.558 |
| IT2a | 324 | 191 | 110,47426 | 35 | 967/1.543 |

En las ocho políticas ZL hay 188–199 cierres -am con predecesor variable y esperanza 106,43471–115,43828. IT2a conserva 191 y 110,47426 en las ocho vistas. No son intervalos de confianza. Las transcripciones relacionadas no representan muestras independientes.

## Qué está listo para usar

El script construye grupos por número de folio físico × primer carácter × último carácter × longitud de token. Caras y paneles del mismo folio se mantienen juntos. Solo participan posiciones interiores de las líneas seleccionadas. Para cada penúltima posición, la probabilidad exacta de cambio es 1-c/k, con repeticiones de candidatos conservadas. Se publican IDs variables, probabilidades racionales, folios y las 24 vistas completas.

Antes de calcular se exigen mismos hashes de corpus, IDs y métricas del paquete de estratos. Se rechazan identificadores cuya agrupación física no se puede resolver, filas duplicadas y tokens vacíos. Los originales no se modifican.

Seis pruebas pasan: enumeración completa de una fixture multilínea con candidatos repetidos, conservación de inventario global y extremos/plantilla por línea, aislamiento entre folios, aislamiento entre firmas, agrupación de caras/paneles, casos degenerados y entradas inválidas. La enumeración da las mismas esperanzas racionales que la fórmula. La salida completa se regeneró y coincide con el snapshot comprimido.

```
python tests/test_folio_context_control.py
python scripts/audit_folio_context_control.py --check research/maintenance/2026-10-23-folio-context-control/results.json.gz
```

## Límites y decisión

Queda resuelto el problema de no disponer de una alternativa ejecutable con más intercambios bajo bordes/longitud conservados. No se ha probado que este nuevo nulo sea un modelo correcto del manuscrito ni que detecte cualquier efecto. Se mantiene el control por línea como referencia, sin cambiar su resultado de 16 líneas variables.

El intercambio entre líneas puede destruir coherencia temática, relaciones con dibujos, relaciones entre posiciones o estructura de párrafo. Por eso una comparación futura evaluará intercambiabilidad entre líneas del mismo folio condicionada a la plantilla, una pregunta diferente a la del control que conservaba cada inventario de línea. No se ha seleccionado una pareja ni afinado un umbral para obtener significación. Antes de ejecutar una asociación, se debe fijar su estadístico, usar el control apropiado y calibrar sensibilidad con un efecto conocido. No se atribuyen todavía significado, gramática o lengua.

## Autoauditoría — skills/audit_experiment.md

**Target-awareness:** el diseño surge después de observar el soporte insuficientemente amplio del control por línea y usa el sufijo conocido. El incremento de soporte es condicional a relajar ese inventario; no es evidencia confirmatoria de dependencia.

**Implementación:** se conserva inventario de folio y firma por posición, pero puede destruir coherencia de línea. Esa pérdida se declara junto al resultado y evita presentar ambos controles como equivalentes. No se usa para descartar toda hipótesis lingüística.

**Extrapolación:** solo los folios, líneas y ocho vistas indicados; oportunidad de intercambio no equivale a potencia estadística suficiente. No se hace una afirmación sobre todas las palabras o dependencias.

**Alcance negativo:** ningún resultado negativo de asociación se calcula ni se atribuye a una clase de mecanismos.

**Controles:** se espera una probabilidad 1-c/k porque cada token del grupo ocupa cada posición con igual probabilidad bajo permutación uniforme. La enumeración multilínea produce igualdad racional exacta; los controles de folios y firmas distintas producen cero cambios, como se espera. El aumento de soporte frente al control por línea se debe a candidatos nuevos de otras líneas: no se interpreta como aumento de evidencia lingüística.

La verificación automática previa ya está resuelta: [consulta correcta y evidencia](../../CI_VERIFICATION.md). La reproducción del presente bloque se incorpora a CI; su commit requiere comprobación separada. No se alteran afirmaciones comprometidas ni hallazgos históricos.
