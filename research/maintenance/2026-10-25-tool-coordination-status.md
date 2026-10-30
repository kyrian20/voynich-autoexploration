# Coordinación de herramientas — estado verificado 25-10-2026

**Actualización que sustituye los bloqueos históricos de abajo:** GitHub y Linear operativos; Gemini ha devuelto una revisión real validada de esquema y procedencia en intento 4 del run 40235310859, job 121298599069. JUA-7 cerrado con evidencia. Modelo efectivo gemini-3.8-flash, sin fallback en esa ejecución. [Respuesta y adjudicación](../external-reviews/2026-10-25-gemini-v2/REVIEW.md). La selección de experimento JUA-9 continúa abierta. Disponibilidad futura y validez científica no quedan garantizadas.

Las secciones siguientes conservan la cronología anterior; sus bloqueos de conexión ya no describen el estado actual.

## Reparto de funciones
- GitHub: fuente de código, protocolos, resultados, correcciones y comprobaciones.
- Linear: tareas y bloqueos con enlaces al commit/resultado; sin copiar conclusiones no verificadas como hechos.
- Gemini: revisión metodológica crítica de un paquete delimitado; su respuesta es propuesta no verificada. No es anotador visual ciego ni validación científica independiente por persona.
- Asistente: integra evidencia, ejecuta pruebas y adjudica propuestas con sus límites.

## Estado real de esta sesión
GitHub: acceso confirmado.
Linear: conexión confirmada posteriormente en esta misma sesión. Se localizó el proyecto existente Investigación del manuscrito Voynich y se actualizaron JUA-7 y JUA-9 con enlaces verificables, conservando sus descripciones y sin cerrar trabajo pendiente. No se crearon duplicados.
Gemini: el run histórico 40133431957, intento 1, fue success. Se solicitó un reintento autorizado, intento 2, job 121294785609; falló antes de API por FileNotFoundError.
El flujo de ese run descargaba el prompt 2026-10-24-gemini-ch-sh-review-prompt.md, mientras el programa actual espera 2026-10-25-gemini-ch-sh-review-prompt-v2.md.
No hay respuesta Gemini nueva de este intento. No reintentar ese run antiguo.
El workflow vigente gemini-methodological-review.yml ya descarga y comprueba el prompt v2; se requiere un workflow_dispatch nuevo desde master. La conexión utilizada no expone dispatch nuevo, solo reintentos.
No se ha cambiado configuración para lanzar llamadas repetidas ni solicitado acceso a secretos.

## Acción pendiente mínima
1. Linear operativo; seguimiento de Gemini en https://linear.app/kyrian20/issue/JUA-7/verificar-la-conexion-con-gemini-mediante-una-prueba-minima y selección científica en JUA-9.
2. Abrir https://github.com/kyrian20/voynich-autoexploration/actions/workflows/gemini-methodological-review.yml y lanzar una ejecución NUEVA sobre master, modelo gemini-3.8-flash (modelo de la ejecución histórica comprobada; compatibilidad actual pendiente de nueva respuesta).
3. Comprobar job, recibo, hash del prompt, estado de esquema y artefacto antes de considerar Gemini operativo.
Un success de Actions o esquema JSON válido no valida metodología ni desciframiento.

## Seguimiento en Linear — actualizado en JUA-7
Título: Verificar nueva revisión Gemini v2 y adjudicar propuestas.
Criterio de cierre: enlace a ejecución nueva y recibo, prompt y modelo exactos; inventario de recomendaciones aceptadas/rechazadas con razones; ninguna propuesta pasa automáticamente a afirmación científica.
Bloqueo restante: dispatch nuevo de Gemini. Linear ya está conectado. La revisión ch/sh existente es metodológica y no reabre experimentos sin una pregunta discriminante y prerequisitos satisfechos.

## Evidencia
- Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/40133431957
- Job fallido intento 2: https://github.com/kyrian20/voynich-autoexploration/actions/runs/40133431957/job/121294785609
- Workflow actual: .github/workflows/gemini-methodological-review.yml
- Programa actual: scripts/request_gemini_review.py
No afirmar que las tres herramientas trabajan coordinadas hasta verificar los dos bloqueos pendientes.
