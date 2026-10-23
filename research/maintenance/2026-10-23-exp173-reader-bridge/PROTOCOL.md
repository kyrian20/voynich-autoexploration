# Puente de lectores para F3/F6 — protocolo descriptivo

Fecha: 23-10-2026. Base: 29677e387d9c44983a28d61baad2f14e55a42c8e. Se escribe antes de ejecutar. Selección retrospectiva de F3/F6; no nueva prueba confirmatoria ni nuevo EXP.

## Alcance fijado

1. Reproducir el snapshot ZL3b del cruce histórico y el cálculo por línea del bloque anterior.
2. Usar los registros identificados del lector común `read_records` y la capa `ivtff_lossless`. Esta capa es la proyección candidata existente, no un certificado de conformidad IVTFF completa. Abortar ante diagnósticos, continuaciones no ensambladas, duplicados o desacuerdo al reconstruir la población histórica.
3. Analizar ZL3b, ZL3a e IT2a como ediciones relacionadas del mismo manuscrito. Fijar sus hashes en la salida. Seleccionar $L=B explícito y locus que empiece por P, igual que el alcance histórico. Sin mínimo adicional de longitud.
4. Reconstruir los tokens históricos por puntos y filtro inicial ASCII exactamente, comprobando secuencia completa frente a `read_legacy_population` para cada fuente. No cambiar clasificación y lector simultáneamente.
5. Ocho vistas candidatas: comas split/join × alternativas primary/exclude_word × ligaduras expand/opaque. Es la rejilla completa de tres opciones ya existentes; no escoger la vista favorable. Mantener códigos opacos e ilegibles dentro de tokens, sin extraer fragmentos ASCII. La coincidencia de -am/inicio y es literal; una ligadura opaca final no se decodifica.
6. Medir O, E=sum(k_i/n_i), O/E y también el cociente agrupado histórico. Informar población propia y población común a los nueve lectores, incluidos el histórico y las ocho vistas. Conservar IDs de exclusiones y filas con cambios en tokens/rasgos de extremos, junto al texto bruto.
7. Para ZL3b, en la intersección, comparar histórico con candidata por defecto (split/primary/expand): eliminar por turno cada folio numérico completo y publicar rango de O/E y de la diferencia pareada. Es sensibilidad determinista, no intervalo de confianza ni p-valor. Las caras y paneles del mismo número salen conjuntamente.

## Controles y límites

Fixtures para marcadores de fin de párrafo, alternativas que cambian el primer token, comas que cambian extremos, ligaduras, códigos opacos y exclusiones de líneas. Los snapshots históricos deben coincidir antes de interpretar la nueva salida. Publicar todas las diferencias; conservar originales. No reinterpretar compromisos C005/C006, estimar significación ni asignar traducciones. Si los signos difieren entre vistas, registrar el desacuerdo. Completar los cinco controles de `skills/audit_experiment.md` antes del informe.
