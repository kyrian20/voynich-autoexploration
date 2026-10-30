# GH-602-HELDOUT-PREDICTION — errata de unidad reservada (28-10-2026)

**Estado:** INVALID_FOR_CLAIM exclusivamente para la afirmación de prueba sobre hojas físicas completamente desconocidas. El resultado negativo original y el intervalo archivado se conservan sin cambios.

El reparto histórico se hace por identificador de cara/panel (por ejemplo, `f34r` frente a `f34v`) y no por hoja física 34. La reconstrucción retrospectiva con la fuente ZL3b congelada encuentra **15 de 18 hojas físicas de evaluación también representadas en entrenamiento** (21 identificadores de página de evaluación, 60 de entrenamiento; 528/1797 líneas). Las hojas de evaluación no vistas físicamente son 46, 103 y 116.

La frase histórica «No folio crosses the deterministic split» se aplica únicamente al identificador de cara/panel, **no a la hoja física**. El criterio positivo predeclarado ya había fallado (ganancia de log-loss para daiin −0,08131); esta auditoría no cambia el signo ni vuelve a ejecutar el predictor. No se puede usar el intervalo histórico como inferencia confirmatoria independiente por hoja física.

Evidencia reproducible: `scripts/audit_exp602_exp603_physical_leaf_holdout.py`, `tests/test_exp602_exp603_physical_leaf_holdout.py` y `research/maintenance/2026-10-28-exp602-exp603-physical-leaf-leakage.md`. Se conservan intactos `script.py`, `results.json`, `result.md` y el corpus. No confundir con el otro experimento histórico llamado EXP-602, el auditor de parser IVTFF.
