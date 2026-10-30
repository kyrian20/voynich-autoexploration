# EXP-170 — no perder identidad de bytes inválidos en timeout (28-10-2026)

**Tipo:** corrección operativa acotada, sin EXP nuevo. **Estado científico de EXP-170:** BLOCKED para reproducción histórica exacta. No se ha ejecutado el cifrador Naibbe ni se han producido vectores nuevos.

## Defecto y evidencia mínima

En `scripts/run_exp170_isolated_reconstruction.py`, la rama normal de `subprocess.run` conserva secuencias UTF-8 inválidas como escapes mediante `errors="backslashreplace"`, pero el manejador de `subprocess.TimeoutExpired` usaba `errors="replace"` en `stdout` y `stderr`. La excepción puede transportar bytes incluso con `text=True`; `replace` convierte tanto `b'\\xff'` como `b'\\xfe'` en el mismo carácter de sustitución U+FFFD, perdiendo la identidad del byte de diagnóstico.

Reproducción mínima local, Python 3, con `TimeoutExpired(cmd=['synthetic'], timeout=1, output=b'partial\\xff', stderr=b'problem\\xfe')`: la decodificación anterior da `'partial�'` y `'problem�'`; `backslashreplace` da `'partial\\xff'` y `'problem\\xfe'`. Esta prueba aislada no es una ejecución de la suite completa ni una reproducción científica.

## Corrección

Cambiar **solo** la decodificación de bytes del manejador de timeout a `errors="backslashreplace"`, igual que la salida normal. Conservar la etiqueta `FAILED`, el código 124 y el marcador `TIMEOUT`; no alterar la semántica de validación ni la publicación del JSON nuevo.

Ampliar `test_timeout_with_bytes_keeps_decoded_logs` en `tests/test_exp170_isolated_reconstruction.py`: exigir escapes literales `\\xff` y `\\xfe`, ausencia de U+FFFD, recibo `FAILED/124`, ausencia de `simulation_results.json` nuevo y SHA-256 del archivo histórico sin cambios. La prueba usa una excepción sintética, **no** lanza las 400 simulaciones.

## Criterios de cierre y límites

Ejecutar en CI canónica `python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v` y su variante `python -O`. Verificar la ejecución en el SHA exacto de la PR y después del merge en `master`; no declarar éxito antes de comprobar logs y resultados. El informe no demuestra que el simulador original haya producido bytes inválidos ni que exista una reproducción histórica de EXP-170.

Los escapes son una representación textual de los bytes inválidos, **no un volcado binario completo**. La ejecución directa del simulador histórico sigue pudiendo sobrescribir resultados; este runner proporciona aislamiento de rutas, no un sandbox de seguridad. La procedencia de entradas y dependencias históricas sigue pendiente. No se modifican corpus, salidas originales, particiones reservadas, semillas, compromisos ni resultados negativos.

**Antecedentes:** [reparación previa de salida no UTF-8](2026-10-28-exp170-nonutf8-subprocess-logs.md), [runner aislado](2026-10-28-exp170-isolated-reconstruction.md), [norma de integridad](../RESEARCH_INTEGRITY_STANDARD.md).
