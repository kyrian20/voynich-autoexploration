# Investigación Voynich — orden residual integrado

**Bloque integrado y público por petición del usuario, 22-10-2026.** El análisis se ejecutó inicialmente en privado; los protocolos conservan esa cronología. [Estado de integración y reproducción](INTEGRATION.md).

El resultado principal es una diferencia exploratoria: tras controlar los bordes y la longitud del token anterior, el predictor calibrado recupera información de identidad en César latino y Dante italiano, mientras la mejora es mucho menor e incierta en las ocho vistas del Voynich. No se recupera significado ni texto plano.

## Qué se ha ejecutado

- Cuatro vistas de las transcripciones sobre la misma intersección de 3.880 registros P0: ZL3b/IT2a × separación/unión de espacios inciertos. Incluye páginas subdivididas.
- Dos controles de identidad comprobada: César latino, Gutenberg #218; Dante italiano, #1012. Se selecciona una vista analítica sin cabecera/pie y se conservan los originales íntegros.
- Dos vocabularios por fuente: completo y 2.000 tipos aprendidos en entrenamiento más UNK. Doce comparaciones principales por versión, con 16 controles de entrenamiento barajado por comparación.
- Siete pruebas de probabilidades, UNK, barajado, agrupación por folio y extracción, y tres de calibración. Los controles se reportan completos, sin elegir semillas favorables.

## Incidencia independiente: identidad de los textos de referencia

Se han identificado seis incidencias en diez archivos de referencia. Dos textos situados en latin/ son traducciones inglesas; el supuesto árabe corresponde a Drum-Taps en inglés; el supuesto KJV es Book of Mormon, también inglés; Cicerón es bilingüe y requiere auditar sus filtros; el sexto archivo está vacío. Las fichas primarias y cabeceras respaldan estas identificaciones. Véanse CORPUS_INCIDENTS.md, SOURCES.md y reference_identity_audit.json; la revisión canónica de identidad está en `research/CORPUS_IDENTITY_REVIEW.json`.

La búsqueda encuentra 103 archivos Python con referencias directas a los corpus dudosos. No se concluye que sean 103 resultados inválidos: algunos aplican filtros, pueden ser referencias opcionales y falta resolver la ejecución y dependencias transitivas. Los originales y los resultados históricos permanecen intactos. Las afirmaciones que dependan de considerar esos archivos monolingües requieren revisión específica.

## Primer predictor: control fallido, conservado

V1 utilizó una jerarquía con tau=20 sin calibrar cuánto confiar en cada capa. Todas las capas empeoraron la pérdida también en los textos conocidos. Por ello, este intento queda **INVALID_FOR_CLAIM** para cualquier afirmación de ausencia de identidad léxica o lenguaje en Voynich. Su código, protocolo y resultados se conservan; no se borran para mostrar únicamente un modelo favorable.

## Predictor calibrado: método y límites de partición

V2 conserva corpus, tokenización, tau y alpha. Selecciona pesos de interpolación de una rejilla fijada usando solo desarrollo. Entrenamiento=grupos hash módulo 5 en 2/3/4; desarrollo=1; evaluación=0. El vocabulario y los conteos se aprenden únicamente en entrenamiento.

Para Voynich se agrupan caras y subdivisiones de cada folio físico: f89r1 y f89v2 pertenecen al mismo grupo f89. Hay 55 folios físicos en entrenamiento, 25 en desarrollo y 18 en evaluación. Los folios ya se habían explorado: esta partición no se presenta como una muestra confirmatoria recién descubierta.

Los controles usan bloques consecutivos de 25 líneas con plantilla de longitud del manuscrito. César aporta 2.511 líneas y 20.515 tokens; Dante, 3.880 líneas y 33.960 tokens. Son controles de sensibilidad, no muestras del mismo género ni tamaño. No se comparan pérdidas absolutas como si lo fueran.

Los modelos son U (unigrama de destinos), E (bordes del token previo), EL (bordes y longitud) y W (identidad completa). La columna de ganancia mide pérdida EL menos pérdida W: positivo significa mejora al añadir identidad, bajo esta implementación. Los bordes son caracteres de transcripción, no glifos o fonemas adjudicados.

## Resultados de V2

