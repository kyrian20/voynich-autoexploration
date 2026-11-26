# Revisión externa: unidades, bordes y separadores en Voynichese

**Fecha de revisión:** 2026-11-05  
**Estado:** método externo inspeccionado; resultados reportados por autores, no reproducidos en este repositorio.  
**Clase:** adquisición de métodos. No es un EXP ni modifica el estado científico.

## Fuente y paquete reproducible

Liudmila Rozanova y Alexander Temerev, *A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space: What the Units of Voynichese Are Not*, arXiv:2608.17096, versión publicada el 17-08-2026: https://arxiv.org/abs/2608.17096

El paquete de código y datos está en https://github.com/lrozanova/voynich-units. El README lo identifica como paquete de reproducción del envío a arXiv, con licencia MIT para el código y licencias de origen para los datos de terceros. El archivo analizado por el artículo cita el snapshot `66f8adaadc120f93e8a4c906685ba66a9d3ab847`; el espejo actual conserva el archivo de reproducción final en `956a7c4fc39981f4d116fa3f4edfccce6d065571`. Las páginas escaneadas de Beinecke/Yale no se redistribuyen; sí se incluyen las mediciones geométricas archivadas.

Scripts especialmente pertinentes:

- `analysis/reproduce_edge_order.py`: calcula cinco asociaciones adyacentes desde el último glifo hasta el primer glifo, pasando por identidad de token, además de métricas de bordes y tokens casi idénticos.
- `analysis/reproduce_headlines.py`: reproduce la comparación de entropía, asociaciones de límites, coordenadas y sensibilidad v101.
- `analysis/reproduce_space_sensitivity.py`: evalúa qué cambia al unir separadores inciertos.

## Resultados que informa el artículo

Las cifras siguientes son resultados de sus autores, no verificaciones nuestras.

1. **La identidad de tokens aporta poca información adyacente.** En una selección de 3.950 líneas y 32.747 tokens, la información mutua excedente de token a token es 0,0661 bits, equivalente al 0,79 % de la entropía del token siguiente. Los controles de texto continuo presentados quedan entre 2,02 % y 9,72 %; un catálogo botánico llega a 15,81 %.

2. **Parte de la dependencia aparece en los bordes.** El emparejamiento último-glifo → primer-glifo da 0,197 bits (5,7 % de la entropía del primer glifo), por encima de los controles de prosa citados (0,018–0,120 bits). El artículo dice que una parte grande se concentra en unos pocos pares frecuentes, incluido `y → q`. Esto no asigna significado a esos signos.

3. **Los separadores marcados inciertos se comportan distinto en la secuencia.** El índice normalizado de asociación interna es 0,494 para separadores inciertos y 0,029 para los ciertos; la diferencia se mantiene al omitir cada quire y aparece en los 16 quires del análisis.

4. **Hay una comprobación geométrica independiente de las etiquetas ZL, con reservas.** En cajas de tokens alineadas, los huecos ciertos son más anchos que los inciertos; el artículo informa AUC 0,905. Los autores señalan que las coordenadas están cuantizadas, que su protocolo de construcción no se publicó y que constituyen otra segmentación humana, no una verdad paleográfica independiente.

## Alcance y límites

El resultado no demuestra que el manuscrito carezca de significado. El artículo restringe sus comparaciones a las unidades, controles y procesos evaluados; reconoce que puede existir información de largo alcance, por diseño de página, ilustraciones, otra segmentación o mecanismos no ensayados. Tampoco demuestra que los separadores ciertos sean límites de palabras léxicas ni que los inciertos sean uniones dentro de una palabra.

El remuestreo usa quires como unidades superiores, pero solo hay 16 quires en el análisis principal. Las transcripciones ZL3b y v101 y las coordenadas de tokens siguen derivando del mismo manuscrito y no son testimonios independientes.

## Relación con nuestros resultados y decisión

- No comparar directamente las cifras con nuestros conteos de EXP-590/593: cambian selección de líneas, corpus efectivo, representación de glifos y definición del estadístico.
- No equiparar este análisis de asociación entre bordes de tokens con EXP-622/623 ni con la reimplementación parcial del estadístico de pares Zhang–Sheng; son preguntas y métricas distintas.
- El resultado sí ofrece un blanco concreto para la vía de unidades: medir por separado orden de identidad de token y dependencia último-glifo → primer-glifo, y no llamar «palabras» a los tokens sin validar esa interpretación.
- Las cifras sensibles a tokenización y separadores quedan **BLOCKED** en nuestro proyecto hasta cerrar los fixtures IVTFF y la comparación diferencial de parsers. La numeración EXP también sigue congelada mientras se concilian colisiones del registro.

## Siguiente paso propuesto, condicionado a las puertas existentes

Cuando se cierren esas puertas, reproducir primero el driver externo desde su snapshot y entradas fijadas; comprobar sus salidas archivadas; después ejecutar una implementación independiente sobre una entrada local con hash explícito. Mantener las métricas de borde y token en endpoints separados, informar controles emparejados y remuestreo por quire, y tratar el análisis de imágenes como una fase independiente con sus limitaciones de procedencia.

Este documento registra una prioridad de método, no una ejecución, reproducción, conclusión lingüística ni traducción.
