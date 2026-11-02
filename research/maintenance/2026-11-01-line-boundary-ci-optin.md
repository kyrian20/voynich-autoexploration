# Puerta explícita para evitar reejecuciones redundantes de la réplica de límites de línea

**Fecha:** 2026-11-01. **Base:** rama de PR #138, commit `b26639e15f79374540c8050f51898b860676c7f5` (incluye la PR #212). **Clase:** reparación operativa de ejecución y procedencia; **sin experimento nuevo**. La PR #138 permanece en borrador y no se solicita su integración en `master`.

## Incidencia concreta y evidencia anterior

El workflow `.github/workflows/voynich-check.yml` ejecutaba incondicionalmente `line_boundary_replication.py` y publicaba su resultado cada vez que una PR cambiaba, aunque la modificación fuera únicamente una auditoría de población. En [run 41272608853](https://github.com/kyrian20/voynich-autoexploration/actions/runs/41272608853), de 2026-11-01 04:18 UTC, el job `check` terminó `success`, y sus pasos **136** «Recalcular réplica corregida de límites de línea» y **137** «Conservar salida nueva de réplica corregida» constan como ejecutados satisfactoriamente. La PR #212 ya había añadido un censo descriptivo que no requería reentrenar el modelo. Este comportamiento repite una evaluación científica retrospectiva al cambiar código de mantenimiento y crea artefactos redundantes.

## Corrección y prueba falsable

El disparador manual `workflow_dispatch` incorpora el booleano `run_line_boundary_replication`, con valor predeterminado `false`. Los dos pasos (ejecución y publicación del JSON) requieren **simultáneamente** un evento `workflow_dispatch` y la opción explícita `true`. Los eventos `pull_request` y `push` siguen ejecutando las regresiones y auditorías de integridad, pero **no** el predictor completo. Una ejecución manual sin marcar la opción tampoco lo ejecuta.

La regresión `tests/test_line_boundary_ci_optin.py` lee el YAML con PyYAML `BaseLoader` y exige que la opción sea booleana, opcional y falsa por defecto, que el único comando de ejecución del predictor y su único upload tengan exactamente la misma puerta, y que el test se ejecute en Python normal y optimizado. El workflow ejecuta esas cuatro pruebas en ambos modos. No se modifica la implementación científica ni se vuelven a estimar sus métricas.

**Comandos:**

```sh
python -m unittest discover -s tests -p 'test_line_boundary_ci_optin.py' -v
python -O -m unittest discover -s tests -p 'test_line_boundary_ci_optin.py' -v
```

La CI de la PR hija debe confirmar tanto las pruebas como que los pasos científicos figuran **skipped**, no `success`, y que no se publica un nuevo artefacto `line-boundary-replication`. No afirmar cierre antes de comprobar esos tres puntos en la ejecución concreta.

## Primer intento de CI y corrección de entorno

La [ejecución 41273467391](https://github.com/kyrian20/voynich-autoexploration/actions/runs/41273467391) terminó en `failure` en el paso 121 de prueba de la puerta: `ModuleNotFoundError: No module named 'yaml'`. El workflow había instalado PyYAML 6.0.3 al principio con Python 3.12, pero después cambió a Python 3.12.14 para la batería histórica; el nuevo intérprete no tenía PyYAML. **No fue un fallo del contrato de opt-in ni una validación científica.** Se trasladó el paso de pruebas inmediatamente después de la instalación de PyYAML y antes del cambio de intérprete. El fallo original se conserva en Actions; no se borra ni se reinterpreta como éxito. La siguiente ejecución debe comprobarse independientemente.

## Integridad y límites

No se modifican corpus ZL3b/IT2a, resultados congelados, seeds, particiones, hashes, métricas, ni `state/committed_claims.md`. Se conserva la ejecución previa como evidencia histórica, sin retirarla ni sustituirla. La medida evita reejecuciones automáticas **de este predictor**; no equivale a una auditoría de todos los workflows ni valida IVTFF o la ciencia del modelo. La activación manual es posible cuando el workflow esté disponible en la rama predeterminada; mientras PR #138 siga en borrador, no se considera habilitación de un nuevo ciclo científico. La adjudicación IVTFF y las diferencias de población de 809/99 unidades de PR #212 siguen pendientes. La evaluación científica global continúa fijada para 2026-11-22 sin promesa de descifrado.
