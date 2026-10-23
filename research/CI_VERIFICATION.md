# Verificar CI sin omitir ejecuciones push

Corrección del procedimiento de consulta, 23-10-2026.

La herramienta `fetch_commit_workflow_runs` utilizada en mensajes anteriores filtra actualmente a eventos pull_request. Una lista vacía de esa herramienta no permite determinar el estado de ejecuciones push en master. La consulta de estados clásicos tampoco sustituye a las ejecuciones de Actions. Las frases anteriores «pendiente de confirmar» describían una limitación de mi verificación, no un fallo observado del workflow.

Usar la colección completa de GitHub Actions, filtrada al SHA exacto:

`GET /repos/kyrian20/voynich-autoexploration/actions/runs?head_sha=SHA&per_page=100`

En el conector actual se puede consultar esa URL mediante `github_fetch`. Revisar todas las páginas si total_count supera el número de elementos recibidos. Comprobar head_sha, nombre/path del workflow, evento, status, conclusion, run_attempt, ID/URL y jobs. Solo completed/success confirma una ejecución satisfactoria. Una lista vacía completa indica ausencia de ejecuciones devueltas; una respuesta filtrada o incompleta no prueba ausencia.

## Evidencia comprobada

| Commit | Evento | Voynich Check | Resultado |
|---|---|---|---|
| ef1ad57738d7cef979b1f28d9513af9f7746bd4c | push | [39926663273](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39926663273) | completed/success |
| 34b9beb89e397e5dd38efc56720e2aa1ab0b5ba0 | push | [39937412849](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39937412849) | completed/success |
| a0471a1b3cd5affd7965f2607afd12a3047ec63d | push | [39938265601](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39938265601) | completed/success; job y pasos success |

No se modificó la configuración para obtener estos éxitos ni se relanzaron ejecuciones: ya existían. Esto cierra la incertidumbre de verificación de los dos bloques científicos recientes y del recibo anterior. No certifica toda la investigación histórica; los commits posteriores requieren su propia comprobación.
