# EXP-170 — preservar bytes originales de diagnóstico (28-10-2026)

**Tipo:** reparación operativa acotada, sin EXP nuevo. **Estado científico:** EXP-170 sigue **BLOCKED** para reproducción histórica exacta. Base inspeccionada: `master` `eccc16abb39f7bf29dbb2afec34c3356aadf93f5` (PR #117 integrada, CI push [40631032892](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40631032892) satisfactoria).

## Defecto específico y criterio falsable

Las reparaciones previas [salida no UTF-8](2026-10-28-exp170-nonutf8-subprocess-logs.md) y [timeout](2026-10-28-exp170-timeout-byte-escapes.md) guardan escapes de bytes inválidos en texto. **No preservan una captura binaria sin ambigüedad**: la secuencia real de bytes `5c 78 66 66` (los caracteres literales `\\xff`) y el byte `ff` pueden aparecer como `\\xff` en el log textual. No es evidencia de corrupción del archivo histórico; es un defecto de procedencia de diagnósticos nuevos.

**Criterio previo de reparación:** al ejecutar únicamente un hijo sintético que escriba `5c 78 66 66 7c ff` en stdout y `5c 78 66 65 7c fe` en stderr y salga con código 3, el runner debe producir `stdout.bin` y `stderr.bin` byte a byte idénticos, recibo FAILED/3 con SHA-256 y longitud de cada flujo, logs textuales legibles y ningún `simulation_results.json` nuevo. En timeout, conservar los bytes parciales exactos `partial ff` y `problem fe` y código 124. El archivo histórico debe mantener su SHA-256 original.

## Cambio y prueba

`scripts/run_exp170_isolated_reconstruction.py`: captura `subprocess.run` en modo binario (sin `text=True`), conserva `stdout.bin`/`stderr.bin`, genera los logs UTF-8 con `backslashreplace`, y registra SHA-256 y `size_bytes` de ambos flujos en `receipt.json`. En un timeout los bytes son **parciales**, no se afirma captura completa. Ante un fallo de lanzamiento se guarda la explicación textual, y los binarios vacíos indican que el hijo no llegó a emitir salida.

`tests/test_exp170_isolated_reconstruction.py`: nueva regresión de hijo sintético real con escapes literales y bytes inválidos, y extensión del caso de timeout para verificar bytes y hashes. Las pruebas existentes conservan los contratos de no sobrescritura y reserva concurrente.

**Comandos de validación previstos en CI:** `python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v` y `python -O -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v`. La validación final exige comprobar la ejecución de la PR en su SHA exacto y la ejecución posterior a la integración; no se presupone que sean satisfactorias.

## Integridad y límites

No se modifican corpus originales, manifiestos, particiones reservadas, vectores históricos, semillas, registros negativos ni `state/committed_claims.md`. La herramienta **no es un sandbox de seguridad**; ejecutar directamente el script histórico sigue pudiendo sobrescribir sus resultados. La identidad exacta de las entradas y dependencias que produjeron los 400 vectores originales sigue sin acreditarse. No se ejecutan simulaciones Naibbe ni se deducen significados o traducciones.

**Próximo paso científico:** recuperar la identidad de entradas históricas y cerrar contradicciones de procedencia antes de nuevos ciclos de hipótesis; no confundir este arreglo diagnóstico con una reproducción de EXP-170.
