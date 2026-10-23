# -am: estratos por locus y marcador de párrafo — 23-10-2026

Estado: **REPRODUCED**, limitado a la ejecución descriptiva, fixtures y snapshot de este paquete. Selección retrospectiva. No constituye prueba confirmatoria, reproducción de EXP-208 ni traducción. Base: `29b86941250e75be46eb62ac9d6efb5032563da0`.

## Resultado principal

El exceso de -am al final de línea **no queda limitado a las líneas que llevan un marcador explícito de fin de párrafo**. Bajo las ocho vistas candidatas fijadas, persiste en P0 sin ese marcador. Ausencia de `<$>` no demuestra que una línea sea interior de un párrafo: aquí no se reconstruyen párrafos ni se infieren cierres al cambiar de página.

Se usan exactamente los registros comunes de los nueve lectores del puente anterior, con `$L=B`. Se comprueba por fuente el hash de IDs y la igualdad de todas las métricas agregadas antes de descomponerlas. Los cuatro estratos forman una partición exhaustiva; sus observados y esperanzas reconstruyen los totales. La esperanza es E=sum(k_i/n_i), manteniendo longitud e inventario por línea. O/E tiene ese denominador específico, distinto de las cifras históricas contra tasa agrupada.

## P0, vista por defecto split/primary/expand

| Edición | Marcador final explícito | Líneas | -am/final observado | Esperanza por línea | O/E |
|---|---|---:|---:|---:|---:|
| ZL3b | Sí | 443 | 30 | 6,61677 | 4,53393 |
| ZL3b | No | 1.883 | 325 | 38,48430 | 8,44500 |
| ZL3a | Sí | 443 | 30 | 6,61677 | 4,53393 |
| ZL3a | No | 1.883 | 325 | 38,48430 | 8,44500 |
| IT2a | Sí | 458 | 32 | 6,98223 | 4,58307 |
| IT2a | No | 1.867 | 324 | 39,01975 | 8,30349 |

Las tres ediciones corresponden al mismo manuscrito y están relacionadas; no representan tres muestras independientes. La igualdad de las dos ediciones ZL no multiplica la evidencia.

En ZL3b/ZL3a, el porcentaje de líneas P0 con -am final es 6,77% con marcador y 17,26% sin él. Las tasas de tokens -am también difieren (1,40% frente a 2,07%). Por eso la comparación debe conservar sus denominadores y no atribuir toda la diferencia a una sola función lingüística. Las secciones, manos y características de línea no se equiparan entre estratos.

## Sensibilidad completa y retirada de folios

| Edición | O/E P0 con marcador: rango de ocho vistas | O/E P0 sin marcador: rango de ocho vistas |
|---|---:|---:|
| ZL3b | 4,05590–4,53393 | 7,91132–8,44500 |
| ZL3a | 4,05590–4,53393 | 7,91132–8,44500 |
| IT2a | 4,58307–4,58307 | 8,30349–8,30349 |

En ZL3b se retira por turno cada uno de los 40 folios numéricos que contribuyen líneas P0 sin marcador, con caras/paneles juntos. Para la vista por defecto, el rango resultante es **8,29273–8,58374**. Considerando todas las ocho vistas y las 40 retiradas, el rango conjunto es **7,77667–8,58374**. No son intervalos de confianza ni una distribución nula. Ninguna retirada ensayada elimina el exceso descriptivo.

No se han optimizado umbrales, semillas o vistas. Las ocho combinaciones son las previamente fijadas; la retirada es exhaustiva, determinista y sin aleatoriedad.

## Qué se separa del agregado anterior

ZL3b/ZL3a tienen 2.326 líneas P0 comunes, además de P1=48, Pb=76, Pc=8, Pr=7 y Pt=1. IT2a tiene 2.325 líneas P0 y P1=48, Pb=75, Pc=8, Pr=7, Pt=1. Estos otros locus permanecen archivados en estratos separados y no se presentan como P0.

