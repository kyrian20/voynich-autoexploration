# Revisión de investigación externa sobre el Manuscrito Voynich

Fecha de revisión: 2026-10-20
Estado: revisión bibliográfica inicial; no equivale a reproducción independiente.

## Objetivo

Importar métodos, datos y preguntas contrastables de proyectos externos sin importar automáticamente sus conclusiones. El manuscrito continúa sin una descodificación académicamente aceptada. Cada afirmación externa debe etiquetarse como dato reproducido, resultado reportado por sus autores, hipótesis o especulación.

## Fuentes externas prioritarias

### 1. Voynich Studies — paquete de replicación y registro de afirmaciones
URL: https://voynich.site/data-and-code?lang=en
URL publicaciones: https://voynich.site/publications?lang=en
Qué aporta según su documentación pública:
- Paquete de replicación con scripts, corpus normalizados, registro de afirmaciones y semillas fijas.
- Declara pruebas de mecanismo, análisis de etiquetas y controles negativos, incluidos resultados nulos.
- Declara haber reproducido e interpretado de nuevo Sig-D/direccionalidad y cerrado algunas líneas con resultados nulos.
Cómo usarlo: descargar el paquete publicado, identificar scripts y corpus exactos, ejecutar sin cambios, comparar hashes, versiones y métricas. Tratar las afirmaciones sobre el mecanismo como hipótesis hasta reproducirlas fuera del proyecto.

### 2. Michael Temkin — VoynichStats
URL: https://github.com/mjtemkin/VoynichStats
Qué aporta según el repositorio:
- Scripts para diferencias Currier A/B, duplicación inmediata de palabras, controles por sección, orden de clases y comparación con corpus de otras lenguas.
- Afirma que la duplicación inmediata y ciertas asimetrías de orden sobreviven a varios controles.
Cómo usarlo: reproducir primero los resultados descriptivos y los controles; comprobar sensibilidad a transcripción, definición de token, secciones, manos y frecuencia. La interpretación como gramática no queda demostrada solo por una asimetría estadística.

### 3. Pantani — Voynich Codex Project
URL: https://github.com/Pantani/voynich
Qué aporta según el repositorio:
- Toolkit reproducible con lector IVTFF, análisis de formas, coocurrencias, posiciones y revisión visual humana.
- Publica estadísticas de asociación entre prefijos/sufijos y posiciones, y declara una batería amplia de tests.
Cómo usarlo: auditar las definiciones de los componentes morfológicos y la selección de candidatos; repetir con particiones de entrenamiento/prueba y controles de palabras artificiales. No adoptar etiquetas como «operador» o «núcleo» sin validación independiente.

### 4. Frank Masciopinto — Voynich Manuscript Decipher
URL: https://github.com/Frank-Masciopinto/voynich-manuscript-decipher/
Qué aporta según el repositorio:
- Estadística de caracteres, frecuencias, entropía, posiciones, Currier A/B y comparación con generadores/cifrados rivales.
- Hipótesis preregistradas y controles de mecanismos, sin afirmar una traducción final.
Cómo usarlo: utilizarlo como segunda implementación independiente para verificar nuestros contadores y comprobar si las conclusiones dependen del parser o de la transliteración.

### 5. The Voynich Project
URL: https://thevoynichproject.org/
Qué aporta según la página:
- Pruebas falsables con modelos nulos, criterios de éxito definidos antes de ejecutar y publicación de hipótesis descartadas.
Cómo usarlo: importar el protocolo experimental y las pruebas de controles, no sus interpretaciones sin revisar los datos y el código de cada afirmación.

### 6. Repositorio epilectrik/voynich — revisión estratégica de 2026
URL: https://github.com/epilectrik/voynich
Qué aporta según la portada:
- Registro numerado de restricciones, niveles de evidencia, procedencia y revisión estratégica contra controles externos y generadores rivales.
- Reconoce explícitamente que algunos resultados anteriores no superaron controles.
Cómo usarlo: como modelo de trazabilidad y revisión adversarial; comparar las reglas de evidencia con las nuestras y aprender de las hipótesis que se abandonaron.

### 7. Fuentes históricas y corpus
Currier (1976): https://www.voynich.com/currier1.htm
Zandbergen–Landini y datos: https://www.voynich.nu/data/
Qué aportan: base histórica de la distinción Currier A/B y transliteraciones para reproducir análisis. No asumir que las clases Currier equivalen directamente a lenguas naturales distintas; son categorías textuales basadas en diferencias estadísticas.

## Prioridades para nuestra investigación

1. Auditar EXP-593 antes de usarlo como evidencia:
   - verificar el parser y los recuentos de líneas/tokens frente a un parser IVTFF conocido;
   - comprobar cómo se extraen los metadatos Currier A/B de las cabeceras;
   - revisar el cálculo de la corrección por máximo estadístico: el estadístico observado y el estadístico nulo deben ser comparables;
   - fijar de antemano si se cuentan ocurrencias o líneas que contienen la forma;
   - comparar ZL3b con al menos otra transcripción independiente.
2. Replicar dos hallazgos externos con más controles:
   - duplicación inmediata de palabras (Temkin);
   - asociaciones entre forma/posición y componentes morfológicos (Pantani / Voynich Codex Project).
3. Crear controles negativos:
   - permutar dentro de línea, entre líneas del mismo folio y entre folios, aclarando qué estructura conserva cada nulo;
   - generar textos artificiales que preserven frecuencias de palabras y longitud de línea;
   - separar folios de entrenamiento y prueba, evitando seleccionar candidatos con todo el corpus.
4. Mantener resultados negativos. Ningún experimento recibe estatus de «validado» solo por un p-valor; registrar tamaño de efecto, intervalos, corrección por múltiples pruebas, sensibilidad y replicación independiente.

## Registro de evidencia

- Revisión de páginas públicas realizada el 2026-10-20.
- En esta fase se ha revisado la documentación de los proyectos, no se han ejecutado aún todos sus scripts.
- Las cifras y conclusiones de cada proyecto son afirmaciones de sus autores hasta que nuestra reproducción las confirme.
- No se ha incorporado ninguna traducción propuesta como hecho.

## Siguiente paso técnico

Crear un inventario por repositorio: URL, commit/tag, versión de corpus, licencia, comandos de ejecución, dependencias, scripts principales, resultados esperados, estado de reproducción y diferencias frente a nuestro pipeline. Ejecutar primero el test de humo más barato de cada proyecto, sin copiar datos o código incompatible con su licencia.
