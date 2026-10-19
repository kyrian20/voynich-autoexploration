# Diagnóstico del error 403 de la integración GitHub

Fecha: 2026-10-19

La integración puede leer `.github/workflows/voynich-agent.yml`, pero anteriormente una llamada de consulta de permisos y un intento de creación de archivo devolvieron HTTP 403 `Resource not accessible by integration`.

Esta prueba comprueba si la conexión de GitHub ya dispone de permiso de escritura. Si el archivo se crea, la operación queda registrada en el historial del repositorio. El flujo autónomo existente requiere además el secreto `OPENAI_API_KEY`; ese requisito es independiente de los permisos de escritura.
