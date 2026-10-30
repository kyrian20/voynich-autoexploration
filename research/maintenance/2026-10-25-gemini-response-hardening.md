# Gemini: rechazo controlado de respuestas mal formadas

25-10-2026. Corrección operativa, sin llamada API nueva ni resultado científico nuevo.

Se reprodujeron AttributeError con envelope de tipo lista o candidato nulo, y TypeError con texto numérico. Algunas formas no quedaban capturadas por el manejador anterior; por ejemplo, una lista como envelope podía terminar sin recibo.

extract_text ahora comprueba objeto raíz, lista de candidatos, candidato, contenido, lista de partes y tipos de texto. La metadata de fallback debe ser objeto y supportedGenerationMethods una lista. Las formas inválidas se rechazan; no se intenta traducirlas o convertir números a texto.

19 pruebas específicas aprobadas, incluidos seis tipos de envelope inválido y dos de metadata incompatible. Se comprueba recibo BLOCKED, ausencia de secretos y ausencia de generación adicional para respuestas mal formadas. No se altera el máximo de dos generaciones ante fallos transitorios.

Se pasó la respuesta real archivada del intento 4 por el extractor corregido: hash de texto igual al recibo y esquema válido. No se volvió a llamar a Google para repetir una comprobación cubierta por la respuesta archivada.

Cambio agrupado en un único commit. La CI configurada ya incluye los archivos de pruebas afectados. La suite completa y conformidad IVTFF quedan fuera del alcance. La corrección no convierte la revisión Gemini en validación científica; se conservan las advertencias de research/external-reviews/2026-10-25-gemini-v2/REVIEW.md.
