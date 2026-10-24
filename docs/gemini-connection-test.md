# Diagnóstico manual de conexión a Gemini

Corrección operativa del 24-10-2026. No es un experimento científico.
La ejecución [#6](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40101038930)
(commit `3ade29294582f42ad0d8a5d4e28a58c21b886b26`) devolvió HTTP 404 en
`generateContent` con `gemini-2.5-flash`. El código HTTP por sí solo no demuestra
retirada del modelo, invalidez de la clave ni problemas de facturación.

## Procedimiento corregido

El workflow `.github/workflows/gemini-smoke-test.yml` sigue siendo exclusivamente
manual, sin checkout, dependencias, corpus ni archivos de investigación.
No cambia `GEMINI_API_KEY`: la usa solo en la cabecera HTTPS `x-goog-api-key`.
TLS permanece activo. No hay redirecciones ni reintentos.

1. GET `https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000`,
   recorriendo `nextPageToken` (máximo diez páginas; repetición o límite abortan).
2. Filtrar por `supportedGenerationMethods` que contenga `generateContent` y una
   lista explícita de modelos Flash de texto documentados. Preferencia:
   `gemini-3.8-flash`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`.
   No se prueban modelos desconocidos, audio, imagen, embeddings ni Live.
   El artefacto contiene solo los nombres de esa lista disponibles para la clave,
   nunca el catálogo bruto ni descripciones. Si ninguno aparece, abortar.
3. GET `models/{seleccionado}` para comprobar nombre, método, `inputTokenLimit`
   entero >=32 y `outputTokenLimit` entero >=1024. Si falla, cero POST.
4. Un único POST `models/{seleccionado}:generateContent` con el texto fijo
   `Reply with exactly OK.` y `generationConfig: {maxOutputTokens: 1024}`.
   Se conservan los valores por defecto de pensamiento, temperatura y candidaturas.
   Se elimina `thinkingBudget: 0`, que no es portable entre familias. El presupuesto
   de salida incluye pensamiento; agotarlo sin respuesta no verifica la conexión.
   No hay modelo alternativo después del POST ni segunda generación.

Solo una respuesta de texto exactamente `OK` tras retirar espacios marca `connected`.
El artefacto de siete días guarda estado, etapa, modelo elegido, modelos de texto
admitidos disponibles, parámetros comprobados, número de GET y número de intentos
de generación, ausencia de datos del manuscrito y código/categoría HTTP si procede.
No se muestran cuerpos remotos, excepciones, cabeceras, claves ni tokens de página.
Las categorías HTTP son etiquetas fijas y no establecen causas: 400 `bad_request`,
401 `authentication_error`, 403 `permission_denied`, 404 `not_found`,
408 `request_timeout`, 429 `rate_limit_or_quota`, otros 4xx `client_error`,
5xx `server_error`, 3xx `redirect_blocked`.

## Fuentes oficiales consultadas

- [Models: list, get y metadatos](https://ai.google.dev/api/models).
- [Catálogo de modelos de Gemini](https://ai.google.dev/gemini-api/docs/models).
- [generateContent y GenerationConfig](https://ai.google.dev/api/generate-content).
- [Pensamiento y diferencias entre modelos](https://ai.google.dev/gemini-api/docs/thinking).

El catálogo general de la documentación no demuestra acceso de nuestra clave;
solo las consultas autenticadas del workflow permiten comprobarlo. Los metadatos
verifican método y límites, no todos los parámetros posibles: por eso se envía
únicamente el límite de salida y se conservan los demás valores por defecto.

## Ejecución y alcance

Ejecutar manualmente el workflow una sola vez sobre la rama de la PR y comprobar
el commit, el resultado y el artefacto antes de afirmar conexión verificada.
El workflow ya existe en `master`; se puede seleccionar la rama sin fusionar la PR.
No usar Re-run: sería otra generación. Los GET de descubrimiento no son pruebas
de generación. La consulta puede consumir cuota o generar cargos según la cuenta.
Un timeout no demuestra que Google no procesara la petición.

Las pruebas locales ejecutan el Python embebido con transporte simulado y nunca
llaman a Google. No validan acceso remoto, cuota, facturación ni ciencia.

## Historial de validación anterior (no describe el procedimiento actual)

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
