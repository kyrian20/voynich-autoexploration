# Auditoría de estabilización del proyecto — 2026-10-22

## Alcance y método
Auditoría estructural de la rama `master` usando el árbol Git recursivo completo de GitHub (respuesta no truncada), inspección de los 31 workflows YAML y consulta de ejecuciones de Actions. No se han ejecutado aquí los scripts científicos ni se han recalculado resultados numéricos. Esta auditoría no certifica todo el contenido de la Biblioteca de ChatGPT.

## Resultado de la inspección del árbol
- HEAD de `master` observado: `3baca1a468c57ef3b2fe663e7860738153eb923a`.
- Árbol recursivo: 2.119 rutas; GitHub indicó `truncated=false`.
- Carpetas de primer nivel dentro de `experiments/`: 624.
- Carpetas con patrón `exp_NNN_nombre`: 624; IDs distintos detectados: 617, con mínimo 1 y máximo 621.
- Colisiones reales de ID entre carpetas de primer nivel: **7 grupos**, no contar como colisión los subdirectorios `data/` ni `archive/`:
  - EXP-177: `exp_177_position_sensitive_cipher` y `exp_177_verify`.
  - EXP-594: `exp_594_daiin_explicit_paragraph_markers` y `exp_594_daiin_paragraph_start`.
  - EXP-596: `exp_596_daiin_position_controls` y `exp_596_zl3a_zl3b_line_level_audit`.
  - EXP-597: `exp_597_daiin_frequency_control_words` y `exp_597_initial_form_next_token_context`.
  - EXP-600: `exp_600_ivtff_parser_conformance` y `exp_600_transcription_concordance`.
  - EXP-601: `exp_601_folio_clustered_confirmation` y `exp_601_primary_statistic_paired_sensitivity`.
  - EXP-602: `exp_602_heldout_predictive_test` y `exp_602_independent_ivtff_parser_audit`.
- No aparecen carpetas top-level independientes con los IDs 29, 571, 614 y 615; esto **no demuestra por sí solo** que haya experimentos perdidos. El nombre `exp_613_615_ch_sh_inference_sensitivity` parece abarcar varios números y debe cotejarse con el registro histórico.
- Regla de seguridad: no renombrar, borrar, fusionar ni reasignar ninguno de estos IDs hasta inspeccionar referencias, commits, scripts, resultados y hashes. Usar prefijos `GH-` y `LIB-` al comparar la Biblioteca con GitHub.

## Workflows de GitHub Actions
Se inspeccionaron los 31 archivos YAML en `.github/workflows/`:
- 30 workflows escritores tienen un grupo de concurrencia propio, `cancel-in-progress: false`, una instrucción de push y un bucle acotado de cinco intentos para rebase/push.
- `voynich-check.yml` es de solo lectura y no tiene bloque de concurrencia de escritor.
- Los grupos por workflow evitan cancelar entre sí todas las ejecuciones pendientes, como sucedería con un único grupo global; sin embargo, **no serializan escrituras de workflows distintos**. Los reintentos reducen el riesgo de conflicto non-fast-forward, pero no constituyen una garantía formal de exclusión mutua entre escritores. La solución estructural futura es centralizar las escrituras (un único workflow escritor o PR/merge queue) o hacer que los análisis publiquen artefactos sin escribir directamente a `master`.
- Las consultas de Actions muestran ejecuciones recientes satisfactorias de `Voynich Check` y de varios controles específicos. La ejecución `39721778175` de `Voynich Check` terminó `success` para el HEAD observado. También se observaron éxitos de controles estratificados, de posición, conformidad IVTFF, marcadores de párrafo, metadatos de línea, controles léxicos, contexto de dos tokens, concordancia de transcripciones y sensibilidad pareada.
- La consulta de las 30 ejecuciones más recientes no sustituye a verificar todas las ejecuciones relevantes ni a ejecutar de nuevo cada experimento afectado. Las cancelaciones del cambio temporal de concurrencia se clasifican como canceladas, nunca como éxitos.

## Puertas científicas pendientes
1. Completar la reconciliación de los siete grupos de colisión y de los IDs históricos en la Biblioteca; preservar todos los artefactos originales.
2. Comparar hashes GitHub/Biblioteca para cada artefacto crítico. La lista visible de Biblioteca consultada en esta sesión está limitada a 200 elementos, por lo que no se afirma que se haya auditado toda la Biblioteca.
3. Completar la conformidad IVTFF contra fixtures explícitos y la especificación independiente; la concordancia entre dos parsers no basta para validar cada convención.
4. Reproducir resultados críticos con comandos, versiones, semillas, hashes y logs guardados; distinguir `reproducido`, `validado`, `exploratorio` e `inválido para una afirmación concreta`.
5. Antes de cualquier experimento nuevo, leer el estado y consultar el registro de experimentos, comprobar trabajos previos y preregistrar hipótesis, controles, criterios de exclusión, semilla y corrección por multiplicidad. Aplicar `skills/audit_experiment.md` antes de actualizar archivos de estado científico.
6. No afirmar desciframiento ni significado a partir de diferencias de frecuencia o p-valores aislados.

## Conclusión operativa
La rama está estructuralmente mejor protegida y varias comprobaciones recientes han pasado. **La investigación aún no está completamente finiquitada**: las colisiones de numeración y la reconciliación GitHub/Biblioteca son bloqueos abiertos; además, la estrategia de escritura concurrente requiere una solución arquitectónica para garantizar que workflows distintos no compitan al actualizar `master`. No se ha creado un EXP nuevo ni se han cambiado conclusiones científicas.
