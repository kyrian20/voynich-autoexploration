# PR #290 — rechazo de recibos IVTFF JSON ambiguos (16-11-2026)

## Incidencia corregida en la rama, pendiente de integrar

El verificador offline de la PR #288, heredado por #289/#290, aceptaba un
recibo sintético con dos campos `status`: `FAIL` seguido de `PASS`. El parser
`json.loads` elegía silenciosamente el último valor y devolvía
`VERIFIED_RECEIPT_ONLY` cuando se suministraba el SHA-256 correcto del ZIP
sintético mediante el argumento de prueba `expected_zip_sha`. Además, una raíz
JSON `[]` y un elemento de `files` que no fuera objeto disparaban
`AttributeError` en vez del rechazo tipado anunciado por la herramienta.

Se exige ahora: ausencia de claves JSON duplicadas en cualquier nivel, raíz
y registros de tipo objeto, y nombre de destino del manifiesto perteneciente
a una lista cerrada. Se conserva la ruta absoluta realmente presente en el
manifiesto original del runner de la PR #287:
`/home/runner/work/_temp/ivtff-minimum-format.json`. La mera comprobación
del basename admitía indebidamente `../ivtff-minimum-format.json` en recibos
sintéticos. No se modifica el SHA fijo ni el artefacto histórico.

## Regresiones y evidencia observada

Comandos desde la raíz del repositorio:

Entorno local: Python 3.12.14, biblioteca estándar; ZIP y JSON sintéticos
deterministas, sin aleatoriedad ni semillas. Los SHA-256 de los ZIP originales
son comprobaciones de identidad, no sustitutos de las entradas archivadas.

```sh
python -m unittest discover -s tests -p 'test_ivtff_receipt_verifier.py' -v
python -O -m unittest discover -s tests -p 'test_ivtff_receipt_verifier.py' -v
python research/maintenance/verify_pr287_ivtff_artifact.py PATH/AL/ZIP-14191233024.zip
```

- Antes del arreglo, el `status` JSON contradictorio `FAIL`/`PASS` se aceptó
  con `VERIFIED_RECEIPT_ONLY` en un ZIP **sintético** cuya huella se pasó
  explícitamente a `verify()`. La raíz `[]` produjo
  `AttributeError: 'list' object has no attribute 'get'`.
- Tras el arreglo, **12/12** pruebas pasan en Python normal y **12/12** con
  `python -O` (frente a las siete anteriores). Cuatro rechazos nuevos y una
  aceptación del destino histórico del manifiesto.
- El ZIP histórico de la PR #287, Actions run
  [43789138871](https://github.com/kyrian20/voynich-autoexploration/actions/runs/43789138871),
  artifact `14191233024`, se descargó y se verificó localmente con el script
  reparado: SHA-256 ZIP
  `9f316ae1993389803d7b0af7b66db0bf6e2dbd45279e7a4547d8326786c31fd6`;
  JSON interno
  `ee9d6200204e21ca68159a6684c42d1f320e72b47f36e8ba8c12e2121117fd3f`;
  resultado `VERIFIED_RECEIPT_ONLY`.
- Se comprobó por separado el ZIP de logs de #290, Actions run
  [43820491607](https://github.com/kyrian20/voynich-autoexploration/actions/runs/43820491607),
  artifact `14203724816`, SHA-256
  `5ac9e12dbba3c6bc005543234af7c100c1cd45f0beb97b955af32821b9c0288a`:
  contiene `receipt-regression-normal.log` y
  `receipt-regression-optimized.log`, 831 bytes cada uno, con siete casos
  y cierre `OK` en cada registro. Es evidencia del commit **anterior**
  `2691f0f9ce5350fb95da5be6558b507205e0ffb1`, no de esta corrección.

## Alcance y límites

El ZIP histórico continúa anclado por su digest predeterminado: no se ha
demostrado que sus bytes estén alterados. Los casos adversariales son
**sintéticos** y prueban el comportamiento si se permite pasar otro SHA al
verificador; no prueban una manipulación real de Actions. La verificación
recorre el recibo y sus huellas declaradas; **no rehashéa los tres corpus
originales**, no adjudica todos los constructos IVTFF y no valida hipótesis
lingüísticas ni traducciones. El código debe revisarse e integrarse por orden
con las PR #287–290, y comprobarse el CI en el SHA final de esta rama.