En ZL3b, los otros locus P aportan 31 líneas con marcador (O=4, E=1,025) y 109 sin él (O=17, E=2,74098), bajo la vista por defecto. Así se reconstruyen exactamente los 376 finales -am del puente anterior: 30+325+4+17. La suma de esperanzas recupera también 48,86706.

El lector histórico literal produce **cero** finales -am en el estrato con marcador: un token como `xam<$>` no termina literalmente en `am`. La vista candidata interpreta el marcador y recupera los extremos. Este cero depende de la implementación; no expresa ausencia de -am en el manuscrito. No debe extrapolarse a EXP-208, cuyo código elimina etiquetas y ensambla párrafos con otro procedimiento.

## Relación con antecedentes y alcance

Se inspeccionó `experiments/exp_208_b_para_model_daiin_hub_am_pf/script.py` como antecedente metodológico. Clasifica por frecuencia de sufijos y reconstruye párrafos mediante inicios de locus; sus filtros de palabras y tratamiento de líneas difieren. Este paquete no ejecuta ese experimento ni recalcula sus cifras. Tampoco modifica C005, C006 u otros compromisos públicos. La interpretación histórica que habla de WP/PF no se traslada automáticamente a estos estratos por presencia de marcador.

El resultado limita una explicación basada exclusivamente en las líneas con marcador explícito. Siguen abiertas explicaciones lingüísticas, de formato, métricas, abreviación y producción artificial. No se identifica una palabra, terminación gramatical o traducción concreta.

## Reproducción y trazabilidad

Python 3.12.14 y bibliotecas estándar. Fuentes y hashes se conservan en `results.json`, junto con los inventarios por locus/estrato, IDs, los nueve lectores y las 40 retiradas. Los archivos originales y snapshots anteriores permanecen intactos.

```sh
python tests/test_exp173_paragraph_strata.py
python scripts/audit_exp173_paragraph_strata.py --check research/maintenance/2026-10-23-paragraph-strata/results.json
```

Cinco pruebas pasadas: partición de fixture con recuentos 0/1 según lector, ausencia de marcador sin inferencia de párrafo, rechazo de marcador anidado, rechazo de payload irresuelto y conservación de líneas unitarias. El snapshot se reproduce íntegramente. `checksums.json` fija los artefactos; las dependencias y transcripciones llevan SHA-256 en la salida.

La CI del bloque anterior terminó correctamente: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39912073278 . Se añade este control a CI; el resultado del nuevo commit debe comprobarse separadamente.

## Autoauditoría — skills/audit_experiment.md

**Target-awareness:** -am fue seleccionado históricamente; la separación por marcador se definió antes de ejecutar esta auditoría, después de conocer los cambios del puente. Es sensibilidad retrospectiva, no confirmación independiente.

**Implementación:** las anotaciones causan falsos negativos literales en el lector histórico. Se muestran ambos lectores y la rejilla completa. Ausencia de marcador no se convierte en interior de párrafo. Las vistas con exclusión de alternativas pueden desplazar extremos; no se interpretan como desaparición del rasgo manuscrito.

**Extrapolación:** solo `$L=B`, locus P y los estratos declarados. Se publican P0 y otros P separados. No se afirma conformidad IVTFF completa, función semántica o exclusión de una familia de mecanismos.

**Alcance negativo:** ninguna teoría de lengua/cifrado/generación se descarta. El resultado solo muestra que el exceso no está limitado a las líneas portadoras de marcador explícito en la población examinada.

**Controles:** para la fixture `y.xam<$>` se esperan y observan 0/1 finales -am bajo histórico/candidato; sin marcador se esperan y observan 1/1. Las sumas por estrato deben igualar totales e igualan observados y esperanzas en las tres fuentes y nueve vistas. La pérdida histórica de extremos marcados queda explicada por el filtro literal; no se presenta como señal lingüística.

Siguiente categoría de trabajo: estudiar la relación entre contexto léxico y posición con controles que conserven estructura de línea/folio. Antes de ejecutar otra prueba, revisar las ya existentes para evitar repetir la batería de bigramas o confundir sus patrones con significados.
