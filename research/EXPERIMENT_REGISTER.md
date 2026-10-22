# Registro de numeracion de experimentos

Actualizado: 2026-10-21.

## Regla
Los identificadores EXP son unicos. Las fases, los experimentos y las ejecuciones de Actions son series distintas. Un reintento no crea un EXP nuevo. No borrar resultados antiguos: registrar conflictos y conservar los artefactos.

## Conflictos conocidos
- EXP-590: los archivos creados el 20-10-2026 pueden colisionar con numeracion previa; no asumir que sean el EXP-590 historico. Además, la primera versión del script leía `$Q` como Currier; el script se corrigió el 20-10-2026 para usar `$L`. Los JSON/MD anteriores a la nueva ejecución siguen siendo inválidos para resultados por clase hasta confirmar que Actions los regeneró.
- EXP-591: existe un experimento previo de analisis held-out folio (commit e00b3f8) y un script posterior de variantes creado el mismo dia. El script de variantes no puede usar el identificador 591.
- EXP-592: existe un analisis max-T previo (commits 70db96a y a74cff7).
- EXP-593: script canonico scripts/exp593_daiin_variants.py; ejecucion completada y resultados guardados en research/experiments/2026-10-20-exp593.md y .json. Fuente SHA-256: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc. El identificador aun debe cotejarse con el indice historico completo.

## EXP-593 — reproducción corregida con ajuste max-T estandarizado

**Estado:** REPRODUCIDO en GitHub Actions; no VALIDADO como hipótesis lingüística ni resultado de desciframiento.

- Run de reproducción: [39569620268](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39569620268), conclusión `success`; el log contiene `observed_standardized_statistic`, `null_sd_initial` y los p ajustados corregidos.
- Fuente: `data/transcriptions/eva_zl3b.txt`, SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; 4.188 líneas, 32.732 tokens; 5.000 permutaciones; semilla 20261021.
- Resultados corregidos: `daiin` 726 ocurrencias (133 inicios, 118 finales; A=440, B=278, unknown=8), p empírico 0,000200 y p max-stat estandarizado 0,000400; `dain` 198 (45 inicios, 26 finales), p empírico 0,000200 y p ajustado 0,000400; `daiiin` 19 (2 inicios, 5 finales), p empírico 0,814637 y p ajustado 0,988602.
- El JSON corregido de 21-10-2026 contiene los campos de estandarización esperados y coincide con los valores visibles en el log del run. Blob SHA del JSON: `a4b7ae7810baf6895010aba8abbfe0cc6369ad06`; informe Markdown: `b11f9c18df6afde5015e8a58705be1ad41ef500a`.
- Los p ajustados históricos del procedimiento anterior quedan inválidos para inferencia; se conservan sin borrar. El ajuste corregido soluciona la comparación entre variantes, pero el nulo sigue permutando tokens dentro de cada línea y no prueba significado ni traducción.
- La clase Currier se extrae de `$L=A/B`, no de `$Q`. Las afirmaciones sensibles a tokenización permanecen limitadas por la conformidad IVTFF aún incompleta.

## Auditoría estructural del repositorio (20-10-2026)
- Inventario recursivo de GitHub: 2.085 rutas, 624 carpetas `experiments/exp_NNN_*`, 617 IDs únicos y 7 grupos de colisión de carpeta (177, 594, 596, 597, 600, 601, 602); el detalle y las limitaciones están en [auditoría de inventario](repository_inventory_audit_2026-10-20.md).
- Se identificaron 31 workflows y 62 carpetas que requieren clasificación porque no contienen a la vez un script y un resultado reconocibles. No se etiquetan automáticamente como defectos.
- No asignar IDs nuevos hasta reconciliar el registro y el archivo maestro histórico.

La salida anterior `2026-10-20-exp593.json` se conserva y está duplicada byte a byte por contenido en `2026-10-20-exp593-corrected-L-metadata.json` (mismo SHA de blob `8379ff62e98f86212937426d2e3cda119efd2d9a`); el informe corregido se guarda como `2026-10-20-exp593-corrected-L-metadata.md`. GitHub Actions run [39491327187](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39491327187) completó las cuatro ejecuciones y la escritura de artefactos con el parser compartido. El resultado se considera `REPRODUCED` bajo el parser común, pero no `VALIDATED`; las afirmaciones sensibles a tokenización siguen `BLOCKED` hasta completar la conformidad IVTFF.

## Literatura externa prioritaria (21-10-2026)
- Añadida [nota sobre la hipótesis de singuliones y protocolo de réplica](EXTERNAL_RESEARCH_MEMO_SINGULION_STRUCTURE_2026-10-21.md), basada en Layfield y Fagin Davis, *Digital Medievalist* 19 (2026), DOI 10.4000/16k0a. El artículo propone que la estructura física actual podría no reflejar el orden original de los bifolios. Se registra como hipótesis publicada, no como hecho probado por nuestro análisis. El protocolo propuesto no tiene ID EXP hasta reconciliar el registro histórico.

## Auditoria tecnica (20-10-2026)
- Corregido `scripts/exp593_daiin_variants.py`: la clase Currier ahora se extrae de `$L=A/B`, no de `$Q`.
- Añadido `scripts/audit_ivtff_metadata.py`, sin identificador EXP, para validar que la transcripcion contiene ambas clases y contar cabeceras clasificadas.
- El workflow ejecuta esta auditoria antes de los experimentos. La nueva salida de EXP-593 debe sustituir/actualizar los artefactos con los resultados corregidos al ejecutarse Actions; hasta entonces, los resultados publicados arriba solo describen la ejecucion inicial y sus estadisticas globales deben volver a verificarse.
- Fuente del formato: IVTFF define `$L` como lengua Currier y `$Q` como cuaderno/quire.

