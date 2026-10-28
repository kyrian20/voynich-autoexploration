# EXP-170 — reserva temprana de destino ante ejecuciones concurrentes (28-10-2026)

**Tipo:** corrección operativa acotada. **Estado científico EXP-170:** BLOCKED para reproducción histórica exacta. No es un experimento lingüístico nuevo y no se asigna ID EXP.

## Defecto comprobado por inspección del código

En `scripts/run_exp170_isolated_reconstruction.py` de `master` `471464d846bdef8ec45b62eb668a13947bb93e23`, la verificación `preflight` rechazaba destinos existentes, pero la creación exclusiva `out_dir.mkdir(..., exist_ok=False)` se hacía **después** de `subprocess.run`. Dos procesos con el mismo destino ausente podían superar el preflight y lanzar cada uno las 400 simulaciones; solo uno lograría publicar. La ausencia de sobrescritura estaba protegida, pero no se evitaba el trabajo científico redundante.

## Corrección propuesta

Mover la creación exclusiva del directorio de salida inmediatamente después de `stage_inputs` (con hashes verificados) y **antes** de lanzar el simulador. La operación `mkdir(exist_ok=False)` es la reserva exclusiva: el segundo proceso aborta sin lanzar Naibbe. `--execute` sigue siendo obligatorio; el preflight sin `--execute` no crea directorios. Los recibos y logs de ejecuciones lanzadas conservan la ruta anterior. No se altera el simulador histórico ni el JSON archivado.

## Pruebas de regresión

`tests/test_exp170_isolated_reconstruction.py` añade:

1. Un subprocess simulado observa el destino ya reservado; una segunda invocación contra ese mismo destino falla con `FileExistsError` antes de lanzar un segundo subprocess. Se conserva el recibo `FAILED` y los logs del primero.
2. Simulación de una reserva concurrente tras el preflight y copiado: el proceso perdedor no llama al subprocess y no altera el archivo marcador del ganador.

**Comandos de verificación:** `python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v` y `python -O -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v`; la CI canónica ya ejecuta ambos. Registrar sus resultados reales antes de declarar la corrección verificada.

## Límites

No se ejecutan las 400 simulaciones. La prueba usa subprocess simulado y una intercalación controlada, no una carrera multiproceso real. Dos procesos pueden copiar los recursos en temporales distintos antes de competir por el destino; se evita la duplicación **del simulador**, no todo trabajo preparatorio. No se proporciona sandbox de seguridad frente a código arbitrario. Si falla la preparación anterior a la reserva, no se crea salida; si falla el simulador tras la reserva, se conservan recibo y logs. La dependencia y los bytes originales de Naibbe/italiano siguen sin acreditarse para reproducción histórica. Los originales, semillas, corpus, particiones reservadas y resultados negativos permanecen intactos.

**Relación:** [reparación anterior](2026-10-28-exp170-isolated-reconstruction.md); [procedencia Naibbe](2026-10-27-exp170-naibbe-source-provenance/REPORT.md); [norma de integridad](../RESEARCH_INTEGRITY_STANDARD.md).
