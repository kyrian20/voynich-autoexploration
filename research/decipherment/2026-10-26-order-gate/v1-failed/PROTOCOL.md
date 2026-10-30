# Selección de claves e idioma con puerta de orden

26-10-2026, Madrid. PROPOSED antes de ejecutar. Exploratorio, sin EXP nuevo ni evaluación Voynich. Extiende la calibración artificial de contenido conocido, no propone un cifrado histórico ni reclama novedad externa.

## Pregunta y alcance

¿Una búsqueda de clave/idioma con abstención y un filtro de orden rechaza barajados y una familia ausente, conservando recuperación exacta de dos positivos? ¿Un generador de pares de palabras muestra el límite del filtro como certificador semántico?

Entradas: inputs.json del bloque residual V2, SHA256 c069548868854c29d294efbc3da891a0f5cf7c62878786be78fa13ce5ba5225d. Solo César y Dante. Mantener grupos hash V2 train>=2/dev=1/test=0. Ningún texto Voynich se procesa. Familias, alfabeto ASCII a-z, reinicio de fase por línea y conjunto candidato de dos idiomas siguen conocidos. Se oculta al selector el idioma correcto, no al investigador; no hay cegamiento independiente.

Clave positiva: rotar cada token por (11+índice mod7) sobre ASCII; conservar diacríticos y límites de línea. Buscar todos los 624 candidatos (dos modelos de idioma train x periodos1..12 x offsets0..25) con pérdida de caracteres dev como en la calibración anterior. No usar claro dev/test para elegir. Publicar todos los costes en archivo comprimido determinista. Margen mínimo 1e-6 bits/carácter entre primero y segundo; empate/margen insuficiente -> NO_IDENTIFICABLE, sin forzar clave.

Puerta de orden, entrenada por idioma: vocabulario top2000 por frecuencia train con desempate léxico, resto UNK; unigramas de destinos alpha=.1; bigramas de palabras con suavizado tau20 y mezcla lambda elegida solo en dev de [0,.1,.25,.5,.75,1] minimizando pérdida, desempate menor lambda. No cruzar líneas. S = pérdida unigramas menos pérdida bigramas, bits/transición. Umbral por idioma = max(.01, máximo S de 16 barajados dev), semillas 2026102610..2026102625. Umbral y lambda quedan congelados antes de puntuar test. Un candidato se admite como ORDEN_DETECTADO solo si S_test>umbral, cobertura de destinos conocidos>=.5 y margen de clave suficiente. Es una puerta de orden local; jamás un validador semántico.

Primaria de recuperación: ambos positivos deben recuperar idioma, clave y 100% tokens reservados, además de superar puerta. Contraste de orden pareado sobre los mismos grupos: S_original menos media S de 16 barajados test, semillas 2026102710..2026102725; bootstrap por bloques fuente de 25 líneas, 2000 réplicas semilla2026102603, con modelos fijados. Publicar intervalo percentil95; no usarlo para ajustar lambda, umbral o clave. Un intervalo positivo sigue siendo exploratorio; no es prueba de significado.

Negativos de orden: 16 barajados por texto de dev/test antes de cifrar (semillas test anteriores y dev=semilla+10000), ejecutar de nuevo búsqueda completa de clave/idioma y la misma puerta. Son 32 desafíos relacionados, no estimación independiente de tasa poblacional. Puerta operativa: 0/32 admitidos; un fallo se conserva y bloquea afirmar rechazo completo, sin cambiar umbral.

Familia ausente: cifrar cada texto con periodo13/offset11, fuera de la búsqueda1..12, mismo resto de reglas. Ambos deberían abstenerse/rechazarse; no se afirma que todo código ausente se detecte. Publicar exactitud de cualquier candidato aun rechazado. Ambigüedad: frecuencias uniformes ASCII para ambos modelos -> todos los costes iguales; debe producir NO_IDENTIFICABLE sin elegir arbitrariamente. Es una prueba de implementación, no un corpus real ambiguo.

Adversario de mayor dificultad: generar dev y test con bigramas empíricos train, primera palabra unigramática y transiciones mezcla de empírico condicional/unigrama con factor n/(n+20), semilla2026102607 para dev y2026102608 para test; mantener cantidades/longitudes de líneas de cada partición, sin copiar sus palabras. Cifrar con periodo7/offset11, buscar clave/idioma y aplicar puerta. Esperamos que pueda superar un filtro de bigramas precisamente porque comparte su rasgo. Si se acepta, documentar contraejemplo al uso de la puerta como certificador de contenido; no declararlo texto sin toda semántica, pues conserva palabras y pares. No adaptar el filtro para rechazarlo en esta versión.

Archivar todas las salidas, costes de los624 candidatos por desafío, hashes y logs. Cinco controles previos adicionales: normalización de probabilidad, S de independencia exactamente0 al calibrar lambda0, abstención ante empate, permutación preserva inventario, normalización y vocabulario sin fuga. Comparar dos ejecuciones byte a byte. Sin p confirmatorios, ni generalización de 32 desafíos a todas las alternativas. No repetir variantes hasta lograr aceptación.

## Antecedentes y decisión de cierre

Consultados calibración de recuperación de26oct, residual V2, sensibilidad de cantidades y BC-2026-10-22 (acepta barajados). La KB histórica ~/voynich-kb no está disponible; cotejo local limitado, sin revisión bibliográfica exhaustiva. Sin nueva llamada ni revisión Gemini: su respuesta v2 archivada es antecedente crítico, no aval de este diseño. Se aplicará skills/audit_experiment.md.

Si recupera positivos/rechaza barajados pero admite Markov, conservar como filtro local y detener su uso como vía de validación semántica. El paso siguiente requeriría evidencia independiente de contenido; no más optimización del mismo filtro sobre estas evaluaciones. No se aplicará a Voynich por superar esta calibración.
