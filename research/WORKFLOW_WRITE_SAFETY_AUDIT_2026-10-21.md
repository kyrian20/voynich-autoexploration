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

Los ocho archivos EXP-604–611 se volvieron a leer desde GitHub y se comprobaron estos marcadores: fetch explícito, rebase, bucle de cinco intentos, parada ante conflicto y ausencia de force-push. Esto verifica el texto publicado, no una ejecución de Actions.

Commits de los workflows EXP-604–611:
- [EXP-604 — 8161616](https://github.com/kyrian20/voynich-autoexploration/commit/8161616d4b28e2c5c0ae6f43fbd34d273bc04e7c)
- [EXP-605 — 152b87d](https://github.com/kyrian20/voynich-autoexploration/commit/152b87d0c8c1c5ba007a600a64a727739fec5c73)
- [EXP-606 — 3abbd99](https://github.com/kyrian20/voynich-autoexploration/commit/3abbd9939adc06d1d1a6394f54a946fdf0c7c326)
- [EXP-607 — 1792563](https://github.com/kyrian20/voynich-autoexploration/commit/17925632d993e93e908598fc1b429334aafa55ad)
- [EXP-608 — aeac253](https://github.com/kyrian20/voynich-autoexploration/commit/aeac253e4d71376726241a169cd13eee15756294)
- [EXP-609 — 26fbd08](https://github.com/kyrian20/voynich-autoexploration/commit/26fbd0814e96c42bc84ecd7979862a0f307ebdca)
- [EXP-610 — 505bcf1](https://github.com/kyrian20/voynich-autoexploration/commit/505bcf1bc2e71febb920f2aeea693417eb2c70ff)
- [EXP-611 — d9a2d07](https://github.com/kyrian20/voynich-autoexploration/commit/d9a2d07c384b6a3942865aca0f3109e04e3bc00f)
- [EXP-603](https://github.com/kyrian20/voynich-autoexploration/commit/0dc539e7e1ce3bc9f637e560868cf64fcdac3c23)
- [Agente autónomo](https://github.com/kyrian20/voynich-autoexploration/commit/7802eb9fa03d45bd1854fa88535336c1aade4144)

## Riesgos y siguientes acciones

1. Revisar individualmente la estrategia de publicación de los otros workflows escritores; no cambiar grupos a ciegas ni ocultar ejecuciones fallidas.
2. Revisar ejecuciones y logs reales de Actions. Hasta comprobarlos, no afirmar que CI ha pasado.
3. Ejecutar pruebas de humo y comparar artefactos con fuentes, hashes y protocolos.
4. Preservar IDs y resultados históricos. No reasignar EXP-623 ni crear IDs nuevos hasta reconciliar el registro de GitHub con la Biblioteca.

## Estado

**PARCIAL, con mejora concreta aplicada.** Se completó el inventario de los 31 workflows y se reforzó la publicación de EXP-603 y EXP-604–611. Falta confirmar ejecuciones reales de Actions y continuar la auditoría científica y de los demás workflows escritores.
