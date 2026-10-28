# EXP-170 — conservar salidas negativas sin convertirlas en resultados válidos (28-10-2026)

**Tipo:** reparación operativa acotada, sin nuevo EXP. **Estado científico:** EXP-170 permanece **BLOCKED** para reproducción histórica exacta. Base: `master` `c3ccf64feb806607406e609c55aa82e37989028f`, con CI push [40636033692](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40636033692) satisfactoria antes del cambio.

## Defecto y criterio previo

El ejecutor aislado descartaba cualquier `simulation_results.json` recién generado si el hijo terminaba con código distinto de cero o si la validación del JSON fallaba. La carpeta temporal se eliminaba y solo se conservaban stdout/stderr y recibo. Esto perdía resultados parciales/negativos necesarios para investigar errores; no implica que los 400 vectores históricos se hayan alterado.

**Criterio:** un hijo **sintético** que escribe bytes parciales (incluido `ff`) y termina con código 3 debe producir `simulation_results.failed.bin` byte a byte idéntico, hash SHA-256 y tamaño en el recibo `FAILED`; nunca `simulation_results.json` validado. Un JSON generado con esquema inválido y salida cero debe quedar también en cuarentena, con código 65. Si no existe archivo, no se crea un falso resultado. Los vectores históricos permanecen con el mismo hash.

## Reparación

`scripts/run_exp170_isolated_reconstruction.py` copia únicamente los bytes de una salida nueva fallida que sea un archivo regular y no un enlace simbólico. El nombre terminado en `.failed.bin`, la etiqueta `UNVALIDATED_FAILED_OUTPUT` y los campos de hash/tamaño impiden confundirla con un resultado aceptado. Una salida irregular no se lee y queda reflejada como `quarantine_error`. El resultado de ejecución fallida continúa levantando `RuntimeError`; no se ocultan los fallos.

`tests/test_exp170_isolated_reconstruction.py` añade un caso de hijo sintético con retorno 3 y bytes no UTF-8, y refuerza la regresión del esquema inválido. La CI ya ejecuta este archivo con Python normal y `-O`. No se ejecuta Naibbe ni se repiten 400 simulaciones.

## Verificación y límites

**Pendiente de comprobación:** CI del commit exacto de esta rama y CI posterior a una eventual fusión. No declarar cierre hasta ambas. El archivo fallido puede contener datos parciales o malformados y no acredita reproducción histórica; sus bytes se preservan exclusivamente para diagnóstico. Si el hijo no genera archivo o el archivo no es regular, no existe resultado recuperable. Esta herramienta no es un sandbox de seguridad. No se modifican corpus, semillas, holdouts, archivos históricos ni `state/committed_claims.md`.

**Siguiente paso:** recuperar las entradas y dependencias históricas exactas de EXP-170 y reconciliar artefactos; mantener la prohibición de experimentos científicos bloqueados por procedencia.
