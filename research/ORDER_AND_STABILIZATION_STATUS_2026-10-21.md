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


## Verificación adicional — 21-10-2026 08:32 UTC

- El workflow programado **Voynich Autonomous Research** terminó con conclusión `success`: [run 39569620268](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39569620268). El mismo run confirmó como exitosos los pasos de auditoría IVTFF, EXP-590, EXP-593, EXP-622, EXP-623 y la publicación de artefactos.
- EXP-593 regenerado con metadatos Currier tomados de `$L`: `daiin` 726 casos (A=440, B=278, unknown=8), `dain` 198 y `daiiin` 19. La corrección de múltiples comparaciones usa estadísticos estandarizados por variante; los resultados siguen siendo evidencia posicional exploratoria, no desciframiento.
- EXP-622 (ZL3b) y EXP-623 (IT2a) prueban si el contraste ch/sh es mayor después del dígrafo que antes. EXP-622: interacción +0,53 puntos porcentuales, p=0,823; EXP-623: interacción −0,91 puntos, p=0,690. Ninguno respalda una especificidad posterior al dígrafo; el resultado reduce la confianza en interpretaciones fonéticas fuertes de ese contraste.
- Se corrigió una errata de copia en el texto de EXP-623: el informe identificaba IT2a como fuente, pero la limitación final decía por error que el experimento usaba ZL3b. Se corrigieron tanto el Markdown como el JSON; no cambian los datos numéricos.
- **Estado global continúa EN AUDITORÍA.** El éxito de este workflow no cierra las colisiones de IDs, la reconciliación con la Biblioteca, la auditoría de concurrencia ni la conformidad completa IVTFF. No asignar nuevos IDs ni sobrescribir resultados históricos hasta cerrar esos bloqueos.


## Auditoría de workflows y cotejo de artefactos — 21-10-2026, revisión posterior

- Los tres runs `Voynich Check` disparados por las correcciones documentales terminaron con éxito: [39662345974](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39662345974), [39662351877](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39662351877) y [39662358400](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39662358400). Los tres completaron comprobación de archivos, sintaxis Python, regresiones IVTFF y auditoría de metadatos Currier.
- Revisión de los 31 YAML de workflows: 30 tienen capacidad de escritura a `master`; 9 no declaran concurrencia ni reintentos; 21 declaran grupos de concurrencia diferentes, que no serializan escrituras de workflows distintos; solo 9 de los 30 tienen reintentos explícitos. `voynich-corpus-experiments.yml` además permite que falle el push con `continue-on-error: true`. La auditoría completa está en [WORKFLOW_CONCURRENCY_AUDIT_2026-10-21.md](WORKFLOW_CONCURRENCY_AUDIT_2026-10-21.md). **No se considera resuelto el riesgo de carreras.**
- Cotejo de EXP-593: la transcripción usada declara SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; el JSON corregido de 21-10-2026 contiene los campos de estadísticos estandarizados y los p ajustados 0,000400 / 0,000400 / 0,988602. El blob SHA del JSON es `a4b7ae7810baf6895010aba8abbfe0cc6369ad06`; el informe Markdown es `b11f9c18df6afde5015e8a58705be1ad41ef500a`. El run [39569620268](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39569620268) reprodujo esos valores y terminó sin cambios adicionales que publicar.
- Cotejo de EXP-590: el script vigente usa `parse_currier_language` y el campo IVTFF `$L`; el informe/JSON corregidos declaran la misma fuente SHA-256 y recuentos globales de 4.188 líneas, 32.732 tokens y 726 `daiin`. El JSON corregido tiene blob SHA `49a202841b1dc30b47e381d3f82b6c7e35ab5ff3`; el informe, `df3dc9bc4007bcbe0cd84671482423eb77f48127`. Los outputs antiguos quedan preservados y no deben usarse para inferencias A/B.
- Importante: los SHA anteriores son SHA de blobs de GitHub, no SHA-256 del contenido del archivo. La fuente de transcripción sí tiene SHA-256 de contenido anotado en los resultados.
- Se corrigió el registro EXP-593 y la errata max-T para que ya no indiquen que la reproducción está pendiente. Estado correcto: **REPRODUCIDO, NO VALIDADO COMO DESCIFRAMIENTO**.

