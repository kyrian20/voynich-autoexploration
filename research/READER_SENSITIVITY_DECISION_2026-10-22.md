# Sensibilidad del lector: resultados y decisión — 22-10-2026

Estado: **auditoría descriptiva ejecutada; integración CI pendiente de verificar para el nuevo commit**. No se asigna ningún EXP. Se conserva el código de los análisis históricos, sus fuentes y sus resultados.

## Qué se ha comparado

Se evaluaron exhaustivamente 128 combinaciones de siete decisiones de normalización en cada una de las tres transcripciones. La máscara 0 reproduce, registro por registro, el filtro ASCII usado por EXP-590 con cobertura amplia. La máscara 127 reproduce la vista candidata existente. Todos los controles de equivalencia pasaron.

Las siete decisiones son ligaduras, alternativas, códigos extendidos, ilegibles, whitespace, anotaciones inline y caracteres no alfabéticos. Las combinaciones son normalizaciones de diagnóstico, incluidas políticas históricas destructivas; no son 128 implementaciones normativas certificadas ni réplicas independientes. Las comas se separan en la rejilla; unirlas se evalúa aparte.

Protocolo fijado antes de estas ejecuciones: [PROTOCOL.md](maintenance/2026-10-22-token-sensitivity/PROTOCOL.md). Es una planificación de sensibilidad exploratoria, no una preinscripción confirmatoria retrospectiva.

## El patrón posicional se conserva dentro de la rejilla

Ratio = inicios observados / suma por línea de apariciones de daiin divididas por longitud de la línea. Solo P0, clase indicada por $L y al menos dos tokens. Se comparan también los IDs comunes a las 128 vistas: el filtro no cambió qué líneas eran elegibles en este corpus.

| Fuente | Líneas B/P0 comunes | Rango del ratio B/P0 en 128 vistas | Rango A/P0 | Inicios B/P0 |
|---|---:|---:|---:|---:|
| ZL3b | 2325 | 2.7930–2.8436 | 0.8352–0.8428 | 88 |
| ZL3a | 2325 | 2.7832–2.8442 | 0.8349–0.8425 | 88 |
| IT2a | 2324 | 2.6035–2.6035 | 0.7826–0.7830 | 84 |

En las normalizaciones evaluadas, B conserva exceso inicial y A conserva déficit bajo esta referencia de intercambiabilidad. Esto es robustez descriptiva dentro de esta rejilla; no identifica una función gramatical, idioma o significado. No se han calculado p-valores nuevos para la rejilla.

## Origen de las diferencias del recuento exacto

| Fuente | Filtro histórico | Candidata | Cambio neto | Ligaduras | Alternativas | Ilegibles |
|---|---:|---:|---:|---:|---:|---:|
| ZL3b | 853 | 848 | -5 | -1 | -1 | -3 |
| ZL3a | 853 | 849 | -4 | -1 | 0 | -3 |
| IT2a | 865 | 863 | -2 | 0 | 0 | -2 |

Las contribuciones son valores de Shapley exactos sobre la rejilla y suman la diferencia de extremos. Son atribución de implementación dependiente de esta rejilla, no causas lingüísticas. Los otros factores tienen contribución neta cero al conteo exacto de esta palabra, lo cual no implica ausencia de cambios en tokenización o en otras estadísticas.

El total de inicios de daiin permanece en 161/161/157 en los extremos para ZL3b/ZL3a/IT2a. Se conservan en el JSON los cuerpos e IDs que cambian el conteo o algún indicador de posición.

## Sensibilidad de las comas, fuera de la rejilla

Con la candidata, unir comas reduce los daiin exactos de ZL3b 848→788 y ZL3a 849→790. El ratio B/P0 sigue por encima de 1: 2,7788 y 2,7688, respectivamente. IT2a no cambia en esta comparación. No se debe sustituir un conteo por otro sin declarar la definición de espacio.

## Intervalo del análisis histórico de folios: reproducción y cambio de lector

Ruta inequívoca: `experiments/exp_601_folio_clustered_confirmation/` (no el otro directorio EXP-601 de sensibilidad pareada). Primero se reprodujo su intervalo guardado con el lector nativo; luego se remuestrearon los mismos 81 folios y 2.325 líneas con ambas vistas. Se conservaron 20.000 réplicas y semilla 60120261019.

| Vista | Observados | Esperados | Ratio | Intervalo percentil del 95 % por folios |
|---|---:|---:|---:|---:|
| Nativa EXP-601 | 88 | 31.279224 | 2.813369 | [2.115596; 3.593170] |
| Candidata completa | 88 | 31.344931 | 2.807471 | [2.111431; 3.585361] |

La diferencia estimada candidata−nativa es -0.005897; intervalo pareado [-0.021960; 0.007783]. Se registra como sensibilidad del mismo análisis y de los mismos folios, no confirmación independiente. El intervalo nuevo queda explícito; no se ha trasladado el antiguo al estimador modificado.

## Predicción: sensibilidad del modelo ya existente EXP-607

