# Contraste externo de investigación Voynich — 2026-10-19

## Alcance
Primera auditoría de estudios públicos y repositorios computacionales externos. Esto es un mapa comparativo inicial, no una revisión sistemática exhaustiva ni una evaluación por pares. No se ha encontrado evidencia verificable de que un superordenador haya producido una lectura aceptada del manuscrito. Los resultados publicados en repositorios personales/preprints se tratan como hipótesis hasta que sus pruebas, corpus, código y controles puedan reproducirse.

## Estudios y líneas relevantes

### 1. Christophe Parisel (2026), distinción Currier A/B
- Preprint: https://arxiv.org/abs/2604.25979
- Afirma que una mezcla Beta-Binomial selecciona dos grupos y predice etiquetas Currier retenidas con 89% de exactitud; propone un cambio de estado por folio relacionado con vocales tras ch/sh.
- Relación con nuestros experimentos: compatible con tratar A/B como estratos estadísticos reales. No confirma una traducción. Nuestro trabajo ha usado A/B como etiquetas descriptivas y detectado que los efectos posicionales de daiin cambian mucho entre A y B. Siguiente contraste útil: replicar sus features con split por folio y comprobar si el supuesto interruptor ch/sh predice fuera de muestra después de controlar transcripción, mano y sección.

### 2. Christophe Parisel (2026), restricciones posicionales/direccionales
- Preprint: https://arxiv.org/abs/2604.19762
- Reporta asimetrías de dirección a nivel de grafemas/palabras y compara generadores de ranuras y rejilla Cardano.
- Relación: nuestro exp607 mide información predictiva de bigramas en folios reservados. El resultado exp607 en ZL3b e IT2a es una mejora de 0.26679 y 0.34096 bits por transición frente al unigram; sin embargo, al barajar el orden de entrenamiento todavía se conservan ganancias de 0.21088 y 0.28598. La ganancia adicional real menos control es solo 0.05591 y 0.05498 bits/token. Esto sugiere que parte grande de la mejora viene de inventarios de línea y suavizado, no solo del orden auténtico. Hace falta un test con permutaciones por línea/folio y baseline mejor controlado antes de concluir que reproduce las restricciones de Parisel.

### 3. Naibbe cipher (publicado en Cryptologia/Taylor & Francis, 2025)
- Artículo: https://www.tandfonline.com/doi/full/10.1080/01611194.2025.2566408
- Propone un cifrado homofónico verbose históricamente plausible que genera textos con varias estadísticas parecidas al Voynich y puede descifrarse cuando se conoce la clave.
- Relación: coincide con nuestra conclusión prudente de que compatibilidad estadística no equivale a descifrado. Nuestros resultados anteriores sobre generadores híbridos (19/19 métricas en una batería definida) no prueban el mecanismo histórico. Prueba prioritaria: comparar Naibbe, control sin texto plano y nuestros modelos bajo exactamente las mismas métricas retenidas y controles de longitud/folios.

### 4. Amancio et al. (2013), física estadística/redes de palabras
- Artículo/preprint: https://arxiv.org/abs/1303.0347
- Encontró que algunas propiedades estadísticas del texto son más compatibles con lenguaje natural que con texto aleatorio.
- Relación: respalda analizar estructura no aleatoria, pero no identifica lengua ni significado. No contradice los resultados posteriores que muestran que generadores estructurados también pueden reproducir muchas regularidades.

### 5. Bowern & Lindemann (2021), revisión lingüística
- Revisión: https://www.annualreviews.org/content/journals/10.1146/annurev-linguistics-011619-030613
- Resume argumentos a favor de regularidades de tipo lingüístico y el estado de los intentos de caracterizar la lengua subyacente.
- Relación: marco académico de fondo; las regularidades estadísticas son necesarias para investigar, pero no sustituyen una traducción reproducible.

### 6. Seeton, Voynich-public (snapshot público 2026)
- Repositorio: https://github.com/seeton/Voynich-public
- Usa predicción fuera de muestra, controles de bifolio/cuaderno, modelos generativos y auditoría de transcripciones. Reporta que el primer token no funciona como selector determinista del resto de la línea; encuentra evidencia de estructura a escalas mayores, pero distingue cuidadosamente esas observaciones de significado.
- Relación: muy buen candidato para comparación metodológica con nuestros exp602/603/607. Su énfasis en separar cara de página, folio, bifolio y cuaderno señala un control importante para fortalecer nuestros splits, que hasta ahora se basan principalmente en folios.

### 7. Frank Masciopinto, voynich-manuscript-decipher (2026)
- Repositorio: https://github.com/Frank-Masciopinto/voynich-manuscript-decipher
- Toolkit reproducible para entropía, morfología, manos, Currier, cifrados y generadores; declara que no tiene traducción.
- Su resumen reporta entropía condicional de caracteres inusualmente baja y dependencia posicional de palabras. También muestra que las métricas Zipf/Heaps por sí solas no discriminan lenguaje, cifrado y generador.
- Relación: coincide con nuestro enfoque de controles negativos y advierte contra tomar una sola estadística como desciframiento. Contraste prioritario: usar sus controles de idioma y generadores como batería externa común.

