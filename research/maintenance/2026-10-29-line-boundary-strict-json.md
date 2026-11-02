# Incidencia acotada: serialización JSON no finita en la réplica de límites de línea

**Fecha:** 2026-10-29. **Estado:** reparación de código propuesta; CI y fusión pendientes de comprobación. **Sin EXP nuevo.** Rama base congelada: PR #138, commit `7db8b26fee30b10e65accf08a73bf7bd69c2a45a`. Rama principal observada antes del parche: `1bce529f2dd4f572f05489443c7a4579e9c0894f`. PR abiertas observadas: #5, #7, #13, #66, #82, #138. La corrección de símbolos EVA de PR #152 ya está fusionada en #138; no se repite.

## Defecto falsable y alcance

La función `write_new_result(path, result)` invocaba `json.dump` con el valor predeterminado `allow_nan=True`. Python emite entonces los literales `NaN`, `Infinity` y `-Infinity`, que **no son números JSON válidos**. El propio lector tiene una ruta real que produce `float("nan")`: `auc(y,s)` cuando el subconjunto evaluado solo contiene una clase. Si una configuración futura llegara a ese estado y el resultado se serializara, el archivo podría parecer JSON aunque incumpliera el estándar. La escritura abría primero el archivo con `x`: un error de serialización posterior también podía dejar un artefacto vacío o parcial. No se afirma que esta situación se haya producido en los corpus congelados.

**Regla de aceptación previa a CI:** serializar completamente con `json.dumps(..., allow_nan=False)` **antes** de abrir el destino. Los valores no finitos deben provocar `ValueError` sin crear archivo; los objetos no serializables deben provocar `TypeError` sin crear archivo. Una salida válida debe poder leerse con `json.loads`, conservar UTF-8 y salto final. El destino ya existente, incluso si es un enlace simbólico, debe seguir rechazándose con `FileExistsError` sin alterar su contenido. No se pretende garantizar escritura atómica frente a cortes de energía/errores de E/S después de abrir el archivo.

## Reproducción y pruebas

- Programa: `research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py`, solo se cambia la función de escritura.
- Regresión: `tests/test_line_boundary_strict_json.py` (cinco pruebas sintéticas, incluidas las tres formas de no finitud).
- CI: `.github/workflows/voynich-check.yml`, ejecuciones en Python normal y `python -O`.
- Comandos: `python -m unittest discover -s tests -p 'test_line_boundary_strict_json.py' -v` y `python -O -m unittest discover -s tests -p 'test_line_boundary_strict_json.py' -v`.
- Semilla: no aplica (casos deterministas). Sin dependencias adicionales; Python 3.12 del workflow.
- Entradas científicas congeladas **no leídas ni recalculadas** por esta prueba: ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`, IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- El `results.json` histórico permanece intacto, blob Git `32756b8ec8430309079b82c288e2dd76807aead4`. Se inspeccionó su texto mediante el conector y no contenía literales `NaN`/`Infinity`; por ello el impacto observado en el artefacto histórico es **cero**, no una recuperación de puntuaciones. El defecto afecta a la seguridad de **futuras** salidas.
- No se utilizan hojas reservadas, no se entrenan modelos y no se modifican políticas IVTFF, métricas ni afirmaciones comprometidas.

## Autoauditoría obligatoria (cinco controles)

1. **Conocimiento del objetivo:** ningún parámetro depende de las estadísticas Voynich. La condición JSON es normativa, no calibrada al resultado.
2. **Destrucción de la señal:** no se cambian tokenización, selección, candidatos ni predicción; únicamente se rechaza la publicación de un número no finito. Un futuro caso con AUC indefinida deberá gestionarse explícitamente en lugar de publicar `NaN`.
3. **Extrapolación:** la prueba acredita solo el contrato de serialización y exclusividad bajo condiciones normales de sistema de archivos; no garantiza atomicidad ante fallos de E/S ni validación del experimento completo.
4. **Resultado negativo:** no hay contraste de hipótesis lingüísticas; no se infiere mecanismo ni significado.
5. **Controles:** un diccionario válido debe crear JSON válido; un diccionario con `NaN` debe fallar sin archivo; un archivo o symlink existente debe permanecer inalterado. No hay comparación de corpus ni distribución nula.

**Pendiente antes del cierre:** verificar CI en el commit exacto, revisar las regresiones normales/optimizadas y, si pasan, integrar solamente en la rama de la PR #138 tras verificar que no avanzó concurrentemente. Después comprobar una CI nueva en el commit integrado. No cerrar adjudicación IVTFF, EXP-170 ni conciliación de artefactos por esta reparación.
