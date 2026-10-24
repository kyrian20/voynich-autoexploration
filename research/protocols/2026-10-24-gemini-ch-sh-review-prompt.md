# Paquete de revisión metodológica externa — ch/sh (sin corpus)

**Estado:** PROPOSED / NO ENVIADO. Versión 1.0, 2026-10-24.
**Uso:** contenido público y limitado para futura revisión por Gemini; no es evidencia experimental.

## Solicitud reproducible para un revisor externo

Eres un revisor crítico independiente. No intentes traducir el manuscrito Voynich ni atribuir fonemas o significados a EVA. Responde en español. No asumas acceso a datos brutos.

Contexto resumido:
- En un subconjunto IVTFF $Q=T, el porcentaje de vocal inmediatamente posterior a los dígrafos EVA ch/sh difiere aproximadamente +5,52 puntos porcentuales (ZL3b) y +5,88 puntos (IT2a), según los informes del proyecto. Son estimaciones históricas pendientes de auditoría independiente del parser.
- Un control de carácter inmediatamente anterior muestra diferencias aproximadamente +7,41 y +8,16 puntos; sus intervalos bootstrap por folio incluyen cero. Esto cuestiona la interpretación direccional.
- Las dos transcripciones corresponden al mismo manuscrito, no son muestras independientes.
- Se desconoce si las asociaciones son efectos de plantillas, composición de tokens, posición o alguna propiedad más específica.

Entrega un objeto JSON con exactamente estas claves:
- `limitations`: lista de al menos cinco advertencias sobre qué no puede inferirse.
- `competing_hypotheses`: lista de al menos tres objetos con `name`, `prediction` y `falsifier`. Incluye explícitamente la hipótesis de plantillas de tokens.
- `proposed_design`: objeto con `unit_of_analysis`, `sampling_frame`, `strata`, `holdout`, `test_statistic`, `negative_controls`, `parser_validation`, `multiple_testing` y `stopping_rule`.
- `pre_registration`: objeto con `primary_outcome`, `decision_rule` y `failure_conditions`.
- `required_inputs`: lista de insumos sin los cuales NO debe ejecutarse el experimento.
- `unresolved_questions`: lista de preguntas abiertas.

Requisitos:
1. Formula un contraste estadístico que distinga efecto posterior de efecto anterior sin reutilizar folios de prueba para elegir parámetros.
2. Incluye un control que conserve longitud, posición de dígrafo y composición de sección.
3. Exige parser IVTFF independiente, verificación de casos de borde y trazabilidad de filtros.
4. Explica qué hacer con folios con soporte insuficiente y cómo informar sensibilidad.
5. Señala explícitamente que un resultado positivo no demostraría idioma, cifrado ni traducción.
6. Si faltan datos para fijar umbrales cuantitativos, devuelve `needs_data` en la regla de decisión; no inventes umbrales ni valores p.
7. No cites artículos inexistentes. No inventes resultados de experimentos.

## Validación humana posterior

La salida debe guardarse como propuesta no verificada con nombre de modelo, versión, fecha y hash de la solicitud; una revisión humana verificará cada campo y la viabilidad de los controles. Ningún resultado generado puede modificar directamente `state/committed_claims.md`, `state/findings.md` o la numeración EXP.

**Este archivo no es una autorización para ejecutar una llamada API ni compartir corpus.**
