# EXP-603 — errata de unidad reservada (28-10-2026)

**Estado:** INVALID_FOR_CLAIM exclusivamente para la afirmación de generalización a hojas físicas completamente reservadas. Las pérdidas, intervalos y resultados históricos se conservan sin modificar.

EXP-603 reutiliza el reparto de GH-602: SHA-256 del identificador de cara/panel `fNNr`/`fNNv`, no de la hoja física `NN`. La reconstrucción con ZL3b congelado identifica **32 de 39 hojas físicas de evaluación también presentes en entrenamiento** (47 identificadores de página de evaluación, 148 de entrenamiento; 919/2928 líneas). Las hojas de evaluación físicamente no vistas son 3, 4, 29, 46, 58, 103 y 116.

La separación por página se respeta, pero el bootstrap agrupado por identificador de cara no es una confirmación con hojas físicas independientes. No se recalculan pérdidas ni intervalos, ni se reinterpreta la pequeña ganancia negativa de daiin como evidencia positiva. La contaminación puede afectar al alcance inferencial; no permite cuantificar su sesgo sin un experimento prospectivo nuevo.

Evidencia: `scripts/audit_exp602_exp603_physical_leaf_holdout.py`, `tests/test_exp602_exp603_physical_leaf_holdout.py` y `research/maintenance/2026-10-28-exp602-exp603-physical-leaf-leakage.md`. Los artefactos originales permanecen congelados.
