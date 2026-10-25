# Coordinación de herramientas — estado verificado 25-10-2026

## Reparto de funciones
- GitHub: fuente de código, protocolos, resultados, correcciones y comprobaciones.
- Linear: tareas y bloqueos con enlaces al commit/resultado; sin copiar conclusiones no verificadas como hechos.
- Gemini: revisión metodológica crítica de un paquete delimitado; su respuesta es propuesta no verificada. No es anotador visual ciego ni validación científica independiente por persona.
- Asistente: integra evidencia, ejecuta pruebas y adjudica propuestas con sus límites.

## Estado real de esta sesión
GitHub: acceso confirmado.
Linear: búsqueda de integración devuelve installed=false; se ha solicitado su incorporación, pero no se ha confirmado instalación o conexión. No se han creado tareas.
Gemini: el run histórico 40133431957, intento 1, fue success. Se solicitó un reintento autorizado, intento 2, job 121294785609; falló antes de API por FileNotFoundError.
El flujo de ese run descargaba el prompt 2026-10-24-gemini-ch-sh-review-prompt.md, mientras el programa actual espera 2026-10-25-gemini-ch-sh-review-prompt-v2.md.
No hay respuesta Gemini nueva de este intento. No reintentar ese run antiguo.
El workflow vigente gemini-methodological-review.yml ya descarga y comprueba el prompt v2; se requiere un workflow_dispatch nuevo desde master. La conexión utilizada no expone dispatch nuevo, solo reintentos.
No se ha cambiado configuración para lanzar llamadas repetidas ni solicitado acceso a secretos.

## Acción pendiente mínima
1. Instalar/conectar Linear y confirmar acceso; entonces identificar proyecto existente antes de crear tareas para evitar duplicados.
2. Abrir https://github.com/kyrian20/voynich-autoexploration/actions/workflows/gemini-methodological-review.yml y lanzar una ejecución NUEVA sobre master, modelo gemini-3.8-flash (modelo de la ejecución histórica comprobada; compatibilidad actual pendiente de nueva respuesta).
3. Comprobar job, recibo, hash del prompt, estado de esquema y artefacto antes de considerar Gemini operativo.
Un success de Actions o esquema JSON válido no valida metodología ni desciframiento.

## Primera tarea prevista en Linear, todavía no creada
Título: Verificar nueva revisión Gemini v2 y adjudicar propuestas.
Criterio de cierre: enlace a ejecución nueva y recibo, prompt y modelo exactos; inventario de recomendaciones aceptadas/rechazadas con razones; ninguna propuesta pasa automáticamente a afirmación científica.
Bloqueos: conexión Linear y dispatch nuevo. La revisión ch/sh existente es metodológica y no reabre experimentos sin una pregunta discriminante y prerequisitos satisfechos.

## Evidencia
- Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/40133431957
- Job fallido intento 2: https://github.com/kyrian20/voynich-autoexploration/actions/runs/40133431957/job/121294785609
- Workflow actual: .github/workflows/gemini-methodological-review.yml
- Programa actual: scripts/request_gemini_review.py
No afirmar que las tres herramientas trabajan coordinadas hasta verificar los dos bloqueos pendientes.
