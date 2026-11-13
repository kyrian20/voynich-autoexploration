# f65r y la lectura externa «emergence of the oak»

**Fecha:** 2026-11-01  
**Tipo:** revisión documental y cotejo descriptivo; sin EXP nuevo, sin clave nueva y sin traducción admitida.  
**Estado:** observación compatible con vocabulario botánico/recetario; lectura semántica **BLOCKED**.

## Pregunta

¿La propuesta externa de leer la etiqueta de f65r como «emergence of the oak» obtiene algún apoyo transferible de las recurrencias de sus componentes en el corpus ya inventariado?

## Propuesta externa localizada

The Voynich Project presenta f65r como tres palabras transcritas **oθeis ðes ahes** y las traduce «emerging of the oak». Su página metodológica plantea lenguas germánicas antiguas, incluso dos sistemas lingüísticos relacionados, y presenta las lecturas como pruebas de concepto que necesitan evaluación por filólogos. El sitio publica tablas gráficas de signos, dígrafos y palabras; en las páginas consultadas no queda fijada una evaluación reservada de esta frase ni un criterio de acierto semántico ajeno a la identificación de la imagen.

Fuentes consultadas:

- [Lectura de f65r en The Voynich Project](https://voynichproject.org/research/65r/)
- [Método declarado](https://voynichproject.org/method/)
- [Tablas de signos, dígrafos y palabras](https://voynichproject.org/cypher/)

La identificación del dibujo no está resuelta independientemente. La descripción de Quire 8 clasifica f65r como página herbal, con una planta de página completa, y recoge identificaciones tentativas distintas: geranio; ruda; dropwort o *Spiraea filipendula*. No son identificaciones definitivas y ninguna convierte el rótulo en texto plano conocido. Véase [Voynich MS, Quire 8](https://www.voynich.nu/q08/index.html).

## Cotejo con la concordancia ya conservada

Se consultó —sin volver a contar ni modificar— `research/decipherment/2026-10-22-anchor-review/concordances.json`. Sus transcripciones fuente están identificadas por SHA-256:

- ZL3b: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- IT2a: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

| Forma | ZL3b separar/unir coma | IT2a separar/unir coma | Observación |
|---|---:|---:|---|
| `otaim` | 2 / 1 | 2 / 2 | f65r.1 (rótulo) y f111v.3 (P0, palabra final de registro) |
| `dam` | 88 / 74 | 98 / 98 | Forma muy extendida; no funciona como ancla semántica aislada |
| `alam` | 11 / 6 | 8 / 8 | Incluye f65r.1 y las páginas f58r/v, f104r, f107r, f108r, f111r/v y f112r |

En las vistas conservadas, cada acierto exacto de `alam` aparece al final de su registro. f65r es herbal; f58 pertenece al grupo de páginas con texto y estrellas marginales, normalmente llamado sección de recetas; f104–f112 cae en la sección final de recetas. La clasificación general está descrita en [The Voynich Illustrations](https://www.voynich.nu/illustr.html). También hay una segunda aparición de `otaim` en f111v.3; `alam` aparece por separado en f111v.21.

## Interpretación

La distribución de `otaim` y `alam` entre un rótulo herbal y registros de la zona de recetas es **compatible** con vocabulario que reaparece al hablar de plantas o ingredientes. Es una conexión pertinente para examinar la propuesta de f65r y no depende de relacionarla con las páginas astronómicas.

La observación no identifica **oak/roble**. El corpus no permite distinguir esa planta de otro ingrediente, de un término gramatical o de una forma de cierre de registro. Además, `dam` aparece muchas veces y asignarle «of the» exigiría comprobar esa glosa en el conjunto de contextos, no solo en f65r. La distribución se conoce después de examinar la propuesta externa; es exploratoria, sin nulo comparable ni anotación botánica independiente.

## Decisión y prueba que faltaría

Se registra una **pista de transferencia léxica** entre f65r y el material herbal/recetario. No se admite «emergence of the oak» como desciframiento ni como ancla validada.

La evaluación útil siguiente debe congelar primero todas las correspondencias gráficas, variantes y excepciones usando únicamente los folios lingüísticos que la propuesta declara como base. Después debe aplicarlas sin cambios a las recurrencias de `otaim`, `dam` y `alam`, conservando todas las alternativas de segmentación, y compararlas con palabras control de longitud, frecuencia y terminación similares. La selección de f65r y la exposición previa a sus recurrencias deben declararse; estos datos no constituyen un holdout ciego. Una lectura de «roble» requeriría además identificación independiente de la planta y validación filológica de las formas germánicas propuestas.

## Autoauditoría

- **Selección:** propuesta externa y términos ya eran visibles; no es prueba ciega.
- **Conciencia del objetivo:** no se optimizaron reglas ni métricas; la coincidencia temática se reporta como compatibilidad, no como verificación.
- **Alcance:** se reutiliza una concordancia archivada; no se vuelve a ejecutar el parser ni se certifica la conformidad completa de IVTFF.
- **Conclusión negativa:** no se refuta la lectura del roble; se bloquea su admisión como significado establecido.
- **Límite de independencia:** las dos transcripciones son ediciones del mismo manuscrito. La correspondencia entre etiquetas y secciones es descriptiva; no sustituye anotación independiente de referentes.
- **Acciones omitidas:** no se hizo reproducción completa de la clave del sitio, estudio botánico, evaluación por un filólogo ni prueba estadística de enriquecimiento.

