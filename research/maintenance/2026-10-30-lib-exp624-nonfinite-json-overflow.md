# LIB-EXP-624 — puerta contra exponentes JSON desbordados y medias no finitas

**Fecha:** 2026-10-30. **Tipo:** corrección de validador de procedencia, sin nuevo EXP ni ejecución del clasificador. **Alcance:** `scripts/audit_library_exp624_archive_format.py` y regresiones asociadas.

## Defecto reproducible

El lector `strict_json` utilizaba `parse_constant` para rechazar `NaN`/`Infinity` explícitos. Sin embargo, el `json.loads` de Python transforma un número JSON legal como `1e400` en `float('inf')` sin llamar a `parse_constant`. Reproducción mínima con Python 3.13.5: `json.loads('{"x":1e400}', parse_constant=reject_constant)` acepta el objeto y `math.isfinite(obj["x"])` es falso.

Además, `validate_summary` comprobaba la finitud de `split_deltas`, pero no de las medias y extremos archivados. Si `mean_real_holdout_bits_per_unit` y `mean_null_holdout_bits_per_unit` fueran ambas infinitas, la resta produciría `NaN` y la comparación `abs(NaN) > 1e-6` devolvería falso. Por tanto, la comprobación de coherencia podía aceptar una fila numéricamente inválida. Esto es un **defecto del validador**, no una constatación de que los bytes originales de Biblioteca estén alterados.

## Reparación

- Se exige que todos los números JSON con punto decimal o exponente sean finitos en el momento de la decodificación mediante `parse_float`. Se conserva el rechazo previo de constantes no estándar y claves duplicadas.
- Se exige explícitamente que las cinco medidas numéricas de cada fila sean números reales finitos, sin booleanos ni cadenas, antes de evaluar medias y extremos.
- Se añaden dos pruebas de regresión: exponentes desbordados positivos, negativos y anidados; y 25 combinaciones de campos de medida con valores no finitos o de tipo incorrecto. Se comprueba también un exponente finito de control.

**Comandos de verificación en CI canónica (Python 3.12):**

```sh
python -m unittest discover -s tests -p 'test_library_exp624_archive_format.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp624_archive_format.py' -v
```

Las pruebas preexistentes de recibo cotejan el archivo `research/maintenance/2026-10-30-lib-exp624-library-native-format-evidence.json` con los tres hashes originales de Biblioteca. El workflow canónico ejecuta ambas variantes. No se adjuntan los originales privados de Biblioteca ni se ejecuta el modelo.

## Integridad, limitaciones y siguiente paso

Los SHA-256 históricos **no cambian**: script `1f00846ab8e91cefd07bc2dcd26ad12cf8a7c4bc7b2478d480afec391a13f3a9`, JSON `d6e1b7490e563c96367ff10ab56feb5487d6b2775a885494f249c89f87bd4bab`, informe `7de18cce59ea21598af7958a7ded3e05b03e305e8a6cc84c0740917b807447c4`. No se modifican fuentes, simulaciones, semillas, particiones ni salidas congeladas. La puerta CI prueba entradas sintéticas y el recibo, **no** relee los tres archivos privados ni acredita reproducción histórica. El estado de LIB-EXP-624 continúa `INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY` para la afirmación de independencia física y `BLOCKED` para reproducción exacta.

La siguiente acción científica sigue siendo recuperar la salida nativa y su recibo de ejecución, o registrar su indisponibilidad; no sustituirlos por una nueva ejecución. Permanecen abiertos EXP-170, la adjudicación IVTFF y la conciliación global de artefactos. No se han interpretado tokens, probado semántica ni obtenido traducción.

**Autoauditoría:** la prueba no ajusta un modelo ni elige parámetros por resultado Voynich; no destruye características; limita su conclusión a validación JSON; conserva los negativos y originales; incluye controles adversariales y uno positivo. Verificar el SHA exacto de la PR y la CI posterior antes de declarar integración.
