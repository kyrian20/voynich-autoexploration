# Revisión integrada GitHub/Codex — 23-10-2026

## Alcance

Checkout comprobado: `54df033bef72a79b9c27810504f42b0dca1db95c` de `kyrian20/voynich-autoexploration`, Python 3.12.14. Esta revisión comprueba funcionamiento y reproducciones seleccionadas; no certifica las conclusiones de los 624 directorios históricos ni configura otras sesiones remotas de Codex.

## Hallazgos y reparaciones

- PR #2: conflicto en `research/EXPERIMENT_REGISTER.md` y `state/open_questions.md`. Se conservaron las aportaciones de la auditoría EXP-170 y las posteriores de master. Reparación publicada sin force: `cf53669fa5366f6cba0d92c7f1ede5f2183871bc`.
- PR #7: conflicto en `state/iteration_log.md`. Se conservaron las dos series de entradas. Reparación publicada sin force: `a289cee2995711b1e7dc596f050e78246150b2d7`.
- GitHub confirmó `mergeable=true` en ambas propuestas tras la reparación. Continúan abiertas; #7 conserva el estado borrador. No se han fusionado resultados científicos ni editado committed_claims.
- PR #6: descripción antigua decía «solo documentación» aunque ya incluía dos archivos de tests y un workflow lector. Se actualizaron título y descripción para reflejar sus seis archivos actuales. Sus dos ejecuciones del commit `81a7e7450303916bddd09c0eff899ca8d52cd938` terminaron en success: [Voynich Check](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39913139597) y [contratos](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39913139337).
- Se añade `AGENTS.md` en la raíz para que Codex encuentre instrucciones, comandos y límites. Aclara las rutas de otra máquina en SOUL.md, los worktrees fijos para análisis largos y la diferencia entre CI y validación científica.

## Pruebas locales

- Master: unittest discover, 127 tests, 126 aprobados y 1 omitido.
- PR #2 actualizada: 134 tests, 133 aprobados y la misma omisión. `python scripts/audit_exp170_archive.py --check research/maintenance/2026-10-22-exp170-audit/results.json`: coincidencia exacta.
- PR #7 actualizada: 127 tests, 126 aprobados y la misma omisión. `python research/analysis/2026-10-23-synthetic-sensitivity/replay.py`: 48 brazos reproducidos con campos científicos y hashes coincidentes. `verify.py`: 100 construcciones de parejas y 256 contextos redundantes comprobados.
- Auditoría estática de master: 665 Python y 163 JSON sin errores de parseo; ningún marcador de conflicto en Markdown/Python/YAML. Ver `format-audit.json`.
- Contratos operativos: 32 workflows, un publicador, 31 lectores/comprobadores, 624 rutas de experimento identificadas y siete grupos históricos de alias numéricos conservados.
- Reproducción local de los 42 pasos shell de Voynich Check en worktree fijo, todos con retorno cero: véase `local-ci-summary.json`. No ejecuta acciones de checkout/setup/upload de GitHub. Se tradujeron variables runner/run_id a rutas temporales; se utilizó Python 3.12.14 instalado y las dependencias presentes. Los artefactos de CI remota se comprueban por separado.

## Límites y pendientes

- La prueba omitida de batería requiere el archivo crudo no publicado. La reconstrucción temporal es una comprobación distinta; no convierte la omisión en una aprobación.
- La simulación histórica EXP-170 requiere `data/derived/naibbe-cipher` y su texto de entrada ausentes. La auditoría de sus 400 vectores archivados sí se reproduce. No se sustituye silenciosamente el código o corpus que falta.
- Persisten referencias históricas a un corpus mal identificado, adjudicaciones de afirmaciones comprometidas, diferencias IVTFF y cotejos con archivos externos pendientes. Éxito operativo no valida su interpretación.
- Esta sesión de Codex accede al checkout y al conector GitHub. No ofrece una API para inspeccionar todas las otras sesiones/configuraciones de Codex del usuario. No se afirma que esas sesiones hayan sido revisadas.
- Tarea ChatGPT horaria activa comprobada por API, hasta el 22-11-2026. Última ejecución registrada consultada: completada el 23-10-2026 a las 08:43 (Europe/Madrid). El próximo horario se devolvió nulo: programación activa no prueba ejecución futura. El publicador de Actions es otro proceso: ejecuta scripts fijos diariamente a las 08:00 UTC y no diseña hipótesis.

No hay traducción validada ni certificación científica global. El siguiente trabajo debe partir de estos límites y de las revisiones pendientes, conservando originales y controles negativos.

Logs locales completos: `execution-logs.zip`, SHA-256 `d658e50058ea80f46ecf00e5b5e283d4a4b03e9b95c96aac18f66bd480a447df`.

## Ejecuciones remotas de las reparaciones

- PR #2: [Voynich Check 39981098948](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39981098948), commit `cf53669fa5366f6cba0d92c7f1ede5f2183871bc`.
- PR #7: [Voynich Check 39981233923](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39981233923), commit `a289cee2995711b1e7dc596f050e78246150b2d7`.

Ambas ejecuciones terminaron en success, comprobado mediante la API de GitHub tras publicar las reparaciones. La ejecución de PR #7 incluye la reproducción de los controles sintéticos. La documentación posterior de master es adicional y no cambia los árboles científicos ensayados.