### Próximo paso seguro

Pilotar una plantilla de publicación con rebase/reintentos y error explícito en un solo workflow; validar el run antes de propagarla a los restantes 29. Mantener congelada la numeración EXP y no fusionar ni renombrar las colisiones hasta completar la comparación con la Biblioteca mediante hashes de contenido reales. No afirmar que la reconciliación GitHub/Biblioteca está terminada: este ciclo ha cotejado los artefactos críticos de EXP-590/593, no los 499 elementos de la Biblioteca.


## Update de estabilización — 2026-10-22

### Cambios operativos realizados
- Se homogeneizó la protección de escritura de los 30 workflows con capacidad de modificar `master`: grupos de concurrencia **individuales por workflow**, `cancel-in-progress: false` y reintentos acotados de rebase/push. El workflow de solo lectura `voynich-check.yml` queda separado.
- Se corrigió la estrategia inicial de grupo global compartido: GitHub puede cancelar una ejecución pendiente cuando llega otra al mismo grupo, así que no era una cola segura para 30 workflows. Los runs cancelados durante esa prueba quedan como **CANCELLED**, nunca como validaciones exitosas.
- Se añadieron guardias a EXP-602 para no producir auditorías parciales si faltan transcripciones, si no se cubren exactamente ZL3b/ZL3a o si algún parser devuelve cero registros.
- Se registraron estos cambios en `state/current_state.md` y en la auditoría de concurrencia. No se asignaron IDs EXP ni se modificaron deliberadamente conclusiones científicas.

### Estado de verificación
Al escribir esta actualización, varias ejecuciones de `Voynich Check` y algunas pruebas específicas han terminado en éxito; otras siguen en cola/en ejecución y hubo cancelaciones durante el diseño transitorio de concurrencia. Por tanto, la infraestructura ha mejorado, pero **CI global aún no está cerrado**. Hay que comprobar el resultado final del último commit y repetir/confirmar los workflows relevantes que quedaron cancelados antes de considerar la estabilización operativa completa.

### Bloqueos científicos/archivísticos que siguen vigentes
1. No crear ni renumerar experimentos hasta reconciliar el registro de EXP, las colisiones entre carpetas y las colisiones GitHub/Biblioteca.
2. Completar fixtures de conformidad IVTFF 2.0.2 y una adjudicación independiente contra la especificación; el acuerdo entre parsers v7 no basta para desbloquear la predicción Currier A/B.
3. Reproducir/confirmar los outputs críticos desde fuentes con hashes y comandos documentados, sin sobrescribir históricos.
4. Cotejar por hashes reales los artefactos de GitHub y la Biblioteca; el cotejo parcial de EXP-590/593 no equivale a revisar la Biblioteca completa.
5. Solo después, seleccionar un único experimento confirmatorio preregistrado y someter el informe a `skills/audit_experiment.md` antes de tocar el estado científico.


## Verificación adicional de CI — 2026-10-22 05:54 UTC

- Se consultó directamente la API de GitHub Actions para el run **Voynich Check #526**, run ID [39730701397](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39730701397), asociado al commit `63b6e68b6816c9ec9e347d633a08fe3146dd850d` (mensaje: `Correct current state after completed EXP-623 reproduction`).
- Resultado del run: `completed / success`. Se verificaron los siete pasos principales: checkout, configuración de Python, existencia de corpus, sintaxis de scripts, regresiones IVTFF, auditoría de metadatos Currier y cierre del job; todos aparecen como `success`.
- Alcance: esto confirma que el workflow de comprobación pasó en ese SHA concreto. **No** demuestra que los 30 workflows que escriben resultados estén todos verdes ni cierra la auditoría de concurrencia, el parser IVTFF completo o el cotejo GitHub/Biblioteca.
- No se han borrado ni renombrado artefactos ni se ha asignado un nuevo ID EXP en esta actualización.
