# Tres experimentos pendientes con mayor valor discriminante

Selección al 22-10-2026 sobre `b314925`, **no ejecutados ni numerados**. Son prioridades razonadas, no una estimación cuantitativa de potencia ni tres pruebas capaces de identificar por sí solas una lengua. El backlog de abril conserva entradas resueltas y objetivos locales de bajo N; su prioridad nominal no reemplaza el registro de octubre.

Se consultaron `research/EXPERIMENT_REGISTER.md`, `EXPERIMENT_PATH_REGISTRY.json`, `ARTIFACT_COLLISION_REGISTER.md`, el backlog, `state/working_position.md`, la adjudicación C001, `next_decisive_test_plan_2026-10-22.md`, la revisión profesional externa y el protocolo/resultado V2 de orden residual. Los siete IDs en colisión y el cotejo incompleto con Biblioteca impiden reservar nuevos números. Usar ruta/commit/hash para cada antecedente. No se afirma haber consultado una KB externa ausente ni haber comprobado dependencias de todos los experimentos históricos.

## 1. Batería común fuera de muestra: lenguaje conocido, cifrado y generadores sin plaintext

**Pendiente registrado:** `research/PROFESSIONAL_EXTERNAL_REVIEW_2026-10-22.md`, orden de aplicación 3, y adjudicación C001 (control Naibbe de idioma/segmentación). Prioridad máxima porque enfrenta directamente las tres familias con el mismo evaluador y corrige el principal límite de EXP-170.

**Diseño a congelar:** lenguas de identidad verificada (latín César e italiano Dante), sus versiones cifradas con reglas fijadas sin acceso a objetivos de evaluación, Naibbe y controles Timm/copia con y sin preservación de onset. Igualar tamaño y política de líneas; informar también una condición que conserve límites originales. Separar parámetros publicados, ajustes aprendidos solo en entrenamiento y ajustes target-aware. Elegir una métrica primaria conjunta antes de generar salidas —por ejemplo pérdida predictiva fuera de muestra de un vector de rasgos predefinido— y dejar am/y/self-succession/repetición como diagnósticos secundarios, con incertidumbre por folio y multiplicidad declarada. Exigir que el control positivo detecte estructura conocida antes de interpretar el Voynich.

**Qué separa:** si solo los modelos con plaintext conservan simultáneamente dependencias y posición en evaluación, se restringe el generador ensayado; si los generadores sin plaintext igualan la batería, los rasgos no identifican lenguaje. Un cifrado puede conservar señales lingüísticas: empate lenguaje/cifrado no distingue ambos. Cualquier modelo que iguale solo los rasgos usados para calibrarlo carece de validación independiente.

**Antiduplicación:** EXP-170/171/176 prueban mecanismos con métricas históricas; EXP-177/179/180/181 prueban cifrado/mezclas calibradas; EXP-314 y los controles EXP-574/575/584/585 ensayan especificidad de arquitecturas. No repetir una rejilla o un 19/19. La novedad necesaria es la comparación común, controles con plaintext cifrado y evaluación de rasgos no utilizados para ajustar. Antes de implementar, cotejar específicamente estos scripts y sus fuentes, no solo sus títulos.

**Dependencias / estado:** BLOQUEADO para Naibbe histórico: `data/derived/naibbe-cipher` y su ejemplo no existen en el checkout. No sustituirlos con el Dante disponible para fingir reproducción. Ya hay textos César/Dante y auditoría de identidad, pero falta fijar hashes de las vistas exactas, versión/tablas/licencia del cifrador y protocolo de generadores. No se recuperan en esta tarea. La comparación será un estudio nuevo si no se demuestra identidad histórica.

## 2. Dependencias más largas y unidades variables con controles cifrados calibrados

**Pendiente registrado:** última dirección de `research/analysis/2026-10-22-residual-order/REPORT.md`: unidades variables o memoria más larga. Se prioriza sobre otra búsqueda local de `daiin` porque pregunta si la débil ganancia de identidad de un token se debe a segmentación o a alcance de memoria.

**Diseño a congelar:** un único contraste primario entre un modelo de memoria limitada y otro de mayor contexto, con presupuesto de parámetros comparable y unidades aprendidas exclusivamente en entrenamiento. Elegir una longitud/contexto primaria antes de evaluar; las demás variantes son sensibilidad con corrección. Cortes por folio/sección, políticas de espacios y ligaduras fijas, controles negativos que preserven frecuencia/posición pero destruyan solo la dependencia a contrastar. Calibrar en César/Dante, cifrados homofónicos/verbosos conocidos y copia algorítmica con ventana conocida. Evaluar ganancia en bits por transición y bootstrap por folio; no usar el inventario verdadero de la línea futura como predictor desplegable.

