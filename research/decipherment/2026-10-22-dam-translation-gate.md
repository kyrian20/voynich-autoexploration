# Puerta de validación para una posible traducción de dam

Fecha: 2026-10-22. Estado: protocolo prospectivo, NO experimento ejecutado, NO traducción.

## Evidencia previa (exploratoria)

Según research/DECIPHERMENT_ANCHOR_REVIEW_2026-10-22.md, dam aparece 88 veces en ZL3b al separar comas, 74 al unirlas y 98 en IT2a bajo ambas políticas. Estos recuentos NO son réplicas independientes; el locus f65r.1 contiene otaim,dam.alam en ZL3b y otaim.dam.alam en IT2a. Ningún significado se ha validado.

## Hipótesis contrastables

H0: dam es una unidad gráfica recurrente sin semántica recuperable con la evidencia disponible.
H1: dam tiene una función gramatical estable y produce distribuciones de vecinos/posiciones similares entre folios, secciones y transcripciones.
H2: dam designa una entidad o procedimiento recurrente; sus contextos deberían concentrarse en loci temáticamente relacionados de forma más marcada que controles emparejados por frecuencia y longitud.
H3: dam es producto de convenciones gráficas, segmentación o familias de patrones; las señales se desvanecen bajo controles que preservan propiedades locales.

Ninguna hipótesis se considera demostrada. H0 no implica que el manuscrito carezca de significado.

## Protocolo para la próxima ejecución (sin resultados anticipados)

1. Congelar hash de ambas transcripciones, reglas exactas de selección y tratamiento de espacios inciertos. Conservar la lectura original y folio/locus por ocurrencia.
2. Reservar folios completos para evaluación sin usar sus contextos para escoger la hipótesis. Separar los folios usados para explorar de los folios de contraste por hash de identificador; documentar antes la partición.
3. Para cada ocurrencia exacta de dam, registrar vecinos izquierdo/derecho, posición relativa en línea, sección, lector y folio; incluir ausencias y alternativas, no solo casos favorables.
4. Construir controles de tokens emparejados por frecuencia, longitud y distribución por sección; comprobar sensibilidad a la segmentación de comas y a las dos transcripciones. No atribuir automáticamente equivalencia de tokens entre fuentes.
5. Contrastar estabilidad de contexto fuera de muestra mediante log-verosimilitud o medida fijada antes del cómputo, con incertidumbre por remuestreo de folios completos (no de tokens independientes).
6. Si se propone una traducción concreta, escribir ANTES de evaluarla una tabla de predicciones de contextos y folios no utilizados, junto con alternativas rivales y criterios explícitos de rechazo. No adaptar reglas fonéticas para cada caso.
7. Publicar también los resultados negativos, código, hashes, semillas y recuentos completos. No añadir EXP ID ni modificar resultados históricos hasta ejecutar una prueba reproducible.

## Criterio de admisión

Solo aceptar una lectura semántica provisional si predice datos reservados mejor que controles y rivales, es consistente con distintas transcripciones y no depende de una identificación botánica circular. Una asociación estadística sin evidencia semántica independiente no equivale a traducción.