## Siguiente accion
Recuperar el archivo maestro historico y enumerar todos los scripts, informes y JSON EXP-* antes de asignar nuevos numeros. El ultimo identificador libre no esta confirmado todavia.

## Conflicto con exportaciones de la Biblioteca ChatGPT
- Dos informes guardados en `/Investigación Voynich/` usan `EXP-623` para controles de orden de palabras; en este repositorio, `EXP-623` es la sensibilidad de la interacción ch/sh en IT2a. Son sistemas de numeración incompatibles. No fusionar, sobrescribir ni reasignar estos archivos sin un inventario de sus scripts y resultados asociados.
- El protocolo v7 de EXP-602 registra cero diferencias entre parsers para ZL3b (5.385 registros) y ZL3a (5.389). Se corrigieron el terminador de comentarios IVTFF, el empalme de alternativas y las anotaciones internas; los resultados de v1–v6 siguen preservados; v7 es la versión actual. El acuerdo es bajo la política de normalización documentada, no una certificación completa de IVTFF. La predicción A/B permanece bloqueada hasta completar fixtures y validación independiente de `$L`.

## Errata enlazada
- EXP-590: consultar [errata de clasificación Currier](experiments/2026-10-20-exp590-erratum.md). El artefacto histórico se conserva; las tablas por clase requieren regeneración con el script corregido.


## EXP-604–611 — bloque de reproducción y controles (21-10-2026)

La síntesis crítica de resultados, hashes de fuentes, criterios de interpretación y limitaciones está en [RESULTS_SYNTHESIS_EXP604-611_2026-10-21.md](RESULTS_SYNTHESIS_EXP604-611_2026-10-21.md). Los artefactos `results.json` y `result.md` de cada experimento siguen siendo las fuentes primarias.

- **EXP-604:** el enriquecimiento posicional de `daiin` en IT2a se reproduce bajo el nulo predeclarado; estado `REPRODUCED`, no evidencia de desciframiento.
- **EXP-605:** las cabeceras coinciden con la lista predeclarada de números de folio ausentes; auditoría de transcripción, no prueba de codicología física. `f116v` requiere cotejo en IT2a.
- **EXP-606:** se detectó un error de metadatos en la primera versión: el script etiquetaba `$Q` (quire/cuaderno) como Currier. Se corrigió para usar `$L=A/B` mediante `parse_currier_language`. Los resultados anteriores quedan **INVALID_FOR_CLAIM** para comparaciones condicionadas por Currier y no deben citarse. Run corregido [39673786598](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673786598) terminó en `success`: la media JSD de los tres bordes elegibles fue 0,6914 (ZL3b) y 0,6734 (IT2a), frente a 0,7019 y 0,7107 en controles de misma clase. La diferencia no apunta a mayor disimilitud media en esos bordes, pero n=3 es demasiado pequeño para una conclusión firme.
- **EXP-607:** señal de predicción de siguiente token en folios retenidos, pero la mejora frente al control de orden barajado es pequeña; resultado estructural exploratorio, no traducción.
- **EXP-608:** auditoría descriptiva de caracteres siguientes a `ch/sh`; no reproduce el modelo condicionado por plantilla de Parisel.
- **EXP-609:** diferencia pareada descriptiva en tasa vocálica después de `ch` frente a `sh`, repetida en dos transcripciones relacionadas; no son testigos independientes.
- **EXP-610:** el contraste `ch/sh` se reduce en tokens largos, indicando que la longitud explica parte de la diferencia bruta.
- **EXP-611:** la diferencia descriptiva persiste en estratos emparejados por longitud exacta y posición; no se calculó p-valor y quedan posibles confusores.

Los workflows EXP-604–611 incluyen ahora publicación con fetch/rebase y hasta cinco intentos de push, sin force-push. Los runs correctos de EXP-604, 605, 607, 608, 609, 610 y 611 constan en la síntesis. No confundir fallos intermedios de YAML durante la reparación con resultados científicos; esos runs fallidos se conservan en el historial. EXP-606 se regeneró tras corregir `$Q`/`$L` y se verificó su run y artefactos; la interpretación queda limitada por la muestra de tres bordes elegibles.


## Revisión estructural independiente — 2026-10-22

El árbol recursivo completo de GitHub confirma 7 colisiones de IDs en carpetas top-level: EXP-177, 594, 596, 597, 600, 601 y 602. Los pares exactos y el método de conteo están en [la auditoría de estabilización del 22-10-2026](stabilization_audit_2026-10-22.md). El árbol tiene 624 carpetas top-level de experimento y 617 IDs distintos; la carpeta combinada `exp_613_615_ch_sh_inference_sensitivity` y los huecos aparentes 29, 571, 614 y 615 requieren cotejo con la historia, no reasignación automática.

**Bloqueo vigente:** no reservar ni renumerar nuevos EXP, no borrar ni fusionar carpetas históricas y no interpretar el número de carpeta como identificador global entre GitHub y Biblioteca hasta completar el cotejo de referencias, commits y hashes. En el trabajo cruzado, usar alias `GH-...` y `LIB-...` descriptivos.
