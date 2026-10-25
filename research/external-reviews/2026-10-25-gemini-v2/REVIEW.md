# Gemini v2: conexión comprobada y revisión crítica
25-10-2026. Conexión verificada en una ejecución; contenido científico PROPOSED_UNVERIFIED.

## Evidencia de funcionamiento
Run 40235310859, intento 4, job 121298599069, success.
https://github.com/kyrian20/voynich-autoexploration/actions/runs/40235310859/job/121298599069
Checkout realmente ejecutado: eb3086b0d3fb5d33611a012a386b8063265e6b17 (según log). El SHA del run original no equivale al checkout de master del reintento.
Modelo solicitado y efectivo: gemini-3.8-flash. Una generación, sin usar alternativa.
La respuesta llegó antes del límite de 180 s; no se puede atribuir este éxito a la alternativa añadida ni afirmar reparación del servicio de Google.
Se incorporó además fallback acotado para futuras fallas transitorias, probado solo sin red: tras timeout/502/503/504, GET de metadata de gemini-3.5-flash-lite y como máximo una generación adicional de 90 s si es compatible. --no-fallback lo desactiva. No se usa ante 403 ni para buscar otra respuesta científica.
17 tests específicos sin red aprobados; CI configurada para incluir diagnóstico y fallback. No se certifica suite o CI global ni disponibilidad futura del proveedor.

## Procedencia y verificaciones
Artefacto 12615605679, ZIP SHA256 b744da7e16798a16da6a1629c0f301bb48f686c8de5f703bbcb30c23424c4691 verificado al descargar.
Se conservan receipt.json, review-untrusted.json y api-response-untrusted.json junto a esta nota.
Se verificaron:
- SHA256 del prompt local = receipt.prompt_sha256.
- SHA256 del texto extraído del envelope = receipt.response_sha256.
- JSON del texto extraído = review-untrusted.json.
- Validación de esquema local: cero errores.
El hash api_envelope_sha256 del recibo refiere a los bytes originales de API antes del reformateo; no se afirma igualdad con los bytes del envelope pretty-printed archivado.
No se enviaron corpus ni imágenes: solo el prompt público metodológico.

## Adjudicación de contenido
La respuesta sigue siendo una propuesta de otra IA, no revisión académica independiente ni evidencia del manuscrito.
Se aceptan como precauciones: exigir hashes, mantener incertidumbre needs_data, no combinar ediciones como muestras independientes y no asignar significado por correlaciones.
Se rechazan o mantienen pendientes:
1. Gemini vuelve a asociar $L=A/B con manos de copista en competing_hypotheses y strata. Es incorrecto: $L es Currier; las manos requieren metadatos/fuentes distintos. No reutilizar ese fragmento.
2. Persistencia tras condicionar por una «plantilla completa» no es falsador válido sin definir plantilla, soporte e intercambiabilidad. Si condiciona toda la identidad, puede no quedar variación.
3. El contexto anterior no es un negativo nulo garantizado; la asimetría es la pregunta. No asumir de antemano que el anterior deba ser cero.
4. Intervalo que incluye cero significa falta de apoyo/precisión bajo el método, no equivalencia ni refutación general.
5. «Diferencia estandarizada» no fija un estadístico ejecutable; FDR o FWER tampoco elige una familia ni corrección concreta. El diseño no está listo para ejecutarse.
6. El contraste posterior/anterior ya tiene EXP-622/623 exploratorios en el repositorio con efectos inciertos y distinto signo entre ediciones. No presentarlo como idea nueva ni repetirlo sin diseño que resuelva limitaciones.
7. Mismo folio físico no garantiza independencia entre hojas de un bifolio o contexto compartido; no tomar «unidad independiente» como hecho demostrado.

## Cierre operativo
Se puede cerrar la comprobación de conexión JUA-7 con alcance de esta respuesta válida.
La selección de un nuevo experimento y adjudicación científica siguen abiertas; no cambiar findings.md, committed_claims.md o hipótesis por aprobación de esquema.
No quedan tareas del usuario para obtener esta respuesta. GitHub conserva el resultado y Linear registra el cierre.
