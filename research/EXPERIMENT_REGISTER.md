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


## Auditoría técnica de ligaduras y cobertura IVTFF (22-10-2026)

- [Informe descriptivo reproducido en CI](ivtff_ligature_view_sensitivity_inventory_2026-10-22.md): compara política histórica, ligadura atómica y expansión derivada; no tiene ID EXP porque la reconciliación de numeración sigue pendiente.
- La especificación IVTFF 2.0.2 §6.6 define `{…}` como ligadura. En cobertura amplia, ZL3b/ZL3a contienen 446/444 spans; 44/45 están dentro de anotaciones cuadradas eliminadas por la política histórica de incertidumbre. La vista expandida cambia `daiin` de 853 a 852 en cada una de esas transcripciones, sin cambiar el número de líneas iniciales en esta auditoría descriptiva.
- Se detectó una diferencia de cobertura independiente: el patrón de EXP-590 no reconoce IDs como `f67r1.5` o `fRos.23`. Su salida histórica se reproduce exactamente (ZL3b: 4.188 líneas con tokens, 32.732 tokens, 726 `daiin`, 133 líneas iniciales); la vista amplia recoge 5.385 registros de texto. No sobrescribir EXP-590. Antes de regenerar resultados, validar la gramática oficial de IDs IVTFF y decidir explícitamente el universo de registros.
- Nuevos scripts/tests: `scripts/audit_ivtff_brace_spans.py`, `scripts/audit_ivtff_ligature_views.py`, `tests/test_ivtff_ligature_views.py`. La auditoría de ligaduras y cobertura pasa por el workflow [run 563](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39738683050).
- Próxima acción: validar los identificadores de línea contra la especificación IVTFF y añadir una comparación de cobertura con EXP-602. Mantener todos los EXP históricos sin cambios hasta que esa adjudicación esté documentada.


## Revisión de evidencia predictiva y siguiente prueba (22-10-2026)

- Se inspeccionó el artefacto `experiments/exp_602_heldout_predictive_test/`. Su criterio predeclarado de mejora predictiva para `daiin` **no se cumplió**: ganancia de log-loss −0,08131; IC bootstrap por folio del 95 % [−0,11174; −0,05641]. El baseline condicional al inventario de tokens de cada línea reservada gana, aunque es un control diagnóstico exigente y no un predictor desplegable.
- El ID EXP-602 colisiona con `exp_602_independent_ivtff_parser_audit`; no adjudicar todavía qué artefacto retiene el ID canónico ni renombrar carpetas sin rastrear referencias y hashes.
- Plan de siguiente prueba, sin asignar EXP nuevo: [`next_decisive_test_plan_2026-10-22.md`](next_decisive_test_plan_2026-10-22.md). Define cobertura IVTFF congelada, división por folio sin fugas, baseline entrenable, métrica/regla de éxito previa y controles negativos.
- No presentar el resultado actual como desciframiento. La próxima prueba solo contará como avance positivo si supera un baseline justo en folios no vistos; un resultado negativo se conserva y no se usa para ajustar repetidamente sobre el mismo conjunto reservado.


## Adjudicación documental de la colisión EXP-602 (22-10-2026)

- Informe: [exp602_collision_adjudication_2026-10-22.md](exp602_collision_adjudication_2026-10-22.md).
- Hasta reconciliar la cronología de commits, referencias cruzadas y registros de la Biblioteca, usar alias descriptivos y limitados a ruta: **GH-602-PARSER-AUDIT** para `experiments/exp_602_independent_ivtff_parser_audit/` y **GH-602-HELDOUT-PREDICTION** para `experiments/exp_602_heldout_predictive_test/`. No renombrar ni asignar un EXP canónico todavía.
- La versión actual del parser audit es `results_v7.json`: cero diferencias de campos entre Parser A y B para ZL3b (5.385 registros) y ZL3a (5.389 registros) bajo la política declarada. Los resultados v1–v6 se conservan como historial.
- La prueba held-out es distinta y su criterio predictivo predeclarado falla para `daiin` (ganancia log-loss −0,08131; IC 95 % por folio [−0,11174; −0,05641]). No mezclar este resultado con la auditoría del parser.
- Ambos resultados son metodológicos/estadísticos, no desciframiento. No asignar otro ID numérico hasta reconciliar el registro global.