Se reprodujeron los resúmenes históricos del modelo sin modificar alpha=0,1, mezcla=0,5, split por hash de folio ni semilla del control 6072026. Después se intersectaron los IDs elegibles de ambos lectores. La candidata conservadora retiene solo palabras completas `[a-z]{2,}`; no rescata fragmentos de palabras con signos ilegibles. Esta vista es distinta de la candidata completa usada en el bootstrap.

| Fuente | Líneas comunes | Train / test | Ganancia real−control, nativa | Ganancia real−control, candidata conservadora |
|---|---:|---:|---:|---:|
| ZL3b | 3730 | 3133 / 597 | 0.054683 | 0.051615 |
| IT2a | 3734 | 3137 / 597 | 0.054708 | 0.052927 |

Unidades de ganancia: bits por transición, calculados dentro de cada vista frente a su control fijo. La ventaja conserva el signo positivo, pero vocabularios y eventos cambian: no se comparan pérdidas absolutas entre lectores como un mismo estimador. Un único barajado es diagnóstico, no una distribución nula ni una prueba de significación. No se eligieron semillas favorables.

La intersección excluyó nueve líneas nativas en ZL3b y una en IT2a. Se conserva el universo original de páginas básicas y la separación por folios, que es disjunta. No se añadieron páginas desplegables ni se ajustó el modelo usando el test.

**Aclaración de alcance encontrada:** el comentario antiguo del cargador decía excluir labels, pero su patrón no imponía ese filtro. Los datos nativos contienen 48 loci L* en ZL3b y 49 en IT2a, además de texto circular/radial y otras clases. Se corrigió el comentario, sin cambiar código ejecutable ni resultados. Este test no debe resumirse como predicción exclusiva de párrafos P0.

## Autoauditoría — los cinco controles

1. **Conocimiento del objetivo:** daiin fue elegido históricamente; estos resultados son exploratorios y condicionales a esa elección. La rejilla completa evita escoger el lector que produzca la cifra favorable. El modelo EXP-607 y sus parámetros se conservaron.
2. **Pérdida de características:** los modos históricos destructivos son controles de sensibilidad; la capa bruta conserva los caracteres. La candidata conservadora del modelo excluye palabras enteras no ASCII, lo que se declara y no se generaliza a todo el manuscrito.
3. **Extrapolación:** los rangos se refieren solo a esta rejilla, estas fuentes y estos perfiles. Ni formato completo ni significado lingüístico quedan validados.
4. **Resultados negativos:** las diferencias de conteo y los casos excluidos se conservan. Ningún resultado se transforma en afirmación de imposibilidad, ni se sobrescriben originales.
5. **Comportamiento del control:** se esperaba reproducir exactamente las ganancias históricas de los controles EXP-607, +0,210881 bits en ZL3b y +0,285981 en IT2a, porque se mantienen código, datos y split; las comprobaciones las reprodujeron. El control barajado también mejora frente al unigram, así que la ganancia frente a unigram por sí sola no se atribuye al orden. La comparación relevante aquí es real frente al control y permanece limitada a un barajado fijo. En el nulo posicional, se espera m/n por construcción y se comprobó mediante enumeración de un ejemplo pequeño, independientemente del acumulador.

## Decisión

- El patrón inicial B/P0 y la dirección del contraste A/B se mantienen como observaciones descriptivas resistentes a las decisiones ensayadas. No se elevan a desciframiento o a función gramatical.
- No hace falta repetir todos los experimentos ni descartar automáticamente la investigación anterior. Los análisis de tokens concretos, extremos, longitudes o vocabularios deben declarar lector y universo.
- La sensibilidad de EXP-601 y EXP-607 se ha ejecutado en rutas separadas; los p-valores y resultados históricos permanecen asociados a sus implementaciones originales.
- Antes de usar el lector para una conclusión confirmatoria nueva siguen pendientes la adjudicación documental/alphabet-specific independiente y un protocolo distinto que no reinterprete el test histórico como nuevo.

## Código y evidencia

- `scripts/audit_token_policy_sensitivity.py`: rejilla exhaustiva, equivalencia de extremos, atribución y puente nativo.
- `scripts/audit_exp601_paired_reader_bootstrap.py`: bootstrap pareado con reproducción histórica obligatoria.
- `scripts/audit_exp607_reader_sensitivity.py`: reproducción y comparación del modelo en líneas comunes.
- `scripts/check_audit_snapshot.py`: estructura y enteros exactos; floats finitos con tolerancia 1e-12.
- [Rejilla y ejemplos](maintenance/2026-10-22-token-sensitivity/results.json).
- [Bootstrap pareado](maintenance/2026-10-22-token-sensitivity/exp601-paired-bootstrap.json).
- [Modelo y exclusiones](maintenance/2026-10-22-token-sensitivity/exp607-results.json).

Las auditorías no asignan IDs EXP, no alteran las transcripciones y no escriben resultados históricos. Las tres fuentes son versiones/transcripciones del mismo manuscrito.
