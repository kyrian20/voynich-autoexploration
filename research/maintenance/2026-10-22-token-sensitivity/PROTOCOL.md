# Auditoría factorial de tokenización — protocolo descriptivo v1

Se fija este protocolo antes de ejecutar la nueva comparación factorial. No es una preinscripción confirmatoria: daiin y los contrastes posicionales se escogieron históricamente y ya se conocen diferencias globales del lector.

## Universo y controles

- Usar los mismos registros brutos de ZL3b, ZL3a e IT2a y sus hashes; no introducir fuentes nuevas.
- Evaluar exhaustivamente 128 combinaciones de siete cambios binarios: ligaduras, alternativas, códigos extendidos, ilegibles, whitespace, anotaciones inline y caracteres no alfabéticos.
- Máscara 0 debe reproducir exactamente el filtro ASCII de EXP-590 sobre cada payload. Máscara 127 debe reproducir exactamente la vista candidata ya existente, en cada registro. Abortar si falla cualquiera de los dos controles.
- Las comas separan palabras en esta rejilla. La alternativa de unir comas se evaluará aparte, sin confundirla con los siete cambios anteriores.
- Ningún resultado histórico se modifica. No hay nuevos p-valores ni búsquedas de una política favorable.

## Medidas

Recuentos exactos, inicios/finales de daiin y expectativa inicial bajo intercambiabilidad uniforme dentro de cada línea (suma m/n). Informar enriquecimiento observado/esperado únicamente como medida descriptiva.

Por cada combinación medir tanto sus propios registros P0 de Currier A/B con al menos dos tokens como la intersección de registros que cumplen el filtro bajo las 128 políticas. Esta última comparación mantiene constante el universo; informar tamaños y hashes de IDs.

Descomponer la diferencia global de recuentos mediante valores de Shapley exactos sobre las 128 combinaciones. Es una identidad de atribución dependiente de esta rejilla, no una causa lingüística ni una probabilidad.

Conservar registros que cambian el conteo o los indicadores de posición del objetivo, con el cuerpo original y las proyecciones de ambos extremos. Comparar por separado el parser nativo de EXP-601 con la candidata, sin llamarlo equivalente al filtro de EXP-590.

## Criterios de lectura

- Un rango que conserve el signo del exceso es robustez descriptiva dentro de la rejilla, no validación confirmatoria.
- Un cambio de signo o de elegibilidad debe registrarse sin elegir la variante favorable.
- Las transcripciones no son muestras independientes. La rejilla no cubre todas las decisiones posibles del formato.
- Aplicar los cinco controles de skills/audit_experiment.md antes de actualizar cualquier síntesis.

## Seguimiento acotado de EXP-607 — definido antes de ejecutarlo

Reutilizar sin modificar el modelo nativo, alpha=0,1, mezcla=0,5, split SHA-256 por folio y semilla de control originales. Primero reproducir su resumen guardado. Después comparar su tokenización con la candidata conservadora: solo palabras completas que cumplan `[a-z]{2,}` después de la proyección, sin extraer fragmentos de palabras con ilegibles/códigos extendidos.

Mantener el universo original de páginas e intersectar por ID las líneas con al menos dos tokens bajo ambos lectores. No ampliar páginas, no cambiar split, ni ajustar parámetros con el test. Informar exclusiones y comprobar disyunción de folios. Ejecutar el control original de entrenamiento barajado con su misma semilla; no hacer una búsqueda de semillas.

Las pérdidas entre tokenizadores no tienen exactamente los mismos eventos ni vocabulario. Comparar el signo de la ventaja real frente al control dentro de cada vista, sin tratar la diferencia entre vistas como un estimador causal ni una nueva prueba confirmatoria. Un único barajado es un diagnóstico, no una distribución nula completa. Si cambia de signo, registrar el desacuerdo sin seleccionar una vista favorable.

## Remuestreo pareado necesario para el cambio de lector en EXP-601

Como la expectativa por línea cambia, no trasladar el intervalo antiguo al estimador nuevo. Para ZL3b solamente, usar las mismas líneas comunes B/P0 y remuestrear los mismos folios en ambos lectores, con 20.000 réplicas, semilla original 60120261019 y cuantiles originales. Primero exigir que el bootstrap nativo reproduzca el intervalo histórico guardado. Informar ambos intervalos y el intervalo de su diferencia pareada. No recalcular p-valores ni llamarlo nueva confirmación: es sensibilidad de un análisis ya observado.
