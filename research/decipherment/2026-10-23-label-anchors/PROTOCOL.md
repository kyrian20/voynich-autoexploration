# Anclas semánticas en etiquetas — protocolo prospectivo

Fecha: 2026-10-23. Estado: **PROPOSED**. Sin nuevo identificador EXP. No se han ejecutado pruebas ni obtenido coincidencias.

## Pregunta y límites

¿Las formas EVA presentes en etiquetas, y especialmente las que no aparecen en texto corrido según el inventario histórico F641, contienen correspondencias reproducibles con referentes botánicos o astronómicos identificables de manera **independiente** del texto? El recuento histórico de 547 tipos exclusivos es una hipótesis de inventario que debe reconstruirse antes de emplearlo: no se toma como muestra verificada. Una coincidencia ortográfica no constituye traducción. Los nombres propuestos para imágenes no se aceptarán como verdad de referencia si su identificación es incierta.

## Etapa 0: verificación de insumos (bloqueante)

1. **Localización resuelta:** el registro `research/EXPERIMENT_PATH_REGISTRY.json` identifica `GH:experiments/exp_580_label_corpus_grammar` (alias exp_580); están disponibles `script.py` y `result.md`. Reconstruir sus tipos y frecuencias, con SHA-256 de ZL3b e IT2a. El informe histórico afirma 1.036 tipos de etiqueta, 489 compartidos con el cuerpo y 547 exclusivos; estas cifras siguen **pendientes de reproducción independiente**. Si no se reproduce el inventario, **BLOCKED**, sin pasar a la búsqueda de nombres.
2. Separar etiquetas de cuerpo por identificadores de locus y metadatos comprobados, sin deducir sección o Currier a partir de la grafía. Documentar etiquetas ambiguas, fragmentos, variantes y exclusiones. Conservar los identificadores de folio y localización.
3. Establecer qué etiquetas tienen un referente visual catalogado de forma independiente, con fuente, folio y grado de certeza. Excluir de la evaluación confirmatoria las imágenes ambiguas. No inferir referentes a partir de supuestas traducciones.
4. Las dos transcripciones describen el mismo manuscrito: tratarlas como **sensibilidad de lectura**, no como replicaciones independientes. No completar etiquetas ausentes en una transcripción mediante la otra sin registrarlo.

## Hipótesis preregistradas

- **H0 (nula):** el sistema de puntuación no relaciona las etiquetas con sus referentes independientes mejor que un emparejamiento aleatorio entre etiquetas y referentes de la misma sección, longitud comparable y folios distintos, con las mismas restricciones de disponibilidad.
- **H1 (alternativa):** una regla de correspondencia congelada, entrenada sin acceso a los referentes del grupo de prueba, mejora la identificación del referente correcto frente a los controles. Se evalúan por separado botánica y astronomía; no se mezclan para seleccionar el mejor resultado.

## Datos externos y riesgo de circularidad

Congelar una tabla de referentes, nombres históricos, variantes, idioma, fecha y fuente primaria o edición crítica, con licencia y hashes. Distinguir nombre moderno, latino histórico y árabe transliterado; no aceptar transliteraciones inventadas para mejorar una coincidencia. Ningún catálogo derivado de propuestas de desciframiento Voynich puede servir como verdad independiente. Las etiquetas sin referente fiable solo sirven para exploración, no para el test de recuperación de nombres.

## División, algoritmo y controles

