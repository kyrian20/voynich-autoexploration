# Inicio de una vía de desciframiento verificable — 22 octubre 2026

## Resultado del bloque

Se ha completado una comprobación estructural pendiente y preparado un primer paquete de posibles anclas textuales. No se ha recuperado texto plano ni establecido una equivalencia entre signos y sonidos o significados.

La pregunta ejecutada es distinta de volver a probar genéricamente si hay orden: ¿la ventaja del modelo EXP-607 se conserva cuando tanto entrenamiento como evaluación excluyen etiquetas, círculos y otros loci, y qué ocurre con distintas semillas de control?

El [protocolo](maintenance/2026-10-22-exp607-scope/PROTOCOL.md) se fijó antes de puntuar. Se conservaron las reglas del modelo, los lectores y la partición histórica. Este seguimiento usa datos ya observados: es exploratorio, no una nueva confirmación con datos intactos.

## Qué se ejecutó

- Modelo original: mezcla unigram/bigram 50/50, suavizado 0,1.
- Partición original por SHA-256 del folio, módulo cinco; ningún folio aparece a la vez en entrenamiento y test.
- Universo original de páginas básicas y registros físicos elegibles en ambos lectores.
- Dos alcances de entrenamiento por seis de test, en dos lectores y dos transcripciones: 48 comparaciones, todas conservadas.
- Diagnóstico principal P0→P0 con las 64 semillas prefijadas por cada lector/transcripción: 256 puntuaciones de control.
- Reproducción obligatoria del snapshot mixto anterior antes de analizar los nuevos alcances.
- Seis pruebas de implementación: selección, partición, conservación del multiconjunto, ausencia de mutación, equivalencia con el control nativo, semillas/cuantil y alcances vacíos.

P0 es el código de locus usado por este diagnóstico; no debe equipararse a todo el texto continuo del manuscrito. Otros códigos P* quedan fuera de esta condición.

## Resultados de párrafos P0

En cada transcripción se usan 2.959 registros de entrenamiento de 146 folios y 581 de evaluación de 30 folios. Los lectores comparten los IDs físicos; pueden diferir en los tokens y transiciones resultantes.

Las ganancias se expresan en bits por transición frente al unigram propio de cada condición. La diferencia real–control se calcula dentro de cada lector.

| Transcripción / lector | Transiciones de test | Ganancia real | Media de 64 controles | Máximo de controles | Real − media | Controles ≥ real |
|---|---:|---:|---:|---:|---:|---:|
| ZL3b / nativo | 4.481 | 0,253544 | 0,198424 | 0,206569 | 0,055120 | 0/64 |
| ZL3b / candidata conservadora | 4.433 | 0,282972 | 0,229774 | 0,237082 | 0,053198 | 0/64 |
| IT2a / nativo | 4.471 | 0,324023 | 0,268860 | 0,274819 | 0,055163 | 0/64 |
| IT2a / candidata conservadora | 4.457 | 0,321675 | 0,266345 | 0,273520 | 0,055330 | 0/64 |

**Interpretación limitada:** en este modelo, muestra y partición, la ventaja del orden real persiste al excluir los loci no-P0 y supera los controles de entrenamiento barajado ensayados. El diagnóstico no necesita etiquetas incluidas en entrenamiento o test para producir ese resultado. No demuestra lenguaje natural, un cifrado concreto, sintaxis, fonética ni semántica.

La mejora del control también es positiva y grande: gran parte de la ganancia frente al unigram se conserva sin el orden auténtico de entrenamiento. El incremento atribuible a esa comparación es de aproximadamente 0,053–0,055 bits por transición, no toda la ganancia de 0,25–0,32. No convertir 0/64 en un p-valor confirmatorio ni el cuantil de controles en un intervalo de confianza.

## Resultados que limitan la generalización

El test mixto solo contiene 16 registros no-P0 por transcripción. La submuestra L* contiene cuatro registros y cinco transiciones: además de excluir páginas subdivididas, el criterio del modelo requiere al menos dos tokens. No representa la mayoría de las etiquetas de una sola palabra.

En las cuatro condiciones con entrenamiento mixto, el orden real pierde frente al control fijo al evaluar esos 16 registros no-P0. Con entrenamiento P0, la diferencia no-P0 es negativa en ZL3b y pequeña positiva en IT2a. Las etiquetas pierden frente al control fijo en los cuatro perfiles de lectores/transcripciones y en ambos alcances de entrenamiento.

Estos resultados se conservan en la matriz completa; no se selecciona solo el resultado favorable. Se mantiene una bandera de control para estos alcances secundarios. El tamaño, selección y cambio de dominio impiden interpretarlos como ausencia de estructura en etiquetas o como evidencia a favor de una lectura. La causa específica de cada pérdida secundaria no queda identificada por esta prueba.

## Primer paquete para buscar equivalencias textuales

