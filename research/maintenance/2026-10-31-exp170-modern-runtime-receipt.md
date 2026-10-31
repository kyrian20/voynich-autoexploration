# EXP-170: trazabilidad del entorno en el recibo de reconstrucción moderna

**Fecha:** 2026-10-31. **Tipo:** reparación operativa acotada, sin EXP nuevo. **Base inspeccionada:** `master` `875561b8210502fb92f78991dd1ab4dacd3161ba`. **Estado científico:** reproducción histórica exacta de EXP-170 **BLOCKED**. Este documento fija criterios de aceptación antes de la CI; no anticipa su resultado.

## Defecto comprobado y alcance

El runner aislado `scripts/run_exp170_isolated_reconstruction.py` conserva los SHA-256 de fuentes y los bytes de stdout/stderr, pero el recibo no registraba qué intérprete de Python, versión de pandas/numpy o timeout se habían usado, ni hacía explícita la fórmula de semillas del script histórico congelado. Dos reconstrucciones modernas con distintas versiones podían producir recibos sin información suficiente para distinguir su entorno. **No hay evidencia de que una simulación histórica se haya ejecutado con versiones distintas**; el defecto es una omisión comprobable del contrato de procedencia del runner.

## Reparación

El recibo `PREFLIGHT_ONLY` y el recibo de ejecución incorporan `runtime_provenance` con ejecutable, versión e implementación de Python, plataforma, versiones instaladas de pandas y numpy (o `null` si no están instaladas), timeout, ruta relativa del script congelado y la **fórmula declarada** de semillas: índices 0–99, `sim_idx*1000 + corpus_offset + protocol_offset`, con offsets italiano/latín 0/500 y A/B 0/250. La fórmula se cotejó con el código histórico `experiments/exp_170_naibbe_simulation/script.py` de la base indicada. Los SHA-256 existentes, logs binarios y validaciones de esquema permanecen intactos.

**Límite esencial:** el recibo captura el entorno del proceso padre antes del lanzamiento. La fórmula es una declaración del código, **no** prueba de que las 400 simulaciones terminaran, ni recibo individual de semillas, ni certificación de identidad de Naibbe/italiano históricos. El campo `historical_reproduction` sigue siendo `false`. No se añaden paquetes ni se ejecuta Naibbe.

## Regresiones y criterios de cierre

- Una prueba de preflight con versiones de paquetes sintéticas verifica Python, versiones, timeout, ruta y offsets; no crea carpeta de salida.
- Una prueba con dependencias no instaladas exige `null`, no versiones inventadas, sin efectos laterales.
- La prueba existente de éxito sintético comprueba que `runtime_provenance` persiste exactamente en `receipt.json`; su salida es una fixture, no una simulación real.
- CI debe ejecutar `python -m unittest discover -s tests -p 'test_exp170_isolated_reconstruction.py' -v` y la variante `python -O`, además del resto de la suite. Verificar el SHA del head, logs y conclusión antes de integrar; tras integrar, verificar el push en `master`.

**No modificados:** corpus, script histórico, 400 vectores congelados, parámetros de cifrado, semillas, hashes originales, resultados negativos, manifiestos, particiones reservadas y `state/committed_claims.md`. La falta de entrada histórica exacta y la identidad de la fuente etiquetada Latin siguen bloqueando una reproducción histórica. No se ha obtenido traducción ni nueva inferencia lingüística. Evaluación general: 2026-11-22, sin prometer descifrado.
