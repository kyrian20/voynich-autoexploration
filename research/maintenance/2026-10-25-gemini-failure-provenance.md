# Gemini: recibo de procedencia ante error de API — 2026-10-25

**Tipo:** reparación operativa acotada; sin nuevo EXP, sin simulaciones, sin modificación de corpus ni de resultados históricos.

## Defecto identificado

En `master` `fe0651f577712427b3c6351f0afa4b970e3641c4`, `scripts/request_gemini_review.py` devolvía error sin escribir ningún archivo si fallaba la llamada de generación o el JSON recibido. Aunque el workflow usa `if: always()` para conservar artefactos, su directorio de salida quedaba vacío: se perdía el recibo que distingue un intento fallido de una ejecución no iniciada. El workflow no se ha lanzado para reproducir un fallo remoto: el camino se ha identificado por inspección del código y se prueba con transporte simulado.

## Reparación y criterio de aceptación

Después de **un único intento** de POST, los fallos de transporte, tiempo de espera, tamaño y análisis JSON producen un `receipt.json` sin respuesta remota. Contiene `status=API_OR_RESPONSE_ERROR`, `scientific_status=BLOCKED`, modelo, SHA-256 del prompt, `api_attempts=1`, `manuscript_corpus_sent=false` y valores nulos para los hashes de respuesta no disponible. No guarda cuerpos de error, credenciales ni fragmentos de respuesta sin validar. Mantiene el código de salida distinto de cero y el comportamiento de un único intento; el workflow conserva el recibo mediante su paso existente `always()`.

Regresiones sin red: `python -m unittest discover -s tests -p 'test_gemini_review_request.py' -v`. Se simulan error de red y respuesta no JSON; ambos deben producir exclusivamente el recibo sanitizado, sin secretos, con el hash del prompt y exactamente una llamada al transporte simulado. Las pruebas son deterministas y no requieren semilla.

## Alcance y limitaciones

- La corrección no autoriza una nueva llamada a Gemini; la ejecución sigue siendo manual y opt-in.
- Los errores **anteriores a la llamada** (p. ej., falta de secreto o carpeta de salida ocupada) continúan sin recibo: no se etiquetan como intento API.
- El recibo prueba que el programa entró en el intento; no certifica que el proveedor recibiera o procesara la petición.
- La respuesta de Gemini sigue siendo una propuesta no verificada; no se actualizan `state/committed_claims.md`, `state/findings.md` ni folios reservados.
- La CI y la integración deberán comprobarse en la PR concreta y sobre el SHA posterior a cualquier fusión. No se declara cierre global de IVTFF ni de procedencia histórica.
