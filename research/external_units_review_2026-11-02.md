# Revisión externa: unidades gráficas, tokens y separadores — 2026-11-02

**Alcance y estado:** lectura documental de un preprint reciente y de su paquete público. Los números siguientes son resultados publicados por sus autores; no son una reproducción nuestra, ni un desciframiento, ni evidencia de que el manuscrito carezca de significado.

## Fuente

Liudmila Rozanova y Alexander Temerev, *A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space: What the Units of Voynichese Are Not* ([arXiv:2608.17096](https://arxiv.org/abs/2608.17096), 17-08-2026). El [paquete de código y datos](https://github.com/lrozanova/voynich-units) incluye controladores de análisis para los resultados principales. El artículo fija su corpus ZL3b, las coordenadas por token y sus controles; advierte que ZL3b, las otras transcripciones y las páginas del mismo manuscrito no constituyen manuscritos independientes.

## Qué aporta y qué no permite concluir

| Medición informada por los autores | Resultado publicado | Lectura prudente |
|---|---:|---|
| Información mutua entre identidades de tokens adyacentes, sobre el nulo de barajar dentro de línea | 0,79 % de la entropía de tokens; 0,54 % al unir todos los separadores dudosos. Los controles de prosa continua van de 2,02 % a 9,72 %. | La secuencia de tokens transcritos tiene poco orden adyacente bajo esa métrica, incluso al cambiar la política de espacios dudosos. No es por sí sola una prueba de que no exista significado. |
| Asociación de glifos a través de un separador, normalizada entre ancla interna y pares independientes | Separador incierto: 0,494; separador cierto: 0,029. El signo del contraste se conserva en los 16 quires. | Las dos clases de separador no se comportan igual en el corpus y modelo ensayados. El índice no estima la probabilidad de que un separador sea una frontera léxica. |
| Geometría de cajas de palabras y certeza de ZL | AUC publicada: 0,905; el análisis incluye controles por par de glifos y remuestreo por folio. | La etiqueta de certeza se asocia con diferencias de hueco en la segmentación visual usada. La fuente visual es una segunda tokenización del mismo conjunto de imágenes: corrobora la geometría, pero no es una lectura paleográfica independiente ni determina si hay palabras. |
| Unidades multi-símbolo aprendidas con BPE | La zona de mínimo está entre 32 y 64 fusiones; aparece también tras borrar los espacios antes del aprendizaje. | Hay una escala reproducible de agrupación local bajo esas decisiones de análisis. La escala no identifica si la causa es lingüística, cifrada, paleográfica o motora. |
| Ataque de sustitución calibrado con cifrados sintéticos | Diferencial Voynich menos sustituto: media −0,0085 en 14 comparaciones; los cifrados sintéticos obtuvieron +0,13 a +0,52 frente al idioma correcto. | El resultado limita las sustituciones y lenguas incluidas en la calibración. El artículo deja fuera inserción nula, transposición, grupos mayores, codificación dependiente de estado y fuentes no ensayadas. No elimina la posibilidad general de texto codificado. |

El trabajo también muestra que los controles de Naibbe y de un generador sin contenido reproducen varios rasgos que suelen interpretarse como lingüísticos (entropía, escala de unidades, bajo orden de tokens y resultado nulo del ataque), pero no recuperan conjuntamente la asociación entre glifo final y glifo inicial ni la cola de vocabulario singleton. Es una comparación informativa entre modelos concretos; no identifica el mecanismo histórico.

## Solapamiento con este repositorio

El foco del proyecto en posición, secuencias y fronteras hace que el artículo sea directamente relevante. Sin embargo, sus variables no deben mezclarse con las nuestras:

- Su medida de orden es entre **identidades de tokens adyacentes** dentro de línea.
- La asociación de frontera es entre el **glifo final y el inicial** de tokens contiguos, normalizada contra cohesión interna.
- Los análisis previos del repositorio sobre pares de palabras, límites de línea y predicción de clases usan poblaciones, unidades o nulos distintos. Que dos resultados mencionen “pares”, “transiciones” o “bordes” no los convierte en réplicas.
- El artículo pregunta si los separadores ciertos y dudosos se comportan distinto; no convierte ninguna de las dos clases en «espacio entre palabras» probado.
- Añadir ZL3a o IT2a como sensibilidad permitiría examinar robustez a lecturas del mismo manuscrito, no obtener una replicación independiente del objeto.

## Consecuencia metodológica y próximo paso

La conclusión útil para nuestro trabajo es tratar **glifo, token y separador como unidades observadas** hasta validar explícitamente su interpretación. Esto encaja con los bloqueos ya vigentes de corpus, tokenización IVTFF e inventario de artefactos; no los resuelve ni autoriza reordenar el manuscrito.

Cuando se reabra la fase experimental, la opción acotada con mayor valor es congelar el snapshot y las reglas del paquete, reconstruir primero una sola cifra primaria (el contraste de asociación entre separador incierto y cierto), auditar denominadores y exclusiones, y después calcularla con un parser independiente y una segunda transcripción como sensibilidad. Antes de hacerlo habría que cotejar el solapamiento exacto con los análisis existentes y dejar por escrito una predicción de qué resultado discriminaría. No asigno un ID EXP: el registro de numeración y la fase de auditoría aún impiden abrir uno con seguridad. Tampoco repito aquí análisis estadísticos.

## Fuentes

- [Artículo y anexos](https://arxiv.org/abs/2608.17096).
- [Código, datos y protocolo de reproducción](https://github.com/lrozanova/voynich-units).
- [Registro del proyecto en este repositorio](https://github.com/kyrian20/voynich-autoexploration/blob/master/research/EXPERIMENT_REGISTER.md) y [estado operativo](https://github.com/kyrian20/voynich-autoexploration/blob/master/research/OPERATIONAL_STATUS.md).