| Fuente / espacios | Vocabulario | Ganancia W sobre EL, bits/transición | Intervalo exploratorio por grupos, 95% | Media de 16 controles |
|---|---|---:|---|---:|
| ZL3b_split | completo | 0.003669 | [-0.001362; 0.008997] | 0.000081 |
| ZL3b_split | 2.000 + UNK | 0.003104 | [-0.000304; 0.007178] | -0.000211 |
| ZL3b_join | completo | 0.002551 | [-0.003256; 0.008104] | 0.000391 |
| ZL3b_join | 2.000 + UNK | -0.000506 | [-0.004292; 0.003698] | 0.000171 |
| IT2a_split | completo | 0.002893 | [-0.002890; 0.009010] | -0.000195 |
| IT2a_split | 2.000 + UNK | 0.002285 | [-0.001650; 0.006803] | 0.000072 |
| IT2a_join | completo | 0.002893 | [-0.002890; 0.009010] | -0.000195 |
| IT2a_join | 2.000 + UNK | 0.002285 | [-0.001650; 0.006803] | 0.000072 |
| Latin_Caesar_218 | completo | 0.028801 | [0.014199; 0.042441] | 0.003255 |
| Latin_Caesar_218 | 2.000 + UNK | 0.020608 | [0.010924; 0.029238] | 0.001983 |
| Italian_Dante_1012 | completo | 0.009633 | [0.006406; 0.012861] | 0.001548 |
| Italian_Dante_1012 | 2.000 + UNK | 0.020349 | [0.014519; 0.026149] | 0.001526 |

En los controles naturales, las cuatro comparaciones de vocabulario recuperan una ganancia positiva con intervalos exploratorios por encima de cero. En las ocho vistas Voynich, las ganancias van aproximadamente de −0,0005 a +0,0037 bits por transición y todos los intervalos incluyen cero. La versión IT2a produce las mismas vistas split/join para esta selección; no se cuenta como evidencia independiente adicional.

**Interpretación limitada:** el experimento no distingue de forma robusta un aporte adicional de la identidad del token anterior en estas vistas. No demuestra que todo el orden se reduzca a los bordes, que el manuscrito carezca de lengua, ni que no existan dependencias más largas o unidades diferentes. Un predictor con una sola posición previa no prueba esas hipótesis.

Los intervalos provienen de 2.000 remuestreos de los grupos de evaluación, con pesos de modelo ya fijados. No incorporan toda la incertidumbre de selección de modelo, desarrollo, sección, mano ni las decisiones históricas. No hay p confirmatorio ni corrección de toda la exploración previa.

## Autoauditoría

**Conciencia del objetivo:** las hipótesis de bordes y tokens proceden del trabajo previo y literatura. V1 falló en controles conocidos. V2 se diseñó después de observar ese fallo y las métricas de V1; por tanto, es una reparación exploratoria. Ningún parámetro de V2 se selecciona con sus pérdidas de evaluación.

**Destrucción de características:** el control negativo baraja solo entrenamiento dentro de cada registro, preservando inventario y longitud; destruye orden local intencionadamente. EL condiciona bordes y longitud y puede absorber estructuras con contenido lingüístico. No es una prueba justa para negar mecanismos basados en esos rasgos.

**Extrapolación:** solo se ensaya memoria de un token, con estas transcripciones, políticas, corpus y jerarquía. No se identifica ni excluye una lengua, familia o clase de cifrados.

**Alcance negativo:** V1 no admite una conclusión lingüística negativa. V2 limita una señal predictiva concreta; no invalida estructuras más largas ni traducciones que aún no se han probado.

**Comportamiento de los controles:** se esperaba que un método útil detectara alguna información de identidad en textos conocidos. V1 no lo hizo y se bloqueó esa interpretación. V2 sí recupera mejoras en los controles de latín e italiano. Los barajados se publican por semilla; sus rangos son diagnósticos y no intervalos de confianza.

## Reproducción, trazabilidad y continuidad

Este directorio conserva scripts, protocolos V1/V2, entradas preparadas y resultados completos. Los cuatro corpus originales se reutilizan desde `data/`, con sus avisos y hashes; no se duplican. La auditoría de identidad queda integrada en `research/CORPUS_IDENTITY_REVIEW.json`. Se puede repetir el análisis desde inputs.json sin conectarse a GitHub. Para regenerar exactamente la extracción desde el lector original, prepare_inputs.py recibe un checkout del commit b566b6fa461f3a4e6fd8bb3a1aaa6e71f035f190.

Pruebas: python test_residual_order.py y python test_calibrated.py. Análisis: python residual_order.py y python residual_order_calibrated.py. Los resultados están versionados en el repositorio público; el runner integrado reproduce y verifica también la extracción desde las fuentes canónicas.

Próxima dirección: contrastar unidades de tamaño variable o dependencias más largas con una prueba calibrada en controles, antes de intentar asignar sonidos o palabras. En paralelo queda pendiente adjudicar los segmentos que usaron los análisis históricos de Cicerón. No se añaden EXP nuevos ni se modifica el registro de afirmaciones comprometidas.
