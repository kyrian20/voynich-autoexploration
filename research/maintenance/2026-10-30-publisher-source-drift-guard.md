# Cierre acotado: impedir publicación de resultados con fuentes cambiadas

**Fecha:** 2026-10-30. **Estado inicial:** FIX PROPOSED / CI PENDING.
**Base congelada:** master `1bce529f2dd4f572f05489443c7a4579e9c0894f`.
**Revisión de PR abiertas:** #5, #7, #13, #66, #82 y #138; esta reparación afecta al publicador de master y no modifica el borrador científico #138.
**Sin EXP nuevo, sin ejecución de hipótesis ni consumo de folios reservados.**

## Defecto verificable

El único publicador `.github/workflows/voynich-agent.yml` ejecuta los scripts sobre el commit de checkout, guarda resultados y, si `master` se ha movido, usa `git pull --rebase origin master`. Si durante la ejecución se modifica un script, dependencia o corpus sin generar conflicto en `research/experiments/`, el rebase puede publicar resultados antiguos sobre una versión nueva del código y de las fuentes. Un push aceptado no demuestra que las salidas correspondan al nuevo árbol. La auditoría anterior cubría carreras de escritura, pero no esta carrera de **procedencia de entradas**.

## Reparación y criterio previo

Antes de cada rebase, el publicador ejecuta un `git fetch --no-tags origin master` y compara el árbol de `$GITHUB_SHA` (commit con el que se calcularon los resultados) contra `origin/master` mediante `scripts/check_publisher_source_drift.py`. Cualquier cambio en rutas fuera de `research/experiments/` bloquea la publicación y deja las salidas en el artefacto Actions previo. Cambios **solo** en resultados publicados permiten rebase/reintento normal. El fetch y la comparación usan el mismo `origin/master` local; si el remoto cambia después, el push sin force falla y el siguiente intento vuelve a comprobar.

**Criterio falsable:** en un repositorio Git temporal, un cambio concurrente de script o transcripción debe rechazarse, un cambio solo de resultados debe admitirse y un ref inexistente debe fallar cerrado. El workflow debe hacer fetch, comprobación y rebase en ese orden. No se modifican las reglas científicas ni los scripts EXP.

## Pruebas reproducibles

```sh
python -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
python -O -m unittest discover -s tests -p 'test_publisher_source_drift.py' -v
```

Siete casos deterministas por modo: cambios solo de salida, script, corpus, carrera compuesta, ref ausente, base vacía y orden de operaciones del YAML. **Prueba local previa a publicación:** 7/7 normales y 7/7 con `-O` en Python, en repositorios temporales sin conexión. CI remota y ejecución del publicador con cambio real de fuentes: pendientes de verificar por separado. Semilla: no aplica. No se crea salida científica.

## Alcance, controles y limitaciones

- La política falla conservadoramente también ante cambios no científicos (por ejemplo, README), pues la exclusión es únicamente `research/experiments/`. Esta elección evita una lista incompleta de dependencias, a costa de requerir una ejecución fresca tras un cambio documental concurrente.
- La barrera protege la procedencia **durante el rebase**; no valida los valores de los experimentos ni sus transcripciones. Un cambio solo de resultados podría implicar una colisión semántica aunque Git no produzca conflicto: la revisión de artefactos sigue siendo necesaria.
- No reproduce los resultados históricos ni corrige las adjudicaciones IVTFF, EXP-170 o las colisiones de artefactos.
- Las publicaciones con `GITHUB_TOKEN` no disparan por sí solas la CI `push`; este parche no convierte la última escritura de master en una ejecución de `Voynich Check` certificada.
- Originales, corpus, resultados negativos, scripts de análisis, parámetros, semillas y particiones reservadas no se alteran. Solo se añaden el guard, regresiones y esta documentación, y se actualizan dos workflows.

## Próxima verificación

Inspeccionar CI de la PR en el SHA exacto, fusionar únicamente tras comprobar resultados y ausencia de concurrencia conflictiva, y comprobar la CI de master posterior. Mantener como bloqueos separados la auditoría de los artefactos y la conformidad IVTFF. No promover ninguna traducción ni métrica histórica por esta reparación.