### 8. Pantani, Voynich Codex Project
- Repositorio: https://github.com/Pantani/voynich
- Propone un sistema de operadores/plantillas y matriz de terminaciones, y afirma que un generador local sin contenido reproduce 13 de 14 firmas estadísticas.
- Relación: coincide con que un generador estructurado puede reproducir estadísticas sin demostrar que el manuscrito carezca de significado. Sus afirmaciones deben evaluarse con controles independientes y particiones retenidas; no adoptamos sus probabilidades subjetivas como estimaciones verificadas.

### 9. Gropper (2026), “What the Voynich Manuscript Says: Nothing”
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7367158
- Preprint que sostiene que el manuscrito no tiene contenido semántico y presenta análisis de entropía condicional y dependencia entre líneas.
- Estado: resultado fuerte y controvertido en un manuscrito/preprint reciente; no se debe tratar como consenso. Su afirmación de independencia entre líneas merece replicación con transcripciones, anotaciones y controles por escriba/folio antes de usarla como premisa.

### 10. Dominik (2026), morfología con validación cruzada
- Zenodo: https://zenodo.org/records/23113674
- Preprint reciente que afirma recuperar morfología superficial con particiones retenidas y replicación en transcripciones alternas, pero deja explícita la diferencia entre morfología y significado léxico.
- Relación: el estándar de validación cruzada es pertinente. Conviene inspeccionar su código/datos y verificar si sus conjuntos alternativos son verdaderamente independientes; distintas transcripciones del mismo manuscrito solo prueban robustez editorial, no replicación independiente.

### 11. Repositorios contemporáneos adicionales
- Pantani y Seeton son especialmente útiles por los controles de generadores y predicción fuera de muestra.
- Repositorio de Epilectrik: https://github.com/epilectrik/voynich — revisión de septiembre de 2026 con generadores rivales y limitaciones explícitas.
- Herramienta de investigación estadística de Temkin: https://github.com/mjtemkin/VoynichStats
- La biblioteca Beinecke de Yale confirma que el texto sigue sin descifrar aceptado: https://beinecke.library.yale.edu/beinecke/collections/beinecke-cipher-voynich-manuscript

## Resultado provisional del contraste
1. No aparece una traducción públicamente aceptada y validada de forma independiente.
2. Existe convergencia amplia en que el texto no es una secuencia aleatoria simple y tiene estructura posicional/morfológica.
3. El gran desacuerdo es interpretativo: lenguaje/cifrado frente a sistema construido o generador estructurado. La capacidad de reproducir estadísticas no resuelve por sí sola esa disputa.
4. Nuestro efecto inicial de daiin al comienzo de líneas Currier B/P0 es un patrón de posición reproducido en varias transcripciones, pero no independiente entre ellas y no semántico. El exp607 muestra que la predicción bigrama mejora respecto a unigramas, aunque gran parte de esa mejora también aparece en el control barajado.
5. No se ha encontrado evidencia verificable de que el uso de un superordenador haya logrado descifrado aceptado. La mayoría de los trabajos revisados se basan en análisis estadístico, aprendizaje automático o ejecución reproducible en ordenadores convencionales; la escala de cómputo no reemplaza una clave, controles y validación independiente.

## Próximos tests concretos
- Replicar el interruptor ch/sh de Parisel en ZL3b e IT2a, split por folio y con controles de mano/sección.
- Comparar nuestro exp607 con modelos/baselines de Seeton y Masciopinto en las mismas particiones, añadiendo baseline de inventario por línea y permutación que preserve longitud.
- Implementar comparación común Naibbe vs generador sin texto plano vs modelos híbridos en un conjunto de métricas fijado antes de mirar el test.
- Revisar la afirmación de dependencia entre líneas de Gropper con un test independiente y sensibilidad a etiquetas/limpieza.
- No usar otra transcripción del mismo testigo como si fuera un corpus independiente.

## Fuentes clave
- https://arxiv.org/abs/2604.25979
- https://arxiv.org/abs/2604.19762
- https://www.tandfonline.com/doi/full/10.1080/01611194.2025.2566408
- https://arxiv.org/abs/1303.0347
- https://www.annualreviews.org/content/journals/10.1146/annurev-linguistics-011619-030613
- https://github.com/seeton/Voynich-public
- https://github.com/Frank-Masciopinto/voynich-manuscript-decipher
- https://github.com/Pantani/voynich
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7367158
- https://zenodo.org/records/23113674
- https://beinecke.library.yale.edu/beinecke/collections/beinecke-cipher-voynich-manuscript