## Cobertura estructural de identificadores IVTFF (22-10-2026)

- Auditoría nueva: [ivtff_page_locus_id_coverage_audit_2026-10-22.md](ivtff_page_locus_id_coverage_audit_2026-10-22.md). CI run [575](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39740049037) terminó en `success`; fixtures de regresión run [574](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39740031613) también terminó en `success`.
- ZL3b: 227 cabeceras únicas, 5.385 registros; ZL3a: 227, 5.389; IT2a: 225, 5.215. En los tres archivos: cero cabeceras malformadas, cero registros malformados, cero discordancias entre la página activa y el ID de locus, y cero números de locus fuera del intervalo de control 1–160.
- Se añadieron `scripts/audit_ivtff_page_locus_ids.py` y `tests/test_ivtff_page_locus_ids.py`, integrados en `.github/workflows/voynich-check.yml`. La auditoría no modifica transcripciones ni resultados históricos.
- Esta validación estructural no reemplaza un validador IVTFF completo ni resuelve automáticamente los experimentos históricos que usaban patrones incompletos. Cada análisis debe declarar su población y política de tokenización antes de regenerarse.


## Reproducción de EXP-573 y portabilidad (22-10-2026)

- Se eliminó la ruta absoluta de máquina de `experiments/exp_573_c007_reconciliation/script.py`, se añadió una función `main()` protegida por `if __name__ == "__main__"`, y se agregó una prueba de portabilidad al workflow.
- La ejecución completa pasó en [CI run 584](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39740259579). Los valores canónicos se reproducen: A `ok` = 1,421× frente a 1,42× publicado; B `qok` = 1,028× frente a 1,03× publicado.
- **Limitación confirmada:** la rama de fórmula antigua + clasificación por folio no reproduce exactamente exp_174: A `ok` = 2,083× frente a 1,930× citado; B `qok` = 1,259× frente a 1,239×. El contraste histórico es una comparación metodológica aproximada, no una reproducción exacta. La errata de atribución 2,047× (B `qo`, no A `ok`) se basa en la tabla histórica citada, no en asumir que la rama antigua se ha reproducido exactamente.
- El detalle se conserva en [result.md de EXP-573](../experiments/exp_573_c007_reconciliation/result.md). No se han modificado las transcripciones ni se ha creado un EXP nuevo.


## EXP-590 — cobertura ampliada de IDs IVTFF (22-10-2026)

- Se amplió `scripts/exp590_daiin_position.py` para reconocer IDs de página subdividida (p. ej., `f67r1`) y `fRos`; también se corrigieron las rutas de entrada/salida para que sean relativas a la raíz del repositorio.
- Añadida la prueba `tests/test_exp590_ivtff_line_ids.py` e integrada en el workflow. La ejecución de CI de la prueba se está verificando: [run 590](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39740873673).
- **Reproducción ampliada completada:** 5.376 líneas con tokens, 39.594 tokens, 853 `daiin`, 161 líneas iniciales y 134 finales. Contraste de permutación de 5.000 réplicas: media nula 109,121; DE 9,315; p empírico corregido 0,000200. La salida queda guardada en [informe Markdown](experiments/2026-10-22-exp590-corrected-L-metadata.md) y [JSON](experiments/2026-10-22-exp590-corrected-L-metadata.json). CI [run 596](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39741331722) terminó en success. Los conteos previos (4.188 líneas, 32.732 tokens, 726 `daiin`) corresponden al parser incompleto y no deben mezclarse con la población corregida. Ver [errata EXP-590](experiments/2026-10-20-exp590-erratum.md).
- No crear otro ID ni afirmar validación lingüística/desciframiento. La corrección mejora la cobertura estructural, pero los resultados estadísticos deberán reevaluarse una vez regenerados.
