# Intento de lectura de una línea elegida sin buscar un significado favorable

23-10-2026. Resultado: **BLOCKED para traducción semántica**. Se han ejecutado selección, cotejo de transcripciones, concordancias y una proyección fonética parcial preexistente. No se ha recuperado una frase española justificable. No es un experimento confirmatorio ni se asigna un nuevo EXP.

## Selección y documento

Script: `scripts/attempt_random_line_reading.py`. Semilla elegida por el analista 20261023; generador Python Random, selección uniforme entre los 3.885 registros P0 del archivo ZL3b, orden original. Índice cero 1036: **f44r.6,+P0**. No es selección uniforme entre frases, folios o todas las líneas del manuscrito. Se conserva el resultado pese a contener signos difíciles.

Original ZL3b:

`dshor.y,tchol.shy.o.@190;cheekchy.qotchy.otchy.dar`

Lectura IT2a:

`dshor.ytchol.shy.o.ocheeky.qotchy.otchy.dar`

Los puntos son separaciones de la transcripción; la coma de ZL3b es espacio dudoso. `@190;` es una representación de signo extendido: no se elimina ni se sustituye silenciosamente. ZL3a coincide aquí con ZL3b y no aporta un testigo independiente. La vista uniendo la coma da ocho unidades en ambas ediciones, pero no resuelve el grupo discrepante.

Se consultó el manifiesto Yale 2002046 y se inspeccionó la imagen de 44r, ID 1006160: https://collections.library.yale.edu/iiif/2/1006160/full/full/0/default.jpg . Se observan una planta y tres bloques de texto. La línea seleccionada está en el bloque central. La imagen no establece por sí sola la identidad botánica, el idioma ni el significado de sus palabras. No se adjudica definitivamente el signo extendido.

## Intento concreto y resultado

1. **Hipótesis de contexto:** podría ser parte de una descripción de planta, preparación o indicación; esas posibilidades no permiten elegir una frase. El dibujo no autoriza traducir «raíz», «hervir» o «agua».
2. **Posible relación formal:** `qotchy` y `otchy` difieren por `q` inicial en EVA. Se puede explorar un elemento añadido o una familia de formas, pero no inferir prefijo, flexión o significado. La segmentación EVA tampoco certifica unidades fonéticas.
3. **Concordancias:** bajo P0 y la proyección completa con espacios dudosos unidos, ZL3b contiene `qotchy` 62 veces en 47 folios, `otchy` 40/34 y `dar` 240/113. La pareja contigua `qotchy otchy` solo aparece en esta línea en ZL3b, ZL3a e IT2a. Son recuentos descriptivos y no una prueba de asociación o significado. Las frecuencias y contextos varían con la edición/política y se publican completos.
4. **Reglas previas sin ajustarlas a esta línea:** se aplicó el subconjunto operativo de correspondencias aproximadas de Bax conservado en `scripts/audit_partial_sound_rule_feasibility.py`, sin completar sonidos desconocidos. Fuente del autor: https://stephenbax.net/wp-content/uploads/2014/01/Voynich-a-provisional-partial-decoding-BAX.pdf , apéndice 1, pp. 56–57. Este subconjunto deja sin asignar varios caracteres de `ytchol`, `qotchy` y `otchy`. Incluso las formas cubiertas ofrecen sonidos propuestos ambiguos, no palabras de idioma establecido. No es una implementación completa ni una refutación del trabajo de Bax.

**Lectura máxima justificable:** una secuencia de formas gráficas, con una pareja de apariencia relacionada al final; significado sin determinar. No hay base para proponer siquiera una palabra española como traducción de esta línea. Una frase de herbolario sería una invención contextual, no una hipótesis derivada de una clave.

## Qué permitiría avanzar

Resolver la discrepancia gráfica ayudaría a fijar la entrada, pero no bastaría para traducirla. Haría falta una correspondencia signo/valor o palabra/significado apoyada fuera de esta línea, un idioma/modelo especificado y una regla que produzca lecturas coherentes en otros lugares sin cambios oportunistas. La pareja única ofrece poco material para validar una regla propia. No se propone reajustar tablas hasta producir una frase convincente.

## Reproducción y autoauditoría

`python scripts/attempt_random_line_reading.py` emite el resultado JSON con selección, hashes de los tres corpus, ambas políticas de espacios, frecuencias, concordancias y proyecciones parciales. No modifica corpus ni salidas previas. Python 3.12.14, biblioteca estándar y lectores versionados del repositorio. Las fuentes/transcripciones son alternativas del mismo objeto; no se suman como réplicas.

**Conciencia del objetivo:** la petición es intentar traducir; no se eligió la línea por afinidad con una hipótesis y no se ajustaron equivalencias para lograr una frase. Semilla elegida por el analista y selección solo P0 declaradas.

**Implementación:** se preservan espacios dudosos, signos extendidos y cuerpos originales; las proyecciones usan alternativas primarias y ligaduras expandidas del lector heredado, no conformidad paleográfica completa. El subconjunto fonético es incompleto: su fracaso no permite descartar un idioma o la propuesta completa de su autor.

**Extrapolación:** una línea, dos ediciones estrechamente relacionadas y un subconjunto de reglas propuestas. No se concluye imposibilidad de traducción en general.

**Alcance negativo:** no hay traducción justificada bajo estos recursos. No se infiere ausencia de significado ni se modifican afirmaciones públicas.

**Controles:** la comprobación principal es conservación de entrada y aplicación de reglas previas sin completarlas; no existe control semántico positivo porque no hay texto plano conocido. Esta carencia bloquea cualquier afirmación de traducción. Los recuentos no se convierten en significación ni equivalencias. No se actualizan findings.md, failed_approaches.md o committed_claims.md.
