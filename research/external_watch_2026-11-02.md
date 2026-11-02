# Vigilancia externa Voynich — 2026-11-02

## Alcance y novedad

Revisión de nuevas publicaciones y recursos públicos respecto a la revisión comunicada el 2026-10-26 y al informe base `research/external_studies_comparison_2026-10-19.md`. Una incorporación sustancial **omitida** en el informe previo, aunque publicada el 25-10-2026, es Zhang y Sheng, arXiv:2610.34499. No se ha verificado en esta revisión otro preprint posterior con datos/código y controles comparables que justifique una nueva línea prioritaria. Este documento es lectura y contraste de fuentes; **no** es reproducción computacional.

## Incorporación prioritaria: Zhang y Sheng (25-10-2026)

**Referencia:** Xin Zhang y Victor S. Sheng, *Does the Voynich Manuscript Mean Anything? Calibrated Tests Find Little Trace of Language*, https://arxiv.org/abs/2610.34499

**Diseño comunicado por los autores:** generadores de autocopia y cifrados con presupuesto igual de búsqueda (4.000 simulaciones por modelo y dos búsquedas); ajuste sobre 22 estadísticas y controles predictivos sobre otras 15 estadísticas no usadas en el ajuste; contraste con 28 textos en 16 lenguas, versiones cifradas y pruebas de recuperación de mensajes insertados. Corpus ZL3b e IT2a con 37.554 y 36.736 tokens respectivamente, según su propia segmentación. ZL/IT son transcripciones del mismo manuscrito, no muestras independientes.

**Resultados reportados, no reproducidos por nosotros:**
- La correlación de recurrencia entre pares de tipos frecuentes que comparten línea es 0,071 (ZL) y 0,053 (IT), frente a 0,139–0,411 en 28 controles de texto natural. Se seleccionan los 300 tipos más frecuentes, se excluyen pares idénticos y vecinos a distancia de un glifo, se comparan dos mitades en bloques alternos de diez páginas y se usa barajado dentro de página como nulo.
- El generador de autocopia con reglas de Timm–Schinner predice varias estadísticas reservadas mejor que cifrados de una sola clave. Cifrados de dos claves o codificación de clases gramaticales también pueden predecirlas. **Ningún modelo supera la comprobación conjunta de las 37 estadísticas**.
- La información mutua entre glifos que flanquean una separación de palabra se comunica como 0,204 bits en ZL, frente a 0,078 en su generador Copy-T; ni la señal de borde ni la distribución de espacios quedan explicadas conjuntamente.
- No obtienen lectura descifrada; algunos nomenclátores con dos claves y tasa de copia errónea superior al 50 % siguen sin excluirse en parte de los controles. Las pruebas negativas solo excluyen las familias de codificación efectivamente ensayadas.

**Reproducibilidad:** el apéndice F declara Python/NumPy, semillas y cachés por hash, pero dice expresamente que el código y las reglas se publicarán con la versión publicada. No se ha localizado en el artículo un paquete de ejecución descargable del experimento. Por ello, **estado: hallazgo de autores / réplica pendiente**, no evidencia independiente confirmada. El 'held-out' principal reserva *estadísticas* del ajuste, no equivale a reservar hojas físicas completas.

## Contraste con nuestros experimentos 602–607

- EXP-602: efecto de `daiin` inicial y predictor de tasa global con ganancia de log-loss histórica negativa (−0,08131). No responde a la recurrencia entre pares de palabras ni a la comparación de mecanismos generativos.
- EXP-603: predictor estratificado A/B y longitud con ganancia histórica negativa (−0,002727). No es prueba de ausencia de semántica.
- EXP-604: señal posicional de `daiin` en IT2a; comprobación de sensibilidad editorial, no segunda muestra manuscrita.
- EXP-605/606: secuencia de folios y contraste léxico en límites de lagunas; no abordan la recurrencia transversal de pares ni la capacidad predictiva de modelos cifradores.
- EXP-607: ganancia adicional histórica de bigrama real frente a control barajado 0,05591 bits/transición en ZL3b y 0,05498 en IT2a. **No** comparar numéricamente con la correlación de pares 0,071/0,053 ni con la información mutua de glifos en límites: son estadísticos y unidades diferentes.
- **Errata de inferencia crítica, 28-10-2026:** `experiments/exp_602_heldout_predictive_test/CORRECTION.md`, `exp_603_stratified_heldout_prediction/CORRECTION.md` y `exp_607_heldout_bigram_prediction/CORRECTION.md` invalidan las afirmaciones históricas de evaluación sobre **hojas físicas totalmente no vistas**, porque la partición era por cara (`fNNr`/`fNNv`) y ambas caras podían cruzarse entre train/test. Los valores históricos se preservan como exploratorios; no afirmar que son confirmación prospectiva por hoja.

## Decisión práctica

Prioridad de réplica cuando se libere el código: verificar selección de 300 tipos, definición exacta de pares y de nulo por página, reglas de separación EVA, hashes de ZL/IT, controles de lenguas y semillas. Como prueba nueva independiente, congelar por adelantado criterios y particiones **por hoja física** (o cuaderno, cuando sea viable), estimar correlación de recurrencia de pares y sensibilidad a selección de tipos, y comparar generadores rivales con el mismo presupuesto. Calibrar antes en textos de verdad conocida. No afirmar que un valor pequeño de recurrencia excluye todas las lenguas, cifrados o mensajes.

## Otros recursos examinados

- 01-11-2026, Tobias Franke, *An Interactive Grammar and Interpretation Decoder*, https://celler-presse.de/forschung/dokument/voynich-manuscript-an-interactive-grammar-and-interpretation-decoder/ : presentación de un intérprete morfológico y reglas versionadas, **sin** validación independiente de lectura ni paquete reproducible contrastado en esta revisión; no priorizar como desciframiento.
- Noviembre 2026, *Voynich Manuscript Decipherment System* v9.13.0, https://voynich.kiltau.com/ : el propio sitio reconoce que su lectura hebreo-aramea **no supera** controles de texto sin significado y que su mapeo no reproduce las estadísticas del Voynich; no tratar el léxico propuesto como palabras descifradas.

**Conclusión:** novedad metodológica importante en controles de recurrencia de pares y comparación equilibrada de generadores, pero sin reproducción independiente ni prueba de contenido semántico.
