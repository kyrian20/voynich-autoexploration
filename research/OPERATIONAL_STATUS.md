# Estado operativo del repositorio — 22-10-2026

Estado: **infraestructura reparada y ejecución verificada para los workflows modificados**. La validez científica de todos los experimentos históricos sigue sin estar certificada.

## Publicación y permisos

- 32 workflows inventariados: un publicador (`voynich-agent.yml`) y 31 lectores (análisis con artefactos o comprobaciones).
- Se retiró la publicación directa de 29 workflows históricos. Sus análisis siguen ejecutándose y guardan artefactos durante 90 días; sus resultados versionados anteriores siguen en Git. La revisión de un artefacto y su incorporación posterior deben ser explícitas.
- El publicador conserva la programación diaria a las 08:00 UTC, limita ejecución y push a `master`, descarga historial completo y aborta los conflictos de rebase. Sube artefactos antes de publicar. Nunca fuerza un push.
- Un único publicador elimina la competencia entre workflows escritores de este inventario. Los cambios humanos o del conector aún pueden causar conflictos: se rechazan y los resultados quedan en artefactos.
- CI ahora rechaza escritores adicionales, comandos de publicación en lectores, force-push y claves YAML duplicadas. No modifica secretos ni necesita crédito API.

## Verificación ejecutada

- 34 comandos de análisis/auditoría de los 30 workflows modificados: retorno cero local. Comandos exactos, tiempos y hashes de logs en [summary.json](operations/2026-10-22/summary.json).
- Los pasos ejecutables de Voynich Check pasaron localmente: [check-summary.json](operations/2026-10-22/check-summary.json).
- 587 archivos Python analizados sintácticamente, 88 JSON leídos y un JavaScript comprobado: cero errores de formato. Esto no ejecuta los 624 experimentos históricos ni valida sus interpretaciones.
- GitHub: los 29 workflows históricos modificados terminaron en éxito, contando la corrección de EXP-603 en su run posterior. El publicador también terminó en éxito: [39744139697](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39744139697).
- Voynich Check del commit de corrección `7d3b903a7d4be7767f3b841beca29de3e28f7470`: [39744302807](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39744302807), éxito. EXP-603 corregido: [39744302712](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39744302712), éxito.
- El fallo inicial de EXP-603 por clave `with` duplicada se conserva como fallo histórico; no se presenta como éxito. La prueba nueva demuestra que ese patrón se rechaza.
- El workflow aislado EXP-623 no cambió en esta reparación; su reproducción anterior se documenta en [el informe comparativo](reproduction/EXP623_REPRODUCTION_COMPARISON_2026-10-22.md). No se cuenta como una ejecución nueva de este ciclo.

## Identidad de experimentos

[EXPERIMENT_PATH_REGISTRY.json](EXPERIMENT_PATH_REGISTRY.json) registra 624 identificadores canónicos únicos basados en ruta completa y 617 alias numéricos. Los siete números repetidos (177, 594, 596, 597, 600, 601, 602) conservan todos sus directorios. CI comprueba la correspondencia entre registro y carpetas.

Esto resuelve la identificación inequívoca de carpetas para herramientas nuevas. No reescribe referencias numéricas históricas ambiguas ni sustituye la reconciliación de contenido con la Biblioteca. Los IDs nuevos siguen congelados mientras se completa esa revisión científica/archivística.

## Las nueve filas de diferencia

El cotejo exacto de IDs confirma 5.385 registros brutos no vacíos frente a 5.376 líneas con tokens bajo el filtro histórico. Las nueve exclusiones son `f49v.11`, `.21`, `.27`, `.29`, `.35`, `.41`, y `f66r.24`, `.38`, `.42`. Sus cuerpos contienen códigos extendidos `@…;`, más un comentario en un caso. El filtro ASCII no los decodifica; no son registros ausentes ni prueba de que carezcan de caracteres manuscritos. Cuerpos e índices originales en [record-and-workflow-audit.json](operations/2026-10-22/record-and-workflow-audit.json).

Se corrigió además el generador EXP-590: las advertencias sobre selección exploratoria y la comparación de cobertura ahora se generan desde código y no dependen de ediciones manuales que la próxima ejecución borraría. Los recuentos y el contraste de permutación permanecen idénticos.

## Autoauditoría del alcance

- Selección del objetivo: no se ha seleccionado una nueva hipótesis lingüística ni ajustado parámetros para mejorar un resultado.
- Destrucción de información: persisten limitaciones conocidas del filtro ASCII, ligaduras e incertidumbre IVTFF; el éxito operativo no las valida.
- Extrapolación: las comprobaciones cubren formatos, configuración y ejecución indicados; no todos los experimentos históricos.
- Resultados negativos: ningún retorno cero se convierte en respaldo de una hipótesis científica; los resultados negativos previos se conservan.
- Controles: no se introducen ni reinterpretan nulos en esta reparación; los parámetros de los comandos existentes se conservaron. El cotejo de EXP-590 verifica igualdad de métricas y permutaciones, no una prueba confirmatoria nueva.

## Pendientes científicos explícitos

Conformidad independiente completa IVTFF; representación de códigos extendidos, ligaduras y alternativas; equivalencia por bytes y procedencia de todos los pares Biblioteca/GitHub; revisión de referencias históricas ambiguas y validación de conclusiones. No hay desciframiento validado. Estos pendientes no bloquean ejecutar los análisis existentes como exploratorios.

Los informes anteriores de concurrencia describen la arquitectura antigua de 30 escritores; esta sección los sustituye respecto a permisos y publicación. La CI de cada commit posterior debe comprobarse separadamente.

Archivo de logs: [execution-logs.zip](operations/2026-10-22/execution-logs.zip). SHA-256: `5970815b019af20e6eee1a04f4addc220f201ca3020a5c4ecda52e8626f7e849`.
