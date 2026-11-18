# EXP-436 — rectificación de auditoría de alcance (2026-11-18)

**RECTIFICACIÓN: EL DIAGNÓSTICO ORIGINAL ERA ERRÓNEO.**

Tras inspeccionar de nuevo el contenido de `experiments/exp_436_latin_hapax_length/script.py` (blob `34996a75107fac6d231c1890d4b8afe480a4578c`), se confirma que `def main():` está **en columna cero**, fuera de `analyze_freq_class`. La llamada final `main()` es válida desde el punto de vista del alcance de Python. **No existe el supuesto NameError por anidamiento.**

Se retira expresamente la afirmación anterior de fallo de indentación y cualquier conclusión basada en ella. No hay evidencia de ejecución fallida por ese motivo. Las discrepancias de corpus y ruta italiana siguen siendo problemas reales, documentados por separado.

Estado: CORREGIDO; esta nota sustituye íntegramente a la versión anterior.