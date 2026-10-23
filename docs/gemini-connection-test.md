# Prueba manual de conexión a Gemini

Prueba operativa, sin experimento científico ni incorporación de Gemini como
investigador. No modifica ni envía manuscrito, corpus, resultados o estado científico.

## Funcionamiento y seguridad

`.github/workflows/gemini-smoke-test.yml` solo admite `workflow_dispatch`.
No se ejecuta por push, PR ni programación. No hace checkout ni instala dependencias.
El secreto existente `GEMINI_API_KEY` se entrega únicamente al paso de consulta como
variable de entorno, y se envía como cabecera `x-goog-api-key` por HTTPS con
validación TLS a la API REST oficial de Google:
`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent`.
No aparece en URL, argumentos, archivos, logs ni artefactos.

Cada ejecución manual hace como máximo un POST con el texto fijo
`Reply with exactly OK.`, una candidatura, máximo 32 tokens de salida y pensamiento
desactivado. No hay reintentos, redirecciones, modelo alternativo ni otras consultas.
Una respuesta exactamente `OK` tras retirar espacios indica `connected`.
Ni el cuerpo de respuesta ni las excepciones se imprimen o archivan.
El artefacto de siete días contiene solo estado, modelo, número de intentos,
ausencia de datos del manuscrito y, si está disponible, código HTTP.
El token de GitHub tiene solo permiso explícito `contents: read` conforme al auditor
del proyecto; no hay escrituras al repositorio.

## Ejecución y límites

GitHub exige que el workflow con `workflow_dispatch` exista en la rama
predeterminada para aceptar una ejecución manual. Mientras solo esté en esta rama
independiente, la conexión real queda pendiente. No fusionar con `master` sin
autorización. Tras una incorporación autorizada: Actions → Gemini manual connection
test → Run workflow, una sola vez. Comprobar el estado y el artefacto de esa ejecución
antes de afirmar que la conexión funciona. No pulsar Re-run: generaría otra consulta.

Los secretos de Actions no se pueden leer desde esta sesión. Su existencia declarada
por el usuario no prueba su validez, acceso al modelo, cuota o configuración de pago.
La disponibilidad de `gemini-2.5-flash` debe verificarse mediante la prueba; no se ha
consultado el catálogo ni se garantiza su vigencia. Un 400 puede indicar parámetros
incompatibles; 401/403, autenticación o permisos; 404, modelo no disponible; 429,
cuota; 5xx, servicio remoto. No se reintenta automáticamente en ningún caso.
Un timeout puede ocurrir después de que Google procese la solicitud: no permite
asegurar que no hubo consumo. Una cancelación abrupta puede impedir el artefacto.

La llamada puede consumir cuota gratuita o generar un cargo según la cuenta de
Google y sus tarifas vigentes; los límites de tokens no garantizan coste cero.
También puede consumir minutos/almacenamiento de Actions según el plan de GitHub.
No hay presupuesto automático, ni gasto periódico, ni tareas de investigación
activadas. Cualquier ejecución manual adicional vuelve a consumir cuota.

Referencias oficiales: [API generateContent](https://ai.google.dev/api/generate-content),
[claves](https://ai.google.dev/gemini-api/docs/api-key),
[precios](https://ai.google.dev/gemini-api/docs/pricing),
[ejecución manual de Actions](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/manually-running-a-workflow).

## Validación local — 23-10-2026

Base revisada: `4488441c840337d9e6708b2b31916429f1e3808a` de `master`.
Python 3.12.14 y PyYAML 6.0.3. YAML analizado con el lector de claves únicas
del auditor del proyecto; comprobados trigger exclusivamente manual, permisos
y sintaxis del Python embebido. Seis casos con transporte simulado: éxito,
respuesta inesperada, JSON inválido, HTTP 403, timeout y secreto ausente.
Verificados número de intentos, destino y texto fijos, ausencia de secreto en logs
y artefacto, y rechazo de redirecciones. Ninguna prueba local llama a Google.

`python -m unittest discover -s tests -v`: 146 pruebas, una omitida.
`python scripts/audit_repository_operations.py` y
`python scripts/check_corpus_integrity.py`: satisfactorios; auditor operativo
repetido con el workflow nuevo. `git diff --check`: satisfactorio.
No se pudo descargar `actionlint` por fallo de conexión al proxy del entorno;
no se afirma validación con esa herramienta ni ejecución satisfactoria de Actions.
No se han reproducido los experimentos históricos ni validado conclusiones
científicas. Conexión real, secreto, modelo y facturación pendientes de la
ejecución manual tras incorporación autorizada del workflow a la rama predeterminada.
