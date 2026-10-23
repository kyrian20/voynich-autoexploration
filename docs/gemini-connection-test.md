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
Los errores HTTP incluyen además una categoría fija tanto en el log como en
el artefacto. Por ejemplo:
`Gemini connection test status: http_error; http_status=403; error_category=permission_denied`.

| HTTP | Categoría |
| --- | --- |
| 400 | `bad_request` |
| 401 | `authentication_error` |
| 403 | `permission_denied` |
| 404 | `not_found` |
| 408 | `request_timeout` |
| 429 | `rate_limit_or_quota` |
| Otros 4xx | `client_error` |
| 5xx | `server_error` |
| 3xx | `redirect_blocked` |
| Otros códigos | `unexpected_http_status` |

Las categorías clasifican el código HTTP; no confirman una causa específica.
No se lee el cuerpo de errores HTTP ni se registra su mensaje, cabeceras o URL.
El script Python sigue embebido en el workflow para conservar la ausencia de
checkout. `tests/test_gemini_smoke.py` ejecuta ese mismo script con el transporte
simulado, sin conexiones de red; la CI habitual ejecuta estas pruebas.
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

## Regresión del diagnóstico HTTP — 24-10-2026

Pruebas automatizadas añadidas en `tests/test_gemini_smoke.py`, ejecutadas también
por Voynich Check. Cubren 400/401/403/404/408/429, otro 4xx, cuatro 5xx,
302/307 y un código fuera de las familias previstas; comprueban salida y
artefacto exactos, una sola llamada, cierre del error sin leer su cuerpo y
ausencia de una marca sensible inyectada en clave, URL, cabeceras y mensaje.
También cubren éxito, timeout, error de transporte, JSON inválido, respuesta
inesperada, secreto ausente y rechazo de redirecciones.

Python 3.12.14: suite completa de 153 pruebas, una omitida (la base tenía
148 pruebas, una omitida). Auditoría operativa, identidad de corpus y
`git diff --check`: satisfactorios. Sin petición real a Gemini ni reproducción
de experimentos históricos; esta corrección es exclusivamente operativa.
