# Auditoría de seguridad de publicación de resultados — 2026-10-21

## Alcance y método

Se inspeccionaron directamente desde GitHub los 31 archivos de `.github/workflows/` presentes en la rama `master` del repositorio `kyrian20/voynich-autoexploration`. Inventario tomado del árbol Git de `master`, commit base `ace0a937ded0e7b997300cfb64e3c421c750dc51`.

Esta auditoría se limita a la estructura de los workflows y sus pasos de publicación. **No demuestra que los experimentos sean científicamente correctos ni que sus últimas ejecuciones hayan terminado bien.**

## Hallazgos comprobados

- Workflows inspeccionados: **31**.
- Workflows con `contents: write` y paso `git push`: **30**.
- Workflow de solo lectura identificado: `voynich-check.yml`.
- Ocho workflows EXP-604 a EXP-611 no declaran bloque `concurrency` y publican resultados con un `git push` directo, sin fetch/rebase/reintento en su paso de commit:
  - `.github/workflows/voynich-exp604.yml`
  - `.github/workflows/voynich-exp605.yml`
  - `.github/workflows/voynich-exp606.yml`
  - `.github/workflows/voynich-exp607.yml`
  - `.github/workflows/voynich-exp608.yml`
  - `.github/workflows/voynich-exp609.yml`
  - `.github/workflows/voynich-exp610.yml`
  - `.github/workflows/voynich-exp611.yml`
- Otros workflows escritores sí tienen concurrencia, pero la mayoría utiliza grupos distintos. **Grupos distintos no serializan entre sí**, por lo que la presencia de `concurrency` por sí sola no protege frente a una carrera con otro workflow.
- `voynich-agent.yml` y `voynich-exp603.yml` se han actualizado para compartir `voynich-master-writes`; los cambios se verificaron volviendo a leer los archivos desde GitHub.
- No se debe asignar a todos los escritores un único grupo compartido sin diseñar la cola: GitHub mantiene como máximo una ejecución pendiente por grupo y una nueva pendiente puede reemplazar a la anterior. Una falsa “solución” podría descartar ejecuciones en cola.

## Cambios ya publicados

1. `voynich-exp603.yml`: grupo `voynich-master-writes`, comprobación de cambios y reintentos de publicación tras rebase; sin force-push.
2. `voynich-agent.yml`: grupo compartido `voynich-master-writes`; conserva su lógica de rebase/reintentos.
3. Este registro: ampliación de alcance, inventario y riesgo operativo específico de EXP-604–611.

Commits previos:
- EXP-603: [0dc539e7e1ce3bc9f637e560868cf64fcdac3c23](https://github.com/kyrian20/voynich-autoexploration/commit/0dc539e7e1ce3bc9f637e560868cf64fcdac3c23)
- Agente autónomo: [7802eb9fa03d45bd1854fa88535336c1aade4144](https://github.com/kyrian20/voynich-autoexploration/commit/7802eb9fa03d45bd1854fa88535336c1aade4144)

## Riesgos y siguientes acciones

1. Corregir EXP-604–611 para que una carrera de push no termine simplemente en error: obtener el estado actual de `origin/master`, rebasar con control de errores y reintentar el push con un límite. Si aparece un conflicto real, detenerse y conservar el fallo visible; no resolver automáticamente contenido científico.
2. Revisar individualmente la estrategia de publicación de los otros 22 workflows escritores. No cambiar sus grupos a ciegas ni ocultar ejecuciones fallidas.
3. Revisar ejecuciones y logs de Actions: el commit y la lectura posterior verifican el contenido publicado, **no** la ejecución de CI.
4. Ejecutar pruebas de humo y comparar los artefactos resultantes con fuentes, hashes y protocolos.
5. Preservar todos los IDs históricos y los resultados originales. No reasignar EXP-623 ni crear IDs nuevos hasta reconciliar el registro de GitHub con la Biblioteca.

## Estado

**PARCIAL.** Inventario de workflows completado; el defecto concreto de publicación de EXP-604–611 está identificado pero aún no corregido; la verificación de ejecuciones reales de Actions y la auditoría científica siguen pendientes.