**Qué separa:** ganancia sostenida más allá de la ventana de copia y robusta a segmentación debilitaría ese generador de ventana finita; recuperación solo al agrupar unidades sería compatible con cifrado verboso o segmentación distinta. Ausencia de ganancia solo limita los modelos si los controles cifrados positivos la recuperan. Lenguaje natural también puede tener dependencias locales débiles; no se convierte ausencia en prueba de texto sin significado.

**Antiduplicación:** EXP-607, GH-602-HELDOUT-PREDICTION, los dos LIB-EXP-623 y el V2 residual ya existen. EXP-175 midió MI por lag (con artefactos retractados), no esta comparación predictiva calibrada. El V2 ya detectó señal conocida con memoria de un token y encontró mejora Voynich pequeña/incierta; no volver a describir esa pregunta como pendiente. La nueva prueba requiere mayor alcance o unidades variables y controles cifrados, sin reciclar su test inspeccionado como intacto.

**Dependencias / estado:** PREPARACIÓN PENDIENTE. Están los scripts y entradas V2, corpus y capas IVTFF; faltan reglas exactas de unidades/contexto, evaluación sin exposición usada para seleccionar modelo y controles cifrados fijados. Verificar paquetes/versiones, manifiesto de fuentes y extracción antes de correr. ZL3b/IT2a son sensibilidades del mismo manuscrito, no muestras independientes.

## 3. Asimetría predictiva directa/inversa frente a controles de lenguaje y mecanismos

**Pendiente registrado:** revisión externa profesional, fila EXP-330/bibliografía direccional y ficha `parisel-2026-direction-v2` del registro de fuentes externas. La réplica exacta de la métrica de perplejidad no figura cerrada allí. Tiene mayor valor que otra tabla de onsets porque examina una propiedad distinta con controles mecanísticos.

**Diseño a congelar:** reconstruir primero la definición publicada de dirección, unidades y pérdida; distinguir invertir caracteres, tokens y orden de líneas. Entrenar modelos forward/reverse simétricos con idéntica información y presupuesto. Fijar log-loss forward menos reverse por folio como métrica primaria y el signo antes de evaluar. Emparejar lenguaje conocido, cifrado conocido del mismo plaintext, copia causal y plantilla posicional; conservar límites físicos y comparar controles que los destruyan explícitamente. No seleccionar la dirección o el nivel que maximice el efecto.

**Qué separa:** una firma reproducida por copia causal pero no por los controles lingüísticos/cifrados limitaría esos controles; la firma preservada a través de cifrados apoyaría compatibilidad con una fuente lingüística, sin demostrarla. Si una plantilla posicional reproduce la asimetría, la dirección por sí sola no identifica sintaxis ni sentido de escritura. Un resultado nulo solo es interpretable si los positivos funcionan y las dos direcciones tienen capacidad equivalente.

**Antiduplicación:** `experiments/exp_330_bigram_directionality` cuenta transiciones de clases según un gradiente posicional; no estima asimetría de perplejidad. Revisar también el V2 residual y EXP-607 para reutilizar evaluadores sin presentar nuevas métricas como una réplica exacta. La clasificación Currier de Parisel propuesta en el plan EXP-625 es otra pregunta; alta exactitud A/B no discrimina origen semántico.

**Dependencias / estado:** BLOQUEADO para llamarlo réplica exacta hasta reconstruir inequívocamente método, código/versión, orientación, fuentes y split del artículo. La ficha bibliográfica no sustituye esos materiales. El corpus local permite preparar fixtures, pero no ejecutar ni proclamar una réplica sin resolverlos. Requiere además los controles cifrados calibrados del punto 1.

## Puerta común antes de cualquier ejecución futura

Comprobar de nuevo master, registro y antecedentes por ruta; cerrar protocolo/métrica/split/multiplicidad; congelar fuentes/licencias/hashes y entorno; verificar parser y `$L` sin inferencia por edy; auditar calibración, destrucción de rasgos y controles según `skills/audit_experiment.md`; conservar todas las salidas y errores. Si un control falla, bloquear la interpretación y documentarlo. No iniciar automáticamente ninguna de estas pruebas desde esta PR.
