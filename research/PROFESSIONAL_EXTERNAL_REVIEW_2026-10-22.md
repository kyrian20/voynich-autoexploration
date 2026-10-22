# Incorporación de investigación profesional externa — 22 octubre 2026

## Resultado de esta revisión

Se incorporan ocho referencias académicas o vinculadas a publicaciones académicas, con niveles de acceso explícitos, y se fijan versiones de cuatro repositorios de autores. Esta revisión bibliográfica no ejecuta ni reproduce sus experimentos. No añade una traducción, una asignación fonética ni una nueva conclusión validada sobre el manuscrito.

La selección combina publicaciones que favorecen interpretaciones lingüísticas con mecanismos artificiales rivales. La publicación en una revista aporta revisión editorial, pero no convierte una interpretación en hecho demostrado. Un DOI de arXiv o Zenodo tampoco implica revisión por pares.

El [registro de fuentes y artefactos](external/2026-10-22-professional-sources/registry.json) contiene autores, versiones, localizadores metodológicos, límites de acceso, commits y hashes Git de archivos. Las notas anteriores se conservan; este documento las complementa y precisa.

## Lecturas y conocimiento transferible

### 1. Reddy y Knight — alcance de las métricas

[Artículo de congreso, ACL/LaTeCH 2011, PDF](https://aclanthology.org/W11-1511.pdf). Consultadas las secciones de corpus, predicción y estructura de página.

Su análisis principal se limita a Currier B, especialmente las secciones balneológica y de estrellas. Distingue predicción de caracteres, palabras completas y caracteres a través de límites de palabra. La evaluación de caracteres usa tipos de palabra reservados: su unidad de partición y su métrica no son las de nuestro EXP-607.

**Aplicación:** no describir nuestra mejora en pérdida predictiva como reproducción de su porcentaje de aciertos. Preparar una tabla de correspondencia de corpus, alfabeto, unidad, partición y estimador antes de comparar. No repetir una prueba genérica de orden: ya existe EXP-607.

### 2. Bowern y Lindemann — revisión lingüística

[Annual Review of Linguistics 7, 2021](https://doi.org/10.1146/annurev-linguistics-011619-030613). Verificados publicación, autores y resumen; el texto completo no se recuperó en esta sesión.

Los autores argumentan a favor de un texto lingüístico y revisan qué inferencias estructurales pueden hacerse sin leerlo. Aquí registramos esa interpretación como posición de los autores, no como consenso probado ni como validación de nuestras hipótesis.

**Aplicación:** usar la revisión para organizar preguntas sobre escritura, morfología y estructura; no elegir un idioma de origen apoyándose solamente en semejanzas estadísticas. La auditoría completa de sus argumentos queda pendiente del texto íntegro.

### 3. Lindemann y Bowern — entropía y corpus de comparación

[Versión de autores, arXiv:2010.14697v2](https://arxiv.org/abs/2010.14697v2). Consultados resumen y árbol del repositorio de corpus; el PDF superó el límite de recuperación.

Describen comparaciones con 294 muestras de lenguas y dieciocho textos históricos, y estudian cómo escritura y composición de glifos afectan a la entropía. Los autores informan que las transformaciones ensayadas no eliminan la peculiar predictibilidad del Voynich.

**Aplicación:** una comparación con pocos idiomas no justifica identificar una familia lingüística. Revisar primero longitud de muestra, alfabeto, espacios y límites de palabra. El repositorio académico es [chirila/Voynich-public](https://github.com/chirila/Voynich-public), distinto de seeton/Voynich-public citado anteriormente.

### 4. Montemurro y Zanette — concentración de palabras y orden del corpus

[PLOS ONE, 2013, texto completo](https://doi.org/10.1371/journal.pone.0066344). Consultados planteamiento, distribución de palabras y métodos.

Estudian concentración de palabras y similitud de sus perfiles de frecuencia. Un detalle relevante: agrupan folios dispersos con sus secciones y presentan resultados sobre ese texto reordenado; no trabajan únicamente con la encuadernación actual. Su interpretación semántica no proporciona equivalencias entre palabras y significados.

**Aplicación:** cualquier reproducción debe conservar separadas la secuencia actual y la reorganización publicada, con mapas de folios explícitos. La concentración también debe contrastarse con diferencias de sección y mano. No puede usarse como validación directa de un análisis nuestro con otro orden o tokenizador.

### 5. Sterneck, Polish y Bowern — agrupaciones, manos y secciones

[Texto de autores, 2021](https://arxiv.org/pdf/2107.02858). Consultadas las secciones de datos, alineación de metadatos y comparación de modelos.

Comparan agrupaciones textuales obtenidas mediante LDA, LSA y NMF con ilustraciones, clases Currier y atribuciones de mano. Reconocen que la similitud puede reflejar significado, codificación o una combinación; sus metadatos tampoco son independientes entre sí.

**Aplicación:** no llamar «tema semántico» a una agrupación sin controlar esas relaciones. En una futura evaluación predictiva, aprender vocabulario, IDF y reducción dimensional solo con entrenamiento. Un análisis descriptivo de todo el corpus debe identificarse como tal. Código localizado y fijado, todavía sin ejecutar.

### 6. Greshko — Naibbe como rival con texto legible

[Publicación identificada, Cryptologia 2025](https://doi.org/10.1080/01611194.2025.2566408); [repositorio del autor](https://github.com/greshko/naibbe-cipher). El editor devolvió 403; se leyeron README y código de naibbe_v2.py.

El autor presenta un cifrado homofónico verboso que transforma textos conocidos en salidas que imitan diversas propiedades del manuscrito. Es una construcción rival, no una lectura recuperada del Voynich.

**Aplicación:** cotejar la versión, tablas y corpus antes de reutilizar resultados históricos. El código depende de un CSV relativo y del generador aleatorio global; importarlo no equivale a una ejecución controlada. El árbol actual incluye el ejemplo requerido por EXP-170. Esto habilita estudiar su recuperación, pero no identifica la versión histórica ausente.

### 7. Timm y Schinner — rival sin recuperación de texto plano

[Publicación identificada, Cryptologia 44(1)](https://doi.org/10.1080/01611194.2019.1596999); [materiales de los autores](https://github.com/TorstenTimm/SelfCitationTextgenerator). Consultados metadatos editoriales y repositorio; el artículo devolvió 403 y no se ejecutó el generador.

El proyecto propone generación por autocitación y publica un programa y materiales auxiliares. Es una alternativa que merece comparación, sin aceptar su explicación histórica por la existencia del programa.

**Aplicación:** enfrentar mecanismos con y sin texto plano bajo una batería común; documentar qué características copia cada uno del Voynich. No generalizar el fallo de una implementación a todos los generadores. Antes de ejecutar el JAR, revisar el código fuente, parámetros y dependencias.

### 8. Parisel — la versión revisada limita la señal direccional

[Prepublicación arXiv:2604.19762v2, 16 junio 2026](https://arxiv.org/abs/2604.19762v2). Consultadas §§3.4, 4.2 y 5.1 y la evaluación conjunta de generadores.

La revisión informa que un remuestreo de Markov reproduce la combinación de señales direccionales. Por tanto, esa combinación no diagnostica por sí sola un mecanismo generativo específico. También compara generadores contra perfiles conjuntos calibrados por clase Currier; sus fallos no excluyen mecanismos fuera de los ensayados.

**Aplicación:** incorporar este límite al contexto del informe externo del 19 de octubre. Una mejora predictiva nuestra no prueba una dirección de lectura ni reproduce ese diagnóstico. Las tolerancias aprendidas del Voynich deben declararse como calibración, no como predicciones independientes.

## Integración con el trabajo existente

Estas son decisiones de método de nuestro proyecto, inspiradas por las lecturas; no resultados nuevos de los artículos.

| Línea existente | Aportación aplicable | Acción y límite |
|---|---|---|
| EXP-607 y sensibilidad de lectores del 22 de octubre | Diferenciar caracteres, palabras, pérdida y aciertos; controlar tipo de texto | Mantener la comprobación P0 frente a mezcla de loci ya protocolizada. No crear otra prueba de orden equivalente. |
| EXP-001/002/003/114 y otras entropías históricas | Comparadores y reglas de escritura importan | Revisar elegibilidad y normalización antes de resumir sus cifras. Un contraste etiquetas/cuerpo no identifica significado. |
| EXP-170 y EXP-178 | Naibbe es un rival explícito con parámetros y fuentes | Registrar la procedencia disponible; conservar el bloqueo de reproducción histórica hasta reconstruir versión, tablas e inputs. |
| Agrupaciones y propuesta de orden de bifolios | Sección, mano, Currier y orden pueden explicar similitudes | Mantener el protocolo específico de singuliones; no confundirlo con predicción de tokens ni validar una secuencia por su máximo seleccionado. |
| EXP-330 y bibliografía direccional | Las métricas direccionales no son intercambiables | El gradiente de clases de inicio de EXP-330 no es la asimetría de perplejidad de Parisel. No presentarlos como reproducción mutua. |

Las rutas se consultan mediante [el registro inequívoco](EXPERIMENT_PATH_REGISTRY.json). Esta tabla identifica solapamientos y evita asignar nuevos IDs; no certifica retrospectivamente los experimentos históricos.

## Qué se ha adquirido materialmente

- Ocho fichas con el nivel de lectura realmente alcanzado, sin fingir acceso a los textos bloqueados.
- Cuatro commits externos fijados, y archivos de interés identificados por hash de blob Git.
- Una precisión sobre la dirección y otra sobre el orden del corpus que deben acompañar las futuras interpretaciones.
- La localización verificable de naibbe_v2.py, su tabla y input/examples/divina_commedia.txt en el mismo commit externo.
- Diferenciación entre el corpus académico chirila y el proyecto independiente seeton.

Los hashes del registro son SHA-1 de objetos Git, no SHA-256 del contenido. La consulta del árbol verifica ubicación, tamaño y objeto; salvo el código Naibbe leído, no supone inspección íntegra de cada archivo. No se han copiado corpus externos ni ejecutado esos programas. Dos repositorios no muestran un archivo de licencia en su árbol completo: su acceso público no concede permiso automático para redistribuirlos.

## Orden de aplicación

1. Completar el diagnóstico ya previsto de EXP-607 sin mezclar etiquetas y párrafos; no sustituirlo por otra exploración de la misma señal.
2. Revisar los materiales Naibbe fijados y el historial de EXP-170 para determinar si puede recuperarse su entorno exacto. Si no, cualquier nueva ejecución será una comparación nueva, no una reproducción del resultado antiguo.
3. Preparar una sola batería común de comparación entre texto conocido, cifrado y generación sin texto plano, después de comprobar solapamiento con los experimentos existentes. Fijar métricas y criterios antes de ver nuevas salidas.
4. Dejar la posible reordenación física como estudio separado con sus propios controles; no modificar el orden de referencia del corpus.

Un conjunto de prueba ya inspeccionado no vuelve a ser «intacto» por cambiar de script. Las futuras decisiones deben declarar exposición previa al corpus; la réplica en otra transcripción es sensibilidad sobre el mismo manuscrito, no un testigo independiente.

## Acceso incompleto y novedades pendientes

Los artículos con DOI 10.1080/01611194.2026.2697318 y 10.1080/01611194.2026.2693462 aparecieron en la búsqueda reciente, pero sus textos devolvieron 403. Se guardan únicamente como pistas para lectura futura; no importamos sus conclusiones. La fuente de singuliones ya registrada el 21 de octubre volvió a bloquear la recuperación mediante Anubis: no se revalidan aquí sus cifras ni fechas.

La selección no pretende ser una revisión sistemática exhaustiva de toda la bibliografía mundial. Se buscó en dos motores y se priorizaron editoriales, ACL, manuscritos de autores y sus repositorios. Las noticias y las propuestas de traducción sin validación no se utilizaron como evidencia científica.

## Control de incorporación

No hubo simulación nueva ni estimación de efectos en este bloque, por lo que no se promocionan resultados a findings.md, failed_approaches.md o committed_claims.md. Tampoco se modificaron cifras históricas, código científico ni workflows. La fiabilidad incorporada consiste en procedencia, límites y diseños utilizables; la reproducción independiente sigue siendo una tarea distinta.

