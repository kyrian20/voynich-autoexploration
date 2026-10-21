# Estado de orden y estabilización — 2026-10-21

Estado global: **EN AUDITORÍA**. No iniciar experimentos nuevos ni asignar nuevos IDs EXP hasta cerrar los bloqueos P0/P1 y reconciliar GitHub con la Biblioteca.

## 1. Cambios comprobados en este ciclo

- Repositorio: `kyrian20/voynich-autoexploration`, rama `master`.
- El workflow `.github/workflows/voynich-check.yml` comprueba que existan dos transcripciones, analiza la sintaxis de los scripts Python, ejecuta `tests/test_ivtff_metadata.py` y después `scripts/audit_ivtff_metadata.py`.
- El error mostrado por una ejecución anterior fue `NameError: name 'q' is not defined`, durante `load_lines(path)` llamado por la prueba de metadatos.
- En la versión actual inspeccionada de `scripts/exp590_daiin_position.py`, `load_lines` no contiene esa referencia a `q`; la clasificación se lee mediante `parse_currier_language` y el campo IVTFF `$L`.
- Se publicó un cambio de diagnóstico en `tests/test_ivtff_metadata.py` para imprimir la ruta absoluta del módulo EXP-590 realmente importado. Commit: `2c5418ff3d68111525bd04f769f8e5ee0a0ab039`.
- El usuario ha aportado una captura posterior donde `Voynich Check` aparece como **Completado en 8 s**, con checks verdes en `Set up job`, descarga del repositorio, configuración de Python, comprobación de archivos, sintaxis, regresiones de metadatos y validación de metadatos Currier. Esto confirma visualmente que ese run terminó correctamente en los pasos mostrados. La captura no expone URL/ID ni SHA del run, y la consulta de estado de commit no devuelve checks; por tanto, aún no se puede asociar inequívocamente el run a un SHA concreto ni cerrar la trazabilidad de CI.

## 2. Bloqueos científicos y de archivo que siguen abiertos

1. **Numeración:** `research/EXPERIMENT_REGISTER.md` indica colisiones y un último ID libre no confirmado. No asignar ni renumerar EXP todavía.
2. **Colisiones de carpetas:** la auditoría estructural detectó colisiones para IDs 177, 594, 596, 597, 600, 601 y 602. Conservar originales; resolver referencias y aliases en el registro, no fusionar por nombre.
3. **GitHub frente a Biblioteca:** existen conflictos de numeración entre EXP-623 de GitHub y documentos de orden de palabras de la Biblioteca. Los nombres similares no demuestran equivalencia. La instantánea anterior de la Biblioteca tenía 499 elementos; aún no se han cotejado todos los hashes de contenido contra GitHub.
4. **EXP-590 / EXP-593:** las versiones antiguas que usaron `$Q` para clasificar Currier son inválidas para afirmaciones por clase. Conservarlas como históricas; usar `$L=A/B` y regenerar artefactos, verificando los hashes y el run de Actions.
5. **IVTFF:** el protocolo de tokenización v7 registró acuerdo entre dos parsers para ZL3b/ZL3a bajo una política de normalización específica, pero esto no certifica conformidad completa IVTFF. La predicción A/B sigue bloqueada hasta completar fixtures y validación independiente.
6. **Workflows:** hay 31 workflows según la auditoría previa; los grupos de concurrencia y las escrituras simultáneas siguen siendo un riesgo no auditado por completo. No hacer push forzado ni borrar outputs.

## 3. Orden de trabajo obligatorio

### P0 — CI y causa raíz
- Comprobar la ejecución de `Voynich Check` que corresponde al commit `2c5418ff3d68111525bd04f769f8e5ee0a0ab039`.
- Si falla, capturar la ruta completa y línea exacta del traceback; corregir el archivo realmente ejecutado, no una copia supuesta.
- Verificar que las pruebas de regresión y la auditoría `$L` pasan en el mismo run.

### P1 — Canonicalización de inventario
- Mantener como fuentes de orientación `research/EXPERIMENT_REGISTER.md`, `research/ARTIFACT_COLLISION_REGISTER.md` y `research/repository_inventory_audit_2026-10-20.md`.
- Inventariar script, resultado, JSON, hashes, commit y estado de cada artefacto crítico.
- Clasificar las 62 carpetas que no tienen pareja script+resultado reconocible; no asumir que son defectos.
- Comparar GitHub y Biblioteca mediante hashes reales antes de fusionar, renombrar o sobrescribir.

### P2 — Reproducibilidad
- Regenerar los resultados de EXP-590/593 con metadatos `$L` corregidos, sin sobrescribir los outputs históricos; registrar nuevas rutas versionadas y hashes.
- Resolver fixtures IVTFF con ejemplos documentados y salidas esperadas antes de desbloquear experimentos sensibles al parser.

### P3 — Reanudar investigación
Solo después de cerrar P0 y documentar un inventario reconciliado. Consultar el registro y el backlog, evitar repetir pruebas ya realizadas y usar IDs nuevos únicamente tras una búsqueda completa.

## 4. Criterios para declarar “ordenado”

No declarar el proyecto “limpio” hasta tener: (a) CI verde confirmado por URL/ID, (b) registro EXP reconciliado, (c) colisiones con aliases y referencias documentadas, (d) outputs críticos reproducidos y con hashes, (e) workflows de escritura revisados, y (f) inventario GitHub/Biblioteca cotejado o con diferencias explícitamente pendientes.

## Verificación CI de la corrección max-T — 21-10-2026 03:47 UTC

- `Voynich Check` para el commit `4af3632956da17a898121d29f2edf653fe476fe3`: **success**, run [39540440576](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39540440576).
- Workflow autónomo: run [39540440693](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39540440693), SHA `4af3632956da17a898121d29f2edf653fe476fe3`. En la consulta del 21-10-2026 a las 03:48:50 UTC, la auditoría IVTFF, EXP-590, EXP-593 y EXP-622 habían terminado correctamente; EXP-623 seguía ejecutándose y la publicación de resultados estaba pendiente.
- La API de Actions aún mostraba el run en curso y cero artefactos publicados. La etapa de EXP-593 terminó con éxito, pero el nuevo JSON/MD y sus valores ajustados **todavía no están confirmados como publicados**. No declarar la reproducción completa hasta que el workflow concluya y se inspeccionen los archivos versionados.

## 6. Hallazgo nuevo — EXP-593 max-T (21-10-2026)

La revisión estadística detectó que el ajuste anterior usaba el máximo de recuentos brutos de `daiin`, `dain` y `daiiin`, aunque sus frecuencias base difieren mucho. Esto invalida los antiguos p ajustados para inferencia, aunque no los recuentos observados ni los p empíricos no ajustados.

- Corregido el script en commit `4af3632956da17a898121d29f2edf653fe476fe3`: ajuste max-T mediante estadísticas estandarizadas por variante.
- Errata añadida: `research/experiments/2026-10-21-exp593-maxT-erratum.md`.
- Registro EXP actualizado en commit `7a8f1948481427537af71baf99736e715b5c7234`.
- **Pendiente:** verificar el workflow disparado por el cambio y confirmar que los nuevos artefactos se generaron y publicaron. No usar los p ajustados antiguos.

## 5. Próxima acción única

**Auditar los workflows restantes con escritura a master y cotejar hashes de EXP-590/593.** El run 39491327187 completó con éxito los cuatro análisis y publicó resultados corregidos; el run 39490460729 documenta una carrera de push anterior. La captura de Voynich Check también aparece verde, pero sin run ID/SHA. No iniciar EXP nuevos ni renumerar hasta completar el inventario y la auditoría de concurrencia.
