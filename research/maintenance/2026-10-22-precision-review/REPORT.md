# Revisión de precisión — 22-10-2026

Fuente revisada: commit `48a76dde6f5c8186f355e5cbeef970619bfbc244`. Sin nuevo EXP ni modificaciones de corpus.

## Defecto corregido

La guardia del manifiesto convertía entradas a diccionario sin rechazar rutas repetidas: una entrada podía ocultar otra. Tampoco validaba estrictamente el estado. Ahora rechaza rutas repetidas, claves JSON duplicadas, estado desconocido, SHA-256 mal formado, tamaños negativos/booleanos y rutas fuera del ámbito o con `..`. No se ha encontrado duplicación en el manifiesto actual; era una carencia preventiva de la validación, no evidencia de corrupción de los 14 corpus.

Cinco pruebas del manifiesto pasan, con casos adversariales de cambios, ausencias, altas, vacíos, duplicados y campos inválidos. Los corpus siguen intactos y el archivo vacío conserva su bloqueo.

## Precisión estadística

El cálculo anterior usaba 9.999 permutaciones. Se conserva como histórico. Ahora se cuenta exactamente la distribución de adyacencias A→B bajo el mismo nulo por registro: A=daiin, B=dam, O=otros. Cada orden de categorías con las multiplicidades fijadas tiene igual probabilidad. Se enumeran sus conteos mediante programación dinámica y se convolucionan registros con fracciones racionales. Se guardan numeradores y denominadores completos; los decimales son solo presentación.

| Fuente / coma | Cola Monte Carlo anterior (+1) | Cola exacta exploratoria | Holm exacto, cuatro vistas |
|---|---:|---:|---:|
| ZL3b / split | 0.0006000 | 0.0002636635 | 0.0010027598 |
| ZL3b / join | 0.0002000 | 0.0002506900 | 0.0010027598 |
| IT2a / split | 0.0019000 | 0.0015327577 | 0.0030655154 |
| IT2a / join | 0.0019000 | 0.0015327577 | 0.0030655154 |

Las diferencias son entre aproximación aleatoria y distribución exacta, no una alteración de los datos. Se mantienen las ocho apariciones y los mismos lugares; el script aborta si cambian sus fuentes, selección activa o localizaciones respecto al bloque previo. No se elige el valor más favorable.

La distribución exacta mejora precisión numérica, no validez semántica. La pareja fue elegida retrospectivamente y Holm solo cubre las cuatro vistas; la exploración previa sigue sin estar corregida. No hay traducción, pronunciación ni confirmación independiente.

## Verificación

- Enumeración independiente de todas las cadenas de tres categorías hasta longitud seis, agrupadas por multiconjunto: acuerdo exacto con el algoritmo dinámico.
- Convolución de dos registros cortos: acuerdo con la distribución conocida 1/4, 1/2, 1/4.
- Cada distribución suma exactamente uno y su media coincide exactamente con n(A)×n(B)/longitud; lo mismo para la convolución global.
- Segunda ejecución coincide con el JSON guardado. CI incorpora estas pruebas, la reproducción exacta y conservación de ambos JSON como artefactos.

## Autoauditoría

**Selección del objetivo:** mismo objetivo conocido; no se presenta como preinscripción de una hipótesis nueva. **Destrucción de información:** el mismo nulo destruye orden local, no composición de cada registro. **Extrapolación:** exactitud solo para el nulo declarado, no todos los mecanismos. **Alcance negativo:** no excluye una lengua ni demuestra significado. **Control:** se esperaba normalización uno y media analítica por registro; ambas igualdades se verifican con fracciones sin tolerancia flotante. No se interpreta el cambio de las colas Monte Carlo como cambio del corpus.

## Límite de la guardia

La guardia verifica consistencia y bytes, pero una persona aún puede editar deliberadamente un archivo y su manifiesto. No certifica procedencia, licencias ni corrección científica. Las revisiones completas de IVTFF e históricos siguen abiertas. Ninguna CI acredita ausencia absoluta de errores.

Reproducción: `python tests/test_corpus_integrity.py`, `python scripts/check_corpus_integrity.py`, `python tests/test_daiin_dam_exact.py`, `python scripts/audit_daiin_dam_exact.py`.
