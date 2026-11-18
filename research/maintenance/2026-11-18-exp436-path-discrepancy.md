# Auditoría de discrepancia de rutas EXP-436 — 2026-11-18

## Hallazgo verificable
En la rama master, `experiments/exp_436_latin_hapax_length/script.py` (blob `34996a75107fac6d231c1890d4b8afe480a4578c`) asigna `LATIN_CORPUS` a `data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt`. Sin embargo, `experiments/exp_436_latin_hapax_length/CORRECTION.md` (9-11-2026) afirma que el script usa `data/reference_corpora/latin/caesar_gallic_wars.txt` y adjudica ese segundo archivo a una traducción inglesa. Las rutas son distintas. La errata no identifica por sí sola los bytes del archivo que el script actual leería.

El script también busca `data/reference_corpora/italian/dante_divine_comedy_italian.txt`, mientras que el manifiesto de identidad contiene `data/reference_corpora/italian/dante_divina_commedia.txt`. El bloque italiano solo se ejecuta si existe la ruta buscada.

## Consecuencias
- La identidad lingüística del archivo `caesar_de_bello_gallico_latin.txt` queda PENDIENTE; no se le puede transferir automáticamente el hash o idioma del archivo `caesar_gallic_wars.txt`.
- La auditoría anterior puede describir una versión histórica distinta o una atribución de ruta equivocada. No se decide entre estas alternativas sin comprobar el historial Git, hashes y archivos.
- Los números históricos de EXP-436 permanecen `INVALID_FOR_CLAIM` para comparaciones externas hasta reconciliar entradas exactas.
- La observación no constituye una nueva inferencia sobre el idioma del Voynich.

## Pasos concretos
1. Obtener el blob y SHA-256 de ambas rutas latinas, verificar su existencia y contenido real; consultar Git history de `script.py` y `CORRECTION.md`.
2. Determinar qué commit y qué bytes produjeron cada fila archivada en `result.md`; si no hay evidencia, declarar procedencia no recuperable.
3. Repetir la inspección con las dos rutas italianas y distinguir ausencia de archivo de ausencia de ejecución.
4. Corregir o complementar la errata mediante una revisión independiente, sin sobrescribir resultados históricos.
5. Solo después iniciar la réplica con corpus monolingües, según `research/maintenance/2026-11-18-exp436-provenance-next-step.md`.

Estado: AUDITORÍA ESTÁTICA, SIN NUEVO CÁLCULO NI TRADUCCIÓN. No modifica compromisos ni hallazgos científicos.
