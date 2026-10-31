# EXP-170: impedir aceptación de snapshots JSON con claves duplicadas

**Fecha:** 2026-10-31. **Base:** `45084484a717599154cf08c677134813990f7b80`. **Clase:** reparación de integridad de la auditoría, sin EXP nuevo. **Estado de reproducción histórica de EXP-170:** BLOCKED.

## Defecto demostrado y criterio falsable

`scripts/audit_exp170_archive.py` ya utilizaba `parse_archive` para rechazar claves duplicadas en los 400 vectores históricos, pero el argumento CLI `--check` leía el snapshot de referencia mediante `json.loads`, que acepta silenciosamente claves repetidas y conserva la última. Un snapshot sintético `{"ok": 1, "ok": 1}` se consideraba igual al resultado `{"ok": 1}`, a pesar de ser ambiguo. El defecto afecta a la comprobación de integridad del **snapshot de referencia**, no demuestra corrupción en el snapshot archivado.

**Criterio:** `--check` debe rechazar un snapshot con cualquier clave JSON duplicada; debe aceptar uno con claves únicas y valores idénticos al resultado de auditoría. La comparación real contra el snapshot congelado debe seguir pasando sin alterar sus bytes.

## Cambio y pruebas

- `scripts/audit_exp170_archive.py`: sustituir `json.loads(args.check.read_text())` por el lector estricto existente `parse_archive(args.check.read_text())`. No se cambia el cálculo de estadísticas ni el parser de las 400 simulaciones.
- `tests/test_exp170_archive.py`: prueba adversarial del `--check` con clave duplicada y control positivo con clave única, ambos sin ejecutar el simulador.
- Ejecutar en Python normal y optimizado: `python -m unittest discover -s tests -p 'test_exp170_archive.py' -v` y `python -O -m unittest discover -s tests -p 'test_exp170_archive.py' -v`.
- Ejecutar el cotejo real: `python scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json`.
- Verificar CI de PR y, solo tras eventual integración, CI del nuevo SHA de master. Las ejecuciones no se consideran satisfactorias hasta consultar su estado y registros.

## Identidades históricas y límites

Se mantienen los locks SHA-256 del informe de 2026-10-31: script histórico `8fe0f7d153211b320b34ca8543dac1ba029e629c4413c203fb2df0031063721c`; informe histórico `740e9997559a43529391ba29e339bbf955722aa0a1b8302efb451cb66706f354`; JSON histórico `c71f7161eb69c6cefa7b7fb6a72c000b6647137200166f331ca920042159e874`; ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.

No se ejecuta Naibbe, no se reconstruyen 400 simulaciones, no se modifica el snapshot histórico, los corpus ni las semillas, y no se reclama procedencia histórica de inputs externos. El fallo sintético anterior queda documentado; no constituye evidencia de significado ni de desciframiento. EXP-170 sigue bloqueado por la identidad exacta del input italiano, el commit histórico de Naibbe y la clasificación incorrecta del texto inglés como «latín». El 22-11-2026 es una fecha de evaluación, no una promesa de traducción.
