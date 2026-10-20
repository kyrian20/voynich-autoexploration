# Auditoría de inventario del repositorio — 20-10-2026

Estado: **inventario estructural reproducido; revisión semántica de artefactos pendiente**.

## Alcance y método

Se consultó el árbol Git recursivo de la rama `master` mediante la API de GitHub. El árbol devuelto no estaba truncado. El inventario cuenta rutas y carpetas, no certifica que cada experimento sea científicamente válido ni que las copias de la Biblioteca sean idénticas.

## Recuento estructural observado

- Rutas totales en el árbol: **2.085**.
- Carpetas bajo `experiments/` cuyo nombre sigue `exp_NNN_…`: **624**.
- IDs numéricos únicos en esas carpetas: **617**.
- ID mínimo/máximo en las carpetas: **1–621**.
- Huecos numéricos observados en la secuencia de IDs de carpeta hasta 621: **29, 571, 614 y 615**. Un hueco no demuestra por sí solo que falte un experimento: puede haber artefactos en otras rutas o numeración histórica.
- Ficheros de workflow bajo `.github/workflows/`: **31**.
- Carpetas de experimento que no contienen simultáneamente un script reconocible y un resultado reconocible con nombres convencionales: **62**. Esto es una cola de triage, no una lista de 62 errores: varios experimentos históricos conservan solo el informe, y algunos están diseñados así.

## Colisiones de ID de carpeta confirmadas

| ID | Carpetas | Acción |
|---|---|---|
| 177 | `exp_177_position_sensitive_cipher`; `exp_177_verify` | Inspeccionar objetivo, commit y referencias; no fusionar |
| 594 | `exp_594_daiin_explicit_paragraph_markers`; `exp_594_daiin_paragraph_start` | Mantener ambas; resolver alias técnicos |
| 596 | `exp_596_daiin_position_controls`; `exp_596_zl3a_zl3b_line_level_audit` | Mantener ambas; resolver alias técnicos |
| 597 | `exp_597_daiin_frequency_control_words`; `exp_597_initial_form_next_token_context` | Mantener ambas; resolver alias técnicos |
| 600 | `exp_600_ivtff_parser_conformance`; `exp_600_transcription_concordance` | Mantener ambas; separar la serie de numeración |
| 601 | `exp_601_folio_clustered_confirmation`; `exp_601_primary_statistic_paired_sensitivity` | Mantener ambas; resolver alias técnicos |
| 602 | `exp_602_heldout_predictive_test`; `exp_602_independent_ivtff_parser_audit` | Mantener ambas; no confundir predicción held-out con auditoría del parser |

Estas colisiones son de nombre/ID, no prueba automática de que los análisis sean erróneos. Los informes y datos deben conservarse; se requiere rastrear las referencias antes de renombrar.

## Hallazgos de automatización

Hay **31 workflows**. El conjunto incluye un workflow autónomo que ejecuta EXP-590, EXP-593, EXP-622 y EXP-623, además de workflows específicos para otras pruebas. La cantidad de workflows no es por sí misma un defecto, pero exige auditar disparadores, concurrencia, escrituras de resultados y colisiones de artefactos antes de permitir que múltiples workflows modifiquen las mismas rutas.

El 20-10-2026, una ejecución de `Voynich Check` falló en la prueba de regresión porque `scripts/exp590_daiin_position.py` conservaba una referencia a la variable `q` ya no definida. Se eliminó esa referencia. La ejecución siguiente de `Voynich Check` para el commit `27f4cd98de28d8b0c1965e0a06582e295ff612d0` completó con éxito las comprobaciones de existencia del corpus, sintaxis Python, pruebas de metadatos y auditoría de `$L`. Las modificaciones posteriores requieren su propia comprobación CI.

## Prioridades derivadas

1. Completar la auditoría de las 7 colisiones de IDs y asignar alias técnicos sin alterar los nombres históricos.
2. Revisar los 31 workflows: triggers, permisos, concurrencia, outputs compartidos y si ejecutan experimentos obsoletos.
3. Clasificar las 62 carpetas sin pareja script+resultado como `report-only`, `script-only`, `data-only`, `archived` o `defect`; no etiquetarlas automáticamente como errores.
4. Resolver las discrepancias de tokenización ZL3b/ZL3a con fixtures derivados de IVTFF 2.0.2.
5. Completar inventario espejo de la Biblioteca con hashes de contenido y commits de GitHub; no asumir equivalencia por nombre.
6. No asignar nuevos IDs EXP hasta reconciliar el registro histórico y las colisiones confirmadas.

## Límites

Esta auditoría es estructural y reproducible desde el árbol de Git. No ejecuta todos los experimentos históricos, no revisa en profundidad cada uno de los 2.085 paths y no valida los resultados estadísticos. El estado global del proyecto sigue siendo **en auditoría**, no «limpio» ni «sin errores».