El [paquete de candidatos](decipherment/2026-10-22-anchor-candidates.json) recoge **todos** los loci marcados Lp en al menos una de las dos transcripciones, con hashes de fuente, texto original y dos políticas de espacio incierto. La selección es descriptiva y posterior a conocer los corpus; no es un conjunto de validación ciego.

| Locus | ZL3b original | IT2a original | Consecuencia |
|---|---|---|---|
| f2r.14 | ytoail | Sin registro Lp en el inventario | Comprobar ubicación y clasificación en la imagen y ambas transcripciones; no inferir ausencia de texto. |
| f41v.1 | keer[e:o]dal | keerodal | Preservar la alternativa e/o: no elegir una letra para que encaje un nombre. |
| f65r.1 | otaim,dam.alam | otaim.dam.alam | La separación incierta cambia el número de palabras bajo la política de unión. |

Las cadenas son transliteraciones, no traducciones. Lp es un punto de partida documental; no certifica que el texto sea el nombre del objeto ilustrado. No se han identificado visualmente las plantas en este bloque.

Los campos de lectura, identidad y texto plano están vacíos deliberadamente porque aún no hay evidencia que los sostenga. Esto evita transformar una conjetura botánica en una clave de desciframiento.

## Condiciones para la primera lectura candidata

La vía inmediata es intentar obtener un ancla imagen–texto–nombre mediante documentación externa, vinculada a un locus exacto. Antes de ajustar cualquier clave:

1. Verificar el signo y la ubicación sobre imagen del manuscrito, conservando variantes y lecturas inciertas.
2. Obtener identificaciones y nombres históricos con procedencia independiente de la cadena EVA. Una semejanza visual propuesta por un modelo no constituye identificación validada.
3. Comparar varias candidatas y explicaciones alternativas; contemplar que el rótulo no sea un nombre de planta.
4. Congelar una correspondencia explícita y todas sus excepciones. Reservar otros loci antes de usar sus posibles equivalencias; el corpus ya observado debe declararse como tal.
5. Evaluar predicciones nuevas, consistencia entre ocurrencias, alternativas rivales y controles de nombres ajenos. No introducir un sonido o regla nueva por cada palabra.
6. Rechazar la propuesta si solo funciona en los ejemplos usados para construirla o si exige resolver la transcripción a conveniencia.

Ninguna regla de estos puntos se presenta como cumplida todavía. La evidencia estructural obtenida ayuda a evaluar futuras propuestas, pero no permite deducir una clave única.

## Autoauditoría del diagnóstico

**Conciencia del objetivo:** el modelo y las reglas proceden de EXP-607; la división ya ha sido observada y la pregunta P0 surge de una auditoría previa. El efecto es condicional a esa elección, elegibilidad y modelo. No se buscaron hiperparámetros ni semillas favorables.

**Implementación que destruye características:** el control destruye intencionadamente el orden dentro de cada locus de entrenamiento y conserva longitudes, tokens y folios; el test mantiene su orden. La candidata ASCII excluye tokens completos no elegibles y modifica el estimando, por lo que no se comparan pérdidas absolutas entre lectores como si fueran idénticas. La selección de páginas y registros limita el alcance.

**Extrapolación:** las conclusiones solo cubren P0 en el universo y partición indicados, con dos lectores y 64 semillas. No excluyen familias de generadores ni establecen una lengua. Los 48 cruces no son 48 réplicas independientes.

**Alcance negativo:** el mal comportamiento secundario no prueba que las etiquetas carezcan de estructura. Los loci L* evaluados tienen solo cinco transiciones por transcripción y no son una muestra representativa.

**Controles:** se esperaba que el entrenamiento barajado retuviera ventaja positiva por los inventarios y el suavizado, como ya ocurría en el snapshot mixto. No se había fijado una media numérica P0, y no se inventa una predicción retrospectiva. Se observaron medias 0,198424/0,229774 en ZL3b y 0,268860/0,266345 en IT2a. Ningún control P0 alcanzó al real. Las pérdidas en los alcances secundarios se mantienen señaladas y sin interpretación lingüística hasta investigarlas.

Esta autoauditoría no sustituye una revisión independiente.

## Reproducción y archivos

- Script: scripts/audit_exp607_scope_sensitivity.py.
- Pruebas: tests/test_exp607_scope_sensitivity.py.
- Resultados completos y semillas: research/maintenance/2026-10-22-exp607-scope/results.json.
- Generador del paquete de anclas: scripts/prepare_decipherment_anchor_packet.py.
- El generador y el diagnóstico solo escriben a stdout; no sobrescriben resultados históricos.
- CI reproduce y compara ambos JSON con estructura y conteos exactos y tolerancia de 1e-12 para flotantes finitos.
- No se asigna un nuevo ID EXP ni se modifican committed_claims.md, findings.md o failed_approaches.md.

