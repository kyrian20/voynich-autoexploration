# LIB-EXP-624 — cotejo de bytes y formato de los tres originales de Biblioteca

**Fecha:** 2026-10-30. **Tipo:** reparación de contrato de procedencia; sin EXP nuevo. **Estado:** evidencia archivística cotejada; reproducción histórica del clasificador NO ejecutada y NO acreditada.

## Incidencia específica

La copia de resultados de Biblioteca `exp624_resultados_2026-10-20.json` **no tiene la estructura JSON que escribe directamente** el `main()` del script histórico `exp624_positional_holdout.py`. El script inicializa la salida con claves `experiment`, `method`, `datasets`, y escribe los resultados por transcripción bajo `datasets[edition]`. El JSON de Biblioteca tiene claves de raíz `experiment`, `date`, `source_data`, `method`, `ZL3b`, `IT2a`, `interpretation`, sin `datasets`. Además, las filas de Currier del resumen emplean las etiquetas de tokenizador `raw`/`glyph`, frente a las etiquetas extensas de la salida del script. **Es un resumen estructurado o transformación archivística, no el archivo nativo inalterado que escribiría ese script.** No se sabe quién realizó la transformación ni si hubo un recibo de ejecución separado. Esto no prueba que sus cifras sean falsas.

La clasificación anterior de fuga física de las 28 particiones permanece válida en su alcance (véanse [auditoría](2026-10-30-lib-exp624-physical-leaf-leakage.md) y [corrección de asignación](2026-10-30-lib-exp624-grouped-leaf-allocation.md)); esta incidencia es distinta: no confundir el resumen archivado con un output nativo reproducido.

## Recuperación de las entradas exactas

Se leyeron **tres archivos originales de la Biblioteca del usuario**, sin modificarlos, y se copiaron temporalmente al entorno de verificación para calcular SHA-256 sobre bytes reales:

| Archivo original | Bytes | SHA-256 |
|---|---:|---|
| `exp624_positional_holdout.py` | 9.109 | `1f00846ab8e91cefd07bc2dcd26ad12cf8a7c4bc7b2478d480afec391a13f3a9` |
| `exp624_resultados_2026-10-20.json` | 8.141 | `d6e1b7490e563c96367ff10ab56feb5487d6b2775a885494f249c89f87bd4bab` |
| `Informe_Voynich_exp624_Control_posicional_2026-10-20.md` | 7.912 | `7de18cce59ea21598af7958a7ded3e05b03e305e8a6cc84c0740917b807447c4` |

Los tres hashes coinciden con los fijados anteriormente en `scripts/audit_library_exp624_leaf_leakage.py`. Se cotejaron **8 filas** del JSON (2 vistas ZL3b, 4 vistas estratificadas y 2 vistas IT2a) y **56 deltas de partición**: las medias, diferencias de medias y extremos son coherentes dentro del redondeo de seis decimales. No se comprobó la generación histórica de esos números a partir de tokens; no hay recibos por réplica.

## Reparación ejecutable

`scripts/audit_library_exp624_archive_format.py` implementa una puerta de procedencia de **solo lectura**. Exige los tres SHA-256 exactos, extrae por AST (sin importar ni ejecutar el script histórico) las claves del objeto `results` en `main()`, rechaza JSON ambiguo (claves duplicadas, NaN/Infinity), verifica la forma del resumen, las ocho filas y sus 56 deltas, y emite `ARCHIVED_CURATED_SUMMARY_NOT_NATIVE_SCRIPT_OUTPUT` con `historical_reproduction=false` y `model_executed=false`. **No** reemplaza el JSON original, no ejecuta el modelo y no altera ninguna transcripción ni partición prospectiva.

Comando para repetir el cotejo cuando se tengan las tres copias originales, desde la raíz del repositorio:

```sh
python scripts/audit_library_exp624_archive_format.py \
  --script /ruta/exp624_positional_holdout.py \
  --results /ruta/exp624_resultados_2026-10-20.json \
  --report /ruta/Informe_Voynich_exp624_Control_posicional_2026-10-20.md
```

Regresiones `tests/test_library_exp624_archive_format.py`: cinco casos (formato distinto, hashes, claves duplicadas/no finitos, sumas y forma inválidas, AST estático), probados con Python normal y `-O`. **Validación local:** Python 3.13.5, 5/5 y 5/5; ejecución real del auditor con los tres originales completada y cotejada. La CI del repositorio usa Python 3.12; su ejecución y sus artefactos se verificarán después de publicar. La CI puede ejecutar las regresiones sintéticas sin acceder a la Biblioteca, pero **no puede repetir el cotejo de bytes reales** si esos archivos no se le proporcionan.

## Alcance y siguiente puerta

**Clasificación:** defecto de identificación de formato/procedencia detectado y controlado por código; **no** se rehabilitan las ganancias históricas ~0,95–0,97 bits/unidad, que siguen `INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY` para independencia física. El resumen archivado se conserva como evidencia histórica, no se retira para su uso descriptivo bajo las limitaciones documentadas. La reproducción histórica exacta sigue **BLOCKED**: falta la salida nativa original o una traza de ejecución autenticada que explique la transformación y vincule datos/semillas a las métricas. No sustituir el resumen por una nueva ejecución y llamarla reproducción. Pendientes independientes: adjudicación IVTFF, EXP-170 y conciliación global de artefactos.

**Autoauditoría:** no hay ajuste al objetivo ni prueba lingüística; no se alteran características del corpus; la conclusión solo trata del contrato JSON; el resultado negativo de procedencia se conserva; el control adversarial rechaza cambios de hash, JSON ambiguo y medias incoherentes. Sin traducción ni afirmación semántica.
