# EXP-170 — salida no UTF-8 del subproceso (28-10-2026)

**Tipo:** reparación operativa acotada, sin EXP nuevo. **Estado científico EXP-170:** BLOCKED para reproducción histórica exacta.

## Defecto reproducible

El runner de reconstrucción aislada usaba `subprocess.run(..., text=True, capture_output=True)` con decodificación estricta implícita. Si el simulador emite un byte inválido para UTF-8, `subprocess.run` puede lanzar `UnicodeDecodeError`. Esa excepción no está cubierta por los manejadores de timeout ni OSError: el directorio ya reservado queda sin `receipt.json`, `stdout.log` ni `stderr.log`. No implica que los datos históricos estén alterados ni que el simulador real haya producido ese byte.

**Reproducción independiente mínima (Python 3.13.5, no es la suite del repositorio):** un hijo sintético que emite `b'bad\xff'` y `b'err\xfe'` y termina con código 3 provoca `UnicodeDecodeError` con `text=True` sin `errors`; con `encoding='utf-8', errors='backslashreplace'` devuelve código 3 y textos `'bad\\xff'`, `'err\\xfe'` (representación escapada). Esto no sustituye la CI en Python 3.12.

## Reparación y regresión

Añadir `encoding='utf-8', errors='backslashreplace'` a la llamada del subprocess para que bytes inválidos queden representados mediante escapes visibles en logs y el recibo de fallo se escriba. Una regresión lanza **un hijo sintético real** con bytes inválidos (mediante sustitución controlada de la invocación al script; nunca ejecuta las 400 simulaciones), exige `FAILED`, código 3, ambos logs con `\\xff`/`\\xfe`, ausencia de salida nueva y hash histórico sin cambios.

**Comandos de CI:** `python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v` y `python -O -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v` (ya incluidos en `.github/workflows/voynich-check.yml`). Consultar ejecuciones por SHA de la PR y del merge antes de declarar cierre.

## Alcance y límites

Los logs son texto UTF-8 con escapes para secuencias inválidas; **no son un volcado binario byte a byte** y no se afirma preservación forense de bytes originales. No se ha ejecutado Naibbe ni reproducido EXP-170. No se han modificado corpus, particiones, semillas, salidas archivadas ni `state/committed_claims.md`. El simulador histórico ejecutado directamente sigue pudiendo sobrescribir su salida: utilizar únicamente el runner con `--execute` y entradas verificadas. Las entradas exactas y dependencias históricas siguen sin acreditarse.

**Relación:** [reserva concurrente](2026-10-28-exp170-concurrent-output-reservation.md); [norma de integridad](../RESEARCH_INTEGRITY_STANDARD.md).
