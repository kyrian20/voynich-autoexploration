# Punto de reanudación y auditoría acotada — 26-10-2026

## Estado guardado

Base auditada: b0d84dab43ea57e305b5909de0d5b96d618aa25e, Python3.12.14. No hay traducción validada ni admisión semántica de f68r3. No se certifica todo el historial.

## Correcciones realizadas en esta rama

1. Inventario astronómico: separar total5385, páginas numéricas5225 y fRos160 en ZL3b; IT2a5215/5215/0. Conservar todas las coincidencias originales. Cambiar autocalificación del CLI a GENERATED y exigir comparación para REPRODUCED. Sustituir assert del locus por rechazo explícito operativo también con -O. Véase ../../decipherment/2026-10-26-astronomical-anchor/COUNT_CORRECTION.md.
2. Conectar las ocho pruebas específicas y reproducción doble a Voynich Check con artefacto. Configuración añadida; éxito remoto de esta rama pendiente de comprobar.
3. Originales inventory.json/VERIFICATION.json y resultados negativos preservados; se añaden artefactos v2 con hashes.

## Duplicación corregida en GitHub

La PR65 presentaba como nueva la recuperación Met19.68.1, aunque ../../decipherment/2026-10-26-documentary-context/REPORT.md ya la contenía en master. Se cerró sin fusionar, conservando rama e historial y enlazando el informe canónico. La PR66 sigue en borrador y su descripción aclara el alcance de los nuevos localizadores de herbarios/baños. No se demuestra secuencia compartida ni relación textual.

Enlaces: https://github.com/kyrian20/voynich-autoexploration/pull/65 y https://github.com/kyrian20/voynich-autoexploration/pull/66 .

## Verificación ejecutada

Suite tests/:304 ejecutadas,303 aprobadas y1 omitida por input histórico ausente. Ocho pruebas de ancla pasan en modo normal y optimizado; dos JSON nuevos idénticos. Auditoría operativa pasa; identidad de14 corpus comprobada con cero errores y cuarentena histórica conservada. Logs de esta carpeta y VERIFICATION-v2.json registran evidencia. La suite general no descubre las pruebas del ancla: por eso se ejecutan además y se añaden a CI.

CI de la base comprobada: https://github.com/kyrian20/voynich-autoexploration/actions/runs/40243966089 , push del SHA b0d84dab43ea57e305b5909de0d5b96d618aa25e, completado success. Esa CI no acredita los cambios nuevos. PR65 tuvo CI success antes de ser cerrada por redundancia, lo que ilustra que CI no detecta duplicación científica.

## Herramientas y límites

Codex ejecutó estas comprobaciones en un checkout local fijo. GitHub permitió lectura y gestión de PR. Linear permitió lecturas anteriores, pero get_agent_context devolvió Tool not found en esta sesión; cualquier escritura posterior se debe verificar por separado.

Se revisó la respuesta Gemini archivada en research/external-reviews/2026-10-25-gemini-v2/. El recibo conserva SCHEMA_VALID_ONLY/PROPOSED_UNVERIFIED y una generación gemini-3.8-flash. Su REVIEW.md ya advierte que confundía Currier $L con manos; no se adopta ese error ni se cuenta la lectura de la respuesta como nueva revisión independiente. GEMINI_API_KEY no está disponible en este entorno y el conector GitHub expuesto no ofrece dispatch de workflows. No se hizo una llamada nueva.

## Publicación bloqueada

La revisión automática rechazó el comando que iba a fetch/commit/push por requerir autorización específica para enviar código, informes y logs a https://github.com/kyrian20/voynich-autoexploration . No se reintenta por otro transporte. Se conserva una rama y commit locales con toda la corrección; la publicación y su CI requieren resolver este bloqueo. Las gestiones previas de PR65/66 sí fueron confirmadas por el conector.

## Registro en Linear confirmado

JUA-11 se actualizó mediante parche de texto: corrección de los denominadores, ocho pruebas específicas y publicación pendiente. La respuesta del servicio confirmó el contenido actualizado y el estado Todo; no se cerró la tarea semántica. URL: https://linear.app/kyrian20/issue/JUA-11/adjudicar-transcripcion-y-referente-independiente-del-candidato-f68r3 .

## Orden de continuación

Primero comprobar el SHA y CI de esta reparación, revisar diff y posible concurrencia antes de integrar. Después, para la PR66, recuperar imágenes de comparadores y contrastar rasgos específicos con alternativas sin puntuar como ausente lo que un catálogo omite. Consultar el informe documental previo antes de repetir búsquedas. La falta de transcripción/identificación independientes mantiene bloqueada la prueba semántica; más ejecuciones o modelos no sustituyen esas entradas.

Esta sesión es acotada; este punto de reanudación no acredita trabajo continuo durante la noche ni una nueva tarea programada.
