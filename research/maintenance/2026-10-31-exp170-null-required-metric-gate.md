# EXP-170: rechazar métricas obligatorias nulas en salidas reconstruidas

**Fecha:** 2026-10-31. **Clase:** corrección de integridad de datos, sin EXP nuevo ni experimento de descifrado. **Base comprobada:** `master` `2fe4bceeca36131514d19f7eab8399b444f57d71`. **Estado de EXP-170 histórico:** BLOCKED para reproducción exacta.

## Defecto y criterio falsable

`scripts/audit_exp170_archive.py::validate_archive` permitía `None` en **cualquier** métrica siempre que las cuatro condiciones conservaran 100 registros y las claves esperadas. `compute_metrics` en el script histórico solo devuelve un diccionario vacío cuando no hay datos; si devuelve un registro de métricas, todas son numéricas salvo `k_para_start_enrichment`, que puede ser `None` cuando no existen inicios de párrafo. Por tanto, una salida sintética de 400 registros con `edy_rate=null` podía superar la puerta de esquema y hacer que el runner la etiquetara `MODERN_RECONSTRUCTION_UNVALIDATED` tras un retorno cero, sin haber generado una métrica obligatoria.

**Criterio predefinido:** permitir `k_para_start_enrichment=null` en registros de forma válida, rechazar `edy_rate=null` (y cualquier otro campo obligatorio nulo) con `ValueError`. Un hijo sintético que retorna 0 pero escribe `edy_rate=null` debe producir recibo `FAILED`, retorno 65, salida bajo `simulation_results.failed.bin` con SHA-256 y ninguna salida `simulation_results.json` publicada. El archivo histórico congelado debe continuar superando la auditoría sin modificar su snapshot.

## Cambio y regresiones

- `scripts/audit_exp170_archive.py`: puerta explícita para campos no anulables, antes de validar números finitos.
- `tests/test_exp170_archive.py`: control positivo de nulo permitido para párrafo y negativo para `edy_rate`.
- `tests/test_exp170_isolated_reconstruction.py`: simulación sintética de retorno 0 con una métrica requerida nula, comprobando cuarentena, recibo y preservación del original.

No se importa ni ejecuta `experiments/exp_170_naibbe_simulation/script.py`; no se usa Naibbe. Las pruebas con datos sintéticos no rehabilitan la procedencia histórica de las 400 simulaciones.

## Identidades congeladas y comandos

Los hashes SHA-256 exigidos por `FROZEN_INPUT_SHA256` se mantienen sin cambio:
- Script histórico: `8fe0f7d153211b320b34ca8543dac1ba029e629c4413c203fb2df0031063721c`
- Informe histórico: `740e9997559a43529391ba29e339bbf955722aa0a1b8302efb451cb66706f354`
- JSON histórico: `c71f7161eb69c6cefa7b7fb6a72c000b6647137200166f331ca920042159e874`
- ZL3b: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`

Comprobaciones requeridas para cerrar:
```sh
python -m unittest discover -s tests -p 'test_exp170_archive.py' -v
python -O -m unittest discover -s tests -p 'test_exp170_archive.py' -v
python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python -O -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v
python scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json
```

La CI del head de esta rama y la posterior a una eventual integración deben verificarse por ID de ejecución y SHA exacto; no se declaran aprobadas de antemano. Conservar cualquier fallo.

## Alcance científico y límites

La corrección protege la **integridad de reconstrucciones futuras**; no demuestra que los 400 vectores originales contengan nulos o errores de ese tipo. La revisión archivística anterior encontró 400 vectores finitos. Persisten el bloqueo de identidad/versión exacta de Naibbe, la procedencia del italiano y la etiqueta histórica de «latín» aplicada a un texto inglés. No sustituir fuentes ni atribuir reproducción histórica a una ejecución moderna. No se alteran corpus, manifiestos de folios reservados, semillas, resultados negativos ni `state/committed_claims.md`.

**Autoauditoría de los cinco riesgos:** (1) sin calibración a métricas objetivo Voynich; la restricción deriva de la implementación histórica de `compute_metrics`. (2) No se transforma ninguna característica del corpus. (3) No se extrapola de esta puerta de esquema a mecanismos de escritura. (4) Ningún resultado negativo nuevo sobre el cifrador. (5) El control sintético positivo `k_para_start_enrichment=null` debe aceptarse y el control adversarial `edy_rate=null` debe rechazarse; no se comparan tasas Voynich contra controles ni se infiere significado.

**Evaluación científica global:** 22-11-2026; no implica descifrado ni promesa de traducción.
