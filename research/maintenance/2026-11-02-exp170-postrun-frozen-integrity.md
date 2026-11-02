# EXP-170 — barrera de integridad congelada después del proceso hijo

**Fecha:** 2026-11-02. **Tipo:** corrección operativa acotada; no nuevo EXP. **Base inspeccionada:** `ba762f62063287b38a18b5144a5a851fabe558e9`. **Reproducción histórica exacta:** BLOCKED.

## Defecto y criterio falsable

`run_reconstruction()` verificaba los SHA-256 de las cuatro entradas congeladas antes de preparar el área temporal, pero al regresar un proceso hijo con código 0 releía el JSON histórico para deducir el esquema **sin volver a comprobar sus hashes**. Una edición concurrente del checkout durante un proceso largo podía cambiar ese archivo o las otras entradas entre la verificación inicial y la aceptación final. La copia staged estaba protegida por hashes, pero el contrato de aceptación seguía leyendo la referencia histórica sin una barrera posterior.

**Criterio previo a la prueba:** si el verificador de entradas congeladas detecta un cambio después del proceso hijo, aunque éste haya salido con código 0 y generado 400 vectores válidos, la salida debe quedar en cuarentena, el recibo debe registrar `FAILED`, `child_returncode=0`, `returncode=65` y el error, y no debe publicarse `simulation_results.json` como reconstrucción moderna.

## Reparación y regresión

- `scripts/run_exp170_isolated_reconstruction.py`: segunda llamada a `verify_frozen_inputs(root)` en la ruta de aceptación, antes de releer el archivo histórico y de publicar la salida. El fallo entra en la ruta de validación y cuarentena ya existente.
- `tests/test_exp170_isolated_reconstruction.py`: proceso hijo **sintético** que devuelve éxito y el payload congelado; el verificador simula deriva en su segunda llamada. Comprueba las dos llamadas, rechazo, recibo, bytes exactos en cuarentena y hash del archivo original intacto.
- No se modifica ninguna transcripción, archivo de 400 vectores, semilla, manifiesto de holdout, compromiso o script histórico. No se lanza el cifrador.

## Verificaciones necesarias

```sh
python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python -O -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python tests/test_exp170_archive.py
python scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

Comprobar CI de la PR en el SHA exacto y, si se integra, CI del nuevo `master`. **No inferir éxito a partir de esta nota.**

## Alcance científico y límites

Esta prueba verifica una **carrera sintética de integridad**, no que tal carrera ocurriera históricamente. La segunda comprobación no es un bloqueo transaccional contra un adversario que cambie el checkout inmediatamente después; los bytes staged ya se cotejan por separado. No recupera las entradas exactas de abril de 2026 ni vincula los 400 vectores a sus semillas efectivas. EXP-170 continúa BLOCKED para reproducción histórica exacta. Las contradicciones de C001, la adjudicación IVTFF integral y la conciliación de artefactos permanecen pendientes. Sin traducción ni conclusión semántica.

**Siguiente acción:** buscar recibo histórico independiente de las tres entradas externas de EXP-170; no sustituir el candidato preabril por una supuesta reproducción.
