# EXP-436 — auditoría estática de alcance de main (2026-11-18)

## Incidencia confirmada por lectura del script de master
Blob Git `34996a75107fac6d231c1890d4b8afe480a4578c`, archivo `experiments/exp_436_latin_hapax_length/script.py`:
- línea 33: `def analyze_freq_class(...):` en columna cero.
- línea 50: `    def main():` indentado cuatro espacios dentro de `analyze_freq_class`.
- líneas 113–114: `if __name__ == '__main__': main()` en columna cero.

En Python, `main` así definido es un nombre local a `analyze_freq_class`, no global. Si se ejecuta ese archivo tal como está, al alcanzar la llamada final se producirá `NameError: name 'main' is not defined`. Esto es una conclusión estática sobre el código inspeccionado, no una ejecución de CI ni una reconstrucción histórica.

## Impacto
- Los resultados de `result.md` no se pueden reproducir ejecutando directamente el `script.py` actual sin modificarlo.
- No implica que los resultados archivados sean fabricados: pudieron provenir de otra versión, de código distinto o de una ejecución no preservada. Falta trazabilidad.
- Se suma a la discrepancia de rutas latinas y a la ruta italiana ausente ya documentadas.
- Mantener `result.md`, `CORRECTION.md` y `state/committed_claims.md` sin cambios hasta una adjudicación.

## Próxima prueba reproducible
1. Ejecutar `python experiments/exp_436_latin_hapax_length/script.py` en un checkout fijado y guardar stderr y código de salida; comparar con la predicción estática.
2. Revisar el historial de `script.py` para localizar cuándo se introdujo la indentación.
3. Crear una copia reparada en una ruta NUEVA, preservando el original; fijar corpus y limpieza de cabeceras antes de medir.
4. Publicar tests que comprueben la invocación CLI, los paths de entrada y la procedencia de las tablas.

Estado: diagnóstico estático; NO ejecución; NO nuevos resultados lingüísticos ni traducción.
