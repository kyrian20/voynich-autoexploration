# Instrucciones para Codex y agentes del repositorio

## Inicio y alcance

Lee `SOUL.md`, `CLAUDE.md`, `README.md` y `research/RESEARCH_INTEGRITY_STANDARD.md` antes de trabajar. Las rutas son relativas a este checkout. Las rutas históricas `~/voynich-cryptanalyst` y `~/voynich-kb` de SOUL.md describen otro entorno: comprueba su existencia y nunca supongas que sus datos están disponibles aquí.

Consulta el registro pertinente y el estado actual de GitHub antes de repetir un análisis. No asignes nuevos EXP mientras siga congelada la numeración. No modifiques `state/committed_claims.md`; registra contradicciones en `state/open_questions.md` y conserva originales y resultados negativos. Aplica `skills/audit_experiment.md` después de cada experimento y antes de actualizar estado científico.

## Entorno y comprobaciones

La CI canónica está en `.github/workflows/voynich-check.yml`; consulta sus comandos actuales. Usa Python 3.12; la reconstrucción histórica de la batería exige exactamente 3.12.14 y sus dependencias fijadas en `experiments/common_battery_2026_10_22/requirements.txt`. La auditoría YAML requiere PyYAML 6.0.3. No instales indiscriminadamente dependencias de experimentos históricos.

Comprobaciones iniciales desde la raíz:

```sh
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

Ejecuta también las reproducciones y checks pertinentes a los archivos cambiados. Una prueba omitida no equivale a una reproducción aprobada. La suite descubierta no cubre por sí sola los análisis fuera de `tests/` ni los 624 directorios históricos.

## Ramas, concurrencia y evidencia

Ejecuta análisis largos en un checkout o worktree fijo: no cambies su rama mientras corren. Comprueba el SHA antes de publicar; conserva cambios ajenos, rechaza conflictos y nunca uses force-push. No interpretes una CI antigua como validación de una fusión actual. Conserva resultados/logs e identifica el commit y la ejecución exactos.

El publicador programado de Actions repite scripts determinados; no es un investigador que diseñe hipótesis nuevas. Las tareas de ChatGPT son ejecuciones acotadas: comprueba su historial real y no afirmes actividad continua por tener una programación activa. No se garantiza acceso desde esta sesión a otras sesiones, configuraciones o tareas remotas de Codex.

Al finalizar informa de cambios, pruebas y omisiones, enlaces de CI y pendientes. Distingue corrección operativa, reproducibilidad y validez científica. No declares el proyecto entero validado ni una traducción sin evidencia suficiente.
