# Integridad de publicación de JSON de la réplica de límites de línea — 29-10-2026

**Estado de la incidencia:** reparación propuesta; verificar CI y, después, integración. **No es un experimento lingüístico** ni una reproducción de métricas históricas.

## Defecto verificable

La reparación anterior de JSON estricto serializaba antes de abrir el destino, pero usaba `path.open("x")` seguido de `write()`. Si el proceso sufría un error de escritura después de crear el archivo, el nombre final podía existir con contenido vacío o incompleto. Un consumidor posterior podía confundir ese archivo con un resultado terminado. La exclusividad impedía sobrescribirlo, pero no impedía publicar un resultado parcial.

## Reparación

`research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py` conserva la serialización `allow_nan=False` y crea primero un archivo temporal exclusivo en el directorio de destino. Tras escribir, vaciar buffers y `fsync`, publica el archivo completo mediante `os.link` (en el mismo sistema de archivos), que **falla sin sobrescribir** si ya existe el nombre final, incluso si es un enlace simbólico. El temporal se elimina en `finally`. No hay `os.replace` ni fallback con sobrescritura.

La publicación del nombre final es atómica en sistemas de archivos con semántica de enlaces duros; **no se garantiza durabilidad frente a pérdida total de energía** sin sincronización del directorio, ni compatibilidad con sistemas que prohíban hardlinks. En esos entornos se aborta, no se rebaja silenciosamente la garantía. Una interrupción forzosa durante la preparación puede dejar un temporal huérfano, pero no un resultado final parcial.

## Regresiones y prueba de fallo

`tests/test_line_boundary_atomic_publication.py` incluye seis casos: JSON completo antes de aparecer el destino, fallo inyectado al enlazar, fallo inyectado en `fsync`, carrera con otro escritor que publica primero, rechazo de enlace simbólico existente y rechazo de `NaN` antes de crear archivos. CI ejecuta los seis casos con Python normal y optimizado (`-O`).

Comandos previstos desde la raíz:

```sh
python -m unittest discover -s tests -p 'test_line_boundary_atomic_publication.py' -v
python -O -m unittest discover -s tests -p 'test_line_boundary_atomic_publication.py' -v
```

## Integridad y alcance

Base comprobada antes de actuar: cabeza de la rama de la PR #138 `2d6854d99c58b366f972f7445bb2e175b50a2f93`; `master` consultado por separado. El histórico `research/analysis/2026-10-28-line-boundary-reproduction/results.json` tenía blob Git `32756b8ec8430309079b82c288e2dd76807aead4`. Esta reparación **no modifica** el histórico, corpus, hashes de transcripción, parámetros, semillas, particiones de folios, resultados negativos ni afirmaciones comprometidas.

No se reejecuta el predictor ni se consume un folio reservado. La clasificación `INVALID_FOR_CLAIM` de las puntuaciones históricas respecto al lector corregido permanece. La reparación mejora la integridad de publicación de **futuros** resultados, no la validez estadística ni la interpretación del manuscrito.

**CI, commit final y revisión de artefactos:** pendientes de adjuntar tras ejecución; un informe sin CI no acredita cierre.
