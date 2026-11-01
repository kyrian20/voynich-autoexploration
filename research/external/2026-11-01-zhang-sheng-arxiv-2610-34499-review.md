# Revisión externa: Zhang y Sheng (arXiv:2610.34499)

**Fecha de revisión:** 2026-11-01  
**Versión examinada:** v1, enviada el 25-10-2026  
**Estado:** preprint; revisión documental, no réplica independiente.

## Referencia

Xin Zhang y Victor S. Sheng, [*Does the Voynich Manuscript Mean Anything? Calibrated Tests Find Little Trace of Language*](https://arxiv.org/abs/2610.34499).

## Pregunta y diseño

El trabajo compara generadores de copia y varias familias de cifrado con programas que comparten formas de palabra, distribución de páginas y un modelo de errores del copista. Ajusta con un presupuesto de búsqueda común y evalúa también estadísticas no usadas en el ajuste. Después mide una señal de orden léxico que no requiere descifrar: cuánto se repite entre mitades del libro la asociación de pares de palabras que comparten línea. Los controles comprenden 28 textos de 16 lenguas y versiones cifradas con tasas de copia errónea conocidas.

Para la métrica de pares, divide páginas en bloques alternos de diez páginas, calcula el exceso de coaparición por pareja en cada mitad, ajusta la tendencia general de cada palabra a compartir líneas y calcula la correlación de Spearman entre mitades. Informa 0,071 para ZL y 0,053 para IT, frente a 0,139–0,411 para los 28 controles lingüísticos. ZL e IT son transcripciones alternativas del mismo manuscrito, no dos testigos independientes.

## Resultado que puede incorporarse

1. **Las estadísticas generales no distinguen por sí solas copia y cifrado.** En sus pruebas, una variante del proceso de copia predice mejor que los cifrados de una sola clave; modelos con una segunda clave o que codifican clases gramaticales quedan competitivos.
2. **El orden de pares de palabras queda muy debilitado frente a sus controles lingüísticos.** Los autores informan que los códigos de palabra retienen normalmente parte de ese orden y que para aproximarse al nivel Voynich suelen requerir un texto con coaparición débil —como latín abreviado— o tasas elevadas de copia errónea.
3. **No descartan todos los cifrados.** Dejan abierta una familia de nomencladores con segunda clave y errores de copia altos en varios idiomas; sus propios solvers no la resuelven de forma concluyente.
4. **La dependencia entre el último glifo de una palabra y el primero de la siguiente sigue sin explicar.** El artículo atribuye gran parte de la señal que detecta su solver a esa frontera de glifos. No constituye una lectura del manuscrito ni demuestra que carezca de significado.

## Relación con el proyecto

La medida de reproducción de pares por bloques de páginas no es equivalente a los análisis locales de sucesores tras `daiin` ya archivados: cambia la unidad, la estadística y la comparación entre mitades. Puede considerarse una posible réplica externa, pero **no debe implementarse todavía**. Los bloqueos vigentes de adjudicación IVTFF, procedencia y particiones físicas afectan a la definición de líneas/páginas y a la interpretación de cualquier evaluación predictiva.

Antes de una réplica se debe recuperar y fijar el código, los corpus de control, los filtros, las reglas de separación de páginas y las semillas del artículo. El artículo indica que el código y las reglas de decisión se publicarán con la versión publicada; no localizamos un paquete oficial en la página arXiv consultada. Por separado, el sitio de V. Averyanov anuncia un paquete propio de replicación de sus análisis. No se ha inspeccionado aquí ese paquete ni se debe confundir con materiales de Zhang y Sheng. Una implementación propia sin el código/datos y las decisiones exactas del artículo sería una nueva prueba inspirada en el trabajo, no una reproducción exacta.

## Límites y decisión

- Es un preprint v1, no una conclusión de consenso.
- Las conclusiones se limitan a los modelos, lenguas, códigos y solvers probados; los autores reconocen mecanismos fuera de su cobertura, incluyendo cambios de clave y transformaciones del texto claro.
- No recalculamos cifras, no ejecutamos modelos, no alteramos corpus ni particiones y no asignamos un ID EXP.
- Estado del proyecto al revisar: la partición LIB-EXP-624 por hoja está protegida por nuevas guardias de integridad, pero la puntuación confirmatoria sigue bloqueada. La procedencia histórica de EXP-170 y la adjudicación IVTFF siguen pendientes.

## Fuente primaria

- Zhang y Sheng, arXiv:2610.34499v1, enviado 25-10-2026: https://arxiv.org/abs/2610.34499


## Contraste posterior: prueba de Averyanov (27-10-2026)

Una revisión posterior del registro público de V. Averyanov informa que reconstruyó la métrica de Zhang y Sheng y obtuvo 0,078 para el Voynich, frente a 0,071 (ZL) y 0,053 (IT) en el preprint. Al aplicarla a su generador de cifrado, informa 0,138 (20 semillas: 0,112–0,156), por encima del manuscrito (0,082) y de un control sin significado de quimqu (0,106). También atribuye al modelo la señal independientemente del texto claro usado y señala que el dialecto por sección eleva la recurrencia entre páginas. Esto plantea una objeción concreta: la métrica puede responder a propiedades de construcción del generador además de a estructura lingüística, por lo que una puntuación baja aislada no identifica la causa.

**Estatus probatorio:** son resultados comunicados por el autor de un modelo que se contrasta; la página consultada enlaza un paquete de replicación, pero no hemos auditado sus scripts, preregistro, datos, semillas ni equivalencia exacta de implementación. Por eso se registra como contraanálisis externo no verificado, no como réplica confirmada ni como refutación de Zhang y Sheng. Tampoco contradice directamente su comparación con 28 textos lingüísticos o con las familias de código ensayadas: evalúa un generador específico y una cuestión de sensibilidad del indicador.

**Siguiente paso útil, aún bloqueado:** recuperar la versión exacta del paquete de Averyanov y el código fuente oficial de Zhang y Sheng cuando esté disponible; cotejar definiciones de páginas, bloques alternos, selección de tipos frecuentes, exclusión de pares idénticos/a una grafía, permutaciones dentro de página, residualización por palabra y cálculo de Spearman. Si difieren las reglas o entradas, registrar dos estimandos y no forzar igualdad. Después se podrá preregistrar una réplica con holdouts por hojas físicas y controles de texto aleatorio, prosa y varios generadores; no asignar EXP hasta que se levante la congelación del registro.
