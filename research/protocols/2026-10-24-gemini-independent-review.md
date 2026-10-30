# Protocolo de revisión independiente Gemini — 24-10-2026

**Estado: PROPOSED.** Documento de diseño; no se ha ejecutado un análisis de corpus, no se ha solicitado revisión a Gemini ni se asigna número EXP.

## Objetivo
Aprovechar la conexión Gemini validada en la prueba manual #13 sin convertir una respuesta de un modelo generativo en evidencia científica. La conexión API y el flujo de revisión científica son capacidades distintas.

## Pregunta prioritaria
¿La diferencia observada entre `ch` y `sh` en el carácter siguiente aporta información específica más allá de plantillas de token y del contexto anterior?

### Evidencia que motiva la revisión
- `state/current_state.md` registra el contraste de vocal siguiente en dos transcripciones, con pruebas de sensibilidad.
- El control de carácter anterior de exp619 presenta un contraste de magnitud similar o mayor; por ello no se ha demostrado especificidad de dirección ni desciframiento.
- exp620 deja pendiente una auditoría independiente del parser y casos límite IVTFF.
- ZL3b e IT2a son dos transcripciones del mismo manuscrito, no dos manuscritos independientes.

## Encargo de revisión (sin corpus ni credenciales)
Entregar a Gemini únicamente esta pregunta, las advertencias anteriores y definiciones metodológicas públicas; pedir:
1. Al menos tres explicaciones rivales, incluyendo efecto de plantilla, posición y sesgo de selección.
2. Una prueba falsable que distinga efecto posterior de efecto anterior, con unidades de remuestreo por folio y partición de validación por folio.
3. Controles adversariales (permutaciones condicionadas por longitud, posición, sección y transcripción) y una auditoría independiente del parser.
4. Criterios de rechazo y resultados que invalidarían la hipótesis, escritos **antes** de ejecutar el experimento.
5. Una lista explícita de datos adicionales imprescindibles y afirmaciones que no pueden inferirse.

## Reglas de integración
- No enviar claves API, corpus completos, material no publicado ni identificadores personales a un modelo externo por defecto.
- Un humano revisa y aprueba cualquier paquete de datos antes de enviarlo.
- Guardar solicitud, modelo exacto, versión, fecha, respuesta íntegra, límites, y coste cuando esté disponible; sanear secretos.
- Tratar las propuestas de Gemini como hipótesis **PROPOSED**, nunca como hallazgos confirmados.
- No asignar nuevos números EXP mientras la numeración esté congelada; consultar registro e historial para evitar duplicados.
- Antes de ejecutar, fijar corpus, hashes, parser, controles, semillas, métricas y criterios; separar entrenamiento y prueba por folio.
- Reproducir localmente con scripts versionados y aplicar `skills/audit_experiment.md` antes de actualizar estado científico.
- No modificar `state/committed_claims.md`; discrepancias a `state/open_questions.md`.
- Registrar tanto resultados negativos como fallos operativos. Nunca proclamar traducción o significado semántico a partir de patrones distribucionales.

## Puertas de avance
**P0:** revisión humana de este protocolo. **P1:** herramienta Gemini de revisión aislada, opt-in, sin corpus y con pruebas offline de seguridad. **P2:** una revisión externa real de texto metodológico autorizado. **P3:** diseño preregistrado y auditoría del parser. **P4:** ejecución reproducible con controles. **P5:** síntesis con límites y revisión independiente.

**Situación actual:** solo el enlace técnico Gemini está verificado; P0–P5 siguen pendientes. Este documento no modifica la investigación ni lanza trabajo en segundo plano.
