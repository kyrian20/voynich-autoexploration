# Errata estadística EXP-593 — corrección del contraste max-T
Fecha: 2026-10-21

## Hallazgo
La versión previa de `scripts/exp593_daiin_variants.py` calculaba `max_null` como el máximo del **recuento bruto** de inicios de línea entre `daiin`, `dain` y `daiiin`. Después comparaba el recuento observado de cada token contra esa distribución máxima común.

Esto no es una corrección max-T válida cuando los tokens tienen frecuencias base muy distintas: el token común `daiin` domina el máximo y hace que las pruebas de variantes menos frecuentes sean artificialmente conservadoras. Por ello, los antiguos valores `max_stat_adjusted_p` de EXP-593 se consideran **INVÁLIDOS PARA INFERENCIA** y deben conservarse solo como histórico.

## Corrección aplicada
En el commit `4af3632956da17a898121d29f2edf653fe476fe3`:
- se conserva cada distribución nula por variante;
- se calcula media y desviación típica propias para cada variante;
- se estandarizan los recuentos observados y nulos por variante;
- se compara cada estadístico observado estandarizado con el máximo estandarizado de las tres variantes por permutación;
- se conserva el p empírico no ajustado como dato separado;
- se actualiza la descripción del modelo nulo en el JSON/MD generado.

No se han borrado ni sobrescrito los resultados históricos ya versionados. La ejecución CI posterior debe regenerar un artefacto nuevo con fecha actual y verificar que el nuevo bloque max-T pasa. Hasta entonces, los p ajustados corregidos permanecen **PENDIENTES DE REPRODUCCIÓN**.

## Alcance e interpretación
La corrección solo arregla el procedimiento de ajuste por comparaciones múltiples. No convierte el resultado en evidencia de significado o desciframiento. El nulo sigue permutando tokens dentro de cada línea y la familia de variantes sigue siendo exploratoria; las decisiones de tokenización y la conformidad IVTFF deben evaluarse por separado.

## Próxima comprobación
Confirmar el run de `Voynich Autonomous Research` disparado por el commit indicado. Verificar en logs que EXP-593 finaliza, que los artefactos nuevos contienen `null_sd_initial` y `observed_standardized_statistic`, y que el push termina sin force-push.
