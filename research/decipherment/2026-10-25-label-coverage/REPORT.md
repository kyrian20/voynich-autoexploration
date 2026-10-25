# Cobertura por hoja física y tipo de locus — 25-10-2026

Estado: **REPRODUCED**, limitado al diagnóstico descriptivo de estos metadatos y fuentes. Evaluación semántica **BLOCKED** por falta de referentes anotados y de una muestra adecuada para el subconjunto Lp. No es un nuevo EXP ni una prueba de ausencia de significado.

## Pregunta y fuentes

Se cruzó el inventario de PR #47 con la partición v2 ya existente, sin cambiarla ni evaluar palabras, nombres, resultados semánticos o modelos. El protocolo reconoce dos recuentos preliminares ya conocidos: Lp solo en train y acuerdo de tipo de locus en los IDs compartidos. Por tanto no se presenta como hipótesis confirmatoria ciega.

SHA256 de los archivos de entrada en coverage.json; SHA256 de script, tests, protocolo y salida en SHA256.json. Se exige coincidencia de los hashes de las fuentes de cada registro y del manifiesto. Recto, verso y paneles se agrupan mediante el número de hoja; fRos permanece sin asignación numérica.

## Resultados

| Edición | Partición | Registros L/R | Hojas numéricas distintas |
| --- | --- | ---: | ---: |
| ZL3b | train | 512 | 21 |
| ZL3b | development | 237 | 5 |
| ZL3b | test | 285 | 5 |
| ZL3b | UNASSIGNED (fRos) | 137 | 0 |
| IT2a | train | 504 | 18 |
| IT2a | development | 237 | 5 |
| IT2a | test | 284 | 4 |

No sumar hojas de ambas ediciones como muestras independientes. La unión de hojas numéricas con registros seleccionados es 31 en ZL3b y 27 en IT2a; son subconjuntos de las 102 hojas del manifiesto, no su cobertura completa. Las 137 filas de fRos no desaparecen: figuran en una categoría sin asignación, que no significa ausencia de página o de texto.

Los 1.024 IDs presentes en la selección de ambas ediciones coinciden en subtipo de locus; este acuerdo no prueba alineamiento con un mismo objeto visual. Hay 147 IDs seleccionados solo en ZL3b y uno solo en IT2a. Ninguno de esos 148 IDs aparece en la lista de otros registros parseados de la edición opuesta. Es una diferencia del inventario textual, no demostración de texto ausente en el manuscrito ni de una lectura correcta.

### El subconjunto Lp no ofrece evaluación reservada

ZL3b aporta tres Lp en tres hojas de entrenamiento (f2r/f41v/f65r); IT2a aporta dos en dos hojas de entrenamiento (f41v/f65r). **Cero Lp en desarrollo y cero en prueba en ambas ediciones.** No hay base para entrenar sobre estas mismas etiquetas y declarar una predicción nueva fuera de entrenamiento bajo esta partición. No moverlas a test después de haberlas examinado.

### La muestra de prueba amplia está concentrada

| Hoja | ZL3b test | IT2a test |
| --- | ---: | ---: |
| 72 | 164 | 164 |
| 70 | 60 | 60 |
| 66 | 50 | 50 |
| 80 | 10 | 10 |
| 11 | 1 | 0 |

Los cientos de registros no son cientos de hojas independientes. Incluso antes de adjudicar imágenes, IT2a tiene solo cuatro hojas de prueba con cualquier código L/R. Un umbral de cinco hojas como el propuesto en PR #13 no se satisface en IT2a para esta selección; no se relaja para acomodar estos datos. Esto no adopta ese umbral como cálculo de potencia ni convierte las cinco hojas de ZL3b en suficientes: ninguna tiene aquí referentes externos verificados.

Los subtipos de test son L0, Ln, Lx, Lz y Ri. **No son categorías botánicas independientes.** Q002 de state/open_questions.md ya advertía de funciones mezcladas en L0; aquí se preserva esa cautela sin revalidar porcentajes históricos ni resolver su anotación visual.

## Reproducción, pruebas y omisiones

```sh
python scripts/audit_label_partition_coverage.py --out research/decipherment/2026-10-25-label-coverage/coverage.json
python -m unittest discover -s tests -p test_label_partition_coverage.py -v
python -m unittest discover -s tests -v
```

Python 3.12.14; cinco pruebas nuevas aprobadas: agrupación de paneles/caras y celdas vacías, particiones solapadas/hojas desconocidas/hashes incompatibles, duplicados y fRos, contraparte fuera de selección frente a ausencia, y desacuerdo de subtipo preservado. La suite local termina con 263 tests OK, skipped=1 por datos crudos históricos ausentes. Incluye los cambios locales del paquete visual de PR #48; no es ejecución de los 624 experimentos ni certificación de un master concurrente. Segunda generación de coverage.json idéntica byte a byte. No se modifican fuentes, partición, committed_claims, hallazgos ni backlog científico.

## Autoauditoría según skills/audit_experiment.md

**Target-awareness:** selección L/R y partición preexistente, sin calibrar sobre una asociación semántica. Dos recuentos preliminares ya vistos se revelan en el protocolo. No hay hipótesis nueva sometida a test.

**Feature-destroying implementation:** se inspeccionan metadatos; no se normalizan palabras ni se descarta fRos. L/R mezcla funciones y por eso los recuentos no sustituyen una muestra de objetos identificados. La selección heredada puede omitir rótulos con otros códigos; no se generaliza al manuscrito completo.

**Extrapolation:** los números se restringen a las dos fuentes, a esta selección y a la partición existente. El acuerdo de IDs/tipos no es una réplica visual independiente ni una prueba de conformidad IVTFF.

**Negative-result scope:** cero Lp reservadas limita este diseño; no refuta la existencia de lenguaje, nombres propios, correspondencias o significado. La falta de cinco hojas IT2a no prueba imposibilidad con otras selecciones legítimamente definidas para investigación futura.

**Control behavior:** no hay comparación inferencial con nulo. Espero que caras/paneles de f1 compartan una sola hoja en el fixture porque su número físico es el mismo; el control produjo dos registros y una hoja. Espero que una partición solapada falle; el fixture fue rechazado. Estos controles verifican contabilidad, no semántica ni potencia.

## Decisión y siguiente bloque

Mantener Lp como exploración y material de entrenamiento. Para cualquier futura evaluación de etiquetas, anotar primero funciones/objetos de las hojas existentes sin usar EVA, agrupar ilustraciones compartidas y medir cobertura y acuerdo. No elegir el tipo de locus según una ventaja predictiva observada en test, ni fabricar nuevos holdouts sobre páginas ya vistas. Si se diseña una selección nueva, declarar su exposición histórica y congelar sus reglas antes de evaluar. La anotación y el diseño muestral preceden al entrenamiento.
