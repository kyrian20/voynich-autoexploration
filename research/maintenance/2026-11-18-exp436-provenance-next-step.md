# Continuación Q022 — protocolo de procedencia antes de replicar EXP-436 (2026-11-18)

## Evidencia comprobada
- `experiments/exp_436_latin_hapax_length/CORRECTION.md` marca las comparaciones externas `INVALID_FOR_CLAIM`.
- `research/CORPUS_IDENTITY_REVIEW.json` identifica `latin/caesar_gallic_wars.txt` como traducción inglesa, `latin/cicero_caesar_latin.txt` como vacío y `latin/cicero_de_officiis_latin.txt` como bilingüe.
- La ruta italiana que busca el script histórico no coincide con la ruta registrada en el manifiesto.
- Ninguno de estos hechos invalida automáticamente los recuentos Voynich A/B; tampoco los reproduce.

## Pregunta falsable
¿Se mantiene la dirección y magnitud del gradiente de hapax por longitud cuando se usan corpus monolingües de latín e italiano con identidad comprobada y exactamente la misma tokenización y selección de unidades que en VMS?

## Puertas obligatorias antes de ejecutar
1. Seleccionar fuentes latinas e italianas monolingües con licencia, edición, idioma, URL de origen y SHA-256 de los bytes fijados. No usar el archivo bilingüe sin separar y auditar ambos idiomas.
2. Congelar el script y documentar diferencias respecto a EXP-436. Registrar criterios de exclusión de cabeceras, notas, numerales, puntuación, grafías y límites de línea.
3. Fijar la métrica exacta, intervalos por bootstrap a nivel documento/folio (no asumir independencia entre palabras), tamaño mínimo de muestra y análisis de sensibilidad por longitud.
4. Incluir controles positivos (dos textos independientes del mismo idioma) y negativos (barajado que conserve longitud y frecuencias globales).
5. Separar claramente replicación descriptiva, contraste inferencial y generalización a lenguas naturales; predefinir umbrales antes de ver resultados.
6. Mantener intactos los resultados históricos y `state/committed_claims.md`. Crear un experimento nuevo solo después de resolver la procedencia y comprobar el registro de identificadores.

## Estado
PROTOCOLO / SIN EJECUCIÓN. No se han calculado estadísticas nuevas ni obtenido traducción. No promover afirmaciones hasta pasar las puertas y la auditoría independiente exigida en `SOUL.md`.