- Usar la partición **v2 por hoja física** publicada en `research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json`: 68 hojas entrenamiento, 16 desarrollo y 18 prueba. Ambas caras, todas las etiquetas de la misma hoja y las transcripciones alternativas deben permanecer juntas. Esta partición evita nueva fuga accidental, pero **no es históricamente ciega** porque ya se han inspeccionado folios del manuscrito.
- Antes de acceder a los referentes de prueba, registrar commit SHA, lista de nombres, tokenizador, transliteración, función de similitud, umbrales, política de empates y de candidatos ausentes, y procedimiento de normalización. Ajustar solo con entrenamiento; seleccionar exclusivamente con desarrollo.
- Baselines: azar estratificado, frecuencia mayoritaria por sección y similitud ortográfica ingenua sin correspondencia aprendida. Controles negativos: permutar referentes entre hojas manteniendo sección y disponibilidad, y etiquetas sintéticas con distribución de longitudes y caracteres conservada cuando sea factible. Control positivo: conjunto sintético de nombres con transformaciones predefinidas y una verdad conocida; si falla, declarar instrumento no apto.
- Unidad primaria: **hoja física**, no ocurrencia individual; evitar que múltiples etiquetas de una hoja inflen la evidencia. Reportar por separado cobertura de referentes fiables, top-1, top-k fijado previamente, ganancia sobre baseline, intervalos remuestreados por hoja y distribución de controles. Reportar todas las secciones, incluidas las negativas. Los tests de permutación deben respetar el emparejamiento y la estructura de folios; corregir multiplicidad por secciones, variantes y métricas.
- **Puerta antes de evaluar:** al menos cinco hojas de prueba con referentes independientes y al menos veinte etiquetas evaluables en la sección examinada; en caso contrario, **BLOCKED / no concluyente** y no modificar umbrales después de ver los datos. Si la correspondencia ortográfica no puede predefinirse sin mirar el test, restringir el trabajo a un inventario exploratorio y no afirmar contraste confirmatorio.
- Criterio de apoyo **fijado ahora**: mejora positiva frente a *todos* los baselines con intervalo de incertidumbre del efecto que excluya cero, y contraste de permutación ajustado p < 0,05; además, recuperación de referentes distintos en al menos tres hojas de prueba. De lo contrario, **NEGATIVE** si hay potencia y ejecución adecuadas, o **BLOCKED/no concluyente** si falla una puerta. No interpretar p < 0,05 como validación semántica.

## Falsación y decisiones

Si las asociaciones desaparecen al estratificar por sección/longitud, al cambiar de transcripción, al eliminar candidatos modernos o al evitar referencias ambiguas, se rechaza la interpretación robusta bajo este protocolo. Si la mejora solo existe frente al azar pero no frente a similitud ingenua, no se apoya una clave lingüística. Si hay señal, se conservarán **predicciones por etiqueta y folio**, falsos positivos y controles antes de proponer un estudio externo nuevo; no se anunciará traducción ni identidad de plantas a partir de correlaciones.

## Registro, reproducibilidad y auditoría

Publicar hashes, versiones, licencia, código, fixtures del lector IVTFF, semilla, comandos, entorno, JSON de resultados y logs. Auditar según `skills/audit_experiment.md` (conciencia del objetivo, implementación que destruye señales, extrapolación, sobreinterpretación de negativos y controles). Conservar todo resultado negativo y los artefactos originales. No editar `state/committed_claims.md`, `state/findings.md` ni el corpus. Este archivo fija **diseño**, no certifica ejecución ni valor semántico.

## Trazabilidad recuperada — 23-10-2026

- Fuente primaria de los recuentos históricos: `experiments/exp_580_label_corpus_grammar/result.md`, sección 5, «Vocabulary Overlap»; código: `experiments/exp_580_label_corpus_grammar/script.py`.
- El script usa la transcripción ZL3b y selecciona etiquetas mediante `^[&@*+=~][LR][^P]`; cuerpo mediante `^[&@*+=~]P`. Su lector elimina marcadores y toma la primera alternativa de las lecturas ambiguas; por ello el recuento no es todavía una medida independiente de la política de lectura.
- El informe documenta 1.087 líneas de etiquetas y 1.442 tokens, 1.036 tipos de etiqueta, 7.030 tipos del cuerpo, 489 compartidos y 547 exclusivos. Son **valores archivados, no recalculados en esta rama**.
- Se debe cotejar la clasificación de secciones del script: incluye reglas basadas en locus y rangos de folio, y una condición `Lz` duplicada. No extrapolar la clasificación histórica a referentes visuales seguros.
- La ruta genérica `experiments/exp_580/` era incorrecta; no se ha perdido el experimento. El registro canónico de rutas evita repetir esta falsa incidencia.

## Verificación automatizada del recuento histórico (2026-10-23)

GitHub Actions [Voynich Check #711](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40023875649) ha completado satisfactoriamente los pasos «Reproducir recuentos archivados de etiquetas EXP-580» y «Conservar trazabilidad de recuentos EXP-580». El replay compara las seis cifras publicadas, comprueba la identidad aritmética 1036 − 489 = 547 y registra hashes de script/corpus. **Alcance:** reproducción automatizada del script original, no verificación independiente de clasificación IVTFF, identidad semántica ni replicación en IT2a. La ejecución completa #711 aún estaba en curso al documentar este resultado. El bloqueo de etapa 0 sobre auditoría independiente de etiquetas y loci permanece vigente.

