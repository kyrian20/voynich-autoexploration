# Auditoría de seguridad de publicación de resultados — 2026-10-21

## Alcance y método

Se inspeccionaron directamente desde GitHub los 31 archivos de `.github/workflows/` en `master` del repositorio `kyrian20/voynich-autoexploration`. Árbol inicial: `ace0a937ded0e7b997300cfb64e3c421c750dc51`.

La auditoría cubre estructura de workflows y estrategia de publicación. **No demuestra que los experimentos sean científicamente correctos ni que las últimas ejecuciones de Actions hayan terminado bien.**

## Inventario comprobado

- Workflows inspeccionados: **31**.
- Workflows con `contents: write` y `git push`: **30**.
- Workflow de solo lectura: `voynich-check.yml`.
- Los escritores no comparten todos el mismo grupo de concurrencia. Grupos diferentes no serializan entre sí.
- No se impuso un grupo global indiscriminadamente: GitHub permite una sola ejecución pendiente por grupo y una nueva pendiente puede reemplazar a otra, con riesgo de descartar ejecuciones en cola.

## Cambios publicados

1. **EXP-603**: grupo `voynich-master-writes`, comprobación de cambios y reintentos de publicación tras rebase; sin force-push.
2. **Agente autónomo**: mismo grupo `voynich-master-writes`; conserva su lógica de rebase/reintentos.
3. **EXP-604 a EXP-611**: los ocho workflows se actualizaron para hacer fetch explícito de `origin/master`, rebasar el commit de resultados, intentar publicar hasta cinco veces y esperar progresivamente entre fallos de push. Si aparece un conflicto de rebase, el workflow se detiene y falla de forma visible; no se sobrescriben resultados ni se fuerza el push.
4. **Auditoría actualizada** con los cambios y las limitaciones.

Los ocho archivos EXP-604–611 se volvieron a leer desde GitHub y se comprobaron estos marcadores: fetch explícito, rebase, bucle de cinco intentos, parada ante conflicto y ausencia de force-push. Después se comprobaron los runs de Actions: los runs finales de EXP-604, 605, 606, 607, 608, 609, 610 y 611 terminaron en `success`, incluido el paso `Commit results`. Runs finales: [604](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673400827), [605](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673408627), [606 corregido](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673786598), [607](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673423239), [608](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673435096), [609](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673443142), [610](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673449155), [611](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39673455023).

Commits finales de corrección de indentación de los workflows: [EXP-604](https://github.com/kyrian20/voynich-autoexploration/commit/997cdf80a19b0f61df1ac3026afd699420636983), [EXP-605](https://github.com/kyrian20/voynich-autoexploration/commit/7ac67ced65bbbef7e341446c8550ffabaefe5db1), [EXP-606 workflow](https://github.com/kyrian20/voynich-autoexploration/commit/7402eccfda863128a4f2e4fe4046236a08548cbb), [EXP-607](https://github.com/kyrian20/voynich-autoexploration/commit/4d65d8092b6b799580aef9c0a241c30def3b45ed), [EXP-608](https://github.com/kyrian20/voynich-autoexploration/commit/e1fed66111d9b7d8ad0d0a275820ac0ba9dc4df2), [EXP-609](https://github.com/kyrian20/voynich-autoexploration/commit/610e2d65fff83f728d855897faea05abf65d908c), [EXP-610](https://github.com/kyrian20/voynich-autoexploration/commit/47c161ad1d41c925613841f086e7527157df1c47), [EXP-611](https://github.com/kyrian20/voynich-autoexploration/commit/974eda81935e6f98957b59991449e953e33dc6ea). EXP-606 recibió además correcciones de metadatos y filtrado: [parser `$L`](https://github.com/kyrian20/voynich-autoexploration/commit/65f6b4cbe52c46cb23a0946994d4f95dfcb64660), [importación en Actions](https://github.com/kyrian20/voynich-autoexploration/commit/cb8f3b6311bc55764ea9eb91247e25206de5d1d7), [comparación solo en bordes elegibles](https://github.com/kyrian20/voynich-autoexploration/commit/49345b20ae86de4a60ab0bda820f54a7bb1febb2).
- [EXP-603](https://github.com/kyrian20/voynich-autoexploration/commit/0dc539e7e1ce3bc9f637e560868cf64fcdac3c23)
- [Agente autónomo](https://github.com/kyrian20/voynich-autoexploration/commit/7802eb9fa03d45bd1854fa88535336c1aade4144)

## Riesgos y siguientes acciones

1. Revisar individualmente la estrategia de publicación de los otros workflows escritores; no cambiar grupos a ciegas ni ocultar ejecuciones fallidas.
2. Los runs finales EXP-604–611 están verificados en verde, pero las versiones intermedias con indentación YAML incorrecta fallaron y se conservan en el historial. La corrección se hizo inmediatamente y los ocho runs finales terminaron correctamente.
3. Ejecutar pruebas de humo y comparar artefactos con fuentes, hashes y protocolos; un workflow verde solo confirma que el script y la publicación finalizaron según su propio protocolo, no la validez científica de la hipótesis.
4. Preservar IDs y resultados históricos. No reasignar EXP-623 ni crear IDs nuevos hasta reconciliar el registro de GitHub con la Biblioteca.

## Estado

**PARCIAL, con mejora verificada.** Inventario de 31 workflows completado; EXP-603 y EXP-604–611 tienen defensas de publicación mejoradas y los ocho runs finales EXP-604–611 están en verde. Sigue pendiente auditar los otros workflows escritores y continuar la auditoría científica.
