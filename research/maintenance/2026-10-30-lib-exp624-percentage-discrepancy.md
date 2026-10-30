# LIB-EXP-624 — discrepancia real en el porcentaje archivado IT2a/glifos

**Fecha:** 2026-10-30. **Tipo:** errata de procedencia y reparación de la puerta de auditoría, sin EXP nuevo. **Estado de la afirmación concreta:** `INVALID_FOR_CLAIM` para el porcentaje archivado **24,77 %** de IT2a con `ch/sh` colapsados; los valores originales no se sobrescriben. Esta nota no rehabilita el experimento ni su independencia por hoja física.

## Entrada exacta y comprobación

Se leyó el original de Biblioteca `exp624_resultados_2026-10-20.json` (**8.141 bytes; SHA-256 `d6e1b7490e563c96367ff10ab56feb5487d6b2775a885494f249c89f87bd4bab`**), sin modificarlo. Se verificó el hash sobre bytes materializados y se recalculó cada porcentaje desde las medias que figuran en ese mismo JSON mediante aritmética decimal:

`100 × mean_null_minus_real_bits_per_unit / mean_null_holdout_bits_per_unit`, redondeo a 0,01 punto porcentual. La copia es un **resumen curado**, no la salida nativa del script histórico; véase [adjudicación de formato](2026-10-30-lib-exp624-library-native-format-adjudication.md).

**Resultado:** siete de las ocho filas coinciden al redondear a dos decimales. La octava, IT2a / todas las páginas / tokenizador `EVA units with ch/sh collapsed`, no coincide:

| Campo | Valor archivado |
|---|---:|
| Media nula (`mean_null_holdout_bits_per_unit`) | 3,8357742633 |
| Diferencia media nulo − real (`mean_null_minus_real_bits_per_unit`) | 0,9498638385 |
| Porcentaje archivado | **24,77 %** |
| Porcentaje recalculado | **24,7632882776 %** |
| Redondeo esperado a 2 decimales | **24,76 %** |
| Distancia entre porcentaje archivado y cálculo | **0,0067117224 puntos porcentuales** |

La diferencia de **0,01 punto porcentual entre etiquetas redondeadas** no queda explicada por el redondeo de las medias archivadas a diez decimales. La discrepancia se refiere a la **etiqueta de porcentaje derivado**, no prueba que las pérdidas del modelo sean falsas. No se sabe cómo se produjo la transformación archivística. La etiqueta 24,77 % queda retirada para cualquier afirmación exacta; el 24,76 % es un **cálculo aritmético condicionado a las medias archivadas**, no una nueva métrica experimental.

## Corrección de código y evidencia congelada

- `scripts/audit_library_exp624_archive_format.py`: nueva comprobación independiente de los porcentajes redondeados; conserva la clasificación `ARCHIVED_CURATED_SUMMARY_NOT_NATIVE_SCRIPT_OUTPUT`, devuelve `relative_percentage_audit` con filas comprobadas y discrepancias, y rechaza porcentajes no numéricos o no finitos. **No** reescribe ni “corrige” el archivo histórico.
- `tests/test_library_exp624_archive_format.py`: regresión que muestra que las comprobaciones previas de medias/deltas aceptaban la fila, pero la puerta nueva detecta la discrepancia; controles positivos y negativos de tipo; verificación del recibo.
- `research/maintenance/2026-10-30-lib-exp624-percentage-evidence.json`: recibo derivado de solo lectura con las ocho filas, valores de entrada, SHA-256 de la fuente y la discrepancia esperada. La CI verifica el recibo, **no** puede acceder a los bytes privados de Biblioteca.

Para repetir con los tres originales recuperados:

```sh
python scripts/audit_library_exp624_archive_format.py \
  --script /ruta/exp624_positional_holdout.py \
  --results /ruta/exp624_resultados_2026-10-20.json \
  --report /ruta/Informe_Voynich_exp624_Control_posicional_2026-10-20.md
python -m unittest discover -s tests -p 'test_library_exp624_archive_format.py' -v
python -O -m unittest discover -s tests -p 'test_library_exp624_archive_format.py' -v
```

La auditoría completa exige además los SHA-256 originales de script `1f00846ab8e91cefd07bc2dcd26ad12cf8a7c4bc7b2478d480afec391a13f3a9` e informe `7de18cce59ea21598af7958a7ded3e05b03e305e8a6cc84c0740917b807447c4`. No se copian al repositorio. No hay semillas nuevas ni simulaciones; las semillas y particiones históricas permanecen congeladas.

## Alcance científico, bloqueo y siguiente paso

Esta errata **no** corrige la fuga entre hojas físicas documentada en 28/28 particiones históricas, ni aporta salida nativa, recibo por semilla o ejecución reproducida. Las puntuaciones antiguas continúan `INVALID_FOR_CLAIM_PHYSICAL_LEAF_HOLDOUT_ONLY` para independencia física y la reproducción exacta continúa `BLOCKED`. Las transcripciones y particiones prospectivas no se han tocado. Siguen pendientes la adjudicación IVTFF, EXP-170 y la conciliación global de artefactos.

La siguiente intervención debe buscar una traza nativa autenticada de LIB-EXP-624 o pasar a una discrepancia IVTFF de datos reales; no convertir este cálculo aritmético en resultado lingüístico ni entrenar un predictor sobre hojas reservadas antes de cerrar las puertas metodológicas.

## Autoauditoría

- **Conocimiento del objetivo:** el cálculo está fijado por los campos del resumen y su propia definición; no se ha ajustado una hipótesis al Voynich.
- **Destrucción de características:** no se tokeniza ni modifica ningún carácter; solo se coteja aritmética archivada.
- **Extrapolación:** el hallazgo se limita a ocho filas y un porcentaje; no certifica el resto del JSON ni el historial.
- **Resultado negativo:** siete filas coherentes no validan el experimento; una fila incoherente no invalida todas las pérdidas del modelo.
- **Control:** se espera que un resumen sintético con 0,5/2,0 reporte 25,00 %; la regresión lo comprueba. La variante con 24,77 % para las medias archivadas IT2a debe fallar el control de dos decimales, sin alterar los originales.

**Verificación remota:** comprobar CI y SHA de la PR antes de fusionar y, si se fusiona, comprobar CI de `master` posterior. No declarar éxito hasta observar los registros.
