# Auditoría de seguridad de publicación de resultados — 2026-10-21

## Alcance real de esta revisión

Esta revisión cubre dos workflows de escritura que se han leído directamente en la rama `master`:
- `.github/workflows/voynich-agent.yml`
- `.github/workflows/voynich-exp603.yml`

No es una auditoría exhaustiva de los 31 workflows registrados en el inventario. No debe interpretarse como que todos los escritores estén ya protegidos.

## Cambios aplicados

1. `voynich-exp603.yml` adopta el grupo de concurrencia `voynich-master-writes`, conserva `cancel-in-progress: false`, comprueba si hay cambios antes de crear un commit y reintenta la publicación tras rebase, con cinco intentos máximos. No utiliza `force-push`.
2. `voynich-agent.yml` adopta el mismo grupo `voynich-master-writes`. Ya tenía una lógica de rebase/reintentos para resolver carreras de publicación.
3. Los cambios se han leído de nuevo desde GitHub después de publicarse.

Commits:
- EXP-603: `0dc539e7e1ce3bc9f637e560868cf64fcdac3c23`
- Agente autónomo: `7802eb9fa03d45bd1854fa88535336c1aade4144`

## Limitaciones y riesgos pendientes

- GitHub Actions solo serializa ejecuciones que comparten exactamente el mismo grupo de concurrencia dentro del alcance aplicable. Los workflows de escritura que sigan usando otros grupos pueden seguir compitiendo por `master`.
- La existencia del commit y la lectura posterior validan que el YAML quedó guardado, pero no demuestran que la ejecución real haya terminado correctamente.
- Un rebase puede detenerse ante conflictos de contenido. No se debe resolver automáticamente un conflicto científico ni sobrescribir artefactos sin revisión.
- La auditoría de escritura no valida los resultados lingüísticos ni criptográficos de ningún experimento.

## Próximas acciones obligatorias

1. Inventariar todos los workflows con permisos `contents: write`, `git push`, o pasos que publiquen artefactos.
2. Identificar sus grupos de concurrencia y unificar únicamente los escritores que operan sobre la misma rama de destino.
3. Verificar la ejecución de ambos workflows en GitHub Actions y revisar sus logs.
4. Ejecutar tests de humo de los scripts y comparar las salidas con las fuentes y hashes registrados.
5. Mantener los IDs históricos, no borrar resultados y no crear nuevos IDs hasta confirmar el registro maestro.

## Estado

**PARCIAL — cambios de configuración publicados; ejecución CI y cobertura de los demás workflows pendientes.**
