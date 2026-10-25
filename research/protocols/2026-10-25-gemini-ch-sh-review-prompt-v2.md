# Paquete de revisión metodológica externa — ch/sh, versión 2 (sin corpus)

**Estado:** PROPOSED / aún no ejecutado en esta versión. Fecha: 2026-10-25.
**Procedencia:** reemplaza para futuras solicitudes el paquete v1 `2026-10-24-gemini-ch-sh-review-prompt.md`, que se conserva sin cambios para verificar su hash y la respuesta histórica. Un resultado solo se considera enviado si existe recibo y run de esa versión.
**Uso:** revisión externa no vinculante. No se envían transcripciones, tokens, imágenes ni datos privados.

## Solicitud al revisor externo

Actúa como revisor metodológico crítico e independiente. Responde en español y en JSON. No intentes traducir el manuscrito Voynich ni asignar significados, fonemas o equivalencias a EVA. No tienes acceso a los datos crudos ni a los folios reservados.

### Glosario obligatorio del formato IVTFF

- `$Q` identifica el **cuaderno (quire)**. Por tanto `$Q=T` significa **cuaderno T**, **NO** una categoría de calidad de transcripción, fiabilidad, idioma ni una sección científica validada.
- `$L=A/B` indica la clasificación **Currier A/B**; `$I` indica tipo de ilustración. No intercambies `$Q`, `$L` y `$I`.
- Los identificadores de folio deben obtenerse y comprobarse contra las cabeceras originales y la edición IVTFF; no inventes una partición por folios ni interpretes una fila como folio independiente.
- ZL3b e IT2a son **ediciones del mismo manuscrito**, no muestras biológicas ni documentales independientes. No combines sus p-valores como si fueran replicaciones independientes.
- El acuerdo entre dos lectores no certifica conformidad IVTFF; las reglas para alternativas, ligaduras, espacios inciertos, comentarios y continuaciones siguen requiriendo adjudicación.

### Contexto histórico, no validado

- Para un subconjunto descrito como `$Q=T`, los informes históricos estiman diferencias de vocal inmediatamente posterior a `ch/sh` de aproximadamente +5,52 puntos porcentuales (ZL3b) y +5,88 (IT2a). No reinterpretar el criterio `$Q=T`.
- Un control del carácter anterior presenta diferencias de aproximadamente +7,41 y +8,16 puntos; sus intervalos bootstrap por folio incluyen cero. La especificidad direccional no está demostrada.
- Puede haber confusión por plantillas, longitud, posición del dígrafo, composición de folios o edición; tampoco hay desciframiento ni una inferencia lingüística validada.

### Condiciones para un diseño futuro

1. Consulta el **manifiesto de separación train/development/test ya existente** y exige su ruta, versión, hash y unidades físicas antes de proponer o ejecutar un contraste. No inventes otro reparto ni elijas parámetros sobre test.
2. Si no se aportan las listas de folios, el mapa verificable de `$Q` y `$L`, la edición exacta y los hashes, declara `needs_data` en `pre_registration.decision_rule`; deja el contraste en PROPOSED.
3. Propón un contraste primario falsable entre contexto posterior y anterior; fija controles negativos que preserven longitud de token, posición del dígrafo y composición de folio o sección **cuando esa composición pueda acreditarse**.
4. Requiere parser IVTFF independiente, fixtures de borde, criterios de inclusión/exclusión y adjudicación de discrepancias antes de probar el contraste.
5. Trata los folios como unidades de independencia para partición e incertidumbre; informa soporte insuficiente, sensibilidad por folio y multiplicidad de todas las variantes exploradas.
6. No inventes valores p, tamaños muestrales, umbrales, citas bibliográficas, folios ni resultados. Un contraste positivo no demostraría idioma, cifrado ni traducción.

### Formato de salida estricto

Devuelve un único objeto JSON con exactamente estas seis claves:

- `limitations`: lista de al menos cinco advertencias sobre inferencias no permitidas.
- `competing_hypotheses`: lista de al menos tres objetos con exactamente `name`, `prediction`, `falsifier`; incluye la hipótesis de plantillas de tokens.
- `proposed_design`: objeto con exactamente `unit_of_analysis`, `sampling_frame`, `strata`, `holdout`, `test_statistic`, `negative_controls`, `parser_validation`, `multiple_testing`, `stopping_rule`.
- `pre_registration`: objeto con exactamente `primary_outcome`, `decision_rule`, `failure_conditions`.
- `required_inputs`: lista de insumos ausentes, incluidos manifiesto, hashes y verificación de metadatos.
- `unresolved_questions`: lista de preguntas pendientes.

Las entradas de texto deben ser cadenas no vacías o listas de cadenas no vacías donde el esquema lo permita. No uses campos adicionales. Si faltan datos, conserva la incertidumbre en lugar de formular una decisión numérica.

## Control posterior

La salida es una propuesta **no verificada**, incluso si supera la validación de esquema. Debe archivarse con el modelo, run, hash de este prompt y hash de respuesta, y someterse a revisión humana antes de cualquier experimento. Ninguna salida de Gemini puede editar `state/committed_claims.md`, `state/findings.md` ni asignar EXP. Este documento no autoriza por sí solo una llamada API.
